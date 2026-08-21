---
id: sg-function
name: SG函数/Sprague-Grundy定理
group: G-E-6
stage: intermediate
priority: P0
depth_tier: deep
---

# SG函数/Sprague-Grundy定理

> 所有公平组合游戏等价于单堆 Nim；SG(x)=mex{SG(后继)}；多个独立子游戏的 SG 异或得总局面 SG，零则先手必败；Sprague-Grundy 定理

<!-- 元信息: id=sg-function · group=G-E-6 · stage=intermediate · priority=P0 · depth_tier=deep -->

## What · 是什么

Sprague-Grundy 理论：任何公平组合游戏（双方行动集相同、完全信息、有限、无平局、正常规则）都等价于某个单堆 Nim 游戏。定义 SG 函数：终止状态 SG=0；一般状态 SG(x)=mex{SG(y): y 是 x 的后继}，其中 mex 是集合外的最小非负整数。SG(x)=k 表示该状态等价于一堆大小为 k 的石子。Sprague-Grundy 定理：多个独立子游戏的和（每步只能操作一个子游戏）的总 SG 值 = 各子游戏 SG 值的异或。总 SG=0 ⟺ 先手必败。

## Why · 为什么

### 直觉 · Intuition

mex 像『给状态打分，分数等于它错过的第一个数值』。SG 值 k 精确表达『这个状态在组合中扮演单堆 Nim 里一堆 k 石子的角色』——它可以被一步走到任何 SG 值 <k 的状态，且走不到 SG=k 的对手态（这正是 Nim 一堆石子的移动性质）。异或把各独立子游戏的'等价 Nim 堆'合起来，Nim 和为零则后手必胜。

### 原理 · Principle

两条引理：(1) 必败游戏 A（SG=0）加在任何游戏 G 上等价于 G（G+A≈G）；(2) G≈G' ⟺ G+G' 是必败态。因此可定义等价类到非负整数的同构：SG(G)=mex{SG(G') : G' 是 G 的后继}。正确性：SG(G)=0 时无后继 SG 为 0 → 所有后继 SG 非 0 → 所有后继必胜 → G 必败；SG(G)=k>0 时存在后继 SG 为 0（mex 定义）→ 可一步到必败态 → 必胜。多子游戏：SG(和)=⊕SG(子)，证明依赖上述引理与 Nim 和的经典论证（异或非 0 可调，异或为 0 不可守）。

### 历史 · History

Roland Sprague（1935，德国）与 Patrick Michael Grundy（1939，英国）独立发现公平组合游戏可化简为 Nim 的表示定理。Grundy 还引入 mex 概念。这一理论把看似千奇百怪的公平游戏统一到异或这一个运算下，是组合博弈论的分水岭，被 OI Wiki、CPH ch25 与 CP-Algorithms 专门讲解。

## How · 实现

### 伪代码

```python
# 对单个状态空间 0..n 计算 SG（moves 为可减少量集合）
def sg_table(n, moves):
  sg = [0]*(n+1)
  for k in 1..n:
    reach = { sg[k-m] for m in moves if k >= m }
    mex = 0
    while mex in reach: mex += 1
    sg[k] = mex
  return sg
# 多个子游戏：总 SG = xor of sg[i]；总 SG==0 → 先手必败
```

### Python 实现

```python
def sg_table(n, moves):
    """计算 SG(0..n)。moves 为一次可取走数量的集合。
    返回 sg 数组，sg[k] 为状态 k 的 SG 值。
    """
    sg = [0] * (n + 1)
    for k in range(1, n + 1):
        reach = {sg[k - m] for m in moves if k >= m}
        mex = 0
        while mex in reach:
            mex += 1
        sg[k] = mex
    return sg


def combine_sg(sub_sg):
    """Sprague-Grundy：多个独立子游戏总 SG = 异或。
    返回 0 表示先手必败，非 0 表示先手必胜。
    """
    x = 0
    for g in sub_sg:
        x ^= g
    return x


def sg_win(sub_sg):
    """总 SG 值异或判定胜负。"""
    return combine_sg(sub_sg) != 0


if __name__ == "__main__":
    # 游戏 1：取 1..K 个石子，SG(k) = k % (K+1)（周期）
    for K in range(1, 6):
        sg = sg_table(60, range(1, K + 1))
        for k in range(61):
            assert sg[k] == k % (K + 1), (K, k, sg[k])

    # 游戏 2：取平方数个石子（subtract-a-square），与递归定义交叉验证
    sq = [i * i for i in range(1, 8)]
    sg = sg_table(30, sq)
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def sg_brute(k):
        if k == 0:
            return 0
        reach = {sg_brute(k - m) for m in sq if k >= m}
        mex = 0
        while mex in reach:
            mex += 1
        return mex

    for k in range(31):
        assert sg[k] == sg_brute(k), (k, sg[k], sg_brute(k))

    # SG 基本性质
    assert sg[0] == 0
    # 取 1 或 2 的游戏：SG(0..5)=0,1,2,0,1,2
    sg2 = sg_table(5, [1, 2])
    assert list(sg2) == [0, 1, 2, 0, 1, 2]
    # 组合游戏：两个取1/2子游戏，各自 3 个石子 → SG=0（先手必败）
    assert sg_win([sg2[3], sg2[3]]) is False
    assert sg_win([sg2[3], sg2[4]]) is True

    print("All tests passed.")
```

**PyPy 提示**: sg_table 中 reach 集合用 set，n=1e6 时内存 O(n) 可行但枚举 moves 复杂。当 moves 有周期结构时先打表找周期（SG 常是周期的，周期 ≤ max(moves) 的若干倍），可只算前几周期然后取模——这是竞赛常用优化。PyPy 下递归 sg_brute 会慢，务必用表格+循环。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 打表 SG(0..n) O(n·\|moves\|)；找周期后可 O(1) 取模；组合判定 O(子游戏数) |
| 空间 | O(n) 或 O(周期) |

### 局限

仅适用于公平组合游戏（双方行动完全相同）。非公平（partizan）、反常规则（最后取者输）不能直接用 SG。状态空间若巨大且无周期结构，暴力打表不可行，需找数学规律或观察。mex 计算依赖集合，moves 集合很大时每次 O(|moves|)。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P2148 | 7 | [SDOI2009] E&D：每组 2 堆的独立游戏，打表找 SG 递推（OI Wiki 例题） | [https://www.luogu.com.cn/problem/P2148](https://www.luogu.com.cn/problem/P2148) |
| Luogu | P2197 / P3480 系列 | 5 | KAM-Pebbles 阶梯 Nim：SG 化归为阶梯博弈，OI Wiki 模板题延伸 | [https://www.luogu.com.cn/problem/P3480](https://www.luogu.com.cn/problem/P3480) |
| AtCoder | ABC 278 G / AGC 017 D Game on Tree | 7 | 树上子游戏 SG 异或（每颗子树独立），OI Wiki 习题 | [https://atcoder.jp/contests/agc017/tasks/agc017_d](https://atcoder.jp/contests/agc017/tasks/agc017_d) |

## Pitfalls · 易错点

- mex 是『集合外最小非负整数』，不是 max+1（除非集合恰好是 0..max 全覆盖）
- 总 SG 用异或而非加法；多个子游戏异或后为 0 是必败而非必胜
- sg_table 里 moves 若含 0（允许不取）会自环，必须保证每次真正减少
- 状态需满足有限 + 无平局（DAG）才有 SG；有环见 game-on-graph 的胜负平局分类
- 找周期时周期起点的偏移也要测（SG 可能在若干项后才进入周期）
- SG 值可能超过 \|moves\|，mex 的上界是 \|moves\|，不必担心溢出

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/game-theory/impartial-game/](https://oi-wiki.org/math/game-theory/impartial-game/)
- CP-Algorithms ✓ [https://cp-algorithms.com/game_theory/sprague-grundy-nim.html](https://cp-algorithms.com/game_theory/sprague-grundy-nim.html)
- 书籍 ✓ `CPH ch25 Game theory, pp.245-252`
