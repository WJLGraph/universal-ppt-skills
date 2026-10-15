---
name: universal-ppt-skill
description: 全场景演示文稿提炼技能（学术/职场/教学/政务/竞赛/日常通用，内置 30+ 风格库）。当用户需要制作 PPT、幻灯片、汇报、路演、答辩、开题报告、中期检查、结题验收、基金申报、文献汇报、组会展示、述职、工作总结、KPI 汇报、复盘、产品发布、招商路演、竞赛路演（互联网+/挑战杯/大创）、党政汇报、课程课件、培训、知识分享、活动演示、从论文/文章/报告/笔记/大纲/图片/截图生成 slides，或要求改进、审计、重构已有 PPT、把图片式 PPT 还原为可编辑 PPT 时使用。覆盖"内容拆解 → 叙事设计 → 视觉系统 → 多路渲染 → 质检交付"五阶段全链路。渲染不绑定任何单一模型：支持代码生成原生 PPTX、模板母版注入、HTML 截图、AI 生图（任意模型）、Marp/Reveal.js、LaTeX Beamer、SVG/Mermaid、图片转可编辑 PPTX 八条路径按需选型。触发词：做PPT、文献汇报、组会PPT、答辩PPT、开题PPT、论文转PPT、slides、presentation、deck、述职、路演、课件、党政汇报、竞赛PPT、发布会、图片转PPT、提炼自17个开源skill。
---
# universal-ppt-skill — 全场景演示文稿提炼技能

> 提炼自 17 个开源 skill 的精华：anthropics/pptx、codex-ppt、deer-flow(ppt-generation / academic-paper-review / systematic-literature-review)、nature-skills(paper2ppt / image2ppt)、academic-pptx、pptx-from-layouts、paper-to-course、PaperSpine、paperpipe、citation-check、academic-research-skills、AlterLab-FC-Skills、support-to-repro-pack、latex-writer、statistical-analyzer、grant-writer、survey-designer。

## 0. 铁律速记（10 条 · 开工前默写一遍 · 交付前逐条核对）

> **本节是整份 skill 的最小记忆集**，references 里的长文都只是它的展开。下面 10 条能独立读懂，不需要上下文；其中 7 条由 `scripts/deck_qa.py` **自动判死**，脚本跑不过就不许交付。
> 总原则（高于编号铁律的整体取向）：**叙事优先于排版** —— argument structure → data → layout → aesthetics，顺序不可颠倒。一份 deck 的价值在讲清一个论点，不在页数和特效。

1. **两阶段铁律** — 先给「页面级大纲 + 2-3 个风格候选」，收到用户确认才动手渲染；用户说"我只要结果"走 §0.2 降级协议，不许静默跳过。（门禁 G12）
2. **论文原图优先铁律** — 素材里**有**对应图就**必须用**（论文 deck 用 `scripts/crop_paper_figs.py` 从源 PDF 裁原文，zoom ≥ 3；日常 deck 用 docs/ 内图片）；**原文有图却不上片、或拿手画/AI 图/图标/截图顶替原文图表 = 违规**。素材里确实没有的才允许自造图，且必须同时满足：① 是**真实图片文件**再嵌入（形状/色块拼的"示意图"不算）② `figures.json` 登记 `source_type=self-made` + `reason`（≥8 字，说明素材为何没有对应图）③ 页内标 `来源：自绘`。论文图页内标 `来源：作者 · Figure x`。（门禁 G10/G11/G15）
3. **图片必须可溯源** — 每张嵌进 deck 的图都要登记在 `figures.json`（文件路径 + PDF 页码 + Figure 号 + sha256）；`deck_qa.py` 用哈希核对嵌入字节、并回查台账登记的图片文件是否真实存在且哈希自洽，**登记不到、对不上、或拿不出对应文件都判"来源不可信"**；学术模式下含图页还必须带 `来源：…`。（门禁 G10/G11）
4. **图文并茂是数值门禁，不是形容词** — 视觉页 = 含**图片 / 原生图表 / 表格**的页；占比 ≥ 60%，禁止连续 3 页非视觉页，content/data/table 页每页 ≥ 1 个视觉锚点（title/statement/closing/section/timeline 页豁免）。**文字框、色块、圆角卡片、纯形状拼的"示意图"一律不算视觉页**——自造图也必须先落成真实图片文件（PNG/渲染后的 SVG）再嵌入；架构/流程页应直接放**论文架构原图**或自绘 PNG，不要用形状硬拼。（门禁 G5/G6/G7）
5. **数字逐一核对** — 上片前每个数字与素材原文核对并记下 Table/Figure 号；对不上就不写。
6. **讲稿 80–120 字** — 脚本逐页打印 `len()`，越界列页号；无打印输出 = 未质检。（门禁 G2）
7. **QA 证据块不可豁免** — 交付必须附 `deck_qa.py` 的**原始输出**（含 PASS/FAIL 明细）；环境无渲染器要显式声明"渲染预览不可用"，不许含糊带过。
8. **Action title 门禁** — 每页标题是完整结论句（不是"研究背景"），只读标题串要能独立讲出全篇论证。（门禁 G13）
9. **视觉反模式清零** — 禁标题下装饰线、横贯色条、单侧竖条纹、卡片单边描边（含顶色条/左色条）。逐页对照 design-language.md §6。
10. **中文去模板化** — 禁"一句话总结 / 值得注意的是 / 不是…而是 / 综上所述"等短语（清单 design-language.md §7，`deck_qa.py` 自动扫）。（门禁 G9）

### 0.1 规则分级：先看级别，再决定能不能商量

| 级别 | 含义 | 违反后果 | 典型条目 |
| --- | --- | --- | --- |
| **R0 铁律** | 任何模型、任何渲染路径、任何场合都不许破 | 直接返工，不交付 | 上面 10 条全部 |
| **G 硬门禁** | 能机器判定，必须有留痕输出 | 脚本 FAIL 即不许交付 | 页数 / 字数 / 越界 / 溢出 / 视觉页占比 / 禁语 / 占位符 / 图片来源哈希 / 确认门 / action title |
| **P 软偏好** | 可按受众取舍，但取舍要写明理由 | 记录即可，不返工 | 配色候选、视觉母题、喘息页位置、字体族选择 |

拿不准某条规则属于哪一级时，**按更高级别执行**。

### 0.2 门禁执行协议（每阶段收尾都做，不许静默跳过）

| 阶段收尾 | 必做动作 | 必留痕 |
| --- | --- | --- |
| Stage 1 后 | 建术语台账 + 主张清单 | 主张清单（论断 / 证据位置 / 强度） |
| Stage 2 后 | 大纲 + 风格候选发给用户 → **STOP-AND-WAIT** | 用户确认原话写进 `work/deck-spec.json` 的 `confirm_evidence` |
| Stage 4 后 | 论文 deck 先跑 `python scripts/crop_paper_figs.py --pdf <论文.pdf> --out work/figs --manifest work/figures.json`（同时产出 `work/paper-figures.json` 论文图片清单）；再跑 `python scripts/deck_qa.py <deck> --spec work/deck-spec.json --figures work/figures.json --paper-figures work/paper-figures.json --mode A --out work/qa_output.txt` | 原样粘贴脚本输出 + 论文图片清单（哪些原图上片、哪些未上片及理由） |
| Stage 5 后 | 渲图逐页目检 + 修一版复检一版 | 缺陷清单（分级）+ 修复记录 |

产物落盘约定：`work/deck-spec.json`（模式/风格/页数/确认证据/`page_types`/`visual_ratio_min`/`unused_figures_reason`）、`work/figures.json`（图片溯源台账）、`work/paper-figures.json`（论文图片清单，由 crop_paper_figs.py 自动扫描 PDF 题注产出，与"裁了哪几张"无关）、`work/qa_output.txt`（QA 原始输出）。这四个文件是"规则被真正执行过"的物证。

**降级协议（用户说"我只要最后结果 / 直接做 / 别问我"时）**：不再逐轮等待，改为**一条消息内**给出「页面级大纲 + 2-3 个风格候选 + 我选定哪个及理由」，随即开始渲染并走完 Stage 4/5。用户事后否决时**按页重做，不重跑全流程**。**唯一不可降级的是 R0 铁律与 G 级门禁的证据块。**

### 0.3 物证文件的字段约定（照抄即可，脚本按这些字段判）

```jsonc
// work/deck-spec.json
{
  "deck": "trae_DeepSeek-V4.1-Flash_iTransformer介绍.pptx",
  "mode": "A",                        // A-F，见 §1 场景路由
  "style_name": "学术克制风",
  "render_path": "R1",
  "pages": 10,
  "docs_dir": "E:/universal-ppt-skills/docs",   // 素材根目录，学术模式的 docs-asset 图必须落在这里
  "visual_ratio_min": 0.6,
  "outline_confirmed": true,          // 用户确认过大纲？(门禁 G12)
  "style_confirmed": true,            // 用户确认过风格？(门禁 G12)
  "confirm_evidence": "用户原话：可以，按这个大纲做",   // ≥8 字，抄用户原话，不要自己编
  "page_types": ["title","content","content","content","content","data","data","data","content","closing"],
  // 论文图逐条交代：每个"没上片"的 Figure 都要给理由，否则 G15 FAIL
  "unused_figures_reason": {
    "Figure 6": "纯超参敏感性曲线，与 Figure 5 的结论重复，篇幅让给机制页",
    "Figure 8": "附录可视化，正文讨论不需要"
  }
}
// work/figures.json —— crop_paper_figs.py 自动写出；自己造的图也必须补登（含 sha256 与 reason）
{
  "figures": [
    {"file":".../fig4_overview.png","source_type":"pdf-crop","origin":".../iTransformer....pdf",
     "page":4,"label":"Figure 4","name":"fig4_overview","sha256":"...","size_px":[1506,523]},
    {"file":".../self_made_pipeline.png","source_type":"self-made",
     "origin":"R7 自绘（SVG→PNG）","reason":"论文没有本项目的三段式落地流程图，故自绘并标注来源",
     "name":"self_made_pipeline","sha256":"...","size_px":[1600,900]}
  ]
}
// work/paper-figures.json —— 由 crop_paper_figs.py 扫描 PDF 题注自动产出，不是人挑的
{"origin":".../iTransformer....pdf",
 "items":[{"label":"Figure 1","kind":"Figure","page":1,"caption":"Overall framework of iTransformer ..."}]}
```

`deck_qa.py` 会核对：spec 的页数与实际一致、`page_types` 长度等于页数、每张嵌入图哈希能在 `figures.json` 里找到（且台账登记的图片文件真实存在、哈希自洽）、学术模式只接受 `pdf-crop` / docs_dir 内 `docs-asset` / 已留痕的 `self-made`、**论文清单里的每个 Figure 要么上片要么在 `unused_figures_reason` 里有理由（G15）**。

## 1. 场景路由（先判定模式，再设计页面）

| 模式                   | 触发场景                                                                                 | 叙事骨架                                                                           | 视觉基调                                         |
| ---------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ------------------------------------------------ |
| **A. 学术论证**  | 文献汇报、组会、开题报告、中期检查、结题验收、毕业答辩、基金/项目申报、会议报告、seminar | 问题→方法→证据→贡献→局限（结构化论证；按子场景变体，见 narrative-patterns.md） | 学术克制/科研答辩风：白底、单字族、≤3 色        |
| **B. 商务汇报**  | 项目汇报、述职、工作总结、KPI 汇报、复盘、路演、产品发布、招商、评审                     | 结论先行（BLUF）→论据→行动项                                                     | 清爽专业/麦肯锡/数据仪表盘/keynote 按受众选      |
| **C. 教学讲解**  | 课程、培训、科普讲座、论文转课程、知识分享                                               | 认知负荷递进：是什么→为什么→怎么用→练一练                                       | 教学课件/手绘白板/手绘技术解释风：大字号、图示化 |
| **D. 日常表达**  | 活动策划、旅行分享、纪念相册、社团招新、读书会                                           | 情感叙事：时间线/主题串烧                                                          | 自由视觉风：允许高表现力                         |
| **E. 政务/党建** | 机关工作汇报、专题学习、政策宣讲、党建活动、年度总结、国企/事业单位汇报                  | 总体情况→主要做法→成效数据→问题不足→下步打算                                   | 党政红：正红+金白、庄重规整、对称结构            |
| **F. 竞赛路演**  | 互联网+、挑战杯、大创、创新创业大赛、招商推介                                            | 痛点→方案→技术壁垒→市场→商业模式→团队→规划                                   | gradient-modern/dark-premium/keynote：冲击力优先 |

**判定有歧义时默认 A（学术）**；用户提到论文/研究/数据/答辩，几乎一定是 A；提到党政/国企/事业单位汇报是 E；提到比赛/路演/投资人是 F。

完整风格选择器与 30+ 风格规范见 references/style-library.md（Stage 3 必读）。

学术模式需进一步判定**素材类型**（提炼自 nature-paper2ppt 的 manifest 路由）：

- `discovery` 发现/机理型 → 问题→证据弧线（默认）
- `methods` 方法/算法/工具型 → 问题→解决方案弧线
- `resource` 数据集/基准/资源型 → 工作流→验证弧线
- `clinical/materials` 实验/工程型 → 设计→推断弧线
- `review` 综述/观点型 → 证据地图弧线

判定结果用一句话告知用户，让用户能低成本纠正。

## 2. 五阶段工作流

### Stage 1 · 素材拆解（读懂）

按场景读取并结构化素材：

- **论文/文献**：提取元数据（标题/作者/venue/年份/领域）→ 深读各章节 → 抽取关键主张清单（每条主张：论断 + 证据位置 + 强度 Strong/Moderate/Weak）。维度：研究背景、科学问题、方法框架、实验设计、关键结果、创新点、局限与启发。必要时补充相关工作脉络（多文献综合见 references/narrative-patterns.md §4）。
- **文章/报告/笔记**：提炼核心论点、关键数据、案例、结论与行动项。
- **模糊需求（只有一句话）**：先问清受众、场合、时长、页数、风格约束、有无模板，一次性打包问，不挤牙膏。
- **已有 PPT（审计/改进）**：先做内容盘点（逐页标题+要点提取），输出诊断报告，改哪几页、怎么改，经确认再动。

**术语台账**：边读边建，模型名/数据集/指标/缩写在全部页面与讲稿中保持逐字一致。

### Stage 2 · 大纲设计（讲清）

产出**页面级大纲**，每页包含：action title（结论式标题）+ 页面类型 + 核心内容 + 视觉元素建议。然后执行两个门禁：

- **Action title 门禁**：标题必须是完整结论句，不是"研究背景"而是"现有方法在低样本场景下性能不稳定"。对照/反例见 references/narrative-patterns.md §1。
- **Ghost deck 测试**：只读全部 action title 串成一条线，必须能独立讲出完整论证。讲不通就改大纲，不是改措辞。

**大纲必须经用户确认后才进入渲染**。发出大纲后**停下等待**（STOP-AND-WAIT）：没有用户明确确认（"可以/按这个做/继续"）就不能开渲染；确认原话记进 `work/deck-spec.json` 的 `confirm_evidence`（门禁 G12 会检查）。各场景的页面结构模板（学术文献汇报/开题/中期/结题/答辩、商务、教学、日常、政务、竞赛）见 references/narrative-patterns.md。模板见 prompts/stage-prompts.md 模板一/二。

### Stage 3 · 视觉系统（先选风格，再定规格）

**第一步选风格（风格确认门，不许自行拍板）**：打开 references/style-library.md §1 选择器，按场景给出 **2-3 个候选风格 + 每个一句推荐理由 + 你推荐哪个**；用户确认后才锁定（用户品牌色/学校模板色永远优先）。风格候选与确认结果一并写入 `work/deck-spec.json`（`style_name` + `style_confirmed` + `confirm_evidence`）。

渲染前再定一页**视觉规格**（写入 deck-spec）：

- **色彩**：一个主色承担 60-70% 视觉权重 + 1-2 个辅色 + 一个尖锐强调色。拒绝默认蓝、拒绝高饱和堆砌。学术模式默认深藏蓝 `1F4E79` + 中蓝 `2E75B6` + 白底。
- **字体**：单一字族，用字号/字重做层级（标题 24-44pt bold / 正文 14-20pt）。中文学术：思源黑体/微软雅黑；正文最小 14pt，会议室后排可读需 ≥18pt。
- **版式**：统一网格与边距（≥0.5"），一页一个焦点，留白是能力不是浪费。承诺一个贯穿全 deck 的视觉母题（圆角图片框/彩色圆底图标等），但**禁止**：标题下加彩色装饰线、横贯页面的色条、单侧竖条纹——这些是"AI 生成味"的标志。
- **图表**（顶刊级标准）：细线、低饱和、直接标注关键数据、少网格线、不堆 3D 与阴影；涨红跌绿（中国市场惯例）。
- **呼吸感**：每页信息密度交替（密→疏→密），连续两页高密度内容之间插入喘息页（大字结论页/分节页/空镜页）。页面级动效从容收尾，拒绝快而急。
- **图文并茂铁律（R0，所有渲染路径通用，违者返工，门禁 G5-G7/G15）**：视觉页 = 该页含**图片 / 原生图表 / 表格**至少其一；**文字框、色块、卡片、纯形状拼的"示意图"不计入**（这是最常被绕过的漏洞，别自欺）。要求：视觉页 ≥ 总页数 60%；禁止连续 3 页非视觉页；content/data/table 页每页 ≥ 1 个视觉锚点（title/statement/closing/section/timeline 页豁免）。落地方式按路径取用：R1 用原生图表承载定量对比、用图片承载证据、架构/流程页**直接嵌论文架构原图或自绘 PNG**（形状拼装不算视觉锚点）；R3/R4 天然满足。**素材里有图就必须用**：论文 deck 的每个 Figure 要么上片、要么在 `work/deck-spec.json` 的 `unused_figures_reason` 里写清为什么不用，不许"原文有图却拿自绘图顶替"。写完必须由 `deck_qa.py` 判过，不许只凭肉眼觉得"挺丰富"。

完整设计语言与反模式清单见 references/design-language.md。

### Stage 4 · 多路渲染（做出来）

**先选路径，再写代码/出图。** 八条路径的完整选型决策树与实现要点见 references/render-paths.md。速查：

| 路径                  | 一句话                                   | 何时选                                             |
| --------------------- | ---------------------------------------- | -------------------------------------------------- |
| R1 代码生成原生 PPTX  | pptxgenjs / python-pptx 逐页构建         | 需要**可编辑**、原生图表、正式交付           |
| R2 模板母版注入       | 读取模板 layouts+placeholders 按版式填充 | 有学校/企业**统一模板**硬约束                |
| R3 HTML→截图→PPTX   | HTML/CSS 排版后整页截图组装              | 追求**视觉自由度**且不需逐字编辑，零生图依赖 |
| R4 AI 生图整页        | 任意生图模型逐页出图（参考图链保持一致） | 冲击力优先、接受图片式 PPT                         |
| R5 Markdown 幻灯片    | Marp / Reveal.js / Slidev                | 开发者向、要 HTML 在线演示、极快速                 |
| R6 LaTeX Beamer       | 公式密集的学术报告                       | 数学/理论场合、需要严谨排版                        |
| R7 SVG/Mermaid 矢量图 | 生成示意图/流程图再嵌入                  | 方法框架图、架构图、关系图                         |
| R8 图片→可编辑 PPTX  | 图片/截图/图片式 PPT 还原为原生对象      | 输入是图片式 PPT、扫描页、截图，要求可编辑         |

路径可组合（例如 R1 主体 + R7 流程图 + R3 封面）。宿主环境若已有官方 PPT 技能（如 WorkBuddy 的 workbuddy-pptx），R1/R2 的文件层操作优先委托它执行，本技能负责规格与 QA。

### Stage 5 · 质检交付（把好最后一关）

渲染后**先跑脚本门禁，再做人工目检**，顺序不许颠倒，详见 references/qa-gates.md：

0. **脚本门禁（不可跳过）**：论文 deck 先 `python scripts/crop_paper_figs.py --pdf <论文.pdf> --out work/figs --manifest work/figures.json`（顺带产出论文图片清单 `paper-figures.json`），再 `python scripts/deck_qa.py <deck> --spec work/deck-spec.json --figures work/figures.json --paper-figures work/paper-figures.json --mode A --out work/qa_output.txt`。有 FAIL 就先修到全 PASS；脚本输出的原始文本要原样贴进交付说明（门禁 G1-G15）。
1. **内容质检**：逐页检查文字截断、术语台账一致性、遗留占位符、引用完整性；讲稿逐页 80–120 字已由脚本打印；论文类 deck 核对**论文原图是否都被用上**（对照 `paper-figures.json` 清单，未上片的必须已在 `unused_figures_reason` 说明）、in-slide citation 齐全、`figures.json` 无未登记图片。
2. **视觉质检**：渲染为图片逐页检查（文字溢出→元素重叠→对齐→边距→对比度，按此优先级），缺陷按 high/medium/low 分级；第一版几乎必有溢出/重叠，修一版、复检一版，两遍干净即停。无渲染器时按 qa-gates.md 的降级流程做程序化检查，并**显式声明"渲染预览不可用"**。
3. **溯源质检**：学术/数据类 deck，关键结论逐一核对素材出处（主张清单先经确认再核验的"两遍法"）；引用格式统一（GB/T 7714 / APA / IEEE 按需）。

每页配 80-120 字中文讲稿（speaker notes）。交付时 present_files，并按 references/delivery-template.md 附**交付证据块**（页数/模式/风格/渲染路径/QA 原始输出/每张图来源/渲染预览可用性/已知限制/变更说明）。

## 3. 与其他技能的协作

- 论文精读评审（单篇深评）→ 本技能 Stage 1 已内化核心维度；需要顶会级完整审稿报告时配合 academic-paper-review 思路输出。
- 多论文系统综述 → 超过 5 篇文献时，按主题聚类提炼 convergences / disagreements / gaps，而不是逐篇罗列。
- 论文复现汇报 → 补充环境依赖、运行命令、踩坑点、复现结果对比四件套。
- 用户研究/问卷类内容 → 问卷设计要点（题型/Likert 量表/跳转逻辑/预试）纳入 Stage 1 拆解维度。

## 4. 参考文件索引（按需加载，不要一次全读）

| 文件                             | 内容                                                                               | 何时读                   |
| -------------------------------- | ---------------------------------------------------------------------------------- | ------------------------ |
| **scripts/deck_qa.py**           | **门禁脚本：页数/讲稿字数/越界/溢出/视觉页占比/禁语/占位符/图片来源哈希与台账自洽/确认门/action title/论文原图使用核查（G1-G15）全自动判定** | **Stage 4 出片后、Stage 5 交付前必跑（不可跳过）** |
| **scripts/crop_paper_figs.py**   | **论文原图裁切：从 PDF 按 caption 定位高清裁切并写 figures.json 溯源台账，同时扫描 PDF 题注产出 paper-figures.json（论文本来有哪些图）** | **论文 deck Stage 4 需插图时必跑** |
| reference 级：references/narrative-patterns.md | 六类场景页面结构模板（含开题/中期/结题/竞赛/政务）、action title 写法、文献综合法  | Stage 2 设计大纲时       |
| references/style-library.md      | 风格选择器、30+ 风格规范（学术/中文实用/现代表现三族）、经典配色板、风格工程化规则 | Stage 3 选风格时（必读） |
| references/render-paths.md       | 八条渲染路径的实现细节、决策树、各路径工程坑                                       | Stage 4 渲染前           |
| references/design-language.md    | 色彩/字体/版式/图表规范、文字预算、AI 味反模式清单、呼吸感法则                     | Stage 3 定视觉时         |
| references/qa-gates.md           | 三道质检的逐项 checklist、严重度分级、常见缺陷图例、溯源核查法                     | Stage 5 交付前           |
| references/delivery-template.md  | 交付证据块模板（不可豁免项 + 可选项），直接照抄填空                                | Stage 5 交付时           |
| prompts/stage-prompts.md         | 可复用 prompt 模板（素材→大纲、大纲→PPT、审计、R8 还原…），每阶段带 STOP-AND-WAIT 检查点 | 任何阶段需要模板时       |

**跑脚本前先确认依赖**：`python -c "import pptx, fitz"`；缺哪个装哪个（`pip install python-pptx PyMuPDF`）。脚本报错不许绕过——报错本身就是"环境未就绪、QA 未完成"。

## 5. 快速参考：12 页学术文献汇报标准结构

1 标题页 · 2 研究背景 · 3 科学问题与动机 · 4 相关工作与现有方法不足 · 5 核心思想 · 6 方法框架 · 7 实验设计 · 8 关键结果① · 9 关键结果② · 10 消融/深入分析 · 11 创新点与贡献 · 12 不足、启发与讨论

10 页版：标题 → 背景与问题 → 相关工作不足 → 核心方法 → 方法细节 → 实验设置 → 关键结果 → 消融分析 → 贡献与不足 → 总结讨论。

其他高频场景速查（完整模板见 narrative-patterns.md §2）：

- **开题报告**：选题背景与意义 → 文献综述与研究缺口 → 研究内容与科学问题 → 研究方案/技术路线 → 创新点 → 进度安排 → 预期成果
- **毕业答辩**：选题意义 → 研究内容与创新点（重头）→ 关键工作与成果 → 结论与不足
- **竞赛路演**：痛点 → 解决方案 → 技术与壁垒 → 市场与商业模式 → 团队 → 规划与诉求
- **政务汇报**：总体情况 → 主要做法 → 成效数据 → 问题不足 → 下步打算

**时长换算**：讲授型约 1-1.5 分钟/页（10 分钟 ≈ 8-12 页）；答辩型 1 分钟/页（15 分钟 ≈ 15 页上下）；路演型节奏快可 40 秒/页。页数未指定时按此推算并告知用户。

## 6. 开工前 30 秒复诵 & 交付前 30 秒复诵（对抗长上下文遗忘）

**开工前默念**：① 大纲要先给、要等确认；② **素材有图就必须用原文图**（论文图从 PDF 裁、要登记台账；没有对应图才自造，自造也是真实图片文件 + 登记 reason + 标"来源：自绘"）；③ 视觉页 = 图片/图表/表格，形状色块不算；④ 讲稿 80-120 字由脚本数。

**交付前默念**：① `deck_qa.py` 跑了没、FAIL 清了没（论文 deck 要带 `--paper-figures`）；② 证据块附了没（含"渲染预览可用性"声明 + 论文图使用情况）；③ 每张图有页码 + Figure 号（自绘图标"来源：自绘"）；④ 标题只读一遍讲得通吗。

**四条最容易翻车的老路（别走）**：跳过确认门直接出片 → 原文有图却不上片/用 AI 图或示意图顶替论文原图 → 用形状和色块把"纯文字页"包装成"看起来有视觉元素" → 论文图没有 in-slide citation 或没登记台账。

**回读顺序**：Stage 1→2 读 narrative-patterns.md；Stage 3 读 style-library.md + design-language.md；Stage 4 读 render-paths.md（含 §10 已知坑）；Stage 5 读 qa-gates.md + delivery-template.md。**任何阶段拿不准时回到 §0 十条铁律。**
