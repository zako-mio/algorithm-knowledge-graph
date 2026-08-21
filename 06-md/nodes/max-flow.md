---
id: max-flow
name: 最大流（Ford-Fulkerson / Edmonds-Karp）
group: G-B-5
stage: intermediate
priority: P1
depth_tier: standard
---

# 最大流（Ford-Fulkerson / Edmonds-Karp）

> Ford-Fulkerson 增广路思想：残量网络 + 反向边退流；EK 用 BFS 找最短增广路 O(VE²)。

<!-- 元信息: id=max-flow · group=G-B-5 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

最大流问题：给定有源汇的网络 G=(V,E)（每条边有容量 c），找流 f 使从源 s 流出的总流量最大，且满足容量限制（0≤f≤c）与除源汇外各点流守恒。Ford-Fulkerson 增广法是一类算法的总称：反复在残量网络中找增广路（s 到 t 的可行路径），沿路推流；残量网络包含正向剩余容量 c-f 与反向边 f（用于退流/反悔）。Edmonds-Karp 是 FF 的 BFS 实现，保证每次找最短增广路，复杂度 O(VE²)。

## Why · 为什么

### 直觉 · Intuition

把网络想象成水管：容量是管径，流量是水流。贪心沿一条从 s 到 t 的路径灌水会「堵死」更优的路径，所以引入反向边：水流可以被退回重走。残量网络中正向边 = 还能灌多少，反向边 = 能退回多少。只要残量网络里还有 s→t 的路径就能继续增广，找不到路径时流量即最大（增广终止定理）。

### 原理 · Principle

① 建图：每条边加一条反向边（cap 0），用 i^1 快速互访；② 循环：BFS/DFS 在残量网络中找 s→t 增广路，记瓶颈 Δ=min 剩余容量，路径每条边 cap-=Δ，反向边 cap+=Δ；③ 直到残量网络无 s→t 路。EK 用 BFS 保证增广路最短，增广轮数 O(VE)（最短路非递减引理），每轮 O(E)，总 O(VE²)。正确性由最大流最小割定理保证：增广停止时，s 可达点集 S 构成的最小割容量等于流量。

### 历史 · History

Ford-Fulkerson 法由 Lester Ford 和 Delbert Fulkerson 于 1956 年提出；Edmonds 和 Karp 于 1972 年给出 BFS 实现并证明多项式复杂度 O(VE²)。Dinic（Yefim Dinitz，1970）进一步用分层图 + 阻塞流做到 O(V²E)，实际性能远优于理论上界。

## How · 实现

### 伪代码

```python
edges = []  # [to, cap] 成对存储, i^1 互为反向
add_edge(u,v,c): edges[u]+=(v,c); edges[v]+=(u,0)
while BFS 能找到 s→t 增广路:
    Δ = min(沿路剩余容量)
    沿路正向 cap-=Δ, 反向 cap+=Δ
    flow += Δ
return flow
```

### Python 实现

```python
# 最大流模板见 dinic 节点（含完整实现）。此处给出 Edmonds-Karp 参考实现。
from collections import deque


def edmonds_karp(n, adj, cap, s, t):
    """EK 最大流. adj: 邻接表[[(v, edge_idx)]], cap 用 dict 或 list 均可.
    这里用简单的 dict 版方便理解：cap[(u,v)] 为剩余容量.
    复杂度 O(V E^2)."""
    cap = {k: v for k, v in cap.items()}
    flow = 0
    INF = 10 ** 18
    while True:
        pre = [-1] * n
        pre[s] = s
        q = deque([s])
        while q and pre[t] == -1:
            u = q.popleft()
            for v in adj[u]:
                if pre[v] == -1 and cap.get((u, v), 0) > 0:
                    pre[v] = u
                    q.append(v)
        if pre[t] == -1:
            break
        # 找瓶颈
        add = INF
        v = t
        while v != s:
            u = pre[v]
            add = min(add, cap[(u, v)])
            v = u
        # 增广
        v = t
        while v != s:
            u = pre[v]
            cap[(u, v)] -= add
            cap[(v, u)] = cap.get((v, u), 0) + add
            v = u
        flow += add
    return flow


if __name__ == "__main__":
    # 0->1(3) 0->2(3) 1->2(2) 1->3(3) 2->3(3), s=0,t=3, 最大流=6
    n = 4
    adj = [[1, 2], [0, 2, 3], [0, 1, 3], [1, 2]]
    cap = {(0, 1): 3, (0, 2): 3, (1, 2): 2, (1, 3): 3, (2, 3): 3}
    print("EK flow =", edmonds_karp(n, adj, cap, 0, 3))
```

**PyPy 提示**: EK 的 dict 版便于理解但常数大；竞赛实现用「邻接表 + 边数组成对存储 + i^1 反向」更优。EK 只适用于小图（VE² 限制），n,m ≥ 2000 时建议直接上 Dinic。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(VE²)（EK）；FF 一般 O(E·\|f\|)（可能指数级，需整数容量且不保证终止） |
| 空间 | O(V+E) |

### 局限

FF 若用 DFS 且容量为实数，可能不终止（甚至无限）；EK 的 BFS 保证多项式。Python 下 VE² 在图稍大时即超时，实际竞赛中最大流几乎都用 Dinic（见 dinic 节点）。无向边需拆成两条有向边。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3376 | 3 | 【模板】网络最大流：EK/Dinic 模板题 | [https://www.luogu.com.cn/problem/P3376](https://www.luogu.com.cn/problem/P3376) |
| Luogu | P2740 | 3 | [USACO4.2] 草地排水 Drainage Ditches：经典最大流模板 | [https://www.luogu.com.cn/problem/P2740](https://www.luogu.com.cn/problem/P2740) |
| CSES | Download Speed | 3 | CSES 最大流模板，Dinic 可过 | [https://cses.fi/problemset/task/1694](https://cses.fi/problemset/task/1694) |

## Pitfalls · 易错点

- 忘记加反向边（或反向边容量设错）导致无法退流，结果偏小
- 重边处理：同 u→v 多边应合并容量或分开存但都参与增广
- 容量很大时 Python int 无需担心溢出，但 INF 要设足够大
- 无向图：add_edge(u,v,c) 后还要 add_edge(v,u,c)，或者反向边初始容量设为 c（视题意）
- EK/FF 的 DFS 实现若无访问标记会死循环；BFS 版更稳

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/flow/max-flow.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/flow/max-flow.md)
- CP-Algorithms ✓ [https://cp-algorithms.com/graph/edmonds_karp.html](https://cp-algorithms.com/graph/edmonds_karp.html)
- 书籍 ✓ `CPH ch20 pp191-204`
