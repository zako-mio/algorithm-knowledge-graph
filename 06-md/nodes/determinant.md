---
id: determinant
name: 行列式
group: G-C-14
stage: advanced
priority: P0
depth_tier: deep
---

# 行列式

> O(n^3)高斯消元法求行列式，矩阵树定理与计数应用基础

<!-- 元信息: id=determinant · group=G-C-14 · stage=advanced · priority=P0 · depth_tier=deep -->

## What · 是什么

行列式是方阵的一种标量运算，记det(A)或|A|。三种等价定义：全排列定义（n!项代数和）、归纳定义（按行/列展开递归）、公理化定义（满足倍乘、对换、倍加性质+单位阵行列式为1）。高斯消元法将矩阵化为上三角矩阵，行列式=对角线元素乘积（考虑行交换的符号变化）。竞赛中常需模质数求行列式（如矩阵树定理求生成树计数）。

## Why · 为什么

### 直觉 · Intuition

行列式的几何意义是矩阵变换对空间的缩放因子（体积/面积的有向变化比）。行列式为0表示矩阵不可逆（空间被压缩降维）。

### 原理 · Principle

高斯消元法：用倍加操作消去下三角部分（行列式不变），行交换改变符号。最终行列式=上三角对角线乘积×符号。模意义下用费马小定理求逆元替代除法。

### 历史 · History

行列式概念由日本数学家关孝和（17世纪）和莱布尼茨（1693年）独立提出。高斯消元法由Gauss命名。矩阵树定理（Kirchhoff定理）将行列式与图论生成树计数关联。

## How · 实现

### 伪代码

```python
det = 1
for col in 0..n-1:
  find pivot row with A[row][col]!=0
  if none: return 0
  swap rows if needed, flip det sign
  for row in col+1..n-1:
    eliminate A[row][col] using row operations
for i: det *= A[i][i]
return det
```

### Python 实现

```python
def determinant(mat, mod=None):
    """Compute determinant via Gaussian elimination. O(n^3)."""
    n = len(mat)
    A = [row[:] for row in mat]
    det = 1
    for col in range(n):
        pivot = -1
        for row in range(col, n):
            if A[row][col] != 0:
                pivot = row
                break
        if pivot == -1:
            return 0
        if pivot != col:
            A[col], A[pivot] = A[pivot], A[col]
            det = -det
        for row in range(col + 1, n):
            if A[row][col] != 0:
                if mod:
                    ratio = A[row][col] * pow(A[col][col], mod - 2, mod) % mod
                    for j in range(col, n):
                        A[row][j] = (A[row][j] - ratio * A[col][j]) % mod
                else:
                    factor = A[row][col] / A[col][col]
                    for j in range(col, n):
                        A[row][j] -= factor * A[col][j]
    for i in range(n):
        if mod:
            det = det * A[i][i] % mod
        else:
            det *= A[i][i]
    if mod:
        det = (det % mod + mod) % mod
    return det

def determinant_naive(mat):
    """Naive recursive determinant via cofactor expansion. O(n!)."""
    n = len(mat)
    if n == 1:
        return mat[0][0]
    if n == 2:
        return mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]
    det = 0
    for j in range(n):
        minor = [row[:j] + row[j+1:] for row in mat[1:]]
        det += ((-1) ** j) * mat[0][j] * determinant_naive(minor)
    return det

if __name__ == "__main__":
    assert abs(determinant([[1, 2], [3, 4]]) - (-2)) < 1e-6
    assert abs(determinant([[1, 2, 3], [4, 5, 6], [7, 8, 10]]) - (-3)) < 1e-6
    assert determinant([[1, 0], [0, 1]]) == 1
    assert determinant([[0, 0], [0, 0]]) == 0
    # Mod arithmetic
    assert determinant([[1, 2], [3, 4]], mod=10**9 + 7) == (10**9 + 7 - 2)
    # Naive comparison
    assert abs(determinant([[2, 1, 0], [1, 2, 1], [0, 1, 2]]) - 4) < 1e-6
    assert determinant_naive([[2, 1, 0], [1, 2, 1], [0, 1, 2]]) == 4
    print("determinant: ALL TESTS PASSED")

```

**PyPy 提示**: 模质数时用pow(x,mod-2,mod)求逆元。非质数模需用辗转相减或扩展GCD。纯Python三层循环n>200可能慢。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n^3) |
| 空间 | O(n^2) |

### 局限

模非质数时需特殊处理（辗转相消法）。浮点数有精度问题。朴素展开O(n!)不可行。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3313 | 6 | 树链剖分+线段树综合（行列式相关应用） | [https://www.luogu.com.cn/problem/P3313](https://www.luogu.com.cn/problem/P3313) |
| Luogu | P4111 | 5 | 矩阵树定理求生成树计数（行列式） | [https://www.luogu.com.cn/problem/P4111](https://www.luogu.com.cn/problem/P4111) |
| Luogu | P4455 | 6 | 行列式在计数中的应用 | [https://www.luogu.com.cn/problem/P4455](https://www.luogu.com.cn/problem/P4455) |

## Pitfalls · 易错点

- 行交换时需翻转det符号
- 模非质数时不能直接用费马小定理求逆元
- 浮点消元有精度问题，建议用分数或模运算
- 对角线出现0不一定行列式为0（需先消元）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/linear-algebra/determinant/](https://oi-wiki.org/math/linear-algebra/determinant/)
- CP-Algorithms ✓ [https://cp-algorithms.com/linear_algebra/determinant-gauss.html](https://cp-algorithms.com/linear_algebra/determinant-gauss.html)
- 书籍 ✓ `CPH ch23 Matrices (p227-234)`
