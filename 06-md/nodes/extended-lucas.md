---
id: extended-lucas
name: 扩展卢卡斯(exLucas)
group: G-C-8
stage: advanced
priority: P1
depth_tier: standard
---

# 扩展卢卡斯(exLucas)

> C(n,m) mod p 当 p 为合数时：分解 p=∏p_i^α_i，对每个素因子幂用『去 p 因子阶乘+Legendre 公式』求余，CRT 合并；处理任意模数组合数

<!-- 元信息: id=extended-lucas · group=G-C-8 · stage=advanced · priority=P1 · depth_tier=standard -->

## What · 是什么

扩展卢卡斯算法（exLucas）解决 Lucas 定理无法处理的合数模情形：求 C(n,m) mod P（P 任意正整数）。步骤：(1) 分解 P=∏ p_i^α_i；(2) 对每个素数幂 p^α，把 n! 写成 n! = p^ν_p(n!) · (n!)_p（(n!)_p 为去掉全部 p 因子后的互素部分），用 Legendre 公式算指数 ν_p，用『素数幂模下的阶乘递推』算 (n!)_p 及其逆元，得余数；(3) 中国剩余定理合并各余数。算法并不使用 Lucas 定理本身，只是名字沿袭。

## Why · 为什么

### 直觉 · Intuition

合数模下 0 不能求逆、阶乘不总可逆，Lucas 按 p 进制拆位失效。于是换个思路：C(n,m)=n!/(m!(n−m)!)，把 n! 里的所有 p 因子全部抽出来单独算指数（Legendre 公式），剩下的『互素部分』在 p^α 下可求逆（扩展欧几里得）。每个素因子 p 处理完得到一条同余，最后 CRT 拼回模 P。

### 原理 · Principle

记 (n!)_p = n! / p^ν_p(n!)。组合数 = p^[ν_p(n!)−ν_p(m!)−ν_p((n−m)!)] · (n!)_p / ((m!)_p (n−m)!)_p。指数部分若 ≥α 则余数直接为 0；否则 p^e 单独算（pow(p,e,pk)）。互素部分：对 n! 的 p 幂模，用周期分解——把 1..pk 中非 p 倍数乘积记为 cycle，则 (n!)_p = cycle^(⌊n/pk⌋) · (⌊n/pk⌋)!_p · ∏(1..n mod pk 中非 p 倍数)。递归算 (⌊n/pk⌋)!_p，深度 O(log_p n)。分母部分乘逆元（扩展欧几里得或 pow(x,−1,pk)）。

### 历史 · History

Lucas 定理仅适用于素数模；Andrew Granville 于 1997 年在《The Arithmetic of Binomial Coefficients》中给出素数幂模 C(n,m) 的完整推广（含指数项与互素部分）。竞赛中的『exLucas』实现（LOJ 181、洛谷 P4720）即按上述素数幂分解+CRT 流程，OI Wiki 将其单列于 Lucas 页面下。

## How · 实现

### 伪代码

```python
# 对素数幂 p^a:
def legendre(n, p):       # ν_p(n!)
  s = 0
  while n: n //= p; s += n
  return s
def fact_mod(n, p, pk):   # (n!)_p mod pk
  if n == 0: return 1
  cycle = prod(1..pk 中非 p 倍数的数) % pk
  res = pow(cycle, n // pk, pk)
  res = res * prod(1..n%pk 中非 p 倍数) % pk
  res = res * fact_mod(n // p, p, pk) % pk
  return res
def comb_ppow(n, m, p, a):
  pk = p**a
  e = legendre(n,p) - legendre(m,p) - legendre(n-m,p)
  if e >= a: return 0
  return p**e * fact_mod(n,p,pk) % pk * inv(fact_mod(m,p,pk)*fact_mod(n-m,p,pk)) % pk
# 主流程
exlucas(n, m, P):
  分解 P = ∏ p_i^α_i
  对每个 p_i^α_i 求 r_i = comb_ppow(n,m,p_i,α_i)
  return CRT(r_i, p_i^α_i)
```

### Python 实现

```python
import math
from math import gcd


def legendre_p(n, p):
    """ν_p(n!) = n//p + n//p^2 + ..."""
    res = 0
    while n:
        n //= p
        res += n
    return res


def fact_without_p(n, p, pk):
    """返回 (n!)_p mod pk，即去掉全部 p 因子后的余数。"""
    if n == 0:
        return 1
    cycle = 1
    for i in range(1, pk + 1):
        if i % p:
            cycle = cycle * i % pk
    res = pow(cycle, n // pk, pk)
    for i in range(1, n % pk + 1):
        if i % p:
            res = res * i % pk
    res = res * fact_without_p(n // p, p, pk) % pk
    return res


def comb_mod_prime_power(n, m, p, a):
    """C(n,m) mod p^a"""
    pk = p ** a
    e = legendre_p(n, p) - legendre_p(m, p) - legendre_p(n - m, p)
    if e >= a:
        return 0
    numer = fact_without_p(n, p, pk)
    denom = fact_without_p(m, p, pk) * fact_without_p(n - m, p, pk) % pk
    res = pow(p, e, pk) * numer % pk * pow(denom, -1, pk) % pk
    return res


def exlucas(n, m, mod):
    """C(n,m) mod mod（mod 为任意正整数）。"""
    if m < 0 or m > n:
        return 0
    if mod == 1:
        return 0
    mm = mod
    factors = []
    d = 2
    while d * d <= mm:
        if mm % d == 0:
            a = 0
            while mm % d == 0:
                mm //= d
                a += 1
            factors.append((d, a))
        d += 1
    if mm > 1:
        factors.append((mm, 1))

    rs = []
    mods = []
    for p, a in factors:
        rs.append(comb_mod_prime_power(n, m, p, a))
        mods.append(p ** a)
    total = 1
    for mi in mods:
        total *= mi
    x = 0
    for r, mi in zip(rs, mods):
        t = total // mi
        x = (x + r * t * pow(t, -1, mi)) % total
    return x


if __name__ == "__main__":
    # 全范围交叉验证（模数含平方因子）
    for mod in range(2, 42):
        for n in range(0, 28):
            for m in range(0, n + 1):
                assert exlucas(n, m, mod) == math.comb(n, m) % mod, (n, m, mod)

    # 经典样例
    assert exlucas(5, 2, 6) == 4
    assert exlucas(7, 3, 10) == 5
    assert exlucas(100, 50, 999999999) == math.comb(100, 50) % 999999999
    # n 较大、模数含素因子高次幂（n 足够大，结果仍精确）
    n = 200000
    assert exlucas(n, n // 3, 2**5 * 3**3) == math.comb(n, n // 3) % (2**5 * 3**3)
    # n 巨大（>1e18）时只做自洽性检查：结果在 [0, mod) 内且 mod 各因子幂同余一致
    big = 10**18
    r = exlucas(big, big // 3, 2**5 * 3**3)
    assert 0 <= r < 2**5 * 3**3
    for pk in (2**5, 3**3):
        assert r % pk == exlucas(big, big // 3, pk)

    print("All tests passed.")
```

**PyPy 提示**: fact_without_p 中每次枚举 1..pk（pk=p^α）与递归 log_p n 层，单次 comb 的复杂度约 O(p^α + log_p n·p^α/2 的枚举)——注意 cycle 与余数枚举均 O(pk)，所以 p^α 很大时（如 >1e6）单次查询退化。可用前缀积数组优化 cycle。递归深度 O(log_p n)，Python 默认递归限制 1000 足够（log_p(1e18)≈60）。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 分解 P O(√P)；对每个素因子幂预处理 O(p^α)；单次查询 O(∑(p^α log) + log_p n 递归)；总计 O(√P + ∑p_i^α_i + ∑log_{p_i} n) |
| 空间 | O(∑ p_i^α_i)（cycle 可 O(1) 但需预处理则 O(pk)） |

### 局限

fact_without_p 的 cycle 若每次重建（循环 1..pk）则每层 O(pk)，pk 大时慢，应预处理为全局表。逆元 pow(x,-1,pk) 要求 x 与 pk 互素——已去掉 p 因子故必然成立。P 可能含重复素数幂（如 8=2^3），分解时聚合幂次。n 巨大（>1e18 也无碍，Python 大整数）。Lucas 不适合大素数模（p 本身 >1e7 时 O(p) 预处理不行，若 p 是极大素数则回到组合数单点算法）。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P4720 | 5 | 【模板】扩展卢卡斯：任意模数 P，n,m≤1e18，直接套 exLucas 全流程 | [https://www.luogu.com.cn/problem/P4720](https://www.luogu.com.cn/problem/P4720) |
| LibreOJ | LOJ 181 | 5 | 【模板】二项式系数：OI Wiki 官方模板题，素数幂分解+CRT 合并 | [https://loj.ac/p/181](https://loj.ac/p/181) |
| Codeforces | Gym 100633 J (Ceizenpok's formula) | 6 | Ceizenpok's formula：n 可达 1e18 的 exLucas 变形（OI Wiki 习题引用） | [http://codeforces.com/gym/100633/problem/J](http://codeforces.com/gym/100633/problem/J) |

## Pitfalls · 易错点

- 指数 e=ν_p(n!)−ν_p(m!)−ν_p((n−m)!)≥α 时结果必为 0，必须先判再算（否则 p^e mod pk=0 但后面分母不可逆）
- fact_without_p 里 cycle 枚举到 pk（含端点），若 i%p 为 0 要跳过
- 递归时参数是 n//p 而非 n//pk——Lucas 递归取 p 进制高位的直觉在 exLucas 里是每层除一次 p
- CRT 合并时各 mod 必须互素（素因子幂天然互素），用 pow(t,-1,mi) 需 Python3.8+；旧版本手写扩展欧几里得
- P=1 时 C(n,m) mod 1=0，特判返回 0
- 分解 P 时用 mm 变量累除，别污染原 mod；合数分解后 mm>1 的剩余是最大素因子

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/number-theory/lucas/](https://oi-wiki.org/math/number-theory/lucas/)
- CP-Algorithms ✓ [https://cp-algorithms.com/algebra/factorial-modulo.html](https://cp-algorithms.com/algebra/factorial-modulo.html)
- CP-Algorithms ✓ [https://cp-algorithms.com/algebra/crt.html](https://cp-algorithms.com/algebra/crt.html)
