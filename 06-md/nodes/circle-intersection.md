---
id: circle-intersection
name: 圆与直线/圆求交
group: G-D-2
stage: advanced
priority: P2
depth_tier: standard
---

# 圆与直线/圆求交

> 解几何方程求圆与直线、圆与圆交点

<!-- 元信息: id=circle-intersection · group=G-D-2 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

计算几何基础运算：求①圆与直线的交点，②圆与圆的交点。圆-直线：把直线写为 Ax+By+C=0，先求直线上离原点最近的点 (x₀,y₀)=(-AC/(A²+B²), -BC/(A²+B²))，其到圆心距离 d₀=|C|/√(A²+B²)；若 d₀>r 无交点，d₀=r 一个切点，d₀<r 两个交点（沿直线方向 ±√(r²-d₀²) 偏移）。圆-圆：两圆方程相减消去二次项，得到一个线性方程（根轴/radical line），把问题化归为『第一圆与该直线求交』；特殊处理同心圆（半径相同则重合无穷多交点，否则无交点）。应用：几何求交、区域划分、计算几何题的基本原语。

## Why · 为什么

### 直觉 · Intuition

圆-直线：几何而非代数。垂直投影给出圆心到直线的垂足 (x₀,y₀)，它就是直线上离圆心最近的点。若垂距大于半径则整条线都在圆外；等于半径相切；小于则弦长 2√(r²-d₀²)，弦的两端就是交点。圆-圆：两个圆方程相减，x²,y² 项抵消，得到根轴的直线方程——两个圆的交点恰在该直线上，于是退化为圆-直线求交。同心圆时根轴退化（0=0），单独讨论。

### 原理 · Principle

① 圆-直线：垂足 x₀=-AC/(A²+B²), y₀=-BC/(A²+B²)；d₀=|C|/√(A²+B²)。d₀>r：无；|d₀-r|<eps：一个点；否则 m=√((r²-d₀²)/(A²+B²))，交点 (x₀±B·m, y₀∓A·m)（方向向量 (-B,A) 单位化）。② 圆-圆：设圆心 C₁(0,0)（平移），C₂=(vx,vy)，半径 r₁,r₂；相减得 Ax+By+C=0，其中 A=-2vx, B=-2vy, C=vx²+vy²+r₁²-r₂²，然后圆-直线求交，最后把交点平移到原始坐标系。③ 同心圆：vx=vy=0，若 r₁=r₂ 无穷交点，否则无。④ 判定相交：圆心距 d 与 r₁+r₂、|r₁-r₂| 比较（外离/外切/相交/内切/内含）。

### 历史 · History

圆与直线/圆的求交是欧氏几何的基本问题，CP-Algorithms 的 'Circle-Line Intersection' 与 'Circle-Circle Intersection' 给出了现代数值稳定解法（源自 e-maxx.ru）。OI Wiki 的 misc 几何章节也收录。这类原语在几何计算题、圆覆盖、圆弧剖分问题中高频复用。

## How · 实现

### 伪代码

```python
# 圆-直线
x0 = -A*C/(A^2+B^2); y0 = -B*C/(A^2+B^2)
d2 = C*C/(A^2+B^2)          # 垂距平方
if d2 > r^2 + eps: return []
if |d2 - r^2| < eps: return [(x0,y0)]
m = sqrt((r^2-d2)/(A^2+B^2))
return [(x0+B*m, y0-A*m), (x0-B*m, y0+A*m)]

# 圆-圆 (平移圆心1到原点)
A=-2*vx; B=-2*vy; C=vx^2+vy^2+r1^2-r2^2
交点 = circle_line_intersect(C1, r1, 直线(A,B,C))  # 再平移回原坐标
```

### Python 实现

```python
import math

EPS = 1e-9


def circle_line_intersect(c, r, line):
    """圆(圆心c, 半径r) 与直线 Ax+By+C=0 的交点.
    c: (x,y). 返回 [(x,y),...] 0/1/2 个."""
    A, B, C = line
    cx, cy = c
    # 平移: 圆心到原点
    C2 = C + A * cx + B * cy
    denom = A * A + B * B
    x0 = -A * C2 / denom
    y0 = -B * C2 / denom
    d2 = C2 * C2 / denom
    r2 = r * r
    if d2 > r2 + EPS:
        return []
    if abs(d2 - r2) < EPS:
        return [(x0 + cx, y0 + cy)]
    m = math.sqrt((r2 - d2) / denom)
    return [(x0 + B * m + cx, y0 - A * m + cy),
            (x0 - B * m + cx, y0 + A * m + cy)]


def circle_circle_intersect(c1, r1, c2, r2):
    """两圆交点. 返回 (state, pts):
    state: 'none'|'point'|'two'|'same'|'inside'
    pts: 交点列表 (0/1/2)."""
    x1, y1 = c1
    x2, y2 = c2
    vx, vy = x2 - x1, y2 - y1
    d2 = vx * vx + vy * vy
    if abs(d2) < EPS:
        if abs(r1 - r2) < EPS:
            return ('same', [])
        return ('inside', [])  # 同心不同半径
    A = -2 * vx
    B = -2 * vy
    C = d2 + r1 * r1 - r2 * r2
    # 圆-直线求交 (以 c1 为圆心), 平移回来
    denom = A * A + B * B
    x0 = -A * C / denom + x1
    y0 = -B * C / denom + y1
    d0_2 = (x0 - x1) ** 2 + (y0 - y1) ** 2
    if d0_2 > r1 * r1 + EPS:
        return ('none', [])
    if abs(d0_2 - r1 * r1) < EPS:
        return ('point', [(x0, y0)])
    m = math.sqrt((r1 * r1 - d0_2) / denom)
    pts = [(x0 + B * m, y0 - A * m), (x0 - B * m, y0 + A * m)]
    return ('two', pts)


def on_circle(c, r, p, eps=1e-6):
    return abs((p[0] - c[0]) ** 2 + (p[1] - c[1]) ** 2 - r * r) < eps


if __name__ == "__main__":
    # 圆-直线: 圆心(0,0) r=5, 直线 y=0 (0,0 半径5, 直线 x轴) => 交点 (±5,0)
    pts = circle_line_intersect((0, 0), 5, (0, 1, 0))  # y=0 => A=0,B=1,C=0
    assert len(pts) == 2
    assert on_circle((0, 0), 5, pts[0]) and on_circle((0, 0), 5, pts[1])
    # 相切: 圆心(0,0) r=1, x=1 => (1,0)
    pts = circle_line_intersect((0, 0), 1, (1, 0, -1))
    assert len(pts) == 1 and abs(pts[0][0] - 1) < 1e-6 and abs(pts[0][1]) < 1e-6
    # 无交: 圆心(0,0) r=1, x=2
    assert circle_line_intersect((0, 0), 1, (1, 0, -2)) == []

    # 圆-圆: 相交两圆 (0,0)r=3, (4,0)r=3 => 圆心距 4, 交点 x=2, y=±√(9-4)
    st, pts = circle_circle_intersect((0, 0), 3, (4, 0), 3)
    assert st == 'two'
    for p in pts:
        assert on_circle((0, 0), 3, p) and on_circle((4, 0), 3, p)
    assert abs(pts[0][0] - 2) < 1e-6
    assert abs(abs(pts[0][1]) - math.sqrt(5)) < 1e-6
    # 外切: (0,0)r=1, (2,0)r=1 => (1,0)
    st, pts = circle_circle_intersect((0, 0), 1, (2, 0), 1)
    assert st == 'point' and abs(pts[0][0] - 1) < 1e-6
    # 内切: (0,0)r=3, (1,0)r=2 => (3,0)
    st, pts = circle_circle_intersect((0, 0), 3, (1, 0), 2)
    assert st == 'point' and abs(pts[0][0] - 3) < 1e-6
    # 无交: 外离
    st, _ = circle_circle_intersect((0, 0), 1, (5, 0), 1)
    assert st == 'none'
    # 内含
    st, _ = circle_circle_intersect((0, 0), 5, (1, 0), 1)
    assert st == 'none'
    # 重合
    st, _ = circle_circle_intersect((0, 0), 3, (0, 0), 3)
    assert st == 'same'
    # 同心不同径
    st, _ = circle_circle_intersect((0, 0), 3, (0, 0), 5)
    assert st == 'inside'

    # 随机交叉验证 (数值满足两圆方程)
    import random
    random.seed(17)
    for _ in range(300):
        c1 = (random.uniform(-10, 10), random.uniform(-10, 10))
        c2 = (random.uniform(-10, 10), random.uniform(-10, 10))
        r1 = random.uniform(0.5, 8)
        r2 = random.uniform(0.5, 8)
        st, pts = circle_circle_intersect(c1, r1, c2, r2)
        for p in pts:
            assert on_circle(c1, r1, p, 1e-6) and on_circle(c2, r2, p, 1e-6), (c1, r1, c2, r2, p)
        if st == 'two':
            assert len(pts) == 2
        elif st == 'point':
            assert len(pts) == 1
    print("All tests passed.")
```

**PyPy 提示**: 圆-直线/圆-圆求交 O(1)。大坐标平方可能溢出 float（1e154+），整点大坐标考虑 Decimal 或 __int128（C++）。EPS 与坐标量级匹配（坐标 1e9 时用 1e-6 级别）。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(1) |
| 空间 | O(1) |

### 局限

浮点精度：内切/外切等临界情形 d≈r₁±r₂ 需 eps 宽容。同心圆退化为单独分支。大坐标平方溢出。圆-圆化归圆-直线时根轴直线方程在同心时退化（A=B=0），必须先行判断。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Codeforces | 933C | 6 | A Colorful Prospect：圆与圆交点数/区域划分（CP-Alg 圆交例题） | [https://codeforces.com/problemset/problem/933/C](https://codeforces.com/problemset/problem/933/C) |
| SPOJ | CIRCINT | 5 | Circle intersection：圆与圆相交判定与交点（CP-Alg 例题） | [https://www.spoj.com/problems/CIRCINT/](https://www.spoj.com/problems/CIRCINT/) |
| TIMUS | 1429 | 6 | Biscuits：圆/圆弧交点类综合（CP-Alg 圆交例题同源） | [https://acm.timus.ru/problem.aspx?space=1&num=1429](https://acm.timus.ru/problem.aspx?space=1&num=1429) |

## Pitfalls · 易错点

- 圆-圆用直线化归时忘记把交点平移回原始坐标系
- 同心圆未单独处理（A=B=0 导致除零）
- 相切判定用 d₂≈r² 而非 d₂≥r²（等号分支）
- 把圆心距 d 与 r₁-r₂ 绝对值比较时符号写反（内含/内切区分）
- 浮点下交点对称性（±m 两个方向）别写反
- 对 0 半径圆（退化）未处理

## Sources · 信源

- CP-Algorithms ✓ [https://cp-algorithms.com/geometry/circle-line-intersection.html](https://cp-algorithms.com/geometry/circle-line-intersection.html)
- CP-Algorithms ✓ [https://cp-algorithms.com/geometry/circle-circle-intersection.html](https://cp-algorithms.com/geometry/circle-circle-intersection.html)
- OI Wiki ✓ [https://oi-wiki.org/geometry/2d/](https://oi-wiki.org/geometry/2d/)
