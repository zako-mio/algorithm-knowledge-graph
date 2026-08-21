---
id: sort-intro
name: 排序基础概念
group: G-A-1
stage: basic
priority: P0
depth_tier: deep
---

# 排序基础概念

> 排序算法总览：稳定性、复杂度、比较与非比较排序的分类

<!-- 元信息: id=sort-intro · group=G-A-1 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

排序算法（sorting algorithm）是把一组数据按某种顺序（如升序/降序）排列的算法。本节点是排序主题的总览，重点掌握三件事：①稳定性（stable）概念——相等元素排序后相对顺序是否改变；②时间复杂度（尤其最坏情况）如何衡量；③比较排序（comparison sort）与非比较排序（non-comparison sort）的分类。基于比较的排序在最坏情况下存在 Ω(n log n) 的比较次数下界；而非比较排序（计数/桶/基数）利用键值的额外结构，可在 O(n+w) 等线性时间内完成。

## Why · 为什么

### 直觉 · Intuition

先建立排序的全局坐标系：稳定/不稳定、最优/平均/最坏复杂度、比较型/非比较型。例如：只要两个元素相等就涉及稳定性，而稳定性在计数排序中决定了能否保留原始相对顺序。比赛中最常用的是 Python 内建 sort（Timsort）与手写快排/归并，理解分类能帮你快速选择工具。

### 原理 · Principle

稳定性：若 R 与 S 键值相等且原列表中 R 在 S 前，排序后 R 仍在 S 前则称该排序稳定。基于比较的排序最坏复杂度下界：任意基于『两两比较』、每次比较二选一的决策树至多有 2^k 个叶子，要区分 n! 种排列需要 k ≥ log2(n!) = Ω(n log n) 次比较。计数排序 O(n+w) 不违背该下界，因为它不是比较排序。OI 竞赛一般只看最坏复杂度，因为它界定了评测不可能更差的表现。

### 历史 · History

排序是计算机科学最古老的算法主题之一。冒泡/插入/选择属于早期教学算法；归并排序 1945 年由 von Neumann 提出；快速排序 1959 年由 C. A. R. Hoare 提出；堆排序 1964 年由 J. W. J. Williams 提出。非比较排序（计数、基数）源于打孔卡片机的卡片排序问题。2002 年 Tim Peters 为 Python 设计了 Timsort，此后 Java、Android、GNU Swift 等标准库相继采用。

## How · 实现

### 伪代码

```python
# 稳定性判定
对每个键值相等的元素对 (i<j, a[i]==a[j])，检查排序后 i 是否仍在 j 之前。

# 复杂度衡量
统计基本操作（比较/交换/赋值）次数随 n 增长的量级。
```

### Python 实现

```python
def is_stable_sort(sort_fn, arr):
    """检测排序算法是否稳定：对带索引的元素排序，检查相同键值是否保持相对顺序"""
    indexed = [(v, i) for i, v in enumerate(arr)]
    sort_fn(indexed, lambda x: x[0])
    # 相同值 v 的索引序列应严格递增才稳定
    by_val = {}
    for v, i in indexed:
        by_val.setdefault(v, []).append(i)
    return all(seq == sorted(seq) for seq in by_val.values())


def stable_demo():
    """用 Python 内建 sort（Timsort，稳定）演示"""
    arr = [(3, 'a'), (1, 'x'), (3, 'b'), (2, 'y')]
    arr.sort(key=lambda x: x[0])
    return arr


def complexity_table():
    """常用排序复杂度总览（最坏情况）"""
    table = [
        ("冒泡/选择/插入", "O(n^2)", "稳定/不稳定/稳定", "比较型"),
        ("归并排序", "O(n log n)", "稳定", "比较型"),
        ("快速排序", "O(n^2)（期望 O(n log n)）", "不稳定", "比较型"),
        ("堆排序", "O(n log n)", "不稳定", "比较型"),
        ("计数排序", "O(n+w)", "稳定", "非比较型"),
        ("基数排序", "O(d(n+k))", "稳定", "非比较型"),
        ("桶排序", "O(n)（均匀分布时）", "视内层排序而定", "非比较型"),
    ]
    return table


if __name__ == "__main__":
    assert is_stable_sort(lambda a, k: a.sort(key=k), [4, 1, 3, 4, 2, 1])
    print("稳定排序检测 OK")
    print("稳定排序演示:", stable_demo())
    for row in complexity_table():
        print("  ".join(row))

```

**PyPy 提示**: PyPy 中列表 sort 仍为 Timsort；手写排序（快排/归并）在 PyPy 上同样可用但常数略高。比赛中优先内建 sort，需要稳定 + 自定义键时用 key 参数而非 cmp。计数排序在值域 w 与 n 同量级时用 Python 的 dict 计数或直接 list 皆可，PyPy 下 list 计数更快。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 比较排序最坏 Ω(n log n)；计数排序 O(n+w)；基数排序 O(d(n+k))；桶排序平均 O(n) |
| 空间 | 依赖具体算法，见各子节点 |

### 局限

没有万能排序：比较排序受 n log n 下界约束；非比较排序需要键值可离散化且值域可控。稳定性并非所有场景必需，但计数排序的『从右往左填』实现恰依赖稳定性来保证正确。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| OI-Wiki | basic/sort-intro | 2 | 排序简介 | [https://oi-wiki.org/basic/sort-intro/](https://oi-wiki.org/basic/sort-intro/) |
| CPH | ch3 p35 | 2 | 排序与复杂度 | [https://cses.fi/book/book.pdf](https://cses.fi/book/book.pdf) |

## Pitfalls · 易错点

- 混淆『平均复杂度』与『最坏复杂度』：快排平均 O(n log n) 但最坏 O(n^2)，评测数据可构造卡死朴素实现
- 误以为计数排序也是基于比较：它利用键值范围，故可突破 n log n 下界
- 把稳定性当『性能』：稳定性只是相等元素的相对顺序属性，与速度无关

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/basic/sort-intro/](https://oi-wiki.org/basic/sort-intro/)
- 书籍 ✓ `CPH ch3 p35`
- Wikipedia ✓ [https://zh.wikipedia.org/wiki/排序算法](https://zh.wikipedia.org/wiki/排序算法)
