# Design Language Specification (loaded on demand at Stage 3)

> Tone: restraint, thin lines, low saturation — top-journal aesthetics. Decoration is part of the information hierarchy; it never exists for its own sake.

## §1 Color System

**60-30-10 rule**: the primary color carries 60-70% of the visual weight, with 1-2 secondary colors and exactly one accent color (reserved only for the most critical data/conclusion).

Academic default: deep navy `1F4E79` (primary) + medium blue `2E75B6` (secondary) on a white background; citations/annotations in low-saturation gray `595959`.

Low-saturation reference palettes (choose by theme; do not default to blue):

| Theme | Primary | Secondary | Accent |
|------|-----|-----|------|
| Navy Academic | 1F4E79 | 2E75B6 | C00000 |
| Forest Natural | 2C5F2D | 97BC62 | 8B5E3C |
| Terracotta Warm | B85042 | E7E8D1 | 6B8F71 |
| Charcoal Minimal | 36454F | F2F2F2 | 212121 |
| Berry Elegant | 6D2E46 | A26769 | 2F3C7E |

Red lines: large expanses of high-saturation color blocks; more than 3 hues on one page; overuse of red-green or cyan-purple gradients; one color per bar in a chart (same-category data uses shades of the same hue family).

## §2 Typography & Hierarchy

- One font family; hierarchy comes from size/weight: titles 24-44pt bold, section headings 20-24pt, body 14-20pt, annotations 10-12pt gray
- Chinese: Source Han Sans / Microsoft YaHei / PingFang; Source Han Serif can be used for titles to create contrast. Monospace for code/formulas: JetBrains Mono
- **CJK + Latin dual-family rule** (Nature style, at most two families): Chinese uses the primary family; English/numbers/model names/DOIs may pair with one Latin companion font (e.g., Arial/Calibri) for a crisper look
- **Safe font list** (QA render widths trustworthy, bundled with Office): Arial, Calibri, Cambria, Times New Roman, Courier New, Bookman Old Style, Century Schoolbook. **Not QA-trusted** (substitute fonts have different widths; reserve a 10% width margin): Georgia, Trebuchet MS, Impact, Arial Black, Garamond, Consolas, Palatino Linotype. **Never default to Aptos** (missing in older Office versions + unreliable in QA on both ends)
- Body text minimum 14pt; ≥18pt when it must be readable from the back row of a formal meeting room; body ≥20pt for thesis defenses / large-lecture-hall presentations
- Left-align body text (lists are always left-aligned); center only titles and axis labels
- Line budget: no more than 5 body bullets per page, each bullet at most 1.5 lines

## §3 Layout & Breathing-Room Rules (B1-B6)

- B1 **One focus per page**: every page has exactly one visual anchor (one chart / one set of numbers / one claim)
- B2 **Density alternation**: arrange information density in a dense→sparse→dense rhythm; insert a breathing page (big-text conclusion / section-divider page) between two high-density pages
- B3 **Constant margins**: unified ≥0.5" margins; block gaps uniformly 0.3" or 0.5", never mixed
- B4 **Whitespace is content**: 40%+ whitespace is where the premium feel comes from; "filling every inch" is the mark of failure
- B5 **Consistent visual motif**: pick one element (rounded cards / circle-base icons / a specific graphic language) and reuse it across the whole deck
- B6 **Opening-closing echo**: the cover and the closing page share the same compositional language, forming a closed loop

Page layout library (choose per content; don't repeat):
two columns (text left, figure right) · icon + text rows · 2×2/2×3 card grid · half-bleed large image · big-number callout · before/after two-column comparison · horizontal timeline · process step bar · pull-quote page.

**Five composition types** (for results/argumentation pages, choose by evidence shape; using one type across the whole deck is forbidden):
- `figure-dominant`: the figure takes 60-75% of the canvas; text is compressed into a narrow track or a bottom strip
- `process-wide`: a workflow spans the full page width + small labels
- `claim-led`: one strong claim + 2-3 supporting fragments; no fake filler cards
- `comparison`: table/chart or dual evidence blocks + one conclusion line
- `discussion`: sparse layout + a few sharp prompts; no dense bullet packing

**Layout adaptation rule** (never default to a 50/50 left-right split): choose the layout by the figure's aspect ratio, density, and role — wide figures / primary evidence get full-width or near-full-width; portrait figures pair with a narrow text track; prefer asymmetric splits of 70/30, 75/25, 65/35; for dense figures, crop the most relevant panels — rather split across two pages than shrink to unreadable size. Equal 1:1 weighting is the exception, not the norm.

**Page fullness** (prevents "a lone word dangling in a corner"): most pages should follow a three-band structure — "top anchor (title zone) + central dominant block + bottom anchor (conclusion strip / source strip)"; when whitespace feels insufficient, first add an evidence-support layer (metric chips, a compact interpretation band, a source strip) rather than decoration.

**Alignment rails**: establish a small set of visual rails (title left edge and baseline, figure left/right edges, interpretation-track edge, bottom annotation-band baseline); every object is either precisely aligned or clearly offset — a few pixels of "approximate alignment" look worse than a deliberate offset. Before delivery, sweep the trailing annotations/footers for a shared baseline, and check that figures and source labels have a visible attribution relationship.

## §4 Text Budget (amounts to check your own writing against, distilled from nature-paper2ppt)

Write "slide text", not "speaker-script text"; all explanation goes into speaker notes:

| Element | Cap |
|------|------|
| Title | One line preferred; two lines only when vertical space is ample |
| Ordinary-page bullets | 2-3 bullets, each ≤18 Chinese characters or 8-10 English words |
| Results page | 1 short interpretation sentence + at most 2 compact callouts |
| Card body | 1 sentence, usually ≤24 Chinese characters |
| Metric labels | One line whenever possible |
| Source attributions | Small type, short phrases; never compete with the figure for attention |

If it doesn't fit, split the page or move it into speaker notes; **never cram by shrinking the font size**.

## §5 Chart Specification (top-journal grade)

- Thin lines (≤1.5pt), low-saturation palette, remove excess gridlines (keep only very faint horizontal gridlines)
- **Directly label** key data points (data labels / arrow annotations) so readers never hunt for the legend
- Chart titles state the conclusion ("Method X leads on metric Y by 12%"), not the metric name
- Draw error bars / confidence intervals truthfully; sample sizes and significance annotations complete
- **Red for gains, green for losses (Chinese-market convention)**; currency defaults to ¥
- One exhibit per page; tabular data stays a table — never force it into a chart

## §6 AI-Flavor Anti-Pattern Checklist (any occurrence triggers rework)

> In this checklist, "same layout on every page / pure-text pages / shapes posing as visual pages" are machine-checked by G5-G7 in `scripts/deck_qa.py`; decorative lines, color bars, vertical stripes, and one-sided outlines must be scanned page-by-page against this list by a human (the script cannot catch them).

- ❌ Colored decorative lines / horizontal rules under titles
- ❌ Color bars spanning the top/bottom of a page, one-sided vertical stripes, one-sided card outlines (including left color bars / top color bars)
- ❌ Same layout on every page (title + three bullets all the way through)
- ❌ Default blue + default Office theme colors
- ❌ Cream/beige default background (use pure white or a brand color when unspecified)
- ❌ Seas of decorative icons; illustrations unrelated to the content
- ❌ Text overflowing its container; elements overlapping each other
- ❌ Body paragraphs that are all center-aligned
- ❌ Charts left bare by default (no title, no data labels, dated palette)
- ❌ A "Thank You" closing page (end with a conclusion page instead)

## §7 De-Templating Wording (mandatory check for academic/formal decks, distilled from nature-paper2ppt)

> The phrases below are auto-scanned by G9 in `scripts/deck_qa.py` (covering titles, bullets, conclusions, and speaker notes); any hit is an instant FAIL — no need to hunt for them by eye.

The following "AI-flavor phrases" are **banned** from titles, bullets, conclusions, and speaker notes (unless quoting the original text):

> In one sentence: · the most valuable direction for future work · not X, but Y · not just X, but more importantly Y · it is worth noting that · in summary · in a sense · provides a new perspective · is of great significance · future work could further explore

Replacement principle: if a sentence would still hold when dropped onto any other paper/project, it must be rewritten — name the specific method, dataset, mechanism, chart evidence, or limitation.

```text
Weak: In one sentence: this method is of great significance.
Good: This method splits retrieval, evidence completion, and answer generation into an auditable pipeline, reducing the risk of missing key literature.
Weak: This is not a mere performance gain, but a paradigm shift.
Good: Ablations show the active-retrieval module mainly improved the answerable rate on long-tail questions.
```

Template flavor at the layout level (check these too): equal-thirds cards + icon bars, uniform metric pills, the same right-side interpretation track on every page, nested fake dashboard cards, uniform boxes that ignore evidence shape. **Sweep the slide-sorter thumbnails once: if 5+ pages share the same composition, some of them must be restructured**.

## §8 Visual Spec Card (Stage 3 deliverable template)

```yaml
deck: <topic>
mode: A-Academic/B-Business/C-Teaching/D-Casual/E-Government/F-Competition
style: <style name, from style-library.md or custom>
canvas: 16:9 (13.33×7.5 in)
palette: {primary: "#", secondary: "#", accent: "#", bg: "#", text_muted: "#"}
typography: {heading: "<font> 28-40pt bold", body: "<font> 16-18pt", mono: "<font>"}
motif: <visual motif in one sentence>
spacing: {margin: 0.5in, gap: 0.3in}
chart_style: thin lines / low saturation / direct labels / red for gains, green for losses
render_path: R1-R8 and combinations
notes_policy: 80-120 chars (CN) / 60-100 words (EN) per page
```
