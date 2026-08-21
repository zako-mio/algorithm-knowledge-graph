---
id: dp-knapsack-complete
name: 完全背包
group: G-A-11
stage: basic
priority: P0
depth_tier: deep
---

# 完全背包

> 每件物品无限取，正序遍历容量

<!-- 元信息: id=dp-knapsack-complete · group=G-A-11 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

完全背包：n 种物品各有重量 w[i] 和价值 v[i]，背包容量 W，每种物品可取无限次，求不超过容量下的最大价值。与 0-1 背包唯一区别是内层 j 正序遍历（w[i]→W），使得 dp[j-w[i]] 在更新 dp[j] 时已是当前轮（物品 i）的值，等价于物品 i 被取多次。转移方程 dp[j]=max(dp[j], dp[j-w[i]]+v[i]) 与 0-1 相同，仅遍历方向不同。

## Why · 为什么

### 直觉 · Intuition

0-1 背包逆序是为了不让物品 i 被取两次。完全背包正好相反——我们要让物品 i 能被取任意次。正序遍历 j 时，更新 dp[j] 用到的 dp[j-w[i]] 已被本轮更新过（因 j-w[i]<j 先处理），那个值已经包含了「取一次物品 i」的效果，再叠加就是取两次……如此递推实现无限取。巧妙地用遍历方向一正一反区分两种背包。

### 原理 · Principle

二维状态 f[i][j]=max(f[i-1][j], f[i][j-w[i]]+v[i])，注意第二项是 f[i]（同轮）而非 f[i-1]——因为物品 i 可重复取。f[i][j-w[i]] 已考虑了取若干次物品 i 的最优，再 +v[i] 就是多取一次。压缩为 1D：dp[j]=max(dp[j], dp[j-w[i]]+v[i])，正序 j 保证 dp[j-w[i]] 是本轮（含物品 i）的值。朴素做法枚举取 k 件 O(n³)，优化后 O(nW)。

### 历史 · History

完全背包是 0-1 背包的直接变体。OI Wiki 以「疯狂的采药」(P1616) 为例题。关键洞察——遍历方向反转即从 0-1 变完全——是背包 DP 的经典技巧。

## How · 实现

### 伪代码

```python
# 完全背包
dp = [0] * (W + 1)
for i in range(1, n+1):
  for j in range(w[i], W+1):  # 正序! 与0-1相反
    dp[j] = max(dp[j], dp[j-w[i]] + v[i])
answer = dp[W]
```

### Python 实现

```python
# 完全背包（含自测）
def knapsack_complete(n, W, w, v):
    """n种物品, 容量W, 每种无限取
    w[0..n-1] 重量, v[0..n-1] 价值
    返回最大价值"""
    dp = [0] * (W + 1)
    for i in range(n):
        wi, vi = w[i], v[i]
        for j in range(wi, W + 1):  # 正序: 允许重复取
            if dp[j - wi] + vi > dp[j]:
                dp[j] = dp[j - wi] + vi
    return dp[W]

def knapsack01_compare(n, W, w, v):
    """0-1背包对比: 逆序"""
    dp = [0] * (W + 1)
    for i in range(n):
        wi, vi = w[i], v[i]
        for j in range(W, wi - 1, -1):  # 逆序
            if dp[j - wi] + vi > dp[j]:
                dp[j] = dp[j - wi] + vi
    return dp[W]

if __name__ == "__main__":
    # 疯狂的采药示例
    # 3种药, 容量10
    #   w=[3,4,5] v=[4,5,6]
    #   完全: 尽量取性价比高的
    W = 10
    w = [3, 4, 5]
    v = [4, 5, 6]
    # 物品1 性价比 4/3≈1.33 最高, 取3件=9 v12, 剩1 不够装
    # 或 物品1取2件(6,v8)+物品2取1件(4,v5)=10 v13
    result = knapsack_complete(3, W, w, v)
    assert result == 13  # w6+v5 + w4+v5 = 10, v=13
    # 对比0-1背包(每件只取一次): 物品2(w4,v5)+物品3(w5,v6)=w9 v11
    result01 = knapsack01_compare(3, W, w, v)
    assert result01 == 11
    # 完全应 >= 0-1 (可取更多)
    assert result >= result01
    # 单种物品全装
    assert knapsack_complete(1, 10, [3], [4]) == 12  # 3*3=9 但3件v12, 实际10/3=3件
    print("dp-knapsack-complete OK")

```

**PyPy 提示**: 完全背包内层正序循环是纯整数操作，PyPy JIT 友好。注意与 0-1 背包仅遍历方向不同，写代码时务必确认方向。大 W 同样有内存/时间问题。PyPy 下 list-strategy 对 int 列表紧凑。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(nW) |
| 空间 | O(W) 滚动数组 |

### 局限

1) W 极大时 O(nW) 超时且 O(W) 内存爆；2) 正序/逆序极易混淆——这是最常见错误；3) 多重背包（每件有限 k 个）需二进制分组优化。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1616 | 3 | 完全背包模板题，每种药草无限取 | [https://www.luogu.com.cn/problem/P1616](https://www.luogu.com.cn/problem/P1616) |
| LeetCode | 322 | 4 | 完全背包求最少硬币数 | [https://leetcode.cn/problems/coin-change/](https://leetcode.cn/problems/coin-change/) |
| LeetCode | 518 | 4 | 完全背包求方案数 dp[j]+=dp[j-coin] | [https://leetcode.cn/problems/coin-change-ii/](https://leetcode.cn/problems/coin-change-ii/) |

## Pitfalls · 易错点

- 把正序写成逆序 → 退化成 0-1 背包（物品只取一次）
- 求方案数用 max 而非 += → 答案错（求最值 vs 求计数转移不同）
- j 范围 range(wi, W+1) 写成 range(0, W+1) → j-wi 为负越界
- 与 0-1 背包代码只差遍历方向，复制粘贴后忘改方向 → 全错
- W 极大直接开数组 → 内存爆，应改其他方法

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/dp/knapsack/](https://oi-wiki.org/dp/knapsack/)
- CP-Algorithms ✓ [https://cp-algorithms.com/dynamic_programming/knapsack.html](https://cp-algorithms.com/dynamic_programming/knapsack.html)
- 书籍 ✓ `CPH ch7 p79`
