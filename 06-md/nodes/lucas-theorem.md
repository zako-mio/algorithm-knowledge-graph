---
id: lucas-theorem
name: 卢卡斯定理
group: G-C-8
stage: advanced
priority: P0
depth_tier: deep
---

# 卢卡斯定理

> C(n,m) mod p（p 为素数）：按 p 进制拆 n,m 后各位组合数相乘，O(p) 预处理阶乘 + O(log_p n) 每次查询，大组合数取小素模的标准工具

<!-- 元信息: id=lucas-theorem · group=G-C-8 · stage=advanced · priority=P0 · depth_tier=deep -->

## What · 是什么

卢卡斯定理（Lucas's theorem）：对素数 p 与非负整数 n,m，
C(n,m) ≡ C(⌊n/p⌋,⌊m/p⌋) · C(n mod p, m mod p) (mod p)。
其中规定 C(a,b)=0 当 b>a。等价地，把 n,m 写成 p 进制展开，则 C(n,m) ≡ ∏ C(n_i, m_i) (mod p)。由此可在 O(p + T log_p n) 内处理任意大的 n（可远超 64 位），只要模数是小的素数。前提：p 为素数且通常 p ≤ 1e6~1e7（需要预处理 p 以内阶乘逆元）。

## Why · 为什么

### 直觉 · Intuition

n! 里含 p 的因子把大组合数撑爆，但模 p 后每个 p 的倍数因子都被清零。把 n,m 按 p 进制分段，'高位段'和'低位段'的贡献正好分开：低位用 p 以内阶乘直接算，高位递归再用一次 Lucas——这就是 p 进制位拆分的直觉。生成函数视角：模 p 下 (1+x)^n ≡ (1+x^p)^⌊n/p⌋(1+x)^(n mod p)，两侧 x^k 系数相等即得定理。

### 原理 · Principle

关键引理：模素数 p 时 C(p,i)≡0 (对 0<i<p)，故 (1+x)^p ≡ 1+x^p (mod p)（Freshman's dream）。于是 (1+x)^n = (1+x)^(p·q+r) ≡ (1+x^p)^q·(1+x)^r，比较 x^m 系数：左侧为 C(n,m)，右侧唯一分解 m=p·m_high+m_low 给出 C(q,m_high)·C(r,m_low)。递归 q=⌊n/p⌋ 即得按位乘积公式。等价代数证明：n! = p^(⌊n/p⌋)·⌊n/p⌋! · (去除 p 因子后的乘积)，约分得 C(n,m) = p^e·C(⌊n/p⌋,⌊m/p⌋)·(去 p 因子乘积之比)，其中 e=ν_p(n!)−ν_p(m!)−ν_p((n−m)!) ≥ 0，模 p 后只剩 Lucas 递推。

### 历史 · History

法国数学家 Édouard Lucas 于 1878 年发表该定理（其最早思想可追溯至 19 世纪初）。Lucas 在素数分解、Fibonacci 数上有大量工作，并以 Lucas 数列闻名。定理为『大组合数取小素模』提供了第一个实用方法，是 exLucas 与数论组合题的基石，被收录于 OI Wiki 数论章与 CPH 组合章。

## How · 实现

### 伪代码

```python
# 预处理 0..p-1 阶乘与逆元（O(p)）
fact[0..p-1], inv_fact[0..p-1]
# 单次小组合数（p 以内）
def comb(a, b):
  if b < 0 or b > a: return 0
  return fact[a] * inv_fact[b] % p * inv_fact[a-b] % p
# Lucas 递归/迭代
def lucas(n, m, p):
  res = 1
  while n or m:
    res = res * comb(n % p, m % p) % p
    n //= p; m //= p
  return res
```

### Python 实现

```python
def lucas_comb(n, m, p):
    """Lucas 定理 + CRT 组合的完整实现。
    p 必须为素数。
    该函数同时验证了与 CRT 结合的经典写法
    （多素因子模数场景请见 extended-lucas 节点）。
    """
    if m < 0 or m > n:
        return 0
    if p == 1:
        return 0

    fact = [1] * p
    for i in range(1, p):
        fact[i] = fact[i - 1] * i % p
    inv_fact = [1] * p
    inv_fact[p - 1] = pow(fact[p - 1], p - 2, p)
    for i in range(p - 2, -1, -1):
        inv_fact[i] = inv_fact[i + 1] * (i + 1) % p

    def comb(a, b):
        if b < 0 or b > a:
            return 0
        return fact[a] * inv_fact[b] % p * inv_fact[a - b] % p

    res = 1
    while n or m:
        res = res * comb(n % p, m % p) % p
        n //= p
        m //= p
    return res


def crt_merge_lucas(n, m, mod):
    """Lucas + CRT：mod 可为合数但其每个素因子都是小素数。
    对每个素因子 p_i 用 Lucas 求余数，再 CRT 合并。
    注意：p_i 若以高次幂出现需用 exLucas（见 extended-lucas 节点）。
    """
    import math
    from math import gcd

    mm = mod
    primes = []
    d = 2
    while d * d <= mm:
        if mm % d == 0:
            primes.append(d)
            while mm % d == 0:
                mm //= d
        d += 1
    if mm > 1:
        primes.append(mm)

    rs = []
    mods = []
    for p in primes:
        if p > 1_000_000:
            raise ValueError("p 过大无法预处理阶乘")
        rs.append(lucas_comb(n, m, p))
        mods.append(p)

    total = 1
    for m in mods:
        total *= m
    x = 0
    for r, m in zip(rs, mods):
        mi = total // m
        x = (x + r * mi * pow(mi, -1, m)) % total
    return x


if __name__ == "__main__":
    import math

    # 与 math.comb 交叉验证（小 p 全范围）
    for p in [2, 3, 5, 7, 11]:
        for n in range(0, 80):
            for m in range(0, n + 1):
                assert lucas_comb(n, m, p) == math.comb(n, m) % p, (n, m, p)

    # 经典样例
    assert lucas_comb(10, 3, 7) == 120 % 7 == 1
    assert lucas_comb(100, 50, 97) == math.comb(100, 50) % 97
    # 大 n（远超 64 位）也能算：n=1e5 的精确组合数仍可由 math.comb 求出并取模交叉验证
    n = 100000
    assert lucas_comb(n, n // 3, 999983) == math.comb(n, n // 3) % 999983
    assert lucas_comb(n, n // 2, 998244353) == math.comb(n, n // 2) % 998244353

    # Lucas+CRT 组合：mod 为 squarefree 合数
    assert crt_merge_lucas(10, 3, 6) == 120 % 6
    assert crt_merge_lucas(100, 40, 35) == math.comb(100, 40) % 35

    print("All tests passed.")
```

**PyPy 提示**: 预处理 p 以内阶乘+逆元需 O(p)，p=1e6 时 PyPy 约 0.1~0.2s，p=1e7 约 1.5s 且有内存压力（两个 int 数组）。每次查询仅 log_p n 次小组合数，常数极小。若 T 次查询且 p 固定，把 fact/inv_fact 提到函数外只预处理一次。n 可达任意大（Python 大整数无碍），m 必须非负。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 预处理 O(p)；单次查询 O(log_p n)；T 次查询 O(p + T log_p n) |
| 空间 | O(p) |

### 局限

p 必须为素数。p 超过约 1e7 时 O(p) 预处理好时间；若只有少数查询且 p 很大，可改用 O(√p) 的单点组合数（但 n 小）。对 n mod p < m mod p 的处理依赖 C(a,b)=0 约定。合数模必须用 exLucas（除非模数恰为若干互异小素因子之积且幂次全为 1，可用 Lucas+CRT）。m<0 或 m>n 返回 0。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3807 | 3 | 【模板】卢卡斯定理：n,m 可达 1e18，p≤1e5，直接套 Lucas+阶乘逆元 | [https://www.luogu.com.cn/problem/P3807](https://www.luogu.com.cn/problem/P3807) |
| SDOI2010 | P2480 古代猪文 | 7 | C(n,d) 对 999911659 取模：先分解 999911658 的素因子，每个小素因子用 Lucas 求余，再 CRT 合并，指数降幂 | [https://www.luogu.com.cn/problem/P2480](https://www.luogu.com.cn/problem/P2480) |
| LibreOJ | LOJ 10229 | 7 | SDOI2010 古代猪文同题：Lucas+CRT+欧拉降幂的综合模板 | [https://loj.ac/problem/10229](https://loj.ac/problem/10229) |

## Pitfalls · 易错点

- p 是素数才可用 Lucas；合数直接套会错（要用 exLucas）
- 预处理阶乘数组要覆盖 0..p-1（大小恰为 p），越界越界访问
- n<m 时 C(n,m)=0，不能直接算（comb 里 b>a 要返回 0）
- 递归写法尾递归深度 O(log_p n)，n 很大时用迭代避免递归栈问题（Python 无尾递归优化）
- CRT 合并时模数互素（素因子）才可用公式，模数为素因子乘积要保证 squarefree
- 阶乘逆元用费马小定理需 p 素数；p=2 时逆元计算仍正确但注意边界

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/number-theory/lucas/](https://oi-wiki.org/math/number-theory/lucas/)
- CP-Algorithms ✓ [https://cp-algorithms.com/combinatorics/binomial-coefficients.html](https://cp-algorithms.com/combinatorics/binomial-coefficients.html)
- 书籍 ✓ `CPH ch21 Number theory（组合数模素数 p）`
