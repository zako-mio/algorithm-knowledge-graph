---
id: enclosing-circle
name: 最小覆盖圆
group: G-D-1
stage: advanced
priority: P1
depth_tier: standard
---

# 最小覆盖圆

> 随机增量法 O(期望n) 求覆盖所有点的最小圆(Welzl)

<!-- 元信息: id=enclosing-circle · group=G-D-1 · stage=advanced · priority=P1 · depth_tier=standard -->

## What · 是什么

最小覆盖圆（Minimum Enclosing Circle, MEC）：给定平面上 n 个点，求半径最小的圆覆盖所有点。最小覆盖圆由边界上的 2 或 3 个点决定：要么是某两点为直径的圆，要么是三点确定的外接圆。Welzl 随机增量法：把点随机打乱，维护当前最小覆盖圆，逐点加入；若新点在圆外，则新最小圆必过该点，于是以该点为约束再对前面已加入的点做一层增量（直径圆），若仍有点在圆外，则再过该点作三层约束得三点外接圆。期望复杂度 O(n)，最坏 O(n^3) 但随机序下概率上几乎不发生。

## Why · 为什么

### 直觉 · Intuition

圆是'平滑'的：如果最小圆 C 已覆盖前 i-1 个点，加入第 i 个点时它不在 C 内，那么新的最小圆必然贴着第 i 个点（圆要'涨大'直到碰到它）。接下来把'必须过点 i'当作硬约束再扫一遍前面的点：某点 j 在圆外则新圆必过 j 和 i（以 ij 为直径），再扫更前的点 k：k 在圆外则新圆必过 i、j、k 三点（外接圆）。三层递进就是 Welzl 的递归结构——'必过某几个点'的限制逐步增强，最终唯一确定圆。

### 原理 · Principle

数学核心：MEC 唯一，且要么由直径两点决定，要么由圆周上三点决定（若所有圆候选在半径 r 下交点非单点，则可再缩小半径，矛盾）。Welzl 用递归 minidisk(P, R)：R 是'必在圆周上'的点集（|R|≤3）。若 P 为空或 |R|=3，由 R 直接定圆；否则取 P 中一点 p，递归算 minidisk(P\{p}, R)，若 p 不在圆内则令 R'=R∪{p} 递归。随机化保证期望 O(n)：p 不在圆内的概率 ≤ 3/(当前规模)，而每次递归的代价与其规模成正比，总期望线性。代码通常写成三层嵌套循环（去递归版），最内层对三点求外接圆。

### 历史 · History

Welzl 于 1991 年在《Smallest enclosing disks (balls and ellipsoids)》(LNCS 555, Results and Trends in Theoretical Computer Science) 中提出随机增量算法，奠定了'随机化增量法'在计算几何的地位；最小覆盖圆问题本身可追溯至 Sylvester 1857 年。CP 圈内经 e-maxx / cp-algorithms 整理为标准模板，OI-wiki 的 random-incremental 页收录。模板题 Luogu P1742、Library Checker min_enclosing_circle。

## How · 实现

### 伪代码

```python
# 输入: 点数组, 随机打乱
# 维护 (cx, cy, r)
cx, cy = p[0]; r = 0
for i in range(1, n):
    if p[i] 在圆内: continue
    cx, cy = p[i]; r = 0            # 以 i 为直径起点，圆必过 i
    for j in range(0, i):
        if p[j] 在圆内: continue
        cx, cy = (p[i]+p[j])/2; r = |ij|/2    # 直径圆，圆必过 i,j
        for k in range(0, j):
            if p[k] 在圆内: continue
            (cx, cy, r) = 外接圆(p[i], p[j], p[k])
```

### Python 实现

```python
# -*- coding: utf-8 -*-
import math
import random


def circle_from_3(a, b, c):
    """三点外接圆，返回 (cx, cy, r)；三点共线返回 None。"""
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
    """Welzl 随机增量法求最小覆盖圆，期望 O(n)。"""
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


if __name__ == '__main__':
    import itertools
    pts = [(0, 0), (4, 0), (0, 3)]
    cx, cy, r = enclosing_circle(pts)
    assert abs(r - 2.5) < 1e-9 and abs(cx - 2.0) < 1e-9, (cx, cy, r)
    # 暴力对拍
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
        assert all(math.hypot(p[0]-cx, p[1]-cy) <= r + 1e-7 for p in P), (P, cx, cy, r)
        assert abs(r - mec_brute(P)) < 1e-6, (r, mec_brute(P))
    print('enclosing-circle all tests passed')

```

**PyPy 提示**: random.shuffle 用 O(n)；内层循环在随机序下期望只触发极少次。浮点求外接圆的分母 \|d\| 接近 0 时数值不稳定，三点近共线会退化，需要特判或提升精度（可用 numpy 矩阵求解但竞赛不必要）。PyPy 下 1e6 点可轻松通过模板题。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 期望 O(n)（随机序）；最坏 O(n^3)（构造数据） |
| 空间 | O(n) |

### 局限

依赖随机化保证期望复杂度，构造恶意数据可能退化到 O(n^3)；浮点坐标下外接圆求解有数值误差，三点近共线需 eps 处理；共线/重复点导致退化时最内层外接圆返回 None 需跳过；输出圆心与半径精度按题目要求（通常 1e-6）。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1742 | 4 | 最小圆覆盖：随机增量法模板题 | [https://www.luogu.com.cn/problem/P1742](https://www.luogu.com.cn/problem/P1742) |
| Luogu | P3222 | 5 | [HNOI2012] 射箭：最小覆盖圆 + 可行性二分等综合 | [https://www.luogu.com.cn/problem/P3222](https://www.luogu.com.cn/problem/P3222) |
| Library Checker | min_enclosing_circle | 4 | MEC 官方评测题（Welzl 模板验证） | [https://judge.yosupo.jp/problem/min_enclosing_circle](https://judge.yosupo.jp/problem/min_enclosing_circle) |

## Pitfalls · 易错点

- 必须随机打乱，否则最坏 O(n^3)
- 外接圆三点共线时返回 None，需跳过（此时圆由直径决定）
- 内层循环起点：第二层 j 从 1 开始（i 为第 0 层约束），第三层 k 从 0 开始
- 浮点精度：判点是否在圆内用 r+eps，外接圆求解用 double/更高精度
- 单点/两点输入退化：半径为 0 或半直径
- 随机种子问题：部分 OJ 需要确定打乱方式（shuffle 即可）

## Sources · 信源

- CP-Algorithms ✓ [https://cp-algorithms.com/geometry/enclosing-circle.html](https://cp-algorithms.com/geometry/enclosing-circle.html)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/geometry/random-incremental.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/geometry/random-incremental.md)
- 书籍 ✓ `CPH ch29`
