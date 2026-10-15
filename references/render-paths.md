# 渲染路径库（Stage 4 按需加载）

> 不绑定任何单一模型或工具。按"交付要求"选路径，路径可组合。

## §0 选型决策树

```
输入是图片/截图/图片式PPT（要求还原为可编辑）？
├─ 是 → R8 图片→可编辑 PPTX
└─ 否 → 需要逐字可编辑吗？
        ├─ 是 → 有统一模板约束吗？
        │       ├─ 是 → R2 模板母版注入
        │       └─ 否 → R1 代码生成原生 PPTX
        └─ 否 → 公式密集吗？
                ├─ 是 → R6 LaTeX Beamer
                ├─ 否 → 追求视觉冲击/艺术感？
                │       ├─ 是 → R4 AI 生图整页（或 R3 高自由排版）
                │       └─ 否 → 要在线 HTML 演示/开发者受众？
                        ├─ 是 → R5 Markdown 幻灯片
                        └─ 否 → R3 HTML→截图→PPTX（零生图依赖的高保真方案）
（流程图/架构图任何路径都可叠加 R7）
```

用户没说清时默认 R1（可编辑、通用、可控），并告知用户存在其他路径供选择。

## §1 R1 · 代码生成原生 PPTX

工具：pptxgenjs（Node）或 python-pptx。宿主有官方 PPT 技能（workbuddy-pptx 等）时优先委托其执行文件层操作。

**pptxgenjs 工程坑（提炼自 anthropics/pptx，血泪级）：**

- 先设 `pres.layout` 再加页；默认画布 10"×5.625"，不是 13.3" 宽；越界坐标不报错、直接消失
- 颜色不带 `#`、绝不 8 位（带 alpha 会**损坏文件**）；透明度用 `transparency: 0-100`
- pptxgenjs 会原地改写 option 对象（转 EMU）：shadow 等配置对象不复用，每次新建
- 阴影 `offset` 必须 ≥0（负值损坏文件）；向上投影用 `angle: 270` + 正 offset
- 字距是 `charSpacing`，`letterSpacing` 会被静默忽略
- 列表逐项 `bullet: true`（不用字面 `•`，会双 bullet）；数组项除末尾外都 `breakLine: true`；段距用 `paraSpaceAfter`
- 一个输出文件一个 `new pptxgen()` 实例；`rectRadius` 只对圆角矩形生效
- 渐变填充不支持——用渐变背景图代替
- 文本框有内边距：与形状对齐时 `margin: 0`
- 讲稿进 `slide.addNotes()`，不放页面文本框
- 图表保持**原生**（可编辑），只有 PPT 无原生形态的图（桑基/弦图/网络图）才贴图
- 堆积图的 `dataLabelPosition` 只能 ctr/inEnd/inBase（outEnd 损坏文件）
- 双轴组合图必须同时给 `valAxes` 和 `catAxes` 各两项，否则 PowerPoint 丢弃图表报损坏
- 图表默认裸奔：必须显式设 `showTitle`+`title`、`showValue: true`+`dataLabelPosition`、`chartColors: [...]`，单系列关图例，坐标轴标签与网格线用低饱和色
- **图标管线**：react-icons 渲染 SVG（`renderToStaticMarkup`）→ `sharp` 栅格化 ≥256px → `addImage({ data: "image/png;base64," + buf })`（前缀必须带）；简单图标也可用形状拼装
- 写完必须跑校验脚本（validate/打开测试），图表类缺陷在生成器里修，不手改 XML；`markitdown deck.pptx` 做内容层 QA（逐页文本 + grep 占位符 XXX/lorem/TODO）

**python-pptx 要点：**不能复制幻灯片（只有 `add_slide(layout)`）；改文字用 `run.text` 赋值（`text_frame.text = "..."` 会丢掉全部段落样式）；SVG/EMF 模板图会报错，先转 PNG。

**XML 直改（编辑已有 deck）时：**解包→改 `ppt/slides/slideN.xml`→重打包；用 defusedxml 解析（ElementTree 会重写命名空间前缀导致损坏）；结构操作（增删/重排页）在改内容**之前**完成；一个列表项一个 `<a:p>`，继承版式 bullet，不写字面 `•`。

**论文/文献素材专用（血泪级，违者返工）：**论文里已有的图（架构/对比/曲线/注意力/效率图）**一律截原文**，不手画——PyMuPDF 整页渲染定位 → 按图元联合包围盒 `clip` 裁切（`matrix=fitz.Matrix(3,3)` ≈ 216dpi）→ 逐张目检清晰度再嵌入；图下加 in-slide citation（10pt 斜体：`来源：作者, 简称, venue 年份 · Figure x`）。定量对比仍优先原生图表（表格数字重画为可编辑柱状图），只有 PPT 原生无法表达的图（架构图/气泡散点/注意力热图）才贴原文截图；每个数字上 slide 前与原文核对并记录表号/图号。

## §2 R2 · 模板母版注入（提炼自 pptx-from-layouts）

核心思想：**不是把文字盖在背景图上**，而是读取模板的 slide layouts 和 placeholders，按版式填充。

流程：模板画像（枚举全部 layouts 与占位符类型/位置）→ 每页内容映射到最合适的 layout → 逐占位符填充（标题占位符进标题、正文占位符进正文、图片占位符进图）→ 校验占位符无遗漏。

- 大纲用带版式声明的 markdown：每页标注 `Visual: cards-3 / process-3-phase / comparison-2 / table / hero-statement / data-contrast / timeline` 等
- 版式选择顺序：流程 > 对比 > 并列卡片 > 数据对比 > 金句 > 表格 > 大字结论 > 列表（列表是最后退路）
- 模板槽位 ≠ 内容项数：模板 4 人介绍而实际 3 人时，删掉第 4 人的整个 group（图+文本框），不是只清文字
- 30% 以上页面要改时直接重新生成，不要逐页补丁
- **工作流**：先用缩略图网格给模板全部 layouts 建档（每个 layout 一张标注图）再选版式；生成后跑校验（零 XML 错误 + 渲图零溢出）才算完成；交付报告里写明每个校验结果

## §3 R3 · HTML→截图→PPTX（零生图依赖的高保真路径）

最适合：无编辑需求但要精细视觉控制的正式 deck。

流程：写全局 CSS 设计系统（CSS 变量统一色彩/字号/间距）→ 每页一个 1280×720（或 1920×1080）画布的 HTML → 无头浏览器整页截图 → 图片逐页组装 PPTX → 讲稿写进 notes。

- 优点：排版能力 = 网页排版能力（任意字体、grid、flex、渐变、阴影全可用），完全确定性、可 diff、可复用主题
- 每页截图前用 JS 校验内容溢出（`scrollHeight > clientHeight` 即溢出）——这是天然 QA 优势
- 图表用 ECharts/Chart.js 渲染，同样截图嵌入（图表失活但视觉质量高于 PPT 原生图表，按需权衡）
- 同一份 HTML 可同时产出在线演示版（加分交付物）

## §4 R4 · AI 生图整页（提炼自 deer-flow ppt-generation / codex-ppt）

适用于冲击力优先、接受图片式 PPT 的场合。**模型无关**：任何可用的生图模型（GPT-image、即梦、SD、ImageGen 等）都行，按宿主环境取用。风格预设直接取用 style-library.md §4 的 prompt 钩子。

- **样张确认门**：先出 1 页样张交用户确认，批准后再批量（批量时记录样张的生成方式并复用到每一页）
- **链式一致性是命门**：逐页串行生成，第 N 页以第 N-1 页成品为参考图，prompt 中显式写 "continuing EXACT visual style from reference image / SAME palette / SAME typography"；**禁止并行生成**（并行=风格崩）
- 第一张图定全局视觉语言，最值得反复重生成到满意
- prompt 要具体到病态：精确 hex 色值、字号字重、构图比例、留白比例、特效参数（"backdrop blur 20px"、"hard shadow 8px offset"）；"professional slide" 这种模糊 prompt = 垃圾产出
- 有子代理能力时可用"每页一个 worker"的并行架构提效，但前提是先把锁定风格的样张 prompt 固化进每个 job——没有参考图链的并行依然是风格崩
- **生图模型文字渲染不可靠**：中文文字密集的内容页慎用整页生图；标题页/分节页/封面适合，正文页优先 R1/R3
- 用户提供的图片素材（论文图、logo、截图）是严格输入：先确认"哪页用哪图"的映射再生成，生成结果里必须可见出现
- 图像式 PPT 的特有 QA：逐页检查文字幻觉/错别字/截断——图像里的错字不可编辑修正，只能重生成；本地绘制/截图拼接是失败模式而非降级方案，产图必须来自生图后端
- 用户认可的视觉规格可存为自定义风格（style-library.md §6），下次同名场景复用

## §5 R5 · Markdown 幻灯片（Marp / Reveal.js / Slidev）

- Marp：最轻，`---` 分页，`marp slides.md -o slides.pptx` 可直接转 PPTX（图片式）
- Reveal.js / Slidev：HTML 在线演示，代码高亮、动画、交互最强；适合技术分享
- 定位：速度优先、开发者受众、需要在线分享链接。视觉上限受主题限制，重要场合不选

## §6 R6 · LaTeX Beamer

- 公式密集（数学/理论/物理）首选；学术会议接受度高
- 结构：`\section` 分节、frame 一页、`\block` 分块、`semiverbatim` 代码
- 模板选 Metropolis（现代简约）或经典主题；中文用 ctex
- 图表用 TikZ 精确绘制，质量上限极高但制作成本高
- 与 R1 组合：正文 Beamer + 特殊图表外部生成后 `\includegraphics`

## §7 R7 · SVG / Mermaid 矢量图示

- 方法框架图/架构图/流程图：Mermaid（快）或手写 SVG（精）生成后嵌入任何路径的 deck
- 嵌入 PPTX 时 SVG 需转 PNG（≥2x 分辨率），matplotlib 亦可选（学术图表标准）
- 流程图遵循"从左到右、从上到下"阅读动线；节点圆角统一、连线正交、配色服从 deck 主色

## §8 R8 · 图片/截图 → 可编辑 PPTX（提炼自 nature-image2ppt）

输入是图片式 PPT、扫描页、课程截图、他人 deck 的照片，输出要求可编辑对象时用此路径。

流程：**逐页区域分解** → 原生重绘 → 页级 QA → 组装 → 整体 QA。

- **区域分解**：每页拆成 3-5 个语义区（标题区/文本区/图形区/表格区/注记区），每区独立决定重建方式
- **原生优先原则**：可测量的圆、卡片、直线/虚线关系、简单连接线一律用原生形状重建；只有真正复杂的局部子图（照片、复杂插画）保留为位图资产并在交付时注明"可替换位图"
- **箭头铁律**：细箭头 = 一个连接线形状（箭头端点在同对象上）；实心箭头 = 一个 Arrow AutoShape（文字放同对象内）。**禁止**"直线+三角形"拼箭头，**禁止**把整张知识图拍平成一张大图
- **文字**：OCR/读图提取后按原样式重建文本框；字号层级按观察结果映射到规范字号
- **公式是硬门禁**：公式必须用公式引擎渲染（LaTeX→图片或 OMML），引擎不可用时该页标记失败并请示用户，不得用模糊截图糊弄
- **页级 QA**：重建页渲染图与原图并排对比（contact sheet），核对结构完整、无遗漏区、无新增幻觉元素；speaker notes 从原 PPT 保留（如有）
- 每页记录重建方式与资产来源，最终报告注明哪些元素仍是位图

## §9 讲稿（speaker notes）规范

- 每页 80-120 字中文，口语化、可直接照读
- 结构：本页一句话结论 → 展开解释 → 与下一页的过渡句
- R1 用 `addNotes()`；R3/R4 组装时写 notes；R5 用 presenter notes 语法；R6 用 `\note{}`；R8 保留原有 notes

## §10 已知坑（都在真实 deck 上踩过并验证过修法，照做即可，别重新发明）

| # | 症状 | 根因 | 修法 |
| --- | --- | --- | --- |
| 1 | 出现贯穿整页的巨型竖条/横条，尺寸离谱（如 9524 英寸） | `Inches(float)` 与 `Inches(Emu(x))` 混用导致双重换算 | 所有几何值统一用 `Inches(float)`；只有从 XML/EMU 读回来的值才用 `Emu` |
| 2 | 论文图裁出来带正文段落或页边竖线 | 双栏页里正文与图形只差几 pt，caption 聚类会把正文 rect 一起并进来 | 候选 rect 必须满足 `r.x0 >= cap.x0-250 and r.x1 <= cap.x1+250`（严格包含过滤）；左右边界放宽到 `min(box.x0-4, 55)` / `max(box.x1+4, pw-55)` 以保住全宽 panel；个别页（双栏首页）只能硬编码 `hard_clip` |
| 3 | 图注下方的子标签（如 "Score Map of Layer 1"）被切掉 | 裁切框底部取到了 `box.y1`，而子标签在图注和图形之间 | 底部一律改成 `cap_top - 1`（图注上沿），不要用 `box.y1 + 6` |
| 4 | 讲稿字数总压不到 120 以内，反复来回 | 中文全角字符的 `len()` 比肉眼的"字数感"更占位，估算普遍偏乐观 | 以脚本实际 `print` 的输出为准迭代，不要凭估算；脚本报 `notes out of range: [(8,134),(9,122)]` 就只改这两页 |
| 5 | 改完再渲图，看到的还是老样子 | 复用了旧 PNG | 每次修改后从改过的文件**重走完整渲染链**，不能复用旧图；批量导出前先记下旧图哈希，导出后比对 |
| 6 | 用 PowerPoint COM 连续导出两个 pptx，第二个报 `RPC 服务器不可用` | 同一进程连续 Open/Close 会把 COM 服务弄挂 | **一次进程只导一个文件**（一个文件一次调用）；或导出后 `Quit` 再重新 `Dispatch` |
| 7 | 中文在 PowerPoint 里变成宋体/默认字体，与设定不符 | 只设了 `font.name`（写入 `<a:latin>`），没写东亚字体 | 每个 run 额外写 `<a:ea typeface="...">` 元素；标题/正文都要设 |
| 8 | 图片放进占位框后被拉伸变形 | 直接给定了宽高 | 用 cover 裁切（`pic.crop_left/right` 或 `crop_top/bottom`，按宽高比算偏移量）或 contain 等比缩放 |
| 9 | 卡片/图片自带阴影，观感廉价 | 继承了主题默认阴影 | 每个形状/图片显式设 `shape.shadow.inherit = False` |
| 10 | 明明"塞了很多形状"，过不了图文并茂门禁 | 视觉页只认 图片/图表/表格，形状拼的示意图不算 | 该放证据图就放真图；纯形状页要额外承载一个原生图表或表格才能算视觉页 |
| 11 | 论文里明明有架构图，自己画了个流程图放上去，被门禁 G15 判"原文有图却用自绘图顶替" | 把"自造图"当成了默认选项 | **原文有对应图就必须用它**（`crop_paper_figs.py` 裁 PDF）；自造图只在素材没有对应图时使用，且要落成真实图片文件 + 登记 `source_type=self-made` + `reason` + 页内标「来源：自绘」 |
| 12 | 论文有 10 个 Figure，只裁了 5 个，G15 报"Figure 6/7 未使用且未给理由" | 清单 `paper-figures.json` 由脚本扫描 PDF 题注生成，不是自己挑的 | 要么补上原图，要么在 `deck-spec.json` 的 `unused_figures_reason` 里逐条写 ≥8 字理由；删清单文件没用，重跑脚本又会生成 |

**裁图不要偷懒用现成的图片文件**：即使素材目录里已经放了 `fig*.png`，也要自己用 `crop_paper_figs.py` 从 PDF 重裁一遍，这样 `figures.json` 里的 sha256 才和 PDF 原文一一对应，门禁 G10 才过得去（用来源不明的图会直接判"来源不可信"）；同一次运行还会产出 `paper-figures.json`，那是论文"本来有哪些图"的独立清单，G15 拿它判有没有漏用。
