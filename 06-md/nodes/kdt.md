---
id: kdt
name: K-D Tree
group: G-D-6
stage: advanced
priority: P2
depth_tier: standard
---

# K-D Tree

> k维空间分块树，轮流按维度切分+中位数建树，处理最近邻与矩形查询

<!-- 元信息: id=kdt · group=G-D-6 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

K-D Tree（k-Dimension Tree）是一种高维空间数据结构，把 k 维点集组织成二叉搜索树：每个节点代表一个点，其子树中所有点都在该点所分割出的一个 k 维超长方体（bounding box）内。建树时轮流选择维度、用该维中位数切分（配合 nth_element 均摊 O(n)），保证树高 O(log n)。可高效处理两类查询：矩形范围聚合（查询复杂度 O(n^{1-1/k})，二维时 O(√n)）与最近邻/第 k 远邻域查询（用子树包围盒与已得答案做剪枝的启发式搜索）。竞赛中一般 k=2。

## Why · 为什么

### 直觉 · Intuition

把平面『一块块切』：每次按 x 或 y 中位数把当前点集切成两半，让每棵子树的空间范围被矩形框住。查矩形时若子树矩形与询问矩形无交就整棵剪掉，完全包含就返回整棵聚合值，部分相交才递归——大多数子树被 O(√n) 个『边界矩形』限住，所以远快于 O(n)。

### 原理 · Principle

建树复杂度：轮流维度 + nth_element 取中位数，T(n)=2T(n/2)+O(n)=O(n log n)。矩形查询递归式 T(n)=2^{k-1}T(n/2^k)+O(1)，主定理得 O(n^{1-1/k})（二维 T(n)=2T(n/4)+O(1)=O(√n)）。最近邻用估价函数剪枝：若查询点到子树矩形的最远/最近距离无法优于当前答案则剪枝；最坏仍 O(n)（OI Wiki 明确警告），但实践远快。插入删除可用根号重构（每 B 次插入重建）或二进制分组，均摊 O(√(n log n)) 修改 + O(√(n log n)+n^{1-1/k}) 查询。

### 历史 · History

K-D Tree 由 Jon Louis Bentley 于 1975 年提出（Multidimensional binary search trees used for associative searching），是经典的多维检索结构。OI Wiki 详细介绍了建树、矩形查询、邻域查询（P1429 最近点对、CQOI2016 K 远点对、P4148 简单题）、根号重构与二进制分组维护动态点集。常用于 KD 树解决平面最近点对/矩形和等问题。

## How · 实现

### 伪代码

```python
# 建树
def build(l, r, depth):
  if l > r: return None
  axis = depth % k
  按 axis 维取中位数 -> mid (用 nth_element)
  node = points[mid]
  node.l = build(l, mid-1, depth+1)
  node.r = build(mid+1, r, depth+1)
  维护子树包围盒 min[axis], max[axis]
  return node

# 最近邻查询 (启发式剪枝)
def nearest(q, node):
  best = INF
  def dfs(u):
    nonlocal best
    if not u: return
    d = dist(q, u.point)
    if d < best: best = d
    # 到两个子树的包围盒距离，先搜近的
    dl = box_dist(q, u.l.box); dr = box_dist(q, u.r.box)
    if dl < dr:
      若 dl < best: dfs(u.l)
      若 dr < best: dfs(u.r)
    else:
      若 dr < best: dfs(u.r)
      若 dl < best: dfs(u.l)
  dfs(root)
  return best
```

### Python 实现

```python
import math
import random


class Node:
    __slots__ = ("pt", "left", "right", "box")

    def __init__(self, pt):
        self.pt = pt
        self.left = None
        self.right = None
        self.box = None  # (minx, miny, maxx, maxy)


def build_kdt(points, depth=0):
    """构建 2-D Tree。points: [(x, y), ...]"""
    if not points:
        return None
    axis = depth % 2
    points = sorted(points, key=lambda p: p[axis])
    mid = len(points) // 2
    node = Node(points[mid])
    node.left = build_kdt(points[:mid], depth + 1)
    node.right = build_kdt(points[mid + 1:], depth + 1)
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    node.box = (min(xs), min(ys), max(xs), max(ys))
    return node


def box_dist(q, box):
    """查询点到包围盒的最近距离平方。"""
    if box is None:
        return float("inf")
    x, y = q
    minx, miny, maxx, maxy = box
    dx = 0 if minx <= x <= maxx else min(abs(x - minx), abs(x - maxx))
    dy = 0 if miny <= y <= maxy else min(abs(y - miny), abs(y - maxy))
    return dx * dx + dy * dy


class KDT:
    def __init__(self, points):
        self.root = build_kdt(points)

    def nearest(self, q):
        """返回到 q 最近点的欧氏距离（非自身时需调用方排除）"""
        best = [float("inf")]

        def dfs(u):
            if u is None:
                return
            d = (q[0] - u.pt[0]) ** 2 + (q[1] - u.pt[1]) ** 2
            if d < best[0]:
                best[0] = d
            dl = box_dist(q, u.left.box if u.left else None)
            dr = box_dist(q, u.right.box if u.right else None)
            if dl < dr:
                if dl < best[0]:
                    dfs(u.left)
                if dr < best[0]:
                    dfs(u.right)
            else:
                if dr < best[0]:
                    dfs(u.right)
                if dl < best[0]:
                    dfs(u.left)

        dfs(self.root)
        return math.sqrt(best[0])


def brute_nearest(points, q):
    return min(math.hypot(q[0] - x, q[1] - y) for x, y in points)


if __name__ == "__main__":
    random.seed(9)
    for trial in range(50):
        n = random.randint(1, 40)
        pts = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(n)]
        kd = KDT(pts)
        for _ in range(20):
            q = (random.randint(0, 100), random.randint(0, 100))
            got = kd.nearest(q)
            exp = brute_nearest(pts, q)
            assert abs(got - exp) < 1e-9, (pts, q, got, exp)
    print("kdt 自测通过：50 组随机点集最近邻查询与暴力一致")

```

**PyPy 提示**: 构建时每次排序是 O(n log n) 建树（简单实现）；要严格 O(n log n) 需 nth_element，Python 可用 statistics.median + partition 手写或直接排序（竞赛 n≤2e5 仍可）。递归深度 O(log n) 安全。最近邻剪枝对随机数据快，但最坏 O(n)，注意用 box_dist 剪枝。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 建树 O(n log n)；矩形查询 O(n^{1-1/k})（二维 O(√n)）；最近邻平均快、最坏 O(n) |
| 空间 | O(n) |

### 局限

最近邻最坏复杂度 O(n)（OI Wiki 警告，属于『优秀骗分』）；维度高时 k 指数恶化（n 需远大于 2^k）。Python 递归建树+剪枝常数较大，n=2e5 可能偏慢。动态插入删除需根号重构/二进制分组维护。对矩形和若要求严格复杂度，2D 可考虑离线 CDQ。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P4148 | 6 | 简单题：20M 内存卡树套树+强制在线，只能 K-D Tree 二进制分组动态维护（OI Wiki 例题） | [https://www.luogu.com.cn/problem/P4148](https://www.luogu.com.cn/problem/P4148) |
| Luogu | P1429 | 5 | 平面最近点对（加强版）：K-D Tree 最近邻剪枝求最近点对（OI Wiki 例题） | [https://www.luogu.com.cn/problem/P1429](https://www.luogu.com.cn/problem/P1429) |
| LOJ | 2043 | 6 | CQOI2016 K 远点对：小根堆维护前 K 远距离+最远距离估价函数剪枝（OI Wiki 例题） | [https://loj.ac/problem/2043](https://loj.ac/problem/2043) |
| Luogu | P4169 | 6 | 天使玩偶/SJY摆棋子：动态 K-D Tree 最近邻（OI Wiki 习题） | [https://www.luogu.com.cn/problem/P4169](https://www.luogu.com.cn/problem/P4169) |

## Pitfalls · 易错点

- 最近邻查询时同一结点自身距离为 0，求最近点对需排除自身
- box_dist 需在 [minx,maxx] 内为 0，跨界才取最近边距离；写错会漏剪枝或剪错
- 建树选择维度需轮流（depth%k），否则退化
- nth_element 位置在 mid，左右区间要排除 mid 本身
- 矩形查询需同时维护包围盒与子树聚合值，先判完全包含/无交再递归
- 最坏复杂度 O(n)，别在严格卡常题里当唯一解法

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/kdt/](https://oi-wiki.org/ds/kdt/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/kdt.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/kdt.md)
