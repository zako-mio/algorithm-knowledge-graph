---
id: random-incremental
name: 随机增量法
group: G-D-3
stage: advanced
priority: P2
depth_tier: standard
---

# 随机增量法

> 按随机序逐点加入并增量维护结构，期望线性复杂度

<!-- 元信息: id=random-incremental · group=G-D-3 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

随机增量法（Randomized Incremental Construction）是计算几何的通用方法论：先把输入元素随机打乱，然后按序逐个加入，增量维护目标结构；每个新元素以'是否破坏当前结构'决定是否触发局部修复。核心是概率论证：对随机序，第 i 个元素触发修复的概率很小（通常 ≤ 常数/i），期望总复杂度线性。最经典应用是最小覆盖圆（Welzl）：圆外点触发 O(i) 修复，期望 O(n)。它还可用于三维凸包（增量删面补面）、随机增量三角剖分、最近点对期望分析等。

## Why · 为什么

### 直觉 · Intuition

增量法像'砌墙'：每放一块砖，若放对了继续，若放歪了（点落在当前圆外/结构外）就局部返工。随机打乱的意义：大部分点一进来就在当前结构内，什么都不做；只有'刺头'点（概率约 常数/i）才需要重扫前面的点。因为刺头通常位于结构边界附近，数量有界，所以平均下来每层修复成本被分摊成常数。

### 原理 · Principle

以最小覆盖圆为例（Welzl）：圆 O 是前 i-1 个点的最小覆盖圆，加入 p_i 若在圆内则 O 不变；否则新圆必过 p_i。此时以'过 p_i'为约束对前面 j<i 的点重做一层：直径圆 (p_i, p_j) 起步，若 p_j 在外则圆必过 p_i、p_j；再内层过三点的外接圆。数学上每层调用等价于 minidisk(P, R) 递归（R 为必过点集，|R|≤3）。概率论证：随机序下 p_i 不在当前圆内的概率 ≤ 3/i（因为最小覆盖圆由最多 3 个点决定，被它排除在外的概率与该点是否决定圆有关，平均为 O(1/i)），于是期望总时间 Σ O(i)·(3/i) = O(n)。

### 历史 · History

随机增量法由 Clarkson 与 Shor 在 1980 年代末系统化（Clarkson-Shor 随机增量技术），Welzl 1991 年将其应用到最小覆盖圆/球，成为计算几何随机化算法的范式。后由 Seidel、Mulmuley 等扩展到凸包、三角剖分等，是《Computational Geometry》教材中随机化章节的支柱内容。

## How · 实现

### 伪代码

```python
# 通用框架
shuffle(points)
结构 S = 由前 1~2 个元素构造
for i in range(n):
    if 元素 i 不破坏 S: continue
    以'必含元素 i'为约束, 增量重建局部: 
    for j in range(i):
        if j 不破坏: continue
        ... 逐层加深约束直到 |约束|=3

# 最小覆盖圆（Welzl 具体化）
cx, cy = p[0]; r = 0
for i in 1..n-1:
    if p[i] 在圆内: continue
    cx, cy = p[i]; r = 0                     # 约束: 圆必过 i
    for j in 0..i-1:
        if p[j] 在圆内: continue
        cx, cy = (p[i]+p[j])/2; r = |ij|/2   # 约束: 必过 i,j
        for k in 0..j-1:
            if p[k] 在圆内: continue
            外接圆(p[i], p[j], p[k])          # 三点定圆
```

### Python 实现

```python
# -*- coding: utf-8 -*-
import math
import random


def circle_from_3(a, b, c):
    ax, ay = a
    bx, by = b
    cx, cy = c
    d = 2 * (ax*(by-cy) + bx*(cy-ay) + cx*(ay-by))
    if abs(d) < 1e-15:
        return None
    ux = ((ax*ax + ay*ay)*(by-cy) + (bx*bx + by*by)*(cy-ay) + (cx*cx + cy*cy)*(ay-by)) / d
    uy = ((ax*ax + ay*ay)*(cx-bx) + (bx*bx + by*by)*(ax-cx) + (cx*cx + cy*cy)*(bx-ax)) / d
    return (ux, uy, math.hypot(ax-ux, ay-uy))


def enclosing_circle(points):
    """最小覆盖圆：随机增量（Welzl）的具体实现，期望 O(n)。"""
    pts = points[:]
    random.shuffle(pts)
    n = len(pts)
    if n == 0:
        return (0.0, 0.0, 0.0)
    cx, cy = pts[0]
    r = 0.0
    for i in range(1, n):
        if math.hypot(pts[i][0]-cx, pts[i][1]-cy) <= r + 1e-12:
            continue
        cx = (pts[i][0] + pts[0][0]) / 2
        cy = (pts[i][1] + pts[0][1]) / 2
        r = math.hypot(pts[i][0]-cx, pts[i][1]-cy)
        for j in range(1, i):
            if math.hypot(pts[j][0]-cx, pts[j][1]-cy) <= r + 1e-12:
                continue
            cx = (pts[i][0] + pts[j][0]) / 2
            cy = (pts[i][1] + pts[j][1]) / 2
            r = math.hypot(pts[i][0]-cx, pts[i][1]-cy)
            for k in range(j):
                if math.hypot(pts[k][0]-cx, pts[k][1]-cy) <= r + 1e-12:
                    continue
                c = circle_from_3(pts[i], pts[j], pts[k])
                if c:
                    cx, cy, r = c
    return (cx, cy, r)


def minidisk_recursive(points, fixed, memo=None):
    """Welzl 递归版（教学用）：minidisk(P, R)。fixed 是必在圆周上的点。"""
    P = points[:]
    if not P or len(fixed) == 3:
        if len(fixed) == 0:
            return (0.0, 0.0, 0.0)
        if len(fixed) == 1:
            a = fixed[0]
            return (a[0], a[1], 0.0)
        if len(fixed) == 2:
            a, b = fixed
            cx, cy = (a[0]+b[0])/2, (a[1]+b[1])/2
            return (cx, cy, math.hypot(a[0]-cx, a[1]-cy))
        return circle_from_3(*fixed) or (0.0, 0.0, 0.0)
    p = P.pop()
    c = minidisk_recursive(P, fixed)
    if math.hypot(p[0]-c[0], p[1]-c[1]) <= c[2] + 1e-12:
        return c
    return minidisk_recursive(P, fixed + [p])


if __name__ == '__main__':
    import itertools
    pts = [(0, 0), (4, 0), (0, 3)]
    cx, cy, r = enclosing_circle(pts)
    assert abs(r - 2.5) < 1e-9 and abs(cx - 2.0) < 1e-9, (cx, cy, r)
    c2 = minidisk_recursive(pts[:], [])
    assert abs(c2[2] - 2.5) < 1e-9, c2
    # 暴力对拍（覆盖所有点且半径最小）
    def mec_brute(P):
        best = 1e18
        for a in P:
            best = min(best, max(math.hypot(p[0]-a[0], p[1]-a[1]) for p in P))
        for a, b in itertools.combinations(P, 2):
            cx2, cy2 = (a[0]+b[0])/2, (a[1]+b[1])/2
            rr = math.hypot(a[0]-cx2, a[1]-cy2)
            if all(math.hypot(p[0]-cx2, p[1]-cy2) <= rr + 1e-9 for p in P):
                best = min(best, rr)
        for a, b, c in itertools.combinations(P, 3):
            cc = circle_from_3(a, b, c)
            if cc:
                cx2, cy2, rr = cc
                if all(math.hypot(p[0]-cx2, p[1]-cy2) <= rr + 1e-9 for p in P):
                    best = min(best, rr)
        return best
    for _ in range(100):
        P = [(random.uniform(-10, 10), random.uniform(-10, 10)) for _ in range(9)]
        cx, cy, r = enclosing_circle(P)
        assert all(math.hypot(p[0]-cx, p[1]-cy) <= r + 1e-7 for p in P)
        assert abs(r - mec_brute(P)) < 1e-6, (r, mec_brute(P))
    print('random-incremental all tests passed')

```

**PyPy 提示**: 随机增量对 Python 友好：主要成本在常数与随机打乱；内层三层循环在随机序下期望触发次数少。PyPy 下 1e6 点可过模板题。最小覆盖圆也可用模拟退火/三分近似解，但随机增量是精确解法。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 期望 O(n)（随机序）；最坏 O(n^3)（构造数据） |
| 空间 | O(n)（递归版额外 O(n) 栈深） |

### 局限

期望复杂度依赖随机化，恶意构造数据可退化到 O(n^3)；递归版在 n 大时栈深可能爆（Python 递归上限 ~1000），工程上常用三层循环迭代版；浮点下三点共线外接圆退化需特判；'概率 ≤ c/i'的论证需要随机均匀打乱（用 random.shuffle 即可）。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1742 | 4 | 最小圆覆盖：随机增量法模板题（本方法论最经典应用） | [https://www.luogu.com.cn/problem/P1742](https://www.luogu.com.cn/problem/P1742) |
| Luogu | P3222 | 5 | [HNOI2012] 射箭：随机增量思想 + 可行性二分综合 | [https://www.luogu.com.cn/problem/P3222](https://www.luogu.com.cn/problem/P3222) |
| Library Checker | min_enclosing_circle | 4 | MEC 官方评测（随机增量/ Welzl 验证） | [https://judge.yosupo.jp/problem/min_enclosing_circle](https://judge.yosupo.jp/problem/min_enclosing_circle) |

## Pitfalls · 易错点

- 忘记随机打乱，最坏数据直接 O(n^3)
- 内层循环的边界（j 从 1 起、k 从 0 起）写错导致结果偏差
- 递归版 Python 默认递归深度 ~1000，大 n 用迭代版
- 三点共线时外接圆返回 None 要跳过
- 浮点 eps 判定点是否在圆内，太小会反复触发修复
- 随机种子固定可能被 hack 构造退化数据（多数 OJ 无此问题）

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/geometry/random-incremental.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/geometry/random-incremental.md)
- CP-Algorithms ✓ [https://cp-algorithms.com/geometry/enclosing-circle.html](https://cp-algorithms.com/geometry/enclosing-circle.html)
- 书籍 ✓ `CPH ch29`
