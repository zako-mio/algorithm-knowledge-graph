---
id: prefix-gcd-optimization
name: 前缀 GCD 变化优化
group: G-E-10
stage: frontier
priority: P3
depth_tier: brief
---

# 前缀 GCD 变化优化

> 利用『前缀 GCD 至多变化 O(log A) 次』的性质，把 O(n²) 优化到 O(n log A)

<!-- 元信息: id=prefix-gcd-optimization · group=G-E-10 · stage=frontier · priority=P3 · depth_tier=brief -->

## What · 是什么

前缀 GCD 变化优化利用数论性质：对固定右端点 r，所有以 r 结尾的子数组的 gcd 值 g = gcd(a[i..r]) 随 i 左移至多变化 O(log A) 次（A 为值域）。这是因为每次 g 变化时至少减半（变为其真因子），至多 log A 次。于是可用『二元组 (gcd 值, 出现段左边界)』的分段列表压缩所有子数组 gcd，将『枚举所有子数组』的 O(n²) 降到 O(n log A)。典型应用：统计 gcd=k 的子数组个数（LeetCode 2447）、子数组 gcd 与子数组和比较、按 gcd 分组 DP（2026 CF Insomnia'26 Editorial Problem O）。

## Why · 为什么

### 直觉 · Intuition

g 从 a[r] 开始，往左每吸收一个新元素只能变小，而且变小必然除以一个 ≥2 的真因子（g' = gcd(g, x) 是 g 的因子）。因此 g 的递减链长度 ≤ log₂ A，即『不同 gcd 值』的数量是 O(log A) 而不是 O(r)。把相同 gcd 值的连续左端点压成一段，段数就很小。

### 原理 · Principle

对每个右端点 r 维护一个分段列表 L = [(g, start), ...] 表示：左端点 i ∈ [start, next.start-1] 时 gcd(a[i..r]) = g，且 g 严格递减。计算 r+1 时：对 L 中每一段取新值 g' = gcd(g, a[r+1])，合并相邻同值段，末尾追加 (a[r+1], r+1)。每步段数 ≤ 已合并次数 ≤ log A + 1，故总复杂度 O(n log A)。统计答案时对每段按长度贡献即可。也可把 a 整体分段归并，得到所有子数组 gcd 集合，用于 DP 分组。

### 历史 · History

『子数组 gcd 值种类少』的性质是经典数论观察（常见于 Codeforces 与 LeetCode hard），LeetCode 2447 直接利用该性质统计 gcd=k 的子数组个数。2026-03 Codeforces Insomnia'26 Editorial Problem O（CF topic 152947）将其用于 DP 转移优化，把 O(n²) 状态压缩到 O(n log A)，成为前沿优化范式。

## How · 实现

### 伪代码

```python
res = 0
for r in 1..n:
    L = merge(L, a[r])   # 每段取 gcd(g, a[r]), 合并相邻同值段
    for (g, start) in L:
        res += f(g) * (段长)
    # L 长度 ≤ O(log A)
```

### Python 实现

```python
import math
import random


def count_subarrays_gcd_equal_k(a, k):
    """统计所有子数组 gcd 恰好等于 k 的个数（LeetCode 2447 模板）。
    对每个右端点维护 gcd 分段列表，段数 O(log A)。
    """
    from math import gcd

    ans = 0
    segments = []  # [(g, start)] 左端点 i∈[start, next.start) 时 gcd(a[i..r])=g
    for r, x in enumerate(a):
        new_seg = []
        for g, start in segments:
            ng = gcd(g, x)
            if new_seg and new_seg[-1][0] == ng:
                continue  # 与上一段同值，仅延长左界（start 不变，合并）
            new_seg.append((ng, start))
        if not new_seg or new_seg[-1][0] != x:
            new_seg.append((x, r))
        segments = new_seg
        # 统计本右端点下 gcd=k 的子数组个数：段长度之和
        for idx, (g, start) in enumerate(segments):
            if g == k:
                end = segments[idx + 1][1] if idx + 1 < len(segments) else r + 1
                ans += end - start
    return ans


def count_brute(a, k):
    n = len(a)
    cnt = 0
    for i in range(n):
        g = 0
        for j in range(i, n):
            g = math.gcd(g, a[j])
            if g == k:
                cnt += 1
    return cnt


if __name__ == "__main__":
    random.seed(3)
    for n in range(1, 10):
        for _ in range(60):
            a = [random.randint(1, 60) for _ in range(n)]
            k = random.randint(1, 60)
            got = count_subarrays_gcd_equal_k(a, k)
            exp = count_brute(a, k)
            assert got == exp, (a, k, got, exp)
    # 全 1 场景：gcd=1 的子数组个数 = n(n+1)/2
    assert count_subarrays_gcd_equal_k([1] * 5, 1) == 15
    print("prefix-gcd-optimization 自测通过：分段统计与暴力对拍一致")

```

**PyPy 提示**: 分段表用 list 存 (g, start)，每轮重建为 O(log A) 长，PyPy 下 n=1e6 时整体 O(n log A) 可跑。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n log A)（每右端点 O(log A) 段，每段 gcd 一次 O(log A)） |
| 空间 | O(log A) |

### 局限

仅当统计对象可表示为『按 gcd 分段』时可用；若需对每个子数组的 gcd 做更复杂的聚合（如 DP 带额外维度）需将分段信息带进状态。gcd 值域很大时 log A 为常数级（≤ 60 对 64-bit）。若同时需要计数 gcd 不等于 k 的需另行维护。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| LeetCode | 2447 | 4 | 统计 gcd 恰为 k 的子数组个数：前缀 gcd 分段模板题 | [https://leetcode.cn/problems/number-of-subarrays-with-gcd-equal-to-k/](https://leetcode.cn/problems/number-of-subarrays-with-gcd-equal-to-k/) |
| LeetCode | 2654 | 5 | 最小操作使全变1：利用 gcd 分段求最短 gcd=1 子数组 | [https://leetcode.cn/problems/minimum-number-of-operations-to-make-all-array-elements-equal-to-1/](https://leetcode.cn/problems/minimum-number-of-operations-to-make-all-array-elements-equal-to-1/) |

## Pitfalls · 易错点

- 段合并只保留与上一段不同的 g 值，且 start 取最早出现位置（段是连续的）
- 统计长度时 end 用下一段 start（或 r+1），别用当前段 start 重复计算
- gcd 递减链长度上限是 log₂(min(a[i])) 而非 n，写循环时别写成 O(段数×r)
- 边界：k 大于所有数时无子数组满足；a 含 0 时 gcd(x,0)=x

## Sources · 信源

- web △ [https://codeforces.com/topic/152947/en1](https://codeforces.com/topic/152947/en1)
- OI Wiki ✓ [https://oi-wiki.org/math/number-theory/gcd/](https://oi-wiki.org/math/number-theory/gcd/)
