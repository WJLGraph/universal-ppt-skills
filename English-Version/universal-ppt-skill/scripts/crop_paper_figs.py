#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""crop_paper_figs.py — crop native paper figures + manifest provenance trail

Crops the native figures in a paper PDF (architecture / comparison / curve /
attention / efficiency plots) into high-resolution PNGs, and records each
figure's sha256 / origin / page / label into figures.json (the data source for
the G10 provenance gate).

It also **scans all Figure/Table captions in the PDF** and writes a separate
paper-figures.json — an independent inventory of "which figures the paper
originally had", not selected by the cropping step. deck_qa.py's G15 uses it
to check "whether every figure in the source paper is used, and whether every
unused one has a documented reason".

Usage:
  python scripts/crop_paper_figs.py --pdf <paper.pdf> --out <image output dir>
        --manifest <path to figures.json> [--targets <targets.json>] [--zoom 3]
        [--inventory <path to paper-figures.json, default: same dir as manifest>]
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
        "[FATAL] PyMuPDF is not installed; crop_paper_figs.py cannot run.\n"
        "        Install it first: pip install PyMuPDF\n"
    )
    raise SystemExit(2)

# 7 built-in targets for the iTransformer paper (parameters validated on a real two-column ICLR paper)
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
    """Find spans containing the caption text; return [(x0,y0,x1,y1,text)] sorted by top ascending."""
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
                f"[{name}] on page {pno}, caption {caption!r} not found; "
                f"text snippet of that page: {snippet!r}"
            )
        cap_x0, cap_top, cap_x1 = hits[0][0], hits[0][1], hits[0][2]
        label = caption.rstrip(":：").strip()

        # Filter: drop body-text blocks of two-column pages and vertical margin rules
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
            sys.stderr.write(f"[WARN] Failed to parse the existing manifest; it will be rebuilt: {e}\n")
    return {}


# ------------------------------------------------------- Paper figure inventory (independent of the crop selection)
CAPTION_RE = re.compile(r"^\s*(Figure|Fig\.?|Table)\s*(\d+)\s*[:：.]?\s*(.*)$", re.IGNORECASE)


def scan_inventory(doc):
    """Scan all captions in the PDF and produce an inventory of the
    Figure/Table items the paper originally contains.

    The inventory is determined solely by the PDF text and is independent of
    "which figures were cropped" — it is the basis for G15 to judge whether any
    figure present in the source paper was missed.
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
                # Captions may span multiple lines; keep appending the following lines
                # in the same block until an empty line or the next caption
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
    ap = argparse.ArgumentParser(description="Crop native paper figures + figures.json / paper-figures.json provenance trail")
    ap.add_argument("--pdf", required=True, help="Path to the paper PDF")
    ap.add_argument("--out", required=True, help="Output directory for cropped images")
    ap.add_argument("--manifest", required=True, help="Path to figures.json")
    ap.add_argument("--targets", default=None, help="Custom targets.json (same structure as the built-in list)")
    ap.add_argument("--inventory", default=None,
                    help="Path to paper-figures.json (default: same directory as the manifest)")
    ap.add_argument("--zoom", type=int, default=3)
    args = ap.parse_args()

    if not os.path.isfile(args.pdf):
        sys.stderr.write(f"[FATAL] PDF does not exist: {args.pdf}\n")
        raise SystemExit(2)

    if args.targets:
        if not os.path.isfile(args.targets):
            sys.stderr.write(f"[FATAL] targets file does not exist: {args.targets}\n")
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
            figs[by_name[rec["name"]]] = rec   # Overwrite the record with the same name
        else:
            by_name[rec["name"]] = len(figs)
            figs.append(rec)

    manifest["figures"] = figs
    os.makedirs(os.path.dirname(os.path.abspath(args.manifest)), exist_ok=True)
    with open(args.manifest, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=2)
    print(f"# manifest written: {os.path.abspath(args.manifest)}  {len(figs)} figures in total")

    # Paper figure inventory (independent provenance record, used by G15 to check "whether any original figure was missed")
    inventory = scan_inventory(doc)
    inv_path = args.inventory or os.path.join(os.path.dirname(os.path.abspath(args.manifest)),
                                              "paper-figures.json")
    with open(inv_path, "w", encoding="utf-8") as fh:
        json.dump({"origin": os.path.abspath(args.pdf), "items": inventory}, fh,
                  ensure_ascii=False, indent=2)
    figs_inv = [i["label"] for i in inventory if i["kind"] == "Figure"]
    tables_inv = [i["label"] for i in inventory if i["kind"] == "Table"]
    print(f"# paper inventory written: {inv_path}")
    print(f"# paper contains {len(figs_inv)} figures: {figs_inv}")
    print(f"# paper contains {len(tables_inv)} tables: {tables_inv}")
    unused = sorted(set(figs_inv) - {f.get('label') for f in figs})
    if unused:
        print(f"# NOTE: the following original paper figures were not cropped this run; a reason must be given before putting them on slides: {unused}")
    doc.close()


if __name__ == "__main__":
    main()
