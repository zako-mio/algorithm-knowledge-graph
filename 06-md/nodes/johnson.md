---
id: johnson
name: Johnson算法
group: G-B-2
stage: intermediate
priority: P1
depth_tier: standard
---

# Johnson算法

> 全源最短路，势能法处理负权，n次Dijkstra O(VElogV)

<!-- 元信息: id=johnson · group=G-B-2 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

Johnson 算法求任意两点间的全源最短路，O(VE log V)，在稀疏图上优于 Floyd 的 O(V³)，且支持负权边（不能有负环）。思路：加虚拟源点 0 向所有点连 0 权边，用 Bellman-Ford 求出各点势能 h(i)；把每条边 (u,v,w) 重新标记为 w'=w+h(u)-h(v)≥0，然后对每个点跑一遍 Dijkstra 求最短路，最后把势能差加回去。是『把负权图变成非负权图再利用 Dijkstra 的贪心优势』的经典势能技巧，也是最小费用流 SSP 里用 Dijkstra 的核心思想来源。

## Why · 为什么

### 直觉 · Intuition

负权边让 Dijkstra 失效，但把每条边统一加一个常数又会改变最短路（走的边数不同，OI Wiki 反例）。观察：若给每个点赋一个『高度』h(i)（势能），把边权 w(u,v) 改成 w+h(u)-h(v)，则任意路径 s→t 的总长变化恒为 h(s)-h(t)，与走哪条路无关——路径长度排序不变，最短路还是那条。若还能让所有新边权非负，就能跑 Dijkstra。Bellman-Ford 从虚拟源点求出的最短路天然满足三角形不等式 h(v)≤h(u)+w(u,v)，故 w'=w+h(u)-h(v)≥0。

### 原理 · Principle

① 加虚拟源点 0，向每个点连权 0 的边；② 从 0 跑 Bellman-Ford 得 h(v)=dis(v)（若检测到负环则无解）；③ 重标号 w'(u,v)=w(u,v)+h(u)-h(v)，由三角形不等式知 w'≥0；④ 对每个顶点跑 Dijkstra 得 d'(s,t)；⑤ 真实最短路 d(s,t)=d'(s,t)-h(s)+h(t)。正确性：路径 s→p1→…→t 长度和 Σ(w+h(u)-h(v)) = Σw + h(s)-h(t)，势能差为常数，因此最短路对应关系不变。

### 历史 · History

Donald B. Johnson 于 1977 年提出（Johnson，Efficient algorithms for shortest paths in sparse networks），将全源最短路从 O(V³) 降为 O(VE log V)。势能重标号思想与差分约束/最短路径势（potential）一脉相承，后成为算法设计中『转负权为非负』的标准范式。OI Wiki 与 CPH ch13 均收录。

## How · 实现

### 伪代码

```python
def johnson(n, edges):
  # 虚拟源点 0
  h = bellman_ford(n+1, edges + [(n,i,0) for i in range(n)], n)[1]
  if 负环: return None
  # 重标号
  w'[u,v] = w[u,v] + h[u] - h[v]   # 全部 >=0
  adj' = 按 w' 建邻接表
  ans = [[0]*n for _ in range(n)]
  for s in range(n):
    d' = dijkstra(adj', s)
    for t in range(n):
      ans[s][t] = d'[t] - h[s] + h[t]
  return ans
```

### Python 实现

```python
import heapq


def _dijkstra(adj, s, n):
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


def johnson(n, edges):
    """全源最短路(支持负权, 无负环). edges: [(u,v,w)].
    返回 dis 矩阵; 不可达为 float('inf'); 存在负环返回 None."""
    INF = float('inf')
    super_src = n
    super_edges = edges + [(super_src, i, 0) for i in range(n)]

    h = [INF] * (n + 1)
    h[super_src] = 0
    for _ in range(n):
        updated = False
        for u, v, w in super_edges:
            if h[u] != INF and h[u] + w < h[v]:
                h[v] = h[u] + w
                updated = True
        if not updated:
            break
    for u, v, w in super_edges:
        if h[u] != INF and h[u] + w < h[v]:
            return None  # 负环

    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        w2 = w + h[u] - h[v]
        if w2 < 0:
            w2 = 0  # 数值保护(理论上 w'>=0, 浮点/取整边界兜底)
        adj[u].append((v, w2))

    ans = [[INF] * n for _ in range(n)]
    for s in range(n):
        d2 = _dijkstra(adj, s, n)
        for t in range(n):
            if d2[t] != INF:
                ans[s][t] = d2[t] - h[s] + h[t]
            else:
                ans[s][t] = INF
    return ans


if __name__ == "__main__":
    # 带负权的稀疏图
    n = 4
    edges = [(0, 1, 3), (0, 2, -2), (1, 3, 2), (2, 3, 5), (2, 1, 1), (3, 1, -1)]
    ans = johnson(n, edges)
    assert ans is not None
    assert ans[0][3] == 1, ans[0]  # 0->2(-2)->1(1)->3(2) = 1
    assert ans[0] == [0, -1, -2, 1], ans[0]

    # 与 Floyd 交叉验证
    import random
    random.seed(41)
    for _ in range(200):
        n = random.randint(1, 7)
        edges = []
        for i in range(n):
            for j in range(n):
                if i != j and random.random() < 0.3:
                    edges.append((i, j, random.randint(-4, 7)))
        # Floyd 参考
        INF = float('inf')
        d = [[INF] * n for _ in range(n)]
        for i in range(n):
            d[i][i] = 0
        for u, v, w in edges:
            d[u][v] = min(d[u][v], w)
        for k in range(n):
            for i in range(n):
                if d[i][k] == INF:
                    continue
                for j in range(n):
                    if d[k][j] == INF:
                        continue
                    d[i][j] = min(d[i][j], d[i][k] + d[k][j])
        neg = any(d[i][i] < 0 for i in range(n))
        ans = johnson(n, edges)
        if neg:
            assert ans is None, (n, edges)
        else:
            assert ans is not None
            for i in range(n):
                for j in range(n):
                    a, b = ans[i][j], d[i][j]
                    if a == INF or b == INF:
                        assert a == b, (i, j, a, b)
                    else:
                        assert abs(a - b) < 1e-9, (i, j, a, b)

    # 负环
    assert johnson(3, [(0, 1, 1), (1, 2, -3), (2, 0, 1)]) is None
    print("All tests passed.")
```

**PyPy 提示**: Bellman-Ford 用边列表一次遍历；Dijkstra 用 heapq。n 次 Dijkstra 是主开销，n,m 均 ~1e4 时约 O(VE log V) 可行；n 大边少时比 Floyd 优。势能 h 可为负大数，Python int 无溢出。若已知图无负权可跳过 BF 直接 n 次 Dijkstra。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(VE) 求势能 + O(VE log V) 的 n 次 Dijkstra |
| 空间 | O(V²) 结果矩阵 + O(V+E) |

### 局限

含负环时无最短路，算法返回 None；V 很大且图稠密时 O(VE log V) 仍不如 Floyd。结果矩阵 O(V²) 内存对 V≥5e3 有压力。仅需单源时不要用 Johnson。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P5905 | 5 | 【模板】Johnson 全源最短路：模板题，负权+全源 | [https://www.luogu.com.cn/problem/P5905](https://www.luogu.com.cn/problem/P5905) |
| CSES | Shortest Routes II | 3 | 全源最短路（非负）：Floyd 或 Johnson 均适用的小数据题 | [https://cses.fi/problemset/task/1672](https://cses.fi/problemset/task/1672) |
| AtCoder | ABC237 E | 5 | Skiing：含负权单源，差分约束/势能思想与 Dijkstra 结合 | [https://atcoder.jp/contests/abc237/tasks/abc237_e](https://atcoder.jp/contests/abc237/tasks/abc237_e) |

## Pitfalls · 易错点

- 忘记先判负环：Bellman-Ford 求 h 时若第 n 轮仍可松弛必须返回无解
- 重标号后忘记把 h 差加回去（ans = d' - h[s] + h[t]）
- 虚拟源点到所有点连 0 权边是必要的，否则 h 只覆盖从 0 可达部分
- n 次 Dijkstra 之间要复用邻接表，别重复建图
- h 数组用 INF 初始化，未从 0 达的点要处理

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/shortest-path/](https://oi-wiki.org/graph/shortest-path/)
- CP-Algorithms ✓ [https://cp-algorithms.com/graph/johnson.html](https://cp-algorithms.com/graph/johnson.html)
- 书籍 ✓ `CPH ch13 pp133-142`
