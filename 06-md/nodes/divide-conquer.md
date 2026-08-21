---
id: divide-conquer
name: 分治与递归
group: G-A-1
stage: basic
priority: P0
depth_tier: deep
---

# 分治与递归

> 分解-解决-合并，递归处理子问题

<!-- 元信息: id=divide-conquer · group=G-A-1 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

分治（divide and conquer）三步：分解（把原问题拆成同类子问题）、解决（递归求解，到最小子问题直接给答案）、合并（把子问题解拼成原问题解）。递归是它的实现载体：两个特征——终止条件 + 自我调用。经典应用：归并排序、快速排序、最大子段和、最近点对、CDQ 分治、分治 DP 优化、FFT。复杂度常由主定理（Master Theorem）刻画：T(n)=aT(n/b)+f(n)。

## Why · 为什么

### 直觉 · Intuition

『要理解递归，就得先理解递归』。递归把问题规模缩小交给同一函数处理，只关心『把大问题切成小问题 + 合并结果』这两步，小问题如何解决不用操心（它自己会递归）。

### 原理 · Principle

主定理：T(n)=aT(n/b)+Θ(n^d)。若 d>log_b a，T(n)=Θ(n^d)；若 d<log_b a，T(n)=Θ(n^(log_b a))；若相等，T(n)=Θ(n^d log n)。归并排序 T(n)=2T(n/2)+Θ(n) → Θ(n log n)。递归代价：每层栈帧 O(1)，深度 O(log n)（二分型）到 O(n)（线性型），深递归可能爆栈（Python 默认递归限制 ~1000）。

### 历史 · History

分治思想自古已有（欧几里得算法、古印度『Chakravala』），作为算法范式由 von Neumann（归并 1945）、Strassen（矩阵乘 1969）、Karatsuba（大数乘 1960）等经典成果确立。1967 年 Bentley 提出主定理思想，1987 年 Cormen 等人在 CLRS 中系统化。现代竞赛的分治范式包括 CDQ 分治、整体二分、点分治、分治 FFT。

## How · 实现

### 伪代码

```python
分治通用骨架:
solve(problem):
    if 最小规模: return 直接答案          # 终止条件
    (p1, p2, ...) = 分解(problem)         # 分解
    s1 = solve(p1); s2 = solve(p2) ...    # 解决（自我调用）
    return 合并(s1, s2, ...)              # 合并
```

### Python 实现

```python
import sys
sys.setrecursionlimit(10 ** 6)


def rec_factorial(n):
    """递归经典示例：阶乘（终止条件 n<=1）"""
    return 1 if n <= 1 else n * rec_factorial(n - 1)


def max_subarray(a, l, r):
    """分治最大子段和：跨越中点的最大段 = 左端后缀 + 右端前缀"""
    if r - l == 1:
        return a[l]
    mid = (l + r) // 2
    left_best = max_subarray(a, l, mid)
    right_best = max_subarray(a, mid, r)
    # 求跨中点的最大和：后缀必须包含 a[mid-1]、前缀必须包含 a[mid]
    best_l = cur = a[mid - 1]
    for i in range(mid - 2, l - 1, -1):
        cur += a[i]
        best_l = max(best_l, cur)
    best_r = cur = a[mid]
    for i in range(mid + 1, r):
        cur += a[i]
        best_r = max(best_r, cur)
    return max(left_best, right_best, best_l + best_r)


def merge_count(a, l, mid, r):
    """归并两段并返回逆序对（分治应用示例，同 merge-sort）"""
    i, j = l, mid
    tmp, inv = [], 0
    while i < mid and j < r:
        if a[j] < a[i]:
            tmp.append(a[j]); inv += mid - i; j += 1
        else:
            tmp.append(a[i]); i += 1
    tmp.extend(a[i:mid]); tmp.extend(a[j:r])
    a[l:r] = tmp
    return inv


def count_inversions(a, l=0, r=None):
    if r is None:
        r = len(a)
    if r - l <= 1:
        return 0
    mid = (l + r) // 2
    return count_inversions(a, l, mid) + count_inversions(a, mid, r) + merge_count(a, l, mid, r)


if __name__ == "__main__":
    assert rec_factorial(10) == 3628800
    assert max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4], 0, 9) == 6
    import random
    for _ in range(300):
        arr = [random.randint(-50, 50) for _ in range(random.randint(1, 100))]
        # 暴力最大子段
        best = -10 ** 18
        for i in range(len(arr)):
            s = 0
            for j in range(i, len(arr)):
                s += arr[j]
                best = max(best, s)
        assert max_subarray(arr, 0, len(arr)) == best, (arr, max_subarray(arr, 0, len(arr)), best)
        inv = sum(1 for i in range(len(arr)) for j in range(i + 1, len(arr)) if arr[i] > arr[j])
        assert count_inversions(arr[:]) == inv, arr
    print("分治（阶乘/最大子段和/逆序对）正确性 OK（300 组暴力对照）")
    print("最大子段和示例:", max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4], 0, 9))

```

**PyPy 提示**: 深递归（线性型，如链表翻转）在 PyPy/CPython 都可能爆栈，用 sys.setrecursionlimit 提高或改迭代。二分型递归深度 O(log n) 安全。分治合并阶段避免频繁切片，用下标区间。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 由主定理决定：归并 O(n log n)、最大子段和 O(n log n)、逆序对 O(n log n) |
| 空间 | 递归栈 O(log n)（二分型）+ 合并辅助空间 |

### 局限

递归调用有栈与函数调用开销；合并步骤处理不当会引入 O(n) 额外成本。非平衡切分（如快排最坏）导致深度 O(n)。递归层级过深可改显式栈/迭代。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| OI-Wiki | basic/divide-and-conquer | 3 | 递归与分治讲解 | [https://oi-wiki.org/basic/divide-and-conquer/](https://oi-wiki.org/basic/divide-and-conquer/) |
| Luogu | P1226 | 2 | 快速幂模板 | [https://www.luogu.com.cn/problem/P1226](https://www.luogu.com.cn/problem/P1226) |
| CPH | ch3 p35 | 2 | 排序分治应用 | [https://cses.fi/book/book.pdf](https://cses.fi/book/book.pdf) |

## Pitfalls · 易错点

- 缺少终止条件 → 无限递归（栈溢出）
- 分解/合并与递归子问题边界重叠或遗漏（[l,mid),[mid,r) 约定统一）
- 忽略递归深度对栈的限制，Python 默认 ~1000 层

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/basic/divide-and-conquer/](https://oi-wiki.org/basic/divide-and-conquer/)
- 书籍 ✓ `CPH ch3 p35`
- OI Wiki ✓ [https://www.luogu.com.cn/problem/P1226](https://www.luogu.com.cn/problem/P1226)
