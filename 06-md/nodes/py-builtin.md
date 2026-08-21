---
id: py-builtin
name: 内置库利用
group: G-E-3
stage: intermediate
priority: P0
depth_tier: deep
---

# 内置库利用

> bisect二分/heapq堆/collections.deque双端队列/itertools排列组合/math.gcd等竞赛常用内置库

<!-- 元信息: id=py-builtin · group=G-E-3 · stage=intermediate · priority=P0 · depth_tier=deep -->

## What · 是什么

Python 标准库提供竞赛常用算法的直接实现，调用内置库比手写更快更不易错。核心库：bisect（二分查找/插入）、heapq（最小堆优先队列）、collections.deque（O(1) 双端队列，BFS 必备）、itertools（permutations/combinations/product 排列组合枚举）、math（gcd/lcm/comb/isqrt/factorial 数论与数学函数）、array（紧凑定长数组省内存）、functools（lru_cache 记忆化）。这些库均 C 实现，比 Python 手写快数十倍。

## Why · 为什么

### 直觉 · Intuition

竞赛中要写二分、堆、BFS 队列、排列组合等通用组件，手写不仅慢还易错。Python 把这些高频算法做成了标准库 C 实现——一行 import 就拿到经过千锤百炼的正确代码，比从零写快几十倍且零 bug。这是 Python 竞赛的最大优势之一：不用背模板。

### 原理 · Principle

标准库均在 C 层实现：bisect 用二分搜索维护有序序列；heapq 用数组模拟二叉小根堆，heappush/heappop O(log n)；collections.deque 用双向链表/环形数组，popleft/appendleft 均 O(1)（list.pop(0) 是 O(n)！）；itertools 的 permutations/combinations/product 用 C 迭代器无中间列表，省内存；math.gcd 用二进制 GCD，math.comb 内部用优化乘法。

### 历史 · History

Python 标准库长期积累。bisect 自 Python 2.1；heapq 自 2.3；collections.deque 自 2.4；itertools 自 2.3；math.gcd 自 3.5；math.comb/lcm/isqrt 自 3.8-3.9。OI Wiki Python 页有常用内置库表格。

## How · 实现

### 伪代码

```python
import bisect, heapq, collections, itertools, math

# 二分查找
pos = bisect.bisect_left(sorted_lst, x)  # 第一个>=x 的位置

# 优先队列（最小堆）
hq = []; heapq.heappush(hq, (dist, node))
val = heapq.heappop(hq)

# BFS 双端队列
q = collections.deque([start]); q.popleft()  # O(1)

# 排列组合
for p in itertools.permutations(range(n), k): ...
for c in itertools.combinations(range(n), k): ...

# 数论
math.gcd(a, b); math.lcm(a, b); math.comb(n, k); math.isqrt(n)
```

### Python 实现

```python
# Python 竞赛常用内置库（含自测）
import bisect
import heapq
import collections
import itertools
import math

def bisect_demo():
    a = [1, 3, 3, 5, 7, 9]
    # bisect_left: 第一个 >= 3 的位置
    assert bisect.bisect_left(a, 3) == 1
    # bisect_right: 第一个 > 3 的位置
    assert bisect.bisect_right(a, 3) == 3
    # insort 保持有序插入
    b = [1, 3, 5]
    bisect.insort(b, 4)
    assert b == [1, 3, 4, 5]

def heap_demo():
    h = []
    for v in [5, 3, 7, 1]:
        heapq.heappush(h, v)
    assert heapq.heappop(h) == 1  # 最小值
    # 堆化 + nlargest/nsmallest
    data = [3, 1, 4, 1, 5, 9, 2, 6]
    heapq.heapify(data)
    assert heapq.nsmallest(3, data) == [1, 1, 2]
    assert heapq.nlargest(2, data) == [9, 6]

def deque_demo():
    q = collections.deque([1, 2, 3])
    q.appendleft(0)
    q.append(4)
    assert list(q) == [0, 1, 2, 3, 4]
    assert q.popleft() == 0  # O(1)，list.pop(0) 是 O(n)!
    # BFS 典型用法
    dist = {0: 0}
    q = collections.deque([0])
    while q:
        u = q.popleft()

def itertools_demo():
    # 排列
    perms = list(itertools.permutations([1, 2, 3], 2))
    assert perms == [(1,2),(1,3),(2,1),(2,3),(3,1),(3,2)]
    # 组合
    combs = list(itertools.combinations([1,2,3,4], 2))
    assert len(combs) == 6
    # 笛卡尔积
    prod = list(itertools.product([0,1], repeat=3))
    assert len(prod) == 8
    # accumulate 前缀和
    acc = list(itertools.accumulate([1,2,3,4]))
    assert acc == [1, 3, 6, 10]

def math_demo():
    assert math.gcd(12, 18) == 6
    assert math.lcm(4, 6) == 12
    assert math.comb(10, 3) == 120
    assert math.isqrt(100) == 10
    assert math.isqrt(99) == 9  # 整数平方根向下取整
    assert math.factorial(5) == 120

if __name__ == "__main__":
    bisect_demo()
    heap_demo()
    deque_demo()
    itertools_demo()
    math_demo()
    print("py-builtin OK")

```

**PyPy 提示**: PyPy 下这些标准库同样可用且优化得当。heapq/deque 在 PyPy 下性能优秀。注意 PyPy 对 itertools 的某些函数有额外优化。collections.deque 在两个实现下都是 O(1) 双端操作——务必用它而非 list 做 BFS 队列（list.pop(0) 是 O(n)）。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | bisect O(log n)；heapq push/pop O(log n)；deque 双端 O(1)；itertools 枚举 O(结果数)；math.gcd O(log min(a,b)) |
| 空间 | 按使用，通常 O(n) |

### 局限

1) heapq 只能做最小堆，最大堆需取负或自定义 __lt__；2) deque 不支持 O(1) 中间随机删除；3) itertools 排列组合结果数爆炸（P(n,k) 可达 n!），大 n 会超时；4) math.comb 不取模，大组合数位数爆炸。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1496 | 3 | BFS 最短步数，deque 做 O(1) 队列 | [https://www.luogu.com.cn/problem/P1496](https://www.luogu.com.cn/problem/P1496) |
| Luogu | P1093 | 3 | heapq.nlargest 或 sorted 取前 K | [https://www.luogu.com.cn/problem/P1093](https://www.luogu.com.cn/problem/P1093) |
| LeetCode | 46 | 3 | itertools.permutations 一行解决，面试应手写回溯 | [https://leetcode.cn/problems/permutations/](https://leetcode.cn/problems/permutations/) |

## Pitfalls · 易错点

- BFS 用 list 当队列 list.pop(0) 是 O(n) → 用 collections.deque
- heapq 做最大堆忘取负 → heappush(-val) + heappop 取负
- itertools.permutations 大 n 超时（n! 爆炸）→ 先判断可行性
- math.comb 大组合数不取模位数爆炸 → 取模时手写或用 Lucas
- bisect 作用于无序列表 → 结果无意义，必须先 sort

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/lang/python/](https://oi-wiki.org/lang/python/)
- web ✓ [https://docs.python.org/3/library/index.html](https://docs.python.org/3/library/index.html)
