---
id: matrix-tree
name: 矩阵树定理
group: G-B-3
stage: advanced
priority: P2
depth_tier: standard
---

# 矩阵树定理

> Laplace矩阵任一n-1阶主子式的行列式 = 生成树个数，O(n^3)

<!-- 元信息: id=matrix-tree · group=G-B-3 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

矩阵树定理(Kirchhoff's Matrix-Tree Theorem)：无向图 G 的生成树个数等于其 Laplace 矩阵 L=D−A 的任一 n−1 阶主子式(删去第 i 行第 i 列)的行列式绝对值。其中 D 为度数矩阵(对角线上为各点度数，重边按条数计，自环忽略)，A 为邻接矩阵(A[u][v]=u 与 v 之间边数)。对带权图，若把 L 的 A 换成权重矩阵、D 换成各点关联边权和，则主子式 = 所有生成树的边权乘积之和(加权计数)。有向图也有对应版本：出度(入度)Laplace 删去第 k 行列的主子式 = 以 k 为根的根向(叶向)树形图数。

## Why · 为什么

### 直觉 · Intuition

行列式天然『合成了所有子结构之和』：对关联矩阵应用 Cauchy–Binet 公式，L 的主子式等于所有『选 n−1 条边』的方式对应的子行列式平方和，而子行列式非零当且仅当选出的边恰好构成一棵生成树(非零行列式⇔无环无孤立点)。所以行列式数值上精确等于生成树计数。

### 原理 · Principle

定义出度/入度关联矩阵 M^out、M^in(每行对应一条边，记录起点/终点)，则 L=M·M^T。由 Cauchy–Binet：det(L 删行删列)=∑_T det(M_T)^2，其中和取遍所有 n−1 条边的子集 T。可证明 det(M_T)∈{−1,0,+1}，且非零当且仅当 T 是生成树。故得生成树计数。带权版只需给每条边乘上权值。无向图: L=D−A，删任意一行一列。

### 历史 · History

Gustav Kirchhoff 于 1847 年在研究电路网络电阻时提出该定理，故又称 Kirchhoff 定理。它是代数图论中最重要的定理之一，连接了图论、线性代数与组合数学。竞赛中常用于生成树计数(模大质数)、等价电路分析、BEST 定理统计有向图欧拉回路等。

## How · 实现

### 伪代码

```python
function spanning_tree_count(n, edges):
  m = n-1
  L = zero matrix [m][m]
  for (u,v) in edges:
    if u==v: continue           # 自环忽略
    for x in (u,v): if x<m: L[x][x] += 1
    if u<m and v<m: L[u][v]-=1; L[v][u]-=1
  return |det(L)|   # 用裸高斯或 Bareiss 精确整数
```

### Python 实现

```python
def bareiss_det(a):
    """精确整数行列式 (Bareiss 消元, 无分数, O(n^3))"""
    n = len(a)
    a = [row[:] for row in a]
    if n == 0:
        return 1
    sign = 1
    prev = 1
    for k in range(n - 1):
        if a[k][k] == 0:
            for r in range(k + 1, n):
                if a[r][k] != 0:
                    a[k], a[r] = a[r], a[k]
                    sign = -sign
                    break
            else:
                return 0
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                a[i][j] = (a[i][j] * a[k][k] - a[i][k] * a[k][j]) // prev
        prev = a[k][k]
        for i in range(k + 1, n):
            a[i][k] = 0
    return sign * a[n - 1][n - 1]


def det_mod(a, mod):
    """模素数 mod 的行列式 (高斯消元, 用逆元)"""
    n = len(a)
    a = [row[:] for row in a]
    res = 1
    for i in range(n):
        if a[i][i] == 0:
            for r in range(i + 1, n):
                if a[r][i] != 0:
                    a[i], a[r] = a[r], a[i]
                    res = -res
                    break
            else:
                return 0
        res = res * a[i][i] % mod
        inv = pow(a[i][i], -1, mod)
        for r in range(i + 1, n):
            if a[r][i]:
                t = a[r][i] * inv % mod
                for c in range(i, n):
                    a[r][c] = (a[r][c] - t * a[i][c]) % mod
    return res % mod


def laplace_minor(n, edges):
    """构造删去第 n-1 行/列的 Laplace 主子式"""
    m = n - 1
    L = [[0] * m for _ in range(m)]
    for u, v in edges:
        if u == v:
            continue
        for x in (u, v):
            if x < m:
                L[x][x] += 1
        if u < m and v < m:
            L[u][v] -= 1
            L[v][u] -= 1
    return L


def spanning_tree_count(n, edges):
    """矩阵树定理: 无向(多重)图生成树个数, 精确大整数"""
    if n <= 1:
        return 1
    return bareiss_det(laplace_minor(n, edges))


def spanning_tree_count_mod(n, edges, mod):
    """带模版(答案可能很大时用 1e9+7 取模)"""
    return det_mod(laplace_minor(n, edges), mod)


if __name__ == "__main__":
    assert spanning_tree_count(3, [(0, 1), (1, 2), (0, 2)]) == 3
    K4 = [(i, j) for i in range(4) for j in range(i + 1, 4)]
    assert spanning_tree_count(4, K4) == 16
    assert spanning_tree_count(2, [(0, 1), (0, 1)]) == 2  # 重边
    assert spanning_tree_count(4, [(0, 1), (1, 2), (2, 3)]) == 1
    K5 = [(i, j) for i in range(5) for j in range(i + 1, 5)]
    assert spanning_tree_count(5, K5) == 125
    print("matrix-tree OK")

```

**PyPy 提示**: n≤500 时裸高斯消元 O(n^3) 在 PyPy 下约 0.5~1s；答案取模时用模素数高斯(需逆元)，不必用 Bareiss 大整数(大整数乘法在 Python 内层循环慢)。稀疏图生成树数可能是指数级，必须取模；纯 Python 精确大整数行列式仅适合 n≤200。注意自环对度数矩阵有贡献吗？矩阵树定理中自环不影响生成树数，直接忽略即可(见 OI-wiki)。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n^3) 高斯消元求行列式 |
| 空间 | O(n^2) |

### 局限

1) 无向图需连通，否则答案 0(行列式自然给出)；2) 重边按条数计入度数/邻接，多组重边需逐条加；3) 答案可能指数级增长，通常模大质数输出；4) 有向图版本需区分出度/入度 Laplace 与根向/叶向树形图；5) 朴素高斯消元处理非模数矩阵时需 Bareiss 或小数，Python 用模版更稳。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| SPOJ | HIGH | 3 | Highways：矩阵树定理裸题，生成树计数(64位内) | [https://www.spoj.com/problems/HIGH/](https://www.spoj.com/problems/HIGH/) |
| Luogu | P4111 | 4 | HEOI2015 小Z的房间：矩阵树定理 + 高斯消元取模模板 | [https://www.luogu.com.cn/problem/P4111](https://www.luogu.com.cn/problem/P4111) |
| Luogu | P3317 | 5 | SDOI2014 重建：带概率/权重的矩阵树定理(边权乘积的期望) | [https://www.luogu.com.cn/problem/P3317](https://www.luogu.com.cn/problem/P3317) |

## Pitfalls · 易错点

- 忘记把重边条数累计进度数矩阵与邻接矩阵
- 自环误计入影响答案(应忽略，但不影响主要结论)
- 无向图删行删列位置任意，但必须删同一行同一列(n−1 阶主子式)
- 用浮点高斯消元求大整数行列式精度丢失，应取模或用 Bareiss
- 有向图误用无向公式(需用出度/入度 Laplace 区分根向/叶向树形图)

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/matrix-tree/](https://oi-wiki.org/graph/matrix-tree/)
- CP-Algorithms ✓ [https://cp-algorithms.com/graph/kirchhoff-theorem.html](https://cp-algorithms.com/graph/kirchhoff-theorem.html)
