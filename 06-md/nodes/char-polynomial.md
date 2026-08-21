---
id: char-polynomial
name: 特征多项式
group: G-C-14
stage: advanced
priority: P2
depth_tier: standard
---

# 特征多项式

> det(λI-A)，特征值与Cayley-Hamilton定理，线性递推加速基础

<!-- 元信息: id=char-polynomial · group=G-C-14 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

特征多项式定义为p_A(λ)=det(λI-A)，是关于λ的n次首一多项式。其根为矩阵A的特征值。特征值之和=迹(A)，乘积=det(A)（韦达定理）。Cayley-Hamilton定理：矩阵满足自身的特征方程，即p_A(A)=0。此定理可用于加速线性递推：将A^n表示为A^0..A^(n-1)的线性组合（系数来自特征多项式），配合多项式取模可将O(n)降为O(n^2)或O(n log n)。

## Why · 为什么

### 直觉 · Intuition

特征值是线性变换中'方向不变'的伸缩倍数。特征多项式的根（特征值）描述了变换的'本质频率'。Cayley-Hamilton定理说明矩阵'满足自身的方程'。

### 原理 · Principle

Faddeev-LeVerrier算法递推计算特征多项式系数：M_0=I, M_k=A*M_{k-1}+c_{k-1}*I, c_k=-trace(M_k)/k。Cayley-Hamilton保证A^n可由低次幂线性表出。

### 历史 · History

特征多项式概念源于特征值问题。Cayley-Hamilton定理由Cayley(1858)和Hamilton证明。Faddeev-LeVerrier算法是O(n^3)求系数的方法。

## How · 实现

### 伪代码

```python
Faddeev-LeVerrier:
  M = I, c[0] = 1
  for k in 1..n:
    M = A * M
    c[k] = -trace(M) / k
    M = M + c[k] * I
```

### Python 实现

```python
def mat_mul_simple(A, B, mod=None):
    n, m = len(A), len(A[0])
    k = len(B[0])
    C = [[0] * k for _ in range(n)]
    for i in range(n):
        for j in range(k):
            s = 0
            for t in range(m):
                s += A[i][t] * B[t][j]
            if mod:
                s %= mod
            C[i][j] = s
    return C

def char_polynomial_coefficients(A, mod=None):
    """Compute coefficients of characteristic polynomial det(xI - A)
    using Faddeev-LeVerrier algorithm.
    Returns [c_0, c_1, ..., c_n] where char poly = c_0*x^n + c_1*x^(n-1) + ... + c_n.
    Actually returns [1, c1, c2, ...] where poly = x^n + c1*x^(n-1) + ... + cn.
    """
    n = len(A)
    I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    M = [row[:] for row in I]
    coeffs = [0] * (n + 1)
    coeffs[0] = 1
    for k in range(1, n + 1):
        MK = mat_mul_simple(A, M, mod)
        trace = sum(MK[i][i] for i in range(n))
        if mod:
            ck = (-trace * pow(k, mod - 2, mod)) % mod
        else:
            ck = -trace / k
        coeffs[k] = ck
        for i in range(n):
            MK[i][i] += ck
        M = MK
    return coeffs

def cayley_hamilton_check(A):
    """Verify Cayley-Hamilton: p(A) = 0 where p is char poly."""
    n = len(A)
    coeffs = char_polynomial_coefficients(A)
    # Compute p(A) = sum(coeffs[k] * A^(n-k)) for k=0..n
    # A^0 = I
    I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    result = [[0] * n for _ in range(n)]
    Ak = [row[:] for row in I]  # A^0
    for k in range(n + 1):
        # Add coeffs[k] * A^(n-k)
        power = n - k
        Ap = [row[:] for row in I]
        for _ in range(power):
            Ap = mat_mul_simple(Ap, A)
        for i in range(n):
            for j in range(n):
                result[i][j] += coeffs[k] * Ap[i][j]
    # Check if result is zero
    for i in range(n):
        for j in range(n):
            if abs(result[i][j]) > 1e-6:
                return False
    return True

if __name__ == "__main__":
    # 2x2: char poly of [[1,2],[3,4]] is x^2 - 5x - 2
    coeffs = char_polynomial_coefficients([[1, 2], [3, 4]])
    assert abs(coeffs[0] - 1) < 1e-6
    assert abs(coeffs[1] - (-5)) < 1e-6
    assert abs(coeffs[2] - (-2)) < 1e-6
    # Identity matrix: char poly = (x-1)^n
    coeffs2 = char_polynomial_coefficients([[1, 0], [0, 1]])
    assert abs(coeffs2[0] - 1) < 1e-6
    assert abs(coeffs2[1] - (-2)) < 1e-6
    assert abs(coeffs2[2] - 1) < 1e-6
    # 3x3
    coeffs3 = char_polynomial_coefficients([[2, 0, 0], [0, 3, 0], [0, 0, 4]])
    assert abs(coeffs3[0] - 1) < 1e-6
    assert abs(coeffs3[1] - (-9)) < 1e-6
    assert abs(coeffs3[2] - 26) < 1e-6
    assert abs(coeffs3[3] - (-24)) < 1e-6
    # Cayley-Hamilton check
    assert cayley_hamilton_check([[1, 2], [3, 4]])
    assert cayley_hamilton_check([[2, 0], [0, 3]])
    print("char-polynomial: ALL TESTS PASSED")

```

**PyPy 提示**: Faddeev-LeVerrier涉及矩阵乘法O(n^3)*n步=O(n^4)。竞赛中更多用于理论分析（Cayley-Hamilton加速递推）而非直接计算。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n^4)（Faddeev-LeVerrier） |
| 空间 | O(n^2) |

### 局限

直接计算特征多项式系数O(n^4)较慢。特征值可能为复数。大矩阵计算精度问题。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3939 | 6 | 线性递推加速（特征多项式应用） | [https://www.luogu.com.cn/problem/P3939](https://www.luogu.com.cn/problem/P3939) |

## Pitfalls · 易错点

- 特征值可能为复数，实矩阵不一定有实特征值
- 代数重数（特征多项式中根的重数）≥几何重数（特征子空间维数）
- Cayley-Hamilton保证A^n可降次，但系数计算需精确
- 浮点计算特征值有精度问题

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/linear-algebra/char-poly/](https://oi-wiki.org/math/linear-algebra/char-poly/)
- 书籍 ✓ `线性代数教材`
