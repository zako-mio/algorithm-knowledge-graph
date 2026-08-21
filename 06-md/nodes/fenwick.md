---
id: fenwick
name: 树状数组(BIT)
group: G-A-5
stage: basic
priority: P0
depth_tier: deep
---

# 树状数组(BIT)

> lowbit分组，O(log n)单点修改+前缀查询，代码短常数小

<!-- 元信息: id=fenwick · group=G-A-5 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

树状数组(Binary Indexed Tree / Fenwick Tree)：利用 lowbit(x)=x&(−x) 把数组划分成 O(log n) 层区间，支持单点修改与前缀和/前缀查询各 O(log n)，代码极短、常数极小。c[x] 管辖区间 [x−lowbit(x)+1, x]。修改点 i 时沿 i+=lowbit(i) 向上更新 O(log n) 个 c；查询前缀 [1..i] 时沿 i−=lowbit(i) 累加 O(log n) 个 c。区间查询用前缀差分。维护的信息需满足结合律且可差分(有逆运算)：加法、乘法、异或等可行；gcd/max 不可差分。应用广泛：前缀和、逆序对、二维偏序、权值树状数组(计数)等。

## Why · 为什么

### 直觉 · Intuition

前缀和可以拆成不超过 log n 段『已知区间和』。c[x] 存的是以 x 为右端点、长度等于 x 的 lowbit 的区间和。查询时从 x 出发每次跳掉 lowbit(x) 个元素，恰好覆盖前缀；修改时从 x 向上跳 lowbit 覆盖所有包含 x 的 c。二进制视角：i 的二进制从低位往高位清 1 的过程就是区间划分，妙处在于『每个下标只参与其祖先的维护』，树高 log n。

### 原理 · Principle

lowbit(x)=x&(−x)=x 二进制最低位 1 及其后 0 组成的数。c[x]=∑a[x−lowbit(x)+1..x]。修改 a[i]+=v：对所有 x=i,i+lowbit(i),…≤n 做 c[x]+=v(这些 x 的管辖区间都包含 i)，共 O(log n)。查询前缀 sum(1..i)：x=i,i−lowbit(i),…>0 累加 c[x]，覆盖 [1..i] 不重不漏。区间和 [l..r]=sum(r)−sum(l−1)。因为每个整数可唯一分解为 O(log n) 个互不相交的 lowbit 区间。

### 历史 · History

由 Ryuhei Mori 在 1970 年代提出，经加拿大籍华裔计算机科学家 Peter Fenwick 于 1994 年在 Software—Practice and Experience 发表论文后广为人知，故称 Fenwick Tree。竞赛中因极简实现与极小常数成为区间查询首选，甚至可替代部分线段树场景。

## How · 实现

### 伪代码

```python
lowbit(x) = x & -x
add(i, v): while i<=n: c[i]+=v; i+=lowbit(i)
sum(i): s=0; while i>0: s+=c[i]; i-=lowbit(i); return s
range_sum(l,r) = sum(r)-sum(l-1)
```

### Python 实现

```python
class Fenwick:
    """树状数组: 单点改 + 区间查。下标 1-based。"""
    def __init__(self, n, init=None):
        self.n = n
        self.bit = [0] * (n + 1)
        if init:
            for i, v in enumerate(init, 1):
                self.bit[i] += v
                j = i + (i & -i)
                if j <= n:
                    self.bit[j] += self.bit[i]

    def add(self, i, x):
        while i <= self.n:
            self.bit[i] += x
            i += i & -i

    def sum(self, i):
        """前缀和 [1, i]"""
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

    def range_sum(self, l, r):
        return self.sum(r) - self.sum(l - 1)


if __name__ == "__main__":
    a = [1, 2, 3, 4, 5]
    n = len(a)
    fw = Fenwick(n, a)
    assert fw.range_sum(1, 5) == 15
    assert fw.range_sum(2, 4) == 9
    fw.add(3, 10)
    assert fw.range_sum(1, 5) == 25
    assert fw.range_sum(3, 3) == 13
    print("fenwick basic OK")

```

**PyPy 提示**: Fenwick 循环是 while 整数运算，PyPy JIT 下 n=1e5 的 1e6 次操作约 0.3s，是目前 PyPy 下最快的区间数据结构。下标必须 1-based，若输入 0-based 记得 +1。O(n) 建树用『由父累加』(代码中 init 分支)比逐点 add 快。权值树状数组(计数)在逆序对/偏序问题中是标配。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 单点修改与前缀查询均 O(log n)；建树 O(n) |
| 空间 | O(n) |

### 局限

1) 维护的信息需满足结合律+可差分(有逆运算)，gcd/max 等不可差分不能用普通版本(见 fenwick-extended)；2) 区间修改需配合差分(见 fenwick-extended)；3) 下标从 1 开始，需处理 0-based 输入；4) 与线段树比不支持直接区间合并(如区间最大子段和)、懒标记；5) 需要求任意区间最值/不可差分信息时用线段树或扩展 BIT。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3374 | 1 | 【模板】树状数组1：单点修改+区间求和，最基础模板 | [https://www.luogu.com.cn/problem/P3374](https://www.luogu.com.cn/problem/P3374) |
| Luogu | P1908 | 2 | 逆序对：权值树状数组/离散化计数，BIT 经典应用 | [https://www.luogu.com.cn/problem/P1908](https://www.luogu.com.cn/problem/P1908) |
| LeetCode | 307 | 3 | Range Sum Query - Mutable：BIT/线段树模板，单点改区间查 | [https://leetcode.cn/problems/range-sum-query-mutable/](https://leetcode.cn/problems/range-sum-query-mutable/) |

## Pitfalls · 易错点

- 下标从 0 开始导致死循环或越界，必须 1-based(输入 +1)
- 更新路径用 i+=lowbit(i)，查询路径用 i−=lowbit(i)，方向搞反
- 区间查询忘记 l−1：range_sum(l,r) 应为 sum(r)−sum(l−1)
- 维护不可差分信息(gcd/max)误用普通 BIT 更新(应走 fenwick-extended 的 O(log²n) 方案)
- O(n log n) 逐点建树慢，忘记 O(n) 前缀累加建树法

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/fenwick/](https://oi-wiki.org/ds/fenwick/)
- CP-Algorithms ✓ [https://cp-algorithms.com/data_structures/fenwick.html](https://cp-algorithms.com/data_structures/fenwick.html)
- 书籍 ✓ `CPH ch9 p97`
