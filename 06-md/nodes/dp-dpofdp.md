---
id: dp-dpofdp
name: DP套DP
group: G-A-13
stage: advanced
priority: P3
depth_tier: brief
---

# DP套DP

> 外层DP的状态是内层DP的结果（DFA状态），内层DP被抽象为自动机供外层转移，用于序列计数/概率/期望问题

<!-- 元信息: id=dp-dpofdp · group=G-A-13 · stage=advanced · priority=P3 · depth_tier=brief -->

## What · 是什么

DP套DP（DP of DP）指在动态规划中把一个子问题的求解过程（内层DP，通常用来判断合法或计算某个属性）抽象成一个自动机（DFA），再在外层设计一层DP在自动机上统计。典型结构：给定字符集 Σ 和长度 n 的合法序列集合 A⊆Σ^n，对每个序列 s 用一个内层 DP 判定合法性/求值，最终要统计 A 的计数、总权值、期望等。若内层 DP 的状态转移可写成 g(i,·;s)=G(g(i−1,·;s), s_i)，则 g 的取值集合就是自动机状态 Q，外层 DP f(i,q) 统计处理到长度 i 时落在自动机状态 q 的前缀数，f(i,q)=Σ_c Σ_{q'∈Q:δ(q',c)=q} f(i−1,q')。关键技巧是状态压缩：如 Hero meet devil 中记录 LCS 行向量的差分数组（每项 0/1），状态数 2^{|S|}；如 ZJOI2019 麻将中把'是否可胡'判断压缩为状态机。

## Why · 为什么

### 直觉 · Intuition

不能枚举所有序列（指数级），但合法的判定过程本身信息量不大：内层 DP 跑完一个前缀后留下的'状态快照'是有限的（通常可压缩）。于是把'内层 DP 在当前前缀结束后的状态'当作自动机状态，外层 DP 只需数'走到每个自动机状态有几种前缀'，就完成了计数。

### 原理 · Principle

内层 DP g(i,·;s) 只由 g(i−1,·;s) 与当前字符 s_i 决定（无后效性），等价于 DFA 的转移函数 δ。将 Q 压缩（状态压缩或 DFA 最小化）后，外层 DP 在 DFA 的 DAG 上做路径计数。接受状态集 F 对应合法序列，答案由 f(n, q∈F) 求和。DP套DP 的复杂度 = 外层长度 n × 自动机状态数 |Q| × 字符集大小 |Σ|。

### 历史 · History

DP套DP 的名称与技巧在国内竞赛圈主要由 ZJOI2019 麻将（期望摸牌次数）与 Hero meet devil（LCS 计数）等题传播，OI Wiki 以'DP 套 DP'专题收录并给出 DFA 化框架。它与'自动机 DP'（如数位 DP、AC 自动机 + 计数 DP）思想同源。

## How · 实现

### 伪代码

```python
# 通用框架
# 1. 设计内层 DP g(i, state; s)，判定/求值
# 2. 压缩 state 为 DFA 状态 q（状态压缩 / 差分 / DFA 最小化）
# 3. 建转移: next[q][c] = G(q, c)
# 4. 外层 DP: f[i+1][next[q][c]] += f[i][q]
# 5. 答案 = sum_{q in F} f[n][q]
```

### Python 实现

```python
# -*- coding: utf-8 -*-
# 例：Hero meet devil 简化版 —— 给定 S(小写字母)，统计长度 m 的串 T
# 与 S 的 LCS 长度分布（字符集 'ab' 简化为 2 个字符便于教学）

def lcs_count(S, m, sigma='ab'):
    """返回列表 ans[i] = 与 S 的 LCS 恰为 i 的串 T 的个数。"""
    n = len(S)

    # 内层 LCS DP 的行向量压缩：差分数组 mask
    def row_to_mask(row):
        # row: list 长 n+1, row[j]=LCS(T前缀, S[:j])
        mask = 0
        for j in range(1, n + 1):
            if row[j] - row[j - 1] == 1:
                mask |= 1 << (j - 1)
        return mask

    def mask_to_row(mask):
        row = [0] * (n + 1)
        for j in range(1, n + 1):
            row[j] = row[j - 1] + ((mask >> (j - 1)) & 1)
        return row

    # 转移表：自动机状态 mask 读入字符 ch -> 新 mask
    def trans(mask, ch):
        row = mask_to_row(mask)
        nrow = [0] * (n + 1)
        for j in range(1, n + 1):
            add = 1 if S[j - 1] == ch else 0
            nrow[j] = max(row[j], nrow[j - 1], row[j - 1] + add)
        return row_to_mask(nrow)

    # 外层 DP
    dp = {0: 1}
    for _ in range(m):
        nd = {}
        for mask, cnt in dp.items():
            for ch in sigma:
                nm = trans(mask, ch)
                nd[nm] = nd.get(nm, 0) + cnt
        dp = nd
    ans = [0] * (n + 1)
    for mask, cnt in dp.items():
        ans[mask.bit_count()] += cnt
    return ans


if __name__ == '__main__':
    import itertools
    S = 'ab'
    m = 3
    got = lcs_count(S, m, sigma='ab')
    # 暴力验证
    brute = [0] * (len(S) + 1)
    for T in itertools.product('ab', repeat=m):
        T = ''.join(T)
        dp = [[0] * (len(T) + 1) for _ in range(len(S) + 1)]
        for i in range(1, len(S) + 1):
            for j in range(1, len(T) + 1):
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1],
                               dp[i - 1][j - 1] + (S[i - 1] == T[j - 1]))
        brute[dp[len(S)][len(T)]] += 1
    assert got == brute, (got, brute)
    print('dp-of-dp tests passed:', got)

```

**PyPy 提示**: 状态数 2^{\|S\|}，外层 DP 用 dict 转移；m、\|S\| 不大（≤20 左右）可跑。正式题常用矩阵快速幂优化外层转移（转移固定时）。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(m · \|Q\| · \|Σ\|)，其中 \|Q\| 为压缩后自动机状态数（如 2^{\|S\|}-1） |
| 空间 | O(\|Q\|) |

### 局限

内层状态必须可压缩为有限自动机；状态数可能仍巨大（需巧妙压缩或 DFA 最小化）。设计内层状态机 + 转移表较难，是典型的'思维题'而非模板题。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P10614 | 5 | Hero meet devil：LCS 行向量差分压缩成 2^{\|S\|} 状态，外层计数 | [https://www.luogu.com.cn/problem/P10614](https://www.luogu.com.cn/problem/P10614) |
| LibreOJ | 3042 | 7 | ZJOI2019 麻将：将'可胡判定'压成状态机 + 期望计数，DP套DP 经典难题 | [https://loj.ac/p/3042](https://loj.ac/p/3042) |

## Pitfalls · 易错点

- 内层 DP 状态压缩必须无损：差分/映射保持全部转移所需信息
- 外层 DP 状态是自动机状态而非具体答案，转移表要预先对所有 (q,c) 建好
- 接受状态 F 的判定要在内层状态机里显式编码（何时合法）
- 期望/概率版本需结合尾和公式等期望技巧，不能只数合法序列

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/dp/dp-of-dp/](https://oi-wiki.org/dp/dp-of-dp/)
- 书籍 ✓ `OI Wiki DP 套 DP 专题（含 Hero meet devil / 麻将题解）`
