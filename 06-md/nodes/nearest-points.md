---
id: nearest-points
name: 最近点对
group: G-D-2
stage: advanced
priority: P1
depth_tier: standard
---

# 最近点对

> 分治 O(nlogn) 求平面最近点对，合并时按扫描线对检查

<!-- 元信息: id=nearest-points · group=G-D-2 · stage=advanced · priority=P1 · depth_tier=standard -->

## What · 是什么

给定平面上 n 个点，求其中欧几里得距离最近的一对点。朴素两两枚举 O(n²)。分治算法 O(n log n)：按 x 坐标排序并从中点切分，递归求左右两半各自最近距离 h=min(h1,h2)，然后只需检查横坐标距分割线 < h 的『条带』内的点——条带内按 y 排序，对每个点只检查其后 y 差 < h 的常数个点（最多 7 个）。Shamos-Hoey（1975）提出，Preparata & Shamos 证明其在决策树模型下最优。另有 Rabin 的随机化线性期望算法（网格分桶）。

## Why · 为什么

### 直觉 · Intuition

把问题切成两半递归解决，合并时只需要关心『一对点分居左右』的情况。关键洞察：如果左右各自最近距离已是 h，那么跨界的更近点对，其两点的 x 坐标差必须 < h（否则距离已 ≥ h），y 坐标差也 < h。于是跨界点对全部落在分割线附近 2h×h 的矩形内。而这个矩形内『不能塞太多点』：左右各 h×h 方块里任意两点距离 ≥ h，把方块四等分成边长 h/2 的小方格，每格至多 1 个点 → 每方块至多 4 个点 → 检查的点数 ≤ 8（实际 ≤7）。这就是分治合并能 O(n) 完成的根本原因。

### 原理 · Principle

① 按 (x,y) 排序，取中点 m=⌊n/2⌋，A₁=前一半(含中点)，A₂=后一半。② 递归 T(n)=2T(n/2)+O(n)=O(n log n)。③ 合并：B={p: |x_p - x_mid| < h}；将 B 按 y 排序（归并融入递归保持 O(n)），对每个点只检查它前面 y 差 < h 的连续点（C(p_i) 至多 7 个）。④ 常数界证明：2h×h 矩形被分割线分成两个 h×h 方块；每个方块内两点距离 ≥ h；方块四等分，每 h/2×h/2 小格至多 1 点，故方块内 ≤4 点，矩形内 ≤8 点，C(p_i) ≤7。⑤ 边界条件 r-l≤3 用暴力。⑥ 整点坐标可全程用距离平方避免 sqrt。⑦ 若存在重合点则答案 0。

### 历史 · History

Shamos 与 Hoey 于 1975 年提出 O(n log n) 分治算法，其最优性由 Preparata 与 Shamos 证明（决策树模型）。Rabin 1976 年提出随机化网格算法（期望线性）。最近点对是计算几何『分治范式』的经典案例，CPH ch29 与 CP-Algorithms 均收录，是 ICPC/CCPC 高频考题。

## How · 实现

### 伪代码

```python
# 按 x 排序, 递归 rec(l,r):
def rec(l, r):
  if r-l <= 3: 暴力更新最近对; 按y排序; return
  m = (l+r)//2; midx = x[m]
  rec(l,m); rec(m,r)
  merge 两半按y (归并)
  for i in [l..r):
    if |x[i]-midx| < h:
      for j in strip, j<i, y差<h:
        update(pair)
  return 按y排序后的数组
```

### Python 实现

```python
import math


def closest_pair(points):
    """分治求最近点对. points: [(x,y)] 浮点/整数.
    返回 (dist, (i, j)) 距离与两个点的原始索引."""
    n = len(points)
    pts = list(points)
    order = list(range(n))
    pts = sorted(zip(pts, order), key=lambda t: (t[0][0], t[0][1]))
    best = float('inf')
    best_pair = None

    def dist2(p, q):
        return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2

    def upd(p, q):
        nonlocal best, best_pair
        d = dist2(p[0], q[0])
        if d < best:
            best = d
            best_pair = (p[1], q[1])

    arr = pts
    buf = [None] * n

    def rec(l, r):
        """处理 arr[l:r), 返回后该段按 y 排序."""
        nonlocal best
        if r - l <= 3:
            for i in range(l, r):
                for j in range(i + 1, r):
                    upd(arr[i], arr[j])
            arr[l:r] = sorted(arr[l:r], key=lambda t: t[0][1])
            return
        m = (l + r) // 2
        midx = arr[m][0][0]
        rec(l, m)
        rec(m, r)
        # 归并按 y
        i, j, k = l, m, l
        while i < m and j < r:
            if arr[i][0][1] <= arr[j][0][1]:
                buf[k] = arr[i]; i += 1
            else:
                buf[k] = arr[j]; j += 1
            k += 1
        while i < m:
            buf[k] = arr[i]; i += 1; k += 1
        while j < r:
            buf[k] = arr[j]; j += 1; k += 1
        arr[l:r] = buf[l:r]
        # 条带检查
        strip = []
        for k in range(l, r):
            if abs(arr[k][0][0] - midx) < best ** 0.5:
                strip.append(arr[k])
        for a in range(len(strip)):
            b = a - 1
            while b >= 0 and strip[a][0][1] - strip[b][0][1] < best ** 0.5:
                upd(strip[a], strip[b])
                b -= 1

    rec(0, n)
    return math.sqrt(best), best_pair


def brute(points):
    n = len(points)
    bd = float('inf'); bp = None
    for i in range(n):
        for j in range(i + 1, n):
            d = (points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2
            if d < bd:
                bd = d; bp = (i, j)
    return math.sqrt(bd), bp


if __name__ == "__main__":
    # 已知: 最近距离 1 (点(0,0)-(1,0))
    pts = [(0, 0), (1, 0), (10, 10), (11, 10), (5, 7)]
    d, p = closest_pair(pts)
    assert abs(d - 1.0) < 1e-9, d
    # 重合点 -> 0
    pts2 = [(3, 3), (3, 3), (9, 9)]
    d, _ = closest_pair(pts2)
    assert abs(d - 0.0) < 1e-9
    # 边界: 2 个点
    pts3 = [(0, 0), (4, 3)]
    d, _ = closest_pair(pts3)
    assert abs(d - 5.0) < 1e-9

    # 随机交叉验证
    import random
    random.seed(2026)
    for _ in range(200):
        n = random.randint(2, 60)
        pts = [(random.randint(-100, 100), random.randint(-100, 100)) for _ in range(n)]
        d1, p1 = closest_pair(pts)
        d2, p2 = brute(pts)
        assert abs(d1 - d2) < 1e-7, (n, d1, d2)
        # 校验返回的点对确实距离 d1
        i, j = p1
        assert abs(((pts[i][0] - pts[j][0]) ** 2 + (pts[i][1] - pts[j][1]) ** 2) ** 0.5 - d1) < 1e-9
    print("All tests passed.")
```

**PyPy 提示**: 整点坐标可全程用距离平方比较避免 sqrt（合并判定用 < best 而非 < sqrt(best)，条带宽度也用 best 平方比）。递归按 y 归并避免每次 sort 使总复杂度退化为 O(n log²n)。Python 递归深度限制注意 setrecursionlimit。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n log n)（分治）；随机化网格算法期望 O(n) |
| 空间 | O(n) |

### 局限

合并阶段若每次调用都对条带单独 sort 会退化为 O(n log²n)。浮点坐标需注意平方误差。点坐标同 x 很多时（全部竖直排列）条带仍受常数界保护。重合点需先特殊处理返回 0。大数据量用距离平方优化。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| UVA | 10245 | 3 | The Closest Pair Problem：分治最近点对经典模板（CP-Alg 例题，低难度） | [https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=24&page=show_problem&problem=282](https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=24&page=show_problem&problem=282) |
| SPOJ | CLOPPAIR | 3 | Closest Point Pair：求最近点对的点编号（OI Wiki/CP-Alg 例题） | [https://www.spoj.com/problems/CLOPPAIR/](https://www.spoj.com/problems/CLOPPAIR/) |
| SPOJ | CLOSEST | 4 | Closest Triple：最小周长三角形（最近点对推广，OI Wiki 例题） | [https://www.spoj.com/problems/CLOSEST/](https://www.spoj.com/problems/CLOSEST/) |

## Pitfalls · 易错点

- 合并时条带检查忘记按 y 排序就遍历，退化为 O(n²)
- 用 x 坐标绝对差 < h 过滤条带，但 h 中途更新后要用最新 h 重新过滤
- 条带内检查方向：只查 y 小于当前点的（避免重复配对）
- 按 y 归并是必须的，否则每层 sort 复杂度错
- 递归终止条件 r-l≤3 用暴力，别在 0/1 点集上做跨立检查
- 浮点 sqrt 高频调用慢；整点用平方比较
- 返回的点对索引要映射回原始输入顺序（排序后索引偏移）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/geometry/nearest-points/](https://oi-wiki.org/geometry/nearest-points/)
- CP-Algorithms ✓ [https://cp-algorithms.com/geometry/nearest_points.html](https://cp-algorithms.com/geometry/nearest_points.html)
- 书籍 ✓ `CPH ch29 Geometry (p291-304)`
