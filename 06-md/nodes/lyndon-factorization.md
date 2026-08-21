---
id: lyndon-factorization
name: Lyndon分解
group: G-C-6
stage: advanced
priority: P2
depth_tier: standard
---

# Lyndon分解

> Duval 算法 O(n) 将字符串分解为字典序非严格递减的 Lyndon 串，同时给出最小循环移位；周期性与字典序的强力工具

<!-- 元信息: id=lyndon-factorization · group=G-C-6 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

Lyndon 串（简单串）：s 严格小于它的所有非平凡后缀（等价地严格小于所有非平凡循环同移）。例：a,b,ab,aab,abb,ababb,abcd 是 Lyndon 串。Lyndon 分解：s=w1w2…wk，每个 wi 是 Lyndon 串且 w1≥w2≥…≥wk（非严格递减），存在且唯一。Duval 算法在 O(n) 时间、O(1) 附加空间求出分解：维护三个指针 i（s2 起点）、j（s3 起点）、k（s2 中当前比较位），把当前串分为已定分解 s1、近似 Lyndon 串 s2（形如 ww…w·前缀）、未处理 s3。比较 s[j] 与 s[k]：相等则 j,k 各 +1；s[j]>s[k] 则 s2+s[j] 成为新的 Lyndon 串（j+1,k 回到 i）；s[j]<s[k] 则 s2 不再近似简单，截出长度 j−k 的循环节（Lyndon 串）加入分解，i 前进。推论应用：最小循环移位（对 ss 做 Duval，找跨越中点且起点<n 的 Lyndon 块起点）。

## Why · 为什么

### 直觉 · Intuition

Lyndon 串直觉上'自己最小'：任何后缀都不比它小。分解唯一性的关键是：s 中第一个 Lyndon 块必须是最长的满足'w 是 Lyndon 串且是前缀'的块，之后递归。Duval 的近似简单串 s2=w^t·w'（w' 是 w 的前缀）说明 s2 本身尚不能拆分，只有当 s[j]<s[k] 破坏周期性时才截出整块 w。

### 原理 · Principle

Duval 正确性：设 i 指向 s2 起点，j 指向 s3 首字符，k 在 s2 中与 s[j] 对应比较。①s[j]==s[k]：s2+s[j] 仍近似简单（周期结构延续），j++,k++；②s[j]>s[k]：由于 s2 是近似简单且比较位更大，s2+s[j] 成为严格 Lyndon 串（字典序小于所有后缀），k 重置为 i，s2 变长为新的 w^1；③s[j]<s[k]：s2+s[j] 破坏近似简单，此时 s2 中周期为 j−k 的整块（长度 j−k）是可确定的 Lyndon 分解块，从 i 开始截出（长度 j−k）加入答案，i+=j−k，循环直到 i>k（即余下部分重新作为 s2）。复杂度：外层 while 每轮 i 增加；内层比较总次数 O(n)（每轮比较的'剩余'长度递减，界 4n−3）。最小循环移位：ss 的 Lyndon 分解中，唯一满足'起点<n 且终点≥n'的块 w 的起点即为最小循环移位的起点（可用 w 的字典序最小性证明）。

### 历史 · History

Lyndon 串与分解得名于 R. C. Lyndon（1954，研究自由群的字问题），Chen–Fox–Lyndon 定理（1958）给出分解的存在唯一性。Duval 算法由 Jean-Pierre Duval 于 1983 年提出，O(n) 线性时间，是竞赛中求 Lyndon 分解与最小表示的标准算法（OI Wiki 与 CP-Algorithms 均收录）。最小表示问题（UVa 719 Glass Beads）与循环字符串处理是其主要应用。

## How · 实现

### 伪代码

```python
# Duval 算法
factorization = []
i = 0
while i < n:
    j, k = i+1, i
    while j < n and s[k] <= s[j]:
        if s[k] < s[j]: k = i      # 成为新的 Lyndon 串
        else: k += 1
        j += 1
    while i <= k:
        factorization.append(s[i : i + j - k])
        i += j - k
return factorization

# 最小循环移位
s = s + s; n = len(s)
i, ans = 0, 0
while i < n//2:
    ans = i
    j, k = i+1, i
    while j < n and s[k] <= s[j]:
        if s[k] < s[j]: k = i
        else: k += 1
        j += 1
    while i <= k: i += j - k
return s[ans : ans + n//2]
```

### Python 实现

```python
# -*- coding: utf-8 -*-
# Duval 算法：O(n) 求 Lyndon 分解

def duval(s):
    """返回 s 的 Lyndon 分解（块列表，字典序非严格递减）。"""
    n, i = len(s), 0
    fac = []
    while i < n:
        j, k = i + 1, i
        while j < n and s[k] <= s[j]:
            if s[k] < s[j]:
                k = i               # s2+s[j] 成为新的 Lyndon 串
            else:
                k += 1
            j += 1
        while i <= k:               # 截出循环节长度 j-k
            fac.append(s[i:i + j - k])
            i += j - k
    return fac


def is_lyndon(s):
    """判断 s 是否为 Lyndon 串（严格小于所有非平凡后缀）。"""
    return all(s < s[i:] for i in range(1, len(s)))


def min_cyclic_shift_duval(s):
    """最小循环移位：对 ss 做 Duval，跨中点的 Lyndon 块起点即答案。"""
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
    return ss[ans:ans + n // 2]


if __name__ == '__main__':
    # 分解性质验证：每个块是 Lyndon 串且块字典序非严格递减，拼接还原
    for s in ['ababab', 'aaaa', 'ababac', 'banana', 'aababbababb']:
        fac = duval(s)
        assert ''.join(fac) == s
        assert all(is_lyndon(w) for w in fac)
        assert all(fac[i] >= fac[i + 1] for i in range(len(fac) - 1)), fac
    assert duval('ababab') == ['ab', 'ab', 'ab']
    assert duval('aaaa') == ['a', 'a', 'a', 'a']
    # 最小循环移位与暴力对拍
    import random
    random.seed(0)
    for _ in range(300):
        n = random.randint(1, 10)
        t = ''.join(random.choice('abc') for _ in range(n))
        shifts = [t[i:] + t[:i] for i in range(n)]
        assert min_cyclic_shift_duval(t) == min(shifts), (t, min_cyclic_shift_duval(t), min(shifts))
    # 分解唯一性：暴力检查所有合法分解（小规模）
    import itertools
    for s in ['aab', 'ababa', 'baba']:
        n = len(s)
        ways = []
        for cut in range(1 << (n - 1)):
            parts, last = [], 0
            for bit in range(n - 1):
                if (cut >> bit) & 1:
                    parts.append(s[last:bit + 1]); last = bit + 1
            parts.append(s[last:])
            if all(is_lyndon(p) for p in parts) and all(parts[i] >= parts[i + 1] for i in range(len(parts) - 1)):
                ways.append(parts)
        assert ways == [duval(s)], (s, ways, duval(s))
    print('lyndon-factorization tests passed')

```

**PyPy 提示**: Duval 是 O(n) 纯指针算法，PyPy 下可处理 1e6 长度。切片 s[i:i+j-k] 建块会 O(n) 内存，若只需块数/长度可直接累加。最小循环移位用双指针算法更省（见 minimal-string 节点）。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | Duval O(n)（总比较次数 ≤4n−3）；判断 Lyndon 串 O(n)；最小循环移位 O(n) |
| 空间 | O(n)（分解结果）/ O(1)（仅长度信息） |

### 局限

分解唯一但构造需小心指针细节；块字典序非严格递减（可相等）。最小循环移位用 Duval 需拼接 ss 并正确处理 n/2 边界。Lyndon 分解与后缀数组/最小表示联系紧密，需理解字典序比较严格性（'<' 与 '<='）。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| UVa | 719 | 3 | Glass Beads：最小循环移位（Duval 或双指针）模板题 | [https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=660](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=660) |
| Luogu | P1368 | 3 | 最小表示法：求循环串字典序最小的起点（双指针或 Duval） | [https://www.luogu.com.cn/problem/P1368](https://www.luogu.com.cn/problem/P1368) |

## Pitfalls · 易错点

- 比较是 s[k] <= s[j] 才继续，s[k] < s[j] 时 k 回 i 而不是 k+=1
- 截块长度是 j-k 不是 j-i，且条件是 while i <= k 而非 i < j
- 最小循环移位的 while 条件 i < n//2，且返回 ss[ans:ans+n//2]
- 分解的块要满足 w_i >= w_{i+1}（非严格递减），验证时注意相等允许
- Lyndon 串要求'严格'小于后缀，全等块（如 aaa）不构成单一 Lyndon 串

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/string/lyndon/](https://oi-wiki.org/string/lyndon/)
- CP-Algorithms ✓ [https://cp-algorithms.com/string/lyndon_factorization.html](https://cp-algorithms.com/string/lyndon_factorization.html)
