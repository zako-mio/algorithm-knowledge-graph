---
id: ntt
name: NTT(数论变换)
group: G-C-12
stage: advanced
priority: P1
depth_tier: standard
---

# NTT(数论变换)

> 模意义下FFT，用原根替代单位根避免浮点误差，998244353为常用模数

<!-- 元信息: id=ntt · group=G-C-12 · stage=advanced · priority=P1 · depth_tier=standard -->

## What · 是什么

数论变换（NTT）是 FFT 在模素数 p 意义下的版本：用模 p 下的本原单位根（原根 g 的幂）替代复数单位根，加减乘全部在整数取模下进行，彻底避免浮点误差。要求 p-1 能被 2^k 整除，常用模数 998244353=119·2^23+1（原根 3），支持长度到 2^23。实现与 FFT 完全同构：位逆序置换+蝶形，只是旋转因子 w_h=g^{(p-1)/h}，逆变换用逆根再乘 n 的逆元。因为结果精确，可处理系数取模的题目、任意模数 NTT(拆系数/多模合并)、以及作为所有多项式算法(逆元/ln/exp/多点求值等)的底层卷积引擎。

## Why · 为什么

### 直觉 · Intuition

复数单位根满足 ω^n=1、ω^{n/2}=-1 等性质，NTT 只是找一个'模 p 下同样满足这些性质'的数——原根的幂。整型运算没有浮点误差，还能直接吃取模系数，完美替代复数 FFT。

### 原理 · Principle

对素数 p=qn+1(n=2^m)，原根 g 满足 g^{p-1}≡1。令 g_n=g^q≡g^{(p-1)/n} 扮演 ω_n，则 g_n^n≡1、g_n^{n/2}≡-1，且迭代到长度 l 时旋转因子为 g^{(p-1)/l}。DFT 公式 X_k=Σ a_j g_n^{jk}。正变换根 g^{(p-1)/h}，逆变换取逆元并整体乘 n^{-1}。NTT 与 FFT 的分治结构完全一致。

### 历史 · History

NTT 源自 1970 年代 Pollard 与 Rader 等人对 DFT 在有限域/数环上的推广。OI/ACM 自 2010s 起成为标准工具，998244353 因 2^23 因子与简洁原根成为首选。OI Wiki 的 poly/ntt 页面列出多个 NTT 友好模数（167772161、469762049、998244353、1004535809 等）。

## How · 实现

### 伪代码

```python
# 迭代 NTT, mod p, 原根 g, n=2^k | p-1
bit_reverse_permute(a)
for h in 2,4,8,...,n:
    w_h = g^((p-1)/h)          # 正变换; 逆变换用逆元
    for i in step h:
        w = 1
        for j in i..i+h/2-1:
            u=a[j]; v=a[j+h/2]*w % p
            a[j]=(u+v)%p; a[j+h/2]=(u-v)%p
            w = w*w_h % p
if invert: 整体乘 n^{-1} mod p
```

### Python 实现

```python
MOD = 998244353
ROOT = 3  # 998244353 = 7*17*2^23 + 1 的原根


def mod_pow(a, b, mod=MOD):
    r = 1
    while b:
        if b & 1:
            r = r * a % mod
        a = a * a % mod
        b >>= 1
    return r


def ntt(a, invert=False):
    """NTT(原根实现, 蝴蝶操作)。a: list[int] mod MOD, 长度须为 2 的幂。"""
    n = len(a)
    a = a[:]
    # 位逆序置换
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
        # w_h = g^((MOD-1)/h) 或逆元
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


def poly_mul_ntt(a, b, mod=MOD):
    n = 1
    need = len(a) + len(b) - 1
    while n < need:
        n <<= 1
    fa = a[:] + [0] * (n - len(a))
    fb = b[:] + [0] * (n - len(b))
    fa = ntt(fa)
    fb = ntt(fb)
    for i in range(n):
        fa[i] = fa[i] * fb[i] % mod
    fa = ntt(fa, True)
    return fa[:need]


def poly_mul_naive(a, b, mod=MOD):
    res = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            res[i + j] = (res[i + j] + x * y) % mod
    return res[:len(a) + len(b) - 1]


if __name__ == "__main__":
    import random
    # 与朴素卷积对拍
    for _ in range(50):
        la = random.randint(1, 10)
        lb = random.randint(1, 10)
        a = [random.randint(0, MOD - 1) for _ in range(la)]
        b = [random.randint(0, MOD - 1) for _ in range(lb)]
        assert poly_mul_ntt(a, b) == poly_mul_naive(a, b), (a, b)
    # OI-wiki 引入样例
    assert poly_mul_ntt([7, 3, 5], [1, 2, 7]) == [7, 17, 60, 31, 35]
    # 单位根性质: g_n^(n/2) = -1
    g4 = mod_pow(ROOT, (MOD - 1) // 4)
    assert g4 * g4 % MOD == MOD - 1
    print("NTT tests passed")

```

**PyPy 提示**: Python NTT 每层蝶形含取模, 1e5 级长度在 PyPy 下勉强/可能 TLE; 优化: 内层用局部变量+延迟取模, 或改用 numpy 向量化。教学正确实现可处理 1e4~1e5 规模。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n log n) |
| 空间 | O(n) |

### 局限

要求模数 p 为 NTT 友好素数(2^k | p-1)且长度 <=2^k; 任意模数(如 1e9+7)需拆系数(每个系数拆高 15 位+低 15 位做 3 次 NTT)或多模 NTT+CRT, 常数大。Python 纯实现性能受限, N=1e5 可能 TLE, 需优化或换语言。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Library Checker | convolution_mod | 3 | 模板题: 模意义卷积, 判 NTT 正确性的权威平台 | [https://judge.yosupo.jp/problem/convolution_mod](https://judge.yosupo.jp/problem/convolution_mod) |
| Luogu | P3803 | 3 | 多项式乘法模板题(NTT 版) | [https://www.luogu.com.cn/problem/P3803](https://www.luogu.com.cn/problem/P3803) |
| Luogu | P4238 | 4 | 多项式求逆: 牛顿迭代+卷积, NTT 的典型应用 | [https://www.luogu.com.cn/problem/P4238](https://www.luogu.com.cn/problem/P4238) |

## Pitfalls · 易错点

- 模数不是 NTT 友好素数(2^k∤p-1)时直接套用会错
- 长度超过模数支持的 2^k 上界(如 998244353 只支持 2^23)
- 逆变换忘记乘 n 的逆元
- 旋转因子方向与 FFT 混淆(正变换与逆变换用反)
- 任意模数题目忘记拆系数/CRT, 用普通 NTT 出错误答案

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/poly/ntt/](https://oi-wiki.org/math/poly/ntt/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/poly/ntt.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/poly/ntt.md)
- CP-Algorithms ✓ [https://cp-algorithms.com/algebra/fft.html](https://cp-algorithms.com/algebra/fft.html)
