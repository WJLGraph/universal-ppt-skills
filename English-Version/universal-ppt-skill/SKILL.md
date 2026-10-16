---
name: universal-ppt-skill
description: Full-scenario presentation skill (academic / business / teaching / government / competition / everyday, with a built-in library of 30+ style presets). Use when the user needs to create a PPT, slides, deck or presentation — thesis defenses, literature-review presentations, lab-meeting talks, thesis proposals, mid-term reviews, project acceptance defenses, grant proposals, conference talks, seminars, performance reviews, work summaries, KPI reports, retrospectives, product launches, investor pitches, startup-competition decks (Internet+ / Challenge Cup), government and public-sector briefings, courseware, training, knowledge sharing, event decks — or to generate slides from papers / articles / reports / notes / outlines / images / screenshots, to improve, audit or refactor an existing deck, or to convert image-based decks back into editable PPTX. Covers the full five-stage chain "content decomposition → narrative design → visual system → multi-path rendering → QA-gated delivery". Rendering is model-agnostic with 8 selectable paths (R1-R8): native editable PPTX via python-pptx, template/master injection, HTML-to-screenshot, AI image generation (any model), Marp / Reveal.js, LaTeX Beamer, SVG / Mermaid, and image-to-editable-PPTX reconstruction. 7 of the 10 iron rules are machine-enforced by scripts/deck_qa.py (gates G1-G15): visual-page ratio ≥ 60%, per-page speaker-note length (bilingual), figure provenance via sha256, action titles, banned-phrase scans, and a paper-figure usage audit. Triggers: make a PPT, slides, presentation, deck, pitch deck, defense slides, paper-to-slides, courseware, keynote, image-to-PPT. Distilled from 17 open-source skills.
---
# universal-ppt-skill — Full-Scenario Presentation Skill

> Distilled from the best of 17 open-source skills: anthropics/pptx, codex-ppt, deer-flow (ppt-generation / academic-paper-review / systematic-literature-review), nature-skills (paper2ppt / image2ppt), academic-pptx, pptx-from-layouts, paper-to-course, PaperSpine, paperpipe, citation-check, academic-research-skills, AlterLab-FC-Skills, support-to-repro-pack, latex-writer, statistical-analyzer, grant-writer, survey-designer.

## 0. Iron Rules at a Glance (10 rules · recite before starting · verify one by one before delivery)

> **This section is the minimal memory set of the entire skill**; the long documents under references/ are only its expansion. The 10 rules below must be independently readable without extra context; 7 of them are **automatically enforced** by `scripts/deck_qa.py` — if the script fails, the deck may not be delivered.
> Overall principle (above the numbered rules): **narrative before layout** — argument structure → data → layout → aesthetics, and never in reverse. A deck's value lies in making one argument land, not in page count or effects.

1. **Two-phase rule** — First present the **page-level outline + 2-3 style candidates**, and start rendering only after the user confirms. If the user says "just give me the result", follow the downgrade protocol in §0.2; never skip silently. (Gate G12)
2. **Paper-figure-first rule** — If the source material **has** a matching figure, you **must use it** (paper decks: crop the original from the source PDF with `scripts/crop_paper_figs.py`, zoom ≥ 3; everyday decks: use images from docs/); **leaving out an original figure that exists in the source, or replacing it with a hand-drawn image / AI-generated image / icon / screenshot = violation**. Only when the material truly has no matching figure may you create one, and then ALL of the following must hold: ① it is a **real image file** before embedding (shape/block-assembled "diagrams" don't count) ② registered in `figures.json` with `source_type=self-made` + `reason` (≥ 8 Chinese chars / 20 chars in English, stating why the material has no matching figure) ③ the slide carries `Source: self-made`. Paper figures carry `Source: authors, Figure x`. (Gates G10/G11/G15)
3. **Every image must be traceable** — every image embedded into the deck is registered in `figures.json` (file path + PDF page + Figure label + sha256); `deck_qa.py` verifies the embedded bytes by hash and re-checks that every registered file exists on disk and hashes consistently. **Unregistered, mismatched, or missing file = "untrusted provenance"**; in academic mode, every figure page must also carry a `Source: …` caption. (Gates G10/G11)
4. **Visual-rich is a numeric gate, not an adjective** — visual page = contains at least one of **image / native chart / table**; ratio ≥ 60%, no 3 consecutive non-visual pages, and every content/data/table page carries ≥ 1 visual anchor (title/statement/closing/section/timeline pages are exempt). **Text boxes, colored blocks, rounded cards, and shape-assembled "diagrams" never count as visual pages** — even self-made figures must first become real image files (PNG / rendered SVG) before embedding; architecture/flow pages embed the paper's original figure or a self-drawn PNG, not shape collages. (Gates G5/G6/G7)
5. **Verify every number** — before any number goes on a slide, cross-check it against the source material and note the Table/Figure number; if it doesn't check out, don't write it.
6. **Speaker notes of 80–120 Chinese characters (≈ 60–100 English words)** — the script prints `len()` per page with language auto-detection and lists out-of-range page numbers; no printed output = QA not done. (Gate G2)
7. **QA evidence block is non-waivable** — delivery must include the **raw output** of `deck_qa.py` (with PASS/FAIL details); if the environment has no renderer, explicitly declare "rendered preview unavailable" — no vague hand-waving.
8. **Action-title gate** — every page title is a full claim sentence (not "Research Background"); reading only the title sequence must retell the whole argument. (Gate G13)
9. **Zero visual anti-patterns** — no decorative rule under titles, no full-width color bars, no one-side vertical stripes, no single-side card borders (top/left color bars included). Check every page against design-language.md §6.
10. **De-templatize** — ban template filler phrases in Chinese and English ("In one sentence / It is worth noting that / In summary / not X, but Y …" — list in design-language.md §7, scanned automatically by `deck_qa.py`). (Gate G9)

### 0.1 Rule tiers: check the tier first, then decide whether it is negotiable

| Tier | Meaning | Consequence of violation | Typical entries |
| --- | --- | --- | --- |
| **R0 Iron Rules** | Never broken by any model, any render path, any occasion | Rework immediately; not delivered | All 10 rules above |
| **G Hard Gates** | Machine-decidable; printed evidence required | Script FAIL = not delivered | Page count / note length / out-of-bounds / overflow / visual-page ratio / banned phrases / placeholders / image provenance hashes / confirmation gate / action title |
| **P Soft Preferences** | May be traded off by audience, but the trade-off must be stated | Record it; no rework | Color candidates, visual motif, breathing-page placement, font family |

When unsure which tier a rule belongs to, **apply the higher tier**.

### 0.2 Gate execution protocol (at the end of every stage; never skipped silently)

| Stage end | Required action | Required evidence |
| --- | --- | --- |
| After Stage 1 | Build the terminology ledger + claim list | Claim list (claim / evidence location / strength) |
| After Stage 2 | Send outline + style candidates to the user → **STOP-AND-WAIT** | The user's confirming words recorded verbatim into `work/deck-spec.json` `confirm_evidence` |
| After Stage 4 | For paper decks first run `python scripts/crop_paper_figs.py --pdf <paper.pdf> --out work/figs --manifest work/figures.json` (which also produces `work/paper-figures.json`, the paper-figure inventory); then run `python scripts/deck_qa.py <deck> --spec work/deck-spec.json --figures work/figures.json --paper-figures work/paper-figures.json --mode A --out work/qa_output.txt` | Paste the script output verbatim + the paper-figure inventory (which originals went on slides, which didn't and why) |
| After Stage 5 | Page-by-page visual inspection of renders + one fix per one re-check | Defect list (graded) + fix log |

Artifact conventions: `work/deck-spec.json` (mode / style / pages / confirmation evidence / `page_types` / `visual_ratio_min` / `unused_figures_reason`), `work/figures.json` (figure provenance manifest), `work/paper-figures.json` (paper-figure inventory, produced automatically by crop_paper_figs.py scanning the PDF captions — not hand-picked), `work/qa_output.txt` (raw QA output). These four files are the physical proof that "the rules were actually executed".

**Downgrade protocol (when the user says "I only want the final result / just do it / stop asking me")**: stop waiting turn by turn; instead, in **one message**, present the "page-level outline + 2-3 style candidates + which one I picked and why", then start rendering and finish Stage 4/5. If the user vetoes afterwards, **redo page by page — do not rerun the whole flow**. The only things that can never be downgraded are the R0 iron rules and the evidence blocks of the G-level gates.

### 0.3 Evidence-file field conventions (copy as-is; the script judges by these fields)

```jsonc
// work/deck-spec.json
{
  "deck": "itransformer_defense_deck.pptx",
  "mode": "A",                        // A-F, see §1 scenario routing
  "style_name": "Academic Restrained",
  "render_path": "R1",
  "pages": 10,
  "docs_dir": "./docs",               // source-material root; docs-asset figures for academic mode must live here
  "visual_ratio_min": 0.6,
  "outline_confirmed": true,          // did the user confirm the outline? (gate G12)
  "style_confirmed": true,            // did the user confirm the style? (gate G12)
  "confirm_evidence": "User's exact words: OK, go with this outline",   // ≥ 8 CJK chars / 20 latin chars; quote the user verbatim, never invent
  "page_types": ["title","content","content","content","content","data","data","data","content","closing"],
  // account for every paper figure: every unused Figure needs a reason, otherwise G15 FAILs
  "unused_figures_reason": {
    "Figure 6": "Pure hyperparameter-sensitivity curves, redundant with Figure 5; the space goes to the mechanism page",
    "Figure 8": "Appendix visualization, not discussed in the main text"
  }
}
// work/figures.json — written automatically by crop_paper_figs.py; self-made figures must also be registered (with sha256 and reason)
{
  "figures": [
    {"file":".../fig4_overview.png","source_type":"pdf-crop","origin":".../iTransformer.pdf",
     "page":4,"label":"Figure 4","name":"fig4_overview","sha256":"...","size_px":[1506,523]},
    {"file":".../self_made_pipeline.png","source_type":"self-made",
     "origin":"R7 self-drawn (SVG→PNG)","reason":"The paper has no figure for this three-stage deployment pipeline, so it was self-drawn and the source is labeled on the slide",
     "name":"self_made_pipeline","sha256":"...","size_px":[1600,900]}
  ]
}
// work/paper-figures.json — produced automatically by crop_paper_figs.py scanning the PDF captions; not hand-picked
{"origin":".../iTransformer.pdf",
 "items":[{"label":"Figure 1","kind":"Figure","page":1,"caption":"Overall framework of iTransformer ..."}]}
```

`deck_qa.py` verifies: the spec page count matches the actual deck, the `page_types` length equals the page count, every embedded image's hash is found in `figures.json` (and every registered file really exists and hashes consistently), academic mode accepts only `pdf-crop` / `docs-asset` inside docs_dir / documented `self-made`, and **every Figure in the paper inventory is either on a slide or excused in `unused_figures_reason` (G15)**.

## 1. Scenario routing (decide the mode first, then design pages)

| Mode | Trigger scenarios | Narrative skeleton | Visual tone |
| --- | --- | --- | --- |
| **A. Academic Argumentation** | literature review presentations, lab meetings, thesis proposals, mid-term reviews, project acceptance defenses, thesis defense, grant/project proposals, conference talks, seminars | problem → method → evidence → contribution → limitations (structured argument; sub-scenario variants in narrative-patterns.md) | Academic Restrained / Research Defense: white background, single font family, ≤ 3 colors |
| **B. Business Reporting** | project reports, performance reviews, work summaries, KPI reports, retrospectives, pitches, product launches, investment promotion, review boards | BLUF (conclusion first) → evidence → action items | Clean Professional / McKinsey / Data Dashboard / Keynote, chosen by audience |
| **C. Teaching & Explanation** | courses, training, public lectures, paper-to-course, knowledge sharing | cognitive-load progression: what → why → how → practice | Teaching Courseware / Hand-drawn Whiteboard / Hand-drawn Tech Explainer: large type, diagram-heavy |
| **D. Everyday Expression** | event planning, travel sharing, memorial albums, club recruiting, book clubs | emotional narrative: timeline / themed medley | Free Visual: high expressiveness allowed |
| **E. Government & Public Sector** | agency work reports, themed study sessions, policy briefings, party-building activities, annual summaries, SOE/public-institution reports | overall situation → key practices → outcome data → problems & gaps → next steps | Government Red: red + gold/white, formal and orderly, symmetrical structure |
| **F. Competition Pitch** | Internet+ / Challenge Cup / college innovation programs, startup contests, investment promotion | pain point → solution → technical moat → market → business model → team → roadmap | Gradient Modern / Dark Premium / Keynote: impact first |

**When the mode is ambiguous, default to A (academic)**; if the user mentions a paper / research / data / defense, it is almost always A; government / SOE / public-institution reports are E; competitions / pitches / investors are F.

The full style selector and the 30+ style specs live in references/style-library.md (required reading at Stage 3).

Academic mode requires a further decision on the **material type** (manifest routing distilled from nature-paper2ppt):

- `discovery` finding/mechanism type → problem → evidence arc (default)
- `methods` method/algorithm/tool type → problem → solution arc
- `resource` dataset/benchmark/resource type → workflow → validation arc
- `clinical/materials` experimental/engineering type → design → inference arc
- `review` review/opinion type → evidence-map arc

State the routing result in one sentence so the user can correct it cheaply.

## 2. The Five-Stage Workflow

### Stage 1 · Source decomposition (understand it)

Read and structure the source material according to the scenario:

- **Papers / literature**: extract metadata (title / authors / venue / year / field) → deep-read each section → build the claim list (each claim: statement + evidence location + strength Strong/Moderate/Weak). Dimensions: research background, scientific problem, method framework, experimental design, key results, innovations, limitations & implications. Add related-work context where needed (multi-paper synthesis in references/narrative-patterns.md §4).
- **Articles / reports / notes**: extract core claims, key data, cases, conclusions and action items.
- **Vague requests (one sentence only)**: first ask about audience, occasion, duration, page count, style constraints, and template availability — bundle the questions, don't drip-feed them.
- **Existing decks (audit / improvement)**: do a content inventory first (per-page titles + point extraction), output a diagnosis (which pages change, how), and act only after confirmation.

**Terminology ledger**: build it while reading; model names / datasets / metrics / acronyms stay verbatim-identical across all pages and speaker notes.

### Stage 2 · Outline design (make the argument land)

Produce a **page-level outline**; every page carries: action title (claim-style title) + page type + core content + suggested visual elements. Then run two gates:

- **Action-title gate**: titles must be full claim sentences — not "Research Background" but "Existing methods are unstable in low-sample regimes". Good/bad examples in references/narrative-patterns.md §1.
- **Ghost-deck test**: read only the action titles in sequence; they must retell the complete argument on their own. If the story doesn't flow, fix the outline — not the wording.

**The outline must be confirmed by the user before rendering starts.** After sending the outline, **stop and wait** (STOP-AND-WAIT): without explicit user confirmation ("OK / go with this / continue") rendering may not start; record the confirming words verbatim into `work/deck-spec.json` `confirm_evidence` (checked by gate G12). Page-structure templates per scenario (academic literature review / proposal / mid-term / acceptance / defense, business, teaching, everyday, government, competition) are in references/narrative-patterns.md. Prompt templates: prompts/stage-prompts.md Templates 1/2.

### Stage 3 · Visual system (pick a style first, then set specs)

**Step one: pick the style (style confirmation gate — never decide unilaterally)**: open references/style-library.md §1 (the selector), offer **2-3 candidate styles per scenario + a one-line recommendation for each + your pick**; lock it only after user confirmation (the user's brand colors / school template colors always win). Write the candidates and the confirmation into `work/deck-spec.json` (`style_name` + `style_confirmed` + `confirm_evidence`).

Before rendering, set the per-deck **visual spec** (written into deck-spec):

- **Color**: one primary color carrying 60-70% of the visual weight + 1-2 supporting colors + one sharp accent. Refuse default blue; refuse saturated pile-ups. Academic default: deep navy `1F4E79` + mid blue `2E75B6` + white background.
- **Fonts**: a single family; hierarchy comes from size/weight (titles 24-44pt bold / body 14-20pt). CJK academic: Source Han Sans / Microsoft YaHei; English decks: Helvetica / Arial / Inter or the venue's standard family. Body minimum 14pt; readable from the back row needs ≥ 18pt.
- **Layout**: one grid and consistent margins (≥ 0.5"), one focal point per page, whitespace is a capability not a waste. Commit to one visual motif across the deck (rounded image frames / colored circular icon chips etc.), but **forbidden**: colored decorative rules under titles, full-width color bars, one-side vertical stripes — these are the fingerprints of the "AI look".
- **Charts** (top-journal standard): thin lines, low saturation, key data labeled directly, few gridlines, no 3D or shadow piles; red for gains, green for losses (Chinese-market convention).
- **Breathing room**: alternate information density (dense → sparse → dense); insert a breathing page (big-claim page / section divider / empty-scene page) between two consecutive high-density pages. Page-level motion settles calmly; reject fast-and-jumpy.
- **Visual-rich iron rule (R0, applies to every render path; violators rework; gates G5-G7/G15)**: a visual page = contains at least one of **image / native chart / table**; **text boxes, colored blocks, cards, and shape-assembled "diagrams" never count** (this is the most commonly gamed loophole — don't fool yourself). Requirements: visual pages ≥ 60% of total; no 3 consecutive non-visual pages; every content/data/table page carries ≥ 1 visual anchor (title/statement/closing/section/timeline exempt). Execution per path: R1 carries quantitative comparisons with native charts, evidence with images, and architecture/flow pages **embed the paper's original figure or a self-drawn PNG directly** (shape collages don't count as anchors); R3/R4 satisfy it naturally. **If the source material has the figure, use it**: every Figure of a paper deck either goes on a slide or gets a reason in `work/deck-spec.json` `unused_figures_reason` — "the original has a figure but I substituted a self-drawn one" is not allowed. The final deck must be judged by `deck_qa.py`; "looks rich enough to me" is not evidence.

The full design language and anti-pattern list: references/design-language.md.

### Stage 4 · Multi-path rendering (build it)

**Pick the path first, then write code / generate images.** The full decision tree and implementation notes for the 8 paths: references/render-paths.md. Quick reference:

| Path | One-liner | When to pick |
| --- | --- | --- |
| R1 Code-generated native PPTX | build page by page with pptxgenjs / python-pptx | needs **editable** output, native charts, formal delivery |
| R2 Template/master injection | read template layouts + placeholders, fill by layout | hard constraint of a school/corporate **template** |
| R3 HTML→screenshot→PPTX | typeset in HTML/CSS, full-page screenshots, assemble | max **visual freedom**, no per-character editing needed, zero image-gen dependency |
| R4 AI full-page images | any image-generation model, page by page (consistent reference chain) | impact first, image-style PPT acceptable |
| R5 Markdown slides | Marp / Reveal.js / Slidev | developer-oriented, HTML online presenting, fastest |
| R6 LaTeX Beamer | formula-dense academic talks | math/theory settings, rigorous typesetting |
| R7 SVG/Mermaid vector diagrams | generate diagrams/flowcharts, then embed | method frameworks, architecture diagrams, relationship maps |
| R8 Image→editable PPTX | reconstruct images / screenshots / image-style PPT into native objects | input is an image-style deck, scanned pages, screenshots; editability required |

Paths are combinable (e.g. R1 body + R7 flowchart + R3 cover). If the host environment already has an official PPT skill, prefer delegating the file-level operations of R1/R2 to it; this skill owns the spec and the QA.

### Stage 5 · QA & delivery (the last line of defense)

After rendering, **run the script gates first, then do the human visual pass** — order never reversed; details in references/qa-gates.md:

0. **Script gates (non-skippable)**: for paper decks first `python scripts/crop_paper_figs.py --pdf <paper.pdf> --out work/figs --manifest work/figures.json` (which also produces the paper-figure inventory `paper-figures.json`), then `python scripts/deck_qa.py <deck> --spec work/deck-spec.json --figures work/figures.json --paper-figures work/paper-figures.json --mode A --out work/qa_output.txt`. Any FAIL: fix until all PASS; paste the raw script output verbatim into the delivery notes (gates G1-G15).
1. **Content QA**: check page by page for text truncation, terminology-ledger consistency, leftover placeholders, citation completeness; speaker-note lengths (80–120 CN chars / 60–100 EN words) already printed by the script; for paper decks verify **every original paper figure is used** (cross-check `paper-figures.json`; anything not on a slide must already be explained in `unused_figures_reason`), in-slide citations complete, and `figures.json` has no unregistered images.
2. **Visual QA**: render to images and inspect page by page (text overflow → element overlap → alignment → margins → contrast, in that priority), defects graded high/medium/low; the first version almost always has overflow/overlap — fix one version, re-check one version, stop after two clean passes. Without a renderer, follow the degraded procedure in qa-gates.md for programmatic checks and **explicitly declare "rendered preview unavailable"**.
3. **Provenance QA**: for academic/data decks, verify every key conclusion against the source (the "two-pass method": claim list confirmed first, then verified); citation style consistent (GB/T 7714 / APA / IEEE as needed).

Every page carries 80-120 Chinese characters (60-100 English words) of speaker notes. Deliver with present_files, and attach the **delivery evidence block** per references/delivery-template.md (pages / mode / style / render path / raw QA output / provenance of every image / rendered-preview availability / known limitations / change log).

## 3. Cooperating with other skills

- Single-paper deep review → Stage 1 already internalizes the core dimensions; pair with an academic-paper-review-style output when a full conference-grade review report is needed.
- Multi-paper systematic review → beyond 5 papers, cluster by theme to extract convergences / disagreements / gaps instead of listing paper by paper.
- Paper-reproduction reports → add the four-piece set: environment dependencies, run commands, gotchas, reproduction-result comparison.
- User-research / survey content → fold questionnaire-design essentials (question types / Likert scales / skip logic / pilot testing) into the Stage 1 decomposition dimensions.

## 4. Reference-file index (load on demand — do not read everything at once)

| File | Contents | When to read |
| --- | --- | --- |
| **scripts/deck_qa.py** | **Gate script: page count / note length / out-of-bounds / overflow / visual-page ratio / banned phrases / placeholders / image provenance hashes and ledger consistency / confirmation gate / action title / paper-figure usage audit (G1-G15), all machine-decided** | **Must run after Stage 4 rendering and before Stage 5 delivery (non-skippable)** |
| **scripts/crop_paper_figs.py** | **Paper-figure cropping: locates figures by caption, crops them hi-res from the PDF, writes the figures.json provenance ledger, and scans the PDF captions to produce paper-figures.json (what figures the paper originally has)** | **Must run at Stage 4 whenever a paper deck needs figures** |
| references/narrative-patterns.md | Page-structure templates for the six scenario families (proposal / mid-term / acceptance / competition / government included), action-title craft, multi-paper synthesis method | Stage 2, when designing the outline |
| references/style-library.md | Style selector, 30+ style specs (academic / practical / modern-expressive families), classic palettes, style engineering rules | Stage 3, when picking a style (required) |
| references/render-paths.md | Implementation details of the 8 render paths, decision tree, per-path engineering pitfalls | Stage 4, before rendering |
| references/design-language.md | Color / font / layout / chart specs, text budgets, AI-look anti-pattern list, breathing rules | Stage 3, when setting visuals |
| references/qa-gates.md | Item-by-item checklist of the three QA passes, severity grading, common defect examples, provenance verification method | Stage 5, before delivery |
| references/delivery-template.md | Delivery evidence-block template (non-waivable + optional items), fill in the blanks | Stage 5, at delivery |
| prompts/stage-prompts.md | Reusable prompt templates (source → outline, outline → deck, audit, R8 reconstruction…), each stage with STOP-AND-WAIT checkpoints | Any stage, when a template is needed |

**Confirm dependencies before running the scripts**: `python -c "import pptx, fitz"`; install whatever is missing (`pip install python-pptx PyMuPDF`). Script errors must never be bypassed — an error itself means "environment not ready, QA not done".

## 5. Quick reference: standard 12-page academic literature-review structure

1 Title · 2 Research background · 3 Scientific problem & motivation · 4 Related work & gaps in existing methods · 5 Core idea · 6 Method framework · 7 Experimental design · 8 Key results I · 9 Key results II · 10 Ablation / deeper analysis · 11 Innovations & contributions · 12 Limitations, implications & discussion

10-page version: Title → Background & problem → Related-work gaps → Core method → Method details → Experimental setup → Key results → Ablation analysis → Contributions & limitations → Summary & discussion.

Other high-frequency scenarios at a glance (full templates in narrative-patterns.md §2):

- **Thesis proposal**: topic background & significance → literature review & research gap → research content & scientific questions → research plan / technical route → innovations → schedule → expected outcomes
- **Thesis defense**: significance of the topic → research content & innovations (the centerpiece) → key work & results → conclusions & limitations
- **Competition pitch**: pain point → solution → technology & moat → market & business model → team → roadmap & the ask
- **Government report**: overall situation → key practices → outcome data → problems & gaps → next steps

**Timing conversion**: lecture-style ≈ 1-1.5 min/page (10 min ≈ 8-12 pages); defense-style 1 min/page (15 min ≈ 15 pages); pitch-style is faster at ~40 s/page. When page count is unspecified, estimate this way and tell the user.

## 6. The 30-second recital before starting & the 30-second recital before delivery (against long-context amnesia)

**Before starting, recite**: ① the outline goes first and waits for confirmation; ② **if the source material has a figure, the original figure must be used** (crop paper figures from the PDF and register them in the ledger; only self-create when no matching figure exists — and a self-created figure is still a real image file + registered reason + "Source: self-made" caption); ③ visual page = image / chart / table; shapes and colored blocks don't count; ④ speaker-note length (80-120 CN chars / 60-100 EN words) is counted by the script, not by feel.

**Before delivering, recite**: ① was `deck_qa.py` run, are all FAILs cleared (paper decks must pass `--paper-figures`); ② is the evidence block attached (including the "rendered-preview availability" declaration + paper-figure usage); ③ does every image have a page + Figure label (self-made marked "Source: self-made"); ④ do the titles alone retell the argument.

**The four most common failure roads (don't take them)**: skipping the confirmation gate and rendering directly → leaving out an original figure that exists, or substituting AI images / diagrams for paper figures → dressing up text-only pages with shapes and colored blocks to "look visual" → paper figures without in-slide citations or ledger registration.

**Read-back order**: Stage 1→2 read narrative-patterns.md; Stage 3 read style-library.md + design-language.md; Stage 4 read render-paths.md (§10 known pitfalls included); Stage 5 read qa-gates.md + delivery-template.md. **Whenever unsure at any stage, return to the 10 iron rules in §0.**
