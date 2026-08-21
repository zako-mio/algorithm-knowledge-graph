---
id: dominator-tree
name: 支配树
group: G-B-4
stage: advanced
priority: P2
depth_tier: standard
---

# 支配树

> 有向图支配关系树：Lengauer-Tarjan算法O((V+E)α)，DAG/树有特例O((V+E)log)解法

<!-- 元信息: id=dominator-tree · group=G-B-4 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

支配树(Dominator Tree)用于描述有向图中'从入口s出发到某点的所有路径都必须经过哪些点'的支配关系。若从s到u的每条路径都经过v，则称v支配u。支配关系满足树形结构：每个节点(除s外)恰有一个直接支配者idom(u)，把所有idom边连起来就得到以s为根的支配树。在支配树上，v支配u当且仅当v是u的祖先。求解支配树的经典算法是Lengauer-Tarjan算法，复杂度O((E+V)α(V))，通过半支配点(semi-dominator)间接求直接支配者。对DAG有更简单的拓扑序+倍增LCA解法，对树则支配树就是它本身。典型应用：ZJOI2012灾难(灭绝树)、程序控制流图分析、统计每个点被哪些点必经支配。

## Why · 为什么

### 直觉 · Intuition

想弄清'哪些点支配了哪些点'，最朴素是删除每个点再DFS(O(n³))，或用数据流方程迭代(O(n²))。支配树把'支配'关系压成一颗树：树上祖先即支配者。Lengauer-Tarjan的核心是半支配点——一个略弱于直接支配者、但更容易算的量：sdom(u)是'从某个节点出发经一条路径(中间节点dfn都大于u)能走到u的节点中dfn最小者'。算出sdom后再通过一条修正公式得到idom，复杂度降至近线性。

### 原理 · Principle

算法分三阶段：(1)从s对原图DFS，得到DFS树T和dfn编号；(2)按dfn从大到小，利用带权并查集计算每个节点的半支配点sdom(u)=min(前驱中dfn<dfn[u]的节点, 满足w>u且存在w→…→v→u路径的sdom(w))；(3)根据定理：令v为sdom(u)到u的路径上sdom最小的节点，则idom(u)=sdom(u)(当sdom(u)=sdom(v))否则idom(u)=idom(v)，通过第二次带权并查集扫描得到所有idom。带权并查集每次find时维护'路径上sdom最小的节点'即可O((E+V)α)。DAG特例：按拓扑序处理，u的idom是其所有前驱在支配树上的LCA(倍增维护)，复杂度O((E+V)log)。

### 历史 · History

支配概念1959年由Prosser在网络流论文中提出，1969年Lowry与Medlock给出首个有效算法，1979年Lengauer与Tarjan发表近线性算法，至今仍是编译器控制流分析与工业软件领域的重要工具。竞赛界最早通过ZJOI2012灾难(灭绝树)引入该概念，OI Wiki的dominator-tree页有完整介绍；CP-Algorithms目前无此条目。

## How · 实现

### 伪代码

```python
# Lengauer-Tarjan 框架
dfs(s):   # 建DFS树, 记录dfn/pos/fth
  dfn[u]=++dfc; pos[dfc]=u
  for v in out[u]: if not dfn[v]: dfs(v); fth[v]=u

# 带权并查集 find(x): 返回sdm最小的节点mn[x]
# 阶段1: 算sdm (按dfc从大到小)
for i in dfc..2:
  u=pos[i]
  res=dfn[u]
  for v in in[u]:            # 入边
    if dfn[v]==0: continue
    find(v)
    if dfn[v]<dfn[u]: res=min(res, dfn[v])
    else: res=min(res, dfn[sdm[mn[v]]])
  sdm[u]=pos[res]
  fa[u]=fth[u]               # 并查集挂到父节点
  # 阶段2(内联): 对挂在sdm[u]下的v: idom[v]=sdm[v]或mn[v]
# 阶段3: 修正
for i in 2..dfc:
  u=pos[i]
  if idom[u]!=sdm[u]: idom[u]=idom[idom[u]]
# 支配树边: (idom[u], u)
```

### Python 实现

```python
# DAG上的支配树: 拓扑序+倍增LCA (P2597灾难的解法)
import sys
from collections import deque

sys.setrecursionlimit(1 << 25)


def dominator_tree_dag(n, s, edges):
    """DAG的支配树.
    n: 节点数, s: 唯一入口(1-based), edges: [(u,v),...]
    返回: idom数组(1-based, idom[s]=s), 支配树上父节点
    """
    g = [[] for _ in range(n + 1)]
    rg = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for u, v in edges:
        g[u].append(v)
        rg[v].append(u)
        indeg[v] += 1

    # 拓扑序
    q = deque([s])
    topo = []
    indeg_saved = indeg[:]
    while q:
        u = q.popleft()
        topo.append(u)
        for v in g[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    LOG = (n + 1).bit_length()
    up = [[0] * (n + 1) for _ in range(LOG)]  # 支配树倍增祖先
    dep = [0] * (n + 1)
    idom = [0] * (n + 1)
    idom[s] = s

    def lca(u, v):
        if dep[u] < dep[v]:
            u, v = v, u
        d = dep[u] - dep[v]
        k = 0
        while d:
            if d & 1:
                u = up[k][u]
            d >>= 1
            k += 1
        if u == v:
            return u
        for k in range(LOG - 1, -1, -1):
            if up[k][u] != up[k][v]:
                u = up[k][u]
                v = up[k][v]
        return up[0][u]

    # 按拓扑序: idom[u] = 所有前驱在支配树上的LCA
    for u in topo:
        if u == s:
            continue
        if not rg[u]:
            continue
        anc = rg[u][0]
        for v in rg[u][1:]:
            anc = lca(anc, v)
        idom[u] = anc
        up[0][u] = anc
        dep[u] = dep[anc] + 1
        for k in range(1, LOG):
            up[k][u] = up[k - 1][up[k - 1][u]]
    return idom


if __name__ == "__main__":
    # 测试DAG: s=1, 1->2, 1->3, 2->4, 3->4, 4->5
    # 支配: 1支配全部; 4支配5; idom: 2<-1,3<-1,4<-1,5<-4
    edges = [(1, 2), (1, 3), (2, 4), (3, 4), (4, 5)]
    idom = dominator_tree_dag(5, 1, edges)
    assert idom[1:] == [1, 1, 1, 1, 4], idom

    # 测试链: 1->2->3->4, idom为直接前驱
    edges2 = [(1, 2), (2, 3), (3, 4)]
    idom2 = dominator_tree_dag(4, 1, edges2)
    assert idom2[1:] == [1, 1, 2, 3], idom2

    # 测试分支再汇合: 1->2,1->3,2->4,3->4, 4的前驱2,3的LCA=1
    edges3 = [(1, 2), (1, 3), (2, 4), (3, 4)]
    idom3 = dominator_tree_dag(4, 1, edges3)
    assert idom3[1:] == [1, 1, 1, 1], idom3

    print("dominator-tree(DAG): ALL TESTS PASSED")

```

**PyPy 提示**: Lengauer-Tarjan的带权并查集需在find时维护'半支配点最小'的节点，Python递归find易栈溢出，建议迭代或提升递归限制；竞赛中P5180/P2597多用C++。DAG特例用倍增LCA较Python友好。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | Lengauer-Tarjan: O((E+V)α(V))；结点删除法O(V(V+E))；DAG特例O((E+V)logV) |
| 空间 | O(V+E) — 原图+反图+DFS树+并查集 |

### 局限

仅对单入口(唯一s)的有向图定义支配树；多个起点需先建超级源点。算法细节多、易错，Python实现带权并查集性能敏感。OI中竞赛题少但ZJOI2012灾难为代表题。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P2597 | 5 | ZJOI2012灾难(灭绝树)：DAG上建支配树求子树size，首次将支配树引入OI的题 | [https://www.luogu.com.cn/problem/P2597](https://www.luogu.com.cn/problem/P2597) |
| Luogu | P5180 | 6 | 【模板】支配树：一般有向图，需Lengauer-Tarjan | [https://www.luogu.com.cn/problem/P5180](https://www.luogu.com.cn/problem/P5180) |

## Pitfalls · 易错点

- 支配树要求唯一入口，多入口需虚拟超级源点处理
- sdom与idom的修正公式容易记错：先算sdom, 再通过路径上sdom最小节点v判断idom=sdom(u)或idom(v)
- 带权并查集find的路径压缩必须维护mn(半支配点最小节点), 不是只维护并查集根
- DAG特例中所有前驱的LCA即为idom，但前提是DAG连通且单源
- 图不连通时，无法到达的节点没有支配关系，需单独讨论

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/dominator-tree/](https://oi-wiki.org/graph/dominator-tree/)
- Wikipedia ✓ [https://en.wikipedia.org/wiki/Dominator_(graph_theory)](https://en.wikipedia.org/wiki/Dominator_(graph_theory))
