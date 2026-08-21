---
id: distance-metric
name: 距离度量
group: G-D-3
stage: intermediate
priority: P2
depth_tier: standard
---

# 距离度量

> 欧氏/曼哈顿/切比雪夫距离及其变换(切比雪夫↔曼哈顿)

<!-- 元信息: id=distance-metric · group=G-D-3 · stage=intermediate · priority=P2 · depth_tier=standard -->

## What · 是什么

距离度量家族定义了点与点之间的'远近'：欧氏距离 d=√((x1-x2)²+(y1-y2)²)；曼哈顿距离 d=|x1-x2|+|y1-y2|；切比雪夫距离 d=max(|x1-x2|,|y1-y2|)；闵可夫斯基距离 p 范数统一三者（p=1 曼哈顿，p=2 欧氏，p→∞ 切比雪夫）。关键变换：曼哈顿 ↔ 切比雪夫，(x,y)→(x+y, x-y) 把曼哈顿距离变成切比雪夫距离，逆变换 (x,y)→((x+y)/2,(x-y)/2) 反向。最远点对：曼哈顿最远点对可枚举 2^d 种符号组合取 max 线性求；切比雪夫最远点对即各坐标极差的最大值。

## Why · 为什么

### 直觉 · Intuition

曼哈顿距离是'只能横竖走'，切比雪夫是'可以斜着走'。把坐标系旋转 45° 再缩放 √2，'横竖格数'就变成'max 差'——这就是变换的几何意义。而曼哈顿最远点对：|x1-x2|+|y1-y2| 展开成四种符号组合，无论两点怎么摆，真实距离等于某一组合的值，所以枚举 2^d 组合取极差即可，像'把绝对值去掉'的暴力思想。

### 原理 · Principle

曼哈顿→切比雪夫：|x1-x2|+|y1-y2| = max( |(x1+y1)-(x2+y2)|, |(x1-y1)-(x2-y2)| )，即点 (x,y) 映到 (x+y, x-y) 后切比雪夫距离不变（旋转 45° 缩放）。切比雪夫→曼哈顿：max 展开后等价于坐标映到 ((x+y)/2,(x-y)/2) 的曼哈顿距离。最远曼哈顿点对 = 对所有符号掩码 msk ∈ {0,1}^d，计算 cur = Σ ±xi（按位决定正负），取 max(库内 max(cur) - min(cur))，因为两点符号互补时差即为距离。d 维复杂度 O(n·2^d·d)。

### 历史 · History

各距离概念源于几何/拓扑（Chebyshev distance 因棋盘国王移动得名，Manhattan distance 出自 Herman Minkowski 论曼哈顿街道规划的传统说法）。两者旋转 45° 等价性的系统整理常见于算法题解集，cp-algorithms 的 Manhattan distance 页、OI-wiki 的 distance 页均有收录。

## How · 实现

### 伪代码

```python
# 曼哈顿最远点对（d 维，O(n·2^d·d)）
ans = 0
for msk in range(1<<d):
    mx, mn = -inf, +inf
    for p in points:
        cur = Σ_j ( +p[j] if msk bit j else -p[j] )
        mx = max(mx, cur); mn = min(mn, cur)
    ans = max(ans, mx - mn)

# 曼哈顿 → 切比雪夫: (x, y) -> (x+y, x-y)
# 切比雪夫 → 曼哈顿: (x, y) -> ((x+y)/2, (x-y)/2)
```

### Python 实现

```python
# -*- coding: utf-8 -*-


def manhattan(p, q):
    return abs(p[0]-q[0]) + abs(p[1]-q[1])


def chebyshev(p, q):
    return max(abs(p[0]-q[0]), abs(p[1]-q[1]))


def manhattan_farthest(points):
    """曼哈顿最远点对距离，O(n·2^d·d)，d=2。"""
    d = 2
    ans = 0
    for msk in range(1 << d):
        mx = -10**30
        mn = 10**30
        for x, y in points:
            cur = x if (msk & 1) else -x
            cur += y if (msk & 2) else -y
            mx = max(mx, cur)
            mn = min(mn, cur)
        ans = max(ans, mx - mn)
    return ans


def chebyshev_farthest(points):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return max(max(xs) - min(xs), max(ys) - min(ys))


def to_chebyshev(p):
    return (p[0] + p[1], p[0] - p[1])


def to_manhattan(p):
    return ((p[0] + p[1]) / 2.0, (p[0] - p[1]) / 2.0)


if __name__ == '__main__':
    pts = [(0, 0), (3, 0), (0, 4)]
    assert manhattan_farthest(pts) == 7, manhattan_farthest(pts)
    assert chebyshev_farthest([(0, 0), (3, 4)]) == 4
    # 变换保距验证
    import random
    for _ in range(200):
        a = (random.randint(-10, 10), random.randint(-10, 10))
        b = (random.randint(-10, 10), random.randint(-10, 10))
        A, B = to_chebyshev(a), to_chebyshev(b)
        assert abs(manhattan(a, b) - chebyshev(A, B)) < 1e-9
        A2, B2 = to_manhattan(a), to_manhattan(b)
        assert abs(chebyshev(a, b) - manhattan(A2, B2)) < 1e-9
    # 曼哈顿最远点对 vs 暴力
    for _ in range(100):
        P = [(random.randint(-20, 20), random.randint(-20, 20)) for _ in range(30)]
        bf = max(manhattan(P[i], P[j]) for i in range(len(P)) for j in range(len(P)))
        assert manhattan_farthest(P) == bf, (manhattan_farthest(P), bf)
    print('distance-metric all tests passed')

```

**PyPy 提示**: 曼哈顿最远点对枚举 2^d 组合常数极小，O(n·4) 对 1e6 点都很快。切比雪夫转换后求'曼哈顿最近点对'可用扫描线+平衡树，或转换后再用分治。整点坐标全程整数（逆变换 /2 需处理奇偶，浮点题才用分数）。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 最远点对 O(n·2^d)；变换 O(n)；单次距离计算 O(1) |
| 空间 | O(n) |

### 局限

曼哈顿↔切比雪夫变换的逆变换带 /2 会出现 .5 小数，整点场景需处理；切比雪夫最远点对仅 max/min，但曼哈顿最近点对不能直接变换（需专门算法）；p<1 的闵可夫斯基距离不是度量（不满足三角不等式）；大坐标溢出注意类型。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P5098 | 3 | Cave Cows 3：曼哈顿最远点对，符号枚举或转切比雪夫 | [https://www.luogu.com.cn/problem/P5098](https://www.luogu.com.cn/problem/P5098) |
| Luogu | P3964 | 4 | 松鼠聚会：切比雪夫→曼哈顿（/2 坐标）后用前缀和求最小总距离 | [https://www.luogu.com.cn/problem/P3964](https://www.luogu.com.cn/problem/P3964) |
| Luogu | P4648 | 5 | pairs 动物对数：曼哈顿转切比雪夫后分块/扫描求解 | [https://www.luogu.com.cn/problem/P4648](https://www.luogu.com.cn/problem/P4648) |

## Pitfalls · 易错点

- 切比雪夫转曼哈顿时忘了 /2，导致答案差 2 倍
- 最远点对符号枚举要覆盖全部 2^d 组合，符号互补的 pair 已在其中
- 整点转曼哈顿用浮点 .5 会引入误差，整数题用 2*距离 或分数
- 曼哈顿最近点对不能直接转切比雪夫求（需扫描线+平衡树）
- 欧氏距离开根丢精度，先算平方比较大小

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/geometry/distance.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/geometry/distance.md)
- CP-Algorithms ✓ [https://cp-algorithms.com/geometry/manhattan-distance.html](https://cp-algorithms.com/geometry/manhattan-distance.html)
