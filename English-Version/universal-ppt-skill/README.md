<div align="center">

<img src="../logo_512.png" width="130" alt="universal-ppt-skill logo"/>

# universal-ppt-skill

</div>

**A model-agnostic, five-stage presentation factory for AI agents.** It turns the three most common failures of AI-generated decks — **all text, untrustworthy image sources, opaque process** — from "depends on model self-discipline" into **machine-enforced gates + on-disk evidence**.

> Five-stage pipeline: **content decomposition → narrative design → visual system → multi-path rendering → QA-gated delivery**, with 30+ style presets across 6 scenarios and 8 selectable render paths. 7 of the 10 iron rules are enforced by `scripts/deck_qa.py` (gates G1–G15) — a deck that fails is not delivered.

## Why it exists

Asking an LLM to "make me a PPT" usually hits three problems:

| Problem | Typical symptom | This skill's answer |
| --- | --- | --- |
| **All text** | 9 of 10 pages are text bullets; "rich visuals" that are really just colored shapes | Strict visual-page definition (only pictures / native charts / tables count); gates G5/G6/G7 enforce ratio ≥ 60% and no 3 consecutive text-only pages |
| **Untrustworthy images** | Ignores the paper's ready-made architecture figure and draws its own; or pastes images of unknown origin | Paper-figure-first iron rule + `crop_paper_figs.py` crops originals from the PDF + sha256 provenance manifest (G10/G11/G15) |
| **Opaque process** | Skips outline confirmation, notes length by gut feeling, QA summarized as "done" | Two-phase STOP-AND-WAIT gates + script-measured evidence + a non-waivable delivery evidence block |

## How it works

```
Stage 1  Source decomposition      term ledger · claim list
Stage 2  Outline design            page-level outline · action titles · STOP-AND-WAIT (user confirms)
Stage 3  Visual system             2-3 style candidates · user picks · visual spec card
Stage 4  Multi-path rendering      R1-R8 (crop_paper_figs.py for paper decks)
Stage 5  QA & delivery             deck_qa.py G1-G15 · visual pass · evidence block
```

Rules are tiered: **R0 iron rules** (never waivable) → **G hard gates** (machine-enforced, any FAIL = rework) → **P soft preferences** (may deviate with a stated reason).

**Render paths** (chosen per task, combinable): R1 native editable PPTX via python-pptx · R2 template/master injection · R3 HTML→screenshot→PPTX · R4 AI full-page images (any image model) · R5 Marp / Reveal.js / Slidev · R6 LaTeX Beamer · R7 SVG / Mermaid · R8 image-to-editable-PPTX reconstruction.

**Scenario modes**: A Academic Argumentation · B Business Reporting · C Teaching & Explanation · D Everyday Expression · E Government & Public Sector · F Competition Pitch — with 30+ style presets in `references/style-library.md` (Academic Restrained, McKinsey, Data Dashboard, Hand-drawn Whiteboard, Government Red, Dark Premium, and more).

## Package layout

```
universal-ppt-skill/
├── SKILL.md                    # Main entry: 10 iron rules + rule tiers + five-stage workflow
├── prompts/stage-prompts.md    # Per-stage prompt templates with STOP-AND-WAIT checkpoints
├── references/
│   ├── qa-gates.md             # G1-G15 gate details & machine checks
│   ├── render-paths.md         # R1-R8 rendering paths (12 hard-won pitfalls)
│   ├── design-language.md      # Color / typography / layout specs + AI-look anti-patterns
│   ├── style-library.md        # 30+ style presets across 6 scenarios
│   ├── narrative-patterns.md   # Scenario page-structure templates & action-title craft
│   └── delivery-template.md    # Delivery evidence block template (non-waivable)
└── scripts/
    ├── deck_qa.py              # Single-entry gate: G1-G15, any FAIL → exit 1 (bilingual: CN/EN)
    └── crop_paper_figs.py      # Paper-figure cropping + figures.json ledger
                                #   + paper-figures.json inventory of the paper
```

## Quick start

1. Read the 10 iron rules in [SKILL.md](SKILL.md) §0 (other docs load per stage);
2. Use Template 1 in [prompts/stage-prompts.md](prompts/stage-prompts.md) to get a page-level outline first — **confirm before continuing**;
3. After rendering, run the gates (paper decks must build a figure ledger first):

```bash
# Paper decks: crop original figures first (also emits the paper figure inventory)
python scripts/crop_paper_figs.py --pdf paper.pdf --out work/figs --manifest work/figures.json

# Then run the single-entry gate (any FAIL → exit 1)
python scripts/deck_qa.py deck.pptx \
    --spec work/deck-spec.json \
    --figures work/figures.json \
    --paper-figures work/paper-figures.json \
    --mode A --out work/qa_output.txt
```

Dependencies: `pip install python-pptx PyMuPDF`.

## Gates at a glance (G1–G15)

| Gate | Checks | Method |
| --- | --- | --- |
| G1 | Page count matches spec | python-pptx |
| G2 | Speaker notes 80–120 chars (CN) / 60–100 words (EN) per page — language auto-detected | measured per page, printed |
| G3/G4 | Shape out-of-bounds / text overflow | geometry estimate + unbreakable-token width |
| G5/G6/G7 | Visual-page ratio ≥ 60% / no 3 consecutive non-visual pages / per-page visual anchors | only pictures · native charts · tables count; colored shapes don't |
| G8/G9 | Placeholder leftovers / banned template phrases (Chinese + English lists) | regex scan |
| G10 | Image provenance: every embedded image's sha256 ↔ `figures.json`; ledger files exist & hash-consistent; academic mode accepts only pdf-crop / docs-asset / documented self-made | hash + ledger |
| G11 | In-slide citation on picture pages (paper figures cite the Figure number; self-made marked "self-made") | text scan |
| G12 | Outline/style two-phase user-confirmation evidence | spec fields |
| G13 | Action titles (claim sentences, never bare section names) | blacklist + position heuristics |
| G14 | Font-family convergence / default-shadow inheritance | XML traversal |
| G15 | **Paper-figure usage audit**: every Figure in the inventory is either in the deck or excused via `unused_figures_reason`; self-made images must not outnumber paper figures | caption inventory vs ledger |

## Benchmark-proven

Built and validated with a public benchmark: **4 different LLMs × 2 topics × 10 pages**, all rendered through this same skill (visual evidence on the product listing). Same rules, same gates, across models — that is what "model-agnostic" means here. Headline findings:

| Deck (model · topic) | Pics | Charts | Tables | Visual-page ratio | Content FAIL |
| --- | ---: | ---: | ---: | ---: | :---: |
| GLM-5.3-flash · personal profile | 5 | 0 | 0 | 50% | 2 |
| GLM-5.3-flash · iTransformer | 4 | 2 | 1 | 60% | 1 |
| DeepSeek-V4.1-Flash · personal profile | 5 | 2 | 0 | 70% | 0 |
| DeepSeek-V4.1-Flash · iTransformer | 7 | 1 | 1 | 90% | 0 |
| Kimi-K3 · personal profile | 5 | 1 | 2 | 80% | 0 |
| Kimi-K3 · iTransformer | 7 | 1 | 2 | 100% | 0 |
| LongCat-2.5-Preview · personal profile | 0 | 0 | 0 | 0% | 3 |
| LongCat-2.5-Preview · iTransformer | 0 | 2 | 1 | 30% | 2 |

1. **The notes-length gate is 100% effective**: all 80 pages' speaker notes measured in range, printed page by page. Hard gates beat gentle reminders.
2. **Visual richness spans 0% → 100% across models** — without gates, "rich visuals" is a matter of faith; with them, the floor is enforceable.
3. **"Looks like a paper figure" ≠ "verifiable"**: 18 embedded images across 4 paper decks, **0 matched** the freshly cropped originals by sha256 (scaling/recompression change bytes) — exactly the hole G10/G15 plug.
4. **Gates catch what human eyes miss**: G4 height overflow, G6 "3 consecutive text pages", G15 "paper figure never accounted for".

> Bottom line: **material sets the ceiling, gates set the floor.**

## Known pitfalls (distilled from real decks — full list in [references/render-paths.md](references/render-paths.md) §10)

- Paper figures **must be re-cropped from the PDF by script** — pre-existing image files cannot pass the sha256 ledger check;
- Visual pages count only **pictures / native charts / tables** — shape-assembled "diagrams" don't qualify (G5/G6/G7 catch this);
- Mixing `Inches(float)` with `Inches(Emu(x))` creates 9524-inch giant shapes; negative shadow offsets **corrupt the file**;
- Iterate notes length against the script's printed output, never estimates.

## License & provenance

[MIT](LICENSE). Distilled from the best of 17 open-source skills (anthropics/pptx, deer-flow, nature-skills paper2ppt/image2ppt, academic-pptx, PaperSpine, and more — full list in SKILL.md). The upstream project remains open source; this packaged edition adds the bilingual QA script, English documentation, and curated defaults so it works out of the box.
