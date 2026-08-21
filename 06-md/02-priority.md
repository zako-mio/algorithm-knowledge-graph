# 优先级视图 · P0 / P1 / P2 / P3

> P0 = 必会 · P1 = 高频 · P2 = 选学 · P3 = 冷门。

## P0 · 必会 (94)

| id | name | stage | group | brief |
| --- | --- | --- | --- | --- |
| determinant | [行列式](nodes/determinant.md) | advanced | G-C-14 | O(n^3)高斯消元法求行列式，矩阵树定理与计数应用基础 |
| lucas-theorem | [卢卡斯定理](nodes/lucas-theorem.md) | advanced | G-C-8 | C(n,m) mod p当p为素数时分位计算，O(p log n)，大组合数取小素模 |
| persistent-seg | [可持久化线段树(主席树)](nodes/persistent-seg.md) | advanced | G-D-5 | 函数式线段树按版本共享节点，支持历史版本查询与区间k小值；保存每次修改的历史版本，区间第k小/历史查询 |
| backtracking | [回溯法](nodes/backtracking.md) | basic | G-A-14 | DFS+撤销操作，走不通就回头，排列/组合/棋盘类问题 |
| bfs | [BFS广度优先搜索](nodes/bfs.md) | basic | G-B-1 | 按层遍历图，队列实现O(V+E)，可求无权最短路；逐层扩展，队列实现，求无权图最短路，空间O(n) |
| binary-exponentiation | [快速幂](nodes/binary-exponentiation.md) | basic | G-C-7 | O(log n)计算a^n，二进制取幂，模意义下核心工具 |
| binary-heap | [二叉堆](nodes/binary-heap.md) | basic | G-A-3 | 完全二叉树维护优先队列，O(log n)插入/删除最值 |
| binary-search | [二分查找](nodes/binary-search.md) | basic | G-A-1 | 有序数组O(log n)查找，含lower_bound/upper_bound |
| bipartite-check | [二分图判定](nodes/bipartite-check.md) | basic | G-B-6 | BFS/DFS染色法判定二分图O(V+E) |
| bit-op-basics | [位运算基础](nodes/bit-op-basics.md) | basic | G-E-2 | 与/或/异或/取反/移位运算，位运算优先级陷阱，整数低位操作 |
| combination-number | [组合数](nodes/combination-number.md) | basic | G-C-10 | C(n,m)的计算：递推/预处理阶乘逆元/Lucas，竞赛计数核心 |
| common-mistakes | [常见错误避免](nodes/common-mistakes.md) | basic | G-E-4 | int溢出/未初始化/运算符优先级/scanf格式符/变量重名shadow等竞赛高频错误清单 |
| compile-debug | [编译与调试](nodes/compile-debug.md) | basic | G-E-9 | g++编译选项(-O2/-g/-Wall/-Wextra)、gdb调试、编译器优化原理(常量折叠/死代码消除等) |
| complexity | [时间/空间复杂度分析](nodes/complexity.md) | basic | G-A-1 | 渐近符号(O/Theta/Omega)与复杂度分析方法 |
| connected-components | [连通分量](nodes/connected-components.md) | basic | G-B-1 | 无向图连通块，BFS/DFS遍历标记O(V+E) |
| contest-strategy | [比赛时间分配与策略](nodes/contest-strategy.md) | basic | G-E-8 | ICPC/OI比赛策略：读题顺序、时间分配、队友分工、罚时控制、封板策略 |
| debug-macro | [调试宏](nodes/debug-macro.md) | basic | G-E-4 | #ifdef DEBUG / -DONLINE_JUDGE 编译宏控制调试输出，提交时无需删代码 |
| dfs | [DFS深度优先搜索](nodes/dfs.md) | basic | G-B-1 | 递归深入遍历O(V+E)，连通性判定与DFS生成树基础；沿一条路径深入到底再回溯，栈/递归实现，空间O(h) |
| dijkstra | [Dijkstra算法](nodes/dijkstra.md) | basic | G-B-2 | 非负权单源最短路，堆优化O((V+E)logV)，贪心松弛 |
| discrete | [离散化](nodes/discrete.md) | basic | G-E-7 | 大值域映射到紧凑排名：排序+去重+lower_bound，保持偏序关系，压缩数组下标 |
| divide-conquer | [分治与递归](nodes/divide-conquer.md) | basic | G-A-1 | 分解-解决-合并，递归处理子问题 |
| dp-basic | [动态规划基础](nodes/dp-basic.md) | basic | G-A-11 | 最优子结构/无后效性/子问题重叠，状态定义与转移方程 |
| dp-knapsack-complete | [完全背包](nodes/dp-knapsack-complete.md) | basic | G-A-11 | 每件物品无限取，正序遍历容量 |
| dp-knapsack01 | [0-1背包](nodes/dp-knapsack01.md) | basic | G-A-11 | 每个物品取/不取，O(nW)转移，滚动数组优化空间 |
| dp-linear | [线性DP(LIS/LCS)](nodes/dp-linear.md) | basic | G-A-11 | 一维序列上的DP，最长递增子序列/最长公共子序列 |
| dp-memo | [记忆化搜索](nodes/dp-memo.md) | basic | G-A-11 | 自顶向下DFS+缓存，DP的递归实现方式 |
| dsu-basic | [并查集(路径压缩+按秩合并)](nodes/dsu-basic.md) | basic | G-A-4 | 近O(1)合并/查询集合，路径压缩+按秩合并 |
| enumerate | [枚举与暴力](nodes/enumerate.md) | basic | G-A-1 | 系统枚举所有可能，常结合剪枝优化 |
| euclidean-gcd | [欧几里得算法(GCD)](nodes/euclidean-gcd.md) | basic | G-C-7 | 辗转相除法求最大公约数，O(log min(a,b))，数论基础工具 |
| fast-io | [快速读入](nodes/fast-io.md) | basic | G-E-1 | 整数快速读入：C++用getchar/fread，Python用sys.stdin.read批量读入+map(int,...split()) |
| fenwick | [树状数组(BIT)](nodes/fenwick.md) | basic | G-A-5 | lowbit分组，O(log n)单点修改+前缀查询，代码短常数小 |
| floyd | [Floyd-Warshall算法](nodes/floyd.md) | basic | G-B-2 | 全源最短路，DP三重循环O(V³)，可处理负权 |
| graph-basics | [图论基础概念](nodes/graph-basics.md) | basic | G-B-1 | 图的基本概念：点、边、有向/无向图、度、路径、环、子图 |
| graph-storage | [图的存储](nodes/graph-storage.md) | basic | G-B-1 | 邻接矩阵、邻接表、链式前向星等存图方式 |
| greedy | [贪心算法](nodes/greedy.md) | basic | G-A-1 | 每步取局部最优，需证明最优子结构与交换论证 |
| hash-table | [哈希表(散列表)](nodes/hash-table.md) | basic | G-A-10 | key-value映射，哈希函数+冲突处理(开链/开放寻址) |
| kruskal | [Kruskal算法](nodes/kruskal.md) | basic | G-B-3 | 最小生成树，贪心排序+并查集O(ElogE) |
| merge-sort | [归并排序](nodes/merge-sort.md) | basic | G-A-1 | 分治排序，O(n log n)稳定排序，可用于求逆序对 |
| mod-arithmetic | [模算术](nodes/mod-arithmetic.md) | basic | G-C-7 | 模意义下加减乘除运算，取模与负数处理，竞赛必备基础 |
| partial-score | [骗分/部分分](nodes/partial-score.md) | basic | G-E-8 | namespace分治写暴力/特殊性质部分分；OI赛制核心技能，按数据范围分档拿分 |
| prefix-sum | [前缀和与差分](nodes/prefix-sum.md) | basic | G-A-1 | O(1)区间和查询/O(1)区间修改，一维与多维 |
| prim | [Prim算法](nodes/prim.md) | basic | G-B-3 | 最小生成树，贪心+堆O(ElogV)，适合稠密图 |
| prime-test-basic | [素数判定(试除)](nodes/prime-test-basic.md) | basic | G-C-7 | O(sqrt(n))试除法判定素数，基础方法，大数用Miller-Rabin |
| problem-types | [题型识别](nodes/problem-types.md) | basic | G-E-8 | 传统题/交互题/提交答案题/通信题的识别与应对策略，评测结果类型(AC/WA/TLE/RE等) |
| py-2d-array | [二维列表正确创建](nodes/py-2d-array.md) | basic | G-E-3 | [[0]*n for _ in range(m)]创建独立行；[[0]*n]*m会导致所有行共享同一对象（引用陷阱） |
| py-batch-io | [Python批量读入](nodes/py-batch-io.md) | basic | G-E-3 | sys.stdin.read().split()一次性读入全部输入再map(int,...)，避免逐行input()超时 |
| py-bigint | [Python大整数原生支持](nodes/py-bigint.md) | basic | G-E-3 | Python int无限精度，无需手写大数类；pow(a,b,mod)内置快速幂；2**512直接算 |
| py-list-comp | [列表推导优化](nodes/py-list-comp.md) | basic | G-E-3 | Python for循环极慢，用列表推导式/filter/map/内置函数替代显式循环获10x+加速 |
| py-pypy | [PyPy差异与注意事项](nodes/py-pypy.md) | basic | G-E-3 | PyPy JIT加速但递归反而更慢；大整数/内存差异；部分库不可用；递归限stack需手动设 |
| py-recursion-limit | [递归栈限制设置](nodes/py-recursion-limit.md) | basic | G-E-3 | sys.setrecursionlimit(1<<20)避免深递归栈溢出；Python默认递归深度仅1000 |
| queue | [队列](nodes/queue.md) | basic | G-A-2 | FIFO先进先出结构，BFS基础组件 |
| quick-sort | [快速排序](nodes/quick-sort.md) | basic | G-A-1 | 分治排序，期望O(n log n)，最坏O(n^2)，常数小 |
| random-gen | [随机数据生成](nodes/random-gen.md) | basic | G-E-4 | 对拍用随机数据生成器：mt19937/random模块，testlib generator框架 |
| sieve-eratosthenes | [埃氏筛](nodes/sieve-eratosthenes.md) | basic | G-C-7 | O(n log log n)筛素数，标记合数，基础素数筛法 |
| simulate | [模拟](nodes/simulate.md) | basic | G-A-1 | 按题意直接模拟过程，考察代码实现能力 |
| sort-intro | [排序基础概念](nodes/sort-intro.md) | basic | G-A-1 | 排序算法总览：稳定性、复杂度、比较与非比较排序的分类 |
| sparse-table | [ST表(稀疏表)](nodes/sparse-table.md) | basic | G-A-5 | 倍增预处理O(1)回答可重复贡献问题(RMQ/GCD)，不支持修改 |
| stack | [栈](nodes/stack.md) | basic | G-A-2 | LIFO后进先出结构，支持括号匹配/表达式求值等 |
| stress-test | [对拍/压力测试](nodes/stress-test.md) | basic | G-E-4 | 生成随机数据→暴力/正解分别运行→比对输出找bug，竞赛调试核心手段 |
| topo-sort | [拓扑排序](nodes/topo-sort.md) | basic | G-B-1 | DAG节点线性排序，Kahn算法(入度BFS)或DFS逆序O(V+E) |
| tree-basics | [树基础](nodes/tree-basics.md) | basic | G-B-7 | 树的基本概念：根、叶、深度、子树、父亲 |
| tree-diameter | [树的直径](nodes/tree-diameter.md) | basic | G-B-7 | 树上最长路径，两次DFS或树形DPO(V) |
| two-pointer | [双指针](nodes/two-pointer.md) | basic | G-E-7 | 同向/相向移动两指针维护区间信息：O(n)解决单调性区间问题，莫队基础 |
| big-integer | [高精度(大整数)](nodes/big-integer.md) | intermediate | G-C-18 | 大整数加减乘除，FFT加速乘法O(n log n)，压位优化 |
| binary-answer | [二分答案](nodes/binary-answer.md) | intermediate | G-A-1 | 对答案值域二分，配合check函数求解最优化问题 |
| crt | [中国剩余定理(CRT)](nodes/crt.md) | intermediate | G-C-8 | 求解同余方程组，将模互素的大模数分解为小模数合并，exCRT处理不互素 |
| dp-interval | [区间DP](nodes/dp-interval.md) | intermediate | G-A-11 | f(i,j)表示区间[i,j]最优，枚举合并点k，O(n^3) |
| dp-tree | [树形DP](nodes/dp-tree.md) | intermediate | G-A-11 | 树上递归DP，DFS后序传递子树最优解到父节点 |
| euler-totient | [欧拉函数](nodes/euler-totient.md) | intermediate | G-C-7 | phi(n)表示1~n中与n互素的数个数，积性函数，欧拉定理基础 |
| expectation-variance | [期望与方差](nodes/expectation-variance.md) | intermediate | G-C-15 | E[X]与Var(X)的线性性质，期望DP核心工具 |
| ext-euclidean | [扩展欧几里得](nodes/ext-euclidean.md) | intermediate | G-C-7 | 求ax+by=gcd(a,b)的一组整数解，模逆元与线性方程的基础 |
| fermat-little-theorem | [费马小定理](nodes/fermat-little-theorem.md) | intermediate | G-C-7 | p素数时a^(p-1)≡1(mod p)，模逆元与素性检测的理论基础 |
| fibonacci | [斐波那契数列](nodes/fibonacci.md) | intermediate | G-C-10 | F(n)=F(n-1)+F(n-2)，矩阵快速幂O(log n)求第n项，恒等式众多 |
| gaussian-elimination | [高斯消元](nodes/gaussian-elimination.md) | intermediate | G-C-14 | O(n^3)解线性方程组/求秩/求行列式，线性代数核心算法 |
| kmp | [KMP算法](nodes/kmp.md) | intermediate | G-C-1 | 线性时间字符串匹配，利用前缀函数(pi数组)避免回溯，O(n+m) |
| lca | [最近公共祖先(LCA)](nodes/lca.md) | intermediate | G-B-7 | 倍增预处理O(VlogV)查询O(logV)，或Tarjan离线O(α) |
| linear-basis | [线性基](nodes/linear-basis.md) | intermediate | G-C-14 | 异或空间基，O(n log max)插入，求最大/最小/第k小异或值 |
| matrix-basics | [矩阵基础](nodes/matrix-basics.md) | intermediate | G-C-14 | 矩阵加减乘与转置，矩阵快速幂O(k^3 log n)，递推加速核心 |
| modular-inverse | [模逆元](nodes/modular-inverse.md) | intermediate | G-C-7 | 求a在模m下的逆元，方法：扩展欧几里得/费马小定理/线性递推 |
| monotonic-queue | [单调队列](nodes/monotonic-queue.md) | intermediate | G-A-2 | 维护滑动窗口最值，O(n)均摊，DP优化基础 |
| monotonic-stack | [单调栈](nodes/monotonic-stack.md) | intermediate | G-A-2 | 维护单调性的栈，O(n)求左右第一个大/小于当前值 |
| nim-game | [Nim游戏](nodes/nim-game.md) | intermediate | G-E-6 | N堆石子轮流取，Nim和(异或)为0则先手必败(P态)，非0则先手必胜(N态)；公平组合博弈，Nim和(异或)为0则先手必败，SG定理基础 |
| offline | [离线算法思想](nodes/offline.md) | intermediate | G-E-7 | 已知全部数据后统一求解：CDQ分治/整体二分/莫队等离线框架的基础思想 |
| probability-basics | [概率基础](nodes/probability-basics.md) | intermediate | G-C-15 | 概率公理、古典概型与几何概型，期望DP的理论基础 |
| py-builtin | [内置库利用](nodes/py-builtin.md) | intermediate | G-E-3 | bisect二分/heapq堆/collections.deque双端队列/itertools排列组合/math.gcd等竞赛常用内置库 |
| py-lru-cache | [lru_cache记忆化](nodes/py-lru-cache.md) | intermediate | G-E-3 | functools.lru_cache(None)装饰器一行实现函数记忆化，递归DP利器 |
| seg-basic | [线段树基础](nodes/seg-basic.md) | intermediate | G-A-6 | O(log n)单点修改+区间查询，递归建树合并子节点信息 |
| seg-lazy | [懒标记线段树](nodes/seg-lazy.md) | intermediate | G-A-6 | 区间修改+区间查询，lazy tag延迟下发均摊O(log n) |
| sg-function | [SG函数/Sprague-Grundy定理](nodes/sg-function.md) | intermediate | G-E-6 | 所有公平组合游戏等价于单堆Nim；SG(x)=mex{SG(后继)}；多子游戏SG值异或得总局面SG；Sprague-Grundy定理：公平组合博弈等价于Nim，SG(x)=mex{SG(后继)} |
| sieve-linear | [线性筛(欧拉筛)](nodes/sieve-linear.md) | intermediate | G-C-7 | O(n)筛素数，每个合数只被最小质因子筛一次，可同时求积性函数 |
| stars-and-bars | [插板法(Stars and Bars)](nodes/stars-and-bars.md) | intermediate | G-C-10 | 将n个相同物品分给k组的方案数C(n+k-1,k-1)，整数拆分计数 |
| string-hash | [字符串哈希](nodes/string-hash.md) | intermediate | G-C-1 | 将字符串映射为多项式哈希值，O(1)比较子串哈希，需双哈希防碰撞 |
| tarjan-scc | [Tarjan强连通分量](nodes/tarjan-scc.md) | intermediate | G-B-4 | 有向图强连通分量，DFS+dfn/low O(V+E) |
| trie | [Trie字典树](nodes/trie.md) | intermediate | G-C-2 | 树形结构存储多字符串公共前缀，O(L)插入查询，AC自动机与可持久化Trie的基础 |

## P1 · 高频 (113)

| id | name | stage | group | brief |
| --- | --- | --- | --- | --- |
| ac-automaton | [AC自动机](nodes/ac-automaton.md) | advanced | G-C-2 | Trie+KMP失配指针，多模式串匹配自动机，O(n+m+z) |
| anti-nim | [反常Nim/Anti-Nim](nodes/anti-nim.md) | advanced | G-E-6 | misère规则：最后行动者输；反常Nim判定比正常复杂，需分类讨论全1堆与非全1堆 |
| block-array | [分块数组](nodes/block-array.md) | advanced | G-D-6 | 块状数组实现区间修改/查询，块内整体保存散块暴力；将数组分为O(sqrt n)块，块间维护聚合信息 |
| bsgs | [BSGS(大步小步)](nodes/bsgs.md) | advanced | G-C-8 | O(sqrt(p))求离散对数a^x≡b(mod p)，baby-step giant-step算法 |
| cdq-divide | [CDQ分治](nodes/cdq-divide.md) | advanced | G-E-7 | 分治处理点对问题：三维偏序/DP优化/动态转静态；陈丹琦(IOI2008)提出 |
| dp-opt-divide-conquer | [分治优化DP](nodes/dp-opt-divide-conquer.md) | advanced | G-A-12 | 决策点单调时利用分治缩小决策空间，O(n log n) |
| dp-opt-slope | [斜率优化DP](nodes/dp-opt-slope.md) | advanced | G-A-12 | 转移方程化为一次函数，凸壳上二分/单调队列维护最值 |
| enclosing-circle | [最小覆盖圆](nodes/enclosing-circle.md) | advanced | G-D-1 | 随机增量法 O(期望n) 求覆盖所有点的最小圆(Welzl) |
| extended-lucas | [扩展卢卡斯(exLucas)](nodes/extended-lucas.md) | advanced | G-C-8 | C(n,m) mod p当p为合数时，分解质因子+CRT合并，处理任意模数组合数 |
| fft | [FFT(快速傅里叶变换)](nodes/fft.md) | advanced | G-C-12 | O(n log n)计算多项式乘法，基于DFT与蝴蝶操作，NTT为模意义版本 |
| fhq-treap | [无旋Treap(FHQ Treap)](nodes/fhq-treap.md) | advanced | G-A-8 | 按值/按秩分裂合并，无需旋转，可持久化友好 |
| frac-programming | [分数规划/01分数规划](nodes/frac-programming.md) | advanced | G-E-7 | 求Σa/Σb极值：二分答案→Σw_i(a_i-mid·b_i)≥0判定；Dinkelbach迭代法 |
| game-on-graph | [有向图游戏](nodes/game-on-graph.md) | advanced | G-E-6 | 任意有向图(可能有环)上的博弈：逆拓扑/BFS标记胜负平局态，O(m)线性求解 |
| half-plane-intersection | [半平面交](nodes/half-plane-intersection.md) | advanced | G-D-1 | S&I 算法 O(nlogn) 求半平面交，结果为凸多边形 |
| integer-factorization | [大整数分解](nodes/integer-factorization.md) | advanced | G-C-9 | 合数分解为质因子乘积，Pollard-Rho为主流方法，试除法为基础 |
| lct | [Link-Cut Tree](nodes/lct.md) | advanced | G-D-4 | 基于 Splay 维护实链剖分，支持动态连断边与路径查询；动态树问题，Splay维护森林路径/子树操作，O(log n)均摊 |
| leftist-tree | [左偏树(可并堆)](nodes/leftist-tree.md) | advanced | G-A-3 | 支持O(log n)合并的可并堆，利用偏侧树高 |
| li-chao-tree | [李超线段树](nodes/li-chao-tree.md) | advanced | G-D-8 | 线段树维护线段/直线集合，标记永久化求横坐标处最值；维护区间最值线段，O(log n)插入线段/O(log n)查询最值；动态线段维护下凸包：线段插入O(log C)、线段插入O(log²C)；2026年有形式化规范论文 |
| miller-rabin | [Miller-Rabin](nodes/miller-rabin.md) | advanced | G-C-9 | 概率性素性测试O(k log n)，基于费马小定理与二次探测定理 |
| mobius-inversion | [莫比乌斯反演](nodes/mobius-inversion.md) | advanced | G-C-8 | 利用莫比乌斯函数mu进行数论反演，将gcd计数问题转化为求和 |
| nearest-points | [最近点对](nodes/nearest-points.md) | advanced | G-D-2 | 分治 O(nlogn) 求平面最近点对，合并时按扫描线对检查 |
| ntt | [NTT(数论变换)](nodes/ntt.md) | advanced | G-C-12 | 模意义下FFT，用原根替代单位根避免浮点误差，998244353为常用模数 |
| odt | [珂朵莉树/ODT](nodes/odt.md) | advanced | G-E-7 | 用平衡树维护颜色段均摊：区间赋值操作下split/assign均摊O(log)，起源CF896C；颜色段均摊，随机数据下区间赋值均摊 O(logn)，源自 CF896C |
| parallel-binsearch | [整体二分/并行二分](nodes/parallel-binsearch.md) | advanced | G-E-7 | 多询问一起二分：把操作和询问按答案值域分治，O(T·log n)同时处理所有询问 |
| persistent-trie | [可持久化 Trie](nodes/persistent-trie.md) | advanced | G-D-5 | 每次只新建被改节点，保留旧版本，支持历史版本字符串查询；保存历史版本的Trie，支持区间异或最值等查询 |
| pollard-rho | [Pollard-Rho](nodes/pollard-rho.md) | advanced | G-C-9 | 期望O(n^1/4)大整数分解，基于生日悖论与伪随机序列环检测 |
| polynomial-basics | [多项式基础](nodes/polynomial-basics.md) | advanced | G-C-12 | 多项式表示、求值、乘法、求导积分，FFT/NTT的前置知识 |
| primitive-root | [原根](nodes/primitive-root.md) | advanced | G-C-8 | 模p下阶为phi(p)的元素g，NTT与离散对数的基础，最小原根O(sqrt)求解 |
| rotating-calipers | [旋转卡壳](nodes/rotating-calipers.md) | advanced | G-D-1 | 在凸包上枚举对踵点，O(n) 求凸包直径/最小矩形覆盖 |
| seg-dynamic | [动态开点线段树](nodes/seg-dynamic.md) | advanced | G-A-6 | 按需创建节点，支持大值域离散化无需预先开空间 |
| seg-merge | [线段树合并与分裂](nodes/seg-merge.md) | advanced | G-A-6 | 合并多棵动态开点线段树，用于树上信息合并；按权值线段树合并实现集合操作，分裂还原，用于树上信息合并 |
| segment-tree-offline | [线段树分治(离线)](nodes/segment-tree-offline.md) | advanced | G-D-8 | 将时间轴建成线段树，把只存在于某时段的信息离线分发到节点 |
| space-optimization | [空间优化](nodes/space-optimization.md) | advanced | G-E-7 | 滚动数组/bitset压位/信息熵下界/利用数据特性(并查集单数组)等节省内存技巧 |
| splay | [Splay(伸展树)](nodes/splay.md) | advanced | G-A-8 | 伸展操作将访问节点旋至根，均摊O(log n)，LCT基础 |
| suffix-array | [后缀数组](nodes/suffix-array.md) | advanced | G-C-3 | SA+rank+height数组，对字符串所有后缀排序，配合LCP做子串统计与匹配 |
| sweep-line | [扫描线](nodes/sweep-line.md) | advanced | G-D-2 | 线扫过平面处理事件，求矩形面积并/周长并/二维数点 |
| treap | [Treap(树堆)](nodes/treap.md) | advanced | G-A-8 | BST+堆随机优先级，旋转维护平衡，期望O(log n) |
| zero-sum-game | [零和博弈/Minimax](nodes/zero-sum-game.md) | advanced | G-E-6 | 序贯零和：V(s)=max/min{V(后继)}；Minimax+Alpha-Beta剪枝；同时零和：纳什均衡/混合策略 |
| 2d-geometry | [二维几何基础](nodes/2d-geometry.md) | basic | G-D-3 | 向量运算/点积叉积/多边形面积/有向面积/线段转直线等基础 |
| flush-buffer | [缓冲区刷新](nodes/flush-buffer.md) | basic | G-E-1 | 交互题必须fflush(stdout)；Python用sys.stdout.flush()或print(...,flush=True) |
| heap-sort | [堆排序](nodes/heap-sort.md) | basic | G-A-1 | 基于二叉堆的O(n log n)原地排序，不稳定 |
| io-optimization | [I/O优化策略](nodes/io-optimization.md) | basic | G-E-8 | 关闭同步/解除关联/快读快写；Python批量读入；I/O瓶颈识别与优化决策 |
| linked-list | [链表](nodes/linked-list.md) | basic | G-A-10 | 节点指针串联，O(1)插入删除，需处理边界 |
| non-comparison-sort | [非比较排序(计数/桶/基数)](nodes/non-comparison-sort.md) | basic | G-A-1 | 线性时间排序，依赖键值范围限制 |
| ternary-search | [三分法](nodes/ternary-search.md) | basic | G-A-1 | 在单峰函数上找极值，O(log n)三分查找；O(log n)求单峰函数极值，基于中点比较缩小区间 |
| amortized-analysis | [均摊分析](nodes/amortized-analysis.md) | intermediate | G-A-1 | 聚合法/势能法/记账法分析均摊复杂度 |
| astar | [A*算法](nodes/astar.md) | intermediate | G-A-14 | f=g+h优先队列搜索，可采纳启发函数保证最优性 |
| bcc | [双连通分量(BCC)](nodes/bcc.md) | intermediate | G-B-4 | 点双/边双连通分量，DFS缩点分解 |
| bellman-ford | [Bellman-Ford算法](nodes/bellman-ford.md) | intermediate | G-B-2 | 含负权单源最短路，松弛操作O(VE)，可判负环 |
| bfs-01 | [0-1 BFS](nodes/bfs-01.md) | intermediate | G-B-2 | 双端队列处理0/1权边最短路O(V+E) |
| bidirectional | [双向搜索/Meet in the Middle](nodes/bidirectional.md) | intermediate | G-A-14 | 从两端同时搜索或折半枚举，O(2^{n/2})降低指数 |
| binary-lifting | [倍增](nodes/binary-lifting.md) | intermediate | G-A-1 | 预处理2^k次幂跳跃，用于ST表/LCA/稀疏表等 |
| bitset-compression | [bitset压位](nodes/bitset-compression.md) | intermediate | G-E-2 | 用bitset将O(n^2/64)bitset操作优化，莫队配合bitset加速，bitset集合运算 |
| bridge | [割边(桥)](nodes/bridge.md) | intermediate | G-B-4 | 删除后使图不连通的边，DFS+low判定O(V+E) |
| bst | [二叉搜索树基础](nodes/bst.md) | intermediate | G-A-8 | 左<根<右性质，期望O(log n)操作，最坏O(n)退化 |
| cartesian-tree | [笛卡尔树](nodes/cartesian-tree.md) | intermediate | G-A-9 | 数组下标BST+值堆性质，单调栈O(n)构建，RMQ转化；键满足 BST、权满足堆性质，可将 RMQ 转为 LCA 实现线性 |
| catalan-number | [卡特兰数](nodes/catalan-number.md) | intermediate | G-C-10 | C_n=C(2n,n)/(n+1)，括号序列/二叉树/出栈序列等计数 |
| conditional-probability | [条件概率](nodes/conditional-probability.md) | intermediate | G-C-15 | P(A\|B)=P(AB)/P(B)，贝叶斯公式与全概率公式 |
| constant-opt | [常数优化](nodes/constant-opt.md) | intermediate | G-E-1 | 循环展开、局部性利用、代码布局优化、编译器O2优化等常数级加速技巧 |
| construction | [构造题](nodes/construction.md) | intermediate | G-A-1 | 构造满足条件的解，需洞察问题结构 |
| convex-hull | [凸包(Andrew/Graham)](nodes/convex-hull.md) | intermediate | G-D-1 | O(nlogn) 求点集凸包，Andrew 单调链与 Graham 扫描两种实现 |
| cut-vertex | [割点(关节点)](nodes/cut-vertex.md) | intermediate | G-B-4 | 删除后使图不连通的点，DFS+low判定O(V+E) |
| dag-dp | [差分约束/DAG最短路](nodes/dag-dp.md) | intermediate | G-B-9 | 差分约束系统建图+最短路，DAG上拓扑序DP |
| dinic | [Dinic最大流](nodes/dinic.md) | intermediate | G-B-5 | 分层图+多路增广O(V²E)，二分图O(E√V) |
| dp-count | [计数DP](nodes/dp-count.md) | intermediate | G-A-11 | 利用DP记忆化求计数问题，划分子集不重不漏 |
| dp-dag | [DAG上的DP](nodes/dp-dag.md) | intermediate | G-A-11 | 有向无环图上的最长/最短路，拓扑序转移 |
| dp-knapsack-group | [分组背包](nodes/dp-knapsack-group.md) | intermediate | G-A-11 | 物品分组，每组最多选一件 |
| dp-knapsack-multiple | [多重背包](nodes/dp-knapsack-multiple.md) | intermediate | G-A-11 | 每件物品有限数量，二进制拆分或单调队列优化 |
| dp-number | [数位DP](nodes/dp-number.md) | intermediate | G-A-11 | 按数位逐位枚举，记忆化记录合法状态，大区间计数 |
| dp-opt-data-structure | [数据结构优化DP](nodes/dp-opt-data-structure.md) | intermediate | G-A-12 | 用线段树/BIT/平衡树加速转移中的查询/修改操作 |
| dp-opt-monotonic-queue | [单调队列/栈优化DP](nodes/dp-opt-monotonic-queue.md) | intermediate | G-A-12 | 用单调队列维护滑动窗口最值加速转移，如多重背包 |
| dp-opt-overview | [DP优化概述](nodes/dp-opt-overview.md) | intermediate | G-A-12 | 利用数据结构/数学性质/状态设计降低DP转移复杂度 |
| dp-probability | [概率/期望DP](nodes/dp-probability.md) | intermediate | G-A-11 | 概率顺推/期望逆推，可能需高斯消元处理环依赖 |
| dp-state | [状压DP](nodes/dp-state.md) | intermediate | G-A-11 | 集合状态编码为二进制整数，适合小规模状态空间 |
| dp-tree-knapsack | [树上背包](nodes/dp-tree-knapsack.md) | intermediate | G-A-11 | 树形DP+背包结合，依赖关系物品选择 |
| dsu-application | [并查集应用](nodes/dsu-application.md) | intermediate | G-D-9 | 扩展域/带权/可撤销并查集与 Kruskal 重构树处理连通性问题 |
| dsu-on-tree | [启发式合并(dsu on tree)](nodes/dsu-on-tree.md) | intermediate | G-B-7 | 轻儿子贡献清空+重儿子保留，离线子树查询O(nlogn) |
| dsu-weighted | [带权/扩展域并查集](nodes/dsu-weighted.md) | intermediate | G-A-4 | 维护节点间权值关系/种类关系，处理冲突判断 |
| euler-path | [欧拉路/回路](nodes/euler-path.md) | intermediate | G-B-8 | 判定(度数条件)+Hierholzer算法O(V+E) |
| expression-eval | [表达式求值](nodes/expression-eval.md) | intermediate | G-E-7 | 中缀→后缀(逆波兰)→栈求值；表达式树；运算符优先级+双栈法O(n) |
| fast-output | [快速输出](nodes/fast-output.md) | intermediate | G-E-1 | 整数快速输出：putchar/fwrite；Python用'\n'.join(map(str,...))批量输出 |
| fenwick-extended | [扩展树状数组](nodes/fenwick-extended.md) | intermediate | G-A-5 | 差分实现区间修改+区间查询，或双BIT维护不可差分信息 |
| game-graph | [博弈图与必胜必败态](nodes/game-graph.md) | intermediate | G-E-6 | 博弈图DAG上N态(存在后继P态)/P态(所有后继N态)；O(\|V\|+\|E\|)标记所有状态 |
| heuristic-search | [启发式搜索](nodes/heuristic-search.md) | intermediate | G-A-14 | 估价函数引导分支选择，可行性/最优性剪枝 |
| hld | [树链剖分(HLD)](nodes/hld.md) | intermediate | G-B-7 | 重链剖分，路径查询/修改O(log²V)，可求LCA；按轻重边将树剖为链，配合线段树 O(log^2 n) 维护路径/子树 |
| huffman-tree | [哈夫曼树](nodes/huffman-tree.md) | intermediate | G-A-3 | 最优前缀编码树，贪心构造，WPL最小 |
| hungarian | [匈牙利算法(Kuhn)](nodes/hungarian.md) | intermediate | G-B-6 | 二分图最大匹配，增广路O(VE) |
| idastar | [IDA*算法](nodes/idastar.md) | intermediate | G-A-14 | 迭代加深+A*剪枝，限制路径成本而非深度 |
| inclusion-exclusion | [容斥原理](nodes/inclusion-exclusion.md) | intermediate | G-C-11 | \|A1∪A2∪...\|=sum(-1)^k S(k)，多集合并集计数与莫比乌斯反演基础 |
| iterative-deepening | [迭代加深(IDDFS)](nodes/iterative-deepening.md) | intermediate | G-A-14 | 逐步增加DFS深度限制，DFS方式实现BFS效果，空间优 |
| johnson | [Johnson算法](nodes/johnson.md) | intermediate | G-B-2 | 全源最短路，势能法处理负权，n次Dijkstra O(VElogV) |
| josephus | [约瑟夫问题](nodes/josephus.md) | intermediate | G-E-7 | n人围圈报数出列：递推f(n,k)=(f(n-1,k)+k)%n，O(n)；大n小k有O(k log n)解法；递推 f(i)=(f(i-1)+m)%i 求 n 人循环报数幸存者 |
| km-algorithm | [KM算法](nodes/km-algorithm.md) | intermediate | G-B-6 | 二分图最大权匹配(Kuhn-Munkres)O(V³) |
| linear-system | [线性方程组](nodes/linear-system.md) | intermediate | G-C-14 | 高斯消元求解Ax=b，判断唯一/无穷/无解，异或方程组变体 |
| majority-element | [主元素/Boyer-Moore投票](nodes/majority-element.md) | intermediate | G-E-7 | 出现>n/2的元素：候选+计数消去法O(n)O(1)；在线流式处理 |
| manacher | [Manacher算法](nodes/manacher.md) | intermediate | G-C-5 | O(n)求最长回文子串，利用回文对称性避免重复扩展 |
| max-flow | [最大流(Edmonds-Karp)](nodes/max-flow.md) | intermediate | G-B-5 | Ford-Fulkerson增广路+EK BFS找路O(VE²) |
| min-cut | [最小割](nodes/min-cut.md) | intermediate | G-B-5 | 最大流最小割定理转化，s-t最小割=最大流 |
| mo-algorithm | [莫队算法](nodes/mo-algorithm.md) | intermediate | G-D-7 | 离线区间询问：排序后双指针移动，O(n√n)处理多类区间查询；离线排序区间询问，块长 sqrt n，O(n sqrt n) 处理可 O(1) 扩展的区间 |
| numeric-binary-search | [数值二分](nodes/numeric-binary-search.md) | intermediate | G-C-16 | 二分搜索求方程近似解/极值，实数二分控制精度 |
| persistent-concept | [可持久化数据结构概念](nodes/persistent-concept.md) | intermediate | G-A-7 | 保存历史版本，部分可持久化vs完全可持久化 |
| rabin-karp | [Rabin-Karp](nodes/rabin-karp.md) | intermediate | G-C-1 | 基于滚动哈希的字符串匹配，O(n+m)期望，字符串哈希的匹配应用 |
| random-technique | [随机化技巧](nodes/random-technique.md) | intermediate | G-E-5 | 随机覆盖目标元素/随机命中目标集合/随机打乱消除最坏情况，概率上界分析 |
| rmq | [RMQ 专题](nodes/rmq.md) | intermediate | G-D-9 | 区间最值查询：ST 表 O(1)/线段树/±1RMQ 线性预处理 |
| search-pruning | [搜索剪枝优化](nodes/search-pruning.md) | intermediate | G-A-14 | 可行性剪枝/最优性剪枝/搜索顺序优化，减少搜索量 |
| segment-intersection | [线段相交判定与求交](nodes/segment-intersection.md) | intermediate | G-D-2 | 跨立实验判两线段是否相交并求交点，几何求交基础 |
| spfa | [SPFA算法](nodes/spfa.md) | intermediate | G-B-2 | Bellman-Ford队列优化，均摊快但最坏O(VE) |
| sqrt-decomposition | [根号分块(通用)](nodes/sqrt-decomposition.md) | intermediate | G-D-6 | 按块长 sqrt(n) 分块，整块维护+散块暴力，O(sqrt n) 操作；O(sqrt n)块内暴力+块间预处理，通用性最强的区间结构 |
| submask-enum | [子集枚举](nodes/submask-enum.md) | intermediate | G-E-2 | 枚举位掩码所有子集的O(3^n)技巧，子集DP常用 |
| testlib | [testlib对拍框架](nodes/testlib.md) | intermediate | G-E-9 | testlib.h：generator/generator/checker/interactor/validator，标准对拍与出题工具 |
| tree-centroid | [树的重心](nodes/tree-centroid.md) | intermediate | G-B-7 | 删除后最大子树最小的节点，分治基础 |
| two-sat | [2-SAT](nodes/two-sat.md) | intermediate | G-B-4 | 2-适定性问题，建图+SCC判定可行性与拓扑逆序 |
| z-function | [Z函数](nodes/z-function.md) | intermediate | G-C-1 | Z数组z[i]表示S与S[i..]的最长公共前缀长度，线性构造，可用于匹配与周期判断 |

## P2 · 选学 (116)

| id | name | stage | group | brief |
| --- | --- | --- | --- | --- |
| 15-puzzle | [15谜题可解性判定](nodes/15-puzzle.md) | advanced | G-E-7 | N-puzzle可解性判定：逆序对数奇偶性+空格行距，不可解则无解；N 数码可解性判据：逆序对奇偶性(奇数阶)或行距+逆序对(偶数阶) |
| 3d-geometry | [三维几何](nodes/3d-geometry.md) | advanced | G-D-3 | 三维向量/平面/法向量/多面体体积与表面积，由二维推广 |
| anti-hash | [防卡Hash随机化](nodes/anti-hash.md) | advanced | G-E-5 | 字符串哈希用随机base/双哈希/随机化seed防止构造数据碰撞攻击 |
| avl | [AVL树](nodes/avl.md) | advanced | G-A-8 | 严格平衡(高度差<=1)，旋转维护 |
| berlekamp-massey | [Berlekamp-Massey](nodes/berlekamp-massey.md) | advanced | G-C-12 | O(n^2)求序列最短线性递推式，配合NTT加速求第n项 |
| bit-tricks | [位运算技巧](nodes/bit-tricks.md) | advanced | G-E-2 | Gray码、lowbit(x&-x)、popcount、前导零、位运算交换/去重等进阶技巧 |
| block-list | [分块链表](nodes/block-list.md) | advanced | G-D-6 | 块状链表，链式分块支持插入删除与区间查询；链表+分块混合，支持插入删除的O(sqrt n)区间操作 |
| boyer-moore | [Boyer-Moore](nodes/boyer-moore.md) | advanced | G-C-1 | 基于坏字符与好后缀规则的字符串匹配算法，子线性平均复杂度 |
| burnside-lemma | [Burnside引理](nodes/burnside-lemma.md) | advanced | G-C-11 | 群作用下不等价轨道数=\|G\|^{-1} sum \|Fix(g)\|，Polya计数基础 |
| cat-tree | [猫树](nodes/cat-tree.md) | advanced | G-D-6 | 分治预处理静态区间，跨越中点的查询 O(1)；分治预处理O(1)静态区间查询，不支持修改 |
| centroid-decomposition | [点分治](nodes/centroid-decomposition.md) | advanced | G-B-7 | 重心递归分解，路径统计O(nlogn) |
| char-polynomial | [特征多项式](nodes/char-polynomial.md) | advanced | G-C-14 | det(λI-A)，特征值与Cayley-Hamilton定理，线性递推加速基础 |
| circle-intersection | [圆与直线/圆求交](nodes/circle-intersection.md) | advanced | G-D-2 | 解几何方程求圆与直线、圆与圆交点 |
| continued-fraction | [连分数](nodes/continued-fraction.md) | advanced | G-C-9 | 实数的有理逼近，渐近分数递推，Pell方程与Stern-Brocot基础 |
| convex-hull-trick | [凸包优化(CHT)](nodes/convex-hull-trick.md) | advanced | G-D-1 | 维护下/上凸壳按斜率二分求 DP 转移最值，斜率优化经典 |
| diagonalization | [矩阵对角化](nodes/diagonalization.md) | advanced | G-C-14 | A=PDP^{-1}，矩阵快速幂优化，特征值分解 |
| dirichlet-convolution | [狄利克雷卷积](nodes/dirichlet-convolution.md) | advanced | G-C-9 | 数论函数的卷积运算，莫比乌斯反演与杜教筛的理论框架 |
| discrete-root | [离散k次根](nodes/discrete-root.md) | advanced | G-C-8 | 求x^k≡a(mod p)的解，基于原根将问题转化为离散对数 |
| dlx | [Dancing Links(X算法)](nodes/dlx.md) | advanced | G-A-14 | 双向十字链表加速精确覆盖/重复覆盖问题的回溯搜索 |
| dmst | [最小树形图(DMST)](nodes/dmst.md) | advanced | G-B-3 | 有向图最小生成树，朱刘算法O(VE) |
| dominator-tree | [支配树](nodes/dominator-tree.md) | advanced | G-B-4 | 支配关系树结构，Lengauer-Tarjan算法O(Eα(V)) |
| dp-dynamic | [动态DP(DDP)](nodes/dp-dynamic.md) | advanced | G-A-13 | 带修改的树上DP，广义矩阵乘法+LCT维护转移矩阵 |
| dp-opt-quadrangle | [四边形不等式/决策单调性优化](nodes/dp-opt-quadrangle.md) | advanced | G-A-12 | w满足四边形不等式则决策单调，分治/单调队列优化 |
| dp-opt-slope-trick | [Slope Trick](nodes/dp-opt-slope-trick.md) | advanced | G-A-12 | 维护凸函数的斜率/拐点序列，简化凸DP转移 |
| dp-opt-wqs | [WQS二分/凸优化DP](nodes/dp-opt-wqs.md) | advanced | G-A-12 | 带数量限制的凸DP，二分惩罚系数消除限制 |
| dp-plug | [插头DP(连通性状态压缩DP)](nodes/dp-plug.md) | advanced | G-A-13 | 轮廓线DP+连通性编码，解决网格哈密顿路径/回路计数 |
| egf | [EGF(指数生成函数)](nodes/egf.md) | advanced | G-C-13 | a_n的指数生成函数=sum a_n x^n/n!，标号结构计数工具 |
| euler-tour-tree | [Euler Tour Tree](nodes/euler-tour-tree.md) | advanced | G-D-4 | 将动态树转为欧拉序上的平衡树区间操作，支持连断边；欧拉序维护动态树，平衡树支持换根/连边/断边 |
| fsm | [有限状态机](nodes/fsm.md) | advanced | G-E-7 | FSM用于字符串匹配/自动机DP/AC自动机基础，竞赛中处理模式匹配问题 |
| fwt | [FWT(快速沃尔什变换)](nodes/fwt.md) | advanced | G-C-12 | O(n log n)计算位运算(and/or/xor)卷积，FFT的位运算推广 |
| generating-function-basics | [生成函数基础](nodes/generating-function-basics.md) | advanced | G-C-13 | 形式幂级数基本运算：加乘求导积分复合逆，OGF/EGF的前置 |
| geometric-inverse | [反演变换](nodes/geometric-inverse.md) | advanced | G-D-3 | 圆/直线相切问题经反演简化，保角变换 |
| hill-climbing | [爬山算法](nodes/hill-climbing.md) | advanced | G-E-5 | 局部择优启发式搜索，每次在当前最优解附近找更优解；易陷入局部最优，单峰函数有效 |
| hopcroft-karp | [Hopcroft-Karp算法](nodes/hopcroft-karp.md) | advanced | G-B-6 | 二分图匹配，多增广路O(E√V) |
| integer-partition | [整数划分](nodes/integer-partition.md) | advanced | G-C-11 | 将n拆为正整数之和的方案数，生成函数与五边形数定理O(n sqrt n) |
| kahan-summation | [Kahan求和](nodes/kahan-summation.md) | advanced | G-E-7 | 补偿求和法降低浮点累加误差：维护误差补偿变量c，精度接近double但只多一个变量 |
| kdt | [KD 树](nodes/kdt.md) | advanced | G-D-6 | k 维空间分块树，高效处理 k 维最近邻/范围查询；k维空间分块树，最近邻/矩形查询，O(n^{1-1/k}) |
| kth-shortest-path | [k短路](nodes/kth-shortest-path.md) | advanced | G-B-2 | 第k短路径，A*或可并堆方法 |
| lattice-points | [格点计数](nodes/lattice-points.md) | advanced | G-D-3 | 线段/多边形内整点计数，结合皮克定理与整除递推 |
| lift-the-exponent | [LTE引理](nodes/lift-the-exponent.md) | advanced | G-C-9 | Lift the Exponent引理，求v_p(a^n-b^n)的公式，简化幂次整除问题 |
| linear-recurrence | [线性递推](nodes/linear-recurrence.md) | advanced | G-C-12 | 常系数线性齐次递推O(k log k log n)求第n项，BM+NTT+Cayley-Hamilton |
| lyndon-factorization | [Lyndon分解](nodes/lyndon-factorization.md) | advanced | G-C-6 | Duval算法O(n)将字符串分解为字典序递减的Lyndon串，用于最小表示法 |
| matrix-rank | [矩阵秩](nodes/matrix-rank.md) | advanced | G-C-14 | 高斯消元求矩阵秩，线性无关向量组最大个数 |
| matrix-tree | [矩阵树定理](nodes/matrix-tree.md) | advanced | G-B-3 | Laplace矩阵行列式求生成树计数 |
| max-avg-segment | [最大平均值区段](nodes/max-avg-segment.md) | advanced | G-E-7 | 求长度≥L的最大平均值子数组：二分+前缀和判定，分数规划经典应用；Kadane 算法 O(n) 求最大子段和，前缀和+单调队列求限制长度的最大/小子段 |
| min-cost-flow | [最小费用最大流](nodes/min-cost-flow.md) | advanced | G-B-5 | SSP算法，SPFA/Dijkstra找最短增广路 |
| min-cycle | [最小环](nodes/min-cycle.md) | advanced | G-B-8 | 图中权值和最小的环，Floyd扩展或无向图方法 |
| minimal-string | [最小表示法](nodes/minimal-string.md) | advanced | G-C-6 | O(n)求循环字符串字典序最小的起始位置，基于Lyndon分解或双指针 |
| minkowski-sum | [闵可夫斯基和](nodes/minkowski-sum.md) | advanced | G-D-1 | 两凸多边形 Minkowski 和仍为凸多边形，用于碰撞检测/半平面并 |
| mo-2d | [二维莫队](nodes/mo-2d.md) | advanced | G-D-7 | 将莫队扩展到二维矩阵区间询问，分块大小n^(2/3)或n^(3/4)；四方向扩展指针，块长 n^(2/3)，处理矩阵区域询问 |
| mo-algo-with-bitset | [莫队+bitset](nodes/mo-algo-with-bitset.md) | advanced | G-D-7 | bitset 维护状态，莫队转移后位运算加速判定类统计 |
| mo-modifiable | [带修莫队](nodes/mo-modifiable.md) | advanced | G-D-7 | 支持单点修改的莫队：增加时间维，块大小n^(2/3)，复杂度O(n^(5/3))；增加时间维三元组排序，支持单点修改的区间询问 |
| mo-on-tree | [树上莫队](nodes/mo-on-tree.md) | advanced | G-D-7 | 欧拉序将树上路径询问转化为序列区间询问，再用莫队处理；用括号序将树压成序列，对路径询问跑莫队 |
| mo-rollback | [回滚莫队](nodes/mo-rollback.md) | advanced | G-D-7 | 不支持删除只支持插入的莫队变体：左右端点同块时暴力，否则只回滚不删除；只增不删，按左端点块排序后回滚，处理难删除的转移 |
| newton-method | [牛顿法](nodes/newton-method.md) | advanced | G-C-16 | O(log log eps)求函数零点，平方收敛，多项式牛顿迭代基础 |
| ogf | [OGF(普通生成函数)](nodes/ogf.md) | advanced | G-C-13 | a_n的普通生成函数=sum a_n x^n，组合计数的代数工具 |
| pairing-heap | [配对堆](nodes/pairing-heap.md) | advanced | G-A-3 | 均摊O(1)插入/O(log n)删除，Fibonacci堆的简单替代 |
| palindrome-automaton | [回文自动机(PAM)](nodes/palindrome-automaton.md) | advanced | G-C-5 | 存储字符串所有回文子串的最小DFA，O(n)构造，fail链指向最长回文后缀 |
| partizan-game | [非公平组合博弈](nodes/partizan-game.md) | advanced | G-E-6 | 双方可采取行动不同(如棋类)；Conway surreal number理论；较公平博弈复杂，竞赛少见；双方行动集不同的博弈，超实数理论与Surreal Number |
| persistent-balanced | [可持久化平衡树](nodes/persistent-balanced.md) | advanced | G-D-5 | 可持久化无旋转 Treap，函数式节点复用实现历史版本；可持久化无旋Treap，保存历史版本 |
| persistent-block-array | [可持久化分块数组](nodes/persistent-block-array.md) | advanced | G-D-5 | 可持久化思想与分块结合，按版本复用块信息 |
| persistent-dsu | [可持久化并查集](nodes/persistent-dsu.md) | advanced | G-A-4 | 基于可持久化线段树实现历史版本回溯的并查集 |
| persistent-heap | [可持久化堆](nodes/persistent-heap.md) | advanced | G-D-5 | 可持久化可并堆(左偏树)，常用于 k 短路问题；支持历史版本的堆，基于左偏树实现 |
| point-in-polygon | [点在多边形内判定](nodes/point-in-polygon.md) | advanced | G-D-1 | 射线法判一般多边形，凸多边形用有序二分 O(logn) |
| polya-enumeration | [Polya计数](nodes/polya-enumeration.md) | advanced | G-C-11 | Burnside+置换群下的染色计数，利用循环指标多项式 |
| prufer-code | [Prüfer序列](nodes/prufer-code.md) | advanced | G-B-7 | 树与序列双射，标号树计数Cayley公式 |
| quadratic-residue | [二次剩余](nodes/quadratic-residue.md) | advanced | G-C-8 | 求x^2≡a(mod p)的解，Cipolla算法O(log p)，Tonelli-Shanks |
| random-incremental | [随机增量法](nodes/random-incremental.md) | advanced | G-D-3 | 按随机序逐点加入并增量维护结构，期望线性复杂度 |
| random-variable | [随机变量](nodes/random-variable.md) | advanced | G-C-15 | 离散/连续随机变量及其分布，概率DP建模工具 |
| rmq-linear | [线性RMQ(±1 RMQ)](nodes/rmq-linear.md) | advanced | G-A-5 | O(n)预处理O(1)查询的RMQ，基于笛卡尔树+LCA |
| sbt | [Size Balanced Tree(SBT)](nodes/sbt.md) | advanced | G-A-8 | 按子树size维护平衡，O(log n)操作 |
| schedule-one-machine | [单机调度](nodes/schedule-one-machine.md) | advanced | G-D-10 | 单机作业排序使最大延迟/完工时间最优，按截止期贪心 |
| schedule-two-machines | [双机调度(Johnson 法则)](nodes/schedule-two-machines.md) | advanced | G-D-10 | 两台流水机作业调度，Johnson 法则求最短完工时间 |
| second-best-mst | [次小生成树](nodes/second-best-mst.md) | advanced | G-B-3 | 严格次小生成树，树链最大边替换法 |
| segments-union-length | [线段并集长度](nodes/segments-union-length.md) | advanced | G-D-2 | 扫描线求一维/二维线段并集长度，离散化+区间合并 |
| seq-automaton | [序列自动机](nodes/seq-automaton.md) | advanced | G-C-4 | next数组记录每个位置后各字符出现位置，O(n\|Σ\|)构造，子序列匹配自动机 |
| sgt | [替罪羊树(Scapegoat Tree)](nodes/sgt.md) | advanced | G-A-8 | 不平衡时按比例重构子树，O(log n)均摊 |
| simpson-integration | [Simpson积分](nodes/simpson-integration.md) | advanced | G-C-16 | 自适应Simpson法数值积分，O(1)抛物线逼近，处理难以解析的积分 |
| simulated-annealing | [模拟退火](nodes/simulated-annealing.md) | advanced | G-E-5 | 以概率e^(-ΔE/T)接受劣解跳出局部最优；初始温度/降温系数/终止温度三参数；卡时技巧clock()；基于Metropolis准则的概率搜索，以一定概率接受劣解逃离局部最优 |
| sqrt-tree | [sqrt 树](nodes/sqrt-tree.md) | advanced | G-D-6 | O(n sqrt n) 预处理静态序列，支持结合律运算 O(1) 查询；O(1)静态区间查询，O(sqrt n)重建，分块递归 |
| steiner-tree | [Steiner树](nodes/steiner-tree.md) | advanced | G-B-3 | 给定关键点集最小连通子图，NP-hard，状压DP |
| stern-brocot | [Stern-Brocot树/Farey序列](nodes/stern-brocot.md) | advanced | G-E-7 | 枚举所有既约分数的二元搜索树：二分逼近实数，求最优分数逼近 |
| stern-brocot-tree | [Stern-Brocot 树与 Farey 序列](nodes/stern-brocot-tree.md) | advanced | G-D-10 | 生成所有既约分数的二叉搜索树，二分定位有理数，关联 Farey 序列 |
| stirling-number | [斯特林数](nodes/stirling-number.md) | advanced | G-C-11 | 第一类(循环排列)与第二类(集合划分)Stirling数，递推与显式公式 |
| suffix-automaton | [后缀自动机(SAM)](nodes/suffix-automaton.md) | advanced | G-C-4 | 识别字符串所有子串的最小DFA，O(n)在线构造，endpos等价类 |
| suffix-tree | [后缀树](nodes/suffix-tree.md) | advanced | G-C-3 | 压缩所有后缀的Trie，Ukkonen算法O(n)在线构造，SA/SAM的等价结构 |
| tangents-two-circles | [两圆公切线](nodes/tangents-two-circles.md) | advanced | G-D-2 | 求两圆内外公切线，几何方程或向量构造 |
| triangulation | [三角剖分](nodes/triangulation.md) | advanced | G-D-2 | 将平面点集细分为三角形，常用耳切与对偶图 |
| vandermonde-convolution | [范德蒙德卷积](nodes/vandermonde-convolution.md) | advanced | G-C-10 | C(n+m,k)=sum C(n,i)C(m,k-i)，组合恒等式的重要工具 |
| vector-space | [向量空间](nodes/vector-space.md) | advanced | G-C-14 | 线性空间、基与维数，线性基与矩阵秩的理论基础 |
| vertical-decomposition | [垂直剖分(梯形剖分)](nodes/vertical-decomposition.md) | advanced | G-D-2 | 将平面按线段端点垂直切分为梯形单元，支持点定位与求交 |
| virtual-tree | [虚树](nodes/virtual-tree.md) | advanced | G-B-7 | 关键点集压缩树结构O(klogk)，配合DP |
| wblt | [WBLT(加权平衡叶树)](nodes/wblt.md) | advanced | G-A-8 | 按子树权重维护平衡，支持可持久化 |
| comparison-sort | [简单比较排序(冒泡/选择/插入/希尔)](nodes/comparison-sort.md) | basic | G-A-1 | O(n^2)简单排序及希尔分组优化，教学与小规模数据 |
| numeral-system | [数制转换](nodes/numeral-system.md) | basic | G-C-18 | 任意进制间转换，除K取余法与大数进制转换 |
| du-sieve | [杜教筛](nodes/du-sieve.md) | frontier | G-C-9 | O(n^2/3)求积性函数前缀和，基于Dirichlet卷积与数论分块 |
| general-sam | [广义后缀自动机](nodes/general-sam.md) | frontier | G-C-4 | 多字符串的SAM，Trie上建SAM或离线BFS建，支持多串子串查询 |
| monotonic-stack-dp | [单调栈优化DP](nodes/monotonic-stack-dp.md) | frontier | G-E-10 | Pareto frontier单调栈优化转移：双单调性(值递增/DP递减)使内层循环均摊O(1)；2025-12 CF教程 |
| seg-beats | [吉司机线段树(Segment Beats)](nodes/seg-beats.md) | frontier | G-D-8 | 区间取 min/max 等操作利用势能标记，均摊高效维护复杂区间信息；维护区间最值操作(区间取min/max)与历史最值；区最值操作(chmin/chmax)的懒标记线段树：mapping失败时下传递归，均摊高效 |
| bracket-sequence | [括号序列专题](nodes/bracket-sequence.md) | intermediate | G-D-9 | 合法括号序列判定/计数/线段树维护匹配(CF380C) |
| contest-resources | [学习资源与刷题路线](nodes/contest-resources.md) | intermediate | G-E-8 | OI Wiki roadmap、CF/AtCoder/Luogu刷题路线、经典教材推荐、进阶学习路径 |
| derangement | [错排问题](nodes/derangement.md) | intermediate | G-C-11 | D(n)=n!(1-1/1!+...+(-1)^n/n!)，全排列中无固定点的方案数 |
| distance-metric | [距离度量](nodes/distance-metric.md) | intermediate | G-D-3 | 欧氏/曼哈顿/切比雪夫距离及其变换(切比雪夫↔曼哈顿) |
| dp-opt-state | [状态设计优化](nodes/dp-opt-state.md) | intermediate | G-A-12 | 改变状态定义降低维度/状态数，题目特异性优化 |
| editor-setup | [编辑器配置](nodes/editor-setup.md) | intermediate | G-E-9 | VSCode/Vim/CLion等编辑器的CP竞赛配置：代码片段、调试、编译任务 |
| endian | [字节序](nodes/endian.md) | intermediate | G-E-7 | 大端序/小端序差异，网络字节序转换，二进制文件读写时需注意 |
| git-version | [Git版本管理](nodes/git-version.md) | intermediate | G-E-9 | 代码模板版本管理、团队协作、代码回溯与备份 |
| gray-code | [格雷码](nodes/gray-code.md) | intermediate | G-C-18 | 相邻二进制仅一位不同，G(i)=i^(i>>1)，汉密尔顿路径应用 |
| interaction-strategy | [交互题策略](nodes/interaction-strategy.md) | intermediate | G-E-8 | 交互次数优化、二分交互、随机撒点、flush时机、STDIO vs Grader交互模式 |
| line-intersection | [直线交点](nodes/line-intersection.md) | intermediate | G-D-2 | 用叉积判定两直线位置关系并求交点坐标 |
| minimax-alpha-beta | [Minimax/Alpha-Beta剪枝](nodes/minimax-alpha-beta.md) | intermediate | G-A-14 | 博弈对抗搜索，Alpha-Beta剪枝减少不必要分支 |
| oj-tool | [OJ工具](nodes/oj-tool.md) | intermediate | G-E-9 | 在线评测工具、代码提交辅助工具、评测机使用 |
| pick-theorem | [皮克定理](nodes/pick-theorem.md) | intermediate | G-D-3 | A=i+b/2-1 关联整点多边形面积与内部/边上格点数 |
| random-shuffle | [随机打乱防hack](nodes/random-shuffle.md) | intermediate | G-E-5 | shuffle打乱输入顺序防止构造数据卡哈希/快排；CF hack常见反制手段 |
| special-judge | [Special Judge](nodes/special-judge.md) | intermediate | G-E-9 | 非唯一解题目的自定义评测器：testlib checker编写，多解/最优解判定 |
| tortoise-hare | [Floyd环检测](nodes/tortoise-hare.md) | intermediate | G-E-7 | 龟兔赛跑算法：快慢指针检测链表/序列环，O(n)O(1)找环起点与周期；Floyd 双指针 O(1) 空间检测链表/序列中的环并定位 |

## P3 · 冷门 (49)

| id | name | stage | group | brief |
| --- | --- | --- | --- | --- |
| bell-number | [贝尔数](nodes/bell-number.md) | advanced | G-C-11 | B(n)表示n个元素集合划分的方案数，Stirling数之和，Bell三角形 |
| block-forest | [圆方树](nodes/block-forest.md) | advanced | G-B-4 | 点双连通缩点为圆方树结构，树上路径查询 |
| bounded-flow | [上下界网络流](nodes/bounded-flow.md) | advanced | G-B-5 | 有容量上下界的可行流/最大流/最小流转化 |
| chord-graph | [弦图](nodes/chord-graph.md) | advanced | G-B-9 | 完美消除序列(PES)，极大团与色数 |
| dp-dpofdp | [DP套DP](nodes/dp-dpofdp.md) | advanced | G-A-13 | 外层DP的状态是内层DP的结果，状态空间需分析 |
| fibonacci-heap | [斐波那契堆](nodes/fibonacci-heap.md) | advanced | G-A-3 | 均摊O(1)decrease-key，理论最优堆，实现复杂 |
| general-match | [一般图匹配](nodes/general-match.md) | advanced | G-B-6 | 带花树算法(Blossom)，一般图最大匹配O(V³) |
| hamilton-path | [哈密顿路](nodes/hamilton-path.md) | advanced | G-B-8 | NP-hard，状压DP O(2ⁿn²) |
| interactive-debug | [交互题调试](nodes/interactive-debug.md) | advanced | G-E-4 | 交互题对拍困难，需模拟交互过程；封装输入输出函数；静态查错能力重要 |
| lgv-lemma | [LGV行列式引理](nodes/lgv-lemma.md) | advanced | G-B-9 | Lindström-Gessel-Viennot引理，不相交路径计数 |
| max-clique | [最大团](nodes/max-clique.md) | advanced | G-B-9 | NP-hard，Bron-Kerbosch回溯或状压DP |
| mod-shortest-path | [同余最短路](nodes/mod-shortest-path.md) | advanced | G-B-2 | 利用同余类建图求最小权值，模数优化 |
| planar-graph | [平面图](nodes/planar-graph.md) | advanced | G-B-9 | 欧拉公式V-E+F=2，对偶图与面着色 |
| polygon | [Polygon出题平台](nodes/polygon.md) | advanced | G-E-9 | Codeforces Polygon：题目打包、测试数据生成、validator/checker配置 |
| rbtree | [红黑树](nodes/rbtree.md) | advanced | G-A-8 | 弱平衡BST，C++ std::map底层，竞赛中少用 |
| schedule-deadline-duration | [截止期限-工期调度](nodes/schedule-deadline-duration.md) | advanced | G-D-10 | 给定截止期限与工期求最优调度可行性，贪心+堆 |
| stoer-wagner | [Stoer-Wagner全局最小割](nodes/stoer-wagner.md) | advanced | G-B-5 | 无向图全局最小割，贪心合并O(V³) |
| tree-decompose | [树分块](nodes/tree-decompose.md) | advanced | G-A-9 | 树上Sqrt分块，配合莫队处理树上路径查询 |
| tree-hash | [树哈希](nodes/tree-hash.md) | advanced | G-B-7 | 树同构判定，哈希递归子树 |
| ai-cp-trend | [AI竞赛编程趋势](nodes/ai-cp-trend.md) | frontier | G-E-10 | 2026年GrandCode/Solvita等AI系统在CF live round超越人类GM；test-time RL+agentic loop趋势 |
| binary-tree-dp-trick | [二叉化树DP Trick](nodes/binary-tree-dp-trick.md) | frontier | G-E-10 | 多叉树添加虚节点链转为二叉树，使O(n²)树形DP的合并复杂度天然成立；2026 CF Round 1100 |
| bitmask-dp-optimization | [位掩码DP优化](nodes/bitmask-dp-optimization.md) | frontier | G-E-10 | 2^n·n·log(A)位掩码DP+二分搜索求最大化最小值；2026 CF Round 1100 Editorial |
| delaunay-triangulation | [Delaunay 三角剖分](nodes/delaunay-triangulation.md) | frontier | G-D-2 | 满足空圆性质的三角剖分，对偶为 Voronoi 图 |
| elementary-generating-functions | [初等生成函数](nodes/elementary-generating-functions.md) | frontier | G-C-13 | 常见序列的生成函数闭式：几何/二项/指数/三角等 |
| eulerian-number | [欧拉数](nodes/eulerian-number.md) | frontier | G-C-11 | A(n,k)表示排列中恰好k个上升段的个数，Worpitzky恒等式 |
| generating-function-shift | [生成函数平移](nodes/generating-function-shift.md) | frontier | G-C-13 | 指数平移与系数平移技巧，生成函数的高级操作 |
| interactive-problem-trend | [交互题兴起趋势](nodes/interactive-problem-trend.md) | frontier | G-E-10 | ICPC 2024-2025 Nanjing连续出袋鼠交互题；NOI/WC系列恢复交互题；交互题成为高频题型 |
| kinetic-tournament-tree | [Kinetic Tournament Tree](nodes/kinetic-tournament-tree.md) | frontier | G-D-8 | 线段树维护线性函数序列，支持线段插入删除的最值查询；动态凸壳维护，线段树节点存一次函数，支持区间最值 |
| lagrange-inversion | [拉格朗日反演](nodes/lagrange-inversion.md) | frontier | G-C-12 | O(n log n)求复合逆的系数，生成函数计数的高级工具 |
| main-lorentz | [Main-Lorentz](nodes/main-lorentz.md) | frontier | G-C-6 | O(n log n)找出字符串所有平方串(重复子串)的出现位置 |
| meissel-lehmer | [Meissel-Lehmer](nodes/meissel-lehmer.md) | frontier | G-C-9 | O(n^2/3)计算pi(n)（n以内素数个数），基于递归容斥 |
| min-25-sieve | [Min_25筛](nodes/min-25-sieve.md) | frontier | G-C-9 | O(n^3/4/log n)求积性函数前缀和，基于埃氏筛思想与状态转移 |
| mo-algo-secondary-offline | [二次离线莫队](nodes/mo-algo-secondary-offline.md) | frontier | G-D-7 | 单次转移非 O(1) 时再离线一次，降低整体复杂度 |
| multipoint-eval-interpolation | [多点求值与插值](nodes/multipoint-eval-interpolation.md) | frontier | G-C-12 | O(n log^2 n)多项式多点求值与插值，基于分治与NTT |
| nested-segment-tree | [线段树嵌套(树套树)](nodes/nested-segment-tree.md) | frontier | G-D-8 | seg-in-seg/seg-in-bit/seg-in-balanced 等多维信息维护结构；线段树套线段树/BIT/平衡树，支持二维或多维区间操作 |
| newton-iteration-poly | [多项式牛顿迭代](nodes/newton-iteration-poly.md) | frontier | G-C-12 | O(n log n)求多项式开根/对数/指数/逆，基于牛顿法推广到形式幂级数 |
| pell-equation | [佩尔方程](nodes/pell-equation.md) | frontier | G-C-9 | x^2-Dy^2=1的整数解，连分数法求解，最小解递推通项 |
| poly-compose-inverse | [多项式复合与求逆](nodes/poly-compose-inverse.md) | frontier | G-C-13 | O(n log^2 n)多项式复合与复合逆，拉格朗日反演的应用 |
| powerful-number-sieve | [Powerful Number筛](nodes/powerful-number-sieve.md) | frontier | G-C-9 | O(n^3/4)求积性函数前缀和，基于Powerful Number分解 |
| prefix-gcd-optimization | [前缀GCD变化优化](nodes/prefix-gcd-optimization.md) | frontier | G-E-10 | 前缀GCD至多变化O(log A)次，利用此性质将O(n²)优化到O(n log A)；2026 CF Insomnia'26 |
| suffix-array-optimal | [最优原地后缀数组](nodes/suffix-array-optimal.md) | frontier | G-C-3 | 线性时间O(n)且O(1)额外空间构造后缀数组的变体(SA-IS等) |
| suffix-bst | [后缀平衡树](nodes/suffix-bst.md) | frontier | G-C-3 | 用平衡BST维护后缀排序，支持动态插入删除字符的后缀结构 |
| symbolic-method | [符号化方法](nodes/symbolic-method.md) | frontier | G-C-13 | 组合类到生成函数的系统化映射(SEQ/SET/MSET等构造子) |
| top-tree | [Top Tree](nodes/top-tree.md) | frontier | G-D-4 | Self-Adjusting Top Tree 维护完全动态森林的路径与子树信息；维护树上层和路径信息的通用框架，LCT的扩展 |
| balanced-ternary | [平衡三进制](nodes/balanced-ternary.md) | intermediate | G-C-18 | 用{-1,0,1}表示的三进制，无符号位自然表示负数 |
| randomized-heap | [随机化堆](nodes/randomized-heap.md) | intermediate | G-A-3 | 随机合并的可并堆，期望O(log n) |
| skiplist | [跳表(Skip List)](nodes/skiplist.md) | intermediate | G-A-10 | 多层链表随机化，期望O(log n)查找/插入 |
| tim-sort | [Timsort](nodes/tim-sort.md) | intermediate | G-A-1 | 归并+插入混合稳定排序，Python/Java标准库使用 |
| tournament-sort | [锦标赛排序](nodes/tournament-sort.md) | intermediate | G-A-1 | 基于锦标赛树的排序，O(n log n) |
