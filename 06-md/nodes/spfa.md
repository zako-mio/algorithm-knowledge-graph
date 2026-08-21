---
id: spfa
name: SPFA算法
group: G-B-2
stage: intermediate
priority: P1
depth_tier: standard
---

# SPFA算法

> Bellman-Ford队列优化，均摊快但最坏O(VE)

<!-- 元信息: id=spfa · group=G-B-2 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

SPFA（Shortest Path Faster Algorithm）是 Bellman-Ford 的队列优化：只把『上一轮被松弛的节点』入队并松弛其出边，跳过无用的全边扫描。均摊情况很快（随机图近似 O(E)），但最坏时间复杂度 O(VE)，可被构造卡死。用 cnt[v] 记录 v 被松弛的次数（等价最短路经过边数），当 cnt[v]≥n 判定源可达负环。是判负环与含负权图最短路的常用实现，但竞赛中『无负权优先 Dijkstra』是铁律。

## Why · 为什么

### 直觉 · Intuition

Bellman-Ford 每轮盲目扫全部边。观察：只有 dis 刚变小（被松弛）的节点 u，它的出边才可能在下一轮继续松弛别人。于是维护一个队列，谁的 dis 变了谁入队，队空即收敛。负环检测：一个节点若最短路的边数超过 n-1（cnt≥n），必然走了重复环且环权为负。

### 原理 · Principle

① dis[s]=0 入队；② 每次弹出 u，松弛 u 的所有出边，若 v 被松弛且不在队中则入队；③ cnt[v]=cnt[u]+1 记录路径边数；④ 若 cnt[v]≥n 说明经 v 的最短路边数超上限 → 存在从源可达的负环；⑤ 出队时置 vis[u]=False 允许再次入队（区别于 Dijkstra 的永久标记）。注意 SLF/LLL/栈优化等变体可提升部分图性能，但最坏仍 O(VE)，甚至堆优化版可被卡到指数级。

### 历史 · History

SPFA 由段凡丁 1994 年在中国提出并命名，本质即 Bellman-Ford 的队列版本（Bellman 1958）。因实现简单、随机图快，曾在中国 OI 圈广泛使用；随着针对性的卡 SPFA 数据出现，OI Wiki 明确警示『最坏 O(nm) 且易卡，考试谨慎使用』。CP-Algorithms 将其归入 D'Esopo-Pape 算法族。

## How · 实现

### 伪代码

```python
def spfa(adj, n, s):
  dis=[INF]*n; dis[s]=0; vis=[False]*n; cnt=[0]*n
  q=deque([s]); vis[s]=True
  while q:
    u=q.popleft(); vis[u]=False
    for (v,w) in adj[u]:
      if dis[u]+w < dis[v]:
        dis[v]=dis[u]+w
        cnt[v]=cnt[u]+1
        if cnt[v]>=n: return False, None   # 负环
        if not vis[v]: q.append(v); vis[v]=True
  return True, dis
```

### Python 实现

```python
from collections import deque


def spfa(n, adj, s):
    """SPFA 单源最短路(可负权) + 负环检测.
    adj: 邻接表 adj[u]=[(v,w),...].
    返回 (True, dis) 或 (False, None) 表示 s 可达负环."""
    INF = float('inf')
    dis = [INF] * n
    vis = [False] * n
    cnt = [0] * n
    dis[s] = 0
    q = deque([s])
    vis[s] = True
    while q:
        u = q.popleft()
        vis[u] = False
        du = dis[u]
        for v, w in adj[u]:
            if du + w < dis[v]:
                dis[v] = du + w
                cnt[v] = cnt[u] + 1
                if cnt[v] >= n:
                    return False, None
                if not vis[v]:
                    q.append(v)
                    vis[v] = True
    return True, dis


def spfa_global_neg_cycle(n, adj):
    """全图负环检测: 虚拟源点连 0 权边 (等价所有点初始入队 dis=0)"""
    INF = float('inf')
    dis = [0] * n
    vis = [True] * n
    cnt = [0] * n
    q = deque(range(n))
    while q:
        u = q.popleft()
        vis[u] = False
        du = dis[u]
        for v, w in adj[u]:
            if du + w < dis[v]:
                dis[v] = du + w
                cnt[v] = cnt[u] + 1
                if cnt[v] >= n:
                    return False
                if not vis[v]:
                    q.append(v)
                    vis[v] = True
    return True


if __name__ == "__main__":
    # 用例
    adj = [[] for _ in range(5)]
    edges = [(0, 1, 6), (0, 2, 7), (1, 2, 8), (1, 3, 5), (1, 4, -4), (2, 3, -3), (2, 4, 9), (3, 1, -2), (4, 0, 2), (4, 3, 7)]
    for u, v, w in edges:
        adj[u].append((v, w))
    ok, dis = spfa(5, adj, 0)
    assert ok and dis == [0, 2, 7, 4, -2], dis

    # 负环
    adj2 = [[] for _ in range(3)]
    for u, v, w in [(0, 1, 1), (1, 2, -3), (2, 0, 1)]:
        adj2[u].append((v, w))
    ok, _ = spfa(3, adj2, 0)
    assert ok is False

    # 与 Bellman-Ford 交叉验证 (随机图)
    import random
    random.seed(31)

    def bf(n, edges, s):
        INF = float('inf')
        dis = [INF] * n
        dis[s] = 0
        for _ in range(n - 1):
            upd = False
            for u, v, w in edges:
                if dis[u] != INF and dis[u] + w < dis[v]:
                    dis[v] = dis[u] + w
                    upd = True
            if not upd:
                break
        for u, v, w in edges:
            if dis[u] != INF and dis[u] + w < dis[v]:
                return False, None
        return True, dis

    for _ in range(400):
        n = random.randint(1, 7)
        edges = []
        a = [[] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j and random.random() < 0.3:
                    w = random.randint(-6, 9)
                    edges.append((i, j, w))
                    a[i].append((j, w))
        s = random.randrange(n)
        o1, d1 = spfa(n, a, s)
        o2, d2 = bf(n, edges, s)
        assert o1 == o2, (n, edges, s, o1, o2)
        if o1:
            for i in range(n):
                assert d1[i] == d2[i], (i, d1[i], d2[i])
    print("All tests passed.")
```

**PyPy 提示**: 队列用 collections.deque（popleft O(1)）。判负环用 cnt 数组；若要全图负环检测，可初始化所有点 dis=0 入队（等价虚拟源）。PyPy 下随机图接近 O(E)，但务必警惕恶意数据。SLF 优化（与队首比较决定插队头/尾）可加但防不住构造数据。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 均摊接近 O(E)；最坏 O(VE) |
| 空间 | O(V+E) |

### 局限

最坏 O(VE) 且极易被构造数据卡死（网格图等）；堆优化变体甚至可被卡到指数级。无负权图必须用 Dijkstra。含负权且图很大时，先判断是否有负环，无负环且边权非负仍优先 Dijkstra。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3385 | 3 | 【模板】负环：SPFA 判负环标准模板题 | [https://www.luogu.com.cn/problem/P3385](https://www.luogu.com.cn/problem/P3385) |
| Luogu | P1993 | 4 | 小 K 的农场：差分约束转最短路/负环判定（OI Wiki 例题） | [https://www.luogu.com.cn/problem/P1993](https://www.luogu.com.cn/problem/P1993) |
| Luogu | P2850 | 4 | 虫洞 Wormholes：负环检测判定时间回溯 | [https://www.luogu.com.cn/problem/P2850](https://www.luogu.com.cn/problem/P2850) |

## Pitfalls · 易错点

- 与 Dijkstra 混淆：vis[] 必须出队后置 False（SPFA 允许重复入队），否则负权图会漏松弛
- 负环判定 cnt[v]≥n 用『边数』而非入队次数，二者在特殊实现下可能不等价
- 初始化所有点入队做全图负环检测时，dis 全部置 0 而非 INF
- 被卡 TLE 时无脑优化队列不如换算法（无负权→Dijkstra）
- 重边/负自环：负自环直接判负环

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/shortest-path/](https://oi-wiki.org/graph/shortest-path/)
- CP-Algorithms ✓ [https://cp-algorithms.com/graph/desopo_pape.html](https://cp-algorithms.com/graph/desopo_pape.html)
- 书籍 ✓ `CPH ch13 pp133-142`
