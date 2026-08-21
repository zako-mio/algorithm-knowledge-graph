---
id: numeric-binary-search
name: 数值二分（二分答案 / 实数二分 / 三分）
group: G-C-16
stage: intermediate
priority: P1
depth_tier: deep
---

# 数值二分（二分答案 / 实数二分 / 三分）

> 二分法在单调谓词/单调函数上以 O(log n)（整数域）或 O(log((R-L)/eps))（实数域）逼近最优解，是『答案二分』与方程求根的基础。

<!-- 元信息: id=numeric-binary-search · group=G-C-16 · stage=intermediate · priority=P1 · depth_tier=deep -->

## What · 是什么

二分搜索（binary search）利用『每次把搜索区间一分为二』把查找/求值变成对数时间。在竞赛与工程中有三类核心形态：① 在有序数组上查找下界/上界；② 在整数域上对单调布尔谓词 f 找 0→1 的分界点（二分答案：把『判定答案是否 ≥x』当作谓词）；③ 在实数域上对连续函数求根或求极值（实数二分），以及与二分同源的『三分』求单峰函数极值。核心不变量是维护 l<r 满足 f(l)=0, f(r)=1，结束时 r-l=1 即得分界点。

## Why · 为什么

### 直觉 · Intuition

『猜答案』思想：很多时候我们不会直接构造最优解，但能高效地检查『答案是否 ≥ m』。若这个检查随 m 单调（答案越大越容易/越难满足），就把 m 当成数轴上的开关，从『不可能』滑向『可能』的分界就是答案。实数二分则是介值定理的算法化：连续函数 f(L)≤y≤f(R) 时，中点把区间切成两半，总有一半仍夹住 y，反复切就能把根的位置框进任意小的区间。

### 原理 · Principle

整数域二分保证不变量 f(l)=0, f(r)=1，每次 m=(l+r)//2，根据 f(m) 收缩到 [l,m] 或 [m,r]，循环不变量始终成立，结束时 r 即第一个使 f=1 的下标（即 lower_bound）。实数二分只需 eps 控制精度：while r-l>eps 时取 m，根据 f(m) 与目标 y 的大小收缩。关于溢出：经典陷阱 m=(l+r)/2 在 C++ 大正数下可能溢出，正确写法 m=l+(r-l)/2。答案二分的典型例子是『求最大的可行答案』——用二分把最优性问题转成判定问题，只要判定函数随答案单调即可。三分（ternary search）对单峰/单谷函数，取 m1=(2l+r)/3, m2=(l+2r)/3 比较 f(m1)、f(m2) 收缩，每轮去掉 1/3，O(log n)。

### 历史 · History

二分思想历史悠久（约 1946 年首次被 John Mauchly 在 ENIAC 论文中提出『二分搜索』方法，D.H. Lehmer 于 1960 年在课程中教授），被 Knuth 称为『第一个算法』。实数的二分求根是数值分析中的经典内容；CP-Algorithms 的 Continuous search 一节系统总结了在 [L,R] 上对连续函数以 O(log((R-L)/δ)) 逼近根的过程。

## How · 实现

### 伪代码

```python
# 整数域二分（找第一个使 f=1 的位置，f 单调）
lo, hi = -1, n          # 不变量: f(lo)=0, f(hi)=1
while hi - lo > 1:
    mid = (lo + hi) // 2
    if f(mid): hi = mid
    else:      lo = mid
return hi

# 实数二分求 f(x)=y 的根（f 连续，f(L)<=y<=f(R)）
while R - L > eps:
    M = (L + R) / 2
    if f(M) < y: L = M
    else:        R = M
return (L + R) / 2

# 三分求单峰 f 的极大值点
while R - L > eps:
    m1 = L + (R - L) / 3
    m2 = R - (R - L) / 3
    if f(m1) < f(m2): L = m1
    else:            R = m2
return (L + R) / 2
```

### Python 实现

```python
def lower_bound(a, x):
    lo, hi = -1, len(a)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if a[mid] >= x:
            hi = mid
        else:
            lo = mid
    return hi

def binary_search_answer(ok, ng, check):
    # check(x) 单调：小值 ok=True，大值 ok=False；返回最大可行 x
    while ng - ok > 1:
        mid = (ok + ng) // 2
        if check(mid):
            ok = mid
        else:
            ng = mid
    return ok

def binary_search_root(f, y, lo, hi, eps=1e-9):
    # 前提 f(lo) <= y <= f(hi) 且 f 连续（经典例：x^3 求根）
    while hi - lo > eps:
        mid = (lo + hi) / 2.0
        if f(mid) < y:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0

def ternary_search(f, lo, hi, eps=1e-9):
    while hi - lo > eps:
        m1 = lo + (hi - lo) / 3.0
        m2 = hi - (hi - lo) / 3.0
        if f(m1) < f(m2):
            hi = m2
        else:
            lo = m1
    return (lo + hi) / 2.0

if __name__ == '__main__':
    a = [1, 3, 3, 5, 7, 9]
    assert lower_bound(a, 3) == 1
    assert lower_bound(a, 6) == 4
    assert lower_bound(a, 10) == 6
    print('lower_bound OK')
    # 二分答案：最大 x 使 x^2 <= 20
    assert binary_search_answer(0, 20, lambda x: x * x <= 20) == 4
    print('binary_search_answer OK')
    # 实数求根: x^3 = 27 => 3.0
    r = binary_search_root(lambda x: x ** 3, 27.0, 0.0, 10.0)
    print('cube root of 27 =', round(r, 9))
    assert abs(r - 3.0) < 1e-8
    # 三分求极小值: f(x)=(x-2)^2
    t = ternary_search(lambda x: (x - 2) ** 2, -10.0, 10.0)
    print('min arg of (x-2)^2 =', round(t, 6))
    assert abs(t - 2.0) < 1e-6
    print('OK')
```

**PyPy 提示**: 整数二分循环层数≤60，纯 Python 完全可接受；实数二分/三分迭代次数与 eps 相关，一般 100~300 次收敛，浮点开销小。注意 PyPy 下整数除法用 //，不要混用 /。对高精度要求可将 eps 设为 1e-7~1e-9 并迭代固定次数（如 200 次）代替 while 判断，避免浮点边界抖动。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 整数域二分 O(log n) 次谓词求值；实数二分 O(log((R-L)/eps)) 次；三分 O(log((R-L)/eps)) 次，每次 2 次 f 求值 |
| 空间 | O(1) |

### 局限

二分答案要求谓词严格单调；实数二分要求函数连续且符号不跳变；三分要求单峰/单谷，多峰函数会陷入局部极值。浮点比较的 eps 选太小会导致循环无法终止或抖动，选太大则精度不足。整数域二分要注意边界（全部 ok 或全部 ng 的情况）以及 mid 下取整的方向一致性。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1873 | 2 | 二分答案模板：对锯片高度二分，check 判定收集木材总量是否≥需求，单调 | [https://www.luogu.com.cn/problem/P1873](https://www.luogu.com.cn/problem/P1873) |
| LeetCode.cn | 704. 二分查找 | 1 | 最基础的有序数组二分，注意循环不变量写法 | [https://leetcode.cn/problems/binary-search/](https://leetcode.cn/problems/binary-search/) |
| Luogu | P3382 | 3 | 三分模板：给定单峰函数求极值点，可分数值稳定性练习 | [https://www.luogu.com.cn/problem/P3382](https://www.luogu.com.cn/problem/P3382) |

## Pitfalls · 易错点

- mid=(lo+hi)//2 在 C++ 大数下溢出；Python 无此问题但需统一 //
- 二分答案必须保证 check 单调，否则二分毫无意义且结果随机
- 实数二分用 f(mid)<y 而不用 f(mid)<=y 收缩方向不一致会导致振荡不收敛
- 三分只适用于单峰；存在平台/离散点时会停在平台边界，需特殊处理
- 整数域二分未覆盖『全部为 0/全部为 1』的退化情形，返回值需调用方校验

## Sources · 信源

- CP-Algorithms ✓ [https://cp-algorithms.com/num_methods/binary_search.html](https://cp-algorithms.com/num_methods/binary_search.html)
- OI Wiki ✓ [https://oi-wiki.org/basic/binary/](https://oi-wiki.org/basic/binary/)
