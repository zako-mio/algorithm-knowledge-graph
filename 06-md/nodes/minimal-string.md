---
id: minimal-string
name: 最小表示法
group: G-C-6
stage: advanced
priority: P2
depth_tier: standard
---

# 最小表示法

> O(n) 求循环字符串字典序最小的起始位置：双指针跳过法或 Lyndon/Duval 法，用于循环同构判断与去重

<!-- 元信息: id=minimal-string · group=G-C-6 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

最小表示问题：给定字符串 s（长度 n），求与 s 循环同构的所有字符串（s[i:]+s[:i]）中字典序最小的一个，或其起始位置。经典算法是双指针：维护两个候选起点 i、j，比较位置 k 上的字符：若 s[i+k]==s[j+k] 则 k++；若 s[i+k]>s[j+k]，说明从 i 开始的任意起点 i'∈[i,i+k] 都不会是最小（因为存在对应的 j 起点更小），直接 i=i+k+1；对称地 j=j+k+1；当 i==j 时 j++；循环到 k==n 或越界，答案是 min(i,j)。复杂度 O(n)（均摊：每次比较要么 k 增大要么 i/j 跳跃）。也可用 Lyndon 分解/Duval 法（对 ss 分解跨中点块），或 SAM（对 ss 建 SAM 贪心走 n 步）。应用：判断两个串是否循环同构（最小表示相同）、字符串最小化重排等。

## Why · 为什么

### 直觉 · Intuition

暴力比较所有 n 个循环同构是 O(n²)（如 aaa…ab）。关键观察：若从 i 与 j 起头的串比较了 k 个字符后，在 i+k 处 s 更大，那么对于任意 i'∈[i,i+k]，从 i' 起头的串都不会优于从 j+(i'−i) 起头的串（两串前 n−k 段相同，i'+… 更大或更差）。因此可以直接把 i 跳到 i+k+1，剪掉整段不可能的解。

### 原理 · Principle

算法维护候选对 (i,j) 与匹配长度 k（s[i..i+k−1]==s[j..j+k−1]）。若 s[i+k]>s[j+k]：对任意 i'∈[i,i+k]，串 T_{i'}（从 i' 起）与 T_{j+i'−i}（从 j 起）的前段相同但 T_{i'} 在相应位置字符更大，故 T_{i'} 不可能是最小，i 跳到 i+k+1；s[i+k]<s[j+k] 对称跳 j。i==j 时强制 j++ 保持两候选不同。当 k==n（两串完全相等）或 i/j 越界 n 时终止，min(i,j) 即答案。正确性：每一轮至少让 i、j 之一严格增加，共 O(n) 轮；每轮内 k 单调增，总比较 O(n)。Lyndon 法：s+s 的 Duval 分解中跨过中点、起点<n 的 Lyndon 块起点即最小表示起点。

### 历史 · History

最小表示法（minimal representation）是中国 OI 圈经典技巧，OI Wiki 有专门条目；同问题在算法竞赛界也常称为'最小循环移位'（CP-Algorithms Lyndon factorization 一章给出 Duval 解法）。UVa 719 Glass Beads 是其经典模板题。双指针版由圈内选手广泛使用，Lyndon 版来源自 e-maxx。

## How · 实现

### 伪代码

```python
# 双指针最小表示（返回最小循环同构的起始位置）
ss = s + s
n = len(s)
i, j, k = 0, 1, 0
while i < n and j < n and k < n:
    a, b = ss[i+k], ss[j+k]
    if a == b:
        k += 1
    elif a > b:
        i = i + k + 1
        if i == j: i += 1
        k = 0
    else:
        j = j + k + 1
        if i == j: j += 1
        k = 0
ans = min(i, j)
return s[ans:] + s[:ans]
```

### Python 实现

```python
# -*- coding: utf-8 -*-
# 最小表示法：返回 s 的字典序最小循环同构

def minimal_string(s):
    """返回 s 的最小循环同构串与起始位置。"""
    n = len(s)
    ss = s + s
    i, j, k = 0, 1, 0
    while i < n and j < n and k < n:
        a, b = ss[i + k], ss[j + k]
        if a == b:
            k += 1
        elif a > b:
            i = i + k + 1
            if i == j:
                i += 1
            k = 0
        else:
            j = j + k + 1
            if i == j:
                j += 1
            k = 0
    ans = min(i, j)
    return ss[ans:ans + n], ans


def minimal_string_via_duval(s):
    """Lyndon/Duval 版：对 ss 做 Duval 分解，跨中点的块起点即最小表示。"""
    ss = s + s
    n = len(ss)
    i, ans = 0, 0
    while i < n // 2:
        ans = i
        j, k = i + 1, i
        while j < n and ss[k] <= ss[j]:
            if ss[k] < ss[j]:
                k = i
            else:
                k += 1
            j += 1
        while i <= k:
            i += j - k
    return ss[ans:ans + n // 2], ans


if __name__ == '__main__':
    import random
    for s in ['bcaa', 'aaaa', 'aba', 'abcabc', 'aab', 'zzzaa']:
        shifts = [s[i:] + s[:i] for i in range(len(s))]
        assert minimal_string(s)[0] == min(shifts), (s, minimal_string(s), min(shifts))
        assert minimal_string_via_duval(s)[0] == min(shifts), s
    random.seed(1)
    for _ in range(300):
        n = random.randint(1, 12)
        t = ''.join(random.choice('abc') for _ in range(n))
        shifts = [t[i:] + t[:i] for i in range(n)]
        m = min(shifts)
        assert minimal_string(t)[0] == m, (t, minimal_string(t)[0], m)
        assert minimal_string_via_duval(t)[0] == m, t
        # 起始位置一致性（多个同构相等时位置不必唯一，但字符串要一致）
        got, pos = minimal_string(t)
        assert got == m and got == t[pos:] + t[:pos]
    print('minimal-string tests passed')

```

**PyPy 提示**: 双指针版 O(n) 且常数极小，PyPy 处理 1e6 无压力。注意拼接 ss=s+s 内存 O(n)；若只需位置可不拼接用取模访问。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n)（均摊：i/j 单调增 + k 单调增） |
| 空间 | O(n)（拼接 ss）或 O(1)（取模不拼接） |

### 局限

双指针版实现细节（i==j 处理、k 重置）易错；在多个相同循环同构时返回的是第一个最小位置。Lyndon 版依赖 Duval 边界正确。判断循环同构需注意长度不同的串。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| UVa | 719 | 3 | Glass Beads：最小循环移位（双指针或 Duval）模板题 | [https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=660](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=660) |
| Luogu | P1368 | 3 | 最小表示法：求循环串字典序最小的起点，双指针模板 | [https://www.luogu.com.cn/problem/P1368](https://www.luogu.com.cn/problem/P1368) |

## Pitfalls · 易错点

- i==j 时必须把其中一个 +1 再置 k=0，否则无限循环
- 跳转用 i=i+k+1（不是 i+=1），否则退化为 O(n²)
- k 达到 n 时（两个候选串完全相同）终止，答案取 min(i,j)
- 比较用 s+s 的取模或拼接，越界处理要小心
- Duval 版返回的是 ss 中位置，需取 ans<n 且长度 n

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/string/minimal-string/](https://oi-wiki.org/string/minimal-string/)
- CP-Algorithms ✓ [https://cp-algorithms.com/string/lyndon_factorization.html](https://cp-algorithms.com/string/lyndon_factorization.html)
