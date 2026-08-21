---
id: kahan-summation
name: Kahan求和
group: G-E-7
stage: advanced
priority: P2
depth_tier: standard
---

# Kahan求和

> 补偿求和法降低浮点累加误差：维护误差补偿变量c，精度接近double但只多一个变量

<!-- 元信息: id=kahan-summation · group=G-E-7 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

Kahan 求和(补偿求和/进位求和)通过额外变量 c 累积每次浮点加法丢失的低位误差，显著降低大量浮点数累加时的舍入误差。标准实现：y=num-c; t=sum+y; c=(t-sum)-y; sum=t。c 捕捉的是't 无法表示 y 的低位'被丢掉的量，下一轮补偿回去。Python 标准库 math.fsum 用 Shewchuk 算法得到精确舍入，效果更优。

## Why · 为什么

### 直觉 · Intuition

浮点加法不满足结合律：sum 变大后，加小量 y 时低位被吞掉。Kahan 用 (t-sum)-y 把这次吞掉的量算出来存进 c，下轮先把它加进 y，于是误差被'找零'式地补偿。c 在代数值上总保持接近 0。

### 原理 · Principle

设 sum 大 y 小。t=sum+y 时 y 的低位丢失。代数上 (t-sum) 恢复 y 的'高位部分'，(t-sum)-y 为负，恰为丢失的低位(取负)，存入 c。下一轮 y'=num-c 就把上次丢失的低位提前加回，从而补偿。此即误差补偿(compensation)机制，由 William Kahan 于 1960s 发现；Ivo Babuška 独立提出类似算法，故又称 Kahan–Babuška 求和。

### 历史 · History

William Kahan 因浮点误差研究获 1989 年图灵奖。Kahan 求和算法 1960s 提出，是 IEEE-754 浮点生态的基础补偿技巧。OI Wiki 将该算法收录为 misc 页面，并指出 Python 的 math.fsum(Shewchuk 多部分和算法)与 Julia 的 sum_kbn(Neumaier 变体)等更优实现的存在。

## How · 实现

### 伪代码

```python
def kahan_sum(nums):
  sum_ = 0.0
  c = 0.0
  for num in nums:
    y = num - c
    t = sum_ + y
    c = (t - sum_) - y   # 捕获本次丢失的低位(负值)
    sum_ = t
  return sum_
```

### Python 实现

```python
import math


def kahan_sum(nums):
    """Kahan 补偿求和。返回浮点累加和。"""
    s = 0.0
    c = 0.0
    for num in nums:
        y = num - c
        t = s + y
        c = (t - s) - y
        s = t
    return s


def naive_sum(nums):
    """朴素从左到右累加(手写循环, 不用 Python 内置 sum, 因其自带补偿)。"""
    s = 0.0
    for x in nums:
        s += x
    return s


if __name__ == '__main__':
    # 场景1: 2^53 之后 +1.0 每次都被吞(ulp=2), 朴素全丢
    big = 2.0 ** 53
    seq = [big] + [1.0] * 100 + [-big]
    r_naive = naive_sum(seq)
    r_kahan = kahan_sum(seq)
    print(f'2^53+100x1.0-2^53: naive={r_naive}, kahan={r_kahan} (期望 100.0)')
    assert abs(r_naive - 100.0) > 50       # 朴素丢失全部 1.0
    assert abs(r_kahan - 100.0) < 1e-9     # Kahan 找回

    # 场景2: 1e16 + 1000x1.0 + (-1e16)
    seq2 = [1e16] + [1.0] * 1000 + [-1e16]
    print(f'1e16+1000x1.0-1e16: naive={naive_sum(seq2)}, kahan={kahan_sum(seq2)} (期望 1000.0)')
    assert abs(naive_sum(seq2) - 1000.0) > 500
    assert abs(kahan_sum(seq2) - 1000.0) < 1e-9

    # 场景3: 10000 x 0.1 累加误差
    many = [0.1] * 10000
    n = naive_sum(many)
    k = kahan_sum(many)
    print(f'10000x0.1: naive={n:.17g}, kahan={k:.17g}, fsum={math.fsum(many):.17g}')
    assert abs(k - 1000.0) <= abs(n - 1000.0) and abs(k - 1000.0) < 1e-9

    print('All kahan-summation tests passed!')

```

**PyPy 提示**: Kahan 求和是纯算术循环, PyPy 效率尚可; 若只需精确求和直接用 math.fsum(内置, C 实现更快更准); 竞赛中浮点精度敏感题(几何/数值)常配合 epsilon 比较。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(N) — 每次加法固定 4 次浮点运算 |
| 空间 | O(1) — 仅需两个累加变量 |

### 局限

Kahan 只降低舍入误差, 不消除(病态条件数时仍可能不够); 不适合大规模并行累加(可用分块/成对求和); Python 下更优选择是 math.fsum(Shewchuk 算法, 精确舍入); 对非浮点(整数)无效。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Codeforces | 800A | 3 | Voltage Keepsake: 二分答案时浮点累加, 可用Kahan降低误差(OI Wiki例题) | [https://codeforces.com/contest/800/problem/A](https://codeforces.com/contest/800/problem/A) |
| Codeforces | 504B | 4 | Misha and Permutations Summation: 排列序数累加(大数场景) | [https://codeforces.com/problemset/problem/504/B](https://codeforces.com/problemset/problem/504/B) |
| LeetCode | 539 | 2 | 浮点时间差与累加场景, 体会精度对答案的影响 | [https://leetcode.cn/problems/minimum-time-difference/](https://leetcode.cn/problems/minimum-time-difference/) |

## Pitfalls · 易错点

- y=num-c 与 c=(t-sum)-y 的顺序不可调换, c 是'本次加法丢失的低位取负'
- Kahan 对极端病态求和仍可能不准, 不是万能; 关键数据用 math.fsum
- Python 的 float 是 double(53位), 1e16+1.0 必丢, 先理解再写补偿
- 多语言精度差异: C++ float/double 需要 Kahan, Python 大整数与 float 混用需注意
- c 不会随 sum 增大而无限增长(代数值保持~0), 但数量级差异过大时仍失效

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/misc/kahan-summation/](https://oi-wiki.org/misc/kahan-summation/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/kahan-summation.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/kahan-summation.md)
- web ✓ [https://en.wikipedia.org/wiki/Kahan_summation_algorithm](https://en.wikipedia.org/wiki/Kahan_summation_algorithm)
