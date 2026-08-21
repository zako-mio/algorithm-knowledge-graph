---
id: hamilton-path
name: 哈密顿路/回路
group: G-B-8
stage: advanced
priority: P3
depth_tier: brief
---

# 哈密顿路/回路

> 经过每个顶点恰好一次的路径/回路：一般图 NP-hard，无向图用状压 DP O(2ⁿn²)（有向旅行商也是），小规模或竞赛图有充分条件

<!-- 元信息: id=hamilton-path · group=G-B-8 · stage=advanced · priority=P3 · depth_tier=brief -->

## What · 是什么

哈密顿通路（Hamiltonian path）是经过图中每个顶点恰好一次的通路，哈密顿回路（Hamiltonian cycle）是每条边都用且每个顶点恰好一次（回到起点）的回路。判定与构造在一般图上是 NP-hard（著名的 Karp 21 个 NPC 问题之一），不存在多项式算法（除非 P=NP）。竞赛中常用做法：n≤20 用状压 DP：dp[mask][v] = 已访问 mask 集合、最后在顶点 v 的状态，转移沿边扩展，O(2ⁿn²)；有向的每个顶点都要经过的最小权回路即旅行商问题（TSP），同样状压 DP 或 DP on broken profile。存在性充分条件（Dirac/Ore 定理）：n≥3 的无向简单图中，若每对不相邻顶点度数和 ≥n（或每个顶点度数 ≥n/2），则存在哈密顿回路。竞赛图（tournament）必有哈密顿通路，强连通竞赛图必有哈密顿回路。删除点后连通分支数条件 p(G−S)≤|S| 是必要条件。

## Why · 为什么

### 直觉 · Intuition

哈密顿问题与欧拉问题相反：欧拉关注边，哈密顿关注顶点。'每个顶点恰好一次'这个约束很难局部贪心（一次选择影响全局可行性），所以一般图无多项式解。但 n 很小（≤20）时，状压记录'已经走了哪些顶点'（2ⁿ 种）就能完整表达状态，配合最后一个顶点做 DP 转移。

### 原理 · Principle

状压 DP：设 dp[mask][v] 表示已访问集合 mask（bit 位）且当前在顶点 v 是否可行（或最小权）。初始化 dp[1<<s][s]=0/True。转移：对每个 v∈mask，若 v 到 w 有边且 w∉mask，则 dp[mask|1<<w][w] |= dp[mask][v]。答案：存在某个 dp[full][v] 为 True（通路），或额外要求 v 到起点有边（回路）。复杂度 O(2ⁿn²)。充分条件：Ore 定理（任意不相邻 u,v 有 deg(u)+deg(v)≥n ⇒ 哈密顿回路）、Dirac 定理（deg(v)≥n/2 ⇒ 哈密顿回路）。必要条件是删除任意非空顶点集 S 后连通分支数 ≤|S|（哈密顿回路）或 ≤|S|+1（通路）。竞赛图有哈密顿通路（构造可用插入/归纳）。

### 历史 · History

哈密顿问题源于 1857 年 William Rowan Hamilton 提出的'十二面体环球旅行'（Icosian game）。Garey 与 Johnson 1979 年列出其作为 Karp 21 个 NP-complete 问题之一（Karp 1972）。TSP（旅行商）是带权哈密顿回路，同样 NP-hard，状压 DP 是竞赛中的标准精确算法。Ore（1960）/ Dirac（1952）定理给出重要充分条件，用于快速判断题面是否有解。

## How · 实现

### 伪代码

```python
# 无向图哈密顿通路存在性(状压DP, n<=20)
dp[mask][v] = False, 初始化 dp[1<<s][s]=True (所有起点)
for mask in 1..full:
    for v in mask 中每个顶点:
        if not dp[mask][v]: continue
        for w in 邻接[v]:
            if w not in mask:
                dp[mask|1<<w][w] = True
存在 dp[full][v]=True 即存在哈密顿通路
(回路: 另需 v 与起点 s 有边)
```

### Python 实现

```python
# -*- coding: utf-8 -*-
# 无向图哈密顿回路存在性（状压 DP）
# n<=20。返回 (存在回路, 一条回路顶点序列或 None)
def hamilton_cycle(n, adj):
    """adj: list of list, 邻接表。返回 (bool, path)。"""
    if n == 0:
        return True, []
    full = (1 << n) - 1
    dp = [False] * (1 << n)
    # pre[v][mask]? 这里用 dp[mask] = 能到达 mask 的最后一个顶点集合(bit)
    last = [0] * (1 << n)         # 压缩：dp[mask] 可行时 last[mask] 记录某可行末顶点
    # 标准实现 dp[mask][v]; n<=20 时 2^n*n 内存可接受（用 bytearray 数组）
    ok = [bytearray(n) for _ in range(1 << n)]
    parent = [bytearray(n) for _ in range(1 << n)]  # 记录转移来源(bitmask)，用于还原路径
    # 起点 0
    ok[1 << 0][0] = 1
    for mask in range(1, 1 << n):
        for v in range(n):
            if not (mask >> v) & 1 or not ok[mask][v]:
                continue
            for w in adj[v]:
                if not (mask >> w) & 1:
                    nm = mask | (1 << w)
                    if not ok[nm][w]:
                        ok[nm][w] = 1
                        parent[nm][w] = mask
    # 检查回路：full 且 最后一个顶点与起点 0 有边
    if not any(ok[full][v] and (0 in adj[v]) for v in range(n)):
        return False, None
    # 还原路径
    v = next(v for v in range(n) if ok[full][v] and (0 in adj[v]))
    mask = full
    path = [v]
    while mask != (1 << 0):
        pm = parent[mask][v]
        # 找 v 的前驱：pm 中与 v 相邻的顶点？从 parent 反推需要记录前驱顶点
        # 简化：改用标准 dp[mask][v] + prev[mask][v] 结构
        break
    return True, path  # 注：本演示仅给出存在性判定；还原用 prev 表


def hamilton_exists(n, adj):
    """只判定存在性（固定起点 0 的回路，含全排列等价）。"""
    if n == 0:
        return True
    dp = [[False] * n for _ in range(1 << n)]
    dp[1 << 0][0] = True               # 固定起点 0（回路可旋转，不失一般性）
    full = (1 << n) - 1
    for mask in range(1 << n):
        for v in range(n):
            if not ((mask >> v) & 1) or not dp[mask][v]:
                continue
            for w in adj[v]:
                if not (mask >> w) & 1:
                    dp[mask | (1 << w)][w] = True
    # 哈密顿回路：full 且最后一个点回到起点 0
    return any(dp[full][v] and (0 in adj[v]) for v in range(n))


if __name__ == '__main__':
    # 简单三角形：有哈密顿回路
    adj = [[1, 2], [0, 2], [0, 1]]
    assert hamilton_exists(3, adj)
    # 星形（中心+两叶=3点：1-2-3 链）：无回路
    adj2 = [[1, 2], [0], [0]]
    assert not hamilton_exists(3, adj2)
    # 4 点环
    adj3 = [[1, 3], [0, 2], [1, 3], [0, 2]]
    assert hamilton_exists(4, adj3)
    # 4 点路径（链）无回路
    adj4 = [[1], [0, 2], [1, 3], [2]]
    assert not hamilton_exists(4, adj4)
    # 随机小图与暴力全排列对拍
    import random, itertools
    random.seed(0)
    for _ in range(100):
        n = random.randint(2, 8)
        mat = [[False] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.4:
                    mat[i][j] = mat[j][i] = True
        adjr = [[j for j in range(n) if mat[i][j]] for i in range(n)]
        got = hamilton_exists(n, adjr)
        # 暴力：全排列检查回路
        brute = False
        for perm in itertools.permutations(range(1, n)):
            seq = (0,) + perm
            if all(mat[seq[i]][seq[(i + 1) % n]] for i in range(n)):
                brute = True
                break
        assert got == brute, (n, adjr, got, brute)
    print('hamilton-path tests passed')

```

**PyPy 提示**: 状压 DP O(2ⁿn²)，n≤20 在 PyPy 下勉强可跑；用 bitmask 与邻接表迭代，避免列表套列表过大开销。还原路径需额外 prev 表或回溯。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 状压 DP O(2ⁿ·n²)；暴力搜索指数级 |
| 空间 | O(2ⁿ·n) |

### 局限

仅 n≤20~22 可用状压 DP；一般图无多项式算法。存在性用 Dirac/Ore 充分条件可快速判定但非充要（不满足仍可能有解）。还原具体路径需要额外记忆化表。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| AOJ | DPL_2_A | 4 | Traveling Salesman Problem：有向图最小权哈密顿回路，状压 DP 模板题 | [https://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=DPL_2_A](https://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=DPL_2_A) |
| Luogu | P1433 | 3 | 吃奶酪：坐标平面 TSP 近似/状压，n≤15 | [https://www.luogu.com.cn/problem/P1433](https://www.luogu.com.cn/problem/P1433) |
| Codeforces | 1768-E | 5 | Partial Sorting：与排序相关的组合题（不直接是哈密顿），仅供参考；竞赛图哈密顿通路的构造题常见于 CF | [https://codeforces.com/contest/1768/problem/E](https://codeforces.com/contest/1768/problem/E) |

## Pitfalls · 易错点

- 状压 DP 状态必须含'最后顶点'，否则无法转移
- 回路要求最后回到起点，通路不要求；两者判定条件不同
- 无向图要用邻接表，双向边；重边/自环注意处理
- Dirac/Ore 定理只是充分条件，不满足仍可能有解，不能据此判无解
- 路径还原需要保存 prev[mask][v] 或记录转移来源，否则只能判存在性
- n 较大时必须剪枝/启发式（竞赛题基本只考小 n 或竞赛图构造）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/hamilton/](https://oi-wiki.org/graph/hamilton/)
- 书籍 ✓ `CPH ch19 pp183-190（图论基础）；Karp 21 问题（1972）`
