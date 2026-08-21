---
id: zero-sum-game
name: 零和博弈/Minimax
group: G-E-6
stage: advanced
priority: P1
depth_tier: standard
---

# 零和博弈/Minimax

> 序贯零和：V(s)=max/min{V(后继)} 递推，Minimax+Alpha-Beta 剪枝；同时零和：收益矩阵、混合策略与 von Neumann 极小极大定理

<!-- 元信息: id=zero-sum-game · group=G-E-6 · stage=advanced · priority=P1 · depth_tier=standard -->

## What · 是什么

零和博弈（zero-sum game）：一名玩家的收益恰为另一名玩家的损失（收益之和为 0）。两类：(1) 序贯零和（轮流行动）：局面 S 的博弈值 V(s)=v(s)（终止），V(s)=max{V(t)}（玩家 1 行动），V(s)=min{V(t)}（玩家 2 行动）——即 Minimax 递推；配合 Alpha-Beta 剪枝、记忆化可加速。(2) 同时零和：收益矩阵 V=(v(a1,a2))，纯策略未必有解（石头剪刀布），需混合策略（概率分布）；von Neumann 极小极大定理断言 max-min=min-max=w，双方最优混合策略的价值唯一，可化为线性规划求解。

## Why · 为什么

### 直觉 · Intuition

零和意味着'我赢多少=你输多少'，所以我可以只站在玩家 1 立场估值。序贯博弈中轮到谁谁就选对自己最有利的分支：自己走时取最大，对手走时取最小，把对手当成永远与自己作对的最优回应。同时博弈没有先后，就引入'随机出招'（混合策略），让对手无法针对性回应——概率加权后的收益由线性规划定出。

### 原理 · Principle

序贯情形：V(s) 的递推由逆拓扑/记忆化求解，正确性来自逆向归纳（backward induction）。Alpha-Beta：维护 α（已知的当前最佳下界，max 方）与 β（当前最佳上界，min 方），当 α≥β 时该分支不可能优于已得结果即剪枝；最佳顺序下剪枝率指数级。同时零和：设玩家 1 的混合策略为概率向量 s1，玩家 2 为 s2，玩家 1 期望收益 v(s1,s2)=s1^T V s2。von Neumann：存在 s1*,s2* 使 max_{s1} min_{s2} v = min_{s2} max_{s1} v = v(s1*,s2*)，称为纳什均衡（二人零和博弈的均衡恰为此极小极大点）；通过把内层写成线性约束可转 LP。

### 历史 · History

John von Neumann 于 1928 年证明二人零和博弈的极小极大定理，1944 年与 Morgenstern 合著《博弈论与经济行为》奠定博弈论学科。Minimax 思想可追溯至更早的棋类分析；Alpha-Beta 剪枝于 1950s 出现并在深蓝等棋类程序中发挥关键作用。John Nash 1950 年把均衡推广到一般博弈。OI Wiki 零和博弈页与 CPH 均收录序贯 Minimax 章节。

## How · 实现

### 伪代码

```python
# 序贯零和：树/图中按轮到谁取 max 或 min
# 用节点表示状态，叶为估值；递归记忆化
def minimax(node, maximizing):
  if node 是叶: return 估值(node)
  if maximizing: return max(minimax(c, False) for c in children)
  else:         return min(minimax(c, True)  for c in children)
# Alpha-Beta: 传入 alpha,beta，越界即剪枝
# 同时零和: 线性规划（numpy/scipy）求混合策略
```

### Python 实现

```python
def minimax(node, maximizing=True):
    """序贯零和博弈 Minimax。
    node 为叶子时是数值，否则是后继节点列表。
    返回玩家 1 的最优收益。
    """
    if isinstance(node, (int, float)):
        return node
    vals = [minimax(c, not maximizing) for c in node]
    return max(vals) if maximizing else min(vals)


def minimax_ab(node, maximizing, alpha, beta, node_id="root", memo=None):
    """Minimax + Alpha-Beta 剪枝（带记忆化）。
    memo: dict id -> 已算值，用于有环/重复子结构加速（需保证能终止）。
    """
    if memo is None:
        memo = {}
    if node_id in memo:
        return memo[node_id]
    if isinstance(node, (int, float)):
        return node
    if maximizing:
        best = float("-inf")
        for i, c in enumerate(node):
            val = minimax_ab(c, False, alpha, beta, f"{node_id}.{i}", memo)
            best = max(best, val)
            alpha = max(alpha, best)
            if beta <= alpha:  # 剪枝
                break
    else:
        best = float("inf")
        for i, c in enumerate(node):
            val = minimax_ab(c, True, alpha, beta, f"{node_id}.{i}", memo)
            best = min(best, val)
            beta = min(beta, best)
            if beta <= alpha:  # 剪枝
                break
    memo[node_id] = best
    return best


def solve_matrix_game(matrix):
    """同时零和：求解 2×n 或 m×2 矩阵博弈的混合策略价值 w（玩家 1）。
    用线性规划：max w  s.t. 对每个列 j: sum_i p_i*m_ij >= w, sum p_i=1, p>=0。
    这里用 scipy.optimize.linprog（依赖 numpy/scipy，竞赛常用手写消元）。
    """
    from scipy.optimize import linprog
    import numpy as np
    m = len(matrix)
    n_cols = len(matrix[0])
    # 变量 x = [p_1..p_m, w]
    c = [0.0] * m + [-1.0]          # 最小化 -w
    A_ub = []
    b_ub = []
    for j in range(n_cols):
        row = [-matrix[i][j] for i in range(m)] + [1.0]  # -sum p_i m_ij + w <= 0
        A_ub.append(row)
        b_ub.append(0.0)
    A_eq = [[1.0] * m + [0.0]]
    b_eq = [1.0]
    bounds = [(0, 1)] * m + [(None, None)]
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")
    if not res.success:
        return None
    w = res.x[-1]
    strat = res.x[:m]
    return w, strat


if __name__ == "__main__":
    # 叶子根
    assert minimax(5, True) == 5
    # max 节点
    assert minimax([1, 2], True) == 2
    assert minimax([1, 2], False) == 1
    # 2 层：max(min(3,7), min(1,9)) = max(3,1) = 3
    assert minimax([[3, 7], [1, 9]], True) == 3
    # 3 层
    assert minimax([[[5, 2], [8, 1]], [[3, 4], [6, 0]]], False) == 3

    # Alpha-Beta 与朴素一致
    assert minimax_ab([[3, 7], [1, 9]], True, float("-inf"), float("inf")) == 3

    # 同时零和：2x2 矩阵博弈价值
    # [[1, 3], [4, 2]]：混合策略价值 w=2.5, p=(0.5,0.5)
    if __import__("importlib").util.find_spec("scipy"):
        r = solve_matrix_game([[1, 3], [4, 2]])
        if r:
            w, strat = r
            assert abs(w - 2.5) < 1e-6, w
            assert abs(strat[0] - 0.5) < 1e-6 and abs(strat[1] - 0.5) < 1e-6
        print("scipy matrix game OK")
    else:
        print("scipy 未安装，跳过同时零和 LP 验证（核心 Minimax 已验证）")

    print("All tests passed.")
```

**PyPy 提示**: Minimax 用记忆化避免重复子结构（关键：很多博弈状态可合并）。Alpha-Beta 剪枝在最优分支顺序下效率最高，分支排序按启发式（如先评估更有利的后继）。同时零和的 LP 求解竞赛中通常手写（单纯形/消元）或用 numpy；纯 Python 下 2×n 可枚举策略概率解析。矩阵博弈价值有上下界 w∈[min col max, max row min]。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | Minimax 全树 O(b^d)；Alpha-Beta 最佳 O(b^(d/2))、最差 O(b^d)；记忆化可降至 O(状态数·分支)；LP O(多项式) |
| 空间 | O(状态数)（记忆化）或 O(d)（无记忆化） |

### 局限

序贯 Minimax 要求状态图无环或可记忆化终止，否则需要类似 game-on-graph 的平局处理。Alpha-Beta 对分支顺序敏感。同时零和 LP 需要混合策略（纯策略可能无均衡）；大矩阵 LP 在竞赛环境下实现成本高。非零和博弈（双矩阵博弈）不能用单一 minimax 价值描述。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Codeforces | 794 E. Choosing Carrot | 7 | 序贯零和区间 DP：f(l,r,1)=max{...}, f(l,r,2)=min{...}，OI Wiki 例题（优化到 O(n)） | [https://codeforces.com/problemset/problem/794/E](https://codeforces.com/problemset/problem/794/E) |
| Luogu | P2734 | 4 | [USACO3.3] 游戏 A Game：区间取数零和 DP 模板（minimax 区间形式） | [https://www.luogu.com.cn/problem/P2734](https://www.luogu.com.cn/problem/P2734) |
| Codeforces | 388 C. Fox and Card Game | 5 | 两侧取牌博弈：中心对称策略 + minimax 思路（OI Wiki 习题） | [https://codeforces.com/problemset/problem/388/C](https://codeforces.com/problemset/problem/388/C) |

## Pitfalls · 易错点

- minimax 树中玩家轮次决定取 max 还是 min，递归参数 (not maximizing) 别写反
- Alpha-Beta 剪枝条件 beta<=alpha，且必须更新 alpha/beta 后才比较
- 同时零和的纯策略可能不存在（石头剪刀布），此时不能直接说'有纯策略均衡'
- LP 模型符号：玩家 1 求 max w，约束 sum_i p_i m_ij >= w（对每列），转 linprog 时把不等式乘 -1
- 记忆化 key 要包含轮到谁（同一状态不同行动者值不同）
- 叶节点估值是玩家 1 视角，玩家 2 的收益是 -v

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/game-theory/zero-sum-game/](https://oi-wiki.org/math/game-theory/zero-sum-game/)
- OI Wiki ✓ [https://oi-wiki.org/math/game-theory/intro/](https://oi-wiki.org/math/game-theory/intro/)
- 书籍 ✓ `CPH ch25 Game theory（含 minimax 区间 DP 例子）`
