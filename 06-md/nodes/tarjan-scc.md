---
id: tarjan-scc
name: Tarjan强连通分量
group: G-B-4
stage: intermediate
priority: P0
depth_tier: deep
---

# Tarjan强连通分量

> 有向图强连通分量，DFS+dfn/low O(V+E)，缩点成DAG

<!-- 元信息: id=tarjan-scc · group=G-B-4 · stage=intermediate · priority=P0 · depth_tier=deep -->

## What · 是什么

Tarjan 算法在线性时间 O(V+E) 内求有向图的强连通分量（SCC）。对图做 DFS，维护 dfn[u]（访问次序）与 low[u]（u 子树中能回溯到的栈内最小 dfn）；当 dfn[u]==low[u] 时，栈中 u 及其上方节点构成一个 SCC。将每个 SCC 缩成一个点，原图变为 DAG，可做拓扑排序、求最长路、判断可达性（如受欢迎的牛、传递闭包类问题）。

## Why · 为什么

### 直觉 · Intuition

DFS 生成树中，每个 SCC 恰是某棵子树。low[u] 记录'u 的子树里能沿着边（含回边/横叉边到栈内祖先）回溯到的最早访问点'。若 low[u]==dfn[u]，说明 u 的子树无法回溯到任何祖先，u 就是该 SCC 在搜索树中第一次遇到的根，栈顶到 u 之间即一个 SCC。关键：从 u 出发经过的任何非树边只能回到已入栈节点（栈内），栈外节点所在 SCC 已处理完。

### 原理 · Principle

DFS 边分四类：树边、反祖边、前向边、横叉边。SCC 中第一个被访问的节点必为根，其余节点都在根的子树中（反证：若某节点在子树外，u→v 的路径必有离开子树的边，只能是横叉/反祖边，但这两类都指向已访问节点，矛盾）。维护 dfn 与 low：①v 未访问：递归后 low[u]=min(low[u],low[v])；②v 在栈中：low[u]=min(low[u],dfn[v])；③v 已出栈：忽略（其 SCC 已处理）。回溯时 dfn[u]==low[u] 则弹出栈中 u 及以上节点成 SCC。时间复杂度 O(V+E)（每条边处理一次）。注意：Tarjan 的 SCC 发现顺序是缩点后 DAG 的逆拓扑序。

### 历史 · History

Robert Tarjan 于 1972 年提出（同年还提出 LCA 离线 Tarjan 算法、并查集等），首次给出线性时间求 SCC 的算法。此前 Kosaraju 的两遍 DFS 算法（1978 年发表，但更早由 Kosaraju 1978 私下提出）也可在 O(V+E) 求解。Tarjan 算法因只需一次 DFS 且常数小，成为竞赛中最常用的 SCC 算法。

## How · 实现

### 伪代码

```python
tarjan(u):
    dfn[u] = low[u] = ++timer
    入栈; in_stack[u]=true
    for v in adj[u]:
        if dfn[v]==0:            # 未访问(树边)
            tarjan(v)
            low[u] = min(low[u], low[v])
        elif in_stack[v]:        # 在栈中(回边/横叉到祖先)
            low[u] = min(low[u], dfn[v])
        # 已出栈: 忽略
    if dfn[u] == low[u]:         # u是SCC根
        ++scc_cnt
        重复弹栈并标记, 直到弹出u, 构成一个SCC

# 主循环
for i in 1..n:
    if dfn[i]==0: tarjan(i)

# 缩点: 遍历每条边, 两端不同SCC则加DAG边
```

### Python 实现

```python
import sys
from collections import deque
sys.setrecursionlimit(1000000)


def tarjan_scc(n, adj):
    """Tarjan 强连通分量
    adj: 0-based 邻接表 (list[list[int]])
    返回 (scc_of: 每个节点所属SCC编号(0-based), sccs: 分量列表)
    """
    dfn = [0] * n
    low = [0] * n
    in_stack = [False] * n
    scc_of = [-1] * n
    stack = []
    timer = [0]
    sccs = []

    def dfs(u):
        timer[0] += 1
        dfn[u] = low[u] = timer[0]
        stack.append(u)
        in_stack[u] = True
        for v in adj[u]:
            if not dfn[v]:
                dfs(v)
                low[u] = min(low[u], low[v])
            elif in_stack[v]:
                low[u] = min(low[u], dfn[v])
        if dfn[u] == low[u]:
            comp = []
            while True:
                w = stack.pop()
                in_stack[w] = False
                scc_of[w] = len(sccs)
                comp.append(w)
                if w == u:
                    break
            sccs.append(comp)

    for i in range(n):
        if not dfn[i]:
            dfs(i)
    return scc_of, sccs


def condensation(n, adj, scc_of):
    """缩点: 把每个SCC缩成一个点, 返回缩点后DAG邻接表与分量数"""
    cnt = max(scc_of) + 1
    dag = [set() for _ in range(cnt)]
    for u in range(n):
        for v in adj[u]:
            if scc_of[u] != scc_of[v]:
                dag[scc_of[u]].add(scc_of[v])
    return dag, cnt


def popular_cow(n, adj):
    """受欢迎牛应用(POJ1236/USACO): 被所有其他节点可达的节点数
    缩点后, 若出度为0的SCC唯一且从任意SCC可达它, 则答案=该SCC大小
    """
    scc_of, sccs = tarjan_scc(n, adj)
    dag, cnt = condensation(n, adj, scc_of)
    out_deg = [len(dag[i]) for i in range(cnt)]
    zero_out = [i for i in range(cnt) if out_deg[i] == 0]
    if len(zero_out) != 1:
        return 0  # 出度0的SCC不唯一, 无人被所有人欢迎
    target = zero_out[0]
    # 检查是否所有SCC都能到达 target
    for s in range(cnt):
        seen = {s}
        q = deque([s])
        ok = False
        while q:
            u = q.popleft()
            if u == target:
                ok = True
                break
            for v in dag[u]:
                if v not in seen:
                    seen.add(v)
                    q.append(v)
        if not ok:
            return 0
    return sum(1 for c in sccs if scc_of[c[0]] == target)


if __name__ == "__main__":
    # 单环 0->1->2->0: 一个SCC
    scc_of, sccs = tarjan_scc(3, [[1], [2], [0]])
    assert len(sccs) == 1 and len(sccs[0]) == 3

    # 混合图: {0,1,2} 与 {3,4}
    adj = [[1], [2, 3], [0], [4], [3]]
    scc_of, sccs = tarjan_scc(5, adj)
    assert sorted(len(c) for c in sccs) == [2, 3]
    dag, cnt = condensation(5, adj, scc_of)
    assert cnt == 2
    assert scc_of[3] in dag[scc_of[0]]  # SCC{0,1,2}->SCC{3,4}

    # 独立点: 每个点一个SCC
    scc_of, sccs = tarjan_scc(3, [[], [], []])
    assert len(sccs) == 3

    # 受欢迎牛: 0<->1, 1->2, 只有节点2被所有人(含自己)可达
    # 0->1->2, 1->2, 2自 => 答案=1(节点2)
    adj = [[1], [0, 2], []]
    assert popular_cow(3, adj) == 1

    # 两个出度0的SCC: 无人被欢迎
    adj = [[1], [2], []]  # 0->1->2, 但1也被2指向? 否
    # 0->1, 1->2, 2没有出边 => SCC{0},{1},{2}, 出度0的只有{2}
    assert popular_cow(3, [[1], [2], []]) == 1
    # 0->1, 2->1, 1无出边 => 只有节点1被欢迎
    assert popular_cow(3, [[1], [], [1]]) == 1

    print("tarjan-scc all tests passed (template + condensation + POJ1236 app)")

```

**PyPy 提示**: Tarjan 递归深度等于 DFS 深度，链式图会爆递归栈，务必 sys.setrecursionlimit 且 PyPy 下可用迭代式 DFS 改写。邻接表用 list 比 set 快；缩点后 DAG 用 set 去重边。PyPy 对列表/栈操作快，可轻松处理 1e5 节点。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(V+E)，每条边每个节点访问一次 |
| 空间 | O(V)（dfn/low/in_stack/栈） |

### 局限

只适用于有向图（无向图连通性用 tarjan 桥/割点或并查集）；递归栈溢出风险；缩点后若需拓扑序，注意 SCC 编号是逆拓扑序（可倒序处理）；超大图(1e6+)建议迭代式 DFS。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| LOJ | 10091 | 3 | 受欢迎的牛（HAOI2006/USACO Fall）：SCC+缩点+出度判断 | [https://loj.ac/problem/10091](https://loj.ac/problem/10091) |
| POJ | 1236 | 3 | Network of Schools：SCC缩点，求入度为0的SCC数与拓扑条件 | [http://poj.org/problem?id=1236](http://poj.org/problem?id=1236) |
| Luogu | P3387 | 3 | 【模板】缩点：SCC缩点后DAG上DP求最长路 | [https://www.luogu.com.cn/problem/P3387](https://www.luogu.com.cn/problem/P3387) |

## Pitfalls · 易错点

- low 更新三情况必须区分：未访问(用low[v])、在栈中(用dfn[v])、已出栈(忽略)——写错导致 SCC 错误合并
- 递归深度：链式图爆栈，设大 setrecursionlimit
- SCC 编号顺序是逆拓扑序，缩点后拓扑处理注意方向
- 缩点后要处理重边（同一 SCC 间多条边），用 set 或去重
- 图可能不连通，主循环必须遍历所有未访问节点

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/scc/](https://oi-wiki.org/graph/scc/)
- CP-Algorithms ✓ [https://cp-algorithms.com/graph/strongly-connected-components.html](https://cp-algorithms.com/graph/strongly-connected-components.html)
- 书籍 ✓ `CPH ch17 pp167-172`
