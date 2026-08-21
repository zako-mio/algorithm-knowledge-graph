---
id: hopcroft-karp
name: Hopcroft-Karp算法
group: G-B-6
stage: advanced
priority: P2
depth_tier: standard
---

# Hopcroft-Karp算法

> 二分图匹配，多增广路O(E√V)

<!-- 元信息: id=hopcroft-karp · group=G-B-6 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

Hopcroft-Karp（HK）算法是二分图最大匹配的最优算法之一，复杂度 O(E√V)。它把 Kuhn 的单次单增广路升级为『每一轮找到多条互不相交的最短增广路（阻塞流）同时增广』：先 BFS 从所有未匹配左部点建层次图（dist），只到找到第一个含未匹配右部点的层为止；再按层次严格递增的限制做 DFS 找若干条点不相交的最短增广路一起翻转。最短增广路长度每轮严格增加，总轮数 O(√V)，故总复杂度 O(E√V)。实际上它是 Dinic 求二分图匹配（容量 1 网络）的特例。

## Why · 为什么

### 直觉 · Intuition

Kuhn 每次只找一条增广路，而很多右部点在同一轮里明明可以并行让座。HK 用 BFS 把『最短增广路』看成一整层的匹配机会：层次图里从每个未匹配左部点出发，找到的所有最短增广路互不相交，一次性全增广。因为每轮用的都是最短增广路，最短长度严格递增，而长度不会超过 √V 次，所以轮次被限制在 O(√V)。

### 原理 · Principle

① 层次图：将匹配边定向为右→左、非匹配边定向为左→右，从所有未匹配左部点 BFS，dist 记录层号，遇到未匹配右部点即停（found=True），若 BFS 结束没找到 → 当前匹配最大；② DFS(u) 沿 dist[v]=dist[u]+1 的边推进，只走未访问点，找到未匹配右部点则完成一条增广路并翻转（用 pairU/pairV）；③ 一轮内收集尽量多的点不相交最短增广路（即 Dinic 的阻塞流）；④ 复杂度证明：增广路长度每轮严格递增（对称差论证 |P'| ≥ |P|+2|P∩P'|），长度至多增加 3|M|^0.5 次，故轮数 O(√V)，每轮 O(E)，总 O(E√V)。随机图中大概率 O(E log V)。

### 历史 · History

John E. Hopcroft 与 Richard M. Karp 于 1973 年在 SIAM J. Comput. 发表『An n^{5/2} algorithm for maximum matchings in bipartite graphs』。该算法奠定了二分图匹配在稀疏大图上的标准做法，也被视为网络流算法在单位容量图上的先声（后与 Dinic 联系）。OI Wiki 与 CP-Algorithms 均有标准实现。

## How · 实现

### 伪代码

```python
pairU[u] = -1 (左部 u 匹配的右部); pairV[v] = -1

bfs():
  q = 所有未匹配左部点, dist=0
  dist[NIL] = -1; found = False
  while q:
    u = pop(q)
    for v in adj[u]:
      w = pairV[v]
      if w == -1: found = True          # 找到未匹配右部点
      elif dist[w] == -1:
        dist[w] = dist[u] + 1; push(q, w)
  return found

dfs(u):
  for v in adj[u]:
    w = pairV[v]
    if w == -1 or (dist[w] == dist[u]+1 and dfs(w)):
      pairU[u] = v; pairV[v] = u; return True
  dist[u] = -1; return False

matching = 0
while bfs():
  for u in 左部点:
    if pairU[u] == -1 and dfs(u): matching += 1
```

### Python 实现

```python
from collections import deque


def hopcroft_karp(left_n, right_m, adj):
    """Hopcroft-Karp 求二分图最大匹配，O(E√V)。
    adj[u]: 左部点 u 的右部点邻居列表。返回 (匹配数, pairU, pairV)。"""
    pairU = [-1] * left_n
    pairV = [-1] * right_m
    NIL = left_n
    dist = [-1] * (left_n + 1)

    def bfs():
        q = deque()
        found = False
        for u in range(left_n):
            if pairU[u] == -1:
                dist[u] = 0
                q.append(u)
            else:
                dist[u] = -1
        dist[NIL] = -1
        while q:
            u = q.popleft()
            for v in adj[u]:
                w = pairV[v]
                if w == -1:
                    found = True
                elif dist[w] == -1:
                    dist[w] = dist[u] + 1
                    q.append(w)
        return found

    def dfs(u):
        for v in adj[u]:
            w = pairV[v]
            if w == -1 or (dist[w] == dist[u] + 1 and dfs(w)):
                pairU[u] = v
                pairV[v] = u
                return True
        dist[u] = -1
        return False

    res = 0
    while bfs():
        for u in range(left_n):
            if pairU[u] == -1 and dfs(u):
                res += 1
    return res, pairU, pairV


if __name__ == '__main__':
    import random

    def kuhn(n, m, adj):
        match = [-1] * m

        def tr(u, vis):
            for v in adj[u]:
                if vis[v]:
                    continue
                vis[v] = True
                if match[v] == -1 or tr(match[v], vis):
                    match[v] = u
                    return True
            return False

        r = 0
        for u in range(n):
            if tr(u, [False] * m):
                r += 1
        return r

    random.seed(5)
    for _ in range(200):
        n = random.randint(1, 20)
        m = random.randint(1, 20)
        adj = [[] for _ in range(n)]
        for u in range(n):
            for v in range(m):
                if random.random() < 0.25:
                    adj[u].append(v)
        r1, _, _ = hopcroft_karp(n, m, adj)
        r2 = kuhn(n, m, adj)
        assert r1 == r2, (n, m, adj, r1, r2)
    print('hopcroft-karp: All tests passed.')
```

**PyPy 提示**: 实现注意：BFS 的 found 逻辑与 dist 更新要在遇到未匹配右部点时不展开其后续；DFS 的 dist[u]=-1 剪枝（走过的失败左部点标记避免重复）。邻接表尽量紧凑；n,m 到 1e5、E 到 5e5 时 O(E√V) 在 PyPy 下是标准做法。Python 递归 dfs 深度最大 √V，安全，但可改显式栈。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(E√V)（O(√V) 轮 × 每轮 BFS+DFS 共 O(E)）；随机图大概率 O(E log V) |
| 空间 | O(V+E) 邻接表 + O(V) dist/pair 数组 |

### 局限

只适用二分图（一般图需带花树）。若图已接近完全（E~n²）或 n 小，Kuhn 常数更小。BFS 提前终止的优化（遇到未匹配右部点不扩展）在某些图反而更慢（OI Wiki 提示）。只求最大匹配基数/方案，无权值。需配合 bipartite-check 确认二分性。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Library Checker | bipartitematching | 3 | Matching on Bipartite Graph 模板题：HK 标准模板，OI Wiki 参考实现题 | [https://judge.yosupo.jp/problem/bipartitematching](https://judge.yosupo.jp/problem/bipartitematching) |
| Luogu | P3386 | 3 | 【模板】二分图最大匹配：Kuhn 与 HK 均可，HK 用于大数据模板 | [https://www.luogu.com.cn/problem/P3386](https://www.luogu.com.cn/problem/P3386) |
| Luogu | P1640 | 4 | 【SCOI2010】连续攻击游戏：属性-编号二分图匹配，图大时 HK 优于 Kuhn | [https://www.luogu.com.cn/problem/P1640](https://www.luogu.com.cn/problem/P1640) |
| LOJ | 6002 | 3 | 最小路径覆盖：DAG 拆点后二分图匹配，\|V\|-最大匹配，HK 加速 | [https://loj.ac/p/6002](https://loj.ac/p/6002) |

## Pitfalls · 易错点

- BFS 中未匹配右部点只是置 found=True，不能再沿它的 pairV（-1）入队
- DFS 必须先判 pairV[v]==-1 或（dist[w]==dist[u]+1 且 dfs(w)），条件顺序错误会走非层次边
- 每轮 while bfs() 后要重新对未匹配左部点 dfs，不能用缓存的上轮 dist
- dist 数组大小 left_n+1（含 NIL 哨兵），索引越界是常见 bug
- 找最大匹配数要在找到后就累加，不能在 while 结束后再数 pairU
- 图巨大时 Python 递归 dfs 每次新建 list 会慢，尽量复用数组

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/graph-matching/bigraph-match/](https://oi-wiki.org/graph/graph-matching/bigraph-match/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/graph-matching/bigraph-match.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/graph-matching/bigraph-match.md)
- 书籍 ✓ `Hopcroft & Karp 1973, An n^{5/2} algorithm for maximum matchings in bipartite graphs`
- 书籍 ✓ `CLRS ch26.3 (bipartite matching via max flow)`
