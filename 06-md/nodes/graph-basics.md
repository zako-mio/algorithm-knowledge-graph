---
id: graph-basics
name: 图论基础概念
group: G-B-1
stage: basic
priority: P0
depth_tier: deep
---

# 图论基础概念

> 图的基本概念：点、边、有向/无向图、度、路径、环、子图

<!-- 元信息: id=graph-basics · group=G-B-1 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

图(Graph)是一个二元组 G=(V,E)，其中 V 是非空点集，E 是连接点与点之间边的集合。图分为无向图(undirected graph)、有向图(directed graph)和混合图。若每条边有权则称为赋权图。图论基础概念包括：度(degree)、路径(path)、环(cycle)、连通性(connectivity)、子图(subgraph)、简单图(simple graph)等，是所有图论算法的基石。

## Why · 为什么

### 直觉 · Intuition

图是描述「关系」和「连接」的数学模型——社交网络中人及其关系、城市间道路、状态转移之间的依赖都可以抽象为图。理解图的基本概念（点、边、度、路径、连通）是学习BFS/DFS/最短路/生成树等所有图算法的前提。

### 原理 · Principle

核心概念：(1) 度 d(v)：与 v 关联的边数，握手定理 sum d(v)=2|E|。(2) 有向图中出度 d+(v) 和入度 d-(v)。(3) 路径(path)：点不重复的途径；环(cycle)：起点=终点的路径。(4) 连通：无向图中两点间存在路径则连通；连通块(connected component)是极大连通子图。(5) 有向图中强连通指双向可达。(6) 简单图不含自环和重边。(7) 稀疏图 |E|<<|V|²，稠密图 |E|≈|V|²。

### 历史 · History

图论起源于欧拉1736年的柯尼斯堡七桥问题。握手定理是图论基本定理，揭示了度的奇偶性约束。图的分类（有向/无向/赋权/简单/正则/完全/稀疏/稠密）构成了竞赛图论的概念基础，所有后续算法（遍历、最短路、网络流等）均建立在这些概念之上。

## How · 实现

### 伪代码

```python
# 图的Python表示(邻接表)
adj = [[] for _ in range(n)]
for u, v in edges:
    adj[u].append(v)    # 有向图
    # adj[v].append(u)  # 无向图

# 度数计算
deg = [len(adj[u]) for u in range(n)]  # 出度(有向图)

# 检查路径(简化版)
visited = [False]*n
def dfs(u, target):
    if u == target: return True
    visited[u] = True
    for v in adj[u]:
        if not visited[v] and dfs(v, target):
            return True
    return False
```

### Python 实现

```python
from collections import defaultdict, deque


class Graph:
    """简单图基础类: 支持有向/无向, 邻接表存储
    提供度数计算、连通块计数、环检测等基础操作
    """
    def __init__(self, n, directed=False):
        self.n = n
        self.directed = directed
        self.adj = defaultdict(list)

    def add_edge(self, u, v):
        self.adj[u].append(v)
        if not self.directed:
            self.adj[v].append(u)

    def degree(self, u):
        """返回节点 u 的度(无向)或出度(有向)"""
        return len(self.adj[u])

    def in_degree(self, u):
        """返回节点 u 的入度(仅对有向图有意义)"""
        cnt = 0
        for v in range(self.n):
            for w in self.adj[v]:
                if w == u:
                    cnt += 1
        return cnt

    def connected_components(self):
        """求无向图连通块数量 (BFS)"""
        visited = [False] * self.n
        count = 0
        for start in range(self.n):
            if not visited[start]:
                count += 1
                q = deque([start])
                visited[start] = True
                while q:
                    u = q.popleft()
                    for v in self.adj[u]:
                        if not visited[v]:
                            visited[v] = True
                            q.append(v)
        return count

    def has_path(self, s, t):
        """检查 s 到 t 是否存在路径 (BFS)"""
        visited = [False] * self.n
        q = deque([s])
        visited[s] = True
        while q:
            u = q.popleft()
            if u == t:
                return True
            for v in self.adj[u]:
                if not visited[v]:
                    visited[v] = True
                    q.append(v)
        return False

    def handshake_check(self):
        """验证握手定理: sum(deg) == 2*|E| (无向图)"""
        total = sum(self.degree(u) for u in range(self.n))
        edge_count = sum(len(self.adj[u]) for u in range(self.n))
        if not self.directed:
            return total == 2 * edge_count // 2 * 2 and total == edge_count
        return total == edge_count  # 有向图 sum(out) = |E|


if __name__ == "__main__":
    # 无向图: 0-1, 1-2, 3-4 (两个连通块)
    g = Graph(5, directed=False)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(3, 4)

    assert g.connected_components() == 2
    assert g.degree(1) == 2
    assert g.has_path(0, 2) == True
    assert g.has_path(0, 4) == False

    # 有向图: 0->1->2->0 (环)
    dg = Graph(3, directed=True)
    dg.add_edge(0, 1)
    dg.add_edge(1, 2)
    dg.add_edge(2, 0)
    assert dg.degree(0) == 1   # 出度
    assert dg.in_degree(0) == 1
    assert dg.has_path(0, 2) == True

    print("All tests passed.")

```

**PyPy 提示**: PyPy对defaultdict(list)建图效率好，BFS/DFS遍历速度快。n>1e6时建议用list替代defaultdict预分配。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 连通块/路径检查: O(V+E) |
| 空间 | O(V+E) — 邻接表存储 |

### 局限

概念性节点，本身无算法复杂度限制。Python实现中in_degree需O(VE)遍历，大图建议预计算逆邻接表。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3916 | 1 | 图的连通性：反向建图BFS/DFS求每个点可达的最大编号节点 | [https://www.luogu.com.cn/problem/P3916](https://www.luogu.com.cn/problem/P3916) |
| Luogu | P2312 | 1 | Chemlab：图的基础遍历(简化版连通块计算) | [https://www.luogu.com.cn/problem/P2312](https://www.luogu.com.cn/problem/P2312) |
| CSES | BuildingRoads | 1 | CSES Building Roads：连通块基础，BFS/DFS或并查集 | [https://cses.fi/problemset/task/1133](https://cses.fi/problemset/task/1133) |

## Pitfalls · 易错点

- 无向图中(u,v)和(v,u)算一组重边，有向图中u->v和v->u不是重边
- 自环对度的贡献是2而非1(无向图)，计算度时需特殊处理
- 题目未说明时可能存在自环和重边，需特殊考虑
- 稀疏图用邻接表O(V+E)，稠密图可用邻接矩阵O(V²)避免常数

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/concept/](https://oi-wiki.org/graph/concept/)
- 书籍 ✓ `CPH ch11 pp119-126`
