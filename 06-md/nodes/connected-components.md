---
id: connected-components
name: 连通分量
group: G-B-1
stage: basic
priority: P0
depth_tier: deep
---

# 连通分量

> 无向图连通块，BFS/DFS遍历标记O(V+E)

<!-- 元信息: id=connected-components · group=G-B-1 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

连通分量是指无向图中极大连通子图。两个节点连通当且仅当它们之间存在路径。求连通分量只需遍历所有未访问节点，从每个未访问节点出发进行DFS/BFS即可标记一个连通分量。有向图需区分强连通分量（SCC）和弱连通分量。连通性还涉及点连通度（最小点割集大小）和边连通度（最小边割集大小），Whitney不等式κ≤λ≤δ。

## Why · 为什么

### 直觉 · Intuition

社交网络中的朋友圈：互相认识的人形成连通块，不同朋友圈之间没有认识关系。求连通分量就是把人分成独立的朋友圈。

### 原理 · Principle

对每个未访问节点i，从i出发DFS/BFS遍历所有可达节点并标记，即可找到一个连通分量。遍历所有节点后，遍历次数=连通分量数。用邻接表存储，时间O(V+E)。

### 历史 · History

连通分量是图论基本概念。Whitney不等式（1932）给出点连通度κ、边连通度λ和最小度δ的关系：κ≤λ≤δ。Menger定理将连通性与路径数量关联。

## How · 实现

### 伪代码

```python
comps = 0
for i in 1..n:
  if not visited[i]:
    comps += 1
    DFS(i)  # or BFS(i)
return comps
```

### Python 实现

```python
import sys
sys.setrecursionlimit(1000000)

def connected_components(n, edges):
    """Count connected components in undirected graph using iterative DFS."""
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    visited = [False] * n
    comps = 0
    for i in range(n):
        if not visited[i]:
            comps += 1
            stack = [i]
            visited[i] = True
            while stack:
                u = stack.pop()
                for v in adj[u]:
                    if not visited[v]:
                        visited[v] = True
                        stack.append(v)
    return comps

def get_components(n, edges):
    """Return list of components (each is a list of node indices)."""
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    visited = [False] * n
    components = []
    for i in range(n):
        if not visited[i]:
            comp = []
            stack = [i]
            visited[i] = True
            while stack:
                u = stack.pop()
                comp.append(u)
                for v in adj[u]:
                    if not visited[v]:
                        visited[v] = True
                        stack.append(v)
            components.append(comp)
    return components

if __name__ == "__main__":
    assert connected_components(5, [(0, 1), (1, 2), (3, 4)]) == 2
    assert connected_components(3, [(0, 1), (1, 2), (2, 0)]) == 1
    assert connected_components(4, []) == 4
    comps = get_components(5, [(0, 1), (1, 2), (3, 4)])
    assert len(comps) == 2
    assert sorted(comps[0]) == [0, 1, 2]
    assert sorted(comps[1]) == [3, 4]
    print("connected-components: ALL TESTS PASSED")

```

**PyPy 提示**: 迭代DFS避免递归深度问题。大规模图用邻接表（list of lists）比dict快。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(V+E) |
| 空间 | O(V+E) |

### 局限

仅适用于无向图。有向图的强连通分量需Tarjan/Kosaraju算法。加权图需考虑边权。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| LeetCode | 200 | 4 | 网格图求连通分量数 | [https://leetcode.cn/problems/number-of-islands/](https://leetcode.cn/problems/number-of-islands/) |
| LeetCode | 547 | 3 | 无向图连通分量数 | [https://leetcode.cn/problems/number-of-provinces/](https://leetcode.cn/problems/number-of-provinces/) |
| Luogu | P3916 | 4 | 反向 DFS 求每个点能到达的最大编号 | [https://www.luogu.com.cn/problem/P3916](https://www.luogu.com.cn/problem/P3916) |

## Pitfalls · 易错点

- 无向图建图时每条边需双向加（adj[u].append(v)且adj[v].append(u)）
- DFS递归深度问题，建议用迭代栈
- 孤立节点也是一个连通分量
- 有向图的弱连通分量需将边视为无向

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/connectivity/](https://oi-wiki.org/graph/connectivity/)
- CP-Algorithms ✓ [https://cp-algorithms.com/graph/search-for-connected-components.html](https://cp-algorithms.com/graph/search-for-connected-components.html)
- 书籍 ✓ `CPH ch16 pp159-166`
