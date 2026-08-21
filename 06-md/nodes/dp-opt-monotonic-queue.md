---
id: dp-opt-monotonic-queue
name: 单调队列/栈优化DP
group: G-A-12
stage: intermediate
priority: P1
depth_tier: standard
---

# 单调队列/栈优化DP

> 用单调队列维护滑动窗口最值加速转移，如多重背包

<!-- 元信息: id=dp-opt-monotonic-queue · group=G-A-12 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

单调队列优化 DP 适用于转移形如 f[i] = opt_{j∈[i-k, i-1]} { g(j) + w(i,j) } 且 w 的取值只依赖一个「窗口」内的候选集，或用「取模分组」把转移划分成若干独立序列的情形。核心是用双端队列维护候选下标，使队首恒为窗口内最优决策，入队时弹出不可能再成为最优的队尾（依据单调性），出队弹出越过窗口左界的队首。每个下标至多入队出队一次，均摊 O(1) 转移，总 O(n)。经典应用：滑动窗口最值、多重背包二进制/单调队列优化、CF372C Watching Fireworks。

## Why · 为什么

### 直觉 · Intuition

朴素转移对每个 i 扫描窗口内 k 个候选 O(k)，n 个状态 O(nk)。观察候选值的「淘汰规则」：若 j1<j2 且 g(j1) ≤ g(j2)（对 min 问题），则 j1 永远不会比 j2 优（更靠前先出窗），可以永久删除。这样队列里只剩「单调递减」的候选，队首即全局最优。滑动窗口使队首位置过期后弹出。这就是「单调」二字的由来。

### 原理 · Principle

单调队列优化多重背包：多重背包 f[i][j] = max_{0≤t≤c} { f[i-1][j-t·v] + t·w }。按 j 对 v 取模分为 v 组，每组内令 j = q·v + r，转移变为 f[q] = max_t { f_prev[q-t] - (q-t)·w } + q·w——括号内是与 q 无关的「候选值」，随 q 递增用单调队列维护（队列元素 f_prev[pos]-pos·w 单调）。每个 q 的转移 O(1)，总 O(n·V)（V 为容量）。窗口宽度即物品数量 c，越界弹出队首。此外 CF372C 等「固定步长移动」问题也直接套用窗口最值。

### 历史 · History

单调队列/单调栈是最早被系统化的 DP 与区间最值优化手段，广泛用于滑动窗口问题（1980s USACO 滑动窗口）与多重背包优化。OI Wiki 设专章（monotonic-queue-stack）并与单调栈并列介绍；多重背包单调队列优化是 NOIP/省选高频考点。

## How · 实现

### 伪代码

```python
# 滑动窗口最值（min 版本）
for i in 0..n-1:
  while dq 非空 and dq[0] < i-k: pop_left()      # 出窗
  while dq 非空 and val(dq[-1]) >= a[i]: pop_right()  # 淘汰劣势
  push(i)
  窗口最值 = val(dq[0])

# 多重背包单调队列优化
for 每件物品(v,w,c):
  for r in 0..v-1:                       # 按容量余数分组
    单调队列 q 存候选 {pos: f_prev[pos]-pos*w}
    for q 从 r 开始按 +v 递增到 V:
      弹出越过窗口(c)的队首
      插入 f_prev[q]-q*w（维护单调）
      f_cur[q] = 队首值 + q*w
```

### Python 实现

```python
def sliding_max(a, k):
    """滑动窗口最大值，窗口为 [i-k+1, i]，O(n)。"""
    from collections import deque
    dq = deque()
    res = []
    for i, x in enumerate(a):
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        while dq and a[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        res.append(a[dq[0]])
    return res


def multiple_knapsack_monoq(n, V, items):
    """多重背包单调队列优化：O(n*V)。
    items: [(value, weight, count)]，求容量 V 下最大价值。
    """
    dp = [0] * (V + 1)          # 上一物品层
    for v, w, c in items:
        ndp = [0] * (V + 1)
        for r in range(v):
            from collections import deque
            dq = deque()        # 存候选下标 pos（同一余数类）
            for pos in range(r, V + 1, v):
                # 窗口大小 c：pos 之前超出 c 步的候选作废
                while dq and dq[0] < pos - c * v:
                    dq.popleft()
                val = dp[pos] - (pos // v) * w
                while dq and dp[dq[-1]] - (dq[-1] // v) * w <= val:
                    dq.pop()
                dq.append(pos)
                ndp[pos] = dp[dq[0]] - (dq[0] // v) * w + (pos // v) * w
        dp = ndp
    return dp[V]


def multiple_knapsack_naive(n, V, items):
    """朴素多重背包（对拍用）"""
    dp = [0] * (V + 1)
    for v, w, c in items:
        ndp = dp[:]
        for j in range(V + 1):
            for t in range(1, c + 1):
                if j >= t * v:
                    ndp[j] = max(ndp[j], dp[j - t * v] + t * w)
        dp = ndp
    return dp[V]


def firework_dp(dist, c, times, shines):
    """CF372C 烟花表演变形：位置移动步长<=d 的 DP。
    返回总最大亮度。此处 d=1 演示单调队列 O(m*n)。
    """
    n = len(dist)
    m = len(times)
    dp = [shines[0] - abs(dist[i]) for i in range(n)]
    for k in range(1, m):
        span = times[k] - times[k - 1]
        step = min(c, span)          # 每步可移动<=span，窗口半径
        from collections import deque
        dq = deque()
        ndp = [0] * n
        for i in range(n):
            # 候选为 i-1 的前 step 个位置（一维简化演示）
            while dq and dq[0] < i - step:
                dq.popleft()
            while dq and dp[dq[-1]] <= dp[i - 1]:
                dq.pop()
            dq.append(i - 1)
            ndp[i] = dp[dq[0]] + shines[k] - abs(dist[i])
        dp = ndp
    return max(dp)


if __name__ == "__main__":
    import random
    random.seed(21)
    # 滑动窗口
    a = [1, 3, -1, -3, 5, 3, 6, 7]
    assert sliding_max(a, 3) == [1, 3, 3, 3, 5, 5, 6, 7]
    for _ in range(50):
        arr = [random.randint(-100, 100) for _ in range(200)]
        k = random.randint(1, 20)
        expect = [max(arr[max(0, i - k + 1):i + 1]) for i in range(len(arr))]
        assert sliding_max(arr, k) == expect
    # 多重背包单调队列 vs 朴素
    items = [(2, 3, 4), (3, 4, 2), (1, 1, 5), (5, 2, 3)]
    for _ in range(30):
        its = [(random.randint(1, 8), random.randint(1, 8), random.randint(1, 6))
               for __ in range(5)]
        V = random.randint(1, 120)
        got = multiple_knapsack_monoq(len(its), V, its)
        exp = multiple_knapsack_naive(len(its), V, its)
        assert got == exp, (got, exp)
    print("All tests passed.")
```

**PyPy 提示**: 单调队列用 collections.deque 实现，均摊 O(1)。多重背包单调队列注意按余数 r 分组遍历，窗口判界用 pos < dq[0] 的候选作废（数量上限 c）。Python 大容量背包（V 达 1e7）内存紧张，可滚动数组 + int 数组（array 模块）。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 滑动窗口/单调队列优化：O(n)；多重背包：O(n·V) |
| 空间 | O(n) 或 O(V)（滚动） |

### 局限

适用前提：转移只依赖窗口内最值且窗口右端点单调；多重背包要求同一物品价值/重量为正整数（否则不可按组取模拆）。若窗口左端点不单调（可任意查询），需改用线段树/稀疏表。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1886 | 3 | 滑动窗口/单调队列最值模板题 | [https://www.luogu.com.cn/problem/P1886](https://www.luogu.com.cn/problem/P1886) |
| Luogu | P1776 | 5 | 宝物筛选：多重背包单调队列优化模板 | [https://www.luogu.com.cn/problem/P1776](https://www.luogu.com.cn/problem/P1776) |
| Codeforces | 372C | 5 | Watching Fireworks：固定步长移动+单调队列（OI Wiki 例题） | [https://codeforces.com/problemset/problem/372/C](https://codeforces.com/problemset/problem/372/C) |
| Luogu | P2254 | 6 | NOI2005 瑰丽华尔兹：方向分段单调队列优化 DP | [https://www.luogu.com.cn/problem/P2254](https://www.luogu.com.cn/problem/P2254) |

## Pitfalls · 易错点

- 队首出窗判断用 < 还是 <= 导致窗口边界差 1
- 多重背包按余数分组时 r 循环遗漏导致部分容量未被更新
- 队列存下标而非值，比较时忘带回原值导致淘汰逻辑错误
- 把 min 问题当成 max 问题维护（单调性方向相反）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/dp/opt/monotonic-queue-stack/](https://oi-wiki.org/dp/opt/monotonic-queue-stack/)
- CP-Algorithms △ [https://cp-algorithms.com/dynamic_programming/monotonic_queue.html](https://cp-algorithms.com/dynamic_programming/monotonic_queue.html)
