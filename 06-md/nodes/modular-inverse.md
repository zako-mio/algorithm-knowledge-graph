---
id: modular-inverse
name: 模逆元
group: G-C-7
stage: intermediate
priority: P0
depth_tier: deep
---

# 模逆元

> 求a在模m下的逆元，方法：扩展欧几里得/费马小定理/线性递推

<!-- 元信息: id=modular-inverse · group=G-C-7 · stage=intermediate · priority=P0 · depth_tier=deep -->

## What · 是什么

模逆元（Modular Multiplicative Inverse）：对 a 与模数 m 互素，存在唯一的 b 使 a·b ≡ 1 (mod m)，记 b = a^(-1) mod m。它是模意义下除法的实现方式：a/b ≡ a·b^(-1) (mod m)。求单个逆元用扩展欧几里得（通用）或费马小定理（m 为质数）；求多个/前 n 个逆元可用前缀积法 O(n+log m) 或线性递推 O(n)。

## Why · 为什么

### 直觉 · Intuition

普通实数中除 b 等于乘 1/b。模世界里「1/b」就是满足 b·x≡1 的 x——一个数乘上它等于乘了单位元 1。费马小定理说质数 p 下 a^(p-1)≡1，于是 a·a^(p-2)≡1，逆元就是 a^(p-2)。扩展欧几里得则是直接把方程 ax+my=1 解出来。

### 原理 · Principle

(1) 扩展欧几里得：解 ax+my=gcd(a,m)=1，得 x 即逆元，O(log m)，最通用；(2) 费马小定理：p 为质数且 a%p≠0 时 a^(-1)≡a^(p-2)，O(log p)；(3) 线性递推：inv[1]=1，inv[i]=-(m//i)·inv[m%i] mod m（m 为质数），O(n) 预处理前 n 个；(4) 前缀积法：对所有 a_i 一次 exgcd 求总积的逆元再反向回推，O(n+log m)，适合任意 m 且 gcd 条件满足时。

### 历史 · History

逆元概念与同余理论同源（高斯《算术研究》），费马小定理由 Pierre de Fermat 于 17 世纪提出，欧拉推广为欧拉定理。模逆元是 RSA 公钥密码体制的核心运算（求 e 的逆元 d），也是竞赛中组合数取模（Lucas）、多项式求逆等高级工具的地基。OI Wiki 与 CP-Algorithms 均专题讲解。

## How · 实现

### 伪代码

```python
# 方法1: exgcd
inv(a, m): (g, x, y) = exgcd(a, m); 断言 g==1; return x % m

# 方法2: 费马小定理（m 为质数）
inv(a, p) = pow(a, p-2, p)

# 方法3: 线性递推前 n 个逆元（m 为质数）
inv[1] = 1
for i in 2..n: inv[i] = (m - m//i) * inv[m%i] % m

# 方法4: 前缀积法 O(n+log m)
pref[0]=1; for i: pref[i]=pref[i-1]*a[i] % m
inv_pref[n] = exgcd(pref[n], m).x
for i=n..1: inv_a[i]=inv_pref[i]*pref[i-1] % m; inv_pref[i-1]=inv_pref[i]*a[i] % m
```

### Python 实现

```python
def exgcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = exgcd(b, a % b)
    return g, y, x - (a // b) * y


def inv_exgcd(a, m):
    """扩展欧几里得求逆元（任意模数，需互素）"""
    g, x, _ = exgcd(a, m)
    if g != 1:
        return None
    return x % m


def inv_fermat(a, p):
    """费马小定理求逆元（p 为质数）"""
    return pow(a, p - 2, p)


def invs_linear(n, p):
    """O(n) 求 1..n 在模 p（质数）下的逆元"""
    inv = [0] * (n + 1)
    inv[1] = 1
    for i in range(2, n + 1):
        inv[i] = (p - p // i) * inv[p % i] % p
    return inv


def invs_prefix(arr, m):
    """前缀积法求数组 arr 中每个数的逆元（要求每个元素与 m 互素）"""
    n = len(arr)
    pref = [1] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] * arr[i] % m
    g, inv_all, _ = exgcd(pref[n], m)
    if g != 1:
        raise ValueError("some element not coprime with m")
    inv_all %= m
    inv_arr = [0] * n
    for i in range(n - 1, -1, -1):
        inv_arr[i] = inv_all * pref[i] % m
        inv_all = inv_all * arr[i] % m
    return inv_arr


if __name__ == "__main__":
    p = 10**9 + 7
    assert inv_exgcd(3, 7) == 5
    assert inv_exgcd(3, 7) == inv_fermat(3, 7) == 5
    assert inv_exgcd(2, 4) is None  # gcd(2,4)=2≠1
    assert (inv_fermat(5, p) * 5) % p == 1

    n = 20
    inv = invs_linear(n, p)
    for i in range(1, n + 1):
        assert (i * inv[i]) % p == 1

    import random
    random.seed(1)
    arr = [random.randint(1, 10**9) for _ in range(10)]
    inv_arr = invs_prefix(arr, p)
    for a, b in zip(arr, inv_arr):
        assert (a * b) % p == 1

    # 与 pow(a, -1, m) 交叉验证（Python 3.8+）
    for m in [7, 11, 1009, 10007]:
        for a in range(1, m):
            if __import__('math').gcd(a, m) == 1:
                assert inv_exgcd(a, m) == pow(a, -1, m), (a, m)
    # 大质数抽查
    assert inv_exgcd(5, 1000000007) == pow(5, -1, 1000000007)

    print("All tests passed.")
```

**PyPy 提示**: 竞赛中直接用 pow(a, -1, m)（Python 3.8+ 内置，C 实现，内部 exgcd 扩展版）最快；求逆元数组用 invs_linear 的 O(n) 递推（PyPy 下 n=1e7 约 1s）。费马小定理 pow(a,p-2,p) 也快。注意 pow(a,-1,m) 在 a,m 不互素时会抛 ValueError。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 单个逆元 O(log m)；线性递推/前缀积 O(n) 或 O(n+log m) |
| 空间 | 单个 O(1)；批量 O(n) |

### 局限

逆元存在当且仅当 gcd(a,m)=1。线性递推法仅适用于质数模数；前缀积法要求每个元素均与 m 互素。对非质数合数模的多个逆元需逐个 exgcd 或使用 CRT。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3811 | 4 | 【模板】乘法逆元：三种求法均可，线性递推模板题 | [https://www.luogu.com.cn/problem/P3811](https://www.luogu.com.cn/problem/P3811) |
| Luogu | P1082 | 4 | 【模板】同余方程 ax≡1(mod b)：exgcd 求逆元 | [https://www.luogu.com.cn/problem/P1082](https://www.luogu.com.cn/problem/P1082) |
| LOJ | 110 | 4 | 乘法逆元：线性递推预处理 1..n 逆元 | [https://loj.ac/problem/110](https://loj.ac/problem/110) |

## Pitfalls · 易错点

- 忘记判断 gcd(a,m)==1，对不存在逆元的 a 强算导致结果错误
- 费马小定理误用于合数模数
- 线性递推 inv[i]=(m-m//i)*inv[m%i]%m 的下标越界（m%i 可能大于 i？不会，但需要 p%i 已算好，故 i<p）
- 前缀积法反向回推时逆元累乘方向写反
- 把 pow(a,-1,m) 写成 pow(a,m-2,m) 用于非质数模数

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/number-theory/inverse/](https://oi-wiki.org/math/number-theory/inverse/)
- CP-Algorithms ✓ [https://cp-algorithms.com/algebra/module-inverse.html](https://cp-algorithms.com/algebra/module-inverse.html)
- 书籍 ✓ `CPH ch21 Number theory (p207-216)`
