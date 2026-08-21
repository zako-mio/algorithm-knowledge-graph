---
id: discrete
name: 离散化
group: G-E-7
stage: basic
priority: P0
depth_tier: deep
---

# 离散化

> 大值域映射到紧凑排名：排序+去重+lower_bound，保持偏序关系，压缩数组下标

<!-- 元信息: id=discrete · group=G-E-7 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

离散化(Discretization)是一种将大值域数据映射到紧凑连续排名的技巧：将原始值排序去重后，用每个值在有序序列中的位置(排名)代替原始值。映射后保持偏序关系(x<y ⟺ rank(x)<rank(y))，但值域从 10^9 压缩到 n 级别，使得数组下标可用。

## Why · 为什么

### 直觉 · Intuition

树状数组/线段数组需要用值做下标，但值域可能 10^9(甚至 10^18)。直接开数组会 MLE。但实际不同的值最多 n 个，只需把它们映射到 [1,n] 即可。离散化本质是一种保序哈希：大值→小排名，但大小关系不变。

### 原理 · Principle

①复制原数组 ②排序副本 ③去重(unique) ④对原数组每个值，用 lower_bound 在去重数组中找排名。方法一(同值同排名): sort + unique + lower_bound。方法二(同值不同排名，按出现顺序): 用 pair(val, idx) 排序，val 相同时按 idx 排。两者均 O(n log n)。

### 历史 · History

离散化是竞赛中极其常用的预处理技巧，几乎所有值域大于数组可开范围的问题都需要。OI Wiki 将其归为杂项技巧。与哈希的区别在于离散化保持偏序关系，而哈希不一定。

## How · 实现

### 伪代码

```python
# 方法一: 同值同排名(常用)
tmp = sorted(set(arr))  # 排序+去重
for i in range(n):
  arr[i] = lower_bound(tmp, arr[i])  # 查排名

# 方法二: 同值不同排名(按出现顺序)
pairs = [(arr[i], i) for i in range(n)]
pairs.sort(key=lambda x: (x[0], x[1]))  # 值相同时按原始位置
for rank, (val, idx) in enumerate(pairs):
  arr[idx] = rank  # 排名从0或1开始
```

### Python 实现

```python
import bisect


def discretize_same(arr):
    """离散化方法一: 相同的值离散化为相同的排名。
    返回离散化后的数组(1-indexed排名)。
    保持偏序: x < y => rank(x) < rank(y)
    """
    tmp = sorted(set(arr))  # 排序+去重
    return [bisect.bisect_left(tmp, v) + 1 for v in arr]  # 1-indexed


def discretize_unique(arr):
    """离散化方法二: 相同的值按出现顺序离散化为不同排名。
    用于需要区分相同值不同位置的场合。
    """
    n = len(arr)
    pairs = [(arr[i], i) for i in range(n)]
    pairs.sort(key=lambda x: (x[0], x[1]))
    result = [0] * n
    for rank, (val, idx) in enumerate(pairs):
        result[idx] = rank + 1  # 1-indexed
    return result


def discretize_with_query(arr):
    """离散化并返回: 离散数组 + 查询函数(原值->排名)。
    便于后续多次查询。
    """
    tmp = sorted(set(arr))
    disc = [bisect.bisect_left(tmp, v) + 1 for v in arr]

    def query(val):
        """原值 -> 排名(1-indexed), 不存在返回插入位置。"""
        return bisect.bisect_left(tmp, val) + 1

    return disc, query, tmp  # tmp为去重有序数组


if __name__ == '__main__':
    # 测试方法一: 同值同排名
    arr1 = [1000, 500, 500, 2000, 1000]
    disc1 = discretize_same(arr1)
    print(f'Original: {arr1}')
    print(f'Discretized (same): {disc1}')  # [2, 1, 1, 3, 2]
    assert disc1 == [2, 1, 1, 3, 2]
    assert all(1 <= x <= 3 for x in disc1)  # 值域压缩到 [1,3]

    # 测试偏序保持
    arr2 = [300, 100, 200]
    disc2 = discretize_same(arr2)
    assert disc2 == [3, 1, 2]  # 100<200<300 => 1<2<3

    # 测试方法二: 同值不同排名
    arr3 = [100, 100, 50, 200]
    disc3 = discretize_unique(arr3)
    print(f'Discretized (unique): {disc3}')  # 50->1, 100(first)->2, 100(second)->3, 200->4
    assert disc3 == [2, 3, 1, 4]

    # 测试带查询函数
    arr4 = [10, 20, 10, 30]
    disc4, query, tmp = discretize_with_query(arr4)
    print(f'Discretized: {disc4}')  # [1, 2, 1, 3]
    print(f'Query 20: {query(20)}')  # 2
    print(f'Query 25: {query(25)}')  # 3 (插入位置)
    assert disc4 == [1, 2, 1, 3]
    assert query(20) == 2

    print('All discretization tests passed!')

```

**PyPy 提示**: PyPy 对排序和 bisect 优化好；离散化是 O(n log n) 预处理，几乎无性能瓶颈；bisect_left 是 C 实现极快。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(N log N) — 排序 O(N log N) + 去重 O(N) + N 次 lower_bound O(N log N) |
| 空间 | O(N) — 去重数组+结果数组 |

### 局限

仅适用于'只需偏序关系'的场景(树状数组/线段树下标)；不适用于需要原始值运算的场景(如值的大小比较后的加减)；离散化后值域变为 [1,n]，但 n 可能仍很大(需配合动态开点线段树等)。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1955 | 3 | NOI2015 程序自动分析: 离散化+并查集, 大值域映射 | [https://www.luogu.com.cn/problem/P1955](https://www.luogu.com.cn/problem/P1955) |
| Luogu | P3740 | 3 | HAOI2014 贴海报: 离散化+倒序处理区间覆盖 | [https://www.luogu.com.cn/problem/P3740](https://www.luogu.com.cn/problem/P3740) |

## Pitfalls · 易错点

- 忘记去重: set() 或 unique() 必须执行, 否则排名不连续(有空洞)
- lower_bound 返回的是 0-indexed 位置, 树状数组需要 1-indexed → 需 +1
- 方法一和方法二选择错误: 需区分相同值时用方法二, 否则用方法一
- 离散化后值域 [1,n] 但 n 可能仍大, 线段树仍需动态开点或离散化后值域分析

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/misc/discrete/](https://oi-wiki.org/misc/discrete/)
- Wikipedia ✓ [https://en.wikipedia.org/wiki/Transitive_reduction](https://en.wikipedia.org/wiki/Transitive_reduction)
