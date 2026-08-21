---
id: dp-knapsack01
name: 0-1背包
group: G-A-11
stage: basic
priority: P0
depth_tier: deep
---

# 0-1背包

> 每个物品取/不取，O(nW)转移，滚动数组优化空间

<!-- 元信息: id=dp-knapsack01 · group=G-A-11 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

0-1 背包：n 个物品各有重量 w[i] 和价值 v[i]，背包容量 W，每件物品最多取一次（取或不取），求不超过容量下的最大价值。状态 dp[j] 表示容量 j 时的最大价值，转移 dp[j]=max(dp[j], dp[j-w[i]]+v[i])。关键：内层 j 必须逆序遍历（W→w[i]），保证每件物品只用一次；若正序则物品被重复取用（退化为完全背包）。滚动数组优化空间至 O(W)。

## Why · 为什么

### 直觉 · Intuition

对每件物品 i，决策只有取或不取。不取 → 价值不变 dp[j]；取 → 容量减少 w[i]、价值增加 v[i]，即 dp[j-w[i]]+v[i]。取较大者。为何逆序？因为 dp[j] 依赖 dp[j-w[i]]（更小容量），若正序则 dp[j-w[i]] 已被当前物品 i 更新过，相当于物品 i 被取了两次。逆序保证更新 dp[j] 时 dp[j-w[i]] 还是上一轮（物品 i-1）的值。

### 原理 · Principle

二维状态 f[i][j]=max(f[i-1][j], f[i-1][j-w[i]]+v[i])，i 是物品、j 是容量。因 f[i] 只依赖 f[i-1]，可压缩为 1D：dp[j]=max(dp[j], dp[j-w[i]]+v[i])。逆序遍历 j=W→w[i] 保证读 dp[j-w[i]] 时它还是 i-1 轮的值（j-w[i]<j 尚未被本轮更新）。正序则 j-w[i]<j 已被更新成 i 轮值，相当于同一物品取多次。这是背包 DP 所有变体的基础。

### 历史 · History

0-1 背包是 Knapsack problem 的最基本形式，由 Dantzig 1957 系统讨论。OI Wiki 以 USACO07 Charm Bracelet 为入门例题。滚动数组逆序遍历是经典技巧。CPH 第7章详细推导。

## How · 实现

### 伪代码

```python
# 0-1背包
dp = [0] * (W + 1)
for i in range(1, n+1):
  for j in range(W, w[i]-1, -1):  # 逆序!
    dp[j] = max(dp[j], dp[j-w[i]] + v[i])
answer = dp[W]
```

### Python 实现

```python
# 0-1背包（含自测）
def knapsack01(n, W, w, v):
    """n物品, 容量W, 重量w[1..n], 价值v[1..n] (1-indexed)
    返回最大价值"""
    dp = [0] * (W + 1)
    for i in range(n):
        wi, vi = w[i], v[i]
        for j in range(W, wi - 1, -1):  # 逆序保证每件只取一次
            if dp[j - wi] + vi > dp[j]:
                dp[j] = dp[j - wi] + vi
    return dp[W]

if __name__ == "__main__":
    # USACO07 Charm Bracelet 示例
    # 4件物品, 容量6
    #   w=[2,3,4,5] v=[1,2,5,6]
    #   最优: 取物品3(w=4,v=5) + 物品1(w=2,v=1) = v6 w6
    W = 6
    w = [2, 3, 4, 5]
    v = [1, 2, 5, 6]
    assert knapsack01(4, W, w, v) == 6
    # 单件物品
    assert knapsack01(1, 5, [3], [10]) == 10
    assert knapsack01(1, 2, [3], [10]) == 0  # 装不下
    # 容量0
    assert knapsack01(3, 0, [1, 2, 3], [10, 20, 30]) == 0
    # 全装下
    assert knapsack01(3, 100, [1, 2, 3], [10, 20, 30]) == 60
    print("dp-knapsack01 OK")

```

**PyPy 提示**: 0-1背包内层逆序循环是纯整数操作，PyPy JIT 友好，O(nW) 快数倍。注意 W 很大（如 10^9）时数组开不下，需改用 dp 状态离散化或 meet-in-the-middle。Python 大 W 可用 dict 存稀疏状态。PyPy 下 list-strategy 对 int 列表紧凑存储省内存。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(nW) |
| 空间 | O(W) 滚动数组 |

### 局限

1) W 很大时 O(nW) 超时且 O(W) 内存爆，需 meet-in-the-middle 或其他方法；2) 逆序遍历易写错成正序（变完全背包）；3) 求方案数而非最值时转移改加法。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P2871 | 3 | 0-1 背包模板题，n≤350, W≤12888 | [https://www.luogu.com.cn/problem/P2871](https://www.luogu.com.cn/problem/P2871) |
| Luogu | P1048 | 2 | 0-1 背包变体（时间=容量），可记忆化或递推 | [https://www.luogu.com.cn/problem/P1048](https://www.luogu.com.cn/problem/P1048) |
| Luogu | P1060 | 3 | 0-1 背包，价值=价格×重要度 | [https://www.luogu.com.cn/problem/P1060](https://www.luogu.com.cn/problem/P1060) |

## Pitfalls · 易错点

- 内层 j 正序遍历 → 变成完全背包（物品被重复取用）
- j 范围写成 range(W, 0, -1) 漏了 -1 上界 → 应 range(W, w[i]-1, -1)
- 二维转一维忘记去掉物品维度 → 空间 O(nW) 可能 MLE
- W 极大（10^9）直接开数组 → 内存爆，应改离散化或 meet-in-middle
- 求方案数时用 max 而非 += → 答案错

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/dp/knapsack/](https://oi-wiki.org/dp/knapsack/)
- CP-Algorithms ✓ [https://cp-algorithms.com/dynamic_programming/knapsack.html](https://cp-algorithms.com/dynamic_programming/knapsack.html)
- 书籍 ✓ `CPH ch7 p78`
