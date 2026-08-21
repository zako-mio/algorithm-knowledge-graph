---
id: line-intersection
name: 直线交点
group: G-D-2
stage: intermediate
priority: P2
depth_tier: standard
---

# 直线交点

> 用叉积判定两直线位置关系并求交点坐标

<!-- 元信息: id=line-intersection · group=G-D-2 · stage=intermediate · priority=P2 · depth_tier=standard -->

## What · 是什么

给定两条直线，求它们的交点或判定平行/重合。直线可用方程 ax+by+c=0 表示，两直线的交点即解二元一次方程组：a₁x+b₁y+c₁=0 与 a₂x+b₂y+c₂=0。用 Cramer 法则：分母 D=a₁b₂-a₂b₁（即法向量叉积）；若 |D|<eps 则平行；若平行且 (a₁,b₁,c₁) 与 (a₂,b₂,c₂) 成比例则重合，否则无交点。交点坐标 x=-(c₁b₂-c₂b₁)/D，y=-(a₁c₂-a₂c₁)/D。也可用两点式构造直线再求交。这是所有几何求交问题（线段相交、圆与线、半平面交）的基础。

## Why · 为什么

### 直觉 · Intuition

两直线的方程是两个线性约束，交点就是同时满足两个方程的点。Cramer 法则把解写成行列式比值：分母是法向量 (a₁,b₁),(a₂,b₂) 的叉积（为 0 说明两法向量共线即两线平行），分子是把常数项替换到对应列后得到的行列式。几何上，法向量叉积=0 意味着两直线方向相同。

### 原理 · Principle

① 直线标准式 ax+by+c=0，法向量 (a,b)。② 相交判定：det=a₁b₂-a₂b₁≠0。③ 交点：x=-(c₁b₂-c₂b₁)/det, y=-(a₁c₂-a₂c₁)/det（Cramer 法则）。④ 平行判定：det=0；重合判定：det=0 且 a₁c₂-a₂c₁=0 且 b₁c₂-b₂c₁=0（系数成比例）。⑤ 浮点处理：用 EPS 比较 |det|<EPS。⑥ 由两点 p,q 构直线：a=q.y-p.y, b=p.x-q.x, c=-a·p.x-b·p.y。

### 历史 · History

Cramer 法则由 Gabriel Cramer（1750）提出，是线性方程组的标准解法之一。直线求交是计算几何最基础运算，CP-Algorithms 的 'Intersection Point of Lines' 是经典参考实现（源自 e-maxx.ru）。OI Wiki 的 2D 几何基础中也将其作为核心原语。

## How · 实现

### 伪代码

```python
# 直线 ax+by+c=0
def line_intersect(l1, l2):
  a1,b1,c1 = l1; a2,b2,c2 = l2
  det = a1*b2 - a2*b1
  if abs(det) < EPS: return PARALLEL   # 是否重合再查
  x = -(c1*b2 - c2*b1)/det
  y = -(a1*c2 - a2*c1)/det
  return (x,y)

def line_from_two_points(p, q):
  a = q.y - p.y; b = p.x - q.x; c = -a*p.x - b*p.y
  return (a,b,c)
```

### Python 实现

```python
EPS = 1e-9


def cross(ax, ay, bx, by):
    return ax * by - ay * bx


def line_from_points(p, q):
    """过 p,q 两点的直线 ax+by+c=0."""
    a = q[1] - p[1]
    b = p[0] - q[0]
    c = -a * p[0] - b * p[1]
    return (a, b, c)


def line_intersect(l1, l2):
    """两直线 ax+by+c=0 求交.
    返回: ('point', x, y) 交点; ('parallel',) 平行; ('same',) 重合."""
    a1, b1, c1 = l1
    a2, b2, c2 = l2
    det = cross(a1, b1, a2, b2)
    if abs(det) < EPS:
        # 检查是否重合: 系数成比例
        if abs(cross(a1, c1, a2, c2)) < EPS and abs(cross(b1, c1, b2, c2)) < EPS:
            return ('same',)
        return ('parallel',)
    x = -(c1 * b2 - c2 * b1) / det
    y = -(a1 * c2 - a2 * c1) / det
    return ('point', x, y)


def point_on_line(l, p):
    """点 p 是否在直线 l 上 (浮点判断)."""
    a, b, c = l
    return abs(a * p[0] + b * p[1] + c) < EPS


if __name__ == "__main__":
    # y=x 与 y=-x => 交点 (0,0)
    l1 = (1, -1, 0)   # x - y = 0
    l2 = (1, 1, 0)    # x + y = 0
    r = line_intersect(l1, l2)
    assert r[0] == 'point' and abs(r[1]) < 1e-9 and abs(r[2]) < 1e-9

    # y=2x+1 与 y=3x-2
    # 2x - y + 1 = 0 ; 3x - y - 2 = 0
    l3 = (2, -1, 1)
    l4 = (3, -1, -2)
    r = line_intersect(l3, l4)
    # 解: x=3, y=7
    assert abs(r[1] - 3) < 1e-9 and abs(r[2] - 7) < 1e-9
    # 交点必须同时满足两方程
    assert point_on_line(l3, (r[1], r[2]))
    assert point_on_line(l4, (r[1], r[2]))

    # 平行: x-y=0 与 x-y=5
    assert line_intersect((1, -1, 0), (1, -1, 5))[0] == 'parallel'
    # 重合: x-y=0 与 2x-2y=0
    assert line_intersect((1, -1, 0), (2, -2, 0))[0] == 'same'

    # 两点式构造: (0,0)-(1,1) 与 (0,2)-(2,0) 交于 (1,1)
    la = line_from_points((0, 0), (1, 1))
    lb = line_from_points((0, 2), (2, 0))
    r = line_intersect(la, lb)
    assert abs(r[1] - 1) < 1e-9 and abs(r[2] - 1) < 1e-9

    # 随机交叉验证: 生成两对随机点 -> 两点式直线 -> 数值核对交点
    import random
    random.seed(3)
    for _ in range(200):
        p1 = (random.uniform(-10, 10), random.uniform(-10, 10))
        q1 = (random.uniform(-10, 10), random.uniform(-10, 10))
        p2 = (random.uniform(-10, 10), random.uniform(-10, 10))
        q2 = (random.uniform(-10, 10), random.uniform(-10, 10))
        # 跳过退化
        if (p1[0] - q1[0]) ** 2 + (p1[1] - q1[1]) ** 2 < 1e-12:
            continue
        if (p2[0] - q2[0]) ** 2 + (p2[1] - q2[1]) ** 2 < 1e-12:
            continue
        l1 = line_from_points(p1, q1)
        l2 = line_from_points(p2, q2)
        r = line_intersect(l1, l2)
        if r[0] == 'point':
            assert point_on_line(l1, (r[1], r[2])), (p1, q1, l1, r)
            assert point_on_line(l2, (r[1], r[2])), (p2, q2, l2, r)
        else:
            # 平行: 方向向量叉积为 0
            d1 = (q1[0] - p1[0], q1[1] - p1[1])
            d2 = (q2[0] - p2[0], q2[1] - p2[1])
            assert abs(cross(*d1, *d2)) < 1e-6
    print("All tests passed.")
```

**PyPy 提示**: 浮点求交注意 EPS 选择（1e-9 对 double 安全）。大规模求交避免创建元组过多可内联。整数直线可全程整数运算再最后除，减少误差。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(1) |
| 空间 | O(1) |

### 局限

浮点误差：平行判定依赖 EPS 阈值，EPS 过小会把几乎平行误判为相交。垂直直线在斜率表示法（y=kx+b）下 k 无穷大，务必用 ax+by+c=0 一般式。两点重合会退化为无效直线。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| CSES | 2190 | 3 | Line Segment Intersection：线段相交（内部用直线交点+线段含点判断，CP-Alg 例题） | [https://cses.fi/problemset/task/2190](https://cses.fi/problemset/task/2190) |
| Luogu | P5490 | 3 | 【模板】扫描线：矩形边求交/线段树维护，直线求交是其子原语 | [https://www.luogu.com.cn/problem/P5490](https://www.luogu.com.cn/problem/P5490) |
| UVA | 191 | 3 | Intersection：线段与矩形相交判定，内部用直线交点原语（经典 UVA 题） | [https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=127](https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=127) |

## Pitfalls · 易错点

- 平行与重合混为一谈：先判 det，再判 c 比例
- 用 y=kx+b 表示垂直直线会崩，改用一般式
- EPS 阈值与数据范围不匹配（坐标 1e9 时用 1e-12 会误判）
- 由两点构直线公式 a=q.y-p.y, b=p.x-q.x 别写反
- 交点代入验证时可容忍 eps 误差，别用 == 判浮点相等

## Sources · 信源

- CP-Algorithms ✓ [https://cp-algorithms.com/geometry/lines-intersection.html](https://cp-algorithms.com/geometry/lines-intersection.html)
- OI Wiki ✓ [https://oi-wiki.org/geometry/2d/](https://oi-wiki.org/geometry/2d/)
