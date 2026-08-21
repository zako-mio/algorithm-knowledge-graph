---
id: astar
name: A*算法
group: G-A-14
stage: intermediate
priority: P1
depth_tier: standard
---

# A*算法

> f=g+h优先队列搜索，可采纳启发函数保证最优性

<!-- 元信息: id=astar · group=G-A-14 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

A*（A-star）搜索是在带权有向图上求起点到终点最短路径的最佳优先搜索算法，是 BFS 的改进。它维护优先队列，每次取出 f(x)=g(x)+h(x) 最小的节点扩展，其中 g(x)=起点到 x 的实际距离，h(x)=x 到终点的距离估计。当启发函数可采纳（0≤h≤h*，即不高估真实距离）时，A* 保证找到最优解；当 h 一致（三角不等式）时每个节点只处理一次。8数码、k短路、机器人路径规划都是典型应用。

## Why · 为什么

### 直觉 · Intuition

A* 像'有方向感'的 Dijkstra：不仅看已经走了多远 g，还看还剩多远（估计）h，总代价 f=g+h 最小者优先扩展，于是搜索'偏向终点方向'而不是四面八方平推。启发函数越接近真实距离，扩展的节点越少，搜索越高效。若 h≡0，A* 退化为 Dijkstra；若边权全 1 且 h≡0，则是 BFS。

### 原理 · Principle

可采纳性（admissible）：0≤h≤h* 保证首次弹出终点时 g 即最短距离——因为所有未扩展节点 f=g+h≤g+h*=真实最短距离，不会出现比当前更短却未弹出的路径。一致性（consistent）：h(x)≤h(y)+d(x,y)（三角不等式）保证已弹出节点不会被再次入队，且每个节点只扩展一次，这使 A* 效率更高。最坏情况下 A* 会扩展所有满足 f(x)≤C* 的节点（C* 为最短距离），因此 h 越接近 h* 分支越少，可看作一种'剪枝'。

### 历史 · History

A* 由 Hart、Nilsson 与 Raphael 于 1968 年提出（斯坦福人工智能实验室），是人工智能规划搜索的奠基算法。其最优性与可采纳性的证明（1972 完善）成为启发式搜索的理论基石，后被大量游戏 AI、路径规划、机器人领域采用。

## How · 实现

### 伪代码

```python
# A* 主循环
open_heap = 优先队列, 按 f = g + h 排序
push (f(start), g=0, start)
came[start] = None

while open_heap 非空:
    u = pop 最小f
    if u == goal: 回溯输出路径
    for v in neighbors(u):
        ng = g[u] + w(u,v)
        if ng < g[v]:
            g[v] = ng
            came[v] = u
            push (ng + h(v), ng, v)

# 可采纳性要求: h(v) <= 真实距离(v->goal)
# 8数码启发: h = 曼哈顿距离和
```

### Python 实现

```python
import heapq

GOAL = "123804765"


def manhattan(state):
    """曼哈顿距离启发: 每个数字到目标位置的距离和
    可采纳且一致(8数码经典启发)
    """
    d = 0
    for i, ch in enumerate(state):
        if ch != '0':
            gi = GOAL.index(ch)
            d += abs(i // 3 - gi // 3) + abs(i % 3 - gi % 3)
    return d


def neighbors(state):
    """空格0与上下左右数字交换"""
    i = state.index('0')
    r, c = i // 3, i % 3
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            j = nr * 3 + nc
            lst = list(state)
            lst[i], lst[j] = lst[j], lst[i]
            yield ''.join(lst)


def inversion_count(state):
    s = [int(c) for c in state if c != '0']
    inv = 0
    for i in range(len(s)):
        for j in range(i + 1, len(s)):
            if s[i] > s[j]:
                inv += 1
    return inv


def solvable(state):
    """8数码可解性: 逆序数奇偶性与目标一致(空格移动不改变奇偶)"""
    return (inversion_count(state) - inversion_count(GOAL)) % 2 == 0


def a_star(start):
    """A* 解8数码: 返回(步数, 状态路径); 不可解返回 None
    目标 123804765
    """
    if not solvable(start):
        return None
    open_heap = [(manhattan(start), 0, start)]
    gscore = {start: 0}
    came = {start: None}
    while open_heap:
        _, g, u = heapq.heappop(open_heap)
        if g > gscore.get(u, float('inf')):
            continue  # 跳过过期条目
        if u == GOAL:
            path = []
            while u is not None:
                path.append(u)
                u = came[u]
            return g, path[::-1]
        for v in neighbors(u):
            ng = g + 1
            if ng < gscore.get(v, float('inf')):
                gscore[v] = ng
                came[v] = u
                heapq.heappush(open_heap, (ng + manhattan(v), ng, v))
    return None


if __name__ == "__main__":
    # 已就位: 0 步
    r = a_star(GOAL)
    assert r is not None and r[0] == 0

    # 经典可解实例
    r = a_star("283104765")
    assert r is not None and r[1][-1] == GOAL
    # 验证路径每一步合法且最短
    for a, b in zip(r[1], r[1][1:]):
        assert b in neighbors(a)

    # 不可解实例
    assert a_star("123804756") is None

    # 可解性判定抽查
    assert not solvable("123804756")
    assert solvable("283104765")

    print(f"astar all tests passed (sample path length: {r[0]})")

```

**PyPy 提示**: 8数码状态用字符串作为 dict 键可读性好但开销大；追求性能可编码为整数（3^9 位或数位压缩）。PyPy 下 heapq + dict 性能足够 8数码/15数码小规模。k短路等大规模问题纯 Python 易 TLE，建议换 C++。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 取决于启发函数：h=0 退化为 Dijkstra O(E log V)；h=h* 时 O(V)；一般介于两者之间 |
| 空间 | O(扩展节点数)，比 IDA* 大（需存 open/closed 表） |

### 局限

h 不满足可采纳性时无最优性保证；状态数巨大时 open 表内存爆炸（此时用 IDA*）；需要目标状态已知且能设计良好启发函数；h 非一致时需允许节点重复入队（用 g 松弛）。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1379 | 3 | 八数码难题：A*经典题，曼哈顿距离启发（目标123804765） | [https://www.luogu.com.cn/problem/P1379](https://www.luogu.com.cn/problem/P1379) |
| OI Wiki | kth-path | 4 | k短路：A* 求 k 短路（次短路），h 用反向图最短路 | [https://oi-wiki.org/graph/kth-path/](https://oi-wiki.org/graph/kth-path/) |

## Pitfalls · 易错点

- h 必须可采纳(不高估)，否则 A* 失去最优性保证
- h 非一致(不满足三角不等式)时，节点可能重复入队，需按 g 松弛处理
- 弹出时若忘记跳过过期条目，可能用旧 g 值扩展导致错误
- 8数码无解状态(逆序奇偶不同)要先判定，否则 A* 无限搜索
- 状态哈希的编码开销在纯 Python 下可能成为瓶颈

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/search/astar/](https://oi-wiki.org/search/astar/)
- 书籍 ✓ `CPH ch25 (k shortest paths), 附录 A* 相关`
