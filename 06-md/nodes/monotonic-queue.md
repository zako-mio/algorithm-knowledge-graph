---
id: monotonic-queue
name: 单调队列
group: G-A-2
stage: intermediate
priority: P0
depth_tier: deep
---

# 单调队列

> 维护滑动窗口最值，O(n)均摊，DP优化基础

<!-- 元信息: id=monotonic-queue · group=G-A-2 · stage=intermediate · priority=P0 · depth_tier=deep -->

## What · 是什么

单调队列(Monotonic Queue)是一个双端队列(deque)，在队尾插入元素时弹出所有破坏单调性的元素，使队列内元素保持单调递增或递减。同时通过记录元素位置来淘汰超出窗口范围的队首。可在 O(n) 均摊时间内维护滑动窗口的最值，是 DP 优化(如多重背包、斜率优化)的基础。

## Why · 为什么

### 直觉 · Intuition

滑动窗口求最值：暴力 O(nk)。关键观察与新元素比较：如果新元素比队尾大(求最大值时)，那么队尾元素永远不会成为未来窗口的最大值——新元素更大且更晚离开窗口。所以可以安全弹出队尾。类似地，队首超出窗口范围时弹出。这样每个元素进出队列各一次，总共 O(n)。

### 原理 · Principle

用双端队列(deque)维护一个单调序列。队列存储元素下标，便于判断是否超出窗口。对每个新元素 i：①弹出队首超出窗口的元素(while dq[0] < i-k+1: popleft) ②弹出队尾不满足单调性的元素(求最大值: while arr[dq[-1]] <= arr[i]: pop) ③将 i 入队尾 ④队首 dq[0] 即为当前窗口的最值下标。求最大值→递减队列；求最小值→递增队列。

### 历史 · History

单调队列的经典应用是 POJ2823(Sliding Window)。在 DP 优化中，单调队列可将 O(nk) 的多重背包/滑动DP优化到 O(n)。OI Wiki 将其与单调栈并列为栈队列的进阶结构。

## How · 实现

### 伪代码

```python
# 滑动窗口最大值 (窗口大小 k)
dq = deque()  # 存下标, 维护递减
for i in range(n):
  # 1. 弹出超出窗口的队首
  while dq and dq[0] < i - k + 1:
    dq.popleft()
  # 2. 弹出不满足单调性的队尾
  while dq and arr[dq[-1]] <= arr[i]:
    dq.pop()
  # 3. 入队
  dq.append(i)
  # 4. 记录答案(i >= k-1 时)
  if i >= k - 1:
    ans.append(arr[dq[0]])
```

### Python 实现

```python
from collections import deque

def sliding_window_max(arr, k):
    """滑动窗口最大值: 返回每个窗口的最大值。
    单调递减队列(存下标)。
    LeetCode 239 模板。
    """
    n = len(arr)
    if n == 0:
        return []
    dq = deque()  # 存下标, arr[dq[i]] 递减
    ans = []
    for i in range(n):
        # 弹出超出窗口的队首
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        # 弹出比当前元素小的队尾(它们不可能成为最大值)
        while dq and arr[dq[-1]] <= arr[i]:
            dq.pop()
        dq.append(i)
        # 第一个窗口完整后开始记录
        if i >= k - 1:
            ans.append(arr[dq[0]])
    return ans


def sliding_window_min(arr, k):
    """滑动窗口最小值: 单调递增队列。"""
    n = len(arr)
    if n == 0:
        return []
    dq = deque()  # 存下标, arr[dq[i]] 递增
    ans = []
    for i in range(n):
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        while dq and arr[dq[-1]] >= arr[i]:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            ans.append(arr[dq[0]])
    return ans


def dp_sliding_window_max(arr, k):
    """DP优化示例: dp[i] = max(arr[i-k..i]) 的递推。
    用单调队列优化到 O(n)。
    """
    n = len(arr)
    if n == 0:
        return []
    dp = [0] * n
    dq = deque()
    for i in range(n):
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        while dq and arr[dq[-1]] <= arr[i]:
            dq.pop()
        dq.append(i)
        dp[i] = arr[dq[0]]
    return dp


if __name__ == '__main__':
    arr = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3

    # 测试滑动窗口最大值
    maxs = sliding_window_max(arr, k)
    print(f'Window max: {maxs}')
    assert maxs == [3, 3, 5, 5, 6, 7]

    # 测试滑动窗口最小值
    mins = sliding_window_min(arr, k)
    print(f'Window min: {mins}')
    assert mins == [-1, -3, -3, -3, 3, 3]

    # 测试DP优化
    dp = dp_sliding_window_max(arr, k)
    print(f'DP max:     {dp}')

    print('All monotonic queue tests passed!')

```

**PyPy 提示**: PyPy 对 deque 操作优化好；单调队列是竞赛高频结构，PyPy 下 N=1e6 约 0.1s；注意 deque 的 popleft/pop 都是 O(1)。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(N) — 每个元素最多入队一次、出队一次(队首或队尾)，均摊 O(1) |
| 空间 | O(K) — 队列最多存窗口大小 K 个元素(实际最坏 O(N) 完全递减序列) |

### 局限

仅适用于滑动窗口/区间最值类问题；窗口大小必须固定(变长窗口需结合双指针)；不能处理区间和(用前缀和/树状数组)；DP优化需转移方程具有单调性。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| LeetCode | 239 | 3 | 滑动窗口最大值: 单调队列经典模板题 | [https://leetcode.cn/problems/sliding-window-maximum/](https://leetcode.cn/problems/sliding-window-maximum/) |
| POJ | 2823 | 2 | Sliding Window: 单调队列起源题, 同时求窗口最大最小 | [http://poj.org/problem?id=2823](http://poj.org/problem?id=2823) |
| Luogu | P2698 | 3 | Flowerpot S: 双单调队列维护区间max-min+双指针 | [https://www.luogu.com.cn/problem/P2698](https://www.luogu.com.cn/problem/P2698) |

## Pitfalls · 易错点

- 队首弹出条件用 dq[0] < i-k+1(下标比较) 而非值比较，存的是下标不是值
- 求最大值用递减队列(弹出<=当前的), 求最小值用递增队列(弹出>=当前的), 方向搞反会错
- 弹出队尾用 pop()(从尾部), 弹出队首用 popleft()(从头部), 不能混用
- 第一个完整窗口在 i=k-1 时形成, 之前不应记录答案

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/monotonic-queue/](https://oi-wiki.org/ds/monotonic-queue/)
- CP-Algorithms ✓ [https://cp-algorithms.com/data_structures/stack_queue_modification.html](https://cp-algorithms.com/data_structures/stack_queue_modification.html)
