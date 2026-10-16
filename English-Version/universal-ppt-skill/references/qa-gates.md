# QA Gates (loaded on demand in Stage 5)

> The first render almost always contains real defects. QA is not a box-ticking exercise — it is the last gate before delivery.

## §0 Hard-Gate Recital (skipping any one of these during generation = rework; derived from the same source as the 10 Iron Rules in SKILL.md §0)

1. Zero visual anti-patterns (design-language.md §6: decorative lines / color bars / vertical stripes / one-sided card borders including top color bars)
2. Paper decks: **any figure already present in the source material must be the original paper figure** — `scripts/crop_paper_figs.py` crops the original from the PDF (zoom ≥ 3), embeds it, and every figure gets an in-slide citation; **having an original figure but not putting it on a slide, or substituting a self-made figure / AI image / icon / screenshot for an original paper figure = violation**; only self-make a figure when the source material genuinely has no counterpart, and a self-made figure must be a real image file + registered in `figures.json` with `source_type=self-made` and a `reason` + an in-slide label "Source: self-made"
3. Every embedded figure is registered in `figures.json` (PDF page number + Figure number + sha256), and the image files registered in the manifest really exist with self-consistent hashes; every Figure in the paper manifest `paper-figures.json` is either on a slide or has a documented reason in `deck-spec.json`'s `unused_figures_reason`
4. Cross-check every number against the source material one by one (record the Table/Figure number)
5. Speaker notes 80–120 Chinese characters (≈60–100 English words): the script prints `len()` per page; trim anything over the limit
6. Programmatic gates must have printed output: paste the raw output of `scripts/deck_qa.py` (checklist in §1.5 below)
7. Visually inspect rendered images for background color / sharpness / overlaps; classify defects as high/medium/low
8. Full action-title coverage (first item of §1)

## §0.5 Division of labor between the gate script and manual inspection (machine first, human eyes second)

| Ruled dead by `scripts/deck_qa.py` (G-tier; no human "feels fine" override) | Manual visual inspection only (the script can't catch these; you must render and look) |
| --- | --- |
| Page count / speaker-note length / shapes out of bounds / text-overflow estimate | Whether text is **visually** truncated (an estimate is not a real render) |
| Visual-page ratio ≥60%, consecutive non-visual pages, visual anchors | Element overlaps, lines crossing text, the overall look of images |
| Banned phrases, leftover placeholders | Contrast, alignment & spacing, layout repetition (slide-sorter scan) |
| Figure provenance hash verification, manifest file existence & self-consistency, in-slide citation presence | Whether charts are bare, whether the palette looks cheap |
| Two-stage confirmation gates (outline_confirmed / style_confirmed) | Image sharpness (render and zoom in) |
| Action-title format | Whether the argument chain truly holds up (read the ghost deck end to end) |
| **Original paper-figure usage check (G15: originals on slides / reasons for non-use / self-made must not outnumber originals)** | **Whether the original figures were cropped correctly (body region not missed, tables not cropped as figures)** |

**Execution order**: run the script and fix until everything PASSes → then render and inspect visually → re-check one full round after fixing. Stage 5 ends only when both are done.

**Strict definition of a visual page (G5, closing the most common bypass)**: a visual page = the page contains **at least one of PICTURE / native chart `has_chart` / table `has_table`**. Text boxes, color blocks, rounded-corner cards, and "diagrams" assembled purely from shapes **do not count**. The script's output is authoritative — never talk yourself into it with "this page looks rich enough".

## §1 Content QA

- [ ] `scripts/deck_qa.py` has been run with zero FAIL (raw output archived in `work/qa_output.txt`)
- [ ] Two-stage confirmation gates on record: `outline_confirmed` / `style_confirmed` in `work/deck-spec.json` are true and the user's verbatim reply is preserved
- [ ] Every page title is an action title (in academic mode, 100% of content-page titles are conclusion-style, never section names)
- [ ] Ghost deck test passes: reading only the titles, the whole story holds together
- [ ] Terminology ledger cross-checked: model names / datasets / metrics / abbreviations verbatim-consistent (speaker notes included)
- [ ] No leftover placeholders / sample text (gate G8 already scanned: XXX, lorem, TODO, TBD / to be added, here)
- [ ] No fabricated content: every key claim is traceable; untraceable ones are marked "needs human verification"
- [ ] Figure manifest complete: every embedded figure has a PDF page number + Figure number + sha256 in `figures.json` (gate G10 verifies by hash, and also re-checks that every registered image file really exists with a self-consistent hash; **unregistered = "untrusted provenance"; in academic mode you won't even get a PASS for "all figure sources compliant"**; G11 in academic mode requires **every page containing a figure** to carry `Source: … Figure x` or `Source: self-made`)
- [ ] **No original paper figure left unused**: every Figure in the `paper-figures.json` manifest is either on a slide or has a clear reason in `deck-spec.json`'s `unused_figures_reason`; self-made figure count ≤ original paper figures on slides (G15); **substituting a self-made figure where the original paper has one = rework**
- [ ] Visual-page ratio on target: ≥60%, no 3 consecutive non-visual pages, and content/data/table pages all have visual anchors (title/statement/closing/section/timeline pages exempt; gates G5-G7)
- [ ] Page count matches the page-level outline; all required pages are present (conclusion page, References page)
- [ ] Speaker notes complete and within the length rule (80–120 chars (CN) / 60–100 words (EN) per page; gate G2 prints per-page measurements)

## §2 Visual QA (render to images and inspect page by page)

Priority order (fix high-severity first):

1. **Text overflow / truncation** (the most common defect, always user-visible)
2. Element overlaps (text pressed over shapes, lines crossing text)
3. Alignment & spacing (same-class elements misaligned, uneven spacing, gaps between blocks <0.3", margins to page edge <0.5")
4. Contrast (light text on light background / dark on dark, icons without a contrasting backing)
5. Layout repetition (three consecutive pages with the same layout; slide-sorter scan for 5+ pages with the same composition)
6. Bare charts (no title / no labels / default colors)
7. AI-flavor anti-patterns (scan item by item against design-language.md §6)
8. De-templated phrasing — banned English template phrases (scan against the design-language.md §7 English-mode banned-phrase list)

**Severity tiers** (distilled from nature-paper2ppt):

- **high (blocks delivery)**: evidence cropped out (axes / legends / panel labels / table rows), main evidence on a key-results page unreadable, text overflowing or clipped, page order scrambled or core evidence missing, fabricated quantitative claims
- **medium**: overcrowded pages, AI-template-flavored layouts (repeated equal-width cards / uniform right rail / decorative metric rows), crop edges too tight, captions detached from their visual, speaker notes missing or useless, vague source attribution
- **low**: minor alignment blemishes, palette/font fine-tuning, dense-but-readable page not split

Handling rule: fix all high; fix medium unless doing so would significantly expand the workload; log low and optionally skip. After fixing, re-render and re-inspect; stop after one consecutive round with no new defects (no endless polishing).

**Programmatic checklist** (**now baked into a script — run it first once the deck is produced; don't hand-copy or hand-compute**):

```bash
python scripts/deck_qa.py <deck.pptx> --spec work/deck-spec.json --figures work/figures.json \
       --paper-figures work/paper-figures.json --mode A --out work/qa_output.txt
```

Script coverage: G1 page count · G2 speaker-note length printed per page (threshold is language-adaptive: 80–120 chars (CN) / 60–100 words (EN)) · G3 shapes out of bounds / giant shapes · G4 text-overflow estimate · G5 visual-page ratio (strict definition in §0.5) · G6 consecutive non-visual pages · G7 visual anchors · G8 placeholder scan · G9 banned-phrase scan (English-mode banned-phrase list) · G10 figure provenance hash check + manifest file existence/self-consistency + academic-mode figure-source compliance · G11 in-slide citation · G12 two-stage confirmation gates · G13 action title · G14 font families & default-shadow count · **G15 original paper-figure usage check (originals on slides / reasons for non-use / self-made must not outnumber originals)**. Any FAIL means no delivery.

Items that still require manual follow-up (the script can't catch them; you must render / zoom in):

- Real-render text truncation (estimate ≠ render), element overlaps, lines crossing text
- Near-alignment (edges of same-class elements a few pixels off), uneven spacing, margins <0.5"
- Contrast (light text on light background / dark on dark)
- Layout repetition: scan the slide-sorter thumbnails once; 5+ pages sharing a composition require rebuilding some of them
- Bare charts: no title / no labels / default colors
- Image sharpness (zoom into the evidence figures to confirm axes / legends / panel labels / table rows are not cropped)
- Canvas background verification: double-confirm via rendered corner pixels + background XML before drawing conclusions (preview scaling can mislead — a white background often reads as gray)
- Main evidence figure too small (below 1/4 of the page requires human confirmation)

**Render-preview policy**: the render pipeline (LibreOffice→PDF→pdftoppm→inspect page by page); after any modification you must re-run the full conversion chain from the modified PPTX — never reuse old renders. Environments without a reliable renderer downgrade to: programmatic checks + asset-crop collage inspection + page-by-page text/shape review, with "render preview unavailable" noted in the delivery notes.

Image-style decks (R3/R4) additions: whether text inside images is hallucinated / mistyped (not editable — can only be regenerated); whether page numbers / watermarks appear unexpectedly. R8 additions: side-by-side comparison of rebuilt pages against the originals (contact sheet) — no structural omissions, no newly hallucinated elements, arrows/formulas are native objects.

Font note: the QA renderer's font substitution differs from the real opening environment — use safe fonts (Calibri/Arial/Microsoft YaHei, etc.) for container-width calculations, and leave 10% width headroom for non-safe fonts (safe-font list in design-language.md §2).

## §3 Provenance QA (mandatory for academic / data decks)

- [ ] **The two-pass method's order must not be flipped**: in the first pass, at the end of Stage 1/2, send the "claim list" to the user for confirmation (each entry: the claim verbatim + its location in the source material + strength); only in the second pass use that confirmed list to verify the finished deck against the original, item by item
- [ ] Every key conclusion is tagged (source, location, strength)
- [ ] Every on-slide number has provenance (Table x / Figure x / page number) and is verbatim-identical to the original value
- [ ] All figures in a paper deck come from `crop_paper_figs.py` (pdf-crop) and are registered; borrowed figures carry an in-slide citation (author/venue/year in small text), and the References page has the full entry
- [ ] Citation style is consistent (GB/T 7714 / APA / IEEE per the user's request)
- [ ] Statistical claims verified: sample size, significance tests, error bars, control setup, whether inference is overstated
- [ ] Reproduction-type content verified: environment dependencies, run commands, and data sources match the paper's description

## §4 Delivery Checklist

1. Deliverables: main file (.pptx / .pdf / .html / .zip) + speaker notes (embedded in notes or a standalone .md)
2. Present via present_files; attach the **delivery evidence block** per references/delivery-template.md (page count, mode A-F, style name, render path, raw QA script output, provenance of every figure, render-preview availability, known limitations, change notes)
3. Attach change notes: what was traded off / added relative to the user's source material
4. Attach the paths of the three evidence files in `work/` (deck-spec.json / figures.json / qa_output.txt)
5. Offer one free iteration round: invite the user to name the pages they want redone (partial redo takes priority over full regeneration — image-style decks regenerate page by page, R1/R3 redo locally, R8 rebuilds per page)
6. After the user confirms the style, save the visual spec card into the skill's style library (`~/.workbuddy/skills/universal-ppt-skill/styles/`) for direct reuse next time
