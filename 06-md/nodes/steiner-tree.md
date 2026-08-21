---
id: steiner-tree
name: Steiner树
group: G-B-3
stage: advanced
priority: P2
depth_tier: standard
---

# Steiner树

> 给定关键点集的最小连通子图，NP-hard，状压DP f[i][S]+Dijkstra松弛 O(3^k n + 2^k m log n)

<!-- 元信息: id=steiner-tree · group=G-B-3 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

最小斯坦纳树(Minimum Steiner Tree)：给定无向图 G、点集 V、关键点集 K(|K|=k)，求连接 K 中所有点的最小权连通子图。允许使用非关键点(斯坦纳点)作为中转。该问题是 NP-hard，但当关键点很少(k≤12 左右)时可用状态压缩 DP：f[i][S] = 以 i 为根、包含关键点子集 S 的最小连通子树权值和。转移分两类：① 子集合并 f[i][S]=min(f[i][T]+f[i][S−T])；② 沿边松弛 f[i][S]=min(f[j][S]+w(i,j))，第二类用 Dijkstra(或直接最短路)处理。复杂度 O(3^k·n + 2^k·m·log n)。

## Why · 为什么

### 直觉 · Intuition

关键点集合很小，把它压成状态 S(bitmask)。想象在图上长一棵树：每个状态 S 的树要么是把两棵包含不相交子集 T 和 S−T 的树在同一个根 i 处『拼起来』，要么是把根 i 沿着一条边挪到 j 去连通更多点。前一种在每对子集间枚举，后一种就是最短路。两棵拼出来的树共享根，所以相加不重复计权。

### 原理 · Principle

设 f[i][S] 为以 i 为根、包含集合 S 的最小树权。边界：f[关键点p][{p}]=0。子集转移：f[i][S]=min_{T⊂S} f[i][T]+f[i][S−T] (枚举真子集)。边转移：f[i][S]=min_j f[j][S]+w(i,j)，等价于在每个固定 S 下对 f[·][S] 跑一次 Dijkstra 松弛。答案为 min_i f[i][K]。复杂度 3^k 来自子集枚举 ∑_{S}2^{|S|}=3^k。要点是子集转移需保证 T 与 S−T 均为真子集避免环。

### 历史 · History

斯坦纳树问题源于 19 世纪初雅可比·斯坦纳研究的『连接三村庄的最短道路网』(平面上三点的费马点问题)。1971 年 Dreyfus 与 Wagner 提出著名的 O(3^k n + 2^k n^2) 动态规划算法，成为竞赛中 k 较小时的通行解法。图上的最小斯坦纳树在电路布线、网络设计中有广泛背景。

## How · 实现

### 伪代码

```python
function steiner(n, adj, key):
  k = len(key)
  f = INF[n][1<<k]
  for idx, v in key: f[v][1<<idx] = 0
  for S in 1..(1<<k)-1:
    for T in proper_subset(S):   # 只枚举一半(T<other)避免重复
      for i in range(n): f[i][S] = min(f[i][S], f[i][T]+f[i][S^T])
    # Dijkstra 对当前 S 做边松弛
    pq = heap([(f[i][S], i) for i if f[i][S]<INF])
    while pq:
      (d,u) = pop; if d != f[u][S]: continue
      for (v,w) in adj[u]: if d+w < f[v][S]: f[v][S]=d+w; push
  return min(f[i][(1<<k)-1])
```

### Python 实现

```python
import heapq

INF = float('inf')


def steiner_tree(n, adj, key):
    """最小斯坦纳树: f[i][S] = 以i为根连通关键点集合S的最小边权和。
    key: 关键点列表(0-index)。adj[i]=list of (v,w)"""
    k = len(key)
    if k <= 1:
        return 0
    f = [[INF] * (1 << k) for _ in range(n)]
    for idx, v in enumerate(key):
        f[v][1 << idx] = 0
    for S in range(1, 1 << k):
        sub = (S - 1) & S
        while sub:
            other = S ^ sub
            if other < sub or other == 0:
                sub = (sub - 1) & S
                continue
            for i in range(n):
                if f[i][sub] < INF and f[i][other] < INF:
                    f[i][S] = min(f[i][S], f[i][sub] + f[i][other])
            sub = (sub - 1) & S
        pq = [(f[i][S], i) for i in range(n) if f[i][S] < INF]
        heapq.heapify(pq)
        while pq:
            d, u = heapq.heappop(pq)
            if d != f[u][S]:
                continue
            for v, w in adj[u]:
                if d + w < f[v][S]:
                    f[v][S] = d + w
                    heapq.heappush(pq, (d + w, v))
    full = (1 << k) - 1
    return min(f[i][full] for i in range(n))


if __name__ == "__main__":
    # 三角形 0-1(2),1-2(3),0-2(4), 关键点{0,2} -> 4
    adj = [[(1, 2), (2, 4)], [(0, 2), (2, 3)], [(0, 4), (1, 3)]]
    assert steiner_tree(3, adj, [0, 2]) == 4
    assert steiner_tree(3, adj, [0, 1, 2]) == 5  # 关键点连成树 = MST
    # 线性图 0-1-2-3, 关键点{0,3}, 用中间点 -> 3
    adj2 = [[(1, 1)], [(0, 1), (2, 1)], [(1, 1), (3, 1)], [(2, 1)]]
    assert steiner_tree(4, adj2, [0, 3]) == 3
    print("steiner OK")

```

**PyPy 提示**: 状态数组 f[n][2^k] 在 k≤12, n≤1e4 时 2^k 太大不可直接开，实际题目(n≤100, k≤10)常用 f[1<<k][n] 转置以利缓存。子集枚举只做一半(sub < other)可省一半时间。每层 Dijkstra 重建优先队列 O(n) 堆化，比逐点 push 快。PyPy 下 3^k·n 的循环是主瓶颈，可考虑用二维滚动。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(3^k · n + 2^k · (m log n)) |
| 空间 | O(2^k · n) |

### 局限

1) 关键点数 k 必须很小(k≤12~15)，否则 2^k/3^k 爆炸；2) 边权须非负(DP 依赖最短路性质)；3) 若需输出具体树边需额外记录 pre 指针；4) 不要求树时(任意连通子图含环)问题退化为更简单，但一般模板即树；5) 点权版(如 WC2008 游览计划)在子集合并时需减去重复计的点权 a[i]。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P6192 | 4 | 【模板】最小斯坦纳树：f[i][S] 状压 DP + Dijkstra 标准模板 | [https://www.luogu.com.cn/problem/P6192](https://www.luogu.com.cn/problem/P6192) |
| Luogu | P4294 | 5 | WC2008 游览计划：点权版斯坦纳树，需记录 pre 输出方案 | [https://www.luogu.com.cn/problem/P4294](https://www.luogu.com.cn/problem/P4294) |
| LOJ | 2110 | 6 | JLOI2015 管道连接：分组斯坦纳树(要求的是满足分组约束的最小连通子图) | [https://loj.ac/p/2110](https://loj.ac/p/2110) |

## Pitfalls · 易错点

- 子集枚举忘记去重(只算 T<other 一半)导致时间加倍或状态重复
- 子集合并时 T 与 other 不能为空集，且应保证无重复计数(共享根相加是定义)
- 每层 Dijkstra 忘记处理 f[i][S]=INF 的初始状态，堆化 INF 导致错误
- k 太大(>15)硬做导致 2^k 数组溢出/超时
- 点权版合并时忘记减重复统计的根点权 a[i]

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/steiner-tree/](https://oi-wiki.org/graph/steiner-tree/)
- CP-Algorithms △ [https://cp-algorithms.com/graph/steiner-tree.html](https://cp-algorithms.com/graph/steiner-tree.html)
