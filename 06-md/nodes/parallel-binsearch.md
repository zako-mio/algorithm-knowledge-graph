---
id: parallel-binsearch
name: 整体二分/并行二分
group: G-E-7
stage: advanced
priority: P1
depth_tier: standard
---

# 整体二分/并行二分

> 多询问一起二分：把操作和询问按答案值域分治，O(T·log n)同时处理所有询问

<!-- 元信息: id=parallel-binsearch · group=G-E-7 · stage=advanced · priority=P1 · depth_tier=standard -->

## What · 是什么

整体二分(Parallel Binary Search)是一种离线算法，将多个二分答案的询问同时进行：在每一层分治中，将所有询问按答案是否 <= mid 分为两组，同时处理所有 <= mid 的修改操作，递归处理两组。总复杂度 O(T log V)，其中 T 是单次操作+查询的复杂度。

## Why · 为什么

### 直觉 · Intuition

如果有 Q 个询问每个都需要二分答案(值域 V)，逐个二分是 O(Q * T * log V)。但很多二分过程重叠：同一层所有询问都猜 mid，可以一次性处理所有 <= mid 的修改对全部询问的贡献。把询问按'答案 <= mid'还是'> mid'分组后递归，每层只处理一次全部操作，共 log V 层 → O(T * (N+Q) * log V)。

### 原理 · Principle

solve(l, r, ops, queries): ①若 l==r，所有 query 的答案为 l ②取 mid=(l+r)/2 ③对当前值域 [l,mid] 的修改操作执行(树状数组等) ④对每个 query 检查答案是否 <= mid(查树状数组)，是则分入 q1(还需处理左半)，否则扣减 k 后分入 q2 ⑤撤销修改 ⑥递归 solve(l,mid,ops1,q1) 和 solve(mid+1,r,ops2,q2)。适用条件：答案可二分、修改贡献独立且可加、允许离线。

### 历史 · History

整体二分是离线算法的经典代表，常用于区间第 k 小(静态/动态)、带修区间第 k 小等。OI Wiki 将其与 CDQ 分治、莫队并列为离线三宝。经典题目包括 Luogu P3834(区间 k 小)和 P2617(Dynamic Rankings)。

## How · 实现

### 伪代码

```python
# 区间第 k 小(静态)
solve(l, r, nums, queries):
  if l == r:
    for q in queries: ans[q.id] = l
    return
  mid = (l + r) / 2
  q1, q2 = [], []
  # 值 <= mid 的数: 在其位置 +1
  for num in nums:
    if num.val <= mid:
      bit.add(num.pos, 1)
  for q in queries:
    t = bit.query(q.r) - bit.query(q.l-1)
    if q.k <= t:
      q1.append(q)
    else:
      q.k -= t
      q2.append(q)
  # 撤销
  for num in nums:
    if num.val <= mid:
      bit.add(num.pos, -1)
  # 分值域递归
  nums1 = [n for n in nums if n.val <= mid]
  nums2 = [n for n in nums if n.val > mid]
  solve(l, mid, nums1, q1)
  solve(mid+1, r, nums2, q2)
```

### Python 实现

```python
class BIT:
    """树状数组: 单点修改+前缀查询。"""
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 2)

    def add(self, i, v):
        while i <= self.n:
            self.tree[i] += v
            i += i & (-i)

    def query(self, i):
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s


def parallel_binsearch_kth(arr, queries):
    """区间第 k 小(整体二分)。
    arr: 原数组(0-indexed值)
    queries: [(l, r, k), ...] 0-indexed, k从1开始
    返回每个查询的答案。
    """
    n = len(arr)
    # 离散化
    vals = sorted(set(arr))
    val_map = {v: i + 1 for i, v in enumerate(vals)}  # 1-indexed
    m = len(vals)

    # 数: (位置, 离散值), 按值排序
    nums = sorted([(i, val_map[arr[i]]) for i in range(n)], key=lambda x: x[1])

    # 查询: (l, r, k, id) 0-indexed -> 1-indexed
    qs = [(q[0] + 1, q[1] + 1, q[2], idx) for idx, q in enumerate(queries)]
    ans = [0] * len(queries)
    bit = BIT(n)

    def solve(l, r, nums, qs):
        if l == r:
            for q in qs:
                ans[q[3]] = vals[l - 1]  # 映射回原值
            return
        mid = (l + r) // 2
        # 处理值 <= mid 的数
        nums_l = []
        nums_r = []
        ni = 0
        for num in nums:
            if num[1] <= mid:
                bit.add(num[0] + 1, 1)  # 位置 1-indexed
                nums_l.append(num)
            else:
                nums_r.append(num)
        # 分配查询
        q1 = []
        q2 = []
        for q in qs:
            t = bit.query(q[1]) - bit.query(q[0] - 1)
            if q[2] <= t:
                q1.append(q)
            else:
                q2.append((q[0], q[1], q[2] - t, q[3]))
        # 撤销
        for num in nums_l:
            bit.add(num[0] + 1, -1)
        # 递归
        if q1:
            solve(l, mid, nums_l, q1)
        if q2:
            solve(mid + 1, r, nums_r, q2)

    solve(1, m, nums, qs)
    return ans


if __name__ == '__main__':
    arr = [1, 5, 2, 6, 3, 7, 4]
    queries = [(0, 5, 4), (2, 4, 2), (0, 6, 5)]  # (l, r, k) 0-indexed
    result = parallel_binsearch_kth(arr, queries)
    print(f'Kth smallest results: {result}')
    # 验证
    # [1,5,2,6,3,7] sorted=[1,2,3,5,6,7], 4th=5
    # [2,6,3] sorted=[2,3,6], 2nd=3
    # [1,5,2,6,3,7,4] sorted=[1,2,3,4,5,6,7], 5th=5
    assert result == [5, 3, 5], f'Expected [5,3,5], got {result}'
    print('Parallel binary search: test passed!')

```

**PyPy 提示**: PyPy 对整体二分中频繁的列表分配和树状数组操作性能尚可；但递归层深 log V，每层 O(N+Q)，N,Q>1e5 时可能 TLE；建议 C++ 实现。Python 用于理解算法。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O((N+Q) * log V * T) — T为单次树状数组操作 O(log N), 共 log V 层 |
| 空间 | O(N+Q) — 每层临时存储操作和查询 |

### 局限

仅适用于离线(已知全部询问)；答案需可二分；修改贡献需独立且可加；动态(带修改)版本需将修改也按时间序融入操作流。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3834 | 4 | 可持久化线段树2(区间k小): 整体二分替代可持久化线段树 | [https://www.luogu.com.cn/problem/P3834](https://www.luogu.com.cn/problem/P3834) |
| Luogu | P2617 | 5 | Dynamic Rankings(带修区间k小): 整体二分+修改操作融入 | [https://www.luogu.com.cn/problem/P2617](https://www.luogu.com.cn/problem/P2617) |

## Pitfalls · 易错点

- 树状数组用完必须撤销(逆序 add -v), 否则跨层污染
- 查询分组时 k 值需扣减(答案>mid 的查询减去 <=mid 的数量后进入右半)
- 值域边界: l==r 时记录答案, 注意映射回原值(离散化逆映射)
- 操作和查询的顺序: 修改必须按时间排在查询之前(带修版本)

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/misc/parallel-binsearch/](https://oi-wiki.org/misc/parallel-binsearch/)
- Wikipedia ✓ [https://en.wikipedia.org/wiki/Binary_search](https://en.wikipedia.org/wiki/Binary_search)
