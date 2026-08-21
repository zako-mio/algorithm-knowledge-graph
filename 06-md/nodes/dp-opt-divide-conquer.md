---
id: dp-opt-divide-conquer
name: 分治优化DP
group: G-A-12
stage: advanced
priority: P1
depth_tier: standard
---

# 分治优化DP

> 决策点单调时利用分治缩小决策空间，O(n log n)

<!-- 元信息: id=dp-opt-divide-conquer · group=G-A-12 · stage=advanced · priority=P1 · depth_tier=standard -->

## What · 是什么

分治优化 DP（Divide and Conquer DP）适用于形如 dp[i][j] = min_{k≤j} { dp[i-1][k-1] + C(k,j) } 的分层转移。当成本函数 C 满足四边形不等式时，最优切分点 opt(i,j) 关于 j 单调不减（决策单调性）。据此用分治递归计算单行的所有状态：计算中点 mid 的最优决策时只在 [optl,optr] 枚举，之后左半状态决策界 [optl,opt(mid)]、右半 [opt(mid),optr]，每层每个决策至多被扫描常数次。单层分治 O(n log n)，全部 m 行 O(m n log n)（朴素 O(m n²)）。

## Why · 为什么

### 直觉 · Intuition

分治优化像二分搜索找最优切点：先算中间 j 的最优 k，就知道左边 j' 的最优 k' ≤ k、右边的最优 ≥ k，两侧候选区间各自缩小一半。递归下去每个状态的枚举范围大幅收窄。之所以敢收窄，是因为决策单调性保证「切点随 j 只增不减」，不会漏掉最优解。

### 原理 · Principle

前提（CP-Algorithms 表述）：dp(i,j) = min_{0≤k≤j} { dp(i-1,k-1) + C(k,j) }，C 满足四边形不等式 ⟹ opt(i,j) ≤ opt(i,j+1)。算法 compute(l,r,optl,optr)：mid=(l+r)/2，在 [optl, min(mid,optr)] 枚举 k 求 dp[i][mid] 的最优 opt；递归 compute(l,mid-1,optl,opt) 与 compute(mid+1,r,opt,optr)。复杂度证明：设第 k 层 opt 区间总长 S_k，每层分裂使 S_{k+1} ≤ S_k + 2^k，由 S_0=n 归纳得 S_k < n+2^k = O(n)，共 O(log n) 层故单行 O(n log n)，全表 O(m n log n)。该优化仅适用于 w 可 O(1) 计算的情形；若 w 需动态计算则用二分队列（Aliens trick）替代。

### 历史 · History

分治优化 DP 的思想来自计算几何与组合优化的经典 divide-and-conquer 加速（最早可追溯至 1970s-80s 决策单调性文献，如 1982 年 F. F. Yao 的 quadrangle inequality 论文）。CP-Algorithms 将其整理为 Divide and Conquer DP 专章，OI Wiki 在四边形不等式章节将其列为两种主要实现之一（另一种为二分队列）。广泛用于邮局选址、IOI/省选分层划分类题目。

## How · 实现

### 伪代码

```python
# dp[i][j] = min_{k<=j} { dp[i-1][k-1] + C(k,j) }，决策单调

compute(l, r, optl, optr):      # 计算第 i 行的状态 dp[i][l..r]
  if l > r: return
  mid = (l + r) // 2
  best_v, best_k = INF, -1
  for k in range(optl, min(mid, optr) + 1):
    v = dp_before[k-1] + C(k, mid)
    if v < best_v: best_v, best_k = v, k
  dp_cur[mid] = best_v
  compute(l, mid-1, optl, best_k)
  compute(mid+1, r, best_k, optr)

# 主流程：for i in 1..m: compute(0, n-1, 0, n-1)
```

### Python 实现

```python
def divide_conquer_dp(n, m, cost):
    """分层 DP 分治优化（1-indexed 元素数）：
    dp[i][j] = min_{k<=j} { dp[i-1][k-1] + cost(k, j) }，j 表示前 j 个元素。
    cost(k, j) 需满足四边形不等式（决策单调）。返回 dp[m][n]。
    n 个元素划分成 m 段的最小代价。"""
    INF = 10 ** 30
    dp_before = [INF] * (n + 1)    # 第 0 行：只有 0 段合法
    dp_before[0] = 0
    dp_cur = [0] * (n + 1)

    def compute(l, r, optl, optr):
        if l > r:
            return
        mid = (l + r) // 2
        best_v, best_k = INF, optl
        for k in range(optl, min(mid, optr) + 1):
            v = dp_before[k - 1] + cost(k, mid)
            if v < best_v:
                best_v, best_k = v, k
        dp_cur[mid] = best_v
        compute(l, mid - 1, optl, best_k)
        compute(mid + 1, r, best_k, optr)

    for i in range(m):
        compute(1, n, 1, n)
        dp_before, dp_cur = dp_cur, dp_before
    return dp_before[n]


def divide_conquer_naive(n, m, cost):
    """朴素 O(m n^2) 对拍（1-indexed）"""
    INF = float('inf')
    dp = [[INF] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            for k in range(1, j + 1):
                dp[i][j] = min(dp[i][j], dp[i - 1][k - 1] + cost(k, j))
    return dp[m][n]


def monge_cost(n):
    """构造满足四边形不等式的成本：cost(k,j) = (j-k)^2（平方函数满足 Monge）"""
    def cost(k, j):
        return (j - k) ** 2
    return cost


def monge_cost_abs(n):
    """绝对距离型：cost(k,j)=sum_{t=k..j} |a[t]|，前缀和可 O(1)，Monge"""
    import random
    random.seed(2)
    a = [random.randint(1, 100) for _ in range(n)]
    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + a[i]
    def cost(k, j):
        return pref[j] - pref[k - 1]
    return cost


if __name__ == "__main__":
    import random
    random.seed(51)
    for n in [3, 5, 8, 12, 20]:
        for m in [1, 2, 3, 4]:
            if m > n:
                continue
            cost = monge_cost(n)
            got = divide_conquer_dp(n, m, cost)
            exp = divide_conquer_naive(n, m, cost)
            assert got == exp, (n, m, got, exp)
            cost2 = monge_cost_abs(n)
            got2 = divide_conquer_dp(n, m, cost2)
            exp2 = divide_conquer_naive(n, m, cost2)
            assert got2 == exp2, (n, m, got2, exp2)
    # 决策单调性验证（单行内 opt 单调，1-indexed）
    cost = monge_cost(30)
    INF = float('inf')
    n = 30
    dpb = [0] * (n + 1)
    dpc = [0] * (n + 1)
    def comp(l, r, ol, opr):
        if l > r:
            return
        mid = (l + r) // 2
        best_v, best_k = INF, ol
        for k in range(ol, min(mid, opr) + 1):
            v = dpb[k - 1] + cost(k, mid)
            if v < best_v:
                best_v, best_k = v, k
        dpc[mid] = best_v
        comp(l, mid - 1, ol, best_k)
        comp(mid + 1, r, best_k, opr)
    comp(1, n, 1, n)
    opt = []
    for j in range(1, n + 1):
        best_k = min(range(1, j + 1), key=lambda k: dpb[k - 1] + cost(k, j))
        opt.append(best_k)
    assert all(opt[i] <= opt[i + 1] for i in range(n - 1)), opt
    print("All tests passed.")
```

**PyPy 提示**: 分治优化实现要点：compute 内枚举上界 min(mid, optr) 而非 optr（避免越界）；dp 行滚动两数组即可（dp_before/dp_cur 交换）。cost 必须 O(1)（预计算前缀和/闭式）。递归深度 O(log n) 安全。m 行复杂度 O(m n log n)，n=1e5 时单行 O(1e5 log 1e5) PyPy 可行。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 单行 O(n log n)，全部 m 行 O(m n log n)（朴素 O(m n²)） |
| 空间 | O(n)（滚动两行） |

### 局限

前提是 C 满足四边形不等式（决策单调）；不满足时不可用。若 C 需依赖已算出的 dp 值（动态计算）则分治失效，需二分队列。cost 须 O(1) 可算（否则需游标维护）。仅适用「分层划分」型 DP（状态有层 i 与位置 j 两维）。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Codeforces | 321E | 6 | Ciel and Gondolas：分治优化 DP 经典模板（CP-Algorithms 例题） | [https://codeforces.com/contest/321/problem/E](https://codeforces.com/contest/321/problem/E) |
| Codeforces | 673E | 6 | Levels And Regions：决策单调分治优化 | [https://codeforces.com/problemset/problem/673/E](https://codeforces.com/problemset/problem/673/E) |
| Luogu | P4767 | 6 | IOI2000 邮局：分治优化经典题（划分型） | [https://www.luogu.com.cn/problem/P4767](https://www.luogu.com.cn/problem/P4767) |
| SPOJ | NKLEAVES | 5 | Leaf Partition 变体：分治优化练习 | [https://www.spoj.com/problems/NKLEAVES/](https://www.spoj.com/problems/NKLEAVES/) |

## Pitfalls · 易错点

- 枚举上界写 min(mid, optr) 漏掉导致访问越界或答案错误
- 未验证 C 满足四边形不等式就套用，决策单调不成立
- 滚动两行时交换顺序写反导致使用未更新行
- C 不是 O(1) 时误用（应预计算或游标）
- 单行 compute 的 optl/optr 初始化错误（应为 0..n-1）

## Sources · 信源

- CP-Algorithms ✓ [https://cp-algorithms.com/dynamic_programming/divide-and-conquer-dp.html](https://cp-algorithms.com/dynamic_programming/divide-and-conquer-dp.html)
- OI Wiki ✓ [https://oi-wiki.org/dp/opt/quadrangle/](https://oi-wiki.org/dp/opt/quadrangle/)
- 论文 ✓ `F. F. Yao, Efficiency of dynamic programming, JACM 1982`
