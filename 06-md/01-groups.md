# 分组视图 · 60 组节点清单

> 供 AI 检索：按组列出节点 id / name / stage / priority / brief。

## G-A-1 排序与基础算法族

- 领域: 基础算法 · 阶段范围: 基础→中级 · 节点数: 20

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| sort-intro | [排序基础概念](nodes/sort-intro.md) | basic | P0 | 排序算法总览：稳定性、复杂度、比较与非比较排序的分类 |
| merge-sort | [归并排序](nodes/merge-sort.md) | basic | P0 | 分治排序，O(n log n) 稳定排序，可用于求逆序对 |
| quick-sort | [快速排序](nodes/quick-sort.md) | basic | P0 | 分治排序，期望 O(n log n)，最坏 O(n^2)，常数小 |
| heap-sort | [堆排序](nodes/heap-sort.md) | basic | P1 | 基于二叉堆的 O(n log n) 原地排序，不稳定 |
| comparison-sort | [简单比较排序(冒泡/选择/插入/希尔)](nodes/comparison-sort.md) | basic | P2 | O(n^2) 简单排序及希尔分组优化，教学与小规模数据 |
| non-comparison-sort | [非比较排序(计数/桶/基数)](nodes/non-comparison-sort.md) | basic | P1 | 线性时间排序，依赖键值范围限制 |
| tim-sort | [Timsort](nodes/tim-sort.md) | intermediate | P3 | 归并+插入混合稳定排序，Python/Java 标准库使用 |
| tournament-sort | [锦标赛排序](nodes/tournament-sort.md) | intermediate | P3 | 基于锦标赛树的排序，O(n log n) |
| binary-search | [二分查找](nodes/binary-search.md) | basic | P0 | 有序数组 O(log n) 查找，含 lower_bound/upper_bound |
| ternary-search | [三分法](nodes/ternary-search.md) | basic | P1 | 在单峰函数上找极值，基于中点比较缩小区间 |
| binary-answer | [二分答案](nodes/binary-answer.md) | intermediate | P0 | 对答案值域二分，配合 check 函数求解最优化问题 |
| greedy | [贪心算法](nodes/greedy.md) | basic | P0 | 每步取局部最优，需证明最优子结构与交换论证 |
| divide-conquer | [分治与递归](nodes/divide-conquer.md) | basic | P0 | 分解-解决-合并，递归处理子问题 |
| enumerate | [枚举与暴力](nodes/enumerate.md) | basic | P0 | 系统枚举所有可能，常结合剪枝优化 |
| simulate | [模拟](nodes/simulate.md) | basic | P0 | 按题意直接模拟过程，考察代码实现能力 |
| construction | [构造题](nodes/construction.md) | intermediate | P1 | 构造满足条件的解，需洞察问题结构 |
| prefix-sum | [前缀和与差分](nodes/prefix-sum.md) | basic | P0 | O(1)区间和查询/O(1)区间修改，一维与多维 |
| binary-lifting | [倍增](nodes/binary-lifting.md) | intermediate | P1 | 预处理2^k次幂跳跃，用于ST表/LCA/稀疏表等 |
| complexity | [时间/空间复杂度分析](nodes/complexity.md) | basic | P0 | 渐近符号(O/Theta/Omega)与复杂度分析方法 |
| amortized-analysis | [均摊分析](nodes/amortized-analysis.md) | intermediate | P1 | 聚合法/势能法/记账法分析均摊复杂度 |

## G-A-2 栈队列与单调结构族

- 领域: 数据结构 · 阶段范围: 基础→中级 · 节点数: 4

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| stack | [栈](nodes/stack.md) | basic | P0 | LIFO后进先出结构，支持括号匹配/表达式求值等 |
| queue | [队列](nodes/queue.md) | basic | P0 | FIFO先进先出结构，BFS基础组件 |
| monotonic-stack | [单调栈](nodes/monotonic-stack.md) | intermediate | P0 | 维护单调性的栈，O(n)求左右第一个大/小于当前值 |
| monotonic-queue | [单调队列](nodes/monotonic-queue.md) | intermediate | P0 | 维护滑动窗口最值，O(n)均摊，DP优化基础 |

## G-A-3 堆与优先队列族

- 领域: 数据结构 · 阶段范围: 基础→高级 · 节点数: 6

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| binary-heap | [二叉堆](nodes/binary-heap.md) | basic | P0 | 完全二叉树维护优先队列，数组实现O(1)查最值/O(log n)插入删除/O(n)建堆，对顶堆动态求中位数 |
| leftist-tree | [左偏树(可并堆)](nodes/leftist-tree.md) | advanced | P1 | 支持O(log n)合并的可并堆，利用偏侧树高 |
| pairing-heap | [配对堆](nodes/pairing-heap.md) | advanced | P2 | 均摊O(1)插入/O(log n)删除，Fibonacci堆的简单替代 |
| huffman-tree | [哈夫曼树](nodes/huffman-tree.md) | intermediate | P1 | 最优前缀编码树，贪心构造，WPL最小 |
| fibonacci-heap | [斐波那契堆](nodes/fibonacci-heap.md) | advanced | P3 | 均摊O(1)decrease-key，理论最优堆，实现复杂 |
| randomized-heap | [随机化堆](nodes/randomized-heap.md) | intermediate | P3 | 随机合并的可并堆，期望O(log n) |

## G-A-4 并查集族

- 领域: 数据结构 · 阶段范围: 基础→高级 · 节点数: 3

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| dsu-basic | [并查集(路径压缩+按秩合并)](nodes/dsu-basic.md) | basic | P0 | 近 O(1) 合并/查询集合，路径压缩 + 按大小/按秩合并，均摊 O(α(n))；模板题 P3367，Kruskal 最小生成树基石 |
| dsu-weighted | [带权/扩展域并查集](nodes/dsu-weighted.md) | intermediate | P1 | 在并查集边上维护权值/种类关系，支持相对距离查询与冲突判定，O(α(n)) |
| persistent-dsu | [可持久化并查集](nodes/persistent-dsu.md) | advanced | P2 | 用主席树（可持久化数组）存 fa/秩，支持历史版本回溯的并查集，O(log n)/操作 |

## G-A-5 区间查询与分块族

- 领域: 数据结构 · 阶段范围: 基础→高级 · 节点数: 4

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| sparse-table | [ST表(稀疏表)](nodes/sparse-table.md) | basic | P0 | 倍增预处理O(n log n) O(1)回答可重复贡献问题(RMQ/GCD)，不支持修改 |
| fenwick | [树状数组(BIT)](nodes/fenwick.md) | basic | P0 | lowbit分组，O(log n)单点修改+前缀查询，代码短常数小 |
| fenwick-extended | [扩展树状数组](nodes/fenwick-extended.md) | intermediate | P1 | 差分实现区间修改+区间查询(双BIT)，或双BIT维护不可差分信息O(log²n) |
| rmq-linear | [线性RMQ(±1 RMQ)](nodes/rmq-linear.md) | advanced | P2 | O(n)预处理O(1)查询的RMQ，基于笛卡尔树规约+LCA(±1 RMQ)+分块位掩码 |

## G-A-6 线段树族

- 领域: 数据结构 · 阶段范围: 中级→高级 · 节点数: 4

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| seg-basic | [线段树基础](nodes/seg-basic.md) | intermediate | P0 | O(log n)单点修改+区间查询，递归建树合并子节点信息 |
| seg-lazy | [懒标记线段树](nodes/seg-lazy.md) | intermediate | P0 | 区间修改+区间查询，lazy tag延迟下发均摊O(log n) |
| seg-dynamic | [动态开点线段树](nodes/seg-dynamic.md) | advanced | P1 | 按需创建节点，支持大值域离散化无需预先开空间 |
| seg-merge | [线段树合并与分裂](nodes/seg-merge.md) | advanced | P1 | 合并多棵动态开点线段树，用于树上信息合并；分裂还原 |

## G-A-7 可持久化数据结构族

- 领域: 数据结构 · 阶段范围: 中级→高级 · 节点数: 1

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| persistent-concept | [可持久化数据结构概念](nodes/persistent-concept.md) | intermediate | P1 | 保留所有历史版本的数据结构：部分可持久化（只读旧版本）vs 完全可持久化（旧版本可继续修改），以可持久化线段树（主席树）为最典型实现。 |

## G-A-8 平衡二叉搜索树族

- 领域: 数据结构 · 阶段范围: 中级→高级 · 节点数: 9

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| bst | [二叉搜索树基础](nodes/bst.md) | intermediate | P1 | 左<根<右性质，期望O(log n)操作，最坏O(n)退化 |
| treap | [Treap(树堆)](nodes/treap.md) | advanced | P1 | BST+堆随机优先级，旋转维护平衡，期望O(log n) |
| fhq-treap | [无旋Treap(FHQ Treap)](nodes/fhq-treap.md) | advanced | P1 | 按值/按秩分裂合并，无需旋转，可持久化友好 |
| splay | [Splay(伸展树)](nodes/splay.md) | advanced | P1 | 伸展操作将访问节点旋至根，均摊O(log n)，LCT基础 |
| sgt | [替罪羊树(Scapegoat Tree)](nodes/sgt.md) | advanced | P2 | 不平衡时按比例重构子树，O(log n)均摊 |
| sbt | [Size Balanced Tree(SBT)](nodes/sbt.md) | advanced | P2 | 按子树size维护平衡，O(log n)操作 |
| avl | [AVL树](nodes/avl.md) | advanced | P2 | 严格平衡(高度差<=1)，旋转维护 |
| wblt | [WBLT(加权平衡叶树)](nodes/wblt.md) | advanced | P2 | 按子树权重维护平衡，支持可持久化 |
| rbtree | [红黑树](nodes/rbtree.md) | advanced | P3 | 弱平衡BST，C++ std::map底层，竞赛中少用 |

## G-A-9 高级树结构族

- 领域: 数据结构 · 阶段范围: 高级→前沿 · 节点数: 2

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| cartesian-tree | [笛卡尔树（Cartesian Tree）](nodes/cartesian-tree.md) | intermediate | P1 | 键满足 BST 性质、值满足堆性质的二叉树，用单调栈 O(n) 构建；把 RMQ 转成树上 LCA，可 O(n)~O(1) 求区间最值，也是 Treap 的理论基础。 |
| tree-decompose | [树分块](nodes/tree-decompose.md) | advanced | P3 | 把树划分成 O(√n) 个块（关键点/块边界），块内暴力、块间预统计，配合树上莫队与 bitset 处理树上路径颜色统计、mex 等查询。 |

## G-A-10 哈希与链表族

- 领域: 数据结构 · 阶段范围: 基础→中级 · 节点数: 3

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| hash-table | [哈希表（散列表）](nodes/hash-table.md) | basic | P0 | key-value 映射，哈希函数+冲突处理（开链/开放寻址），期望 O(1) 插入/查找 |
| linked-list | [链表](nodes/linked-list.md) | basic | P1 | 节点指针串联，O(1) 插入删除，O(n) 随机访问，注意边界哨兵 |
| skiplist | [跳表（Skip List）](nodes/skiplist.md) | intermediate | P3 | 多层有序链表随机化，期望 O(log n) 查找/插入/删除，实现简单于平衡树 |

## G-A-11 动态规划基础族

- 领域: 动态规划 · 阶段范围: 基础→中级 · 节点数: 15

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| dp-basic | [动态规划基础](nodes/dp-basic.md) | basic | P0 | 最优子结构/无后效性/子问题重叠，状态定义与转移方程 |
| dp-memo | [记忆化搜索](nodes/dp-memo.md) | basic | P0 | 自顶向下DFS+缓存，DP的递归实现方式 |
| dp-knapsack01 | [0-1背包](nodes/dp-knapsack01.md) | basic | P0 | 每个物品取/不取，O(nW)转移，滚动数组优化空间 |
| dp-knapsack-complete | [完全背包](nodes/dp-knapsack-complete.md) | basic | P0 | 每件物品无限取，正序遍历容量 |
| dp-knapsack-multiple | [多重背包](nodes/dp-knapsack-multiple.md) | intermediate | P1 | 每件物品有限数量，二进制拆分或单调队列优化 |
| dp-knapsack-group | [分组背包](nodes/dp-knapsack-group.md) | intermediate | P1 | 物品分组，每组最多选一件 |
| dp-linear | [线性DP(LIS/LCS)](nodes/dp-linear.md) | basic | P0 | 一维序列上的DP，最长递增子序列/最长公共子序列 |
| dp-interval | [区间DP](nodes/dp-interval.md) | intermediate | P0 | f(i,j)表示区间[i,j]最优，枚举合并点k，O(n^3) |
| dp-tree | [树形DP](nodes/dp-tree.md) | intermediate | P0 | 树上递归DP，DFS后序传递子树最优解到父节点 |
| dp-tree-knapsack | [树上背包](nodes/dp-tree-knapsack.md) | intermediate | P1 | 树形DP+背包结合，依赖关系物品选择 |
| dp-state | [状压DP](nodes/dp-state.md) | intermediate | P1 | 集合状态编码为二进制整数，适合小规模状态空间 |
| dp-count | [计数DP](nodes/dp-count.md) | intermediate | P1 | 利用DP记忆化求计数问题，划分子集不重不漏 |
| dp-number | [数位DP](nodes/dp-number.md) | intermediate | P1 | 按数位逐位枚举，记忆化记录合法状态，大区间计数 |
| dp-dag | [DAG上的DP](nodes/dp-dag.md) | intermediate | P1 | 有向无环图上的最长/最短路，拓扑序转移 |
| dp-probability | [概率/期望DP](nodes/dp-probability.md) | intermediate | P1 | 概率顺推/期望逆推，可能需高斯消元处理环依赖 |

## G-A-12 DP优化族

- 领域: 动态规划 · 阶段范围: 中级→高级 · 节点数: 9

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| dp-opt-overview | [DP优化概述](nodes/dp-opt-overview.md) | intermediate | P1 | 利用数据结构/数学性质/状态设计降低DP转移复杂度 |
| dp-opt-monotonic-queue | [单调队列/栈优化DP](nodes/dp-opt-monotonic-queue.md) | intermediate | P1 | 用单调队列维护滑动窗口最值加速转移，如多重背包 |
| dp-opt-slope | [斜率优化DP](nodes/dp-opt-slope.md) | advanced | P1 | 转移方程化为一次函数，凸壳上二分/单调队列维护最值 |
| dp-opt-quadrangle | [四边形不等式/决策单调性优化](nodes/dp-opt-quadrangle.md) | advanced | P2 | w满足四边形不等式则决策单调，分治/单调队列优化 |
| dp-opt-divide-conquer | [分治优化DP](nodes/dp-opt-divide-conquer.md) | advanced | P1 | 决策点单调时利用分治缩小决策空间，O(n log n) |
| dp-opt-slope-trick | [Slope Trick](nodes/dp-opt-slope-trick.md) | advanced | P2 | 维护凸函数的斜率/拐点序列，简化凸DP转移 |
| dp-opt-wqs | [WQS二分/凸优化DP](nodes/dp-opt-wqs.md) | advanced | P2 | 带数量限制的凸DP，二分惩罚系数消除限制 |
| dp-opt-state | [状态设计优化](nodes/dp-opt-state.md) | intermediate | P2 | 改变状态定义降低维度/状态数，题目特异性优化 |
| dp-opt-data-structure | [数据结构优化DP](nodes/dp-opt-data-structure.md) | intermediate | P1 | 用线段树/BIT/平衡树加速转移中的查询/修改操作 |

## G-A-13 高级DP族

- 领域: 动态规划 · 阶段范围: 高级→前沿 · 节点数: 3

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| dp-plug | [插头DP（连通性状态压缩DP）](nodes/dp-plug.md) | advanced | P2 | 轮廓线DP + 连通性编码，逐格转移，解决网格图的哈密顿回路/路径计数、生成树计数等问题 |
| dp-dynamic | [动态DP（DDP）](nodes/dp-dynamic.md) | advanced | P2 | 带点权/边权修改的树上DP，用广义矩阵乘法（max,+）把转移写成矩阵，树链剖分+线段树/LCT维护单点修改后 O(log²n) 或 O(log n) 更新答案 |
| dp-dpofdp | [DP套DP](nodes/dp-dpofdp.md) | advanced | P3 | 外层DP的状态是内层DP的结果（DFA状态），内层DP被抽象为自动机供外层转移，用于序列计数/概率/期望问题 |

## G-A-14 搜索算法族

- 领域: 搜索算法 · 阶段范围: 基础→高级 · 节点数: 9

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| backtracking | [回溯法](nodes/backtracking.md) | basic | P0 | DFS+撤销操作，走不通就回头，排列/组合/棋盘类问题 |
| bidirectional | [双向搜索/Meet in the Middle](nodes/bidirectional.md) | intermediate | P1 | 从两端同时搜索或折半枚举，O(2^{n/2})降低指数 |
| iterative-deepening | [迭代加深(IDDFS)](nodes/iterative-deepening.md) | intermediate | P1 | 逐步增加DFS深度限制，DFS方式实现BFS效果，空间优 |
| heuristic-search | [启发式搜索](nodes/heuristic-search.md) | intermediate | P1 | 估价函数引导分支选择，可行性/最优性剪枝 |
| astar | [A*算法](nodes/astar.md) | intermediate | P1 | f=g+h优先队列搜索，可采纳启发函数保证最优性 |
| idastar | [IDA*算法](nodes/idastar.md) | intermediate | P1 | 迭代加深+A*剪枝，限制路径成本而非深度 |
| search-pruning | [搜索剪枝优化](nodes/search-pruning.md) | intermediate | P1 | 可行性剪枝/最优性剪枝/搜索顺序优化，减少搜索量 |
| minimax-alpha-beta | [Minimax/Alpha-Beta剪枝](nodes/minimax-alpha-beta.md) | intermediate | P2 | 博弈对抗搜索，Alpha-Beta剪枝减少不必要分支 |
| dlx | [Dancing Links(X算法)](nodes/dlx.md) | advanced | P2 | 双向十字链表加速精确覆盖/重复覆盖问题的回溯搜索 |

## G-B-1 图基础与遍历

- 领域: 图论 · 阶段范围: 基础 · 节点数: 6

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| graph-basics | [图论基础概念](nodes/graph-basics.md) | basic | P0 | 图的基本概念：点、边、有向/无向图、度、路径、环、子图 |
| graph-storage | [图的存储](nodes/graph-storage.md) | basic | P0 | 邻接矩阵、邻接表、链式前向星等存图方式 |
| bfs | [BFS广度优先搜索](nodes/bfs.md) | basic | P0 | 按层遍历图，队列实现O(V+E)，可求无权最短路 |
| dfs | [DFS深度优先搜索](nodes/dfs.md) | basic | P0 | 递归深入遍历O(V+E)，连通性判定与DFS生成树基础；沿一条路径深入到底再回溯，栈/递归实现，空间O(h) |
| topo-sort | [拓扑排序](nodes/topo-sort.md) | basic | P0 | DAG节点线性排序，Kahn算法(入度BFS)或DFS逆序O(V+E) |
| connected-components | [连通分量](nodes/connected-components.md) | basic | P0 | 无向图连通块，BFS/DFS遍历标记O(V+E) |

## G-B-2 最短路族

- 领域: 图论 · 阶段范围: 基础→高级 · 节点数: 8

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| dijkstra | [Dijkstra算法](nodes/dijkstra.md) | basic | P0 | 非负权单源最短路，堆优化O((V+E)logV)，贪心松弛 |
| floyd | [Floyd-Warshall算法](nodes/floyd.md) | basic | P0 | 全源最短路，DP三重循环O(V³)，可处理负权 |
| bellman-ford | [Bellman-Ford算法](nodes/bellman-ford.md) | intermediate | P1 | 含负权单源最短路，松弛操作O(VE)，可判负环 |
| spfa | [SPFA算法](nodes/spfa.md) | intermediate | P1 | Bellman-Ford队列优化，均摊快但最坏O(VE) |
| johnson | [Johnson算法](nodes/johnson.md) | intermediate | P1 | 全源最短路，势能法处理负权，n次Dijkstra O(VElogV) |
| bfs-01 | [0-1 BFS](nodes/bfs-01.md) | intermediate | P1 | 双端队列处理0/1权边最短路O(V+E) |
| kth-shortest-path | [k短路](nodes/kth-shortest-path.md) | advanced | P2 | 第k短路径，A*或可并堆方法 |
| mod-shortest-path | [同余最短路](nodes/mod-shortest-path.md) | advanced | P3 | 利用同余类建图求最小权值，模数优化 |

## G-B-3 生成树族

- 领域: 图论 · 阶段范围: 基础→高级 · 节点数: 6

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| kruskal | [Kruskal算法](nodes/kruskal.md) | basic | P0 | 最小生成树：把边按权值从小到大排序，并查集维护连通性，不成环则加入，O(E log E)；贪心+并查集的经典 |
| prim | [Prim算法](nodes/prim.md) | basic | P0 | 最小生成树，贪心+堆O(E log V)，适合稠密图(暴力O(n^2)在完全图上最优) |
| second-best-mst | [次小生成树](nodes/second-best-mst.md) | advanced | P2 | 严格次小生成树，Kruskal建MST+倍增求环上最大边替换，O(m log n) |
| dmst | [最小树形图(DMST)](nodes/dmst.md) | advanced | P2 | 有向图最小生成树，朱刘算法(Edmonds) O(VE)，缩环+入边修正 |
| steiner-tree | [Steiner树](nodes/steiner-tree.md) | advanced | P2 | 给定关键点集的最小连通子图，NP-hard，状压DP f[i][S]+Dijkstra松弛 O(3^k n + 2^k m log n) |
| matrix-tree | [矩阵树定理](nodes/matrix-tree.md) | advanced | P2 | Laplace矩阵任一n-1阶主子式的行列式 = 生成树个数，O(n^3) |

## G-B-4 连通性族

- 领域: 图论 · 阶段范围: 中级→高级 · 节点数: 7

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| tarjan-scc | [Tarjan强连通分量](nodes/tarjan-scc.md) | intermediate | P0 | 有向图强连通分量，DFS+dfn/low O(V+E)，缩点成DAG |
| cut-vertex | [割点(关节点)](nodes/cut-vertex.md) | intermediate | P1 | 删除后使图极大连通分量数增加的点，Tarjan(dfn/low)判定O(V+E)，根节点需特判子节点数 |
| bridge | [割边(桥)](nodes/bridge.md) | intermediate | P1 | 删除后使图不连通的边，Tarjan判定low[v]>dfn[u]得桥O(V+E)，有重边需按边编号处理 |
| bcc | [双连通分量(BCC)](nodes/bcc.md) | intermediate | P1 | 点双(无割点)/边双(无桥)极大连通子图，Tarjan+栈分解，O(V+E)，点双缩点得圆方树 |
| two-sat | [2-SAT](nodes/two-sat.md) | intermediate | P1 | 2-适定性问题：布尔方程(a∨b)型约束，建蕴含图+SCC判定，用SCC反拓扑序赋解O(V+E) |
| dominator-tree | [支配树](nodes/dominator-tree.md) | advanced | P2 | 有向图支配关系树：Lengauer-Tarjan算法O((V+E)α)，DAG/树有特例O((V+E)log)解法 |
| block-forest | [圆方树](nodes/block-forest.md) | advanced | P3 | 点双连通缩点的树形结构：原图点=圆点、点双=方点，把一般无向图问题转化为树上问题 |

## G-B-5 网络流族

- 领域: 图论 · 阶段范围: 中级→高级 · 节点数: 6

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| max-flow | [最大流（Ford-Fulkerson / Edmonds-Karp）](nodes/max-flow.md) | intermediate | P1 | Ford-Fulkerson 增广路思想：残量网络 + 反向边退流；EK 用 BFS 找最短增广路 O(VE²)。 |
| dinic | [Dinic 最大流](nodes/dinic.md) | intermediate | P1 | BFS 分层图 + DFS 多路增广阻塞流 + 当前弧优化，O(V²E)；二分图匹配单位容量图 O(E√V)。 |
| min-cut | [最小割](nodes/min-cut.md) | intermediate | P1 | s-t 割：把点分成 S（含 s）与 T（含 t），割容量 = S→T 边容量和；最大流最小割定理：s-t 最小割 = 最大流。 |
| min-cost-flow | [最小费用最大流（SSP）](nodes/min-cost-flow.md) | advanced | P2 | SSP（Successive Shortest Path）：每次沿单位费用最短的增广路增广，SPFA/Bellman-Ford 或势能+Dijkstra 找路。 |
| bounded-flow | [上下界网络流](nodes/bounded-flow.md) | advanced | P3 | 边流量限 b≤f≤c：无源汇可行流、有源汇可行流/最大流/最小流，通过附加源汇 + 超级源汇跑最大流转化。 |
| stoer-wagner | [Stoer-Wagner 全局最小割](nodes/stoer-wagner.md) | advanced | P3 | 无向正权图的全局最小割（任意 s-t 划分的最小割）：最大邻接贪心合并 + 递归收缩，O(V³)（朴素）或 O(VE+V²log V)。 |

## G-B-6 二分图与匹配族

- 领域: 图论 · 阶段范围: 基础→高级 · 节点数: 5

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| bipartite-check | [二分图判定](nodes/bipartite-check.md) | basic | P0 | BFS/DFS染色法判定二分图O(V+E) |
| hungarian | [匈牙利算法(Kuhn)](nodes/hungarian.md) | intermediate | P1 | 二分图最大匹配，增广路O(VE) |
| km-algorithm | [KM算法](nodes/km-algorithm.md) | intermediate | P1 | 二分图最大权匹配(Kuhn-Munkres)O(V³) |
| hopcroft-karp | [Hopcroft-Karp算法](nodes/hopcroft-karp.md) | advanced | P2 | 二分图匹配，多增广路O(E√V) |
| general-match | [一般图匹配](nodes/general-match.md) | advanced | P3 | 带花树算法(Blossom)，一般图最大匹配O(V³) |

## G-B-7 树算法族

- 领域: 图论 · 阶段范围: 基础→高级 · 节点数: 10

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| tree-basics | [树基础](nodes/tree-basics.md) | basic | P0 | 树的基本概念：根、叶、深度、子树、父亲；无根树/有根树定义，邻接表/父数组存储，DFS/BFS 遍历 |
| lca | [最近公共祖先(LCA)](nodes/lca.md) | intermediate | P0 | 倍增预处理O(VlogV)查询O(logV)，或Tarjan离线O(α)；欧拉序转RMQ可O(1)查询 |
| tree-diameter | [树的直径](nodes/tree-diameter.md) | basic | P0 | 树上最长简单路径，两次DFS或树形DP O(V)，负权边只能树形DP |
| tree-centroid | [树的重心](nodes/tree-centroid.md) | intermediate | P1 | 删除后最大连通块大小不超过 n/2 的节点，点分治/重心分解基础 |
| hld | [树链剖分(HLD)](nodes/hld.md) | intermediate | P1 | 重链剖分把树剖为若干重链，配合线段树 O(log^2 n) 维护路径/子树信息，亦可 O(log n) 求 LCA |
| dsu-on-tree | [启发式合并(dsu on tree)](nodes/dsu-on-tree.md) | intermediate | P1 | 轻儿子清空+重儿子保留的树上离线统计，子树查询 O(n log n) |
| centroid-decomposition | [点分治](nodes/centroid-decomposition.md) | advanced | P2 | 重心递归分解，统计树上路径 O(n log n)，建点分树后支持带修 |
| virtual-tree | [虚树](nodes/virtual-tree.md) | advanced | P2 | 把关键点及其 LCA 压缩成小树，DP 复杂度从 O(nq) 降到 O(Σk log k) |
| prufer-code | [Prüfer序列](nodes/prufer-code.md) | advanced | P2 | 树与 n-2 长度序列的双射，证明 Cayley 公式 n^(n-2)，标号树计数利器 |
| tree-hash | [树哈希](nodes/tree-hash.md) | advanced | P3 | 把子树哈希成多重集函数值，判定有根/无根树同构 |

## G-B-8 欧拉与哈密顿族

- 领域: 图论 · 阶段范围: 中级→高级 · 节点数: 3

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| euler-path | [欧拉路/欧拉回路](nodes/euler-path.md) | intermediate | P1 | 经过每条边恰好一次的路径/回路：度数判定 + Hierholzer 算法 O(V+E)，支持有向/无向与字典序最小输出 |
| hamilton-path | [哈密顿路/回路](nodes/hamilton-path.md) | advanced | P3 | 经过每个顶点恰好一次的路径/回路：一般图 NP-hard，无向图用状压 DP O(2ⁿn²)（有向旅行商也是），小规模或竞赛图有充分条件 |
| min-cycle | [最小环](nodes/min-cycle.md) | advanced | P2 | 求图中边权和最小的环（围长）：Floyd 扩展 O(n³)、Dijkstra 删边 O(m(n+m)log n)、暴力 O(n²m)，可记录路径 |

## G-B-9 图论高级专题

- 领域: 图论 · 阶段范围: 中级→高级 · 节点数: 5

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| dag-dp | [差分约束 / DAG 最短路 DP](nodes/dag-dp.md) | intermediate | P1 | 差分约束系统建图+最短路判负环；DAG 上按拓扑序 DP 求最长/最短路 |
| chord-graph | [弦图](nodes/chord-graph.md) | advanced | P3 | 任意>3环都有弦的图，完美消除序列(MCS)使最大团/色数/独立集等NP难问题O(n+m)可解 |
| planar-graph | [平面图](nodes/planar-graph.md) | advanced | P3 | 可嵌入平面的图：欧拉公式V-E+F=2、对偶图转最短路/最小割、稀疏边数\|E\|≤3\|V\|-6 |
| max-clique | [最大团](nodes/max-clique.md) | advanced | P3 | NP-hard，Bron-Kerbosch回溯或状压DP |
| lgv-lemma | [LGV行列式引理](nodes/lgv-lemma.md) | advanced | P3 | Lindström-Gessel-Viennot引理，不相交路径计数 |

## G-C-1 字符串匹配族

- 领域: 字符串 · 阶段范围: 中级→高级 · 节点数: 5

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| kmp | [KMP算法](nodes/kmp.md) | intermediate | P0 | 线性时间字符串匹配，前缀函数(pi数组)避免回溯，O(n+m) |
| z-function | [Z函数](nodes/z-function.md) | intermediate | P1 | Z数组 z[i]=LCP(S, S[i..])，线性构造O(n)，用于匹配与周期判断 |
| boyer-moore | [Boyer-Moore](nodes/boyer-moore.md) | advanced | P2 | 坏字符+好后缀双规则从后往前匹配，平均子线性 O(n/m)~O(n)，最坏 O(nm) |
| string-hash | [字符串哈希](nodes/string-hash.md) | intermediate | P0 | 多项式哈希，O(1)比较任意子串，双哈希/大素数防碰撞 |
| rabin-karp | [Rabin-Karp](nodes/rabin-karp.md) | intermediate | P1 | 基于滚动哈希的字符串匹配，O(n+m)期望，多模式匹配友好 |

## G-C-2 字典树与AC自动机族

- 领域: 字符串 · 阶段范围: 中级→高级 · 节点数: 2

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| trie | [Trie 字典树](nodes/trie.md) | intermediate | P0 | 树形结构存储多字符串公共前缀，插入/查询 O(\|S\|)，是 AC 自动机与可持久化 Trie 的基础 |
| ac-automaton | [AC 自动机](nodes/ac-automaton.md) | advanced | P1 | Trie + KMP 失配指针，多模式串匹配自动机，预处理 O(Σ\|s\|)，匹配 O(文本长+z) |

## G-C-3 后缀结构族

- 领域: 字符串 · 阶段范围: 高级→前沿 · 节点数: 4

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| suffix-array | [后缀数组](nodes/suffix-array.md) | advanced | P1 | SA+rank+height数组，对字符串所有后缀排序，配合LCP做子串统计与匹配 |
| suffix-array-optimal | [最优原地后缀数组](nodes/suffix-array-optimal.md) | frontier | P3 | 线性时间O(n)且O(1)额外空间构造后缀数组的变体(SA-IS等) |
| suffix-tree | [后缀树](nodes/suffix-tree.md) | advanced | P2 | 压缩所有后缀的Trie，Ukkonen算法O(n)在线构造，SA/SAM的等价结构 |
| suffix-bst | [后缀平衡树](nodes/suffix-bst.md) | frontier | P3 | 用平衡BST维护后缀排序，支持动态插入删除字符的后缀结构 |

## G-C-4 后缀自动机族

- 领域: 字符串 · 阶段范围: 高级→前沿 · 节点数: 3

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| suffix-automaton | [后缀自动机(SAM)](nodes/suffix-automaton.md) | advanced | P2 | 识别字符串所有子串的最小 DFA，O(n) 在线构造，endpos 等价类 + 后缀链接树，解决不同子串计数/出现次数/最长公共子串等一揽子问题 |
| general-sam | [广义后缀自动机(GSAM)](nodes/general-sam.md) | frontier | P2 | 多字符串的 SAM：先在多串上建 Trie，再 BFS 逐节点在 Trie 上做 SAM 增量插入，支持多串不同子串计数、多串最长公共子串等 |
| seq-automaton | [序列自动机](nodes/seq-automaton.md) | advanced | P2 | 接受一个串所有子序列的最小自动机：next[i][c]=i 之后字符 c 第一次出现的位置，O(n\|Σ\|) 构造，用于子序列匹配与计数 DP |

## G-C-5 回文族

- 领域: 字符串 · 阶段范围: 中级→高级 · 节点数: 2

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| manacher | [Manacher 算法（O(n) 最长回文子串）](nodes/manacher.md) | intermediate | P1 | 利用回文的对称性维护『最右回文串』边界，O(n) 求出所有奇/偶长度回文半径数组 d1/d2，进而得到最长回文子串，是最重要的回文串线性算法。 |
| palindrome-automaton | [回文自动机 / 回文树（PAM，Palindromic Automaton）](nodes/palindrome-automaton.md) | advanced | P2 | 存储串中所有本质不同回文子串的最小 DFA（O(n) 个状态），增量 O(n) 构造；转移边表示在回文串两端加同一字符，fail 指向最长回文后缀，支持统计出现次数、最小回文划分等。 |

## G-C-6 Lyndon与周期族

- 领域: 字符串 · 阶段范围: 高级→前沿 · 节点数: 3

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| lyndon-factorization | [Lyndon分解](nodes/lyndon-factorization.md) | advanced | P2 | Duval 算法 O(n) 将字符串分解为字典序非严格递减的 Lyndon 串，同时给出最小循环移位；周期性与字典序的强力工具 |
| main-lorentz | [Main-Lorentz（重串查找）](nodes/main-lorentz.md) | frontier | P3 | 分治 + Z 函数找出字符串所有平方串（重串）的压缩表示，O(n log n)，用于周期结构统计 |
| minimal-string | [最小表示法](nodes/minimal-string.md) | advanced | P2 | O(n) 求循环字符串字典序最小的起始位置：双指针跳过法或 Lyndon/Duval 法，用于循环同构判断与去重 |

## G-C-7 数论基础族

- 领域: 数学 · 阶段范围: 基础→中级 · 节点数: 10

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| sieve-eratosthenes | [埃氏筛](nodes/sieve-eratosthenes.md) | basic | P0 | O(n log log n)筛素数，标记合数，基础素数筛法 |
| sieve-linear | [线性筛(欧拉筛)](nodes/sieve-linear.md) | intermediate | P0 | O(n)筛素数，每个合数只被最小质因子筛一次，可同时求积性函数 |
| euclidean-gcd | [欧几里得算法(GCD)](nodes/euclidean-gcd.md) | basic | P0 | 辗转相除法求最大公约数，O(log min(a,b))，数论基础工具 |
| ext-euclidean | [扩展欧几里得](nodes/ext-euclidean.md) | intermediate | P0 | 求ax+by=gcd(a,b)的一组整数解，模逆元与线性方程的基础 |
| mod-arithmetic | [模算术](nodes/mod-arithmetic.md) | basic | P0 | 模意义下加减乘除运算，取模与负数处理，竞赛必备基础 |
| modular-inverse | [模逆元](nodes/modular-inverse.md) | intermediate | P0 | 求a在模m下的逆元，方法：扩展欧几里得/费马小定理/线性递推 |
| binary-exponentiation | [快速幂](nodes/binary-exponentiation.md) | basic | P0 | O(log n)计算a^n，二进制取幂，模意义下核心工具 |
| euler-totient | [欧拉函数](nodes/euler-totient.md) | intermediate | P0 | phi(n)表示1~n中与n互素的数个数，积性函数，欧拉定理基础 |
| fermat-little-theorem | [费马小定理](nodes/fermat-little-theorem.md) | intermediate | P0 | p素数时a^(p-1)≡1(mod p)，模逆元与素性检测的理论基础 |
| prime-test-basic | [素数判定(试除)](nodes/prime-test-basic.md) | basic | P0 | O(sqrt(n))试除法判定素数，基础方法，大数用Miller-Rabin |

## G-C-8 数论进阶族

- 领域: 数学 · 阶段范围: 中级→高级 · 节点数: 8

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| crt | [中国剩余定理(CRT)](nodes/crt.md) | intermediate | P0 | 求解同余方程组，将模互素的大模数分解为小模数合并，exCRT处理不互素 |
| bsgs | [BSGS(大步小步)](nodes/bsgs.md) | advanced | P1 | O(sqrt(p))求离散对数a^x≡b(mod p)，baby-step giant-step算法 |
| primitive-root | [原根](nodes/primitive-root.md) | advanced | P1 | 模 p 下阶为 φ(p) 的元素 g，其幂次跑遍全部既约剩余系，是 NTT、离散对数与离散根的基础；最小原根 O(φ^(1/4) log^2) 求解 |
| discrete-root | [离散k次根](nodes/discrete-root.md) | advanced | P2 | 求 x^k≡a (mod p) 的全部解：以原根 g 作对数坐标把问题化为离散对数 (g^k)^y≡a，BSGS 求一个解后用阶的结构扩展出全部解 |
| lucas-theorem | [卢卡斯定理](nodes/lucas-theorem.md) | advanced | P0 | C(n,m) mod p（p 为素数）：按 p 进制拆 n,m 后各位组合数相乘，O(p) 预处理阶乘 + O(log_p n) 每次查询，大组合数取小素模的标准工具 |
| extended-lucas | [扩展卢卡斯(exLucas)](nodes/extended-lucas.md) | advanced | P1 | C(n,m) mod p 当 p 为合数时：分解 p=∏p_i^α_i，对每个素因子幂用『去 p 因子阶乘+Legendre 公式』求余，CRT 合并；处理任意模数组合数 |
| mobius-inversion | [莫比乌斯反演](nodes/mobius-inversion.md) | advanced | P1 | 利用莫比乌斯函数 μ(n) 进行数论反演，把 [gcd(i,j)=1] 条件展开为 Σμ(d)，将 gcd 计数问题转化为可整除分块的求和 |
| quadratic-residue | [二次剩余](nodes/quadratic-residue.md) | advanced | P2 | 求 x^2≡a (mod p) 的解：Euler 判别法判定存在性，Cipolla 算法 O(log p) 求根（引入 F_p[x]/(x^2-g) 扩域），Tonelli-Shanks 亦可用 |

## G-C-9 数论高级族

- 领域: 数学 · 阶段范围: 高级→前沿 · 节点数: 11

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| pollard-rho | [Pollard–Rho 大整数分解](nodes/pollard-rho.md) | advanced | P1 | 期望 O(n^{1/4}) 找合数非平凡因子，生日悖论+伪随机序列环检测，配 Miller-Rabin 递归分解 |
| miller-rabin | [Miller–Rabin 素性测试](nodes/miller-rabin.md) | advanced | P1 | 概率性素性测试 O(k log n)，费马小定理+二次探测定理，可确定性判定 2^64 内整数 |
| integer-factorization | [大整数分解](nodes/integer-factorization.md) | advanced | P1 | 将合数分解为质因子乘积，试除法为基础，大数用 Pollard-Rho，配套约数计数/枚举 |
| du-sieve | [杜教筛](nodes/du-sieve.md) | frontier | P2 | O(n^{2/3}) 求积性函数前缀和，Dirichlet 卷积 + 数论分块 + 记忆化 |
| min-25-sieve | [Min_25 筛](nodes/min-25-sieve.md) | frontier | P3 | O(n^{3/4}/log n) 求积性函数前缀和，埃氏筛过程 + 有效点值压缩（Extended Eratosthenes Sieve） |
| powerful-number-sieve | [Powerful Number 筛](nodes/powerful-number-sieve.md) | frontier | P3 | O(n^{3/4}) 求积性函数前缀和，基于 PN 分解 f=g*h，h 仅在 PN 处非零 |
| meissel-lehmer | [Meissel–Lehmer 素数计数](nodes/meissel-lehmer.md) | frontier | P3 | 亚线性 O(n^{2/3}/log²n) 计算 π(x)（≤x 素数个数），递归容斥 φ(x,a) + P₂ |
| pell-equation | [佩尔方程](nodes/pell-equation.md) | frontier | P3 | x^2-Dy^2=1 的整数解，连分数法求解，最小解递推通项 |
| continued-fraction | [连分数](nodes/continued-fraction.md) | advanced | P2 | 实数的有理逼近，渐近分数递推，Pell方程与Stern-Brocot基础 |
| lift-the-exponent | [LTE引理](nodes/lift-the-exponent.md) | advanced | P2 | Lift the Exponent引理，求v_p(a^n-b^n)的公式，简化幂次整除问题 |
| dirichlet-convolution | [狄利克雷卷积](nodes/dirichlet-convolution.md) | advanced | P2 | 数论函数的卷积运算，莫比乌斯反演与杜教筛的理论框架 |

## G-C-10 组合计数基础族

- 领域: 数学 · 阶段范围: 基础→中级 · 节点数: 5

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| combination-number | [组合数](nodes/combination-number.md) | basic | P0 | C(n,m) 计算：杨辉递推/阶乘逆元预处理/Lucas，竞赛计数核心 |
| catalan-number | [卡特兰数](nodes/catalan-number.md) | intermediate | P1 | C_n=C(2n,n)/(n+1)，括号序列/二叉树/出栈序列等计数 |
| stars-and-bars | [插板法(Stars and Bars)](nodes/stars-and-bars.md) | intermediate | P0 | 将n个相同物品分给k组的方案数C(n+k-1,k-1)，整数拆分计数 |
| fibonacci | [斐波那契数列](nodes/fibonacci.md) | intermediate | P0 | F(n)=F(n-1)+F(n-2)，矩阵快速幂O(log n)求第n项，恒等式众多 |
| vandermonde-convolution | [范德蒙德卷积](nodes/vandermonde-convolution.md) | advanced | P2 | C(n+m,k)=sum C(n,i)C(m,k-i)，组合恒等式的重要工具 |

## G-C-11 组合进阶族

- 领域: 数学 · 阶段范围: 中级→高级 · 节点数: 8

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| inclusion-exclusion | [容斥原理](nodes/inclusion-exclusion.md) | intermediate | P1 | \|A1∪A2∪...\|=sum(-1)^k S(k)，多集合并集计数与莫比乌斯反演基础 |
| polya-enumeration | [Polya计数](nodes/polya-enumeration.md) | advanced | P2 | Burnside引理+循环指标多项式：本质不同染色数 = (1/\|G\|)Σ m^{c(g)}，m为颜色数、c(g)为置换g的轮换数 |
| burnside-lemma | [Burnside引理](nodes/burnside-lemma.md) | advanced | P2 | 群 G 在集合 X 上的轨道数 = (1/\|G\|)·Σ_{g∈G}\|Fix(g)\|，不动点平均数，Pólya 计数的基础 |
| derangement | [错排问题](nodes/derangement.md) | intermediate | P2 | D(n)=n!Σ_{k=0}^n (-1)^k/k! ≈ n!/e，无固定点（P_i≠i）排列数，递推 D_n=(n-1)(D_{n-1}+D_{n-2}) |
| stirling-number | [斯特林数](nodes/stirling-number.md) | advanced | P2 | 第一类 s(n,k)=将n个元素分成k个无标号非空轮换；第二类 S(n,k)=分成k个无标号非空子集；两类递推与幂/阶乘幂互转 |
| integer-partition | [整数划分](nodes/integer-partition.md) | advanced | P2 | p(n) 将 n 拆成正整数之和(顺序无关)的方案数，生成函数 ∏1/(1-x^k)，五边形数定理 O(n√n) |
| bell-number | [贝尔数](nodes/bell-number.md) | advanced | P2 | B(n) 将 n 个不同元素划分为任意个无标号非空子集的方案数，B_{n+1}=ΣC(n,k)B_k，EGF=e^{e^x-1} |
| eulerian-number | [欧拉数](nodes/eulerian-number.md) | frontier | P3 | A(n,m)=恰好 m 个『上升』(P_i<P_{i+1})的排列数，递推 (n-m)A(n-1,m-1)+(m+1)A(n-1,m)，Worpitzky 恒等式 |

## G-C-12 多项式与FFT族

- 领域: 数学 · 阶段范围: 高级→前沿 · 节点数: 9

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| fft | [FFT(快速傅里叶变换)](nodes/fft.md) | advanced | P1 | O(n log n)计算多项式乘法，基于DFT与蝴蝶操作，NTT为模意义版本 |
| ntt | [NTT(数论变换)](nodes/ntt.md) | advanced | P1 | 模意义下FFT，用原根替代单位根避免浮点误差，998244353为常用模数 |
| fwt | [FWT(快速沃尔什变换)](nodes/fwt.md) | advanced | P2 | O(n log n)计算位运算(and/or/xor)卷积，FFT的位运算推广 |
| polynomial-basics | [多项式基础](nodes/polynomial-basics.md) | advanced | P1 | 多项式表示、求值、乘法、求导积分，FFT/NTT的前置知识 |
| multipoint-eval-interpolation | [多点求值与插值](nodes/multipoint-eval-interpolation.md) | frontier | P3 | O(n log^2 n)多项式多点求值与插值，基于分治与NTT |
| linear-recurrence | [线性递推](nodes/linear-recurrence.md) | advanced | P2 | 常系数齐次线性递推O(k log k log n)求第n项，BM+NTT+Cayley-Hamilton |
| berlekamp-massey | [Berlekamp-Massey](nodes/berlekamp-massey.md) | advanced | P2 | O(n^2)求序列最短线性递推式，配合NTT加速求第n项 |
| lagrange-inversion | [拉格朗日反演](nodes/lagrange-inversion.md) | frontier | P3 | O(n log n)求复合逆的系数，生成函数计数的高级工具 |
| newton-iteration-poly | [多项式牛顿迭代](nodes/newton-iteration-poly.md) | frontier | P3 | O(n log n)求多项式开根/对数/指数/逆，基于牛顿法推广到形式幂级数 |

## G-C-13 生成函数族

- 领域: 数学 · 阶段范围: 高级→前沿 · 节点数: 7

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| ogf | [OGF(普通生成函数)](nodes/ogf.md) | advanced | P2 | 序列 a 的普通生成函数 F(x)=Σ a_n x^n，加法=按项加、乘法=卷积，封闭形式 1/(1-px) 等比等 |
| egf | [EGF(指数生成函数)](nodes/egf.md) | advanced | P2 | 序列 a 的指数生成函数 F̂(x)=Σ a_n x^n/n!，乘法=二项式卷积，标号结构计数工具，e^{e^x-1} 等 |
| symbolic-method | [符号化方法](nodes/symbolic-method.md) | frontier | P3 | 组合类→生成函数系统化映射：SEQ/PSET/MSET/CYC 构造的 OGF/EGF 对应，Analytic Combinatorics 体系 |
| generating-function-basics | [生成函数基础](nodes/generating-function-basics.md) | advanced | P2 | 形式幂级数环与生成函数框架：定义、加乘卷积、求导积分、逆元、复合、常见展开式，OGF/EGF 的前置 |
| generating-function-shift | [生成函数平移](nodes/generating-function-shift.md) | frontier | P3 | 多项式平移 f(x+c) 与连续点值平移 f(0..n)→f(c..c+n)，Taylor公式/二项式定理/Lagrange插值法，O(n log n) |
| poly-compose-inverse | [多项式复合与求逆](nodes/poly-compose-inverse.md) | frontier | P3 | f(g(x)) mod x^n 与复合逆：朴素 O(n²)/分治，Kinoshita-Li 2024 O(M(n)log n)，拉格朗日反演应用 |
| elementary-generating-functions | [初等生成函数](nodes/elementary-generating-functions.md) | frontier | P3 | 常见序列的生成函数闭式：几何/二项/指数/三角/对数等展开式，形式幂级数版 Taylor 级数表 |

## G-C-14 线性代数族

- 领域: 数学 · 阶段范围: 中级→高级 · 节点数: 9

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| matrix-basics | [矩阵基础](nodes/matrix-basics.md) | intermediate | P0 | 矩阵加减乘与转置，矩阵快速幂O(k^3 log n)，递推加速核心 |
| determinant | [行列式](nodes/determinant.md) | advanced | P0 | O(n^3)高斯消元法求行列式，矩阵树定理与计数应用基础 |
| gaussian-elimination | [高斯消元](nodes/gaussian-elimination.md) | intermediate | P0 | O(n^3)解线性方程组/求秩/求行列式，线性代数核心算法 |
| linear-system | [线性方程组](nodes/linear-system.md) | intermediate | P1 | 高斯消元求解Ax=b，判断唯一/无穷/无解，异或方程组变体 |
| linear-basis | [线性基](nodes/linear-basis.md) | intermediate | P0 | 异或空间基，O(n log max)插入，求最大/最小/第k小异或值 |
| matrix-rank | [矩阵秩](nodes/matrix-rank.md) | advanced | P2 | 高斯消元求矩阵秩，线性无关向量组最大个数 |
| vector-space | [向量空间](nodes/vector-space.md) | advanced | P2 | 线性空间、基与维数，线性基与矩阵秩的理论基础 |
| char-polynomial | [特征多项式](nodes/char-polynomial.md) | advanced | P2 | det(λI-A)，特征值与Cayley-Hamilton定理，线性递推加速基础 |
| diagonalization | [矩阵对角化](nodes/diagonalization.md) | advanced | P2 | A=PDP^{-1}，矩阵快速幂优化，特征值分解 |

## G-C-15 概率族

- 领域: 数学 · 阶段范围: 中级→高级 · 节点数: 4

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| probability-basics | [概率基础](nodes/probability-basics.md) | intermediate | P0 | 样本空间/事件域/概率空间三要素，古典概型与几何概型，概率公理与基本性质 |
| conditional-probability | [条件概率](nodes/conditional-probability.md) | intermediate | P1 | P(B\|A)=P(AB)/P(A)，概率乘法公式、全概率公式与贝叶斯公式，事件独立性 |
| random-variable | [随机变量](nodes/random-variable.md) | advanced | P2 | 随机变量是样本空间到实数的函数，离散/连续型分布与分布函数、密度函数，随机变量独立性 |
| expectation-variance | [期望与方差](nodes/expectation-variance.md) | intermediate | P0 | 离散/连续期望定义，期望线性性与乘积期望，方差/标准差，条件期望与全期望公式 |

## G-C-16 数值方法族

- 领域: 数学 · 阶段范围: 中级→高级 · 节点数: 3

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| newton-method | [牛顿迭代法](nodes/newton-method.md) | advanced | P2 | 用切线迭代求函数零点：x_{i+1}=x_i−f(x_i)/f'(x_i)，平方收敛，用于求平方根/整数平方根/高精度开方及多项式牛顿迭代基础 |
| simpson-integration | [Simpson 积分（自适应辛普森法）](nodes/simpson-integration.md) | advanced | P2 | 用二次函数逐段逼近被积函数的数值积分法，自适应地细分区间以保证精度，适合无法解析求积的定积分。 |
| numeric-binary-search | [数值二分（二分答案 / 实数二分 / 三分）](nodes/numeric-binary-search.md) | intermediate | P1 | 二分法在单调谓词/单调函数上以 O(log n)（整数域）或 O(log((R-L)/eps))（实数域）逼近最优解，是『答案二分』与方程求根的基础。 |

## G-C-18 大整数与数制族

- 领域: 数学 · 阶段范围: 基础→中级 · 节点数: 4

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| big-integer | [高精度(大整数)](nodes/big-integer.md) | intermediate | P0 | 大整数加减乘除：Python 原生 int 无上限直接可用；C++/PyPy 需数组模拟，乘法 O(n^2) 可 Karatsuba/FFT 加速，压位优化常数 |
| gray-code | [格雷码](nodes/gray-code.md) | intermediate | P2 | 相邻两数二进制仅一位不同的编码，G(n)=n^(n>>1)，逆变换 rev_g 逐位异或；用于汉密尔顿路径、汉诺塔、避免信号误判 |
| balanced-ternary | [平衡三进制](nodes/balanced-ternary.md) | intermediate | P3 | 用 {-1,0,1} 表示的三进制，负数无需符号位；2 进位成 Z 并高位加 1，用于天平称重等问题 |
| numeral-system | [数制转换](nodes/numeral-system.md) | basic | P2 | 任意进制间转换：整数除基取余法、小数乘基取整法，2/8/16 快速互转；Python int(x,base) 与 format() 内置支持 |

## G-D-1 凸包族

- 领域: 计算几何 · 阶段范围: 中级→高级 · 节点数: 7

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| convex-hull | [凸包(Andrew/Graham)](nodes/convex-hull.md) | intermediate | P1 | O(nlogn) 求点集凸包，Andrew 单调链与 Graham 扫描两种实现 |
| rotating-calipers | [旋转卡壳](nodes/rotating-calipers.md) | advanced | P1 | 在凸包上枚举对踵点，O(n) 求凸包直径/最小矩形覆盖 |
| half-plane-intersection | [半平面交](nodes/half-plane-intersection.md) | advanced | P1 | S&I 算法 O(nlogn) 求半平面交，结果为凸多边形 |
| convex-hull-trick | [凸包优化(CHT)](nodes/convex-hull-trick.md) | advanced | P2 | 维护下/上凸壳按斜率二分求 DP 转移最值，斜率优化经典 |
| minkowski-sum | [闵可夫斯基和](nodes/minkowski-sum.md) | advanced | P2 | 两凸多边形 Minkowski 和仍为凸多边形，用于碰撞检测/半平面并 |
| point-in-polygon | [点在多边形内判定](nodes/point-in-polygon.md) | advanced | P2 | 射线法判一般多边形，凸多边形用有序二分 O(logn) |
| enclosing-circle | [最小覆盖圆](nodes/enclosing-circle.md) | advanced | P1 | 随机增量法 O(期望n) 求覆盖所有点的最小圆(Welzl) |

## G-D-2 平面扫描与几何求交

- 领域: 计算几何 · 阶段范围: 中级→高级 · 节点数: 10

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| sweep-line | [扫描线](nodes/sweep-line.md) | advanced | P1 | 线扫过平面处理事件，求矩形面积并/周长并/二维数点 |
| line-intersection | [直线交点](nodes/line-intersection.md) | intermediate | P2 | 用叉积判定两直线位置关系并求交点坐标 |
| segment-intersection | [线段相交判定与求交](nodes/segment-intersection.md) | intermediate | P1 | 跨立实验判两线段是否相交并求交点，几何求交基础 |
| vertical-decomposition | [垂直剖分(梯形剖分)](nodes/vertical-decomposition.md) | advanced | P2 | 将平面按线段端点垂直切分为梯形单元，支持点定位与求交 |
| nearest-points | [最近点对](nodes/nearest-points.md) | advanced | P1 | 分治 O(nlogn) 求平面最近点对，合并时按扫描线对检查 |
| triangulation | [三角剖分](nodes/triangulation.md) | advanced | P2 | 将平面点集细分为三角形，常用耳切与对偶图 |
| delaunay-triangulation | [Delaunay 三角剖分](nodes/delaunay-triangulation.md) | frontier | P3 | 满足空圆性质的三角剖分，对偶为 Voronoi 图 |
| circle-intersection | [圆与直线/圆求交](nodes/circle-intersection.md) | advanced | P2 | 解几何方程求圆与直线、圆与圆交点 |
| tangents-two-circles | [两圆公切线](nodes/tangents-two-circles.md) | advanced | P2 | 求两圆内外公切线，几何方程或向量构造 |
| segments-union-length | [线段并集长度](nodes/segments-union-length.md) | advanced | P2 | 扫描线求一维/二维线段并集长度，离散化+区间合并 |

## G-D-3 计算几何基础与度量

- 领域: 计算几何 · 阶段范围: 基础→高级 · 节点数: 7

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| 2d-geometry | [二维几何基础](nodes/2d-geometry.md) | basic | P1 | 向量运算/点积叉积/多边形面积/线段相交/直线交点等二维计算几何基础 |
| 3d-geometry | [三维几何](nodes/3d-geometry.md) | advanced | P2 | 三维向量/平面/法向量/多面体体积与表面积，由二维推广 |
| distance-metric | [距离度量](nodes/distance-metric.md) | intermediate | P2 | 欧氏/曼哈顿/切比雪夫距离及其变换(切比雪夫↔曼哈顿) |
| pick-theorem | [皮克定理](nodes/pick-theorem.md) | intermediate | P2 | A=i+b/2-1 关联整点多边形面积与内部/边上格点数 |
| lattice-points | [格点计数](nodes/lattice-points.md) | advanced | P2 | 线段/多边形内整点计数，结合皮克定理与整除递推 |
| random-incremental | [随机增量法](nodes/random-incremental.md) | advanced | P2 | 按随机序逐点加入并增量维护结构，期望线性复杂度 |
| geometric-inverse | [反演变换](nodes/geometric-inverse.md) | advanced | P2 | 圆/直线相切问题经反演简化，保角变换 |

## G-D-4 树链剖分与动态树

- 领域: 高级数据结构 · 阶段范围: 高级→前沿 · 节点数: 3

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| lct | [Link-Cut Tree（LCT，动态树）](nodes/lct.md) | advanced | P1 | 用 Splay 森林维护实链剖分（Preferred Path Decomposition）的动态树数据结构，支持 O(log n) 均摊的加边、删边、换根、路径修改与路径查询。 |
| euler-tour-tree | [Euler Tour Tree（ETT，欧拉游览树）](nodes/euler-tour-tree.md) | advanced | P2 | 把树映射为欧拉游览序列，将动态树的连边/断边/换根转化为序列的拆分与合并操作，用平衡树维护序列，适合维护子树信息（如子树最值）。 |
| top-tree | [Top Tree（Self-Adjusting Top Tree，SATT）](nodes/top-tree.md) | frontier | P3 | 基于树收缩（Compress/Rake）的簇（Cluster）级动态树框架，Self-Adjusting Top Tree 用三叉树维护完全动态森林的路径与子树信息。 |

## G-D-5 可持久化数据结构

- 领域: 高级数据结构 · 阶段范围: 高级 · 节点数: 5

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| persistent-seg | [可持久化线段树(主席树)](nodes/persistent-seg.md) | advanced | P0 | 函数式线段树按版本共享节点，支持历史版本查询与区间k小值 |
| persistent-trie | [可持久化 Trie](nodes/persistent-trie.md) | advanced | P1 | 保存历史版本的Trie，支持区间异或最值等查询 |
| persistent-balanced | [可持久化平衡树](nodes/persistent-balanced.md) | advanced | P2 | 可持久化无旋转Treap，函数式节点复用实现历史版本 |
| persistent-heap | [可持久化堆](nodes/persistent-heap.md) | advanced | P2 | 可持久化可并堆(左偏树)，常用于k短路问题 |
| persistent-block-array | [可持久化分块数组](nodes/persistent-block-array.md) | advanced | P2 | 分块数组的每个版本保留一份块副本，单点修改 O(sqrt n) 拷贝、查询 O(sqrt n)，空间 O(n + V·B) |

## G-D-6 分块与根号算法

- 领域: 高级数据结构 · 阶段范围: 中级→高级 · 节点数: 6

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| sqrt-decomposition | [根号分块（通用分块）](nodes/sqrt-decomposition.md) | intermediate | P1 | 按块长 √n 分块，整块维护（打标记/预统计）+ 散块暴力，单次操作 O(√n)；通用性最强的区间结构。 |
| block-array | [块状数组（分块）](nodes/block-array.md) | advanced | P1 | 将数组分成O(√n)块，整块维护懒标记、散块暴力，实现O(√n)区间修改/查询 |
| block-list | [块状链表](nodes/block-list.md) | advanced | P2 | 链表+分块混合，节点指向数组，支持插入/删除/区间访问的O(√n)操作 |
| sqrt-tree | [Sqrt 树](nodes/sqrt-tree.md) | advanced | P2 | O(n log log n)预处理+O(1)查询的可结合运算静态区间询问结构，树高O(log log n) |
| cat-tree | [猫树（Cat Tree）](nodes/cat-tree.md) | advanced | P2 | 静态线段树分治预处理，跨中点询问O(1)合并，不支持修改 |
| kdt | [K-D Tree](nodes/kdt.md) | advanced | P2 | k维空间分块树，轮流按维度切分+中位数建树，处理最近邻与矩形查询 |

## G-D-7 莫队算法族

- 领域: 高级数据结构 · 阶段范围: 中级→前沿 · 节点数: 7

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| mo-algo-secondary-offline | [二次离线莫队](nodes/mo-algo-secondary-offline.md) | frontier | P3 | 单次转移非 O(1) 时把每次转移的贡献差分并再离线一次，用值域分块/扫描线批量处理，降低整体复杂度。 |
| mo-algo-with-bitset | [莫队 + bitset](nodes/mo-algo-with-bitset.md) | advanced | P2 | 莫队维护区间状态 + bitset 存储权值出现信息，转移后位运算加速判定/统计类问题（如区间集合并、交、对称差）。 |
| mo-modifiable | [带修莫队](nodes/mo-modifiable.md) | advanced | P2 | 给莫队加时间维，询问变三元组 (l,r,t)，块长 n^(2/3)，O(n^(5/3)) 支持单点修改的区间询问。 |
| mo-on-tree | [树上莫队](nodes/mo-on-tree.md) | advanced | P2 | 用欧拉括号序把树上路径压成序列，路径询问转化为序列区间询问后用莫队处理；LCA 不在区间时需临时加入。 |
| mo-rollback | [回滚莫队](nodes/mo-rollback.md) | advanced | P2 | 只增不删的莫队变体：同块询问暴力，跨块询问左端点每问重置回滚，处理「删除难、增加易」的区间统计，O(n√m)。 |
| mo-2d | [二维莫队](nodes/mo-2d.md) | advanced | P2 | 莫队扩展到二维矩阵：状态为 (x1,y1,x2,y2) 子矩形，四方向整行/整列扩展，块长 n*q^(-1/4)，复杂度 O(n²*q^(3/4))。 |
| mo-algorithm | [莫队算法（普通莫队）](nodes/mo-algorithm.md) | intermediate | P1 | 离线区间询问：按 l 所在块排序 + 奇偶化 r，双指针 O(1) 转移，O(n√n) 处理多类可差分区间的询问。 |

## G-D-8 高级线段树与离线

- 领域: 高级数据结构 · 阶段范围: 高级→前沿 · 节点数: 5

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| seg-beats | [吉司机线段树(Segment Beats)](nodes/seg-beats.md) | frontier | P2 | 区间取 min/max 等操作利用势能标记，均摊高效维护复杂区间信息 |
| li-chao-tree | [李超线段树](nodes/li-chao-tree.md) | advanced | P1 | 线段树维护线段/直线集合，标记永久化求横坐标处最值 |
| kinetic-tournament-tree | [Kinetic Tournament Tree](nodes/kinetic-tournament-tree.md) | frontier | P3 | 线段树维护线性函数序列，支持线段插入删除的最值查询 |
| segment-tree-offline | [线段树分治(离线)](nodes/segment-tree-offline.md) | advanced | P1 | 将时间轴建成线段树，把只存在于某时段的信息离线分发到节点 |
| nested-segment-tree | [线段树嵌套(树套树)](nodes/nested-segment-tree.md) | frontier | P3 | seg-in-seg/seg-in-bit/seg-in-balanced 等多维信息维护结构 |

## G-D-9 专题(topic 域)

- 领域: 高级专题 · 阶段范围: 中级→高级 · 节点数: 3

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| rmq | [RMQ 专题（区间最值查询）](nodes/rmq.md) | intermediate | P1 | Range Minimum/Maximum Query：静态区间最值。ST 表 O(n log n) 预处理 O(1) 查询；另有 Four Russians、±1RMQ 与基于笛卡尔树的 O(n)~O(1) 解法，动态版本用线段树。 |
| bracket-sequence | [括号序列专题](nodes/bracket-sequence.md) | intermediate | P2 | 合法括号序列的判定、计数（卡特兰数）、字典序后继、线段树维护括号序列的匹配（前缀和/最小值），以及 CF380C 等经典模型。 |
| dsu-application | [并查集应用（扩展域 / 带权 / 可撤销 / Kruskal 重构树）](nodes/dsu-application.md) | intermediate | P1 | 并查集不只做连通性合并：扩展域（食物链）、带权（银河英雄传说）、按秩合并+可撤销（离线回退）、Kruskal 重构树（最小生成树转树上问题）、启发式合并（在线桥、连通时间）等，把连通性问题变成 O(α(n)) 或 O(log n) 的结构。 |

## G-D-10 调度与其他专题

- 领域: 高级专题 · 阶段范围: 中级→高级 · 节点数: 4

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| schedule-one-machine | [单机调度](nodes/schedule-one-machine.md) | advanced | P2 | 单机作业排序使最大延迟/完工时间最优，按截止期贪心 |
| schedule-two-machines | [双机调度(Johnson 法则)](nodes/schedule-two-machines.md) | advanced | P2 | 两台流水机作业调度，Johnson 法则求最短完工时间 |
| schedule-deadline-duration | [截止期限-工期调度](nodes/schedule-deadline-duration.md) | advanced | P3 | 给定截止期限与工期求最优调度可行性，贪心+堆 |
| stern-brocot-tree | [Stern-Brocot 树与 Farey 序列](nodes/stern-brocot-tree.md) | advanced | P2 | 生成所有既约正有理数的二叉搜索树：相邻分数插入中位分数 (a+c)/(b+d)，支持二分定位任意有理数与最优有理逼近，关联连分数与 Farey 序列 |

## G-E-1 IO与常数优化族

- 领域: 技巧 · 阶段范围: 基础→中级 · 节点数: 4

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| fast-io | [快速读入](nodes/fast-io.md) | basic | P0 | 整数快速读入：C++ 用 getchar/fread；Python 用 sys.stdin.buffer.read().split() 批量读入 + map(int,...)，比逐行 input() 快 5-20 倍 |
| fast-output | [快速输出](nodes/fast-output.md) | intermediate | P1 | 整数快速输出：C++ 用 putchar/fwrite 攒缓冲；Python 用 '\n'.join(map(str, ...)) 一次 write，避免逐行 print() 慢 |
| constant-opt | [常数优化](nodes/constant-opt.md) | intermediate | P1 | 算法正确但常数过大超时的优化：局部性/循环展开（C++）、Python 局部变量绑定、避免属性访问、列表推导、预分配数组、用 int 位集等 |
| flush-buffer | [缓冲区刷新](nodes/flush-buffer.md) | basic | P1 | 交互题必须每次输出后刷新缓冲区：C++ fflush(stdout)/std::endl，Python sys.stdout.flush() 或 print(..., flush=True)，否则 Idleness limit exceeded |

## G-E-2 位运算族

- 领域: 技巧 · 阶段范围: 基础→高级 · 节点数: 4

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| bit-op-basics | [位运算基础](nodes/bit-op-basics.md) | basic | P0 | 按位与/或/异或/取反/移位，优先级陷阱（& 低于 ==、^ 低于比较），lowbit、置位/清位/翻转、补码表示，Python 无限位宽差异 |
| bitset-compression | [bitset压位](nodes/bitset-compression.md) | intermediate | P1 | 用 bitset 把 O(n^2)/w 的操作压成位运算：Python 用 int 当 bitset（int 无限位宽+bit_count），莫队配合 bitset 加速区间统计 |
| submask-enum | [子集枚举](nodes/submask-enum.md) | intermediate | P1 | 枚举位掩码所有子集的 O(3^n) 技巧：s=(s-1)&m 从大到小枚举，子集 DP（状压）核心 |
| bit-tricks | [位运算技巧](nodes/bit-tricks.md) | advanced | P2 | 进阶位运算套路：lowbit、popcount、前导/后缀零、格雷码、交换/去重、集合交并差、mask 变换等妙用 |

## G-E-3 Python竞赛特性族

- 领域: 语言特性 · 阶段范围: 基础→中级 · 节点数: 8

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| py-batch-io | [Python批量读入](nodes/py-batch-io.md) | basic | P0 | sys.stdin.read().split()一次性读入全部输入再map(int,...)，避免逐行input()超时 |
| py-list-comp | [列表推导优化](nodes/py-list-comp.md) | basic | P0 | Python for循环极慢，用列表推导式/filter/map/内置函数替代显式循环获10x+加速 |
| py-recursion-limit | [递归栈限制设置](nodes/py-recursion-limit.md) | basic | P0 | sys.setrecursionlimit(1<<20)避免深递归栈溢出；Python默认递归深度仅1000 |
| py-lru-cache | [lru_cache记忆化](nodes/py-lru-cache.md) | intermediate | P0 | functools.lru_cache(None)装饰器一行实现函数记忆化，递归DP利器 |
| py-pypy | [PyPy差异与注意事项](nodes/py-pypy.md) | basic | P0 | PyPy JIT加速循环但递归反而更慢；大整数/内存差异；部分库不可用；递归限stack需手动设 |
| py-bigint | [Python大整数原生支持](nodes/py-bigint.md) | basic | P0 | Python int无限精度，无需手写大数类；pow(a,b,mod)内置快速幂；2**512直接算 |
| py-2d-array | [二维列表正确创建](nodes/py-2d-array.md) | basic | P0 | [[0]*n for _ in range(m)]创建独立行；[[0]*n]*m会导致所有行共享同一对象（引用陷阱） |
| py-builtin | [内置库利用](nodes/py-builtin.md) | intermediate | P0 | bisect二分/heapq堆/collections.deque双端队列/itertools排列组合/math.gcd等竞赛常用内置库 |

## G-E-4 调试与对拍族

- 领域: 竞赛策略 · 阶段范围: 基础→中级 · 节点数: 5

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| stress-test | [对拍/压力测试](nodes/stress-test.md) | basic | P0 | 生成随机数据→暴力/正解分别运行→比对输出找bug，竞赛调试核心手段 |
| debug-macro | [调试宏](nodes/debug-macro.md) | basic | P0 | #ifdef DEBUG / -DONLINE_JUDGE 编译宏控制调试输出，提交时无需删代码 |
| random-gen | [随机数据生成](nodes/random-gen.md) | basic | P0 | 对拍用随机数据生成器：mt19937/random模块，testlib generator框架 |
| common-mistakes | [常见错误避免](nodes/common-mistakes.md) | basic | P0 | int溢出/未初始化/运算符优先级/scanf格式符/变量重名shadow等竞赛高频错误清单 |
| interactive-debug | [交互题调试](nodes/interactive-debug.md) | advanced | P3 | 交互题对拍困难，需模拟交互过程；封装输入输出函数；静态查错能力重要 |

## G-E-5 随机化与元启发式族

- 领域: 技巧 · 阶段范围: 中级→高级 · 节点数: 5

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| random-technique | [随机化技巧](nodes/random-technique.md) | intermediate | P1 | 随机覆盖目标元素/随机命中目标集合/随机打乱消除最坏情况，概率上界分析 |
| hill-climbing | [爬山算法](nodes/hill-climbing.md) | advanced | P2 | 局部择优启发式搜索，每次在当前最优解附近找更优解；易陷入局部最优，单峰函数有效 |
| simulated-annealing | [模拟退火](nodes/simulated-annealing.md) | advanced | P2 | 以概率e^(-ΔE/T)接受劣解跳出局部最优；初始温度/降温系数/终止温度三参数；卡时技巧clock()；Metropolis准则 |
| random-shuffle | [随机打乱防hack](nodes/random-shuffle.md) | intermediate | P2 | shuffle打乱输入顺序防止构造数据卡哈希/快排；CF hack常见反制手段 |
| anti-hash | [防卡Hash随机化](nodes/anti-hash.md) | advanced | P2 | 字符串哈希用随机base/双哈希/随机化seed防止构造数据碰撞攻击 |

## G-E-6 博弈论族

- 领域: 数学/博弈 · 阶段范围: 中级→高级 · 节点数: 7

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| nim-game | [Nim游戏](nodes/nim-game.md) | intermediate | P0 | n 堆石子轮流取任意堆任意多枚，Nim 和（全部堆的异或）为 0 则先手必败（P 态），非 0 则先手必胜（N 态）；公平组合博弈的基础模型 |
| sg-function | [SG函数/Sprague-Grundy定理](nodes/sg-function.md) | intermediate | P0 | 所有公平组合游戏等价于单堆 Nim；SG(x)=mex{SG(后继)}；多个独立子游戏的 SG 异或得总局面 SG，零则先手必败；Sprague-Grundy 定理 |
| game-graph | [博弈图与必胜必败态](nodes/game-graph.md) | intermediate | P1 | 把公平组合游戏的状态画成有向无环图：无后继态为 P（先手必败）；存在后继为 P 的是 N（必胜）；所有后继都是 N 的才是 P；O(\|V\|+\|E\|) 逆拓扑标记 |
| anti-nim | [反常Nim/Anti-Nim](nodes/anti-nim.md) | advanced | P1 | misère 规则：取最后一枚石子者输；判定需分类讨论——全 1 堆看奇偶，否则仍看 Nim 和（与正常 Nim 相同） |
| game-on-graph | [有向图游戏](nodes/game-on-graph.md) | advanced | P1 | 在任意有向图（可能含环）上移动的博弈：利用反图 BFS + 出度归零技巧，O(\|V\|+\|E\|) 线性分类每个顶点为必胜/必败/平局态 |
| zero-sum-game | [零和博弈/Minimax](nodes/zero-sum-game.md) | advanced | P1 | 序贯零和：V(s)=max/min{V(后继)} 递推，Minimax+Alpha-Beta 剪枝；同时零和：收益矩阵、混合策略与 von Neumann 极小极大定理 |
| partizan-game | [非公平组合博弈](nodes/partizan-game.md) | advanced | P2 | 双方可用行动集不同的博弈（如棋类）：Conway 超现实数理论描述，结果分类 L/R/N/P 四种；比公平博弈复杂得多，竞赛少见 |

## G-E-7 离线与杂项技巧族

- 领域: 杂项技巧 · 阶段范围: 中级→高级 · 节点数: 18

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| cdq-divide | [CDQ分治](nodes/cdq-divide.md) | advanced | P1 | 分治处理点对问题：三维偏序/DP优化/动态转静态；陈丹琦(IOI2008)提出 |
| parallel-binsearch | [整体二分/并行二分](nodes/parallel-binsearch.md) | advanced | P1 | 多询问一起二分：把操作和询问按答案值域分治，O(T·log n)同时处理所有询问 |
| odt | [珂朵莉树/ODT](nodes/odt.md) | advanced | P1 | 用平衡树维护颜色段均摊：区间赋值操作下split/assign均摊O(log)，起源CF896C；颜色段均摊，随机数据下区间赋值均摊 O(logn)，源自 CF896C |
| offline | [离线算法思想](nodes/offline.md) | intermediate | P0 | 已知全部数据后统一求解：CDQ分治/整体二分/莫队等离线框架的基础思想 |
| two-pointer | [双指针](nodes/two-pointer.md) | basic | P0 | 同向/相向移动两指针维护区间信息：O(n)解决单调性区间问题，莫队基础 |
| discrete | [离散化](nodes/discrete.md) | basic | P0 | 大值域映射到紧凑排名：排序+去重+lower_bound，保持偏序关系，压缩数组下标 |
| frac-programming | [分数规划/01分数规划](nodes/frac-programming.md) | advanced | P1 | 求Σa/Σb极值：二分答案→Σw_i(a_i-mid·b_i)≥0判定；Dinkelbach迭代法 |
| expression-eval | [表达式求值](nodes/expression-eval.md) | intermediate | P1 | 中缀→后缀(逆波兰)→栈求值；双栈法O(n)；含一元/右结合运算符扩展 |
| josephus | [约瑟夫问题](nodes/josephus.md) | intermediate | P1 | n人围圈报数出列：递推f(n,k)=(f(n-1,k)+k)%n O(n)；大n小k有O(k log n)解法 |
| majority-element | [主元素/Boyer-Moore投票](nodes/majority-element.md) | intermediate | P1 | 出现>n/2的元素：候选+计数消去法O(n)O(1)；在线流式处理 |
| kahan-summation | [Kahan求和](nodes/kahan-summation.md) | advanced | P2 | 补偿求和法降低浮点累加误差：维护误差补偿变量c，精度接近double但只多一个变量 |
| space-optimization | [空间优化](nodes/space-optimization.md) | advanced | P1 | 滚动数组/bitset压位/信息熵下界/利用数据特性(并查集单数组)等节省内存技巧 |
| 15-puzzle | [15谜题可解性判定](nodes/15-puzzle.md) | advanced | P2 | N-puzzle可解性判定：逆序对数奇偶性+空格行距，不可解则无解 |
| fsm | [有限状态机](nodes/fsm.md) | advanced | P2 | FSM用于字符串匹配/自动机DP/AC自动机基础，竞赛中处理模式匹配问题 |
| endian | [字节序](nodes/endian.md) | intermediate | P2 | 大端序/小端序差异，网络字节序转换，二进制文件读写时需注意 |
| tortoise-hare | [Floyd环检测](nodes/tortoise-hare.md) | intermediate | P2 | 龟兔赛跑算法：快慢指针检测链表/序列环，O(n)O(1)找环起点与周期 |
| max-avg-segment | [最大平均值区段](nodes/max-avg-segment.md) | advanced | P2 | 求长度≥L的最大平均值子数组：二分+前缀和判定，分数规划经典应用 |
| stern-brocot | [Stern-Brocot树/Farey序列](nodes/stern-brocot.md) | advanced | P2 | 枚举所有既约分数的二元搜索树：二分逼近实数，求最优分数逼近 |

## G-E-8 竞赛策略族

- 领域: 竞赛策略 · 阶段范围: 基础→中级 · 节点数: 6

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| contest-strategy | [比赛时间分配与策略](nodes/contest-strategy.md) | basic | P0 | ICPC/CCPC/OI 全局策略：读题顺序、时间分配、队友分工、罚时控制、封板策略 |
| partial-score | [骗分/部分分](nodes/partial-score.md) | basic | P0 | OI 赛制按数据范围分档拿分：暴力/特殊性质部分分，namespace 分治提交 |
| io-optimization | [I/O优化策略](nodes/io-optimization.md) | basic | P1 | 关闭同步/快读快写、Python 批量读入 sys.stdin.buffer，I/O 瓶颈识别与优化决策 |
| interaction-strategy | [交互题策略](nodes/interaction-strategy.md) | intermediate | P2 | 交互次数优化、二分交互、随机撒点、flush 时机、STDIO vs Grader 模式 |
| problem-types | [题型识别](nodes/problem-types.md) | basic | P0 | 传统题/交互题/提交答案题/通信题的识别与应对，评测结果类型(AC/WA/TLE/RE等) |
| contest-resources | [学习资源与刷题路线](nodes/contest-resources.md) | intermediate | P2 | OI Wiki/CPH 等教程、CF/AtCoder/Luogu 刷题路线、经典教材与进阶路径 |

## G-E-9 工具链族

- 领域: 工具 · 阶段范围: 基础→中级 · 节点数: 7

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| compile-debug | [编译与调试](nodes/compile-debug.md) | basic | P0 | g++编译选项(-O2/-g/-Wall/-Wextra)、Sanitizer、gdb调试与Python调试技巧，竞赛提交前必备检查 |
| testlib | [testlib对拍框架](nodes/testlib.md) | intermediate | P1 | testlib.h：generator/validator/checker/interactor四件套，出题与对拍的标准库，与Polygon完全兼容 |
| oj-tool | [OJ工具](nodes/oj-tool.md) | intermediate | P2 | cf-tool/Competitive Companion/ac-predictor等命令行与浏览器工具，简化样例拉取、测试、提交与rating跟踪 |
| editor-setup | [编辑器配置](nodes/editor-setup.md) | intermediate | P2 | VSCode/Vim/CLion等编辑器竞赛配置：编译任务、调试launch、代码片段、按键效率优化 |
| polygon | [Polygon出题平台](nodes/polygon.md) | advanced | P3 | Codeforces多人协作出题平台：版本管理+validator/generator/checker/solutions环环相扣+数据自动生成+对拍(stress) |
| special-judge | [Special Judge](nodes/special-judge.md) | intermediate | P2 | 多解/浮点/构造题的专用评测器：testlib checker编写范式，_ok/_wa/_fail三态与readAns模式 |
| git-version | [Git版本管理](nodes/git-version.md) | intermediate | P2 | 代码模板版本管理、提交回退、分支协作与代码回溯；竞赛模板库/团队协作的基础设施 |

## G-E-10 前沿趋势组

- 领域: 前沿 · 阶段范围: 高级→前沿 · 节点数: 6

| id | name | stage | priority | brief |
| --- | --- | --- | --- | --- |
| monotonic-stack-dp | [单调栈优化 DP](nodes/monotonic-stack-dp.md) | frontier | P2 | 利用单调栈维护 Pareto 前沿，对『值递增/DP值递减』的转移做到均摊O(1) |
| prefix-gcd-optimization | [前缀 GCD 变化优化](nodes/prefix-gcd-optimization.md) | frontier | P3 | 利用『前缀 GCD 至多变化 O(log A) 次』的性质，把 O(n²) 优化到 O(n log A) |
| binary-tree-dp-trick | [二叉化树 DP Trick](nodes/binary-tree-dp-trick.md) | frontier | P3 | 多叉树添加虚节点链转为二叉树，使 O(n²) 树形 DP 的合并复杂度成立 |
| bitmask-dp-optimization | [位掩码 DP 优化](nodes/bitmask-dp-optimization.md) | frontier | P3 | 子集DP从O(3^n)优化到O(2^n·n)：按lowbit分治/仅枚举补集子集等技巧 |
| ai-cp-trend | [AI 竞赛编程趋势](nodes/ai-cp-trend.md) | frontier | P3 | 2026年GrandCode/Solvita等AI系统在CF live round超越人类GM，test-time RL+agentic loop成主流 |
| interactive-problem-trend | [交互题兴起趋势](nodes/interactive-problem-trend.md) | frontier | P3 | ICPC 2024-2025南京连续出交互题，NOI/WC恢复交互题，交互题成为高频新题型 |
