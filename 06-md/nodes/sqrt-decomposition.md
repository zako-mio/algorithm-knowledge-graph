---
id: sqrt-decomposition
name: 根号分块（通用分块）
group: G-D-6
stage: intermediate
priority: P1
depth_tier: standard
---

# 根号分块（通用分块）

> 按块长 √n 分块，整块维护（打标记/预统计）+ 散块暴力，单次操作 O(√n)；通用性最强的区间结构。

<!-- 元信息: id=sqrt-decomposition · group=G-D-6 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

根号分块（Sqrt Decomposition，国内常称「分块」）是把序列按块长 s≈√n 分成若干块，为每个整块预处理聚合信息（如块和、块最大值、懒惰标记），对区间操作时「整块整块处理、散块暴力扫」，单次操作 O(s+n/s)，s=√n 时最优 O(√n)。它是一类思想而非单一数据结构：从区间加/求和、区间第 k 小，到莫队（离线询问分块）、值域分块（O(√n) 插入 O(1) 排名查询）、对操作分块等，都是根号思想的体现。相比线段树/树状数组，通用性更强、能维护很多线段树维护不了的信息（如区间众数、区间 mex）。

## Why · 为什么

### 直觉 · Intuition

把长序列切成块后，「查询/修改一个区间」被拆成三部分：两头的散块（长度 <s，暴力）和中间的整块（数量 ≈n/s，整块处理）。单次操作代价 = O(s)（散块）+ O(n/s)（整块），用均值不等式在 s=√n 处最小。整块的「懒」处理让区间修改只动块级标记，不必逐个元素改。这就是「空间换时间 + 懒维护」的朴素但极通用形态。

### 原理 · Principle

① 分块：块长 s=⌈√n⌉，块数 n/s；记录每块和/最大值/标记等；② 区间加/求和：同块直接暴力；跨块则散块暴力逐元素（更新块聚合），整块只打加法标记（lazy）或直接用块聚合值；③ 区间第 k 小：块内排序 + 值域二分 + 整块二分；④ 值域分块：按值域分块支持 O(√n) 插入 + O(1) 查排名；⑤ 对询问分块（莫队的前身）：每 √n 个操作重构前缀，修改 O(1)、询问 O(√n)。复杂度核心是均值不等式平衡散块与整块代价。

### 历史 · History

分块思想来自 sqrt-decomposition，CP-Algorithms 与 OI Wiki 均有系统介绍（OI Wiki 译自 e-maxx 博文）。它适用范围极广：从基础区间问题到 NOI 级 Ynoi 题都大量使用；莫队算法本质就是基于分块排序的离线分块。

## How · 实现

### 伪代码

```python
s = ceil(sqrt(n)); nb = (n+s-1)//s
sum_block[b] = 每块元素和; lazy[b] = 整块加法标记
range_add(l,r,x):
    if l,r 同块: for i in [l,r]: a[i]+=x; sum_block+=x*len
    else:
        for i in [l, 块l右界]: a[i]+=x; 更新 sum_block[l块]
        for b in (l块+1 .. r块-1): lazy[b]+=x
        for i in [块r左界, r]: a[i]+=x; 更新 sum_block[r块]
range_sum(l,r): 同理，整块用 sum_block[b]+lazy[b]*len，散块暴力
```

### Python 实现

```python
class SqrtDecomp:
    """根号分块：区间加 + 区间求和. 单次 O(sqrt(n))."""
    def __init__(self, arr):
        self.n = len(arr)
        self.s = max(1, int(self.n ** 0.5))
        self.a = list(arr)
        self.nb = (self.n + self.s - 1) // self.s
        self.sum_b = [0] * self.nb
        self.lazy = [0] * self.nb
        for i, v in enumerate(arr):
            self.sum_b[i // self.s] += v
    def _left(self, b):
        return b * self.s
    def _right(self, b):
        return min(self.n - 1, (b + 1) * self.s - 1)
    def _push(self, b):
        if self.lazy[b]:
            L, R = self._left(b), self._right(b)
            ln = R - L + 1
            for i in range(L, R + 1):
                self.a[i] += self.lazy[b]
            self.sum_b[b] += self.lazy[b] * ln
            self.lazy[b] = 0
    def range_add(self, l, r, x):
        bl, br = l // self.s, r // self.s
        if bl == br:
            self._push(bl)
            for i in range(l, r + 1):
                self.a[i] += x
            self.sum_b[bl] += x * (r - l + 1)
            return
        # 散块
        self._push(bl)
        for i in range(l, self._right(bl) + 1):
            self.a[i] += x
        self.sum_b[bl] += x * (self._right(bl) - l + 1)
        self._push(br)
        for i in range(self._left(br), r + 1):
            self.a[i] += x
        self.sum_b[br] += x * (r - self._left(br) + 1)
        # 整块
        for b in range(bl + 1, br):
            self.lazy[b] += x
    def range_sum(self, l, r):
        bl, br = l // self.s, r // self.s
        res = 0
        if bl == br:
            self._push(bl)
            for i in range(l, r + 1):
                res += self.a[i]
            return res
        self._push(bl)
        for i in range(l, self._right(bl) + 1):
            res += self.a[i]
        self._push(br)
        for i in range(self._left(br), r + 1):
            res += self.a[i]
        for b in range(bl + 1, br):
            res += self.sum_b[b] + self.lazy[b] * (self._right(b) - self._left(b) + 1)
        return res


if __name__ == "__main__":
    arr = [1, 2, 3, 4, 5, 6, 7, 8]
    sd = SqrtDecomp(arr)
    assert sd.range_sum(0, 7) == 36
    sd.range_add(1, 6, 10)      # 区间加
    # 暴力参照
    br = list(arr)
    for i in range(1, 7):
        br[i] += 10
    assert sd.range_sum(0, 7) == sum(br)
    assert sd.range_sum(2, 5) == sum(br[2:6])
    import random
    random.seed(29)
    for _ in range(300):
        n = random.randint(1, 30)
        a = [random.randint(-50, 50) for _ in range(n)]
        sd = SqrtDecomp(a)
        b = list(a)
        for _op in range(50):
            l = random.randrange(n); r = random.randrange(l, n)
            if random.random() < 0.5:
                x = random.randint(-10, 10)
                sd.range_add(l, r, x)
                for i in range(l, r + 1):
                    b[i] += x
            else:
                g = sd.range_sum(l, r)
                e = sum(b[l:r + 1])
                assert g == e, (a, l, r, g, e)
    print("All tests passed.")
```

**PyPy 提示**: 散块暴力前先 push 该块的 lazy；整块求和用 sum_b + lazy*len 避免逐个访问；块长可微调（√n 附近），大 n 时 PyPy 优势明显；区间第 k 小类问题块内排序 + 二分。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 单次操作 O(√n)；建块 O(n)；区间第 k 小 O(√n log n) 等 |
| 空间 | O(n) |

### 局限

渐近复杂度不如线段树/树状数组（O(√n) vs O(log n)），但对「信息难合并」的问题（众数、mex、区间查询套查询）分块几乎唯一可行；块长需按问题微调；Python 下 O(√n)·q 在 n=q=1e5 时 3e7 次内层操作，需 PyPy 压常数。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| LOJ | 6280 | 3 | 数列分块入门 4：区间加 + 区间和，分块模板，OI Wiki 例题 | [https://loj.ac/p/6280](https://loj.ac/p/6280) |
| CSES | Range Updates and Sums | 4 | 区间加/赋值 + 区间和，分块或线段树 | [https://cses.fi/problemset/task/1735](https://cses.fi/problemset/task/1735) |
| SPOJ | GSS4 | 4 | 区间开方 + 区间和：分块「块内全 1 后跳过」技巧 | [https://www.spoj.com/problems/GSS4/](https://www.spoj.com/problems/GSS4/) |
| Codeforces | 797E | 4 | Array Queries：按步长分块，DP 与暴力平衡的根号分治 | [https://codeforces.com/problemset/problem/797/E](https://codeforces.com/problemset/problem/797/E) |

## Pitfalls · 易错点

- 散块操作前必须 push 所在块的 lazy，否则散块读到旧值
- 整块求和用 sum_b + lazy*len，不要逐元素访问（退化为暴力）
- 块长不调优会劣化：s 过大整块慢，过小散块慢，取 √n 附近按题微调
- 最后一个块可能不满 s，_right 要取 min(n-1,...) 防越界
- 对每个问题「整块能维护什么信息」要想清楚，不是所有操作都能 O(1) 合并

## Sources · 信源

- CP-Algorithms ✓ [https://cp-algorithms.com/data_structures/sqrt_decomposition.html](https://cp-algorithms.com/data_structures/sqrt_decomposition.html)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/decompose.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/decompose.md)
- 书籍 ✓ `CPH ch27 p261`
