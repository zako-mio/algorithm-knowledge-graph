---
id: bellman-ford
name: Bellman-Ford算法
group: G-B-2
stage: intermediate
priority: P1
depth_tier: standard
---

# Bellman-Ford算法

> 含负权单源最短路，松弛操作O(VE)，可判负环

<!-- 元信息: id=bellman-ford · group=G-B-2 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

Bellman-Ford 算法求解含负权边的单源最短路，并对『从源可达的负环』给出检测。核心是 n-1 轮全边松弛：每轮对所有边 (u,v,w) 尝试 dis[v] = min(dis[v], dis[u]+w)，第 n 轮仍能松弛说明存在可达负环。时间复杂度 O(VE)。它是 Dijkstra（只能非负权）无法覆盖场景的兜底算法，也是 SPFA、差分约束、Johnson 求势能的子程序。

## Why · 为什么

### 直觉 · Intuition

一条最短路径若存在，其简单路径至多含 n-1 条边（无负环）。第 i 轮松弛保证所有『恰用 ≤i 条边可达』的最短路被算出：因为第 i 条边只有在第 i 轮才会被考虑进路径。类似把信息沿边逐层广播 n-1 轮。若第 n 轮还能松弛，说明存在长度持续变小的环（负环），最短路无界。

### 原理 · Principle

① 初始化 dis[s]=0，其余 +∞；② 重复 n-1 次：对每条边 (u,v,w) 若 dis[u]+w<dis[v] 则松弛；③ 若某轮无任何松弛可提前终止；④ 再做第 n 轮，若仍松弛则 s 可达负环；⑤ 从 s 出发的判定局限：只有 s 能到达的负环会被发现，全图负环需加超级源点连 0 权边。

### 历史 · History

算法由 Richard Bellman (1958) 与 Lester Ford (1956) 独立提出，故得名；Lester Ford 1962 发表。它是动态规划思想用于最短路的最早范例，也是差分约束系统（转化为最短路）的理论基础。OI Wiki 与 CP-Algorithms 均有完整实现与负环判定讨论。

## How · 实现

### 伪代码

```python
def bellman_ford(n, edges, s):
  dis[s]=0; 其余 INF
  for i in range(n):
    updated = False
    for (u,v,w) in edges:
      if dis[u]!=INF and dis[u]+w < dis[v]:
        dis[v] = dis[u]+w; updated=True
    if not updated: break
  # 第 n 轮检测负环
  for (u,v,w) in edges:
    if dis[u]!=INF and dis[u]+w < dis[v]:
      return 's 可达负环'
  return dis
```

### Python 实现

```python
def bellman_ford(n, edges, s):
    """含负权单源最短路 + 负环检测.
    n: 点数; edges: [(u,v,w)]; s: 起点 (0-indexed).
    返回 (ok, dis); ok=False 表示 s 可达负环, dis 无效."""
    INF = float('inf')
    dis = [INF] * n
    dis[s] = 0
    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dis[u] != INF and dis[u] + w < dis[v]:
                dis[v] = dis[u] + w
                updated = True
        if not updated:
            break
    for u, v, w in edges:
        if dis[u] != INF and dis[u] + w < dis[v]:
            return False, dis
    return True, dis


def has_negative_cycle_global(n, edges):
    """全图负环检测: 加超级源点连 0 权边, 跑 Bellman-Ford"""
    super_edges = edges + [(n, i, 0) for i in range(n)]
    ok, _ = bellman_ford(n + 1, super_edges, n)
    return not ok


if __name__ == "__main__":
    # 标准用例
    edges = [(0, 1, 6), (0, 2, 7), (1, 2, 8), (1, 3, 5), (1, 4, -4), (2, 3, -3), (2, 4, 9), (3, 1, -2), (4, 0, 2), (4, 3, 7)]
    ok, dis = bellman_ford(5, edges, 0)
    assert ok and dis == [0, 2, 7, 4, -2], dis

    # 负环 (0 可达): 0->1(1),1->2(-3),2->0(1) 总 -1
    neg = [(0, 1, 1), (1, 2, -3), (2, 0, 1)]
    ok, _ = bellman_ford(3, neg, 0)
    assert ok is False
    # 无负环
    no_neg = [(0, 1, 1), (1, 2, -3), (2, 0, 5)]
    ok, dis = bellman_ford(3, no_neg, 0)
    assert ok and dis == [0, 1, -2], dis

    # 与 SPFA 交叉验证
    def spfa(n, edges, s):
        from collections import deque
        INF = float('inf')
        dis = [INF] * n
        cnt = [0] * n
        vis = [False] * n
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
        dis[s] = 0
        q = deque([s])
        vis[s] = True
        while q:
            u = q.popleft()
            vis[u] = False
            for v, w in adj[u]:
                if dis[u] + w < dis[v]:
                    dis[v] = dis[u] + w
                    cnt[v] = cnt[u] + 1
                    if cnt[v] >= n:
                        return False, None
                    if not vis[v]:
                        q.append(v)
                        vis[v] = True
        return True, dis

    import random
    random.seed(23)
    for _ in range(300):
        n = random.randint(1, 7)
        edges = []
        for i in range(n):
            for j in range(n):
                if i != j and random.random() < 0.3:
                    edges.append((i, j, random.randint(-5, 8)))
        s = random.randrange(n)
        ok1, d1 = bellman_ford(n, edges, s)
        ok2, d2 = spfa(n, edges, s)
        assert ok1 == ok2, (n, edges, s, ok1, ok2)
        if ok1:
            for i in range(n):
                assert d1[i] == d2[i], (i, d1[i], d2[i])
    print("All tests passed.")
```

**PyPy 提示**: 用列表存边，外层 n-1 次内层遍历 m 条边；加 visited 标记加速（dis 变化过的 u 才参与）。判负环时第 n 轮若更新则直接返回 False。PyPy 下 O(VE) 在 n,m 均 ~2e3 时 4e6 次可过；更大规模应优先 Dijkstra/SPFA。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(VE)（提前终止时通常更优） |
| 空间 | O(V+E) |

### 局限

O(VE) 在稠密图上较慢（n 数千+全边时会超时）。只能检测『源点可达』的负环；若要求全图负环检测需加超级源点。不能输出负环本身（需额外 DFS/拓扑，见 CP-Alg negative cycle 篇）。对无负权图应优先 Dijkstra。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3385 | 3 | 【模板】负环：SPFA/Bellman-Ford 判负环模板题 | [https://www.luogu.com.cn/problem/P3385](https://www.luogu.com.cn/problem/P3385) |
| CSES | High Score | 4 | CP-Alg 例题：正权环路/最长路，负环判定+可达性检查 | [https://cses.fi/problemset/task/1673](https://cses.fi/problemset/task/1673) |
| CSES | Cycle Finding | 4 | CP-Alg 例题：检测负环并输出环中一个顶点 | [https://cses.fi/problemset/task/1197](https://cses.fi/problemset/task/1197) |

## Pitfalls · 易错点

- 第 n 轮判定负环时误认为『某边可松弛即全图负环』——只有 s 可达的负环才算
- 忘记 dis[u]==INF 时跳过（INF 参与运算会污染结果）
- 负环检测与最短路解耦：先判负环再输出 dis，否则 dis 无意义
- 边权很大的负值用 Python int 无溢出问题，但 INF 要足够大
- 邻接表实现时注意重边与自环；自环负权也是负环

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/shortest-path/](https://oi-wiki.org/graph/shortest-path/)
- CP-Algorithms ✓ [https://cp-algorithms.com/graph/bellman_ford.html](https://cp-algorithms.com/graph/bellman_ford.html)
- 书籍 ✓ `CPH ch13 pp133-142`
