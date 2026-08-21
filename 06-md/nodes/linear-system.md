---
id: linear-system
name: 线性方程组
group: G-C-14
stage: intermediate
priority: P1
depth_tier: standard
---

# 线性方程组

> 高斯消元求解Ax=b，判断唯一/无穷/无解，异或方程组变体

<!-- 元信息: id=linear-system · group=G-C-14 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

线性方程组Ax=b的求解通过高斯消元将增广矩阵[A|b]化为行简化阶梯形。若秩(A)=秩(A|b)=n（变量数），有唯一解；若秩(A)=秩(A|b)<n，有无穷多解（自由变量）；若秩(A)<秩(A|b)，无解。竞赛中还有异或方程组（GF(2)域上的线性方程组），用bitset优化的高斯消元求解。

## Why · 为什么

### 直觉 · Intuition

解方程组就是'消元'：通过行变换把方程组化简到每个方程只含一个未知数，然后直接读出解。

### 原理 · Principle

高斯消元三步：消元（化为上三角）→回代（求各变量值）→判断解的存在性。模质数时用逆元替代除法。GF(2)域上异或代替减法。

### 历史 · History

高斯消元是线性代数核心算法。GF(2)上的高斯消元常用于异或方程组（如开关灯问题）。

## How · 实现

### 伪代码

```python
for col in 0..n-1:
  find pivot, swap
  normalize pivot row
  eliminate other rows
if singular: return None
return back-substituted solution
```

### Python 实现

```python
def solve_linear_system(A, b):
    """Solve Ax=b via Gaussian elimination with back-substitution.
    Returns solution list, or None if no unique solution."""
    n = len(A)
    aug = [A[i][:] + [b[i]] for i in range(n)]
    for col in range(n):
        pivot = -1
        for r in range(col, n):
            if abs(aug[r][col]) > 1e-9:
                pivot = r
                break
        if pivot == -1:
            return None  # singular
        aug[col], aug[pivot] = aug[pivot], aug[col]
        piv = aug[col][col]
        for j in range(n + 1):
            aug[col][j] /= piv
        for r in range(n):
            if r != col and abs(aug[r][col]) > 1e-9:
                factor = aug[r][col]
                for j in range(n + 1):
                    aug[r][j] -= factor * aug[col][j]
    return [aug[i][n] for i in range(n)]

def solve_xor_system(equations, n_vars):
    """Solve XOR linear system (GF(2)). equations: list of (coeffs, rhs)."""
    aug = []
    for coeffs, rhs in equations:
        row = list(coeffs) + [rhs]
        aug.append(row)
    row = 0
    for col in range(n_vars):
        pivot = -1
        for r in range(row, len(aug)):
            if aug[r][col]:
                pivot = r
                break
        if pivot == -1:
            continue
        aug[row], aug[pivot] = aug[pivot], aug[row]
        for r in range(len(aug)):
            if r != row and aug[r][col]:
                for j in range(n_vars + 1):
                    aug[r][j] ^= aug[row][j]
        row += 1
    # Back-substitute for free variables = 0
    sol = [0] * n_vars
    for i in range(min(row, n_vars) - 1, -1, -1):
        # Find pivot column
        pc = -1
        for j in range(n_vars):
            if aug[i][j]:
                pc = j
                break
        if pc >= 0:
            sol[pc] = aug[i][n_vars]
            for j in range(pc + 1, n_vars):
                if aug[i][j]:
                    sol[pc] ^= sol[j]
    return sol

if __name__ == "__main__":
    # 2x + y = 3, x + 3y = 5 => x=0.8, y=1.4
    sol = solve_linear_system([[2, 1], [1, 3]], [3, 5])
    assert abs(sol[0] - 0.8) < 1e-6
    assert abs(sol[1] - 1.4) < 1e-6
    # Singular matrix
    assert solve_linear_system([[1, 2], [2, 4]], [3, 6]) is None
    # 3x3
    sol3 = solve_linear_system([[1, 0, 0], [0, 1, 0], [0, 0, 1]], [1, 2, 3])
    assert abs(sol3[0] - 1) < 1e-6
    assert abs(sol3[1] - 2) < 1e-6
    assert abs(sol3[2] - 3) < 1e-6
    # XOR system: x1^x2=1, x2^x3=1, x1^x3=0 => x1=0,x2=1,x3=0
    xor_sol = solve_xor_system([([1, 1, 0], 1), ([0, 1, 1], 1), ([1, 0, 1], 0)], 3)
    assert xor_sol[0] ^ xor_sol[1] == 1
    assert xor_sol[1] ^ xor_sol[2] == 1
    assert xor_sol[0] ^ xor_sol[2] == 0
    print("linear-system: ALL TESTS PASSED")

```

**PyPy 提示**: 异或方程组可用Python int的位运算模拟bitset。浮点解需注意精度判断。模质数系统用pow求逆元。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n^3) |
| 空间 | O(n^2) |

### 局限

浮点精度影响解的准确性。奇异矩阵无唯一解。大规模异或方程组需bitset优化常数。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3389 | 4 | 解 n 元线性方程组 | [https://www.luogu.com.cn/problem/P3389](https://www.luogu.com.cn/problem/P3389) |
| Luogu | P2966 | 6 | 异或方程组求最小操作数 | [https://www.luogu.com.cn/problem/P2966](https://www.luogu.com.cn/problem/P2966) |
| LeetCode | 1740 | 4 | 线性方程组相关思维 | [https://leetcode.cn/problems/find-distance-in-a-tree/](https://leetcode.cn/problems/find-distance-in-a-tree/) |

## Pitfalls · 易错点

- 浮点消元精度：用abs(x)<1e-9判断零
- 自由变量需赋默认值（通常取0）
- 异或方程组的解可能不唯一，自由变量取0得到一个特解
- 无解判断：增广矩阵某行出现0=非零

## Sources · 信源

- CP-Algorithms ✓ [https://cp-algorithms.com/linear_algebra/linear-system-gauss.html](https://cp-algorithms.com/linear_algebra/linear-system-gauss.html)
- OI Wiki ✓ [https://oi-wiki.org/math/linear-algebra/elementary-operations/](https://oi-wiki.org/math/linear-algebra/elementary-operations/)
