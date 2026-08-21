---
id: minkowski-sum
name: 闵可夫斯基和
group: G-D-1
stage: advanced
priority: P2
depth_tier: standard
---

# 闵可夫斯基和

> 两凸多边形 Minkowski 和仍为凸多边形，用于碰撞检测/半平面并

<!-- 元信息: id=minkowski-sum · group=G-D-1 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

点集 P 与 Q 的闵可夫斯基和定义为 P+Q = {a+b | a∈P, b∈Q}。若 P、Q 都是凸多边形，则 P+Q 也是凸多边形，且顶点数 ≤ |P|+|Q|。算法：将两凸多边形按'最低点（y 最小、x 次小）'重排使得边按极角有序，然后用双指针按极角归并两族的边向量，每次取极角较小的边拼接到当前顶点，得到 P+Q 的顶点序列。复杂度 O(|P|+|Q|)。主要应用：凸多边形碰撞检测（两凸多边形的距离/相交判定——P 与 Q 相交当且仅当原点在 P+(-Q) 内）、滑动/运动规划、半平面并等。

## Why · 为什么

### 直觉 · Intuition

把 P 沿着 Q 的每个点平移得到的叠加区域，边界就是 P 的边与 Q 的边'接龙'的结果。凸多边形的边按极角天然有序，两族的边按极角归并拼接，正好一圈走完边界——像把两串珠子（边向量）按角度合并成一条项链。

### 原理 · Principle

凸性保真：P、Q 凸 → P+Q 凸（对任意 a,c∈P、b,d∈Q 及 t∈[0,1]，t(a+b)+(1-t)(c+d) = [ta+(1-t)c]+[tb+(1-t)d] ∈ P+Q）。边集性质：P+Q 的边序列是 P 的边与 Q 的边按极角排序后的归并，共线同向的边向量可合并。实现：先找到两多边形最低点重排（之后各边按极角从 0 递增到 2π），双指针 i,j 比较当前边 dP = P[i+1]-P[i] 与 dQ = Q[j+1]-Q[j] 的极角（用叉积符号判定），极角小的先接上；把各边向量依次加到累加点上即得顶点。碰撞检测：构造 P+(-Q)（-Q 是 Q 关于原点对称），原点在 P+(-Q) 内 ⇔ P 与 Q 相交。

### 历史 · History

闵可夫斯基和以德国数学家 Hermann Minkowski（1864-1909）命名，源于凸几何（Minkowski 加法的概念）。在计算几何中用于凸体 Minkowski 和、机器人运动规划（configuration space obstacle）与碰撞检测；CP 圈内经 e-maxx / cp-algorithms 整理为标准模板，OI-wiki 的凸包章节也收录了凸包 Minkowski 和，典型例题为 JSOI2018 战争。

## How · 实现

### 伪代码

```python
# P, Q 为逆时针凸多边形（不重复首尾）
# 1) 重排到最低点开头（y 最小、x 次小）
k = argmin (poly[i].y, poly[i].x); poly = poly[k:] + poly[:k]
# 2) 双指针归并边向量
i = j = 0; R = [P[0] + Q[0]]
while i < |P| or j < |Q|:
    dP = P[i+1] - P[i]; dQ = Q[j+1] - Q[j]
    cp = cross(dP, dQ)
    if j == |Q| or (i < |P| and cp > 0): i += 1
    elif i == |P| or cp < 0: j += 1
    else: i += 1; j += 1
    R.append(P[i % |P|] + Q[j % |Q|])
R 去掉相邻重复点，末尾去重 → P+Q
```

### Python 实现

```python
# -*- coding: utf-8 -*-


def bottom_left(poly):
    return min(range(len(poly)), key=lambda i: (poly[i][1], poly[i][0]))


def reorder(poly):
    k = bottom_left(poly)
    return poly[k:] + poly[:k]


def minkowski_sum(P, Q):
    """两凸多边形（逆时针、首尾不重复）的闵可夫斯基和。整数坐标。"""
    P = reorder(P)
    Q = reorder(Q)
    n, m = len(P), len(Q)
    i = j = 0
    R = [(P[0][0] + Q[0][0], P[0][1] + Q[0][1])]
    while i < n or j < m:
        dP = (P[(i+1) % n][0] - P[i][0], P[(i+1) % n][1] - P[i][1])
        dQ = (Q[(j+1) % m][0] - Q[j][0], Q[(j+1) % m][1] - Q[j][1])
        cp = dP[0]*dQ[1] - dP[1]*dQ[0]
        if j == m or (i < n and cp > 0):
            i += 1
        elif i == n or cp < 0:
            j += 1
        else:
            i += 1
            j += 1
        R.append((P[i % n][0] + Q[j % m][0], P[i % n][1] + Q[j % m][1]))
    final = []
    for p in R:
        if not final or p != final[-1]:
            final.append(p)
    return final[:-1] if len(final) > 1 else final


def cross(o, a, b):
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])


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


def polygon_area(poly):
    s = 0.0
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i+1) % n]
        s += x1*y2 - x2*y1
    return abs(s) / 2.0


if __name__ == '__main__':
    # 两个矩形
    P = [(0, 0), (4, 0), (4, 2), (0, 2)]
    Q = [(1, 1), (3, 1), (3, 3), (1, 3)]
    R = minkowski_sum(P, Q)
    # 暴力点集凸包对照
    brute = [(a[0]+b[0], a[1]+b[1]) for a in P for b in Q]
    H = convex_hull(brute)
    assert abs(polygon_area(R) - polygon_area(H)) < 1e-9, (polygon_area(R), polygon_area(H))
    # 凸性：所有点都在 R 内或边界
    for p in brute:
        ok = False
        for i in range(len(R)):
            a, b = R[i], R[(i+1) % len(R)]
            if cross(a, b, p) == 0 and min(a[0],b[0])-1e-9 <= p[0] <= max(a[0],b[0])+1e-9 and min(a[1],b[1])-1e-9 <= p[1] <= max(a[1],b[1])+1e-9:
                ok = True
        # 非边界点应严格在每条边左侧
        if not ok:
            assert all(cross(R[i], R[(i+1) % len(R)], p) >= -1e-9 for i in range(len(R)))
    # 平移后相交检测思路自检：P + (-Q) 含原点 ⇔ P、Q 相交
    negQ = [(-x, -y) for x, y in Q]
    S = minkowski_sum(P, negQ)
    def pip_origin(poly):
        # 射线法判原点
        inside = False
        n = len(poly)
        for i in range(n):
            x1, y1 = poly[i]
            x2, y2 = poly[(i+1) % n]
            if (y1 > 0) != (y2 > 0):
                xi = x1 + (x2-x1)*(0-y1)/(y2-y1)
                if 0 < xi:
                    inside = not inside
        return inside
    assert pip_origin(S) is True   # P 与 Q 确实相交
    print('minkowski-sum all tests passed')

```

**PyPy 提示**: 整数坐标全程整数运算（叉积判极角大小），无浮点误差。双指针合并 O(\|P\|+\|Q\|)，Python 完全胜任 1e5 级。若坐标是浮点，极角比较仍可用叉积符号避免 atan2 的误差与开销。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(\|P\|+\|Q\|)，重排找最低点为线性 |
| 空间 | O(\|P\|+\|Q\|) |

### 局限

要求输入是凸多边形（逆时针、首尾不重复）；共线相邻边会在归并时产生重复点需清理；浮点坐标下边向量叉积判极角受精度影响，建议整数坐标使用；仅讨论凸包的 Minkowski 和，一般点集的 Minkowski 和需先凸包化。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P4557 | 5 | [JSOI2018] 战争：两凸包平移相交判定 → 平移向量 ∈ P+(-Q)，Minkowski 和模板题 | [https://www.luogu.com.cn/problem/P4557](https://www.luogu.com.cn/problem/P4557) |
| CP-Algorithms | minkowski | 4 | Minkowski 和原理 + 两凸多边形距离/相交判定 O(n+m) | [https://cp-algorithms.com/geometry/minkowski.html](https://cp-algorithms.com/geometry/minkowski.html) |
| Luogu | P5459 | 5 | 凸包 Minkowski 和相关综合（双凸包相撞判定类题） | [https://www.luogu.com.cn/problem/P5459](https://www.luogu.com.cn/problem/P5459) |

## Pitfalls · 易错点

- 输入多边形必须逆时针且首尾不重复，否则边极角序错误
- 最低点重排的键要 (y, x) 而非 (x, y)
- 边向量归并时共线同向要同时推进双指针并合并
- 最后顶点列表可能有相邻重复点（共线合并），需要去重
- 碰撞检测记得取 -Q（关于原点对称）而非直接 P+Q
- 浮点坐标的极角比较不要用 atan2 直接比，用叉积符号

## Sources · 信源

- CP-Algorithms ✓ [https://cp-algorithms.com/geometry/minkowski.html](https://cp-algorithms.com/geometry/minkowski.html)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/geometry/convex-hull.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/geometry/convex-hull.md)
- 书籍 ✓ `CPH ch29`
