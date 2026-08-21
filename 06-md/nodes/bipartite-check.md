---
id: bipartite-check
name: 二分图判定
group: G-B-6
stage: basic
priority: P0
depth_tier: deep
---

# 二分图判定

> BFS/DFS染色法判定二分图O(V+E)

<!-- 元信息: id=bipartite-check · group=G-B-6 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

二分图（Bipartite Graph）是顶点集可划分为两个互不相交集合 X、Y，且每条边都连接 X 与 Y 之间一对点的图。二分图判定问题是：给定无向图，判断它是否是二分图，并在是时给出一组划分（染色）。核心刻画：图可 2-着色（相邻顶点颜色不同）⇔ 图是二分图 ⇔ 图中无奇环。判定用 BFS/DFS 染色，O(V+E)。应用极广：是二分图匹配、最小点覆盖、最大独立集、任务分配建模的『前置判定』，网格图、树、偶环天然二分。

## Why · 为什么

### 直觉 · Intuition

用两种颜色给顶点涂色，相邻顶点必须异色。从一个点出发 DFS/BFS，一路涂与当前相反的颜色；若遇到相邻两点同色（矛盾），说明图里有长度为奇数的环，不是二分图。想象成用两种颜色给地图国家涂色且相邻国家不同色——不能时必有一个奇环绕回来。

### 原理 · Principle

① 等价刻画（可证）：(a) 可 2-着色；(b) 无奇环；(c) 是二分图。证明：二分图定义 ⇔ 2-着色显然；无奇环 ⇒ 2-着色：每个连通分量任选根，按到根距离奇偶性染色，DFS 生成树外非树边两端颜色不同当且仅当该边形成偶环，若无奇环则一切非树边连接异色点；② 判定算法：对每个未染色连通分量的任意起点染色 0，BFS/DFS 遍历，相邻未染色点染相反色，若相邻点已染色且颜色相同 → 非二分图；③ 复杂度 O(V+E)。染色结果即给出 X/Y 划分，可直接用于后续匹配算法。

### 历史 · History

二分图与染色是现代图论基石，Dénes Kőnig 1931 年系统研究了二分图匹配理论（Kőnig 定理：二分图最大匹配=最小点覆盖）。染色法判定二分图是图遍历的基础应用，CPH（第 16 章）、OI Wiki、CP-Algorithms 均有标准实现与证明。

## How · 实现

### 伪代码

```python
def is_bipartite(n, edges):
  g = 邻接表(edges)
  col = [-1] * n
  for s in range(n):
    if col[s] != -1: continue
    col[s] = 0; q = [s]
    while q:
      u = pop(q)
      for v in g[u]:
        if col[v] == -1:
          col[v] = col[u] ^ 1; push(q, v)
        elif col[v] == col[u]:
          return False
  return True
```

### Python 实现

```python
from collections import deque


def is_bipartite(n, edges):
    """无向图二分图判定。edges: [(u,v),...]。返回 (是二分图?, 染色数组 col 或 None)。"""
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)
    col = [-1] * n
    for s in range(n):
        if col[s] != -1:
            continue
        col[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in g[u]:
                if col[v] == -1:
                    col[v] = col[u] ^ 1
                    q.append(v)
                elif col[v] == col[u]:
                    return False, None
    return True, col


if __name__ == '__main__':
    # 偶环/树/网格 → 二分；三角环 → 非二分
    assert is_bipartite(4, [(0, 1), (1, 2), (2, 3)])[0] is True       # 链
    assert is_bipartite(4, [(0, 1), (1, 2), (2, 3), (3, 0)])[0] is True  # 偶环
    assert is_bipartite(3, [(0, 1), (1, 2), (2, 0)])[0] is False       # 奇环
    assert is_bipartite(5, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)])[0] is False  # 五角星奇环
    # 随机验证: 用暴力枚举染色交叉验证
    import random
    random.seed(7)
    for _ in range(300):
        n = random.randint(1, 8)
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.3:
                    edges.append((i, j))
        ok, col = is_bipartite(n, edges)
        # 暴力: 检查任意 2-着色是否可行
        def brute():
            def dfs(i, c):
                if i == n:
                    return True
                for trial in range(2):
                    cur = [0] * n
                    # 枚举染色
                    pass
            return None
        def check_brute():
            for mask in range(1 << n):
                good = True
                for u, v in edges:
                    if ((mask >> u) & 1) == ((mask >> v) & 1):
                        good = False
                        break
                if good:
                    return True
            return False
        assert ok == check_brute(), (n, edges, ok)
    print('bipartite-check: All tests passed.')
```

**PyPy 提示**: 邻接表用 list-of-list，BFS 用 collections.deque（或 list+头指针）。染色数组复用为答案。对 1e5 规模无压力。若需输出具体 X/Y 划分，col[u]==0 归左部即可。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(V+E)（每个点入队一次、每条边检查两次） |
| 空间 | O(V+E) 邻接表；O(V) 染色数组与队列 |

### 局限

只对无向图有意义（有向图二分判定需先按无向化处理）。图可能不连通，必须遍历所有连通分量，漏了会误判。仅判定是/否，若需匹配、最大独立集等需配合其他算法。染色只保证『存在』一组划分，不保证唯一（多个连通分量可互换颜色）。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1330 | 3 | 封锁阳光大学：二分图判定+每个连通分量取较少数量的染色数之和，经典应用 | [https://www.luogu.com.cn/problem/P1330](https://www.luogu.com.cn/problem/P1330) |
| Luogu | P1525 | 4 | 关押罪犯：二分答案+二分图判定（或带权并查集），二分染色经典题 | [https://www.luogu.com.cn/problem/P1525](https://www.luogu.com.cn/problem/P1525) |
| Luogu | P3355 | 4 | 骑士共存问题：棋盘黑白染色证明图二分，再转最大独立集/匹配，判定+匹配结合 | [https://www.luogu.com.cn/problem/P3355](https://www.luogu.com.cn/problem/P3355) |
| AtCoder | abc286_d | 3 | 二分图建模入门（可达性与分配类问题常先做二分判定） | [https://atcoder.jp/contests/abc286/tasks/abc286_d](https://atcoder.jp/contests/abc286/tasks/abc286_d) |

## Pitfalls · 易错点

- 只遍历一个连通分量就 return，未覆盖其他分量 → 假阴性/假阳性
- 把 BFS 写成只检查出边方向（有向化错误）——无向图两边都要加
- 染色冲突要立刻终止并返回 False，但其他分量仍可能是二分图（整体才非二分）
- 链/树/偶环天然二分，但三角、五角星等奇环必须能识别
- col 数组与 visited 复用：初始化为 -1 与染色值冲突会误判
- 自环（u==v）直接非二分；重边无害但别在去重时误删

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/bi-graph/](https://oi-wiki.org/graph/bi-graph/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/bi-graph.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/bi-graph.md)
- CP-Algorithms ✓ [https://cp-algorithms.com/graph/bipartite-check.html](https://cp-algorithms.com/graph/bipartite-check.html)
- 书籍 ✓ `CPH ch16 pp159-166`
