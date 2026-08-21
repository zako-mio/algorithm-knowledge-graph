---
id: dp-probability
name: 概率/期望DP
group: G-A-11
stage: intermediate
priority: P1
depth_tier: standard
---

# 概率/期望DP

> 概率顺推/期望逆推，可能需高斯消元处理环依赖

<!-- 元信息: id=dp-probability · group=G-A-11 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

概率/期望DP是用动态规划解决概率与期望问题的技术。概率问题通常用顺推（从初始状态推向结果），期望问题通常用逆推（从目标状态倒推回起始状态）。当状态转移存在后效性（环依赖）时，需用高斯消元处理线性方程组。

## Why · 为什么

### 直觉 · Intuition

概率DP：从已知概率的初始状态出发，按事件发生的概率逐步推到最终状态的获胜/成功概率。期望DP：从目标状态（期望=0）出发，倒推到达目标的期望步数。若状态间存在环依赖（如机器人在同一行左右移动），期望方程构成线性方程组，需高斯消元。

### 原理 · Principle

概率DP顺推：f(S)=sum{P(转移) * f(next_S)}，从初始状态f(S0)=1开始。期望DP逆推：f(S)=sum{P(转移) * f(next_S)} + 1，从目标f(target)=0开始倒推。期望线性性质：E[X]=sum{P(x)*x}。环依赖时：f(S)出现在自身方程中，移项后构成线性方程组 Af=b，用高斯消元求解。

### 历史 · History

概率/期望DP是竞赛数学的重要专题，结合了概率论与动态规划。OI Wiki将其分为概率DP(顺推)、期望DP(逆推)、有后效性DP(高斯消元)三部分。CF 148D(Bag of mice)和POJ 2096(Collecting Bugs)是经典教学题。NOIP2016换教室是期望DP的综合应用。

## How · 实现

### 伪代码

```python
# 概率DP(顺推)
f[S0] = 1  # 初始状态概率
for S in states (forward order):
  for next_S, p in transitions(S):
    f[next_S] += f[S] * p

# 期望DP(逆推)
f[target] = 0  # 目标状态期望
for S in states (reverse order):
  f[S] = sum(p * f[next_S]) + 1  # +1为当前步

# 有环依赖(高斯消元)
# 整理为 Af = b 后解线性方程组
```

### Python 实现

```python
def bag_of_mice(w, b):
    """CF 148D Bag of mice: 袋中w白鼠b黑鼠, 公主先抓
    公主抓到白鼠则赢; 龙抓完后老鼠可能跑出来
    返回公主赢的概率
    """
    # f[i][j] = 轮到公主时袋中i白j黑, 公主赢概率
    f = [[0.0] * (b + 1) for _ in range(w + 1)]

    for i in range(w + 1):
        for j in range(b + 1):
            if i == 0:
                f[i][j] = 0.0  # 没白鼠, 龙赢
            elif j == 0:
                f[i][j] = 1.0  # 全白鼠, 公主赢
            else:
                total = i + j
                # 公主直接抓到白鼠
                p_win = i / total
                # 公主抓黑, 龙抓白 -> 龙赢(不贡献)
                # 公主抓黑, 龙抓黑, 跑出黑 -> f[i][j-3]
                p_lose_bb = (j / total) * ((j - 1) / (total - 1)) if j >= 2 else 0
                p_case3 = p_lose_bb * ((j - 2) / (total - 2)) if j >= 3 else 0
                # 公主抓黑, 龙抓黑, 跑出白 -> f[i-1][j-2]
                p_case4 = p_lose_bb * (i / (total - 2)) if j >= 2 and total > 2 else 0
                val = p_win
                if j >= 3:
                    val += p_case3 * f[i][j - 3]
                if j >= 2 and i >= 1 and total > 2:
                    val += p_case4 * f[i - 1][j - 2]
                f[i][j] = val

    return f[w][b]


def collecting_bugs(n, s):
    """POJ 2096 Collecting Bugs: n种bug分类s个子系统
    每天发现1个bug, 属于某分类1/n概率, 属于某子系统1/s概率
    求发现所有n种分类且所有s个子系统的期望天数
    f[i][j] = 已发现i分类j子系统的期望天数
    目标 f[n][s] = 0, 答案 f[0][0]
    """
    f = [[0.0] * (s + 1) for _ in range(n + 1)]
    # 逆序: 从 f[n][s]=0 倒推
    for i in range(n, -1, -1):
        for j in range(s, -1, -1):
            if i == n and j == s:
                f[i][j] = 0.0
                continue
            # P1: 已发现的分类和子系统
            p1 = (i / n) * (j / s) if i > 0 else 0
            # P2: 已发现分类, 新子系统
            p2 = (i / n) * ((s - j) / s) if i > 0 else 0
            # P3: 新分类, 已发现子系统
            p3 = ((n - i) / n) * (j / s) if j > 0 else 0
            # P4: 新分类, 新子系统
            p4 = ((n - i) / n) * ((s - j) / s)
            # f[i][j] = 1 + p1*f[i][j] + p2*f[i][j+1] + p3*f[i+1][j] + p4*f[i+1][j+1]
            # (1-p1)*f[i][j] = 1 + p2*f[i][j+1] + p3*f[i+1][j] + p4*f[i+1][j+1]
            rhs = 1.0
            if j + 1 <= s:
                rhs += p2 * f[i][j + 1]
            if i + 1 <= n:
                rhs += p3 * f[i + 1][j]
            if i + 1 <= n and j + 1 <= s:
                rhs += p4 * f[i + 1][j + 1]
            f[i][j] = rhs / (1 - p1)

    return f[0][0]


if __name__ == "__main__":
    # CF 148D: 1白鼠1黑鼠
    # 公主抓: 1/2概率直接赢
    # 公主抓黑(1/2), 龙抓白(1/1)->龙赢
    # 所以公主赢概率=1/2
    result = bag_of_mice(1, 1)
    assert abs(result - 0.5) < 1e-9, f"Expected 0.5, got {result}"

    # 2白0黑: 公主必赢
    assert abs(bag_of_mice(2, 0) - 1.0) < 1e-9
    # 0白1黑: 公主必输
    assert abs(bag_of_mice(0, 1) - 0.0) < 1e-9

    # POJ 2096: 1分类1子系统 -> 1天
    result2 = collecting_bugs(1, 1)
    assert abs(result2 - 1.0) < 1e-9, f"Expected 1.0, got {result2}"

    # 2分类1子系统: f[0][0]=1/(1-0) + ... 
    # f[0][0] = (1 + 1*f[1][0]) / (1-0) ; f[1][0] = (1 + 0.5*f[1][0]) / 0.5 -> f[1][0]=2
    # f[0][0] = 1 + 2 = 3
    result3 = collecting_bugs(2, 1)
    assert abs(result3 - 3.0) < 1e-9, f"Expected 3.0, got {result3}"

    print("All tests passed.")

```

**PyPy 提示**: PyPy对浮点数运算和二维列表访问快。概率/期望DP的状态数通常不大(n*m<=1e4)，PyPy足够。高斯消元部分需注意精度(eps=1e-9)。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(状态数 * 转移数)；高斯消元O(状态数³) |
| 空间 | O(状态数) |

### 局限

有环依赖时状态方程构成线性方程组，状态数>500时高斯消元O(n³)可能慢。浮点精度问题需注意。期望DP逆推方向容易搞反。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Codeforces | 148D | 3 | Bag of mice：概率DP顺推经典题 | [https://codeforces.com/problemset/problem/148/D](https://codeforces.com/problemset/problem/148/D) |
| POJ | 2096 | 3 | Collecting Bugs：期望DP逆推经典题 | [http://poj.org/problem?id=2096](http://poj.org/problem?id=2096) |
| Luogu | P2473 | 4 | SCOI2008 奖励关：期望DP+状压，逆序递推 | [https://www.luogu.com.cn/problem/P2473](https://www.luogu.com.cn/problem/P2473) |

## Pitfalls · 易错点

- 概率DP用顺推(从初始状态)，期望DP用逆推(从目标状态)，方向搞反导致错误
- 有环依赖时f(S)出现在自身方程中，需移项后用高斯消元
- 边界条件：概率题中不可能的状态概率为0，期望题中目标状态期望为0
- 浮点精度：概率乘法累积误差，建议用double而非float

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/dp/probability/](https://oi-wiki.org/dp/probability/)
- CP-Algorithms ✓ [https://cp-algorithms.com/dynamic_programming/knapsack.html](https://cp-algorithms.com/dynamic_programming/knapsack.html)
