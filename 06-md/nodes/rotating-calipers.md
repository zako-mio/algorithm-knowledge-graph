---
id: rotating-calipers
name: 旋转卡壳
group: G-D-1
stage: advanced
priority: P1
depth_tier: standard
---

# 旋转卡壳

> 在凸包上枚举对踵点，O(n) 求凸包直径/最小矩形覆盖

<!-- 元信息: id=rotating-calipers · group=G-D-1 · stage=advanced · priority=P1 · depth_tier=standard -->

## What · 是什么

旋转卡壳（Rotating Calipers）是在凸包上求解与凸包几何性质相关极值问题的线性算法族。核心思想：逆时针枚举凸包的每条边，同时维护一个指针指向'离当前边最远'的顶点（对踵点），由于凸包上'离边最远点'随边的旋转单调移动，指针总共只会前进 O(n) 步，从而在 O(n) 内求出凸包直径（最远点对距离平方）、最小面积矩形覆盖等。必须先求出凸包（Andrew/Graham），再在凸包上运行。

## Why · 为什么

### 直觉 · Intuition

想象用两把平行卡尺从两边夹住凸包，一边贴合一条边，另一边顶在对面的顶点上；卡尺绕凸包转一圈，每次'边—对踵点'的距离就是该方向上的宽度，最大值即直径。因为凸包是凸的，当边旋转时对踵点只会沿凸包单向移动（不会倒转），所以用一个'单调指针'就能线性维护最优点——这是分治与双指针思想的几何版。

### 原理 · Principle

对凸包顶点按逆时针 p0..p_{m-1} 存储。对每条边 (i, i+1)，用叉积绝对值 |cross(p_i, p_{i+1}, p_j)| 度量点 p_j 到该边所在直线的'两倍三角形面积'（同底边，面积大小正比于高），在 j 处比较 j+1 是否更远，是则前进。直径候选为 dist(p_i, p_j) 与 dist(p_{i+1}, p_j)。正确性：凸包直径必然出现在某对'边—对踵点'之间（最远点对至少有一个点是某条边的对踵点），且单调指针保证每个对踵对至少被访问一次。最小矩形覆盖还需对每条边同时维护左右两侧用点积投影度量的最远点（l 与 r），面积 = (边方向的宽度)×(垂直方向的投影跨度)。

### 历史 · History

Rotating Calipers 术语与概念由 Godfried Toussaint 于 1983 年在论文《Solving geometric problems with the rotating calipers》(MELECON '83) 中系统提出；其思想渊源可追溯至 Shamos 1978 年的计算几何博士论文中凸多边形直径的线性算法。此后被扩展为求解凸多边形最小面积外接矩形、两凸多边形最近/最远距离、并集周长等一大族问题。

## How · 实现

### 伪代码

```python
# hull: 凸包逆时针顶点列表, m = len(hull)
# 求直径（最远点对距离平方）
def rotating_calipers_diameter(hull):
    if m == 1: return 0
    if m == 2: return dist2(hull[0], hull[1])
    j = 1; best = 0
    for i in range(m):
        ni = (i+1) % m
        while |cross(hull[i], hull[ni], hull[(j+1)%m])| > |cross(hull[i], hull[ni], hull[j])|:
            j = (j+1) % m
        best = max(best, dist2(hull[i], hull[j]), dist2(hull[ni], hull[j]))
    return best
```

### Python 实现

```python
# -*- coding: utf-8 -*-


def cross(o, a, b):
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])


def dist2(a, b):
    return (a[0]-b[0])**2 + (a[1]-b[1])**2


def convex_hull(points):
    pts = sorted(set(points))
    if len(pts) <= 1:
        return pts
    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    res = []
    for p in lower[:-1] + upper[:-1]:
        if not res or res[-1] != p:
            res.append(p)
    return res


def diameter(hull):
    """凸包直径：最远点对距离的平方。hull 为逆时针凸包。"""
    m = len(hull)
    if m == 1:
        return 0
    if m == 2:
        return dist2(hull[0], hull[1])
    j = 1
    best = 0
    for i in range(m):
        ni = (i + 1) % m
        while abs(cross(hull[i], hull[ni], hull[(j+1) % m])) > abs(cross(hull[i], hull[ni], hull[j])):
            j = (j + 1) % m
        best = max(best, dist2(hull[i], hull[j]), dist2(hull[ni], hull[j]))
    return best


if __name__ == '__main__':
    import random
    # 正方形对角线
    sq = [(0, 0), (10, 0), (10, 10), (0, 10)]
    h = convex_hull(sq)
    assert diameter(h) == 200, diameter(h)
    # 与 O(n^2) 暴力对拍
    for _ in range(200):
        pts = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(40)]
        hull = convex_hull(pts)
        brute = max(dist2(a, b) for a in pts for b in pts)
        assert diameter(hull) == brute, (diameter(hull), brute)
    # 退化
    assert diameter(convex_hull([(1, 1)])) == 0
    assert diameter(convex_hull([(1, 1), (4, 5)])) == 25
    print('rotating-calipers all tests passed')

```

**PyPy 提示**: 整数坐标全流程整数运算（叉积、距离平方），无精度问题；求'直径'时距离用平方表示，开根只在输出时做一次。Python 的 % 取模与函数调用较多，可把 cross 内联提升常数性能；PyPy 下双指针循环可轻松跑 1e6 级凸包顶点。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n)（在凸包上，凸包构建另需 O(n log n)） |
| 空间 | O(n) |

### 局限

必须先构建凸包；凸包顶点数 < 3 时直径定义退化需特判；多组平行等距边时 while 条件用 > 可能漏掉并列对踵点（用 >= 会在并列时多走几步但结果仍正确）；求浮点坐标的最小矩形覆盖时叉积/点积比较需 eps，且输出四角要小心数值误差。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1452 | 3 | Beauty Contest：凸包 + 旋转卡壳求最大距离（直径模板） | [https://www.luogu.com.cn/problem/P1452](https://www.luogu.com.cn/problem/P1452) |
| Luogu | P3187 | 5 | 最小矩形覆盖：维护对踵点 + 左右投影点，O(n) 求最小面积外接矩形 | [https://www.luogu.com.cn/problem/P3187](https://www.luogu.com.cn/problem/P3187) |
| AtCoder | abc130_f | 4 | Minimum Bounding Box：凸包枚举方向求最小外接矩形（卡壳思路） | [https://atcoder.jp/contests/abc130/tasks/abc130_f](https://atcoder.jp/contests/abc130/tasks/abc130_f) |

## Pitfalls · 易错点

- 忘记先求凸包直接在原点上跑双指针会得到错误答案
- 指针初始化 j=1 要从凸包第二点开始，否则第一条边的对踵点遗漏
- 凸包退化（顶点 < 3）时 diameter 需特判
- 并列最远点时 while 用 > 可能跳过部分对踵对；对拍验证
- 求最小矩形时左右投影点 l、r 的单调性要独立维护，不能共用一个指针
- 输出距离时漏开根（题目要求整数平方时除外）

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/geometry/rotating-calipers.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/geometry/rotating-calipers.md)
- 书籍 ✓ `CPH ch29`
- CP-Algorithms ✓ [https://cp-algorithms.com/geometry/minkowski.html](https://cp-algorithms.com/geometry/minkowski.html)
