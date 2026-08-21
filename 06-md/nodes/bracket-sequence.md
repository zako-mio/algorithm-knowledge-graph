---
id: bracket-sequence
name: 括号序列专题
group: G-D-9
stage: intermediate
priority: P2
depth_tier: standard
---

# 括号序列专题

> 合法括号序列的判定、计数（卡特兰数）、字典序后继、线段树维护括号序列的匹配（前缀和/最小值），以及 CF380C 等经典模型。

<!-- 元信息: id=bracket-sequence · group=G-D-9 · stage=intermediate · priority=P2 · depth_tier=standard -->

## What · 是什么

括号序列问题围绕『合法括号序列（balanced bracket sequence）』展开：由 '(' 和 ')' 组成，满足任意前缀 '(' 数 ≥ ')' 数且总 '(' 数 = ')' 数（可递归定义：空串合法；s 合法则 (s) 合法；s,t 合法则 st 合法）。经典问题包括：① 判定合法性（栈，O(n)）；② 计数——长度为 2n 的合法序列数为卡特兰数 C_n = C(2n,n)/(n+1)（k 种括号则乘 k^n）；③ 字典序后继/字典序排名；④ 区间操作版——用线段树维护区间内『未匹配的 '(' 数』与『未匹配的 ')' 数』，支持括号序列的区间查询与修改（CF380C 模型：匹配括号对数）。

## Why · 为什么

### 直觉 · Intuition

括号序列与『栈』和『平衡（Dyck 语言）』同构：把 '(' 记为 +1、')' 记为 -1，则合法序列是前缀和恒非负且总和为 0 的 ±1 序列。这个映射让很多看似组合的括号问题变成简单的『前缀和/最小值』问题，从而能用线段树等区间结构维护。计数之所以是卡特兰数，因为按第一个 '(' 的匹配位置把序列切两半，两半各自合法，递推式 f_n = Σ f_i·f_{n-i-1} 恰是卡特兰数递推。

### 原理 · Principle

① 判定：从左到右维护栈；遇 '(' 压栈，遇 ')' 且栈顶为对应左括号则弹栈，否则压入；结束时栈空则合法。② 计数：f_n = Σ_{i=0}^{n-1} f_i·f_{n-i-1} = C(2n,n)/(n+1)（卡特兰数）；k 种括号类型时乘 k^n。③ 字典序后继：找最大的 i 使 s[i]=='(' 且把其改为 ')' 后前缀仍合法（s[1..i-1] 中 '(' 数 > ')' 数），再把后缀重排成字典序最小的形式。④ 线段树维护：节点存 (unmatched_open, unmatched_close)，合并 (a_open,a_close) 与 (b_open,b_close) 得 (a_open+b_open-min(a_open,b_close), a_close+b_close-min(a_open,b_close))，这样区间内匹配对数 = 长度/2 - (open+close)/2；支持区间翻转（把 '('↔')' 交换时 open/close 互换）。

### 历史 · History

括号序列与 Dyck 语言、卡特兰数密不可分，卡特兰数由欧拉（Euler）在 1751 年左右研究多边形三角剖分时发现，以比利时数学家 Eugène Charles Catalan 命名。括号序列的判定/计数是组合数学经典；线段树维护括号匹配在 CF380C（Sereja and Brackets）等题目中成为区间数据结构模板。CP-Algorithms 与 OI Wiki 均有系统章节。

## How · 实现

### 伪代码

```python
# 判定合法（栈）
stack = []
for c in s:
    if c == '(' : stack.push(c)
    elif c == ')' and stack and stack.top == '(': stack.pop()
    else: stack.push(c)
return len(stack) == 0

# 线段树维护（区间匹配对数）
node = (open, close)  # 区间内未匹配的左右括号数
merge(a, b):
    match = min(a.open, b.close)
    return (a.open + b.open - match, a.close + b.close - match)
```

### Python 实现

```python
def is_balanced(s):
    st = []
    for c in s:
        if c == '(':
            st.append(c)
        elif c == ')' and st and st[-1] == '(':
            st.pop()
        else:
            st.append(c)
    return len(st) == 0

def count_catalan(n):
    # 长度为 2n 的合法括号序列个数 = 卡特兰数 C_n
    c = 1
    for k in range(n):
        c = c * (2 * n - k) // (k + 1)
    return c // (n + 1)

def next_balanced(s):
    """字典序后继；不存在返回 None（s 已是最后一个）"""
    s = list(s)
    n = len(s)
    depth = 0
    for i in range(n - 1, -1, -1):
        if s[i] == '(':
            depth -= 1
        else:
            depth += 1
        if s[i] == '(' and depth > 0:
            depth -= 1
            open_cnt = (n - i - 1 - depth) // 2
            close_cnt = n - i - 1 - open_cnt
            nxt = ''.join(s[:i]) + ')' + '(' * open_cnt + ')' * close_cnt
            return None if nxt == ''.join(s) else nxt
    return None

class BracketSeg:
    """线段树维护括号序列区间：查询区间内匹配括号对数"""
    def __init__(self, s):
        self.n = len(s)
        self.t = [(0, 0)] * (4 * self.n + 5)
        self._build(s, 1, 0, self.n - 1)

    def _build(self, s, p, l, r):
        if l == r:
            self.t[p] = (1, 0) if s[l] == '(' else (0, 1)
            return
        m = (l + r) // 2
        self._build(s, p * 2, l, m)
        self._build(s, p * 2 + 1, m + 1, r)
        self.t[p] = self._merge(self.t[p * 2], self.t[p * 2 + 1])

    def _merge(self, a, b):
        m = min(a[0], b[1])
        return (a[0] + b[0] - m, a[1] + b[1] - m)

    def query(self, ql, qr, p=1, l=0, r=None):
        if r is None:
            r = self.n - 1
        if ql <= l and r <= qr:
            return self.t[p]
        m = (l + r) // 2
        acc = (0, 0)
        if ql <= m:
            acc = self._merge(acc, self.query(ql, qr, p * 2, l, m))
        if qr > m:
            acc = self._merge(acc, self.query(ql, qr, p * 2 + 1, m + 1, r))
        return acc

if __name__ == '__main__':
    assert is_balanced('(())()') is True
    assert is_balanced(')()') is False
    assert is_balanced('') is True
    print('is_balanced OK')
    assert count_catalan(3) == 5  # C3 = 5
    assert count_catalan(4) == 14
    print('catalan OK')
    # 长度 6 的合法括号序列字典序：((())) < (()()) < (())() < ()(()) < ()()()
    assert next_balanced('((()))') == '(()())'
    assert next_balanced('(()())') == '(())()'
    assert next_balanced('(())()') == '()(())'
    assert next_balanced('()(())') == '()()()'
    assert next_balanced('()()()') is None
    print('next_balanced OK')
    seg = BracketSeg('(()())')
    op, cl = seg.query(0, 5)   # 全串合法
    assert op == 0 and cl == 0
    seg2 = BracketSeg('(())(()')
    op, cl = seg2.query(0, 6)
    assert (op, cl) == (1, 0)
    matched = (7 - op - cl) // 2
    assert matched == 3
    assert seg2.query(0, 3) == (0, 0)
    print('bracket seg OK (open=%d close=%d matched=%d)' % (op, cl, matched))
```

**PyPy 提示**: 线段树递归在 PyPy 下可跑 1e5 数据；若区间修改频繁（翻转括号），需加懒标记并维护 open/close 互换。next_balanced 的字符串拼接用 list 操作避免重复生成。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 判定 O(n)；计数 O(n)；字典序后继 O(n)；线段树单次查询/修改 O(log n) |
| 空间 | 线段树 O(n)；其余 O(1)/O(n) |

### 局限

变种括号（多类型）的线段树维护需处理不匹配类型的非法情况，合并逻辑复杂；区间翻转（括号取反）只对单类型括号合法（'(' 与 ')' 互换），多类型需换用更复杂维护。字典序排名用 O(n²) DP，n 大时需优化。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Codeforces | 380C. Sereja and Brackets | 4 | 线段树维护区间匹配括号对数，CF 经典区间数据结构题 | [https://codeforces.com/problemset/problem/380/C](https://codeforces.com/problemset/problem/380/C) |
| Luogu | P5658 | 5 | [CSP-S 2019] 括号树：树上括号匹配计数，把栈思想搬到树上 | [https://www.luogu.com.cn/problem/P5658](https://www.luogu.com.cn/problem/P5658) |
| Luogu | P3205 | 3 | [HNOI2010] 合唱队：区间 DP，可与括号匹配思维结合训练 | [https://www.luogu.com.cn/problem/P3205](https://www.luogu.com.cn/problem/P3205) |

## Pitfalls · 易错点

- 判定时把 ')' 压栈是常见错误——非匹配 ')' 压栈后栈永远不清空，需按『弹/压』规则严格区分
- 卡特兰数取模时要用模逆元或组合数递推，直接整除会错（n 大时）
- 线段树合并顺序不可交换（括号合并非交换），查询时左右顺序必须保持
- 区间翻转 '(' 与 ')' 后 open/close 需互换，漏换则结果全错
- 字典序后继中 depth 的符号约定（从右往左扫时 '(' 减 1、')' 加 1）容易写反

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/topic/bracket.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/topic/bracket.md)
- CP-Algorithms ✓ [https://cp-algorithms.com/combinatorics/bracket_sequences.html](https://cp-algorithms.com/combinatorics/bracket_sequences.html)
