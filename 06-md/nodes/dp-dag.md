---
id: dp-dag
name: DAG上的DP
group: G-A-11
stage: intermediate
priority: P1
depth_tier: standard
---

# DAG上的DP

> 有向无环图上的最长/最短路，拓扑序转移

<!-- 元信息: id=dp-dag · group=G-A-11 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

DAG上的DP是在有向无环图(DAG)上求最长路或最短路的动态规划。由于DAG天然无环，节点间的依赖关系定义了一个偏序——按拓扑序处理可保证每个节点的状态在处理前已全部就绪。实际问题中的二元依赖关系（如砖块堆叠、任务调度）可建模为DAG，转化为最长/最短路问题。

## Why · 为什么

### 直觉 · Intuition

DAG没有环，所以从起点到终点的所有路径构成一个偏序结构。按拓扑序处理节点，每个节点的最优值只依赖于「指向它的节点」——这些节点在拓扑序中排在前面，已被处理。这就是DAG上DP无后效性的来源。

### 原理 · Principle

状态定义：d(u)表示从u出发(或到u结束)的最长/短路。转移：d(u)=max{d(v)+w(u,v) | v是u的后继}（最长路）或min同理。处理顺序：按拓扑序（或逆拓扑序）遍历。记忆化搜索也可：DFS(u)时递归处理所有后继v后取最优。时间O(V+E)。

### 历史 · History

DAG上的DP是最自然的DP模型——DP本质上就是在DAG上做最长/短路（如OI Wiki basic页面所述）。巴比伦塔(UVa 437)是经典教学题，将砖块堆叠建模为DAG最长路。关键路径(CPM)调度也是DAG最长路的应用。

## How · 实现

### 伪代码

```python
# 方法1: 记忆化搜索
d(u):
  if d[u] != -inf: return d[u]
  d[u] = 0
  for (v, w) in adj[u]:
    d[u] = max(d[u], d(v) + w)
  return d[u]

# 方法2: 拓扑序递推
toposort(G)  # 得到拓扑序列
for u in reversed(topo):
  for (v, w) in adj[u]:
    d[u] = max(d[u], d[v] + w)
```

### Python 实现

```python
from collections import defaultdict, deque


def dag_longest_path(n, edges, weights=None):
    """DAG最长路 (记忆化搜索)
    n: 节点数 (0-indexed)
    edges: [(u, v), ...] 有向边 u->v
    weights: { (u,v): w } 边权, 默认为1
    返回: (最长路长度, 最长路起点)
    """
    if weights is None:
        weights = {}
    adj = defaultdict(list)
    for u, v in edges:
        w = weights.get((u, v), 1)
        adj[u].append((v, w))

    memo = {}

    def dfs(u):
        if u in memo:
            return memo[u]
        best = 0
        for v, w in adj.get(u, []):
            best = max(best, dfs(v) + w)
        memo[u] = best
        return best

    best_len, best_start = 0, -1
    for u in range(n):
        val = dfs(u)
        if val > best_len:
            best_len = val
            best_start = u
    return best_len, best_start


def dag_longest_path_topo(n, edges, weights=None):
    """DAG最长路 (拓扑排序+递推)"""
    if weights is None:
        weights = {}
    adj = defaultdict(list)
    in_deg = [0] * n
    for u, v in edges:
        w = weights.get((u, v), 1)
        adj[u].append((v, w))
        in_deg[v] += 1

    # Kahn拓扑排序
    q = deque(u for u in range(n) if in_deg[u] == 0)
    topo = []
    while q:
        u = q.popleft()
        topo.append(u)
        for v, w in adj[u]:
            in_deg[v] -= 1
            if in_deg[v] == 0:
                q.append(v)

    # 逆拓扑序求最长路: dist[u] = max over v of (dist[v] + w)
    dist = [0] * n
    for u in reversed(topo):
        for v, w in adj[u]:
            if dist[v] + w > dist[u]:
                dist[u] = dist[v] + w

    return max(dist), dist.index(max(dist))


def babylon_tower(blocks):
    """UVa 437 巴比伦塔: 每种砖块可3种摆放, 求最大堆叠高度
    blocks: [(a, b, c), ...] 各砖块三条边
    返回: 最大塔高
    """
    # 每个砖块拆为3种摆放方式(选不同边为高)
    # 底面取较小边作为长, 较大为宽
    items = []  # (length, width, height)
    for a, b, c in blocks:
        for h, (l, w) in [(a, sorted([b, c])), (b, sorted([a, c])), (c, sorted([a, b]))]:
            items.append((l, w, h))

    n = len(items)
    # 建DAG: i可放在j上, 当j底面严格大于i底面
    adj = defaultdict(list)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if items[i][0] > items[j][0] and items[i][1] > items[j][1]:
                # i底面更大, j可放在i上, 边 i->j, 权=j的高度
                adj[i].append((j, items[j][2]))

    memo = {}
    def dfs(u):
        if u in memo:
            return memo[u]
        best = items[u][2]  # u本身的高度
        for v, w in adj.get(u, []):
            best = max(best, dfs(v) + items[u][2])
        # 注意: 边权应包含u的高度而非v的
        memo[u] = best
        return best

    # 重新计算: d(u) = u为最底时最大高度
    memo.clear()
    def dfs2(u):
        if u in memo:
            return memo[u]
        best = 0  # 上面还能堆多高
        for v, _ in adj.get(u, []):
            if items[u][0] > items[v][0] and items[u][1] > items[v][1]:
                best = max(best, dfs2(v))
        memo[u] = best + items[u][2]  # 加上自身高度
        return memo[u]

    return max(dfs2(i) for i in range(n))


if __name__ == "__main__":
    # DAG最长路测试
    # 0->1->3, 0->2->3, 1->2
    # 0->1(w=1)->3(w=1) = 2
    # 0->2(w=1)->3(w=1) = 2
    # 最长路: 0->1->2->3 = 3 (边(0,1),(1,2),(2,3))
    edges = [(0, 1), (1, 3), (0, 2), (2, 3), (1, 2)]
    weights = {(0,1):1, (1,3):1, (0,2):1, (2,3):1, (1,2):1}
    length, start = dag_longest_path(4, edges, weights)
    assert length == 3, f"Expected 3, got {length}"

    length2, _ = dag_longest_path_topo(4, edges, weights)
    assert length2 == 3, f"Expected 3, got {length2}"

    # 带权DAG: 0->1(w=3)->2(w=4) = 7
    edges2 = [(0, 1), (1, 2)]
    weights2 = {(0,1):3, (1,2):4}
    length3, _ = dag_longest_path(3, edges2, weights2)
    assert length3 == 7, f"Expected 7, got {length3}"

    # 巴比伦塔: 1个砖块(1,1,1) -> 高度1
    assert babylon_tower([(1, 1, 1)]) == 1
    # 2个砖块: (10,10,1)和(5,5,5)
    # 方案1: 块1竖放(h=10,base=1x10) -> 高10
    # 方案2: 块1平放(h=1,base=10x10)+块2(h=5,base=5x5) -> 高6
    # 最优=10
    assert babylon_tower([(10, 10, 1), (5, 5, 5)]) == 10

    print("All tests passed.")

```

**PyPy 提示**: PyPy对记忆化搜索(dict+递归)优化好，V+E=1e6时约0.3s。拓扑排序的Kahn算法用deque高效。注意递归深度需setrecursionlimit。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(V+E) — 每个节点和边各处理一次 |
| 空间 | O(V+E) — 邻接表+记忆化数组 |

### 局限

DAG上DP需保证图确实无环，否则记忆化搜索会死循环。有环时需先用SCC缩点。Python递归深度限制需注意。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| UVa | 437 | 3 | 巴比伦塔：DAG最长路经典题，砖块拆解为3种摆放方式 | [https://onlinejudge.org/external/4/437.pdf](https://onlinejudge.org/external/4/437.pdf) |
| Luogu | P4017 | 2 | 最大食物链计数：DAG上DP计数，拓扑序 | [https://www.luogu.com.cn/problem/P4017](https://www.luogu.com.cn/problem/P4017) |
| Luogu | P1137 | 2 | _STA_旅行计划：DAG最长路，拓扑序递推 | [https://www.luogu.com.cn/problem/P1137](https://www.luogu.com.cn/problem/P1137) |

## Pitfalls · 易错点

- 记忆化搜索前需确认图无环，否则DFS不会终止
- 拓扑序递推时方向：最长路从终点(逆拓扑序)向前推，最短路从起点(拓扑序)向后推
- 巴比伦塔中底面边长需排序(小为大)才能正确判断可堆叠
- 有多个起点时需对所有起点取最优，不能只从一个起点DFS

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/dp/dag/](https://oi-wiki.org/dp/dag/)
- Wikipedia ✓ [https://en.wikipedia.org/wiki/Directed_acyclic_graph](https://en.wikipedia.org/wiki/Directed_acyclic_graph)
