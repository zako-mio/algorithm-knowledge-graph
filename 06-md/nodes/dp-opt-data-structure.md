---
id: dp-opt-data-structure
name: 数据结构优化DP
group: G-A-12
stage: intermediate
priority: P1
depth_tier: standard
---

# 数据结构优化DP

> 用线段树/BIT/平衡树加速转移中的查询/修改操作

<!-- 元信息: id=dp-opt-data-structure · group=G-A-12 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

数据结构优化 DP 指用线段树、树状数组(BIT)、单调队列/栈、平衡树等加速 DP 转移中出现的区间查询或单点/区间修改。典型情形一：转移形如 f(i)=F(a_i,{f(j):j<i})，把之前的 f(j) 组织进数据结构，每次转移=一次查询+一次插入（如 ABC DP_Q Flowers、ABC DP_W Intervals 用线段树区间加区间取 max，LIS 用 BIT 维护前缀 max）；情形二：f(i,·) 依赖 f(i-1,·) 的数组整体变换，用懒标记线段树/分块加速（如 CF 115E 线性王国赛马）。配合前缀和、单调队列（滑窗最值）、倍增、CDQ 分治构成 DP 优化的基础工具箱。

## Why · 为什么

### 直觉 · Intuition

把 DP 数组当成一个被反复'查询区间最值/和'和'单点更新'的结构。朴素每次 O(n) 扫描的转移，用线段树/BIT 变成 O(log n)。数据结构干的活就是把'维护一堆候选值'这件事自动化。

### 原理 · Principle

以 ABC DP_Q Flowers 为例：f[i]=max_{j<i, h_j<h_i}(f[j])+a_i，本质是按高度维护前缀 max。把高度离散化，用 BIT 支持前缀 max 查询与单点更新，转移降为 O(log n)。ABC DP_W Intervals 用线段树做区间加+全局 max（每个区间 [l,r] 加 w 到其内的 dp 值）。单调队列优化适合转移窗口内的滑动最值，线段树适合任意区间，CDQ 分治适合需要离线+偏序约束的 1D1D 转移。

### 历史 · History

数据结构优化 DP 是 DP 优化的入门门类，OI Wiki 的 dp/opt/dp-opt 页面按'前缀和/单调队列/线段树/CDQ/倍增'分类整理，AtCoder Educational DP Contest 的 M/Q/W 题是公认训练入口。与斜率优化、四边形不等式一起构成经典优化三件套。

## How · 实现

### 伪代码

```python
# 例: LIS 用 BIT 加速 (O(n log n))
vals = 离散化(a)
BIT(支持前缀 max, 单点更新)
for x in a:
    best = BIT.query(idx(x)-1)  # 之前所有较小值的最大 dp
    BIT.update(idx(x), best+1)
return BIT.query(len(vals))

# 例: ABC DP_Q Flowers (高度 h, 美丽 a)
for i in 1..n:
    f[i] = BIT.query(h_i-1) + a_i
    BIT.update(h_i, f[i])
ans = max f
```

### Python 实现

```python
import bisect


class FenwickMax:
    """支持单点取max、前缀max的BIT(用于 dp-opt-data-structure 演示, 如 ABC DP_Q)."""

    def __init__(self, n):
        self.n = n
        self.t = [0] * (n + 1)

    def update(self, i, v):
        while i <= self.n:
            if v > self.t[i]:
                self.t[i] = v
            i += i & -i

    def query(self, i):
        r = 0
        while i > 0:
            if self.t[i] > r:
                r = self.t[i]
            i -= i & -i
        return r


def lis_with_bit(a):
    """最长上升子序列(O(n log n) 离散化+BIT): 演示数据结构优化 DP.
    也等价于 ABC DP_Q Flowers 的 BIT 优化(按高度排序)."""
    vals = sorted(set(a))
    idx = {v: i + 1 for i, v in enumerate(vals)}
    bit = FenwickMax(len(vals))
    for x in a:
        i = idx[x]
        best = bit.query(i - 1)
        bit.update(i, best + 1)
    return bit.query(len(vals))


def lis_brute(a):
    n = len(a)
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if a[j] < a[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp) if n else 0


if __name__ == "__main__":
    import random
    for _ in range(300):
        n = random.randint(1, 12)
        a = [random.randint(-5, 5) for _ in range(n)]
        assert lis_with_bit(a) == lis_brute(a), a
    assert lis_with_bit([3, 1, 2, 1, 8, 5]) == 3
    assert lis_with_bit([2, 2, 2]) == 1
    print("dp-opt-data-structure (BIT for LIS / ABC DP_Q) tests passed")

```

**PyPy 提示**: BIT 在 Python 中快且省内存(数组+位运算)；线段树需数组实现(堆式/迭代式)避免递归常数。离散化用 sorted(set())+二分。1e5~1e6 级 Python+PyPy 均可。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n log n) 每个状态一次查询一次更新; 线段树区间操作 O(log n) |
| 空间 | O(n) |

### 局限

要求转移可拆成'范围查询+点更新'的静态模式；若需动态插入删除+最值，需换平衡树。线段树区间加取 max 需懒标记，实现易错。单调队列要求窗口单调、只进不退。CDQ 分治要求可离线。Python 在大常数(线段树)下 1e6 级需谨慎。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| AtCoder | dp_q | 3 | Flowers: BIT 维护前缀 max 的经典模板 | [https://atcoder.jp/contests/dp/tasks/dp_q](https://atcoder.jp/contests/dp/tasks/dp_q) |
| AtCoder | dp_w | 4 | Intervals: 线段树区间加+全局 max | [https://atcoder.jp/contests/dp/tasks/dp_w](https://atcoder.jp/contests/dp/tasks/dp_w) |
| Codeforces | 115E | 4 | Linear Kingdom Races: 线段树优化区间分拆 DP | [https://codeforces.com/problemset/problem/115/E](https://codeforces.com/problemset/problem/115/E) |

## Pitfalls · 易错点

- 离散化下标从 1 开始, 查询前缀要用 idx-1
- BIT 求前缀 max 时单点更新要取 max 而非赋值
- 线段树区间加取 max 的懒标记顺序(先加后取)搞错
- 状态更新顺序: 必须先查询旧值再更新当前, 防止同一轮内自转移
- 只适用于查询/修改分离的转移, 强依赖转移形式

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/dp/opt/dp-opt/](https://oi-wiki.org/dp/opt/dp-opt/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/dp/opt/dp-opt.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/dp/opt/dp-opt.md)
