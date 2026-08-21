---
id: lattice-points
name: 格点计数
group: G-D-3
stage: advanced
priority: P2
depth_tier: standard
---

# 格点计数

> 线段/多边形内整点计数，结合皮克定理与整除递推

<!-- 元信息: id=lattice-points · group=G-D-3 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

格点计数问题：统计线段上、直线下区域、多边形内（或内加边界）的整点（整数坐标点）数量。三条主线：① 线段上的整点：端点 (x1,y1)-(x2,y2) 间整点数 = gcd(|x2-x1|,|y2-y1|)+1；② 整点多边形：皮克定理反解内部点数 i = (A2 - b + 2)/2，其中 A2 是两倍面积（叉积和），b 是边界整点数（各边 gcd 之和）；③ 一般（非整点顶点）多边形：把每条边看作直线 y=k·x+b，用 floor sum Σ floor((a·x+b)/m) 的类欧几里得递推 O(log n) 求出直线下整点数，再按边方向带符号累加（类似梯形积分）。核心引擎是 floor_sum。

## Why · 为什么

### 直觉 · Intuition

数'直线下的整点'就是数每个 x 处 y 能取几层，即 Σ floor((a·x+b)/m)。naive 逐个 x 是 O(n)，但把坐标轴翻转、斜率取倒数，剩余的点恰好构成一个规模更小的同构子问题——这就像欧几里得算法的'辗转'，每次参数减半，所以 O(log n)。多边形则是把每条边'底下的整点'像梯形积分一样带符号累加，凸的取正、凹的抵消，最后正好是内部整点数。

### 原理 · Principle

floor_sum(n,m,a,b) = Σ_{x=0}^{n-1} floor((a·x+b)/m)。递推：① 若 a≥m，拆出 floor(a/m)·(n-1)n/2 并取模；② 若 b≥m，拆出 floor(b/m)·n 并取模；③ 令 y_max = a·n+b，若 y_max < m 结束；④ 翻转：递归 floor_sum(n', a, m, y_max mod m)，其中 n' = floor(y_max/m)——几何意义是把直线关于 y=x 对称重数，直线下的点与翻转后直线下的点一一对应。整点多边形内部点用皮克定理 O(n)；非整点顶点时用 floor_sum 逐边积分，还需处理边界归属（端点/边上点）。

### 历史 · History

floor sum 的 O(log n) 递推被称作'类欧几里得算法'，因递归结构与欧几里得算法同构，在数论 OI 界流行，Luogu P5170 为模板题；cp-algorithms 的 'Lattice points of non-lattice polygon' 页将其用于非整点多边形格点计数。皮克定理（1899）处理整点多边形，二者互补覆盖格点计数问题族。

## How · 实现

### 伪代码

```python
# 线段上整点数（含端点）
on_segment(a, b) = gcd(|b.x-a.x|, |b.y-a.y|) + 1

# floor_sum: Σ_{x=0}^{n-1} floor((a*x+b)/m)，a,b≥0，O(log n)
def floor_sum(n, m, a, b):
    ans = 0
    while True:
        if a >= m: ans += (n-1)*n*(a//m)//2; a %= m
        if b >= m: ans += n*(b//m); b %= m
        y_max = a*n + b
        if y_max < m: break
        n, b = y_max // m, y_max % m
        m, a = a, m
    return ans

# 整点多边形内部点数（皮克定理）
def polygon_interior(poly):
    A2 = |Σ x_i*y_{i+1} - x_{i+1}*y_i|          # 两倍面积
    b  = Σ gcd(|dx_i|, |dy_i|)                    # 边界整点数
    return (A2 - b + 2) // 2
```

### Python 实现

```python
# -*- coding: utf-8 -*-
import math


def floor_sum(n, m, a, b):
    """Σ_{x=0}^{n-1} floor((a*x + b) / m)。要求 a,b>=0, m>0。O(log n)。
    这就是'类欧几里得'的核心递推。
    """
    ans = 0
    while True:
        if a >= m:
            ans += (n - 1) * n * (a // m) // 2
            a %= m
        if b >= m:
            ans += n * (b // m)
            b %= m
        y_max = a * n + b
        if y_max < m:
            break
        n = y_max // m
        b = y_max % m
        m, a = a, m
    return ans


def floor_sum_signed(n, m, a, b):
    """与 floor_sum 相同但允许 a、b 为负（先对 a 取模归并到 [0,m)，再平移 b）。"""
    ans = 0
    q, r = divmod(a, m)          # a = q*m + r, 0 <= r < m
    if q != 0:
        ans += q * n * (n - 1) // 2
        a = r
    if b < 0:
        k = (-b + m - 1) // m
        ans -= k * n
        b += k * m
    return ans + floor_sum(n, m, a, b)


def lattice_on_segment(a, b):
    """线段 a→b 上的整点数（含两端）。"""
    return math.gcd(abs(b[0]-a[0]), abs(b[1]-a[1])) + 1


def polygon_interior_points(poly):
    """整点多边形内部整点数（皮克定理）。顶点必须都是整点。"""
    n = len(poly)
    A2 = 0
    b = 0
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i+1) % n]
        A2 += x1*y2 - x2*y1
        b += math.gcd(abs(x2-x1), abs(y2-y1))
    A2 = abs(A2)
    return (A2 - b + 2) // 2


def polygon_boundary_points(poly):
    """整点多边形边界整点数。"""
    n = len(poly)
    return sum(math.gcd(abs(poly[(i+1) % n][0]-poly[i][0]),
                        abs(poly[(i+1) % n][1]-poly[i][1])) for i in range(n))


if __name__ == '__main__':
    import random
    # floor_sum 对拍暴力
    for _ in range(1000):
        n = random.randint(1, 40)
        m = random.randint(1, 50)
        a = random.randint(0, 40)
        b = random.randint(0, 50)
        bf = sum((a*i + b) // m for i in range(n))
        assert floor_sum(n, m, a, b) == bf, (n, m, a, b, floor_sum(n, m, a, b), bf)
    # floor_sum_signed 对拍（允许负 a,b）
    for _ in range(1000):
        n = random.randint(1, 40)
        m = random.randint(1, 50)
        a = random.randint(-30, 30)
        b = random.randint(-40, 40)
        bf = sum((a*i + b) // m for i in range(n))
        assert floor_sum_signed(n, m, a, b) == bf, (n, m, a, b, floor_sum_signed(n, m, a, b), bf)
    # 线段整点数
    assert lattice_on_segment((0, 0), (6, 9)) == 4    # gcd(6,9)=3 → 4 个点
    assert lattice_on_segment((0, 0), (0, 5)) == 6
    assert lattice_on_segment((0, 0), (1, 1)) == 2
    # 皮克定理与暴力对拍
    def brute_interior(poly):
        xs = [p[0] for p in poly]
        ys = [p[1] for p in poly]
        cnt = 0
        for x in range(min(xs), max(xs)+1):
            for y in range(min(ys), max(ys)+1):
                n = len(poly)
                onb = False
                for i in range(n):
                    x1, y1 = poly[i]
                    x2, y2 = poly[(i+1) % n]
                    if (y1-y)*(x2-x) == (y2-y)*(x1-x) and min(x1,x2) <= x <= max(x1,x2) and min(y1,y2) <= y <= max(y1,y2):
                        onb = True
                if onb:
                    continue
                inside = False
                for i in range(n):
                    x1, y1 = poly[i]
                    x2, y2 = poly[(i+1) % n]
                    if (y1 > y) != (y2 > y):
                        xi = x1 + (x2-x1)*(y-y1)/(y2-y1)
                        if x < xi:
                            inside = not inside
                if inside:
                    cnt += 1
        return cnt
    polys = [
        [(0, 0), (5, 0), (5, 3), (0, 3)],
        [(0, 0), (4, 0), (4, 4), (0, 4)],
        [(0, 0), (3, 1), (4, 4), (1, 3)],
        [(0, 0), (2, 0), (2, 2), (0, 2)],
    ]
    for poly in polys:
        assert polygon_interior_points(poly) == brute_interior(poly), (poly, polygon_interior_points(poly), brute_interior(poly))
    print('lattice-points all tests passed')

```

**PyPy 提示**: floor_sum 迭代 O(log n)，PyPy 下极快，参数可到 1e18（Python 大整数无溢出）。多边形整点：整点用皮克 O(n)；非整点顶点需按边方向对 floor_sum 做带符号累加，注意每条边要把 x 区间离散化并用 ceil/floor 处理非整端点，边界点归属单独修正。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 线段上整点 O(log C)（gcd）；floor_sum 单次 O(log C)；皮克定理 O(n) |
| 空间 | O(1) |

### 局限

floor_sum 要求 a,b≥0，负数需先归一化（floor_sum_signed）；非整点多边形逐边积分时，端点非整点的取整方向（ceil/floor）与边界点归属需要仔细处理，否则差 1；皮克定理仅适用整点顶点且不自交；浮点直线不能用 floor_sum（斜率必须有理数）。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| CSES | 2193 | 3 | Polygon Lattice Points：皮克定理 + 边界 gcd，求内部与边界整点数 | [https://cses.fi/problemset/task/2193/](https://cses.fi/problemset/task/2193/) |
| Luogu | P5170 | 5 | 【模板】类欧几里德算法：floor_sum 三合一递推模板题 | [https://www.luogu.com.cn/problem/P5170](https://www.luogu.com.cn/problem/P5170) |
| Luogu | P2735 | 4 | 网 Electric Fences：整点多边形计数综合（皮克定理） | [https://www.luogu.com.cn/problem/P2735](https://www.luogu.com.cn/problem/P2735) |

## Pitfalls · 易错点

- floor_sum 的 a、b 必须非负，负输入要先归一化
- 非整点多边形逐边积分时端点取整方向写反会差 1
- 边界整点归属：内部点数不含边界（皮克定理 i 的定义）
- 自交多边形不适用
- 线段上整点数公式是 gcd+1（含两端），不要漏 +1 或重复计端点

## Sources · 信源

- CP-Algorithms ✓ [https://cp-algorithms.com/geometry/lattice-points.html](https://cp-algorithms.com/geometry/lattice-points.html)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/geometry/pick.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/geometry/pick.md)
