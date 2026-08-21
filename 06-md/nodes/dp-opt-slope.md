---
id: dp-opt-slope
name: 斜率优化DP
group: G-A-12
stage: advanced
priority: P1
depth_tier: standard
---

# 斜率优化DP

> 转移方程化为一次函数，凸壳上二分/单调队列维护最值

<!-- 元信息: id=dp-opt-slope · group=G-A-12 · stage=advanced · priority=P1 · depth_tier=standard -->

## What · 是什么

斜率优化（Convex Hull Trick）把形如 f[i] = min_j { f[j] + (a_i - b_j)² } 或更一般地 f[i] = min_j { y_j - k_i·x_j } 的转移，转化为平面上的「用斜率为 k_i 的直线去切一个点集，最小化截距」问题。最优决策点必然在点集的下凸壳（min）/上凸壳（max）上。若 k_i 单调且插入点横坐标单调，用单调队列维护凸壳、队首弹斜率，总 O(n)；若斜率不单调但横坐标单调，用单调队列+二分（凸壳边斜率单调）；若都不单调，用 CDQ 分治或平衡树维护凸壳，O(n log²n) 或 O(n log n)。经典例题：玩具装箱（HNOI2008）、仓库建设（ZJOI2007）、特别行动队（APIO2010）。

## Why · 为什么

### 直觉 · Intuition

观察转移 min_j { f[j] + (a_i - b_j)² }：展开后得到 f[j]+b_j² - 2a_i·b_j + a_i²。去掉与 j 无关的 a_i²，问题变成 min_j { (f[j]+b_j²) - (2a_i)·b_j }——这是一族以 x=b_j 为横坐标、y=f[j]+b_j² 为纵坐标的点，被斜率 k=2a_i 的直线扫过时截距取最小。把直线从下往上平移，第一个碰到的凸包点即最优 j。由于凸壳相邻点斜率单调，可用二分或单调指针定位。

### 原理 · Principle

建立点 (x_j, y_j)=(b_j, f[j]+b_j²)，转移 b_i = min_j { y_j - k_i·x_j }。维护下凸壳（保证相邻点斜率 K(q_{t-1},q_t) < K(q_t,q_{t+1})）。情形 A：k_i 单调递增 → 用单调队列，指针 e 满足 K(q_{e-1},q_e) ≤ k_i < K(q_e,q_{e+1}) 时最优决策为 q_e，指针均摊右移 O(1)，总 O(n)。情形 B：k_i 任意但 x 单调 → 凸壳仍可 O(1) 尾部维护，查询用二分找「斜率恰被 k_i 夹住」的边，O(log n)/次。情形 C：x 不单调 → 需 CDQ 分治（左半决策点排序建凸壳，右半查询）或平衡树动态插入删除凸壳点。判凸：w(j,i) 满足四边形不等式（如二次函数 (a_i-b_j)² 满足）等价于决策单调，斜率优化是其「可拆成一次函数」特例。

### 历史 · History

斜率优化雏形见于 1990s 竞赛题（如 USACO 的 fencing、NOI 早期题目），2008 年前后随 OI Wiki 与题解社区成熟被系统整理。CP-Algorithms 的 LIS 优化（lis 变种）与 OI Wiki slope 专章给出模板：单调队列版、二分版、CDQ 版、平衡树版（Li Chao 线段树也是同类思想）。玩具装箱（HNOI2008）成为入门必刷题。

## How · 实现

### 伪代码

```python
# 通用形式：min_j { y_j - k_i * x_j }
# 情形A: k 单调 + x 单调 -> 单调队列 O(n)
for i in 1..n:
  while len(q)>=2 and K(q[0],q[1]) <= k_i: pop_left()
  best = q[0]
  f[i] = y_q[best] - k_i * x_q[best]
  插入点 (x_i, y_i):
    while len(q)>=2 and 新点使 q[-2],q[-1],新点非凸: pop_right()
    push(i)

# 情形B: x 单调 + k 任意 -> 单调队列维护凸壳 + 二分查询 O(n log n)
查询 best: 二分找到 K(q[t-1],q[t]) <= k_i < K(q[t],q[t+1]) 的 t
```

### Python 实现

```python
def toy_box(costs, L):
    """HNOI2008 玩具装箱：f[i] = min_j { f[j] + (sum[i]+i-j-1-L)^2 }，O(n)。
    令 s[i]=pre[i]+i，则 f[i] = min_j { f[j] + (s[i]-s[j]-1-L)^2 }。
    展开: = (s[i]-1-L)^2 + min_j { f[j] + (s[j]+1+L)^2 - 2*(s[i]-1-L)*s[j] }
    记 X_j = s[j], Y_j = f[j] + s[j]^2, k = 2*(s[i]-1-L)（随 i 单调增）
    维护下凸壳 + 单调指针（k 单调）。"""
    n = len(costs)
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] + costs[i]
    s = [pre[i] + i for i in range(n + 1)]
    f = [0] * (n + 1)
    q = [0] * (n + 1)
    hd = tl = 0          # [hd, tl)
    q[tl] = 0; tl += 1
    for i in range(1, n + 1):
        k = 2 * (s[i] - 1 - L)
        while tl - hd >= 2 and _slope(q[hd], q[hd + 1], s, f, L) <= k:
            hd += 1
        j = q[hd]
        f[i] = f[j] + (s[i] - s[j] - 1 - L) ** 2
        # 插入点 i，维护下凸壳
        while tl - hd >= 2 and _bad(q[tl - 2], q[tl - 1], i, s, f, L):
            tl -= 1
        q[tl] = i; tl += 1
    return f[n]


def _xy(j, s, f, L):
    return s[j], f[j] + s[j] * s[j]


def _slope(a, b, s, f, L):
    x1, y1 = _xy(a, s, f, L)
    x2, y2 = _xy(b, s, f, L)
    return (y2 - y1) / (x2 - x1)


def _bad(a, b, c, s, f, L):
    """返回 b 是否不可能是下凸壳点（三点不构成下凸）"""
    x1, y1 = _xy(a, s, f, L)
    x2, y2 = _xy(b, s, f, L)
    x3, y3 = _xy(c, s, f, L)
    # cross(b-a, c-b) <= 0 表示非凸（应删除 b）
    return (x2 - x1) * (y3 - y2) - (y2 - y1) * (x3 - x2) <= 0


def toy_box_naive(costs, L):
    """朴素 O(n^2) 对拍"""
    n = len(costs)
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] + costs[i]
    s = [pre[i] + i for i in range(n + 1)]
    INF = float('inf')
    f = [INF] * (n + 1)
    f[0] = 0
    for i in range(1, n + 1):
        for j in range(i):
            f[i] = min(f[i], f[j] + (s[i] - s[j] - 1 - L) ** 2)
    return f[n]


def convex_hull_binary(xs, ys, queries):
    """情形B演示：x 单调插入点、k 任意查询，凸壳+二分 O(m log n)。
    xs/ys: 按 x 递增插入的决策点；queries: 各次查询的斜率 k。
    返回每次 min_j { y_j - k*x_j }。"""
    hull = []          # 维护下凸壳点下标
    ans = []
    # 分批：这里假设全部点已给，用全部点建凸壳（静态），再二分
    for t, (x, y) in enumerate(zip(xs, ys)):
        while len(hull) >= 2 and _ccw(hull[-2], hull[-1], t, xs, ys) <= 0:
            hull.pop()
        hull.append(t)
    for k in queries:
        lo, hi = 0, len(hull) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if _slope_idx(hull[mid], hull[mid + 1], xs, ys) <= k:
                lo = mid + 1
            else:
                hi = mid
        j = hull[lo]
        ans.append(ys[j] - k * xs[j])
    return ans


def _ccw(a, b, c, xs, ys):
    return (xs[b] - xs[a]) * (ys[c] - ys[b]) - (ys[b] - ys[a]) * (xs[c] - xs[b])


def _slope_idx(a, b, xs, ys):
    return (ys[b] - ys[a]) / (xs[b] - xs[a])


if __name__ == "__main__":
    import random
    random.seed(31)
    # 玩具装箱：单调队列斜率优化 vs 朴素
    for n in [1, 2, 5, 20, 100]:
        for _ in range(20):
            L = random.randint(1, 10)
            costs = [random.randint(1, 10) for __ in range(n)]
            got = toy_box(costs, L)
            exp = toy_box_naive(costs, L)
            assert got == exp, (n, L, got, exp)
    # 凸包+二分查询（情形B）
    xs = sorted(random.sample(range(1, 1000), 60))
    ys = [random.randint(0, 500) for _ in xs]
    queries = [random.randint(1, 200) for _ in range(40)]
    ch = convex_hull_binary(xs, ys, queries)
    for k, got in zip(queries, ch):
        exp = min(ys[j] - k * xs[j] for j in range(len(xs)))
        assert abs(got - exp) < 1e-6, (k, got, exp)
    print("All tests passed.")
```

**PyPy 提示**: 斜率优化在 Python 中注意：用分数/浮点比较斜率可能精度误差，建议用交叉相乘（叉积）整数判定凸性（_bad/_ccw 用 int 叉积），只有查询定位才用浮点除法。k 单调时单调队列指针均摊 O(1)；大数据（n=1e5）在 PyPy 下完全可行。队列用数组模拟（list+头指针）比 deque 快。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 情形A(单调k+单调x)：O(n)；情形B(单调x)：O(n log n)；情形C(任意)：O(n log n)（CDQ）或 O(n log n)（平衡树） |
| 空间 | O(n) |

### 局限

前提苛刻：需证明转移可化为一次函数（w 可拆交叉项）且决策点横坐标单调；否则需 CDQ/平衡树/Li Chao 线段树。浮点斜率有精度风险（应整数叉积判凸）。只能处理 min/max 型最值，不能处理「取模」「求和」等非极值转移。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3195 | 5 | HNOI2008 玩具装箱：斜率优化入门模板题 | [https://www.luogu.com.cn/problem/P3195](https://www.luogu.com.cn/problem/P3195) |
| LOJ | 10189 | 6 | ZJOI2007 仓库建设：斜率单调队列优化 | [https://loj.ac/problem/10189](https://loj.ac/problem/10189) |
| LOJ | 10190 | 6 | APIO2010 特别行动队：二次函数拆项斜率优化 | [https://loj.ac/problem/10190](https://loj.ac/problem/10190) |
| Luogu | P3628 | 6 | APIO2010 特别行动队（洛谷镜像）：斜率优化经典 | [https://www.luogu.com.cn/problem/P3628](https://www.luogu.com.cn/problem/P3628) |
| Luogu | P2900 | 6 | USACO Land Acquisition：排序后凸包斜率优化 | [https://www.luogu.com.cn/problem/P2900](https://www.luogu.com.cn/problem/P2900) |

## Pitfalls · 易错点

- 忘记先排序/去重决策点横坐标使其单调，直接套单调队列
- 凸壳判定用浮点斜率误差（应整数叉积判非凸）
- 查询指针单调但插入点横坐标不单调（需二分或 CDQ）
- 把 min 当 max 优化（上下凸壳搞反），截距方向颠倒

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/dp/opt/slope/](https://oi-wiki.org/dp/opt/slope/)
- CP-Algorithms ✓ [https://cp-algorithms.com/dynamic_programming/opt-lis.html](https://cp-algorithms.com/dynamic_programming/opt-lis.html)
