---
id: 3d-geometry
name: 三维几何
group: G-D-3
stage: advanced
priority: P2
depth_tier: standard
---

# 三维几何

> 三维向量/平面/法向量/多面体体积与表面积，由二维推广

<!-- 元信息: id=3d-geometry · group=G-D-3 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

三维计算几何把二维原语推广到空间：点与向量变成三元组，点积仍是投影，叉积变成向量叉积（结果是与两向量都垂直的法向量），通过三点/一点+法向量表示平面 Ax+By+Cz+D=0。基本运算：空间两点距离、直线与平面交点、点到平面距离、直线与平面的夹角（方向向量与法向量）、两平面夹角（法向量夹角）、四面体体积（混合积/6）、多面体体积（对每个三角面做带符号混合积求和/6）。高维三维凸包（增量法）与三维最近点对也属此家族。

## Why · 为什么

### 直觉 · Intuition

三维不过是在二维基础上加一个 z 坐标：'点积判垂直'变成'向量判平行'，'二维叉积（标量）'升级成'三维叉积（向量）'。法向量是平面的'表盘指针'：平面方程 Ax+By+Cz+D=0 的 (A,B,C) 就是法向量，点到平面的距离等于沿法方向投影的长度——这正是点积的意义。多面体体积由'底面积×高/3'推广：把每个面与原点连成四面体，带符号求和，凹面自动抵消。

### 原理 · Principle

平面表示：点 P0 与法向量 n=(A,B,C)，平面内任意点 P 满足 n·(P-P0)=0，展开得 Ax+By+Cz+D=0，D=-(n·P0)。点到平面距离 d=|Ax+By+Cz+D|/|n|。直线与平面交点：直线 P=P1+t·d，代入平面方程解 t=-(A·x1+B·y1+C·z1+D)/(A·dx+B·dy+C·dz)。两直线夹角用方向向量点积；直线与平面夹角 sinφ=|n·d|/(|n||d|)。四面体体积 = |(b-a)·((c-a)×(d-a))|/6（混合积）。多面体体积：对每个三角形面 (a,b,c) 累加 (a·(b×c))/6 取绝对值。三维凸包用增量法：维护三角面，新点可见的面删掉，用新点补面，O(n^2)。

### 历史 · History

三维计算几何与线性代数相伴发展，欧拉公式 V-E+F=2 与混合积为立体几何提供了组合/代数工具；增量法三维凸包在 Preparata-Shamos、de Berg 等教材中系统化。OI 中三维几何多出现在模板题（如 Luogu P4724 三维凸包）与少量综合题，实用频率低于二维但概念相通。

## How · 实现

### 伪代码

```python
# 三维原语（点/向量 = (x,y,z) 三元组）
dot3(a,b) = a.x*b.x + a.y*b.y + a.z*b.z
cross3(a,b) = (a.y*b.z - a.z*b.y, a.z*b.x - a.x*b.z, a.x*b.y - a.y*b.x)

# 平面: 过 p,q,r 三点
n = cross3(q-p, r-p); D = -dot3(n, p)   # 平面方程 n·X + D = 0

# 点到平面距离
return |dot3(n, X) + D| / |n|

# 直线与平面交点 (直线 X = p + t*d)
t = -(dot3(n, p) + D) / dot3(n, d)
return p + t*d

# 四面体体积
V = |dot3(b-a, cross3(c-a, d-a))| / 6
```

### Python 实现

```python
# -*- coding: utf-8 -*-
import math


def dot3(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]


def cross3(a, b):
    return (a[1]*b[2] - a[2]*b[1],
            a[2]*b[0] - a[0]*b[2],
            a[0]*b[1] - a[1]*b[0])


def sub3(a, b):
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])


def norm3(v):
    return math.sqrt(dot3(v, v))


def plane_from_3(p, q, r):
    """过三点平面，返回 (法向量 n, D)，平面方程 n·X + D = 0。"""
    n = cross3(sub3(q, p), sub3(r, p))
    D = -dot3(n, p)
    return (n, D)


def point_plane_dist(x, plane):
    n, D = plane
    return abs(dot3(n, x) + D) / norm3(n)


def line_plane_intersect(p, d, plane):
    """直线 p + t*d 与平面交点；平行返回 None。"""
    n, D = plane
    den = dot3(n, d)
    if abs(den) < 1e-15:
        return None
    t = -(dot3(n, p) + D) / den
    return (p[0]+t*d[0], p[1]+t*d[1], p[2]+t*d[2])


def tetra_volume(a, b, c, d):
    return abs(dot3(sub3(b, a), cross3(sub3(c, a), sub3(d, a)))) / 6.0


def polyhedron_volume(faces):
    """faces: 三角形顶点三元组列表，各面顶点顺序一致（均指向外侧）。"""
    vol = 0.0
    for a, b, c in faces:
        vol += dot3(a, cross3(b, c))
    return abs(vol) / 6.0


def line_angle(s1, s2):
    """两方向向量夹角（0~π），余弦公式。"""
    return math.acos(max(-1.0, min(1.0, dot3(s1, s2) / (norm3(s1)*norm3(s2)))))


if __name__ == '__main__':
    # z=0 平面
    plane = plane_from_3((0, 0, 0), (1, 0, 0), (0, 1, 0))
    assert abs(point_plane_dist((0, 0, 5), plane) - 5.0) < 1e-9
    ip = line_plane_intersect((0, 0, 10), (0, 0, -1), plane)
    assert ip and abs(ip[2] - 0.0) < 1e-9, ip
    # 四面体体积: 单位立方体的一个切角 = 1/6
    assert abs(tetra_volume((0,0,0), (1,0,0), (0,1,0), (0,0,1)) - 1/6) < 1e-9
    # 正四面体面集合体积（选原点一角的三角面组合）
    faces = [((0,0,0),(1,0,0),(0,1,0)),
             ((0,0,0),(1,0,0),(0,0,1)),
             ((0,0,0),(0,1,0),(0,0,1)),
             ((1,0,0),(0,1,0),(0,0,1))]
    assert abs(polyhedron_volume(faces) - 1/6) < 1e-9
    # 两向量夹角
    assert abs(line_angle((1,0,0),(0,1,0)) - math.pi/2) < 1e-9
    assert abs(line_angle((1,0,0),(1,1,0)) - math.pi/4) < 1e-9
    print('3d-geometry all tests passed')

```

**PyPy 提示**: 三维运算点数较少，纯 Python 足够；若涉及 O(n^2) 三维凸包增量，注意面集合的删除/更新用 dict 或并查集优化。浮点向量叉积/混合积直接算即可，注意归一化避免数值抖动。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 基础原语 O(1)；三维凸包增量 O(n^2)；最近点对等由具体算法决定 |
| 空间 | O(n) 基础结构；三维凸包 O(n) |

### 局限

平面表示需避免三点共线（叉积为零）；浮点误差在体积/距离计算中累积，凹多面体顶点顺序需一致；三维凸包对四点共面敏感，需微小扰动或容差；空间坐标大时混合积可能溢出（Python 整数可避免，浮点需注意）。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P4724 | 5 | 【模板】三维凸包：增量法求三维凸包表面积 | [https://www.luogu.com.cn/problem/P4724](https://www.luogu.com.cn/problem/P4724) |
| CSES | CSES 2191 | 2 | Polygon Area：二维面积是三维混合积的基础（先掌握二维） | [https://cses.fi/problemset/task/2191/](https://cses.fi/problemset/task/2191/) |
| Luogu | P3958 | 4 | [NOIP2017 提高组] 奶酪：三维空间距离/连通性判定（欧氏距离原语） | [https://www.luogu.com.cn/problem/P3958](https://www.luogu.com.cn/problem/P3958) |

## Pitfalls · 易错点

- 三点共线时平面法向量为零向量，需特判
- 直线与平面平行（法向量与方向点积≈0）时无交点
- 四面体/多面体体积的顶点顺序必须一致，否则带符号求和会抵消
- 混合积可能溢出/精度损失，坐标大时用 Python 整数先乘除
- 三维凸包对共面点敏感，先扰动

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/geometry/3d.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/geometry/3d.md)
- 书籍 ✓ `CPH ch29`
