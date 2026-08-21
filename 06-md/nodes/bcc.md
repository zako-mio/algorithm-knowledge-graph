---
id: bcc
name: 双连通分量(BCC)
group: G-B-4
stage: intermediate
priority: P1
depth_tier: deep
---

# 双连通分量(BCC)

> 点双(无割点)/边双(无桥)极大连通子图，Tarjan+栈分解，O(V+E)，点双缩点得圆方树

<!-- 元信息: id=bcc · group=G-B-4 · stage=intermediate · priority=P1 · depth_tier=deep -->

## What · 是什么

双连通分量(Biconnected Component)分为两类：边双连通分量(2-edge-connected component)：任意两点间存在两条边不相交的路径，等价于子图内无桥；点双连通分量(2-vertex-connected component)：任意两点间存在两条点不相交的路径，等价于子图内无割点(孤立点/单边特判)。求法：边双可通过'先求桥再删除桥后DFS'或'Tarjan SCC式'求得；点双用Tarjan+栈，遇到low[v]==dfn[u]时弹栈直到v出栈，u与弹出的点同属一个点双。边双具有传递性而点双没有(两个点双至多共享一个割点)。边双缩点后形成树(桥连接各分量)，点双缩点(圆方树)后也为树结构。复杂度O(V+E)。

## Why · 为什么

### 直觉 · Intuition

无桥的连通块=边双：桥是被'剪断即分离'的边，若一个块内没有这样的边，删任意一条边仍连通，即边双。无割点的块=点双：割点是'删掉即分离'的点，块内没有这样的点，则删任意一个点仍连通。边双之间由桥连接成树，点双之间由割点衔接(圆方树的方点代表点双、圆点代表原图点)。

### 原理 · Principle

边双连通分量求法1：先Tarjan求所有桥，再从每个未被访问的起点DFS，不经过桥的连通块即边双。求法2(等价)：求桥后删桥，余下连通块即边双。点双连通分量求法(Tarjan+栈)：维护一个栈，DFS时把节点压栈；当对子节点v满足low[v]>=dfn[u]时(u为当前节点)，说明u是割点(或根)，此时不断弹栈直到v出栈，u与弹出的这些节点共同构成一个点双连通分量；每次弹栈得到的块即为一个点双。注意：点双中u自己会出现在多个点双中(作为割点)，因此弹栈时u不弹出，只在每个块中把u加入。孤立点单独构成一个点双，单条边构成一个点双。

### 历史 · History

双连通分量理论源于图论中网络可靠性研究(How to make a network robust to node/edge failure)，Tarjan在1972年给出了基于DFS的线性时间算法。OI Wiki的bcc.md和cut.md详细给出边双与点双的多种实现(先求桥再DFS / Tarjan栈 / 差分)，CPH ch17(pp167-172)也覆盖了双连通分量。洛谷P8435(点双)/P8436(边双)为模板题。

## How · 实现

### 伪代码

```python
# 边双(先求桥, 再DFS)
find_bridges()  # Tarjan
vis=set()
for s in V:
  if s not in vis:
    bcc=[]
    dfs_bridge(s):  # 不经过桥的边
      若(u,v)是桥则不跨越
      bcc.append 所有可达点
# 点双(Tarjan+栈)
tarjan(u,parent):
  dfn[u]=low[u]=++timer
  stk.push(u)
  for v in adj[u]:
    if not visited[v]:
      tarjan(v,u)
      low[u]=min(low[u],low[v])
      if low[v]>=dfn[u]:   # u为割点或根
        new_bcc=[]
        while stk.top()!=v:
          new_bcc.append(stk.pop())
        new_bcc.append(stk.pop())
        new_bcc.append(u)
        record(new_bcc)
    elif v!=parent:
      low[u]=min(low[u],dfn[v])
```

### Python 实现

```python
import sys

sys.setrecursionlimit(1 << 25)


def edge_bcc(n, adj):
    """求边双连通分量(边双)。
    adj[u] = [v, ...], 无重边版本
    return: list[list[int]] 每个边双内的顶点集合
    """
    dfn = [0] * n
    low = [0] * n
    timer = [0]
    is_bridge_e = set()

    def dfs_bridge(u, parent):
        dfn[u] = low[u] = timer[0] = timer[0] + 1
        for v in adj[u]:
            if v == parent:
                continue
            if not dfn[v]:
                dfs_bridge(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > dfn[u]:
                    is_bridge_e.add((min(u, v), max(u, v)))
            else:
                low[u] = min(low[u], dfn[v])

    for s in range(n):
        if not dfn[s]:
            dfs_bridge(s, -1)

    vis = [False] * n
    res = []

    def dfs_bcc(u):
        vis[u] = True
        comp = [u]
        for v in adj[u]:
            if (min(u, v), max(u, v)) in is_bridge_e:
                continue
            if not vis[v]:
                comp += dfs_bcc(v)
        return comp

    for s in range(n):
        if not vis[s]:
            res.append(dfs_bcc(s))
    return res


def vertex_bcc(n, adj):
    """求点双连通分量(点双)。
    adj[u] = [v, ...]
    return: (bccs list, 割点集合)
    """
    dfn = [0] * n
    low = [0] * n
    timer = [0]
    is_cut = [False] * n
    stk = []
    bccs = []

    def tarjan(u, parent):
        dfn[u] = low[u] = timer[0] = timer[0] + 1
        stk.append(u)
        child = 0
        for v in adj[u]:
            if not dfn[v]:
                child += 1
                tarjan(v, u)
                low[u] = min(low[u], low[v])
                if low[v] >= dfn[u]:
                    is_cut[u] = parent != -1 or child > 1
                    bcc = []
                    while True:
                        x = stk.pop()
                        bcc.append(x)
                        if x == v:
                            break
                    bcc.append(u)
                    bccs.append(bcc)
            elif v != parent:
                low[u] = min(low[u], dfn[v])

    for s in range(n):
        if not dfn[s]:
            tarjan(s, -1)
    return bccs, [i for i in range(n) if is_cut[i]]


if __name__ == "__main__":
    # 边双: 0-1-2, 2-3-0 环(2-0边), 2-4. 桥: 2-4. 边双: {0,1,2,3} 和 {4}
    adj = [[] for _ in range(5)]
    for u, v in [(0, 1), (1, 2), (2, 0), (2, 3), (3, 0), (2, 4)]:
        adj[u].append(v)
        adj[v].append(u)
    ebcc = edge_bcc(5, adj)
    comps = [tuple(sorted(c)) for c in ebcc]
    assert set(comps) == {(0, 1, 2, 3), (4,)}, comps

    # 点双: 0-1-2-3-0 环 + 2-4, 点双: {0,1,2,3} 和 {2,4}, 割点 {2}
    vbcc, cuts = vertex_bcc(5, adj)
    comps2 = [tuple(sorted(c)) for c in vbcc]
    assert set(comps2) == {(0, 1, 2, 3), (2, 4)}, comps2
    assert cuts == [2], cuts

    # 单边 0-1: 边双各含单点(0,1), 点双 {0,1}
    adj2 = [[] for _ in range(2)]
    adj2[0].append(1); adj2[1].append(0)
    comps3 = [tuple(sorted(c)) for c in edge_bcc(2, adj2)]
    assert set(comps3) == {(0,), (1,)}, comps3
    vbcc2, cuts2 = vertex_bcc(2, adj2)
    assert [tuple(sorted(c)) for c in vbcc2] == [(0, 1)] and cuts2 == [], \
        (vbcc2, cuts2)

    print("bcc: ALL TESTS PASSED")

```

**PyPy 提示**: 点双弹栈逻辑易错，建议先在纸上模拟小环+挂边图。边双的桥集合用tuple(sorted)存便于查重。大规模图仍注意递归栈深。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(V+E) — 一次Tarjan加一次分量划分 |
| 空间 | O(V+E) — 邻接表+栈+dfn/low |

### 局限

点双与边双定义不同：边双有传递性、点双无。点双中一个点(割点)可属于多个点双；边双中一个点只属于一个边双。孤立点与单边需特判。点双缩点后得到圆方树，边双缩点后得到普通树。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P8435 | 3 | 【模板】点双连通分量：Tarjan+栈模板，输出每个点双顶点集合 | [https://www.luogu.com.cn/problem/P8435](https://www.luogu.com.cn/problem/P8435) |
| Luogu | P8436 | 3 | 【模板】边双连通分量：求桥后划分，或Tarjan SCC式 | [https://www.luogu.com.cn/problem/P8436](https://www.luogu.com.cn/problem/P8436) |
| LOJ | 2788 | 5 | CEOI2015管道：受限内存求每个连通块的桥，并查集优化非树边覆盖 | [https://loj.ac/p/2788](https://loj.ac/p/2788) |

## Pitfalls · 易错点

- 点双弹栈时到v为止，u留在栈中(可能属于多个点双)；边双则每个点只属一个分量
- 点双判定用low[v]>=dfn[u]，边双/桥判定用low[v]>dfn[u]，边界值不同
- 孤立点、自环、重边对点双/边双的分量计数有特判要求
- 边双'删桥再DFS'时注意图不连通需对每个起点处理

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/bcc/](https://oi-wiki.org/graph/bcc/)
- OI Wiki ✓ [https://oi-wiki.org/graph/cut/](https://oi-wiki.org/graph/cut/)
- 书籍 ✓ `CPH ch17 pp167-172`
