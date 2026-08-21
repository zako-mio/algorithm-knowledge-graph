---
id: geometric-inverse
name: 反演变换
group: G-D-3
stage: advanced
priority: P2
depth_tier: standard
---

# 反演变换

> 圆/直线相切问题经反演简化，保角变换

<!-- 元信息: id=geometric-inverse · group=G-D-3 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

反演变换（Inversion）：给定反演中心 O 与反演半径 R，点 P 的反演点 P' 满足 P' 在射线 OP 上且 |OP|·|OP'| = R²。关键性质：① 过 O 的直线仍为过 O 的直线，不过 O 的直线变为过 O 的圆，过 O 的圆变为不过 O 的直线，不过 O 的圆仍为不过 O 的圆（圆心与半径有公式）；② 反演是保角变换（交角不变），相切关系保持；③ O 上的点不变。因此，圆/直线相切类问题（如'过一点与两圆相切的圆'）可在反演后变成'求两圆公切线'等简单问题。典型应用：Apollonius 圆问题、Soddy 圆、插入圆半径。

## Why · 为什么

### 直觉 · Intuition

反演像一面'凸面镜'：以 O 为圆心把平面翻进去，离 O 近的点被弹远，离 O 远的点被拉近，圆周上的点不动。圆与直线的界限被打破——不过圆心的圆会'拉直'成直线，这正是魔法所在：原本难解的圆-圆相切，反演后变成直线-直线/直线-圆相切，而相切关系又被保角性原封不动地保留，于是难题被'透视'成了简单题。

### 原理 · Principle

定义 |OP|·|OP'|=R²。核心几何事实（坐标计算可得）：不过 O 的圆 C(圆心 A 半径 r) 反演成不过 O 的圆 C'，半径 r' = (1/(|OA|-r) - 1/(|OA|+r))·R²/2，圆心 A' 在射线 OA 上满足 |OA'| = |OA|·r'/r 等；过 O 的圆反演成直线（直线过两交点方向的延伸），过 O 的直线反演为自身，不过 O 的直线反演为过 O 的圆。由于反演是保角的（两曲线交角反演后不变），相切/相离/相交关系全部保持，从而可以把'找过点 P 且与两圆相切的圆'转化为'找两圆反演像的公切线'，再反演回去。

### 历史 · History

反演几何（Inversive geometry）由 Steiner、Laguerre 等在 19 世纪系统发展，与射影几何、圆几何（Möbius 变换）同源；Apollonius 圆问题（求与三已知圆相切的圆）是古典几何著名难题，反演是标准解法之一。CP/OI 圈经 OI-wiki 的 inverse 页整理，出现于 HDU 4773（ICPC 2013 杭州）等题。

## How · 实现

### 伪代码

```python
# 点反演: inv(P) = O + R² * (P-O) / |P-O|²
# 圆反演（不过 O）: 记 OA=|A-O|, r 为半径
d   = OA
r2  = 0.5 * (1/(d-r) - 1/(d+r)) * R²
d2  = d * r2 / r
A'  = O + (A-O) * (d2 / d)
返回 (A', r2)

# 直线反演为过 O 的圆: 取 O 到直线垂足 P, 距离 h
r' = R² / (2h); 圆心在 OP 方向, 距 O 为 r'

# 使用流程
1) 选反演中心 O（常为'过某点'的切圆问题取该点）
2) 对已知圆做反演
3) 求反演后图形的公切线/交点
4) 把结果反演回原平面
```

### Python 实现

```python
# -*- coding: utf-8 -*-
import math


def invert_point(P, O, R):
    """点 P 关于圆心 O 半径 R 的反演点。"""
    dx = P[0] - O[0]
    dy = P[1] - O[1]
    d2 = dx*dx + dy*dy
    if d2 < 1e-30:
        return None
    k = R * R / d2
    return (O[0] + dx * k, O[1] + dy * k)


def invert_circle(circle, O, R):
    """不过 O 的圆 (圆心, 半径) 的反演圆。返回 (圆心, 半径)。"""
    cx, cy, r = circle
    d = math.hypot(cx - O[0], cy - O[1])
    if abs(d - r) < 1e-12:
        return None          # 过 O 的圆反演成直线
    r2 = 0.5 * (1/(d - r) - 1/(d + r)) * R * R
    d2 = d * r2 / r
    nx = O[0] + (cx - O[0]) * (d2 / d)
    ny = O[1] + (cy - O[1]) * (d2 / d)
    return (nx, ny, r2)


def line_from_circle_through_O(circle, O):
    """过 O 的圆反演为直线：返回 (线上一点, 方向向量)。
    利用圆与以 O 为圆心的任一圆交点的连线方向。
    """
    cx, cy, r = circle
    # 圆过 O, 取圆上与 O 相对的直径端点 T = 2*C - O
    tx = 2*cx - O[0]
    ty = 2*cy - O[1]
    dirv = (tx - O[0], ty - O[1])      # 方向 = 直径方向
    # 直线上另一点: 取圆上异于 O 的任意点
    d = math.hypot(tx - O[0], ty - O[1])
    perp = (-dirv[1]/d, dirv[0]/d)
    p = (cx + perp[0] * r, cy + perp[1] * r)
    return (p, dirv)


if __name__ == '__main__':
    # 反演两次回到自身
    P = (3.0, 4.0)
    O = (0.0, 0.0)
    R = 2.0
    P1 = invert_point(P, O, R)
    P2 = invert_point(P1, O, R)
    assert abs(P2[0]-P[0]) < 1e-9 and abs(P2[1]-P[1]) < 1e-9, (P2, P)
    # 单位圆反演半径为 1 的圆(圆心(2,0) r=1) -> 半径 = 1/(2-1) - ... 计算校验
    c = invert_circle((2.0, 0.0, 1.0), (0.0, 0.0), 1.0)
    assert c is not None
    # 反演保持相切：两圆在 (3,0) 相切（且 (3,0) 不是 O），反演后仍相切
    c1 = invert_circle((2.0, 0.0, 1.0), (0.0, 0.0), 2.0)
    c2 = invert_circle((4.0, 0.0, 1.0), (0.0, 0.0), 2.0)
    d = math.hypot(c1[0]-c2[0], c1[1]-c2[1])
    assert abs(d - (c1[2]+c2[2])) < 1e-9 or abs(d - abs(c1[2]-c2[2])) < 1e-9, (d, c1, c2)
    print('geometric-inverse all tests passed')

```

**PyPy 提示**: 反演全部是 O(1) 坐标运算，Python 处理成百上千个圆毫无压力。注意浮点：当圆很接近过 O（\|d-r\|≈0）时反演半径爆炸，需要 eps 或按题目保证输入规避。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 单次反演 O(1)；整套流程 O(待反演图形数) |
| 空间 | O(1) |

### 局限

反演中心不能落在待反演图形上（否则定义失效）；过反演中心的圆反演成直线，需单独分支处理；浮点误差在半径接近 0 或 d≈r 时放大；反演后求出的直线/圆要反演回原平面，注意原题目可能要求圆心与半径输出精度。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| HDU | 4773 | 5 | ICPC 2013 杭州 Apollonius 问题：过外点且与两圆相切的所有圆，反演后求公切线 | [https://acm.hdu.edu.cn/showproblem.php?pid=4773](https://acm.hdu.edu.cn/showproblem.php?pid=4773) |
| HDU | 6158 | 5 | CCPC 2017 网络赛 The Designer：插入圆半径序列（反演技巧） | [https://acm.hdu.edu.cn/showproblem.php?pid=6158](https://acm.hdu.edu.cn/showproblem.php?pid=6158) |
| OI Wiki | inverse | 5 | 反演变换性质与例题标准参考 | [https://oi-wiki.org/geometry/inverse/](https://oi-wiki.org/geometry/inverse/) |

## Pitfalls · 易错点

- 反演中心选在'过某点'问题的该点上，否则不构成直线化
- 过反演中心的圆 → 直线，别当成普通圆处理
- 相切关系在反演下保持，但切点在 O 上的相切是例外（需注意）
- 反演半径 R 可任取，通常取便于计算的值（如点到图形距离）
- 浮点误差：圆半径接近 0 或过 O 时放大，需 eps 保护
- 反演回去时要判断哪个解对应原问题的有效解（如圆心在合法侧）

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/geometry/inverse.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/geometry/inverse.md)
- Wikipedia ✓ [https://en.wikipedia.org/wiki/Inversive_geometry](https://en.wikipedia.org/wiki/Inversive_geometry)
