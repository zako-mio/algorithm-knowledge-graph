---
id: partizan-game
name: 非公平组合博弈
group: G-E-6
stage: advanced
priority: P2
depth_tier: standard
---

# 非公平组合博弈

> 双方可用行动集不同的博弈（如棋类）：Conway 超现实数理论描述，结果分类 L/R/N/P 四种；比公平博弈复杂得多，竞赛少见

<!-- 元信息: id=partizan-game · group=G-E-6 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

非公平组合博弈（partizan game）：两名玩家（左 L 与右 R）拥有不同的可行动作集合，典型的如国际象棋（双方棋子不同）。与公平博弈的关键区别：每个状态 G={G^L | G^R} 由左方选项集合与右方选项集合组成，且左右不对称。结果是四分类而非两分类：L（左方必胜）、R（右方必胜）、N（先手必胜）、P（后手必胜）。John Conway 的《On Numbers and Games》(1976) 将这类博弈与超现实数（surreal numbers）统一：简单博弈对应数值，另有非数值博弈（如星 * 和 up）。由于一般 partizan 博弈的 SG 理论不存在，竞赛中仅出现一些退化特例（如只需判断 P/N 的二值博弈）。

## Why · 为什么

### 直觉 · Intuition

公平博弈里'对称'允许我们用异或把一个值压缩成 Nim 数。非公平博弈失去对称性，每个状态必须同时记录'左方能做的'和'右方能做的'两套选项。结果只取决于：左方是否有一步能到自己必胜（L 或 P）的态，右方同理。四条规则给出四分类。数值化的特例（超现实数）让许多博弈可以'加减'，如 {0|}=1，{0|0}=*。

### 原理 · Principle

结果分类（Conway）：对状态 G={G^L|G^R}，定义左结果 L 当且仅当存在 G^L 为 L 或 P；右结果 R 当且仅当存在 G^R 为 R 或 P。于是：若左结果 L 且右结果 L → 态为 L（左必胜）；若左结果 R 且右结果 R → 态为 R（右必胜）；若左结果 L 且右结果 R → 态为 N（先手必胜）；若左结果 R 且右结果 L → 态为 P（后手必胜）。数值博弈：若 G={a|b} 且 a<b（a,b 为超现实数），则 G 等于某数 x 使 a<x<b；{0|}=1、{|0}=−1、{0|1}=1/2、{1|}=2 等构成数。{0|0}=* 是第一个非数值博弈，{*|0}、{0|*} 等构造 up/down 系列。复合与加和用超现实数加法。

### 历史 · History

partizan 博弈的现代理论由 John Horton Conway 建立，代表作《On Numbers and Games》(1976) 与 Berlekamp、Conway、Guy 合著的《Winning Ways》(1982)。Conway 证明所有超现实数都能由博弈构造，反之数值博弈即超现实数。此前 Sprague/Grundy（公平）是唯一完整理论；partizan 理论把博弈论与序数算术、组合数学相连，是数学与 CS 交叉的经典。竞赛中因实现复杂极少考到。

## How · 实现

### 伪代码

```python
# 结果四分类：状态表示为 (L_options, R_options)
def outcome(G):
  lr = 'R'   # 左方能否赢（有选项到 L 或 P）
  for o in G.L:
    if outcome(o) in ('L','P'): lr = 'L'; break
  rr = 'L'   # 右方能否赢（有选项到 R 或 P）
  for o in G.R:
    if outcome(o) in ('R','P'): rr = 'R'; break
  if lr=='L' and rr=='L': return 'L'
  if lr=='R' and rr=='R': return 'R'
  if lr=='L' and rr=='R': return 'N'
  return 'P'
```

### Python 实现

```python
def outcome(G, memo=None):
    """非公平组合博弈的结果四分类。
    G = (L_opts, R_opts)，选项同为该形式（递归）。
    返回 'L'/'R'/'N'/'P'。
    """
    if memo is None:
        memo = {}
    if G in memo:
        return memo[G]
    L_opts, R_opts = G

    left_wins = False  # 左方能否走到自己必胜（L 或 P）的态
    for o in L_opts:
        if outcome(o, memo) in ("L", "P"):
            left_wins = True
            break
    right_wins = False  # 右方能否走到自己必胜（R 或 P）的态
    for o in R_opts:
        if outcome(o, memo) in ("R", "P"):
            right_wins = True
            break

    if left_wins and right_wins:
        res = "N"
    elif not left_wins and not right_wins:
        res = "P"
    elif left_wins:
        res = "L"
    else:
        res = "R"
    memo[G] = res
    return res


if __name__ == "__main__":
    # 用元组表示 (L_opts, R_opts)，元素本身也是同结构元组
    zero = ((), ())            # 0 = { | }
    assert outcome(zero) == "P"

    star = ((zero,), (zero,))  # * = {0 | 0}
    assert outcome(star) == "N"

    one = ((zero,), ())        # 1 = {0 | }
    assert outcome(one) == "L"

    minus_one = ((), (zero,))  # -1 = { | 0}
    assert outcome(minus_one) == "R"

    up = ((zero,), (star,))    # {0 | *}
    assert outcome(up) == "L"

    down = ((star,), (zero,))  # {* | 0}
    assert outcome(down) == "R"

    two = ((one,), ())         # 2 = {1 | }  （数值博弈左必胜）
    assert outcome(two) == "L"

    print("All tests passed.")
```

**PyPy 提示**: 结果分类用记忆化递归，状态空间大时注意 key 的可哈希性（用元组表示博弈树）。竞赛中 partizan 极罕见；若出现通常是退化到二值（如左必赢或右必赢）的情形，可直接按 L/R 分支判断。数值博弈的加法（超现实数）实现需要分数运算，PyPy 下用 Fraction 或手写。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 单点结果分类 O(\|L_opts\|+\|R_opts\|)（记忆化后 O(状态数·分支)） |
| 空间 | O(状态数) |

### 局限

一般 partizan 博弈没有类似 SG 的简洁数值表示（除数值博弈），分析工具（超现实数、冷博弈/热博弈、temperature）远超竞赛范围。OI Wiki 的 partizan-game 页面为空/未维护（github 上文件为空），竞赛中极少出现，若出现几乎必是退化特例。实现上博弈树需是有限无环的。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| OI-Wiki | intro 公平/非公平概念 | 4 | 基础概念：非公平组合博弈定义与公平博弈对照（OI Wiki intro 页） | [https://oi-wiki.org/math/game-theory/intro/](https://oi-wiki.org/math/game-theory/intro/) |
| CP-Algorithms | Sprague-Grundy（公平前提说明） | 5 | SG 定理的公平性前提：理解哪些游戏不适用 SG（即 partizan 范畴） | [https://cp-algorithms.com/game_theory/sprague-grundy-nim.html](https://cp-algorithms.com/game_theory/sprague-grundy-nim.html) |
| Wikipedia | Surreal number | 6 | 超现实数：partizan 博弈数值化的理论背景（Conway 定义） | [https://en.wikipedia.org/wiki/Surreal_number](https://en.wikipedia.org/wiki/Surreal_number) |

## Pitfalls · 易错点

- partizan 结果四分类中 'L'/'R' 判断是看『存在选项到 L 或 P』（左）与『存在选项到 R 或 P』（右），不要用公平博弈的 N/P 规则
- N（先手胜）与 P（后手胜）在不对称时易混淆：N 需左右都能动手赢
- 不能用异或组合 partizan 博弈的'值'（除非数值博弈）
- 超现实数的 {a\|b} 只在该数为可构造时才等于普通分数，注意左/右选项顺序（左<右）
- 判断循环时用记忆化 + 显式环检测，防递归死循环
- OI Wiki 的 partizan-game 页面实际为空，主参考应以 Conway《On Numbers and Games》为准

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/game-theory/intro/](https://oi-wiki.org/math/game-theory/intro/)
- OI Wiki △ [https://oi-wiki.org/math/game-theory/partizan-game/](https://oi-wiki.org/math/game-theory/partizan-game/)
- 书籍 ✓ `Conway, On Numbers and Games (1976)`
