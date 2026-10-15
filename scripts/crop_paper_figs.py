#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""crop_paper_figs.py — 论文原图裁切 + manifest 溯源留痕

把论文 PDF 里的原生图（架构/对比/曲线/注意力/效率图）裁成高清 PNG，
并把每张图的 sha256 / 来源 / 页码 / 图号写进 figures.json（G10 溯源门禁的数据源）。

同时**全量扫描 PDF 里的 Figure/Table 题注**，另写一份 paper-figures.json
（论文"本来有哪些图"的独立清单，不由裁图者挑）。deck_qa.py 的 G15 用它判定
"原文有图是否都被用上/未被用上是否都有理由"。

用法:
  python scripts/crop_paper_figs.py --pdf <论文.pdf> --out <图片输出目录>
        --manifest <figures.json 路径> [--targets <targets.json>] [--zoom 3]
        [--inventory <paper-figures.json 路径，默认与 manifest 同目录>]
"""

import argparse
import hashlib
import json
import os
import re
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    sys.stderr.write(
        "[FATAL] 未安装 PyMuPDF，无法运行 crop_paper_figs.py。\n"
        "        请先执行: pip install PyMuPDF\n"
    )
    raise SystemExit(2)

# iTransformer 论文的 7 张内置 targets（在真实双栏 ICLR 论文上验证过的参数）
DEFAULT_TARGETS = [
    {"name": "fig1_overall", "page": 1, "caption": "Figure 1:", "pad": 30,
     "hard_clip": [368, 514, 612, 657]},
    {"name": "fig2_compare", "page": 2, "caption": "Figure 2:", "pad": 30},
    {"name": "fig3_taxonomy", "page": 3, "caption": "Figure 3:", "pad": 30},
    {"name": "fig4_overview", "page": 4, "caption": "Figure 4:", "pad": 30},
    {"name": "fig5_general", "page": 7, "caption": "Figure 5:", "pad": 30},
    {"name": "fig7_analysis", "page": 9, "caption": "Figure 7:", "pad": 55},
    {"name": "fig10_efficiency", "page": 16, "caption": "Figure 10:", "pad": 30},
]


def find_caption_spans(page, caption):
    """在 span 里找包含 caption 的 span，返回 [(x0,y0,x1,y1,text)]，按 top 升序。"""
    hits = []
    d = page.get_text("dict")
    for block in d.get("blocks", []):
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                if caption in span.get("text", ""):
                    x0, y0, x1, y1 = span["bbox"]
                    hits.append((x0, y0, x1, y1, span["text"]))
    hits.sort(key=lambda h: h[1])
    return hits


def collect_candidate_rects(page):
    rects = []
    for dr in page.get_drawings():
        r = dr.get("rect")
        if r is not None:
            rects.append(fitz.Rect(r))
    for img in page.get_images(full=True):
        xref = img[0]
        try:
            for r in page.get_image_rects(xref):
                rects.append(fitz.Rect(r))
        except Exception:
            pass
    return rects


def crop_target(doc, target, out_dir, zoom):
    name = target["name"]
    pno = int(target["page"])
    caption = target["caption"]
    page = doc[pno - 1]
    pw = page.rect.width

    if target.get("hard_clip"):
        clip = fitz.Rect(*target["hard_clip"])
        label = caption.rstrip(":：").strip()
    else:
        hits = find_caption_spans(page, caption)
        if not hits:
            snippet = page.get_text("text")[:200].replace("\n", " ")
            raise RuntimeError(
                f"[{name}] 第 {pno} 页找不到 caption {caption!r}；"
                f"该页文本片段：{snippet!r}"
            )
        cap_x0, cap_top, cap_x1 = hits[0][0], hits[0][1], hits[0][2]
        label = caption.rstrip(":：").strip()

        # 过滤：剔除双栏页面正文段落与页边竖线
        xlo = cap_x0 - 250
        xhi = cap_x1 + 250
        kept = [r for r in collect_candidate_rects(page)
                if r.x0 >= xlo and r.x1 <= xhi]
        if kept:
            box = fitz.Rect(kept[0])
            for r in kept[1:]:
                box = box | r
        else:
            box = fitz.Rect(cap_x0, cap_top, cap_x1, cap_top)

        left = min(box.x0 - 4, 55)
        right = max(box.x1 + 4, pw - 55)
        if right - left < 300:
            right = left + 300
        clip = fitz.Rect(left, max(box.y0 - 5, 40), right, cap_top - 1)

    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=clip)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.abspath(os.path.join(out_dir, f"{name}.png"))
    pix.save(out_path)

    with open(out_path, "rb") as fh:
        sha = hashlib.sha256(fh.read()).hexdigest()
    return {
        "file": out_path,
        "source_type": "pdf-crop",
        "origin": os.path.abspath(doc.name),
        "page": pno,
        "label": label,
        "name": name,
        "sha256": sha,
        "size_px": [pix.width, pix.height],
        "_aspect": round(pix.width / pix.height, 3) if pix.height else 0,
    }


def load_manifest(path):
    if path and os.path.isfile(path):
        try:
            with open(path, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except Exception as e:
            sys.stderr.write(f"[WARN] 旧 manifest 解析失败，将重建：{e}\n")
    return {}


# ------------------------------------------------------- 论文图片清单（独立于裁图选择）
CAPTION_RE = re.compile(r"^\s*(Figure|Fig\.?|Table)\s*(\d+)\s*[:：.]?\s*(.*)$", re.IGNORECASE)


def scan_inventory(doc):
    """全量扫描 PDF 题注，产出论文"本来有哪些 Figure/Table"的清单。

    清单只由 PDF 文本决定，与"裁了哪几张"无关——这是 G15 判"原文图有没有被漏用"的依据。
    """
    items, seen = [], set()
    for pno in range(doc.page_count):
        page = doc[pno]
        try:
            d = page.get_text("dict")
        except Exception:
            continue
        for block in d.get("blocks", []):
            lines = block.get("lines", [])
            for idx, line in enumerate(lines):
                txt = "".join(s.get("text", "") for s in line.get("spans", []))
                t = txt.strip()
                m = CAPTION_RE.match(t)
                if not m:
                    continue
                kind = "Figure" if m.group(1).lower().startswith("fig") else "Table"
                label = f"{kind} {m.group(2)}"
                if label in seen:
                    continue
                # 题注可能跨行，续接同 block 后续行直到空行/下一个题注
                cap = m.group(3).strip()
                for nxt in lines[idx + 1: idx + 4]:
                    more = "".join(s.get("text", "") for s in nxt.get("spans", [])).strip()
                    if not more or CAPTION_RE.match(more):
                        break
                    cap += " " + more
                seen.add(label)
                items.append({"label": label, "kind": kind, "page": pno + 1,
                              "caption": cap[:200]})
    items.sort(key=lambda x: (x["kind"], int(x["label"].split()[1])))
    return items


def main():
    ap = argparse.ArgumentParser(description="论文原图裁切 + figures.json / paper-figures.json 留痕")
    ap.add_argument("--pdf", required=True, help="论文 PDF 路径")
    ap.add_argument("--out", required=True, help="图片输出目录")
    ap.add_argument("--manifest", required=True, help="figures.json 路径")
    ap.add_argument("--targets", default=None, help="自定义 targets.json（结构同内置列表）")
    ap.add_argument("--inventory", default=None,
                    help="paper-figures.json 路径（默认：与 manifest 同目录）")
    ap.add_argument("--zoom", type=int, default=3)
    args = ap.parse_args()

    if not os.path.isfile(args.pdf):
        sys.stderr.write(f"[FATAL] PDF 不存在：{args.pdf}\n")
        raise SystemExit(2)

    if args.targets:
        if not os.path.isfile(args.targets):
            sys.stderr.write(f"[FATAL] targets 文件不存在：{args.targets}\n")
            raise SystemExit(2)
        with open(args.targets, "r", encoding="utf-8") as fh:
            targets = json.load(fh)
    else:
        targets = DEFAULT_TARGETS

    doc = fitz.open(args.pdf)
    print(f"# crop_paper_figs.py  pdf={args.pdf}  pages={doc.page_count}  zoom={args.zoom}")

    manifest = load_manifest(args.manifest)
    manifest["deck"] = os.path.basename(args.pdf)
    manifest["generated_by"] = "crop_paper_figs.py"
    manifest["zoom"] = args.zoom
    figs = manifest.get("figures", [])
    by_name = {f.get("name"): i for i, f in enumerate(figs)}

    for t in targets:
        try:
            rec = crop_target(doc, t, args.out, args.zoom)
        except Exception as e:
            sys.stderr.write(f"[FAIL] {e}\n")
            raise SystemExit(1)
        w, h = rec["size_px"]
        print(f"{rec['name']:<16} page={rec['page']:<3} size_px={w}x{h}  aspect={rec['_aspect']}")
        rec.pop("_aspect", None)
        if rec["name"] in by_name:
            figs[by_name[rec["name"]]] = rec   # 同 name 覆盖
        else:
            by_name[rec["name"]] = len(figs)
            figs.append(rec)

    manifest["figures"] = figs
    os.makedirs(os.path.dirname(os.path.abspath(args.manifest)), exist_ok=True)
    with open(args.manifest, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=2)
    print(f"# manifest 写入：{os.path.abspath(args.manifest)}  共 {len(figs)} 张图")

    # 论文图片清单（独立留痕，供 G15 判"原文有图是否被漏用"）
    inventory = scan_inventory(doc)
    inv_path = args.inventory or os.path.join(os.path.dirname(os.path.abspath(args.manifest)),
                                              "paper-figures.json")
    with open(inv_path, "w", encoding="utf-8") as fh:
        json.dump({"origin": os.path.abspath(args.pdf), "items": inventory}, fh,
                  ensure_ascii=False, indent=2)
    figs_inv = [i["label"] for i in inventory if i["kind"] == "Figure"]
    tables_inv = [i["label"] for i in inventory if i["kind"] == "Table"]
    print(f"# 论文清单写入：{inv_path}")
    print(f"# 论文共有 Figure {len(figs_inv)} 个：{figs_inv}")
    print(f"# 论文共有 Table {len(tables_inv)} 个：{tables_inv}")
    unused = sorted(set(figs_inv) - {f.get('label') for f in figs})
    if unused:
        print(f"# 提示：以下论文原图本次未裁切，上片前必须给出理由：{unused}")
    doc.close()


if __name__ == "__main__":
    main()
