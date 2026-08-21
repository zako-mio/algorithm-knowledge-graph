---
id: nim-game
name: Nim游戏
group: G-E-6
stage: intermediate
priority: P0
depth_tier: deep
---

# Nim游戏

> n 堆石子轮流取任意堆任意多枚，Nim 和（全部堆的异或）为 0 则先手必败（P 态），非 0 则先手必胜（N 态）；公平组合博弈的基础模型

<!-- 元信息: id=nim-game · group=G-E-6 · stage=intermediate · priority=P0 · depth_tier=deep -->

## What · 是什么

Nim 游戏：共 n 堆石子，第 i 堆有 a_i 枚。两名玩家轮流操作，每次选取任意一堆，取走该堆中的任意正整数枚石子。无法操作（所有堆为空）的玩家输。结论（Bouton 定理）：局面先手必胜（N 态）当且仅当 Nim 和 s=a_1⊕a_2⊕⋯⊕a_n≠0；先手必败（P 态）当且仅当 s=0。必胜策略：找到最高位的 1（s 的最高位），选一堆 a_i 使其最高位为 1，将其改为 a_i⊕s（该值 < a_i），使新异或和为 0。

## Why · 为什么

### 直觉 · Intuition

异或像是『二进制的奇偶校验』。两个相等的堆互相抵消（同堆策略——对手拿什么你拿什么），异或和恰好刻画了这个抵消后的残余。残余为 0 说明局面完全'对称'，后手永远跟一手就能赢；残余非 0 先手只需一步把残余清零，把'对称'交给对手。

### 原理 · Principle

三性质完备：①终止态（全 0）异或和为 0（P 态）。②异或和非 0 时存在合法操作把它变 0：设 s 最高位为 k，取最高位含 1 的一堆 a_i，因 a_i≥2^k 而 a_i⊕s < a_i（s 使 k 位翻转为 0，更高位不变），拿走 a_i−(a_i⊕s) 个即可。③异或和为 0 时任何合法操作（把某一堆 a_i 减小为 a_i'）必使新异或非 0：因 s'=s⊕a_i⊕a_i'=a_i⊕a_i'≠0（a_i≠a_i'）。①②③ 恰为博弈图 P/N 标记的归纳条件。

### 历史 · History

Nim 起源于中国古代游戏（'捡石子' Jianshizi 类似）。Charles L. Bouton 于 1901 年首次发表完整数学分析（含异或策略），并命名 Nim。之后 Sprague 与 Grundy（1935/1939）把结论推广为 SG 理论，证明所有公平组合游戏都等价于某种单堆 Nim。Nim 因此是组合博弈论的基石模型，被 OI Wiki、CPH 与 CP-Algorithms 收录。

## How · 实现

### 伪代码

```python
# 判定先手胜负
def nim_win(piles):
  s = 0
  for a in piles: s ^= a
  return s != 0

# 构造必胜走法：返回 (堆下标, 取走后该堆大小) 或 None
def nim_move(piles):
  s = 0
  for a in piles: s ^= a
  if s == 0: return None
  for i, a in enumerate(piles):
    if (a ^ s) < a:
      return (i, a ^ s)  # 从第 i 堆取走 a-(a^s) 枚
```

### Python 实现

```python
def nim_win(piles):
    """返回当前局面是否为先手必胜（正常规则）。"""
    s = 0
    for a in piles:
        s ^= a
    return s != 0


def nim_move(piles):
    """返回必胜策略中的一步：元组 (堆下标, 操作后该堆剩余)。
    若已是 P 态（先手必败）返回 None。
    """
    s = 0
    for a in piles:
        s ^= a
    if s == 0:
        return None
    for i, a in enumerate(piles):
        if (a ^ s) < a:
            return (i, a ^ s)
    return None


def nim_strategy(piles):
    """演示：输出先手操作，并让后手（模拟最佳）应对后判断结果。
    仅用于教学演示。
    """
    if not nim_win(piles):
        return "P 态：先手必败"
    i, rest = nim_move(piles)
    return f"先手取第 {i} 堆，使其变为 {rest}"


if __name__ == "__main__":
    # 经典判定
    assert nim_win([1, 1]) is False        # 对称局面，后手跟手必胜
    assert nim_win([1, 2, 3]) is False     # 1^2^3 = 0
    assert nim_win([2, 5, 4]) is True      # 2^5^4 = 3
    assert nim_win([3]) is True
    assert nim_win([]) is False
    assert nim_win([1, 1, 1]) is True      # 1^1^1 = 1

    # 必胜走法正确性：移动后应为 P 态（异或和 0）
    for piles in [[2, 5, 4], [3, 4, 5, 6], [10, 8, 2], [7]]:
        i, rest = nim_move(piles)
        nxt = piles[:]
        nxt[i] = rest
        s = 0
        for a in nxt:
            s ^= a
        assert s == 0, (piles, nxt)

    # P 态无合法必胜走法
    assert nim_move([1, 1]) is None
    assert nim_move([1, 2, 3]) is None

    print("All tests passed.")
```

**PyPy 提示**: O(n) 异或扫描即可，n=1e5、a_i=1e9 轻松通过。构造走法时 (a^s)<a 的判断等价于最高位含 1，不需要位运算技巧包装。Python 的整数异或无溢出顾虑。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 判定 O(n)；构造走法 O(n) |
| 空间 | O(1) |

### 局限

适用于公平组合游戏（双方行动集相同、完全信息、无平局、正常规则）。若规则含『不能取』约束或反常规则（最后取者输），结论需调整（见 anti-nim）。存在走法但题目若要求输出字典序最小等需要额外排序。多堆且 a_i 巨大时仍 O(n)。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P2197 | 2 | 【模板】Nim 游戏：直接判定异或和，OI Wiki 模板题 | [https://www.luogu.com.cn/problem/P2197](https://www.luogu.com.cn/problem/P2197) |
| AtCoder | ABC 278 G? / AGC 系列组合博弈 | 7 | AGC 002 E Candy Piles：Nim 思想 + 阶梯/排序化归（OI Wiki 习题） | [https://atcoder.jp/contests/agc002/tasks/agc002_e](https://atcoder.jp/contests/agc002/tasks/agc002_e) |
| SPOJ | COT3 Combat on a tree | 8 | 树上博弈的 SG/Nim 组合综合题（OI Wiki 习题） | [https://www.spoj.com/problems/COT3/](https://www.spoj.com/problems/COT3/) |

## Pitfalls · 易错点

- 判断用『异或和==0 → 先手必败』，方向别记反
- a_i 可能为 0（空堆），异或不变，但全空局面是 P 态
- 构造走法时要找 (a^s)<a 的那一堆，不能随便取一堆
- P 态没有必胜走法，nim_move 返回 None 时别误报有解
- 异或用 Python 的 ^ 而非数学加号，两者不同
- 只适用于正常规则（最后取者赢）；misère 规则见 anti-nim

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/game-theory/impartial-game/](https://oi-wiki.org/math/game-theory/impartial-game/)
- CP-Algorithms ✓ [https://cp-algorithms.com/game_theory/sprague-grundy-nim.html](https://cp-algorithms.com/game_theory/sprague-grundy-nim.html)
- 书籍 ✓ `CPH ch25 Game theory, pp.245-252`
