---
id: dp-knapsack-multiple
name: 多重背包
group: G-A-11
stage: intermediate
priority: P1
depth_tier: standard
---

# 多重背包

> 每件物品有限数量，二进制拆分或单调队列优化

<!-- 元信息: id=dp-knapsack-multiple · group=G-A-11 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

多重背包是0-1背包的变式：每种物品有有限数量 k_i 个而非仅一个。朴素做法将每种物品拆成 k_i 个独立物品做0-1背包(O(W*sum k_i))；二进制分组优化将 k_i 拆成 1+2+4+...+余数 的二进制组(O(W*sum log k_i))；单调队列优化可进一步降至O(nW)。

## Why · 为什么

### 直觉 · Intuition

朴素拆分的问题在于大量重复等效枚举。二进制分组利用「任意整数可用二进制表示」的性质，将 k_i 个相同物品拆成 log(k_i) 个捆绑大物品，每种数量都能被唯一组合表示，大幅减少物品数。

### 原理 · Principle

二进制分组：将数量 k_i 拆为 1,2,4,...,2^t,余数，每个捆绑物品的价值和重量为原来的对应倍数。拆分后做标准0-1背包。正确性：任意 0<=x<=k_i 都能由这些二进制分量唯一表示。单调队列优化：将转移 f(j)=max{f(j-k*w)+k*v | 0<=k<=min(k_i,j/w)} 按余数分组，用单调队列在O(1)内取滑动窗口最大值。

### 历史 · History

多重背包是背包DP的基础变式之一，与0-1背包、完全背包、分组背包合称四大背包模型。二进制分组优化是竞赛中的标准做法，单调队列优化则是进阶技巧。OI Wiki将它们统一收录在背包DP页面中。

## How · 实现

### 伪代码

```python
# 二进制分组优化
items = []  # (weight, value) 拆分后的0-1背包物品
for i in 1..n:
  c = 1
  while c < k[i]:
    items.append((c*w[i], c*v[i]))
    k[i] -= c; c *= 2
  items.append((k[i]*w[i], k[i]*v[i]))
# 标准0-1背包
for item in items:
  for j in W down to item.weight:
    f[j] = max(f[j], f[j-item.weight] + item.value)
```

### Python 实现

```python
def multiple_knapsack(W, weights, values, counts):
    """多重背包(二进制分组优化)
    W: 背包容量
    weights: [w1, w2, ...] 各物品重量
    values: [v1, v2, ...] 各物品价值
    counts: [k1, k2, ...] 各物品数量
    返回: 最大价值
    """
    n = len(weights)
    f = [0] * (W + 1)

    for i in range(n):
        w, v, k = weights[i], values[i], counts[i]
        # 二进制分组拆分
        c = 1
        while c < k:
            bw, bv = c * w, c * v
            for j in range(W, bw - 1, -1):
                if f[j - bw] + bv > f[j]:
                    f[j] = f[j - bw] + bv
            k -= c
            c <<= 1
        # 剩余部分
        if k > 0:
            bw, bv = k * w, k * v
            for j in range(W, bw - 1, -1):
                if f[j - bw] + bv > f[j]:
                    f[j] = f[j - bw] + bv

    return f[W]


def multiple_knapsack_naive(W, weights, values, counts):
    """多重背包(朴素三重循环, 用于验证)"""
    n = len(weights)
    f = [0] * (W + 1)
    for i in range(n):
        w, v, k = weights[i], values[i], counts[i]
        for j in range(W, w - 1, -1):
            for c in range(1, k + 1):
                if c * w <= j and f[j - c * w] + c * v > f[j]:
                    f[j] = f[j - c * w] + c * v
    return f[W]


if __name__ == "__main__":
    # 测试: 容量10, 物品[(w=2,v=3,k=4),(w=3,v=2,k=2),(w=4,v=5,k=1)]
    W = 10
    w = [2, 3, 4]
    v = [3, 2, 5]
    k = [4, 2, 1]

    ans = multiple_knapsack(W, w, v, k)
    ans_naive = multiple_knapsack_naive(W, w, v, k)
    assert ans == ans_naive, f"Binary={ans}, Naive={ans_naive}"
    # 最优: 取4个物品0(重8值12) + 1个物品2不可(重8+4>10)
    # 或: 3个物品0(重6值9)+1个物品2(重4值5)=重10值14
    assert ans == 14, f"Expected 14, got {ans}"

    # 边界测试
    assert multiple_knapsack(0, [1], [1], [1]) == 0
    assert multiple_knapsack(5, [3], [10], [1]) == 10

    print("All tests passed.")

```

**PyPy 提示**: PyPy对内层for循环JIT优化好，二进制分组后物品数减少为sum(log k_i)。n*W=1e7时约0.5s。单调队列优化在PyPy中需注意deque操作常数。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 二进制分组: O(W*sum log k_i)；朴素: O(W*sum k_i)；单调队列优化: O(nW) |
| 空间 | O(W) — 一维滚动数组 |

### 局限

朴素三重循环在sum k_i大时必TLE。二进制分组是竞赛标准做法，单调队列优化更优但实现复杂。Python在W>1e4时可能慢，需PyPy。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1776 | 2 | 宝物筛选：多重背包模板题，需单调队列优化才能过 | [https://www.luogu.com.cn/problem/P1776](https://www.luogu.com.cn/problem/P1776) |
| AcWing | 4 | 2 | 多重背包问题：二进制分组优化基础练习 | [https://www.acwing.com/problem/content/4/](https://www.acwing.com/problem/content/4/) |

## Pitfalls · 易错点

- 二进制拆分时余数处理：c < k 时继续拆，最后剩余 k 作为一组，不是 c <= k
- 拆分后的捆绑物品做0-1背包时容量必须倒序枚举(避免同一捆绑组内多次取)
- 单调队列优化时余数分组，同余数类内维护滑动窗口最大值
- k_i=0的物品应跳过，不要加入拆分

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/dp/knapsack/](https://oi-wiki.org/dp/knapsack/)
- CP-Algorithms ✓ [https://cp-algorithms.com/dynamic_programming/knapsack.html](https://cp-algorithms.com/dynamic_programming/knapsack.html)
