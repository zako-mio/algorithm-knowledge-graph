---
id: newton-iteration-poly
name: 多项式牛顿迭代
group: G-C-12
stage: frontier
priority: P3
depth_tier: brief
---

# 多项式牛顿迭代

> O(n log n)求多项式开根/对数/指数/逆，基于牛顿法推广到形式幂级数

<!-- 元信息: id=newton-iteration-poly · group=G-C-12 · stage=frontier · priority=P3 · depth_tier=brief -->

## What · 是什么

多项式牛顿迭代：求形式幂级数 f(x) 满足 G(x,f(x))≡0 (mod x^n)（如求逆、开方、指数、对数、exp、三角函数等）。由泰勒展开，若 f_n 是模 x^n 的解，则 f_{2n} = f_n - G(x,f_n)/G_y(x,f_n) (mod x^{2n})，其中 G_y 是 G 对 y 的偏导。因此每次把精度翻倍，T(n)=T(n/2)+O(M(n))=O(M(n) log n)=O(n log n)（NTT）。具体：求逆 f_{2n}=2f_n - f_n²·h；开方 f_{2n}=(f_n + h/f_n)/2；ln(f)=∫f'/f；exp 用 f·(1-ln f+a)。这套机制支撑整个多项式全家桶的 O(n log n) 实现。

## Why · 为什么

### 直觉 · Intuition

解一个模 x^{2n} 的方程，先用较小的解 f_n（对 x^n 成立），把 G 在 f_n 处泰勒展开，因为修正项 h=f-f_n 的最低次>=n，h² 在模 x^{2n} 下消失，方程变成线性的，直接解出 h。每轮长度翻倍。

### 原理 · Principle

G(f_n+h)≡G(f_n)+G_y(f_n)·h (mod x^{2n})。令其为 0 得 h=-G(f_n)/G_y(f_n)，即迭代公式。这是分析学牛顿法的形式幂级数推广。求逆时 G(x,y)=1/y-h(x)，得 f_{2n}=2f_n-f_n²h。开方 G=y²-h(x)，得 f_{2n}=(f_n+h/f_n)/2。exp 由 g=ln f-a 的根给出。底子都需要 NTT 卷积。

### 历史 · History

形式幂级数的牛顿迭代源自 1970s 计算代数（Sieveking, Kung 等），是现代多项式算法的核心框架，Modern Computer Algebra 有系统论述。OI 中 2010s 由多项式全家桶（求逆/ln/exp/开方）带入，OI Wiki 的 poly/newton 页面给出完整推导与各应用。

## How · 实现

### 伪代码

```python
# 通用迭代
f = 初始解(mod x^1, 如 sqrt 需要二次剩余解)
m = 1
while m < n:
    m2 = min(2m, n)
    f = f - G(x,f) / G_y(x,f)   (mod x^{m2})
    m = m2
# 具体: 求逆 f_{2n}=2f-f²h; 开方 f_{2n}=(f+h/f)/2; exp f·(1-ln f+a)
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
    res = [pow(a[0], MOD - 2, MOD)]
    m = 1
    while m < n:
        m2 = min(m * 2, n)
        t = poly_mul(a[:m2], res)
        t = t[:m2]
        t[0] = (2 - t[0]) % MOD
        for i in range(1, len(t)):
            t[i] = (-t[i]) % MOD
        res = poly_mul(res, t)[:m2]
        m = m2
    return res


def newton_sqrt(a, n):
    """牛顿迭代开方: 求 f(x) = x^2 - h(x) = 0 的解, h(x)=a.
    需要二次剩余解 f_1 = sqrt(a[0]). 简化: 仅支持 a[0]=1(平方为 1)."""
    assert a[0] == 1, "教学版仅演示 a[0]=1 的开方"
    res = [1]
    m = 1
    while m < n:
        m2 = min(m * 2, n)
        # f_next = f - (f^2 - a)/(2f) = (f + a/f)/2
        a_ = a[:m2]
        invf = poly_inv(res, m2)
        t = poly_mul(invf, a_)[:m2]
        new = [0] * m2
        for i in range(m2):
            new[i] = ((res[i] if i < len(res) else 0) + t[i]) % MOD
        inv2 = (MOD + 1) // 2
        res = [x * inv2 % MOD for x in new]
        m = m2
    return res


def poly_log(a, n):
    """多项式对数 ln(f) = integral(f'/f) mod x^n. f[0]=1."""
    assert a[0] == 1
    f = a[:n]
    df = [(i * f[i]) % MOD for i in range(1, len(f))]
    invf = poly_inv(f, n)
    q = poly_mul(df, invf)[:n - 1]
    inv = [0] * n
    inv[1] = 1
    for i in range(2, n):
        inv[i] = (MOD - MOD // i) * inv[MOD % i] % MOD
    res = [0]
    for i in range(len(q)):
        res.append(q[i] * inv[i + 1] % MOD)
    return res[:n]


def poly_exp(a, n):
    """牛顿迭代指数: exp(a), a[0]=0. 迭代 f = f*(1 - ln f + a)."""
    assert a[0] == 0
    res = [1]
    m = 1
    while m < n:
        m2 = min(m * 2, n)
        lnf = poly_log(res, m2)
        t = [0] * m2
        for i in range(m2):
            t[i] = ((a[i] if i < len(a) else 0) - (lnf[i] if i < len(lnf) else 0)) % MOD
        t[0] = (t[0] + 1) % MOD
        res = poly_mul(res, t)[:m2]
        m = m2
    return res


def poly_log_naive(a, n):
    """朴素 ln 验证。"""
    f = a[:n]
    # 逐项递推: ln f 系数 g: n*g_n = f_n - sum_{k=1}^{n-1} k*g_k*f_{n-k} (g0=0)
    g = [0] * n
    for i in range(1, n):
        s = 0
        for k in range(1, i):
            s = (s + k * g[k] * f[i - k]) % MOD
        g[i] = (f[i] - s) * pow(i, MOD - 2, MOD) % MOD
    return g


def exp_naive_pow(a, n):
    """exp(a) = sum a^k/k! 朴素验证。"""
    res = [0] * n
    res[0] = 1
    cur = [1]
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD
    for k in range(0, n):
        if k == 0:
            cur = [1]
        else:
            cur = poly_mul(cur, a[:n])[:n]
        invk = pow(fact[k], MOD - 2, MOD)
        for i in range(n):
            res[i] = (res[i] + cur[i] * invk) % MOD
        if k >= n:
            break
    return res


if __name__ == "__main__":
    import random
    # 牛顿开方: sqrt(1+x) 的系数
    a = [1, 1, 0, 0, 0, 0, 0, 0]
    sq = newton_sqrt(a, 8)
    # 检查 sq^2 = a mod x^8
    sq2 = poly_mul(sq, sq)[:8]
    assert sq2 == [1, 1, 0, 0, 0, 0, 0, 0], sq2
    # ln: ln(1+x)
    ln = poly_log([1, 1, 0, 0, 0, 0, 0, 0], 8)
    ln_naive = poly_log_naive([1, 1, 0, 0, 0, 0, 0, 0], 8)
    assert ln == ln_naive, (ln, ln_naive)
    # ln(1+x) = x - x^2/2 + x^3/3 - ...
    assert ln[0] == 0 and ln[1] == 1
    assert ln[2] == (MOD - 1) * pow(2, MOD - 2, MOD) % MOD
    assert ln[3] == pow(3, MOD - 2, MOD) % MOD
    # exp: exp(x) = 1 + x + x^2/2 + ...
    e = poly_exp([0, 1, 0, 0, 0, 0, 0, 0], 8)
    # e = sum x^k/k!
    expected = [0] * 8
    fact = [1] * 8
    for i in range(1, 8):
        fact[i] = fact[i - 1] * i % MOD
    for k in range(8):
        expected[k] = pow(fact[k], MOD - 2, MOD)
    assert e == expected, (e, expected)
    print("newton-iteration-poly tests passed")

```

**PyPy 提示**: Python 需 NTT 卷积+每轮多次 conv, 常数大; 1e5 级逼近极限。教学版演示求逆/开方/ln/exp 小规模正确性。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n log n)(每轮 O(M(n)) 倍增) |
| 空间 | O(n) |

### 局限

初始解的存在性(开方要求 f[0] 有二次剩余, ln/exp 要求 f[0]=1/0); 每步需除法/求逆子程序, 实现链条长; 纯 Python 大规模不现实; 模数需 NTT 友好, 否则退化为 O(n²)。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P4238 | 4 | 多项式求逆: 牛顿迭代最基础应用 | [https://www.luogu.com.cn/problem/P4238](https://www.luogu.com.cn/problem/P4238) |
| Luogu | P5205 | 5 | 多项式开根: 牛顿迭代+二次剩余 | [https://www.luogu.com.cn/problem/P5205](https://www.luogu.com.cn/problem/P5205) |
| Luogu | P4726 | 5 | 多项式 exp: 基于 ln 的牛顿迭代经典题 | [https://www.luogu.com.cn/problem/P4726](https://www.luogu.com.cn/problem/P4726) |

## Pitfalls · 易错点

- 开方初始常数需是二次剩余, 否则无解直接错
- 迭代时 mod x^{m2} 截断错误(乘法结果要取前 m2 项)
- 求逆每轮 f_n 必须从 mod x^m 开始倍增, 不能重头算
- G 的偏导 G_y 忘记(公式里漏除)
- exp 迭代依赖 ln 子程序, 递归正确性依赖链

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/poly/newton/](https://oi-wiki.org/math/poly/newton/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/poly/newton.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/poly/newton.md)
