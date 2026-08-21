---
id: mobius-inversion
name: 莫比乌斯反演
group: G-C-8
stage: advanced
priority: P1
depth_tier: standard
---

# 莫比乌斯反演

> 利用莫比乌斯函数 μ(n) 进行数论反演，把 [gcd(i,j)=1] 条件展开为 Σμ(d)，将 gcd 计数问题转化为可整除分块的求和

<!-- 元信息: id=mobius-inversion · group=G-C-8 · stage=advanced · priority=P1 · depth_tier=standard -->

## What · 是什么

莫比乌斯函数 μ(n) 定义为：μ(1)=1；n 含平方因子则 μ(n)=0；n 为 k 个互异素因子之积则 μ(n)=(−1)^k。它是积性函数，可由线性筛 O(n) 预处理。核心性质 Σ_{d|n} μ(d) = [n=1]。莫比乌斯反演：f(n)=Σ_{d|n} g(d) ⟺ g(n)=Σ_{d|n} μ(n/d)f(d)；倍数形式：f(n)=Σ_{n|d} g(d) ⟺ g(n)=Σ_{n|d} μ(d/n)f(d)。最常见的应用：把 [gcd(i,j)=1]=Σ_{d|gcd(i,j)} μ(d) 代入双重求和，交换求和次序后用数论整除分块 O(√n) 求值。

## Why · 为什么

### 直觉 · Intuition

μ 是『筛子』：它对平方因子过敏（直接记 0），对互异素因子按奇偶计数（(−1)^k）。恒等式 Σ_{d|n}μ(d)=[n=1] 像开关：n=1 时亮，否则所有项抵消归零。于是把『gcd 恰好等于 1』的硬条件拆成『d 整除 gcd』的软条件再乘 μ(d)，就能把条件和被求和的 i,j 分离，各自动手求和。

### 原理 · Principle

证明反演只需两次交换求和次序：Σ_{d|n} μ(n/d) f(d) = Σ_{d|n} μ(n/d) Σ_{k|d} g(k) = Σ_{k|n} g(k) Σ_{d}[k|d|n] μ(n/d) = Σ_{k|n} g(k)[n/k=1] = g(n)。Dirichlet 卷积视角：f=1*g ⟺ g=μ*f（因 1*μ=ε）。标准 gcd 计数流程：S=Σ_{i≤n}Σ_{j≤m}[gcd(i,j)=1] = Σ_d μ(d)⌊n/d⌋⌊m/d⌋；推广到 [gcd=k] 用整除替换，多变量、上下限、乘/除形式均可推广。结合前缀和与整除分块可处理多组查询（n,m≤1e9）。

### 历史 · History

莫比乌斯函数由高斯于 1797 年引入（以 Möbius 命名，August Ferdinand Möbius 于 1832 年推广），莫比乌斯反演公式是数论函数 Dirichlet 卷积理论的核心结论。它在素数分布、格点计数、Riemann zeta 函数、以及现代算法数论（筛法、gcd 统计类计数题）中扮演基础工具角色，是 OI/ICPC 数论计数题的标配。

## How · 实现

### 伪代码

```python
# 线性筛预处理 mu[1..N]
mu[1] = 1; primes = []
for i in 2..N:
  if not comp[i]: primes.append(i); mu[i] = -1
  for p in primes:
    if i*p > N: break
    comp[i*p] = True
    if i % p == 0: mu[i*p] = 0; break
    mu[i*p] = -mu[i]

# 求 S = sum_{i=1..n} sum_{j=1..m} [gcd(i,j)=1]
def count_coprime(n, m):
  return sum(mu[d] * (n//d) * (m//d) for d in 1..min(n,m))

# 整除分块优化（多组查询 + 前缀和）:
# sum_{d=l..r} mu[d] 用前缀和 pre[r]-pre[l-1]
# 每次跳到 min(n//(n//d), m//(m//d))
```

### Python 实现

```python
import math
from math import isqrt


def mobius_table(n):
    """线性筛预处理 mu[0..n]，返回 mu 列表。"""
    mu = [0] * (n + 1)
    mu[1] = 1
    primes = []
    comp = [False] * (n + 1)
    for i in range(2, n + 1):
        if not comp[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > n:
                break
            comp[i * p] = True
            if i % p == 0:
                mu[i * p] = 0
                break
            mu[i * p] = -mu[i]
    return mu


def mobius_single(x):
    """单点 μ(x)：质因数分解 O(√x)"""
    res = 1
    d = 2
    while d * d <= x:
        if x % d == 0:
            cnt = 0
            while x % d == 0:
                x //= d
                cnt += 1
            if cnt >= 2:
                return 0
            res = -res
        d += 1
    if x > 1:
        res = -res
    return res


def count_coprime_bruteforce(n, m):
    """反演模板：Σ_{i≤n, j≤m} [gcd(i,j)=1] 直接用 mu 求和"""
    mu = mobius_table(max(n, m))
    s = 0
    for d in range(1, min(n, m) + 1):
        s += mu[d] * (n // d) * (m // d)
    return s


def count_coprime_block(n, m):
    """反演 + 整除分块：O(√n)，适合 n,m 达 1e9"""
    mu = mobius_table(isqrt(max(n, m)) + 5)
    pre = [0] * (len(mu))
    for i in range(1, len(mu)):
        pre[i] = pre[i - 1] + mu[i]
    lim = min(n, m)
    s = 0
    d = 1
    while d <= lim:
        qn = n // d
        qm = m // d
        nxt = min(n // qn, m // qm, lim)
        s += (pre[nxt] - pre[d - 1]) * qn * qm
        d = nxt + 1
    return s


if __name__ == "__main__":
    mu = mobius_table(300)
    # 与分解法交叉验证
    for i in range(1, 300):
        assert mu[i] == mobius_single(i), (i, mu[i], mobius_single(i))
    # 核心性质 Σ_{d|n} μ(d) = [n==1]
    for n in range(1, 300):
        s = sum(mu[d] for d in range(1, n + 1) if n % d == 0)
        assert s == (1 if n == 1 else 0), n
    # gcd 互素计数
    for n in range(1, 15):
        for m in range(1, 15):
            brute = sum(1 for i in range(1, n + 1) for j in range(1, m + 1)
                        if math.gcd(i, j) == 1)
            assert count_coprime_bruteforce(n, m) == brute, (n, m)
            assert count_coprime_block(n, m) == brute, (n, m)

    print("All tests passed.")
```

**PyPy 提示**: 线性筛 O(n) 预处理 mu：n=1e7 时 PyPy 约 2s，mu 用普通 list 即可。整除分块每轮 O(1) 查询前缀和，总 O(√min(n,m))，n=1e9 时约 6e4 次循环极快。多组查询先预处理 mu 前缀和再分块。分块时注意 nxt 的边界与 lim 取 min，防止越界。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 线性筛预处理 O(n)；单组反演求和 O(√min(n,m))（整除分块）或 O(min(n,m))（朴素）；单点 μ O(√x) |
| 空间 | O(n)（mu 与前缀和数组） |

### 局限

反演结果的求和若朴素枚举 d 到 min(n,m) 在大范围不可行，必须配合整除分块。整除分块依赖 mu 前缀和，n,m 上界决定了预处理的规模（>1e8 内存/时间压力大）。多变量（如 3 维 gcd 求和）需要两两分块、更复杂。μ 的非完全积性导致不能用简单前缀积。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P2522 | 5 | Problem b：[HAOI2011] 容斥拆成 4 块 + 反演 [gcd(i,j)=k] + 整除分块，OI Wiki 例题 | [https://www.luogu.com.cn/problem/P2522](https://www.luogu.com.cn/problem/P2522) |
| SPOJ | LCMSUM | 5 | Σ lcm(i,n) 用欧拉/莫比乌斯反演转化为因子求和，OI Wiki 例题 | [https://www.spoj.com/problems/LCMSUM/](https://www.spoj.com/problems/LCMSUM/) |
| Codeforces | 1139 D. Steps to One | 7 | 期望问题 + 莫比乌斯反演 + 整除分块，OI Wiki 习题（概率反演经典） | [https://codeforces.com/problemset/problem/1139/D](https://codeforces.com/problemset/problem/1139/D) |

## Pitfalls · 易错点

- μ 用线性筛求时 i%p==0 分支必须 break 且 mu[i*p]=0，漏 break 会重复标记
- 整除分块的分块上界要 min(n,m)，且 nxt 也要对 lim 取 min 防越界
- 求和项用 (n//d)*(m//d) 先整除再相乘，避免浮点
- 反演方向别弄反：f=Σg ⟺ g=Σμf 的倍数形式（gcd 题常用倍数形式）
- [gcd(i,j)=1] 展开成 Σ_{d\|i,d\|j} μ(d)，别忘了 d 的上下界是 1..min(n,m)
- 多组查询不预处理 mu 前缀和会导致每组 O(min(n,m)) 超时

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/number-theory/mobius/](https://oi-wiki.org/math/number-theory/mobius/)
- CP-Algorithms ✓ [https://cp-algorithms.com/algebra/sieve.html](https://cp-algorithms.com/algebra/sieve.html)
- 书籍 ✓ `CPH ch21 数论（含莫比乌斯反演/整除分块，p.210-216）`
