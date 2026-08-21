---
id: general-match
name: 一般图匹配
group: G-B-6
stage: advanced
priority: P3
depth_tier: brief
---

# 一般图匹配

> 带花树算法(Blossom)，一般图最大匹配O(V³)

<!-- 元信息: id=general-match · group=G-B-6 · stage=advanced · priority=P3 · depth_tier=brief -->

## What · 是什么

一般图匹配（maximum matching in general graphs）问题是求任意无向图（含奇环）的最大匹配。二分图匹配的增广路法在奇环上失效（沿环翻转会让某点被两条边同时匹配），因此 Edmonds 1961 年提出带花树算法（Blossom Algorithm）：在 BFS 找增广路的过程中，遇到标记『o』的两点形成奇环时，将整个奇环收缩为一个『花根』（虚点），缩花后的图上继续找增广路，找到后在原图展开。最简实现 O(VE²)（OI Wiki），随机化/优化版 O(V³)；还有基于 Tutte 矩阵高斯消元的 O(V³) 随机化算法。

## Why · 为什么

### 直觉 · Intuition

二分图匹配时偶环可绕开，但一般图的奇环是拦路虎：沿着奇环做交替翻转会让某点同时匹配两条边。带花树的核心洞察：奇环本质上像一个『大点』，环内点最终只会有一个对外匹配边。所以把奇环收缩成一个花根继续跑增广路，找到后展开即可。这是『把一般图问题降维成类似二分图』的经典手法。

### 原理 · Principle

① 从每个未匹配点出发做 BFS，交错标记 o（外点）/i（内点），i→o 边是匹配边；② 遇到已访问的外点 u 且 orig[v]≠orig[u]（v 也是外点，或 v 的配偶可延伸），则找到奇环，用 LCA 找花根 h，把环上点收缩（用并查集式 orig 数组记录属于哪朵花），环上 i 标记点变为外点入队继续；③ 找到未匹配点则沿 parent 链展开增广；④ 每次 BFS 尝试所有边并维护花，最坏 O(E²)，枚举所有未匹配点作根总 O(VE²)。正确性：缩花保持『G 有增广路 ⇔ G' 有增广路』。

### 历史 · History

Jack Edmonds 1961 年提出带花树（Blossom）算法并给出最大匹配问题的多项式算法——这是计算复杂性理论史上第一个『非平凡、可在多项式时间求解的组合优化问题』证明，Edmonds 因此获得 1985 图灵奖。后续由优化/线性代数（Tutte 矩阵，Mucha-Sankowski）延伸。加权一般图匹配则有 Blossom 的加权版（Edmonds 1965）。

## How · 实现

### 伪代码

```python
match[v] = 配偶 (全局)
bfs(root):
  label[root]=o; q=[root]; 初始化 orig[i]=i
  while q:
    v = pop(q)
    for u in adj[v]:
      if label[u] == 未标记:
        label[u]=i; parent[u]=v
        if match[u] == -1: augment(u); return True
        label[match[u]]=o; push(q, match[u])
      elif label[u]==o and orig[v]!=orig[u]:
        a = lca(orig[v], orig[u])   # 用时间戳交替跳匹配边父链求花根
        blossom(u, v, a); blossom(v, u, a)  # 缩花
  return False
主循环: 贪心初匹配后, 对每个未匹配点跑 bfs, 有则增广
```

### Python 实现

```python
from collections import deque


def general_match_max(n, adj):
    """一般图最大匹配（带花树，最简实现 O(VE²)）。
    adj[u]: 邻居列表（无向）。返回 match: match[u] = u 的配偶（-1 未匹配）。"""
    match = [-1] * n
    p = [-1] * n
    base = list(range(n))
    used = [False] * n
    blossom = [False] * n
    q = deque()

    def lca(a, b):
        used_lca = [False] * n
        while True:
            a = base[a]
            used_lca[a] = True
            if match[a] == -1:
                break
            a = p[match[a]]
        while True:
            b = base[b]
            if used_lca[b]:
                return b
            b = p[match[b]]

    def mark_path(v, b, children):
        while base[v] != b:
            blossom[base[v]] = blossom[base[match[v]]] = True
            p[v] = children
            children = match[v]
            v = p[match[v]]

    def find_path(root):
        used[:] = [False] * n
        p[:] = [-1] * n
        for i in range(n):
            base[i] = i
        q = deque([root])
        used[root] = True
        while q:
            v = q.popleft()
            for u in adj[v]:
                if base[v] == base[u] or match[v] == u:
                    continue
                if u == root or (match[u] != -1 and p[match[u]] != -1):
                    curbase = lca(v, u)
                    blossom[:] = [False] * n
                    mark_path(v, curbase, u)
                    mark_path(u, curbase, v)
                    for i in range(n):
                        if blossom[base[i]]:
                            base[i] = curbase
                            if not used[i]:
                                used[i] = True
                                q.append(i)
                elif p[u] == -1:
                    p[u] = v
                    if match[u] == -1:
                        return u
                    u = match[u]
                    used[u] = True
                    q.append(u)
        return -1

    def enlarge(u):
        while u != -1:
            v = p[u]
            nv = match[v]
            match[u], match[v] = v, u
            u = nv

    for i in range(n):
        if match[i] == -1:
            v = find_path(i)
            if v != -1:
                enlarge(v)
    return match


if __name__ == '__main__':
    import random

    def brute_max(n, adj):
        """一般图最大匹配的暴力枚举（每个点至多被匹配一次）"""
        best = 0

        def rec(used_v, cnt):
            nonlocal best
            best = max(best, cnt)
            u = -1
            for i in range(n):
                if not (used_v >> i) & 1:
                    u = i
                    break
            if u == -1:
                return
            rec(used_v | (1 << u), cnt)
            for w in adj[u]:
                if not (used_v >> w) & 1:
                    rec(used_v | (1 << u) | (1 << w), cnt + 1)
        rec(0, 0)
        return best

    random.seed(7)
    for _ in range(150):
        n = random.randint(2, 10)
        adj = [set() for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.35:
                    adj[i].add(j)
                    adj[j].add(i)
        adj = [list(s) for s in adj]
        mt = general_match_max(n, adj)
        size = sum(1 for i in range(n) if mt[i] != -1 and mt[i] > i)
        assert size == brute_max(n, adj), (n, adj, mt, size, brute_max(n, adj))
    print('general-match: All tests passed.')
```

**PyPy 提示**: 该实现 O(VE²)，适合 n≤500。优化：BFS 用时间戳 lca、base 用并查集带路径压缩；展开增广时注意循环链。大规模（n 1e4）需随机化/线性代数 O(V³) 版或直接调库。Python 中 blossom 数组复用避免每次 new。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 朴素带花树 O(VE²)；随机化/优化 O(V³)；高斯消元 Tutte 矩阵 O(V³) |
| 空间 | O(V+E) 图 + O(V) match/p/base/blossom 数组 |

### 局限

实现复杂、易错，OI/ICPC 出现频率低（多为模板题或算法学习）。最简版 O(VE²) 在 n 大时超时。加权一般图最大匹配需带花树的加权版或费用流变体，更复杂。必须确认图含奇环才需要（二分图请用 HK/Kuhn 更快更简单）。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| UOJ | 79 | 5 | 一般图最大匹配模板题：带花树标准模板（OI Wiki 参考实现题） | [https://uoj.ac/problem/79](https://uoj.ac/problem/79) |
| UOJ | 171 | 6 | 【WC2016】挑战 NPC：一般图匹配建模（求最大匹配+特殊结构计数），OI Wiki 习题 | [https://uoj.ac/problem/171](https://uoj.ac/problem/171) |
| Codeforces | 1427B | 4 | 奇环图匹配的思维训练：判断结构是否可匹配的建模练习 | [https://codeforces.com/problemset/problem/1427/B](https://codeforces.com/problemset/problem/1427/B) |

## Pitfalls · 易错点

- 忘了奇环：直接对一般图跑 Kuhn/HK 会得到错误答案
- 缩花后 base 数组未对所有子树更新，导致后续 lca/parent 错乱
- lca 用时间戳实现时两个方向跳匹配边父链必须交替且正确记录
- find_path 中条件『u==root 或 p[match[u]]!=-1』判断花的形成，漏判会漏缩花
- 增广展开 enlarge 时 p 链的顺序要按 parent 逆序回退，写反死循环
- 贪心初匹配可显著加速，但随机顺序下正确性不依赖它（可略）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/graph-matching/general-match/](https://oi-wiki.org/graph/graph-matching/general-match/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/graph-matching/general-match.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/graph-matching/general-match.md)
- 书籍 ✓ `Edmonds 1965, Paths, trees, and flowers (Can. J. Math.); CPH ch20 (bipartite only, general via blossom)`
