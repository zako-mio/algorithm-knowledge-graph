---
id: polynomial-basics
name: 多项式基础
group: G-C-12
stage: advanced
priority: P1
depth_tier: standard
---

# 多项式基础

> 多项式表示、求值、乘法、求导积分，FFT/NTT的前置知识

<!-- 元信息: id=polynomial-basics · group=G-C-12 · stage=advanced · priority=P1 · depth_tier=standard -->

## What · 是什么

多项式基础是形式幂级数理论及所有多项式算法（FFT/NTT、求逆、ln/exp、开方、多点求值、拉格朗日反演等）的地基。核心概念：多项式环 R[x] 与形式幂级数环 R[[x]]（系数序列视角）；次数 deg f；乘法（系数卷积，FFT/NTT 加速到 O(n log n)）；复合 f∘g；形式导数与不定积分（逐项求导/积分）；乘法逆元（常数项非零存在，牛顿迭代 O(n log n)）；带余除法与模多项式（q、r 的唯一性）；常见的幂级数展开式（e^x、ln(1+x)、(1+x)^a、三角/反三角）；生成函数。

## Why · 为什么

### 直觉 · Intuition

把多项式想成'系数序列'，x 只是占位符。这样 导数=乘下标、积分=除下标、逆元=解递推、卷积=乘积——所有操作都变成序列上的运算，可以用 NTT 加速，最后就能'操纵'生成函数解计数题。

### 原理 · Principle

形式导数 f'=Σ k·a_k x^{k-1} 无需极限即可定义；形式积分是导数的逆(任取常数项)。乘法逆元满足 (f·f^{-1})_0=1 的递推 f^{-1}_n=-f_0^{-1}Σ_{k<n} f^{-1}_k f_{n-k}，朴素 O(n^2)，牛顿迭代 O(n log n)。带余除法 f=qg+r 中 q、r 唯一(deg r<deg g)，可 O(n^2) 也可用逆元+反转 O(n log n)。复合逆存在当且仅当 f(0)=0 且 f'(0)≠0。

### 历史 · History

形式幂级数方法源自 18-19 世纪的分析/生成函数传统(Euler、Laplace)，20 世纪组合学中发展成 powerful 工具（Stanley 的 Enumerative Combinatorics 是标准文献）。OI 中 2010s 起以 FFT/NTT 为引擎普及全套多项式操作，OI Wiki 的 poly/intro 页面是中文社区的标准入门。

## How · 实现

### 伪代码

```python
# 核心操作一览
乘:    c = conv(a,b)                 # 卷积, NTT O(n log n)
导数:  df[i-1] = i*a[i]
积分:  it[i] = a[i-1]/i (i>=1)
逆元:  inv(f, n) 牛顿迭代 O(n log n)
带余除: q = rev(rev(f) * inv(rev(g)) mod x^{n-m+1}); r = f - q*g
求值:  Horner O(n) 单点
```

### Python 实现

```python
MOD = 998244353


def poly_mul(a, b, mod=MOD):
    """朴素多项式乘法(教学版)。O(nm)。"""
    res = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x == 0:
            continue
        for j, y in enumerate(b):
            res[i + j] = (res[i + j] + x * y) % mod
    return res


def poly_add(a, b, mod=MOD):
    n = max(len(a), len(b))
    res = [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)]
    return [x % mod for x in res]


def poly_sub(a, b, mod=MOD):
    n = max(len(a), len(b))
    res = [((a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)) % mod for i in range(n)]
    return res


def poly_derivative(a, mod=MOD):
    """形式导数 f'(x)。"""
    return [(i * a[i]) % mod for i in range(1, len(a))]


def poly_integral(a, mod=MOD):
    """形式不定积分(取 0 常数项). 需要模逆元预计算。"""
    n = len(a) + 1
    inv = [0] * n
    inv[1] = 1
    for i in range(2, n):
        inv[i] = (mod - mod // i) * inv[mod % i] % mod
    return [0] + [a[i - 1] * inv[i] % mod for i in range(1, n)]


def poly_evaluate(a, x, mod=MOD):
    """Horner 求值。"""
    r = 0
    for c in reversed(a):
        r = (r * x + c) % mod
    return r


def poly_naive_inverse(a, n, mod=MOD):
    """多项式逆元 O(n^2)(教学版): f0 != 0 时存在。a 可不足 n 项(高位视为 0)。"""
    aa = a[:] + [0] * (n - len(a))
    inv0 = pow(aa[0], mod - 2, mod)
    res = [inv0]
    for i in range(1, n):
        s = 0
        for k in range(i):
            s = (s + res[k] * aa[i - k]) % mod
        res.append((-inv0 * s) % mod)
    return res


def poly_naive_division(f, g, mod=MOD):
    """带余除法 f = q*g + r (系数从低到高), deg(g)<=deg(f)。O(n^2)。"""
    f = f[:]
    g = g[:]
    n, m = len(f), len(g)
    if n < m:
        return [], f[:]
    inv_lead = pow(g[-1], mod - 2, mod)
    q = [0] * (n - m + 1)
    for i in range(n - 1, m - 2, -1):
        coef = f[i] * inv_lead % mod
        pos = i - m + 1
        q[pos] = coef
        for j in range(m):
            f[pos + j] = (f[pos + j] - coef * g[j]) % mod
    return q, f[:m - 1]


def poly_compose_naive(f, g, n, mod=MOD):
    """多项式复合 f(g(x)) 前 n 项, O(n^2)。"""
    res = [0] * n
    cur = [1]
    for c in f:
        if c:
            for i in range(len(cur)):
                if i < n:
                    res[i] = (res[i] + c * cur[i]) % mod
        # cur = cur * g
        new = [0] * min(n, len(cur) + len(g) - 1)
        for i in range(len(cur)):
            if cur[i] == 0:
                continue
            for j in range(len(g)):
                if i + j < n:
                    new[i + j] = (new[i + j] + cur[i] * g[j]) % mod
        cur = new
    return res


if __name__ == "__main__":
    import random
    for _ in range(100):
        n = random.randint(1, 8)
        m = random.randint(1, 8)
        f = [random.randint(0, 9) for _ in range(n)]
        g = [random.randint(0, 9) for _ in range(m)]
        # 乘法: (f*g) 系数
        prod = poly_mul(f, g)
        prod2 = [0] * (n + m - 1)
        for i, x in enumerate(f):
            for j, y in enumerate(g):
                prod2[i + j] = (prod2[i + j] + x * y) % MOD
        assert prod == prod2
        # 带余除法回代: f = q*g + r
        if len(f) >= len(g) and g[-1] % MOD != 0:
            q, r = poly_naive_division(f, g)
            back = poly_add(poly_mul(q, g), r + [0] * (len(f) - len(r)))
            assert back[:len(f)] == f
    # 多项式逆元: (1 - x)^{-1} = 1 + x + x^2 + ...
    inv = poly_naive_inverse([1, MOD - 1], 6)
    assert inv == [1, 1, 1, 1, 1, 1], inv
    # 导数与积分
    f = [1, 2, 3, 4]
    df = poly_derivative(f)
    assert df == [2, 6, 12]
    it = poly_integral([2, 6, 12])  # 积分(常数项取 0)
    assert it == [0, 2, 3, 4]
    # 导积分还原(去常数项)
    assert poly_derivative(it) == [2, 6, 12]
    print("polynomial-basics tests passed")

```

**PyPy 提示**: 朴素 O(n^2) 实现教学足够(1e4 级); 生产用 NTT 版乘法+牛顿迭代。Python 大 n 依赖 NTT 常数优化。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 朴素: 乘/逆 O(n^2); NTT 版: 乘 O(n log n), 逆 O(n log n) |
| 空间 | O(n) |

### 局限

逆元要求常数项非零(否则不存在); 导数求导次数到 0 次项消失; 幂级数展开只在收敛域内成立(形式幂级数层面不需收敛, 但换元复合需常数项为 0); 形式积分需模逆元预计算。教学朴素版大 n 慢, 实际使用要换 NTT 实现。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3803 | 3 | 多项式乘法: 检验基础卷积与 FFT/NTT 实现 | [https://www.luogu.com.cn/problem/P3803](https://www.luogu.com.cn/problem/P3803) |
| Library Checker | inv_of_formal_power_series | 4 | 形式幂级数求逆: 牛顿迭代入门 | [https://judge.yosupo.jp/problem/inv_of_formal_power_series](https://judge.yosupo.jp/problem/inv_of_formal_power_series) |
| AtCoder | abc331_g | 5 | 生成函数思想用于计数问题(容斥+FWT) | [https://atcoder.jp/contests/abc331/tasks/abc331_g](https://atcoder.jp/contests/abc331/tasks/abc331_g) |

## Pitfalls · 易错点

- 逆元存在性条件(常数项非零)忽略
- 卷积长度/补零错误导致结果截断
- 形式导数的常数项消失, 积分后再求导常数丢失
- 复合运算要求内层常数项为 0(否则项数无穷)
- 幂级数展开盲目代入非收敛域(数值问题)

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/poly/intro/](https://oi-wiki.org/math/poly/intro/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/poly/intro.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/poly/intro.md)
- CP-Algorithms ✓ [https://cp-algorithms.com/algebra/polynomial.html](https://cp-algorithms.com/algebra/polynomial.html)
