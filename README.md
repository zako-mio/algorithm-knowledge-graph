# 算法知识图谱

372 个算法知识点的完整知识图谱，覆盖算法竞赛与系统学习所需的核心数据结构、算法与专题。以 DAG（有向无环图）组织知识点间的前置依赖关系，支持按阶段 / 优先级 / 分组多视图浏览。

## 项目结构

```
.
├── index.html                  # 根入口（统计 + 导航 + 快速开始）
├── quality-gate.md             # 质量门控报告
├── report.md / report.html     # 项目报告（AI 友好 + 人类可读）
├── 00-plan/                    # 计划文档
├── 01-dag-data/
│   ├── algorithm-dag.json      # 核心 DAG 数据（60 组 / 372 节点 / 318 边）
│   └── stats.md                # DAG 统计与环检测说明
├── 02-node-pages/              # 372 个知识点详情页（HTML）
├── 03-groups/                  # 60 个知识组页 + index.html 组总索引
├── 04-interactive/             # 交互 DAG 总览（cytoscape，本地渲染）
│   └── vendor/                 # cytoscape.min.js + cytoscape-dagre.min.js
├── 05-views/                   # 人类入口视图（index.html 总入口 + 优先级 + 学习路径）
├── 06-md/                      # AI 友好 Markdown 镜像（非人类浏览入口）
│   ├── 00-index.md / 01-groups.md / 02-priority.md / 03-learning-path.md
│   └── nodes/                  # 372 个知识点 MD
├── 07-checkpoint/              # 构建脚本 gen-*.py（可重新生成各交付物）
└── research/                   # 阶段产物（stage1-inventory / stage2-nodes / cross-validation）
```

## 快速开始

1. 打开根入口 `index.html`，查看核心统计与入口导航。
2. 进入 **交互 DAG 总览**（`04-interactive/index.html`），组级视图下点击组节点下钻组内 DAG。
3. 从 **分组目录**（`03-groups/index.html`）或交互图进入组页，浏览组内知识点。
4. 点入知识点页读 what（是什么）→ why（为什么）→ how（怎么做）→ 例题 → 易错点。
5. 按优先级视图（`05-views/02-priority.html`）或学习路径（`05-views/03-learning-path.html`）安排学习顺序（`06-md/` 为 AI 镜像，md 保留作 AI 检索用途，人类浏览请走 HTML）。

## 数据说明

| 指标 | 值 |
|---|---|
| 知识组 | 60（A=基础/数据结构，B=图论/树，C=字符串/数学，D=计算几何/高级，E=技巧/专题/工具） |
| 知识点 | 372 |
| 关系边 | 318（prerequisite 113 / variant 101 / combination 56 / cooccurrence 48） |
| 学习阶段 | 4 层（basic 69 / intermediate 121 / advanced 153 / frontier 29） |
| 优先级 | P0-P3 四档 |
| 真实例题 | 1037 |

边类型：`prerequisite`（前置依赖，DAG 合法性判据）/ `variant`（变体）/ `combination`（组合）/ `cooccurrence`（共现）。

## 质量门控

详见 `quality-gate.md`，七项门控全部通过：

- 文件覆盖：372 页 / 60 组 / 372 MD / 4 视图 / 2 vendor ✅
- HTML 结构：434 页扫描，0 结构问题（UTF-8 无 U+FFFD / 标签平衡）✅
- 断链：修复后 0 断链 ✅
- DAG 无环：Kahn 校验通过 ✅
- 四向覆盖：DAG ↔ 02-node-pages ↔ 06-md/nodes ↔ stage2-nodes = 372 全一致 ✅
- 内容抽查：seg-lazy/dijkstra/kmp/fft/manacher 关键区块齐全 ✅
- 交互图 DATA：372 节点 / 318 边与 DAG 完全一致 ✅

## 与 rc8 的关系

本图谱为 `0820-plugin-dag-rc8` 的**方法重构复用**：继承其「根入口 + 交互 DAG + 分组目录 + 知识点页 + MD 镜像」的五层交付骨架、暗色 UI 风格与三级下钻交互范式，但数据模型完全不同（算法知识点 DAG 取代插件依赖链），并新增优先级 / 阶段 / 例题体系。方法论迁移详见留档报告。

## 构建脚本（07-checkpoint/）

| 脚本 | 用途 |
|---|---|
| gen-node-pages.py | 从 algorithm-dag.json 生成 372 个知识点详情页（02-node-pages/） |
| gen-group-pages.py | 生成 60 个知识组页（03-groups/） |
| gen-md.py | 生成 Markdown 镜像（06-md/ 视图 + nodes/） |
| gen-views.py | 从 algorithm-dag.json 生成人类入口 HTML 视图（05-views/ 优先级 + 学习路径 + 总入口） |
| gen-report-html.py | 生成项目报告（report.html） |

数据主源为 `01-dag-data/algorithm-dag.json`；修改数据后重跑对应脚本即可再生交付物。
