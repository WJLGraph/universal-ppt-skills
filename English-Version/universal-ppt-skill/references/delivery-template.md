# Delivery Evidence Block Template (Required for Stage 5 — copy it and fill in the blanks)

> On delivery you must not write only "QA passed". The block below **must appear verbatim in the delivery notes**; missing any single field marked [Non-waivable] counts as a process violation. Raw script output must not be summarized, paraphrased, or reduced to "checked".

## 1. Delivery Announcement (the first thing the user sees; keep it within 10 lines)

```text
Deliverable: <file name>  (path: computer://...)
Pages: N pages  ·  Mode: A-F (<scenario verdict in one sentence>)  ·  Style: <style name>  ·  Render path: R1-R8
Visual pages: k/N = xx% (pages containing images/charts/tables)  ·  Consecutive non-visual pages: 0
One-sentence conclusion: <the one judgment this deck wants the audience to remember>
```

## 2. Non-Waivable Fields (fill in each item; any missing field is a violation)

| Field | What to fill in | Source |
| --- | --- | --- |
| Outline confirmation evidence | Verbatim quote of the user's exact words confirming the outline (≥8 words) | `work/deck-spec.json` → `confirm_evidence` |
| Style confirmation evidence | The user-locked style name + the user's exact confirmation words | `deck-spec.json` → `style_name` / `style_confirmed` |
| Raw QA script output | Full contents of `qa_output.txt` (including every PASS/FAIL line) | An actual run of `scripts/deck_qa.py` |
| FAIL/WARN handling notes | For each FAIL, what was fixed; for each WARN, why it is acceptable | Comparison of the previous round's output vs the final round's output |
| Source of every figure | `file → PDF page number + Figure No.` (original paper figure) / `docs source-material path` (source-material image) / `Source: self-made + reason` (self-made figure — must state why the source material has no matching original figure) | `work/figures.json` |
| **Original paper figure usage** | The paper's manifest lists N Figures in total: which ones are on slides (page number → Figure No.), which are not + a one-line reason for each, and how many self-made figures there are with their purposes | `work/paper-figures.json` + `deck-spec.json → unused_figures_reason` |
| Render preview availability | "Rendered pages visually inspected one by one (tool: X)" or "**Render preview unavailable**; replaced with programmatic checks + cropped-asset collages + text/shape review" | Actual Stage 5 record |
| Known limitations | Unresolved items + their impact (e.g. "the smallest axis labels in Figure 5 are slightly blurry at 1600px rendering, but readable when projected") | Actual Stage 5 record |

## 3. Optional Items (include them if you have them; omit if you don't)

- Page-by-page speaker-note word-count list (already printed by the script; you may paste the whole block)
- Number provenance table: `number → source (Table x / Figure x)`; recommended for academic/data decks
- Change notes: what trade-offs/additions were made relative to the user's source material (which pages were dropped, what was merged, and why)
- Paths of the four evidence files under `work/`: `deck-spec.json` / `figures.json` / `paper-figures.json` / `qa_output.txt`

## 4. Free Iteration Points After Delivery

Proactively invite the user to name any pages they want redone, and state the redo granularity: for image-based decks (R3/R4), redoing one page means regenerating that page; R1/R3 allow editing individual objects in place; R8 rebuilds page by page. **Never re-run the whole deck**, unless the user asks to change the style or the argumentation structure.

## 5. Negative Examples (any of these counts as having delivered no delivery notes at all)

- ❌ "QA completed, no issues"
- ❌ "Checked speaker-note word counts and visual coverage; all pass" (no raw output)
- ❌ "All images come from the paper" (no page numbers / Figure numbers / hash evidence)
- ❌ "This page uses its own diagram in place of the paper's framework figure" (if the original paper has the figure, you must use the original figure; self-made figures may only supplement; G15 will block this)
- ❌ Pasting nothing but "QA passed ✅" and stopping there
