---
id: lgv-lemma
name: LGV行列式引理
group: G-B-9
stage: advanced
priority: P3
depth_tier: brief
---

# LGV行列式引理

> Lindström-Gessel-Viennot引理，不相交路径计数

<!-- 元信息: id=lgv-lemma · group=G-B-9 · stage=advanced · priority=P3 · depth_tier=brief -->

## What · 是什么

LGV 引理（Lindström–Gessel–Viennot lemma）用于在**有向无环图**上计算若干对起终点之间的不相交路径计数。设起点集合 A={a1..an}、终点集合 B={b1..bn}，e(ai,bj) 表示从 ai 到 bj 的所有路径的边权之积之和（路径计数时边权取 1，边权可为生成函数）。则由矩阵 M[i][j]=e(ai,bj) 的行列式等于：所有从 A 到 B 的不相交路径组 S（每个 ai 恰好连到某个 bσ(i)，且各路径无公共顶点）的权值之和再乘以符号 (-1)^t(σ)。

## Why · 为什么

### 直觉 · Intuition

行列式展开是 '所有排列 σ 的带符号路径组' 的求和。含交叉的路径组（两条路径在某点 u 相交）可以成对抵消：若路径 i 与路径 j 在 u 相交，则交换它们在 u 之后的部分，得到另一条路径组，二者权值相同而排列奇偶性相反（交换了两个终点，逆序对奇偶性改变），符号相反，恰好抵消。于是剩余的就只有不相交路径组，从而 det(M) = 带符号的不相交路径组求和。若起终点满足 ai→bi 是自然对应（如单调递增的配对），则 σ 为恒等排列，符号全为正。

### 原理 · Principle

关键前提是图必须是有向无环图（保证'交换相交点之后的部分'仍合法且权重相同），且 A、B 两两互不重复。应用流程：选定合适的 A、B（通常取必经的入口/出口集合），用 DP 或组合数算出每个 e(ai,bj)，再求行列式。当配对自然（如 a1<a2<...<an 与 b1<b2<...<bn 且路径不交即对应），答案直接是 det(M)，无需处理符号。

### 历史 · History

引理由 Lindström 于 1973 年、Gessel 与 Viennot 于 1985 年分别证明/推广，是组合数学中把不相交路径与行列式联系起来的经典工具。在信息学竞赛中最常见的形式是格点棋盘上（只能向下/向右走）的路径计数，1980 年代后成为 combinatorics on lattice paths 的基本工具。

## How · 实现

### 伪代码

```python
# 网格不相交路径计数 (经典应用)
# 起点 A, 终点 B, 边权=1
# 1. 对每个 (ai, bj) 用组合数/DP 求路径数 e(ai,bj)
#    DP: dp[i][j] = dp[i-1][j] + dp[i][j-1] (带障碍)
#    无障碍时 e(ai,bj) = C(Δx+Δy, Δx)
# 2. 构造矩阵 M[i][j] = e(ai,bj)
# 3. 答案 = det(M) (配对自然时无符号问题)
# 4. 行列式用高斯消元 O(n^3) 求, 模质数下除法用逆元
```

### Python 实现

```python
MOD = 10**9 + 7


def comb(n, k):
    """组合数 C(n,k) mod MOD, n<=2000 用阶乘表"""
    fac = [1] * (n + 1)
    for i in range(1, n + 1):
        fac[i] = fac[i - 1] * i % MOD
    inv = [1] * (n + 1)
    inv[n] = pow(fac[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        inv[i - 1] = inv[i] * i % MOD
    return lambda x, y: fac[x] * inv[y] % MOD * inv[x - y] % MOD if 0 <= y <= x else 0


def det_mod(a):
    """模质数下的高斯消元行列式"""
    n = len(a)
    res = 1
    for i in range(n):
        piv = i
        while piv < n and a[piv][i] == 0:
            piv += 1
        if piv == n:
            return 0
        if piv != i:
            a[i], a[piv] = a[piv], a[i]
            res = -res
        inv = pow(a[i][i], MOD - 2, MOD)
        for j in range(i + 1, n):
            f = a[j][i] * inv % MOD
            for k in range(i, n):
                a[j][k] = (a[j][k] - f * a[i][k]) % MOD
    for i in range(n):
        res = res * a[i][i] % MOD
    return res


def lgv_paths_2(start_pts, end_pts, n_grid):
    """2x2 LGV: 格点棋盘(只能右/下)从两个起点到两个终点的
    不相交路径数. 每个 e(ai,bj) 用组合数, 行列式即答案.
    返回 (行列式, e矩阵)
    """
    C = comb(2 * n_grid, n_grid)
    M = [[0, 0], [0, 0]]
    for i in range(2):
        for j in range(2):
            x1, y1 = start_pts[i]
            x2, y2 = end_pts[j]
            dx, dy = x2 - x1, y2 - y1
            M[i][j] = C(dx + dy, dx)
    d = det_mod([row[:] for row in M])
    return d % MOD, M


if __name__ == "__main__":
    # 小棋盘: (0,0)->(1,1) 与 (0,1)->(1,2) 两条路径不交
    # 起点 (0,0),(0,1); 终点 (1,1),(1,2)
    # e((0,0),(1,1)) = C(2,1)=2 ; e((0,0),(1,2)) = C(3,1)=3
    # e((0,1),(1,1)) = C(1,1)=1 ; e((0,1),(1,2)) = C(2,1)=2
    # det = 2*2 - 3*1 = 1
    start = [(0, 0), (0, 1)]
    end = [(1, 1), (1, 2)]
    d, M = lgv_paths_2(start, end, 3)
    assert d == 1, d
    assert M == [[2, 3], [1, 2]]

    # 起点 (0,0),(0,1); 终点 (1,1),(2,1) : 第一条必经过
    # e((0,0),(1,1))=C(2,1)=2, e((0,0),(2,1))=C(3,1)=3
    # e((0,1),(1,1))=1, e((0,1),(2,1))=C(2,1)=2 => det=2*2-3*1=1
    # 实际 det = 2*1 - 3*1 = -1 (mod MOD) -> MOD-1
    d2, _ = lgv_paths_2([(0, 0), (0, 1)], [(1, 1), (2, 1)], 3)
    assert d2 == MOD - 1, d2

    print("lgv-lemma tests passed")

```

**PyPy 提示**: 核心是组合数 + 行列式。格点路径数在障碍情况下改用 O(nm) DP 预处理每个 e(ai,bj)。行列式模运算在 PyPy 下高斯消元 O(k^3) 可跑 k≤100 左右；注意 Python 二维列表逐行乘在 k 较大时用内建循环优化。组合数表若 n 很大（1e5+）需用阶乘+逆元全局预处理。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | DP 求 e 为 O(nm)（或 O(n) 组合数），行列式高斯消元 O(k^3)，k 为起点个数 |
| 空间 | O(nm + k^2) |

### 局限

只适用于 DAG；A、B 中元素必须两两不同；必须正确选择起点/终点集合（通常取必经的关键集合），选错则行列式无意义；k 较大时行列式求解成本高。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Codeforces | 348D | 4 | Turtles：网格障碍路径计数，取 A={(1,2),(2,1)}, B={(n-1,m),(n,m-1)} 应用 LGV，O(nm) DP | [https://codeforces.com/problemset/problem/348/D](https://codeforces.com/problemset/problem/348/D) |
| Luogu | U461211 | 4 | （此题为字符串哈希加强题，非 LGV 题；仅作交叉对比参考） | [https://www.luogu.com.cn/problem/U461211](https://www.luogu.com.cn/problem/U461211) |

## Pitfalls · 易错点

- 只适用于有向无环图；存在环时交换路径部分不合法
- A、B 起点/终点不能重复，集合大小必须相等
- 配对非自然时，行列式带符号，需按 σ 的逆序数取符号
- 起点终点集合选择不当会得到错误/无意义答案，选关键必经点
- 行列式需在模数下用逆元；模数为质数时简单，否则用高斯消元除法

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/lgv/](https://oi-wiki.org/graph/lgv/)
- Wikipedia ✓ [https://en.wikipedia.org/wiki/Lindström–Gessel–Viennot_lemma](https://en.wikipedia.org/wiki/Lindström–Gessel–Viennot_lemma)
