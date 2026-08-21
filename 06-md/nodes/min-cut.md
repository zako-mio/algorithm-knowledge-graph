---
id: min-cut
name: 最小割
group: G-B-5
stage: intermediate
priority: P1
depth_tier: standard
---

# 最小割

> s-t 割：把点分成 S（含 s）与 T（含 t），割容量 = S→T 边容量和；最大流最小割定理：s-t 最小割 = 最大流。

<!-- 元信息: id=min-cut · group=G-B-5 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

最小割（minimum s-t cut）：把网络点集划分为 S∪T=V、s∈S、t∈T，割容量 c(S,T)=Σ_{u∈S,v∈T} c(u,v)，求最小割容量。最大流最小割定理（Max-flow Min-cut Theorem）指出任意网络的最大流值 = s-t 最小割容量，且最小割的割集可由「残量网络中 s 可达的点集 S」直接读出（S 中所有跨到 T 的边即最小割边）。因此求最小割只需跑一次最大流，再对残量网络从 s DFS/BFS 标记可达点。

## Why · 为什么

### 直觉 · Intuition

任何 s→t 的流都必须穿过 s-t 割——割是「水流必须跨越的墙」。所以任意流的流量 ≤ 任意割的容量。反过来，最大流达到饱和时，残量网络里 s 到达不了 t，s 能到达的点构成一个割，这个割恰好把所有跨边灌满、反向跨边清空，于是流量=割容量，两边都最优。这就是对偶：最大化流量 = 最小化墙的厚度。

### 原理 · Principle

① 流-割不等式：对任意流 f 与割 (S,T)，|f| ≤ c(S,T)（跨 S→T 的流量受容量约束，且 T→S 流量抵消部分）；② 最大流最小割定理：存在流 f* 与割 (S*,T*) 使 |f*|=c(S*,T*)；③ 构造：跑完最大流后，S* = 残量网络中 s 可达的点集；④ 得到最小割边 = { (u,v)∈E : u∈S*, v∉S* }；⑤ 应用：二分图最大匹配（König 定理是特例）、二者选其一割模型、最大权闭合图（最大权值 = 正权总和 - 最小割）。

### 历史 · History

最大流最小割定理由 Ford 与 Fulkerson（1956）证明，与线性规划对偶理论紧密相关；König 定理（二分图最大匹配=最小点覆盖）是其特殊情形。最小割建模是网络流题的核心考察点之一，OI Wiki 收录两类经典模型（二者选其一、最大权闭合图）。

## How · 实现

### 伪代码

```python
# 1. 建图跑最大流（Dinic）
flow = dinic(s, t)
# 2. 求最小割点集 S*：从 s 在残量网络 DFS 标记可达
vis = [False]*n; vis[s]=True
stack=[s]
while stack:
    u=stack.pop()
    for e in adj[u]:
        if not vis[e.v] and e.cap>0:
            vis[e.v]=True; stack.append(e.v)
# 3. 最小割容量 = flow; 割边 = 所有 (u,v) 满足 vis[u] and not vis[v]
```

### Python 实现

```python
# 最小割 = 最大流 + 残量网络可达性标记。以下依赖 dinic 节点的 Dinic 类。
from collections import deque

class Dinic:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n)]
    def add_edge(self, u, v, cap):
        self.adj[u].append([v, cap, len(self.adj[v])])
        self.adj[v].append([u, 0, len(self.adj[u]) - 1])
    def _bfs(self, s, t):
        self.level = [-1] * self.n
        self.level[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v, cap, rev in self.adj[u]:
                if cap > 0 and self.level[v] < 0:
                    self.level[v] = self.level[u] + 1
                    q.append(v)
        return self.level[t] >= 0
    def _dfs(self, u, t, f):
        if u == t:
            return f
        while self.it[u] < len(self.adj[u]):
            e = self.adj[u][self.it[u]]
            v, cap, rev = e
            if cap > 0 and self.level[v] == self.level[u] + 1:
                pushed = self._dfs(v, t, min(f, cap))
                if pushed:
                    e[1] -= pushed
                    self.adj[v][rev][1] += pushed
                    return pushed
            self.it[u] += 1
        return 0
    def max_flow(self, s, t):
        flow = 0
        INF = 10 ** 18
        while self._bfs(s, t):
            self.it = [0] * self.n
            while True:
                pushed = self._dfs(s, t, INF)
                if not pushed:
                    break
                flow += pushed
        return flow
    def min_cut_set(self, s):
        """返回残量网络中 s 可达的点集（最小割 S* 侧）."""
        vis = [False] * self.n
        vis[s] = True
        stack = [s]
        while stack:
            u = stack.pop()
            for v, cap, rev in self.adj[u]:
                if cap > 0 and not vis[v]:
                    vis[v] = True
                    stack.append(v)
        return vis


if __name__ == "__main__":
    # 图: s=0,t=3; 0->1(3) 0->2(3) 1->2(2) 1->3(3) 2->3(3); 最大流=最小割=6
    g = Dinic(4)
    g.add_edge(0, 1, 3); g.add_edge(0, 2, 3)
    g.add_edge(1, 2, 2); g.add_edge(1, 3, 3); g.add_edge(2, 3, 3)
    flow = g.max_flow(0, 3)
    S = g.min_cut_set(0)
    # 割边 = u in S, v not in S
    cut_edges = []
    for u in range(4):
        for v, cap, rev in g.adj[u]:
            if S[u] and not S[v]:
                cut_edges.append((u, v))
    print("maxflow =", flow)
    print("S =", [i for i in range(4) if S[i]])
    print("cut_edges =", cut_edges)
    assert flow == 6
```

**PyPy 提示**: 求最小割点集只需一次 DFS（残量网络 cap>0 的边），O(V+E)；割边枚举遍历邻接表即可。跑最大流部分复用 Dinic。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(V²E)（最大流，Dinic）；求点集 O(V+E) |
| 空间 | O(V+E) |

### 局限

Python 大图 TLE 同 dinic 节点；求「最小割前提下边数最少」需二次建图（满流边权 1、非满流 INF 再跑一遍）；无向边割建模需按题意转换。二分图/闭合图建模是重点，别只求流而忘建图。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1344 | 5 | [USACO4.4] Pollutant Control：最小割 + 最小割边数，OI Wiki 习题 | [https://www.luogu.com.cn/problem/P1344](https://www.luogu.com.cn/problem/P1344) |
| Luogu | P2057 | 5 | [SHOI2007] 善意的投票：二者选其一最小割建模，OI Wiki 习题 | [https://www.luogu.com.cn/problem/P2057](https://www.luogu.com.cn/problem/P2057) |
| Luogu | P1361 | 5 | 小 M 的作物：二者选其一 + 组合收益割模型，OI Wiki 习题 | [https://www.luogu.com.cn/problem/P1361](https://www.luogu.com.cn/problem/P1361) |
| Luogu | P1345 | 4 | [USACO5.4] Telecowmunication：点割（拆点转边割），OI Wiki 习题 | [https://www.luogu.com.cn/problem/P1345](https://www.luogu.com.cn/problem/P1345) |

## Pitfalls · 易错点

- 最大流跑完后直接读 flow 作为最小割容量即可，但求割边集必须用残量网络可达性，不能想当然
- 「最小割前提下割边最少」需二次建图重跑，不要直接数满流边
- 二者选其一建模：连 s 边权 a_i、t 边权 b_i、u-v 双向 w，注意方向与割语义
- 最大权闭合图：正权连 s、负权连 t、原图边权 INF，答案是正权和-最小割
- 拆点（点割）时：每个点拆成入点→出点容量 1，原边容量 INF

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/flow/min-cut.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/flow/min-cut.md)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/flow/max-flow.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/flow/max-flow.md)
- 书籍 ✓ `CPH ch20 pp191-204`
