---
id: max-avg-segment
name: 最大平均值区段
group: G-E-7
stage: advanced
priority: P2
depth_tier: standard
---

# 最大平均值区段

> 求长度≥L的最大平均值子数组：二分+前缀和判定，分数规划经典应用

<!-- 元信息: id=max-avg-segment · group=G-E-7 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

最大平均值区段问题：给数组 a[1..n] 与下界 L，求长度不小于 L 的连续子段使平均值最大。经典解法：二分答案 x，把判定转化为检查是否存在长度≥L 且 sum-a*x 非负的子段(即 max subarray sum 限制长度)。等价于分数规划(最大化 sum(A)/len(A) 的约束版)。可用前缀和+单调队列 O(n) 判定，二分后总复杂度 O(n log precision)。

## Why · 为什么

### 直觉 · Intuition

直接枚举所有长度≥L 子段 O(n²) 不可行。观察'平均值≥x'等价于'子段每个数减去 x 后和≥0'，于是二分 x 后问题变成找最大子段和(带长度下界)。该子段和可通过前缀和最小化 O(n) 求出(当前 r 处最大和 = pref[r] - min(pref[0..r-L]))。

### 原理 · Principle

判定(x)：构造 b[i]=a[i]-x，前缀和 pref。对右端点 r，长度≥L 的最大子段和为 pref[r]-min(pref[0..r-L])，只需维护窗口内前缀和最小值。若存在≥0，说明存在子段平均值≥x，提高下界；否则降低。二分迭代至精度满足(通常 1e-6)。该技巧是分数规划(0/1分数规划二分)的基础形态。

### 历史 · History

问题本质是'最大子段和'的约束长度版本。CP-Algorithms 的最大/最小子段和页给出前缀和+维护当前最小值的 O(n) 求最大子段和算法，并延伸到限制长度(L 下界)需用单调队列/双端队列维护窗口内前缀和极值。这是二分答案结合判定函数的典型题，POJ 上有多道同名经典题。

## How · 实现

### 伪代码

```python
# 二分答案求最大平均值(长度>=L)
lo, hi = min(a), max(a)
for _ in range(60):
  mid = (lo + hi) / 2
  if feasible(mid): lo = mid
  else: hi = mid
return lo

def feasible(x):
  pref[0] = 0
  for i in 1..n: pref[i] = pref[i-1] + a[i] - x
  min_pref = inf
  for r in L..n:
    min_pref = min(min_pref, pref[r - L])
    if pref[r] - min_pref >= 0: return True
  return False
```

### Python 实现

```python
def max_avg_segment(a, L):
    """长度>=L 的最大平均值子段。二分+前缀和判定 O(n log)。"""
    n = len(a)

    def feasible(x):
        pref = 0.0
        # 维护窗口 [0..r-L] 内前缀和最小值
        # 用前缀和数组便于取 pref[r-L]
        pref_list = [0.0] * (n + 1)
        for i in range(n):
            pref_list[i + 1] = pref_list[i] + a[i] - x
        min_pref = float('inf')
        for r in range(L, n + 1):
            # 可用左端点 l 属于 [1, r-L+1], 对应 pref[l-1] 最小
            min_pref = min(min_pref, pref_list[r - L])
            if pref_list[r] - min_pref >= 0:
                return True
        return False

    lo, hi = min(a), max(a)
    for _ in range(60):  # 足够精度
        mid = (lo + hi) / 2.0
        if feasible(mid):
            lo = mid
        else:
            hi = mid
    return lo


def max_avg_segment_brute(a, L):
    """O(n^2) 暴力用于对拍。"""
    best = float('-inf')
    n = len(a)
    for i in range(n):
        s = 0.0
        for j in range(i, n):
            s += a[j]
            if j - i + 1 >= L:
                best = max(best, s / (j - i + 1))
    return best


def max_subarray_sum_kadane(a):
    """Kadane: 最大子段和(不限长度)。"""
    cur = best = a[0]
    for x in a[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best


if __name__ == '__main__':
    import random
    random.seed(3)
    # 确定性样例
    a = [1, 4, 7, 2, 5, 8]
    assert abs(max_avg_segment(a, 2) - 6.5) < 1e-9  # 4+7+2+5+8 = 26/4? 不对
    # 实际最优: 取 [7,2,5,8]=22/4=5.5? 取 [4,7,2,5,8]=26/5=5.2 ... 最优是 [7,2,5,8]=5.5
    # 或 [1,4,7,2,5,8] 全段 27/6=4.5; [4,7]=5.5; [5,8]=6.5 -> 最优 [5,8]=6.5
    assert abs(max_avg_segment(a, 2) - 6.5) < 1e-9
    assert abs(max_avg_segment_brute(a, 2) - 6.5) < 1e-9

    assert max_subarray_sum_kadane([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert max_subarray_sum_kadane([5, 4, -1, 7, 8]) == 23

    # 对拍
    for _ in range(100):
        n = random.randint(1, 12)
        arr = [random.randint(-10, 10) for _ in range(n)]
        L = random.randint(1, n)
        r1 = max_avg_segment(arr, L)
        r2 = max_avg_segment_brute(arr, L)
        assert abs(r1 - r2) < 1e-6, (arr, L, r1, r2)

    print('max_avg a,L=2 =', max_avg_segment(a, 2))
    print('kadane [-2,1,-3,4,-1,2,1,-5,4] =', max_subarray_sum_kadane([-2, 1, -3, 4, -1, 2, 1, -5, 4]))
    print('random brute-compare (100 cases): OK')
    print('All max-avg-segment tests passed!')

```

**PyPy 提示**: 二分 60 轮每轮 O(n), n=1e5 时 PyPy 可行; 判定中可用 deque 维护窗口前缀和最小值代替列表重算; 浮点比较用绝对精度, 别用 == 0。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(N log(precision)) — 每轮判定 O(N) |
| 空间 | O(N) — 前缀和数组(或 O(1) 用单调队列) |

### 局限

答案非整数时需二分到指定精度(通常 1e-5~1e-7); 若数组可含大量负值, 判定依然正确(子段和可能为负); 要求输出子段端点时需在判定中记录; 单调队列优化仅当窗口上界也有约束时更必要(仅下界可用前缀和+min 扫描)。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1419 | 3 | 寻找段落: 长度在[L,R]的最大平均值, 二分+单调队列, 经典分数规划模板 | [https://www.luogu.com.cn/problem/P1419](https://www.luogu.com.cn/problem/P1419) |
| Luogu | P2396 | 3 | 均分纸牌变体: 二分答案+前缀和判定场景 | [https://www.luogu.com.cn/problem/P2396](https://www.luogu.com.cn/problem/P2396) |
| POJ | 2018 | 3 | Best Cow Fences: 长度>=F的最大平均子段, 二分+判定经典 | [http://poj.org/problem?id=2018](http://poj.org/problem?id=2018) |

## Pitfalls · 易错点

- 判定函数里长度下限 L 对应窗口内取 pref[r-L], 边界别写成 r-L+1
- 二分 60 轮够精度, 但浮点输出要求精确小数位时按题保留; POJ 2018 要求输出*1000取整
- 子段和减去 x 后可能为负仍可能增大下界, 判定条件写 >=0 而非 >0
- 用浮点二分时 lo/hi 初值取 min/max 元素(而非整个范围), 收敛更快
- max_subarray_sum_kadane 处理全负数组: cur 每步 max(x, cur+x) 保证答案≥最大单元素

## Sources · 信源

- CP-Algorithms ✓ [https://cp-algorithms.com/others/maximum_average_segment.html](https://cp-algorithms.com/others/maximum_average_segment.html)
- web ✓ [http://poj.org/problem?id=2018](http://poj.org/problem?id=2018)
- CP-Algorithms ✓ [https://cp-algorithms.com/others/maximum_average_segment.html](https://cp-algorithms.com/others/maximum_average_segment.html)
