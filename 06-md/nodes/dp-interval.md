---
id: dp-interval
name: 区间DP
group: G-A-11
stage: intermediate
priority: P0
depth_tier: deep
---

# 区间DP

> f(i,j)表示区间[i,j]最优，枚举合并点k，O(n^3)

<!-- 元信息: id=dp-interval · group=G-A-11 · stage=intermediate · priority=P0 · depth_tier=deep -->

## What · 是什么

区间DP是一种以区间为状态定义的动态规划：状态 f(i,j) 表示将区间 [i,j] 内所有元素通过某种合并方式处理后的最优值。转移时枚举合并点 k，将 [i,k] 和 [k+1,j] 两部分的最优解合并。典型问题如石子合并、矩阵链乘法。

## Why · 为什么

### 直觉 · Intuition

当问题本质是「将若干部分合并」时，最终的最优合并方案一定是在某个位置 k 处将区间分成左右两部分分别合并——这就是区间DP的决策点。由于左右子区间的长度都严格小于原区间，按长度递增枚举即可保证无后效性。

### 原理 · Principle

状态转移方程：f(i,j)=max{f(i,k)+f(k+1,j)+cost(i,j)}，其中 i<=k<j，cost(i,j) 为合并 [i,j] 两部分的代价（如区间和）。按区间长度 len 从 2 到 n 枚举，再枚举起点 i（j=i+len-1），最后枚举合并点 k。时间复杂度 O(n³)。环上问题将数组复制为 2n，在长度 2n 的链上做区间DP，最后取 min/max f(1,n)...f(n,2n-1)。

### 历史 · History

区间DP是矩阵链乘法(1960s)和最优括号化问题的推广。其核心思想——按区间长度递增枚举、枚举合并点——已成为竞赛中合并类问题的标准范式。石子合并(NOI1995)是其经典教学题。

## How · 实现

### 伪代码

```python
for len in 2..n:
  for i in 1..(n-len+1):
    j = i + len - 1
    for k in i..(j-1):
      f[i][j] = max(f[i][j], f[i][k] + f[k+1][j] + cost(i,j))
```

### Python 实现

```python
def stone_merge(a):
    """石子合并(环形) 求最大得分
    a: 各堆石子数量, 环形排列
    返回: 最大合并得分
    """
    n = len(a)
    # 环形 -> 断环成链, 复制为 2n
    b = a + a
    N = 2 * n
    s = [0] * (N + 1)  # 前缀和
    for i in range(1, N + 1):
        s[i] = s[i - 1] + b[i - 1]

    INF = float('-inf')
    f = [[0] * (N + 1) for _ in range(N + 1)]

    for length in range(2, n + 1):  # 枚举区间长度
        for i in range(1, N - length + 2):  # 枚举起点
            j = i + length - 1
            f[i][j] = INF
            for k in range(i, j):  # 枚举合并点
                val = f[i][k] + f[k + 1][j] + s[j] - s[i - 1]
                if val > f[i][j]:
                    f[i][j] = val

    ans = INF
    for i in range(1, n + 1):
        if f[i][i + n - 1] > ans:
            ans = f[i][i + n - 1]
    return ans


def stone_merge_min(a):
    """石子合并(环形) 求最小得分"""
    n = len(a)
    b = a + a
    N = 2 * n
    s = [0] * (N + 1)
    for i in range(1, N + 1):
        s[i] = s[i - 1] + b[i - 1]

    INF = float('inf')
    f = [[0] * (N + 1) for _ in range(N + 1)]

    for length in range(2, n + 1):
        for i in range(1, N - length + 2):
            j = i + length - 1
            f[i][j] = INF
            for k in range(i, j):
                val = f[i][k] + f[k + 1][j] + s[j] - s[i - 1]
                if val < f[i][j]:
                    f[i][j] = val

    ans = INF
    for i in range(1, n + 1):
        if f[i][i + n - 1] < ans:
            ans = f[i][i + n - 1]
    return ans


if __name__ == "__main__":
    # 石子合并: 4堆 [4,5,9,4] 环形
    a = [4, 5, 9, 4]
    # 链上合并: 4+5=9(+9), 9+9=18(+18), 9+4=13(+13) -> varies
    # 最大得分 = 54, 最小得分 = 43 (经典答案)
    print(f"max = {stone_merge(a)}")  # 54
    print(f"min = {stone_merge_min(a)}")  # 43
    assert stone_merge(a) == 54
    assert stone_merge_min(a) == 43
    print("All tests passed.")

```

**PyPy 提示**: PyPy 对三层嵌套循环优化较好，n=200 的 O(n³) 约 0.1s；n>400 时需考虑四边形不等式优化到 O(n²)。列表初始化用 [[0]*(N+1) for _ in range(N+1)]。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n³) — 三重循环(长度×起点×合并点)；可用四边形不等式优化至 O(n²) |
| 空间 | O(n²) — 二维DP表；环形复制为 2n |

### 局限

O(n³) 在 n>500 时 Python 必 TLE（C++ 也勉强）。四边形不等式优化可降至 O(n²) 但实现复杂。环上问题需 2n 空间。Python 建议 n<=200 使用。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| LOJ | 10147 | 2 | NOI1995 石子合并：环形区间DP模板题 | [https://loj.ac/problem/10147](https://loj.ac/problem/10147) |
| Luogu | P1063 | 2 | NOIP2006 能量项链：区间DP，合并代价为左端点×分割点×右端点 | [https://www.luogu.com.cn/problem/P1063](https://www.luogu.com.cn/problem/P1063) |
| Luogu | P1005 | 3 | NOIP2007 矩阵取数游戏：每行独立做区间DP，高精度加法 | [https://www.luogu.com.cn/problem/P1005](https://www.luogu.com.cn/problem/P1005) |

## Pitfalls · 易错点

- 环形问题忘记将数组复制为 2n 长度，只在 n 上做DP导致遗漏断点
- 区间长度从 2 开始枚举而非从 1（长度为 1 时 f(i,i)=0 是边界）
- 合并点 k 的范围是 [i, j-1] 而非 [i, j]（k=j 时 k+1 越界）
- 前缀和用 s[j]-s[i-1] 而非 s[j]-s[i]，注意下标对齐

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/dp/interval/](https://oi-wiki.org/dp/interval/)
- 书籍 ✓ `CPH ch7 p82`
