---
id: fsm
name: 有限状态机
group: G-E-7
stage: advanced
priority: P2
depth_tier: standard
---

# 有限状态机

> FSM用于字符串匹配/自动机DP/AC自动机基础，竞赛中处理模式匹配问题

<!-- 元信息: id=fsm · group=G-E-7 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

有限状态机(Finite State Machine, FSM)是描述'按字符逐一转移状态'的数学模型。DFA 是五元组 (Q, Σ, δ, q0, F)：有限状态集、字符集、转移函数、起始状态、接受状态集。DFA 接受的语言恰为正则语言；NFA 与其等价(幂集构造)。竞赛应用：判断二进制数奇偶/偶长串、KMP 自动机、AC 自动机(Trie+失配链接)、后缀自动机、序列自动机、DP 套 DP(内层 DP 状态建自动机外层 DP 计数)。

## Why · 为什么

### 直觉 · Intuition

把'问题的所有中间可能'编码成图的状态，每个输入字符是一次转移。判定问题变成'按图走到底看停在哪'。例如判断二进制数奇偶只需两个状态(末位0/1)。自动机的价值在于把子序列/模式匹配这类'本需回溯'的问题变成 O(n) 的线性游走。

### 原理 · Principle

DFA 计算：从 q0 开始，对每个字符 w_i 执行 δ(r_i, w_i)=r_{i+1}，读完若 r_n ∈ F 则接受。NFA 转移返回状态集，等价于并行运行多个分支，可用幂集构造转成 DFA。复杂度：DFA 模拟 O(n)，朴素 NFA O(n·s²)，bitset 优化到 O(n·s²/w)。正则语言满足封闭性(并/交/补/连接/闭包/同态等)，Myhill–Nerode 定理给出最小 DFA 状态数=等价类数。

### 历史 · History

自动机理论源自 20 世纪中叶计算理论奠基人(Church, Turing, Kleene 等)的研究。FSM 作为最简单的计算模型，是正则语言与编译原理的词法分析基础。竞赛中 OI Wiki 专门设立 FSM 页面，强调在学习 KMP/AC 自动机/SAM 前先掌握自动机思想，并收录 DFA 最小化(Hopcroft 算法)与 DP 套 DP 等进阶内容。

## How · 实现

### 伪代码

```python
# 一般 DFA 模拟
def run_dfa(delta, q0, accept, s):
  q = q0
  for ch in s:
    q = delta[q][ch]
  return q in accept

# 例: 判断二进制串是否为偶数(从左到右, 末位决定)
# 状态 0: 已处理前缀对应偶数, 状态 1: 奇数
# 转移: 读0偶数保持偶, 读1变奇; 奇读0变偶, 奇读1保持奇
```

### Python 实现

```python
def is_even_binary(bits):
    """DFA 判定二进制串是否表示偶数。
    状态 q=0 表示当前前缀是偶数, q=1 表示奇数。
    """
    q = 0
    for ch in bits:
        if ch not in '01':
            raise ValueError('非法字符')
        if q == 0:
            q = 0 if ch == '0' else 1
        else:
            q = 0 if ch == '0' else 1
    return q == 0


def build_kmp_automaton(pattern):
    """构造 KMP 自动机。
    状态 i 表示已匹配 pattern 前 i 个字符;
    delta[i][c] 为读入 c 后应到的状态。
    用失配函数实现(简化版)。
    """
    m = len(pattern)
    # 前缀函数
    pi = [0] * m
    for i in range(1, m):
        j = pi[i - 1]
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        pi[i] = j
    # 字符集
    alpha = set(pattern)
    delta = {i: {c: 0 for c in alpha} for i in range(m + 1)}
    for i in range(m + 1):
        for c in alpha:
            if i < m and c == pattern[i]:
                delta[i][c] = i + 1
            elif i == 0:
                delta[0][c] = 0
            else:
                delta[i][c] = delta[pi[i - 1]][c]
    return delta, m


def kmp_count(text, pattern):
    """用自动机统计 pattern 出现次数(含重叠)。"""
    delta, m = build_kmp_automaton(pattern)
    q = 0
    cnt = 0
    for ch in text:
        if ch in delta[q]:
            q = delta[q][ch]
        else:
            q = 0
        if q == m:
            cnt += 1
    return cnt


if __name__ == '__main__':
    # 二进制偶数判定
    assert is_even_binary('0') is True
    assert is_even_binary('1') is False
    assert is_even_binary('1010') is True
    assert is_even_binary('101') is False
    assert all(is_even_binary(f'{i:b}') == (i % 2 == 0) for i in range(30))

    # KMP 自动机计数
    assert kmp_count('aaaa', 'aa') == 3
    assert kmp_count('ababcabab', 'ab') == 4   # 位置 0,2,5,7
    assert kmp_count('abc', 'def') == 0
    assert kmp_count('abcabc', 'abc') == 2
    assert kmp_count('abcababcabc', 'abc') == 3  # 位置 0,6,8(重叠)

    print('binary even check (0..29): OK')
    print('kmp automaton counts:')
    print('  aaaa/#aa  =', kmp_count('aaaa', 'aa'))
    print('  ababcabab/#ab =', kmp_count('ababcabab', 'ab'))
    print('  abcabc/#abc= ', kmp_count('abcabc', 'abc'))
    print('All fsm tests passed!')

```

**PyPy 提示**: 自动机 DP 大状态常用 dict 存转移或 list 索引; KMP/SAM 自动机用数组 delta 时 PyPy 快于 dict; 大规模自动机 DP 用递推而非递归。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | DFA 模拟 O(N)；KMP 自动机构造 O(M\|Σ\|)；朴素 NFA O(N·S²) |
| 空间 | O(S·\|Σ\|) — 转移表; NFA 需存状态集 |

### 局限

自动机只接受正则语言, 无法识别非正则语言(如 a^n b^n); 状态数指数爆炸场景(幂集构造)需谨慎; 单纯 FSM 不是算法, 具体实现与优化(表/递归)影响常数; 处理任意模式匹配仍需 KMP/AC 等特定构造。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P12294 | 5 | THUPC2025决赛 01串三目运算: Myhill–Nerode定理建自动机+倍增/猫树 | [https://www.luogu.com.cn/problem/P12294](https://www.luogu.com.cn/problem/P12294) |
| Luogu | P10436 | 5 | JOISC2024 卡牌收集: 自动机状态压缩+区间查询 | [https://www.luogu.com.cn/problem/P10436](https://www.luogu.com.cn/problem/P10436) |
| Codeforces | 956F | 5 | Minimal Subset Difference: 内层DP建自动机+DFA最小化, DP套DP经典 | [https://codeforces.com/contest/956/problem/F](https://codeforces.com/contest/956/problem/F) |

## Pitfalls · 易错点

- 自动机是模型不是算法: 描述时需明确转移表与失配状态, 别漏未定义字符的转移
- KMP 自动机要处理失配回退: 未定义转移在竞赛中常加一个显式 fail 状态
- DFA 计算复杂度 O(n) 但转移表空间 O(S\|Σ\|); 字符集大时用 dict 稀疏存储
- NFA 多分支必须并行维护状态集, 勿用单状态直接模拟
- DP 套 DP 的'内层DP状态'是外层状态, 构造前先确认状态上界避免指数爆炸

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/misc/fsm/](https://oi-wiki.org/misc/fsm/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/fsm.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/fsm.md)
- web ✓ [https://en.wikipedia.org/wiki/Finite-state_machine](https://en.wikipedia.org/wiki/Finite-state_machine)
