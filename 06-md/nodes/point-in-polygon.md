---
id: point-in-polygon
name: 点在多边形内判定
group: G-D-1
stage: advanced
priority: P2
depth_tier: standard
---

# 点在多边形内判定

> 射线法判一般多边形，凸多边形用有序二分 O(logn)

<!-- 元信息: id=point-in-polygon · group=G-D-1 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

点在多边形内判定（Point-in-Polygon, PIP）有两类主流方法：① 射线法（ray casting / even-odd rule）：从点向右作水平射线，统计与多边形边的交点数，奇数在内部，偶数在外部，适用于任意简单多边形（含凹），O(n)/次；② 凸多边形二分法：凸多边形按逆时针存储时，以最左点 p0 为极把所有点按极角排序，先判 p 是否在 p0p1 与 p0p_{n-1} 两侧夹角的扇形内，再二分定位 p 落在三角形 p0,p_i,p_{i+1} 中，O(log n)/次，适合大规模查询。回转数（winding number）算法可处理自交多边形但竞赛中少用。

## Why · 为什么

### 直觉 · Intuition

射线法：从点发射一条射线，每穿过一次边界就内外切换一次（Jordan 曲线定理），穿奇数次就是起点在内部。凸二分：凸多边形以 p0 为中心呈'扇形'排列，先用叉积夹出 p 所在的两条辐射边 p0p_i、p0p_{i+1}，再判 p 是否在扇形底边 p_i p_{i+1} 内侧——整个扇形区域被 p0 与凸包的'锥角'覆盖。

### 原理 · Principle

射线法实现要点：只统计与水平射线严格相交（端点跨立）的边，y 用 > 严格比较避免顶点被算两次；交点 x 在点右侧才计数。凸二分：选最小 x 的点 p0（并列取最小 y），其余点按逆时针排好后极角严格递增。先特判 p 在 p0p1 或 p0p_{n-1} 直线上；然后二分找到最后一个使叉积 (p_i-p0)×(p-p0) ≥ 0 的 i（即 p 在 p0p_i 左侧的最后一个），最后检查 p 是否在三角形 p0,p_i,p_{i+1} 内（叉积 (p_i-p)×(p_{i+1}-p) ≥ 0）。

### 历史 · History

射线法（pnpoly）源自经典的奇偶规则，W. R. Franklin 的 pnpoly 算法（1980s）是流传最广的单行实现；回转数概念来自拓扑学（winding number）。凸多边形对数查询由 Preparata & Shamos 在计算几何早期工作（1978 博士论文）中给出，e-maxx 与 cp-algorithms 收录了标准实现，OI-wiki 的 misc 页也整理过射线法。

## How · 实现

### 伪代码

```python
# 射线法（任意简单多边形，O(n)）
def pip_ray(p, poly):
    inside = False
    for each edge (p_i, p_{i+1}):
        if (p_i.y > p.y) != (p_{i+1}.y > p.y):   # 严格跨立
            x_cross = p_i.x + (p_{i+1}.x - p_i.x) * (p.y - p_i.y) / (p_{i+1}.y - p_i.y)
            if p.x < x_cross: inside = not inside
    return inside

# 凸多边形二分（逆时针、首尾不重复，O(log n)）
p0 = 多边形中 x 最小（次小 y）的点，其余点极角有序
if 叉积(p0,p1,p) < 0 or 叉积(p0,p_{n-1},p) > 0: return False   # 扇形外
if 叉积(p0,p1,p) == 0: return p 在 p0p1 上（含端点）
lo, hi = 1, n-1
while hi - lo > 1:
    mid = (lo+hi)//2
    if 叉积(p0, poly[mid], p) >= 0: lo = mid
    else: hi = mid
return 叉积(poly[lo], poly[hi], p) >= 0
```

### Python 实现

```python
# -*- coding: utf-8 -*-


def cross(o, a, b):
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])


def pip_ray(p, poly):
    """射线法：任意简单多边形，O(n)。含边界时边界点可能判为内部/外部，需另行特判。"""
    x, y = p
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i+1) % n]
        if (y1 > y) != (y2 > y):
            xi = x1 + (x2 - x1) * (y - y1) / (y2 - y1)
            if x < xi:
                inside = not inside
    return inside


def in_convex(p, poly):
    """凸多边形（逆时针、首尾不重复）O(log n) 判定，含边界。"""
    n = len(poly)
    p0 = poly[0]
    c1 = cross(p0, poly[1], p)
    if c1 < 0:
        return False
    if cross(p0, poly[-1], p) > 0:
        return False
    if c1 == 0:
        return (p[0]-p0[0])*(p[0]-poly[1][0]) + (p[1]-p0[1])*(p[1]-poly[1][1]) <= 0
    lo, hi = 1, n - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if cross(p0, poly[mid], p) >= 0:
            lo = mid
        else:
            hi = mid
    return cross(poly[lo], poly[hi], p) >= 0


if __name__ == '__main__':
    sq = [(0, 0), (4, 0), (4, 4), (0, 4)]
    assert pip_ray((2, 2), sq) is True
    assert pip_ray((5, 2), sq) is False
    assert in_convex((2, 2), sq) is True
    assert in_convex((5, 5), sq) is False
    assert in_convex((0, 2), sq) is True    # 边界
    assert in_convex((4, 4), sq) is True    # 顶点
    # 凸多边形随机对拍：in_convex == pip_ray（严格内外一致，边界统一按 pip 计）
    import random, math
    def rnd_convex():
        angs = sorted(random.random()*2*math.pi for _ in range(6))
        return [(math.cos(a)*5, math.sin(a)*5) for a in angs]
    for _ in range(100):
        cp = rnd_convex()
        # 保证 p0 是最左点（凸多边形旋转即可，构造时让 p0 为最左下）
        k = min(range(len(cp)), key=lambda i: (cp[i][0], cp[i][1]))
        cp = cp[k:] + cp[:k]
        for _2 in range(40):
            q = (random.uniform(-8, 8), random.uniform(-8, 8))
            a = in_convex(q, cp)
            b = pip_ray(q, cp)
            # 边界点在射线法下可能偏差，仅当 q 明显不在边界时要求一致
            onb = False
            for i in range(len(cp)):
                x1, y1 = cp[i]
                x2, y2 = cp[(i+1) % len(cp)]
                if cross(cp[i], cp[(i+1) % len(cp)], q) == 0 and min(x1,x2)-1e-9 <= q[0] <= max(x1,x2)+1e-9 and min(y1,y2)-1e-9 <= q[1] <= max(y1,y2)+1e-9:
                    onb = True
            if not onb:
                assert a == b, (q, a, b)
    print('point-in-polygon all tests passed')

```

**PyPy 提示**: 射线法每次 O(n)，n 大且查询多时先凸包再二分；in_convex 用二分 O(log n)，Python 处理 1e5 查询轻松。射线法内部循环是纯算术，可把叉积/交点内联。整数坐标射线法可用整数交点比较避免浮点。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 射线法 O(n)/次；凸二分 O(log n)/次（凸包/预处理需 O(n) 或 O(n log n)） |
| 空间 | O(n) |

### 局限

射线法只适用简单多边形，自交多边形需回转数；射线穿过顶点/与边重合要用严格跨立处理；凸二分要求 p0 为最左点且其余点严格极角有序（凸多边形天然满足），输入若含重复点或退化需预处理；边界归属（在边上算内还是外）要按题目约定。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| CSES | 2192 | 3 | Point in Polygon：射线法判点在任意多边形内（含边界） | [https://cses.fi/problemset/task/2192/](https://cses.fi/problemset/task/2192/) |
| Luogu | P1452 | 3 | 凸包题目中常与凸多边形二分 PIP 配合（直径/包含判定） | [https://www.luogu.com.cn/problem/P1452](https://www.luogu.com.cn/problem/P1452) |
| CP-Algorithms | point-in-convex-polygon | 3 | 凸多边形 O(log n) 二分判定的标准实现 | [https://cp-algorithms.com/geometry/point-in-convex-polygon.html](https://cp-algorithms.com/geometry/point-in-convex-polygon.html) |

## Pitfalls · 易错点

- 射线法 y 比较必须用严格 > 避免顶点被计两次
- 射线水平穿过边时该边不计数（用跨立条件排除）
- 凸二分时 p0 必须取最左下点，且多边形逆时针
- 边界归属：在边上时两个算法可能给出不同答案，需统一约定
- 射线法对自交多边形失效
- 浮点：叉积判 0 用 eps，否则边界点误判

## Sources · 信源

- CP-Algorithms ✓ [https://cp-algorithms.com/geometry/point-in-convex-polygon.html](https://cp-algorithms.com/geometry/point-in-convex-polygon.html)
- CP-Algorithms ✓ [https://cp-algorithms.com/geometry/point-location.html](https://cp-algorithms.com/geometry/point-location.html)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/geometry/2d.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/geometry/2d.md)
