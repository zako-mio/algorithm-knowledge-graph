---
id: dirichlet-convolution
name: 狄利克雷卷积
group: G-C-9
stage: advanced
priority: P2
depth_tier: standard
---

# 狄利克雷卷积

> 数论函数的卷积运算，莫比乌斯反演与杜教筛的理论框架

<!-- 元信息: id=dirichlet-convolution · group=G-C-9 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

数论函数 f,g 的 Dirichlet 卷积定义为 (f*g)(n)=Σ_{d|n} f(d)g(n/d)，对 n 的所有正因子求和。它在数论函数全体上构成交换环（Dirichlet 环），单位元为 ε(n)=[n=1]（Iverson 括号）。关键恒等式：ε=μ*1（莫比乌斯反演之基）、τ=1*1（因子数）、σ=id*1（因子和）、φ=id*μ（欧拉函数）、id=φ*1。积性函数对卷积封闭；完全积性函数 f 的卷积逆为 μf。应用：莫比乌斯反演、杜教筛、狄利克雷前缀和/差分、积性函数求和，是数论算法（尤其是 O(n^{2/3}) 级数论求和）的理论核心。

## Why · 为什么

### 直觉 · Intuition

把『对因子求和』抽象成代数运算：f*g 表示『f 作用在因子上、g 作用在商上，再全加起来』。若 f 是积性函数，卷积保持积性，于是只要算素因子幂次上的值即可还原全体。ε=μ*1 意味着『μ 是常数函数 1 的逆元』——莫比乌斯反演就是数论函数的『乘法逆元』运算：g=f*1 可解出 f=g*μ。杜教筛则利用卷积把难求的函数 h 写成 h=f*g，用 g 的『好』前缀和递推 h 的前缀和。

### 原理 · Principle

① 定义 (f*g)(n)=Σ_{d|n}f(d)g(n/d)，交换律/结合律/分配律成立，ε 为单位元。② ε=μ*1：由 μ(d)=(-1)^k(无平方因子) 的定义与二项式求和可得 Σ_{d|n}μ(d)=[n=1]。③ 常见恒等式：τ=1*1, σ=id*1, φ=id*μ, id=φ*1。④ 逆元递推：g(1)=1/f(1), g(n)=(-1/f(1))Σ_{d|n,d>1}f(d)g(n/d)。⑤ 计算：一般情形直接 O(n log n)（调和级数）枚举；g 为积性/完全积性时用欧拉乘积加速至 O(n log log n)；结果积性时用素因子分解逐素数算。⑥ Dirichlet 生成函数 D_f(s)=Σf(n)/n^s，卷积对应生成函数乘积（形式级数层面）。

### 历史 · History

Dirichlet 卷积由德国数学家 P.G.L. Dirichlet（1805-1859）在解析数论中引入，与 Dirichlet 级数、L 函数相关；名称『Dirichlet』纪念其开创的『除数问题』与算术函数研究。莫比乌斯反演（August Ferdinand Möbius）是它的直接应用。在现代算法竞赛中，杜教筛（2015 前后由杜瑜皓推广）把卷积前缀和技巧带火，成为 OI 数论压轴考点。

## How · 实现

### 伪代码

```python
# 暴力卷积 O(n log n)
def dirichlet_conv(f, g, n):
  h = [0]*(n+1)
  for d in range(1, n+1):
    for k in range(1, n//d + 1):
      h[d*k] += f[d] * g[k]
  return h

# 莫比乌斯反演: g = f*1  =>  f = g*μ
# 杜教筛: S(n) = Σ_{i<=n} h(i), h = f*g, 选好 g 使前缀和可求
```

### Python 实现

```python
def conv_naive(f, g, n):
    """Dirichlet 卷积 (f*g)(1..n). f,g 为长度 n+1 的列表(索引从1开始)."""
    h = [0] * (n + 1)
    for d in range(1, n + 1):
        fd = f[d]
        if fd == 0:
            continue
        for k in range(1, n // d + 1):
            h[d * k] += fd * g[k]
    return h


def mobius(n):
    """莫比乌斯函数表 mu[1..n] (线性筛)."""
    mu = [0] * (n + 1)
    mu[1] = 1
    primes = []
    is_comp = [False] * (n + 1)
    for i in range(2, n + 1):
        if not is_comp[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > n:
                break
            is_comp[i * p] = True
            if i % p == 0:
                mu[i * p] = 0
                break
            mu[i * p] = -mu[i]
    return mu


def conv_with_mu(f, n):
    """f*mu: 莫比乌斯反演的一步."""
    return conv_naive(f, mobius(n), n)


def conv_with_one(f, n):
    """f*1: 前缀和型卷积 (Dirichlet 前缀和)."""
    h = f[:]
    primes = [i for i in range(2, n + 1) if mobius(i) != 0 or i == 2]
    # 用线性筛质数
    comp = [False] * (n + 1)
    pr = []
    for i in range(2, n + 1):
        if not comp[i]:
            pr.append(i)
        for p in pr:
            if i * p > n:
                break
            comp[i * p] = True
            if i % p == 0:
                break
    for p in pr:
        for k in range(1, n // p + 1):
            h[k * p] += h[k]
    return h


def divisor_count_from_conv(n):
    """用 tau=1*1 验证: tau(k)=因子个数."""
    one = [0] + [1] * n
    tau = conv_naive(one, one, n)
    return tau


if __name__ == "__main__":
    N = 30
    # tau = 1*1
    one = [0] + [1] * N
    tau = conv_naive(one, one, N)
    for k in range(1, N + 1):
        cnt = sum(1 for d in range(1, k + 1) if k % d == 0)
        assert tau[k] == cnt, k

    # epsilon = mu*1
    mu = mobius(N)
    eps = conv_naive(mu, one, N)
    for k in range(1, N + 1):
        assert eps[k] == (1 if k == 1 else 0), k

    # sigma = id*1
    ids = [0] + list(range(1, N + 1))
    sig = conv_naive(ids, one, N)
    for k in range(1, N + 1):
        s = sum(d for d in range(1, k + 1) if k % d == 0)
        assert sig[k] == s, k

    # phi = id*mu
    phi = conv_naive(ids, mu, N)
    for k in range(1, N + 1):
        assert phi[k] == sum(1 for i in range(1, k + 1) if __import__('math').gcd(i, k) == 1), k

    # id = phi*1 (反向验证)
    id_back = conv_naive(phi, one, N)
    for k in range(1, N + 1):
        assert id_back[k] == k

    # 结合律: (1*1)*mu == 1*(1*mu) == 1*eps == 1
    t1 = conv_naive(conv_naive(one, one, N), mu, N)
    for k in range(1, N + 1):
        assert t1[k] == one[k]
    print("All tests passed.")
```

**PyPy 提示**: conv_naive 的 O(n log n) 在 n≤1e6 可跑；n 更大用欧拉乘积优化或 Dirichlet 前缀和（内层对质数枚举）。杜教筛对 n 做 sqrt 分块+记忆化，PyPy 下注意递归/记忆化字典的开销。线性筛 μ 是 O(n) 标准做法。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 暴力卷积 O(n log n)；积性函数优化 O(n log log n)；杜教筛 O(n^{2/3})（取阈值） |
| 空间 | O(n) |

### 局限

暴力卷积对大 n（>1e6）太慢。杜教筛需要构造合适的 g 使 f*g 与 g 的前缀和都易求，构造不出时退化为分块枚举。卷积中数论函数需存储成数组，n 超过内存时要用杜教筛的按需记忆化。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P4213 | 6 | 【模板】杜教筛：φ 和 μ 的前缀和，Dirichlet 卷积核心应用 | [https://www.luogu.com.cn/problem/P4213](https://www.luogu.com.cn/problem/P4213) |
| Luogu | P3768 | 7 | 简单的数学题：杜教筛+卷积构造 g 的经典综合题（OI Wiki 例题） | [https://www.luogu.com.cn/problem/P3768](https://www.luogu.com.cn/problem/P3768) |
| Luogu | P3327 | 6 | d(i*j)：莫比乌斯反演+卷积恒等式 τ 的化简（数论分块综合） | [https://www.luogu.com.cn/problem/P3327](https://www.luogu.com.cn/problem/P3327) |

## Pitfalls · 易错点

- 卷积求和范围是 d\|n，不是 d≤n 全枚举（暴力时要按倍数累加）
- 积性函数卷积仍积性，但完全积性卷积不保证完全积性
- ε(n)=[n=1]，单位元别和常数函数 1 混淆
- 莫比乌斯反演符号方向：g=f*1 ⇔ f=g*μ（μ 是 1 的逆）
- 线性筛 μ 时 i%p==0 要置 mu[i*p]=0 并 break，否则数组错位
- 杜教筛选择 g 时若 f*g 不是易求的常见函数会卡死

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/number-theory/dirichlet/](https://oi-wiki.org/math/number-theory/dirichlet/)
- OI Wiki ✓ [https://oi-wiki.org/math/number-theory/mobius/](https://oi-wiki.org/math/number-theory/mobius/)
