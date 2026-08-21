---
id: seq-automaton
name: 序列自动机
group: G-C-4
stage: advanced
priority: P2
depth_tier: standard
---

# 序列自动机

> 接受一个串所有子序列的最小自动机：next[i][c]=i 之后字符 c 第一次出现的位置，O(n\|Σ\|) 构造，用于子序列匹配与计数 DP

<!-- 元信息: id=seq-automaton · group=G-C-4 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

序列自动机（sequence automaton）是接受且仅接受给定串 s 的全部子序列的 DFA：状态 0..n（n=|s|），状态 i 表示'已匹配到 s 的前 i 个字符'，转移 δ(i,c)=s 中 i 之后（严格大于 i）字符 c 第一次出现的位置，即 next[i][c]=min{j | j>i, s[j]=c}（不存在为 null）。所有状态都是接受状态。构造：从后向前扫描，维护每个字符当前最近出现位置 last[c]，则 next[i][c]=last[c]，之后 last[s[i]]=i。复杂度 O(n|Σ|)。应用：判断 t 是否为 s 的子序列（贪心沿 next 走，O(|t|)）；计数 s 的不同子序列数；与其他自动机叠加做 DP（如 HEOI2015 最短不公共子序列）；字典序第 k 小子序列等。

## Why · 为什么

### 直觉 · Intuition

判断子序列的贪心：匹配时总是选'最靠前的下一个字符'最优——因为越靠前的后缀，包含的子序列越多（后缀 s[i..] 的子序列集合是 s[j..] 的子集，对 i>j）。所以每个状态只需记录每个字符下一次出现的最前位置，这就是转移表。

### 原理 · Principle

转移 δ(u,c)=min{i|i>u, s[i]=c}。构造从后往前：维护 last[c] 表示扫描过的后缀中 c 的最前出现位置，则 next[i][c]=last[c]（即 i 之后 c 第一次出现）；随后更新 last[s[i]]=i。正确性：贪心选最前位置不会丢解，因为若用更靠后的位置能匹配成功，改用更靠前的位置也一定能成功（后者是前者子序列的超集）。所有状态均接受（空串与任意子序列都可停止）。子序列计数：不同子序列数可在 DAG 上 DP（状态数 n+1，转移去重）。多自动机叠加：如求'最短的既不是 A 子串也不是 B 子序列的串'，在 A 的 SAM 与 B 的序列自动机上做双自动机 BFS/DP。

### 历史 · History

序列自动机是自动机理论中'子序列识别'的经典构造，竞赛中由 OI Wiki 等以'序列自动机'专题整理推广，常用于子序列匹配、子序列计数及与 SAM/AC 自动机叠加的'最短非公共子序列'类题目（如 HEOI2015）。

## How · 实现

### 伪代码

```python
# 构造 O(n|Σ|)
last[c] = null (所有 c)
next = [n+1][|Σ|] 全 null
for i = n-1 downto 0:
    for c in Σ: next[i][c] = last[c]
    last[s[i]] = i
# 判断 t 是否子序列
pos = 0
for ch in t:
    pos = next[pos][ch]
    if pos == null: return False
    pos += 1    # 匹配后移到 pos+1
return True
```

### Python 实现

```python
# -*- coding: utf-8 -*-
# 序列自动机：状态 i 表示已匹配 s[0..i-1]（消耗了前 i 个字符）。
# next[i][c] = s 中位置 >= i 的字符 c 第一次出现的位置；不存在为 -1。
# 匹配时：u = next[u][ch]；若为 -1 失败；否则 u += 1（消耗该字符）。
def build_seq(s, sigma=26):
    """返回 next: (n+1) x sigma 数组。"""
    n = len(s)
    nxt = [[-1] * sigma for _ in range(n + 1)]
    last = [-1] * sigma                 # 扫描过的后缀中 c 的最前出现位置
    for i in range(n, 0, -1):           # 状态 i 的转移来自位置 >= i 的后缀
        nxt[i] = last[:]
        last[ord(s[i - 1]) - 97] = i - 1
    nxt[0] = last[:]                    # 状态 0 可用整个串（位置 >= 0）
    return nxt


def is_subsequence(nxt, t, sigma=26):
    """判断 t 是否为 s 的子序列。"""
    u = 0
    for ch in t:
        u = nxt[u][ord(ch) - 97]
        if u == -1:
            return False
        u += 1                          # 消耗该字符，下次查找从 u 开始
    return True


def count_distinct_subseq(s, sigma=26):
    """s 的不同子序列数（含空串）。经典去重 DP：g(u)=2*g(u+1)-g(同字符下次出现位置+1)。"""
    n = len(s)
    g = [0] * (n + 1)
    g[n] = 1
    nxtp = [-1] * sigma                 # 当前位置右边同字符首次出现
    for i in range(n - 1, -1, -1):
        c = ord(s[i]) - 97
        g[i] = 2 * g[i + 1]
        p = nxtp[c]                     # s[i] 在 i 之后第一次出现的位置
        if p != -1:
            g[i] -= g[p + 1]
        nxtp[c] = i
    return g[0]


if __name__ == '__main__':
    s = 'abcde'
    nxt = build_seq(s)
    for t in ['ace', 'aec', 'b', 'ad', '', 'zz', 'de']:
        def brute(t):
            i = 0
            for ch in s:
                if i < len(t) and ch == t[i]:
                    i += 1
            return i == len(t)
        assert is_subsequence(nxt, t) == brute(t), (t, is_subsequence(nxt, t), brute(t))
    import random
    random.seed(0)
    for _ in range(200):
        n = random.randint(1, 10)
        s2 = ''.join(random.choice('abc') for _ in range(n))
        nx = build_seq(s2)
        for _ in range(10):
            m = random.randint(0, 6)
            t = ''.join(random.choice('abc') for _ in range(m))
            def brute2(t):
                i = 0
                for ch in s2:
                    if i < len(t) and ch == t[i]:
                        i += 1
                return i == len(t)
            assert is_subsequence(nx, t) == brute2(t), (s2, t)
    # 不同子序列数暴力验证
    for s3 in ['ab', 'aaa', 'abc', 'aba', 'abcabc', 'banana']:
        n3 = len(s3)
        alls = set([''])
        for i in range(n3):
            for j in range(i + 1, n3 + 1):
                for mask in range(1 << (j - i)):
                    sub = ''.join(s3[i + k] for k in range(j - i) if (mask >> k) & 1)
                    alls.add(sub)
        assert count_distinct_subseq(s3) == len(alls), (s3, count_distinct_subseq(s3), len(alls))
    print('seq-automaton tests passed')

```

**PyPy 提示**: next 数组 (n+1)×\|Σ\|，n≤1e5、Σ=26 时内存约 26e6 int（PyPy 下偏大）；可用 dict 稀疏化或只在需要时构建。子序列计数/最短非公共子序列的 DP 注意状态规模。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 构造 O(n\|Σ\|)；子序列判断 O(\|t\|)；子序列计数 O(n\|Σ\|) |
| 空间 | O(n\|Σ\|) |

### 局限

只能处理单个串的子序列；构造需要 |Σ| 空间。多自动机叠加（SAM+seq-auto）做最短非公共子串/子序列时状态是两者的笛卡尔积，注意剪枝。字符集大时 O(n|Σ|) 不可行。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| LibreOJ | 2123 | 4 | HEOI2015 最短不公共子串：四问，其中子序列问用序列自动机 DP/叠加 SAM | [https://loj.ac/p/2123](https://loj.ac/p/2123) |
| Luogu | P3976 | 4 | 子序列计数类（不同子序列数），序列自动机/DP 均可 | [https://www.luogu.com.cn/problem/P3976](https://www.luogu.com.cn/problem/P3976) |

## Pitfalls · 易错点

- next[i][c] 记的是'第一次出现位置'，判断子序列时要 pos+=1 跳过已用字符
- 状态从 0（未匹配）到 n（匹配完整个 s），n+1 个状态；next[n] 全为 -1
- 构造是倒序扫描，last 数组维护后缀最前出现，顺序错了会错位
- 不同子序列计数去重公式易错：dp[i]=1+Σ(dp[nxt+1]−1)，不要漏减重复空串
- 字符集下界注意：'a'..'z' 的偏移或离散化

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/string/seq-automaton/](https://oi-wiki.org/string/seq-automaton/)
- 书籍 ✓ `HEOI2015 最短不公共子串（loj 2123）题解`
