---
id: dag-dp
name: 差分约束 / DAG 最短路 DP
group: G-B-9
stage: intermediate
priority: P1
depth_tier: standard
---

# 差分约束 / DAG 最短路 DP

> 差分约束系统建图+最短路判负环；DAG 上按拓扑序 DP 求最长/最短路

<!-- 元信息: id=dag-dp · group=G-B-9 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

本节点包含两个紧密相关的话题：(1) 差分约束系统：一组形如 x_i - x_j ≤ c 的约束，等价于在图上连边 (j→i, 权 c)，求一组解等价于求单源最短路；若存在负环则无解。可用 Bellman-Ford/SPFA 判负环 O(nm)，或对无负环情形用最短路给出解。(2) DAG 最短路/最长路 DP：在无环图上用拓扑序（或记忆化搜索）在 O(n+m) 内求单源最长/最短路径，是图论 DP 的基础模型（见 OI Wiki dag.md 与 dp/dag）。二者都体现『把不等式/依赖关系编码成图，用图算法求解』的核心思想。

## Why · 为什么

### 直觉 · Intuition

差分约束的每条 x_i - x_j ≤ c 变形为 x_i ≤ x_j + c，恰与最短路三角形不等式 dist[y] ≤ dist[x] + z 同构——把 j 到 i 连边权 c 的边，跑最短路后 dist 就是一组解；负环意味着存在 x_i < x_i 的矛盾。DAG 上无环则依赖关系是偏序，拓扑序保证每个状态被处理前其前驱全部就绪，所以 O(n+m) 即可递推。

### 原理 · Principle

差分约束：设 dist[0]=0 并加 0 边到所有点，跑 SPFA/Bellman-Ford。若出现负环 → 无解；否则 x_i = dist[i] 为合法解。约束翻转：x_a - x_b ≥ c → 连 (a→b, -c)；x_a = x_b → (a→b,0) 与 (b→a,0)；比值约束取 log 变加法。DAG DP：拓扑排序后按序松弛 dist[v]=min/max(dist[v], dist[u]+w)。最长路等价于关键路径（CPM）。

### 历史 · History

差分约束系统在调度与规划领域历史悠久（最早可追溯至 Bellman 与 Ford 的最短路视角），是『约束满足→最短路』的经典建模；OI Wiki diff-constraints 章节用洛谷 P1993 小K的农场、P4926 倍杀测量者为例。DAG 上 DP 是最自然的 DP 模型，CPH ch16 与 OI Wiki dp/dag 均有专题。

## How · 实现

### 伪代码

```python
# 差分约束: 求可行解或判无解
add(0 -> i, 0) 对所有 i
add(j -> i, c) 对每个 x_i - x_j <= c
跑 Bellman-Ford:
  若第 n 轮仍能松弛 -> 有负环, 无解
  否则 x_i = dist[i]

# DAG 最长路 (拓扑序递推)
topo = 拓扑排序结果
dist[s] = 0
for u in topo:
  for (v, w) in adj[u]:
    dist[v] = max(dist[v], dist[u] + w)
```

### Python 实现

```python
from collections import deque, defaultdict

INF = 10 ** 18


def dag_longest_path(n, edges):
    """DAG 最长路（从任意点出发的最大路径长度）。
    n: 节点数; edges: [(u, v)] 有向边, 边权默认 1。返回最长路长度。
    """
    adj = defaultdict(list)
    indeg = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1
    q = deque(u for u in range(n) if indeg[u] == 0)
    dist = [0] * n
    while q:
        u = q.popleft()
        for v in adj[u]:
            dist[v] = max(dist[v], dist[u] + 1)
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return max(dist)


def diff_constraints_solve(n, cons):
    """差分约束: 判断是否有解并返回一组解。
    cons: [(i, j, c)] 表示 x_i - x_j <= c (1-indexed 变量)。
    返回 (True, [x_1..x_n]) 或 (False, []) 无解。
    """
    m = n + 1  # 0 为超级源
    adj = defaultdict(list)
    for i in range(1, n + 1):
        adj[0].append((i, 0))            # dist[i] <= dist[0] + 0
    for i, j, c in cons:
        adj[j].append((i, c))            # x_i - x_j <= c -> x_i <= x_j + c
    # SPFA 判负环
    dist = [INF] * m
    dist[0] = 0
    inq = [False] * m
    cnt = [0] * m
    q = deque([0])
    inq[0] = True
    while q:
        u = q.popleft()
        inq[u] = False
        for v, w in adj[u]:
            if dist[v] > dist[u] + w:
                dist[v] = dist[u] + w
                cnt[v] = cnt[u] + 1
                if cnt[v] > n:          # 入队超过 n 次 -> 负环
                    return False, []
                if not inq[v]:
                    q.append(v)
                    inq[v] = True
    return True, [dist[i] for i in range(1, n + 1)]


def dag_longest_naive(n, edges):
    """朴素 O(V·(V+E)) 对拍。"""
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
    best = 0
    from functools import lru_cache

    @lru_cache(None)
    def dfs(u):
        m = 0
        for v in adj[u]:
            m = max(m, dfs(v) + 1)
        return m

    return max((dfs(u) for u in range(n)), default=0)


if __name__ == "__main__":
    # DAG 最长路
    edges = [(0, 1), (1, 2), (0, 2), (2, 3), (1, 3)]
    assert dag_longest_path(4, edges) == dag_longest_naive(4, edges) == 3
    assert dag_longest_path(1, []) == 0

    # 差分约束: x2 - x1 <= 3, x1 <= 4 => x1=4, x2=7 可行
    ok, sol = diff_constraints_solve(2, [(2, 1, 3), (1, 0, 4)])
    assert ok
    # 校验约束
    assert sol[1] - sol[0] <= 3 + 1e-9
    assert sol[0] <= 4 + 1e-9

    # 无解: x1 - x2 <= -5, x2 - x1 <= -5 => x1 < x2 且 x2 < x1
    ok2, _ = diff_constraints_solve(2, [(1, 2, -5), (2, 1, -5)])
    assert not ok2
    print("dag-dp 自测通过：DAG最长路(拓扑/记忆化)与差分约束(有解/无解)均正确")

```

**PyPy 提示**: SPFA 判负环在随机图上快，最坏 O(nm)；DAG DP 用 deque 拓扑排序 O(n+m)。Python 递归记忆化需 setrecursionlimit；差分约束若已知图为 DAG 可用拓扑序 O(n+m) 替代 SPFA。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | DAG DP: O(n+m)；差分约束 Bellman-Ford/SPFA: O(nm)（最坏） |
| 空间 | O(n+m) |

### 局限

差分约束若隐含环且环和为正仍可能有解（只是最短路法以 dist 解可能不最小），判无解需确认为负环；SPFA 在最坏图上会退化。DAG DP 前提是无环，有环需先 SCC 缩点。非连通/多源场景需超级源或对每个源分别跑。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1993 | 4 | 小K的农场：差分约束建图+判负环模板题（OI Wiki 例题） | [https://www.luogu.com.cn/problem/P1993](https://www.luogu.com.cn/problem/P1993) |
| AtCoder | dp_g | 3 | Longest Path：DAG 上按拓扑序求最长路（EDPC 例题） | [https://atcoder.jp/contests/dp/tasks/dp_g](https://atcoder.jp/contests/dp/tasks/dp_g) |
| Luogu | P1137 | 3 | 旅行计划：DAG 最长路拓扑序递推 | [https://www.luogu.com.cn/problem/P1137](https://www.luogu.com.cn/problem/P1137) |
| Luogu | P4017 | 3 | 最大食物链计数：DAG 上 DP 计数 | [https://www.luogu.com.cn/problem/P4017](https://www.luogu.com.cn/problem/P4017) |

## Pitfalls · 易错点

- 差分约束连边方向反了（x_i - x_j ≤ c 是 j→i 不是 i→j）
- ≥ 约束需翻转取负；= 约束拆两条
- SPFA 判负环的入队计数初值（cnt[v]=cnt[u]+1 而非 ++cnt[v]）
- DAG DP 忘记拓扑排序直接乱序会得到错误依赖
- 多源最长路要对所有源初始化 dist=0；单源要设 dist[s]=0, 其余 -INF

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/diff-constraints/](https://oi-wiki.org/graph/diff-constraints/)
- OI Wiki ✓ [https://oi-wiki.org/graph/dag/](https://oi-wiki.org/graph/dag/)
- OI Wiki ✓ [https://oi-wiki.org/dp/dag/](https://oi-wiki.org/dp/dag/)
- 书籍 ✓ `CPH ch16 pp159-166`
