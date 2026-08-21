---
id: triangulation
name: 三角剖分
group: G-D-2
stage: advanced
priority: P2
depth_tier: standard
---

# 三角剖分

> 将平面点集细分为三角形，常用耳切与对偶图

<!-- 元信息: id=triangulation · group=G-D-2 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

三角剖分（Triangulation）是把平面点集（或多边形/平面区域）细分为一组互不重叠的三角形，覆盖整个点集凸包（或多边形内部），且所有点都作为三角形顶点。多边形三角剖分：顶点数 n 的多边形恰有 n-2 个三角形、n-3 条对角线；点集三角剖分：含 n 个点（其中 h 个凸包点）有 2n-2-h 个三角形。构造方法：耳切法（Ear Clipping，O(n²)，适合简单多边形）、三角剖分存在无限多种；『最优』剖分（最大化最小角、最小化总边长等）需用 Delaunay 或贪婪启发。应用：3D 渲染网格化、有限元、多边形面积/重心分解、单调多边形分解。

## Why · 为什么

### 直觉 · Intuition

三角形的性质最好：面积公式简单、点定位容易、任意多边形都能拆成三角形拼接。耳切法直观：多边形顶点中『耳朵』（相邻两边构成三角形的第三点内部没有其他顶点）逐个切掉，每次去掉一个耳朵减少一个顶点，直到剩一个三角形。为什么一定存在耳朵？简单多边形的任何三角剖分必有至少两个耳朵（二耳定理）。点集剖分的难点在于保证三角形互不重叠、无点落在三角形内部。

### 原理 · Principle

① 二耳定理：任何简单多边形（n≥4）至少有两个不重叠的耳朵（顶点 v 是耳朵当且仅当由 v 及其前后顶点构成的三角形内不包含其他多边形顶点，且 v 为凸顶点）。② 耳切法：找凸顶点→验证为空三角形（内部无点）→切掉→更新邻域凸性，O(n²)（凸顶点检测+包含测试），凸多边形 O(n)。③ 三角剖分数：多边形 C(n-2)（卡特兰），任意剖分 n-2 个三角形。④ 点集剖分：先求凸包，内部点逐个插入（增量法）或分治（Guibas-Stolfi），保证无重叠。⑤ 对偶图：三角形为节点、共享边为连边，构成树（对凸多边形）。⑥ Delaunay 是最小角最大化特例。

### 历史 · History

三角剖分是计算几何核心主题，源于地形建模（DTM）与网格生成。凸多边形三角剖分计数由 Euler 与 Segner（18 世纪）研究（卡特兰数）。Guibas-Stolfi 1985 年给出 Delaunay 分治 O(n log n) 算法。二耳定理是耳切法的基础，Poly2Tri 等库广泛采用。CPH ch29 将其列为计算几何基本主题。

## How · 实现

### 伪代码

```python
# 耳切法剖分简单多边形
def triangulate(poly):
  if len < 3: return []
  tris = []
  while len(poly) > 3:
    for i in range(len(poly)):
      if is_ear(poly, i):
        prev, cur, nxt = neighbors
        tris.append((prev,cur,nxt))
        poly.remove(cur)
        break
  tris.append((poly[0],poly[1],poly[2]))
  return tris

def is_ear(poly, i):
  cur = poly[i]; prev=..., nxt=...
  if not is_convex(prev,cur,nxt): return False
  for p in poly(except these 3):
    if point_in_triangle(p, prev,cur,nxt): return False
  return True
```

### Python 实现

```python
def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def point_in_tri(p, a, b, c):
    """点 p 是否在三角形 abc 内部或边上 (边界归为外部更稳妥? 此处含边)."""
    d1 = cross(a, b, p)
    d2 = cross(b, c, p)
    d3 = cross(c, a, p)
    has_neg = d1 < -1e-12 or d2 < -1e-12 or d3 < -1e-12
    has_pos = d1 > 1e-12 or d2 > 1e-12 or d3 > 1e-12
    return not (has_neg and has_pos)


def is_ear(poly, i):
    n = len(poly)
    prev = poly[(i - 1) % n]
    cur = poly[i]
    nxt = poly[(i + 1) % n]
    # 凸顶点检查 (假设多边形逆时针)
    if cross(prev, cur, nxt) <= 0:
        return False
    # 三角形内部无其他顶点
    for j, p in enumerate(poly):
        if p in (prev, cur, nxt):
            continue
        # 严格内部 (排除边上重叠)
        if point_in_tri(p, prev, cur, nxt) and \
           abs(cross(prev, cur, p)) > 1e-12 and \
           abs(cross(cur, nxt, p)) > 1e-12 and \
           abs(cross(nxt, prev, p)) > 1e-12:
            return False
    return True


def ear_clipping(poly):
    """耳切法: 简单多边形 -> 三角形列表 (逆时针)."""
    poly = list(poly)
    tris = []
    guard = 0
    while len(poly) > 3 and guard < 1000:
        guard += 1
        clipped = False
        for i in range(len(poly)):
            if is_ear(poly, i):
                prev = poly[(i - 1) % len(poly)]
                cur = poly[i]
                nxt = poly[(i + 1) % len(poly)]
                tris.append((prev, cur, nxt))
                poly.pop(i)
                clipped = True
                break
        if not clipped:
            break  # 数值问题或退化
    if len(poly) == 3:
        tris.append((poly[0], poly[1], poly[2]))
    return tris


def area(poly):
    s = 0.0
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return s / 2.0


def tri_area(a, b, c):
    return abs(cross(a, b, c)) / 2.0


if __name__ == "__main__":
    # 凸多边形: 正方形
    sq = [(0, 0), (2, 0), (2, 2), (0, 2)]
    tris = ear_clipping(sq)
    assert len(tris) == 2
    assert abs(sum(tri_area(*t) for t in tris) - 4.0) < 1e-9

    # L 形多边形 (凹多边形): (0,0),(3,0),(3,1),(1,1),(1,3),(0,3)
    L = [(0, 0), (3, 0), (3, 1), (1, 1), (1, 3), (0, 3)]
    tris = ear_clipping(L)
    assert len(tris) == len(L) - 2
    total = sum(tri_area(*t) for t in tris)
    assert abs(total - abs(area(L))) < 1e-9, (total, area(L))

    # 五边形 (凸): 面积核对
    pent = [(0, 0), (4, 0), (5, 3), (2, 5), (0, 3)]
    tris = ear_clipping(pent)
    assert len(tris) == 3
    assert abs(sum(tri_area(*t) for t in tris) - abs(area(pent))) < 1e-9

    # C 形多边形 (严重凹): 面积核对
    c_poly = [(0, 0), (3, 0), (3, 3), (2, 3), (2, 1), (1, 1), (1, 3), (0, 3)]
    tris = ear_clipping(c_poly)
    assert len(tris) == len(c_poly) - 2, len(tris)
    assert abs(sum(tri_area(*t) for t in tris) - abs(area(c_poly))) < 1e-9

    # 三角形本身
    tri = [(0, 0), (1, 0), (0, 1)]
    tris = ear_clipping(tri)
    assert len(tris) == 1
    print("All tests passed.")
```

**PyPy 提示**: 耳切法 O(n²)：顶点多时慢；凸多边形可 O(n)。整数坐标避免浮点；凹点检测用 cross 符号。对浮点坐标，is_ear 的『内部无点』判定用严格不等式防止边界误判。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 耳切法 O(n²)（凸多边形 O(n)）；点集分治剖分 O(n log n) |
| 空间 | O(n) |

### 局限

耳切法要求简单多边形（无自交、无洞、无重复点），否则行为未定义。浮点坐标下共线点/近共线点会导致耳朵检测不稳定。点集三角剖分（非 Delaunay）的最优性定义需额外准则。退化的重复点需预处理。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| UVA | 1331 | 5 | Minimax Triangulation：多边形三角剖分 DP（最小化最大三角形面积），三角剖分+区间DP 经典题 | [https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=4077](https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=4077) |
| Luogu | P1856 | 5 | IOI1998 矩形周长 Picture：扫描线几何综合，三角剖分/分解思想的应用场景 | [https://www.luogu.com.cn/problem/P1856](https://www.luogu.com.cn/problem/P1856) |
| UVA | 10387 | 3 | Billiard：几何计算综合（多边形的三角形分解背景） | [https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=10387](https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=10387) |

## Pitfalls · 易错点

- 多边形方向（顺/逆时针）影响 cross 符号，耳切需一致处理
- 凹顶点不能被切（cross<0 不是耳朵）
- 内部包含测试要排除自身三个顶点
- 退化共线点会造出面积 0 三角形，破坏 n-2 计数
- 浮点下『点在三角形边界上』判定需 eps，否则耳朵误判
- 点集剖分要先把凸包点与内部点分离，直接耳切不适用

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/geometry/triangulation/](https://oi-wiki.org/geometry/triangulation/)
- 书籍 ✓ `CPH ch29 Geometry (p291-304)`
