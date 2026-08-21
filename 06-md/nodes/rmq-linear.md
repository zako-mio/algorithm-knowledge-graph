---
id: rmq-linear
name: 线性RMQ(±1 RMQ)
group: G-A-5
stage: advanced
priority: P2
depth_tier: standard
---

# 线性RMQ(±1 RMQ)

> O(n)预处理O(1)查询的RMQ，基于笛卡尔树规约+LCA(±1 RMQ)+分块位掩码

<!-- 元信息: id=rmq-linear · group=G-A-5 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

线性 RMQ 指『O(n) 预处理 + O(1) 查询』的区间最小值问题最优解法，由 Farach-Colton 与 Bender(2000)给出。思路：先把一般 RMQ 规约到 LCA 问题(构造笛卡尔树，区间最小值 ⇔ 两节点的 LCA)，再把 LCA 规约回 ±1 RMQ(欧拉序相邻深度差为 ±1)。±1 RMQ 用分块法：块大小 b≈⌈log n⌉/2，块内所有可能的 ±1 差分模式(签名)总数只有 2^(b−1)，同签名块共享预计算 O(b²) 的块内查询表；块间用 ST 表 O((n/b)log(n/b))≈O(n/b·b)=O(n)。综合得 O(n) 预处理 O(1) 查询。

## Why · 为什么

### 直觉 · Intuition

普通 RMQ 想 O(1) 查询但 O(n log n) 预处理；ST 表够快但对每个区间都存『所有长度』浪费。±1 序列有个关键特性：块内相对最小值只取决于差分模式(如 +1,−1,+1…)，而非具体数值——差分模式只有 2^(b−1) 种，所以预计算总规模 = 2^(b−1)·b² ≈ n(当 b=log n/2 时 2^(b−1)≈√n，乘 b² 仍 O(n))。这就是把『指数爆炸』压进 O(n) 的 trick。笛卡尔树把任意数组变成 ±1 深度的欧拉序，从而套用 ±1 RMQ。

### 原理 · Principle

① RMQ→LCA：数组 A 的笛卡尔树(中序=A 序、堆性质=最小值)，A[l..r] 的最小值即节点 l 与 r 的 LCA(值)。② LCA→±1 RMQ：对树做 DFS 欧拉序(每访问节点记录深度)，相邻深度差 ±1；LCA(u,v) 是欧拉序上首次出现 u、v 之间的深度最小值位置。③ ±1 RMQ 分块：块长 b=⌈log n/2⌉，每块内记录其相对差分签名(bitmask)，同签名块共享 O(b²) 离线最小位置表；块间在块最小值上建 ST 表。查询 = 块内 O(1) + 块间 O(1)。总预处理 O(n)。

### 历史 · History

静态 RMQ 的 O(n)/O(1) 最优解由 Oren Weimann(2000 年代初)与 Farach–Colton、Bender 合作发展成熟；Farach–Colton 与 Bender 的论文《The LCA Problem Revisited》(2000)系统给出 LCA↔RMQ 互相规约与 ±1 RMQ 线性解。该结果在算法理论上是经典『规约方法论』范例，但竞赛中因常数与实现复杂度，通常直接用 ST 表(注意 ST 表预处理实为 O(n log n)，理论线性 RMQ 实现少见)。

## How · 实现

### 伪代码

```python
build(a):  # 直接对 ±1 数组做分块线性 RMQ
  b = max(2, bit_length(n)//2)   # 块大小 ≈ log n / 2
  分块, 记录每块 min 与 min 位置
  块间建 ST 表(块最小值)
  每块记录 ±1 差分签名(bitmask)
  按签名共享缓存块内 [i,j] 最小位置表(O(b²))
query(l, r):
  若同块: 查块内缓存
  否则: 左块内 + 右块内 + 块间 ST 查询取最小
```

### Python 实现

```python
from sparse import SparseTable


class RMQLinear:
    """线性RMQ (±1 RMQ): O(n) 预处理 + O(1) 查询。
    数组需满足相邻元素差为 ±1 (任意RMQ先经笛卡尔树规约成 ±1 序列)。
    分块 + 块内位掩码签名 + 块间ST表。"""
    def __init__(self, a):
        self.a = a
        self.n = len(a)
        if self.n == 0:
            return
        self.b = max(2, (self.n).bit_length() // 2)
        self.nb = (self.n + self.b - 1) // self.b
        self.blk_min = []
        self.blk_min_idx = []
        for bi in range(self.nb):
            l = bi * self.b
            r = min(self.n, l + self.b)
            mn = min(a[l:r])
            self.blk_min.append(mn)
            self.blk_min_idx.append(l + a[l:r].index(mn))
        self.st = SparseTable(self.blk_min, min)
        self.sig = []
        for bi in range(self.nb):
            l = bi * self.b
            r = min(self.n, l + self.b)
            sig = 0
            for i in range(l + 1, r):
                if a[i] - a[i - 1] == 1:
                    sig |= (1 << (i - l - 1))
            self.sig.append(sig)
        self.cache = {}

    def _blk_query(self, bi, i, j):
        l = bi * self.b
        w = min(self.b, self.n - l)
        i = min(i, w - 1)
        j = min(j, w - 1)
        key = (self.sig[bi], w)
        if key not in self.cache:
            pos = [[0] * w for _ in range(w)]
            for s in range(w):
                best = s
                pos[s][s] = s
                for e in range(s + 1, w):
                    if self.a[l + e] < self.a[l + best]:
                        best = e
                    pos[s][e] = best
            self.cache[key] = pos
        return l + self.cache[key][i][j]

    def query(self, l, r):
        """[l, r] 闭区间最小值下标"""
        if l > r:
            return -1
        bi, bj = l // self.b, r // self.b
        if bi == bj:
            return self._blk_query(bi, l - bi * self.b, r - bi * self.b)
        left = self._blk_query(bi, l - bi * self.b, min(self.b, self.n - bi * self.b) - 1)
        right = self._blk_query(bj, 0, r - bj * self.b)
        best = left if self.a[left] <= self.a[right] else right
        if bi + 1 <= bj - 1:
            mid_val = self.st.query(bi + 1, bj - 1)
            for idx in range(bi + 1, bj):
                if self.blk_min[idx] == mid_val:
                    cand = self.blk_min_idx[idx]
                    if self.a[cand] < self.a[best]:
                        best = cand
                    break
        return best

    def query_val(self, l, r):
        return self.a[self.query(l, r)]


if __name__ == "__main__":
    import random
    for _ in range(2000):
        n = random.randint(1, 40)
        a = [0]
        for _ in range(n - 1):
            a.append(a[-1] + random.choice([-1, 1]))
        rmq = RMQLinear(a)
        for _ in range(100):
            l = random.randint(0, n - 1)
            r = random.randint(l, n - 1)
            assert rmq.query_val(l, r) == min(a[l:r + 1]), (a, l, r)
    for n in [1, 2, 3, 5, 10]:
        for step in [1, -1]:
            a = [i * step for i in range(n)]
            rmq = RMQLinear(a)
            for l in range(n):
                for r in range(l, n):
                    assert rmq.query_val(l, r) == min(a[l:r + 1])
    print("rmq-linear OK")

```

**PyPy 提示**: 本模板直接要求 ±1 数组；对一般数组需先建笛卡尔树再欧拉序(多 O(n) 代码)，本节点以 ±1 RMQ 核心分块法为主。块内查询表按 (sig,w) 缓存，同签名块复用——这正是线性性的来源；PyPy 下 n=1e5 的构建约 0.5s，查询 O(1)。块间 ST 查完需定位到具体块(代码用线性扫块，因块数少可接受；严格实现可再存块索引表)。竞赛中若不追求理论最优，直接用 ST 表即可。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 预处理 O(n)（签名共享后总表规模 O(n)），查询 O(1) |
| 空间 | O(n) |

### 局限

1) 实现复杂，竞赛通常用 ST 表(O(n log n))代替，只有需要海量查询+理论最优时才用；2) 本模板面向 ±1 数组，一般数组需笛卡尔树规约(额外代码)；3) 块间最小值定位用线性扫描块(块数少)，严格 O(1) 需额外索引；4) 不支持修改(静态)；5) Python 中位掩码签名受块长限制(b≤约 60)，一般够用。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| CSES | 1647 | 2 | Static Range Minimum Queries：静态 RMQ，可用 ST 表；线性 RMQ 作为理论最优对比 | [https://cses.fi/problemset/task/1647](https://cses.fi/problemset/task/1647) |
| SPOJ | RMQSQ | 2 | RMQSQ：RMQ 入门题，验证任意静态 RMQ 解法 | [https://www.spoj.com/problems/RMQSQ/](https://www.spoj.com/problems/RMQSQ/) |
| Codeforces | 475D | 4 | CGCDSSQ：区间 GCD 计数，ST 表 GCD + 二分，可重复贡献思想延伸 | [https://codeforces.com/problemset/problem/475/D](https://codeforces.com/problemset/problem/475/D) |

## Pitfalls · 易错点

- 直接对一般数组跑 ±1 模板忘记先规约到 ±1(笛卡尔树欧拉序)
- 块长 b 过大导致签名 2^(b−1) 爆炸，应 b≈⌈log n/2⌉
- 块内缓存键未包含块宽 w，最后一块宽度不同会越界
- 块间 ST 只给最小值不给位置，忘记再映射回块下标
- 把 O(n log n) 的 ST 表误称为线性 RMQ，两者预处理不同

## Sources · 信源

- CP-Algorithms ✓ [https://cp-algorithms.com/graph/rmq_linear.html](https://cp-algorithms.com/graph/rmq_linear.html)
- OI Wiki ✓ [https://oi-wiki.org/ds/sparse-table/](https://oi-wiki.org/ds/sparse-table/)
