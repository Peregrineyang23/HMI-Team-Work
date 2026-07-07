# 项目工作担当分析

- generated_at: 2026-07-06
- timezone: Asia/Shanghai
- source_project_table: `tmp/org-structure-slides.xml` 第 2 页，2026Q1-Q2 设计项目担当
- source_domain_formation: `agents/domain-formation.yml`，2026Q3-Q4 DDD 阵型
- source_organization: `agents/organization-teams.yml`，2026 三团队模型

## 分析口径

本分析把 Slides 第 2 页视为历史项目担当线索，把 DDD 阵型视为当前规划职责，把三团队模型视为组织职责。项目担当是否仍在进行，需要后续由杨帆或对应 owner 确认。

李达已离职且不在当前 roster 中，张婕即将离职；两人不纳入本次个人负载分析。张婕仍保留为历史迁移风险，因为她在 DDD 阵型中有 DD006、DD009、DD010、DS002、DM005 五个 partner 角色。

## 总体判断

当前负载不是均匀分配，而是明显集中在“组织机制 owner + 多领域 leader + 多项目支援”的少数人身上。李苏南、张劲、李玮、李颖是最需要保护注意力的四个节点；顾颖芝、张云豪、余宗历处于高覆盖但仍可通过清晰边界稳定运行的第二梯队。

另一侧，陈宁子、杜馨柯、李昊星没有历史项目或领域绑定；刘锦峰、孙若一有项目支援记录但没有 DDD 领域锚点。根据最新团队划分，这 5 位先进入李苏南架构下的超级合作支援池，用于承接跨项目执行、资料整理、项目支援协调和 onboarding；领域绑定作为后续能力发展路径。

## 高风险负载

| 成员 | 主要风险 | 建议 |
| --- | --- | --- |
| 李苏南 | 超级合作 owner；6 个 leader、14 个 partner；历史项目 5 项 | 保留机制和协作 owner 职责，项目执行必须拆二级 owner |
| 张劲 | 4 个 leader、16 个 partner；基础设施型领域多 | 不承接张婕迁出职责；DM005 只保留机制评审或另设执行 owner |
| 李玮 | 6 个 leader、11 个 partner；游戏/Launcher/Car Visualization/实时任务多线 | 拆 DD018 或 DM006 执行层给新人或支援成员 |
| 李颖 | AI提效 owner；fufu 001 首测；AI 桌面和 Workflow 主线并行 | 收缩非 AI 主线项目支持，优先跑通 AI worker 闭环 |

## 成员分析

### 李苏南

历史项目：奔腾E541、东风M18、东风8397、东风4SR、超级合作组。当前同时是超级合作 owner，并承担 ADAS、UI kit、Image Library、Cognitive Align、Action Plan、Design Specification 等 6 个 leader 角色。

判断：这是组织型关键节点，不宜再作为多个项目的一线交付 owner。更合理的定位是跨项目协作机制、设计管理机制、规范和评审的负责人。

### 李玮

历史项目：红旗8397蒙太奇落地、红旗DLP游戏、理想游戏商城。当前 leader 覆盖 Launcher、Car Visualization、Game Design、Design Support、3D Engine Library、Realtime Task Management。

判断：领域跨度从桌面/车辆可视化到游戏和实时任务管理，容易成为“所有工程化与可视化问题”的默认入口。建议将 Design Support 或 Realtime Task Management 的日常执行拆出。

### 张劲

历史项目：红旗8397蒙太奇落地、设计系统/动效平台化、东风M18-3。当前 leader 为 Car setting、UX Framework、Smart Cockpit、File Management，partner 数量最高。

判断：张劲适合负责底层框架、文件管理、复杂车控/座舱结构，但 partner 覆盖已经过宽。张婕离职后的 DM005、DD009 等相关职责不能默认继续叠到张劲身上。

### 李颖

历史项目：车展DEMO、AIOS 平台化、红旗8397 AI桌面、AI workflow。当前是 AI提效 owner，负责首个 AI worker `fufu 001` 测试，同时 leader DD006 AI center / AI Desktop 与 DM004 Workflow。

判断：李颖的职责天然可以整合成“AI 提效平台化主线”。短期目标应是跑通 AI worker 接入、任务反馈结构化、领域知识库和 workflow 自动化，减少非 AI 主线支援。

### 顾颖芝

历史项目：红旗8397-金葵花-天工品牌创意、车展DEMO、美术天空盒支援。当前 leader 为 Navigation、Creative Design、Style Library、Icon Library。

判断：顾颖芝是视觉语言、品牌创意和设计系统风格判断节点。适合承担创意/视觉方向最终判断，不宜被大量临时美术支援打断。

### 张云豪

历史项目：红旗8397、东风8397开机动画、捷途灯语。当前 leader 为 Motion/Animation、Motion Library、3D Assets Library。

判断：动效与三维资产职责聚焦，适合做平台化资产规范和关键动效评审。执行层可通过李苏南的超级合作支援池引入孙若一、刘锦峰等有支援记录的人共同沉淀。

### 韩康佳

历史项目：红旗8397音频可视化+角色设计落地、广汽音频可视化。当前 leader 为 Media、Character Design。

判断：负载相对聚焦，适合继续沉淀音频可视化、角色设计、语音交互方向，也可和李颖的 AI 桌面/AI 角色方向形成搭档。

### 张帆

历史项目：红旗报奖、红旗8397 总结视频、东风。当前 leader 为 Movie Creative。

判断：项目复盘、报奖、总结视频和 Movie Creative 自然吻合。建议把复盘视频、传播物料、分镜脚本沉淀成可复用模板，交给 AI worker 做素材整理和初稿辅助。

### 余宗历

历史项目：奔驰HMI。当前没有 leader 角色，但有 12 个 partner 角色。

判断：余宗历是典型的广覆盖协作者。建议选择一个方向升级为明确二级 owner，例如 Navigation、ADAS、Smart Cockpit、3D Engine 或 Workflow 中与个人能力最贴近的一项。

### 孙若一

历史项目：东风、上汽、大众美术TA支援、理想游戏支援、东风8397支援。当前已转入李苏南架构下的超级合作支援池。

判断：项目支援经验多，适合承担跨项目执行、资料整理和项目支援协调。后续可按能力发展再绑定 3D Assets、3D Engine、Game Design 或 Design Support 等领域。

### 刘锦峰

历史项目：红旗8397 SR+总结视频支援、东风8397 SR 美术调优。当前已转入李苏南架构下的超级合作支援池。

判断：可在超级合作支援池中负责 SR、美术调优、总结视频素材整理等可标准化工作，并与 Car Visualization、Movie Creative 或 Design Support 的领域 owner 配合。

### 陈宁子

2026-07-06 正式入职，当前已转入李苏南架构下的超级合作 onboarding 池。

判断：适合从资料整理、项目复盘、设计资产归档、AI worker 数据集维护等低风险任务开始，逐步形成稳定协作职责。

### 杜馨柯

2026-06-15 入职实习，当前已转入李苏南架构下的超级合作 onboarding 池。

判断：建议绑定导师和单一协作职责，不进入多项目并行。可从 DS/DM 资料整理、组件标注、反馈模板维护开始。

### 李昊星

当前没有历史项目、领域职责或补充能力信息，已转入李苏南架构下的超级合作容量池。

判断：属于未分配容量，但需要补充能力画像后再分配。短期可以安排一次 subagent profile 补全任务，再纳入具体协作 lane。

## 张婕职责迁移

张婕不纳入新工作分析，但她的 DDD partner 角色需要迁移或冻结：

| 领域 | 当前含义 | 建议迁移方向 |
| --- | --- | --- |
| DD006 AI center / AI Desktop | AI 桌面与 AI 新交互 | 李颖主责，韩康佳/顾颖芝按角色与创意支持 |
| DD009 UX Framework | 交互框架、信息架构、模板 | 张劲保留机制 owner，余宗历或陈宁子承接资料整理 |
| DD010 Car Visualization | 车辆可视化 | 李玮主责，刘锦峰承接美术调优/素材整理 |
| DS002 Style Library | 风格库 | 顾颖芝主责，杜馨柯可做整理支援 |
| DM005 File Management | 文档管理 | 张劲保留规则，陈宁子/杜馨柯做归档执行 |

## AI Worker 可接管事项

- 每周从 feedback 模板抽取项目状态，生成状态表和 blocker 列表。
- 为 DD006、DM004、DS008、DM005 建立知识库索引和资料清单。
- 对红旗8397、东风8397、车展 DEMO 等高频项目生成复盘素材目录。
- 自动检查 requirement 是否满足 owner、deadline、acceptance criteria、feedback_channel。
- 为超级合作组生成跨项目评审议程、会议纪要初稿和待办分发草稿。

## 超级合作适合承接的跨项目任务

- 跨项目设计评审组织和冲突协调。
- 多领域共同参与的工作坊，例如 AI 桌面、车控车设、动效平台化、设计系统更新。
- 高峰项目支援池管理，特别是东风8397、红旗8397、车展 DEMO、设计系统平台化。
- 人类协作规则沉淀：交付物定义、评审节奏、文件命名、反馈口径。
- 李苏南架构下的执行支援池：刘锦峰、陈宁子、李昊星、孙若一、杜馨柯承接跨项目支援、资料整理、onboarding 和可标准化执行任务。

## 未分配与需补信息

- 陈宁子、杜馨柯、李昊星：需要能力画像、导师、首个超级合作协作 lane。
- 刘锦峰、孙若一：需要把历史支援经验转换为超级合作中的标准化支援能力，并与对应领域 owner 建立评审关系。
- Slides 第 2 页项目担当是 2026Q1-Q2 历史线索，需要确认哪些仍是当前进行中项目。
- DS008 HMI Agents 当前没有 leader 或 partner，建议由李颖牵头、杨帆验收，作为 AI worker 系统的正式领域入口。
