---
id: fwt
name: FWT(快速沃尔什变换)
group: G-C-12
stage: advanced
priority: P2
depth_tier: standard
---

# FWT(快速沃尔什变换)

> O(n log n)计算位运算(and/or/xor)卷积，FFT的位运算推广

<!-- 元信息: id=fwt · group=G-C-12 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

快速沃尔什变换（FWT）在 O(n log n) 内计算位运算卷积：C[k]=Σ_{i⊕j=k} A[i]·B[j]，其中 ⊕ 为按位与/或/异或（以及同或、max/min 等）。与 FFT 把时域卷积变频域乘积一样，FWT 找出一个可逆线性变换 T 使得 T(A⊕B)=T(A)·T(B)（逐点），于是 变换→逐点乘→逆变换。对 or：T 是子集和(SOS/高维前缀和)，对 and：超集和，对 xor：沃尔什变换(用 ±1 特征)。FWT 是线性变换，常用于位运算相关计数、期望 min-max 容斥、高维子集卷积、以及把 DP 的转移写成位卷积后用 FWT 加速（如 CF1103E Radix Sum）。

## Why · 为什么

### 直觉 · Intuition

位运算卷积像一种'按位求和'的乘法。对每一位独立做小变换：or 是前缀和(1 的传递)、and 是后缀和、xor 是 [1,1;1,-1] 的哈达玛变换，然后把各位变换复合(蝴蝶),复杂度 O(n log n)。

### 原理 · Principle

设 n=2^m，把数组按最高位分成两半 a0,a1。or 卷积变换：T(a)=(T(a0), T(a0)+T(a1))，其中前半不包含该位 1、后半包含。递归 m 层，总 O(n log n)。and 类似：T=(T(a0)+T(a1), T(a1))。xor 用哈达玛：T=(T(a0)+T(a1), T(a0)-T(a1))。逆变换对应层内做逆运算（or/and 交换加减，xor 再乘 1/2）。K 维 FWT 对每个二进制位做同一蝴蝶。

### 历史 · History

沃尔什变换(1923)是 FFT 的 ±1 矩阵版本；推广到位运算卷积的 FWT 在 1970s 成型，1990s 进入算法竞赛。OI Wiki 的 math/poly/fwt 页面系统整理 or/and/xor/同或/K 维/max/min 各版本，并给出 CF1103E 的进制不进位加法例题。

## How · 实现

### 伪代码

```python
# 异或卷积模板
fwt_xor(a, invert):
    for h in 1,2,4,...,n/2:
        for i in step 2h:
            for j in i..i+h-1:
                x=a[j]; y=a[j+h]
                a[j]=x+y; a[j+h]=x-y
                if invert: a[j]/=2; a[j+h]/=2
# 使用: fwt_xor(a); fwt_xor(b); c=a*b 逐点; fwt_xor(c, invert=True)
# or 版本: 正 a[j]=x+y,a[j+h]=x; 逆 a[j]=y,a[j+h]=x-y
# and 版本: 正 a[j]=y,a[j+h]=x+y; 逆 a[j]=y-x,a[j+h]=x
```

### Python 实现

```python
MOD = 998244353
INV2 = (MOD + 1) // 2


def fwt_or(a, invert=False):
    """FWT 或卷积(原地)。invert 为 True 时做逆变换(除以 n 由调用方处理)."""
    n = len(a)
    h = 1
    while h < n:
        for i in range(0, n, h * 2):
            for j in range(i, i + h):
                x = a[j]
                y = a[j + h]
                if not invert:
                    a[j] = (x + y) % MOD
                    a[j + h] = x
                else:
                    a[j] = y
                    a[j + h] = (x - y) % MOD
        h <<= 1
    return a


def fwt_and(a, invert=False):
    """FWT 与卷积(原地)。"""
    n = len(a)
    h = 1
    while h < n:
        for i in range(0, n, h * 2):
            for j in range(i, i + h):
                x = a[j]
                y = a[j + h]
                if not invert:
                    a[j] = y
                    a[j + h] = (x + y) % MOD
                else:
                    a[j] = (y - x) % MOD
                    a[j + h] = x
        h <<= 1
    return a


def fwt_xor(a, invert=False):
    """FWT 异或卷积(原地). 逆变换需再乘 n^-1。"""
    n = len(a)
    h = 1
    while h < n:
        for i in range(0, n, h * 2):
            for j in range(i, i + h):
                x = a[j]
                y = a[j + h]
                a[j] = (x + y) % MOD
                a[j + h] = (x - y) % MOD
                if invert:
                    a[j] = a[j] * INV2 % MOD
                    a[j + h] = a[j + h] * INV2 % MOD
        h <<= 1
    return a


def xor_convolution(a, b):
    n = 1
    need = max(len(a), len(b))
    while n < need:
        n <<= 1
    fa = a[:] + [0] * (n - len(a))
    fb = b[:] + [0] * (n - len(b))
    fwt_xor(fa)
    fwt_xor(fb)
    for i in range(n):
        fa[i] = fa[i] * fb[i] % MOD
    fwt_xor(fa, True)
    return fa


def or_convolution(a, b):
    n = 1
    need = max(len(a), len(b))
    while n < need:
        n <<= 1
    fa = a[:] + [0] * (n - len(a))
    fb = b[:] + [0] * (n - len(b))
    fwt_or(fa)
    fwt_or(fb)
    for i in range(n):
        fa[i] = fa[i] * fb[i] % MOD
    fwt_or(fa, True)
    return fa


def xor_naive(a, b):
    res = [0] * (max(len(a), len(b)))
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            res[i ^ j] = (res[i ^ j] + x * y) % MOD
    return res


def or_naive(a, b):
    res = [0] * (max(len(a), len(b)))
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            res[i | j] = (res[i | j] + x * y) % MOD
    return res


def and_convolution(a, b):
    n = 1
    need = max(len(a), len(b))
    while n < need:
        n <<= 1
    fa = a[:] + [0] * (n - len(a))
    fb = b[:] + [0] * (n - len(b))
    fwt_and(fa)
    fwt_and(fb)
    for i in range(n):
        fa[i] = fa[i] * fb[i] % MOD
    fwt_and(fa, True)
    return fa


def and_naive(a, b):
    res = [0] * (max(len(a), len(b)))
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            res[i & j] = (res[i & j] + x * y) % MOD
    return res


if __name__ == "__main__":
    import random
    for _ in range(200):
        n = 1 << random.randint(1, 4)
        a = [random.randint(0, 20) for _ in range(n)]
        b = [random.randint(0, 20) for _ in range(n)]
        assert xor_convolution(a, b) == xor_naive(a, b), ("xor", a, b)
        assert or_convolution(a, b) == or_naive(a, b), ("or", a, b)
        assert and_convolution(a, b) == and_naive(a, b), ("and", a, b)
    # 手工样例: (1+x^1)(1+x^1) 的异或卷积
    assert xor_convolution([1, 1], [1, 1]) == [2, 2]
    print("FWT (and/or/xor) tests passed")

```

**PyPy 提示**: FWT 无乘法、纯加减, Python 实现比 FFT/NTT 快得多, 1e6 级可过。逐层蝴蝶内层用局部变量缓存数组引用可再提速。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n log n) |
| 空间 | O(n) |

### 局限

数组长度必须是 2 的幂。非 2 的幂需补零。xor 逆变换除以 2 在模数需用 2 的逆元。子集卷积(要求不交并)不能直接 FWT, 需按 popcount 分层的 FWT(fast zeta transform + 附加维)。对非标准运算(如 K 进制不进位加法)需定制变换矩阵。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P6097 | 4 | 子集卷积模板题: 需要按 popcount 分层的 FWT | [https://www.luogu.com.cn/problem/P6097](https://www.luogu.com.cn/problem/P6097) |
| Codeforces | 1103E | 6 | Radix Sum: 10 进制不进位加法的 K 维 FWT 高级应用 | [https://www.luogu.com.cn/problem/CF1103E](https://www.luogu.com.cn/problem/CF1103E) |
| AtCoder | abc331_g | 5 | Collect Them All: FWT+容斥/期望的经典组合 | [https://atcoder.jp/contests/abc331/tasks/abc331_g](https://atcoder.jp/contests/abc331/tasks/abc331_g) |

## Pitfalls · 易错点

- and/or/xor 三版的蝴蝶公式互相记混
- xor 逆变换忘记乘 2 的逆元(模意义下)
- 子集卷积直接套 FWT(结果混入重叠集合)
- 长度不是 2 的幂没补零
- 把 FWT 当 FFT 用在多项式卷积上(运算类型不同)

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/poly/fwt/](https://oi-wiki.org/math/poly/fwt/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/poly/fwt.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/poly/fwt.md)
