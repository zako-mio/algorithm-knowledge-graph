---
id: graph-storage
name: 图的存储
group: G-B-1
stage: basic
priority: P0
depth_tier: deep
---

# 图的存储

> 邻接矩阵、邻接表、链式前向星等存图方式

<!-- 元信息: id=graph-storage · group=G-B-1 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

图的存储是图论算法的物理实现基础。常见存图方式包括：(1) 直接存边——用数组存储所有边，适合Kruskal等需排序边的场景；(2) 邻接矩阵——用二维数组adj[u][v]存边，O(1)查询但O(V²)空间，适合稠密图；(3) 邻接表——用vector/list存每个点的出边，O(V+E)遍历，最通用；(4) 链式前向星——用数组模拟链表实现的邻接表，常数小、边有编号，适合网络流。

## Why · 为什么

### 直觉 · Intuition

图算法的效率高度依赖存图方式：遍历图需要快速访问某点的所有出边，Kruskal需要按边权排序，网络流需要快速找到反向边。不同的存储结构在这些操作上有不同优劣，需根据问题选择。

### 原理 · Principle

邻接表: adj[u] 是一个列表，存储 u 的所有出边(终点v, 边权w)。遍历 u 的出边 O(d+(u))，遍历全图 O(V+E)，空间 O(V+E)。Python中用list of list或defaultdict(list)实现。链式前向星: 用三个数组 head[u](u的第一条边编号), to[i](边i的终点), nxt[i](边i的下一条边)。add(u,v): nxt[++cnt]=head[u]; head[u]=cnt; to[cnt]=v。遍历: for i=head[u]; ~i; i=nxt[i]。cnt初值为奇数时 i^1 是反边(网络流用)。

### 历史 · History

图的存储方式与数据结构发展紧密相关。邻接矩阵是最直觉的表示但空间浪费严重。邻接表(vector)成为竞赛C++主流。链式前向星(数组模拟链表)因常数小、支持反边编号而在网络流中被广泛使用。Python竞赛中由于没有指针操作，邻接表(defaultdict(list))是最自然的选择。

## How · 实现

### 伪代码

```python
# 邻接表
adj = [[] for _ in range(n)]
for u, v, w in edges:
    adj[u].append((v, w))

# 链式前向星 (Python数组版)
head = [-1] * (n+1)
to = [0] * (2*m+1)
nxt = [0] * (2*m+1)
cnt = 0
def add(u, v):
    global cnt
    cnt += 1
    nxt[cnt] = head[u]
    head[u] = cnt
    to[cnt] = v

# 遍历 u 的出边
i = head[u]
while i != -1:
    v = to[i]
    # do something with v
    i = nxt[i]
```

### Python 实现

```python
from collections import defaultdict


class AdjListGraph:
    """邻接表存图 (Python最常用方式)
    支持有向/无向, 带权/不带权
    """
    def __init__(self, n, directed=False):
        self.n = n
        self.directed = directed
        self.adj = [[] for _ in range(n)]  # adj[u] = [(v, w), ...]

    def add_edge(self, u, v, w=1):
        self.adj[u].append((v, w))
        if not self.directed:
            self.adj[v].append((u, w))

    def neighbors(self, u):
        return self.adj[u]

    def find_edge(self, u, v):
        for v2, _ in self.adj[u]:
            if v2 == v:
                return True
        return False

    def edge_count(self):
        cnt = sum(len(self.adj[u]) for u in range(self.n))
        return cnt if self.directed else cnt // 2


class ChainForwardStar:
    """链式前向星 (数组模拟链表)
    适合网络流等需要边编号/反边的场景
    """
    def __init__(self, n, max_edges):
        self.n = n
        self.head = [-1] * n
        self.to = [-1] * (max_edges + 1)
        self.nxt = [-1] * (max_edges + 1)
        self.w = [0] * (max_edges + 1)  # 边权
        self.cnt = -1  # 从-1开始, add后变为0,1,2...

    def add_edge(self, u, v, weight=1):
        """添加有向边 u->v"""
        self.cnt += 1
        self.nxt[self.cnt] = self.head[u]
        self.head[u] = self.cnt
        self.to[self.cnt] = v
        self.w[self.cnt] = weight

    def add_edge_undirected(self, u, v, weight=1):
        """添加无向边(两条有向边, cnt为偶数时 i^1 是反边)"""
        self.add_edge(u, v, weight)
        self.add_edge(v, u, weight)

    def neighbors(self, u):
        """遍历 u 的所有出边, 返回 [(edge_id, v, w), ...]"""
        result = []
        i = self.head[u]
        while i != -1:
            result.append((i, self.to[i], self.w[i]))
            i = self.nxt[i]
        return result

    def reverse_edge(self, edge_id):
        """获取反向边编号 (仅当 add_edge_undirected 或成对加边时有效)
        i^1: 偶数边i的反边是i+1, 奇数边i的反边是i-1
        """
        return edge_id ^ 1


if __name__ == "__main__":
    # 邻接表测试
    g = AdjListGraph(4, directed=True)
    g.add_edge(0, 1, 5)
    g.add_edge(0, 2, 3)
    g.add_edge(1, 3, 2)

    assert g.find_edge(0, 1) == True
    assert g.find_edge(1, 0) == False
    assert g.edge_count() == 3
    assert g.neighbors(0) == [(1, 5), (2, 3)]

    # 无向图
    g2 = AdjListGraph(3, directed=False)
    g2.add_edge(0, 1)
    g2.add_edge(1, 2)
    assert g2.edge_count() == 2
    assert g2.find_edge(1, 0) == True

    # 链式前向星测试
    cfs = ChainForwardStar(4, 10)
    cfs.add_edge_undirected(0, 1, 5)
    cfs.add_edge_undirected(1, 2, 3)
    cfs.add_edge_undirected(0, 3, 7)

    # 0 的邻居: 3(权重7) 和 1(权重5)
    nbrs = cfs.neighbors(0)
    assert len(nbrs) == 2
    nbr_set = {(v, w) for _, v, w in nbrs}
    assert nbr_set == {(1, 5), (3, 7)}

    # 反向边: edge 0 和 edge 1 互为反向
    assert cfs.reverse_edge(0) == 1
    assert cfs.reverse_edge(1) == 0

    print("All tests passed.")

```

**PyPy 提示**: PyPy对list of list操作快，邻接表是首选。链式前向星在PyPy中数组访问也快，但Python的list访问有边界检查开销。网络流推荐链式前向星+cnt从0开始成对加边。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 邻接表: 遍历出边 O(d+(u)), 遍历全图 O(V+E); 邻接矩阵: 查边 O(1), 遍历 O(V²) |
| 空间 | 邻接表 O(V+E); 邻接矩阵 O(V²); 链式前向星 O(V+E) |

### 局限

邻接矩阵在V>5000时空间不可承受(O(V²))。Python链式前向星不如C++自然但可用于网络流。无向图用邻接表时每条边存两次，注意不重复计数。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3916 | 1 | 图的遍历：邻接表建图+BFS/DFS，存图与遍历基础练习 | [https://www.luogu.com.cn/problem/P3916](https://www.luogu.com.cn/problem/P3916) |
| CSES | CountingRooms | 1 | 网格图DFS/BFS：邻接表或直接方向数组，连通块计数 | [https://cses.fi/problemset/task/1192](https://cses.fi/problemset/task/1192) |
| Luogu | P3366 | 2 | 最小生成树：Kruskal需直接存边排序，展示直接存边的应用 | [https://www.luogu.com.cn/problem/P3366](https://www.luogu.com.cn/problem/P3366) |

## Pitfalls · 易错点

- 无向图用邻接表时每条边存两次，统计边数需除2
- 链式前向星cnt从0开始成对加边时 i^1 是反边，从1开始则失效
- 邻接矩阵无法处理重边(同一边覆盖)，有重边需用邻接表
- Python递归DFS在n>1000需setrecursionlimit，大图优先BFS

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/save/](https://oi-wiki.org/graph/save/)
- 书籍 ✓ `CPH ch11 pp119-126`
