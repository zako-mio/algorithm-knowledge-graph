---
id: dijkstra
name: Dijkstra算法
group: G-B-2
stage: basic
priority: P0
depth_tier: deep
---

# Dijkstra算法

> 非负权单源最短路，堆优化O((V+E)logV)，贪心松弛

<!-- 元信息: id=dijkstra · group=G-B-2 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

Dijkstra 算法是求解『非负权图』上单源最短路径的经典算法（由 E. W. Dijkstra 1956 年发现、1959 年发表）。维护两个集合：已确定最短路的点集 S 与未确定的点集 T；每次从 T 中取出当前 dis 最小的点 u 加入 S，并用 u 松弛其所有出边。用优先队列（堆）实现时复杂度 O((V+E)log V)，朴素 O(V²)。它要求所有边权非负，否则贪心的『当前最小即确定』不再成立。是竞赛中最常用的单源最短路算法，也是分层图、Johnson 全源、最小费用流等的子程序。

## Why · 为什么

### 直觉 · Intuition

把地图想象成积水从源点向外扩散：水位（dis）最小的地方最先被淹没，因为所有边权非负，从别处绕道只会更晚到达。贪心保证『每次取出的最小 dis 就是最终最短路径』——比它小的路径若存在，必经过某个已确定点，但那早就把它松弛过了。堆则负责快速取出当前最小。

### 原理 · Principle

① 初始化 dis[s]=0，其余 +∞；② 从 T 中取 dis 最小的 u（堆顶）移入 S；③ 对 u 的每条出边 (u,v,w)：若 dis[v] > dis[u]+w 则松弛并压堆；④ 用 visited 标记已确定点，堆中过时条目（取出时已被标记）直接跳过。正确性由数学归纳法（OI Wiki 反证版）：设 u 为第一个加入 S 时 dis 错误（dis(u)>D(u)）的点，其真实最短路 s→x→y→u 中 y 是第一个仍属 T 的点，则 y 的 dis 已在 x 入 S 时被松弛为 D(y)，且由非负权 D(y)≤D(u)，推出 D(y)=D(u)，矛盾。关键不等式 D(y)≤D(u) 依赖非负权。

### 历史 · History

Dijkstra 于 1956 年一次喝咖啡休息时在纸上发明算法，1959 年发表于 Numerische Mathematik。同年与 Bellman-Ford、Floyd-Warshall 共同奠定了最短路径算法基础。现代实现标配二叉堆/优先队列（O((V+E)logV)），斐波那契堆可达 O(E+V log V)。CP-Algorithms 与 OI Wiki 均有标准实现与正确性证明。

## How · 实现

### 伪代码

```python
# 堆优化 Dijkstra (无负权边)
def dijkstra(adj, s):
  INF = inf
  dis = [INF]*n; dis[s]=0
  pq = [(0, s)]
  while pq:
    d, u = heappop(pq)
    if d > dis[u]: continue      # 过时条目
    for v, w in adj[u]:
      if dis[v] > d + w:
        dis[v] = d + w
        heappush(pq, (dis[v], v))
  return dis
```

### Python 实现

```python
import heapq
from collections import defaultdict


def dijkstra(adj, s, n):
    """堆优化 Dijkstra. adj: 邻接表 adj[u]=[(v,w),...]; s: 起点; n: 点数.
    返回 dis 列表 (0-indexed); 不可达为 float('inf')。要求边权非负。"""
    INF = float('inf')
    dis = [INF] * n
    dis[s] = 0
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dis[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dis[v]:
                dis[v] = nd
                heapq.heappush(pq, (nd, v))
    return dis


def dijkstra_path(adj, s, t, n):
    """额外重建路径: 返回 (dist, path); path 为从 s 到 t 的节点序列"""
    INF = float('inf')
    dis = [INF] * n
    pre = [-1] * n
    dis[s] = 0
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dis[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dis[v]:
                dis[v] = nd
                pre[v] = u
                heapq.heappush(pq, (nd, v))
    if dis[t] == INF:
        return INF, []
    path = []
    cur = t
    while cur != -1:
        path.append(cur)
        cur = pre[cur]
    path.reverse()
    return dis[t], path


if __name__ == "__main__":
    # 手动构造: 0-1(2),0-2(5),1-3(1),2-3(2),1-2(1)
    adj = defaultdict(list)
    adj[0] = [(1, 2), (2, 5)]
    adj[1] = [(3, 1), (2, 1)]
    adj[2] = [(3, 2)]
    adj[3] = []
    dis = dijkstra(adj, 0, 4)
    assert dis[0] == 0 and dis[1] == 2 and dis[2] == 3 and dis[3] == 3, dis
    d, p = dijkstra_path(adj, 0, 3, 4)
    assert d == 3 and p == [0, 1, 3], (d, p)

    # 与 Floyd 交叉验证 (随机图)
    import random
    random.seed(7)
    for _ in range(200):
        n = random.randint(1, 8)
        g = defaultdict(list)
        dmat = [[float('inf')] * n for _ in range(n)]
        for i in range(n):
            dmat[i][i] = 0
        for i in range(n):
            for j in range(n):
                if i != j and random.random() < 0.3:
                    w = random.randint(1, 9)
                    g[i].append((j, w))
                    dmat[i][j] = w
        s = random.randrange(n)
        dis = dijkstra(g, s, n)
        # Floyd
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    dmat[i][j] = min(dmat[i][j], dmat[i][k] + dmat[k][j])
        for i in range(n):
            a = dis[i]
            b = dmat[s][i]
            if a == float('inf'):
                assert b == float('inf'), (a, b)
            else:
                assert a == b, (a, b)
    print("All tests passed.")
```

**PyPy 提示**: 堆用 heapq（内置 C 实现）；邻接表用 list 而非 dict 更快（list of list）；优先队列里存 (dist, v) 无 compare 歧义。稠密图 (m~n²) 用朴素 O(n²) 反而更快且实现简单，PyPy 下两者皆可。注意 INF 用很大的整数（如 1<<60）比 float('inf') 更快且可避免 float 比较。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 堆优化 O((V+E) log V)；朴素 O(V²) |
| 空间 | O(V+E) 邻接表；堆最坏 O(E) |

### 局限

只适用非负权图——负权边会让『当前最小即确定』失效，需换 Bellman-Ford/SPFA 或 Johnson 预处理势能。稠密图中朴素实现更优。多条重边时堆中会积累过时条目，visited/比较检查需正确。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P4779 | 3 | 【模板】单源最短路径（标准版）：堆优化 Dijkstra 标准模板，n,m 达 2e5 | [https://www.luogu.com.cn/problem/P4779](https://www.luogu.com.cn/problem/P4779) |
| Luogu | P3371 | 2 | 【模板】单源最短路径（弱化版）：入门模板，n 较小 | [https://www.luogu.com.cn/problem/P3371](https://www.luogu.com.cn/problem/P3371) |
| Luogu | P1144 | 3 | 最短路计数：Dijkstra + 最短路径条数统计 | [https://www.luogu.com.cn/problem/P1144](https://www.luogu.com.cn/problem/P1144) |

## Pitfalls · 易错点

- 有负权边时结果错误且无提示——题面若未保证非负应改用 SPFA/Bellman-Ford
- 过时堆条目未检查 d > dis[u] 就继续松弛，导致重复处理/错误
- dis 用 float('inf') 时与 int 加法比较混合有隐患，建议统一大整数 INF
- 重边/自环需逐边松弛而非取 min 后建图（堆优化天然处理，但邻接表要都保留）
- 朴素实现每次 O(V) 找最小点，稠密图专用；堆优化在稀疏图才明显
- n 很大时 INF 要设 > 可能的最大路径和（如 n*maxw），用 1<<60 稳妥

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/shortest-path/](https://oi-wiki.org/graph/shortest-path/)
- CP-Algorithms ✓ [https://cp-algorithms.com/graph/dijkstra.html](https://cp-algorithms.com/graph/dijkstra.html)
- 书籍 ✓ `CPH ch13 pp133-142`
