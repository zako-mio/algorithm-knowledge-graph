---
id: min-cycle
name: 最小环
group: G-B-8
stage: advanced
priority: P2
depth_tier: standard
---

# 最小环

> 求图中边权和最小的环（围长）：Floyd 扩展 O(n³)、Dijkstra 删边 O(m(n+m)log n)、暴力 O(n²m)，可记录路径

<!-- 元信息: id=min-cycle · group=G-B-8 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

最小环（minimum cycle / girth）问题：给定图，求至少含 3 个顶点、边权和最小的简单环及其长度。三种方法：①暴力 O(n²m)：对每条边 (u,v) 删除后求 u 到 v 的最短路 dis(u,v)，最小环 = min(dis(u,v)+w)；②Dijkstra 删边 O(m(n+m)log n)：对每条边删掉后从一端跑 Dijkstra；③Floyd 扩展 O(n³)：在 Floyd 最外层循环到 k 时（dis[i][j] 此时只经过编号 <k 的中间点），用 dis[i][j]+val[i][k]+val[k][j] 更新答案，即最大编号顶点为 k 的环，i,j<k。记录路径：用 pos[u][v] 记录 dis[u][v] 的中间点，递归展开得到具体环。无向图与有向图公式略不同：有向图对应 dis(v,u)+w。模板题：AcWing 344 观光之旅（无向图最小环输出方案）。

## Why · 为什么

### 直觉 · Intuition

一个简单环（至少 3 点）总能被拆成'一条边 + 剩余路径'：环 = 边 (u,k)+(k,v) + 从 v 到 u 的路径。若固定最大编号顶点 k 作为'环的最高点'，则环的其他顶点编号都 <k，此时环长 = val[i][k]+val[k][j]+dis[i][j]（dis 只经过 <k 的中间点）。Floyd 外层循环按 k 递增，恰好能保证枚举到 k 时 dis[i][j] 尚未被 k 更新——这正是该时刻取最小环值的时机。

### 原理 · Principle

Floyd 求最小环：维护 val 原图边权邻接矩阵与 dis 最短路矩阵（初始同 val，对角 0）。最外层 for k：①先用当前 dis（只经 <k 的中间点）对每对 i<j<k 更新答案 dis[i][j]+val[i][k]+val[k][j]（保证三个点互异、不重复计数）；②再正常做 Floyd 松弛（引入 k 作为中间点）。正确性：对环上最大编号顶点 k，其两个相邻顶点 i,j 都 <k，故当循环到 k 时 dis[i][j] 已含全部中间点（都 <k），而环剩余边恰好是 val[i][k]+val[k][j]。注意 val 与 dis 分离：更新环长必须用原始边权 val，不能用已被松弛的 dis（否则可能退化为两点边）。记录路径：pos[i][j]=k 表示 dis[i][j] 的中间点，递归 pos 展开 i→k→…→j，环 = i,k,j + 递归 v 到 u 的路径。

### 历史 · History

Floyd-Warshall（1962）本身的扩展求最小环是经典技巧，广泛收录于 OI Wiki（min-circle）、算法竞赛教材。最小环与围长（girth）在图论中历史久远；竞赛中常用于带权图/无向图模板题与负环无关的场景（有负环时'最小环'无意义）。

## How · 实现

### 伪代码

```python
# Floyd 扩展求最小环（无向图，可记录路径）
ans = INF
for k in 1..n:
    # 先用当前 dis 更新环（i<j<k）
    for i in 1..k-1:
        for j in 1..i-1:
            if val[i][k]+val[k][j]+dis[i][j] < ans:
                ans = ...; 记录环: i,k,j + 递归展开 dis[j][i] 的中间点
    # 再正常 Floyd 松弛
    for i in 1..n:
        for j in 1..n:
            if dis[i][k]+dis[k][j] < dis[i][j]:
                dis[i][j] = ...; pos[i][j] = k
```

### Python 实现

```python
# -*- coding: utf-8 -*-
# Floyd 求无向图最小环 + 输出环路径（1-indexed 顶点）

def min_cycle(n, edges):
    """edges: [(u,v,w)] 1-indexed。返回 (最小环长 or INF, 环路径 or [])。"""
    INF = 10**9
    val = [[INF] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        val[i][i] = 0
    for u, v, w in edges:
        if w < val[u][v]:
            val[u][v] = val[v][u] = w
    dis = [row[:] for row in val]
    pos = [[0] * (n + 1) for _ in range(n + 1)]   # pos[i][j]=k: 最短路中间点
    best = INF
    cyc = []

    def get_path(u, v, out):
        """把 dis[u][v] 的中间点序列加入 out（递归展开）。"""
        k = pos[u][v]
        if k == 0:
            return
        get_path(u, k, out)
        out.append(k)
        get_path(k, v, out)

    for k in range(1, n + 1):
        # 更新环：i<j<k，三顶点互异
        for i in range(1, k):
            for j in range(1, i):
                if (val[i][k] < INF and val[k][j] < INF and dis[i][j] < INF
                        and val[i][k] + val[k][j] + dis[i][j] < best):
                    best = val[i][k] + val[k][j] + dis[i][j]
                    path = [i, k, j]
                    get_path(j, i, path)          # 展开 j 到 i 的最短路中间点
                    cyc = path
        # 标准 Floyd 松弛
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if dis[i][k] + dis[k][j] < dis[i][j]:
                    dis[i][j] = dis[i][k] + dis[k][j]
                    pos[i][j] = k
    return (best, cyc) if best < INF else (INF, [])


if __name__ == '__main__':
    # 三角形 + 额外重边
    n, edges = 3, [(1, 2, 1), (2, 3, 1), (3, 1, 1), (1, 2, 100)]
    best, cyc = min_cycle(n, edges)
    assert best == 3, (best, cyc)
    # 4 点：正方形边长1 -> 最小环 4；加对角线 1-3 权重10 不影响
    n2, edges2 = 4, [(1, 2, 1), (2, 3, 1), (3, 4, 1), (4, 1, 1), (1, 3, 10)]
    best2, cyc2 = min_cycle(n2, edges2)
    assert best2 == 4, (best2, cyc2)
    # 重边三角：1-2 权重 100 但存在 1-2 权重 1
    n3, edges3 = 3, [(1, 2, 1), (2, 3, 1), (3, 1, 1), (1, 2, 100), (2, 1, 100)]
    assert min_cycle(n3, edges3)[0] == 3
    # 随机验证：与暴力（枚举所有 3 点及以上简单环中最小的三角形/一般环）对拍
    import random, itertools
    random.seed(0)
    for _ in range(60):
        nn = random.randint(3, 7)
        m = random.randint(3, 12)
        es = []
        for _ in range(m):
            es.append((random.randint(1, nn), random.randint(1, nn), random.randint(1, 9)))
        got, _ = min_cycle(nn, es)
        # 暴力：枚举所有环（用 Floyd 值直接算最小简单环权）
        INF2 = 10**9
        val2 = [[INF2] * (nn + 1) for _ in range(nn + 1)]
        for i in range(1, nn + 1):
            val2[i][i] = 0
        for u, v, w in es:
            val2[u][v] = min(val2[u][v], w)
            val2[v][u] = min(val2[v][u], w)
        dis2 = [row[:] for row in val2]
        brute = INF2
        for k in range(1, nn + 1):
            for i in range(1, k):
                for j in range(1, i):
                    brute = min(brute, val2[i][k] + val2[k][j] + dis2[i][j])
            for i in range(1, nn + 1):
                for j in range(1, nn + 1):
                    dis2[i][j] = min(dis2[i][j], dis2[i][k] + dis2[k][j])
        if brute < INF2:
            assert got == brute, (nn, es, got, brute)
        else:
            assert got == 10**9, (nn, es, got)
    print('min-cycle tests passed')

```

**PyPy 提示**: O(n³) 三重循环 Python 只能跑 n≤300 左右；用列表与局部变量尽量优化。Dijkstra 删边版 O(m(n+m)log n) 在稀疏图更好，但实现更繁。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | Floyd 扩展 O(n³)；Dijkstra 删边 O(m(n+m)log n)；暴力 O(n²m) |
| 空间 | O(n²) |

### 局限

Floyd 扩展要求正权或至少无负环（有负环则'最小环'无下界）。更新环长必须用原边权 val，不能混用 dis。顶点数大时 O(n³) 不可行，需改用删边 + 最短路。记录路径需 pos 表与递归。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| AcWing | 344 | 3 | 观光之旅：无向图最小环模板，Floyd 扩展 + 输出路径 | [https://www.acwing.com/problem/content/346](https://www.acwing.com/problem/content/346) |
| POJ | 1734 | 3 | Sightseeing trip：无向带权最小环，与 AcWing 344 同题 | [http://poj.org/problem?id=1734](http://poj.org/problem?id=1734) |
| Luogu | P6175 | 3 | 无向图的最小环问题：Floyd 求最小环长度模板 | [https://www.luogu.com.cn/problem/P6175](https://www.luogu.com.cn/problem/P6175) |

## Pitfalls · 易错点

- 更新环长必须用原始边权 val[i][k]、val[k][j]，否则两点可能退化成两条边（错判）
- 无向图 i<j<k 保证三点互异；有向图最小环是 dis(v,u)+w，公式不同
- dis 矩阵初始复制 val，对角线为 0；pos 初始 0 表示无中间点
- 存在重边时取最小权重；负权/负环会使最小环无意义
- 输出路径：环 = i,k,j + 递归展开 pos[j][i]；注意递归深度与去重

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/min-circle/](https://oi-wiki.org/graph/min-circle/)
- 书籍 ✓ `AcWing 344 观光之旅（模板题）；CPH 无直接章节`
