---
id: seg-basic
name: 线段树基础
group: G-A-6
stage: intermediate
priority: P0
depth_tier: deep
---

# 线段树基础

> O(log n)单点修改+区间查询，递归建树合并子节点信息

<!-- 元信息: id=seg-basic · group=G-A-6 · stage=intermediate · priority=P0 · depth_tier=deep -->

## What · 是什么

线段树是一棵维护区间信息的二叉树：每个节点管辖一段区间，叶节点对应单个元素，内部节点信息由左右子节点合并得到，可在 O(log n) 内完成单点修改与区间查询。

## Why · 为什么

### 直觉 · Intuition

任意查询区间 [l,r] 可被拆成至多 O(log n) 个互不相交的「极大」线段树节点区间，把这些节点的信息合并即为答案——这正是分治思想的体现。

### 原理 · Principle

采用堆式存储：节点 p 的左儿子为 2p、右儿子为 2p+1。建树时递归将区间 [s,t] 从中点 m=s+((t-s)>>1) 切分，叶节点 s==t 时直接赋值，否则合并 d[2p]+d[2p+1]。查询时若当前区间被询问区间完全包含则直接返回，否则按中点递归进入有交集的子节点。整树高度为 ceil(log n)。

### 历史 · History

线段树是区间数据结构研究中的经典产物，与树状数组(Fenwick Tree)同属一阶离散化区间结构。其核心递归分治+合并子节点信息的范式可推广到 RMQ、染色、历史版本等众多变体，是后续懒标记、动态开点、可持久化、树套树等全部线段树族结构的共同基础。

## How · 实现

### 伪代码

```python
build(s,t,p): 若 s==t 则 d[p]=a[s]; 否则 m=(s+t)/2, 递归 build 左右, d[p]=d[2p]+d[2p+1]
query(l,r,s,t,p): 若 [s,t]⊆[l,r] 返回 d[p]; 否则按 m 递归左右子节点合并结果
```

### Python 实现

```python
import sys

def build(s, t, p, a, d):
    # 对 [s,t] 区间建立线段树, 当前根编号为 p
    if s == t:
        d[p] = a[s]
        return
    m = s + ((t - s) >> 1)  # 用 (t-s)>>1 避免 (s+t) 溢出
    build(s, m, p * 2, a, d)
    build(m + 1, t, p * 2 + 1, a, d)
    d[p] = d[p * 2] + d[p * 2 + 1]  # 合并子节点信息


def update_point(x, val, s, t, p, d):
    # 单点修改: 把 a[x] 改为 val
    if s == t:
        d[p] = val
        return
    m = s + ((t - s) >> 1)
    if x <= m:
        update_point(x, val, s, m, p * 2, d)
    else:
        update_point(x, val, m + 1, t, p * 2 + 1, d)
    d[p] = d[p * 2] + d[p * 2 + 1]


def query(l, r, s, t, p, d):
    # 查询 [l,r] 区间和
    if l <= s and t <= r:
        return d[p]
    m = s + ((t - s) >> 1)
    res = 0
    if l <= m:
        res += query(l, r, s, m, p * 2, d)
    if r > m:
        res += query(l, r, m + 1, t, p * 2 + 1, d)
    return res


if __name__ == "__main__":
    sys.setrecursionlimit(1 << 20)
    n = 5
    a = [0, 10, 11, 12, 13, 14]  # 1-indexed
    d = [0] * (4 * n + 4)
    build(1, n, 1, a, d)
    print(query(1, 5, 1, n, 1, d))  # 60
    update_point(3, 100, 1, n, 1, d)
    print(query(3, 5, 1, n, 1, d))  # 127

```

**PyPy 提示**: PyPy 对本实现(递归+列表)JIT 友好，但深递归仍建议 sys.setrecursionlimit(1<<20)；大整数与列表访问均较 CPython 快；区间操作常数约为 C++ 的 5-15 倍，N>1e6 且时限 1s 的题易 TLE。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O((N+Q)log N) — 建树 O(N)，单点修改/区间查询各 O(log N) |
| 空间 | O(4N) — 堆式存储需 4N(严格上界 4N-5) 大数组；自底向上 2N-1 可达最优 |

### 局限

Python 递归常数大、N>1e6 且时限 1s 的题易 TLE；可用 sys.setrecursionlimit 提栈、或改迭代式(自底向上)减常数；只需区间和且无修改时优先树状数组(常数更小)。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3372 | 2 | 区间加+区间和，线段树入门模板题(单点查询退化版也可过) | [https://www.luogu.com.cn/problem/P3372](https://www.luogu.com.cn/problem/P3372) |
| Codeforces | 339D | 1600 | Xenia and Bitwise Operation：层数交替 or/xor 的线段树，单点修改+根查询 | [https://codeforces.com/problemset/problem/339/D](https://codeforces.com/problemset/problem/339/D) |
| HihoCoder | 1078 | 3 | 区间赋值+区间求和，线段树区间修改基础 | [https://vjudge.net/problem/HihoCoder-1078](https://vjudge.net/problem/HihoCoder-1078) |

## Pitfalls · 易错点

- 数组大小必须开 4N 而非 2N：n=2^k+1 时节点数恰为 4N-5，开 2N 会越界
- 求中点用 m=s+((t-s)>>1) 而非 (s+t)>>1，前者防整数溢出(Python 无此问题但保持习惯可移植)
- 1-indexed 与 0-indexed 混用导致边界 off-by-one，建议统一一种并在建树/查询中一致
- 递归过深未 setrecursionlimit 导致 RecursionError，Python 默认仅 1000

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/seg/](https://oi-wiki.org/ds/seg/)
- CP-Algorithms ✓ [https://cp-algorithms.com/data_structures/segment_tree.html](https://cp-algorithms.com/data_structures/segment_tree.html)
- 书籍 ✓ `Competitive Programmer's Handbook (CPH) ch9`
