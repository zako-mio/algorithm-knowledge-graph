---
id: dfs
name: DFS深度优先搜索
group: G-B-1
stage: basic
priority: P0
depth_tier: deep
---

# DFS深度优先搜索

> 递归深入遍历O(V+E)，连通性判定与DFS生成树基础；沿一条路径深入到底再回溯，栈/递归实现，空间O(h)

<!-- 元信息: id=dfs · group=G-B-1 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

DFS（Depth First Search）是图/树遍历算法，从起点出发，每次尝试向更深的节点走，走到无路可走时回溯。通过递归调用自身或显式栈实现。每个节点仅访问一次（打访问标记）。DFS生成树是原图的一个生成树，其性质可用于求强连通分量、割点、桥等。DFS序列中每个子树对应连续区间，可用于树上问题。

## Why · 为什么

### 直觉 · Intuition

想象走迷宫：每次选一条路走到尽头，走不通了就退回上一个岔路口换路。这就是'深度优先'——优先往深处探索，而非广度优先地逐层展开。

### 原理 · Principle

DFS的核心是递归调用自身+访问标记。对当前节点打标记后遍历其所有邻居，若邻居未访问则递归。递归调用栈天然实现回溯。时间O(V+E)需用邻接表存储图（均摊O(1)遍历每条边）。

### 历史 · History

DFS由Tarjan在1972年系统化用于图论算法。递归实现利用函数调用栈，与BFS用队列形成对应。OI Wiki指出大部分竞赛支持无限栈空间。

## How · 实现

### 伪代码

```python
DFS(v):
  mark v as visited
  for u in neighbors(v):
    if u not visited:
      DFS(u)
```

### Python 实现

```python
import sys
sys.setrecursionlimit(1000000)

def dfs_recursive(adj, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    for v in adj[start]:
        if v not in visited:
            dfs_recursive(adj, v, visited)
    return visited

def dfs_iterative(adj, start):
    visited = set()
    stack = [start]
    while stack:
        u = stack.pop()
        if u in visited:
            continue
        visited.add(u)
        for v in adj[u]:
            if v not in visited:
                stack.append(v)
    return visited

def dfs_tree_edges(adj, start):
    """Return DFS tree edges (parent, child)."""
    visited = set([start])
    edges = []
    def _dfs(u):
        for v in adj[u]:
            if v not in visited:
                visited.add(v)
                edges.append((u, v))
                _dfs(v)
    _dfs(start)
    return edges

if __name__ == "__main__":
    adj = {0: [1, 2], 1: [0, 3], 2: [0, 3], 3: [1, 2]}
    r1 = dfs_recursive(adj, 0)
    r2 = dfs_iterative(adj, 0)
    assert r1 == r2 == {0, 1, 2, 3}, f"DFS failed: {r1}, {r2}"
    tree = dfs_tree_edges(adj, 0)
    assert len(tree) == 3
    # Disconnected graph: only reaches one component
    adj2 = {0: [1], 1: [0], 2: [3], 3: [2]}
    r3 = dfs_recursive(adj2, 0)
    assert r3 == {0, 1}, f"Discon DFS failed: {r3}"
    print("dfs: ALL TESTS PASSED")

```

**PyPy 提示**: 递归DFS在PyPy中可能因递归深度限制（默认1000）而崩溃。用sys.setrecursionlimit调大，或改用迭代栈实现。PyPy递归比CPython慢，深递归建议迭代化。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(V+E) |
| 空间 | O(V)（含递归栈） |

### 局限

递归深度受栈空间限制，深图（如链）可能栈溢出。非连通图只能访问起点所在连通分量。DFS序列不唯一（取决于邻居遍历顺序）。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| LeetCode | 200 | 4 | 用 DFS/BFS 统计连通块数量 | [https://leetcode.cn/problems/number-of-islands/](https://leetcode.cn/problems/number-of-islands/) |
| Luogu | P3916 | 4 | 反向建图 DFS 求可达最大编号 | [https://www.luogu.com.cn/problem/P3916](https://www.luogu.com.cn/problem/P3916) |
| AtCoder | ABC277 D | 3 | DFS 遍历连通分量求和 | [https://atcoder.jp/contests/abc277](https://atcoder.jp/contests/abc277) |

## Pitfalls · 易错点

- 递归深度限制：Python默认1000层，需setrecursionlimit或改用栈
- 邻接矩阵存储时时间退化为O(V^2)
- 迭代栈实现中，pop顺序可能导致访问顺序与递归不同（逆序压栈）
- 未标记已访问节点可能导致重复访问/死循环

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/dfs/](https://oi-wiki.org/graph/dfs/)
- CP-Algorithms ✓ [https://cp-algorithms.com/graph/depth-first-search.html](https://cp-algorithms.com/graph/depth-first-search.html)
- 书籍 ✓ `CPH ch12 pp127-132`
