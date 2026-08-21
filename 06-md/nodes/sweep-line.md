---
id: sweep-line
name: 扫描线
group: G-D-2
stage: advanced
priority: P1
depth_tier: standard
---

# 扫描线

> 线扫过平面处理事件，求矩形面积并/周长并/二维数点

<!-- 元信息: id=sweep-line · group=G-D-2 · stage=advanced · priority=P1 · depth_tier=standard -->

## What · 是什么

扫描线（Sweep Line）是一种把二维问题化为一维的通用技巧：让一条线沿某个方向扫过平面，在遇到『事件』（点的进入/离开、线段端点、矩形边）时更新一维数据结构，从而把静态二维问题转换为动态一维问题。经典应用：① 矩形面积并（横边事件+线段树维护覆盖长度）；② 矩形周长并（横纵两个方向各扫一次）；③ 二维数点/离线区间查询（扫一维、树状数组维护另一维）；④ 线段求交、最近点对。复杂度 O((n+m)log n)，是计算几何与数据结构结合的最高频套路之一。

## Why · 为什么

### 直觉 · Intuition

想象一条水平线从下往上掠过平面。矩形在它扫过时『活』一段区间——下边沿使区间进入活跃、上边沿使区间退出。用线段树记录每条竖线切片上『覆盖次数>0』的总长度，乘上扫过的高度差就是该切片面积。这本质上把矩形拆成『覆盖深度函数』随 y 变化，线段树维护深度>0 的宽度。二维数点同理：把每个点变成『在某个 x 时刻加进树状数组』，询问变成两个时刻的差分前缀和。

### 原理 · Principle

① 矩形面积并：对每个矩形下边标 +1、上边标 -1，按 y 排序生成事件；线段树维护区间被覆盖次数 cov 与被覆盖长度 len：若 cov>0 则 len=区间全长，否则 len=左右子 len 之和（无需懒标记下传）。面积=Σ 相邻事件 y 差 × 当前 len。② 二维数点：点(x,y)视为在 x 处 add(y,1)；询问矩形 [x1,x2]×[y1,y2] 差分 f(x2,y1..y2)-f(x1-1,y1..y2)，用树状数组按 x 扫描回答。③ 可差分信息才能扫描+前缀和；不可差分则用 CDQ 分治。④ 线段求交：事件为线段端点/交点，用平衡树维护与扫描线的交点顺序，只检查相邻段（O((n+k)log n)，k 为交点数）。

### 历史 · History

扫描线思想源于计算几何的平面扫描范式，1970 年代 Bentley-Ottmann 用它求线段交点（O((n+k)log n)）奠定地位。矩形面积并是经典应用，出现在 POJ 1151 Atlantis 等早期题目。OI Wiki 的扫描线章节系统地整理了面积并、周长并、二维数点三大应用，是 ICPC/CCPC 高频考点。

## How · 实现

### 伪代码

```python
# 矩形面积并
edges = []
for each rect(x1,y1,x2,y2):
  edges.append((y1, x1, x2, +1))   # 下边
  edges.append((y2, x1, x2, -1))   # 上边
xs = sorted(set of all x1,x2)       # 离散化
sort(edges) by y
build segtree over xs intervals
ans = 0
for i in range(len(edges)):
  ans += (edges[i].y - edges[i-1].y) * segtree.len(covered>0)
  segtree.update(x-range, edges[i].delta)
return ans
```

### Python 实现

```python
class SegTree:
    """覆盖次数 + 覆盖长度 线段树 (区间加, 不递归下传)."""
    def __init__(self, xs):
        self.xs = xs                # 离散化坐标 (升序)
        self.cov = [0] * (4 * len(xs))
        self.len = [0.0] * (4 * len(xs))

    def _update(self, node, l, r, ql, qr, val):
        if qr <= l or r <= ql:
            return
        if ql <= l and r <= qr:
            self.cov[node] += val
        else:
            mid = (l + r) // 2
            self._update(node * 2, l, mid, ql, qr, val)
            self._update(node * 2 + 1, mid, r, ql, qr, val)
        if self.cov[node] > 0:
            self.len[node] = self.xs[r] - self.xs[l]
        elif r - l == 1:
            self.len[node] = 0.0
        else:
            self.len[node] = self.len[node * 2] + self.len[node * 2 + 1]

    def update(self, ql, qr, val):
        """对 [xs[ql], xs[qr]) 区间加 val."""
        self._update(1, 0, len(self.xs) - 1, ql, qr, val)

    def total_len(self):
        return self.len[1]


def union_area(rects):
    """矩形面积并. rects: (x1,y1,x2,y2) 左下右上."""
    xs = sorted(set([x for r in rects for x in (r[0], r[2])]))
    idx = {v: i for i, v in enumerate(xs)}
    events = []
    for x1, y1, x2, y2 in rects:
        events.append((y1, idx[x1], idx[x2], 1))
        events.append((y2, idx[x1], idx[x2], -1))
    events.sort(key=lambda e: e[0])
    seg = SegTree(xs)
    ans = 0.0
    last_y = events[0][0]
    for y, l, r, d in events:
        ans += (y - last_y) * seg.total_len()
        seg.update(l, r, d)
        last_y = y
    return ans


def union_area_brute(rects):
    """暴力网格计数(整数坐标小范围)用于交叉验证."""
    pts = set()
    for x1, y1, x2, y2 in rects:
        for x in range(x1, x2):
            for y in range(y1, y2):
                pts.add((x, y))
    return len(pts)


if __name__ == "__main__":
    # 两个重叠矩形
    rects = [(0, 0, 4, 4), (2, 2, 6, 6)]
    # 并面积 = 4*4 + 4*4 - 2*2 = 28
    assert abs(union_area(rects) - 28) < 1e-9
    # 三个矩形覆盖测试 (整数小范围暴力对照)
    rects2 = [(0, 0, 3, 3), (1, 1, 5, 4), (2, 0, 4, 5)]
    assert abs(union_area(rects2) - union_area_brute(rects2)) < 1e-9
    # 相离矩形
    rects3 = [(0, 0, 1, 1), (5, 5, 7, 8)]
    assert abs(union_area(rects3) - union_area_brute(rects3)) < 1e-9
    # 完全包含
    rects4 = [(0, 0, 6, 6), (1, 1, 3, 3)]
    assert abs(union_area(rects4) - 36) < 1e-9

    # 随机交叉验证
    import random
    random.seed(5)
    for _ in range(50):
        n = random.randint(1, 6)
        rs = []
        for _ in range(n):
            x1 = random.randint(-5, 5)
            x2 = random.randint(-5, 5)
            y1 = random.randint(-5, 5)
            y2 = random.randint(-5, 5)
            if x1 > x2: x1, x2 = x2, x1
            if y1 > y2: y1, y2 = y2, y1
            if x1 == x2 or y1 == y2:
                x2 += 1
                y2 += 1
            rs.append((x1, y1, x2, y2))
        a = union_area(rs)
        b = union_area_brute(rs)
        assert abs(a - b) < 1e-9, (rs, a, b)
    print("All tests passed.")
```

**PyPy 提示**: 线段树数组 4 倍空间；递归版常数在 PyPy 下尚可，n≤2e5 时事件 4e5，注意用 sys.setrecursionlimit。离散化用 dict 映射坐标。整点坐标可全程用 int 面积，但推荐 float 统一。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O((n+m) log n)，面积并/数点均摊每事件 O(log n) |
| 空间 | O(n) |

### 局限

矩形面积并要求事件按 y 排序且同 y 需先算再更新（先减后加顺序影响边界精度，整点无碍）。线段求交的平衡树实现复杂，Python 需手写 Treap/Splay 或用 sortedcontainers。二维数点要求查询可差分；不可差分信息退化 CDQ。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P5490 | 3 | 【模板】扫描线 & 矩形面积并：扫描线+线段树模板（OI Wiki 例题） | [https://www.luogu.com.cn/problem/P5490](https://www.luogu.com.cn/problem/P5490) |
| Luogu | P1856 | 5 | IOI1998/USACO5.5 矩形周长 Picture：横竖两个方向扫描求周长（OI Wiki 例题） | [https://www.luogu.com.cn/problem/P1856](https://www.luogu.com.cn/problem/P1856) |
| Luogu | P2163 | 4 | SHOI2007 园丁的烦恼：二维数点/扫描线+树状数组（OI Wiki 例题） | [https://www.luogu.com.cn/problem/P2163](https://www.luogu.com.cn/problem/P2163) |

## Pitfalls · 易错点

- 事件排序后同一 y 的多条边：面积并要先加新覆盖再算 ans 会漏/重复，标准做法是『先计算 ans 再更新』，或对同一 y 批量处理
- 线段树叶子是区间 [xs[i], xs[i+1]) 而非单点，离散化后线段数 = 点数-1
- 离散化必须去重并排序，映射到区间下标而非坐标值
- 覆盖次数 cov 用 int，覆盖长度 len 需要 double/long long；二者存储逻辑不同
- 面积并时浮点坐标用 ≤/≥ 的 EPS 边界处理要一致，否则相邻矩形边产生负宽度
- 二维数点把询问拆成 4 个前缀（容斥）别漏项

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/geometry/scanning/](https://oi-wiki.org/geometry/scanning/)
- 书籍 ✓ `CPH ch30 Sweep-line algorithms (p305-317)`
