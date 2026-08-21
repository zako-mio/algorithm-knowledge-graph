---
id: convex-hull
name: 凸包(Andrew/Graham)
group: G-D-1
stage: intermediate
priority: P1
depth_tier: standard
---

# 凸包(Andrew/Graham)

> O(nlogn) 求点集凸包，Andrew 单调链与 Graham 扫描两种实现

<!-- 元信息: id=convex-hull · group=G-D-1 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

凸包是包含点集中所有点的最小凸多边形。求解思路是把点按序扫描，用单调栈维护'一路左转'的凸壳：Andrew 单调链按 x 为第一关键字、y 为第二关键字排序，先扫出下凸壳再扫出上凸壳合并；Graham 扫描则取最低点（y 最小、x 次小）为极，其余点按极角排序后逐个压栈，遇到右转就弹栈。两者均为 O(n log n)（瓶颈是排序），且被证明是渐近最优的。凸包是旋转卡壳、凸包优化(CHT)、半平面交、闵可夫斯基和等几乎所有计算几何高级算法的前置结构。

## Why · 为什么

### 直觉 · Intuition

想象用一根橡皮筋把点集绷紧，松开后橡皮筋的轮廓就是凸包。'左转/右转'直觉：从凸包上一点沿逆时针走，每一步都是左转；一旦出现右转就说明中间那个点凹进去了，可以被移除。Andrew 分上下壳扫描：从最左下走到最右上构成下壳（像船底），从最右上走回最左下构成上壳（像船顶），因为上下壳的转向约定相反，所以要用两次方向相反的扫描。

### 原理 · Principle

Andrew：排序后升序扫一遍用叉积条件 (p[stk[-2]]→p[stk[-1]])×(p[stk[-1]]→p[i]) ≤ 0 弹栈得到下凸壳（弹掉共线点可选 ≤ 或 <），记录 size 后降序再扫一遍得到上凸壳，两壳拼接（头尾重复一个点）得到完整凸包。正确性来自凸多边形上相邻三点的叉积符号恒定非负。Graham：P0 为最低点，其余点按极角排序；因为扫描顺序即极角序，任意相邻三点在凸包上必然左转，右转则中间点出栈。复杂度瓶颈均为排序 O(n log n)。若要求凸包包含所有共线边界点，把弹栈条件从 < 改成 ≤ 或单独处理极径最大点序列。

### 历史 · History

Graham 扫描由 Ronald Graham 于 1972 年发表；Andrew 单调链（Monotone Chain）由 Andrew 于 1979 年提出。二者都是计算几何最早的经典算法，被写入 Preparata & Shamos《Computational Geometry》(1985) 等教材。因为排序下界，O(n log n) 被证明是点集凸包的渐近最优复杂度（除非输入有序或允许随机化/在线处理）。

## How · 实现

### 伪代码

```python
# Andrew 单调链
pts.sort() by (x, y)
lower = []
for p in pts:
    while len(lower)>=2 and cross(lower[-2], lower[-1], p) <= 0: lower.pop()
    lower.append(p)
upper = []
for p in reversed(pts):
    while len(upper)>=2 and cross(upper[-2], upper[-1], p) <= 0: upper.pop()
    upper.append(p)
hull = lower[:-1] + upper[:-1]   # 逆时针，含所有凸包顶点

# cross(o,a,b) = (a-o)×(b-o)
# 用 <= 0 弹栈 → 不保留共线边界点；用 < 0 → 保留
```

### Python 实现

```python
# -*- coding: utf-8 -*-


def cross(o, a, b):
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])


def convex_hull(points, keep_collinear=False):
    """Andrew 单调链。返回逆时针凸包顶点（首尾不重复）。
    keep_collinear=True 时保留共线边界点。
    """
    cmp = lambda x: x <= 0 if not keep_collinear else x < 0
    pts = sorted(set(points))
    if len(pts) <= 1:
        return pts
    lower = []
    for p in pts:
        while len(lower) >= 2 and cmp(cross(lower[-2], lower[-1], p)):
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cmp(cross(upper[-2], upper[-1], p)):
            upper.pop()
        upper.append(p)
    hull = lower[:-1] + upper[:-1]
    # 去掉拼接处的连续重复点（全共线/退化时会出现）
    res = []
    for p in hull:
        if not res or res[-1] != p:
            res.append(p)
    return res


def polygon_area(poly):
    s = 0.0
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i+1) % n]
        s += x1*y2 - x2*y1
    return abs(s) / 2.0


def pip_ray(p, poly):
    x, y = p
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i+1) % n]
        if (y1 > y) != (y2 > y):
            xi = x1 + (x2-x1)*(y-y1)/(y2-y1)
            if x < xi:
                inside = not inside
    return inside


if __name__ == '__main__':
    sq = [(0, 0), (1, 0), (1, 1), (0, 1)]
    h = convex_hull(sq)
    assert len(h) == 4 and abs(polygon_area(h) - 1.0) < 1e-9
    # 共线点只保留两端
    col = [(0, 0), (1, 1), (2, 2)]
    h2 = convex_hull(col)
    assert len(h2) == 2, h2
    # 矩形边界上有内部共线点：keep_collinear 时保留
    rect = [(0, 0), (2, 0), (1, 0), (2, 2), (0, 2), (1, 2)]
    h3 = convex_hull(rect)
    assert len(h3) == 4, h3
    h3c = convex_hull(rect, keep_collinear=True)
    assert (1, 0) in h3c and (1, 2) in h3c and len(h3c) == 6, h3c
    # 随机点全部被覆盖
    import random
    pts = [(random.randint(-50, 50), random.randint(-50, 50)) for _ in range(300)]
    hull = convex_hull(pts)
    for p in pts:
        ok = True
        for i in range(len(hull)):
            if cross(hull[i], hull[(i+1) % len(hull)], p) < -1e-9:
                ok = False
                break
        assert ok, p
    for i in range(len(hull)):
        assert cross(hull[i], hull[(i+1) % len(hull)], hull[(i+2) % len(hull)]) >= -1e-9
    print('convex-hull all tests passed')

```

**PyPy 提示**: Python 实现注意：(1) 去重用 set 或排序后去重，重复点会破坏单调栈不变量；(2) 整点坐标用整数叉积（不涉及除法）天然无精度损失，凸包模板应全程整数运算；(3) 超过 1e6 点时不建议 Python 硬扛，PyPy 下常数仍大，大 N 换 C++。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n log n)，瓶颈为排序；单调栈部分线性 |
| 空间 | O(n) |

### 局限

浮点坐标下叉积判符号受 eps 影响，共线点归属需明确约定（保留与否）；退化情况：n≤1、所有点共线、重复点需特判；若要求输出周长/面积注意首尾顶点是否重复；Andrew 对 y 轴平行的竖直线族也适用（排序已处理），但 Graham 对重合极角需要按距离排序。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P2742 | 3 | 【模板】二维凸包：Andrew 模板题，求凸包周长 | [https://www.luogu.com.cn/problem/P2742](https://www.luogu.com.cn/problem/P2742) |
| Luogu | P1452 | 3 | Beauty Contest：凸包 + 旋转卡壳求直径（凸包前置） | [https://www.luogu.com.cn/problem/P1452](https://www.luogu.com.cn/problem/P1452) |
| Luogu | P3829 | 4 | 信用卡凸包：将圆角图形规约为偏移后的点集凸包 + 周长 | [https://www.luogu.com.cn/problem/P3829](https://www.luogu.com.cn/problem/P3829) |

## Pitfalls · 易错点

- 排序后未去重导致栈内重复点/退化（先 set 去重）
- 弹栈条件 <= 与 < 的选择决定是否保留共线边界点，题目语义要提前确认
- 上下壳拼接时去掉重复的首尾点，否则周长/面积会算错
- 浮点坐标直接比较 == 判重会误判，整点问题用整数或 eps 判重
- Graham 的极角排序需处理极角相等时按距离排序
- 凸包顶点数 < 3 时（退化）调用旋转卡壳等算法要特判

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/geometry/convex-hull.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/geometry/convex-hull.md)
- CP-Algorithms ✓ [https://cp-algorithms.com/geometry/convex-hull.html](https://cp-algorithms.com/geometry/convex-hull.html)
- 书籍 ✓ `CPH ch29`
