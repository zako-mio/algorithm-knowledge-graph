---
id: fermat-little-theorem
name: 费马小定理
group: G-C-7
stage: intermediate
priority: P0
depth_tier: deep
---

# 费马小定理

> p素数时a^(p-1)≡1(mod p)，模逆元与素性检测的理论基础

<!-- 元信息: id=fermat-little-theorem · group=G-C-7 · stage=intermediate · priority=P0 · depth_tier=deep -->

## What · 是什么

费马小定理（Fermat's little theorem）：设 p 为素数，对任意整数 a，若 p∤a 则 a^(p-1)≡1 (mod p)；等价地，对任意整数 a 均有 a^p≡a (mod p)。它是欧拉定理（a^φ(m)≡1 mod m, gcd(a,m)=1）在素数模下的特例，因为 φ(p)=p-1。定理解决了任意素数模下大指数幂的降幂计算问题，是模逆元（a^(p-2) mod p）、Fermat 素性测试与 Miller-Rabin 的理论基础。

## Why · 为什么

### 直觉 · Intuition

把 1,2,…,p-1 这 p-1 个数看成模 p 的剩余系。将它们全部乘以 a（a 与 p 互素），所得 p-1 个余数仍是 {1,2,…,p-1} 的一个排列（只是顺序变了）。于是排列前全体之积 ≡ 排列后全体之积，即 (p-1)! ≡ a^(p-1)·(p-1)! (mod p)，两边消去 (p-1)! 即得 a^(p-1)≡1。

### 原理 · Principle

设 R={1,…,p-1}。因 gcd(a,p)=1，映射 r→ar mod p 是 R→R 的双射（若 ia≡ja 则 (i-j)a≡0，因 a 可逆故 i≡j）。故 ∏r∈R r ≡ ∏r∈R (ar) = a^(p-1)·∏r∈R r (mod p)，消去 ∏r 得 a^(p-1)≡1。第二种形式 a^p≡a 可用归纳法+二项式定理证明：(a+1)^p≡a^p+1≡a+1，组合数 C(p,k) 在 0<k<p 时被 p 整除。

### 历史 · History

费马约 1640 年在致 Frénicle 的信中提出，未给出证明。欧拉 1736 年首次公开发表证明。莱布尼茨更早的手稿中已有等价结果但未发表。它是数论中最古老的定理之一。

## How · 实现

### 伪代码

```python
# 计算 a^k mod p（p 为素数），利用费马小定理降幂
if gcd(a,p)==1:
    exponent = k mod (p-1)   # 费马小定理降幂
else:
    exponent = k              # 不能直接降幂
return pow(a, exponent, p)
# 求模逆元 a^{-1} mod p（p 素数，a 不为 0）
return pow(a, p-2, p)
```

### Python 实现

```python
# 费马小定理：模逆元 + 降幂验证
import sys, math

def modinv(a, p):
    """费马小定理求逆元: a^{-1} = a^(p-2) mod p (p 素数)"""
    return pow(a, p - 2, p)

def is_prime(n):
    """试除法判素数（用于保证模数是素数）"""
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True

def fermat_lower(a, k, p):
    """利用费马小定理对 a^k mod p 降幂 (p 素数, gcd(a,p)=1)"""
    if math.gcd(a, p) != 1:
        return pow(a, k, p)  # 不互素不能降
    return pow(a, k % (p - 1), p)

if __name__ == "__main__":
    P = 998244353  # 常见竞赛素数模
    assert is_prime(P)
    # 1) 逆元验证: a * inv(a) ≡ 1
    a = 123456789
    inv = modinv(a, P)
    assert (a * inv) % P == 1, "逆元错误"
    # 2) 费马小定理本身: a^(p-1) ≡ 1 (p 素数, p∤a)
    assert pow(a, P - 1, P) == 1, "费马小定理失败"
    # 3) 降幂正确性: a^k mod p == a^(k mod (p-1)) mod p
    k = 10**18
    assert fermat_lower(a, k, P) == pow(a, k, P), "降幂错误"
    print("fermat-little-theorem OK")

```

**PyPy 提示**: PyPy 下 pow(a,b,mod) 走的是底层 C 实现，速度与 CPython 相当（均 O(log b)）。大数快速幂自写循环在 PyPy JIT 下反而可能更快（纯整数循环可被 JIT 优化），但一般直接用内置 pow 最稳妥。注意 PyPy 大整数乘法常数略大，b 较大时差距可忽略。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 逆元/降幂计算 O(log p)（快速幂）；费马小定理验证单次 O(log p) |
| 空间 | O(1) |

### 局限

1) 逆公式 a^(p-2) 仅在 p 为素数时成立，合数模需用扩展欧几里得；2) 费马小定理的逆不成立（Carmichael 数如 561 满足 ∀a⊥n: a^(n-1)≡1 但 n 非素），故不能仅靠它做可靠素性检测；3) gcd(a,p)≠1 时不能直接降幂，需用扩展欧拉定理。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1082 | 2 | ax≡1 mod b 最小正整数解；b 素数时 pow(a,b-2,b) | [https://www.luogu.com.cn/problem/P1082](https://www.luogu.com.cn/problem/P1082) |
| Luogu | P5091 | 4 | a^b mod m 降幂；素数模退化为费马小定理 | [https://www.luogu.com.cn/problem/P5091](https://www.luogu.com.cn/problem/P5091) |
| Codeforces | 906D | 6 | 幂塔 a↑↑b mod m 递归扩展欧拉降幂 | [https://codeforces.com/problemset/problem/906/D](https://codeforces.com/problemset/problem/906/D) |

## Pitfalls · 易错点

- p 不是素数时 a^(p-2) 不是逆元，必须先验证素性或改用 exgcd
- gcd(a,p)≠1 时 a^(p-1)≢1，费马降幂失效；需改用扩展欧拉定理三段式
- 误把费马小定理当作素数判定的充要条件——Carmichael 数（561,1105,1729…）是反例，满足 ∀a⊥n:a^(n-1)≡1 但 n 合数
- pow(a,p-2,p) 中 p-2 为负当 p<2，需处理 p=2 的边界
- k mod (p-1) 当 gcd(a,p)≠1 时结果错误，需额外判断是否 k≥φ(p) 再加 φ(p)

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/number-theory/fermat/](https://oi-wiki.org/math/number-theory/fermat/)
- CP-Algorithms ✓ [https://cp-algorithms.com/algebra/module-inverse.html](https://cp-algorithms.com/algebra/module-inverse.html)
- 书籍 ✓ `CPH ch21 Number theory (p207-216)`
