---
id: dp-opt-overview
name: DP优化概述
group: G-A-12
stage: intermediate
priority: P1
depth_tier: standard
---

# DP优化概述

> 利用数据结构/数学性质/状态设计降低DP转移复杂度

<!-- 元信息: id=dp-opt-overview · group=G-A-12 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

DP 优化的总目标是降低转移时间复杂度。朴素 DP 常因枚举全部决策 j 而达到 O(n²) 甚至更高。优化手段按性质分类：①数据结构加速（前缀和、线段树、树状数组、单调队列/栈、平衡树、堆）；②数学性质（决策单调性/四边形不等式/斜率优化/WQS二分、矩阵快速幂加速线性递推）；③状态设计（状态压缩、滚动数组降空间、卷积/FFT 加速组合转移、倍增优化）。多数优化把「对每个状态枚举所有决策」变为「用数据结构或单调性快速求最优决策」。

## Why · 为什么

### 直觉 · Intuition

朴素转移 f(i) = min_j { g(j) + w(j,i) } 里 j 的自由度是 O(n)。优化的本质是看到 w(j,i) 的结构——若 w 是「可累加」的（前缀和），或决策值 j 单调排列，或目标函数在平面上是凸的，就可以不用枚举 j 而直接算出最优。把「穷举」变成「维护一个有序集合 + 查询」，往往从 O(n²) 降到 O(n log n) 或 O(n)。

### 原理 · Principle

OI Wiki 将 DP 优化分为两型：型一 f(i)=F(a_i, {f(j): j<i})——维护一个数据结构，每次计算 f(i) 视为一次查询，算完插入，典型如前缀和优化、单调队列优化、斜率优化（凸壳）；型二 f(i,·)=F(a_i, f(i-1,·))——状态本身是大对象（数组/集合），需优化单次转移，如状态压缩、SOS DP、用树状数组/线段树做范围转移。另一个分类维度：转移值优化（降空间，滚动数组）与转移时间优化（降时间复杂度）。判断能否优化：观察 w(j,i) 是否满足可分解/可二分/凸性/单调性。

### 历史 · History

DP 优化随竞赛发展逐步系统化：1970s Knuth 提出 Knuth 优化（四边形不等式）；1980s-90s 斜率优化在 USACO/IOI 出现（如 1997 年 IOI 类似题）；2000s 后 OI Wiki 将其整理为「DP 优化」专章，覆盖数据结构加速、单调队列、斜率、四边形不等式、WQS 二分、Slope Trick、矩阵快速幂等。CP-Algorithms 亦系统收录 Divide and Conquer DP 与 Knuth's Optimization。

## How · 实现

### 伪代码

```python
# 优化选型速查
# w(j,i) 可拆成 (A_i 项) + (B_j 项) + (C_i*D_j 交叉项) -> 斜率优化
# w(j,i) 是滑动窗口区间最值         -> 单调队列
# opt(i) 单调 + w 满足四边形不等式   -> 分治优化 / Knuth / 二分队列
# 转移是简单加和（区间和）          -> 前缀和优化
# 递推可写成矩阵（线性）            -> 矩阵快速幂
# 只关心上一步状态                 -> 滚动数组

判断决策单调性步骤:
1. 写出 f(i)=min_j {f(j)+w(j,i)}
2. 验证 w 是否满足四边形不等式 (a<=b<=c<=d => w(a,c)+w(b,d)<=w(a,d)+w(b,c))
3. 满足 -> 使用决策单调性优化
```

### Python 实现

```python
def prefix_sum_opt(a):
    """前缀和优化 DP 演示：f[i] = 前 i 项中最小子段和，O(n)。
    对应 w(j,i)=sum(a[j+1..i]) 可拆成前缀和差，避免每段重算。"""
    n = len(a)
    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + a[i]
    # 经典 O(n)：维护前缀最小前缀和
    min_pref = 0
    best = float('-inf')
    for i in range(1, n + 1):
        best = max(best, pref[i] - min_pref)
        min_pref = min(min_pref, pref[i])
    return best


def monotonic_queue_dp(a, k):
    """单调队列优化：f[i] = max(a[i-k..i]) 滑动窗口最值，O(n)。
    是 DP 优化里最基础的「维护候选集」模板。"""
    from collections import deque
    dq = deque()
    res = []
    for i, x in enumerate(a):
        while dq and dq[0] < i - k:
            dq.popleft()
        while dq and a[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        res.append(a[dq[0]])
    return res


def rolling_array(dp0, dp1):
    """滚动数组演示：只保留上一行，空间 O(n)。
    通常用于背包等 f[i][j] 只依赖 f[i-1][*] 的转移。"""
    return dp1, dp0


def matrix_pow_transfer(trans, steps):
    """矩阵快速幂优化线性递推：f_{n+1} = M * f_n。
    O(log n) 次矩阵乘代替 O(n) 次迭代。"""
    def mul(A, B):
        k = len(A)
        C = [[0] * k for _ in range(k)]
        for i in range(k):
            Ai = A[i]
            Ci = C[i]
            for t in range(k):
                if Ai[t]:
                    Bt = B[t]
                    for j in range(k):
                        Ci[j] += Ai[t] * Bt[j]
        return C
    k = len(trans)
    res = [[1 if i == j else 0 for j in range(k)] for i in range(k)]
    while steps:
        if steps & 1:
            res = mul(res, trans)
        trans = mul(trans, trans)
        steps >>= 1
    return res


if __name__ == "__main__":
    # 前缀和优化：最大子段和
    a = [3, -1, 2, -5, 4, 6, -2]
    assert prefix_sum_opt(a) == 10  # 4+6
    assert prefix_sum_opt([-3, -1, -2]) == -1
    # 单调队列滑动窗口
    a = [1, 3, -1, -3, 5, 3, 6, 7]
    assert monotonic_queue_dp(a, 3) == [1, 3, 3, 3, 5, 5, 6, 7]
    # 矩阵快速幂：Fibonacci（M=[[1,1],[1,0]]）
    M = [[1, 1], [1, 0]]
    f = matrix_pow_transfer(M, 10)  # F_10 = 55
    assert f[0][0] == 89 and f[0][1] == 55
    print("All tests passed.")
```

**PyPy 提示**: Python 中 DP 优化选型：n≤1e5 用 O(n log n) 单调队列/斜率/分治均安全；矩阵乘法用纯 Python 需注意常数，n 大（矩阵维数高）建议用 numpy（竞赛环境一般无）。优先做时间复杂度优化（O(n²)→O(n log n)），空间滚动次之。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 随方法不同：O(n)、O(n log n) 或 O(n log C)（WQS/二分）；相比朴素 O(n²) 均大幅下降 |
| 空间 | 多为 O(n)；滚动数组可降至 O(k) |

### 局限

优化手段各有适用前提：单调队列需窗口右端点递增、斜率需凸性与决策横坐标/斜率单调（否则需 CDQ/平衡树）、四边形不等式需验证 w 的凸性、矩阵快速幂仅限线性递推。识别转移结构是前提，选错优化会得到错误答案。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1776 | 5 | 宝物筛选：单调队列优化多重背包，DP优化入门综合题 | [https://www.luogu.com.cn/problem/P1776](https://www.luogu.com.cn/problem/P1776) |
| Luogu | P1886 | 3 | 滑动窗口/单调队列：数据结构加速最值查询的基础模板 | [https://www.luogu.com.cn/problem/P1886](https://www.luogu.com.cn/problem/P1886) |
| Luogu | P1397 | 5 | NOI2013 矩阵游戏：矩阵快速幂优化 DP 递推 | [https://www.luogu.com.cn/problem/P1397](https://www.luogu.com.cn/problem/P1397) |

## Pitfalls · 易错点

- 先写朴素 DP 确认转移结构，再套优化——跳过朴素直接套优化易把式子写错
- 混淆「优化转移时间」与「优化状态空间」（滚动数组不能降低时间复杂度）
- 忘记验证单调性/凸性前提就套用斜率优化或四边形不等式
- 数据结构优化时未把「查询/插入」顺序对齐转移依赖（先查后插）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/dp/opt/dp-opt/](https://oi-wiki.org/dp/opt/dp-opt/)
- CP-Algorithms ✓ [https://cp-algorithms.com/dynamic_programming/divide-and-conquer-dp.html](https://cp-algorithms.com/dynamic_programming/divide-and-conquer-dp.html)
