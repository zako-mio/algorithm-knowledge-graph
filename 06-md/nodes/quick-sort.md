---
id: quick-sort
name: 快速排序
group: G-A-1
stage: basic
priority: P0
depth_tier: deep
---

# 快速排序

> 分治排序，期望 O(n log n)，最坏 O(n^2)，常数小

<!-- 元信息: id=quick-sort · group=G-A-1 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

快速排序（quicksort）通过选取基准（pivot）把数组划分为『小于/大于』两部分后递归排序。期望/平均 O(n log n)，最坏 O(n^2)（每次取到最值做基准），空间 O(log n)（递归栈）。非稳定排序。工程上通过随机基准、三数取中、插入排序兜底、三路划分等优化，是 C 库 qsort 与多数语言内建排序的基础。

## Why · 为什么

### 直觉 · Intuition

『选一个中间数，把小的放左边、大的放右边，然后只负责把两边各自排好』。与归并不同，划分本身就在『修位置』，所以无需合并步骤。平均情况下每个元素被比较约 O(log n) 次，故总代价 O(n log n)。

### 原理 · Principle

期望复杂度证明（经典引理）：设 X 为总比较次数，第 i 小与第 j 小的元素发生比较当且仅当两者之一是最先被选为基准的，概率 2/(j-i+1)。由期望线性性 E[X]=Σ 2/(j-i+1) = O(n log n)。最坏情况（每次基准都是极值）递推 T(n)=T(n-1)+Θ(n)=Θ(n^2)。三路快排（荷兰国旗划分）把相等元素集中到中间，处理大量重复值时最优可达 O(n)。

### 历史 · History

1960 年由 Tony Hoare 发明，并在 Algol 中实现，是『快排』名字的来源。因其缓存局部性好、常数小，成为实用排序的首选。2009 年前后 Java 等标准库开始转向 Timsort/introsort，C++ std::sort 用 introsort（快排+堆排混合）保证最坏 O(n log n)。

## How · 实现

### 伪代码

```python
quick_sort(a, l, r):            # 排序 [l, r)
    if r - l <= 1: return
    p = partition(a, l, r)        # 划分，返回基准最终下标
    quick_sort(a, l, p)
    quick_sort(a, p + 1, r)

partition(a, l, r):               # Lomuto 划分
    pivot = a[r - 1]
    i = l
    for j in range(l, r - 1):
        if a[j] < pivot:
            swap(a, i, j); i += 1
    swap(a, i, r - 1)
    return i
```

### Python 实现

```python
import random


def partition(a, l, r):
    """Lomuto 划分，基准取区间最后一个元素，返回基准最终位置"""
    pv = a[r - 1]
    i = l
    for j in range(l, r - 1):
        if a[j] < pv:
            a[i], a[j] = a[j], a[i]
            i += 1
    a[i], a[r - 1] = a[r - 1], a[i]
    return i


def quick_sort(a, l=0, r=None):
    """快速排序 [l,r)，随机基准（期望 O(n log n)，防毒瘤数据卡成 O(n^2)）"""
    if r is None:
        r = len(a)
    if r - l <= 1:
        return a
    p = random.randrange(l, r)
    a[l], a[p] = a[p], a[l]
    p = partition(a, l, r)
    quick_sort(a, l, p)
    quick_sort(a, p + 1, r)
    return a


def quick_select(a, k, l=0, r=None):
    """快速选择：返回第 k 小元素（0-based），期望 O(n)"""
    if r is None:
        r = len(a)
    while True:
        p = random.randrange(l, r)
        a[l], a[p] = a[p], a[l]
        p = partition(a, l, r)
        if p == k:
            return a[p]
        if p < k:
            l = p + 1
        else:
            r = p


def quick_sort_3way(a, l=0, r=None):
    """三路快排：处理大量重复值不退化（荷兰国旗划分）"""
    if r is None:
        r = len(a)
    if r - l <= 1:
        return a
    p = random.randrange(l, r)
    a[l], a[p] = a[p], a[l]
    pv = a[l]
    lt, gt = l, r
    i = l
    while i < gt:
        if a[i] < pv:
            a[i], a[lt] = a[lt], a[i]
            lt += 1
            i += 1
        elif a[i] > pv:
            gt -= 1
            a[i], a[gt] = a[gt], a[i]
        else:
            i += 1
    quick_sort_3way(a, l, lt)
    quick_sort_3way(a, gt, r)
    return a


if __name__ == "__main__":
    random.seed(42)
    for _ in range(300):
        arr = [random.randint(0, 50) for _ in range(random.randint(0, 120))]
        b = arr[:]
        quick_sort(b)
        assert b == sorted(arr), (arr, b)
        b3 = arr[:]
        quick_sort_3way(b3)
        assert b3 == sorted(arr), (arr, b3)
        if arr:
            k = random.randrange(len(arr))
            assert quick_select(arr[:], k) == sorted(arr)[k], (arr, k)
    print("快排 / 三路快排 / 快速选择 全部正确 OK（300 组随机）")
    print("第 3 小（0-based）示例:", quick_select([3, 1, 4, 1, 5, 9, 2, 6], 3))

```

**PyPy 提示**: 递归深度最坏 O(n) 会爆栈，比赛可改成非递归（显式栈存区间）或随机化。Python 递归开销大，n 很大时手写循环式快排更稳。切片式快排（list 推导式分区）简洁但额外 O(n) 空间且慢，不推荐用于大 n。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 期望/平均 O(n log n)，最坏 O(n^2)，三路快排含重复值最优 O(n) |
| 空间 | O(log n) 期望（递归栈），最坏 O(n) |

### 局限

不稳定；朴素实现最坏 O(n^2) 会被毒瘤数据卡；需配合随机化/三数取中/三路划分。快速选择（partition 定位第 k 大）是重要衍生技巧。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1177 | 3 | 快速排序模板（需优化防卡） | [https://www.luogu.com.cn/problem/P1177](https://www.luogu.com.cn/problem/P1177) |
| OI-Wiki | basic/quick-sort | 2 | 快排期望复杂度证明 | [https://oi-wiki.org/basic/quick-sort/](https://oi-wiki.org/basic/quick-sort/) |

## Pitfalls · 易错点

- 朴素选取首个元素做基准在升序/降序输入下退化为 O(n^2)，必须随机化或三数取中
- Lomuto 划分对全相同元素退化为 O(n^2)（三路划分解决）
- partition 返回值边界处理错误导致死循环（如区间未收敛）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/basic/quick-sort/](https://oi-wiki.org/basic/quick-sort/)
- 书籍 ✓ `CPH ch3 p38`
- OI Wiki ✓ [https://www.luogu.com.cn/problem/P1177](https://www.luogu.com.cn/problem/P1177)
