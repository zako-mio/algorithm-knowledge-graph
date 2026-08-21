---
id: minimax-alpha-beta
name: Minimax/Alpha-Beta剪枝
group: G-A-14
stage: intermediate
priority: P2
depth_tier: standard
---

# Minimax/Alpha-Beta剪枝

> 博弈对抗搜索，Alpha-Beta剪枝减少不必要分支

<!-- 元信息: id=minimax-alpha-beta · group=G-A-14 · stage=intermediate · priority=P2 · depth_tier=standard -->

## What · 是什么

Minimax（极小化极大）是双人零和完全信息博弈的对抗搜索算法：我方（MAX）选择使自己分数最大的走法，对方（MIN）选择使我方分数最小的走法，自底向上回溯求得双方最优策略下我方能保证的分数。Alpha-Beta 剪枝在搜索中维护 α（MAX 玩家可保证的分数下界）与 β（MIN 玩家可保证的上界），当某节点出现 α≥β 时，其剩余分支不可能被双方理性选择，直接剪掉，从而大幅减少搜索量。

## Why · 为什么

### 直觉 · Intuition

下棋时想'我走这步，对手会怎么回应，我再看……'——Minimax 就是把这层推理推到尽头：MAX 层取最大、MIN 层取最小。Alpha-Beta 的洞见是：一旦发现对手有更好的选择(β)，我这条路就不可能被采用，后面的分支不必再看。例如根节点已有分支保底 15，看新分支发现对手能压到 1，那这个分支后面的 12/20/22 都不必看了。

### 原理 · Principle

Minimax 值递归定义：叶子为静态估值，MAX 节点取子节点最大值，MIN 节点取最小值。Alpha-Beta 中 α 为'MAX 已能保证的下界'，β 为'MIN 已能保证的上界'，初始 α=-∞, β=+∞ 下传；MAX 节点更新 α=max，MIN 节点更新 β=min；当 α≥β 时剪枝。剪枝保证根节点值不变（等价于完整 minimax），且搜索顺序越好剪枝越有效，最优顺序下复杂度从 O(b^d) 降至 O(b^{d/2})。负极大值（negamax）形式可统一两种节点。

### 历史 · History

Minimax 思想源于博弈论（von Neumann 1928 年极小极大定理）。Alpha-Beta 剪枝 1950s 由 John McCarthy 团队在 MIT 提出并命名，成为国际象棋程序（Deep Blue）的基础技术。Knuth & Moore 于 1975 年给出其复杂度的严格分析（负极大形式与最坏情况），是博弈 AI 的奠基算法。

## How · 实现

### 伪代码

```python
# Negamax 统一形式
score = minimax(state, depth, alpha, beta, is_max)

if 终局/到达深度: return 静态估值
if is_max:  # MAX节点
    for each move:
        alpha = max(alpha, minimax(child, alpha, beta, False))
        if alpha >= beta: break   # 剪枝
    return alpha
else:  # MIN节点
    for each move:
        beta = min(beta, minimax(child, alpha, beta, True))
        if alpha >= beta: break   # 剪枝
    return beta
```

### Python 实现

```python
LINES = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]


def evaluate(state):
    """终局判定: 1=max(X)赢, -1=max输, 0=平; 未终局返回None"""
    for a, b, c in LINES:
        if state[a] == state[b] == state[c] and state[a] != '.':
            return 1 if state[a] == 'X' else -1
    if '.' not in state:
        return 0
    return None


def minimax(state, is_max):
    """Minimax: 井字棋, X=MAX, O=MIN, 返回MAX可保证分数"""
    e = evaluate(state)
    if e is not None:
        return e
    if is_max:
        best = -2
        for i in range(9):
            if state[i] == '.':
                ns = state[:i] + 'X' + state[i+1:]
                best = max(best, minimax(ns, False))
        return best
    else:
        best = 2
        for i in range(9):
            if state[i] == '.':
                ns = state[:i] + 'O' + state[i+1:]
                best = min(best, minimax(ns, True))
        return best


def alpha_beta(state, is_max, alpha, beta):
    """Alpha-Beta剪枝: 与minimax结果一致但剪去无效分支"""
    e = evaluate(state)
    if e is not None:
        return e
    if is_max:
        for i in range(9):
            if state[i] == '.':
                ns = state[:i] + 'X' + state[i+1:]
                alpha = max(alpha, alpha_beta(ns, False, alpha, beta))
                if alpha >= beta:
                    break  # 剪枝
        return alpha
    else:
        for i in range(9):
            if state[i] == '.':
                ns = state[:i] + 'O' + state[i+1:]
                beta = min(beta, alpha_beta(ns, True, alpha, beta))
                if alpha >= beta:
                    break  # 剪枝
        return beta


if __name__ == "__main__":
    # 空棋盘: 完美博弈下先手(X)是平局 -> 分数0
    assert minimax('.' * 9, True) == 0
    assert alpha_beta('.' * 9, True, -2, 2) == 0

    # X在中心, 轮到O: O应打平 -> 0
    s = '.....X...'
    assert minimax(s, False) == 0
    assert alpha_beta(s, False, -2, 2) == 0

    # X差一步连线(第1行XX.), 轮到X: 必胜 -> 1
    s = 'XX......O'
    assert minimax(s, True) == 1
    assert alpha_beta(s, True, -2, 2) == 1

    # O差一步连线(第1行OO.), 轮到O: 必胜(对X为-1) -> -1
    s = 'OO......X'
    assert minimax(s, False) == -1
    assert alpha_beta(s, False, -2, 2) == -1

    # 终局
    assert minimax('XXX......', True) == 1
    assert minimax('OOO......', True) == -1

    # 交叉验证所有中间局面
    def gen_states(depth):
        res = []
        def rec(s, d, turn):
            res.append(s)
            if d == depth:
                return
            for i in range(9):
                if s[i] == '.':
                    rec(s[:i] + turn + s[i+1:], d + 1, 'O' if turn == 'X' else 'X')
        rec('.' * 9, 0, 'X')
        return res

    tested = 0
    for s in gen_states(4):
        if evaluate(s) is not None:
            continue
        mx = s.count('X'); mo = s.count('O')
        if mx < mo or mx > mo + 1:
            continue
        is_max = (mx == mo)
        a = minimax(s, is_max)
        b = alpha_beta(s, is_max, -2, 2)
        assert a == b, (s, a, b)
        tested += 1
    print(f"minimax-alpha-beta all tests passed ({tested} positions cross-validated)")

```

**PyPy 提示**: 博弈搜索递归深度大，PyPy 需 setrecursionlimit。剪枝效率取决于走法顺序：先搜最有希望的走法(启发排序)可大幅提升剪枝。井字棋/五子棋规模小纯 Python 可跑，围棋/国际象棋深搜索需换 C++ 或用位运算+转置表。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | Minimax 最坏 O(b^d)；Alpha-Beta 最优顺序 O(b^{d/2})，一般顺序介于两者间 |
| 空间 | O(d) 递归栈（转置表可选，空间另计） |

### 局限

零和完全信息才适用；深度受时间限制，超过则需静态评估函数截断（非精确）；走法顺序差时剪枝几乎无效；搜索空间巨大(围棋 10^170)时即使剪枝也不可行，需蒙特卡洛树搜索。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| OI Wiki | alpha-beta | 3 | Minimax+Alpha-Beta 完整推导示例（α≥β 剪枝语义，含四叉树逐步演示） | [https://oi-wiki.org/search/alpha-beta/](https://oi-wiki.org/search/alpha-beta/) |
| Wikipedia | Alpha-beta_pruning | 2 | Alpha-Beta 剪枝可视化示例与 negamax 形式 | [https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning) |

## Pitfalls · 易错点

- α 与 β 的语义(MAX下界/MIN上界)颠倒会导致错误剪枝
- 剪枝条件 α≥β 时两种节点都成立，α=β 也必须剪
- 根节点返回值应为 α(MAX) 或 β(MIN)，勿混淆
- 深度受限时需静态评估函数截断，返回值需有界(在(α,β)内才有剪枝意义)
- 走法顺序不排序时剪枝效率大幅下降

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/search/alpha-beta/](https://oi-wiki.org/search/alpha-beta/)
- 书籍 ✓ `CPH ch22 (Game theory / minimax 相关)`
