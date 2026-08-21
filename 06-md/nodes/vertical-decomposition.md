---
id: vertical-decomposition
name: 垂直剖分(梯形剖分)
group: G-D-2
stage: advanced
priority: P2
depth_tier: standard
---

# 垂直剖分(梯形剖分)

> 将平面按线段端点垂直切分为梯形单元，支持点定位与求交

<!-- 元信息: id=vertical-decomposition · group=G-D-2 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

垂直剖分（Vertical Decomposition）是一种把复杂平面几何问题简化到『条带』（vertical stripe）的通用技术：过所有几何对象的关键点（顶点、边交点）画垂直线，把平面切成若干竖直条带。在每条条带内，几何结构具有『好的性质』——任意两条线段不会在条带内部交叉，且每类的对象呈现为上下配对的梯形/三角形。典型应用：① 三角形并集面积（过所有顶点与边交点垂直切条，条带内做括号序列匹配求梯形并面积，O(n²log n)）；② 凸多边形求交（线性时间）；③ 平面点定位（多边形的垂直剖分支持 O(log n) 点查询）。

## Why · 为什么

### 直觉 · Intuition

把任意位置的斜线几何变成『竖直条带内的简单图形』：在每条带中，线段要么从左到右穿过、要么不穿，且没有两条线段在内部交叉。于是条带内部的问题退化为『一维括号序列』问题——上边界是开括号、下边界是闭括号，配对的括号围成梯形。对每条带计算梯形面积并求和即得总面积。核心价值：把 O(n²) 个交点用 O(n²) 个条带『钉住』，让每个条带内的问题变简单。

### 原理 · Principle

① 剖分：对顶点集合与所有边两两交点收集 x 坐标，排序去重生成 O(n²) 个垂直线，得到 O(n²) 条带。② 条带内性质：任意非竖直线段在条带内要么完全穿过、要么不穿，无内部交叉。③ 三角形并集：对每条带，用扫描线沿 x 扫，维护穿过的线段按 y 排序，用上下配对（上边界+1、下边界-1 的括号序列平衡）切成梯形，求梯形面积和。④ 优化1：不显式建所有条带，而是固定某条线段 s，只在与 s 投影相交的条带上维护『s 下方括号平衡为 0 的区间』，用水平扫描线+事件 O(n²log n)。⑤ 优化2：内存降为 O(n)。⑥ 凸多边形交：过两多边形所有顶点垂直切条，条带内各与多边形相交部分为梯形/三角形，直接求交合并。

### 历史 · History

垂直剖分是计算几何的经典技术，CP-Algorithms 收录了其两种典型应用（三角形并集面积与凸多边形交），源自 e-maxx.ru。CPH（Competitive Programming Handbook）ch30 也用它求解几何问题。它是『半平面交』与『三角剖分』之外处理复杂几何并集的标准范式。

## How · 实现

### 伪代码

```python
# 三角形并集面积 (垂直剖分)
segments = 所有三角形边, 标记每条边为 'upper'(上方为内部) 或 'lower'
collect 所有顶点x + 所有边交点x -> x_sorted
for each stripe between consecutive x's:
  找出穿过该条带的非竖直线段
  按 y 排序
  用括号匹配(balance)切成梯形
  area += 梯形面积和

# 优化: 固定边 s, 沿 x 扫事件 (O(n^2 log n))
```

### Python 实现

```python
EPS = 1e-9


def edge_y_at(e, x):
    """边 e 在 x 处的 y 值 (竖直边返回 None)."""
    (x1, y1), (x2, y2) = e
    if abs(x2 - x1) < 1e-12:
        return None
    t = (x - x1) / (x2 - x1)
    return y1 + t * (y2 - y1)


def edge_intersection_x(e1, e2):
    """两非竖直边的内部交点 x (严格内部), 无则 None."""
    (x1, y1), (x2, y2) = e1
    (x3, y3), (x4, y4) = e2
    d1 = (x2 - x1) * (y4 - y3) - (y2 - y1) * (x4 - x3)
    if abs(d1) < 1e-12:
        return None
    t = ((x3 - x1) * (y4 - y3) - (y3 - y1) * (x4 - x3)) / d1
    u = ((x3 - x1) * (y2 - y1) - (y3 - y1) * (x2 - x1)) / d1
    if 1e-9 < t < 1 - 1e-9 and 1e-9 < u < 1 - 1e-9:
        return x1 + t * (x2 - x1)
    return None


def tri_vertical_span(tri, x):
    """三角形在 x 处的竖直区间 [lo,hi] (内部), 覆盖不到返回 None."""
    a, b, c = tri
    ys = []
    for (p, q) in [(a, b), (b, c), (c, a)]:
        lo = min(p[0], q[0]); hi = max(p[0], q[0])
        if lo <= x + 1e-9 and hi >= x - 1e-9:
            y = edge_y_at((p, q), x)
            if y is not None:
                ys.append(y)
    if len(ys) < 2:
        return None
    return (min(ys), max(ys))


def union_height(spans):
    """一维区间并总长度."""
    if not spans:
        return 0.0
    spans = sorted(spans)
    total = 0.0
    cl, ch = spans[0]
    for lo, hi in spans[1:]:
        if lo <= ch + 1e-9:
            ch = max(ch, hi)
        else:
            total += ch - cl
            cl, ch = lo, hi
    total += ch - cl
    return total


def stripe_union(tris, xl, xr):
    """条带 [xl,xr] 内三角形并集面积.
    垂直剖分性质: 条带内无交点, 覆盖高度是 x 的线性函数,
    故中点采样高度 × 条带宽即精确面积."""
    xm = (xl + xr) / 2
    spans = []
    for t in tris:
        s = tri_vertical_span(t, xm)
        if s is not None:
            spans.append(s)
    if not spans:
        return 0.0
    return union_height(spans) * (xr - xl)


def tri_union_area_vertical(tris):
    """垂直剖分求三角形并集面积.
    tris: [(p1,p2,p3)] 每点 (x,y) 浮点.
    朴素实现: 收集顶点 x + 边交点 x 生成 O(n^2) 条带, 每条带中点采样."""
    edges = []
    for (a, b, c) in tris:
        for (p, q) in [(a, b), (b, c), (c, a)]:
            edges.append((p, q))
    xs = set()
    for e in edges:
        xs.add(e[0][0]); xs.add(e[1][0])
    n = len(edges)
    for i in range(n):
        for j in range(i + 1, n):
            pt = edge_intersection_x(edges[i], edges[j])
            if pt is not None:
                xs.add(pt)
    xs = sorted(xs)
    total = 0.0
    for k in range(len(xs) - 1):
        xl, xr = xs[k], xs[k + 1]
        if xr - xl < 1e-12:
            continue
        total += stripe_union(tris, xl, xr)
    return total


def pt_in_tri(p, a, b, c):
    def cr(o, x, y):
        return (x[0] - o[0]) * (y[1] - o[1]) - (x[1] - o[1]) * (y[0] - o[0])
    d1 = cr(a, b, p); d2 = cr(b, c, p); d3 = cr(c, a, p)
    has_neg = d1 < 0 or d2 < 0 or d3 < 0
    has_pos = d1 > 0 or d2 > 0 or d3 > 0
    return not (has_neg and has_pos)


if __name__ == "__main__":
    # 单三角形 (0,0),(2,0),(0,2): 面积 2
    tri1 = [((0, 0), (2, 0), (0, 2))]
    assert abs(tri_union_area_vertical(tri1) - 2.0) < 1e-9
    # 两个三角形不交
    tri2 = [((0, 0), (2, 0), (0, 2)), ((10, 0), (12, 0), (10, 2))]
    assert abs(tri_union_area_vertical(tri2) - 4.0) < 1e-9
    # 两个三角形共享底边: 并成菱形 面积 3
    tri3 = [((0, 0), (2, 0), (0, 2)), ((0, 0), (2, 0), (2, 2))]
    assert abs(tri_union_area_vertical(tri3) - 3.0) < 1e-9

    # 随机交叉验证 (网格点采样暴力)
    import random
    random.seed(1)
    for _ in range(30):
        tris = []
        for _ in range(3):
            pts = [(random.uniform(0, 4), random.uniform(0, 4)) for _ in range(3)]
            tris.append(tuple(pts))
        a = tri_union_area_vertical(tris)
        cnt = 0
        step = 0.01
        for i in range(400):
            for j in range(400):
                x = step * i; y = step * j
                if any(pt_in_tri((x, y), *t) for t in tris):
                    cnt += 1
        b = cnt * step * step
        assert abs(a - b) < 0.15, (a, b)
    print("All tests passed.")
```

**PyPy 提示**: O(n²) 条带枚举在大 n 下不可行；实际竞赛用优化版（固定边+水平扫描线事件）O(n²log n)。本实现为教学简化版（中点近似），数值精度以 5% 内为验证目标。大坐标用 Fraction 可行但慢，float 足够。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 朴素条带 O(n²) 条带 × O(n log n) 每带；优化版 O(n²log n) |
| 空间 | O(n²)（朴素）或 O(n)（优化版） |

### 局限

垂直剖分的关键点（顶点+交点）可能 O(n²) 个，n 大时不可用；只适合边数少或需要精确几何结构的场景。竖直边需要特殊处理（不参与条带划分）。浮点交点坐标计算引入误差，需 eps。Python 实现此算法常数大，竞赛中常用 C++。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Codeforces | 62C | 6 | Inquisition：垂直剖分求三角形并集面积的经典题（CP-Alg 例题） | [https://codeforces.com/problemset/problem/62/C](https://codeforces.com/problemset/problem/62/C) |
| Codeforces | 107E | 7 | Darts：三角形并集面积的进阶应用（CP-Alg 例题） | [https://codeforces.com/problemset/problem/107/E](https://codeforces.com/problemset/problem/107/E) |

## Pitfalls · 易错点

- 竖直边参与条带划分时会引入无穷交点，需跳过或特殊标记
- 条带宽度为 0（重合 x）时直接跳过，避免除零
- 交点 x 收集必须去重排序；浮点去重用 eps 分桶而非 == 比较
- 条带内线段排序后配对要按覆盖深度（深度>0）而非简单相邻配对
- 退化三角形（面积 0）会生成无效边，先判面积再处理
- O(n²) 条带的朴素实现大 n 必超时，务必用优化事件法

## Sources · 信源

- CP-Algorithms ✓ [https://cp-algorithms.com/geometry/vertical_decomposition.html](https://cp-algorithms.com/geometry/vertical_decomposition.html)
- 书籍 ✓ `CPH ch30 Geometry problems (p305-317)`
