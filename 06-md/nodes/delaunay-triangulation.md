---
id: delaunay-triangulation
name: Delaunay 三角剖分
group: G-D-2
stage: frontier
priority: P3
depth_tier: brief
---

# Delaunay 三角剖分

> 满足空圆性质的三角剖分，对偶为 Voronoi 图

<!-- 元信息: id=delaunay-triangulation · group=G-D-2 · stage=frontier · priority=P3 · depth_tier=brief -->

## What · 是什么

Delaunay 三角剖分（DT）是给定平面点集 P 的一种特殊三角剖分，满足空圆性质：每个三角形的外接圆内部不含任何其他点（点可在外接圆边界上，即退化情形四点共圆）。若点集中任意四点不共圆，DT 唯一。性质：① 最大化最小角（所有三角剖分中最接近正则化的）；② 最小欧氏生成树是 DT 边的子集；③ 对偶于 Voronoi 图（互为对偶图，可 O(n) 互相转换）；④ 最外边界是凸包；⑤ 局部修改只影响邻近三角形。构造：Guibas-Stolfi 分治 O(n log n)（quad-edge 数据结构）、Boyer-Watson 增量法 O(n log n) 期望、随机增量法。应用：最近邻查询、网格生成、Voronoi 图、最小生成树、插值、碰撞检测。

## Why · 为什么

### 直觉 · Intuition

三角形要『肥』不要『瘦』：瘦长三角形的内角很小，数值不稳定。Delaunay 用空圆准则保证每个三角形尽量饱满——外接圆里没有别的点，意味着没有点能『抢』走这个三角形的区域。空圆性质局部可检验（四点共圆判定），于是可以用翻转对角线（edge flip）把非 Delaunay 局部逐步修正成 Delaunay。对偶视角：每个 Delaunay 三角形对应 Voronoi 图的一个顶点（外接圆圆心），共享边对应相邻 Voronoi 单元之间的边。

### 原理 · Principle

① 空圆判定 inCircle(a,b,c,d)：用 4×4 行列式 det(x,y,x²+y²) 判定 d 是否在 abc 外接圆内（带符号）。② 分治（Guibas-Stolfi）：按 x 排序，递归剖分左右，合并时从底部 base 边开始，逐个添加跨左右的下一条 LR 边，用 inCircle 检验候选点。③ 增量法（Boyer-Watson）：逐点插入，找包含新点的三角形，删除其公共外接圆含新点的三角形，重连成凸包扇形成新三角形。④ 对偶：Delaunay 边 ⟷ Voronoi 边（垂直平分线段），DT 三角形 ⟷ Voronoi 顶点。⑤ 退化处理：四点共圆时 DT 不唯一，可扰动或指定规则。⑥ quad-edge 数据结构统一表示原边/反向边/对偶边。

### 历史 · History

Delaunay 三角剖分得名于法国数学家 Boris Delaunay（1934），他证明了最大化最小角性质。Voronoi 图更早（Voronoï, 1908；更早还有 Dirichlet 与 Thiessen 的多边形）。Guibas 与 Stolfi 1985 年发表 O(n log n) 分治算法与 quad-edge 结构；Boyer（1977）与 Watson（1981）独立提出增量算法。是计算几何与图形学核心工具。

## How · 实现

### 伪代码

```python
# Boyer-Watson 增量法 (教学简洁版)
def delaunay(points):
  # 用超大包围三角形初始化
  sup = 大三角形包住所有点
  tris = [sup]
  for p in points:
    bad = [t for t in tris if in_circle(p, t)]
    boundary = 所有 bad 三角形的外边界边(只出现一次)
    remove bad from tris
    for e in boundary:
      tris.append((e.a, e.b, p))
  # 删除包含包围三角形顶点的三角形
  return [t for t in tris if not t.uses(super_vertices)]
```

### Python 实现

```python
EPS = 1e-9


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def in_circle(a, b, c, d):
    """d 是否严格在 abc 外接圆内 (精确行列式, 整数点下无精度损失)."""
    ax, ay = a[0] - d[0], a[1] - d[1]
    bx, by = b[0] - d[0], b[1] - d[1]
    cx, cy = c[0] - d[0], c[1] - d[1]
    a2 = ax * ax + ay * ay
    b2 = bx * bx + by * by
    c2 = cx * cx + cy * cy
    det = (ax * (by * c2 - b2 * cy)
           - ay * (bx * c2 - b2 * cx)
           + a2 * (bx * cy - by * cx))
    if cross(a, b, c) > 0:
        return det > 0
    return det < 0


def delaunay_bw(points):
    """Boyer-Watson 增量法 Delaunay 剖分 (浮点).
    返回三角形列表 [(p_i, p_j, p_k)] (点的原始索引).
    用远包围三角形处理; 可能因浮点退化产生少量非 Delaunay, 教学演示足够."""
    pts = list(points)
    n = len(pts)
    if n < 3:
        return []
    # 包围三角形
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    dx = maxx - minx; dy = maxy - miny
    dmax = max(dx, dy)
    midx = (minx + maxx) / 2.0
    midy = (miny + maxy) / 2.0
    sup = [(midx - 20 * dmax, midy - dmax), (midx, midy + 20 * dmax), (midx + 20 * dmax, midy - dmax)]
    sup_idx = [n, n + 1, n + 2]
    allpts = pts + sup
    tris = [tuple(sup_idx)]

    def has_vertex(t, idx):
        return idx in t

    for k, p in enumerate(pts):
        bad = []
        for t in tris:
            if in_circle(allpts[t[0]], allpts[t[1]], allpts[t[2]], p):
                bad.append(t)
        # 边界边 (bad 三角形中出现一次的边)
        from collections import defaultdict
        cnt = defaultdict(int)
        edge_list = []
        for t in bad:
            for e in [(t[0], t[1]), (t[1], t[2]), (t[2], t[0])]:
                e2 = e if e[0] < e[1] else (e[1], e[0])
                cnt[e2] += 1
        for t in bad:
            tris.remove(t)
        boundary = []
        for e, c in cnt.items():
            if c == 1:
                boundary.append(e)
        for (a, b) in boundary:
            tris.append((a, b, k))
    # 去除含超级顶点的三角形
    tris = [t for t in tris if not (has_vertex(t, n) or has_vertex(t, n + 1) or has_vertex(t, n + 2))]
    return tris


def validate_empty_circle(tris, points):
    """验证每个三角形的外接圆不包含其他点 (退化容忍)."""
    for t in tris:
        a, b, c = points[t[0]], points[t[1]], points[t[2]]
        for k, p in enumerate(points):
            if k in t:
                continue
            if in_circle(a, b, c, p):
                return False
    return True


def hull_boundary_size(ps):
    """凸包边界上的点数 (含共线边界点; 三角剖分数公式用此值)."""
    pts = sorted(set(ps))
    if len(pts) <= 2:
        return len(pts)
    def build(poly):
        if len(poly) <= 2:
            return poly
        h = []
        for p in poly:
            while len(h) >= 2 and cross(h[-2], h[-1], p) < 0:
                h.pop()
            h.append(p)
        return h
    lower = build(pts)
    upper = build(pts[::-1])
    return len(set(lower[:-1] + upper[:-1]))


if __name__ == "__main__":
    import random
    random.seed(8)
    # 规则网格 (四点共圆退化 -> 可能不唯一, 只验证数量与覆盖)
    pts = [(0, 0), (1, 0), (0, 1), (1, 1)]
    tris = delaunay_bw(pts)
    assert len(tris) >= 1

    # 随机无共圆点集: 验证空圆性质 + 欧拉计数 (容差 1, 浮点退化)
    for trial in range(30):
        n = random.randint(4, 20)
        ps = set()
        while len(ps) < n:
            ps.add((random.randint(0, 100), random.randint(0, 100)))
        ps = list(ps)
        tris = delaunay_bw(ps)
        assert abs(len(tris) - (2 * len(ps) - 2 - hull_boundary_size(ps))) <= 1, \
            (len(ps), len(tris), hull_boundary_size(ps))
        assert validate_empty_circle(tris, ps), "empty circle violated"
    print("All tests passed.")



```

**PyPy 提示**: in_circle 行列式用整数可精确判定（无共圆时）；浮点需 eps。增量法整体期望 O(n log n)，但最坏 O(n²)（全共圆时）。大数据量需 quad-edge 结构，Python 实现偏慢，竞赛较少直接用完整 DT。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | Guibas-Stolfi 分治 O(n log n)；Boyer-Watson 增量期望 O(n log n)（最坏 O(n²)） |
| 空间 | O(n) |

### 局限

四点共圆退化导致 DT 不唯一，需扰动或容错规则。共线点集不存在 DT（退化）。增量法对浮点精度敏感，大坐标需 __int128 或高精行列式。Python 完整实现 quad-edge 复杂且慢，竞赛多为理论/少量点。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| TIMUS | 1504 | 7 | Good Manners：Delaunay/最近邻几何应用（CP-Alg 例题） | [https://acm.timus.ru/problem.aspx?space=1&num=1504](https://acm.timus.ru/problem.aspx?space=1&num=1504) |
| TIMUS | 1520 | 7 | Empire Strikes Back：Voronoi/Delaunay 对偶应用（CP-Alg 例题） | [https://acm.timus.ru/problem.aspx?space=1&num=1520](https://acm.timus.ru/problem.aspx?space=1&num=1520) |
| Codeforces | 933C | 6 | A Colorful Prospect：圆/区域划分（Voronoi 式划分思路，CP-Alg 圆交例题同源） | [https://codeforces.com/problemset/problem/933/C](https://codeforces.com/problemset/problem/933/C) |

## Pitfalls · 易错点

- in_circle 行列式的符号约定与三角形方向（逆/顺时针）有关，必须一致
- 四点共圆退化：不加处理会生成重叠三角形，需扰动或删除冗余边
- 包围三角形选得太小会漏点；太大则数值误差增大
- 增量法删除 bad 三角形时边界边收集错误（共享边计数必须=1）
- 共线点集无 DT，需先判退化
- 验证空圆性质时跳过自身三角形顶点，否则永远失败

## Sources · 信源

- CP-Algorithms ✓ [https://cp-algorithms.com/geometry/delaunay.html](https://cp-algorithms.com/geometry/delaunay.html)
- 书籍 ✓ `CPH ch29 Geometry (p291-304)`
