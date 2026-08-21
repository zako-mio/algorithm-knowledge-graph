---
id: vector-space
name: 向量空间
group: G-C-14
stage: advanced
priority: P2
depth_tier: standard
---

# 向量空间

> 线性空间、基与维数，线性基与矩阵秩的理论基础

<!-- 元信息: id=vector-space · group=G-C-14 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

向量空间（线性空间）是由向量集合V、域P、加法和数乘组成的代数结构。满足8条公理（加法群公理+数乘公理）。核心概念：线性相关/无关、极大线性无关组（基）、维数、子空间、线性包（张成空间）。矩阵的行向量/列向量张成行空间/列空间，其维数即为矩阵秩。OI中常用GF(2)域上的向量空间（异或空间）和实数域上的向量空间。

## Why · 为什么

### 直觉 · Intuition

三维空间中的任意向量可用3个基向量i,j,k表示。推广到n维：用最少的基向量描述整个空间，基的个数就是维数。'多余'的向量（可被其他表出）是线性相关的。

### 原理 · Principle

线性无关：向量组中没有任何向量可被其余线性表出。极大线性无关组=基，基的大小=维数=秩。高斯消元不改变行空间，消元后非零行即为极大无关组。

### 历史 · History

向量空间公理由Peano(1888年)给出。线性代数基本定理：行秩=列秩=矩阵秩。

## How · 实现

### 伪代码

```python
linear_independent(vectors):
  return rank(vectors) == len(vectors)

span_dim(vectors):
  return rank(vectors)
```

### Python 实现

```python
def is_linearly_independent(vectors, mod=None):
    """Check if vectors are linearly independent by computing rank."""
    if not vectors:
        return True
    n = len(vectors)
    m = len(vectors[0])
    # Transpose: treat each vector as a row
    A = [list(v) for v in vectors]
    rank = _compute_rank(A, mod)
    return rank == n

def _compute_rank(A, mod=None):
    n, m = len(A), len(A[0])
    A = [row[:] for row in A]
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

def span_dimension(vectors, mod=None):
    """Dimension of the subspace spanned by given vectors."""
    if not vectors:
        return 0
    return _compute_rank([list(v) for v in vectors], mod)

if __name__ == "__main__":
    # Linearly independent
    assert is_linearly_independent([[1, 0], [0, 1]]) == True
    # Linearly dependent
    assert is_linearly_independent([[1, 2], [2, 4]]) == False
    # Three vectors in 2D are dependent
    assert is_linearly_independent([[1, 0], [0, 1], [1, 1]]) == False
    # Span dimension
    assert span_dimension([[1, 0], [0, 1]]) == 2
    assert span_dimension([[1, 2], [2, 4]]) == 1
    assert span_dimension([[1, 0, 0], [0, 1, 0], [0, 0, 1]]) == 3
    # Mod arithmetic
    assert is_linearly_independent([[1, 2], [3, 4]], mod=10**9 + 7) == True
    print("vector-space: ALL TESTS PASSED")

```

**PyPy 提示**: 概念性内容，Python实现为线性无关判断和维数计算，本质是高斯消元求秩。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n*m*min(n,m)) |
| 空间 | O(n*m) |

### 局限

浮点精度影响判断。模非质数需辗转相消。无限维空间不适用。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3812 | 4 | GF(2) 向量空间的基应用 | [https://www.luogu.com.cn/problem/P3812](https://www.luogu.com.cn/problem/P3812) |

## Pitfalls · 易错点

- 零向量与任意向量线性相关
- 向量个数>维数时必然线性相关
- 基不唯一但维数唯一
- GF(2)域上加减法=异或，数乘=与

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/linear-algebra/vector-space/](https://oi-wiki.org/math/linear-algebra/vector-space/)
- 书籍 ✓ `线性代数教材`
