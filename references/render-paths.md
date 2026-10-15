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

**pptxgenjs 工程坑（蒸馏自 anthropics/pptx，血泪级）：**

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

## §2 R2 · 模板母版注入（蒸馏自 pptx-from-layouts）

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

## §4 R4 · AI 生图整页（蒸馏自 deer-flow ppt-generation / codex-ppt）

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

## §8 R8 · 图片/截图 → 可编辑 PPTX（蒸馏自 nature-image2ppt）

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
