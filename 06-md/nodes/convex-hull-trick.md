---
id: convex-hull-trick
name: 凸包优化(CHT)
group: G-D-1
stage: advanced
priority: P2
depth_tier: standard
---

# 凸包优化(CHT)

> 维护下/上凸壳按斜率二分求 DP 转移最值，斜率优化经典

<!-- 元信息: id=convex-hull-trick · group=G-D-1 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

凸包优化（Convex Hull Trick, CHT / 斜率优化）是 DP 优化技术：当转移形如 dp[i] = min_j (k_j * x_i + b_j) + C_i 时，把每个决策 j 看成平面上的直线 y = k_j*x + b_j（或点 (k_j, b_j)），则 dp[i] 是在 x = x_i 处所有直线的最低点。若插入的斜率单调（或 x_i 单调），可用单调队列在均摊 O(1) 维护下凸壳并在 O(1)/O(log n) 内查询；若都不单调，可用动态开点李超线段树或平衡树。它是斜率优化 DP 的最主流实现之一，典型例题为「HNOI2008」玩具装箱。

## Why · 为什么

### 直觉 · Intuition

把每条候选直线画出来，取 min 就是在'当前 x 处挑最低的那条直线'。把所有直线围成的下包络看成一堆倾斜的雨伞骨架，在任意 x 处最低点是包络上唯一的直线——这正是凸包。若决策直线的斜率按某种顺序单调，包络的'拐点'也单调移动，用双端队列像维护凸包一样维护即可：新直线到来时，若它让队尾两条直线的交点不再有效就弹出队尾。

### 原理 · Principle

以 min、斜率严格递增插入、查询 x 递增为例：维护下凸壳（相邻直线交点的 x 坐标严格递增）。插入直线 L_new 时，若它与倒数第二条的交点横坐标 ≤ 倒数第二条与倒数第一条的交点横坐标，则倒数第一条被完全覆盖，弹出。查询时，由于交点横坐标单调，用指针 ptr 从左向右移动直到当前直线在 x 处取值最小（若查询 x 单调）。数学上，三线交点的叉积/比较可用整数判定避免浮点：bad(l1,l2,l3) 当且仅当 (b3-b1)(k1-k2) <= (b2-b1)(k1-k3)（注意斜率递减时符号翻转）。这也是把问题看作点 (k,b) 的下凸包、查询等价于求 (x,1) 与该点集最小点积的过程。

### 历史 · History

凸包优化由 Glover 1970 年代与'斜率优化'（monotone queue optimization）在竞赛圈普及，e-maxx 与 OI-wiki 的斜率优化章节系统化了这套模板；Li Chao 于 1989 年提出李超线段树作为可支持任意查询的替代结构。CPH 第 28 章（DP 优化）收录了斜率优化。如今 CHT 是 OI/ACM 斜率优化 DP 的标准工具箱。

## How · 实现

### 伪代码

```python
# 维护 min, 要求插入斜率严格单调（此处示例: 递减），查询 x 递增
class CHT:
    m, b = [], []        # 直线 y = m[k]*x + b[k], m 递减
    ptr = 0
    def bad(l1, l2, l3):  # l2 是否冗余
        return (b[l3]-b[l1])*(m[l1]-m[l2]) <= (b[l2]-b[l1])*(m[l1]-m[l3])
    def add(nm, nb):
        m.append(nm); b.append(nb)
        while len(m) >= 3 and bad(len(m)-3, len(m)-2, len(m)-1):
            删除倒数第二条
    def query(x):
        while ptr+1 < len(m) and m[ptr]*x+b[ptr] >= m[ptr+1]*x+b[ptr+1]:
            ptr += 1
        return m[ptr]*x + b[ptr]
```

### Python 实现

```python
# -*- coding: utf-8 -*-


class CHT:
    """下凸壳，求 min。要求插入斜率严格单调；
    若查询 x 单调递增，用单调指针 O(1)；否则用二分 O(log n)。
    """
    def __init__(self):
        self.m = []   # 斜率，严格递减
        self.b = []
        self.ptr = 0

    def _bad(self, l1, l2, l3):
        return (self.b[l3] - self.b[l1]) * (self.m[l1] - self.m[l2]) <= \
               (self.b[l2] - self.b[l1]) * (self.m[l1] - self.m[l3])

    def add(self, k, b):
        self.m.append(k)
        self.b.append(b)
        while len(self.m) >= 3 and self._bad(len(self.m)-3, len(self.m)-2, len(self.m)-1):
            self.m.pop(-2)
            self.b.pop(-2)

    def _f(self, i, x):
        return self.m[i] * x + self.b[i]

    def query(self, x):
        while self.ptr + 1 < len(self.m) and self._f(self.ptr, x) >= self._f(self.ptr + 1, x):
            self.ptr += 1
        return self._f(self.ptr, x)


def cht_query_binary(lines, x):
    """二分查询版：不要求 x 单调。lines 为按斜率递减排序的直线列表。"""
    lo, hi = 0, len(lines) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        k1, b1 = lines[mid]
        k2, b2 = lines[mid + 1]
        # 两直线交点 x = (b2-b1)/(k1-k2)
        if (b2 - b1) / (k1 - k2) <= x:
            lo = mid + 1
        else:
            hi = mid
    k, b = lines[lo]
    return k * x + b


if __name__ == '__main__':
    lines = [(1, 5), (2, 1), (3, -2), (4, 0)]  # 斜率递增
    cht = CHT()
    for k, b in reversed(lines):               # 插入需要斜率递减
        cht.add(k, b)
    for x in range(-3, 6):
        bf = min(k*x + b for k, b in lines)
        assert abs(cht.query(x) - bf) < 1e-9, (x, cht.query(x), bf)
    # 二分查询版（任意 x 顺序）
    hull = cht.m and sorted(list(zip(cht.m, cht.b)), key=lambda t: -t[0]) or []
    for x in [10, -5, 0, 3]:
        bf = min(k*x + b for k, b in lines)
        assert abs(cht_query_binary(hull, x) - bf) < 1e-9, (x, cht_query_binary(hull, x), bf)
    print('convex-hull-trick all tests passed')

```

**PyPy 提示**: 单调指针版均摊 O(1)，非常适合斜率 DP 模板题；二分版 O(log n) 处理 x 非单调。整数斜率/整数 x 时 bad 判据全程整数无精度问题；若斜率相等需先合并（保留截距更优者）。大数据（n=1e6）下 Python 可过玩具装箱类题目，超大用例建议 PyPy。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 插入均摊 O(1)；查询单调指针 O(1)、二分 O(log n) |
| 空间 | O(n) |

### 局限

经典实现要求插入斜率单调（递增或递减选其一）且查询 x 单调（用指针时）；斜率不单调时需平衡树/李超树；斜率相等需去重合并；浮点斜率时 bad 判定受精度影响，整数可避。求 max 时把符号取反或改为上凸壳。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3195 | 4 | [HNOI2008] 玩具装箱：斜率优化 DP 经典模板（单调队列 CHT） | [https://www.luogu.com.cn/problem/P3195](https://www.luogu.com.cn/problem/P3195) |
| Luogu | P2900 | 4 | Land Acquisition G：按 w/h 排序后斜率优化分组 DP | [https://www.luogu.com.cn/problem/P2900](https://www.luogu.com.cn/problem/P2900) |
| Luogu | P5785 | 5 | [SDOI2012] 任务安排：斜率 + 时间非单调，需二分查询的 CHT | [https://www.luogu.com.cn/problem/P5785](https://www.luogu.com.cn/problem/P5785) |

## Pitfalls · 易错点

- 斜率插入方向与查询单调性必须与维护的凸壳类型匹配（增/减、min/max）
- 斜率相等时先合并，只保留截距较优的直线
- bad 判据的叉积符号随斜率单调方向翻转，写反会丢直线
- 查询 x 非单调时不能用单调指针，要用二分/李超树
- 浮点溢出/精度：大整数时用分数比较或 __int128 思路（Python 大整数天然安全）
- DP 初始决策（j=0）必须作为第一条直线先加入

## Sources · 信源

- CP-Algorithms ✓ [https://cp-algorithms.com/geometry/convex_hull_trick.html](https://cp-algorithms.com/geometry/convex_hull_trick.html)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/dp/opt/slope.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/dp/opt/slope.md)
- 书籍 ✓ `CPH ch28`
