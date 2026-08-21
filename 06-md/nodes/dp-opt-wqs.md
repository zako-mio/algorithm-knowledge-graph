---
id: dp-opt-wqs
name: WQS二分/凸优化DP
group: G-A-12
stage: advanced
priority: P2
depth_tier: standard
---

# WQS二分/凸优化DP

> 带数量限制的凸DP，二分惩罚系数消除限制

<!-- 元信息: id=dp-opt-wqs · group=G-A-12 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

WQS 二分（Aliens Trick / 带权二分 / 凸优化 DP）处理一类'恰好选 k 个'（或至多 k 个）的最优化 DP：若去除数量限制后问题可解，且最优价值 v(k) 关于 k 是凹（或凸）函数，则对每个被选元素附加惩罚 λ（每选一个价值 -λ），解无数量限制问题得到最优个数 g(λ)。因为 g(λ) 关于 λ 单调，可二分 λ 使 g(λ)=k，答案 = 惩罚问题的价值 + λ·k。单次无限制问题 O(T)，总复杂度 O(T log C)，比 O(nk) 的二维 DP 快得多。

## Why · 为什么

### 直觉 · Intuition

数量限制就像'多选一个的边际收益递减'(凹函数)。给每个选择加个统一惩罚 λ，等于给'选 k 个'这条曲线叠加一条斜率为 -λ 的直线，最大值点会随着 λ 变大而往 k 变小的方向移动。二分 λ 就能精确定位到恰好取 k 个的那个点。

### 原理 · Principle

设 v(k) 为恰选 k 个的最优值。定义 h(λ)=max_k (v(k)-λk)，即惩罚问题的答案。v 凹 ⇔ h(λ) 的最优 k 关于 λ 单调。二分 λ 求使最优 k=目标数的最小 λ，则答案 = h(λ)+λk。共线情形需保证求解 h(λ) 时记录的 k 是最大（或最小）的 argmax，再按 'k>=目标'/'k<=目标' 调整二分边界。凸性可用四边形不等式、交换论证或通过构造区间分拆证明。

### 历史 · History

WQS 二分由中国选手王钦石（Wang Qiushi）在 2011 年左右提出并命名，2013 年入选国家队候选队论文《浅析一类二分方法》。国外称为 Aliens Trick（源于 AtCoder AGC 某外星人题）。OI Wiki 的 wqs-binary-search 页面系统整理了凸性证明三种方法（状态转移方程、四边形不等式、交换论证）与共线处理。

## How · 实现

### 伪代码

```python
# 模板: 恰选 k 个, 价值 v(k) 凹
lo, hi = 惩罚下界, 惩罚上界
ans = None
while lo <= hi:
    mid = (lo+hi)//2
    val, cnt = solve_with_penalty(mid)  # 每选一个价值-mid, 解无数量限制
    if cnt >= k:        # 选多了: 惩罚(负斜率)应加大
        ans = val + mid*k   # 还原真实价值
        lo = mid + 1
    else:
        hi = mid - 1
return ans
```

### Python 实现

```python
import random


def plant_trees_brute(a, m):
    """P1484 种树: n 个坑, 至多种 m 棵, 不相邻, 求最大收益和.
    暴力 DP O(n*m)."""
    n = len(a)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(0, m + 1):
            dp[i][j] = dp[i - 1][j]
            if j >= 1:
                if i - 2 >= 0:
                    dp[i][j] = max(dp[i][j], dp[i - 2][j - 1] + a[i - 1])
                elif i == 1:
                    dp[i][j] = max(dp[i][j], a[0])
    return max(dp[n][j] for j in range(m + 1))


def plant_trees_wqs(a, m):
    """WQS 二分(P1484 至多 m 棵).
    对每个惩罚 c: 每选一棵价值 -c, 无数量限制 DP 求 h(c)=max(v(k)-ck) 及
    kmin(c)=argmax 中最小的 k。二分求最小 c>=0 使 kmin(c)<=m, ans=h(c)+c*m."""
    n = len(a)

    def solve(c):
        # dp0: 不种当前坑; dp1: 种当前坑. 各带 (价值, 棵数)
        # 初始允许 0 棵
        dp0v, dp0c = 0, 0
        dp1v, dp1c = -10 ** 18, 0
        for x in a:
            # 不种当前: 取 dp0/dp1 中价值大者; 相同时取棵数小者(最小 argmax)
            if dp0v > dp1v or (dp0v == dp1v and dp0c <= dp1c):
                ndp0v, ndp0c = dp0v, dp0c
            else:
                ndp0v, ndp0c = dp1v, dp1c
            # 种当前: 只能从 dp0 来
            ndp1v = dp0v + x - c
            ndp1c = dp0c + 1
            dp0v, dp0c = ndp0v, ndp0c
            dp1v, dp1c = ndp1v, ndp1c
        if dp0v > dp1v or (dp0v == dp1v and dp0c <= dp1c):
            return dp0v, dp0c
        return dp1v, dp1c

    lo, hi = 0, 10 ** 9
    ans = None
    while lo <= hi:
        mid = (lo + hi) // 2
        v, cnt = solve(mid)
        if cnt <= m:
            ans = v + mid * m
            hi = mid - 1
        else:
            lo = mid + 1
    return ans


if __name__ == "__main__":
    for _ in range(300):
        n = random.randint(1, 9)
        a = [random.randint(-8, 8) for _ in range(n)]
        m = random.randint(0, (n + 1) // 2)
        bv = plant_trees_brute(a, m)
        wv = plant_trees_wqs(a, m)
        if wv != bv:
            print("MISMATCH", a, m, "brute=", bv, "wqs=", wv)
            break
    else:
        print("plant_trees WQS vs brute: all matched!")
    print("a=[1..5], m=2 ->", plant_trees_wqs([1, 2, 3, 4, 5], 2),
          "brute:", plant_trees_brute([1, 2, 3, 4, 5], 2))

```

**PyPy 提示**: solve_with_penalty 内部是 O(n) 或 O(n log n) 贪心/DP，整个 WQS 二分 O(n log C)。Python 1e5 级 30~40 次二分可过；内层要避免高开销写法，PyPy 优势明显。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(T log C), T 为单次无限制问题复杂度, C 为惩罚值域 |
| 空间 | O(n) |

### 局限

必须满足价值关于个数凸/凹（需要证明，非凸会二分出错误答案）。共线（多个 k 取到相同最大值）时需要固定 argmax 方向，否则二分会振荡。惩罚值域要包含最优斜率。恰好 k 个 vs 至多 k 个边界处理不同。二维限制（同时限个数和另一参数）需升级为三分/特殊处理，复杂度上升。Python 若 T 较大(如 O(n log n)) 总时间可能吃紧。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1484 | 4 | 种树: 至多 m 棵不相邻最大收益, WQS 模板题 | [https://www.luogu.com.cn/problem/P1484](https://www.luogu.com.cn/problem/P1484) |
| Luogu | P2619 | 4 | 国家集训队 Tree I: 恰好 k 条白边的最小生成树, WQS+MST | [https://www.luogu.com.cn/problem/P2619](https://www.luogu.com.cn/problem/P2619) |
| Codeforces | 739E | 5 | Gosha is hunting: 二维 WQS(球与种子双惩罚), 经典进阶题 | [https://codeforces.com/problemset/problem/739/E](https://codeforces.com/problemset/problem/739/E) |

## Pitfalls · 易错点

- 未证明 v(k) 凸性就二分, 非凸时结果错误
- 共线情形没固定 argmax(取最大/最小 k), 二分会死循环或答错
- 还原答案时错用 cnt 而非 k: 必须是 val + mid*k
- 恰好 k 个与至多 k 个的边界(初始惩罚范围)混淆
- 惩罚整数二分时斜率可能为半整数, 需处理小数斜率

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/dp/opt/wqs-binary-search/](https://oi-wiki.org/dp/opt/wqs-binary-search/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/dp/opt/wqs-binary-search.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/dp/opt/wqs-binary-search.md)
- web ✓ [https://codeforces.com/blog/entry/98334](https://codeforces.com/blog/entry/98334)
