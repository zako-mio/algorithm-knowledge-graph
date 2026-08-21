---
id: bridge
name: 割边(桥)
group: G-B-4
stage: intermediate
priority: P1
depth_tier: deep
---

# 割边(桥)

> 删除后使图不连通的边，Tarjan判定low[v]>dfn[u]得桥O(V+E)，有重边需按边编号处理

<!-- 元信息: id=bridge · group=G-B-4 · stage=intermediate · priority=P1 · depth_tier=deep -->

## What · 是什么

割边(桥/bridge)是删除后使无向图连通分量数增加的边。判定与割点高度相似，同样用Tarjan的dfn/low数组：对于DFS树边u-v(v为u的子节点)，若low[v]>dfn[u]，则u-v是桥。因为v的子树除了经过u-v这条边，没有任何路径能到达u及其祖先。时间复杂度O(V+E)。在有重边的图中，直接跳过父节点会误判：两条重边之间本不构成桥，需改为记录'来时的边的编号'，只跳过同一条边而不跳过父节点。桥是边双连通分量的边界，求桥后去掉桥即可分解出边双连通分量。

## Why · 为什么

### 直觉 · Intuition

low[v]>dfn[u]意味着v子树的所有节点中最高的'逃生天桥'都在u之下，即v子树完全被u-v这条边'锁住'。只要剪断这条边，v子树就与外界完全隔离，所以u-v是桥。若low[v]<=dfn[u]，说明v子树能通过返祖边绕到u或u的祖先，存在替代路径，u-v不是桥。

### 原理 · Principle

算法流程：(1)DFS，dfn[u]为时间戳，low[u]初始化=dfn[u]；(2)树边v：low[u]=min(low[u],low[v])；返祖边v(非来时边)：low[u]=min(low[u],dfn[v])；(3)树边u-v若满足low[v]>dfn[u]则为桥。无重边时可用parent标记跳过父节点；有重边时必须改为记录每条边的编号(edge id)，DFS参数传递'来时边的编号'，只跳过同一条编号的边，这样另一条重边会作为返祖边被正常处理，从而正确判定不构成桥。桥的判定不需要像割点那样特判根节点。

### 历史 · History

桥的概念是图论中割集理论的基本对象，Tarjan的DFS算法(1972)将dfn/low体系扩展到割边求解。OI Wiki的cut.md与CP-Algorithms的bridge-searching页均提供标准实现，并明确警告无重边版本在有重边图上的错误，给出按边编号的处理。CPH ch17(pp167-172)亦有介绍。

## How · 实现

### 伪代码

```python
# 无重边版
tarjan(u, parent):
  dfn[u]=low[u]=++timer
  for v in adj[u]:
    if not visited[v]:
      tarjan(v,u)
      low[u]=min(low[u],low[v])
      if low[v]>dfn[u]: is_bridge[(u,v)]=True
    elif v!=parent:
      low[u]=min(low[u],dfn[v])

# 有重边版: 记录边编号, 只跳过来时边
tarjan(u, eid):  # eid为进入u时所经过边的编号
  dfn[u]=low[u]=++timer
  for (v,id) in adj[u]:
    if id==eid: continue
    if not visited[v]:
      tarjan(v,id)
      low[u]=min(low[u],low[v])
      if low[v]>dfn[u]: is_bridge[id]=True
    else:
      low[u]=min(low[u],dfn[v])
```

### Python 实现

```python
import sys

sys.setrecursionlimit(1 << 25)


def find_bridges(n, adj):
    """求无向图所有桥(含重边安全版本).
    adj[u] = [(v, edge_id), ...]
    return: 桥的边编号list
    """
    dfn = [0] * n
    low = [0] * n
    is_bridge = [False] * (len(sum(adj, [])) // 2 + 1)
    timer = [0]

    def dfs(u, parent_edge):
        dfn[u] = low[u] = timer[0] = timer[0] + 1
        for v, eid in adj[u]:
            if eid == parent_edge:
                continue
            if not dfn[v]:
                dfs(v, eid)
                low[u] = min(low[u], low[v])
                if low[v] > dfn[u]:
                    is_bridge[eid] = True
            else:
                low[u] = min(low[u], dfn[v])

    for s in range(n):
        if not dfn[s]:
            dfs(s, -1)
    return [eid for eid, b in enumerate(is_bridge) if b]


if __name__ == "__main__":
    # 测试1: 链 0-1-2-3, 所有边都是桥
    adj = [[] for _ in range(4)]
    eid = 0
    for u, v in [(0, 1), (1, 2), (2, 3)]:
        adj[u].append((v, eid))
        adj[v].append((u, eid))
        eid += 1
    assert find_bridges(4, adj) == [0, 1, 2], find_bridges(4, adj)

    # 测试2: 带环图, 仅环外挂边为桥
    # 0-1-2-3-0 环 + 2-4, 桥只有 2-4 (编号最后一条)
    adj2 = [[] for _ in range(5)]
    eid = 0
    for u, v in [(0, 1), (1, 2), (2, 3), (3, 0), (2, 4)]:
        adj2[u].append((v, eid))
        adj2[v].append((u, eid))
        eid += 1
    assert find_bridges(5, adj2) == [4], find_bridges(5, adj2)

    # 测试3: 重边: 0-1两条重边, 无桥
    adj3 = [[] for _ in range(2)]
    adj3[0].append((1, 0)); adj3[1].append((0, 0))
    adj3[0].append((1, 1)); adj3[1].append((0, 1))
    assert find_bridges(2, adj3) == [], find_bridges(2, adj3)

    # 测试4: 单边 0-1, 该边是桥
    adj4 = [[] for _ in range(2)]
    adj4[0].append((1, 0)); adj4[1].append((0, 0))
    assert find_bridges(2, adj4) == [0], find_bridges(2, adj4)

    print("bridge: ALL TESTS PASSED")

```

**PyPy 提示**: 与割点同理，需setrecursionlimit；大规模图(n>2e5)优先考虑迭代DFS或C++实现。邻接表存(邻居,边编号)元组，内存约为无编号版的两倍，注意数组大小。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(V+E) — 每个点/边各访问一次 |
| 空间 | O(V+E) — 邻接表 + dfn/low + 递归栈 |

### 局限

无重边版本在有重边图上会误判重边为桥，必须使用边编号版本。桥判定对根节点无特殊要求(不同于割点)。断桥后DFS可得到边双连通分量。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1656 | 3 | 炸铁路：求所有桥的裸题，注意输出按字典序 | [https://www.luogu.com.cn/problem/P1656](https://www.luogu.com.cn/problem/P1656) |
| HDU | 4738 | 4 | Caocao's Bridges：桥+最小权边，且有重边(用边编号)与全图已连通的特判 | [https://acm.hdu.edu.cn/showproblem.php?pid=4738](https://acm.hdu.edu.cn/showproblem.php?pid=4738) |
| HDU | 2460 | 4 | Network：动态加边后桥的数量，用LCA+缩点维护 | [https://acm.hdu.edu.cn/showproblem.php?pid=2460](https://acm.hdu.edu.cn/showproblem.php?pid=2460) |

## Pitfalls · 易错点

- 有重边时必须用边编号而非父节点标记，否则两条重边会被误判为桥
- 返祖边用dfn[v]更新low，树边用low[v]更新，二者不可混淆
- 割边判定条件为严格大于(>)而非>=：low[v]==dfn[u]意味着能绕回u，不是桥
- 桥判定不需要特判根节点(割点才需要)

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/cut/](https://oi-wiki.org/graph/cut/)
- CP-Algorithms ✓ [https://cp-algorithms.com/graph/bridge-searching.html](https://cp-algorithms.com/graph/bridge-searching.html)
- 书籍 ✓ `CPH ch17 pp167-172`
