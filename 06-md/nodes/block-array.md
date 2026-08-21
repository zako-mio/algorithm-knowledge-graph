---
id: block-array
name: 块状数组（分块）
group: G-D-6
stage: advanced
priority: P1
depth_tier: standard
---

# 块状数组（分块）

> 将数组分成O(√n)块，整块维护懒标记、散块暴力，实现O(√n)区间修改/查询

<!-- 元信息: id=block-array · group=G-D-6 · stage=advanced · priority=P1 · depth_tier=standard -->

## What · 是什么

块状数组（分块，sqrt decomposition）把长度为 n 的序列切成约 O(√n) 个块，每块长度约 O(√n)。块内元素整体维护聚合信息（如 lazy 加法标记、块内排序数组），跨块的区间操作只需对整块 O(√n) 个块做整体处理，而两端的散块（部分被覆盖的块）直接暴力修改后重构。它把「区间修改/区间查询」这类线段树能处理的问题推广到需要「块内排序二分」等不可线段树维护的操作上（如查询区间内 ≥z 的数的个数），代价是单次操作 O(√n log n)。

## Why · 为什么

### 直觉 · Intuition

√n·√n=n 的分裂让每个操作最多触碰 √n 个整块和 √n 个散点：散块暴力 O(√n)，整块只需 O(1) 打标记或 O(log n) 二分。根号平衡使复杂度从 O(n) 降到 O(√n)，并且能塞进线段树不好维护的「排序后二分」类操作。

### 原理 · Principle

设块长 B≈√n。维护原数组 a、每个元素的所属块 belong[i]、每个块的 lazy 标记与块内排序副本 t（对块排序）。区间加 [l,r]+c：同块则暴力加后 sort 重构；否则散块暴力加+重构，中间整块 lazy[b]+=c。查询 ≥z 的个数：散块逐个判断 a[i]+lazy≥z，整块用 bisect 在 t 上数 ≥ z-lazy[b] 的个数。总复杂度 O(q√n log n)。复杂度分析的根号平衡思想（徐明宽 2017 国家集训队论文《非常规大小分块算法初探》专题展开）。

### 历史 · History

分块思想源自数据结构的经典 trade-off，OI Wiki 在《块状数组》章节系统介绍，并用洛谷 P2801 教主的魔法、P4168 蒲公英、P4135 作诗等作为练习；CP-Algorithms 的 sqrt_decomposition 章节亦收录。它常作为线段树/树套树的低配替代，也用于莫队等离线算法的块内维护。

## How · 实现

### 伪代码

```python
# 区间加 + 查询区间内 >= z 的个数
def Range_Add(l, r, c):
  bl, br = belong[l], belong[r]
  if bl == br:
    for i in l..r: a[i] += c
    Sort(bl); return
  for i in l..块尾: a[i] += c      # 散块
  for i in 块头..r: a[i] += c
  Sort(bl); Sort(br)
  for b in bl+1..br-1: lazy[b] += c  # 整块打标记

def Count_GE(l, r, z):
  bl, br = belong[l], belong[r]
  ans = 0
  if bl == br: return 散块逐个判断 a[i]+lazy[bl] >= z
  for i in l..块尾: if a[i]+lazy[bl] >= z: ans += 1
  for i in 块头..r: if a[i]+lazy[br] >= z: ans += 1
  for b in bl+1..br-1:
    ans += 块长 - bisect_left(t[b], z - lazy[b])
```

### Python 实现

```python
import bisect
import math
import random


class BlockArray:
    """块状数组：区间加 + 查询区间内 >= z 的个数（洛谷 P2801 模板）。
    整块维护 lazy 标记与块内排序副本，散块暴力后重建排序。"""

    def __init__(self, arr, block_size=0):
        self.n = len(arr)
        self.a = list(arr)
        self.B = block_size or int(self.n ** 0.5) + 1
        self.nb = (self.n + self.B - 1) // self.B
        self.belong = [i // self.B for i in range(self.n)]
        self.sorted = []
        self.lazy = [0] * self.nb
        for b in range(self.nb):
            l, r = b * self.B, min((b + 1) * self.B, self.n)
            self.sorted.append(sorted(self.a[l:r]))

    def rebuild(self, b):
        l, r = b * self.B, min((b + 1) * self.B, self.n)
        self.sorted[b] = sorted(self.a[l:r])

    def range_add(self, l, r, c):
        bl, br = self.belong[l], self.belong[r]
        if bl == br:
            for i in range(l, r + 1):
                self.a[i] += c
            self.rebuild(bl)
            return
        for i in range(l, (bl + 1) * self.B):
            self.a[i] += c
        self.rebuild(bl)
        for i in range(br * self.B, r + 1):
            self.a[i] += c
        self.rebuild(br)
        for b in range(bl + 1, br):
            self.lazy[b] += c

    def count_ge(self, l, r, z):
        bl, br = self.belong[l], self.belong[r]
        ans = 0
        if bl == br:
            for i in range(l, r + 1):
                if self.a[i] + self.lazy[bl] >= z:
                    ans += 1
            return ans
        for i in range(l, (bl + 1) * self.B):
            if self.a[i] + self.lazy[bl] >= z:
                ans += 1
        for i in range(br * self.B, r + 1):
            if self.a[i] + self.lazy[br] >= z:
                ans += 1
        for b in range(bl + 1, br):
            target = z - self.lazy[b]
            ans += len(self.sorted[b]) - bisect.bisect_left(self.sorted[b], target)
        return ans


if __name__ == "__main__":
    random.seed(42)
    for n in [1, 2, 5, 17, 100, 250]:
        base = [random.randint(1, 100) for _ in range(n)]
        ba = BlockArray(base)
        brute = list(base)
        for _ in range(400):
            l = random.randrange(n)
            r = random.randrange(n)
            if l > r:
                l, r = r, l
            if random.random() < 0.6:
                c = random.randint(-20, 20)
                ba.range_add(l, r, c)
                for i in range(l, r + 1):
                    brute[i] += c
            else:
                z = random.randint(1, 200)
                expect = sum(1 for i in range(l, r + 1) if brute[i] >= z)
                got = ba.count_ge(l, r, z)
                assert got == expect, (n, l, r, z, got, expect)
    print("block-array 自测通过：随机 区间加/查询 与暴力对拍一致")

```

**PyPy 提示**: 块长取 int(sqrt(n))+1，PyPy 下 bisect 在列表上速度可接受；对拍数据量小则常数无所谓。若块数很大，可把 sorted 副本改存列表引用复用。注意 Python 的 bisect 是 C 实现，性能远好于手写二分。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 区间操作 O(√n log n)（散块 O(√n)+整块二分 O(log n)；若不需排序则 O(√n)） |
| 空间 | O(n)（原数组 + 每块排序副本，总 O(n)） |

### 局限

只支持静态区间或带有 lazy 标记的整块操作；若操作需要整块内保持有序（如 count_ge），散块修改后必须重建排序，使单次 O(√n log n)。对「可离线+无修改」类问题分块不如莫队；对需要区间可合并信息的场景线段树 O(log n) 更快。块长需按 n 调优。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P2801 | 4 | 教主的魔法：块状数组模板，区间加+查询区间内≥z个数（OI Wiki 例题1） | [https://www.luogu.com.cn/problem/P2801](https://www.luogu.com.cn/problem/P2801) |
| Luogu | P4168 | 5 | 蒲公英：区间众数，分块维护块间信息+散块枚举（OI Wiki 练习） | [https://www.luogu.com.cn/problem/P4168](https://www.luogu.com.cn/problem/P4168) |
| Codeforces | 13E | 4 | Holes：分块维护每块内跳步信息，支持单点修改（CP-Algorithms 例题） | [https://codeforces.com/contest/13/problem/E](https://codeforces.com/contest/13/problem/E) |
| LOJ | 130 | 3 | 单点修改区间查询分块模板（OI Wiki 练习） | [https://loj.ac/problem/130](https://loj.ac/problem/130) |

## Pitfalls · 易错点

- 散块修改后必须重建排序副本，否则 count_ge 用旧排序会错
- 整块查询时要把 lazy 标记算进阈值：数 ≥ z-lazy[b] 而非 ≥ z
- l、r 同块时只做暴力并重建该块，别走到整块分支
- 块长取 √n 附近；取 1 或 n 都会退化为 O(n) 操作
- 区间加可叠加 lazy，但赋值操作（寒夜方舟类）需要 pushdown 并区分『未赋值』标记
- 归零/负数 lazy 与排序副本的交互：bisect_left 处理相等值边界要一致

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/block-array/](https://oi-wiki.org/ds/block-array/)
- CP-Algorithms ✓ [https://cp-algorithms.com/data_structures/sqrt_decomposition.html](https://cp-algorithms.com/data_structures/sqrt_decomposition.html)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/block-array.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/block-array.md)
- 书籍 ✓ `CPH ch27 (p277)`
