---
id: palindrome-automaton
name: 回文自动机 / 回文树（PAM，Palindromic Automaton）
group: G-C-5
stage: advanced
priority: P2
depth_tier: standard
---

# 回文自动机 / 回文树（PAM，Palindromic Automaton）

> 存储串中所有本质不同回文子串的最小 DFA（O(n) 个状态），增量 O(n) 构造；转移边表示在回文串两端加同一字符，fail 指向最长回文后缀，支持统计出现次数、最小回文划分等。

<!-- 元信息: id=palindrome-automaton · group=G-C-5 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

回文自动机（EER Tree / Palindromic Tree / PAM）是一棵『树 + fail 指针』结构，存储给定串的所有本质不同回文子串：每个节点代表一个回文子串，转移边 ch[c] 表示『在该回文串两端各加字符 c』得到的新回文串，fail 指针指向该回文串的最长回文后缀。有两个初始节点：奇根（长度 -1）与偶根（长度 0）。在线增量构造，加入每个字符时沿 fail 跳转找『两端可加该字符』的最长回文后缀，必要时新建节点并求其 fail。由于每加一个字符本质不同回文子串最多增 1，总状态数 O(n)，构造 O(n)。经典应用：本质不同回文子串个数、各回文子串出现次数（拓扑逆序累计）、最小回文划分（配合 dp 与等差数列优化）。

## Why · 为什么

### 直觉 · Intuition

Manacher 只能得到半径数组，无法回答『每个回文子串出现次数』这类统计问题。PAM 的洞察：回文子串是『对称增长的』——想扩展一个回文，只能在两端同时加字符。于是回文子串之间的转移天然形成树结构（两端加字符），而『最长回文后缀』给出 fail 链。奇根长度 -1 的巧妙设计使单字符也能作为合法的扩展，处理了奇偶两种回文。

### 原理 · Principle

① 结构：节点 = 本质不同回文子串；节点带 len；ch 转移在两端加字符；fail 指向最长回文后缀。② 构造：添加字符 c 于位置 p（下标从 0 起，s 前加哨兵），从上一字符结尾的最长回文后缀节点 last 沿 fail 跳，找到满足 s[p-len-1]==s[p] 的节点 cur，则 cur 扩展 c 后得到新回文节点；若 ch[cur][c] 不存在则新建 node（len=len[cur]+2），并沿 cur 的 fail 继续找其最长回文后缀的扩展作为新节点 fail。③ 线性性：状态 O(n)；每字符 fail 跳转均摊 O(1)（深度增 1 与跳转递减平衡）。④ 出现次数：节点创建顺序即拓扑序，逆序把 cnt[node] 累加到 cnt[fail[node]] 即可得每个回文子串出现次数。⑤ 最小回文划分：dp[i]=1+min{dp[j]}（s[j+1..i] 回文），用 fail 树的等差数列（slink）优化至 O(n log n)。

### 历史 · History

回文树由 Mikhail Rubinchik 与 Arseny M. Shur 于 2015 年在论文《EERTREE: An Efficient Data Structure for Processing Palindromes in Strings》中提出；此前类似思想以 Palindromic Tree 之名在社区流传（adilet.org 博客等）。2017 年 IOI 国家候选队论文（翁文涛《回文树及其应用》）将其引入国内 OI，随后普及。APIO2014 回文串是其经典应用。

## How · 实现

### 伪代码

```python
struct PAM:
    ch[MAXN][26], fail[MAXN], len[MAXN], cnt[MAXN], s[MAXN]
    last = 0; node 计数 = 1  (0=偶根 len0, 1=奇根 len-1)
    fail[0] = 1, fail[1] = 1

    get_fail(x, p):   # 沿 fail 找两端可加 s[p] 的节点
        while p - len[x] - 1 < 0 or s[p] != s[p - len[x] - 1]:
            x = fail[x]
        return x

    add(p, c):
        s[p] = c
        cur = get_fail(last, p)
        if not ch[cur][c]:
            new = 新建节点; len[new] = len[cur] + 2
            fail[new] = ch[get_fail(fail[cur], p)][c]
            if fail[new] == new: fail[new] = 0
            ch[cur][c] = new
        last = ch[cur][c]
        cnt[last] += 1

    build(): for i in 0..n-1: add(i, s[i])
    出现次数: for i 逆序: cnt[fail[i]] += cnt[i]
```

### Python 实现

```python
class PAM:
    def __init__(self, n):
        self.maxn = n + 3
        self.ch = [[0] * 26 for _ in range(self.maxn)]
        self.fail = [0] * self.maxn
        self.len = [0] * self.maxn
        self.cnt = [0] * self.maxn
        self.s = [''] * self.maxn
        self.cur_node = 2  # 0=偶根, 1=奇根, 新节点从 2 起
        self.last = 0
        self.sz = 0  # 已处理字符数
        self.len[0] = 0
        self.len[1] = -1
        self.fail[0] = 1
        self.fail[1] = 1

    def get_fail(self, x, p):
        while True:
            curlen = self.len[x]
            if p - curlen - 1 >= 0 and self.s[p] == self.s[p - curlen - 1]:
                return x
            x = self.fail[x]

    def add(self, c):
        p = self.sz
        self.s[p] = c
        self.sz += 1
        code = ord(c) - ord('a')
        cur = self.get_fail(self.last, p)
        if self.ch[cur][code] == 0:
            nxt = self.cur_node
            self.cur_node += 1
            self.len[nxt] = self.len[cur] + 2
            f = self.get_fail(self.fail[cur], p)
            self.fail[nxt] = self.ch[f][code]
            if self.fail[nxt] == nxt:
                self.fail[nxt] = 0
            self.ch[cur][code] = nxt
        self.last = self.ch[cur][code]
        self.cnt[self.last] += 1

    def build(self, s):
        for c in s:
            self.add(c)

    def distinct_palindromes(self):
        return self.cur_node - 2

    def occurrence(self):
        """返回各节点代表的回文子串出现次数（按节点编号）"""
        for i in range(self.cur_node - 1, 1, -1):
            self.cnt[self.fail[i]] += self.cnt[i]
        return self.cnt[:self.cur_node]

if __name__ == '__main__':
    s = 'abacababbab'
    pam = PAM(len(s))
    pam.build(s)
    print('distinct palindromes =', pam.distinct_palindromes())
    occ = pam.occurrence()
    # 验证：手工枚举本质不同回文子串个数
    pal = set()
    n = len(s)
    for i in range(n):
        for j in range(i, n):
            sub = s[i:j + 1]
            if sub == sub[::-1]:
                pal.add(sub)
    assert pam.distinct_palindromes() == len(pal), (pam.distinct_palindromes(), len(pal))
    print('distinct count matches brute force:', len(pal))
    # 出现次数抽样验证：枚举所有回文子串，逐串在 PAM 中匹配并核对次数
    from collections import Counter
    brute = Counter()
    for i in range(n):
        for j in range(i, n):
            sub = s[i:j + 1]
            if sub == sub[::-1]:
                brute[sub] += 1
    # 通过两端扩展在 PAM 上定位节点（fail 链寻址）
    def node_of(pal):
        if pal == '':
            return 0
        if len(pal) == 1:
            return pam.ch[1][ord(pal) - ord('a')]
        inner = pal[1:-1]
        nid = node_of(inner)
        return pam.ch[nid][ord(pal[0]) - ord('a')]
    checked = 0
    for pal_s, c in brute.items():
        occ_id = node_of(pal_s)
        assert occ[occ_id] == c, (pal_s, occ[occ_id], c)
        checked += 1
    assert checked == len(brute) == len(pal)
    print('occurrence counts verified for %d distinct palindromes' % checked)
    print('OK')
```

**PyPy 提示**: ch 用 list-of-list 在 PyPy 下内存与访问开销可接受（n≤1e5）；若内存紧张可改 dict 转移或滚动数组。get_fail 是热点，用 while True 且缓存 len/fail 局部变量。cnt 的逆序累加用纯 for 循环。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 构造 O(n)（每字符均摊 O(1)）；出现次数统计 O(n)；最小回文划分朴素 O(n²)，slink 优化 O(n log n) |
| 空间 | O(n·Σ)（ch 表）或 O(n)（dict 转移） |

### 局限

只能处理固定字符集（本实现 26 字母，需扩展或 dict）；本质不同回文子串上限 O(n) 保证状态数，但含大量重复字符时转移表可能稀疏；最小回文划分的 slink 优化（引理：回文串后缀为 border 当且仅当其回文）较难理解，需先掌握 border/周期概念。Python 实现 n≤1e6 时 get_fail 递归链长可能退化，需保证 fail 树深度可控。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3649 | 5 | [APIO2014] 回文串：最大『出现次数×长度』，PAM 构造后逆序累加 cnt 即得 | [https://www.luogu.com.cn/problem/P3649](https://www.luogu.com.cn/problem/P3649) |
| Luogu | P4555 | 6 | [国家集训队] 最长双回文串：PAM 或 Manacher 预处理左右最长回文，PAM 亦可 | [https://www.luogu.com.cn/problem/P4555](https://www.luogu.com.cn/problem/P4555) |
| Luogu | P1659 | 4 | [国家集训队] 拉拉队排练：前 k 大奇数长度回文子串长度之积，PAM+计数 | [https://www.luogu.com.cn/problem/P1659](https://www.luogu.com.cn/problem/P1659) |
| Luogu | P4287 | 5 | [SHOI2011] 双倍回文：一半长度也是回文的回文串计数，PAM 结构+倍增/哈希 | [https://www.luogu.com.cn/problem/P4287](https://www.luogu.com.cn/problem/P4287) |
| Codeforces | 932G Palindrome Partition | 8 | 最小/计数回文划分的 slink 等差数列优化，PAM 高级应用 | [https://codeforces.com/problemset/problem/932/G](https://codeforces.com/problemset/problem/932/G) |

## Pitfalls · 易错点

- 奇根 len=-1 的意义与 fail 初值（fail[0]=fail[1]=1）缺一不可，否则单字符失配处理错误
- 新建节点 fail 的求取必须从 fail[cur] 出发而非 cur，否则得到自身或错链
- get_fail 的边界条件 p-len[x]-1<0 必须先判，防止负下标访问哨兵前
- cnt 只在 add 时 +1，出现次数必须在全部添加完后逆序累加到 fail
- ch 表大小 = n+3（含奇偶根），开小会越界；多组数据需重置 0/1 根
- 最小回文划分的 dp 方向与 slink 前缀和 g 数组需与节点顺序一致

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/string/pam.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/string/pam.md)
- OI Wiki ✓ [https://oi-wiki.org/string/pam/](https://oi-wiki.org/string/pam/)
