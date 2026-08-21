---
id: floyd
name: Floyd-Warshall算法
group: G-B-2
stage: basic
priority: P0
depth_tier: deep
---

# Floyd-Warshall算法

> 全源最短路，DP三重循环O(V³)，可处理负权

<!-- 元信息: id=floyd · group=G-B-2 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

Floyd-Warshall 算法（又称 Floyd）求任意两点间（全源）最短路径，O(V³)。它用动态规划：令 dis[k][i][j] 表示只允许经过前 k 个节点（编号 ≤k）中转时 i 到 j 的最短路，转移 dis[k][i][j]=min(dis[k-1][i][j], dis[k-1][i][k]+dis[k-1][k][j])，滚掉第一维后即为三重循环 dis[i][j]=min(dis[i][j], dis[i][k]+dis[k][j])。可处理负权边，并在循环结束后检测负环（dis[i][i]<0）。常用于点数较少（n≤500）的全源最短路、传递闭包、最小环等。

## Why · 为什么

### 直觉 · Intuition

把『所有点』当做一个一个加入的『允许中转点』。新加入点 k 时，检查每一对 (i,j)：经 k 中转是否更短。因为每步只依赖上一次的结果，三重循环里 k 在最外层是精妙的『以 k 为最大中转点编号』的 DP 顺序，保证每个中转点恰好被考虑一次。

### 原理 · Principle

① 状态 dis[k][i][j]：只用 {0..k} 中节点做中转时 i→j 最短路；② 转移 dis[k]=min(dis[k-1], dis[k-1][i][k]+dis[k-1][k][j])，即 k 要么不在中转路径里，要么被使用；③ 滚掉 k 维得标准三重循环（k 外层），原因是 k 层只用上一层的 i,k 与 k,j，原地更新不破坏正确性；④ 路径重建：记录 nxt[i][j] 为从 i 到 j 路径上的下一节点，松弛时同步更新；⑤ 负环：若某 dis[i][i]<0，说明存在总权为负的闭合路径（负环）。

### 历史 · History

算法以 Robert Floyd 命名（1962 年发表于 Communications of the ACM），但本质是 Stephen Warshall（1962）传递闭包思想的推广；同时 Bernard Roy（1959）也独立发表。是四大经典最短路算法（Dijkstra/Bellman-Ford/Floyd/Johnson）中唯一的全源 DP 方法，教材（CLRS、CPH ch13）标准内容。

## How · 实现

### 伪代码

```python
# 三重循环 (k 外层)
dis = 距离矩阵; 无边记 INF; dis[i][i]=0
for k in range(n):
  for i in range(n):
    if dis[i][k] == INF: continue
    for j in range(n):
      if dis[k][j] == INF: continue
      dis[i][j] = min(dis[i][j], dis[i][k]+dis[k][j])

# 负环检测: 结束后存在 dis[i][i] < 0
# 路径重建:
nxt[i][j] 初始 = j (若有边)
if 松弛: nxt[i][j] = nxt[i][k]
```

### Python 实现

```python
def floyd(n, edges):
    """Floyd-Warshall: 返回 dis 距离矩阵 (可处理负权, 不含负环)。
    edges: [(u,v,w),...] 0-indexed"""
    INF = float('inf')
    dis = [[INF] * n for _ in range(n)]
    for i in range(n):
        dis[i][i] = 0
    for u, v, w in edges:
        dis[u][v] = min(dis[u][v], w)
    for k in range(n):
        for i in range(n):
            if dis[i][k] == INF:
                continue
            ik = dis[i][k]
            for j in range(n):
                if dis[k][j] == INF:
                    continue
                nd = ik + dis[k][j]
                if nd < dis[i][j]:
                    dis[i][j] = nd
    return dis


def floyd_has_neg_cycle(n, edges):
    """检测负环: Floyd 结束后存在 dis[i][i]<0"""
    dis = floyd(n, edges)
    for i in range(n):
        if dis[i][i] < 0:
            return True
    return False


def floyd_path(n, edges, s, t):
    """Floyd + 路径重建: 返回 (dist, path 节点列表); 不可达返回 (inf, [])"""
    INF = float('inf')
    dis = [[INF] * n for _ in range(n)]
    nxt = [[-1] * n for _ in range(n)]
    for i in range(n):
        dis[i][i] = 0
    for u, v, w in edges:
        if w < dis[u][v]:
            dis[u][v] = w
            nxt[u][v] = v
    for k in range(n):
        for i in range(n):
            if dis[i][k] == INF:
                continue
            for j in range(n):
                if dis[k][j] == INF:
                    continue
                nd = dis[i][k] + dis[k][j]
                if nd < dis[i][j]:
                    dis[i][j] = nd
                    nxt[i][j] = nxt[i][k]
    if dis[s][t] == INF:
        return INF, []
    path = []
    cur = s
    while cur != -1:
        path.append(cur)
        if cur == t:
            break
        cur = nxt[cur][t]
    return dis[s][t], path


if __name__ == "__main__":

    def dijkstra_all(adj, n):
        import heapq
        out = []
        for s in range(n):
            dis = [float('inf')] * n
            dis[s] = 0
            pq = [(0, s)]
            while pq:
                d, u = heapq.heappop(pq)
                if d > dis[u]:
                    continue
                for v, w in adj[u]:
                    if d + w < dis[v]:
                        dis[v] = d + w
                        heapq.heappush(pq, (dis[v], v))
            out.append(dis)
        return out

    import random
    random.seed(11)
    for _ in range(150):
        n = random.randint(1, 7)
        edges = []
        adj = [[] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j and random.random() < 0.35:
                    w = random.randint(1, 8)
                    edges.append((i, j, w))
                    adj[i].append((j, w))
        disF = floyd(n, edges)
        disD = dijkstra_all(adj, n)
        for i in range(n):
            for j in range(n):
                a, b = disF[i][j], disD[i][j]
                if a == float('inf') or b == float('inf'):
                    assert a == b, (i, j, a, b)
                else:
                    assert a == b, (i, j, a, b)

    # 负环检测
    assert floyd_has_neg_cycle(3, [(0, 1, 1), (1, 2, -1), (2, 0, -2)]) is True
    assert floyd_has_neg_cycle(3, [(0, 1, 1), (1, 2, -1), (2, 0, 1)]) is False

    # 路径重建
    edges = [(0, 1, 2), (0, 2, 5), (1, 3, 1), (2, 3, 2), (1, 2, 1)]
    d, p = floyd_path(4, edges, 0, 3)
    assert d == 3 and p == [0, 1, 3], (d, p)
    print("All tests passed.")
```

**PyPy 提示**: 三重循环用局部变量 ik=dis[i][k] 与 nd 减少索引；跳过 INF 提前 continue 显著提速。稠密图 n≤500 时三重 1.25e8 次运算 PyPy 约 2-3s，可接受；更大只能换 Johnson 或 n 次 Dijkstra。内层 j 循环用 range 而非 list 切片。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(V³) |
| 空间 | O(V²) 距离矩阵；路径重建额外 O(V²) |

### 局限

V 大时 O(V³) 不可行（n≤500 以内为宜，n=1000 约 1e9 操作超时）。可处理负权但不能含负环（检测到负环即无有限最短路）。对含负环的图，floyd 无法给出答案，需先判负环。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1119 | 4 | 灾后重建：按时间逐点开放中转点，恰好对应 Floyd 的 k 循环 | [https://www.luogu.com.cn/problem/P1119](https://www.luogu.com.cn/problem/P1119) |
| CSES | Shortest Routes II | 3 | 全源最短路模板（Floyd），n≤500 标准题 | [https://cses.fi/problemset/task/1672](https://cses.fi/problemset/task/1672) |
| Luogu | P4768 | 6 | 最短路径+离线：结合 Kruskal 重构树，Floyd 思路的推广 | [https://www.luogu.com.cn/problem/P4768](https://www.luogu.com.cn/problem/P4768) |

## Pitfalls · 易错点

- k 必须在最外层——把 k 放内层会得到错误结果
- 重边取 min 建矩阵，否则丢边
- INF 太大导致 inf+w 溢出（Python float 无此问题，但 int INF 需足够大）
- 负环时 dis[i][i]<0，但无负环图从任意 i 出发回到 i 应为 0
- 路径重建忘记初始化 nxt 或在松弛时同步更新
- n 超过 ~500 时 O(V³) 超时，需换 Johnson/SPFA

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/shortest-path/](https://oi-wiki.org/graph/shortest-path/)
- CP-Algorithms ✓ [https://cp-algorithms.com/graph/all-pair-shortest-path-floyd-warshall.html](https://cp-algorithms.com/graph/all-pair-shortest-path-floyd-warshall.html)
- 书籍 ✓ `CPH ch13 pp133-142`
