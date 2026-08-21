---
id: block-forest
name: 圆方树
group: G-B-4
stage: advanced
priority: P3
depth_tier: brief
---

# 圆方树

> 点双连通缩点的树形结构：原图点=圆点、点双=方点，把一般无向图问题转化为树上问题

<!-- 元信息: id=block-forest · group=G-B-4 · stage=advanced · priority=P3 · depth_tier=brief -->

## What · 是什么

圆方树(Round-Square Tree / Block-Cactus Tree)是将无向图转化为树的一种结构：原图每个点对应一个圆点，每个点双连通分量对应一个方点，方点与它代表的点双中所有圆点连边。这样原图有n个点、c个点双时，圆方树有n+c个点(小于2n)，每条边连接一个圆点和一个方点。原图连通时圆方树是一棵树，否则是森林。圆方树的关键性质：两圆点在圆方树上的路径经过的方点+圆点集合，恰好对应原图中两点间所有简单路径并集上的点集。因此常把'简单路径必经/可达哪些点'类问题(如铁人两项、战略游戏、点权最值)转化为树上路径问题，用树链剖分/倍增LCA/树形DP求解。

## Why · 为什么

### 直觉 · Intuition

圆方树把'由割点铰链连接的多个点双'结构化地拉直成一棵树：每个点双(方点)挂起它包含的所有圆点，割点被多个方点共享(出现在多个点双中)。由于原图中跨点双的唯一通路就是割点，两点间简单路径的必经点集在圆方树上表现为一条简单树上路径。这样就把一般图的复杂路径问题简化成了树上的路径问题。

### 原理 · Principle

构造算法是Tarjan求点双的变体：(1)DFS记录dfn/low，low允许通过父边向上更新；(2)维护栈，DFS时压栈；(3)当子节点v满足low[v]==dfn[u]时，说明找到一个以u为根的点双，不断弹栈直到v出栈，弹出的节点与u一起构成该点双，新建方点并与这些圆点连边；(4)u本身不弹出(作为割点可能属于多个点双)，但每个块中u都连向方点。方点编号从n+1开始。孤立点按题意单独处理。构造复杂度O(n+m)。

### 历史 · History

圆方树最初用于处理仙人掌图(每条边至多属于一个简单环)，后来推广到一般无向图，成为将图问题树上化的重要工具。其理论源于点双连通分量与割点理论(Tarjan,1972)。OI Wiki的block-forest页、以及APIO2018铁人两项、CF487E Tourists、SDOI2018战略游戏等经典题的官方题解都是其应用。

## How · 实现

### 伪代码

```python
build(u, parent):
  dfn[u]=low[u]=++timer
  stk.push(u)
  for v in adj[u]:
    if not dfn[v]:
      build(v,u)
      low[u]=min(low[u],low[v])
      if low[v]==dfn[u]:      # u为点双的根
        cnt+=1                # 新建方点 cnt
        while stk.top()!=v:
          x=stk.pop()
          add_edge(cnt, x)    # 方点连圆点
        x=stk.pop(); add_edge(cnt, x)
        add_edge(cnt, u)      # u也连向方点, 但不弹出
    elif v!=parent:
      low[u]=min(low[u],dfn[v])
```

### Python 实现

```python
import sys

sys.setrecursionlimit(1 << 25)


def build_block_forest(n, adj):
    """构造圆方树.
    n: 原图点数(0-based), adj[u]=[v,...]
    return: (tree, square_start)
      tree: 圆方树邻接表 (0..n-1圆点, n.. 方点)
      square_start: 方点起始编号
    """
    dfn = [0] * n
    low = [0] * n
    timer = [0]
    stk = []
    tree = [[] for _ in range(2 * n)]
    sq_cnt = [n]

    def add(u, v):
        tree[u].append(v)
        tree[v].append(u)

    def tarjan(u):
        dfn[u] = low[u] = timer[0] = timer[0] + 1
        stk.append(u)
        for v in adj[u]:
            if not dfn[v]:
                tarjan(v)
                low[u] = min(low[u], low[v])
                if low[v] == dfn[u]:  # u是该点双的根
                    sq = sq_cnt[0]
                    sq_cnt[0] += 1
                    while True:
                        x = stk.pop()
                        add(sq, x)
                        if x == v:
                            break
                    add(sq, u)  # u不弹出, 也连方点
            else:
                low[u] = min(low[u], dfn[v])

    for s in range(n):
        if not dfn[s]:
            tarjan(s)
    return tree, n


if __name__ == "__main__":
    # 测试: 环 0-1-2-0 (一个点双) + 2-3 (单边, 一个点双)
    # 点双: {0,1,2} 和 {2,3}, 割点 2
    # 圆方树: 先触发方点4(点双{2,3}), 再触发方点5(点双{0,1,2})
    adj = [[] for _ in range(4)]
    for u, v in [(0, 1), (1, 2), (2, 0), (2, 3)]:
        adj[u].append(v)
        adj[v].append(u)
    tree, _ = build_block_forest(4, adj)
    # 统计方点(编号>=4)
    squares = [i for i in range(len(tree)) if i >= 4 and tree[i]]
    assert squares == [4, 5], squares
    # 方点4连2,3; 方点5连0,1,2
    assert set(tree[4]) == {2, 3}, tree[4]
    assert set(tree[5]) == {0, 1, 2}, tree[5]
    # 边数 = 圆点数+方点数-1(连通树) = 4+2-1=5
    edge_count = sum(len(x) for x in tree) // 2
    assert edge_count == 5, edge_count

    # 简单链 0-1-2: 每个点双为单边, 三个方点, 圆方树即原树
    adj2 = [[] for _ in range(3)]
    for u, v in [(0, 1), (1, 2)]:
        adj2[u].append(v)
        adj2[v].append(u)
    tree2, _ = build_block_forest(3, adj2)
    edge2 = sum(len(x) for x in tree2) // 2
    assert edge2 == 4, edge2  # 3圆点+2方点, 树边=5-1=4

    print("block-forest: ALL TESTS PASSED")

```

**PyPy 提示**: 树数组要开2n以上(方点数< n, 总点数<2n)。弹栈逻辑(到v为止, u不弹出)是正确性关键。图不连通时圆方树为森林，路径查询需按连通块处理。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(V+E) — 一次Tarjan构造 |
| 空间 | O(V+E) — 邻接表+栈+圆方树(≤2n点) |

### 局限

圆方树基于点双而非边双；孤立点与单边点双需按题意特判。构造用low[v]==dfn[u]触发(可含自环/重边情形需具体分析)。一般图圆方树上的方点代表点双, 仙人掌图则每个方点对应一个环。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| LOJ | 2587 | 6 | APIO2018铁人两项：圆方树+方点权值(点双大小)/圆点权-1, 树形DP统计 | [https://loj.ac/p/2587](https://loj.ac/p/2587) |
| Codeforces | 487E | 2600 | Tourists：圆方树+multiset维护方点权+树链剖分, 支持单点修改路径最小值 | [https://codeforces.com/contest/487/problem/E](https://codeforces.com/contest/487/problem/E) |
| LOJ | 2562 | 6 | SDOI2018战略游戏：圆方树上统计点集对应连通子图中圆点个数 | [https://loj.ac/p/2562](https://loj.ac/p/2562) |

## Pitfalls · 易错点

- 数组要开2n以上(圆方树点数<2n), 开小会越界
- 弹栈到v为止且u不弹出: u作为割点属于多个点双
- low[v]==dfn[u]才触发建方点(与割点判定low[v]>=dfn[u]不同, 与桥判定low[v]>dfn[u]更不同)
- 查询路径最值时若LCA是方点需额外取LCA父亲圆点的权
- 图不连通时是圆方森林, 需按连通块处理

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/block-forest/](https://oi-wiki.org/graph/block-forest/)
- Wikipedia ✓ [https://en.wikipedia.org/wiki/Biconnected_component](https://en.wikipedia.org/wiki/Biconnected_component)
