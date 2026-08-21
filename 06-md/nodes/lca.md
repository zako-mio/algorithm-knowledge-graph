---
id: lca
name: 最近公共祖先(LCA)
group: G-B-7
stage: intermediate
priority: P0
depth_tier: deep
---

# 最近公共祖先(LCA)

> 倍增预处理O(VlogV)查询O(logV)，或Tarjan离线O(α)；欧拉序转RMQ可O(1)查询

<!-- 元信息: id=lca · group=G-B-7 · stage=intermediate · priority=P0 · depth_tier=deep -->

## What · 是什么

LCA(Lowest Common Ancestor)指树上两点 u,v 的所有公共祖先中离根最近的那个。核心应用：树上任意两点距离 d(u,v)=depth[u]+depth[v]-2*depth[lca(u,v)]，因此树上最短路径查询、树上差分、最小生成树/Kruskal重构树、动态树上问题均以 LCA 为基石。主流求法：倍增(在线, O(nlogn)预处理/O(logn)查询)、Tarjan(离线, O(n+m)α)、欧拉序转RMQ(可O(1)查询)。

## Why · 为什么

### 直觉 · Intuition

朴素求法让两点逐步上跳到相遇，最坏 O(n)。倍增的思路是预先把'向上跳 2^i 步到谁'存下来，用二进制把 O(n) 次跳跃压缩成 O(logn) 次。Tarjan 则利用回溯时刻的并查集，把'两个子树的查询'在根节点处一次性合并得到答案，从而离线线性完成。

### 原理 · Principle

倍增：设 up[u][i] 为 u 向上 2^i 层的祖先，up[u][0]=parent[u]，up[u][i]=up[up[u][i-1]][i-1]。查询分两阶段：①把较深点向上跳到与较浅点同深度；②两指针同深度同步向上，从大到小尝试 i，若 up[u][i]!=up[v][i] 则同时上跳，最终 lca=up[u][0]。Tarjan：DFS 过程维护并查集，某结点 u 的子树回溯完成后其并查集根指向 u 的父侧链；处理 u 关联的查询 (u,v) 时若 v 已访问，find(v) 即 lca(u,v)。

### 历史 · History

LCA 问题由 Harel 和 Tarjan 于 1984 年给出 O(n) 预处理 O(1) 查询的经典线性算法。倍增法源自 2000 年代初期竞赛普及的二进制拆分技巧，是 CPH ch18 与 OI Wiki 的标准教学内容；Tarjan 离线算法由 Robert Tarjan 提出，利用并查集的路径压缩与回溯思想，成为离线求 LCA 的标准做法。

## How · 实现

### 伪代码

```python
# 倍增 LCA: 预处理
LOG = ceil(log2(n))
for i in 0..LOG-1:
  for u in 0..n-1:
    up[u][i] = up[up[u][i-1]][i-1]  # 自底向上按 i 递推

# 查询 lca(u, v)
if depth[u] < depth[v]: swap(u, v)
d = depth[u] - depth[v]
for i in 0..LOG-1:
  if d & (1<<i): u = up[u][i]          # 二进制拆分抬升
if u == v: return u
for i in LOG-1..0:
  if up[u][i] != up[v][i]:             # 不同则一起跳
    u = up[u][i]; v = up[v][i]
return up[u][0]

# Tarjan 离线: 每个查询(u,v)在 v 访问完时 find(u) 得答案
```

### Python 实现

```python
import sys
sys.setrecursionlimit(1 << 25)


def lca_binary_lifting(n, edges, queries):
    """倍增在线 LCA。
    edges: (u,v) 无向边; queries: [(u,v), ...]
    返回每个查询的 lca 列表。
    """
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    LOG = (n).bit_length()
    up = [[-1] * LOG for _ in range(n)]
    depth = [0] * n

    # 以 0 为根 DFS 求 parent 与 depth
    stack = [(0, -1, 0)]
    order = []
    while stack:
        u, p, d = stack.pop()
        if p != -1:
            up[u][0] = p
            depth[u] = d
        order.append(u)
        for v in adj[u]:
            if v != p:
                stack.append((v, u, d + 1))
    # 按 BFS/DFS 序正序填 up 表(保证 up[u][i-1] 已就绪)
    # 这里用深度从小到大: 由于父深度<子深度, 直接按 order 中父先于子即可
    up[0][0] = 0
    for u in order:
        for i in range(1, LOG):
            mid = up[u][i - 1]
            up[u][i] = up[mid][i - 1] if mid != -1 else -1

    def query(u, v):
        if depth[u] < depth[v]:
            u, v = v, u
        diff = depth[u] - depth[v]
        i = 0
        while diff:
            if diff & 1:
                u = up[u][i]
            diff >>= 1
            i += 1
        if u == v:
            return u
        for i in range(LOG - 1, -1, -1):
            if up[u][i] != up[v][i]:
                u = up[u][i]
                v = up[v][i]
        return up[u][0]

    return [query(u, v) for u, v in queries]


class DSU:
    def __init__(self, n):
        self.par = list(range(n))

    def find(self, x):
        while self.par[x] != x:
            self.par[x] = self.par[self.par[x]]
            x = self.par[x]
        return x


def lca_tarjan(n, edges, queries):
    """Tarjan 离线 LCA (并查集+回溯)。
    返回查询顺序对应的 lca 列表。
    """
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    qadj = [[] for _ in range(n)]
    for i, (u, v) in enumerate(queries):
        qadj[u].append((v, i))
        qadj[v].append((u, i))

    dsu = DSU(n)
    visited = [False] * n
    ans = [0] * len(queries)

    def dfs(u, parent):
        visited[u] = True
        for v in adj[u]:
            if v != parent and not visited[v]:
                dfs(v, u)
                dsu.par[v] = u  # 子树回溯后并入父节点
        for (v, qi) in qadj[u]:
            if visited[v]:
                ans[qi] = dsu.find(v)

    dfs(0, -1)
    return ans


if __name__ == '__main__':
    # 树: 0-1-2, 1-3, 3-4
    edges = [(0, 1), (1, 2), (1, 3), (3, 4)]
    queries = [(2, 4), (2, 1), (4, 0), (0, 1)]
    a = lca_binary_lifting(5, edges, queries)
    b = lca_tarjan(5, edges, queries)
    assert a == [1, 1, 0, 0], a
    assert b == a, (a, b)

    # 随机对拍: 30 点随机树, 100 查询
    import random
    random.seed(7)
    n = 30
    tedges = []
    for v in range(1, n):
        tedges.append((random.randrange(v), v))
    tqueries = [(random.randrange(n), random.randrange(n)) for _ in range(100)]
    r1 = lca_binary_lifting(n, tedges, tqueries)
    r2 = lca_tarjan(n, tedges, tqueries)
    assert r1 == r2

    print('queries:', queries)
    print('lca     :', a)
    print('Random tree (n=30, q=100): binary lifting == tarjan')
    print('All lca tests passed!')

```

**PyPy 提示**: PyPy 上 Tarjan 离线算法常数较大(并查集+回溯)，倍增在小数据更省时；记忆化 up[u][i] 用 list-of-lists 而非 dict；递归 DFS 在链状树须加大递归上限或改迭代。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 倍增: 预处理 O(N log N), 单次查询 O(log N)；Tarjan: O((N+M) α(N))；欧拉序+ST表: 预处理 O(N log N), 查询 O(1) |
| 空间 | 倍增: O(N log N)；Tarjan: O(N+M) 存查询；欧拉序法: O(N log N) ST表 |

### 局限

倍增空间 O(nlogn) 在 n=2e5 时尚可，更大需树剖(空间 O(n))；Tarjan 为离线算法，交互/在线场景不适用；欧拉序+ST表不支持在线修改(动态树需 LCT)；树上距离公式 d(u,v)=depth[u]+depth[v]-2depth[lca] 仅对边权意义成立，点权需另行处理。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3379 | 3 | 【模板】最近公共祖先: 倍增/Tarjan/树剖均可, 标准板子题 | [https://www.luogu.com.cn/problem/P3379](https://www.luogu.com.cn/problem/P3379) |
| Luogu | P2420 | 2 | 让我们异或吧: 树上边权异或和, 用 d(u,v)=xorSum[u]^xorSum[v] 与LCA无关性技巧 | [https://www.luogu.com.cn/problem/P2420](https://www.luogu.com.cn/problem/P2420) |
| HDU | 2586 | 3 | How far away?: 树上距离=深度差利用LCA, 经典倍增模板 | [https://acm.hdu.edu.cn/showproblem.php?pid=2586](https://acm.hdu.edu.cn/showproblem.php?pid=2586) |

## Pitfalls · 易错点

- 倍增循环上界 i 从大到小, 方向写反会跳过公共祖先或跳到更上层
- 深度差抬升时用 while diff 拆位即可; 若写成遍历所有 i 需注意 & (1<<i) 判断, 别用 >0 误判符号位
- Tarjan 中并查集必须在子树完全回溯后才并入父, 顺序错会得到错误祖先
- 树上距离公式适用于边权; 点权路径和需预处理根到点权前缀再结合 LCA 减除
- 多个查询离线时记得在查询邻接表同时存 u->v 与 v->u, 否则访问顺序会漏答案

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/lca/](https://oi-wiki.org/graph/lca/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/lca.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/lca.md)
- CP-Algorithms ✓ [https://cp-algorithms.com/graph/lca_binary_lifting.html](https://cp-algorithms.com/graph/lca_binary_lifting.html)
- 书籍 ✓ `CPH ch18 pp.173-182`
