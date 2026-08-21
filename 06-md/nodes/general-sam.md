---
id: general-sam
name: 广义后缀自动机(GSAM)
group: G-C-4
stage: frontier
priority: P2
depth_tier: standard
---

# 广义后缀自动机(GSAM)

> 多字符串的 SAM：先在多串上建 Trie，再 BFS 逐节点在 Trie 上做 SAM 增量插入，支持多串不同子串计数、多串最长公共子串等

<!-- 元信息: id=general-sam · group=G-C-4 · stage=frontier · priority=P2 · depth_tier=standard -->

## What · 是什么

广义后缀自动机（General Suffix Automaton, GSAM）把后缀自动机推广到字典树（多字符串）上：先将所有字符串插入一棵 Trie，再对 Trie 做 BFS，按 len 不递减顺序把每个 Trie 节点作为'插入点'执行修改版的 SAM 增量插入（区别：cur 不是新建而是复用 Trie 节点 next[last][c]，且 clone 复制转移时跳过 len 为 0 的目标）。这样构造的状态数 O(总长)，与普通 SAM 性质兼容。常见'伪广义 SAM'：①用特殊分隔符拼接多串建 SAM；②对每个串重置 last=0 依次插入同一个 SAM。方法②在特定题意下正确但复杂度危险（多次重复串会退化）。GSAM 应用：所有串不同子串总数（Σ len[v]−len[link[v]]，模板 P6139）、多串最长公共子串（LCS2：对每个 SAM 状态记录被哪些串覆盖，按 len 降序沿 link 合并标记）。

## Why · 为什么

### 直觉 · Intuition

直接对每个串重置 last 插同一个 SAM：如果串之间有相同前缀，last 跳转会让部分路径被重复'扩展'，可能产生多余的状态与高复杂度。正确做法是把所有串的前缀结构先并成 Trie——每个 Trie 节点天然对应'从根到它的字符串'，BFS 保证父节点先于子节点处理，这样每个节点只被插入一次，复杂度线性。

### 原理 · Principle

在 Trie 上，节点 u 的'字符串'就是根到 u 的路径。对 Trie 做 BFS 得到 len 不递减序列（len=深度），按该顺序对每个节点 u（对应字符 c，父为 p）执行：cur=Trie节点 u（已在 next[p][c] 中），len[cur]=len[p]+1；从 link[p] 上溯补 c 转移（若 p 处已有则停）；找到 q 后若 len[q]==len[p]+1 则 link[cur]=q，否则 clone。clone 复制 q 的转移时必须只复制 len 非 0 的目标（避免把尚未插入的 Trie 分支复制进去）。BFS 时注意后续用 SAM 的 next 数组扩展队列（Trie 结构在 SAM 化后不再独立保留）。性质：状态数 ≤ 所有串总长×2 左右；不同子串总数 Σ(len[v]−len[link[v]])。多串 LCS：每个串在 Trie 上打标记（经过的节点），BFS 插入时把标记并入对应 SAM 状态，按 len 降序沿 link 合并，找被所有串标记的 len 最大值。

### 历史 · History

广义后缀自动机由刘研绎在 2015 年国家队论文《后缀自动机在字典树上的拓展》中提出，将 SAM 构造直接建立在字典树上。OI Wiki 有专门章节（general-sam），并指出'分隔符拼接'与'last 重置'两种伪写法在特定题目下可用但最坏复杂度不好。Luogu P6139 是其模板题。

## How · 实现

### 伪代码

```python
# 建 Trie（与 SAM 共用 next 数组）
for s in strings:
    cur = 0
    for ch in s:
        if next[cur][ch]==0: next[cur][ch]=新建节点
        cur = next[cur][ch]

# BFS 逐节点做 SAM 插入
insertSAM(last, c):
    cur = next[last][c]                 # 复用 Trie 节点
    len[cur] = len[last]+1
    p = link[last]
    while p!=-1:
        if next[p][c]==0: next[p][c]=cur
        else: break
        p = link[p]
    if p==-1: link[cur]=0; return
    q = next[p][c]
    if len[q]==len[p]+1: link[cur]=q; return
    clone = 新节点(len[p]+1, link[q])
    for 每个字符 t: if len[next[q][t]]!=0: next[clone][t]=next[q][t]
    while p!=-1 and next[p][c]==q: next[p][c]=clone; p=link[p]
    link[clone]=link[q]; link[cur]=link[q]=clone

BFS 队列初始放根的所有儿子(c,0)，处理后把 SAM 上新增的子节点继续入队
```

### Python 实现

```python
# -*- coding: utf-8 -*-
# 广义后缀自动机：Trie 上 BFS 构建，求所有串不同子串总数
from collections import deque


def build_gsa(strings, sigma=26):
    """返回 (next, link, len)。注意 Trie 与 SAM 共用 next 数组。"""
    nxt = [[0] * sigma]
    link = [-1]
    length = [0]

    def add_state(l, lk):
        nxt.append([0] * sigma)
        link.append(lk)
        length.append(l)
        return len(length) - 1

    # 1. 建 Trie
    for s in strings:
        cur = 0
        for ch in s:
            c = ord(ch) - 97
            if nxt[cur][c] == 0:
                nxt[cur][c] = add_state(0, -1)   # len 暂记 0，BFS 时填入
            cur = nxt[cur][c]

    # 2. BFS 逐节点 SAM 插入
    def insertSAM(last, c):
        cur = nxt[last][c]
        length[cur] = length[last] + 1
        p = link[last]
        while p != -1:
            if not nxt[p][c]:
                nxt[p][c] = cur
            else:
                break
            p = link[p]
        if p == -1:
            link[cur] = 0
            return cur
        q = nxt[p][c]
        if length[p] + 1 == length[q]:
            link[cur] = q
            return cur
        clone = add_state(length[p] + 1, link[q])
        for i in range(sigma):
            nq = nxt[q][i]
            if nq and nq < len(length) and length[nq] != 0:
                nxt[clone][i] = nq
        while p != -1 and nxt[p][c] == q:
            nxt[p][c] = clone
            p = link[p]
        link[clone] = link[q]
        link[cur] = clone
        link[q] = clone
        return cur

    q = deque()
    for c in range(sigma):
        if nxt[0][c]:
            q.append((nxt[0][c], 0, c))
    while q:
        node, parent, c = q.popleft()
        last = insertSAM(parent, c)
        for nc in range(sigma):
            if nxt[last][nc]:
                child = nxt[last][nc]
                if child < len(length) and length[child] == 0:
                    q.append((child, last, nc))
    return nxt, link, length


def count_distinct_all(strings, sigma=26):
    """所有字符串的不同子串总数。"""
    nxt, link, length = build_gsa(strings, sigma)
    return sum(length[i] - length[link[i]] for i in range(1, len(length)))


if __name__ == '__main__':
    def brute(strings):
        s = set()
        for t in strings:
            for i in range(len(t)):
                for j in range(i + 1, len(t) + 1):
                    s.add(t[i:j])
        return len(s)

    tests = [('ab', 'ba'), ('abc', 'bcd'), ('aa', 'aaa'), ('abc', 'def'),
             ('abab', 'baba'), ('hello', 'world'), ('abcabc', 'bca')]
    for t in tests:
        assert count_distinct_all(t) == brute(t), t
    import random
    random.seed(0)
    for _ in range(100):
        k = random.randint(1, 4)
        ss = []
        for _ in range(k):
            n = random.randint(1, 10)
            ss.append(''.join(random.choice('abc') for _ in range(n)))
        assert count_distinct_all(ss) == brute(ss), ss
    print('general-sam tests passed')

```

**PyPy 提示**: next 用 26 数组 + Trie 与 SAM 共享，n≤1e5 总长在 PyPy 可跑；字符集再大用 dict 并注意 clone 复制的 len 过滤条件。多串 LCS 的标记数组按 len 降序合并，可用基数排序。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 建 Trie O(总长)；BFS 构建 O(总长·\|Σ\|)（数组）或 O(总长)；不同子串计数 O(状态数)；多串 LCS O(状态数·k) |
| 空间 | O(总长·\|Σ\|) 或 O(总长)（dict） |

### 局限

伪广义写法（分隔符拼接/重置 last）在最坏情况（大量重复前缀串）复杂度退化，应优先用 Trie+BFS 正规写法。Trie 结构在 SAM 化后会被破坏（next 数组改指向），若还需 Trie 需双倍空间。多串 LCS 需额外标记与按 len 拓扑合并。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P6139 | 4 | 【模板】广义后缀自动机：多串不同子串计数模板 | [https://www.luogu.com.cn/problem/P6139](https://www.luogu.com.cn/problem/P6139) |
| SPOJ | LCS2 | 4 | Longest Common Substring II：多串最长公共子串，标记 + link 树合并 | [https://www.spoj.com/problems/LCS2/](https://www.spoj.com/problems/LCS2/) |

## Pitfalls · 易错点

- clone 复制转移时只复制 len 非 0 的目标，否则会把未插入的 Trie 节点错误复制
- BFS 队列要用 SAM 的 next（SAM 化后）扩展，且判重（length[child]==0）
- Trie 节点的 len 初始为 0，插入时才赋值；不能复用普通 SAM 的建点逻辑
- 不同子串数公式中 len[link[i]] 对 link=-1 的根要跳过
- 多串 LCS 的串标记要在 Trie 插入阶段打好，SAM 化后按 len 降序沿 link 合并
- 避免伪广义写法的最坏退化；必要时双倍空间保 Trie

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/string/general-sam/](https://oi-wiki.org/string/general-sam/)
- 书籍 ✓ `刘研绎 2015 国家集训队论文《后缀自动机在字典树上的拓展》`
