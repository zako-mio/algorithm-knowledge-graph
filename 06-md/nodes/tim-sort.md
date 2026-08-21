---
id: tim-sort
name: Timsort
group: G-A-1
stage: intermediate
priority: P3
depth_tier: brief
---

# Timsort

> 归并+插入混合稳定排序，Python/Java 标准库使用

<!-- 元信息: id=tim-sort · group=G-A-1 · stage=intermediate · priority=P3 · depth_tier=brief -->

## What · 是什么

Timsort 是 2002 年 Tim Peters 为 Python 设计的混合稳定排序，结合插入排序与归并排序，并针对『已存在有序段（Run）』做优化：识别 Run → 不足 MIN_RUN 用插入排序扩展 → 用栈+特定归并规则（galloping 加速）合并相邻 Run。已有序数据接近 O(n)，最坏 O(n log n)，空间 O(n)。是 Python、Java SE7+ 对象数组、GNU Swift 的默认排序。

## Why · 为什么

### 直觉 · Intuition

真实数据常有大量部分有序段。Timsort 先把这些天然有序段找出来（升序直接用、降序反转），再把它们高效合并——就像人类对『大半已排好的牌』补几张牌而不是全盘重排。

### 原理 · Principle

三个关键设计：①Run 识别：升序段直接取，降序段反转；长度不足 MIN_RUN（32~64，按 n 计算）用二分插入排序扩展。②栈归并规则：压入 Run 后检查栈顶 X,Y,Z 满足 len(Z)>len(Y)+len(X) 且 len(Y)>len(X)，否则合并较小的相邻对，保证归并平衡（防斐波那契式退化，见 ESA 2018 最坏情况论文）。③Galloping：当一侧连续赢 ≥Min_Gallop(7) 次就进入加速模式，用指数查找+二分查找批量搬移元素，动态调整 Min_Gallop。

### 历史 · History

2002 年 Tim Peters 在 Python 2.3 引入，Python 内建 sort 至今用它；2009 年 Java SE 7 用于非原始类型数组；也被 Android、GNU Swift 采用。其最坏情况复杂度直到 2015 年才由 Augusteijn 等给出严格证明（论文《On the Worst-Case Complexity of TimSort》，ESA 2018）。

## How · 实现

### 伪代码

```python
tim_sort(a):
    nRemaining = len(a)
    minRun = compute_min_run(n)          # 32~64
    start = 0
    while nRemaining > 0:
        runLen = 识别天然 Run（不足 minRun 用插入排序补齐到 minRun）
        push (start, runLen) 到栈
        merge_collapse(栈)               # 保证堆叠平衡
        start += runLen; nRemaining -= runLen
    merge_force_collapse(栈)
    return a
```

### Python 实现

```python
MIN_RUN = 32


def binary_insertion_sort(a, lo, hi):
    """二分插入排序区间 [lo, hi)，用于补齐小 Run"""
    for i in range(lo + 1, hi):
        key = a[i]
        # 二分找插入点（lo, i] 区间已有序）
        l, r = lo, i
        while l < r:
            m = (l + r) // 2
            if a[m] <= key:
                l = m + 1
            else:
                r = m
        for j in range(i, l, -1):
            a[j] = a[j - 1]
        a[l] = key


def count_run(a, lo):
    """识别从 lo 开始的天然 Run，降序则反转，返回 Run 的结束下标"""
    n = len(a)
    if lo + 1 >= n:
        return lo + 1
    if a[lo] <= a[lo + 1]:           # 升序
        hi = lo + 1
        while hi + 1 < n and a[hi] <= a[hi + 1]:
            hi += 1
    else:                            # 降序 → 反转成升序
        hi = lo + 1
        while hi + 1 < n and a[hi] > a[hi + 1]:
            hi += 1
        a[lo:hi + 1] = a[lo:hi + 1][::-1]
    return hi + 1


def merge_runs(a, lo, mid, hi):
    """合并两个相邻有序段 [lo,mid) 与 [mid,hi)"""
    left = a[lo:mid]
    i, j, k = 0, mid, lo
    while i < len(left) and j < hi:
        if a[j] < left[i]:
            a[k] = a[j]; j += 1
        else:
            a[k] = left[i]; i += 1
        k += 1
    while i < len(left):
        a[k] = left[i]; i += 1; k += 1


def tim_sort(a):
    """简化版 Timsort：识别 Run + 插入补齐 + 归并所有 Run"""
    n = len(a)
    if n <= 1:
        return a
    runs = []
    lo = 0
    while lo < n:
        hi = count_run(a, lo)
        if hi - lo < MIN_RUN:
            hi = min(lo + MIN_RUN, n)
            binary_insertion_sort(a, lo, hi)
        runs.append((lo, hi))
        lo = hi
    while len(runs) > 1:
        new_runs = []
        for k in range(0, len(runs) - 1, 2):
            merge_runs(a, runs[k][0], runs[k][1], runs[k + 1][1])
            new_runs.append((runs[k][0], runs[k + 1][1]))
        if len(runs) % 2:
            new_runs.append(runs[-1])
        runs = new_runs
    return a


if __name__ == "__main__":
    import random
    for _ in range(200):
        arr = [random.randint(0, 200) for _ in range(random.randint(0, 150))]
        b = arr[:]
        tim_sort(b)
        assert b == sorted(arr), (arr, b)
    near_sorted = list(range(5000))
    near_sorted[2500], near_sorted[2501] = near_sorted[2501], near_sorted[2500]
    b = near_sorted[:]
    tim_sort(b)
    assert b == sorted(near_sorted)
    print("简化 Timsort 正确性 OK（200 组随机 + 近乎有序）")
    print("示例:", tim_sort([3, 7, 4, 9, 5, 2, 6, 1]))

```

**PyPy 提示**: 比赛中不需要手写 Timsort——Python 内建 list.sort 就是它。本实现为教学简化版，去掉了 galloping 与栈平衡规则，仅演示 Run 识别+插入补齐+归并骨架。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 已有序 O(n)，最坏 O(n log n) |
| 空间 | O(n) |

### 局限

真实实现（galloping、mergeCollapse 栈规则、Min_Gallop 动态调整）相当复杂，比赛中应直接用内建 sort；理解其原理有助于写出对有序数据更友好的代码。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| OI-Wiki | basic/tim-sort | 3 | Timsort 伪代码与归并规则 | [https://oi-wiki.org/basic/tim-sort/](https://oi-wiki.org/basic/tim-sort/) |
| CPython | Objects/listsort.txt | 3 | Tim Peters 原始说明 | [https://github.com/python/cpython/blob/main/Objects/listsort.txt](https://github.com/python/cpython/blob/main/Objects/listsort.txt) |

## Pitfalls · 易错点

- 不要把 Timsort 简单理解为『插入+归并』——栈平衡与 galloping 决定其最坏复杂度保证
- 降序 Run 识别时要先判断 a[lo]<=a[lo+1] 再区分升/降，边界处 lo+1 可能越界
- 简化实现省略 mergeCollapse 后，最坏情况内存/时间可能不再严格受控

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/basic/tim-sort/](https://oi-wiki.org/basic/tim-sort/)
- github ✓ [https://github.com/python/cpython/blob/main/Objects/listsort.txt](https://github.com/python/cpython/blob/main/Objects/listsort.txt)
- Wikipedia ✓ [https://en.wikipedia.org/wiki/Timsort](https://en.wikipedia.org/wiki/Timsort)
