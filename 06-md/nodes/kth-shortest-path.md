---
id: kth-shortest-path
name: k短路
group: G-B-2
stage: advanced
priority: P2
depth_tier: standard
---

# k短路

> 第k短路径，A*或可并堆方法

<!-- 元信息: id=kth-shortest-path · group=G-B-2 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

k 短路问题：求从 s 到 t 的第 k 短路径长度（允许重复经过边/点，即『途径』k-shortest walk）。主流方法：① A* 搜索：用反向图上到 t 的最短路作为启发函数 h，状态 (g(x), x) 以 f=g+h 为优先级出队，第 k 次弹到 t 即为第 k 短；② Eppstein 的可持久化可并堆法：按最短路树上的『偏离边』建立 k 短路径偏序，预处理后 O(log n + k log n) 逐条输出，是严格多项式最坏界方法。竞赛模板题常用 A*（实现简单、k 较小可行）。

## Why · 为什么

### 直觉 · Intuition

最短路树（从 t 反跑 Dijkstra 得到）把每个点连向 t 的最短路径固定下来。任意一条 s→t 的路径与最短路树的差异，在于它『偏离』树边、走了一条非树边，之后可能再回树。若给每条非树边 (u,v) 定义额外代价 Δ=w(u,v)+h(v)-h(u)（h 为到 t 的最短路），则任意路径长 = 最短路长 + Σ 偏离边的 Δ，且偏离边序列满足首尾相接（路演性质）。k 短路即找 ΣΔ 第 k 小的合法偏离序列——这就是 Eppstein 法的建模。A* 则直接按 f=g+h 逐条生成，天然按路径长升序弹出。

### 原理 · Principle

① 反向图上从 t 跑 Dijkstra，得 h(x)=x 到 t 的最短路（正权图）；② A*：状态 (x, g(x)) 入优先队列，键 f=g+h；每次弹最小 f，若弹到 t 记一条答案（第 1 次=最短路，第 k 次=第 k 短）；③ 注意弹出 t 也继续搜（不是终止），因为要第 k 条；④ Eppstein：以最短路树为骨架，维护可持久化可并堆存每个点出发的非树边（按 Δ 排序），从 s 开始按 Δ 升序扩展路径，配合『走一段树边+跨一条非树边』的分解，用堆合并实现 O(log n) 出第 1..k 条；⑤ 无负权前提（最短路树需要非负边权）。

### 历史 · History

k 短路问题 1970s 起被系统研究：Yen (1971) 提出 O(k·V·(E+VlogV)) 的删边枚举法；Jiménez-Marzal 改进；Eppstein (1998) 用可持久化可并堆给出 O(E+VlogV+k·logk) 的近最优算法。竞赛界普及的是 A* 版本（启发式 = 反向最短路，非满可采纳时仍可用）。OI Wiki 专章介绍 A* 与 Eppstein 法，模板题是 Library Checker - K-Shortest Walk。

## How · 实现

### 伪代码

```python
# A* 版 (正权图)
def kth_shortest(n, adj, radj, s, t, k):
  h = dijkstra_on_reverse(radj, t)   # h[x]=x到t最短路
  pq = [(h[s], 0, s)]                 # (f, g, node)
  cnt = [0]*n
  while pq:
    f, g, u = heappop(pq)
    cnt[u] += 1
    if u == t and cnt[u] == k: return g
    if cnt[u] > k: continue
    for v, w in adj[u]:
      heappush(pq, (g + w + h[v], g + w, v))
  return -1
```

### Python 实现

```python
import heapq


def kth_shortest_astar(n, adj, radj, s, t, k):
    """A* 求第 k 短路径长度 (允许重复走边; 正权图).
    adj: 正向邻接表; radj: 反向邻接表."""
    INF = float('inf')
    # 1) 反向 Dijkstra 求 h[x] = x 到 t 的最短路
    h = [INF] * n
    h[t] = 0
    pq = [(0, t)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > h[u]:
            continue
        for v, w in radj[u]:
            nd = d + w
            if nd < h[v]:
                h[v] = nd
                heapq.heappush(pq, (nd, v))

    # 2) A* 扩展
    cnt = [0] * n
    pq = [(h[s], 0, s)]  # (f=g+h, g, node)
    while pq:
        f, g, u = heapq.heappop(pq)
        cnt[u] += 1
        if u == t and cnt[u] == k:
            return g
        if cnt[u] > k:
            continue
        for v, w in adj[u]:
            if h[v] == INF:
                continue
            heapq.heappush(pq, (g + w + h[v], g + w, v))
    return -1  # 不足 k 条


if __name__ == "__main__":
    # 小型图
    n = 4
    adj = [[] for _ in range(n)]
    radj = [[] for _ in range(n)]
    edges = [(0, 1, 1), (1, 2, 1), (2, 3, 1), (0, 2, 3), (0, 3, 10), (1, 3, 5)]
    for u, v, w in edges:
        adj[u].append((v, w))
        radj[v].append((u, w))
    # 0->3 的所有路径长度: 0-3=10; 0-1-3=6; 0-2-3=4; 0-1-2-3=3
    # 排序: 3, 4, 6, 10, 且允许重复绕圈 (无穷多条)
    got = [kth_shortest_astar(n, adj, radj, 0, 3, k) for k in (1, 2, 3, 4)]
    assert got == [3, 4, 6, 10], got

    # 枚举验证前 4 条 (小图直接枚举路径)
    import random
    random.seed(61)

    def brute_k(n, adj, s, t, k, cap_len=8):
        res = []
        def dfs(u, d, steps):
            if u == t:
                res.append(d)
            if steps >= cap_len:
                return
            for v, w in adj[u]:
                dfs(v, d + w, steps + 1)
        dfs(s, 0, 0)
        res.sort()
        return res[k - 1] if len(res) >= k else -1

    for _ in range(60):
        n = random.randint(2, 6)
        adj = [[] for _ in range(n)]
        radj = [[] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j and random.random() < 0.35:
                    w = random.randint(1, 5)
                    adj[i].append((j, w))
                    radj[j].append((i, w))
        k = random.randint(1, 4)
        a = kth_shortest_astar(n, adj, radj, 0, n - 1, k)
        b = brute_k(n, adj, 0, n - 1, k)
        # 允许重复走边时 A* 会得到无穷多条; 只当枚举 cap 覆盖时比较
        if b != -1:
            assert a == b, (n, k, a, b)
    print("All tests passed.")
```

**PyPy 提示**: A* 版在 k 较小时 (k≤100) 可行，但节点 cnt 会随搜索膨胀，注意剪枝 cnt[u]>k continue。若图较大或 k 很大，改用 Eppstein 可持久化可并堆（模板题 Library Checker 需要该复杂度）。PyPy 下 heapq 性能足够。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | A*: O((V+E)log V) 建 h + 最坏 O(k·(V+E)logV) 扩展；Eppstein: O(E+VlogV+k·logk) |
| 空间 | A*: O(V+E)（堆最大存 k 倍边）；Eppstein 需可持久化堆 O(E+V) |

### 局限

A* 在 k 大或图稠密时可能超时/爆堆；『允许重复走边』才有意义（否则第 k 短可能不存在，简单路径版是另一问题）。负权图不能直接用（需先 Bellman-Ford 求势能再做 A*）。模板题要求 O(k log k) 出第 k 条时 A* 不够，须 Eppstein。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Library Checker | K-Shortest Walk | 6 | 模板题：OI Wiki 用可持久化可并堆实现的 k 短路模板 | [https://judge.yosupo.jp/problem/k_shortest_walk](https://judge.yosupo.jp/problem/k_shortest_walk) |
| Luogu | P2483 | 7 | SDOI2010 魔法猪学院：OI Wiki 习题，A*/k 短路应用 | [https://www.luogu.com.cn/problem/P2483](https://www.luogu.com.cn/problem/P2483) |
| POJ | 2449 | 5 | Remmarguts' Date：经典 A* 求 k 短路模板题 | [http://poj.org/problem?id=2449](http://poj.org/problem?id=2449) |

## Pitfalls · 易错点

- A* 弹出 t 第 k 次才是第 k 短——不能一弹到 t 就终止
- 负权图：h 需先用势能法处理（Bellman-Ford 求 h 再 A*）
- 『简单路径』k 短路与『途径』k 短路是不同问题，题面要看清
- k 很大时 A* 状态爆炸，应换 Eppstein/删边法
- 重边/环导致无穷多条路径，答案可能含重复绕圈，注意题面约定
- h[v]==INF（v 到不了 t）的节点不能入队

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/kth-path/](https://oi-wiki.org/graph/kth-path/)
- CP-Algorithms △ [https://cp-algorithms.com/graph/kth-shortest-path.html](https://cp-algorithms.com/graph/kth-shortest-path.html)
- web ✓ [https://en.wikipedia.org/wiki/K_shortest_path_routing](https://en.wikipedia.org/wiki/K_shortest_path_routing)
