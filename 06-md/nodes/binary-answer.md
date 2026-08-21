---
id: binary-answer
name: 二分答案
group: G-A-1
stage: intermediate
priority: P0
depth_tier: deep
---

# 二分答案

> 对答案值域二分，配合 check 函数求解最优化问题

<!-- 元信息: id=binary-answer · group=G-A-1 · stage=intermediate · priority=P0 · depth_tier=deep -->

## What · 是什么

二分答案（binary search on answer）把『求最优化问题』转化为『判定可行性』：对答案的值域做二分，用 check(x) 判断 x 是否可行，利用答案的单调性收敛到最优解。适用于『最大值最小化』/『最小值最大化』类问题。前提三条件：①答案在固定区间；②check 比求最优容易；③可行解关于区间单调（x 可行则 x 更宽松的方向也可行）。

## Why · 为什么

### 直觉 · Intuition

很多最优化问题直接求最优很难，但『给定一个值，判断是否可行』很简单。若答案具有单调性（可行域是区间），就可二分搜索这个区间的边界。例如 P1873 砍树：给定锯片高度 H，贪心 O(n) 就能判断能否砍够 M 米，于是对 H 在 [1,1e9] 上二分。

### 原理 · Principle

设答案 x 可行当且仅当 x ∈ [L, R]（或单调延伸），则用二分找 L/R。最大值最小化：找最小可行 x，二分时 check(mid) 可行 → 答案在左半（含 mid）r=mid；否则 l=mid+1。最小值最大化：找最大可行 x，check(mid) 可行 → l=mid；否则 r=mid-1。注意整数二分与实数二分的收敛写法不同；check 的复杂度决定总复杂度 O(check_cost × log(值域))。

### 历史 · History

二分答案的思想本质上是『搜索答案空间 + 可行性判定』的降维，在竞赛中非常普及（OI Wiki 二分章节、众多最优解题解均采用）。它把『求最优』重述为『判定单调性质』，与广义二分（单调布尔条件）一脉相承。典型：P1873 砍树、P1182 数列分段。

## How · 实现

### 伪代码

```python
# 最大值最小化：找最小的可行答案
lo, hi = 下界, 上界           # 答案必在 [lo, hi]
while lo < hi:
    mid = (lo + hi) // 2
    if check(mid):            # mid 可行 → 尝试更小
        hi = mid
    else:
        lo = mid + 1
answer = lo

# 最小值最大化：找最大的可行答案
while lo < hi:
    mid = (lo + hi + 1) // 2  # 上取整，防止死循环
    if check(mid):
        lo = mid
    else:
        hi = mid - 1
```

### Python 实现

```python
def solve_tree_cutting(trees, m):
    """P1873 砍树：找最大整数高度 H，使砍下的木材总量 >= m"""
    def check(h):
        total = 0
        for t in trees:
            if t > h:
                total += t - h
            if total >= m:            # 提前剪枝，防溢出/提速
                return True
        return total >= m

    lo, hi = 0, max(trees)
    while lo < hi:
        mid = (lo + hi + 1) // 2      # 上取整：找『最大可行』
        if check(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo


def solve_array_seg(a, seg):
    """P1182 数列分段：把 a 分成恰好 seg 段，使每段和的最大值最小"""
    def check(limit):
        cnt, cur = 1, 0
        for v in a:
            if cur + v > limit:
                cnt += 1
                cur = v
            else:
                cur += v
        return cnt <= seg

    lo, hi = max(a), sum(a)           # 单段最大 / 整段
    while lo < hi:
        mid = (lo + hi) // 2
        if check(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


if __name__ == "__main__":
    assert solve_tree_cutting([20, 15, 10, 17], 7) == 15
    assert solve_tree_cutting([4, 42, 40, 26, 46], 20) == 36
    assert solve_array_seg([4, 2, 4, 5, 1], 3) == 6
    assert solve_array_seg([1, 2, 3, 4, 5], 2) == 9
    import random
    for _ in range(200):
        n = random.randint(1, 10)
        arr = [random.randint(1, 500) for _ in range(n)]
        k = random.randint(1, n)
        # 暴力验证 P1182：DP 求把 arr 分成恰好 k 段的最小"最大段和"
        dp = [[float("inf")] * (k + 1) for _ in range(n + 1)]
        dp[0][0] = 0
        for i in range(1, n + 1):
            for j in range(1, k + 1):
                s = 0
                for t in range(i, 0, -1):
                    s += arr[t - 1]
                    dp[i][j] = min(dp[i][j], max(dp[t - 1][j - 1], s))
        assert solve_array_seg(arr, k) == dp[n][k], (arr, k, solve_array_seg(arr, k), dp[n][k])
    print("二分答案（P1873 砍树 / P1182 数列分段）正确性 OK（200 组暴力对照）")
    print("P1873 示例:", solve_tree_cutting([20, 15, 10, 17], 7))

```

**PyPy 提示**: check 是热点函数：用 for 循环与局部变量而非 sum()/切片，PyPy 下差距明显。整数二分上取整写法 (lo+hi+1)//2 配合 lo=mid 可防死循环；下取整配合 lo=mid+1。实数二分要定最大迭代次数（如 100 次）而非 while 条件。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(check 代价 × log(值域)) |
| 空间 | check 所用空间，通常 O(1) 或 O(n) |

### 局限

答案必须满足单调性（可行域是连续的取值区间）；check 必须易写且快；浮点答案需注意精度与收敛次数。不适合非单调的『最优化』。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1873 | 3 | 二分答案模板：砍树高度最大化最小值 | [https://www.luogu.com.cn/problem/P1873](https://www.luogu.com.cn/problem/P1873) |
| Luogu | P1182 | 4 | 二分答案：最大值最小化 | [https://www.luogu.com.cn/problem/P1182](https://www.luogu.com.cn/problem/P1182) |

## Pitfalls · 易错点

- 整数二分两种写法混用导致死循环：上取整必须配 lo=mid，下取整必须配 lo=mid+1
- check 中贪心策略本身错误或越界（如 P1182 中单个元素 > limit 会返回 cnt 超大）
- 值域上下界取错（下界取 0 或 1 而非 max(a)，上界取太小）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/basic/binary/](https://oi-wiki.org/basic/binary/)
- OI Wiki ✓ [https://www.luogu.com.cn/problem/P1873](https://www.luogu.com.cn/problem/P1873)
- OI Wiki ✓ [https://www.luogu.com.cn/problem/P1182](https://www.luogu.com.cn/problem/P1182)
