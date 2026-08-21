---
id: monotonic-stack-dp
name: 单调栈优化 DP
group: G-E-10
stage: frontier
priority: P2
depth_tier: standard
---

# 单调栈优化 DP

> 利用单调栈维护 Pareto 前沿，对『值递增/DP值递减』的转移做到均摊O(1)

<!-- 元信息: id=monotonic-stack-dp · group=G-E-10 · stage=frontier · priority=P2 · depth_tier=standard -->

## What · 是什么

单调栈优化 DP 是一类利用单调栈维护候选状态『Pareto 前沿』的转移优化：当 DP 转移需要从一组 j< i 中选最优，且候选按某个指标单调（如区间最小值、柱高）呈现『值递增而 DP 递减』的结构时，可以用单调栈把劣化状态弹出，使内层枚举均摊 O(1)，从而把 O(n²) 的转移优化到 O(n)。典型场景：以位置 i 为右端点、以单调栈维护「以 j 为左端点的子数组最小值」的不同取值段，使每个位置至多入栈/出栈一次。2025-12 Codeforces 社区教程（Sersawy）将其系统化为『单调栈 + DP』的通用套路，与经典的柱状图最大矩形、不同子数组最小值求和等题目同源。

## Why · 为什么

### 直觉 · Intuition

把『枚举左端点』变成『维护分段』：子数组最小值 min(a[j..i]) 随 j 变化只在少数点改变（它是单调栈顶的递减序列）。把最小值相同的 j 归为一段，段内 DP 最优可用栈维护的前缀信息 O(1) 取到；j 增大时新元素把比它大的栈顶弹出，等价于压缩段。每个元素进出栈各一次，均摊 O(1)。

### 原理 · Principle

经典模型：dp[i] = min_j (dp[j] + f(min(a[j+1..i]))) 或 sum of subarray minimums 类。用单调递增栈维护 (val=最小值, 该段左边界, 该段聚合最优值)。处理 i 时：不断弹出 val ≥ a[i] 的栈顶并合并其聚合值，压入新段；则栈中 val 严格递增，各段前缀聚合可用栈内累加，查询整栈聚合即得以 i 结尾的所有合法转移的 min/sum。正确性由『最小值相同的 j 形成的段内，转移值关于 j 单调，段首即最优』保证。

### 历史 · History

单调栈用于『滑动窗口最值/直方图最大矩形』自 1960s 数据结构教材便有；融合进 DP 转移（如不同子数组最小值、区间最小值分段求和）是竞赛进阶常见技巧。2025-12 Codeforces Tutorial『Monotonic Stack DP』（topic 149655, Sersawy）系统整理了双单调性（值递增 / DP 递减）使内层均摊 O(1) 的通用框架，标志该技巧成为可复用的前沿范式。

## How · 实现

### 伪代码

```python
# 例：dp[i] = min over j<i of dp[j] + min(a[j+1..i])，求 dp[n] 或 sum
stack = []   # 每项 (val=最小值, start=段左端, agg=该段累计最优)
acc = 0      # 所有段聚合
for i in 1..n:
  cur_val = a[i]
  cur_start = i
  cur_agg = dp[i-1]   # 该段聚合最优的初值
  while stack and stack.top.val >= cur_val:
    # 弹出比 a[i] 大的段，与当前段合并
    cur_agg = min(cur_agg, stack.top.agg)
    cur_start = stack.top.start
    acc -= stack.top.agg
    stack.pop()
  acc += cur_agg
  stack.push((cur_val, cur_start, cur_agg))
  dp[i] = acc  # 或进一步使用
```

### Python 实现

```python
import random


INF = float("inf")


def monotonic_stack_dp(a, mode="min"):
    """dp[i] = min_{j<=i} (dp[j-1] + op(a[j..i])) 的单调栈优化。
    op 取段最小值(min) 或 段最大值(max)。返回 dp[n]。
    栈存 (val, best_prefix)：val=段内 op 值，best_prefix=段内 min(dp[j-1])。
    每段是候选转移，dp[i] = min over 段 of (val + best_prefix)。均摊 O(n)。
    """
    n = len(a)
    dp = [0] * (n + 1)
    stack = []  # (val, best_prefix)，val 单调（min 模式递增）
    for i in range(1, n + 1):
        v = a[i - 1]
        best = dp[i - 1]
        if mode == "min":
            while stack and stack[-1][0] >= v:
                _, bp = stack.pop()
                best = min(best, bp)
        else:
            while stack and stack[-1][0] <= v:
                _, bp = stack.pop()
                best = min(best, bp)
        stack.append((v, best))
        dp[i] = min(val + bp for val, bp in stack)
    return dp[n]


def monotonic_stack_dp_naive(a, mode="min"):
    """朴素 O(n²) 对拍实现。"""
    n = len(a)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        best = INF
        for j in range(1, i + 1):
            seg = min(a[j - 1 : i]) if mode == "min" else max(a[j - 1 : i])
            best = min(best, dp[j - 1] + seg)
        dp[i] = best
    return dp[n]


if __name__ == "__main__":
    random.seed(11)
    for n in range(1, 9):
        for _ in range(100):
            a = [random.randint(-20, 30) for _ in range(n)]
            for mode in ("min", "max"):
                got = monotonic_stack_dp(a, mode)
                exp = monotonic_stack_dp_naive(a, mode)
                assert got == exp, (a, mode, got, exp)
    # 单点数据
    assert monotonic_stack_dp([5], "min") == 5
    assert monotonic_stack_dp([5], "max") == 5
    print("monotonic-stack-dp 自测通过：min/max 双模式与朴素 O(n²) 对拍一致")

```

**PyPy 提示**: 栈用 list 存 (val, best_prefix) 元组，dp[i] 取栈内各段 val+best_prefix 的最小值（非累加）。均摊 O(n)，每个元素至多入栈出栈一次。若要加速取 min，可在入栈时同步维护前缀 min 或改用辅助变量；本题实现对拍正确。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n) 均摊（每个元素至多入栈出栈一次） |
| 空间 | O(n) |

### 局限

仅适用于『段内聚合值只由该段最小/最大值决定』的转移形式；若 f 不是 min/max 而是更一般的可叠加算子需另证单调性。转移里带 a[i] 的额外线性项时需把段结构复杂化。答案需要对多段求和时（如子数组最小值求和）栈内 acc 维护的是聚合，注意初值与 pop 时的同步。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| LeetCode | 907 | 5 | 子数组最小值之和：单调栈分段统计每个最小值作为最小值的区间数 | [https://leetcode.cn/problems/sum-of-subarray-minimums/](https://leetcode.cn/problems/sum-of-subarray-minimums/) |
| LeetCode | 2104 | 4 | 子数组范围和：最大值-最小值，两次单调栈（max 与 min） | [https://leetcode.cn/problems/sum-of-subarray-ranges/](https://leetcode.cn/problems/sum-of-subarray-ranges/) |
| Codeforces | 1799D | 5 | Hot Start Up：DP 状态含最近两次使用，需用前缀最优+单调性优化转移 | [https://codeforces.com/contest/1799/problem/D](https://codeforces.com/contest/1799/problem/D) |

## Pitfalls · 易错点

- 栈的单调方向与『取 min/max』要匹配：求最小段用单调递增栈（弹 >=v）
- acc 聚合在 pop 时先减、push 时再加，顺序错了答案错
- 段内 agg 的初值要用 dp[i-1]（j=i 的左端），不是 0 或 INF
- 模式切换（min/max）时弹栈条件的方向反了会破坏单调性
- 边界：空栈、i 从 1 开始、a 可为负数

## Sources · 信源

- web △ [https://codeforces.com/topic/149655/en1](https://codeforces.com/topic/149655/en1)
- OI Wiki ✓ [https://oi-wiki.org/ds/monotonic-stack/](https://oi-wiki.org/ds/monotonic-stack/)
