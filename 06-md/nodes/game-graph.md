---
id: game-graph
name: 博弈图与必胜必败态
group: G-E-6
stage: intermediate
priority: P1
depth_tier: standard
---

# 博弈图与必胜必败态

> 把公平组合游戏的状态画成有向无环图：无后继态为 P（先手必败）；存在后继为 P 的是 N（必胜）；所有后继都是 N 的才是 P；O(\|V\|+\|E\|) 逆拓扑标记

<!-- 元信息: id=game-graph · group=G-E-6 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

博弈图：公平组合游戏的所有状态作为顶点，状态 x 到后继 y 连有向边（一次合法操作）。若游戏有限且无平局，博弈图是有向无环图（DAG）。必胜必败态（N/P 态）由归纳规则定义：① 无后继的状态是 P 态（先手无路可走而失败）；② 存在至少一个后继为 P 的状态是 N 态；③ 所有后继都是 N 的状态是 P 态。通过逆拓扑序（从出度为 0 的顶点开始反图 BFS）可在 O(|V|+|E|) 内标记所有状态。该框架是 Nim 定理、SG 函数与有向图游戏的共同基础。

## Why · 为什么

### 直觉 · Intuition

把整个游戏倒着看：终点状态是'已知输'（P）。一个状态只要有一条通向'已知输'的路，先手走那条路就赢（N）。如果一个状态的所有出口都通向'对手能赢'，那无论先手怎么走都会输（P）。这就成了图上反向传播的标注过程——像在 DAG 上倒着染色。

### 原理 · Principle

三条规则构成良定义归纳：对 DAG 按拓扑序反向处理，每个状态的后继都已被标好。N/P 互斥且完备：任何非空后继集合要么含 P（则本身 N），要么全 N（则本身 P）。用反图 + 队列实现：初始把出度为 0 的点标 P 入队；弹出 u，对每个前驱 v：若 u 是 P 则 v 直接标 N；若 u 是 N 则给 v 的出度减一，v 的出度归零时（其所有后继都已知为 N）标 P。复杂度 O(V+E)。与 SG 的联系：SG=0 ⟺ P 态，SG≠0 ⟺ N 态。

### 历史 · History

N/P 态的归纳刻画是组合博弈论最古老也最基础的结论，可追溯至 Zermelo（1913）关于棋类博弈无平局可判定的思想，Bouton（1901）在 Nim 的证明中已隐含使用，Sprague/Grundy 的 SG 理论将其数值化为 mex。OI Wiki 在 impartial-game 页『博弈图和状态』一节系统介绍，是理解后续所有博弈算法的入口。

## How · 实现

### 伪代码

```python
# DAG 上标记 N/P 态（逆拓扑 + 反图队列）
indeg_out = [len(succ[u]) for u]      # 出度
state = [未知] * V                     # -1=P, 1=N
queue = [u for u in V if outdeg[u]==0]
for u in queue: state[u] = P
while queue:
  u = queue.pop(0)
  for v in pred[u]:                   # 反图
    if state[v] != 未知: continue
    if state[u] == P: state[v] = N; queue.append(v)
    else:
      outdeg[v] -= 1
      if outdeg[v] == 0: state[v] = P; queue.append(v)
```

### Python 实现

```python
from collections import deque


def classify_dag(n, graph):
    """在 DAG 上标记全部状态的 N/P 态。
    graph[u] = u 的后继列表。
    返回 state: 1=先手必胜(N), -1=先手必败(P)。
    """
    outdeg = [len(graph[u]) for u in range(n)]
    pred = [[] for _ in range(n)]
    for u in range(n):
        for v in graph[u]:
            pred[v].append(u)

    state = [0] * n
    q = deque()
    for u in range(n):
        if outdeg[u] == 0:
            state[u] = -1
            q.append(u)
    while q:
        u = q.popleft()
        for v in pred[u]:
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
    # 链式博弈 0->1->2->3（终点 3 无后继）
    g1 = [[1], [2], [3], []]
    s1 = classify_dag(4, g1)
    assert s1 == [1, -1, 1, -1], s1

    # 取 1 或 2 个石子的单堆游戏：状态 k 有后继 k-1,k-2
    g2 = [[], [0], [0, 1], [1, 2], [2, 3], [3, 4]]
    s2 = classify_dag(6, g2)
    assert s2 == [-1, 1, 1, -1, 1, 1], s2  # SG: 0,1,2,0,1,2

    # 与 SG 表交叉验证：取 1..K 的游戏 SG(k)=k%(K+1)，N 态 ⟺ SG≠0
    def sg_win(k, K):
        return k % (K + 1) != 0

    for K in [1, 2, 3]:
        g = [[max(0, k - d) for d in range(1, K + 1) if k >= d] for k in range(12)]
        s = classify_dag(12, g)
        for k in range(12):
            assert (s[k] == 1) == sg_win(k, K), (K, k, s[k])

    print("All tests passed.")
```

**PyPy 提示**: DAG 顶点可到 1e6、边 1e6，用 list 存邻接表与反图即可，PyPy 下 BFS O(V+E) 约 1s。state 用 -1/0/1 整数数组省内存。若只需判定单点胜负也可用记忆化 DFS，但逆拓扑 BFS 更稳定无递归深度风险。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(\|V\|+\|E\|) |
| 空间 | O(\|V\|+\|E\|) |

### 局限

要求博弈图为 DAG（无平局、有限步）。若图有环（存在平局可能），N/P 标记会漏掉平局态，需用 game-on-graph 的三分类算法。状态空间巨大时（如连续量的 Nim 变体）无法显式建图，只能找规律或转 SG。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P2197 | 2 | Nim 模板：Nim 和判定的背后就是博弈图 P/N 归纳，理解该题即理解本节点 | [https://www.luogu.com.cn/problem/P2197](https://www.luogu.com.cn/problem/P2197) |
| Luogu | P6560 | 6 | [SBCOI2020] 时光的流逝：有环图上带必胜/必败/平局的博弈（game-on-graph 分类的 DAG 简化版前置） | [https://www.luogu.com.cn/problem/P6560](https://www.luogu.com.cn/problem/P6560) |

## Pitfalls · 易错点

- P 态定义是『所有后继都是 N』，不是『存在后继是 N』（后者是 N 态）
- 标记过程必须用反图（pred），正图会漏更新
- 出度为 0 的顶点初始化为 P 态，别忘了入队
- 有环图不能直接跑该算法（会残留未知状态当作 P 导致错误），需三分类
- state 用 0 表示未定，注意与真实 P(-1)/N(1) 区分
- 若状态含大量未达态（孤点）要按真实出度处理

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/game-theory/impartial-game/](https://oi-wiki.org/math/game-theory/impartial-game/)
- OI Wiki ✓ [https://oi-wiki.org/math/game-theory/intro/](https://oi-wiki.org/math/game-theory/intro/)
- 书籍 ✓ `CPH ch25 Game theory, pp.245-252`
