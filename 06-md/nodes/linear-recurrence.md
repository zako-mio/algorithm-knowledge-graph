---
id: linear-recurrence
name: 线性递推
group: G-C-12
stage: advanced
priority: P2
depth_tier: standard
---

# 线性递推

> 常系数齐次线性递推O(k log k log n)求第n项，BM+NTT+Cayley-Hamilton

<!-- 元信息: id=linear-recurrence · group=G-C-12 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

常系数齐次线性递推：给定初值 a_0..a_{d-1} 与递推 a_n=Σ_{j=1}^d c_j a_{n-j}（n>=d），求 a_k（k 可极大）。直接迭代 O(dk) 或矩阵快速幂 O(d^3 log k) 太慢。Fiduccia 算法用特征多项式 Γ(x)=x^d-Σ_{j=0}^{d-1} c_{d-j}x^j，则 a_k=⟨x^k mod Γ, A(x)⟩（内积，A(x)=Σ a_j x^j），用多项式快速幂+取模做到 O(d log d log k)（NTT 加速乘法）。另一条路线 Bostan–Mori：把母函数写成有理函数 P(x)/Q(x)（Q(x)=x^dΓ(1/x)），通过 Q(x)Q(-x) 把系数减半迭代求 [x^k]P/Q，O(M(d) log k)。若递推未知，先用 Berlekamp-Massey 从序列恢复递推式，再套本算法。

## Why · 为什么

### 直觉 · Intuition

矩阵快速幂太浪费——转移矩阵其实是'友矩阵'，x^k mod Γ 抓住了它的本质：友矩阵 C 的第 i 列正是 x^i mod Γ 的系数向量，所以 C^k 的第一行= x^k mod Γ 的系数。多项式幂和取模比矩阵幂快得多。

### 原理 · Principle

Fiduccia: 定义内积 ⟨f,g⟩=Σ f_j g_j。由友矩阵性质 B_{x·b mod Γ}=C·B_b 归纳得 C^k=[B_{x^k mod Γ},…]，于是 a_k（即 (C^T)^k 的第一行点乘初值向量）=⟨x^k mod Γ, A⟩。x^k mod Γ 用快速幂（多项式乘法+取模），乘法用 NTT，得 O(d log d log k)。Bostan–Mori 用 Graeffe 迭代 P/Q = (P Q(-x))/(Q Q(-x)) = (U0(x²)+xU1(x²))/V(x²)，每轮只取 k 奇偶对应的一半，k 每次减半，代价两次多项式乘法。

### 历史 · History

Fiduccia 算法(1985)与 Bostan–Mori 算法(2020 年前后在 OI 普及)是求解线性递推的两大现代方法。Berlekamp(1968)–Massey(1969) 负责从序列反推递推式，三者组合成'黑盒线性递推'技术：给前 2d 项就能推出第 k 项。OI Wiki 的 poly/linear-recurrence 页面系统介绍。

## How · 实现

### 伪代码

```python
# Fiduccia: a_k = <x^k mod Gamma, A>
Gamma = [c_d, c_{d-1},...,c_1, -1] 反序的特征多项式系数
# 即 Gamma(x)=x^d - sum c_j x^{d-j}
res = poly_powmod(x^k mod Gamma)   # 快速幂+取模, 乘法用 NTT
ans = sum res[i]*init[i]

# Bostan-Mori: [x^k] P/Q
while k > 0:
    U0, U1 = split(P * Q(-x))       # P*Q(-x) 的偶/奇系数
    V = Q * Q(-x)
    P, Q = (U0|U1)[k&1], V(x)       # 取奇偶对应, 同时缩 k//2
return P(0)*inv(Q(0))
```

### Python 实现

```python
MOD = 998244353
ROOT = 3


def mod_pow(a, b, mod=MOD):
    r = 1
    while b:
        if b & 1:
            r = r * a % mod
        a = a * a % mod
        b >>= 1
    return r


def ntt(a, invert=False):
    n = len(a)
    a = a[:]
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    h = 2
    while h <= n:
        w_h = mod_pow(ROOT, (MOD - 1) // h)
        if invert:
            w_h = mod_pow(w_h, MOD - 2)
        for i in range(0, n, h):
            w = 1
            for j in range(i, i + h // 2):
                u = a[j]
                v = a[j + h // 2] * w % MOD
                a[j] = (u + v) % MOD
                a[j + h // 2] = (u - v) % MOD
                w = w * w_h % MOD
        h <<= 1
    if invert:
        inv_n = mod_pow(n, MOD - 2)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD
    return a


def poly_mul(a, b):
    if not a or not b:
        return []
    need = len(a) + len(b) - 1
    n = 1
    while n < need:
        n <<= 1
    fa = a[:] + [0] * (n - len(a))
    fb = b[:] + [0] * (n - len(b))
    fa = ntt(fa)
    fb = ntt(fb)
    for i in range(n):
        fa[i] = fa[i] * fb[i] % MOD
    fa = ntt(fa, True)
    return fa[:need]


def poly_inv(a, n):
    """多项式逆元(牛顿迭代). a[0] != 0. 返回前 n 项。"""
    assert a[0] != 0
    res = [pow(a[0], MOD - 2, MOD)]
    m = 1
    while m < n:
        m2 = min(m * 2, n)
        # res = res * (2 - a*res) mod x^m2
        t = poly_mul(a[:m2], res)
        t = t[:m2]
        t[0] = (2 - t[0]) % MOD
        for i in range(1, len(t)):
            t[i] = (-t[i]) % MOD
        res = poly_mul(res, t)[:m2]
        m = m2
    return res


def poly_divmod(f, g):
    """多项式带余除法 f=q*g+r 用 NTT 加速(系数低->高)。"""
    n, m = len(f), len(g)
    if n < m:
        return [], f[:]
    # q_rev = rev(f)_top * inv(rev(g)_top) mod x^{n-m+1}
    fr = f[::-1][:n - m + 1]
    gr = g[::-1]
    igr = poly_inv(gr, n - m + 1)
    qrev = poly_mul(fr, igr)[:n - m + 1]
    q = qrev[::-1]
    qg = poly_mul(q, g)
    r = [(f[i] - qg[i]) % MOD for i in range(m - 1)]
    return q, r


def linear_recurrence_fiduccia(init, coeff, k):
    """常系数齐次线性递推求第 k 项(0-index).
    init: a_0..a_{d-1}; coeff: c_1..c_d (a_n = sum c_j a_{n-j}).
    用 Fiduccia 算法: a_k = < x^k mod Gamma(x), A(x) >, 多项式乘幂用 NTT. O(d log d log k)."""
    d = len(coeff)
    if k < d:
        return init[k] % MOD
    # Gamma(x) = x^d - sum_{j=0}^{d-1} c_{d-j} x^j  (系数低->高)
    gamma = [0] * (d + 1)
    gamma[d] = 1
    for j in range(d):
        gamma[j] = (-coeff[d - 1 - j]) % MOD
    # A(x) = a_0 + a_1 x + ... + a_{d-1} x^{d-1}
    A = [x % MOD for x in init]
    # 计算 x^k mod Gamma
    res = [1]  # x^0
    base = [0, 1]  # x
    e = k
    while e:
        if e & 1:
            res = poly_mul(res, base)
            res = poly_mod(res, gamma)
        base = poly_mul(base, base)
        base = poly_mod(base, gamma)
        e >>= 1
    # 内积
    ans = 0
    for i in range(min(len(res), d)):
        ans = (ans + res[i] * A[i]) % MOD
    return ans


def poly_mod(f, g):
    q, r = poly_divmod(f, g)
    return r


def linear_recurrence_naive(init, coeff, k):
    """朴素 O(d^2 k) 验证用。"""
    d = len(coeff)
    a = [x % MOD for x in init]
    if k < len(a):
        return a[k]
    for i in range(len(a), k + 1):
        s = 0
        for j in range(d):
            s = (s + coeff[j] * a[i - 1 - j]) % MOD
        a.append(s)
    return a[k]


if __name__ == "__main__":
    import random
    # Fibonacci: F_0=0,F_1=1, F_n=F_{n-1}+F_{n-2}; coeff c1=1,c2=1
    init = [0, 1]
    coeff = [1, 1]
    for k in range(20):
        assert linear_recurrence_fiduccia(init, coeff, k) == linear_recurrence_naive(init, coeff, k), k
    assert linear_recurrence_fiduccia([0, 1], [1, 1], 10) == 55
    # 随机递推对拍
    for _ in range(20):
        d = random.randint(1, 5)
        init = [random.randint(0, 10) for _ in range(d)]
        coeff = [random.randint(0, 10) for _ in range(d)]
        k = random.randint(0, 40)
        a = linear_recurrence_fiduccia(init, coeff, k)
        b = linear_recurrence_naive(init, coeff, k)
        assert a == b, (init, coeff, k, a, b)
    print("linear-recurrence (Fiduccia+NTT) tests passed")

```

**PyPy 提示**: Python 用 NTT 实现多项式乘法与取模, 小规模(1e4 以下)可跑通; 大规模建议 C++。教学版提供朴素除法验证正确性。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | Fiduccia/Bostan-Mori: O(M(d) log k)=O(d log d log k)(NTT) |
| 空间 | O(d) |

### 局限

仅适用于常系数齐次线性递推(非齐次需先转化); 初值/系数需齐全; Python 实现 NTT+取模链常数大, 大规模不现实; 若递推未知需先跑 BM(需足够项数, 一般 2d 项)。模数若非 NTT 友好素数, 复杂度退化为普通多项式乘法。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P4721 | 5 | 分治 FFT 求线性递推(配合 NTT), 经典进阶题 | [https://www.luogu.com.cn/problem/P4721](https://www.luogu.com.cn/problem/P4721) |
| Codeforces | 1851G | 5 | BM+线性递推组合应用类问题的参考 | [https://codeforces.com/problemset/problem/1851/G](https://codeforces.com/problemset/problem/1851/G) |
| Library Checker | find_linear_recurrence | 4 | 求序列线性递推模板题(BM) | [https://judge.yosupo.jp/problem/find_linear_recurrence](https://judge.yosupo.jp/problem/find_linear_recurrence) |

## Pitfalls · 易错点

- 特征多项式符号/反序搞错(Γ 系数方向)
- x^k mod Γ 快速幂时忘记 mod(结果超出度 d)
- 内积只取前 d 项(Γ 次数为 d 时 res 长度<=d)
- Bostan-Mori 偶奇拆分时下标与 k 奇偶对应错位
- 递推未知时直接套 Fiduccia(需先 BM 求递推)

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/poly/linear-recurrence/](https://oi-wiki.org/math/poly/linear-recurrence/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/poly/linear-recurrence.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/poly/linear-recurrence.md)
- web ✓ [https://arxiv.org/abs/2008.08822](https://arxiv.org/abs/2008.08822)
