---
id: merge-sort
name: 归并排序
group: G-A-1
stage: basic
priority: P0
depth_tier: deep
---

# 归并排序

> 分治排序，O(n log n) 稳定排序，可用于求逆序对

<!-- 元信息: id=merge-sort · group=G-A-1 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

归并排序（merge sort）是基于分治的稳定排序算法：把数组一分为二，递归排序两半，再合并两个有序数组。最坏/平均/最优复杂度均为 Θ(n log n)，空间 O(n)。关键操作是 merge（合并两个有序序列）。额外价值：合并过程中可顺便统计逆序对（i<j 且 a[i]>a[j]），复杂度仍为 O(n log n)。

## Why · 为什么

### 直觉 · Intuition

『把大问题切成两半分别排好，再逐个小比，拼起来』。合并两半时只需线性扫描，总代价是每层 O(n) × log n 层 = O(n log n)，且这是严格的、不依赖数据分布——因此归并是理论最优的比较排序之一。

### 原理 · Principle

数学归纳：长度为 1 的数组天然有序；若左右两半已各自有序，合并后整体有序。合并时用『前段首元素 ≤ 后段首元素』（而非 <）保证稳定性——相等时先取前段，则原在前面的元素继续在前。倍增法实现（bottom-up）从长度 1 的段开始逐轮翻倍合并，避免递归栈。

### 历史 · History

1945 年由 John von Neumann 提出，是最早被提出的高效通用排序之一。其在外部排序（磁带排序）中也有应用（多路归并）。求逆序对是其经典工程应用：合并时每当后段元素被取走，前段剩余元素个数就是新发现的逆序对数量。

## How · 实现

### 伪代码

```python
merge_sort(a, l, r):
    if r - l <= 1: return
    mid = (l + r) // 2
    merge_sort(a, l, mid)
    merge_sort(a, mid, r)
    merge(a, l, mid, r)   # 合并 [l,mid) 与 [mid,r)

merge(a, l, mid, r):
    i, j = l, mid; tmp = []
    while i < mid and j < r:
        if a[j] < a[i]: tmp.append(a[j]); j += 1   # 先取后段 → 统计逆序对
        else:           tmp.append(a[i]); i += 1
    tmp += a[i:mid]; tmp += a[j:r]
    a[l:r] = tmp
```

### Python 实现

```python
def merge(a, l, mid, r):
    """合并有序区间 [l,mid) 与 [mid,r)，返回本次合并发现的逆序对数量"""
    i, j = l, mid
    tmp = []
    inv = 0
    while i < mid and j < r:
        if a[j] < a[i]:
            tmp.append(a[j])
            inv += mid - i          # 后段元素比前段剩余所有元素都小 → 逆序对
            j += 1
        else:
            tmp.append(a[i])
            i += 1
    tmp.extend(a[i:mid])
    tmp.extend(a[j:r])
    a[l:r] = tmp
    return inv


def merge_sort(a, l=0, r=None):
    """原地归并排序 [l,r)，返回区间内逆序对数量"""
    if r is None:
        r = len(a)
    if r - l <= 1:
        return 0
    mid = (l + r) // 2
    inv = merge_sort(a, l, mid) + merge_sort(a, mid, r)
    inv += merge(a, l, mid, r)
    return inv


def merge_sort_bottomup(a):
    """倍增（自底向上）实现，避免递归"""
    n = len(a)
    seg = 1
    while seg < n:
        for l1 in range(0, n - seg, seg + seg):
            r1 = l1 + seg
            l2 = r1
            r2 = min(l2 + seg, n)
            merge(a, l1, r1, r2)
        seg <<= 1
    return a


def count_inversions(a):
    """暴力验证用：O(n^2) 数逆序对"""
    return sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > a[j])


if __name__ == "__main__":
    import random
    for _ in range(200):
        arr = [random.randint(0, 30) for _ in range(random.randint(0, 80))]
        b = arr[:]
        inv = merge_sort(b)
        assert b == sorted(arr), (arr, b)
        assert inv == count_inversions(arr), (arr, inv)
    # 稳定性检查
    data = [(random.randint(0, 5), i) for i in range(50)]
    d2 = data[:]
    merge_sort(d2)
    by_val = {}
    for v, i in d2:
        by_val.setdefault(v, []).append(i)
    assert all(seq == sorted(seq) for seq in by_val.values()), "不稳定!"
    print("归并排序正确性 OK（200 组随机含重复值）")
    print("逆序对示例:", merge_sort([5, 3, 2, 4, 1]))
    print("倍增法:", merge_sort_bottomup([5, 3, 2, 4, 1]))

```

**PyPy 提示**: 递归深度 = log n，不会爆栈；PyPy 下切片 a[l:r] 创建新列表较慢，竞赛可改用显式 tmp 数组下标回填。统计逆序对时注意 Python int 无溢出，但要用正确公式 mid - i。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 最优/平均/最坏均为 Θ(n log n) |
| 空间 | O(n)（辅助数组） |

### 局限

非原地排序（需要 O(n) 辅助空间）；对缓存不友好（与快排相比常数大）。但稳定、复杂度严格保证，且天然支持外部排序。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1908 | 3 | 归并排序求逆序对 | [https://www.luogu.com.cn/problem/P1908](https://www.luogu.com.cn/problem/P1908) |
| OI-Wiki | basic/merge-sort | 2 | 归并排序含倍增法 | [https://oi-wiki.org/basic/merge-sort/](https://oi-wiki.org/basic/merge-sort/) |

## Pitfalls · 易错点

- 合并时用 < 而非 ≤ 会破坏稳定性（相等时取了后段）
- 倍增法最后一段长度可能不完整，右边界用 min(l2+seg, n) 否则越界
- 递归区间 [l,r) 与 [l,mid),[mid,r) 混淆导致元素丢失或重复

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/basic/merge-sort/](https://oi-wiki.org/basic/merge-sort/)
- 书籍 ✓ `CPH ch3 p35`
- OI Wiki ✓ [https://www.luogu.com.cn/problem/P1908](https://www.luogu.com.cn/problem/P1908)
