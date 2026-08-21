---
id: binary-search
name: 二分查找
group: G-A-1
stage: basic
priority: P0
depth_tier: deep
---

# 二分查找

> 有序数组 O(log n) 查找，含 lower_bound/upper_bound

<!-- 元信息: id=binary-search · group=G-A-1 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

二分查找（binary search，折半搜索）在有序数组中 O(log n) 定位元素。核心：每次取中值比较，据此丢弃一半区间。衍生变体：精确查找是否存在、lower_bound（首个 ≥ key 的下标）、upper_bound（首个 > key 的下标）。广义二分：单调布尔条件（满足/不满足）也是『有序』，因此可求『最后一个满足条件的位置』——这是二分答案的基石。迭代实现空间 O(1)。

## Why · 为什么

### 直觉 · Intuition

猜数字游戏：每次问『目标是否 ≥ mid』，答案是非黑即白，区间一分为二。因为数组有序，一次比较能确定目标在左半边还是右半边，把搜索空间指数级缩小。

### 原理 · Principle

不变式：维护区间 [l, r) 使 l 及其左侧均满足条件 P、r 及其右侧均不满足（或相反）。每轮取 mid=(l+r)//2，若 P(mid) 成立则 l=mid（或 l=mid+1），否则 r=mid。循环终止时 l 就是『最后一个满足条件的位置』。lower_bound 用 P(x)=(a[x]>=key)，upper_bound 用 P(x)=(a[x]>key)。中值用 l+(r-l)//2 防止 (l+r) 溢出（Python 无此问题，但代码风格建议）。

### 历史 · History

二分查找思想可追溯至古代（数论与图书馆查书），现代首次成文是 1946 年 John Mauchly；1960 年 D. H. Lehmer 给出第一个无 bug 版本；1962 年发表论文。但它『简单而难写对』，1962 年 Knuth 即指出直到 1960s 才有人写出正确版本。1988 年 John Bentley 在《Programming Pearls》中统计：专业程序员中约 90% 首次写错。

## How · 实现

### 伪代码

```python
lower_bound(a, key):            # 首个下标 i 使 a[i] >= key，不存在返回 n
    l, r = 0, len(a)              # [l, r) 半开区间
    while l < r:
        mid = (l + r) // 2
        if a[mid] < key:
            l = mid + 1
        else:
            r = mid
    return l

upper_bound(a, key):            # 首个下标 i 使 a[i] > key
    ... if a[mid] <= key: l = mid + 1
        else: r = mid

binary_search(a, key):          # 精确查找
    i = lower_bound(a, key)
    return i < len(a) and a[i] == key
```

### Python 实现

```python
def lower_bound(a, key):
    """首个 >= key 的下标；全部小于 key 时返回 len(a)"""
    l, r = 0, len(a)
    while l < r:
        mid = (l + r) // 2
        if a[mid] < key:
            l = mid + 1
        else:
            r = mid
    return l


def upper_bound(a, key):
    """首个 > key 的下标；全部 <= key 时返回 len(a)"""
    l, r = 0, len(a)
    while l < r:
        mid = (l + r) // 2
        if a[mid] <= key:
            l = mid + 1
        else:
            r = mid
    return l


def binary_search(a, key):
    i = lower_bound(a, key)
    return i < len(a) and a[i] == key


def last_leq(a, key):
    """最后一个 <= key 的下标，不存在返回 -1（广义二分示例）"""
    l, r = 0, len(a)
    while l < r:
        mid = (l + r) // 2
        if a[mid] <= key:
            l = mid + 1
        else:
            r = mid
    return l - 1


if __name__ == "__main__":
    import random
    for _ in range(300):
        n = random.randint(0, 60)
        a = sorted(random.randint(0, 30) for _ in range(n))
        key = random.randint(0, 35)
        # 与暴力对照
        assert lower_bound(a, key) == sum(1 for x in a if x < key), (a, key)
        assert upper_bound(a, key) == sum(1 for x in a if x <= key), (a, key)
        expect = key in a
        assert binary_search(a, key) == expect, (a, key)
        le = [i for i, x in enumerate(a) if x <= key]
        assert last_leq(a, key) == (le[-1] if le else -1), (a, key)
    print("lower_bound/upper_bound/精确查找/广义二分 全部正确 OK（300 组随机）")
    a = [1, 2, 2, 2, 3, 5, 8]
    print(f"a={a}, lower_bound(2)={lower_bound(a, 2)}, upper_bound(2)={upper_bound(a, 2)}")
    print(f"binary_search(4)={binary_search(a, 4)}, last_leq(4)={last_leq(a, 4)}")

```

**PyPy 提示**: PyPy 下手写二分与内建 bisect 性能差异不大，但 bisect_left/bisect_right 更少出错，强烈建议直接用。Python 无整数溢出，mid=(l+r)//2 即可。大循环用 bisect 的 C 实现有优势。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(log n) |
| 空间 | O(1) 迭代；O(log n) 递归 |

### 局限

前提是数组有序（或条件单调）。非单调条件无法二分。写错多发生在边界：while l<r vs l<=r、mid+1/mid-1、l=mid vs l=mid+1 的组合。统一用半开区间 [l,r) 与 l=mid+1 策略可系统避免。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P2249 | 2 | lower_bound 模板 | [https://www.luogu.com.cn/problem/P2249](https://www.luogu.com.cn/problem/P2249) |
| LeetCode | 704 / 34 | 2 | 二分查找及查找区间端点 | [https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/](https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/) |
| CP-Algorithms | num_methods/binary_search | 3 | 二分搜索有序数组官方教程 | [https://cp-algorithms.com/num_methods/binary_search.html](https://cp-algorithms.com/num_methods/binary_search.html) |

## Pitfalls · 易错点

- while l < r 却写 mid-1 造成死循环或漏元素
- 精确查找未判越界：lower_bound 返回 len(a) 时直接 a[i] 越界
- lower_bound 与 upper_bound 比较符写反（< vs <=）——它们是孪生错误高发区

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/basic/binary/](https://oi-wiki.org/basic/binary/)
- CP-Algorithms ✓ [https://cp-algorithms.com/num_methods/binary_search.html](https://cp-algorithms.com/num_methods/binary_search.html)
- leetcode ✓ [https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/](https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/)
