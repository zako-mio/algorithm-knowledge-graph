---
id: tree-basics
name: 树基础
group: G-B-7
stage: basic
priority: P0
depth_tier: deep
---

# 树基础

> 树的基本概念：根、叶、深度、子树、父亲；无根树/有根树定义，邻接表/父数组存储，DFS/BFS 遍历

<!-- 元信息: id=tree-basics · group=G-B-7 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

树是无圈连通无向图，n 个结点 n-1 条边，任意两点间有且仅有一条简单路径。树是图论、DP、数据结构(线段树/平衡树)、LCA、直径、重心、树剖等一系列算法的基础载体。需要掌握：无根树与有根树的等价定义、叶/深度/高度/子树/祖先等术语、邻接表/父数组/左孩子右兄弟等存储方式、树上 DFS/BFS 遍历（含求深度与父亲）。

## Why · 为什么

### 直觉 · Intuition

树是一种'处处唯一路径'的图，信息传播没有分叉闭环，因此遍历一次即可把整棵树信息（深度、父亲、子树大小、子树信息聚合）收集全。几乎所有树算法都建立在'深度+父亲+子树'三件套之上，后续的直径、LCA、树剖、DP 都是在其上叠加技巧。

### 原理 · Principle

无根树：指定任意一个结点为根即得根节点，遍历时记录每个结点的父亲(parent)与深度(depth=根到该点边数)。邻接表存储：对无向输入，从根出发 DFS，用 from 参数避免回走父结点即可区分父子关系。树遍历的核心性质：n 个结点 n-1 条边，因此 DFS/BFS 均为 O(n)，不会重复访问。常用三种存储：父数组(自底向上递推)、邻接表(通用)、左孩子右兄弟(节省内存的变种)。

### 历史 · History

树论是图论最古老的分支之一。Cayley(1889)证明了 n 个结点的标号树有 n^(n-2) 棵。竞赛中树作为'可递归处理的连通图'进入问题体系，OI Wiki 将其列为图论基础第一页；CPH(Competitive Programmer's Handbook)ch14 也以树遍历作为起点，树上 DP、LCA、直径、重心全部建立在树基础之上。

## How · 实现

### 伪代码

```python
# 无根树转有根树 + 求深度(DFS)
def dfs(u, from_):
  for v in adj[u]:
    if v == from_: continue
    parent[v] = u
    depth[v] = depth[u] + 1
    dfs(v, u)

dfs(root, -1)

# BFS 层序遍历(区分层次)
q = [root]
while q:
  cur = q.pop(0)  # 用 collections.deque 更优
  for v in adj[cur]:
    if v == parent[cur]: continue
    parent[v] = cur; depth[v] = depth[cur] + 1
    q.append(v)
```

### Python 实现

```python
from collections import deque


def build_tree(n, edges, root=0):
    """由无向边列表建邻接表。
    返回 adj, parent, depth, order(dfs序)。
    """
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    parent = [-1] * n
    depth = [0] * n
    order = []

    def dfs(u, from_):
        order.append(u)
        for v in adj[u]:
            if v == from_:
                continue
            parent[v] = u
            depth[v] = depth[u] + 1
            dfs(v, u)

    dfs(root, -1)
    return adj, parent, depth, order


def subtree_sizes(parent, order):
    """自底向上(逆dfs序)求子树大小。
    每个结点初始大小1，逆序累加到父亲。
    """
    size = [1] * len(parent)
    for u in reversed(order[1:]):
        size[parent[u]] += size[u]
    return size


def bfs_levels(adj, root, parent):
    """BFS 层序遍历，返回 [[第0层], [第1层], ...]。"""
    levels = []
    dq = deque([root])
    while dq:
        level = []
        for _ in range(len(dq)):
            u = dq.popleft()
            level.append(u)
            for v in adj[u]:
                if v != parent[u]:
                    dq.append(v)
        levels.append(level)
    return levels


if __name__ == '__main__':
    # 0-1-2, 1-3, 1-4  即一棵有5个结点的树
    edges = [(0, 1), (1, 2), (1, 3), (1, 4)]
    adj, parent, depth, order = build_tree(5, edges, root=0)
    assert order == [0, 1, 2, 3, 4], order
    assert parent == [-1, 0, 1, 1, 1], parent
    assert depth == [0, 1, 2, 2, 2], depth
    assert sum(1 for x in parent[1:] if x != -1) == 4  # 4条边

    size = subtree_sizes(parent, order)
    assert size[1] == 4, size   # 子树1含 {1,2,3,4}
    assert size[0] == 5, size

    levels = bfs_levels(adj, 0, parent)
    assert levels == [[0], [1], [2, 3, 4]], levels
    assert all(len(level) >= 1 for level in levels)

    print('DFS order:', order)
    print('parent   :', parent)
    print('depth    :', depth)
    print('subtree  :', size)
    print('BFS levels:', levels)
    print('All tree-basics tests passed!')

```

**PyPy 提示**: PyPy 递归深度默认较小，树上 DFS 用递归在链状树(深度可达 10^5)时易栈溢出，建议 sys.setrecursionlimit(1 << 25) 或用显式栈迭代；BFS 用 collections.deque 而非 list.pop(0)(O(n) 弹出)。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(N) — 遍历/建树/求深度与父亲均为 O(N)，每条边恰访问两次 |
| 空间 | O(N) — 邻接表 O(N)，DFS 栈深度 O(N) 最坏 |

### 局限

递归 DFS 在链状大树上有栈溢出风险；无根树的'根'是任选的，不同根不影响直径/重心等结构量但会影响深度与父子关系；邻接矩阵存储稀疏树浪费空间，应优先邻接表。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| LeetCode | 104 | 1 | 二叉树深度: 树遍历基础，递归 max(左,右)+1 | [https://leetcode.cn/problems/maximum-depth-of-binary-tree/](https://leetcode.cn/problems/maximum-depth-of-binary-tree/) |
| LeetCode | 144 | 1 | 前序遍历: 根左右, 二叉树三种遍历的基础 | [https://leetcode.cn/problems/binary-tree-preorder-traversal/](https://leetcode.cn/problems/binary-tree-preorder-traversal/) |
| Luogu | P1305 | 2 | 前序遍历: 输入父子关系建树后按根左右输出 | [https://www.luogu.com.cn/problem/P1305](https://www.luogu.com.cn/problem/P1305) |

## Pitfalls · 易错点

- 递归 DFS 不设递归上限，链状树深度 10^5 时 Python 直接 RecursionError
- 遍历时忘记排除 from/父亲结点，会在无向树上死循环
- 叶子定义不同：无根树叶=度数≤1(单点树根也是叶)，有根树叶=无子结点，两者在 n=1 时不一致
- '满二叉树'在中文语境多指完美二叉树，不同教材定义不同，读题需谨慎

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/tree-basic/](https://oi-wiki.org/graph/tree-basic/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/tree-basic.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/tree-basic.md)
- 书籍 ✓ `CPH ch14 Tree algorithms, pp.143-150`
