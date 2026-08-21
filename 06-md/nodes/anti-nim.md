---
id: anti-nim
name: 反常Nim/Anti-Nim
group: G-E-6
stage: advanced
priority: P1
depth_tier: standard
---

# 反常Nim/Anti-Nim

> misère 规则：取最后一枚石子者输；判定需分类讨论——全 1 堆看奇偶，否则仍看 Nim 和（与正常 Nim 相同）

<!-- 元信息: id=anti-nim · group=G-E-6 · stage=advanced · priority=P1 · depth_tier=standard -->

## What · 是什么

反常 Nim（Misère Nim）：规则与 Nim 完全相同，但取走最后一枚石子的玩家失败（即无法操作者获胜）。判定结论（反 Nim 定理）：设 Nim 和 s=a_1⊕a_2⊕⋯⊕a_n。若所有堆都 ≤1（每堆至多 1 枚），则先手必败当且仅当石子数为奇数；若存在某堆 ≥2，则先手必败当且仅当 s=0（与正常 Nim 相同）。合并：P 态 ⟺ (存在堆>1 且 s=0) 或 (全堆≤1 且非空堆数为奇数)。

## Why · 为什么

### 直觉 · Intuition

misère 规则下终点『全空』变成了先手的胜利，诱导规则在末端'反转'。但反转只发生在所有堆都退化到 ≤1 的临界区：只要还有一堆 ≥2，Nim 的异或论证依然有效（可以控制在临界局面把奇偶性做对）。全 ≤1 时每步只能拿走 1 枚，奇偶性直接决定谁拿最后一枚。

### 原理 · Principle

归纳证明。全 1 堆情形：n 堆各 1 枚，每步拿 1 枚，恰好 n 步结束，拿最后一枚者输 → n 为奇数时先手输，n 为偶数时先手赢（先手把最后一步留给对手）。含 ≥2 的情形分两况：只有一堆 >1 时，先手可把它改成 0 或 1 使剩余全 1 堆的奇偶性满足『对手必败』，故先手必胜（此时 Nim 和必非 0）；有多堆 >1 时，任何一步都会破坏≥2 性（新状态仍含≥2 或退到临界），归纳假设下 Nim 和非 0 可调为 0（正常 Nim 论证），Nim 和 0 无法守住 0（同正常 Nim 性质③），结论与正常 Nim 一致。

### 历史 · History

反常（misère）规则下的 Nim 由 Bouton 于 1901 年同一篇论文中解决，他完整给出了含'最后一着者输'的判定。misère 组合博弈的一般理论比正常规则复杂得多（SG 理论不直接适用），但 Nim 是少数可用简单分类处理的特例。OI Wiki 在 impartial-game 页『反常 Nim 游戏』一节收录，CPH 亦提及。

## How · 实现

### 伪代码

```python
# 反 Nim 判定（返回 True 表示先手必胜）
def anti_nim_win(piles):
  if all(a <= 1 for a in piles):
    return (sum(piles) % 2 == 0)   # 全 1：偶数枚则先手赢
  s = 0
  for a in piles: s ^= a
  return s != 0                    # 含 >1：看 Nim 和
```

### Python 实现

```python
def anti_nim_win(piles):
    """反常 Nim（最后取者输）判定：True=先手必胜，False=先手必败。"""
    if not piles:
        return False  # 无堆即无操作，先手无法行动而获胜（misère 下空局先手胜）
    if all(a <= 1 for a in piles):
        return sum(piles) % 2 == 0
    s = 0
    for a in piles:
        s ^= a
    return s != 0


def anti_nim_pseudo_moves(piles):
    """演示：若先手必胜，给出一种必胜走法。
    返回 (堆下标, 操作后剩余) 或 None。
    注意 misère 规则下必胜走法并非一律清零 Nim 和：
    - 恰有一堆 >1 时，把它调到 0/1 使全 1 堆总数为奇数（给对手 P 态）；
    - 至少两堆 >1 时，才按正常 Nim 的异或清零走法。
    """
    if not anti_nim_win(piles):
        return None
    big = [i for i, a in enumerate(piles) if a > 1]
    if len(big) == 1:
        i = big[0]
        ones = sum(1 for j, a in enumerate(piles) if j != i and a == 1)
        target = 1 if ones % 2 == 0 else 0  # 使 1 的个数为奇数（对手 P 态）
        return (i, target)
    if len(big) >= 2:
        s = 0
        for a in piles:
            s ^= a
        for i, a in enumerate(piles):
            if (a ^ s) < a:
                return (i, a ^ s)
    # 全 1 且先手胜（1 的个数为偶数）：拿任意一堆 1 枚即可
    for i, a in enumerate(piles):
        if a == 1:
            return (i, 0)
    return None


if __name__ == "__main__":
    from functools import lru_cache

    # 暴力验证：misère 终局判定（无操作者赢）
    @lru_cache(maxsize=None)
    def win(state):
        state = tuple(sorted(x for x in state if x > 0))
        if not state:
            return True  # 无法操作：当前玩家赢（misère）
        for i, v in enumerate(state):
            for take in range(1, v + 1):
                nxt = list(state)
                nxt[i] -= take
                if not win(tuple(nxt)):
                    return True
        return False

    import itertools
    for n in range(1, 5):
        for piles in itertools.product(range(1, 4), repeat=n):
            if sum(piles) > 10:
                continue
            assert anti_nim_win(list(piles)) == win(tuple(piles)), piles

    # 关键样例
    assert anti_nim_win([1, 1, 1]) is False   # 3 堆 1 枚：先手必败
    assert anti_nim_win([1, 1]) is True       # 2 堆 1 枚：先手胜
    assert anti_nim_win([1, 1, 1, 1]) is True
    assert anti_nim_win([2, 3]) is True       # 2^3=1≠0 → 先手胜
    assert anti_nim_win([1, 2, 3]) is False   # 含>1 且 1^2^3=0 → 先手败
    assert anti_nim_win([5]) is True

    # 必胜走法后局面应为必败
    for piles in [[2, 3], [5], [1, 1], [1, 1, 4]]:
        m = anti_nim_pseudo_moves(piles)
        assert m is not None, piles
        i, rest = m
        nxt = piles[:]
        nxt[i] = rest
        assert not anti_nim_win(nxt), (piles, nxt)

    print("All tests passed.")
```

**PyPy 提示**: O(n) 判定极快。misère 一般游戏（非 Nim）不能简单套 SG，需注意区分；Nim 的 misère 有上面的特判分类，记住两分支即可。若题目是 Anti-Nim 变体（每堆可减任意数量但有上限），需转 SG+找规律。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n) |
| 空间 | O(1) |

### 局限

仅适用于标准 Nim 规则的 misère 变体。misère 规则的任意公平组合游戏（如 misère 取石子一般化）没有统一 SG 捷径，一般要具体分析。若存在堆>1 但 Nim 和恰为 0，此时先手必败（与正常 Nim 结论相同，这是反直觉点，容易错判为必败/必胜）。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P4279 | 4 | [SHOI2008] 小约翰的游戏：Anti-Nim 判定模板，OI Wiki 习题 | [https://www.luogu.com.cn/problem/P4279](https://www.luogu.com.cn/problem/P4279) |
| Luogu | P4101 | 5 | [HEOI2014] 人人尽说江南好：misère 思想的组合博弈变体（OI Wiki 习题） | [https://www.luogu.com.cn/problem/P4101](https://www.luogu.com.cn/problem/P4101) |
| AtCoder | ARC 168 B Arbitrary Nim | 6 | Arbitrary Nim：可限制每堆取的上限，Anti-Nim 判定思想延伸（OI Wiki 习题） | [https://atcoder.jp/contests/arc168/tasks/arc168_b](https://atcoder.jp/contests/arc168/tasks/arc168_b) |

## Pitfalls · 易错点

- misère 判定必须分类：全 ≤1 与存在 >1 两分支，直接用正常 Nim 异或会错（如 [1,1] 正常是 P、misère 是 N）
- 全 ≤1 分支看『石子总数奇偶』而非『堆数奇偶』（堆数=石子数时等价，但含 0 堆时别混淆）
- 空局（无堆）在 misère 下当前玩家无法操作 → 获胜，务必特判
- 必胜走法在含>1 时仍按异或清零，但全 1 分支要拿 1 枚（若误按异或会取不到）
- misère 的 SG 理论不成立，别试图对 misère 游戏套 SG 异或

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/game-theory/impartial-game/](https://oi-wiki.org/math/game-theory/impartial-game/)
- OI Wiki ✓ [https://oi-wiki.org/math/game-theory/intro/](https://oi-wiki.org/math/game-theory/intro/)
- 书籍 ✓ `CPH ch25 Game theory（misère 简要提及）`
