---
id: suffix-automaton
name: 后缀自动机(SAM)
group: G-C-4
stage: advanced
priority: P2
depth_tier: standard
---

# 后缀自动机(SAM)

> 识别字符串所有子串的最小 DFA，O(n) 在线构造，endpos 等价类 + 后缀链接树，解决不同子串计数/出现次数/最长公共子串等一揽子问题

<!-- 元信息: id=suffix-automaton · group=G-C-4 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

后缀自动机（Suffix Automaton, SAM）是识别给定字符串 s 所有后缀的最小 DFA，等价地包含 s 全部子串的压缩信息：从初始状态 t0 出发的任意路径的标号都是 s 的一个子串，反之每个子串对应一条路径。状态是子串按 endpos 集合（出现结束位置集合）划分的等价类，后缀链接 link(v) 指向 endpos 更大的最长后缀等价类，形成后缀链接树（=endpos 集合的包含树）。性质：状态数 ≤2n−1，转移数 ≤3n−4，构造 O(n)（字符集常数量级；字符集大时 O(n log|Σ|)）。在线增量构造：每加一个字符创建 cur（len[last]+1），沿后缀链接补充转移；遇到已有转移 p→c 时，若 len[p]+1==len[q] 直接连 link，否则复制 clone。应用：不同子串数=Σ(len[v]−len[link[v]])；子串出现次数=沿 link 树从前缀状态向上累计；最小循环移位；两串最长公共子串；字典序第 k 小子串；第一次/所有出现位置。

## Why · 为什么

### 直觉 · Intuition

把所有子串按'出现在哪些位置'分组（endpos 等价类）：同组子串的结束位置完全相同，它们的出现行为一致，可以共用一个自动机状态。endpos 相同的子串必然是'长串的后缀'关系，长度连续。把每个等价类作为一个状态、类中较短者通过后缀链接连接到较长类，就得到一棵'后缀链接树'，整棵树的每个叶到根路径恰好枚举了某个前缀的所有后缀。增量构造就是在每加一个字符时，为新的前缀补齐'后缀路径'并压缩合并。

### 原理 · Principle

endpos 性质：两子串 u⊂w 若 endpos 相同，则 u 以 w 的后缀出现且仅以该形式出现（引理1）；endpos 集合要么互斥要么包含（引理2），故构成树；同等价类子串长度连续且互为后缀（引理3）。link(v) 指向 longest(v) 的 endpos 不同且最长的那条后缀。增量构造正确性：加字符 c 时，新状态 cur 代表新前缀；从 last 沿 link 上溯，为所有尚未有 c 转移的状态补上 →cur；遇到的第一个已有转移 p→c 记 q：若连续（len[q]==len[p]+1）则 link[cur]=q；否则复制 clone（len=len[p]+1，继承 q 的转移与 link），把 link[cur] 与 link[q] 改为 clone，并把所有仍指向 q 的 c 转移改指 clone。复杂度：每个状态至多创建一次 clone，重定向边均摊 O(n)。状态数上界 2n−1（每次迭代至多加 1 新状态 +1 clone），转移数上界 3n−4。出现次数：每个前缀状态初始 1，按 len 降序沿 link 累加到父节点，sz[v] 即该等价类子串出现次数。

### 历史 · History

后缀自动机由 Blumer 等人于 1984-1985 年在'DAWG（有向无环子串图）'工作中建立，是接受全部后缀的最小 DFA。它在算法竞赛中作为'字符串神器'被广泛使用（OI Wiki、CP-Algorithms 均有完整章节），CP-Algorithms 列出了 13+ 类应用（出现次数、不同子串数、第 k 小子串、最小循环移位、最长公共子串等）。与后缀树/后缀数组可互相转化。

## How · 实现

### 伪代码

```python
# 增量构造
t0: len=0, link=-1; last=t0
sam_extend(c):
    cur = 新状态(len[last]+1)
    p = last
    while p!=-1 and p 无 c 转移:
        p 加 c->cur; p = link[p]
    if p==-1:
        link[cur] = 0
    else:
        q = p 的 c 转移
        if len[p]+1 == len[q]: link[cur]=q
        else:
            clone = 复制 q(len=len[p]+1, 转移, link)
            while p!=-1 and p 的 c 转移 == q:
                p 的 c 转移 = clone; p = link[p]
            link[q] = link[cur] = clone
    last = cur

# 不同子串数 = sum(len[v]-len[link[v]])
# 出现次数: 前缀状态 sz=1, 按 len 降序沿 link 累加
```

### Python 实现

```python
# -*- coding: utf-8 -*-
# 后缀自动机完整实现（O(n)），含常见应用

class SAM:
    """用 dict 存转移；字符集为常数时可换数组。"""
    def __init__(self):
        self.next = []      # 转移
        self.link = []      # 后缀链接
        self.len = []       # 状态最长串长度
        self.last = 0
        self._new(0, -1)

    def _new(self, l, lk):
        self.next.append({})
        self.link.append(lk)
        self.len.append(l)
        return len(self.len) - 1

    def extend(self, c):
        cur = self._new(self.len[self.last] + 1, -1)
        p = self.last
        while p != -1 and c not in self.next[p]:
            self.next[p][c] = cur
            p = self.link[p]
        if p == -1:
            self.link[cur] = 0
        else:
            q = self.next[p][c]
            if self.len[p] + 1 == self.len[q]:
                self.link[cur] = q
            else:
                clone = self._new(self.len[p] + 1, self.link[q])
                self.next[clone] = self.next[q].copy()
                while p != -1 and self.next[p].get(c) == q:
                    self.next[p][c] = clone
                    p = self.link[p]
                self.link[q] = self.link[cur] = clone
        self.last = cur


def build_sam(s):
    sam = SAM()
    for ch in s:
        sam.extend(ch)
    return sam


def count_distinct_substrings(s):
    """不同子串数 = Σ(len[v]-len[link[v]])。"""
    sam = build_sam(s)
    return sum(sam.len[i] - sam.len[sam.link[i]] for i in range(1, len(sam.len)))


def max_occurrence(s):
    """s 中任意子串的最大出现次数。"""
    sam = build_sam(s)
    n = len(sam.len)
    sz = [0] * n
    last = 0
    for ch in s:                       # 前缀状态各计 1
        last = sam.next[last][ch]
        sz[last] += 1
    order = sorted(range(1, n), key=lambda i: sam.len[i], reverse=True)
    for v in order:                    # 沿 link 树向上累计
        if sam.link[v] >= 0:
            sz[sam.link[v]] += sz[v]
    return max(sz[1:])                 # 排除根（根非子串）


def longest_common_substring(a, b):
    """两串最长公共子串长度（SAM on a，扫描 b）。"""
    sam = build_sam(a)
    v, l, best = 0, 0, 0
    for ch in b:
        while v != -1 and ch not in sam.next[v]:
            v = sam.link[v]
            if v != -1:
                l = sam.len[v]
        if v == -1:
            v, l = 0, 0
        else:
            v = sam.next[v][ch]
            l += 1
            best = max(best, l)
    return best


if __name__ == '__main__':
    assert count_distinct_substrings('abc') == 6
    assert count_distinct_substrings('aaaa') == 4
    assert count_distinct_substrings('ababa') == 9
    assert max_occurrence('ababa') == 3        # 'a' 出现 3 次
    assert max_occurrence('aaaa') == 4
    assert longest_common_substring('abcde', 'cdefg') == 3   # 'cde'
    assert longest_common_substring('abcdef', 'xyz') == 0
    assert longest_common_substring('abcabc', 'bca') == 3    # 'bca'
    # 随机对拍
    import random
    random.seed(0)
    for _ in range(100):
        n = random.randint(1, 12)
        s = ''.join(random.choice('abc') for _ in range(n))
        brute = len({s[i:j] for i in range(n) for j in range(i + 1, n + 1)})
        assert count_distinct_substrings(s) == brute, s
        occ = {s[i:j] for i in range(n) for j in range(i + 1, n + 1)}
        mo = max(sum(1 for i in range(n - len(t) + 1) if s[i:i + len(t)] == t) for t in occ)
        assert max_occurrence(s) == mo, (s, max_occurrence(s), mo)
        # LCS 对拍
        m = random.randint(1, 12)
        t = ''.join(random.choice('abc') for _ in range(m))
        bl = max((len(x) for i in range(len(s)) for j in range(i + 1, len(s) + 1)
                  for x in [s[i:j]] if x in t), default=0)
        assert longest_common_substring(s, t) == bl, (s, t, longest_common_substring(s, t), bl)
    print('suffix-automaton tests passed')

```

**PyPy 提示**: dict 转移在 PyPy 下 O(n log\|Σ\|) 可跑 1e6 规模偏慢；字符集小（如 26）用数组 next[2n][26] 换 O(n)。出现次数排序用基数排序（按 len 计数）避免 O(n log n)。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 构造 O(n)（字符集常数）或 O(n log\|Σ\|)；不同子串数 O(n)；出现次数 O(n)；LCS O(n+m) |
| 空间 | O(n·\|Σ\|)（数组）或 O(n) 转移总数（dict） |

### 局限

endpos 集合本身（具体位置集合）不直接存储，需处理；大字符集 dict 慢。构造细节（clone 复制转移与 link）易错。最小循环移位也可用 Lyndon/双指针（见 minimal-string），SAM 法是另一种路线。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3804 | 3 | 【模板】后缀自动机：不同子串数 / 出现次数统计模板 | [https://www.luogu.com.cn/problem/P3804](https://www.luogu.com.cn/problem/P3804) |
| Luogu | P3975 | 4 | 弦论：SAM 上求字典序第 k 小子串（需区分不同位置子串） | [https://www.luogu.com.cn/problem/P3975](https://www.luogu.com.cn/problem/P3975) |
| SPOJ | LCS | 3 | Longest Common Substring：两串 LCS 的 SAM 模板 | [https://www.spoj.com/problems/LCS/](https://www.spoj.com/problems/LCS/) |
| SPOJ | SUBST1 | 3 | New Distinct Substrings：不同子串计数（SAM 或 SA） | [https://www.spoj.com/problems/SUBST1/](https://www.spoj.com/problems/SUBST1/) |

## Pitfalls · 易错点

- link[0]=-1；从 last 上溯补转移时 p=-1 必须终止并连 link[cur]=0
- clone 必须复制 q 的全部转移（字典 copy）与 link，len 重新设置
- 重定向转移时条件是 next[p][c]==q，漏掉条件会把无关转移改坏
- 出现次数统计要按 len 降序（拓扑序），且根不计入 max
- 不同子串数公式对每个非根状态求和；含空串时注意边界
- 最小性：SAM 状态可被 Myhill-Nerode 证明为最少，但实现不一定显式终止状态

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/string/sam/](https://oi-wiki.org/string/sam/)
- CP-Algorithms ✓ [https://cp-algorithms.com/string/suffix-automaton.html](https://cp-algorithms.com/string/suffix-automaton.html)
