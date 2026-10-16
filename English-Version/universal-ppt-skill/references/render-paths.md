# Render Path Library (Stage 4, loaded on demand)

> Not bound to any single model or tool. Choose a path based on the delivery requirements; paths are composable.

## §0 Path Selection Decision Tree

```
Is the input an image / screenshot / image-based PPT (must be reconstructed as editable)?
├─ Yes → R8 image-to-editable-PPTX
└─ No → Does the text need to be editable word-for-word?
        ├─ Yes → Is there a unified template constraint?
        │       ├─ Yes → R2 template/master injection
        │       └─ No → R1 native python-pptx PPTX
        └─ No → Formula-dense?
                ├─ Yes → R6 LaTeX Beamer
                ├─ No → Chasing visual impact / artistic flair?
                │       ├─ Yes → R4 AI image generation (or R3 for high layout freedom)
                │       └─ No → Online HTML presentation / developer audience?
                        ├─ Yes → R5 Marp/Reveal.js
                        └─ No → R3 HTML-to-screenshot → PPTX (high-fidelity with zero image-generation dependency)
(R7 SVG/Mermaid can be layered onto any path for flowcharts / architecture diagrams)
```

When the user hasn't made it clear, default to R1 (editable, universal, controllable), and tell the user that other paths exist as options.

## §1 R1 · Native python-pptx PPTX (code-generated)

Tools: pptxgenjs (Node) or python-pptx. When the host has an official PPT skill (workbuddy-pptx, etc.), prefer delegating file-level operations to it.

**pptxgenjs engineering pitfalls (distilled from anthropics/pptx — hard-won lessons):**

- Set `pres.layout` before adding slides; the default canvas is 10"×5.625", not 13.3" wide; out-of-bounds coordinates don't error — they just vanish
- Colors without `#`, never 8-digit (alpha will **corrupt the file**); use `transparency: 0-100` for opacity
- pptxgenjs rewrites option objects in place (converting to EMU): never reuse config objects like shadow — create new ones each time
- Shadow `offset` must be ≥0 (negative values corrupt the file); for an upward shadow use `angle: 270` + a positive offset
- Letter spacing is `charSpacing`; `letterSpacing` is silently ignored
- Set `bullet: true` per list item (don't use a literal `•` — you'll get double bullets); array items get `breakLine: true` except the last; paragraph spacing via `paraSpaceAfter`
- One `new pptxgen()` instance per output file; `rectRadius` only applies to rounded rectangles
- Gradient fills are not supported — use a gradient background image instead
- Text boxes have internal padding: use `margin: 0` when aligning with shapes
- Speaker notes go into `slide.addNotes()`, not into on-slide text boxes
- Keep charts **native** (editable); only paste images for chart types PPT has no native form of (sankey / chord / network diagrams)
- For stacked charts, `dataLabelPosition` only allows ctr/inEnd/inBase (outEnd corrupts the file)
- Dual-axis combo charts must provide exactly two entries in both `valAxes` and `catAxes`, or PowerPoint drops the chart and reports corruption
- Charts ship bare by default: explicitly set `showTitle`+`title`, `showValue: true`+`dataLabelPosition`, `chartColors: [...]`; turn off the legend for single series; use low-saturation colors for axis labels and gridlines
- **Icon pipeline**: render SVG with react-icons (`renderToStaticMarkup`) → rasterize with `sharp` at ≥256px → `addImage({ data: "image/png;base64," + buf })` (the prefix is mandatory); simple icons can also be assembled from shapes
- After writing, always run the validation script (validate / open test); fix chart defects in the generator, never by hand-editing XML; use `markitdown deck.pptx` for content-level QA (per-page text + grep for placeholders XXX/lorem/TODO)

**python-pptx essentials:** you cannot copy slides (only `add_slide(layout)`); change text by assigning to `run.text` (`text_frame.text = "..."` wipes all paragraph styling); SVG/EMF template images raise errors — convert to PNG first.

**When editing XML directly (editing an existing deck):** unpack → edit `ppt/slides/slideN.xml` → repack; parse with defusedxml (ElementTree rewrites namespace prefixes and causes corruption); finish structural operations (adding/removing/reordering slides) **before** editing content; one `<a:p>` per list item, inherit bullets from the layout, never write a literal `•`.

**For paper/literature source material (hard-won lessons — violate and you redo the work):** figures already present in the paper (architecture / comparison / curves / attention / efficiency plots) must **always be cropped from the original**, never hand-drawn — render the full page with PyMuPDF to locate, `clip`-crop by the union bounding box of the figure elements (`matrix=fitz.Matrix(3,3)` ≈ 216dpi), visually inspect each one for clarity, then embed; add an in-slide citation under the figure (10pt italic: `Source: Author et al., Abbrev., Venue Year · Figure x`). For quantitative comparisons still prefer native charts (redraw table numbers as editable bar charts); only paste original-paper screenshots for figures PPT cannot express natively (architecture diagrams / bubble scatter / attention heatmaps); verify every number against the paper before it goes on a slide and record the table/figure number.

## §2 R2 · Template/Master Injection (distilled from pptx-from-layouts)

Core idea: **not overlaying text on a background image**, but reading the template's slide layouts and placeholders, then filling content by layout.

Flow: template profiling (enumerate all layouts and placeholder types/positions) → map each page's content to the most suitable layout → fill placeholder by placeholder (title placeholders get titles, body placeholders get body text, picture placeholders get images) → verify no placeholder is left unfilled.

- The page-level outline uses markdown with layout declarations: annotate each page with `Visual: cards-3 / process-3-phase / comparison-2 / table / hero-statement / data-contrast / timeline` etc.
- Layout selection order: process > comparison > parallel cards > data contrast > pull quote > table > big-statement conclusion > list (list is the last resort)
- Template slots ≠ number of content items: if the template introduces 4 people but there are only 3, delete the 4th person's entire group (image + text box), don't just clear the text
- When more than 30% of pages need changes, regenerate from scratch instead of patching page by page
- **Workflow**: first profile all of the template's layouts with a thumbnail grid (one annotated image per layout) before choosing layouts; a run only counts as done after validation passes (zero XML errors + zero overflow in rendered images); state every validation result in the delivery report

## §3 R3 · HTML-to-screenshot → PPTX (high-fidelity path with zero image-generation dependency)

Best for: formal decks with no editing requirements but demanding fine-grained visual control.

Flow: write a global CSS design system (CSS variables unifying colors / font sizes / spacing) → one HTML page per slide on a 1280×720 (or 1920×1080) canvas → full-page screenshots via a headless browser → assemble the PPTX from images page by page → write speaker notes into the notes.

- Advantage: layout capability = web layout capability (any font, grid, flex, gradients, shadows all available), fully deterministic, diffable, reusable themes
- Before screenshotting each page, use JS to check for content overflow (`scrollHeight > clientHeight` means overflow) — a natural QA advantage
- Render charts with ECharts/Chart.js and embed as screenshots likewise (the charts become inert, but visual quality beats native PPT charts — trade off as needed)
- The same HTML can also produce an online presentation version (a bonus deliverable)

## §4 R4 · AI Image Generation (distilled from deer-flow ppt-generation / codex-ppt)

For scenarios where impact comes first and an image-based PPT is acceptable. **Model-agnostic**: any available image-generation model works (GPT-image, Jimeng, SD, ImageGen, etc.) — use whatever the host environment provides. Style presets take their prompt hooks directly from style-library.md §4.

- **Sample-page confirmation gate**: produce 1 sample page for user confirmation first, then batch after approval (during batching, record how the sample was generated and reuse that for every page)
- **Chained consistency is the lifeline**: generate page by page serially, with page N using the finished page N-1 as the reference image; explicitly write "continuing EXACT visual style from reference image / SAME palette / SAME typography" in the prompt; **parallel generation is forbidden** (parallel = style collapse)
- The first image sets the global visual language and is the one most worth regenerating repeatedly until you're satisfied
- Prompts must be specific to the point of pathology: exact hex values, font sizes/weights, composition ratios, whitespace ratios, effect parameters ("backdrop blur 20px", "hard shadow 8px offset"); a vague prompt like "professional slide" = garbage output
- With sub-agent capability you can speed things up with a "one worker per page" parallel architecture, but only after the style-locked sample prompt is baked into every job — parallelism without a reference-image chain still collapses the style
- **Image-generation models render text unreliably**: be cautious with full-page image generation for text-dense content pages; title pages / section-divider pages / covers suit it well, body pages prefer R1/R3
- User-provided image assets (paper figures, logos, screenshots) are strict inputs: confirm the "which figure goes on which page" mapping before generating, and each must visibly appear in the results
- Image-based-PPT-specific QA: check every page for text hallucinations / typos / truncation — typos inside images cannot be edited away, only regenerated; local drawing / screenshot stitching is a failure mode, not a downgrade path; output images must come from the image-generation backend
- User-approved visual specs can be saved as a custom style (style-library.md §6) and reused for the same-named scenario next time

## §5 R5 · Marp/Reveal.js (Markdown slides)

- Marp: the lightest; `---` separates slides; `marp slides.md -o slides.pptx` converts straight to PPTX (image-based)
- Reveal.js / Slidev: HTML online presentations; strongest for code highlighting, animations, and interactivity; suits tech talks
- Positioning: speed first, developer audience, need for a shareable online link. The visual ceiling is limited by the theme — don't pick it for high-stakes occasions

## §6 R6 · LaTeX Beamer

- First choice for formula-dense content (math / theory / physics); widely accepted at academic conferences
- Structure: `\section` for sections, one frame per page, `\block` for blocks, `semiverbatim` for code
- Theme: Metropolis (modern minimalist) or a classic theme; use ctex for Chinese
- Draw figures precisely with TikZ — extremely high quality ceiling but high production cost
- Combine with R1: Beamer body + externally generated special figures via `\includegraphics`

## §7 R7 · SVG/Mermaid (vector diagrams)

- Method/framework/architecture/flow diagrams: generate with Mermaid (fast) or hand-written SVG (precise), then embed into any path's deck
- When embedding into PPTX, SVG must be converted to PNG (≥2x resolution); matplotlib is also an option (the academic-chart standard)
- Flow diagrams follow a left-to-right, top-to-bottom reading flow; uniform node corner radius, orthogonal connectors, palette subservient to the deck's primary color

## §8 R8 · image-to-editable-PPTX (distilled from nature-image2ppt)

Use this path when the input is an image-based PPT, scanned pages, course screenshots, or photos of someone else's deck, and the output must be editable objects.

Flow: **per-page region decomposition** → native redrawing → page-level QA → assembly → whole-deck QA.

- **Region decomposition**: split each page into 3–5 semantic regions (title / text / graphics / table / annotation), and decide the reconstruction method for each region independently
- **Native-first principle**: measurable circles, cards, solid/dashed line relationships, and simple connectors are always rebuilt as native shapes; only genuinely complex sub-figures (photos, complex illustrations) stay as bitmap assets, noted as "replaceable bitmaps" at delivery
- **Arrow Iron Rule**: thin arrows = one connector shape (arrow endpoints on the same object); solid arrows = one Arrow AutoShape (text inside the same object). **Forbidden**: assembling arrows from "line + triangle", and flattening an entire knowledge diagram into one big image
- **Text**: extract via OCR / image reading, then rebuild text boxes in the original style; map the observed font-size hierarchy to the canonical font sizes
- **Formulas are a hard gate**: formulas must be rendered with a formula engine (LaTeX→image or OMML); if the engine is unavailable, mark that page as failed and ask the user — never fudge it with a blurry screenshot
- **Page-level QA**: compare the rebuilt page's render side-by-side with the original (contact sheet); verify structural completeness, no missing regions, no new hallucinated elements; keep speaker notes from the original PPT (if any)
- Record the reconstruction method and asset provenance for every page; the final report notes which elements remain bitmaps

## §9 Speaker Notes Specification

- 80–120 Chinese characters (≈60–100 English words) per page; conversational, ready to read aloud verbatim
- Structure: one-sentence conclusion for this page → expanded explanation → transition into the next page
- R1 uses `addNotes()`; R3/R4 write notes during assembly; R5 uses presenter-notes syntax; R6 uses `\note{}`; R8 keeps the original notes

## §10 Known Pitfalls (all encountered and verified on real decks — just follow the fixes, don't reinvent)

| # | Symptom | Root Cause | Fix |
| --- | --- | --- | --- |
| 1 | Giant vertical/horizontal bars spanning the whole page, with absurd sizes (e.g. 9524 inches) | Mixing `Inches(float)` and `Inches(Emu(x))` causes double conversion | Use `Inches(float)` uniformly for all geometry; use `Emu` only for values read back from XML/EMU |
| 2 | Cropped paper figures come out with body paragraphs or page-margin rules attached | On two-column pages, body text sits within a few pt of the figures, and caption clustering merges the body-text rects in as well | Candidate rects must satisfy `r.x0 >= cap.x0-250 and r.x1 <= cap.x1+250` (strict containment filter); relax the left/right bounds to `min(box.x0-4, 55)` / `max(box.x1+4, pw-55)` to preserve full-width panels; a few pages (the two-column first page) can only be handled with a hard-coded `hard_clip` |
| 3 | Sub-labels below the caption (e.g. "Score Map of Layer 1") get cut off | The crop box's bottom took `box.y1`, but sub-labels sit between the caption and the figure | Always change the bottom to `cap_top - 1` (the caption's top edge); never use `box.y1 + 6` |
| 4 | Speaker notes never fit under the length limit; endless back-and-forth tweaking | Full-width CJK characters count for more in `len()` than the eye's sense of "length"; estimates skew optimistic | Iterate against the script's actual `print` output, not gut estimates; if the script reports `notes out of range: [(8,134),(9,122)]`, fix only those two pages |
| 5 | After editing and re-rendering, the output still looks the same | Reused stale PNGs | After every change, **re-run the full render chain** from the modified files — never reuse old images; before batch export, record the old images' hashes and compare after export |
| 6 | Exporting two pptx files back-to-back via PowerPoint COM — the second one fails with `RPC server unavailable` | Repeated Open/Close in the same process breaks the COM service | **One process exports one file** (one call per file); or `Quit` after export and `Dispatch` again |
| 7 | Chinese text in PowerPoint falls back to SimSun / the default font, mismatching what was set | Only `font.name` was set (writes `<a:latin>`); the East Asian font wasn't | Additionally write an `<a:ea typeface="...">` element per run; set it for both titles and body text |
| 8 | Images get stretched/distorted when placed into placeholder frames | Width and height were given directly | Use cover cropping (`pic.crop_left/right` or `crop_top/bottom`, computing offsets from the aspect ratio) or contain-style uniform scaling |
| 9 | Cards/images come with their own shadows, looking cheap | Theme default shadows were inherited | Explicitly set `shape.shadow.inherit = False` on every shape/image |
| 10 | "Lots of shapes were crammed in", yet the deck fails the visual-rich gate | Visual pages only count images/charts/tables; diagrams assembled from shapes don't count | Put in real evidence figures where evidence belongs; a pure-shape page must additionally carry a native chart or table to count as a visual page |
| 11 | The paper clearly has an architecture figure, but a self-drawn flowchart was put on the slide instead — gate G15 flags "original figure exists but was replaced by a self-made figure" | "Self-made figures" were treated as the default option | **If the paper has the corresponding figure, you must use it** (crop the PDF with `crop_paper_figs.py`); self-made figures are only for when the source material has no matching figure, and must be saved as a real image file + registered with `source_type=self-made` + `reason` + an in-slide "Source: self-made" label |
| 12 | The paper has 10 figures but only 5 were cropped — G15 reports "Figure 6/7 unused with no reason given" | The manifest `paper-figures.json` is generated by the script scanning PDF captions, not hand-picked | Either add the missing original paper figures, or write a substantive reason for each entry (≥8 Chinese characters ≈ a full English sentence) in `unused_figures_reason` in `deck-spec.json`; deleting the manifest file doesn't help — re-running the script regenerates it |

**Don't lazily reuse ready-made image files for cropped figures**: even if the source-material directory already contains `fig*.png`, re-crop them yourself from the PDF with `crop_paper_figs.py`, so that the sha256 values in `figures.json` map one-to-one to the original PDF and gate G10 can pass (figures of unknown origin are ruled "untrusted provenance" outright); the same run also produces `paper-figures.json`, an independent manifest of "which figures the paper originally had", which G15 checks against for missed figures.
