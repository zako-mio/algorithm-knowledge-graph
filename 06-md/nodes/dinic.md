---
id: dinic
name: Dinic 最大流
group: G-B-5
stage: intermediate
priority: P1
depth_tier: standard
---

# Dinic 最大流

> BFS 分层图 + DFS 多路增广阻塞流 + 当前弧优化，O(V²E)；二分图匹配单位容量图 O(E√V)。

<!-- 元信息: id=dinic · group=G-B-5 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

Dinic 算法是目前竞赛中最主流的最大流算法。每轮：① 在残量网络上 BFS 分层（level[u]=s 到 u 的最短边数），只保留 level[v]=level[u]+1 的边构成层次图（有向无环）；② 在层次图上 DFS 求阻塞流（一种使得层次图上 s 到 t 不再有路径的流，可能由多条增广路组成，配合多路增广）；③ 合并入总流。层次图最短路在每轮严格增加，故至多 O(V) 轮；每轮阻塞流 O(VE)；总 O(V²E)。实际运行远快于理论上界。当前弧优化（cur[u] 指向下一条未尝试的边）是保证复杂度正确性的关键，多路增广是常数优化。单位容量图上 Dinic 达 O(E√V)。

## Why · 为什么

### 直觉 · Intuition

EK 每轮只沿一条最短增广路推流，太慢。Dinic 的思想是一轮内「把同一长度的所有最短路一次推完」：先 BFS 把节点按到 s 的距离分层，DFS 时只允许从第 k 层走到 k+1 层，这样不会绕圈、路径必然最短；多路增广让一次 DFS 返回时就沿多条岔路继续推；当前弧优化避免反复尝试已饱和/已阻塞的边。每推完一轮，s→t 的最短距离 +1，最多 V 层就结束了。

### 原理 · Principle

① 加边：成对存储，i 与 i^1 互为反向边，反向初始 cap=0；② BFS(s,t) 分层，若 t 不可达则算法结束；③ DFS(u,t,f) 沿 level 严格 +1 的边推流，返回实际推流量；多路增广写法 `for e in cur[u]: pushed=dfs(...); flow+=pushed` 允许一个节点多条出路；④ 当前弧：`cur[u]` 每轮复制 head，DFS 中前进过的饱和/阻塞边直接跳过；⑤ 每轮结束后 level[t] 增加，重复至不可达。单位容量/二分图：复杂度 O(E√V)（用最大流最小割 + 鸽巢证明）。

### 历史 · History

Yefim Dinitz 于 1970 年提出（比 Edmonds-Karp 更早但发表较晚），故也称 Dinitz 算法。由 e-maxx 译者与 OI Wiki 详细介绍；Dinitz 与 Edmonds 是同时代独立发现者。当前弧优化 + 多路增广的组合已成为竞赛标准写法。

## How · 实现

### 伪代码

```python
while BFS 分层(残量网络, s→t 可达):
    cur[u] = head[u] for all u     # 当前弧
    while True:
        pushed = DFS(s, t, INF)
        if pushed == 0: break
        flow += pushed
# DFS(u,t,f):
#   if u==t: return f
#   for i in cur[u]..:
#       v=to[i]; if cap[i]>0 and level[v]==level[u]+1:
#           d=DFS(v,t,min(f,cap[i]))
#           if d: cap[i]-=d; cap[i^1]+=d; return d
#       cur[u]前进
#   return 0
```

### Python 实现

```python
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

if __name__ == "__main__":
    # 经典图: s=0, t=3; 边 0->1(3) 0->2(3) 1->2(2) 1->3(3) 2->3(3); 最大流=6
    g = Dinic(4)
    g.add_edge(0, 1, 3); g.add_edge(0, 2, 3)
    g.add_edge(1, 2, 2); g.add_edge(1, 3, 3); g.add_edge(2, 3, 3)
    assert g.max_flow(0, 3) == 6
    # EK 交叉验证
    import random
    def ek_max_flow(n, edges, s, t):
        cap = {}
        def key(u, v): return (u, v)
        for u, v, c in edges:
            cap[key(u, v)] = cap.get(key(u, v), 0) + c
        flow = 0
        while True:
            parent = [-1] * n
            parent[s] = s
            q = deque([s])
            while q and parent[t] == -1:
                u = q.popleft()
                for v in range(n):
                    if parent[v] == -1 and cap.get(key(u, v), 0) > 0:
                        parent[v] = u
                        q.append(v)
            if parent[t] == -1:
                break
            # 找瓶颈
            f = 10 ** 18
            v = t
            while v != s:
                u = parent[v]
                f = min(f, cap[key(u, v)])
                v = u
            v = t
            while v != s:
                u = parent[v]
                cap[key(u, v)] -= f
                cap[key(v, u)] = cap.get(key(v, u), 0) + f
                v = u
            flow += f
        return flow

    random.seed(3)
    for _ in range(150):
        n = random.randint(2, 8)
        edges = []
        for u in range(n):
            for v in range(n):
                if u != v and random.random() < 0.25:
                    edges.append((u, v, random.randint(1, 8)))
        s = 0; t = n - 1
        g = Dinic(n)
        for u, v, c in edges:
            g.add_edge(u, v, c)
        got = g.max_flow(s, t)
        exp = ek_max_flow(n, edges, s, t)
        assert got == exp, (n, edges, got, exp)
    print("Dinic OK")

```

**PyPy 提示**: 邻接表用「边数组 + 索引」存储（Python 可用 list 存 [v, cap, rev] 或 [v, cap] 成对 + i^1）；DFS 递归深度可能达 n，需 sys.setrecursionlimit 或迭代；Python 在 n,m 达 1e5 时 Dinic 可能仍紧张（每轮 DFS 的 Python 层开销大），建议 PyPy 并尽量压缩递归/循环；图特别大时考虑 ISAP。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(V²E)；单位容量图 O(E√V)；二分图匹配 O(E√V) |
| 空间 | O(V+E) |

### 局限

Python 性能挑战大：n,m 达 1e5 的大图极易 TLE（递归 DFS + Python 层循环开销），需 PyPy + 常优化；Dinic 的 O(V²E) 上界在稠密图接近理论时很慢，但竞赛数据几乎不会命中。建图错误（漏反向边、重边、无向边处理）是最常见错因。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3376 | 3 | 【模板】网络最大流：Dinic 模板，OI Wiki 例题 | [https://www.luogu.com.cn/problem/P3376](https://www.luogu.com.cn/problem/P3376) |
| CSES | Download Speed | 3 | CSES 最大流模板 | [https://cses.fi/problemset/task/1694](https://cses.fi/problemset/task/1694) |
| Luogu | P2756 | 4 | 飞行员配对方案问题：二分图最大匹配转最大流，Dinic 单位容量 O(E√V) | [https://www.luogu.com.cn/problem/P2756](https://www.luogu.com.cn/problem/P2756) |

## Pitfalls · 易错点

- 当前弧优化是复杂度保证，不是可选的常数优化（OI Wiki 明确纠正「当前弧 vs 多路增广」的常见误区）
- BFS 必须从残量网络（cap>0 的边）分层，不能直接复用原图
- 递归 DFS 深栈：n 大时加 sys.setrecursionlimit(1<<20)，仍超则改迭代
- 反向边更新要用 cap[i^1] 配对称更新，写错一条就整体错
- 多路增广的 DFS 返回 0 时才停止，不要一遇到 d=0 就 break 整层

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/flow/max-flow.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/flow/max-flow.md)
- CP-Algorithms ✓ [https://cp-algorithms.com/graph/dinic.html](https://cp-algorithms.com/graph/dinic.html)
- 书籍 ✓ `CPH ch20 pp191-204`
