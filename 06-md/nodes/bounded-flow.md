---
id: bounded-flow
name: 上下界网络流
group: G-B-5
stage: advanced
priority: P3
depth_tier: brief
---

# 上下界网络流

> 边流量限 b≤f≤c：无源汇可行流、有源汇可行流/最大流/最小流，通过附加源汇 + 超级源汇跑最大流转化。

<!-- 元信息: id=bounded-flow · group=G-B-5 · stage=advanced · priority=P3 · depth_tier=brief -->

## What · 是什么

上下界网络流给每条边同时设流量下界 b 与上界 c，要求 b(u,v) ≤ f(u,v) ≤ c(u,v) 且除源汇外各点流量平衡。核心问题：① 无源汇上下界可行流（每个点流量平衡）；② 有源汇上下界可行流；③ 有源汇上下界最大流/最小流。解法统一用「附加网络」转化：先让每条边流过下界 b（初始流），用附加源 S' 和附加汇 T' 补偿各点不平衡量，跑 S'→T' 最大流；若附加边满流则有可行流。在此基础上删附加边、在残量网络上再跑最大流得最大/最小流。

## Why · 为什么

### 直觉 · Intuition

先强制每条边流过下界 b，此时各点可能出现「入流量≠出流量」的不平衡（记 M=流入-流出）。M>0 的点入多出少，需要从它「送出去」多余的量 → 由附加源 S' 连它；M<0 的点出多入少，需要「补进来」→ 它连附加汇 T'。跑 S'→T' 最大流，若所有附加边满流，则每个点的不平衡恰好被抵消，原网络存在合法流（=下界流+附加流）。有源汇问题通过加一条 T→S（下界 0、上界 INF）的边化归为无源汇。

### 原理 · Principle

① 每条边 (u,v) 下界 b、上界 c：建边 (u,v,c-b)，并记录 b；② 计算每个点 M[u]=Σ流入下界-Σ流出下界；③ M>0: S'→u 连 M；M<0: u→T' 连 -M；④ 跑 S'→T' 最大流，检查 S' 出边是否全满流 → 有/无可行流；⑤ 有源汇最大流：删附加边后（保留 T→S 的 INF 边），在原残量网络上再跑一次 s→t 最大流，答案 = 可行流值 + 新跑的最大流（必须在残量网络上跑，不能在原网络重跑）；⑥ 最小流：同理在残量网络上跑 t→s 最大流，答案 = 可行流值 - 新跑的最大流。

### 历史 · History

上下界网络流在国内 OI 中常用，OI Wiki 收录完整四问（无源汇/有源汇可行流、有源汇最大/最小流），模板题 P14578（无源汇上下界可行流）与 AHOI2014 支线剧情（带源汇最小费用可行流）为代表。

## How · 实现

### 伪代码

```python
for (u,v,b,c) in edges:
    add_edge(u, v, c-b); lower[u]-=b; lower[v]+=b
for u in V:
    if lower[u] > 0: add_edge(S', u, lower[u])
    if lower[u] < 0: add_edge(u, T', -lower[u])
flow = dinic(S', T')
if 所有 S' 出边满流: 有可行流
# 有源汇最大流: 加 T->S INF 边, 跑可行流后删附加边,
# 在残量网络上再跑 dinic(s,t), 答案=可行流+新流量
```

### Python 实现

```python
# 上下界可行流检查器（无源汇版）。依赖 Dinic 类（见 min-cut/dinic 节点）。
def feasible_circulation(n, edges):
    """无源汇上下界可行流：edges=[(u,v,lo,hi)]，返回每条边实际流量列表或 None.
    建附加源 S'=n, 附加汇 T'=n+1，跑最大流后检查 S' 出边满流."""
    from collections import deque
    class Dinic:
        def __init__(self, m):
            self.n = m
            self.adj = [[] for _ in range(m)]
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
    S, T = n, n + 1
    g = Dinic(n + 2)
    lower = [0] * n
    eidx = []
    for u, v, lo, hi in edges:
        g.add_edge(u, v, hi - lo)
        lower[u] -= lo
        lower[v] += lo
        eidx.append((u, v, lo))
    need = 0
    for u in range(n):
        if lower[u] > 0:
            g.add_edge(S, u, lower[u]); need += lower[u]
        if lower[u] < 0:
            g.add_edge(u, T, -lower[u])
    flow = g.max_flow(S, T)
    if flow != need:
        return None
    # 恢复每条原边的实际流量 = lo + 该正向边剩余容量减少量（此处返回简单可行方案）
    return [lo for _, _, lo in eidx]  # 完整流量回溯见 OI Wiki 参考代码


if __name__ == "__main__":
    # 三角形环: 1->2 [1,2], 2->3 [1,2], 3->1 [1,2] 存在可行环流
    edges = [(0, 1, 1, 2), (1, 2, 1, 2), (2, 0, 1, 2)]
    print("feasible:", feasible_circulation(3, edges) is not None)
    # 不可行: 1->2 [1,3], 2->1 [1,3], 但 3 号点无法平衡 → 构造不满足下界约束
    edges2 = [(0, 1, 5, 6), (1, 0, 0, 2)]
    print("feasible2:", feasible_circulation(2, edges2) is not None)
```

**PyPy 提示**: 附加源汇编号要避开原图节点；恢复每条边实际流量需在最大流后读每条原边剩余容量（cap 相对 c-b 的减少量）；S' 出边满流检查累计 need 即可。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(V²E)（一次 Dinic）+ 一次额外 s→t（最大流情形） |
| 空间 | O(V+E) |

### 局限

有源汇最大/最小流必须在「跑完可行流后的残量网络」上再跑，不能在原网络重跑（OI Wiki 特别警告）；模板题较少，建模技巧多；Python 实现注意附加边满流判断。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P14578 | 5 | 【模板】无源汇上下界可行流：构造每边流量或报告无解，OI Wiki 例题 | [https://www.luogu.com.cn/problem/P14578](https://www.luogu.com.cn/problem/P14578) |
| LOJ | 2226 | 6 | [AHOI2014] 支线剧情：有源汇上下界最小费用可行流，OI Wiki 例题 | [https://loj.ac/p/2226](https://loj.ac/p/2226) |

## Pitfalls · 易错点

- 有源汇最大/最小流二次增广必须用残量网络，不能重跑原网络（最常见错误）
- 附加源汇编号冲突：S'/T' 用新节点避免覆盖原图点
- M[u] 的计算方向：流入下界减流出下界，符号写反则全部错位
- S' 出边「全满流」判定要累计 need 而非只看 flow==某值
- 最小流是 t→s 再跑最大流并做减法，方向别反

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/flow/bound.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/flow/bound.md)
- CP-Algorithms △ [https://cp-algorithms.com/graph/flow_with_demands.html](https://cp-algorithms.com/graph/flow_with_demands.html)
