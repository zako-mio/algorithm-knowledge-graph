---
id: matrix-rank
name: 矩阵秩
group: G-C-14
stage: advanced
priority: P2
depth_tier: standard
---

# 矩阵秩

> 高斯消元求矩阵秩，线性无关向量组最大个数

<!-- 元信息: id=matrix-rank · group=G-C-14 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

矩阵的秩是其行向量（或列向量）的极大线性无关组的大小，即线性无关向量组的最大个数。行秩=列秩=矩阵秩。通过高斯消元将矩阵化为行阶梯形，非零行数即为秩。满秩方阵可逆。秩等于矩阵标准形中1的个数。在向量空间中，秩=向量组张成空间的维数。

## Why · 为什么

### 直觉 · Intuition

秩衡量矩阵'有效信息量'。秩=2意味着第三行（或第三列）可由前两行线性表出，是'多余'的。秩越小，矩阵越'退化'。

### 原理 · Principle

高斯消元不改变矩阵的行空间（行向量张成的空间），消元后的非零行数即为秩。模质数时用逆元消元，浮点时用除法消元。

### 历史 · History

秩的概念由Frobenius在1879年系统化。行秩=列秩是线性代数基本定理。

## How · 实现

### 伪代码

```python
rank = 0
for col in 0..m-1:
  find pivot in rows rank..n-1
  if none: continue
  swap to rank, normalize, eliminate
  rank++
return rank
```

### Python 实现

```python
def matrix_rank(mat, mod=None):
    """Compute rank of a matrix via Gaussian elimination."""
    if not mat or not mat[0]:
        return 0
    n, m = len(mat), len(mat[0])
    A = [row[:] for row in mat]
    rank = 0
    for col in range(m):
        if rank >= n:
            break
        pivot = -1
        for row in range(rank, n):
            val = A[row][col]
            if mod:
                val %= mod
            if val != 0:
                pivot = row
                break
        if pivot == -1:
            continue
        A[rank], A[pivot] = A[pivot], A[rank]
        if mod:
            inv = pow(A[rank][col] % mod, mod - 2, mod)
            for j in range(m):
                A[rank][j] = A[rank][j] * inv % mod
            for r in range(n):
                if r != rank and A[r][col] % mod != 0:
                    factor = A[r][col]
                    for j in range(m):
                        A[r][j] = (A[r][j] - factor * A[rank][j]) % mod
        else:
            piv = A[rank][col]
            for j in range(m):
                A[rank][j] /= piv
            for r in range(n):
                if r != rank and abs(A[r][col]) > 1e-9:
                    factor = A[r][col]
                    for j in range(m):
                        A[r][j] -= factor * A[rank][j]
        rank += 1
    return rank

if __name__ == "__main__":
    assert matrix_rank([[1, 2, 3], [2, 4, 6], [1, 1, 1]]) == 2
    assert matrix_rank([[1, 0], [0, 1]]) == 2
    assert matrix_rank([[1, 2], [2, 4]]) == 1
    assert matrix_rank([[0, 0], [0, 0]]) == 0
    assert matrix_rank([[1]]) == 1
    # Mod arithmetic
    assert matrix_rank([[1, 2], [2, 4]], mod=10**9 + 7) == 1
    assert matrix_rank([[1, 2], [3, 4]], mod=10**9 + 7) == 2
    print("matrix-rank: ALL TESTS PASSED")

```

**PyPy 提示**: 模质数秩计算比浮点快（无精度问题）。纯Python三层循环n>100可能慢。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n*m*min(n,m)) |
| 空间 | O(n*m) |

### 局限

浮点精度影响零行判断。模非质数需辗转相消法。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3389 | 4 | 高斯消元中秩判断是核心 | [https://www.luogu.com.cn/problem/P3389](https://www.luogu.com.cn/problem/P3389) |

## Pitfalls · 易错点

- 浮点消元精度：abs(x)<1e-9判断零
- 行秩=列秩但行向量和列向量可能不同
- 满秩方阵行列式非零（可逆）
- 零矩阵的秩为0

## Sources · 信源

- CP-Algorithms ✓ [https://cp-algorithms.com/linear_algebra/rank-matrix.html](https://cp-algorithms.com/linear_algebra/rank-matrix.html)
- OI Wiki ✓ [https://oi-wiki.org/math/linear-algebra/vector-space/](https://oi-wiki.org/math/linear-algebra/vector-space/)
