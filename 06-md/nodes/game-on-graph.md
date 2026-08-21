---
id: game-on-graph
name: 有向图游戏
group: G-E-6
stage: advanced
priority: P1
depth_tier: standard
---

# 有向图游戏

> 在任意有向图（可能含环）上移动的博弈：利用反图 BFS + 出度归零技巧，O(\|V\|+\|E\|) 线性分类每个顶点为必胜/必败/平局态

<!-- 元信息: id=game-on-graph · group=G-E-6 · stage=advanced · priority=P1 · depth_tier=standard -->

## What · 是什么

有向图游戏：给定有向图 G（顶点为状态，边为移动），从起始顶点出发，玩家轮流沿出边移动一步，无法移动者判定胜/负（按规则）。与 Nim/SG 的 DAG 情形不同，这里图允许有环，因此存在平局（双方都不犯错则永不停机）。每个顶点有三种可能：先手必胜（W）、先手必败（L）、平局（D）。分类规则：无出边顶点按规则定 W/L；有出边指向 L 的 → W；所有出边都指向 W 的 → L；其余为 D（无法确定时游戏可在环上无限进行）。O(|V|+|E|) 算法用反图 BFS + 出度递减实现。

## Why · 为什么

### 直觉 · Intuition

和 DAG 博弈图一样的'反向传播'，但有环打破了完备性：环上的顶点可能既到不了 L 也不被全 W 包围，就会'卡'在 D。技巧是给每个顶点维护剩余出度数：从确定态（出度为 0）开始反向剥洋葱，剥不掉的剩下全是平局。环像'死区'，只有从确定态能'波及'到的顶点才被着色。

### 原理 · Principle

两条传播规则：① 从 L 态沿反边到达的未定顶点 → W（直接覆盖）；② 从 W 态沿反边到达的未定顶点，其出度减一，若出度归零（所有后继都已确认是 W）→ L。正确性：W 态的定义是有后继 L；L 态定义是所有后继 W。出度为 0 的顶点直接定 W 或 L（无移动者胜/负）。处理完队列后，剩余未定顶点既无到达 L 的出口（否则被标 W），又未被全 W 判定（否则出度会归零），只能形成环上循环 → D。该算法与拓扑排序同构，是 CP-Algorithms『Games on arbitrary graphs』与 OI Wiki 有向图游戏的推荐解法。

### 历史 · History

有环图博弈的胜负平局三分类是算法博弈论基础结论，其 O(m) 逆拓扑 BFS 技巧在竞赛中广泛用于『追及/移动棋子』类问题。CP-Algorithms 将其专章收录（'Games on arbitrary graphs'），OI Wiki 在有向图游戏一节给出同样流程，用于 Luogu P6560（时光的流逝）等题。

## How · 实现

### 伪代码

```python
# 输入: n 顶点，adj[u] 出边表，normal=True 表示无法移动者输（反常则取反初始）
outdeg[u] = len(adj[u]); 反图 radj
state[u] = 0 (未定), 1 (W), -1 (L)
queue ← 所有 outdeg==0 的 u，state[u] = -1 (无法移动者输，正常规则)
while queue:
  u = pop()
  for v in radj[u]:
    if state[v] != 0: continue
    if state[u] == -1:
      state[v] = 1; queue.push(v)
    else:
      outdeg[v] -= 1
      if outdeg[v] == 0:
        state[v] = -1; queue.push(v)
剩余 state==0 的顶点 → 平局 D
```

### Python 实现

```python
from collections import deque


def classify_cycles(n, adj, normal=True):
    """任意有向图（可含环）的胜负平局三分类。
    normal=True: 无法移动者输；False: 无法移动者赢（反常）。
    返回 state: 1=先手必胜, -1=先手必败, 0=平局。
    """
    outdeg = [len(adj[u]) for u in range(n)]
    radj = [[] for _ in range(n)]
    for u in range(n):
        for v in adj[u]:
            radj[v].append(u)

    state = [0] * n
    q = deque()
    for u in range(n):
        if outdeg[u] == 0:
            state[u] = -1 if normal else 1
            q.append(u)
    while q:
        u = q.popleft()
        for v in radj[u]:
            if state[v] != 0:
                continue
            if state[u] == -1:
                state[v] = 1
                q.append(v)
            else:
                outdeg[v] -= 1
                if outdeg[v] == 0:
                    state[v] = -1
                    q.append(v)
    return state


if __name__ == "__main__":
    # 无环：0->1->2->3（正常规则）
    s = classify_cycles(4, [[1], [2], [3], []])
    assert s == [1, -1, 1, -1], s

    # 纯环 0<->1：无出度 0 顶点，全部平局
    s2 = classify_cycles(2, [[1], [0]])
    assert s2 == [0, 0], s2

    # 环 1<->2 + 出口 2->3：3 输, 2 赢, 1 所有后继(2)赢→输, 0 赢
    s3 = classify_cycles(4, [[1], [2], [1, 3], []])
    assert s3[3] == -1 and s3[2] == 1 and s3[1] == -1 and s3[0] == 1, s3

    # 反常规则翻转无出边顶点的初值：无环链 0->1->2->3
    s4 = classify_cycles(4, [[1], [2], [3], []], normal=False)
    # 3: 无法移动者赢 → W(1)；2: 后继全 W → L；1: 有后继 L → W；0: L
    assert s4 == [-1, 1, -1, 1], s4

    print("All tests passed.")
```

**PyPy 提示**: 邻接表与反图各 O(V+E) 内存，PyPy 下 V,E=1e6 约 1-2s。用数组存 state（-1/0/1）避免 dict。若图极稀疏且只查单点，可记忆化搜索但需显式判环（三色标记），不如全量 BFS 稳。注意递归 DFS 在 1e6 顶点会爆栈，用迭代队列。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(\|V\|+\|E\|) |
| 空间 | O(\|V\|+\|E\|) |

### 局限

区分平局需要正确处理出度递减——漏减会误把环上点标成 L/W。反常规则（无法移动者赢）只需翻转初值。若有多个起点的目标型问题（类似追逐），建模时把目标态设为无出边即可。顶点数巨大但边稀疏时可只建可达子图。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P6560 | 6 | [SBCOI2020] 时光的流逝：有向图博弈三分类模板（正常规则），OI Wiki 习题 | [https://www.luogu.com.cn/problem/P6560](https://www.luogu.com.cn/problem/P6560) |
| CP-Algorithms | Games on arbitrary graphs 例题 | 6 | 官方章节：含环任意图上的 W/L/D 线性分类算法与证明 | [https://cp-algorithms.com/game_theory/games_on_graphs.html](https://cp-algorithms.com/game_theory/games_on_graphs.html) |
| Luogu | P6487 | 6 | [COCI 2010/2011] HRPA：阶梯型有向图博弈（OI Wiki 习题） | [https://www.luogu.com.cn/problem/P6487](https://www.luogu.com.cn/problem/P6487) |

## Pitfalls · 易错点

- 有环时不能直接当作 DAG 标记 N/P（残留未定会被误判），必须先跑出度归零流程
- 出度递减要放在 state[u]==1 分支，且检查归零后标 L；state[u]==-1 分支直接标 W 不递减
- 正常/反常规则决定无出边顶点的初值，别统一设 L
- 反图构建必须完整（每条正向边对应一条反向边）
- 平局态的判定是'流程结束仍 state==0'，不是在中间标记
- 多个测试用例共用一个图时 state/outdeg 要重新初始化

## Sources · 信源

- CP-Algorithms ✓ [https://cp-algorithms.com/game_theory/games_on_graphs.html](https://cp-algorithms.com/game_theory/games_on_graphs.html)
- OI Wiki ✓ [https://oi-wiki.org/math/game-theory/impartial-game/](https://oi-wiki.org/math/game-theory/impartial-game/)
