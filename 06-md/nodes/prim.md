---
id: prim
name: Prim算法
group: G-B-3
stage: basic
priority: P0
depth_tier: deep
---

# Prim算法

> 最小生成树，贪心+堆O(E log V)，适合稠密图(暴力O(n^2)在完全图上最优)

<!-- 元信息: id=prim · group=G-B-3 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

Prim 算法是求无向连通图最小生成树(MST)的经典贪心算法。与 Kruskal 加边不同，Prim 不断加点：从任一源点出发，维护一个已加入集合，每次选取连接已选集合与未选集合的最小边，把对应新点加入集合，重复 n-1 次。朴素版每次 O(n) 扫描找最小边，总复杂度 O(n^2+m)，适合稠密图/完全图；堆优化版用优先队列维护候选边，复杂度 O((n+m)log n)。

## Why · 为什么

### 直觉 · Intuition

像从一块区域向外扩地皮：已圈定的区域内所有点到外部的边中，必然存在一条最小生成树边，贪心选它永远不亏。每次扩张都保证当前区域是最优连通的，最终连满 n 个点即得全局 MST。和 Dijkstra 长得一模一样，只是把『到源点距离』换成『到已选集合的最小边』。

### 原理 · Principle

贪心选择 + 切定理(Cut Property)：对任意顶点集 S，跨过切 (S, V\S) 的最小权边必属于某棵 MST。Prim 每一步选取跨过『已选集合』这条切的最小边，故得到全局最优。正确性依赖边权非负（MST 本身要求正权/可负但无负环影响；一般题目边权为正）。堆优化版借 decrease-key 思想：新点入集合后只更新其邻居的 min_edge。

### 历史 · History

由捷克数学家 Vojtěch Jarník 于 1930 年提出，1957 年由 Robert Prim 重新发现，1959 年 Edsger Dijkstra 也独立发表，故又名 Jarník–Prim–Dijkstra 算法。是 MST 三大经典算法(Kruskal/Prim/Borůvka)之一。

## How · 实现

### 伪代码

```python
function prim(n, adj):  # adj[v] = list of (w, to)
  visited[n]=false, min_w[n]=INF, min_w[0]=0
  pq = min-heap([(0,0)]); total=0
  while pq not empty:
    (w,u) = pop min
    if visited[u] or w != min_w[u]: continue
    visited[u]=true; total+=w
    for (nw,v) in adj[u]:
      if not visited[v] and nw < min_w[v]:
        min_w[v]=nw; push (nw,v)
  if not all visited: return None
  return total
```

### Python 实现

```python
import heapq


def prim_mst(n, adj):
    """堆优化 Prim: adj[i] = list of (w, j)。返回 (总权, parent)，不连通返回 None"""
    visited = [False] * n
    min_w = [float('inf')] * n
    parent = [-1] * n
    min_w[0] = 0
    pq = [(0, 0)]
    total = 0
    cnt = 0
    while pq:
        w, u = heapq.heappop(pq)
        if visited[u] or w != min_w[u]:
            continue
        visited[u] = True
        total += w
        cnt += 1
        for nw, v in adj[u]:
            if not visited[v] and nw < min_w[v]:
                min_w[v] = nw
                parent[v] = u
                heapq.heappush(pq, (nw, v))
    if cnt != n:
        return None
    return total, parent


def prim_matrix(n, a):
    """暴力 O(n^2) Prim: a 为邻接矩阵，INF 表示无边，适合稠密图/完全图"""
    INF = float('inf')
    visited = [False] * n
    min_w = [INF] * n
    min_w[0] = 0
    total = 0
    for _ in range(n):
        v = -1
        for j in range(n):
            if not visited[j] and (v == -1 or min_w[j] < min_w[v]):
                v = j
        if min_w[v] == INF:
            return None
        visited[v] = True
        total += min_w[v]
        for j in range(n):
            if not visited[j] and a[v][j] < min_w[j]:
                min_w[j] = a[v][j]
    return total


if __name__ == "__main__":
    # 三角形 0-1(2), 1-2(3), 0-2(4) -> MST = 5
    adj = [[(2, 1), (4, 2)], [(2, 0), (3, 2)], [(4, 0), (3, 1)]]
    total, parent = prim_mst(3, adj)
    assert total == 5, total
    INF = 10**9
    a = [[0, 2, 4], [2, 0, 3], [4, 3, 0]]
    assert prim_matrix(3, a) == 5
    adj2 = [[(1, 1)], [(1, 0)], []]  # 不连通
    assert prim_mst(3, adj2) is None
    print("prim OK")

```

**PyPy 提示**: PyPy 下 heapq + 邻接表在 n,m ≤ 2e5 时约可跑 1e6 次操作/秒级。注意判断不连通：cnt != n 时返回 None；连通图必经 visited[0] 从 0 出发。堆里可能残留旧的大权值条目，用 w != min_w[u] 或 visited 判重跳过，不要用 count 计数错误叠加。完全图(如 Euclid MST 需两两算距离)务必用 O(n^2) 暴力版，PyPy 下 n=5000 约 0.1s。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 暴力 O(n^2+m)；二叉堆 O((n+m) log n) |
| 空间 | O(n+m) |

### 局限

1) 只适用于无向图求 MST，有向图最小树形图需朱刘算法(dmst 节点)；2) 不连通图无 MST，需特判；3) 边权可为负但对 MST 无影响(负权边仍优先选)，Prim 不依赖非负性；4) 堆优化版用二叉堆常数比 Kruskal 大，稀疏图优先 Kruskal；稠密/完全图用 O(n^2) 暴力版更快。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3366 | 2 | 最小生成树模板：Kruskal/Prim 均可，验证基础 MST 正确性 | [https://www.luogu.com.cn/problem/P3366](https://www.luogu.com.cn/problem/P3366) |
| Luogu | P1265 | 3 | 公路修建：完全图 MST，必须用 O(n^2) 暴力 Prim(边数 n^2 无法存) | [https://www.luogu.com.cn/problem/P1265](https://www.luogu.com.cn/problem/P1265) |
| POJ | 1287 | 2 | Networking：多重边取最小权的 Prim/Kruskal 模板 | [http://poj.org/problem?id=1287](http://poj.org/problem?id=1287) |

## Pitfalls · 易错点

- 堆中残留旧条目未判重：pop 后必须检查 visited[u] 或 min_w[u]，否则重复累加
- 完全图用堆优化版反而慢(O(n^2 log n))，必须用 O(n^2) 暴力扫描
- 忘记处理不连通图(返回 None/No MST)导致无限循环
- 把 Prim 用于有向图(应走最小树形图)或稀疏大图(应走 Kruskal)
- 邻接表存成 (w,v) 与 (v,w) 顺序不一致导致解包错误

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/mst/](https://oi-wiki.org/graph/mst/)
- CP-Algorithms ✓ [https://cp-algorithms.com/graph/mst_prim.html](https://cp-algorithms.com/graph/mst_prim.html)
- 书籍 ✓ `CPH ch15 pp151-158`
