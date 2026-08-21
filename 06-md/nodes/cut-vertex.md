---
id: cut-vertex
name: 割点(关节点)
group: G-B-4
stage: intermediate
priority: P1
depth_tier: deep
---

# 割点(关节点)

> 删除后使图极大连通分量数增加的点，Tarjan(dfn/low)判定O(V+E)，根节点需特判子节点数

<!-- 元信息: id=cut-vertex · group=G-B-4 · stage=intermediate · priority=P1 · depth_tier=deep -->

## What · 是什么

割点(articulation point / cut vertex)是删除后使无向图极大连通分量数增加的点。朴素做法是枚举每个点删除后跑一遍DFS判连通性，复杂度O(V(V+E))。Tarjan算法在DFS过程中维护dfn(DFS序)和low(不经过父边能到达的最小dfn)，在O(V+E)内一次DFS求出所有割点。判定条件：对于非根节点u，若存在子节点v使得low[v]>=dfn[u]，则u是割点；对于根节点，若在DFS生成树中有两个及以上子节点，则根是割点。该算法是割点/桥/双连通分量/圆方树等系列结构的基础。

## Why · 为什么

### 直觉 · Intuition

如果从u的子节点v的子树出发，只能回到v本身或其祖先之下，即low[v]>=dfn[u]，说明v所在的子树无法通过其他路径绕回u的祖先，那么一旦删掉u，v的整个子树就与u之上的部分分离，连通分量数必然增加，所以u是割点。low就像是'每个子树能找到的最高的逃生天桥'，找不到通往祖先的路，就说明u是关键枢纽。

### 原理 · Principle

Tarjan算法过程：(1)DFS遍历，dfn[u]记录访问时间戳；(2)low[u]初始化为dfn[u]，对树边v：low[u]=min(low[u],low[v])，对非树边(返祖边)v(且v≠父节点)：low[u]=min(low[u],dfn[v])；(3)非根节点u是割点当且仅当存在子节点v满足low[v]>=dfn[u]；(4)根节点是割点当且仅当DFS树中它有两个及以上子节点（若从根只搜出一个子树，删根不增加分量数，如一个环）。注意需使用递归DFS而非迭代，且在无向图上需用边的编号或父节点标记区分返祖边与父边。

### 历史 · History

割点概念与DFS生成树理论源于图论中图连通性的研究，Tarjan在1972年提出的DFS深度优先搜索框架以及基于dfn/low的算法至今仍是求割点/桥/强连通分量的标准方法。OI Wiki的cut.md与CP-Algorithms的cutpoints页均给出标准Tarjan实现，CPH第17章(pp167-172)也介绍了该思路。

## How · 实现

### 伪代码

```python
tarjan(u, parent):
  dfn[u] = low[u] = ++timer
  child_count = 0
  for v in adj[u]:
    if not visited[v]:
      child_count += 1
      tarjan(v, u)
      low[u] = min(low[u], low[v])
      if parent != root and low[v] >= dfn[u]:
        is_cut[u] = True
      # 根节点判断在循环外: if parent==root and child_count>=2: is_cut[u]=True
    elif v != parent:
      low[u] = min(low[u], dfn[v])
```

### Python 实现

```python
import sys

sys.setrecursionlimit(1 << 25)


def find_cut_vertices(n, adj):
    """求无向图所有割点。
    adj[u] = [v, ...], 顶点编号 0..n-1
    return: 割点集合(升序list)
    """
    dfn = [0] * n
    low = [0] * n
    is_cut = [False] * n
    timer = [0]

    def dfs(u, parent):
        dfn[u] = low[u] = timer[0] = timer[0] + 1
        child = 0
        for v in adj[u]:
            if not dfn[v]:
                child += 1
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if parent != -1 and low[v] >= dfn[u]:
                    is_cut[u] = True
            elif v != parent:
                low[u] = min(low[u], dfn[v])
        if parent == -1 and child >= 2:
            is_cut[u] = True

    for s in range(n):
        if not dfn[s]:
            dfs(s, -1)
    return [i for i in range(n) if is_cut[i]]


if __name__ == "__main__":
    # 测试1: OI Wiki示例, 割点为2
    # 0-1-2-3, 2-4, 2-5, 4-6(环), 5-6  => 割点应为 {1, 2}
    adj = [[] for _ in range(7)]
    edges = [(0, 1), (1, 2), (2, 3), (2, 4), (2, 5), (4, 6), (5, 6)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    assert find_cut_vertices(7, adj) == [1, 2], find_cut_vertices(7, adj)

    # 测试2: 单个环, 无割点
    adj2 = [[] for _ in range(4)]
    for u, v in [(0, 1), (1, 2), (2, 3), (3, 0)]:
        adj2[u].append(v)
        adj2[v].append(u)
    assert find_cut_vertices(4, adj2) == [], find_cut_vertices(4, adj2)

    # 测试3: 简单链 0-1-2, 1为割点
    adj3 = [[] for _ in range(3)]
    for u, v in [(0, 1), (1, 2)]:
        adj3[u].append(v)
        adj3[v].append(u)
    assert find_cut_vertices(3, adj3) == [1], find_cut_vertices(3, adj3)

    # 测试4: 根节点为割点: 星形 0-1,0-2,0-3, 0为根且多子树
    adj4 = [[] for _ in range(4)]
    for v in (1, 2, 3):
        adj4[0].append(v)
        adj4[v].append(0)
    assert find_cut_vertices(4, adj4) == [0], find_cut_vertices(4, adj4)

    print("cut-vertex: ALL TESTS PASSED")

```

**PyPy 提示**: PyPy递归较慢且默认栈有限，n在1e5~2e5时建议显式sys.setrecursionlimit(1<<25)；若仍栈溢出，可手动维护栈模拟DFS(记录进入/回溯事件)。Python默认递归深度限制约1000，务必先提高。邻接表用list of list即可。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(V+E) — 每个点/边各访问一次 |
| 空间 | O(V+E) — 邻接表 + dfn/low数组 + 递归栈 |

### 局限

Tarjan割点判定基于DFS树，适用于任意无向图(含重边不影响割点判定，但割边/桥判定需区分重边)。Python递归版本可能栈溢出，大规模图需迭代实现。多连通分量的图需对每个起点独立跑DFS。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3388 | 3 | 【模板】割点(割顶)：直接套Tarjan，需特判根节点 | [https://www.luogu.com.cn/problem/P3388](https://www.luogu.com.cn/problem/P3388) |
| POJ | 2117 | 3 | Electricity：求删除一点后最大连通分量数，需统计各连通块的子节点数 | [http://poj.org/problem?id=2117](http://poj.org/problem?id=2117) |
| POJ | 1523 | 3 | SPF：经典割点题，输出每个割点删除后增加的分量数 | [http://poj.org/problem?id=1523](http://poj.org/problem?id=1523) |

## Pitfalls · 易错点

- 根节点割点判定条件不同：必须有>=2个DFS子树才算割点，单子树根删除不增加分量
- 返祖边更新low时用dfn[v]而非low[v]，且必须跳过父节点(无重边时)以免误判
- Python递归默认栈深~1000，需setrecursionlimit，大图考虑迭代栈
- 无向图建边要双向add，漏了会导致图不完整误判

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/cut/](https://oi-wiki.org/graph/cut/)
- CP-Algorithms ✓ [https://cp-algorithms.com/graph/cutpoints.html](https://cp-algorithms.com/graph/cutpoints.html)
- 书籍 ✓ `CPH ch17 pp167-172`
