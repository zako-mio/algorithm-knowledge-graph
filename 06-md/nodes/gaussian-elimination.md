---
id: gaussian-elimination
name: 高斯消元
group: G-C-14
stage: intermediate
priority: P0
depth_tier: deep
---

# 高斯消元

> O(n^3)解线性方程组/求秩/求行列式，线性代数核心算法

<!-- 元信息: id=gaussian-elimination · group=G-C-14 · stage=intermediate · priority=P0 · depth_tier=deep -->

## What · 是什么

高斯消元法通过初等行变换将矩阵化为行简化阶梯形（RREF）。三种初等变换：倍乘（某行乘非零数k）、对换（交换两行）、倍加（某行k倍加到另一行）。初等变换对应左乘初等矩阵。消元后矩阵的非零行数即为秩。增广矩阵可用于解线性方程组Ax=b。竞赛中常需模质数消元（用逆元替代除法）。

## Why · 为什么

### 直觉 · Intuition

解方程组的消元过程：把方程组的系数排成矩阵，通过行变换把矩阵化简到'一目了然'的阶梯形，然后回代求解。

### 原理 · Principle

逐列处理：对每列找非零主元，交换到当前行，用倍加消去该列其他行的元素。主元归一化后消去上下行，得到行简化阶梯形。非零行数=矩阵秩。

### 历史 · History

高斯消元法以Carl Friedrich Gauss命名，但其方法更早由中国古代《九章算术》中已有记载。是线性代数最基本的算法。

## How · 实现

### 伪代码

```python
row = 0
for col in 0..m-1:
  find pivot (nonzero) in rows row..n-1
  if none: continue
  swap to row
  normalize pivot row (divide by pivot)
  eliminate other rows
  row++
return rank = row
```

### Python 实现

```python
def gauss_eliminate(A, b=None):
    """Gaussian elimination with partial pivoting.
    A: n x m matrix, b: optional RHS vector.
    Returns (augmented_matrix, rank).
    """
    n = len(A)
    m = len(A[0])
    aug = [row[:] for row in A]
    if b is not None:
        for i in range(n):
            aug[i] = aug[i] + [b[i]]
    m2 = len(aug[0])
    row = 0
    for col in range(m):
        if row >= n:
            break
        pivot = -1
        for r in range(row, n):
            if aug[r][col] != 0:
                pivot = r
                break
        if pivot == -1:
            continue
        aug[row], aug[pivot] = aug[pivot], aug[row]
        piv = aug[row][col]
        for j in range(m2):
            aug[row][j] /= piv
        for r in range(n):
            if r != row and aug[r][col] != 0:
                factor = aug[r][col]
                for j in range(m2):
                    aug[r][j] -= factor * aug[row][j]
        row += 1
    return aug, row

def gauss_mod(A, mod):
    """Gaussian elimination under modular arithmetic (mod must be prime)."""
    n = len(A)
    m = len(A[0])
    aug = [row[:] for row in A]
    row = 0
    for col in range(m):
        if row >= n:
            break
        pivot = -1
        for r in range(row, n):
            if aug[r][col] % mod != 0:
                pivot = r
                break
        if pivot == -1:
            continue
        aug[row], aug[pivot] = aug[pivot], aug[row]
        inv = pow(aug[row][col] % mod, mod - 2, mod)
        for j in range(m):
            aug[row][j] = aug[row][j] * inv % mod
        for r in range(n):
            if r != row and aug[r][col] % mod != 0:
                factor = aug[r][col]
                for j in range(m):
                    aug[r][j] = (aug[r][j] - factor * aug[row][j]) % mod
        row += 1
    return aug, row

if __name__ == "__main__":
    aug, rank = gauss_eliminate([[1, 1], [1, 0]])
    assert rank == 2
    aug2, rank2 = gauss_eliminate([[1, 2, 3], [2, 4, 6], [1, 1, 1]])
    assert rank2 == 2
    # With RHS
    aug3, rank3 = gauss_eliminate([[2, 1], [1, 3]], b=[3, 5])
    assert rank3 == 2
    assert abs(aug3[0][2] - 0.8) < 1e-6
    assert abs(aug3[1][2] - 1.4) < 1e-6
    # Modular
    aug4, rank4 = gauss_mod([[1, 1], [1, 0]], 10**9 + 7)
    assert rank4 == 2
    print("gaussian-elimination: ALL TESTS PASSED")

```

**PyPy 提示**: 模质数时用pow(pivot,mod-2,mod)求逆元。浮点消元需注意精度，模运算无精度问题。三层循环Python慢，n>100建议PyPy。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n^3) |
| 空间 | O(n^2) |

### 局限

浮点数精度问题（可改用分数运算）。模非质数时需辗转相消法。高消不能直接处理异或方程组（需bitset优化）。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3389 | 4 | 高斯消元解线性方程组模板题 | [https://www.luogu.com.cn/problem/P3389](https://www.luogu.com.cn/problem/P3389) |
| Luogu | P4452 | 6 | 高斯消元在计数中的应用 | [https://www.luogu.com.cn/problem/P4452](https://www.luogu.com.cn/problem/P4452) |
| LeetCode | 1030 | 3 | 简单矩阵距离排序（入门） | [https://leetcode.cn/problems/matrix-cells-in-distance-order/](https://leetcode.cn/problems/matrix-cells-in-distance-order/) |

## Pitfalls · 易错点

- 浮点精度：abs(x)<1e-9判断零而非==0
- 模质数消元中逆元计算需mod为质数
- 自由变量处理：秩<变量数时有无穷多解
- 部分主元选择可减少浮点误差

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/linear-algebra/elementary-operations/](https://oi-wiki.org/math/linear-algebra/elementary-operations/)
- CP-Algorithms ✓ [https://cp-algorithms.com/linear_algebra/linear-system-gauss.html](https://cp-algorithms.com/linear_algebra/linear-system-gauss.html)
- 书籍 ✓ `CPH ch23 Matrices (p227-234)`
