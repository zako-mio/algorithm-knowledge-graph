---
id: pick-theorem
name: 皮克定理
group: G-D-3
stage: intermediate
priority: P2
depth_tier: standard
---

# 皮克定理

> A=i+b/2-1 关联整点多边形面积与内部/边上格点数

<!-- 元信息: id=pick-theorem · group=G-D-3 · stage=intermediate · priority=P2 · depth_tier=standard -->

## What · 是什么

皮克定理：对顶点均为整点的简单多边形，面积 A = i + b/2 - 1，其中 i 是严格在内部的整点数，b 是边界（边与顶点）上的整点数。配套公式：以整点为端点的线段 (Δx, Δy) 上（含两端）整点数为 gcd(|Δx|,|Δy|)+1，所以多边形边界上整点数 b = Σ gcd(|Δx_i|,|Δy_i|)（每条边内部贡献 gcd，顶点在相邻边重复——求和公式恰好覆盖）。已知 i 与 b 可在 O(1) 求面积，反之用多边形面积公式求 A 后可解内部点数 i = A - b/2 + 1。

## Why · 为什么

### 直觉 · Intuition

面积可以看成'内部点各占 1、边上点各占半格、顶点额外欠 1 格'的守恒式。想象把单位格分成三类：完全在多边形内的、被边界穿过的、顶点所在的。皮克定理的奇妙之处是它们恰好满足 A = i + b/2 - 1——先在矩形上验证（A=ab, i=(a-1)(b-1), b=2(a+b)），再靠'三角形拼接不改变公式'推广到任意多边形。

### 原理 · Principle

证明骨架：① 轴对齐矩形成立；② 直角三角形（两直角边平行于坐标轴）成立；③ 任意三角形可由矩形减若干直角三角形成；④ 多边形三角剖分后，把三角形拼接回多边形时公式保持（内部被共享的边在 b 与 i 中抵消）。高维不成立：Reeve 四面体 (0,0,0),(1,0,0),(0,1,0),(1,1,k) 内部边界整点不变但体积随 k 变化，反例说明无高维直接推广（需 Ehrhart 多项式）。

### 历史 · History

奥地利数学家 Georg Alexander Pick 于 1899 年发现并证明该定理。1957 年 John Reeve 构造的四面体反例终结了高维直接推广的尝试。皮克定理与欧拉公式 V-E+F=2 等价，现代证明常借平面图欧拉公式。CP 界经 e-maxx / cp-algorithms 与 OI-wiki 收录，典型例题 POJ 1265。

## How · 实现

### 伪代码

```python
# 多边形顶点 (x_i, y_i) 为整点, 逆/顺时针均可
# 1) 面积（2 倍面积用整数叉积）
A2 = |Σ_i (x_i*y_{i+1} - x_{i+1}*y_i)|   # 2*面积
# 2) 边界整点数
b = Σ_i gcd(|x_{i+1}-x_i|, |y_{i+1}-y_i|)
# 3) 皮克定理
A = A2 / 2 = i + b/2 - 1
→ i = A2/2 - b/2 + 1 = (A2 - b + 2) / 2
```

### Python 实现

```python
# -*- coding: utf-8 -*-
import math


def pick(poly):
    """皮克定理：返回 (面积 A, 边界整点数 b, 内部整点数 i)。顶点为整点。"""
    n = len(poly)
    A2 = 0
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        A2 += x1 * y2 - x2 * y1
    A2 = abs(A2)
    b = 0
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        b += math.gcd(abs(x2 - x1), abs(y2 - y1))
    A = A2 / 2.0
    i = (A2 - b + 2) // 2
    return A, b, i


def lattice_points_on_segment(a, b):
    """线段 a→b 上的整点数（含端点）。"""
    return math.gcd(abs(b[0]-a[0]), abs(b[1]-a[1])) + 1


if __name__ == '__main__':
    sq = [(0, 0), (2, 0), (2, 2), (0, 2)]
    A, b, i = pick(sq)
    assert A == 4 and b == 8 and i == 1, (A, b, i)
    tri = [(0, 0), (2, 0), (0, 2)]
    A, b, i = pick(tri)
    assert A == 2 and b == 6 and i == 0, (A, b, i)
    # 直角梯形对拍: 顶点整点, 用暴力数点验证
    poly = [(0, 0), (5, 0), (5, 3), (2, 3)]
    A, b, i = pick(poly)
    # 暴力数内部整点
    cnt = 0
    for x in range(0, 6):
        for y in range(0, 4):
            if (x, y) == (0, 0) or (x, y) == (5, 0) or (x, y) == (5, 3) or (x, y) == (2, 3):
                continue
            # 粗判在边界
            onb = False
            n = len(poly)
            for k in range(n):
                x1, y1 = poly[k]
                x2, y2 = poly[(k+1) % n]
                if (y1-y)*(x2-x) == (y2-y)*(x1-x) and min(x1,x2) <= x <= max(x1,x2) and min(y1,y2) <= y <= max(y1,y2):
                    onb = True
                    break
            if onb:
                continue
            # 射线法判内
            inside = False
            for k in range(n):
                x1, y1 = poly[k]
                x2, y2 = poly[(k+1) % n]
                if (y1 > y) != (y2 > y):
                    xi = x1 + (x2-x1)*(y-y1)/(y2-y1)
                    if x < xi:
                        inside = not inside
            if inside:
                cnt += 1
    assert i == cnt, (i, cnt)
    print('pick-theorem all tests passed')

```

**PyPy 提示**: 全程整数运算（叉积、gcd），无浮点；i 的公式 (A2 - b + 2)//2 中 A2 恒为偶数，整除安全。Python 的 math.gcd 支持大整数，坐标 1e9 也没问题。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n)：一遍算面积、一遍算边界 gcd |
| 空间 | O(1) |

### 局限

仅适用顶点为整点的简单多边形（不自交）；内部点计数是严格内部（边上点不计入 i）；若坐标非整点或边经过大量格点则需其他方法（如格点计数 floor_sum）；面积公式的 A 若用浮点会丢精度，务必用整数 2 倍面积。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| POJ | 1265 | 3 | Area：机器人沿网格走形成多边形，求面积+边界点+内部点（皮克经典） | [http://poj.org/problem?id=1265](http://poj.org/problem?id=1265) |
| Luogu | P2735 | 4 | 网 Electric Fences：整点多边形计数综合（皮克定理） | [https://www.luogu.com.cn/problem/P2735](https://www.luogu.com.cn/problem/P2735) |
| CP-Algorithms | picks-theorem | 3 | 皮克定理证明与高维反例（Reeve 四面体）参考 | [https://cp-algorithms.com/geometry/picks-theorem.html](https://cp-algorithms.com/geometry/picks-theorem.html) |

## Pitfalls · 易错点

- 面积必须用整数 2 倍叉积求和，浮点面积会导致 i 计算错误
- b 的计算是每条边贡献 gcd，不是边界点数+1
- i 是严格内部点，含边界点的变体公式不同
- 自交多边形不适用
- 坐标有非整点时定理不成立

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/geometry/pick.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/geometry/pick.md)
- CP-Algorithms ✓ [https://cp-algorithms.com/geometry/picks-theorem.html](https://cp-algorithms.com/geometry/picks-theorem.html)
