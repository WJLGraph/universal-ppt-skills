# Narrative Patterns Library (loaded on demand in Stage 2)

> **The page-level outline produced from this file must be confirmed by the user (Hard Gate G12)**: after outputting the page-level outline + the action-title chain, STOP-AND-WAIT; record the user's confirmation verbatim in `confirm_evidence` inside `work/deck-spec.json`. Starting rendering without confirmation = workflow violation.

## §1 How to Write Action Titles (distilled from academic-pptx)

A title = a complete conclusion sentence, so that someone who reads only the titles can follow the whole argument.

| ❌ Section-name style | ✅ Conclusion style |
|-----------|---------|
| Research Background | Existing methods struggle to maintain stable performance in low-sample scenarios |
| Experimental Results | The proposed method outperforms existing baselines on all three datasets |
| Method Framework | The two-stage optimization framework reduces training instability |
| Market Analysis | Lower-tier markets are the primary growth driver for the next three years |
| Project Progress | Phase 1 delivery exceeded expectations; Phase 2 risk is concentrated in the supply chain |

Note: in Business / Teaching / Everyday modes, the title page and section-divider pages may use phrase-style titles, but content pages should still be conclusion-style whenever possible.

## §2 Page Structure Templates by Scenario

### A. Academic Argumentation (12-page standard version / 10-page compact version: see SKILL.md §5)

Per-page spec: the title page carries the paper title / venue / presenter; results pages = figure on the left, interpretation on the right (chart on the left, interpretation bullets on the right), one exhibit per page, with key findings annotated directly on the chart ("so what" notes); the last content page must be a conclusions page (not "Thank you" — the conclusions page stays on screen to carry the Q&A); References get their own page. Decks over 15 pages add section-divider pages or a breadcrumb bar.

**Original paper figures first (Hard Gates G10/G11/G15)**: the core evidence of a literature review presentation is the paper's own figures — **any Figure that already exists in the paper must appear on a slide**, cropped from the PDF with `scripts/crop_paper_figs.py` and embedded as-is (do not substitute hand-drawn shapes or color blocks for architecture or flow diagrams); for figures that genuinely don't fit or don't apply, list them one by one in `unused_figures_reason` in `deck-spec.json` (a reason of at least 8 words). On each paper-figure page, mark the source inline as `Source: authors · Figure x`. Self-made figures not present in the source material (e.g., "a diagram relating this work to the broader topic") may be drawn, but they must be saved as real image files, registered in `figures.json` with `source_type=self-made` + `reason`, marked on-page as `Source: self-made`, and must not outnumber the original paper figures used on slides.

**Academic sub-scenario variants** (distilled from the codex-ppt research-defense style):

- **Thesis proposal**: 1 Cover (topic title / candidate / advisor) · 2 Background and significance of the topic · 3 Literature review and research gap · 4 Research content and scientific questions · 5 Research plan and technical route (key page, with a roadmap diagram) · 6 Feasibility analysis · 7 Innovations · 8 Schedule (Gantt / timeline) · 9 Expected outcomes · 10 References. Reviewers care about "whether the topic is well justified + whether the plan is feasible"; a clear technical-route diagram and visible workload are bonus points.
- **Mid-term review**: 1 Cover · 2 Project recap (original plan in one sentence) · 3 Overall progress comparison (planned vs. actual, table or Gantt) · 4 Completed work ① ② (with interim data / charts) · 5 Interim outputs (papers / patents / systems) · 6 Problems and cause analysis · 7 Adjustment plan · 8 Next steps · 9 Expected outcomes at project completion. The core is "report progress against the plan" — don't dodge problems, but always pair them with countermeasures.
- **Project acceptance defense**: completion status vs. research objectives → main research achievements (ranked by contribution) → deliverables list (papers / patents / software copyrights / applications) → budget usage (if required) → innovation summary → future outlook.
- **Grant/project proposal defense**: rationale (importance and gap) → research objectives and scientific questions → research plan and technical route → research foundation and team (prior results proving feasibility) → budget and schedule → expected outcomes and impact. Reviewers by default doubt "can this actually be delivered" — answer with the research-foundation page.
- **Thesis defense**: 1 Cover · 2 Background and significance of the topic · 3 Overview of research content (thesis structure) · 4-8 Key work chapters (one page per chapter, core: method → results) · 9 Innovations (the centerpiece, capped at 3) · 10 Conclusions and limitations · 11 Publications during the degree · 12 Acknowledgments (may be merged). The defense weighs "what did I do and what's new about it"; compress the literature review to 1 page or less.

### B. Business Reporting (8-12 pages)

1 Cover (topic + one-sentence value proposition) · 2 Conclusion-first page (BLUF: 3 core conclusions) · 3-6 Argument pages (one point + data support per page) · 7 Risks and countermeasures · 8 Action items (owner / deadline) · 9 Resource requirements · 10 Appendix index. Data pages use big-number callouts (60-72pt number + small label); comparison pages use a two-column left/right layout.

**Business sub-scenario variants**:

- **Performance review / work summary**: recap of responsibilities and goals → key work and achievements (3-4 items, quantified) → data overview (big-number KPI page) → problems and reflections → next-phase plan.
- **Retrospective**: goal recap → results comparison (visualize the gaps) → cause analysis (layered subjective / objective) → lessons and action items.
- **Product launch / keynote**: suspenseful opening (trend / pain point) → one-sentence positioning → three killer features (one full-bleed visual per feature) → live demo page → ecosystem / partnerships → pricing and availability → closing vision.

### C. Teaching & Explanation (pages = number of knowledge points × 2)

Three pages per knowledge point: concept page (what it is: diagram + one-sentence definition) → principle page (why: contrast / analogy / formula breakdown) → application page (how to use: example + quick practice). Add a learning-objectives page at the start and a summary + quiz page at the end. For formula-dense content, use the "line-by-line breakdown" layout: formula on top, with each symbol annotated with its meaning below (distilled from paper-to-course's Formula Breakdown).

**Slide-type quick reference for courseware** (distilled from paper-to-course's slides-config; map directly when generating data-driven): title / outline / content (bullets · cards-2/3/4 · steps · grid-2x2) / flow / table (supports highlighted rows) / bars / stats (big numbers) / formula / timeline / summary / limitations (two-column). Well suited to being turned into a config so the builder can batch-produce pages.

### D. Everyday Expression (6-15 pages)

Timeline style (travel / event recaps: one highlight moment per page) · themed medley style (albums / commemorations: one theme + short caption per page) · proposal style (event planning: current state → ideas → plan → division of labor → budget). Highly expressive visuals are allowed, but "one focus per page" still applies.

### E. Government & Public Sector (8-15 pages)

1 Cover (red key visual, solemn) · 2 Overall situation (background and general requirements) · 3-6 Main practices (split into blocks: Party-building leadership / core operations / workforce building, etc., one page per block, with neatly parallel sub-headings) · 7 Results data (let the data speak, moderate big numbers) · 8 Problems and shortcomings (candid but restrained, 1 page) · 9 Next-step work plan (bullet items, verb-first). Style: government/party red; headings favor parallel phrasing ("focus on X, deliver Y" pattern); charts use red-flag / bar-chart motifs with a gold-red palette; overall orderly and symmetrical, with minimal flashy graphics.

### F. Competition Pitch (10-14 pages, distilled from the pitch scenario)

1 Cover (project name + one-sentence positioning) · 2 Pain point (real scenario + supporting data) · 3 Solution (one page that makes clear "what we do") · 4 Technical approach and moat (architecture diagram + metrics vs. existing solutions) · 5 Product / prototype showcase (screenshots or photos) · 6 Market analysis (TAM-SAM-SOM sizing) · 7 Business model (monetization logic / unit economics) · 8 Competitive analysis (2x2 positioning map or comparison table) · 9 Team (photos + roles + awards as endorsement) · 10 Operating data / project progress (traction) · 11 Roadmap and milestones · 12 The ask (funding / resource needs + contact info, closing with a 3-year vision). Visual impact first; one memorable point per page; data over adjectives.

## §3 Outline Output Format (Stage 2 deliverable)

```markdown
# Deck Outline: <topic>
- Mode: A Academic / B Business / C Teaching / D Everyday
- Pages: N pages · Style: <one sentence> · Suggested render path: R?
- Visual motif: <e.g., rounded cards + circular icons>

## P1 · <action title>
- Type: title / content / chart / table / flow / quote / section
- Content: …
- Visual: … (chart / image / diagram suggestions)
- Speaker-note key points: …
```

## §4 Multi-Paper Synthesis Method (distilled from systematic-literature-review)

With more than 5 papers, paper-by-paper listing is forbidden; you must do thematic synthesis:

- **Themes**: 3-6 research threads running through the paper set
- **Convergences**: findings that multiple papers agree on
- **Disagreements**: where conclusions conflict or methods are mutually exclusive
- **Gaps**: questions the body of literature has not yet answered (often buried in each paper's limitations)
- If too few or too scattered papers make synthesis impossible, state plainly that "thematic synthesis is premature" — don't force it

## §5 Key-Claim Provenance Format (distilled from papi-ground / citation-check)

Annotate every key claim with: `(source: <doc name / paper title>, location: section / figure / table, strength: direct evidence / inference / needs manual verification)`

Two-pass method: the first pass only extracts the claim list (No. | claim | type | location) for user confirmation; the second pass verifies each item's provenance one by one. Never mix extraction and verification in a single pass.

## §6 Paper Close-Reading Dimension Cards (Stage 1, Academic mode)

1. Metadata: title / authors / venue / year / field / type
2. Research background: what the field needs to solve, why it matters, shortcomings of existing methods
3. Scientific question: what exactly it solves, motivation
4. Method: core idea, framework, key formulas, differences from existing methods
5. Experiments: datasets, baselines, metrics, setup
6. Key results: the 2-3 most important, each mapped to its location in the original figures/tables
7. Innovations: theoretical / methodological / experimental or applied
8. Limitations: assumptions, experimental shortcomings, generalizability, directions for improvement
9. Inspiration for one's own research (one sentence, for the discussion page)
