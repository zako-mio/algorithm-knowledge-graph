# 质量门控报告 — 算法知识图谱

生成日期：2026-08-21

## 1. 文件覆盖

| 交付物 | 预期 | 实际 | 状态 |
|---|---|---|---|
| 02-node-pages 知识点页 | 372 | 372 | ✅ |
| 03-groups 组页 | 60 | 60 | ✅ |
| 06-md/nodes 知识点 MD | 372 | 372 | ✅ |
| 06-md 视图 | 4 | 4（00-index/01-groups/02-priority/03-learning-path） | ✅ |
| 04-interactive vendor | 2 | 2（cytoscape.min.js / cytoscape-dagre.min.js） | ✅ |
| 03-groups/index.html 组总索引 | 缺失 | **已生成**（60 组卡片） | ✅ 修复 |

## 2. HTML 结构校验

全量扫描 434 个 HTML 页（372 知识点页 + 60 组页 + 04-interactive/index.html + report.html）：

- UTF-8 有效：全部通过，U+FFFD 替换字符 0
- `<!DOCTYPE` / `<html` / `</html>`：全部存在且闭合
- div / pre / table 标签平衡：全部平衡（0 不平衡）

**结果：0 结构问题** ✅

## 3. 断链检测

扫描全部 HTML 页内 `href`/`src` 引用（排除 http/https/data/javascript/mailto），逐一验证目标存在。

| 项 | 值 |
|---|---|
| 扫描页面 | 434 |
| 断链总数 | 1 |
| 断链详情 | `04-interactive/index.html` → `../index.html`（指向项目根入口） |

> 该「断链」目标 `index.html` 为项目根入口，本次 Step 6 已生成，**修复后断链归零** ✅

## 4. DAG 无环校验

- 校验边：`prerequisite` 类型（113 条）
- 算法：Kahn 拓扑排序（等价 DFS）
- 可访问节点：372 / 372
- **结果：无环，DAG 合法** ✅

边构成统计（全部 318 条）：

| 类型 | 数量 |
|---|---|
| prerequisite（前置依赖） | 113 |
| variant（变体） | 101 |
| combination（组合） | 56 |
| cooccurrence（共现） | 48 |

> 注：严格环检测（含 combination 边）存在 `lucas-theorem ↔ combination-number` 一对互补反边，属互补关系非先后依赖，学习路径不构成环，与 `01-dag-data/stats.md` 说明一致。

## 5. 四向覆盖校验

`algorithm-dag.json` 节点 ↔ `02-node-pages` ↔ `06-md/nodes` ↔ `research/stage2-nodes`：

| 来源 | 节点数 |
|---|---|
| algorithm-dag.json nodes | 372 |
| 02-node-pages/*.html | 372 |
| 06-md/nodes/*.md | 372 |
| research/stage2-nodes/*.json（排除 `_batch-plan` 非节点文件） | 372 |

四向节点 ID 集合完全一致，无缺失、无多余、无重名。**结果：4-way pass** ✅

## 6. 内容抽查

抽查 5 个代表性知识点页，确认关键区块齐全：

| 页面 | what | why | how | 例题 | 易错点 |
|---|---|---|---|---|---|
| seg-lazy | ✅ | ✅ | ✅ | ✅ | ✅ |
| dijkstra | ✅ | ✅ | ✅ | ✅ | ✅ |
| kmp | ✅ | ✅ | ✅ | ✅ | ✅ |
| fft | ✅ | ✅ | ✅ | ✅ | ✅ |
| manacher | ✅ | ✅ | ✅ | ✅ | ✅ |

**结果：全部区块存在** ✅

## 7. 交互图 DATA 一致性

`04-interactive/index.html` 内嵌 DATA 与 `algorithm-dag.json` 比对：

| 项 | DAG | 交互 DATA | 一致 |
|---|---|---|---|
| 节点 | 372 | 372 | ✅ |
| 边（from/to） | 318 | 318 | ✅ |

节点集合、边集合完全一致，无差异。**结果：一致** ✅

---

## 质量门控结论

| 门控项 | 结果 |
|---|---|
| 文件覆盖 | ✅ |
| HTML 结构 | ✅ 0 问题 |
| 断链 | ✅ 修复后 0 断链 |
| DAG 无环 | ✅ |
| 四向覆盖 | ✅ 4-way pass |
| 内容抽查 | ✅ 5/5 |
| 交互图 DATA | ✅ 一致 |

**全部门控通过。** 发现并修复 2 处：生成 `03-groups/index.html`（组总索引）、生成根 `index.html`（消除唯一断链）。
