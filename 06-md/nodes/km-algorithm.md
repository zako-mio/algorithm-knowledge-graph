---
id: km-algorithm
name: KM算法
group: G-B-6
stage: intermediate
priority: P1
depth_tier: standard
---

# KM算法

> 二分图最大权匹配(Kuhn-Munkres)O(V³)

<!-- 元信息: id=km-algorithm · group=G-B-6 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

KM 算法（Kuhn–Munkres 算法，又称匈牙利算法的带权版）求二分图的最大权完美匹配，O(n³)。它维护一组可行顶标 lx/ly（满足对任意边 w(u,v) ≤ lx(u)+ly(v)），定义相等子图为满足 w = lx+ly 的边构成的子图；不断调整顶标、在相等子图中找完美匹配，当相等子图出现完美匹配时，它就是最大权完美匹配（因任何完美匹配权值和 ≤ Σlx+Σly，相等子图匹配权值和 = Σlx+Σly）。对于非平衡/非完全二分图，通过补点（少的一侧补到相等）+ 缺失边权设 0 或 -inf 转为方阵问题。是解决指派问题（assignment problem）的经典 O(n³) 算法。

## Why · 为什么

### 直觉 · Intuition

给每个左点一个『心理价』lx、右点 ly，要求任意配对 u-v 的权值不超过 lx(u)+ly(v)（可行顶标）。若存在一组配对使得每对的权值恰好等于两者顶标之和（相等子图完美匹配），那么这些配对的权值和等于所有顶标之和，这已经是任何配对的权值和的上界——所以就是最优。算法像爬山：从宽松顶标开始，在相等子图中反复找增广路；找不到时把交错树 S 中的左点顶标降 a、T 中的右点顶标升 a（a 取 S-T' 边的最小 slack），把新边『拉进』相等子图，直到匹配完美。

### 原理 · Principle

① 可行顶标：w(u,v) ≤ lx(u)+ly(v)；② 相等子图：只含 w=lx+ly 的边；③ 定理：若某组可行顶标的相等子图有完美匹配 M，则 M 是最大权完美匹配（任意匹配权值和 ≤ Σlx+ly = M 的权值和）；④ 算法：初始化 lx(u)=max_v w(u,v), ly=0；对每个左部点做 BFS 增广，在相等子图中找增广路；若失败，交错树 S（左部在树内）/T（右部在树内），a = min{lx(u)+ly(v)-w(u,v) | u∈S, v∈T'}，对 u∈S: lx-=a，对 v∈T: ly+=a，则 S-T 边仍相等、S-T' 边 slack 变小可能加入相等子图，重复；⑤ 维护 slack(v)=min_{u∈S}{lx(u)+ly(v)-w(u,v)}，使每次顶标调整与更新为 O(n)，整体 O(n³)。

### 历史 · History

指派问题最早可追溯到 1784 年 Monge；算法命名：Harold Kuhn 1955 年发表（基于 Kőnig 与 Egerváry 的匈牙利工作），James Munkres 1957 年证明其多项式时间，因此称 Kuhn–Munkres（KM）。2006 年发现 Jacobi 1890 年已用拉丁文发表了等价算法。O(n³) 的顶标优化由 Edmonds-Karp 与 Tomizawa 独立给出。OI Wiki 称其为 Hungarian Algorithm（最大权完美匹配），与 Kuhn 的增广路最大匹配区分。

## How · 实现

### 伪代码

```python
# 平衡方阵 n×n，求最大权完美匹配 (缺失边设 -inf 或 0)
init: lx[i]=max_j w[i][j]; ly[j]=0
for i in 左部点:
  while True:
    visited_左/右 = False
    if dfs(i) 找到增广路: break
    a = min{ lx[u]+ly[v]-w[u][v] | u∈S(vis左), v∉T(vis右) }
    for u∈S: lx[u]-=a
    for v∉T: ly[v]+=a   # 等价于调整使新边进入相等子图
# O(n^3) 实现用 slack 数组 + BFS
```

### Python 实现

```python
def km_max_weight(weights):
    """Kuhn-Munkres 求最大权完美匹配 (O(n^3))。
    weights: n×n 二维数组，缺失边权值用 -INF。
    返回 (最大权和, match_row): match_row[i] = 第 i 行匹配的列。"""
    n = len(weights)
    INF = 10 ** 18
    # 最大权 → 对权值取负转最小指派（加常数不影响 argmin，故直接取负）
    a = [[-weights[i][j] for j in range(n)] for i in range(n)]
    u = [0] * (n + 1)      # 行顶标
    v = [0] * (n + 1)      # 列顶标
    p = [0] * (n + 1)      # 列匹配的行
    way = [0] * (n + 1)
    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = [INF] * (n + 1)
        used = [False] * (n + 1)
        while True:
            used[j0] = True
            i0 = p[j0]
            delta = INF
            j1 = 0
            for j in range(1, n + 1):
                if not used[j]:
                    cur = a[i0 - 1][j - 1] - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                    if minv[j] < delta:
                        delta = minv[j]
                        j1 = j
            for j in range(n + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break
    match_row = [0] * (n + 1)
    for j in range(1, n + 1):
        match_row[p[j]] = j
    total = sum(weights[i - 1][match_row[i] - 1] for i in range(1, n + 1))
    return total, [match_row[i] - 1 for i in range(1, n + 1)]


if __name__ == '__main__':
    import itertools, random

    def brute(a):
        best = -10 ** 18
        for perm in itertools.permutations(range(len(a))):
            s = sum(a[i][perm[i]] for i in range(len(a)))
            best = max(best, s)
        return best

    # 手测
    assert km_max_weight([[3, 1], [2, 1]])[0] == 4   # 选 3+1
    assert km_max_weight([[5, 4], [3, 6]])[0] == 11  # 选 5+6
    # 随机交叉验证（含负权）
    random.seed(5)
    for _ in range(500):
        n = random.randint(1, 5)
        a = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
        r1, _ = km_max_weight(a)
        r2 = brute(a)
        assert r1 == r2, (a, r1, r2)
    print('km-algorithm: All tests passed.')

```

**PyPy 提示**: O(n³) 的顶标实现必须用 slack/way 数组 + 交替路径维护（DFS 朴素版会退化为 O(n⁴)）。权值可能为负：最大权完美匹配需补 -INF 处理不存在边，或整体加常数转非负。n≤300 时 O(n³) 在 PyPy 下勉强可跑，更大规模考虑费用流。注意此题实现是『方阵』，矩形需补点。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n³)（n 轮 × 每轮 BFS/顶标调整 O(n) × 每轮扫描 O(n)） |
| 空间 | O(n²) 权重矩阵 + O(n) 顶标/slack/匹配数组 |

### 局限

标准 KM 求的是完美匹配（方阵）；矩形图需补点、缺失边权设 -INF（最大权）或 0（可放任不匹配）。负权与 -INF 混合时初始化 lx=max 需小心。O(n³) 在 n 大（>1000）时超时，可换费用流/网络流。与最小权指派问题仅相差符号取负。若只求最大匹配（无权）用 Kuhn/HK 更快。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| UOJ | 80 | 4 | 二分图最大权匹配模板题：KM 标准模板（n 可达 400），OI Wiki 习题 | [https://uoj.ac/problem/80](https://uoj.ac/problem/80) |
| Luogu | P6577 | 4 | 【模板】二分图最大权完美匹配：KM O(n³) 模板，含负数与缺失边处理 | [https://www.luogu.com.cn/problem/P6577](https://www.luogu.com.cn/problem/P6577) |
| Luogu | P4014 | 4 | 分配问题：指派问题模板，KM 最小/最大权两种（取负转换），网络流 24 题 | [https://www.luogu.com.cn/problem/P4014](https://www.luogu.com.cn/problem/P4014) |
| Luogu | P2756 | 3 | 飞行员配对方案：二分图最大匹配建模入门（也可 KM 权为 1 或网络流） | [https://www.luogu.com.cn/problem/P2756](https://www.luogu.com.cn/problem/P2756) |

## Pitfalls · 易错点

- 朴素的 DFS 顶标调整（每次扫 S×T' 求 a）是 O(n⁴)，必须用 slack 数组维护到 O(n³)
- 最大权完美匹配要求方阵：矩形须补点并把缺失边设 -INF（不能设 0，会退化）
- 负权与 -INF 并存时初始化 lx=max 会把 -INF 也纳入，需逐行跳过 -INF
- 顶标更新顺序：S 中左点减 a、T 中右点加 a，写反导致相等子图变化方向错误
- way/p 数组重置：每轮 i 循环必须重置 used/minv，way 与 p 不清除会串
- 与匈牙利算法（无权增广路）同名易混：KM 是带权完美匹配 O(n³)，hungarian 是无权最大匹配 O(VE)

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/graph-matching/bigraph-weight-match/](https://oi-wiki.org/graph/graph-matching/bigraph-weight-match/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/graph-matching/bigraph-weight-match.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/graph-matching/bigraph-weight-match.md)
- CP-Algorithms ✓ [https://cp-algorithms.com/graph/hungarian-algorithm.html](https://cp-algorithms.com/graph/hungarian-algorithm.html)
- 书籍 ✓ `CPH ch20 pp191-204 (assignment problem)`
