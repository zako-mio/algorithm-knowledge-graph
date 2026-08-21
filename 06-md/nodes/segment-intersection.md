---
id: segment-intersection
name: 线段相交判定与求交
group: G-D-2
stage: intermediate
priority: P1
depth_tier: standard
---

# 线段相交判定与求交

> 跨立实验判两线段是否相交并求交点，几何求交基础

<!-- 元信息: id=segment-intersection · group=G-D-2 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

给定两条线段 AB、CD（各由两端点定义，可退化为单点），判定是否相交并求交集的形状：空集、单个点、或整条重叠线段。整数坐标下可用纯整数运算（跨立实验）判定：① 先做包围盒检查（x/y 投影区间相交），处理共线重叠；② 跨立实验：A、B 分居直线 CD 两侧且 C、D 分居直线 AB 两侧（用叉积符号判定）。求交点：构造两线段的直线方程，用 Cramer 法则求直线交点，再检查交点是否在两条线段上（包围盒内）。共线时交点为区间交叠。这是几何求交、扫描线线段求交、以及众多平面几何题的基础原语。

## Why · 为什么

### 直觉 · Intuition

叉积的几何意义是『有向面积/方向判断』：cross(P,Q)>0 表示 Q 在 P 的逆时针方向。线段相交判定的本质是方向测试：若 A、B 在直线 CD 的两侧，说明 AB 与直线 CD 相交；同时 C、D 在直线 AB 的两侧，则 AB 与 CD 真的『互相穿过』。边界情形（端点共线、共线重叠）用包围盒区间交叠兜住。这比『求交点再看是否在段上』更快且能处理整数。

### 原理 · Principle

① 叉积 cross(a,b,c)=(b-a)×(c-a)，符号表示 c 在 ab 的哪侧。② 跨立实验：sgn(cross(a,b,c))≠sgn(cross(a,b,d)) 且 sgn(cross(c,d,a))≠sgn(cross(c,d,b)) ⇒ 相交（严格内侧）。③ 共线情形：若 cross(a,b,c)=cross(a,b,d)=0 则四点共线，检查投影区间 [min(a.x,b.x),max(a.x,b.x)] 与 [min(c.x,d.x),max(c.x,d.x)] 相交（x 与 y 两个方向），用 inter1 函数 max(l1,l2)≤min(r1,r2)。④ 求交点：直线方程 Cramer 法则，若平行则共线重叠情形取左端点最大/右端点最小；否则交点需满足 0≤t≤1 参数化在段内。⑤ EPS 处理浮点；整数情形 sgn 精确。

### 历史 · History

线段相交判定是计算几何的经典基础问题，出现在 Bentley-Ottmann 扫描线算法（1979）以及大量几何问题中。CP-Algorithms 收录了整数版『Check if two segments intersect』（源自 e-maxx.ru）与浮点版『Intersection of Segments』，是目前标准参考。OI Wiki 的 2D 几何也把它列为基本运算。

## How · 实现

### 伪代码

```python
# 判定相交 (整数, 精确)
def sgn(x): return 1 if x>0 else (-1 if x<0 else 0)
def cross(a,b,c): return (b-a)×(c-a)   # 叉积

def segments_intersect(a,b,c,d):
  if cross(a,b,c)==0 and cross(a,b,d)==0:
    # 共线: 检查 x 和 y 投影区间
    return inter1(a.x,b.x,c.x,d.x) and inter1(a.y,b.y,c.y,d.y)
  return sgn(cross(a,b,c))!=sgn(cross(a,b,d)) and \
         sgn(cross(c,d,a))!=sgn(cross(c,d,b))

def inter1(l1,r1,l2,r2):
  if l1>r1: l1,r1=r1,l1
  if l2>r2: l2,r2=r2,l2
  return max(l1,l2) <= min(r1,r2)

# 求交点 (浮点): 直线方程 Cramer + 参数化检查
```

### Python 实现

```python
EPS = 1e-9


def cross(ax, ay, bx, by):
    return ax * by - ay * bx


def orient(a, b, c):
    """叉积 (b-a)×(c-a), 判断 c 相对 ab 的方位."""
    return cross(b[0] - a[0], b[1] - a[1], c[0] - a[0], c[1] - a[1])


def on_segment(a, b, p, eps=EPS):
    """点 p 是否在闭线段 ab 上 (含端点)."""
    return (min(a[0], b[0]) - eps <= p[0] <= max(a[0], b[0]) + eps and
            min(a[1], b[1]) - eps <= p[1] <= max(a[1], b[1]) + eps and
            abs(orient(a, b, p)) <= eps)


def segments_intersect(a, b, c, d, eps=EPS):
    """整数或浮点通用: 判定两线段是否相交 (含端点)."""
    o1 = orient(a, b, c)
    o2 = orient(a, b, d)
    o3 = orient(c, d, a)
    o4 = orient(c, d, b)
    if abs(o1) < eps and abs(o2) < eps and abs(o3) < eps and abs(o4) < eps:
        # 共线: 投影区间交叠
        ix = max(min(a[0], b[0]), min(c[0], d[0])) <= min(max(a[0], b[0]), max(c[0], d[0])) + eps
        iy = max(min(a[1], b[1]), min(c[1], d[1])) <= min(max(a[1], b[1]), max(c[1], d[1])) + eps
        return ix and iy
    def sgn(v):
        return 1 if v > eps else (-1 if v < -eps else 0)
    return sgn(o1) != sgn(o2) and sgn(o3) != sgn(o4)


def segment_intersection_point(a, b, c, d):
    """求两线段交点(浮点).
    返回 ('point',x,y) 单点; ('segment',p,q) 重叠段; ('none',) 无交点."""
    # 直线 ax+by+c=0
    def lf(p, q):
        A = q[1] - p[1]; B = p[0] - q[0]; C = -A * p[0] - B * p[1]
        return (A, B, C)
    A1, B1, C1 = lf(a, b)
    A2, B2, C2 = lf(c, d)
    det = cross(A1, B1, A2, B2)
    if abs(det) < EPS:
        # 平行: 若共线且区间交叠 -> 重叠段
        if abs(orient(a, b, c)) < EPS and segments_intersect(a, b, c, d):
            # 取两个方向的左端最大值, 右端最小值
            pts = sorted([a, b, c, d])
            lo = max(min(a, b), min(c, d))
            hi = min(max(a, b), max(c, d))
            return ('segment', tuple(lo), tuple(hi))
        return ('none',)
    x = -(C1 * B2 - C2 * B1) / det
    y = -(A1 * C2 - A2 * C1) / det
    if on_segment(a, b, (x, y)) and on_segment(c, d, (x, y)):
        return ('point', x, y)
    return ('none',)


if __name__ == "__main__":
    # 相交: (0,0)-(2,2) 与 (0,2)-(2,0) 交于 (1,1)
    assert segments_intersect((0, 0), (2, 2), (0, 2), (2, 0))
    r = segment_intersection_point((0, 0), (2, 2), (0, 2), (2, 0))
    assert r[0] == 'point' and abs(r[1] - 1) < 1e-9 and abs(r[2] - 1) < 1e-9

    # 不相交: 平行且不共线
    assert not segments_intersect((0, 0), (1, 1), (0, 2), (1, 3))
    assert segment_intersection_point((0, 0), (1, 1), (0, 2), (1, 3))[0] == 'none'

    # 共线重叠: (0,0)-(3,0) 与 (1,0)-(4,0)
    assert segments_intersect((0, 0), (3, 0), (1, 0), (4, 0))
    r = segment_intersection_point((0, 0), (3, 0), (1, 0), (4, 0))
    assert r[0] == 'segment'
    assert abs(r[1][0] - 1) < 1e-9 and abs(r[2][0] - 3) < 1e-9

    # 端点相接: (0,0)-(1,1) 与 (1,1)-(2,0)
    assert segments_intersect((0, 0), (1, 1), (1, 1), (2, 0))
    r = segment_intersection_point((0, 0), (1, 1), (1, 1), (2, 0))
    assert r[0] == 'point' and abs(r[1] - 1) < 1e-9 and abs(r[2] - 1) < 1e-9

    # 相距很远
    assert not segments_intersect((0, 0), (1, 0), (10, 10), (11, 10))

    # 随机交叉验证 (用整数精确 orient 判定)
    import random
    random.seed(9)

    def exact_int(a, b, c, d):
        def sgn(v):
            return 1 if v > 0 else (-1 if v < 0 else 0)
        o1 = sgn(orient(a, b, c))
        o2 = sgn(orient(a, b, d))
        o3 = sgn(orient(c, d, a))
        o4 = sgn(orient(c, d, b))
        if o1 == 0 and o2 == 0:
            ix = max(min(a[0], b[0]), min(c[0], d[0])) <= min(max(a[0], b[0]), max(c[0], d[0]))
            iy = max(min(a[1], b[1]), min(c[1], d[1])) <= min(max(a[1], b[1]), max(c[1], d[1]))
            return ix and iy
        return o1 != o2 and o3 != o4

    for _ in range(500):
        pts = [(random.randint(-10, 10), random.randint(-10, 10)) for _ in range(4)]
        a, b, c, d = pts
        g = segments_intersect(a, b, c, d)
        e = exact_int(a, b, c, d)
        assert g == e, (pts, g, e)
    print("All tests passed.")
```

**PyPy 提示**: 整数坐标下 orient 全整数运算无精度问题；浮点需 eps。高频调用时把 orient 写成局部变量/内联可显著提速。sorted 对点按 x 再 y 排序即可做共线区间取交。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(1) 单次判定；n 条线段两两 O(n²) |
| 空间 | O(1) |

### 局限

浮点坐标下四点近似共线的判定可能不稳定（eps 敏感性）。整数坐标是最佳场景（sgn 精确）。跨立实验对『T 形』接触（一端点落在另一条上）仍正确，但浮点时端点恰在线上需要 eps 宽容。求交点需要额外一次直线求交。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| CSES | 2190 | 3 | Line Segment Intersection：纯整数线段相交判定模板（CP-Alg 例题） | [https://cses.fi/problemset/task/2190](https://cses.fi/problemset/task/2190) |
| Luogu | P1496 | 3 | 火烧赤壁：线段覆盖/区间合并，与线段相交同源的扫描线题 | [https://www.luogu.com.cn/problem/P1496](https://www.luogu.com.cn/problem/P1496) |
| UVA | 866 | 4 | Intersecting line segments in a grid：判断线段相交并计段数（经典 UVA 线段相交题） | [https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=807](https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=807) |

## Pitfalls · 易错点

- 只用跨立实验不检查共线情形（共线时必须检查投影区间交叠）
- 叉积符号判断方向写反（orient(a,b,c) 与 orient(b,a,c) 互为相反数）
- 浮点坐标下 sgn 误判 0：需用 eps 而非 ==0
- 求交点时平行/共线分不清：先判 det=0 再判是否共线，共线再取区间交
- 忽略退化线段（单点）：单点也要能判定相交
- 线段端点恰在对方上（T 形）容易漏判：跨立实验边界符号要用 ≥/≤ 处理（含 0）

## Sources · 信源

- CP-Algorithms ✓ [https://cp-algorithms.com/geometry/check-segments-intersection.html](https://cp-algorithms.com/geometry/check-segments-intersection.html)
- CP-Algorithms ✓ [https://cp-algorithms.com/geometry/segments-intersection.html](https://cp-algorithms.com/geometry/segments-intersection.html)
- OI Wiki ✓ [https://oi-wiki.org/geometry/2d/](https://oi-wiki.org/geometry/2d/)
