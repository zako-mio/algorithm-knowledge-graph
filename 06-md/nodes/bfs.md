---
id: bfs
name: BFS广度优先搜索
group: G-B-1
stage: basic
priority: P0
depth_tier: deep
---

# BFS广度优先搜索

> 按层遍历图，队列实现O(V+E)，可求无权最短路

<!-- 元信息: id=bfs · group=G-B-1 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

BFS(Breadth First Search)是图上最基础最重要的搜索算法之一。每次尝试访问同一层的节点，同层访问完后再访问下一层。用队列实现，从起点出发逐层扩展。BFS找到的路径是从起点开始的最短合法路径（边数最少）。时间复杂度O(V+E)，空间O(V)。

## Why · 为什么

### 直觉 · Intuition

BFS的过程类似火苗传播：起点最先着火，每个时刻有着火的节点向所有相邻节点传播火苗。由于是逐层扩展的，第一次到达某节点时的路径一定是最短路径（最少边数）。这就是BFS用于无权图最短路的原理。

### 原理 · Principle

算法流程：(1) 初始化：起点s入队，vis[s]=true，dist[s]=0。(2) 出队u，遍历u的所有未访问邻居v：v入队，vis[v]=true，dist[v]=dist[u]+1，prev[v]=u。(3) 重复直到队列为空。队列保证FIFO顺序，即先入队的先处理，确保按层扩展。dist数组记录最短边数，prev数组可还原最短路径。0-1 BFS：边权为0/1时用双端队列，权0边加到队首、权1边加到队尾，仍保证单调性。

### 历史 · History

BFS是图遍历的基础算法，与DFS并列为图论两大遍历范式。其队列实现简单但性质强大：可求无权图最短路、连通块、最小环等。0-1 BFS是BFS到Dijkstra的桥梁，用双端队列代替优先队列实现O(V+E)的0/1权最短路。OI Wiki将其列为图论基础中的核心内容。

## How · 实现

### 伪代码

```python
bfs(s):
  q = queue()
  q.push(s); vis[s] = true; dist[s] = 0
  while q not empty:
    u = q.pop_front()
    for v in neighbors(u):
      if not vis[v]:
        vis[v] = true
        dist[v] = dist[u] + 1
        prev[v] = u
        q.push(v)
  # dist[t] = 最短边数, prev[] 还原路径
```

### Python 实现

```python
from collections import deque, defaultdict


def bfs(adj, n, start):
    """BFS遍历, 返回dist(最短边数)和prev(前驱)
    adj: 邻接表 adj[u] = [v, ...]
    n: 节点数
    start: 起点
    """
    dist = [-1] * n
    prev = [-1] * n
    dist[start] = 0
    q = deque([start])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                prev[v] = u
                q.append(v)
    return dist, prev


def bfs_shortest_path(adj, n, start, target):
    """用BFS求无权图最短路径, 返回路径列表(不含起点则返回空)"""
    dist, prev = bfs(adj, n, start)
    if dist[target] == -1:
        return None  # 不可达
    path = []
    v = target
    while v != -1:
        path.append(v)
        v = prev[v]
    path.reverse()
    return path


def bfs_01(adj, n, start):
    """0-1 BFS: 边权为0或1的最短路
    adj[u] = [(v, w), ...], w为0或1
    用双端队列: 权0边加队首, 权1边加队尾
    """
    INF = float('inf')
    dist = [INF] * n
    dist[start] = 0
    dq = deque([start])
    while dq:
        u = dq.popleft()
        for v, w in adj[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                if w == 0:
                    dq.appendleft(v)
                else:
                    dq.append(v)
    return dist


def count_components_bfs(adj, n):
    """用BFS求连通块数量"""
    visited = [False] * n
    count = 0
    for s in range(n):
        if not visited[s]:
            count += 1
            visited[s] = True
            q = deque([s])
            while q:
                u = q.popleft()
                for v in adj[u]:
                    if not visited[v]:
                        visited[v] = True
                        q.append(v)
    return count


if __name__ == "__main__":
    # 测试图: 0-1-2-3, 0-3 (最短路应为0->3, 边数1)
    adj = defaultdict(list)
    adj[0].extend([1, 3])
    adj[1].extend([0, 2])
    adj[2].extend([1, 3])
    adj[3].extend([0, 2])
    n = 4

    dist, prev = bfs(adj, n, 0)
    assert dist == [0, 1, 2, 1], f"dist={dist}"

    path = bfs_shortest_path(adj, n, 0, 3)
    assert path == [0, 3], f"path={path}"

    # 连通块测试
    adj2 = defaultdict(list)
    adj2[0].append(1)
    adj2[1].append(0)
    adj2[2].append(3)
    adj2[3].append(2)
    assert count_components_bfs(adj2, 4) == 2

    # 0-1 BFS测试
    adj3 = defaultdict(list)
    adj3[0].append((1, 0))  # 0->1, 权0
    adj3[1].append((2, 1))  # 1->2, 权1
    adj3[0].append((2, 1))  # 0->2, 权1
    dist01 = bfs_01(adj3, 3, 0)
    assert dist01 == [0, 0, 1], f"dist01={dist01}"

    print("All tests passed.")

```

**PyPy 提示**: PyPy的deque操作快，BFS在n=1e5,m=1e6时约0.2s。0-1 BFS用deque的appendleft也高效。避免用list当队列(pop(0)是O(n))，必须用deque。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(V+E) — 每个节点和边各访问一次 |
| 空间 | O(V) — vis数组+队列+dist/prev数组 |

### 局限

BFS只适用于无权图(边数最短)或0-1权图。带权图最短路需Dijkstra。Python的list.pop(0)是O(n)，必须用collections.deque。多源BFS可一次入队多个起点。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1135 | 2 | 奇怪的电梯：BFS求最短步数，状态为楼层 | [https://www.luogu.com.cn/problem/P1135](https://www.luogu.com.cn/problem/P1135) |
| Luogu | P1746 | 2 | 逃离迷宫：BFS求无权最短路，网格图方向限制 | [https://www.luogu.com.cn/problem/P1746](https://www.luogu.com.cn/problem/P1746) |
| Codeforces | 173B | 1800 | Chamber of Secrets：0-1 BFS经典应用，方向切换权0权1 | [https://codeforces.com/problemset/problem/173/B](https://codeforces.com/problemset/problem/173/B) |

## Pitfalls · 易错点

- 用list当队列做BFS(pop(0)是O(n))导致O(n²)，必须用deque
- 入队时未立即标记vis[v]=true，导致同一节点多次入队(重复访问)
- dist初始化为-1还是0混淆：-1表示未访问更安全，避免与起点dist=0混淆
- 0-1 BFS中权0边加队首而非队尾，否则不保证单调性

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/bfs/](https://oi-wiki.org/graph/bfs/)
- CP-Algorithms ✓ [https://cp-algorithms.com/graph/breadth-first-search.html](https://cp-algorithms.com/graph/breadth-first-search.html)
- 书籍 ✓ `CPH ch12 pp127-132`
