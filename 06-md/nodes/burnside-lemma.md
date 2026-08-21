---
id: burnside-lemma
name: Burnside引理
group: G-C-11
stage: advanced
priority: P2
depth_tier: standard
---

# Burnside引理

> 群 G 在集合 X 上的轨道数 = (1/\|G\|)·Σ_{g∈G}\|Fix(g)\|，不动点平均数，Pólya 计数的基础

<!-- 元信息: id=burnside-lemma · group=G-C-11 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

Burnside 引理（Burnside's lemma，又称 Cauchy–Frobenius 引理）给出群作用下的『本质不同』对象数：设有限群 G 作用在有限集合 X 上，则不同轨道（orbits）的数目 |X/G| = (1/|G|)·Σ_{g∈G} |X^g|，其中 X^g = {x∈X : g·x = x} 是 g 的不动点集。也就是说：本质不同的类别数 = 所有群操作的不动点数的平均值。直观例子（OI Wiki）：4 珠 2 色项链，旋转群 G={r0,r1,r2,r3}，四类操作不动点数分别为 16,2,4,2，平均 (16+2+4+2)/4 = 6 即本质不同染色数。应用时不需群论深细节，只要不重不漏枚举所有对称操作并逐个数不动点。它与 Pólya 定理的关系：Pólya 把 |X^g| 改写为 m^{c(g)}（用轮换数），使计数可直接计算。

## Why · 为什么

### 直觉 · Intuition

把每个对象 x 画成一张纸，群操作 g 把纸翻面/旋转。每个对象 x 被 g 作用后可能映射到自己（不动），也可能映射到别人。把所有操作下『保持不动的对象』数量加起来再除以操作总数——为什么等于轨道数？因为每个轨道里所有对象都在『互相映来映去』，恰好有 |G|/|stab(x)| 个不同的像、重复 |stab(x)| 次，而这正好让每个轨道对整个平均值贡献 1。于是平均不动点数就恰好是轨道数。

### 原理 · Principle

严格证明用轨道-稳定子定理（orbit-stabilizer theorem）：对任意 x∈X，|Orbit(x)|·|Stab(x)| = |G|。对不动点对 (g,x) 双重计数：Σ_g |X^g| = Σ_x |Stab(x)| = Σ_{轨道 O} Σ_{x∈O} |G|/|O| = Σ_{轨道 O} |G| = |G|·|X/G|，除以 |G| 即得引理。交换求和顺序（Σ_gΣ_x[g·x=x] = Σ_xΣ_g[g·x=x]）是证明的关键一步（OI Wiki 有完整推导）。注意条件：G 必须是群（每个操作有逆元），X 可以是染色方案集合，G 作用在 X 上。当 X 是染色方案、g 是置换时，|X^g| 通常为 m^{c(g)}，引出 Pólya 定理。

### 历史 · History

该引理最早可追溯至 Cauchy（1845）与 Frobenius（1887）的工作，因 Burnside 在其 1911 年教科书《Theory of Groups of Finite Order》中的介绍而广为人知（Burnside 本人标注了出处）。它是 Pólya 计数原理（1927）的理论基础，也是竞赛计数题『本质不同/同构去重』的标准工具。CP-Algorithms 的 Burnside 页以『项链染色』与 PET 形式给出应用；OI Wiki 群论章节亦给出轨道-稳定子定理的严格表述。

## How · 实现

### 伪代码

```python
# 输入: 群 G 的元素列表(每个是 X 上的置换), 以及枚举 X 的方案
# 输出: 轨道数 |X/G|

def burnside(G, count_fixed):
  return sum(count_fixed(g) for g in G) / len(G)

def count_fixed_naive(g, X):
  # 朴素: 遍历所有对象 x 检查 g·x == x
  return sum(1 for x in X if apply(g, x) == x)

# 染色场景: X = C^m (m 个位置, 颜色集 C), g 是位置置换
#   x 不动 ⟺ 每个轮换内的位置同色
#   |Fix(g)| = |C| ** cycle_count(g)
```

### Python 实现

```python
from math import gcd


def cycle_count(perm):
    """置换 perm 的轮换个数(含 1-轮换)."""
    n = len(perm)
    seen = [False] * n
    cnt = 0
    for i in range(n):
        if not seen[i]:
            cnt += 1
            j = i
            while not seen[j]:
                seen[j] = True
                j = perm[j]
    return cnt


def burnside_necklace_rot(n, m):
    """Burnside 引理直接实现: n 珠 m 色项链(只算旋转群)本质不同数.
    旋转 k 次的不动点 = 轮换数 gcd(n,k) 个, 每轮换 m 色 => m**gcd(n,k)."""
    return sum(m ** gcd(n, k) for k in range(n)) // n


def burnside_generic(perms, m, n):
    """通用: perms 为置换列表(位置集 {0..n-1}), 返回轨道数."""
    total = 0
    for p in perms:
        total += m ** cycle_count(p)
    assert len(perms) > 0
    return total // len(perms)


def fixed_points_by_bruteforce(g, m, n):
    """朴素不动点统计: 枚举所有 m^n 个染色方案(仅小规模演示)."""
    from itertools import product
    cnt = 0
    for coloring in product(range(m), repeat=n):
        ok = all(coloring[i] == coloring[g[i]] for i in range(n))
        if ok:
            cnt += 1
    return cnt


if __name__ == "__main__":
    n, m = 4, 2
    # 旋转群四个置换
    perms = [[(i + k) % n for i in range(n)] for k in range(n)]
    assert burnside_generic(perms, m, n) == 6          # OI Wiki 项链例子
    assert burnside_necklace_rot(n, m) == 6
    # 与朴素不动点统计一致(4 珠 2 色全部方案只有 16 个)
    for g in perms:
        assert fixed_points_by_bruteforce(g, m, n) == m ** cycle_count(g)
    # n=3,m=2 手链: 旋转群+3 反射, 共 6 个操作, 轨道数=4
    perms3 = [[(i + k) % 3 for i in range(3)] for k in range(3)]
    perms3 += [[(k - i) % 3 for i in range(3)] for k in range(3)]
    assert burnside_generic(perms3, 2, 3) == 4
    print("burnside-lemma: all tests passed")

```

**PyPy 提示**: 枚举全部操作并数不动点，\|G\| 通常小（旋转群 n、二面体群 2n、立方体 24），O(\|G\|·\|X\|) 朴素或 O(\|G\|·n) 染色轮换即可。取模时除法用逆元；不取模时整除必然精确。旋转群不动点数可预计算：旋转 k 次轮换数 = gcd(n,k)。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(\|G\|·\|X\|) 朴素；染色场景 O(\|G\|·n)（轮换分解） |
| 空间 | O(n) 或 O(\|X\|) |

### 局限

① G 必须是群（封闭、含逆），若只给部分操作不能直接除 |G|；② 需不重不漏枚举所有操作，漏操作会导致分子偏小；③ 朴素遍历 |X| 只适用于小对象集，大规模必须用轮换/组合技巧算 |Fix(g)|；④ 不适用于无限群/无限集合；⑤ 分子分母可能巨大需模意义处理（此时|G|必须可逆）。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P4980 | 4 | 【模板】Polya 定理：旋转群不动点 m^gcd(n,k)，n 达 1e9 用欧拉函数分组，Burnside 引理的直接应用 | [https://www.luogu.com.cn/problem/P4980](https://www.luogu.com.cn/problem/P4980) |
| Luogu | P1446 | 5 | HNOI2008 Cards：受限颜色数的 Burnside 引理 + 背包，逐个置换统计不动点 | [https://www.luogu.com.cn/problem/P1446](https://www.luogu.com.cn/problem/P1446) |
| Luogu | P4916 | 6 | MtOI2018 魔力环：Burnside + 组合计数统计各旋转不动点，OI Wiki 习题 | [https://www.luogu.com.cn/problem/P4916](https://www.luogu.com.cn/problem/P4916) |
| CP-Algorithms | burnside | 3 | 官方教程：项链染色、Pólya 形式与更多例题 | [https://cp-algorithms.com/combinatorics/burnside.html](https://cp-algorithms.com/combinatorics/burnside.html) |

## Pitfalls · 易错点

- 操作集合不构成群（缺恒等/逆操作）却直接除 \|G\|
- 忘数恒等置换的不动点 = \|X\| 全集
- 不动点统计时把『对象』与『操作后结果』搞混（必须满足 g·x=x）
- 取模时直接整除而非乘模逆元
- 轮换计数把 1-轮换漏掉导致不动点数偏小

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/combinatorics/polya/](https://oi-wiki.org/math/combinatorics/polya/)
- oiwiki-raw ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/combinatorics/polya.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/combinatorics/polya.md)
- CP-Algorithms ✓ [https://cp-algorithms.com/combinatorics/burnside.html](https://cp-algorithms.com/combinatorics/burnside.html)
- Wikipedia ✓ [https://en.wikipedia.org/wiki/Burnside%27s_lemma](https://en.wikipedia.org/wiki/Burnside%27s_lemma)
