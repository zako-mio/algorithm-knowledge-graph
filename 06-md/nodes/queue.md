---
id: queue
name: 队列
group: G-A-2
stage: basic
priority: P0
depth_tier: deep
---

# 队列

> FIFO先进先出结构，BFS基础组件

<!-- 元信息: id=queue · group=G-A-2 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

队列(Queue)是先进先出(FIFO, First In First Out)的线性数据结构：在队尾(rear)插入(enqueue)，在队首(front)删除(dequeue)。Python 中用 collections.deque 实现，支持 O(1) 的双端操作。是 BFS(广度优先搜索)的核心组件。

## Why · 为什么

### 直觉 · Intuition

队列模拟'排队'——先来的先服务。这种'按到达顺序处理'的属性天然适合层序遍历(BFS)：同一层的节点按入队顺序依次处理，保证先处理的层先完成。

### 原理 · Principle

队列维护一个线性序列，只允许在队尾插入、队首删除。enqueue(x): 队尾追加；dequeue(): 队首移除并返回；front(): 查看队首。用 collections.deque 实现：append()=enqueue O(1)，popleft()=dequeue O(1)。关键应用：①BFS(层序遍历图/树，队列保证按距离顺序处理) ②拓扑排序(Kahn算法，入度为0的节点入队) ③滑动窗口(单调队列基础) ④双端队列(deque)支持双端操作。

### 历史 · History

队列与栈同为最基础的线性数据结构。FIFO 语义对应现实中的排队模型。C++ STL 提供 std::queue(适配器，默认基于 deque)和 std::deque(双端队列)。Python 提供 collections.deque 作为高效双端队列。

## How · 实现

### 伪代码

```python
enqueue(x): q.append(x)
dequeue(): return q.popleft()
front(): return q[0]
empty(): return len(q) == 0

# BFS
bfs(start):
  q.enqueue(start)
  visited[start] = True
  while not q.empty():
    u = q.dequeue()
    for v in adj[u]:
      if not visited[v]:
        visited[v] = True
        q.enqueue(v)
```

### Python 实现

```python
from collections import deque

class Queue:
    """基于 deque 的队列实现。"""
    def __init__(self):
        self._data = deque()

    def enqueue(self, x):
        self._data.append(x)

    def dequeue(self):
        return self._data.popleft()

    def front(self):
        return self._data[0]

    def empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)


def bfs(adj, start, n):
    """广度优先搜索: 从 start 出发, 返回各节点到 start 的最短距离。
    adj: 邻接表(0-indexed), n: 节点数
    """
    dist = [-1] * n
    q = Queue()
    q.enqueue(start)
    dist[start] = 0
    while not q.empty():
        u = q.dequeue()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.enqueue(v)
    return dist


def topo_sort(adj, indeg, n):
    """拓扑排序(Kahn算法): 返回拓扑序, 若有环返回空列表。
    adj: 邻接表, indeg: 入度数组, n: 节点数
    """
    q = Queue()
    for i in range(n):
        if indeg[i] == 0:
            q.enqueue(i)
    order = []
    while not q.empty():
        u = q.dequeue()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.enqueue(v)
    return order if len(order) == n else []


if __name__ == '__main__':
    # 测试队列基本操作
    q = Queue()
    for i in range(5):
        q.enqueue(i)
    print(f'Queue size: {q.size()}')  # 5
    print(f'Front: {q.front()}')  # 0
    while not q.empty():
        print(q.dequeue(), end=' ')  # 0 1 2 3 4 (FIFO)
    print()

    # 测试BFS
    # 图: 0-1, 0-2, 1-3, 2-3, 3-4
    adj = [[1, 2], [3], [3], [4], []]
    dist = bfs(adj, 0, 5)
    print(f'BFS dist from 0: {dist}')  # [0, 1, 1, 2, 3]
    assert dist == [0, 1, 1, 2, 3]

    # 测试拓扑排序
    # DAG: 0->1, 0->2, 1->3, 2->3, 3->4
    adj2 = [[1, 2], [3], [3], [4], []]
    indeg = [0, 1, 1, 2, 1]
    order = topo_sort(adj2, indeg[:], 5)
    print(f'Topo order: {order}')  # [0, 1, 2, 3, 4]
    assert len(order) == 5
    print('All tests passed!')

```

**PyPy 提示**: PyPy 对 deque 的 popleft/append JIT 优化好；BFS 中队列操作频繁，deque 是最佳选择；list.pop(0) 是 O(N) 绝对不要用。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | enqueue/dequeue/front/empty/size 均 O(1)；BFS O(V+E)；拓扑排序 O(V+E) |
| 空间 | O(V) BFS/拓扑排序中队列最多存全部节点 |

### 局限

Python list 的 pop(0) 是 O(N) 不能当队列用，必须用 deque；队列大小无上限但受内存限制；BFS 的 dist 数组在 N>1e7 时可能内存不足。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| LeetCode | 200 | 2 | 岛屿数量: BFS/DFS 搜索连通分量 | [https://leetcode.cn/problems/number-of-islands/](https://leetcode.cn/problems/number-of-islands/) |
| LeetCode | 207 | 2 | 课程表: 拓扑排序判环 | [https://leetcode.cn/problems/course-schedule/](https://leetcode.cn/problems/course-schedule/) |
| Luogu | B3616 | 1 | 队列模板题: 数组模拟队列基本操作 | [https://www.luogu.com.cn/problem/B3616](https://www.luogu.com.cn/problem/B3616) |

## Pitfalls · 易错点

- 用 list.pop(0) 当队列 → O(N) 每次 → 整体 O(N^2) TLE；必须用 deque.popleft()
- BFS 忘记标记 visited → 重复入队 → 死循环/超时
- BFS 中在出队时才标记 visited 而非入队时 → 同一节点可能多次入队 → TLE/MLE
- 拓扑排序忘记检测 len(order)!=n 的情况(有环时无拓扑序)

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/queue/](https://oi-wiki.org/ds/queue/)
- CP-Algorithms ✓ [https://cp-algorithms.com/data_structures/stack_queue_modification.html](https://cp-algorithms.com/data_structures/stack_queue_modification.html)
- 书籍 ✓ `CPH ch4 p45`
