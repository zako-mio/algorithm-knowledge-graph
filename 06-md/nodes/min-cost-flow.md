---
id: min-cost-flow
name: 最小费用最大流（SSP）
group: G-B-5
stage: advanced
priority: P2
depth_tier: standard
---

# 最小费用最大流（SSP）

> SSP（Successive Shortest Path）：每次沿单位费用最短的增广路增广，SPFA/Bellman-Ford 或势能+Dijkstra 找路。

<!-- 元信息: id=min-cost-flow · group=G-B-5 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

最小费用最大流（minimum-cost maximum-flow）：在每条边有容量 c 和单位流量费用 w 的网络中，先最大化总流量，再在该前提下最小化总费用 Σf·w。SSP（Successive Shortest Path，连续最短路）算法是竞赛主流做法：反复用最短路算法在残量网络中找「单位费用和最小」的 s→t 增广路并增广，直到无增广路。费用有负数时用 SPFA/Bellman-Ford 找路；费用非负或已用势能（Johnson 技巧）转非负后用 Dijkstra 加速。

## Why · 为什么

### 直觉 · Intuition

贪心思路：每次选「单位流量最便宜」的一条路先灌，就像先走低价路线。为什么全局最优？用归纳法证明：若当前流 f_i 已是流量 i 的最小费用流，则沿最短路增广得到 f_{i+1} 也是最小费用流——否则存在更优的 f'_{i+1}，其相对于 f_i 的增广差异必含一个负费用圈，而负圈意味着 f_i 还能降费，矛盾。前提：原图无负费用圈（否则需先消圈）。

### 原理 · Principle

① 建图：每条边加反向边，容量 0、费用 -w（退流时费用回退）；② 每次找 s→t 的最短（单位费用和最小）增广路：负边存在则 SPFA，否则（或势能化后）Dijkstra；③ 沿路推流：瓶颈 Δ，正向 cap-=Δ、反向 cap+=Δ，maxflow+=Δ，mincost+=Δ*最短路长；④ 重复到无路。势能（Primal-Dual）：初始跑一次最短路得 h[u]（负权也兼容），此后每条边权改为 w+h[u]-h[v] 保证非负，用 Dijkstra，增广后 h[u]+=dist[u] 更新，保持非负。

### 历史 · History

SSP 思想源自 Ford-Fulkerson 族的推广，国内 OI 习惯称 SSP 并用 SPFA 版（支持负费用边）；Dijkstra 版借助势能（Johnson 全源最短路思想，源自 Johnson 1977）。OI Wiki 与 CP-Algorithms 均有 SSP 与原始对偶的完整介绍；消圈算法处理负圈是理论补充。

## How · 实现

### 伪代码

```python
add_edge(u,v,cap,cost): 正向 [cap,cost], 反向 [0,-cost]
while True:
    dist,pre = SPFA(s,t)   # 或势能+Dijkstra
    if t 不可达: break
    Δ = 沿路最小剩余容量
    沿路正向 cap-=Δ, 反向 cap+=Δ
    maxflow += Δ; mincost += Δ * dist[t]
```

### Python 实现

```python
from collections import deque

class MCMF:
    """最小费用最大流（SSP + SPFA，支持负费用边）."""
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n)]

    def add_edge(self, u, v, cap, cost):
        self.adj[u].append([v, cap, cost, len(self.adj[v])])
        self.adj[v].append([u, 0, -cost, len(self.adj[u]) - 1])

    def _spfa(self, s, t):
        INF = 10 ** 18
        dist = [INF] * self.n
        inq = [False] * self.n
        pre_v = [-1] * self.n
        pre_e = [-1] * self.n
        dist[s] = 0
        q = deque([s])
        inq[s] = True
        while q:
            u = q.popleft()
            inq[u] = False
            for i, e in enumerate(self.adj[u]):
                v, cap, cost, rev = e
                if cap > 0 and dist[v] > dist[u] + cost:
                    dist[v] = dist[u] + cost
                    pre_v[v] = u
                    pre_e[v] = i
                    if not inq[v]:
                        q.append(v)
                        inq[v] = True
        return dist[t] != INF, dist[t], pre_v, pre_e

    def min_cost_flow(self, s, t):
        flow, cost = 0, 0
        INF = 10 ** 18
        while True:
            ok, d, pre_v, pre_e = self._spfa(s, t)
            if not ok:
                break
            # 找增广路瓶颈
            add = INF
            v = t
            while v != s:
                u = pre_v[v]
                e = self.adj[u][pre_e[v]]
                add = min(add, e[1])
                v = u
            v = t
            while v != s:
                u = pre_v[v]
                e = self.adj[u][pre_e[v]]
                e[1] -= add
                self.adj[v][e[3]][1] += add
                v = u
            flow += add
            cost += add * d
        return flow, cost

if __name__ == "__main__":
    # 简单网络: 0->1(2,1) 0->2(1,2) 1->2(1,1) 1->3(1,3) 2->3(2,1), s=0,t=3
    m = MCMF(4)
    m.add_edge(0, 1, 2, 1); m.add_edge(0, 2, 1, 2)
    m.add_edge(1, 2, 1, 1); m.add_edge(1, 3, 1, 3); m.add_edge(2, 3, 2, 1)
    fl, co = m.min_cost_flow(0, 3)
    assert fl == 3, fl
    assert co == 10, co  # 流3: 0->1->3(4)+0->1->2->3(3)+0->2->3(3)=10
    print("MCMF basic flow=%d cost=%d" % (fl, co))
    # 用暴力枚举验证小图
    import random, itertools
    random.seed(5)
    for _ in range(120):
        n = random.randint(2, 6)
        edges = []
        for u in range(n):
            for v in range(n):
                if u != v and random.random() < 0.3:
                    edges.append((u, v, random.randint(1, 5), random.randint(0, 5)))
        s = 0; t = n - 1
        m = MCMF(n)
        for u, v, c, w in edges:
            m.add_edge(u, v, c, w)
        fl, co = m.min_cost_flow(s, t)
        # 暴力: 枚举所有流（小图, 容量小）
        def brute(u, cap_left, cost_acc):
            if u == t:
                return (0, cost_acc, cap_left)
            best = None
            # 简化: 只验证最大流值（费用需完整 SSP, 这里不暴力比对费用）
            return None
        # 最大流值用 EK 对照
        def ek(n, edges, s, t):
            cap = {}
            def k(a, b): return (a, b)
            for u, v, c, w in edges:
                cap[k(u, v)] = cap.get(k(u, v), 0) + c
            flow = 0
            while True:
                parent = [-1] * n; parent[s] = s
                q = deque([s])
                while q and parent[t] == -1:
                    u = q.popleft()
                    for v in range(n):
                        if parent[v] == -1 and cap.get(k(u, v), 0) > 0:
                            parent[v] = u; q.append(v)
                if parent[t] == -1: break
                f = 10 ** 18; v = t
                while v != s:
                    u = parent[v]; f = min(f, cap[k(u, v)]); v = u
                v = t
                while v != s:
                    u = parent[v]; cap[k(u, v)] -= f; cap[k(v, u)] = cap.get(k(v, u), 0) + f; v = u
                flow += f
            return flow
        exp_fl = ek(n, edges, s, t)
        assert fl == exp_fl, (n, edges, fl, exp_fl)
    print("MCMF flow-crosscheck OK")

```

**PyPy 提示**: SPFA 版能处理负费用边；若确认费用非负用势能+Dijkstra（heapq）更快。SPFA 在竞赛毒瘤数据可能退化，费用全部非负时优先 Dijkstra。Python 中邻接表用 [v, cap, cost, rev] 四元组 list 存储。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(F·V·E)（SPFA 版，F=流量，伪多项式）；势能+Dijkstra O(F·(E+V log V)) |
| 空间 | O(V+E) |

### 局限

SSP 是伪多项式时间：流量 F 巨大时（如 2^(n/2) 构造）会超时，但竞赛数据一般可控；存在负费用圈时 SSP 不保证正确（需先消圈，竞赛很少遇到）；Python 下 F 大（如 1e5 流量）时每次最短路 + 增广开销累积，极易 TLE，需 PyPy + 优化。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3381 | 4 | 【模板】最小费用最大流：SSP 模板，OI Wiki 例题 | [https://www.luogu.com.cn/problem/P3381](https://www.luogu.com.cn/problem/P3381) |
| Luogu | P4015 | 4 | 运输问题：二分图最小/最大费用流，网络流 24 题 | [https://www.luogu.com.cn/problem/P4015](https://www.luogu.com.cn/problem/P4015) |
| Luogu | P2053 | 5 | [SCOI2007] 修车：费用流建模（拆时间点），OI Wiki 习题 | [https://www.luogu.com.cn/problem/P2053](https://www.luogu.com.cn/problem/P2053) |
| Luogu | P2517 | 5 | [HAOI2010] 订货：费用流建模，OI Wiki 习题 | [https://www.luogu.com.cn/problem/P2517](https://www.luogu.com.cn/problem/P2517) |

## Pitfalls · 易错点

- 反向边费用必须是 -w，不是 0，否则退流退不回费用
- 有负费用边时不能用裸 Dijkstra，需 SPFA 或先跑一次最短路做势能
- 存在负费用圈时 SSP 不保证正确（先消圈）
- 每次最短路后更新势能 h[u]+=dist[u]（Primal-Dual），否则势能失效
- Python 大流量时注意 F 次增广的总代价，必要时用容量缩放

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/flow/min-cost.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/flow/min-cost.md)
- CP-Algorithms ✓ [https://cp-algorithms.com/graph/min_cost_flow.html](https://cp-algorithms.com/graph/min_cost_flow.html)
- 书籍 ✓ `CPH ch20 pp191-204`
