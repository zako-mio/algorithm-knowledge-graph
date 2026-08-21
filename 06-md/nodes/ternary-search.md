---
id: ternary-search
name: 三分法
group: G-A-1
stage: basic
priority: P1
depth_tier: standard
---

# 三分法

> 在单峰函数上找极值，基于中点比较缩小区间

<!-- 元信息: id=ternary-search · group=G-A-1 · stage=basic · priority=P1 · depth_tier=standard -->

## What · 是什么

三分法（ternary search）在单峰/单谷函数上找极值点：每轮取区间内两个分点 lmid<rmid，比较 f(lmid) 与 f(rmid)，据此舍去一侧子区间。实数域收敛到 ε 精度，整数域则需在 r-l 很小时暴力收尾。优化：黄金分割法每轮只调用一次 f。复杂度 O(log n)。用于凸/单峰优化问题。

## Why · 为什么

### 直觉 · Intuition

单峰函数『先升后降』（或先降后升）。若 f(lmid)<f(rmid)，说明 lmid 在峰左侧更陡处，峰值必在 lmid 右侧，舍去 [l,lmid]；反之舍去 [rmid,r]。每轮丢弃一段，区间等比收缩。

### 原理 · Principle

正确性不依赖分点选取，但效率依赖：取 mid±ε 近似求导，或三等分点，或黄金分割点（复用上一轮计算结果，每轮仅 1 次 f 调用）。实数实现循环条件 r-l>eps；整数域函数可能平坦（f 相等），需在小区间暴力扫描。对离散整数域，三分只能处理严格单峰且相邻差为 1 的函数，否则会漏极值——此时通常改用二分答案或枚举。

### 历史 · History

三分法/黄金分割法源于 20 世纪数值优化。黄金分割搜索由 Donald Knuth 等在 1970s 系统化，华罗庚（优选法，1970s）在中国推广了类似的 0.618 法用于工程试验优化。OI 中典型应用：求单峰函数极值（如代价函数最小化）。

## How · 实现

### 伪代码

```python
ternary_search_max(f, l, r, eps):   # 实数单峰，求最大值
    while r - l > eps:
        m1 = l + (r - l) / 3
        m2 = r - (r - l) / 3
        if f(m1) < f(m2):
            l = m1
        else:
            r = m2
    return (l + r) / 2

# 整数版：循环到 r-l 很小时暴力扫描
```

### Python 实现

```python
def f_peak(x):
    """示例单峰函数：-(x-2.5)^2 + 7，最大值 7 在 x=2.5"""
    return -(x - 2.5) ** 2 + 7


def ternary_search_max(f, l, r, eps=1e-7):
    """实数三分求单峰函数最大值点，返回 x* 近似值"""
    while r - l > eps:
        m1 = l + (r - l) / 3
        m2 = r - (r - l) / 3
        if f(m1) < f(m2):
            l = m1
        else:
            r = m2
    return (l + r) / 2


def ternary_search_min(f, l, r, eps=1e-7):
    """单谷函数求最小值点（与最大值版对称）"""
    while r - l > eps:
        m1 = l + (r - l) / 3
        m2 = r - (r - l) / 3
        if f(m1) > f(m2):
            l = m1
        else:
            r = m2
    return (l + r) / 2


def ternary_search_int(f, lo, hi):
    """整数定义域单峰：三分到区间很小时暴力扫描收尾（防平坦区间漏极值）"""
    while hi - lo > 3:
        m1 = lo + (hi - lo) // 3
        m2 = hi - (hi - lo) // 3
        if f(m1) < f(m2):
            lo = m1
        else:
            hi = m2
    best, bx = f(lo), lo
    for x in range(lo, hi + 1):
        if f(x) > best:
            best, bx = f(x), x
    return bx


if __name__ == "__main__":
    xm = ternary_search_max(f_peak, -10, 10)
    assert abs(xm - 2.5) < 1e-6, xm
    xmin = ternary_search_min(lambda x: (x - 1.0) ** 2 + 3, -10, 10)
    assert abs(xmin - 1.0) < 1e-6, xmin
    import random
    for _ in range(100):
        cx = random.randint(0, 100)
        vals = [(x - cx) ** 2 * (-1) + random.random() * 0.0 for x in range(0, 101)]
        f = lambda x, cx=cx: -(x - cx) ** 2
        assert abs(ternary_search_int(f, 0, 100) - cx) <= 1, (cx, ternary_search_int(f, 0, 100))
    print("三分法（实数最大/最小/整数版）正确性 OK")
    print("f_peak 最大值点 x* ≈ %.6f" % xm)

```

**PyPy 提示**: 三分实现简单，无特殊 PyPy 技巧。实数题注意浮点精度与 eps 选择；整数题用暴力收尾区间长度 3 的写法避免平坦区间误判。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(log((r-l)/eps)) 次 f 调用；黄金分割版每轮 1 次调用 |
| 空间 | O(1) |

### 局限

要求函数单峰/单谷（连续且无平台或平台可接受）；整数域且函数值跳变（相邻差 >1）时三分可能失效，需暴力收尾或改用二分答案。多峰函数不可用。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3382 | 3 | 三分求函数极值模板 | [https://www.luogu.com.cn/problem/P3382](https://www.luogu.com.cn/problem/P3382) |
| CP-Algorithms | num_methods/ternary_search | 3 | 三分法官方教程 | [https://cp-algorithms.com/num_methods/ternary_search.html](https://cp-algorithms.com/num_methods/ternary_search.html) |

## Pitfalls · 易错点

- 整数定义域平坦区间（f(m1)==f(m2)）会静默丢弃极值，必须小区间暴力收尾
- 循环条件用 r-l>eps 但 eps 过小导致死循环/精度溢出，需设最大迭代次数
- 把三分当二分答案用：二分答案要求单调，三分要求单峰，二者前提不同

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/basic/binary/](https://oi-wiki.org/basic/binary/)
- CP-Algorithms ✓ [https://cp-algorithms.com/num_methods/ternary_search.html](https://cp-algorithms.com/num_methods/ternary_search.html)
- OI Wiki ✓ [https://www.luogu.com.cn/problem/P3382](https://www.luogu.com.cn/problem/P3382)
