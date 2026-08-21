---
id: polya-enumeration
name: Polya计数
group: G-C-11
stage: advanced
priority: P2
depth_tier: standard
---

# Polya计数

> Burnside引理+循环指标多项式：本质不同染色数 = (1/\|G\|)Σ m^{c(g)}，m为颜色数、c(g)为置换g的轮换数

<!-- 元信息: id=polya-enumeration · group=G-C-11 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

Pólya 计数原理（Pólya Enumeration Theorem, PET）是 Burnside 引理在染色计数问题上的应用与推广，专门回答『本质不同』的计数问题：给定一个带对称性（如旋转、翻转）的结构，在其上染色，经对称操作可互相转化的染色方案视为同一类，问共有多少类。与 Burnside 引理逐条列举不动点不同，Pólya 定理把每个对称操作 g 看作置换，只需知道 g 的轮换分解中轮换的数目 c(g)，即可得到 g 的不动点数 = m^{c(g)}（m 为颜色数）。于是本质不同染色数 = (1/|G|)·Σ_{g∈G} m^{c(g)}。带权重的版本进一步给出循环指标多项式 Z(G)=Σ_{g∈G} ∏_k z_k^{j_k(g)} / |G|（j_k(g) 为 g 中 k-轮换个数），本质不同染色按颜色使用数的生成函数为 Z(G)[z_k ← Σ_{c∈C} w_c^k]，可用于『每种颜色恰用若干次』等受限计数。经典例子：4 珠 2 色项链，旋转群 G={r0,r1,r2,r3}，各置换轮换数为 4,1,2,1，答案为 (2^4+2^1+2^2+2^1)/4=6。

## Why · 为什么

### 直觉 · Intuition

想象一条项链，旋转一下看起来一样的都算同一种。Pólya 的思路是：先别管『哪颗珠子是第几颗』，只看每个旋转操作把珠子们分成了几个『小循环』（轮换）。在一个轮换里，只要一颗珠子定了颜色，整个轮换的颜色就全定了（因为它们旋转后互相重合）。所以旋转一次产生的不动方案数 = 颜色数^轮换数。把所有操作的不动方案数求平均，就是答案——这正是 Burnside 引理的意思，Pólya 只是把『数不动点』变成了『数轮换』，省去了枚举染色方案的麻烦。

### 原理 · Principle

核心是置换的轮换分解。给定结构的位置集合 X 与对称群 G（作用在 X 上），一个染色方案 f∈C^X 是 g 的不动点 ⟺ 对 g 的每个轮换 (x_1 x_2 … x_k)，有 f(x_1)=f(x_2)=…=f(x_k)（轮换内所有位置同色）。轮换之间相互独立可任意选色，故 |Fix(g)|=|C|^{c(g)}=m^{c(g)}。代入 Burnside 引理 |X/G|=(1/|G|)Σ_g|Fix(g)| 即得无权重公式。带权重版本：给每种颜色赋权 w_c，则 g 的权重和（按轮换）为 ∏_k (Σ_c w_c^k)^{j_k(g)}，对所有 g 求和除以 |G| 得到循环指标多项式 Z(G)，再把 z_k 替换为 Σ_c w_c^k，[w_1^{a_1}w_2^{a_2}…] 即『恰用 a_i 次颜色 i』的本质不同染色数。正确性由 Burnside 引理保证，仅把 |Fix(g)| 用轮换结构重写。

### 历史 · History

1927 年 G. Pólya 在『组合数论中的若干定理』中系统提出该计数定理；其核心——Burnside 引理——则更早由 Burnside（1911）在其教科书《Theory of Groups of Finite Order》中表述，而最早其实出现在 Frobenius（1887）与 Cauchy 的工作中。Pólya 把对称性计数的思想从物理/几何推广到染色与分子同分异构体计数，是组合化学（化学异构体）的重要工具。OI Wiki《Pólya 计数》页给出完整理论推导与习题集，CP-Algorithms 的 Burnside 页也给出 PET 表述。现代竞赛中广泛用于项链、骰子、图的同构计数等『本质不同』问题。

## How · 实现

### 伪代码

```python
# 输入: 对称群 G 的置换列表(每个是位置集 X={0..n-1} 上的置换), 颜色数 m
# 输出: 本质不同染色数

def polya(G, m):
  total = 0
  for g in G:
    c = number_of_cycles(g)   # 分解 g 的轮换个数(含1-轮换)
    total += m ** c
  return total // len(G)       # 或模 p 意义下乘逆元

def number_of_cycles(g):
  seen = [False]*len(g); cnt = 0
  for i in range(len(g)):
    if not seen[i]:
      cnt += 1
      j = i
      while not seen[j]:
        seen[j] = True
        j = g[j]
  return cnt
# 带权重: 循环指标 Z(G)=Σ_g ∏_k z_k^{j_k(g)}/|G|, 答案=[w1^a1 w2^a2 ...] Z[z_k←Σ_c w_c^k]
```

### Python 实现

```python
from math import gcd


def cycle_count(perm):
    """置换 perm 的轮换个数(含1-轮换). perm[i] 表示位置 i 映射到 perm[i]."""
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


def polya_necklace(n, m):
    """n 颗珠子, m 种颜色, 项链(可旋转)本质不同染色数.
    旋转群: 第 k 次旋转把位置 i 移到 (i+k)%n."""
    g = 0
    for k in range(n):
        perm = [(i + k) % n for i in range(n)]
        g += m ** cycle_count(perm)
    return g // n


def polya_bracelet(n, m):
    """手链(可旋转+可翻转)本质不同染色数. 对奇/偶 n 分别给反射置换."""
    perms = [(i + k) % n for k in range(n) for i in range(n)]
    if n % 2 == 1:
        # 反射: 固定一个位置, 其余两两配对
        for k in range(n):
            perm = [(k - i) % n for i in range(n)]
            perms += perm
    else:
        # 两类反射: 过相对珠子 / 过相对边的中点
        for k in range(n // 2):
            perm = [(k - i) % n for i in range(n)]
            perms += perm
        for k in range(n // 2):
            perm = [(k + 1 - i) % n for i in range(n)]
            perms += perm
    total = 0
    for i in range(0, len(perms), n):
        total += m ** cycle_count(perms[i:i + n])
    return total // (len(perms) // n)


if __name__ == "__main__":
    # 4 珠 2 色项链, 旋转群: (2^4+2+2^2+2)/4 = 6 (OI Wiki 例子)
    assert polya_necklace(4, 2) == 6
    # 立方体 6 面 3 色, 空间对称群 24 元: (1*3^6 + 6*3^3 + 3*3^4 + 6*3^3 + 8*3^2)/24 = 57
    assert (3 ** 6 + 6 * 3 ** 3 + 3 * 3 ** 4 + 6 * 3 ** 3 + 8 * 3 ** 2) // 24 == 57
    # 3 珠 2 色手链: 旋转群(2^3+2+2)/3=4, 翻转群: (4*3)/6=2, 共 (8+2+2+8)/6... 直接验证
    from itertools import product
    n, m = 3, 2
    colors = list(product(range(m), repeat=n))
    seen = set()
    for c in colors:
        rots = set()
        for k in range(n):
            rots.add(tuple(c[(i + k) % n] for i in range(n)))
        for k in range(n):
            rots.add(tuple(c[(k - i) % n] for i in range(n)))
        seen.add(min(rots))
    assert polya_bracelet(n, m) == len(seen), (polya_bracelet(n, m), len(seen))
    print("polya-enumeration: all tests passed")

```

**PyPy 提示**: 置换轮换计数 O(n) 每次，群规模 \|G\| 通常很小（旋转群 n、二面体群 2n），直接迭代即可。m**c 用 Python 大整数自然支持；取模时用 pow(m, c, MOD)。当 n 较大且需要所有旋转的轮换数时，可用 gcd 性质：第 k 次旋转的轮换数 = gcd(n, k)，从而 O(n) 预处理 m^d 的幂次即可 O(n) 求项链答案（或 O(sqrt(n)) 按约数枚举）。P4980 模板题 n 达 1e9，必须用欧拉函数按约数分组：Σ_{k} m^{gcd(n,k)} = Σ_{d\|n} φ(n/d)·m^d。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 朴素 O(\|G\|·n)（每个置换数轮换）；项链用 gcd 性质 O(n log MOD) 或按约数 O(√n·d(n)) |
| 空间 | O(n)（记录 visited 数组） |

### 局限

① 只适用于『对称操作构成群』的场景，必须不重不漏枚举所有操作；② 无权重版本只给总数，受限颜色计数需带权（循环指标）版本；③ 结构复杂的图同构计数（如 P4128 有色图）轮换枚举本身很难，需对边置换群做二阶分析；④ 颜色数 m 大、结构大时 m^c 可能巨大，需模运算；⑤ 必须确保每个 g 是不动点的『完整』分析，漏操作即错。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P4980 | 4 | 【模板】Polya 定理：n 点环 k 色染色，n 达 1e9，用欧拉函数按约数分组 Σ_{d\|n}φ(n/d)·k^d，OI Wiki 模板 | [https://www.luogu.com.cn/problem/P4980](https://www.luogu.com.cn/problem/P4980) |
| Luogu | P1446 | 5 | HNOI2008 Cards：颜色受限（每种颜色张数固定），需 Burnside/带权 Pólya + 背包 DP 对每个置换轮换做组合计数 | [https://www.luogu.com.cn/problem/P1446](https://www.luogu.com.cn/problem/P1446) |
| Luogu | P2561 | 4 | AHOI2002 黑白瓷砖：三角形瓷砖旋转群，本质不同黑白染色数，OI Wiki 习题 | [https://www.luogu.com.cn/problem/P2561](https://www.luogu.com.cn/problem/P2561) |
| Luogu | P4128 | 6 | SHOI2006 有色图：Pólya 在边的置换群上的应用，图同构计数（边置换轮换数二阶分析） | [https://www.luogu.com.cn/problem/P4128](https://www.luogu.com.cn/problem/P4128) |

## Pitfalls · 易错点

- 把空间对称群（几何变换）与对称群（全体置换）混淆——Pólya 需要的是作用在位置集合上的置换表示
- 轮换计数忘掉 1-轮换（固定点），尤其旋转 0 次恒等置换的轮换数 = n 而非 1
- 翻转/反射置换写错：奇偶 n 的反射类型不同（固定 1 点 vs 不固定点）
- 取模时用整除而不是乘逆元
- 受限颜色计数直接套无权重公式 m^c（应改用循环指标多项式）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/combinatorics/polya/](https://oi-wiki.org/math/combinatorics/polya/)
- oiwiki-raw ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/combinatorics/polya.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/combinatorics/polya.md)
- CP-Algorithms ✓ [https://cp-algorithms.com/combinatorics/burnside.html](https://cp-algorithms.com/combinatorics/burnside.html)
- Wikipedia ✓ [https://en.wikipedia.org/wiki/Pólya_enumeration_theorem](https://en.wikipedia.org/wiki/Pólya_enumeration_theorem)
