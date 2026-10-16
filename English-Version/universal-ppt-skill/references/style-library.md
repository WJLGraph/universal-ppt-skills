# Style Library (Stage 3 on-demand loading)

> Distilled from deer-flow ppt-generation (Modern Expression family), the codex-ppt style reference library (Chinese Practical family), anthropics/pptx + theme-factory (color palettes / themes), and nature-paper2ppt (Academic Restrained family).
> Usage rule (**Style Confirmation Gate, hard gate G12**): **first present 2-3 candidates from the §1 selector + a one-line recommendation for each + which one you recommend → stop and wait for user confirmation (STOP-AND-WAIT) → after confirmation, lock it in and write `style_name` / `style_confirmed` into `work/deck-spec.json`**. Starting to render without confirmation = workflow violation (the script will judge FAIL when `style_confirmed=false`). If the user explicitly says "you decide", copy that sentence verbatim as `confirm_evidence` and treat the style as confirmed. Once a style is confirmed, the entire deck keeps one visual identity; only layouts may vary according to page role.

## §1 Style Selector (scenario → candidate styles)

| Scenario | First choice | Alternatives |
|------|------|------|
| Literature review / group meeting / seminar | Academic Restrained (学术克制风) | Clean Professional (清爽专业) |
| Thesis defense / pre-defense | Research Defense (科研答辩风) | Clean Professional, Academic Restrained |
| Proposal defense / mid-term review / final acceptance / grant application | Research Defense | Academic Restrained |
| Government work reporting / Party building / policy briefings | Government Red (党政红) | Clean Professional |
| Competition pitch (Internet+ / Challenge Cup / undergraduate innovation programs) | gradient-modern | dark-premium, keynote |
| Business consulting / strategy frameworks / 2x2 matrix | McKinsey (麦肯锡风) | Data Dashboard (数据仪表盘) |
| Performance reviews / work summaries / KPI / retrospectives | Clean Professional | Data Dashboard, McKinsey |
| Data analysis reports / business performance showcases | Data Dashboard | McKinsey |
| Product launches / keynote speeches | keynote | dark-premium |
| Tech product / AI / SaaS launches | glassmorphism | gradient-modern, 3d-isometric |
| Tech sharing / developer talks | Hand-drawn Tech Explainer (手绘技术解释) | minimal-swiss, Data Dashboard |
| Teaching / training courseware | Teaching Courseware (教学课件) | Hand-drawn Whiteboard (手绘白板), Warm Handcrafted (温暖手工) |
| Brainstorming / concept explanation | Hand-drawn Whiteboard | Hand-drawn Tech Explainer |
| Creative proposals / portfolios / fashion | Creative Magazine (创意杂志) | editorial, Retro Flat Illustration (复古扁平插画) |
| Brand stories / cultural-creative / cultural tourism | Retro Flat Illustration | Creative Magazine |
| Annual reports / premium brands / thought leadership | editorial | dark-premium |
| Consulting-grade executive briefings / C-suite | dark-premium | editorial, minimal-swiss |
| Children / parent-child / community nonprofit | Warm Handcrafted | Retro Flat Illustration |
| Travel / photo albums / everyday sharing | Retro Flat Illustration | Warm Handcrafted |
| Images/screenshots → editable PPT | Rebuild following the original image's style | — |

When judgment is ambiguous: default to Clean Professional for business-oriented decks and Academic Restrained for academic ones.

## §2 Academic Restrained Family

- **Academic Restrained** (default academic): white background, deep navy `1F4E79` primary + medium blue `2E75B6` secondary + red accent; a single sans-serif family; thin-line charts on white; decorative icons forbidden, full-bleed background images forbidden; figure on the left / interpretation on the right; the deck closes on a conclusion page built to carry Q&A. Nature-style (top-journal) enhanced variant: hero image occupies 60-75% of the layout, explanation compressed into a narrow rail / bottom strip; Chinese primary font family + Latin/numeric companion family (at most two families); figures carry panel sub-labels a/b/c; dark background only for image-led visual pages.
- **Research Defense**: formal reporting aimed at review committees. Well-structured, complete, and traceable information, often paired with "project decomposition / technical route / research foundation / risk analysis / expected outcomes" modules; blue-white or school-badge color scheme, steady and restrained, footer with page number and presenter; emphasizes visibility of workload (progress Gantt chart, deliverables list).
- **Clean Professional**: a minimalist business-academic hybrid of white background + a single accent color. Generous whitespace, thin dividers, no decoration; suits formal "content-is-king" occasions such as defenses, performance reviews, and retrospectives.

## §3 Chinese Practical Family (distilled from the codex-ppt style library)

| Style | Visual keys | Typical pages |
|------|---------|---------|
| **McKinsey** | White/light-gray background with an ink-blue-gray `243447` thin-line system; cover/viewpoint pages use "giant reconstructed headline type + a single business metaphor" (funnel / path / matrix / flywheel …); analysis pages get one core structure + 3-6 modules; icon seas forbidden, default rounded-corner card arrays forbidden | Framework pages, matrix charts, roadmaps, value chains, five forces, 2x2 |
| **Government Red** | Pure red `C7000B` / deep-red gradient primary + gold/white auxiliaries; imagery such as Tiananmen / huabiao columns / flags used sparingly; centered, solemn titles with tidy symmetrical structure; red-header-document-style title bar | Government work reports, Party building, annual summaries, policy briefings |
| **Data Dashboard** | Dark or light-gray background + highlighted data colors; big-number KPI cards, progress rings, mini trend lines; gridded yet strictly aligned; emphasis on "numbers visible at a glance" | KPI reporting, business analysis, monitoring dashboards |
| **Teaching Courseware** | Bright friendly colors, large type, illustrated step bars; one knowledge point per page + example + quick exercise; interaction markers emphasized (think / in-class practice) | Courses, training |
| **Hand-drawn Whiteboard** | Whiteboard background + hand-drawn wireframes/arrows/sticky-note texture, near-black handwriting-style annotations; deliberately less polished, reinforcing "thinking together" | Brainstorming, concept explanation |
| **Hand-drawn Tech Explainer** | White background + blue-black hand-drawn diagrams; components in rounded boxes with a hand-drawn feel; analogy illustrations lower the comprehension threshold; suits technical concepts, AI/software engineering | Tech talks, knowledge cards |
| **Retro Flat Illustration** | Retro warm palette (mustard / brick orange / ink green) + flat illustration elements, coarse grain texture; illustrations carry the narrative | Cultural-creative merchandise, cultural tourism, brand stories |
| **Creative Magazine** | Bold typography: oversized headlines, cropped images, clashing color blocks, pull quotes; break the grid from within | Creative proposals, portfolios |
| **Warm Handcrafted** | Cream/off-white background, soft rounded corners, paper-texture sticker elements, warm-lit illustrations | Children's education, parent-child, nonprofit |
| **E-ink Magazine** | E-ink-like black/white/gray + a single accent color; strong typographic grid, large serif headlines, print-media reading feel | In-depth reports, book clubs, essay collections |

## §4 Modern Expression Family (distilled from deer-flow; suited to the R3/R4 render paths)

| Style | Palette hook | Composition keys |
|------|---------|---------|
| **glassmorphism** | Purple→cyan gradient `667eea→00d4ff`, frosted white glass at 15-20% opacity | Floating glass cards with 32px corner radius, backdrop-blur, glow and depth of field; visionOS temperament |
| **dark-premium** | `0a0a0a` base + electric blue / neon purple / gold single accent | 60%+ negative space, edge glow, cinematic lighting; luxury-tech feel |
| **gradient-modern** | Stripe/Linear-style mesh gradient `7c3aed→ec4899→f97316` | Asymmetric composition, giant headlines at 80pt+, fluid gradient shapes; cutting-edge SaaS feel |
| **neo-brutalist** | Black & white + fluorescent pink/yellow/red high contrast | 4-8px thick black outlines, hard shadows without blur, broken grid; Gen-Z rebellious feel |
| **3d-isometric** | Low-saturation purple/cyan/coral + light-gray background | 30° isometric 3D illustration as hero, unified light source top-left; friendly tech feel |
| **editorial** | Off-white `f5f5f0` + charcoal + burgundy/forest-green single accent | 12-column grid, serif headlines at 96pt, full-bleed photography, pull quotes; magazine texture |
| **minimal-swiss** | Pure white + pure black + Swiss red/Klein blue single accent | Strict grid, no decoration, no shadows, Helvetica-based type scale 12/16/24/48/96; modernism |
| **keynote** | Pure black/dark gray + white text + Apple blue `0071e3` | One sentence per page, cinematic product shots, extreme type-size contrast; launch-keynote vibe |

For R4 image generation, write the palette hooks from the table above into the prompt (exact hex, font sizes, effect parameters); for R3, implement the same spec with CSS variables.

## §5 Classic Color Palettes (distilled from anthropics/pptx; directly usable for R1/R2)

| Theme | Primary | Secondary | Accent | | Theme | Primary | Secondary | Accent |
|------|-----|-----|-----|---|------|-----|-----|-----|
| Midnight Executive | 1E2761 | CADCFC | FFFFFF | | Teal Trust | 028090 | 00A896 | 02C39A |
| Forest & Moss | 2C5F2D | 97BC62 | F5F5F5 | | Berry & Cream | 6D2E46 | A26769 | ECE2D0 |
| Coral Energy | F96167 | F9E795 | 2F3C7E | | Sage Calm | 84B59F | 69A297 | 50808E |
| Warm Terracotta | B85042 | E7E8D1 | A7BEAE | | Cherry Bold | 990011 | FCF6F5 | 2F3C7E |
| Ocean Gradient | 065A82 | 1C7293 | 21295C | | Charcoal Minimal | 36454F | F2F2F2 | 212121 |

The palette principles stay unchanged: the primary color carries 60-70% of the visual weight; a palette must be "chosen for this specific topic" — if your palette would still work on a PPT about a different topic, it is not specific enough. theme-factory also ships ten named themes — Ocean Depths / Sunset Boulevard / Forest Canopy / Modern Minimalist / Golden Hour / Arctic Frost / Desert Rose / Tech Innovation / Botanical Garden / Midnight Galaxy — pick one by matching its temperament.

## §6 Style Engineering Rules

1. **Dark-light sandwich**: dark background for the cover + closing page, light background for content pages; or go full-deck dark for a premium route. Never switch randomly mid-deck.
2. **Every page needs a visual element**: an image, chart, icon, or color-block structure — pick one; a pure-text page always loses.
3. **Style confirmation gate**: offer 2-3 candidates + a one-line recommendation → user confirms → lock it into the visual spec card (design-language.md §8). For the R4 path, produce one sample page for confirmation before batch rendering.
4. **Style reuse**: a user-confirmed spec card can be stored in the style library (e.g. `./styles/`); the same scenario next time invokes it directly; user-provided brand colors / template colors take precedence over every default.
5. **Custom style**: when no preset fits, generate a named style on the spot from the four-part set "palette (hex) + font pairing + motif elements + light/dark tonality", preview it for the user, and after confirmation write it into the spec card following the §4 hook approach.
