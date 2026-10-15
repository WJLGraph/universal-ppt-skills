# 个人项目信息精炼档案（个人信息介绍 PPT 源材料）

> 用途：个人信息介绍类演示的内容源。所有数据均来自真实项目仓库，可直接引用、可溯源。
> 身份标识：WJL · GitHub / Gitee @WJLGraph · 方向：AI Agent × 数据可视化 × 全栈开发。

---

## 一、一段式自我介绍（开场页可直接用）

我是 WJL，一名专注于 **AI Agent** 与**数据可视化**的开发者。从 Vue 小程序起步，经历地理信息大屏、推荐算法与时间序列预测的锤炼，如今专注于以大模型为核心的多 Agent 系统与 Agent 安全测试。我相信好的工程是**理性架构**与**审美直觉**的结合 —— 系统要可靠，界面要克制，体验要有呼吸感。

一句话定位：**从火险大屏到多 Agent 系统，把「看数据」升级为「由系统替你研判数据」，并亲手为它打造红队防线。**

---

## 二、技能矩阵（分类标签：技能列表）

- **前端开发**：Vue2 / Vue3、Vite、Pinia、Element Plus、ECharts、Three.js、OpenLayers、微信小程序原生开发、GSAP 动效、Lenis 平滑滚动
- **后端工程**：Python、FastAPI、SQLAlchemy、PostgreSQL、JWT 认证、SSE 流式、Flask、Alembic
- **AI 工程**：LangChain / LangGraph、多 Agent 编排、RAG 知识库、HITL 人工审批、Prompt 工程、MCP 协议、Langfuse 观测、OpenAI / DashScope
- **Agent 安全**：红队测试、提示注入（直接 / 间接 / 工具返回夹带）、蜜罐、混沌注入、defense_score 量化判定
- **算法与数据**：KNN 状态空间重构、Attention-LSTM、Informer、协同过滤 UserCF / ItemCF、scikit-learn、pandas / numpy、GeoPandas / Shapely
- **工程美学**：GSAP 动效体系、暗亮双主题、零第三方依赖实现、指挥中心级数据大屏

---

## 三、核心项目（简介 + 技术栈 + 动词开头短句）

### 1. 焰哨系统 · Fire Agent（2026.09 — 至今，持续迭代）

多 Agent 协同的智慧火险预警平台，「火防三部曲」的终点站：由多 Agent 完成火险数据检索、风险研判与结构化报告生成。
技术栈：Vue3 + FastAPI + LangGraph + PostgresSaver + SSE 流式 + RAG

- 基于 LangGraph 编排 8 节点工作流（parse_task → 双路并行 fan-out → join 汇聚 → 报告生成 → 评审循环 → HITL 审批门），实现研判全流程自动化与人工监督并存；
- 使用 SSE 节点级进度推送 + PostgresSaver checkpoint，解决长任务黑盒与任意节点中断恢复问题；
- 针对 LLM 输出不稳定，落地 review_report 评审循环 + 失败模板兜底双重降级，报告服务零中断；
- 构建 Vue3 八大模块前端（2D/3D 数字孪生、明暗双主题、全链路语音交互），支撑指挥中心级使用场景。

### 2. Agent-Gauntlet · 红队测试平台（2026.10）

为焰哨系统打造的红队评测平台：故障注入 + 对抗攻击 + 判定评分。
技术栈：Python + YAML Payloads + CLI 工具链

- 针对 Agent 系统的间接注入风险，实现工具返回夹带注入器（字符串追加 / 字典注字段），复现最隐蔽的攻击通路；
- 基于 canary 标记与四级防御判定（LEAKED_PROMPT → COMPROMISED → NOT_TRIGGERED → BLOCKED）量化 defense_score，安全水位可回归对比；
- 使用混沌故障注入度量 recovery_rate 恢复率，与焰哨 env 门控 chaos hook 联动，形成「攻击 — 防御 — 修复」安全闭环。

### 3. 火防三部曲 · 毕业设计（智火卫渝 → 云南大屏 → 焰哨）

从机器学习建模到可视化大屏再到 Agent 系统的完整演进链。
技术栈：PyTorch / TensorFlow + OpenLayers + 高德地图 API + ECharts + Flask

- 针对火点数据高度稀疏问题，基于 KNN 状态空间重构实现火点预测，测试集 R² 达 **0.971**；
- 基于 Attention-LSTM 预测气象趋势、气候态-AR 混合模型预测 NDVI（R² 0.801），构建 FE 五分项火险指数五级分档体系；
- 使用 OpenLayers + 高德底图 + ECharts 构建云南省火险监测大屏，落地火点聚合、四级风险着色、热力成像、时空筛选等 17 项功能（Gitee ★ 3）。

### 4. Wjl-Mine-Blog · 个人博客（2026）

零模板依赖的多页面个人站点，本博客即「高端前端工作流」的参考实现。
技术栈：Vue3 + GSAP 3 + ScrollTrigger + Lenis + 手写正则高亮器

- 基于原生 JS + GSAP + Lenis 构建多页面工程，实现滚动叙事、双向可逆入场与 B1–B6 呼吸感节奏律动效体系；
- 手写正则 tokenizer 语法高亮器与 CJK 拆字器，零第三方高亮 / 拆字依赖；
- 支持暗亮双主题、macOS 风格 IDE 窗口、KaTeX 公式与 Markdown 文档站内渲染（Word 式目录导航）。

### 5. 开源 AI Agent 技能 ×2（2026.10）

把开发方法沉淀为可复用、可分发的 agent 技能并开源。

- **Haute · 高端 GSAP Skills**：蒸馏 GSAP 官方 skills，产出 6 大风格体系 + 12 动效模式 + 10 节引擎纪律 + 12+ 即贴配方，四路分发（skills CLI / Claude / Cursor / Copilot）全部合规打通（MIT）；
- **Universal PPT · 全场景演示技能**：蒸馏 17 个开源 PPT skill，建成六类场景路由 × 30+ 风格库 × 8 条渲染路径 + 内容—视觉—溯源三道质检闸的演示文稿生成系统（MIT）。

### 6. 算法复现与工程落地（2026.01 — 02）

- **Informer 时间序列复现**：无阉割复现 ProbSparse Attention，通过「6 轮早停 vs 30 轮不早停」对照实验定量验证早停价值（测试 R² 0.77 vs 0.45），踩坑与调参全程留痕；
- **协同过滤推荐系统**：从零实现 UserCF / ItemCF 双算法（行为加权 → 余弦相似度 → KNN 邻居 → Top-N → 离线评估），Precision 0.96 / 0.99、覆盖率 1.0，并落地「臻享云牧」云养殖平台（Vue2 + SpringBoot + Redis + JWT）完成算法到产品的闭环；
- **前端工程起点**：5 天交付 Vue2 积分商城全链路（三合一登录 + 购物车）与微信小程序严选商城，沉淀拦截器 / 守卫 / api 统一管理等可迁移工程习惯。

---

## 四、亮点数据速查（数据页直接引用）

| 维度 | 数据 |
| --- | --- |
| 火点预测精度（KNN 状态空间重构） | 测试 R² **0.971** |
| NDVI 预测精度（气候态-AR 混合） | 测试 R² **0.801** |
| 推荐精确率（UserCF / ItemCF） | **0.96 / 0.99**（覆盖率 1.0） |
| Informer 复现（早停对照） | 测试 R² 0.77 vs 0.45 |
| Agent 编排规模 | LangGraph **8 节点**（并行 fan-out + HITL） |
| 红队判定体系 | **四级**防御判定 + defense_score 量化 |
| 大屏功能沉淀 | 17 项功能演示 · Gitee ★ 3 |
| 技能蒸馏 | 17 个开源 skill → 6 场景 × 30+ 风格 × 8 渲染路径 |
| 开源仓库 | GitHub / Gitee @WJLGraph · 17+ 公开仓库 |

---

## 五、成长时间线（叙事页骨架）

1. **前端筑基**：Vue2 积分商城（5 天交付）与微信小程序严选商城，建立工程化思维；
2. **全栈 & 初触 AI**：Vue3 全栈应用 + 大模型能力接入产品（New Bing 演示站与提示词支持）；
3. **机器学习建模**：智火卫渝 —— KNN + Attention-LSTM + 气候态-AR 三模型分而治之的火险预测；
4. **时间序列**：Informer2020 分步复现，早停对照实验定量留痕；
5. **推荐算法**：协同过滤双算法 + 臻享云牧平台落地；
6. **毕业设计**：云南省火险可视化大屏，17 项功能 + Gitee ★ 3；
7. **AI Agent**：焰哨系统 —— LangGraph 8 节点编排 + SSE + HITL + RAG 报告中心；
8. **Agent 安全**：Agent-Gauntlet 红队平台，攻击—防御—修复闭环；
9. **开源沉淀**：Haute GSAP Skills 与 Universal PPT 双技能开源发布。

---

## 六、PPT 叙事建议（供「个人信息介绍」实验取材）

- **开场**：用「一句话定位」+ 三组数字（17+ 仓库 / 8+ 完整项目 / 5 大技术方向）建立第一印象；
- **主线叙事**：按「火防三部曲」讲演进 —— 大屏（看数据）→ Agent（研判数据）→ 红队（守护系统），一条线讲完技术深度与产品思维；
- **能力面**：技能矩阵六分组做雷达 / 标签墙，避免逐条罗列；
- **收尾**：开源双技能收束 —— 既会做系统，也会把方法沉淀为可复用的工程资产。
