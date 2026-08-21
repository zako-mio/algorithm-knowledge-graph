# 算法知识图谱 · 调研计划

> **阶段**：调研（先计划后执行，本文件为待审阅计划，尚未执行）
> **复杂度**：[COMPLEXITY: 13/20] → Deep
> **前置**：见 `design-decisions.md`（16 条收敛决策）
> **原则**：调研质量决定知识图谱质量；遵循委派协议与过程文档管理

---

## 0. 核心理念

调研是知识图谱的"数据源"。rc8 的教训：依赖判定用"三硬依据 + 源码行引用"逐条可溯源，才做到 180 节点 578 边零矛盾。算法知识图谱沿用同款纪律——**每条知识声明都必须挂信源 + 交叉验证**，不允许"AI 凭记忆写"。

调研分两阶段串行接力，每阶段内部并行：

| 阶段 | 目标 | 产物 | 并行度 |
|------|------|------|--------|
| **Stage 1 域调研** | 产出节点/边/分组清单（"放什么进图谱"）| `research/stage1-inventory/inventory.json` | 4-5 路并行 |
| **Stage 2 点调研** | 产出每节点完整内容（what/why/how/例题/信源/步骤图）| `research/stage2-nodes/{node_id}.json` | 节点分批并行 |

两阶段之间有**用户检查点**：Stage 1 产出清单后先呈交用户抽查/调整，定稿后才进 Stage 2。避免"内容写完才发现漏了某个主题域"。

---

## 1. 信源策略与交叉验证

### 1.1 信源分层

| 层 | 信源 | 用途 | 获取方式 |
|----|------|------|----------|
| **S1 权威骨架** | OI Wiki（中文，最全树状索引）、CP-Algorithms（英文，深度条目）| 定义主题域/节点清单/关系骨架 | 联网抓取目录树 |
| **S2 经典书** | 《算法竞赛进阶指南》李煜东（DP/图论/数据结构权威）、《算法竞赛入门经典》刘汝佳紫书（基础）、CLRS（理论严谨性背书）、CPH（Antti Laaksonen，竞赛视角）、国家队论文集（高级/冷门）| 内容深度 + 严谨性交叉验证 | **下载 PDF → pdf-worker 提取**，存 `research/sources/books/` |
| **S3 题库** | Codeforces、AtCoder、LeetCode、洛谷 | 例题匹配（题号+链接+难度+考点）| 联网检索 + 题目页解析 |
| **S4 前沿** | 2024-2026 Codeforces 题型趋势、近年 ICPC/CCPC 区域赛题、新版数据结构论文 | 防过时 + 补冷门前沿 | 联网检索（Google→arXiv→CF blog）|

### 1.2 交叉验证规则（硬门控）

- **R1 双源验证**：每个知识点的核心机制（原理/复杂度）必须有 ≥2 个独立信源印证；仅单源的标"待验证"并进复查队列。
- **R2 溯源分级**（沿用 `cycle-20260813-coding-agent-security-textbook` 教训）：区分"一手核验"（我直接读了 OI Wiki/书原文）vs"转引"（子 Agent 转述）。转引数据在产物中标注信源+置信度。
- **R3 高危数据强制回源**：复杂度界（如某数据结构的均摊复杂度）、宏观统计（如"高频考点分布"）必须回 S1/S2 原文核对，不接受子 Agent 转引。
- **R4 新鲜度门控**（沿用教训）：调研先行时主动检索最新版本/发布时间，新版优先采用；2024 前的"已知最新"需复核是否过时（实证：Terminal-Bench 归属错 + Verified 过时）。
- **R5 xlsx/PDF 权威源解析防错位**（沿用 `cycle_0818_v4_fix`）：多 sheet/多章节按 name 映射真实内容，不硬套顺序。

### 1.3 经典书 PDF 处理流程

1. **下载阶段**（串行，pdf-worker 子 Agent 前置）：检索并下载 S2 书籍 PDF 至 `research/sources/books/`，记录每书的目录结构（章节→页码映射）存 `research/sources/books-index.json`。
2. **提取阶段**：pdf-worker 按需提取指定章节文本（含公式/图表 OCR），存 `research/sources/extracted/{book}/{chapter}.md`。
3. **引用阶段**：Stage 2 点调研子 Agent 读取相关章节做交叉验证，引用时挂 `[书名, 章节/页码]`。

> 下载清单（待确认，调研执行前可调）：
> - 《算法竞赛进阶指南》李煜东（第二版）
> - 《算法竞赛入门经典》刘汝佳（紫书，第二版）
> - 《算法导论》CLRS（第三版，英文版严谨性背书）
> - Competitive Programmer's Handbook (Antti Laaksonen，免费 PDF)
> - 国家队论文集（按年，可获取的年份）

---

## 2. Stage 1 域调研：产出节点/边清单

### 2.1 目标

产出一个 `inventory.json`，含：所有节点（变体级中粒度）、所有边（多类型）、12-15 个分组、每节点的 stage/priority 初值。这是"图谱放什么"的定稿。

### 2.2 域分片（并行 shard）

按 ICPC 主题域分 4-5 个并行 shard，每 shard 覆盖 ~3 个领域组。分片草案（调研中可微调）：

| Shard | 覆盖领域（领域组草案） | 主信源 |
|-------|----------------------|--------|
| **A 数据结构与算法范式** | 数据结构基础（栈/队列/链表/堆/ST 表/单调栈队列）、线段树树状数组组、并查集进阶组、DP 背包/DP 区间/DP 树形/DP 状压/DP 数位、贪心与分治 | OI Wiki 数据结构+动态规划+杂项树 + 进阶指南 DP/数据结构章 + CP-Algorithms data-structures + CPH ch7-8,20-23 |
| **B 图论** | 图论基础（遍历/连通/欧拉）、最短路（Dijkstra/Bellman-Ford/Floyd/Johnson）、网络流（最大流/最小割/费用流/上下界）、双连通与强连通（Tarjan）、二分图匹配、拓扑排序与关键路径 | OI Wiki 图论 + 进阶指南图论章 + CP-Algorithms graph + CPH ch13-16 |
| **C 字符串与数学** | 字符串（KMP/Trie/AC 自机/后缀数组/后缀自动机/Manacher/哈希）、数学-数论（筛/模逆/BSGS/exLucas）、数学-组合（计数/容斥/生成函数）、数学-概率与期望、数论进阶（原根/二次剩余）| OI Wiki 字符串+数学 + 进阶指南数学/字符串章 + CP-Algorithms strings+numerical + 国家队论文集（生成函数/高级数论）|
| **D 计算几何与高级专题** | 计算几何（凸包/旋转卡壳/半平面交/Voronoi）、高级数据结构（LCT/树链剖分/可持久化数据结构/分块/莫队）、FFT/NTT、博弈论与 SG 函数 | OI Wiki 计算几何+高级数据结构 + 进阶指南几何章 + 国家队论文集 + CP-Algorithms geometry |
| **E 技巧元层 + 前沿** | 技巧元层（快速读入/位运算/压位/懒标记套路/常数优化/对拍调试/随机化/模拟退火）、前沿追踪（2024-2026 CF 题型趋势/新数据结构/ICPC 近年高频考点）| OI Wiki 杂项 + CF blog/AtCoder editorials + 2024-2026 论文 |

> 注：分片边界不绝对，跨 shard 的交叉主题（如"线段树优化 DP"既属 A 又涉图论）由主 Agent 聚合时归一化（沿用 `cycle_20260814_conflict`：异构结构先定义统一 schema 归一化，≤2 次重试）。

### 2.3 每 shard 的委派契约

每 shard 委派 1 个 general 子 Agent（联网），prompt 含：
- ⚠️ Agent Identity — SUBAGENT，仅执行不委派
- Role: 竞赛算法域调研员
- Task: 调研指定领域组，产出该域的**节点清单 + 关系边 + stage/priority 初值 + 信源引用**
- 联网代理：`curl -x http://172.29.0.1:7890`，允许 Google→arXiv→CF 自适应降级
- 返回 JSON（结构化 schema，见 §4）：
```json
{
  "status": "success|partial|failed",
  "summary": "≤200字",
  "data": {
    "shard": "A",
    "nodes": [{"id","name","group","stage","priority","brief","sources"}],
    "edges": [{"from","to","type","evidence"}],
    "groups": [{"id","name","stage_range"}],
    "unresolved": ["存疑待主Agent裁决的项"]
  },
  "files_created": [],
  "decisions": [],
  "warnings": [],
  "errors": []
}
```

### 2.4 Stage 1 聚合与质量门控

主 Agent 收齐 5 shard 后：
1. **归一化**：统一 id 命名、去重、跨 shard 关系合并
2. **冲突裁决**（沿用 `cycle_20260814_conflict`）：数量/归属口径不一致时主 Agent 终裁，不重跑
3. **拓扑校验**：前置依赖边构成的子图无环（DAG 性）
4. **优先级校准**：P0/P1/P2/P3 分布合理性（P0 不过多不过少）
5. **覆盖校验**：对照 OI Wiki 顶层目录确认无大主题遗漏
6. 写 `research/stage1-inventory/inventory.json` + 人类可读 `inventory.md`
7. **[检查点] 呈交用户抽查**：清单/分组/优先级，用户确认后定稿进 Stage 2

---

## 3. Stage 2 点调研：产出每节点完整内容

### 3.1 目标

为 inventory 中每个节点产出完整内容 schema（what/why/how/例题/信源/步骤图数据），即 HTML 页的内容源。

### 3.2 分批委派（并行）

按节点分批，每批 ~8-12 节点（按 group 邻近成批，便于复用信源）。每批委派 1 个 general 子 Agent。预期 ~200-350 节点 → ~20-40 批。可分波次执行（每波 ~5-8 批并行，控制并发与上下文）。

### 3.3 每 batch 的委派契约

- Role: 算法知识点内容研究员
- 输入：该批节点清单（id/name/group/stage/priority/brief）+ 相关信源引用（OI Wiki/CP-Algorithms 条目 URL + 经典书章节）
- Task: 为每节点产出**分级深度内容**（按 priority：P0 深度/P1 标准/P2-P3 精简）+ **真实竞赛例题匹配**（CF/AtCoder/LC/洛谷 题号+链接+难度+考点）+ **步骤分解迷你图数据**（多阶段算法才填）
- 交叉验证：核心机制 ≥2 源；高危数据回源
- 返回 JSON（节点内容 schema，见 §4）
- pdf-worker 子 Agent 按需提取经典书章节供引用（并行于内容 batch，共享 `research/sources/extracted/`）

### 3.4 Stage 2 聚合与质量门控

1. **内容完整性**：每节点字段齐全（what/why/how/例题/信源/步骤图按深度档要求）
2. **信源覆盖**：每声明挂信源；转引标注置信度
3. **例题有效性**：题号/链接真实可访问（抽样验证）
4. **Python 实现校验**：how 的 Python 代码可跑（抽样 py_compile + 关键样例运行）
5. **跨节点一致性**：共享概念（如"懒标记"）描述不矛盾
6. 写 `research/stage2-nodes/{node_id}.json`
7. **[检查点] 呈交用户抽查关键节点** → 定稿 → 交付构建阶段（单独计划）

---

## 4. 结构化 schema 定义

### 4.1 节点 schema（Stage 2 产出，Stage 1 用其子集）

```jsonc
{
  "id": "seg-tree-lazy",            // 唯一 id，kebab-case
  "name": "懒标记线段树",
  "group": "G-DS-SEG",              // 所属领域组 id
  "stage": "intermediate",          // basic|intermediate|advanced|frontier
  "priority": "P0",                 // P0|P1|P2|P3
  "depth_tier": "deep",             // deep|standard|brief（内容深度档）
  "brief": "支持区间修改+区间查询的线段树，懒标记延迟下发",
  "what": "一句话定义",
  "why": {
    "intuition": "直觉引入（为什么需要它）",
    "principle": "原理（懒标记机制详解）",
    "history": "历史/由来（可选，deep 档填）"
  },
  "how": {
    "pseudocode": "伪代码",
    "python": "完整 Python 实现（含 PyPy 注意事项）",
    "pypy_notes": "PyPy 专属优化提示（如类型注解/避免动态开销）",
    "complexity": {"time": "O((N+Q)logN)", "space": "O(N)"},
    "limitations": "Python 劣势处：常数大，N>1e6 易 TLE，替代思路"
  },
  "examples": [                     // 真实竞赛例题
    {"oj":"Codeforces","pid":"1234C","url":"...","difficulty":2200,"key_point":"区间赋值+历史和查询"}
  ],
  "pitfalls": ["易错点1：下标越界","易错点2：标记未清空"],
  "step_dag": {                     // 页内步骤迷你图（多阶段算法填）
    "nodes": [{"id":"init","label":"初始化 dist/建树"}],
    "edges": [{"from":"init","to":"relax"}]
  },
  "sources": [                      // 信源（必挂）
    {"type":"oiwiki","url":"...","verified":true},
    {"type":"book","ref":"进阶指南,ch5.3,p132","verified":true},
    {"type":"cpalg","url":"...","verified":false,"note":"转引待回源"}
  ]
}
```

### 4.2 边 schema（Stage 1 产出）

```jsonc
{"from":"seg-tree-basic","to":"seg-tree-lazy","type":"variant","evidence":"懒标记是基础线段树的区间修改变体"}
```
`type` 枚举：`prerequisite`(前置依赖) | `variant`(变体演进) | `combination`(组合应用) | `cooccurrence`(考点共现)

### 4.3 组 schema（Stage 1 产出）

```jsonc
{"id":"G-DS-SEG","name":"线段树族","stage_range":["intermediate","advanced"],"domain":"数据结构"}
```

---

## 5. 过程文档管理（目录结构）

```
0820-algorithm-knowledge-graph/
├── 00-plan/
│   ├── design-decisions.md        # ✅ 16 条决策留档
│   └── research-plan.md           # ✅ 本文件
├── research/
│   ├── stage1-inventory/          # Stage 1 产物
│   │   ├── shard-A.json ... shard-E.json   # 各子 Agent 原始返回
│   │   ├── inventory.json         # 聚合后清单（节点/边/组）
│   │   └── inventory.md           # 人类可读清单（检查点用）
│   ├── stage2-nodes/              # Stage 2 产物
│   │   └── {node_id}.json         # 每节点内容 schema
│   ├── sources/
│   │   ├── books/                 # 下载的经典书 PDF
│   │   ├── books-index.json       # 书→章节→页码映射
│   │   ├── extracted/{book}/{chapter}.md  # pdf-worker 提取的章节文本
│   │   └── verified-urls.json     # 交叉验证通过的 URL 库
│   └── cross-validation/
│       └── reconciliation-log.md  # 冲突裁决记录（沿用教训）
├── 01-dag-data/                   # （构建阶段产物，调研后）
├── 02-node-pages/                 # （构建阶段产物）
├── 03-groups/
├── 04-interactive/
├── 06-md/
├── 07-checkpoint/                 # 构建脚本与中间产物
└── README.md
```

每阶段产出即时落盘，不依赖对话记忆（沿用通用编码准则：从磁盘读取）。

---

## 6. 委派协议遵循

- **调度者非执行者**：主 Agent 仅编排 + 聚合 + 问答，不自行联网调研/写节点内容
- **独立并行、依赖接力**：Stage 1 内 5 shard 并行；Stage 1→Stage 2 串行（有检查点）；Stage 2 内 batch 并行
- **角色优先匹配 agency-agents**：联网调研用 general 子 Agent（无 MCP 工具省 token）；PDF 处理用 pdf-worker 子 Agent
- **返回精简 JSON**：子 Agent 按结构化 schema 返回，summary ≤200 字
- **超 3 分钟没发 task → 执行者模式**：但本计划已规划好委派，不触发

### 子 Agent prompt 骨架（示例）

```
## ⚠️ Agent Identity — You are a SUBAGENT. Execute ONLY. No delegation. No search-agents.
## Role Activation: 竞赛算法域调研员（general）
## Task: 调研 [领域组清单]，产出节点/边/stage/priority 清单 + 信源引用
## 联网: curl -x http://172.29.0.1:7890；允许 Google→arXiv→CF 自适应降级；代理不可用降级国内源
## 交叉验证: 核心机制≥2源；高危数据回源；区分一手核验 vs 转引
## 返回: {status,summary,data:{shard,nodes,edges,groups,unresolved},files_created,decisions,warnings,errors}
```

---

## 7. 执行序列（含检查点）

| 步 | 动作 | 责任 | 产物 |
|----|------|------|------|
| 0 | 建目录 + 写计划文档（本步已完成）| 主 Agent | `00-plan/*` |
| **1** | **[检查点] 用户审阅本调研计划** | 用户 | 计划定稿 |
| 2 | 下载经典书 PDF + 建章节索引 | pdf-worker 子 Agent | `research/sources/books/` |
| 3 | Stage 1：5 路 shard 并行域调研 | 5×general 子 Agent | `shard-*.json` |
| 4 | Stage 1 聚合 + 归一化 + 拓扑/覆盖门控 | 主 Agent | `inventory.json`+`inventory.md` |
| **5** | **[检查点] 用户抽查清单/分组/优先级** | 用户 | 清单定稿 |
| 6 | Stage 2：节点分批并行内容调研 + pdf-worker 按需提书 | 多×general 子 Agent | `stage2-nodes/*.json` |
| 7 | Stage 2 聚合 + 内容/信源/例题/Python 实现门控 | 主 Agent | 节点内容库 |
| **8** | **[检查点] 用户抽查关键节点** | 用户 | 内容定稿 |
| 9 | 交付构建阶段（单独计划，不在本计划内）| — | — |

---

## 8. 调研质量门控总表

| 门 | 标准 | 检测方式 |
|----|------|----------|
| 信源覆盖 | 每声明挂信源 | schema 校验 sources 非空 |
| 双源验证 | 核心机制≥2 独立源 | 抽样 + unresolved 队列 |
| 溯源分级 | 区分一手/转引 | sources.verified 字段 |
| 覆盖完整 | 无大主题遗漏 | 对照 OI Wiki 顶层目录 |
| DAG 无环 | 前置依赖子图无环 | 拓扑排序校验 |
| 优先级合理 | P0/P1/P2/P3 分布合理 | 分布统计 + 人工校准 |
| 例题有效 | 题号/链接可访问 | 抽样 HTTP 校验 |
| Python 可跑 | how 代码无语法错 | py_compile 抽样 |
| 跨节点一致 | 共享概念描述不矛盾 | 主 Agent 抽查 |

---

## 9. 网络环境与并发对策（实测，2026-08-20）

### 9.1 代理配置

WSL2 代理 env 已正确设置，子 Agent 用普通 curl 即自动走代理（无需 `-x`）：
- `http_proxy=http://172.29.0.1:7890` / `https_proxy=http://172.29.0.1:7890`
- `no_proxy=localhost,127.0.0.1,172.29.0.0/20,*.local`
- 代理延迟 ~30-45ms（快）

### 9.2 信源可达性（实测）

| 信源 | HTTP | 访问方式 | 用途 |
|------|:---:|----------|------|
| `oi-wiki.org` | 200 | 代理 | S1 权威骨架（中文，最全）|
| `raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/` | 200 | 代理 | OI Wiki 原始 MD（结构化抓取更稳）|
| `cp-algorithms.com` | 200 | 代理 | S1 权威骨架（英文深度条目）|
| `github.com` / `raw.githubusercontent.com` | 200 | 代理 | S2 下载书/仓库 + OI Wiki raw |
| `arxiv.org` | 200 | 代理 | S4 前沿论文 |
| `www.luogu.com.cn` | 200 | 代理或直连 | S3 题库（中文 OJ）|
| `leetcode.cn` | 200 | 直连（中文站，不需代理）| S3 题库 |
| `atcoder.jp` | 200 | 代理 + UA 头 | S3 题库 |
| `codeforces.com` 页面 | **403** | Cloudflare 拦 curl | 题面需 browser-harness |
| `codeforces.com/api/problemset.problems` | **200** | 代理 + UA（慢~20s，但一次返全库）| S3 题库元数据 |

> ⚠️ OI Wiki 正确域名是 `oi-wiki.org`（`.com` 不可达）。

### 9.3 并发对策与 CF 策略修正

1. ~~CF bulk 缓存~~ **不可行**：实测 `codeforces.com/api/problemset.problems` 即便 120s 仍超时（响应过大被限速）。改为：**子 Agent 用 Google 搜索 "codeforces <topic>" 定位具体题**，题面用 Luogu 的 CF 镜像（curl 可达）或 browser-harness 读 CF 原页（罕见）。
2. **例题主源改 curl 可达站**：Luogu（curl 可达，含 CF 镜像）、AtCoder（curl+UA 可达）、LeetCode.cn（直连可达）。CF 仅作题号引用 + Google 检索定位，不强求抓题面。
3. **全量信源扛并发**：OI Wiki / CP-Algorithms / GitHub / arXiv / 洛谷 / LC.cn 全部 curl+UA 返 200，多 sub Agent 并行无虞。
4. **统一 UA 头**：所有子 Agent curl 加 `-A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36"`。
5. **波次执行**：Stage 2 节点分批按波次 5-8 批并行，不一次性全开（控制上下文与并发）。

### 9.4 信源可获取性实测结论

| 信源 | 可获取性 | 处理 |
|------|----------|------|
| OI Wiki（GitHub raw MD，docs/ 按域分目录）| ✅ 直接 curl raw | **主骨架** |
| CP-Algorithms（按域分目录，深度条目）| ✅ curl | **主深度内容** |
| CPH（cses.fi/book/book.pdf，~672KB 有效 PDF）| ✅ 下载 | 参考书，pdf-worker 提取 |
| AtCoder / Luogu / LeetCode.cn | ✅ curl | **例题主源** |
| arXiv | ✅ curl | 前沿论文 |
| 国家队论文集 | ⚠️ GitHub 搜索未中 | 各高级主题调研时 best-effort 单独检索 |
| Codeforces | ⚠️ 页面 403 / API 超时 | 仅题号引用 + Google 定位，题面用 Luogu 镜像 |
| 商业书（CLRS / 刘汝佳紫书黑书 / 进阶指南）| ❌ 无合法免费下载 | **待用户决策**（见待确认项 2）|

### 9.4 子 Agent 联网规范（注入 prompt）

```
联网：已配置 http_proxy/https_proxy=http://172.29.0.1:7890，用普通 curl 即走代理（勿加 -x）。
UA 头：-A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36"
OI Wiki 用 oi-wiki.org（勿用 .com）；GitHub/raw 走代理；CF 题面 403 改读本地 cf-problems.json 缓存或报 browser-harness 需求。
例题匹配：读 research/sources/cf-problems.json（已缓存全 CF 题库 tags+rating），勿重复调 CF API。
```

---

## 待用户确认项

1. ~~本调研计划整体方案~~ ✅ 已认可（两阶段串行 + 检查点 + 域分片）
2. **经典书 PDF 下载清单**（§1.3 末尾）是否增删
3. **域分片草案**（§2.2 表，A-E 五片）边界是否调整
4. 网络环境已实测通过（§9），是否现在开始执行步骤 2（下载 PDF + 建 CF 题库缓存）
