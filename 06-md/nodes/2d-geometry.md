---
id: 2d-geometry
name: 二维几何基础
group: G-D-3
stage: basic
priority: P1
depth_tier: standard
---

# 二维几何基础

> 向量运算/点积叉积/多边形面积/线段相交/直线交点等二维计算几何基础

<!-- 元信息: id=2d-geometry · group=G-D-3 · stage=basic · priority=P1 · depth_tier=standard -->

## What · 是什么

二维计算几何基础是用坐标与向量表示点、线、多边形并在此基础上进行几何运算的模板代码族。核心原语包括：点积 dot(a,b)=x1x2+y1y2（衡量投影与垂直），叉积 cross(a,b)=x1y2-x2y1（衡量有向面积与旋转方向，其符号决定三点 (o,a,b) 的转向），多边形面积 S=1/2|Σ v_i×v_{i+1}|（有向面积），线段相交判定（快速排斥实验+跨立实验），两直线交点（叉积比例），以及点在多边形内的射线法/回转数判定。几乎一切计算几何（凸包、旋转卡壳、半平面交、最近点对等）都构建在这一层原语之上。

## Why · 为什么

### 直觉 · Intuition

叉积的符号就是'手表'：cross(o,a,b)>0 表示从 o→a 看向 o→b 是逆时针（左转），<0 是顺时针（右转），=0 三点共线。点积则回答'它们垂直吗/投影有多长'。面积公式把多边形切成很多小三角形求和，正是'有向面积'的由来——凹多边形也不会算错，因为符号会自动抵消。

### 原理 · Principle

所有方向判定统一走叉积：线段相交的跨立实验要求两条线段互相'跨立'（各自端点位于对方直线两侧），再加上快速排斥实验（包围盒不交则必不相交）处理共线/退化情况；直线交点用叉积比例：t=(P2-P1)×d2 / (d1×d2)，即在方向 d1 上按平行四边形面积比例取平移量。面积公式来自 Stokes 意义上的格林公式离散化：有向面积 ∮(x dy - y dx)/2 在折线上逐段求和，相邻顶点与原点构成的三角形自动带符号。

### 历史 · History

计算几何作为独立学科兴起于 1970 年代（Shamos、Preparata 等），二维基础原语源自解析几何与向量代数，Shamos 1978 的博士论文《Computational Geometry》系统化了点线面的算法表述。OI/CP 圈内经 OI-wiki、e-maxx 等整理为标准模板，是竞赛几何的公共基础设施。

## How · 实现

### 伪代码

```python
# 基础原语（假设点 = (x,y) 元组）
dot(u,v)  = u.x*v.x + u.y*v.y
cross(u,v)= u.x*v.y - u.y*v.x

# 三点方向判定 (o -> a -> b)
turn(o,a,b) = cross(a-o, b-o)
# >0 左转 / <0 右转 / =0 共线

# 多边形有向面积 (p0..pn-1 按序)
area2 = Σ_i cross(p_i, p_{i+1})   # 结果 = 2*有向面积
area  = |area2| / 2

# 线段相交判定：快速排斥 + 跨立
if 快速排斥失败(包围盒不相交): return False
if cross(a,b,c)*cross(a,b,d) <= 0 and cross(c,d,a)*cross(c,d,b) <= 0:
    return True   # 注意共线退化要用 on_segment 特判

# 两直线交点: 直线 l1 = p1 + t*d1, l2 = p2 + s*d2
den = cross(d1, d2); 若 |den|≈0 → 平行
 t  = cross(p2-p1, d2) / den
return p1 + t*d1
```

### Python 实现

```python
# -*- coding: utf-8 -*-
import math


def dot(u, v):
    return u[0]*v[0] + u[1]*v[1]


def cross_vec(u, v):
    return u[0]*v[1] - u[1]*v[0]


def turn(o, a, b):
    return cross_vec((a[0]-o[0], a[1]-o[1]), (b[0]-o[0], b[1]-o[1]))


def polygon_area(poly):
    s = 0.0
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i+1) % n]
        s += x1*y2 - x2*y1
    return abs(s) / 2.0


def on_segment(p, a, b):
    return (min(a[0], b[0])-1e-12 <= p[0] <= max(a[0], b[0])+1e-12 and
            min(a[1], b[1])-1e-12 <= p[1] <= max(a[1], b[1])+1e-12)


def seg_intersect(a, b, c, d):
    o1 = turn(a, b, c)
    o2 = turn(a, b, d)
    o3 = turn(c, d, a)
    o4 = turn(c, d, b)
    if o1*o2 < 0 and o3*o4 < 0:
        return True
    if abs(o1) < 1e-12 and on_segment(c, a, b):
        return True
    if abs(o2) < 1e-12 and on_segment(d, a, b):
        return True
    if abs(o3) < 1e-12 and on_segment(a, c, d):
        return True
    if abs(o4) < 1e-12 and on_segment(b, c, d):
        return True
    return False


def line_intersect(p1, d1, p2, d2):
    den = cross_vec(d1, d2)
    if abs(den) < 1e-15:
        return None
    t = cross_vec((p2[0]-p1[0], p2[1]-p1[1]), d2) / den
    return (p1[0]+t*d1[0], p1[1]+t*d1[1])


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
    sq = [(0, 0), (4, 0), (4, 4), (0, 4)]
    assert abs(polygon_area(sq) - 16.0) < 1e-9
    assert abs(polygon_area(sq[::-1]) - 16.0) < 1e-9
    assert seg_intersect((0, 0), (4, 4), (0, 4), (4, 0))
    assert not seg_intersect((0, 0), (1, 0), (2, 0), (3, 0))
    p = line_intersect((0, 0), (1, 1), (0, 1), (1, 0))
    assert p and abs(p[0]-1.0) < 1e-9 and abs(p[1]-1.0) < 1e-9
    p = line_intersect((0, 0), (1, 1), (0, 1), (1, -1))
    assert p and abs(p[0]-0.5) < 1e-9 and abs(p[1]-0.5) < 1e-9
    assert pip_ray((2, 2), sq) is True
    assert pip_ray((5, 2), sq) is False
    assert turn((0, 0), (1, 0), (1, 1)) > 0
    assert turn((0, 0), (1, 0), (1, -1)) < 0
    print('2d-geometry all tests passed')

```

**PyPy 提示**: 纯 Python 处理 1e5 以上规模时建议：(1) 用元组/列表存点，避免类封装开销；(2) 预先展开叉积计算减少函数调用；(3) 整点问题尽量用整数运算避免浮点误差与慢速 sqrt；(4) 线段相交高频场景可把 turn 写成内联表达式。CPython 3.11+ 的浮点已很快，瓶颈通常是排序与常数项。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 基础原语 O(1)；线段相交判定 O(1)；多边形面积 O(n)；射线法点在多边形内 O(n)；排序/整体结构类问题由上层算法决定 |
| 空间 | O(n) 存储点集/多边形，原语操作 O(1) |

### 局限

浮点运算引入精度误差：判共线/相等需用 eps（如 1e-9）与 sgn 函数，避免直接比较 ==；退化输入（重复点、三点共线、零面积）需特判；射线法不适用自交多边形（应用回转数/winding number）；坐标范围极大（1e18）时浮点可能溢出，尽量用整数有理数。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| CSES | 2189 | 1 | Point Location Test：三点叉积判断点在直线左/右/上 | [https://cses.fi/problemset/task/2189/](https://cses.fi/problemset/task/2189/) |
| CSES | 2190 | 2 | Line Segment Intersection：线段相交判定模板 | [https://cses.fi/problemset/task/2190/](https://cses.fi/problemset/task/2190/) |
| CSES | 2191 | 2 | Polygon Area：有向面积（可为负，需取绝对值） | [https://cses.fi/problemset/task/2191/](https://cses.fi/problemset/task/2191/) |

## Pitfalls · 易错点

- 叉积为 0 是共线而非'不相交'，线段相交必须额外处理三点共线+on_segment
- 面积公式结果是有向面积，凹多边形也需取绝对值
- 浮点比较不要用 ==，统一 sgn(x)=(-1/0/1) 配合 eps
- 射线法遇射线穿过顶点/平行边会出错，用无理数斜率或特殊处理规避
- cross(a,b) 与 cross(o,a,b) 参数形式混用导致方向颠倒
- 点坐标大时叉积可能溢出 int，用 long long/Python 大整数

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/geometry/2d.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/geometry/2d.md)
- CP-Algorithms ✓ [https://cp-algorithms.com/geometry/basic-geometry.html](https://cp-algorithms.com/geometry/basic-geometry.html)
- CP-Algorithms ✓ [https://cp-algorithms.com/geometry/area-of-simple-polygon.html](https://cp-algorithms.com/geometry/area-of-simple-polygon.html)
- CP-Algorithms ✓ [https://cp-algorithms.com/geometry/oriented-triangle-area.html](https://cp-algorithms.com/geometry/oriented-triangle-area.html)
- CP-Algorithms ✓ [https://cp-algorithms.com/geometry/segment-to-line.html](https://cp-algorithms.com/geometry/segment-to-line.html)
- 书籍 ✓ `CPH ch29`
