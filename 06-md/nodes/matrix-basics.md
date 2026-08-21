---
id: matrix-basics
name: 矩阵基础
group: G-C-14
stage: intermediate
priority: P0
depth_tier: deep
---

# 矩阵基础

> 矩阵加减乘与转置，矩阵快速幂O(k^3 log n)，递推加速核心

<!-- 元信息: id=matrix-basics · group=G-C-14 · stage=intermediate · priority=P0 · depth_tier=deep -->

## What · 是什么

矩阵是按行列排列的数表。矩阵乘法遵循'左行右列'法则：C[i][j]=ΣA[i][k]*B[k][j]。矩阵乘法满足结合律但不满足交换律。利用结合律和快速幂思想，可在O(n^3 log k)内计算矩阵k次幂，用于加速线性递推（如斐波那契数列）。单位矩阵I是对角线为1其余为0的方阵。特殊矩阵包括对角矩阵、三角矩阵、对称矩阵等。

## Why · 为什么

### 直觉 · Intuition

矩阵是对数据的'打包处理'。线性方程组Ax=b中，A将未知数向量x变换为结果向量b。矩阵乘法是向量内积的推广：结果矩阵的每个元素是左矩阵一行与右矩阵一列的内积。

### 原理 · Principle

矩阵快速幂利用结合律：(A^2)^2=A^4。二进制分解指数k，每次平方矩阵并按需累乘。对于n阶方阵，每次乘法O(n^3)，共O(log k)次，总O(n^3 log k)。线性递推f(n)=c1*f(n-1)+...+ck*f(n-k)可表示为矩阵乘法，用快速幂加速到O(k^3 log n)。

### 历史 · History

矩阵概念源于线性方程组的研究。矩阵快速幂是竞赛中加速线性递推的标准方法。Strassen算法可做到O(n^2.807)但常数大，竞赛中很少使用。

## How · 实现

### 伪代码

```python
mat_mul(A, B):
  C[i][j] = sum(A[i][k]*B[k][j])

mat_pow(A, p):
  result = I (identity)
  while p > 0:
    if p & 1: result = mul(result, A)
    A = mul(A, A)
    p >>= 1
  return result
```

### Python 实现

```python
def mat_mul(A, B, mod=None):
    """Multiply matrices A (n x m) and B (m x k), optional mod."""
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

def mat_pow(A, p, mod=None):
    """Matrix fast exponentiation A^p using binary exponentiation."""
    n = len(A)
    result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    while p > 0:
        if p & 1:
            result = mat_mul(result, A, mod)
        A = mat_mul(A, A, mod)
        p >>= 1
    return result

def mat_add(A, B, mod=None):
    n, m = len(A), len(A[0])
    C = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            C[i][j] = A[i][j] + B[i][j]
            if mod:
                C[i][j] %= mod
    return C

def mat_transpose(A):
    n, m = len(A), len(A[0])
    return [[A[i][j] for i in range(n)] for j in range(m)]

if __name__ == "__main__":
    # Matrix multiplication
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    C = mat_mul(A, B)
    assert C == [[19, 22], [43, 50]], f"mat mul failed: {C}"
    # Matrix fast power (Fibonacci)
    F = [[1, 1], [1, 0]]
    result = mat_pow(F, 9)
    assert result[0][0] == 55, f"mat pow failed: {result[0][0]}"  # F(10)=55
    # With mod
    result_mod = mat_pow([[1, 1], [1, 0]], 100, 10**9 + 7)
    assert result_mod[0][0] > 0
    # Transpose
    T = mat_transpose([[1, 2, 3], [4, 5, 6]])
    assert T == [[1, 4], [2, 5], [3, 6]]
    print("matrix-basics: ALL TESTS PASSED")

```

**PyPy 提示**: PyPy的JIT对三层嵌套循环优化好。纯Python矩阵乘法比numpy慢，但竞赛环境通常无numpy。可手动展开小矩阵乘法减小常数。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 乘法O(n^3)，快速幂O(n^3 log k) |
| 空间 | O(n^2) |

### 局限

纯Python三层循环常数大，大矩阵(>100阶)可能TLE。不支持非方阵快速幂。浮点矩阵可能有精度问题。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1939 | 5 | a[k]=a[k-1]+a[k-3] 矩阵快速幂 | [https://www.luogu.com.cn/problem/P1939](https://www.luogu.com.cn/problem/P1939) |
| Luogu | P3390 | 4 | 模板题：A^k | [https://www.luogu.com.cn/problem/P3390](https://www.luogu.com.cn/problem/P3390) |
| LeetCode | 50 | 3 | 标量快速幂（矩阵快速幂简化版） | [https://leetcode.cn/problems/powx-n/](https://leetcode.cn/problems/powx-n/) |

## Pitfalls · 易错点

- 矩阵乘法不满足交换律：AB≠BA
- 快速幂结果初始化为单位矩阵I而非全0
- 取模运算在累加时进行，防止溢出
- Python大整数乘法不溢出但可能慢，需取模

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/linear-algebra/matrix/](https://oi-wiki.org/math/linear-algebra/matrix/)
- 书籍 ✓ `CPH ch23 Matrices (p227-234)`
- OI Wiki ✓ [https://oi-wiki.org/math/binary-exponentiation/](https://oi-wiki.org/math/binary-exponentiation/)
