---
id: hungarian
name: 匈牙利算法(Kuhn)
group: G-B-6
stage: intermediate
priority: P1
depth_tier: standard
---

# 匈牙利算法(Kuhn)

> 二分图最大匹配，增广路O(VE)

<!-- 元信息: id=hungarian · group=G-B-6 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

匈牙利算法（Kuhn 算法）求二分图最大匹配（maximum bipartite matching）：从空匹配出发，反复寻找增广路并沿其翻转匹配，直到不存在增广路——由 Berge 引理，此时匹配最大。Kuhn 版本对每个左部未匹配点做一次 DFS 找增广路，单次 O(E)，总 O(VE)。实现极简：维护右部点的匹配对象 match[v]，DFS 尝试为左部点 u 找未匹配右部点，被占用的右部点则递归让它的左部匹配对象『挪窝』。是竞赛最常用的二分图匹配模板，也是网络流与 Hopcroft-Karp 的思想基石。

## Why · 为什么

### 直觉 · Intuition

把右部点看成『座位』，左部点来抢座。有人坐了就去找坐着的那个左部点：你能换别的座吗？能就让座，不能就另寻。递归地『让座』构成一条交错路；当这条路的起点左部点和终点右部点都未匹配，就是增广路，沿路反转即可把匹配数 +1。没有增广路时（Berge 引理）就达到了最大。

### 原理 · Principle

① 匹配 M、增广路定义：交替路径且首尾都是未匹配点；② Berge 引理：M 最大 ⇔ 不存在相对于 M 的增广路（若存在则 M⊕P 更大；若 M' 更大，对称差 M⊕M' 的连通分量中必有从 M' 边多于 M 边的交替路，即增广路）；③ Kuhn 算法：对每个左部点 u 做一次 DFS（增广一次，最多 n 次增广），DFS 中 visited 标记本次已访问的右部点避免死循环，对右部点 v：若未匹配则匹配 u-v；否则递归 try(match[v]) 让座；④ 复杂度：n 次增广 × 每次 DFS O(E) = O(VE)。小优化：优先选未匹配右部点、visited 复用（每轮 O(E) 找到多条增广路）可常数级优化。

### 历史 · History

1931 年 Kőnig 证明了二分图匹配基本定理；匈牙利算法（Hungarian algorithm）名称源于 Kőnig 与 Egerváry 的匈牙利工作。Kuhn 1955 年发表求解指派问题（最大权完美匹配）的算法，后来 'Kuhn 算法' 通常特指增广路法最大匹配（OI Wiki 与 CP-Algorithms 均如此分类），O(VE)。该算法是理解网络流增广、Hopcroft-Karp 的前提。

## How · 实现

### 伪代码

```python
match[v] = -1 for v in 右部

def try_kuhn(u, visited):
  for v in adj[u]:
    if visited[v]: continue
    visited[v] = True
    if match[v] == -1 or try_kuhn(match[v], visited):
      match[v] = u
      return True
  return False

matching = 0
for u in 左部:
  visited = [False] * m
  if try_kuhn(u, visited): matching += 1
```

### Python 实现

```python
def hungarian_maximum_matching(left_n, right_m, adj):
    """Kuhn 算法求二分图最大匹配。
    left_n/right_m: 左右部点数; adj[u]: 左部点 u 可连的右部点列表。
    返回 (最大匹配数, match: 右部点 v 匹配的左部点, -1 表示未匹配)。"""
    match = [-1] * right_m

    def try_kuhn(u, visited):
        for v in adj[u]:
            if visited[v]:
                continue
            visited[v] = True
            if match[v] == -1 or try_kuhn(match[v], visited):
                match[v] = u
                return True
        return False

    res = 0
    for u in range(left_n):
        if try_kuhn(u, [False] * right_m):
            res += 1
    return res, match


if __name__ == '__main__':
    # 手工例子: 左 {0,1,2}, 右 {0,1,2}
    adj = [[0, 1], [1], [2]]
    res, match = hungarian_maximum_matching(3, 3, adj)
    assert res == 3, res
    # 随机图与 Hopcroft-Karp/暴力交叉验证
    import random
    random.seed(5)

    def brute_max(n, m, adj):
        from itertools import combinations
        edges = []
        for u in range(n):
            for v in adj[u]:
                edges.append((u, v))
        best = 0
        for r in range(min(n, m) + 1):
            for comb in combinations(edges, r):
                lu = set(e[0] for e in comb)
                rv = set(e[1] for e in comb)
                if len(lu) == r and len(rv) == r:
                    best = max(best, r)
        return best

    for _ in range(60):
        n = random.randint(1, 5)
        m = random.randint(1, 5)
        adj = [[] for _ in range(n)]
        for u in range(n):
            for v in range(m):
                if random.random() < 0.4:
                    adj[u].append(v)
        res, _ = hungarian_maximum_matching(n, m, adj)
        assert res == brute_max(n, m, adj), (n, m, adj, res)
    print('hungarian: All tests passed.')
```

**PyPy 提示**: 注意每次 DFS 都要重置 visited 数组（[False]*m 每个 u 一次），这是 O(VE) 的来源。优化技巧：visited 时间戳（每轮用一个递增整数标记而非新建 list）可省常数；优先选未匹配右部点；左右部可交换取小的一侧做左部使复杂度 O(min(X,Y)·E)。用数组模拟栈替代递归可避免深递归。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(V·E)（n 次增广，每次 DFS O(E)）；其中 V 是左部点数，可优化为 O(min(X,Y)·E) |
| 空间 | O(V+E) 邻接表 + O(右部点数) match 数组 |

### 局限

稠密图或大规模时 O(VE) 会超时，需用 Hopcroft-Karp O(E√V)。递归 DFS 在深图会爆栈（PyPy 需加大递归限制或改迭代）。只求最大匹配基数，若需求最大权匹配用 KM 算法。二分图性质是前提，一般图需带花树。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3386 | 3 | 【模板】二分图最大匹配：Kuhn 标准模板题（n,m 500，E 50000 恰好 O(VE) 可过） | [https://www.luogu.com.cn/problem/P3386](https://www.luogu.com.cn/problem/P3386) |
| Luogu | P1129 | 4 | 矩阵游戏：01 矩阵能否交换行列使对角线全 1，建模为行-列二分图完美匹配，OI Wiki 例题 | [https://www.luogu.com.cn/problem/P1129](https://www.luogu.com.cn/problem/P1129) |
| Luogu | P1640 | 4 | 【SCOI2010】连续攻击游戏：属性-编号二分图匹配求最大连续值，经典建图 | [https://www.luogu.com.cn/problem/P1640](https://www.luogu.com.cn/problem/P1640) |
| AtCoder | abc274_g | 5 | Security Camera 3：网格行/列覆盖二分图建图（最大匹配=最小点覆盖），OI Wiki 习题 | [https://atcoder.jp/contests/abc274/tasks/abc274_g](https://atcoder.jp/contests/abc274/tasks/abc274_g) |
| LOJ | 6002 | 3 | 最小路径覆盖：DAG 拆点二分图匹配，\|V\|-最大匹配，OI Wiki 习题 | [https://loj.ac/p/6002](https://loj.ac/p/6002) |

## Pitfalls · 易错点

- visited 数组忘重置会导致同一右部点被重复递归 → 错误/死循环
- match 数组方向写反（match[左] vs match[右]）导致增广失败
- 递归让座 try_kuhn(match[v], visited) 忘记传 visited，导致循环依赖
- 左部点遍历到匹配点仍要尝试（可能换座得到更大的匹配），不能跳过已匹配左部点
- 二分图前提：非二分图直接跑会得到错误结果（需先 bipartite-check）
- 稠密大图 O(VE) 超时：n≥1e4 或 E 大时应换 Hopcroft-Karp

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/graph-matching/bigraph-match/](https://oi-wiki.org/graph/graph-matching/bigraph-match/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/graph-matching/bigraph-match.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/graph-matching/bigraph-match.md)
- CP-Algorithms ✓ [https://cp-algorithms.com/graph/kuhn_maximum_bipartite_matching.html](https://cp-algorithms.com/graph/kuhn_maximum_bipartite_matching.html)
- 书籍 ✓ `CPH ch20 pp191-204`
