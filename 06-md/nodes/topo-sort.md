---
id: topo-sort
name: 拓扑排序
group: G-B-1
stage: basic
priority: P0
depth_tier: deep
---

# 拓扑排序

> DAG节点线性排序，Kahn算法(入度BFS)或DFS逆序O(V+E)

<!-- 元信息: id=topo-sort · group=G-B-1 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

拓扑排序将DAG（有向无环图）的所有节点排成线性序列，使得对任意有向边(u,v)，u在序列中位于v之前。常用Kahn算法（基于入度的BFS）或DFS后序逆序实现。拓扑排序不唯一。若图有环则不存在拓扑序。AOV网（顶点活动网）的拓扑排序可用于课程安排、任务调度等。AOE网可在此基础上求关键路径。

## Why · 为什么

### 直觉 · Intuition

排课表：学数据结构前必须学离散数学，学编译技术前必须学算法语言。将所有课程按依赖关系排序，这就是拓扑排序。

### 原理 · Principle

Kahn算法：维护入度为0的节点集合，每次取出一个放入结果序列，删除其所有出边，将新入度为0的节点加入集合。DFS算法：对所有未访问节点DFS，完成时逆序记录（后序逆序=拓扑序）。

### 历史 · History

Kahn算法由Arthur Kahn于1962年提出。DFS方法利用了'完成时间逆序即拓扑序'的性质。两者时间复杂度均为O(V+E)。

## How · 实现

### 伪代码

```python
Kahn:
  S ← {nodes with indeg=0}
  L ← []
  while S not empty:
    remove u from S, append to L
    for each edge (u,v):
      indeg[v] -= 1
      if indeg[v]==0: add v to S
  if len(L)<n: has cycle
  return L
```

### Python 实现

```python
from collections import deque
import sys

def topo_sort_kahn(n, edges):
    """Kahn's algorithm (BFS-based). Returns topological order or None if cycle."""
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == n else None

def topo_sort_dfs(n, edges):
    """DFS-based topological sort. Returns order or None if cycle."""
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    UNVISITED, VISITING, DONE = 0, 1, 2
    state = [UNVISITED] * n
    order = []
    has_cycle = [False]
    def dfs(u):
        state[u] = VISITING
        for v in adj[u]:
            if state[v] == VISITING:
                has_cycle[0] = True
                return
            if state[v] == UNVISITED:
                dfs(v)
                if has_cycle[0]:
                    return
        state[u] = DONE
        order.append(u)
    for i in range(n):
        if state[i] == UNVISITED:
            dfs(i)
            if has_cycle[0]:
                return None
    order.reverse()
    return order

if __name__ == "__main__":
    edges = [(0, 1), (0, 2), (1, 3), (2, 3)]
    order = topo_sort_kahn(4, edges)
    assert order is not None
    assert order.index(0) < order.index(1)
    assert order.index(0) < order.index(2)
    assert order.index(1) < order.index(3)
    assert order.index(2) < order.index(3)
    order2 = topo_sort_dfs(4, edges)
    assert order2 is not None
    assert order2.index(0) < order2.index(1)
    # Cycle detection
    cycle_edges = [(0, 1), (1, 0)]
    assert topo_sort_kahn(2, cycle_edges) is None
    assert topo_sort_dfs(2, cycle_edges) is None
    print("topo-sort: ALL TESTS PASSED")

```

**PyPy 提示**: Kahn用deque.popleft()在PyPy上高效。DFS递归注意栈深度。大图用邻接表比邻接矩阵快。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(V+E) |
| 空间 | O(V+E) |

### 局限

仅适用于DAG。有环图无法拓扑排序。拓扑序不唯一（取决于入度为0的节点取出顺序）。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| LeetCode | 207 | 3 | DAG 是否有环判定 | [https://leetcode.cn/problems/course-schedule/](https://leetcode.cn/problems/course-schedule/) |
| LeetCode | 210 | 4 | 求拓扑排序序列 | [https://leetcode.cn/problems/course-schedule-ii/](https://leetcode.cn/problems/course-schedule-ii/) |
| Luogu | P4017 | 4 | 拓扑排序+DP 统计最大食物链数量 | [https://www.luogu.com.cn/problem/P4017](https://www.luogu.com.cn/problem/P4017) |

## Pitfalls · 易错点

- 忘记检测环：Kahn算法中若len(order)<n则有环
- DFS方法中VISITING状态用于检测回边（环），DONE状态避免重复访问
- 多组数据需重置indeg数组
- 拓扑序不唯一，不同实现可能给出不同合法序列

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/topo/](https://oi-wiki.org/graph/topo/)
- CP-Algorithms ✓ [https://cp-algorithms.com/graph/topological-sort.html](https://cp-algorithms.com/graph/topological-sort.html)
- 书籍 ✓ `CPH ch16 pp159-166`
