# Two-Phase Prompt Template Library

> Use Template 1 for Stage 1→2 (source material → outline), **STOP-AND-WAIT for user confirmation**; use Template 2 for Stage 4 (outline → PPT). Each template can be copied wholesale; replace the bracketed placeholders as needed.

## Stage Checkpoint Master Table (follow it at the close of every stage; missing any one item counts as a process violation)

| Stage | Required at close-out | STOP-AND-WAIT? | Evidence files |
| --- | --- | --- | --- |
| 1 Content Decomposition | Terminology ledger + claim list (claim / evidence location / strength) | No (but for vague requirements, clarify audience / occasion / page count first) | Claim list |
| 2 Narrative Design | action-title chain + ghost deck test + page types | **Yes**: send the outline to the user and wait for confirmation before moving on | `outline_confirmed` + `confirm_evidence` in `work/deck-spec.json` |
| 3 Visual System | 2-3 style candidates + recommendation rationale + visual spec card | **Yes**: wait for the user to lock in a style | `style_name` + `style_confirmed` in `deck-spec.json` |
| 4 Multi-path Rendering | Run `scripts/crop_paper_figs.py` (paper decks; also produces the paper-figure inventory) + render the deck + run `scripts/deck_qa.py` | No | `work/figures.json` + `work/paper-figures.json` + `work/qa_output.txt` |
| 5 QA-Gated Delivery | Render to images and inspect page by page (graded) → fix one version, re-check one version → delivery evidence block | No | Defect list + verbatim `qa_output.txt` |

## Downgrade Protocol (when the user says "I just want the final result / do it directly / stop asking me")

Do not skip the outline and style confirmations because of this; instead merge them and send them as **one message**:

```text
Page-level outline (action title + page type for every page) + 2-3 style candidates (one-line rationale each + which one I recommend) + I will proceed with X.
— Then go straight into Stage 4/5, attaching the complete QA evidence block at delivery.
```

Key points: ① the outline and the style candidates are **merged into one** message, not split into two rounds of waiting; ② declare "I will proceed with X" so the user can correct course at low cost; ③ **the evidence blocks of the R0 Iron Rules and the G Hard Gates are non-waivable under any circumstances**.

## Template 1: Close Reading of Source Material → Presentation Outline (ask for the outline first; do not generate the PPT directly)

```text
Act as a [graduate literature review presentation / project reporting / courseware production] assistant and read closely the [paper PDF / report / source material] I provide.

Do NOT generate the PPT yet. Instead, first output a presentation outline that includes:

1. Basic information: title, source/venue, year, field
2. Background: what problem the field is trying to solve, why it matters, and where existing methods/approaches fall short
3. Core problem: what exactly is solved this time, and the motivation
4. Method/approach: core idea, framework structure, key formulas or pipeline, and how it differs from existing approaches
5. Experiments/argumentation: datasets/samples, baselines/controls, evaluation metrics, main settings
6. Key results: the 2-3 most important results, each annotated with its location in the original (figure/table/section)
7. Innovations: contributions at the theoretical/methodological/application level
8. Weaknesses and limitations: assumptions, defects, generalization, directions for improvement
9. A page-structure suggestion for an N-page PPT (give each page a conclusion-style title)

Notes:
- Do not fabricate anything that is not in the source material;
- Annotate key conclusions with their source locations (sections/figures/tables) wherever possible;
- Write every page title as a conclusion sentence (action title), not a section name;
- **After outputting the outline, STOP and wait for my confirmation; do not start generating the PPT on your own** (this is the two-phase iron rule; skipping it means rework);
- The output should be suitable for directly generating the presentation PPT afterwards.
```

## Template 2: Outline → PPT (after the outline is confirmed)

> Precondition: the outline has been confirmed by the user. Item 2 of this template triggers the **style confirmation gate** once more — do not start writing rendering code before the style is locked in; present the candidates first and wait for a one-line confirmation.

```text
Based on the presentation outline confirmed above, generate an N-page PPT.

Requirements:
1. It is for a [graduate lab meeting / defense / performance review / teaching / government briefing / competition pitch] occasion, about X minutes long;
2. Style: first give me 2-3 style candidates (each with a one-line recommendation rationale); lock in and execute only after I confirm;
3. Every page title is a conclusion sentence (action title); the whole deck must make sense from the titles alone;
4. Body text per page: no more than 5 bullets, each no longer than 1.5 lines;
5. Method pages use flowcharts/structure diagrams, not plain text;
6. Result pages highlight the key conclusions; annotate the takeaways directly on the charts instead of piling up numbers;
7. Insert a breathing page (a big-type conclusion or a section-divider page) between any two high-density pages;
8. Add speaker notes of 80–120 Chinese characters (≈60–100 English words) to every page;
9. Charts follow top-journal style: thin lines, low saturation, direct annotations, red for gains and green for losses;
10. If the source material includes a paper: **every figure already present in the material MUST go on a slide** — use `scripts/crop_paper_figs.py` to crop the original paper figures from the PDF (zoom≥3, visually inspect every crop for sharpness); **having an original figure available but not using it, or substituting a self-made figure / AI-generated image / icons for the original figures = a violation**; add a citation under each figure (author · venue · year · Figure x) and register every figure in `work/figures.json`; the script also produces `work/paper-figures.json` (which Figures the paper originally contains). **Cross-check against that inventory item by item**: any Figure that cannot go on a slide must have a reason written in `unused_figures_reason` in `work/deck-spec.json` (≥8 characters); self-made figures are allowed only when the source material truly has no corresponding figure; a self-made figure must be a real image file (shape assemblies don't count), registered in `figures.json` with `source_type=self-made` + `reason`, and labeled "Source: self-made" on the slide. Verify every number against the original before it goes on a slide and record its Table/Figure number;
11. The generation script must print: page count, and len() of every page's speaker notes (80–120 chars (CN) / 60–100 words (EN));
12. After rendering, you **MUST run the gate script** and paste the raw output:
    `python scripts/deck_qa.py <deck.pptx> --spec work/deck-spec.json --figures work/figures.json --paper-figures work/paper-figures.json --mode A --out work/qa_output.txt`
    Fix any FAIL and rerun until everything is PASS (including G15 "is any original paper figure left unused / does a self-made figure substitute for an original"); then render to images and inspect page by page (text overflow → overlaps → alignment → margins → contrast);
13. At delivery, attach the delivery evidence block (fill in the blanks per references/delivery-template.md) and check the 10 Iron Rules in SKILL.md §0 one by one.
```

## Template 3: When a School/Corporate Template Must Be Applied

```text
I have uploaded a standard PPT template. First analyze the template's layouts and placeholders,
then generate the PPT against the template master: titles go into title placeholders, body text into body placeholders, images into picture placeholders.
Do not overlay text directly on the background image.
When the template has 4 slots but the actual content only fills 3, delete the entire element group of the extra slot.
```

## Template 4: Audit/Improve an Existing PPT

```text
Read this PPTX and first take a content inventory (page by page: title + key points + layout), then output a diagnostic report:
1. Which pages have titles that are not conclusion-style (give rewrite suggestions);
2. Which pages suffer text overload / overflow / repeated layouts;
3. Which charts are "naked" (no annotations, default color scheme);
4. Which "AI-generated look" problems exist (decorative lines, color bars, leftover placeholders);
5. Whether citations are complete and speaker notes are all in place.
Give the diagnosis first; make page-by-page fixes only after I confirm.
```

## Template 5: Style-Lock Addendum for the AI Image-Generation Path (R4)

```text
First use the image-generation model to produce a sample render of page 1; continue only after I confirm it passes.
From page 2 onward, use the finished page 1 as the reference image for every page and state explicitly in the prompt:
"continuing EXACT visual style from reference image, SAME palette, SAME typography",
and generate page by page serially; parallel generation is forbidden.
```

## Template 6: Multi-Paper Literature Review Outline (>5 papers)

```text
Synthesize the following N papers around [research topic] and output a review outline (do not enumerate papers one by one):
1. Themes: 3-6 research directions running through the paper set;
2. Convergences: findings that multiple papers agree on;
3. Disagreements: conflicting conclusions or methodological divergences;
4. Gaps: questions the paper set has not yet solved;
5. For each part, give a 1-2-page PPT structure suggestion, annotated with the supporting papers.
If the papers are too scattered to synthesize, say so directly instead of forcing a theme.
```

## Template 7: Image-Based PPT → Editable PPTX (R8)

```text
What I provide is an [image-based PPT / scanned pages / course screenshots]; restore it as an object-level editable PPTX:
1. Page by page, split the layout into 3-5 semantic regions (title / text / shapes / tables / annotations) and rebuild region by region;
2. Measurable circles, cards, connectors, and arrows must all be rebuilt as native shapes — thin arrows use one connector shape, solid arrows use one arrow shape (text goes inside the arrow); assembling arrows from "a line + a triangle" is forbidden, and flattening the entire image into one picture is forbidden;
3. Extract the text from the image and rebuild the text boxes preserving the original hierarchy;
4. Formulas must be rendered with a formula engine; if no engine is available, stop and ask me — do not fudge it with a blurry screenshot;
5. Truly complex local illustrations/photos may stay as bitmaps; note at delivery which parts are still images;
6. Self-check each page by comparing its rendered result side by side with the original: no structural omissions and no newly hallucinated elements; assemble only after it passes.
```

## Template 8: Bespoke Style (when no preset fits)

```text
No existing style matches my needs. Please custom-build a named style on the spot using the "four-piece set" and give me a preview:
1. Palette: primary color + 1-2 secondary colors + accent color (give exact hex values; the primary color carries 60-70% of the visual weight);
2. Font pairing: CJK font family + Latin/numeric companion fonts, plus the type-size hierarchy;
3. Visual motif: one reusable element that runs through the whole deck (e.g., rounded-corner cards / circular icons / a specific graphic language);
4. Light/dark tone: dark-light sandwich (dark cover + light content) or all-dark / all-light.
My topic is [topic], and my mood keywords are [keywords]. After confirmation, write this spec into the visual spec card and apply it across the whole deck.
```

## Template 9: Gate-Run Playbook (run it yourself after rendering and paste the raw output to the user)

```text
After rendering, execute the following in order and paste the output verbatim; no summarizing, no "already checked" claims:
1. python scripts/crop_paper_figs.py --pdf [paper.pdf] --out work/fig --manifest work/figures.json    # paper decks only; also produces work/paper-figures.json
2. python scripts/deck_qa.py [final_deck.pptx] --spec work/deck-spec.json --figures work/figures.json --paper-figures work/paper-figures.json --mode A --out work/qa_output.txt
3. If there are FAILs: explain item by item what was fixed, rerun, and repeat until everything is PASS; for WARN items, explain why they are acceptable. When G15 reports "Figure X exists in the paper but is unused", either add that original paper figure or write a reason in unused_figures_reason in deck-spec.json — do not game it by trimming the inventory (the inventory is generated by the script scanning the PDF captions).
4. Render to images and inspect page by page; list defects graded high/medium/low; every high defect must be fixed.
In the delivery notes, attach the confirmation evidence from deck-spec.json (the user's exact words) + the verbatim qa_output.txt + the provenance of every figure (PDF page / Figure number / self-made, with reason) + original-paper-figure usage (placed on a slide or not, with reasons).
```

## Template 10: Rule Self-Check (verify the 10 Iron Rules in SKILL.md §0 one by one before delivery)

```text
Self-check against the 10 Iron Rules in SKILL.md §0 one by one; for each rule pick one of "compliant / non-compliant / not applicable" plus one line of evidence:
1 Two-phase iron rule (both outline and style confirmed; evidence = the user's exact words)
2 Original-paper-figure-first iron rule (figures in the source material must go on slides; no hand-drawn/AI/icon substitutes for original figures; self-made figures carry a reason and are labeled "Source: self-made")
3 Figure provenance traceable (figures.json complete; manifest files exist and hashes are self-consistent)
4 Visual-rich numeric gate (visual-page ratio, consecutive non-visual pages, visual anchors; shape color blocks don't count)
5 Numbers verified one by one (every number has a Table/Figure source)
6 Speaker notes 80–120 chars (CN) / 60–100 words (EN) (the script output is authoritative)
7 QA evidence block (including a rendered-preview availability statement)
8 action title (the whole deck makes sense from the titles alone)
9 Visual anti-patterns cleared (item by item per design-language §6)
10 De-templated wording (item by item per design-language §7, already scanned by the script)
Any "non-compliant" item must be fixed first, then run the self-check once more.
```
