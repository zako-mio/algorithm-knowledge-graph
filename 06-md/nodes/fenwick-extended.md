---
id: fenwick-extended
name: 扩展树状数组
group: G-A-5
stage: intermediate
priority: P1
depth_tier: standard
---

# 扩展树状数组

> 差分实现区间修改+区间查询(双BIT)，或双BIT维护不可差分信息O(log²n)

<!-- 元信息: id=fenwick-extended · group=G-A-5 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

扩展树状数组有两类核心用途：① 区间加 + 区间求和：用两个 BIT 维护差分数组 d[i] 与 d[i]·i，推导得前缀和 sum(1..r)=sum_B1(r)·r−sum_B2(r)，区间加只做 4 次点加；② 区间加 + 单点查：单个 BIT 维护差分，区间加两次点加，单点查询一次前缀和。③ 维护不可差分信息(区间最值等)：因 BIT 单点更新需要『从区间移除旧值』做逆运算，对不可差分信息改为 O(log²n) 的块内重构式更新。二维 BIT 则是树状数组套树状数组，支持二维单点改/区间查。

## Why · 为什么

### 直觉 · Intuition

差分把『区间加』变成两次『单点加』：区间 [l,r] 加 v ⇔ d[l]+=v, d[r+1]−=v，而前缀和就是对差分数组求和，于是区间修改转成了单点修改，直接套 BIT。但区间查询需要 ∑a[i]，即差分 d 的『二重前缀和』——展开后每项 d[j] 被加 (r−j+1) 次，拆成 ∑d[j]·(r+1)−∑d[j]·j 两部分，各用一个 BIT 维护即可。不可差分信息因为无法『减回去』，只能把受影响的 c 区间用其儿子+单点重构。

### 原理 · Principle

设 d[i]=a[i]−a[i−1]，则 a[i]=∑_{j≤i}d[j]，前缀和 ∑_{i=1}^r a[i]=∑_{j=1}^r d[j]·(r−j+1)=∑d[j]·(r+1)−∑d[j]·j。故用 B1 维护 d[j]、B2 维护 d[j]·j，pre(r)=sumB1(r)·r−sumB2(r)。区间加 [l,r] 加 v：B1: add(l,v), add(r+1,−v)；B2: add(l,v·(l−1)), add(r+1,−v·r)。区间求和 = pre(r)−pre(l−1)。区间加+单点查是特例(一个 BIT)。不可差分(最值)：query 沿 lowbit 跳但防止越过 l，单点更新用 c 的儿子们+点 a[x] 重构，均 O(log²n)。

### 历史 · History

树状数组扩展能力由竞赛社区在上世纪 90~00 年代逐步完善：差分法解决区间修改源自『差分+前缀和』思想的 BIT 化；区间加+区间求和的『双 BIT』trick 在 CPH、USACO、TopCoder 教程中广泛流传；二维 BIT 则是 BIT 的维度推广。

## How · 实现

### 伪代码

```python
class FenwickRange:
  b1, b2  (both BIT)
  range_add(l,r,x):
    b1.add(l,x); b1.add(r+1,-x)
    b2.add(l,x*(l-1)); b2.add(r+1,-x*r)
  prefix_sum(i) = b1.sum(i)*i - b2.sum(i)
  range_sum(l,r) = prefix_sum(r)-prefix_sum(l-1)
class FenwickDiff:
  range_add(l,r,x): add(l,x); add(r+1,-x)
  point(i) = prefix_sum(i)
```

### Python 实现

```python
class FenwickRange:
    """扩展树状数组: 区间加 + 区间求和。双 BIT 维护差分 d[i] 与 d[i]*i。"""
    def __init__(self, n, init=None):
        self.n = n
        self.b1 = [0] * (n + 1)
        self.b2 = [0] * (n + 1)
        if init:
            for i, v in enumerate(init, 1):
                self.range_add(i, i, v)

    def _add(self, bit, i, x):
        while i <= self.n:
            bit[i] += x
            i += i & -i

    def _sum(self, bit, i):
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s

    def range_add(self, l, r, x):
        self._add(self.b1, l, x)
        self._add(self.b1, r + 1, -x)
        self._add(self.b2, l, x * (l - 1))
        self._add(self.b2, r + 1, -x * r)

    def prefix_sum(self, i):
        return self._sum(self.b1, i) * i - self._sum(self.b2, i)

    def range_sum(self, l, r):
        return self.prefix_sum(r) - self.prefix_sum(l - 1)


class FenwickDiff:
    """扩展树状数组: 区间加 + 单点查 (单 BIT 维护差分)"""
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, x):
        while i <= self.n:
            self.bit[i] += x
            i += i & -i

    def range_add(self, l, r, x):
        self.add(l, x)
        self.add(r + 1, -x)

    def point(self, i):
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s


if __name__ == "__main__":
    import random
    a = [random.randint(-100, 100) for _ in range(20)]
    n = len(a)
    fr = FenwickRange(n, a)
    assert fr.range_sum(1, n) == sum(a)
    assert fr.range_sum(5, 10) == sum(a[4:10])
    fr.range_add(3, 7, 5)
    for i in range(3, 8):
        a[i - 1] += 5
    assert fr.range_sum(1, n) == sum(a)
    assert fr.range_sum(4, 6) == sum(a[3:6])
    fd = FenwickDiff(n)
    b = [0] * n
    for _ in range(100):
        l = random.randint(1, n)
        r = random.randint(l, n)
        x = random.randint(-10, 10)
        fd.range_add(l, r, x)
        for i in range(l - 1, r):
            b[i] += x
    for i in range(n):
        assert fd.point(i + 1) == b[i]
    print("fenwick-extended OK")

```

**PyPy 提示**: 双 BIT 每操作 4 次单点 add(每个 O(log n))，PyPy 下 n=1e5, 1e6 次操作约 1s。注意 b2 的更新值在 r+1 处是 −x*r(不是 −x*(r+1))——这与 CP-alg 一致，源于推导 pre(i)=∑d·(r+1)−∑d·j 的常数处理；若混淆公式会整体错。区间加+单点查用单 BIT 更省。二维 BIT 用 list of lists 实现 n² 内存，n≤1000 可用。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 区间加+区间查 O(log n)；区间加+单点查 O(log n)；不可差分最值 O(log²n) |
| 空间 | O(n) |

### 局限

1) 双 BIT 区间求和公式易错，务必对照推导或对拍；2) 区间加区间查仅适用于可差分信息(和)；3) 二维 BIT 内存 O(n²)；4) 不可差分信息(最值/gcd)的扩展 BIT 复杂度 O(log²n) 比线段树 O(log n) 差；5) 若需区间乘区间查、区间赋值等更强操作需线段树+懒标记。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3372 | 3 | 【模板】线段树1(区间加+区间求和)：双 BIT 差分方案可解(或线段树) | [https://www.luogu.com.cn/problem/P3372](https://www.luogu.com.cn/problem/P3372) |
| Luogu | P4514 | 4 | 上帝造题的七分钟：二维 BIT(区间加+区间求和)，二维差分扩展 | [https://www.luogu.com.cn/problem/P4514](https://www.luogu.com.cn/problem/P4514) |
| LOJ | 135 | 3 | 二维树状数组3(区间修改+区间查询)：二维差分双 BIT 模板 | [https://loj.ac/p/135](https://loj.ac/p/135) |

## Pitfalls · 易错点

- b2 在 r+1 的更新写成 −x*(r+1) 而非 −x*r，公式全错
- 区间加+单点查与区间加+区间查混用同一实现
- 前缀和公式 pre(i)=sumB1(i)*i−sumB2(i) 乘的是 i(查询下标)不是 l
- 二维 BIT 坐标 +1 与差分矩阵偏移处理遗漏
- 把不可差分信息用普通 BIT 的『直接赋值 max』更新，会得到错误(旧值残留)

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/fenwick/](https://oi-wiki.org/ds/fenwick/)
- CP-Algorithms ✓ [https://cp-algorithms.com/data_structures/fenwick.html](https://cp-algorithms.com/data_structures/fenwick.html)
