---
id: diagonalization
name: 矩阵对角化
group: G-C-14
stage: advanced
priority: P2
depth_tier: standard
---

# 矩阵对角化

> A=PDP^{-1}，矩阵快速幂优化，特征值分解

<!-- 元信息: id=diagonalization · group=G-C-14 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

矩阵对角化是将方阵A表示为A=PDP^{-1}，其中D为对角矩阵（对角线元素为特征值），P的列向量为对应特征向量。可对角化条件：A有n个线性无关的特征向量（等价于每个特征值的代数重数=几何重数，或最小多项式无重根）。对角化后A^k=PD^kP^{-1}，D^k只需对角线元素k次幂，可加速矩阵快速幂。相似变换A→P^{-1}AP不改变特征多项式。

## Why · 为什么

### 直觉 · Intuition

对角化是找到'最佳视角'看线性变换。在对角矩阵对应的基下，变换只是各方向独立伸缩。A^k=PD^kP^{-1}让幂运算变得简单。

### 原理 · Principle

求特征值λ（解det(λI-A)=0）→求特征向量v（解(λI-A)v=0）→组装P和D→验证A=PDP^{-1}。有n个线性无关特征向量则可对角化。

### 历史 · History

特征值/特征向量概念源于线性变换研究。对角化是线性代数核心内容。Cayley-Hamilton定理与对角化密切相关。

## How · 实现

### 伪代码

```python
1. Compute eigenvalues: det(lambda*I - A) = 0
2. For each eigenvalue, find eigenvectors
3. If n linearly independent eigenvectors exist:
   P = [v1, v2, ..., vn], D = diag(lambda1, ..., lambdan)
4. A^k = P * D^k * P^(-1)
```

### Python 实现

```python
import math

def eigenvalues_2x2(A):
    """Compute eigenvalues of a 2x2 matrix."""
    a, b = A[0][0], A[0][1]
    c, d = A[1][0], A[1][1]
    trace = a + d
    det = a * d - b * c
    disc = trace * trace - 4 * det
    if disc < 0:
        return None  # Complex eigenvalues
    sqrt_disc = math.sqrt(disc)
    return [(trace + sqrt_disc) / 2, (trace - sqrt_disc) / 2]

def is_diagonalizable(A):
    """Check if 2x2 matrix is diagonalizable over R."""
    n = len(A)
    if n != 2:
        return "Only 2x2 implemented"
    eigs = eigenvalues_2x2(A)
    if eigs is None:
        return False  # Complex eigenvalues
    lambda1, lambda2 = eigs
    if abs(lambda1 - lambda2) < 1e-9:
        # Repeated eigenvalue: diagonalizable iff A is already diagonal
        return abs(A[0][1]) < 1e-9 and abs(A[1][0]) < 1e-9
    return True  # Distinct real eigenvalues => diagonalizable

def diagonalize_2x2(A):
    """Diagonalize 2x2 matrix: A = P * D * P^(-1).
    Returns (P, D) or None if not diagonalizable."""
    if not is_diagonalizable(A):
        return None
    eigs = eigenvalues_2x2(A)
    if eigs is None:
        return None
    lambda1, lambda2 = eigs
    D = [[lambda1, 0], [0, lambda2]]
    # Find eigenvectors
    # (A - lambda*I) * v = 0
    P = [[0, 0], [0, 0]]
    for idx, lam in enumerate([lambda1, lambda2]):
        # A - lam*I = [[a-lam, b], [c, d-lam]]
        a_lam = A[0][0] - lam
        b_val = A[0][1]
        if abs(b_val) > 1e-9:
            P[0][idx] = b_val
            P[1][idx] = -a_lam
        else:
            c_val = A[1][0]
            if abs(c_val) > 1e-9:
                P[0][idx] = -(A[1][1] - lam)
                P[1][idx] = c_val
            else:
                P[0][idx] = 1
                P[1][idx] = 0
    return P, D

def mat_inv_2x2(M):
    a, b = M[0][0], M[0][1]
    c, d = M[1][0], M[1][1]
    det = a * d - b * c
    if abs(det) < 1e-12:
        return None
    return [[d / det, -b / det], [-c / det, a / det]]

def mat_mul_2x2(A, B):
    return [[A[0][0]*B[0][0]+A[0][1]*B[1][0], A[0][0]*B[0][1]+A[0][1]*B[1][1]],
            [A[1][0]*B[0][0]+A[1][1]*B[1][0], A[1][0]*B[0][1]+A[1][1]*B[1][1]]]

if __name__ == "__main__":
    # Diagonal matrix is trivially diagonalizable
    assert is_diagonalizable([[2, 0], [0, 3]]) == True
    # Non-diagonalizable (repeated eigenvalue, not diagonal)
    assert is_diagonalizable([[1, 1], [0, 1]]) == False
    # Distinct eigenvalues
    assert is_diagonalizable([[1, 2], [3, 4]]) == True
    # Complex eigenvalues
    assert is_diagonalizable([[0, -1], [1, 0]]) == False  # eigenvalues ±i
    # Diagonalize and verify
    A = [[4, 1], [2, 3]]
    result = diagonalize_2x2(A)
    assert result is not None
    P, D = result
    Pinv = mat_inv_2x2(P)
    assert Pinv is not None
    # Verify A = P * D * P^(-1)
    PD = mat_mul_2x2(P, D)
    PDPinv = mat_mul_2x2(PD, Pinv)
    for i in range(2):
        for j in range(2):
            assert abs(PDPinv[i][j] - A[i][j]) < 1e-6, f"Diag verify failed: {PDPinv[i][j]} != {A[i][j]}"
    print("diagonalization: ALL TESTS PASSED")

```

**PyPy 提示**: 仅实现2x2对角化作为教学。大矩阵对角化需数值方法（QR算法等），竞赛中很少直接实现。主要用于理论理解。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 求特征值O(n^3)（数值方法），对角化验证O(n^3) |
| 空间 | O(n^2) |

### 局限

不是所有矩阵都可对角化（如Jordan块）。特征值可能为复数。大矩阵对角化需数值近似。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1939 | 5 | 矩阵快速幂（对角化可优化但竞赛直接快速幂更通用） | [https://www.luogu.com.cn/problem/P1939](https://www.luogu.com.cn/problem/P1939) |

## Pitfalls · 易错点

- 不是所有矩阵可对角化：重复特征值需检查几何重数=代数重数
- 特征值可能是复数
- P的列必须是线性无关的特征向量
- A^k=PD^kP^{-1}要求P可逆

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/linear-algebra/diagonalization/](https://oi-wiki.org/math/linear-algebra/diagonalization/)
- OI Wiki ✓ [https://oi-wiki.org/math/linear-algebra/char-poly/](https://oi-wiki.org/math/linear-algebra/char-poly/)
