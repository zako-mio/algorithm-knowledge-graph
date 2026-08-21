---
id: half-plane-intersection
name: 半平面交
group: G-D-1
stage: advanced
priority: P1
depth_tier: standard
---

# 半平面交

> S&I 算法 O(nlogn) 求半平面交，结果为凸多边形

<!-- 元信息: id=half-plane-intersection · group=G-D-1 · stage=advanced · priority=P1 · depth_tier=standard -->

## What · 是什么

半平面是一条直线及其一侧构成的点集，半平面交是多个半平面交集。几何上，n 个半平面的交集要么为空，要么是凸多边形（可为无界，加边界框限定）。Sort-and-Incremental (S&I) 算法：按半平面方向向量的极角排序，用双端队列维护当前相交的凸多边形，依次加入每个半平面，若队尾/队首相邻半平面的交点不在当前半平面内侧则弹出对应半平面，最后用队首半平面清理队尾。复杂度 O(n log n)（排序瓶颈）。典型应用：多边形的核（内核）、线性规划可行域、瞭望塔最远点、最小面积包围等。

## Why · 为什么

### 直觉 · Intuition

想象从四面八方用'巨型刮刀'（每条半平面的边界直线）刮一块橡皮泥：每把刀切一刀，剩下的形状始终是凸多边形。把刀按方向（极角）绕一圈切，每次新刀只可能影响当前多边形'头'或'尾'的一部分，所以用双端队列维护当前凸多边形即可，被切掉的边直接弹出。

### 原理 · Principle

把半平面表示为 (p, d)：直线过 p，方向 d，取 d 的左侧。按 atan2(d.y, d.x) 排序，同向共线只保留最靠左（即最内）的一条。维护队列 q 与交点数组 t（t[i] 为 q[i-1] 与 q[i] 交点）。新半平面 line 加入时：先弹队尾（若 t[尾] 在 line 右侧，说明上一条边被新刀切掉），再弹队首（若 t[首+1] 在 line 右侧）；然后入队并计算新交点。结束后用队首半平面把队尾多余交点清掉（闭合）。判'在右侧'用叉积 on_left(p, line) = cross(d, p - a) >= -eps。结果若队列 < 3 个则交为空。注意循环中必须先处理队尾再处理队首，否则当一条新半平面能把队列全部弹空时，会误用已过期的交点。

### 历史 · History

半平面交的排序+增量法由 O'Rourke 等人在 1980 年代早期的工作中系统化，被广泛收录于计算几何教材（如 de Berg《Computational Geometry: Algorithms and Applications》第 4 章线性规划章节、Berg 的 half-plane intersection）。e-maxx / OI-wiki 将其整理为竞赛标准模板。多边形内核判定源于美术馆问题（Art Gallery Problem），其解恰为多边形各边内侧半平面之交。

## How · 实现

### 伪代码

```python
# 半平面: (p, d) 取 d 左侧; on_left(x, hp) = cross(d, x-p) >= -eps
lines.sort(by polar angle of d)   # atan2
去重: 同极角只留最靠左者
q = deque(); t = []
for line in lines:
    while len(q) >= 2 and not on_left(交点(q[-2], q[-1]), line): q.pop()
    while len(q) >= 2 and not on_left(交点(q[0], q[1]), line): q.popleft()
    q.append(line)
    if len(q) >= 2: t.append(交点(q[-1], q[-2]))
# 收尾: 用队首清理队尾
while len(q) >= 2 and not on_left(交点(q[-2], q[-1]), q[0]): q.pop()
if len(q) < 3: return 空
结果多边形 = [交点(q[i], q[i+1]) for i in range(len(q))]
```

### Python 实现

```python
# -*- coding: utf-8 -*-
import math


def vec_cross(u, v):
    return u[0]*v[1] - u[1]*v[0]


def on_left(p, line):
    # line = (起点, 方向), 取方向左侧
    return vec_cross(line[1], (p[0]-line[0][0], p[1]-line[0][1])) >= -1e-12


def line_inter(l1, l2):
    p1, d1 = l1
    p2, d2 = l2
    den = vec_cross(d1, d2)
    if abs(den) < 1e-15:
        return None
    t = vec_cross((p2[0]-p1[0], p2[1]-p1[1]), d2) / den
    return (p1[0] + t*d1[0], p1[1] + t*d1[1])


def polygon_area(poly):
    s = 0.0
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i+1) % n]
        s += x1*y2 - x2*y1
    return abs(s) / 2.0


def halfplane_intersection(lines):
    """S&I 算法。返回凸多边形顶点列表；交集为空返回 None。"""
    lines = sorted(lines, key=lambda l: math.atan2(l[1][1], l[1][0]))
    dedup = []
    for l in lines:
        if dedup:
            a1 = math.atan2(dedup[-1][1][1], dedup[-1][1][0])
            a2 = math.atan2(l[1][1], l[1][0])
            if abs(a1 - a2) < 1e-12:
                p = dedup[-1][0]
                if vec_cross(l[1], (p[0]-l[0][0], p[1]-l[0][1])) > 0:
                    dedup[-1] = l
                continue
        dedup.append(l)
    dq = []
    for i, line in enumerate(dedup):
        while len(dq) >= 2:
            ip = line_inter(dedup[dq[-2]], dedup[dq[-1]])
            if ip is None or not on_left(ip, line):
                dq.pop()
            else:
                break
        while len(dq) >= 2:
            ip = line_inter(dedup[dq[0]], dedup[dq[1]])
            if ip is None or not on_left(ip, line):
                dq.pop(0)
            else:
                break
        dq.append(i)
    while len(dq) >= 2:
        ip = line_inter(dedup[dq[-2]], dedup[dq[-1]])
        if ip is None or not on_left(ip, dedup[dq[0]]):
            dq.pop()
        else:
            break
    while len(dq) >= 2:
        ip = line_inter(dedup[dq[0]], dedup[dq[1]])
        if ip is None or not on_left(ip, dedup[dq[-1]]):
            dq.pop(0)
        else:
            break
    if len(dq) < 3:
        return None
    poly = []
    for i in range(len(dq)):
        ip = line_inter(dedup[dq[i]], dedup[dq[(i+1) % len(dq)]])
        if ip is None:
            return None
        poly.append(ip)
    return poly


if __name__ == '__main__':
    # 单位正方形区域
    hp = [
        ((0.0, 0.0), (0.0, -1.0)),   # x >= 0
        ((1.0, 1.0), (0.0, 1.0)),    # x <= 1
        ((0.0, 0.0), (1.0, 0.0)),    # y >= 0
        ((1.0, 1.0), (-1.0, 0.0)),   # y <= 1
    ]
    poly = halfplane_intersection(hp)
    assert poly is not None
    assert abs(polygon_area(poly) - 1.0) < 1e-6, polygon_area(poly)
    # 空交: x>=1 且 x<=0
    hp2 = [
        ((1.0, 0.0), (0.0, -1.0)),
        ((0.0, 0.0), (0.0, 1.0)),
        ((0.0, 0.0), (1.0, 0.0)),
        ((1.0, 1.0), (-1.0, 0.0)),
    ]
    assert halfplane_intersection(hp2) is None
    print('half-plane-intersection all tests passed')

```

**PyPy 提示**: 排序瓶颈 O(n log n)；Python 中每轮双端队列操作大量调用 line_inter/on_left，注意把交点计算内联或用小函数。浮点输入时 eps 建议 1e-9~1e-12，与坐标量级相关。无界交（半平面朝外）记得补 4 条边界框半平面约束。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n log n)，排序为瓶颈；增量过程线性 |
| 空间 | O(n) |

### 局限

浮点精度：极角排序与 on_left 判断对退化输入（三点近似共线、狭长交区域）敏感，需按 eps 处理；平行半平面需去重；交集可能无界，若需有界答案要加边界框；若交集退化（点为线段/线段）则多边形顶点 < 3，需按题目语义处理。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P4196 | 4 | 【模板】半平面交 / [CQOI2006] 凸多边形：多凸多边形求交面积 | [https://www.luogu.com.cn/problem/P4196](https://www.luogu.com.cn/problem/P4196) |
| Luogu | P2600 | 5 | [ZJOI2008] 瞭望塔：半平面交求多边形核内最远观察点 | [https://www.luogu.com.cn/problem/P2600](https://www.luogu.com.cn/problem/P2600) |
| CP-Algorithms | halfplane-intersection | 4 | S&I 算法原理与边界框处理的标准参考 | [https://cp-algorithms.com/geometry/halfplane-intersection.html](https://cp-algorithms.com/geometry/halfplane-intersection.html) |

## Pitfalls · 易错点

- 必须先处理队尾再处理队首，否则一条新边可弹空全队时会用过期交点误判
- 同极角共线半平面要去重，保留最靠内侧的那条
- on_left 的 eps 方向写反导致把合法点判出
- 忽略无界交，需要时补边界框四条约束
- 交点退化（平行边）时 line_inter 返回 None 需处理
- 面积要取绝对值（多边形顶点顺序不定）

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/geometry/half-plane.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/geometry/half-plane.md)
- CP-Algorithms ✓ [https://cp-algorithms.com/geometry/halfplane-intersection.html](https://cp-algorithms.com/geometry/halfplane-intersection.html)
- 书籍 ✓ `CPH ch29`
