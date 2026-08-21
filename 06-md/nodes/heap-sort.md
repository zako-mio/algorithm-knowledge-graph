---
id: heap-sort
name: 堆排序
group: G-A-1
stage: basic
priority: P1
depth_tier: standard
---

# 堆排序

> 基于二叉堆的 O(n log n) 原地排序，不稳定

<!-- 元信息: id=heap-sort · group=G-A-1 · stage=basic · priority=P1 · depth_tier=standard -->

## What · 是什么

堆排序（heapsort）本质是建立在二叉堆上的选择排序：先用 O(n) 建堆，再反复取堆顶（当前最大/最小）与末尾交换并下沉调整。最优/平均/最坏均为 O(n log n)，原地 O(1) 额外空间，不稳定。数组下标约定：i 的父结点 (i-1)//2，左子 2i+1，右子 2i+2。

## Why · 为什么

### 直觉 · Intuition

把数组看成一颗完全二叉树，堆性质保证根是极值。每取一次根 O(log n)，取 n 次共 O(n log n)。建堆从最后一个非叶结点向上做 sink，总代价 O(n)（叶子层不做，越底层结点数越多但下沉次数越少）。

### 原理 · Principle

关键操作 sift_down（下沉）：父结点与较大的子结点交换，直到堆性质满足。建堆 for i in [n//2-1 .. 0] 逐层下沉；排序阶段把堆顶与末尾交换，缩小堆范围后对新堆顶下沉。稳定性被破坏的根源是任意下标交换：相等元素可能越过彼此。

### 历史 · History

二叉堆由 J. W. J. Williams 于 1964 年提出（同时提出 heapsort），同年 R. W. Floyd 给出了 O(n) 建堆方法。堆排序无需额外数组、复杂度严格 O(n log n)，是其相比快排的确定优势；但常数较大且缓存不友好，实际性能通常不如快排/Timsort。

## How · 实现

### 伪代码

```python
sift_down(a, start, end):
    parent = start
    child = 2*parent + 1
    while child <= end:
        if child+1 <= end and a[child] < a[child+1]: child += 1
        if a[parent] >= a[child]: return
        swap(a[parent], a[child])
        parent = child; child = 2*parent + 1

heap_sort(a):
    # 建堆：从最后一个非叶结点开始下沉
    for i in range(n//2 - 1, -1, -1):
        sift_down(a, i, n - 1)
    # 取堆顶放到末尾
    for i in range(n - 1, 0, -1):
        swap(a[0], a[i])
        sift_down(a, 0, i - 1)
```

### Python 实现

```python
def sift_down(a, start, end):
    parent = start
    child = 2 * parent + 1
    while child <= end:
        if child + 1 <= end and a[child] < a[child + 1]:
            child += 1
        if a[parent] >= a[child]:
            return
        a[parent], a[child] = a[child], a[parent]
        parent = child
        child = 2 * parent + 1


def heap_sort(a):
    n = len(a)
    for i in range(n // 2 - 1, -1, -1):
        sift_down(a, i, n - 1)
    for i in range(n - 1, 0, -1):
        a[0], a[i] = a[i], a[0]
        sift_down(a, 0, i - 1)
    return a


if __name__ == "__main__":
    import random
    for _ in range(300):
        arr = [random.randint(0, 100) for _ in range(random.randint(0, 150))]
        b = arr[:]
        heap_sort(b)
        assert b == sorted(arr), (arr, b)
    print("堆排序正确性 OK（300 组随机）")
    print("示例:", heap_sort([5, 3, 8, 1, 2, 7, 4, 6]))

```

**PyPy 提示**: 竞赛中『取前 k 大/第 k 大』优先用内建 heapq（heappush/heappop），不要手写堆排序。堆排序手写时注意 0-based 下标与 1-based 模板混用极易出错。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 最优/平均/最坏均为 O(n log n) |
| 空间 | O(1) 原地 |

### 局限

不稳定；常数大、缓存局部性差，实际速度通常不如快排。若只需维护动态极值，直接用二叉堆/优先队列（heapq）而非堆排序。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| OI-Wiki | basic/heap-sort | 2 | 堆排序数组实现 | [https://oi-wiki.org/basic/heap-sort/](https://oi-wiki.org/basic/heap-sort/) |
| CPH | ch3 p41 | 2 | 堆排序章节 | [https://cses.fi/book/book.pdf](https://cses.fi/book/book.pdf) |

## Pitfalls · 易错点

- 0-based 下标子结点公式 2i+1/2i+2 与 1-based 的 2i/2i+1 混淆
- 建堆起点应为最后一个非叶结点 n//2-1，从 n-1 开始会多做无效下沉
- 排序阶段每次下沉的 end 是 i-1（已排好的尾部不再参与）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/basic/heap-sort/](https://oi-wiki.org/basic/heap-sort/)
- 书籍 ✓ `CPH ch3 p41`
- Wikipedia ✓ [https://zh.wikipedia.org/wiki/堆排序](https://zh.wikipedia.org/wiki/堆排序)
