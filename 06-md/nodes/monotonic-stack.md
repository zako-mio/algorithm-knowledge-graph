---
id: monotonic-stack
name: 单调栈
group: G-A-2
stage: intermediate
priority: P0
depth_tier: deep
---

# 单调栈

> 维护单调性的栈，O(n)求左右第一个大/小于当前值

<!-- 元信息: id=monotonic-stack · group=G-A-2 · stage=intermediate · priority=P0 · depth_tier=deep -->

## What · 是什么

单调栈(Monotonic Stack)是在栈的基础上维护元素单调性(递增或递减)的数据结构。在元素入栈时，弹出所有破坏单调性的栈顶元素，使得栈内元素始终保持有序。可在 O(n) 时间内对每个元素找到其左侧/右侧第一个大于/小于它的元素。

## Why · 为什么

### 直觉 · Intuition

对于序列中每个元素，我们常需找到'下一个更大元素'。暴力是 O(n^2)。关键观察：如果 i < j 且 a[i] <= a[j]，那么对于 j 之后的元素，a[i] 永远不可能是'下一个更大'——a[j] 更近且更大，挡住了 a[i]。所以 a[i] 可以被安全丢弃。单调栈就是高效维护这个'丢弃'过程：栈中保留递减的候选者，新元素入栈时弹出所有被它'挡住'的旧元素。

### 原理 · Principle

维护一个单调递减(或递增)的栈。遍历序列时，对每个新元素 x：①while 栈非空且栈顶满足弹出条件(如递减栈中栈顶 < x)，弹出栈顶并记录结果(此时 x 就是弹出元素的'下一个更大') ②将 x 入栈。每个元素最多入栈一次、出栈一次，故总 O(n)。变体：递增栈找'下一个更小'；逆向遍历找'左侧第一个更大'。

### 历史 · History

单调栈是竞赛中的经典技巧。OI Wiki 将其与单调队列并列为栈/队列的进阶应用。经典例题 LeetCode 739(每日温度)和 POJ3250(Bad Hair Day)是其标准模板。

## How · 实现

### 伪代码

```python
# 求每个元素右侧第一个更大的元素位置
# 维护单调递减栈(栈存下标)
for i in range(n):
  while not st.empty() and a[st.top()] < a[i]:
    ans[st.pop()] = i  # i 是 st.top() 右侧第一个更大的位置
  st.push(i)
# 栈中剩余元素的 ans 为 -1(无更大元素)
```

### Python 实现

```python
def daily_temperatures(temps):
    """LeetCode 739: 每日温度
    对每天, 求下一个更暖和的日子在几天后。
    单调递减栈(存下标), 弹出时记录距离。
    """
    n = len(temps)
    ans = [0] * n
    st = []  # 栈存下标, 维护对应的温度递减
    for i in range(n):
        while st and temps[st[-1]] < temps[i]:
            j = st.pop()
            ans[j] = i - j  # 距离 = 天数差
        st.append(i)
    return ans


def next_greater_element(nums):
    """求每个元素右侧第一个更大的元素值(不存在则-1)。
    单调递减栈。
    """
    n = len(nums)
    ans = [-1] * n
    st = []
    for i in range(n):
        while st and nums[st[-1]] < nums[i]:
            ans[st.pop()] = nums[i]
        st.append(i)
    return ans


def left_right_smaller(n, arr):
    """对每个元素, 求左侧第一个<它 和 右侧第一个<它 的下标。
    左侧: 从左到右维护递增栈; 右侧: 从右到左维护递增栈。
    """
    left = [-1] * n
    st = []
    for i in range(n):
        while st and arr[st[-1]] >= arr[i]:
            st.pop()
        if st:
            left[i] = st[-1]
        st.append(i)

    right = [-1] * n
    st = []
    for i in range(n - 1, -1, -1):
        while st and arr[st[-1]] >= arr[i]:
            st.pop()
        if st:
            right[i] = st[-1]
        st.append(i)

    return left, right


if __name__ == '__main__':
    # 测试每日温度
    temps = [73, 74, 75, 71, 69, 72, 76, 73]
    result = daily_temperatures(temps)
    print(f'Daily temperatures: {result}')
    assert result == [1, 1, 4, 2, 1, 1, 0, 0]

    # 测试下一个更大元素
    nums = [2, 1, 2, 4, 3]
    nge = next_greater_element(nums)
    print(f'Next greater: {nge}')
    assert nge == [4, 2, 4, -1, -1]

    # 测试左右更小
    arr = [3, 1, 4, 1, 5, 9, 2, 6]
    left, right = left_right_smaller(len(arr), arr)
    print(f'Left smaller:  {left}')
    print(f'Right smaller: {right}')

    print('All monotonic stack tests passed!')

```

**PyPy 提示**: PyPy 对 list 的 append/pop JIT 极好；单调栈是纯列表操作，PyPy 性能接近 C；N=1e6 的单调栈在 PyPy 下约 0.1s。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(N) — 每个元素最多入栈一次、出栈一次，均摊 O(1) per element |
| 空间 | O(N) — 栈最坏存全部元素(完全递减序列) |

### 局限

只能处理'单调性可维护'的问题(如下一个更大/更小)；不适用于需要区间查询的问题(应用线段树)；栈中通常存下标而非值以便记录答案位置。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| LeetCode | 739 | 2 | 每日温度: 单调栈经典模板, 求下一个更大元素的距离 | [https://leetcode.cn/problems/daily-temperatures/](https://leetcode.cn/problems/daily-temperatures/) |
| LeetCode | 496 | 2 | 下一个更大元素I: 单调栈+哈希映射 | [https://leetcode.cn/problems/next-greater-element-i/](https://leetcode.cn/problems/next-greater-element-i/) |
| Luogu | P5788 | 2 | 单调栈模板题: 求每个数右侧第一个比它大的元素位置 | [https://www.luogu.com.cn/problem/P5788](https://www.luogu.com.cn/problem/P5788) |

## Pitfalls · 易错点

- 栈中存值还是存下标: 需要答案位置时必须存下标，存值会丢失位置信息
- 递增还是递减搞反: 求下一个更大→递减栈(弹出比当前小的); 求下一个更小→递增栈
- 弹出条件用 <= 还是 <: 含等号时相等的元素也弹出(适用于'严格更大')，不含等号则保留(适用于'非严格更大')
- 忘记处理栈中剩余元素(它们的答案为 -1/0 表示无更大元素)

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/monotonic-stack/](https://oi-wiki.org/ds/monotonic-stack/)
- CP-Algorithms ✓ [https://cp-algorithms.com/data_structures/stack_queue_modification.html](https://cp-algorithms.com/data_structures/stack_queue_modification.html)
