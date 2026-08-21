---
id: dp-count
name: 计数DP
group: G-A-11
stage: intermediate
priority: P1
depth_tier: standard
---

# 计数DP

> 利用DP记忆化求计数问题，划分子集不重不漏

<!-- 元信息: id=dp-count · group=G-A-11 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

计数DP是一种利用类似DP的记忆化方法解决计数（和求和）问题的技术。与最优化DP的关键区别在于：计数问题要求将状态空间划分为若干两两无交的子集（不重不漏），而最优化DP只需子集的并覆盖全集即可。典型问题包括整数划分、路径计数、组合数计算等。

## Why · 为什么

### 直觉 · Intuition

如果集合S可以划分为两两无交的子集S1,S2,...,Sk，则|S|=|S1|+|S2|+...+|Sk|。关键是找到一种划分方式使得每个子集的计数与原问题同构（规模更小的同类问题），从而可以用记忆化递推求解。

### 原理 · Principle

基本范式：f(S)=sum{f(S_i)} 其中S=并集(S_i)且S_i两两无交。与最优化DP的区别：max可以取任意划分(只需覆盖全集)，但计数要求不重不漏。整数划分：f(n,M)=f(n,M-1)+f(n-M,M)（含M与不含M两类，不重叠）。状态转移方程确定后用递推或记忆化搜索计算。

### 历史 · History

计数DP是竞赛中处理大规模计数问题的核心技术。OI Wiki将其与最优化DP对比，强调了「不重不漏」的划分要求。整数划分问题是最经典的计数DP教学案例，从O(n²)到O(n^{3/2})有多种优化。

## How · 实现

### 伪代码

```python
# 整数划分(顺序不同算同一种)
# f(n, M) = 将n划分为不超过M的正整数的方案数
f(n, M) = f(n, M-1) + f(n-M, M) if n >= M else f(n, M-1)
# 边界: f(0, M)=1, f(n, 0)=0 (n>0)
# 优化: 滚动数组
```

### Python 实现

```python
def integer_partition(n):
    """整数划分: 将n划分为若干正整数之和的方案数(顺序无关)
    如 n=4: 4=3+1=2+2=2+1+1=1+1+1+1, 共5种
    f(n, M) = f(n, M-1) + f(n-M, M)  (不含M + 含M)
    """
    f = [0] * (n + 1)
    f[0] = 1
    for M in range(1, n + 1):  # 枚举最大数
        for j in range(M, n + 1):
            f[j] += f[j - M]
    return f[n]


def integer_partition_ordered(n):
    """有序整数划分(顺序不同算不同种)
    如 n=4: 1+1+1+1, 1+1+2, 1+2+1, 2+1+1, 1+3, 3+1, 2+2, 4 = 8种
    g(n) = 2^(n-1) (n>=1)
    """
    if n == 0:
        return 1
    return 1 << (n - 1)


def count_paths(n, m):
    """网格路径计数: 从(0,0)到(n-1,m-1)只向下向右走的方案数
    C(n+m-2, n-1)
    """
    f = [[0] * m for _ in range(n)]
    f[0][0] = 1
    for i in range(n):
        for j in range(m):
            if i > 0:
                f[i][j] += f[i - 1][j]
            if j > 0:
                f[i][j] += f[i][j - 1]
    return f[n - 1][m - 1]


if __name__ == "__main__":
    # 整数划分测试
    assert integer_partition(4) == 5, f"Expected 5, got {integer_partition(4)}"
    assert integer_partition(1) == 1
    # 5的划分: {5},{4,1},{3,2},{3,1,1},{2,2,1},{2,1,1,1},{1,1,1,1,1} = 7
    assert integer_partition(5) == 7, f"Expected 7, got {integer_partition(5)}"
    assert integer_partition(6) == 11

    # 有序划分
    assert integer_partition_ordered(4) == 8
    assert integer_partition_ordered(1) == 1

    # 路径计数
    assert count_paths(3, 3) == 6  # C(4,2)=6
    assert count_paths(2, 2) == 2
    assert count_paths(1, 1) == 1

    print("All tests passed.")

```

**PyPy 提示**: PyPy对列表操作和整数加法快，n=5000的整数划分约0.1s。注意结果可能很大，Python天然支持大整数无需取模处理。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 整数划分: O(n²) → O(n^{3/2})优化；路径计数: O(nm) |
| 空间 | O(n) 滚动数组 |

### 局限

结果可能极大需取模。整数划分O(n²)在n>1e4时Python慢。计数DP的正确性核心在于不重不漏的划分证明，容易出错。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1025 | 2 | NOIP2001 数的划分：将n划分为k个正整数的方案数，计数DP | [https://www.luogu.com.cn/problem/P1025](https://www.luogu.com.cn/problem/P1025) |
| LeetCode | 62 | 1 | 不同路径：网格路径计数DP入门 | [https://leetcode.cn/problems/unique-paths/](https://leetcode.cn/problems/unique-paths/) |

## Pitfalls · 易错点

- 划分不重不漏是正确性的关键：确保子集两两无交，否则会重复计数
- 整数划分中「有序」vs「无序」的状态转移方程完全不同
- 结果可能溢出：Python天然大整数，其他语言需取模
- 边界f(0)=1（空集是一种方案）容易遗漏

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/dp/count/](https://oi-wiki.org/dp/count/)
- CP-Algorithms ✓ [https://cp-algorithms.com/dynamic_programming/knapsack.html](https://cp-algorithms.com/dynamic_programming/knapsack.html)
