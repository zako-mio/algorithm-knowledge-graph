---
id: max-clique
name: 最大团
group: G-B-9
stage: advanced
priority: P3
depth_tier: brief
---

# 最大团

> NP-hard，Bron-Kerbosch回溯或状压DP

<!-- 元信息: id=max-clique · group=G-B-9 · stage=advanced · priority=P3 · depth_tier=brief -->

## What · 是什么

团（clique）是无向图中两两相邻的顶点子集（完全子图）。极大团（maximal clique）是不能再加入任何顶点仍保持团的团；最大团（maximum clique）是所有极大团中顶点数最多的一个，即最大完全子图。求最大团问题是经典的 NP-hard 问题，一般规模下用 Bron–Kerbosch 回溯搜索或折半/状压 DP，小规模（n≤40 左右）可用折半枚举，n 很大时只能靠启发式。最大团与最大独立集互补：独立集指两两不相邻的顶点集，在图 G 的补图（边变非边）上，G 的团就是补图的独立集，反之亦然。

## Why · 为什么

### 直觉 · Intuition

最大团的核心困难在于：你不知道某个顶点最终是否属于最大团。Bron–Kerbosch 用三个集合 R/P/X 递归：R 是当前已经选入的团，P 是仍可与 R 中所有点相邻的候选点，X 是已被排除（曾经尝试过）的点。每次从 P 取一个点 v 加入 R 并递归（同时用 N(v) 收紧 P 和 X），随后把 v 从 P 移入 X，避免重复枚举同一团。当 P 与 X 同时为空，R 就是极大团，记录其大小。枚举所有极大团后取最大者即最大团。

### 原理 · Principle

正确性依赖：任何包含当前 R 的极大团，其下一步加入的点必然来自 P∩N(v)；把 v 从 P 移到 X 保证每种'哪一步选哪个点'的选择只被枚举一次，避免重复。优化：选 pivot 点 u（P∪X 中的点），只枚举 P\N(u) 中的点——因为含 u 的极大团若再加一个与 u 相邻的点，则只需枚举 u 本身即可覆盖，这样大幅剪枝。另一个常见优化是按度数排序并加剪枝（当前 R 大小 + 剩余候选数 ≤ 已知最优则剪掉）。

### 历史 · History

团问题起源于图论（1930 年代 Ramsey 理论的相关问题），Bron–Kerbosch 算法由 Coen Bron 与 Joep Kerbosch 于 1973 年提出，至今仍是枚举所有极大团的标准算法。最大团问题的 NP-hard 性在 1972 年 Karp 的 21 个 NP-complete 问题列表中得到确认（顶点覆盖/独立集/团归约）。

## How · 实现

### 伪代码

```python
BronKerbosch(R, P, X):
    if P and X are both empty:
        报告 R 为一个极大团; 更新全局最大团大小
    u = 从 P ∪ X 中选 pivot
    for v in P \ N(u):
        BronKerbosch(R ∪ {v}, P ∩ N(v), X ∩ N(v))
        P = P \ {v}
        X = X ∪ {v}
```

### Python 实现

```python
def max_clique(n, adj):
    """Bron-Kerbosch with pivot 求无向图最大团大小.
    adj: 邻接表, n 个点(0-index), adj[i] 为集合.
    """
    best = 0
    cur = []

    def bk(R, P, X):
        nonlocal best
        if not P and not X:
            best = max(best, len(R))
            return
        # 剪枝: 当前团大小 + 候选数 <= best 则不可能超越
        if len(R) + len(P) <= best:
            return
        # 选 pivot: 使 P \ N(u) 尽量小
        u = next(iter(P | X))
        for v in list(P - adj[u]):
            bk(R | {v}, P & adj[v], X & adj[v])
            P.discard(v)
            X.add(v)

    bk(set(), set(range(n)), set())
    return best


if __name__ == "__main__":
    # 三角形 0-1-2-0
    adj = [
        {1, 2},
        {0, 2},
        {0, 1},
    ]
    assert max_clique(3, adj) == 3

    # 四边形 + 一条对角线 => 最大团为三角形
    adj2 = [
        {1, 2, 3},
        {0, 2},
        {0, 1, 3},
        {0, 2},
    ]
    assert max_clique(4, adj2) == 3

    # 空图 => 1
    adj3 = [set() for _ in range(5)]
    assert max_clique(5, adj3) == 1

    # 完全图 K5 => 5
    adj4 = [set(range(5)) - {i} for i in range(5)]
    assert max_clique(5, adj4) == 5

    print("max-clique tests passed")

```

**PyPy 提示**: Python 实现用 set 交集方便但常数大，n 稍大（>50）会非常慢。竞技中最大团常直接交 C++ 模板；若 Python 必写，小规模（n≤30~40）建议折半枚举（meet-in-the-middle）或 bitset 优化邻接矩阵。n=1 时答案应为 1（单点本身是团）。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 最坏指数级（枚举所有极大团，n 很大时不可接受）；带 pivot 的 Bron–Kerbosch 在一般图上通常远快于最坏情况 |
| 空间 | O(n + 递归深度)，递归深度最坏 O(n) |

### 局限

NP-hard：n 较大时无多项式算法；回溯在稠密图/大 n 下必然超时；最大独立集/顶点覆盖可互化但复杂度同样是指数级。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| POJ | 2989 | 4 | All Friends：Bron–Kerbosch 模板题，求所有极大团的个数 | [http://poj.org/problem?id=2989](http://poj.org/problem?id=2989) |
| Luogu | U461211 | 4 | 数据加强版字符串 Hash：卡碰撞/随机化相关，可与团无关，用于对比哈希与精确判定 | [https://www.luogu.com.cn/problem/U461211](https://www.luogu.com.cn/problem/U461211) |

## Pitfalls · 易错点

- Bron–Kerbosch 忘记 pivot 优化在一般图上会指数爆炸，务必剪枝
- P 与 X 同时为空才记录极大团，只判 P 空会重复计数/漏解
- 孤立点构成的'团'大小为 1，边界不能判 0
- 与最大独立集互补：别忘了补图转换
- Python 的 set 交集在递归中反复构造开销大，n>50 建议换 C++

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/max-clique/](https://oi-wiki.org/graph/max-clique/)
- Wikipedia ✓ [https://en.wikipedia.org/wiki/Clique_problem](https://en.wikipedia.org/wiki/Clique_problem)
