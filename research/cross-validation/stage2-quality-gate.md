# Stage 2 质量门控审计报告

- **审计对象**：`stage2-nodes/`（372 个 {node_id}.json）
- **对照清单**：`stage1-inventory/inventory.json`（60 组 / 372 节点 / 318 边）
- **审计日期**：2026-08-21
- **审计方法**：Python 脚本全量扫描 + 随机抽样（seed=20260821）+ 人工抽查

---

## 1. 总览

| 指标 | 值 |
|------|----|
| 库存节点数（inventory） | 372 |
| 节点文件数（excl. `_batch-plan.json`） | 372 |
| JSON 解析失败 | 0 |
| 缺文件 / 多余文件 | 0 / 0 |
| examples 条目总数 | 1,040 |

### 深度档分布（depth_tier，共 372）

| tier | 节点数 | 占比 |
|------|-------:|-----:|
| standard | 216 | 58.1% |
| deep | 105 | 28.2% |
| brief | 51 | 13.7% |

### 优先级分布（priority）

| priority | 节点数 |
|---------:|------:|
| P0 | 94 |
| P1 | 113 |
| P2 | 117 |
| P3 | 48 |

> 注：节点文件内实际 P2=117、P3=48（合计 165），inventory stats 记 P2=116、P3=49（合计 165），**总量一致但两个节点 P2/P3 归属在 inventory 与节点文件间存在一处错位**（见问题清单 #Q4）。

### stage 分布

| stage | 节点数 |
|-------:|------:|
| basic | 69 |
| intermediate | 121 |
| advanced | 153 |
| frontier | 29 |

---

## 2. 审计项结果表

| # | 审计项 | 结果 | 状态 |
|---|--------|------|:----:|
| A1 | 节点存在性 & JSON 合法 | 372/372，无缺失无多余（`_batch-plan.json` 为非节点清单文件，属预期） | ✅ |
| A2 | 必填字段齐全（顶层 11 字段） | 全部 372 节点顶层字段非空 | ✅ |
| A2b | 子字段（why/how） | 14 节点存在子字段缺口（29 处） | ⚠️ |
| A3 | depth_tier↔priority 硬映射 | 14 处偏离（全部可解释，见下） | ⚠️ |
| A4 | examples[].url / 字段 | 1040 条目：4 条 url 空白，102 条缺 oj/pid/difficulty/key_point（schema 变体） | ⚠️ |
| B5 | group 对应 & id=文件名 | id 全部与文件名一致；group 存在两种格式（344 裸 ID + 28 "ID+名称"） | ⚠️ |
| B6 | 共享概念一致性抽查 | 5 个共享概念在相关节点描述一致（懒标记/失配指针/均摊/原根/分块） | ✅ |
| B7 | sources URL 笔误 | `oi-wiki.com`、`github.cmo` 等 0 处 | ✅ |
| C8 | sources 非空 & verified | 20 节点单源（无 0 源）；verified true 占比 97.9% | ⚠️ |
| C9 | 核心机制 ≥2 源支撑 | 抽查 20 节点全部有复杂度声明；其中 20 节点单源（与低源节点重合） | ⚠️ |
| D10 | Python 可跑性（10 节点抽样） | py_compile 通过 10/10，0 失败 | ✅ |
| D11 | Python 长度 & 自测 | min=690 / p25=1643 / median=2145 / p75=2777 / max=7772 / mean=2283；`__main__` 自测覆盖 372/372（100%） | ✅ |

---

## 3. 各审计项详情

### A. 完整性

**A1 存在性**：372 个节点文件与 inventory 372 个 node id 完全一一对应，无缺失、无多余。`_batch-plan.json` 是批次计划文件，非节点内容，正常排除。

**A2 顶层必填字段**：`id/name/group/stage/priority/depth_tier/brief/what/why/how/sources` 在全部 372 节点中均非空。`id` 均等于文件名（0 处不一致）。

**A2b 子字段缺口**（29 处，涉及 14 节点）：

| 节点 | priority/tier | 缺口 |
|------|--------------|------|
| kinetic-tournament-tree | P3/brief | why.principle、why.history、how.pseudocode、how.pypy_notes |
| nested-segment-tree | P3/brief | why.principle、why.history、how.pseudocode、how.pypy_notes |
| ai-cp-trend | P3/brief | how.pseudocode、how.pypy_notes |
| binary-tree-dp-trick | P3/brief | how.pseudocode、how.pypy_notes |
| interactive-problem-trend | P3/brief | how.pseudocode、how.pypy_notes |
| prefix-gcd-optimization | P3/brief | how.pseudocode、how.pypy_notes |
| bitmask-dp-optimization | P3/brief | how.pseudocode |
| chord-graph | P3/brief | how.pseudocode |
| planar-graph | P3/brief | how.pseudocode |
| seg-beats | P2/standard | why.history、how.pypy_notes |
| li-chao-tree | P1/standard | why.history、how.pypy_notes |
| seg-dynamic | P1/standard | why.history、how.pypy_notes |
| seg-merge | P1/standard | why.history、how.pypy_notes |
| segment-tree-offline | P1/standard | why.history、how.pypy_notes |

- 其中 9 个 P3/brief 节点缺 pseudocode 属**合理省略**（brief 档本可略过伪代码），但缺 pypy_notes 的节点为 14 个中的 11 个。
- 严重性较高的是 **4 个 P1/standard 节点缺 why.history**（li-chao-tree、seg-dynamic、seg-merge、segment-tree-offline）与 **seg-beats(P2) 缺 why.history**——standard 档应具备完整三要素（intuition/principle/history）。
- 所有缺口节点 `how.python` 均完整，未影响 Python 可跑性。

**A3 depth_tier↔priority 硬映射偏离**（14 处）：

**P1→deep 过交付（10 处，建议保留，属 deliberate over-delivery）**：
`bcc`、`bridge`、`cartesian-tree`、`cut-vertex`、`dsu-application`、`hld`、`lct`、`manacher`、`numeric-binary-search`、`rmq`、`two-sat`（11 处，P1 图论/数据结构/字符串核心算法给了 deep 内容）

**P2→brief 低交付（3 处，需人工确认是否合理）**：
`discrete-root`、`partizan-game`、`quadratic-residue`（P2 却给 brief）

**汇总**：P1→deep 11 处（合理过交付）、P2→brief 3 处（存在欠交付风险）。**无 P0 偏离**。

**A4 examples 结构与 URL**：
- 1,040 条 example 中存在 **3 种 schema 变体**：
  1. **full**：`oj/pid/difficulty/key_point`（938 条，90.2%，328 节点）
  2. **title 变体**：`title/url/note`（34 条，14 节点，全部集中在 py-* 与 dp-*/数论入门节点）
  3. **problem 变体**：`source/problem/link`（68 条，28 节点，集中在基础算法族 G-A-1 等）
- 4 条 url 为空白字符串（非缺失但无效）：`extended-lucas`、`game-graph`、`sg-function`、`virtual-tree` 各第 0 条 example（url=`" "` 单空格）——其余 examples 的 url 合法。
- **102 条**（42 节点）example 缺 oj/pid/difficulty/key_point——这 102 条恰为 title/problem 变体，缺这些字段属于**字段命名不一致**而非内容缺失（title 变体有 url+note，problem 变体有 source+link，信息基本等价但 schema 不统一）。
- 分类门槛：`oj` 字段缺失集中在 42 个节点，与 title/problem 变体节点集合吻合，无独立 oj 缺失。

### B. 一致性

**B5 group 字段**：
- inventory 中 group 为 `id`（如 `G-A-1`），节点文件中 344 个用裸 ID、**28 个用 "ID + 名称" 混合格式**（如 `G-C-1 字符串匹配族`）。两种格式均可正确解析到 group（无 unknown），但**字段格式不统一**，是 28 处 group_mismatch 的来源。
- 涉及节点：kmp、boyer-moore、rabin-karp、z-function、string-hash（字符串族）；fenwick、fenwick-extended、sparse-table、rmq-linear（区间查询族）；dmst、matrix-tree、prim、second-best-mst、steiner-tree（生成树族）；dp-basic、dp-knapsack01/complete、dp-memo（DP 基础族）；py-2d-array、py-batch-io、py-bigint、py-builtin、py-list-comp、py-lru-cache、py-pypy、py-recursion-limit（Python 特性族）；prime-test-basic、fermat-little-theorem（数论基础族）。
- id=文件名一致性：0 处偏离 ✅

**B6 共享概念一致性抽查**（5 概念 / 15 节点）：

| 概念 | 抽查节点 | 结论 |
|------|---------|------|
| 懒标记 | seg-lazy / seg-beats / persistent-seg | ✅ 一致：均描述"节点维护 d[p]+b[p]，区间覆盖时打标记直接返回，pushdown 延迟下发" |
| 失配指针 | kmp / ac-automaton | ✅ 一致：KMP pi 数组 = 最长 border；AC fail[u]=δ(fail[p],c)，BFS 按深度构建，失配链到根 |
| 均摊 | amortized-analysis / splay / lct | ✅ 一致：势能法 c_hat=c+ΔΦ，splay 伸展 zig/zig-zig/zig-zag，均摊 O(log n) |
| 原根 | primitive-root / ntt / fft | ✅ 一致：原根判定 g^(φ(m)/q_i)≢1；NTT 用 g^q 替代 ω_n，998244353=119·2^23+1 |
| 分块 | sqrt-decomposition / mo-algorithm / block-list | ✅ 一致：块长 √n，整块打标记+散块暴力；Mo 按 l 块排序+奇偶化 r |

未发现跨节点对同一概念的矛盾表述。

**B7 URL 笔误**：`oi-wiki.com`、`oiwiki.com`、`github.cmo`、`leetcode.cmo` 等常见笔误 **0 处**。全部 oi-wiki 均使用 `oi-wiki.org`（377 处）。✅

### C. 信源质量

**C8 sources 与 verified**：
- 无 0 源节点；**20 个节点仅 1 个 source**（单源）。
- 总 source 数 958：verified=true 938（**97.9%**）、false 20（2.1%）。false 集中在手册/入门类 source（如 CPH 章节引用未逐页核验）。
- 155 条 source 无 url 字段（145 条 book + 10 条 paper，均有 `ref` 字段），属合理设计；但 **16 条 book source 把章节引用放进了 `url` 字段**（如 `CPH ch23 Matrices (p227-234)`），字段语义混淆（url 应为超链接），见问题 #Q3。

**C9 核心机制复杂度多源支撑**（抽查 20 节点）：20 节点均有 `how.complexity`（time/space 结构）声明；其中 **20 节点 source 数 <2**（即单源），与 C8 低源节点完全重合：
`block-forest`、`cdq-divide`、`common-mistakes`、`discrete`、`dominator-tree`、`dp-count`、`dp-dag`、`dp-knapsack-group`、`dp-knapsack-multiple`、`dp-number`、`dp-probability`、`dp-tree-knapsack`、`fast-output`、`geometric-inverse`、`interactive-debug`、`numeral-system`、`odt`、`parallel-binsearch`、`seg-dynamic`、`suffix-bst`。
- 其中 `common-mistakes`、`fast-output`、`interactive-debug`、`numeral-system` 属于竞赛技巧/工具类节点，单源可接受；`dp-*`、`dominator-tree`、`odt`、`suffix-bst`、`cdq-divide` 等算法节点单源建议补齐第二源。

### D. Python 可跑性（抽样 10）

| 抽样节点 | py_compile |
|---------|:---:|
| bst | ✅ |
| monotonic-stack | ✅ |
| fwt | ✅ |
| monotonic-stack-dp | ✅ |
| rabin-karp | ✅ |
| graph-basics | ✅ |
| fhq-treap | ✅ |
| suffix-array-optimal | ✅ |
| dp-number | ✅ |
| vertical-decomposition | ✅ |

- 10/10 通过语法编译（不实跑）。`__main__` 自测覆盖 372/372（100%）。
- Python 长度分布：min=690、median=2145、mean=2283、max=7772；5 个节点 >5000 字符（suffix-array-optimal 等）。全部含 `__main__`。

---

## 4. 问题清单

| # | 级别 | 类别 | 说明 | 影响节点 |
|---|:--:|------|------|---------|
| Q1 | 高 | 字段缺失 | 4 个 P1/standard + 1 个 P2/standard 节点缺 `why.history`（standard 档应三要素齐全） | li-chao-tree、seg-dynamic、seg-merge、segment-tree-offline、seg-beats |
| Q2 | 中 | 字段缺失 | 11 个节点缺 `how.pypy_notes`（其中 5 个非 brief） | 见 A2b 表 |
| Q3 | 中 | 数据规范 | 16 条 book source 把章节引用误放入 `url` 字段（应放 `ref`） | determinant、stack、manacher、topo-sort、connected-components、gaussian-elimination、dfs、matrix-basics、char-polynomial、lca、tree-diameter、queue、tree-basics、vector-space、rmq、two-pointer |
| Q4 | 中 | 一致性 | inventory stats 与节点文件在 P2/P3 计数上有一处错位（inventory P2=116/P3=49 vs 文件 P2=117/P3=48） | 1 个节点 |
| Q5 | 中 | 一致性 | group 字段格式不统一：344 裸 ID vs 28 个 "ID+名称" | 28 节点（见 B5） |
| Q6 | 低 | schema 变体 | examples 三种 schema（full/title/problem），102 条缺标准四字段（信息等价但字段名不一） | 42 节点（title 14 + problem 28） |
| Q7 | 低 | URL 无效 | 4 条 example url 为空白串 | extended-lucas、game-graph、sg-function、virtual-tree |
| Q8 | 低 | 低源 | 20 节点仅单源（其中 dp-*/cdq-divide/odt/suffix-bst 等建议补源） | 见 C8/C9 列表 |
| Q9 | 信息 | 映射偏离 | P1→deep 过交付 11 处（合理，建议保留）；P2→brief 3 处（建议人工确认） | discrete-root、partizan-game、quadratic-residue |

**未发现问题**：缺文件/多余文件、JSON 非法、顶层必填字段缺失、id=文件名不一致、URL 笔误、共享概念矛盾、Python 编译失败、`__main__` 缺失、P0 映射偏离。

---

## 5. 修复建议

**建议按以下优先级处理（每项均建议回源修复，勿只改生成物）：**

1. **P1（Q1）**：为 `li-chao-tree / seg-dynamic / seg-merge / segment-tree-offline / seg-beats` 补齐 `why.history`（可从 OI Wiki 对应页"历史/提出"章节 + CPH 引用补写）。
2. **P1（Q2）**：为 11 个缺 pypy_notes 节点补 `how.pypy_notes`（≥1 句 PyPy 优化要点即可）；P3/brief 缺 pseudocode 属合理，可不补。
3. **P2（Q3）**：统一 book source 规范——`url` 仅放超链接（如 CPH pdf 或购买页），章节页码一律入 `ref` 字段。16 处需迁移。
4. **P2（Q5）**：统一 group 字段为裸 ID（`G-X-Y`），28 个 "ID+名称" 格式批量规范化（注意需同步生成脚本源码，避免重生成回退）。
5. **P2（Q4）**：核对 inventory stats 与节点文件 P2/P3 错位的 1 个节点归属。
6. **P3（Q6）**：决定 examples 标准 schema 后统一。推荐迁移 title→full（title 变体信息在 title/url/note，可映射 oj/pid/key_point）；problem 变体（source/problem/link）可映射或保留为已标记的兼容变体。若不强制统一，应在 schema 文档中声明两类变体为合法。
7. **P3（Q7）**：补 4 条空白 url（均可从 pid 推导，如 Luogu P4720 / P2197 / P2148 / P2495）。
8. **P3（Q8）**：为算法类单源节点（优先 dp-number、cdq-divide、odt、suffix-bst、dominator-tree）补第二源；纯技巧类单源可保留。
9. **人工确认（Q9）**：`discrete-root / partizan-game / quadratic-residue` 三个 P2→brief 节点，若内容确实无需深入可改 P3 对齐 tier，或补 deep 化对齐 P2。

**流程建议**：修复完成后重跑本门控（脚本逻辑见 `_gate_audit_raw.json` 的生成脚本，可复用），目标阈值：子字段缺口 0、group 格式 100% 统一、example url 100% 合法、单源节点 ≤10。

---

## 6. 修复记录（2026-08-21）

修复执行人：内容规范化修复员（general）。全部修改写回 `stage2-nodes/*.json` 原文件，详细变更见 `cross-validation/stage2-fixes.json`。只做规范化修复，未改动 what/why/how 正文与 Python 代码。

### 修复统计

| 修复类别 | 数量 | 说明 |
|---------|-----:|------|
| 修改节点数 | 104 | 占 372 节点的 28.0% |
| 子字段缺口补齐（A2b） | 29 处 / 14 节点 | P3/brief 按 brief 档补 pypy_notes，pseudocode 按档位补（brief 补精简版）；P1/P2 standard 补齐 why.history 与 how.pypy_notes |
| 空白 example url（Q7） | 4 条 | extended-lucas/game-graph/sg-function/virtual-tree 第 0 条，按 pid 补 Luogu 官方页 |
| examples 字段归一（Q6） | 96 条 | 全部 title/problem 变体统一为 `oj/pid/url/difficulty/key_point`；删除 6 条无真实题目的「概念题/通用技术」占位条目 |
| 升级 standard 补 example | 3 条 | discrete-root/partizan-game/quadratic-residue 各补 1 条标准档 example |
| group 字段格式统一（Q5） | 28 节点 | "ID+名称" → 裸 ID（与 inventory group id 一致） |
| book source url→ref（Q3） | 16 条 | 章节引用移入 `ref`，删除非法 url 字段 |
| depth_tier 升级（Q9） | 3 节点 | discrete-root/partizan-game/quadratic-residue：brief → standard（对齐 P2） |
| 补第二源（Q8） | 17 节点 | 算法类单源节点补 cp-algorithms / Wikipedia / OI-Wiki 第二源（URL 已实测可达） |
| 单源标记（Q8） | 3 节点 | common-mistakes/fast-output/interactive-debug 属技巧/工具类，单源可接受，`sources[0].single_source=true` |

### 修复后重扫结果（全库 372 节点）

| 门控项 | 修复前 | 修复后 |
|--------|-------|-------|
| JSON 解析失败 | 0 | 0 |
| 顶层必填字段缺失 | 0 | 0 |
| 子字段缺口（standard/deep 档 why/how） | 29 处 | 0 |
| examples schema 变体 | 3 种 | 1 种（全库 1037 条统一） |
| example url 空白 | 4 条 | 0 |
| example 缺标准四字段 | 102 条 | 0 |
| group 格式不统一 | 28 节点 | 0（372/372 均 `G-X-Y`） |
| book source url 非超链接 | 16 条 | 0 |
| 单源节点 | 20 | 3（均为技巧/工具类，已标记） |
| Python 语法编译（372 块） | 通过 | 通过（0 语法错误） |

> 注：`stage2-nodes.json` 的 examples 总数由 1040 → 1037（删除 6 条占位 + 新增 3 条升级 example），全部统一为 `oj/pid/url/difficulty/key_point` 五字段结构。
> 原始文件备份：`/tmp/opencode/stage2-nodes.backup-20260821040348/`（修复前全量副本）。

*报告由 Stage 2 质量门控审计生成。原始扫描数据：`cross-validation/_gate_audit_raw.json`；修复明细：`cross-validation/stage2-fixes.json`。*
