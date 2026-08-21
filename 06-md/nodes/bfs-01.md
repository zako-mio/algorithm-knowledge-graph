---
id: bfs-01
name: 0-1 BFS
group: G-B-2
stage: intermediate
priority: P1
depth_tier: standard
---

# 0-1 BFS

> 双端队列处理0/1权边最短路O(V+E)

<!-- 元信息: id=bfs-01 · group=G-B-2 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

0-1 BFS 是处理『边权只有 0 或 1』（可推广为 0 或任意常数 k）图的最短路算法，O(V+E) 时间 O(V) 空间，比 Dijkstra 少一个 log。用双端队列（deque）维护：0 权边扩展的节点插入队首，1 权边扩展的节点插入队尾，从而保证队内距离单调不降（类 BFS 的分层性质），每个节点至多入队少数几次。是边权二进制图中最高效的算法，也常作为分层图、图论建模优化。

## Why · 为什么

### 直觉 · Intuition

普通 BFS 只适合权全为 1。若边权是 0/1，则用双端队列：走 0 权边距离不变，应优先处理 → 插队首；走 1 权边距离 +1，稍后处理 → 插队尾。这样队列从头到尾距离单调，等价于『分层 BFS』：0 权边在层内移动，1 权边跨层。当从队首取出的节点距离已经是全队最小，其最短路即确定（与 Dijkstra 的贪心同理，但靠权值只有两档省掉了堆）。

### 原理 · Principle

① 初始化 dis[s]=0，deque=[s]；② 弹出队首 u（保证是当前最小距离，需配合 vis 标记防重复扩展）；③ 对 0 权边 (u,v)：若 dis[v] > dis[u] 则更新并 appendleft(v)；对 1 权边：更新并 append(v)；④ 终止条件与 BFS 相同。正确性：队列单调性保证队首距离最小，由归纳法每个节点第一次出队即确定最短路。可推广到边权∈{0, k}（k 常数）或 {a, b}（把 b 拆成 b/a 个 a？不，{a,b} 需按比例，一般仅 {0,1} 或 {0,k}）。

### 历史 · History

0-1 BFS 是现代算法竞赛的标准技巧，其思想可视为 Dijkstra 在只有两种边权下的退化（用双端队列替代优先队列）。CP-Algorithms 有专章（01_bfs），OI Wiki 在 BFS 页『双端队列 BFS』一节介绍，广泛用于迷宫『花金币 vs 免费步数』、网格图、状态图建模题。

## How · 实现

### 伪代码

```python
from collections import deque
def bfs01(adj, s):
  dis=[INF]*n; dis[s]=0; dq=deque([s])
  while dq:
    u=dq.popleft()
    for v, w in adj[u]:       # w in {0,1}
      if dis[u]+w < dis[v]:
        dis[v]=dis[u]+w
        if w==0: dq.appendleft(v)
        else: dq.append(v)
  return dis
```

### Python 实现

```python
from collections import deque


def bfs01(n, adj, s):
    """0-1 BFS: 边权仅 0/1 的单源最短路, O(V+E).
    adj: 邻接表 adj[u]=[(v,w),...], w in {0,1}."""
    INF = float('inf')
    dis = [INF] * n
    dis[s] = 0
    dq = deque([s])
    while dq:
        u = dq.popleft()
        du = dis[u]
        for v, w in adj[u]:
            nd = du + w
            if nd < dis[v]:
                dis[v] = nd
                if w == 0:
                    dq.appendleft(v)
                else:
                    dq.append(v)
    return dis


def bfs01_path(n, adj, s, t):
    """带路径重建: 返回 (dist, path)"""
    INF = float('inf')
    dis = [INF] * n
    pre = [-1] * n
    dis[s] = 0
    dq = deque([s])
    while dq:
        u = dq.popleft()
        du = dis[u]
        for v, w in adj[u]:
            nd = du + w
            if nd < dis[v]:
                dis[v] = nd
                pre[v] = u
                if w == 0:
                    dq.appendleft(v)
                else:
                    dq.append(v)
    if dis[t] == INF:
        return INF, []
    path = []
    cur = t
    while cur != -1:
        path.append(cur)
        cur = pre[cur]
    path.reverse()
    return dis[t], path


if __name__ == "__main__":
    # 图: 0-1(1),0-2(0),1-3(0),2-3(1),2-4(1),3-4(0)
    adj = [[] for _ in range(5)]
    for u, v, w in [(0, 1, 1), (0, 2, 0), (1, 3, 0), (2, 3, 1), (2, 4, 1), (3, 4, 0)]:
        adj[u].append((v, w))
    dis = bfs01(5, adj, 0)
    assert dis == [0, 1, 0, 1, 1], dis
    d, p = bfs01_path(5, adj, 0, 4)
    assert d == 1 and p == [0, 2, 4], (d, p)  # 0->2(0)->4(1)=1 为最短路

    # 与 Dijkstra 交叉验证
    import heapq, random
    random.seed(53)

    def dijkstra(n, adj, s):
        INF = float('inf')
        dis = [INF] * n
        dis[s] = 0
        pq = [(0, s)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dis[u]:
                continue
            for v, w in adj[u]:
                nd = d + w
                if nd < dis[v]:
                    dis[v] = nd
                    heapq.heappush(pq, (nd, v))
        return dis

    for _ in range(300):
        n = random.randint(1, 8)
        a = [[] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j and random.random() < 0.3:
                    a[i].append((j, random.randint(0, 1)))
        s = random.randrange(n)
        d1 = bfs01(n, a, s)
        d2 = dijkstra(n, a, s)
        for i in range(n):
            assert d1[i] == d2[i], (i, d1[i], d2[i])
    print("All tests passed.")
```

**PyPy 提示**: deque 的 appendleft/append 均 O(1)，PyPy 性能优秀。0 权边优先处理保证单调性，不要用普通队列。若边权是 {0,k}，把 k 视作 1 档即可（相当于 w=1 的推广，只要两种权值成比例）。INF 用大整数避免 float 比较开销。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(V+E) |
| 空间 | O(V+E) |

### 局限

仅适用于边权只有两档（0/1 或 0/k）。边权多样时必须用 Dijkstra/Bellman-Ford。0-1 BFS 要求权值可比较的『0 或 1』语义；若边权为 {1,2} 之类，可通过拆点/换权换算，但一般不划算。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Codeforces | 173B | 5 | Chamber of Secrets：OI Wiki 例题，激光网格建模为 0-1 BFS | [https://codeforces.com/problemset/problem/173/B](https://codeforces.com/problemset/problem/173/B) |
| Luogu | P4554 | 4 | 小明的游戏：棋盘 0/1 权最短路经典题 | [https://www.luogu.com.cn/problem/P4554](https://www.luogu.com.cn/problem/P4554) |
| Codeforces | 1341E | 5 | Nastya and Unexpected Guest：模时间建图 0-1 BFS（0/1 权状态图） | [https://codeforces.com/problemset/problem/1341/E](https://codeforces.com/problemset/problem/1341/E) |

## Pitfalls · 易错点

- 用普通队列代替 deque 会破坏单调性，结果错误
- 0 权边插队首、1 权边插队尾，顺序写反会 TLE/错误
- dis 初始 INF 且更新后必须判断 nd<dis[v] 才能入队，否则死循环（0 权环）
- 边权不止 0/1 时硬套 0-1 BFS 会错，须换 Dijkstra
- 0 权环可能让节点多次入队，dis 检查可避免无限循环

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/bfs/](https://oi-wiki.org/graph/bfs/)
- CP-Algorithms ✓ [https://cp-algorithms.com/graph/01_bfs.html](https://cp-algorithms.com/graph/01_bfs.html)
- 书籍 ✓ `CPH ch13 pp133-142`
