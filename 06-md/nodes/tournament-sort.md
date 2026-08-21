---
id: tournament-sort
name: 锦标赛排序
group: G-A-1
stage: intermediate
priority: P3
depth_tier: brief
---

# 锦标赛排序

> 基于锦标赛树的排序，O(n log n)

<!-- 元信息: id=tournament-sort · group=G-A-1 · stage=intermediate · priority=P3 · depth_tier=brief -->

## What · 是什么

锦标赛排序（tournament sort，树形选择排序）是选择排序的优化：用一颗完全二叉树（锦标赛树）每次 O(log n) 找出当前最小元素，n 次共 O(n log n)。叶子存元素，内部结点存两子中较小者的下标；选出最小元素后把它置为 +∞ 再沿路径重建。不稳定，空间 O(n)。

## Why · 为什么

### 直觉 · Intuition

体育锦标赛：n 个选手两两比赛决出冠军只需 n-1 场。亚军不是决赛对手而是被冠军击败者——但排序需要按顺序决出所有名次。锦标赛排序把每轮比较结果存进树里复用，避免每次全量重扫。

### 原理 · Principle

建树：叶子放 n 个元素，内部结点两两比较存胜者下标（O(n) 建树）。取最小：树根就是最小值下标。重建：把该叶子置 +∞，沿它到根的路径重新比较（每层一个比较，O(log n)）。反复 n 次。它与堆排序同源于『用完全二叉树找极值』，区别是锦标赛树维护完整比较历史。

### 历史 · History

锦标赛树思想源自 20 世纪中期 k-路归并（k-way merge）的外排序实践（K. E. Iverson 等人）。由于堆排序更简洁、原地且常数小，锦标赛排序在现代竞赛中已少见，主要价值在理解『复用比较结果』与树形选择。

## How · 实现

### 伪代码

```python
tournament_sort(a):
    n = len(a)
    建树：tmp[n..2n-1] = a，内部结点两两取小者下标
    for i in range(n):
        a[i] = a[tmp[1]]          # 树根 = 当前最小
        把 tmp[1] 指向的叶子置 +∞
        沿 tmp[1] 到根路径重建
    return a
```

### Python 实现

```python
def tournament_sort(a):
    a = list(a)                         # 拷贝，避免破坏调用方输入
    n = len(a)
    INF = float("inf")
    tree = [n] * (2 * n)            # 内部结点存元素下标，叶子初始为 n(哨兵)
    for i in range(n):
        tree[n + i] = i
    for i in range(n - 1, 0, -1):
        li = tree[2 * i]
        ri = tree[2 * i + 1]
        lv = a[li] if li < n else INF
        rv = a[ri] if ri < n else INF
        tree[i] = li if lv <= rv else ri
    out = []
    for _ in range(n):
        idx = tree[1]               # 当前最小元素下标
        out.append(a[idx])
        a[idx] = INF                # 淘汰该元素
        p = (n + idx) // 2          # 沿路径向上重建
        while p >= 1:
            li = tree[2 * p]
            ri = tree[2 * p + 1]
            lv = a[li] if li < n else INF
            rv = a[ri] if ri < n else INF
            tree[p] = li if lv <= rv else ri
            p //= 2
    return out


if __name__ == "__main__":
    import random
    for _ in range(200):
        arr = [random.randint(0, 100) for _ in range(random.randint(0, 80))]
        assert tournament_sort(arr) == sorted(arr), (arr, tournament_sort(arr))
    print("锦标赛排序正确性 OK（200 组随机）")
    print("示例:", tournament_sort([5, 3, 8, 1, 9, 2, 7]))

```

**PyPy 提示**: 比赛中该算法罕见；若需要『维护极值』直接用 heapq。本实现用 INF 哨兵简化边界处理，PyPy 下 float('inf') 与 int 比较正常。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 最优/平均/最坏均为 O(n log n) |
| 空间 | O(n) |

### 局限

不稳定、非原地、常数大；实现需维护下标树与哨兵。现代用途主要在理解『复用比较结果的树形选择』与归并排序的 k-路合并思想。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| OI-Wiki | basic/tournament-sort | 3 | 锦标赛排序 | [https://oi-wiki.org/basic/tournament-sort/](https://oi-wiki.org/basic/tournament-sort/) |
| Wikipedia | Tournament_sort | 2 | 锦标赛排序百科 | [https://en.wikipedia.org/wiki/Tournament_sort](https://en.wikipedia.org/wiki/Tournament_sort) |

## Pitfalls · 易错点

- 叶子下标与内部结点下标映射容易错（完全二叉树 1-based 存储）
- 淘汰元素置 INF 后，沿路径重建的起点是 (n+idx)//2，不是 idx
- 相同元素用 ≤ 取左侧胜者，注意与稳定性无关（该算法本身不稳定）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/basic/tournament-sort/](https://oi-wiki.org/basic/tournament-sort/)
- Wikipedia ✓ [https://en.wikipedia.org/wiki/Tournament_sort](https://en.wikipedia.org/wiki/Tournament_sort)
