---
id: ac-automaton
name: AC 自动机
group: G-C-2
stage: advanced
priority: P1
depth_tier: standard
---

# AC 自动机

> Trie + KMP 失配指针，多模式串匹配自动机，预处理 O(Σ\|s\|)，匹配 O(文本长+z)

<!-- 元信息: id=ac-automaton · group=G-C-2 · stage=advanced · priority=P1 · depth_tier=standard -->

## What · 是什么

AC（Aho–Corasick）自动机以 Trie 结构为基础、结合 KMP 失配指针思想，解决『一次匹配多个模式串』问题。构建分两步：① 把所有模式串插入 Trie；② BFS 构建 fail 指针——fail[u] 指向 u 的最长真后缀状态（即字典树中存在的最长后缀字符串所对应的节点）。常配合『Trie 图』优化：把不存在的转移补全为 fail 的转移，使匹配过程每字符 O(1) 无需回溯。匹配：文本串沿 Trie 图走，每到一个节点沿 fail 链累加所有匹配模式。优化：fail 树拓扑/DFS 求和可在 O(len) 统计每个模式出现次数。时间复杂度：建 O(Σ|s_i|+n·字符集)，匹配 O(|S|+z)（z 为匹配总数）。

## Why · 为什么

### 直觉 · Intuition

单模式匹配用 KMP，多模式若每个都跑一遍 KMP 太慢。AC 自动机把多个模式塞进一棵 Trie，然后给每个节点配一根‘失败了去哪接’的弹簧（fail 指针）——匹配到某节点失败时，弹簧直接跳到所有模式前缀中与之最长后缀相同的节点，一次到位，不必从头再来。就像查字典时发现整页没有，直接翻到能接上的那一页。

### 原理 · Principle

fail[u] 定义：u 代表的字符串的最长真后缀，且该后缀是某个模式串的前缀。构建（BFS 按深度）：设 u 由父 p 经字符 c 到达，则 fail[u]=δ(fail[p],c)（若不存在则递归 fail 链直到根，最终为根或补全转移直接取到）。Trie 图补全：对不存在的 δ(u,c) 令其=δ(fail[u],c)，这样一次转移即到达‘最合理继续点’。匹配每字符 u=δ(u,c)，随后沿 fail 链收集匹配（或用 fail 树差分：只给命中节点打标记，最后按 fail 树自底向上求和）。正确性：每个状态代表文本当前后缀与某个模式前缀的最大匹配；fail 链上的所有状态都代表可匹配模式。

### 历史 · History

1975 年 Alfred Aho 与 Margaret Corasick 提出该算法（论文 “Efficient string matching: an aid to bibliographic search”），源于贝尔实验室的检索需求。它把 KMP 从单模式推广到多模式，复杂度线性。现代文本索引、病毒库扫描（如 ClamAV）、正则引擎 NFA 化均有其思想。CP-Algorithms 与 OI Wiki《AC 自动机》页给出完整实现，含拓扑优化与 AC 自动机 DP（如 HNOI2004 L 语言）。

## How · 实现

### 伪代码

```python
# 节点: tr[u][26] 转移(Trie图), fail[u], cnt[u]
def build():
  q = deque(根的所有直接儿子)   # 根儿子 fail=0
  while q:
    u = q.popleft()
    for c in range(26):
      v = tr[u][c]
      if v:
        fail[v] = tr[fail[u]][c]
        q.append(v)
      else:
        tr[u][c] = tr[fail[u]][c]   # 补全 Trie图
def query(text):
  u = 0; res = 0
  for ch in text:
    u = tr[u][ch]
    v = u
    while v and cnt[v]: res += cnt[v]; cnt[v]=0; v = fail[v]
  return res
# 求每个模式次数: 命中节点 acc++ -> 按 fail 树逆拓扑累加
```

### Python 实现

```python
from collections import deque


class AhoCorasick:
    """AC 自动机: Trie + 失配指针(fail) + Trie图(补全转移).
    build 后 tr[u][c] 为补全后的转移; fail[u] 指向最长后缀状态.
    匹配复杂度 O(文本长) 不计输出, 建图 O(模式串总长 * 字符集)."""
    def __init__(self, alpha_size=26):
        self.alpha = alpha_size
        self.tr = [[0] * self.alpha]    # tr[0] 全 0 表示根
        self.fail = [0]
        self.cnt = [0]                  # 该节点作为模式串结尾的次数(0/1)
        self.used = []                  # 匹配时已计入答案的模式(去重)

    def add(self, s):
        u = 0
        for ch in s:
            c = ord(ch) - ord('a')
            if self.tr[u][c] == 0:
                self.tr[u][c] = len(self.tr)
                self.tr.append([0] * self.alpha)
                self.fail.append(0)
                self.cnt.append(0)
                self.used.append(False)
            u = self.tr[u][c]
        self.cnt[u] += 1

    def build(self):
        """BFS 构建 fail, 同时把不存在的转移补全为 fail 的转移(Trie图)."""
        q = deque()
        for c in range(self.alpha):
            v = self.tr[0][c]
            if v:
                self.fail[v] = 0
                q.append(v)
        while q:
            u = q.popleft()
            for c in range(self.alpha):
                v = self.tr[u][c]
                if v:
                    self.fail[v] = self.tr[self.fail[u]][c]
                    q.append(v)
                else:
                    self.tr[u][c] = self.tr[self.fail[u]][c]

    def query(self, text):
        """返回文本中出现的模式串个数(每个模式串计一次)."""
        u = 0
        res = 0
        for ch in text:
            c = ord(ch) - ord('a')
            u = self.tr[u][c]
            v = u
            while v and self.cnt[v]:
                res += self.cnt[v]
                self.cnt[v] = 0
                v = self.fail[v]
        return res

    def query_count_all(self, text):
        """返回每个模式串在文本中的出现次数(含重叠), 借助 fail 树自底向上累加.
        要求已 build. 返回数组 acc, 下标为节点号, acc[结束节点] 即该模式串出现次数."""
        n = len(self.tr)
        acc = [0] * n
        u = 0
        for ch in text:
            c = ord(ch) - ord('a')
            u = self.tr[u][c]
            acc[u] += 1
        # BFS 序(按真实 Trie 边, 深度非降). 逆序累加 => 自底向上沿 fail 树求和
        for v in reversed(self._order):
            acc[self.fail[v]] += acc[v]
        return acc

    def _record_order(self):
        """在 build 前调用: 用真实 Trie 边做 BFS, 记录节点序."""
        order = [0]
        q = deque([0])
        while q:
            u = q.popleft()
            for c in range(self.alpha):
                v = self.tr[u][c]
                if v:
                    order.append(v)
                    q.append(v)
        self._order = order

def build_ac(patterns):
    """便捷封装: 返回 (ac, end_nodes). end_nodes[i] 为第 i 个模式串的结束节点."""
    ac = AhoCorasick()
    ends = []
    for p in patterns:
        ac.add(p)
    # 记录真实儿子(在补全前)
    ac._record_order()
    for p in patterns:
        u = 0
        for ch in p:
            u = ac.tr[u][ord(ch) - ord('a')]
        ends.append(u)
    ac.build()
    return ac, ends


if __name__ == "__main__":
    patterns = ["she", "he", "his", "hers"]
    text = "ushersheishis"
    ac, ends = build_ac(patterns)
    assert ac.query("ushersheishis") >= 1
    # 计数每种模式
    ac2, ends2 = build_ac(patterns)
    acc = ac2.query_count_all(text)
    # 暴力验证
    def brute(patterns, text):
        res = {}
        for p in patterns:
            c = 0
            for i in range(len(text) - len(p) + 1):
                if text[i:i+len(p)] == p:
                    c += 1
            res[p] = c
        return res
    expected = brute(patterns, text)
    for p, e in zip(patterns, ends2):
        assert acc[e] == expected[p], (p, acc[e], expected[p])
    print("ac-automaton: all tests passed")

```

**PyPy 提示**: 用 list 嵌套 list 存 tr，字符集 26 时每节点 26 ints；总节点 1e6 时内存 ~100MB+，必要时用 dict 转移换内存。匹配用 while 沿 fail 链累加在极端数据（如所有模式互为后缀）会退化，务必用 fail 树拓扑/差分优化。build 的 BFS 用 collections.deque。PyPy 下 for c in range(26) 固定循环比遍历 dict 快。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 构建 O(Σ\|s_i\|·字符集)；匹配 O(\|S\|+z)；fail树统计 O(\|S\|+节点数) |
| 空间 | O(Σ\|s_i\|·字符集) 节点 |

### 局限

① 字符集大时每节点数组爆炸（改用 map 或压缩）；② 朴素匹配每次沿 fail 链跳在重叠严重数据上退化，需拓扑优化；③ 不能匹配重叠模式的最长公共后缀之外的形态（需后缀自动机）；④ Python 实现注意对象/数组内存权衡；⑤ 建图补全修改了 tr 结构，无法直接复用为纯 Trie。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3808 | 3 | AC 自动机（简单版）：统计出现过的模式串个数，OI Wiki 模板 | [https://www.luogu.com.cn/problem/P3808](https://www.luogu.com.cn/problem/P3808) |
| Luogu | P3796 | 3 | AC 自动机（简单版 II）：统计出现次数最多的模式串（需要逐个计数） | [https://www.luogu.com.cn/problem/P3796](https://www.luogu.com.cn/problem/P3796) |
| Luogu | P5357 | 3 | AC 自动机【模板】：全模式计数，必须用 fail 树拓扑优化，OI Wiki 模板 | [https://www.luogu.com.cn/problem/P5357](https://www.luogu.com.cn/problem/P5357) |
| Luogu | P2292 | 4 | HNOI2004 L 语言：AC 自动机 + DP / 状态压缩优化 | [https://www.luogu.com.cn/problem/P2292](https://www.luogu.com.cn/problem/P2292) |

## Pitfalls · 易错点

- 根的儿子 fail 忘了置 0（应直接入队而非根本身）
- build 时没做 Trie 图补全，匹配时回溯 fail 太慢
- 朴素 query 每次跳 fail 链在重叠数据上 TLE（必须拓扑/DFS 优化）
- 多模式计数时重复清零 cnt 导致多模式计数丢失
- 字符集下标/文本字符越界
- 递归建树过深（总长 1e6）导致 RecursionError

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/string/ac-automaton/](https://oi-wiki.org/string/ac-automaton/)
- CP-Algorithms ✓ [https://cp-algorithms.com/string/aho_corasick.html](https://cp-algorithms.com/string/aho_corasick.html)
- 论文 ✓ [https://dl.acm.org/doi/10.1145/360825.360855](https://dl.acm.org/doi/10.1145/360825.360855)
