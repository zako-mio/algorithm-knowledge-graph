---
id: two-pointer
name: 双指针
group: G-E-7
stage: basic
priority: P0
depth_tier: deep
---

# 双指针

> 同向/相向移动两指针维护区间信息：O(n)解决单调性区间问题，莫队基础

<!-- 元信息: id=two-pointer · group=G-E-7 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

双指针(Two Pointers)是用两个指针在序列上同向或相向移动来维护区间信息的技巧。同向双指针(快慢指针)维护滑动窗口；相向双指针(左右指针)利用有序性从两端逼近。可在 O(n) 时间内解决具有单调性的区间问题，是莫队算法的基础。

## Why · 为什么

### 直觉 · Intuition

暴力枚举区间是 O(n^2)。如果区间具有单调性(如正数之和随右端点递增)，则可以只移动一个指针：当区间不满足条件时移动左指针缩小，满足时移动右指针扩大。两个指针各自只前进不后退，总共最多各走 n 步 → O(n)。

### 原理 · Principle

同向双指针(滑动窗口)：l=0, 遍历 r 从 0 到 n-1，当 [l,r] 不满足条件时 l++。利用单调性：若 [l,r] 满足则 [l+1,r] 也满足(缩小只会更好)，若不满足则需 l++ 或 r++。相向双指针：l=0, r=n-1，根据 a[l]+a[r] 与 target 的关系移动 l++ 或 r--，利用有序性从两端逼近答案。

### 历史 · History

双指针是竞赛和面试中最基础的技巧之一。CPH(Competitive Programmer's Handbook)ch5 将其归为 Complete Search 的高效变体。经典应用包括 LeetCode 167(两数之和II)、713(乘积小于K的子数组)。莫队算法即基于双指针的区间移动。

## How · 实现

### 伪代码

```python
# 同向双指针(滑动窗口): 求满足条件的最长区间
l = 0
for r in range(n):
  add(arr[r])  # 扩展右端
  while not valid():  # 不满足条件时收缩
    remove(arr[l])
    l += 1
  ans = max(ans, r - l + 1)

# 相向双指针: 有序数组两数之和
l, r = 0, n-1
while l < r:
  s = arr[l] + arr[r]
  if s == target: found
  elif s < target: l += 1
  else: r -= 1
```

### Python 实现

```python
def subarray_product_less_than_k(nums, k):
    """LeetCode 713: 乘积小于K的子数组个数。
    同向双指针(滑动窗口), 利用正整数乘积单调性。
    """
    if k <= 1:
        return 0
    prod = 1
    l = 0
    ans = 0
    for r in range(len(nums)):
        prod *= nums[r]
        while prod >= k:
            prod //= nums[l]
            l += 1
        ans += r - l + 1  # 以r结尾的合法子数组个数
    return ans


def two_sum_sorted(numbers, target):
    """LeetCode 167: 有序数组两数之和II。
    相向双指针, 利用有序性从两端逼近。
    返回两数下标(1-indexed)。
    """
    l, r = 0, len(numbers) - 1
    while l < r:
        s = numbers[l] + numbers[r]
        if s == target:
            return [l + 1, r + 1]  # 1-indexed
        elif s < target:
            l += 1
        else:
            r -= 1
    return []


def min_subarray_len(target, nums):
    """LeetCode 209: 长度最小的子数组(和>=target)。
    同向双指针。
    """
    l = 0
    s = 0
    ans = len(nums) + 1
    for r in range(len(nums)):
        s += nums[r]
        while s >= target:
            ans = min(ans, r - l + 1)
            s -= nums[l]
            l += 1
    return ans if ans <= len(nums) else 0


def is_subsequence(s, t):
    """LeetCode 392: 判断s是否为t的子序列。
    双指针匹配。
    """
    i = 0
    for ch in t:
        if i < len(s) and s[i] == ch:
            i += 1
    return i == len(s)


if __name__ == '__main__':
    # 测试乘积小于K的子数组
    assert subarray_product_less_than_k([10, 5, 2, 6], 100) == 8
    print(f'Subarray product < 100: {subarray_product_less_than_k([10, 5, 2, 6], 100)}')  # 8

    # 测试两数之和
    assert two_sum_sorted([2, 7, 11, 15], 9) == [1, 2]
    print(f'Two sum [2,7,11,15] target=9: {two_sum_sorted([2, 7, 11, 15], 9)}')  # [1,2]

    # 测试最小子数组
    assert min_subarray_len(7, [2, 3, 1, 2, 4, 3]) == 2
    print(f'Min subarray len target=7: {min_subarray_len(7, [2, 3, 1, 2, 4, 3])}')  # 2

    # 测试子序列
    assert is_subsequence('abc', 'ahbgdc') == True
    assert is_subsequence('axc', 'ahbgdc') == False
    print(f'Is subsequence abc/ahbgdc: {is_subsequence("abc", "ahbgdc")}')  # True

    print('All two-pointer tests passed!')

```

**PyPy 提示**: PyPy 对双指针的简单数组操作优化极佳，性能接近 C；双指针是最轻量的算法之一，几乎无性能瓶颈。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(N) — 两个指针各最多移动 N 次 |
| 空间 | O(1) — 仅需常数额外空间(同向) / O(1) (相向) |

### 局限

需要区间具有单调性(否则无法只前进不后退)；不适用于需要随机访问区间信息的问题(应用前缀和/线段树)；相向双指针要求序列有序。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| LeetCode | 713 | 2 | 乘积小于K的子数组: 同向双指针经典模板 | [https://leetcode.cn/problems/subarray-product-less-than-k/](https://leetcode.cn/problems/subarray-product-less-than-k/) |
| LeetCode | 167 | 2 | 两数之和II: 相向双指针, 利用有序性 | [https://leetcode.cn/problems/two-sum-ii-input-array-is-sorted/](https://leetcode.cn/problems/two-sum-ii-input-array-is-sorted/) |
| LeetCode | 209 | 2 | 最小长度子数组: 滑动窗口双指针 | [https://leetcode.cn/problems/minimum-size-subarray-sum/](https://leetcode.cn/problems/minimum-size-subarray-sum/) |

## Pitfalls · 易错点

- 乘积/和的中间值可能溢出: C++ 需用 long long, Python 自动大整数无此问题
- 滑动窗口收缩条件错误: 应在'不满足'时收缩而非'满足'时, 方向搞反会漏解
- k<=1 时乘积子数组无解(正整数乘积>=1不可能<k), 需特判
- 相向双指针要求序列有序: 无序数组需先排序(可能打乱原始下标)

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/misc/two-pointer/](https://oi-wiki.org/misc/two-pointer/)
- 书籍 ✓ `CPH ch5 Complete search, pp.57-66`
