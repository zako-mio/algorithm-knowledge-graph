---
id: du-sieve
name: 杜教筛
group: G-C-9
stage: frontier
priority: P2
depth_tier: standard
---

# 杜教筛

> O(n^{2/3}) 求积性函数前缀和，Dirichlet 卷积 + 数论分块 + 记忆化

<!-- 元信息: id=du-sieve · group=G-C-9 · stage=frontier · priority=P2 · depth_tier=standard -->

## What · 是什么

杜教筛（Du Jiao Sieve）在亚线性时间 O(n^{2/3})（预处理后）内计算积性函数的前缀和 S(n)=Σ_{i≤n} f(i)。思想：构造一个『好算』的数论函数 g，使 f*g（Dirichlet 卷积）与 g 的前缀和都易求，再由恒等式 g(1)S(n) = Σ(f*g)(i) − Σ_{i≥2} g(i)·S(⌊n/i⌋) 递推，数论分块加速右边，记忆化每个 ⌊n/k⌋ 点值。经典应用：Σμ(i)（f=μ,g=1,f*g=ε）与 Σφ(i)（f=φ,g=1,f*g=id）。配合线性筛预处理前 n^{2/3} 个值，只对 >阈值 的点递归，总复杂度 O(n^{2/3})。是数论高级题（区间 gcd/互质对、积性函数求和）的常用子程序。

## Why · 为什么

### 直觉 · Intuition

直接累加 f(1..n) 太慢；把 f 与 g 卷积后，整体前缀和被拆成『易算的部分』减掉『可分块的递归部分』。关键在于：需要算的 S 只在形如 ⌊n/k⌋ 的 O(√n) 个值上出现，记忆化后每个值只算一次。把大部分工作留给线性筛（预处理），剩余的点很少且共享——像先盖好地基（筛），再用脚手架（数论分块）快速收尾。

### 原理 · Principle

Σ_{i≤n}(f*g)(i) = Σ_{d≤n} g(d)·S(⌊n/d⌋)（交换求和顺序）。移项：g(1)S(n) = Σ(f*g)(i) − Σ_{d=2}^{n} g(d)·S(⌊n/d⌋)。若 Σ(f*g) 与 Σg(d) 可 O(1)/分块求，则右边按 ⌊n/d⌋ 相等分块 O(√n) 段递归。记忆化所有 S(⌊n/k⌋)：这些值构成 R(n)={⌊n/k⌋}，|R(n)|=O(√n)，且 R(m)⊆R(n)。复杂度：不预处理 O(n^{3/4})；线性筛预处理到 m=n^{2/3} 得 O(T₀(m)+n/√m)=O(n^{2/3})。对 μ：f*g=ε → S(n)=1−Σ_{d≥2}S(⌊n/d⌋)。对 φ：f*g=id → S(n)=n(n+1)/2 − Σ_{d≥2}S(⌊n/d⌋)。

### 历史 · History

杜教筛由杜子德（中国国家队）于 2016 年集训队论文《积性函数求和的几种方法》系统整理并推广（命名源自此）。核心技巧（利用 R(n) 记忆化）早在更早的计数数论中出现，但杜教筛将其工程化为模板。Luogu P4213 模板题即求 μ/φ 前缀和。OI Wiki《杜教筛》页有完整推导与伪证辨析（强调记忆化是亚线性复杂度的关键）。

## How · 实现

### 伪代码

```python
# 预处理阈值内用线性筛, 之上递归记忆化
class DuSieve:
  smu, sphi = linear_sieve(TH)   # 前缀和表
  def S_mu(n):
    if n <= TH: return smu[n]
    if n in memo: return memo[n]
    ans = 1                     # Σ(f*g)(i) = Σ ε = 1
    l = 2
    while l <= n:
      r = n // (n // l)
      ans -= (r-l+1) * S_mu(n//l)
      l = r + 1
    memo[n] = ans; return ans
  def S_phi(n):
    ... ans = n*(n+1)//2       # Σ id = n(n+1)/2
      ans -= (r-l+1) * S_phi(n//l)
```

### Python 实现

```python
"""杜教筛: 求积性函数前缀和 S(n) = sum f(i), 亚线性.
核心递推: g(1)S(n) = sum_{i=1..n}(f*g)(i) - sum_{i=2..n} g(i) S(n//i).
- 对 mu:  f=mu, g=1, f*g=eps, S(n)=1 - sum_{i>=2} S(n//i)
- 对 phi: f=phi, g=1, f*g=id, S(n)=n(n+1)/2 - sum_{i>=2} S(n//i)
数论分块加速, 记忆化 O(n^{2/3})."""
import math
from functools import lru_cache


def linear_sieve(n):
    mu = [0] * (n + 1); phi = [0] * (n + 1)
    mu[1] = 1; phi[1] = 1
    primes = []
    is_comp = [False] * (n + 1)
    for i in range(2, n + 1):
        if not is_comp[i]:
            primes.append(i)
            mu[i] = -1; phi[i] = i - 1
        for p in primes:
            if i * p > n: break
            is_comp[i * p] = True
            if i % p == 0:
                mu[i * p] = 0
                phi[i * p] = phi[i] * p
                break
            else:
                mu[i * p] = -mu[i]
                phi[i * p] = phi[i] * (p - 1)
    smu = [0] * (n + 1); sphi = [0] * (n + 1)
    for i in range(1, n + 1):
        smu[i] = smu[i - 1] + mu[i]
        sphi[i] = sphi[i - 1] + phi[i]
    return smu, sphi


class DuSieve:
    """杜教筛 mu 与 phi 前缀和. THRESHOLD 内线性筛打表, 之上递归记忆化."""
    def __init__(self, threshold=10**6):
        self.T = threshold
        self.smu, self.sphi = linear_sieve(threshold)
        self.mu_map = {}
        self.phi_map = {}

    def S_mu(self, n):
        if n <= self.T:
            return self.smu[n]
        if n in self.mu_map:
            return self.mu_map[n]
        ans = 1
        l = 2
        while l <= n:
            r = n // (n // l)
            ans -= (r - l + 1) * self.S_mu(n // l)
            l = r + 1
        self.mu_map[n] = ans
        return ans

    def S_phi(self, n):
        if n <= self.T:
            return self.sphi[n]
        if n in self.phi_map:
            return self.phi_map[n]
        ans = n * (n + 1) // 2
        l = 2
        while l <= n:
            r = n // (n // l)
            ans -= (r - l + 1) * self.S_phi(n // l)
            l = r + 1
        self.phi_map[n] = ans
        return ans


if __name__ == "__main__":
    # 暴力验证 mu/phi 前缀和
    def brute(n):
        mu = [0] * (n + 1); phi = list(range(n + 1))
        for i in range(1, n + 1):
            mu[i] = 1
        is_p = [True] * (n + 1)
        for i in range(2, n + 1):
            if is_p[i]:
                for j in range(i, n + 1, i):
                    is_p[j] = False
                    mu[j] *= -1
                ii = i * i
                for j in range(ii, n + 1, ii):
                    mu[j] = 0
        # phi via sieve
        for i in range(2, n + 1):
            if phi[i] == i:
                for j in range(i, n + 1, i):
                    phi[j] -= phi[j] // i
        smu = [0] * (n + 1); sphi = [0] * (n + 1)
        for i in range(1, n + 1):
            smu[i] = smu[i - 1] + mu[i]
            sphi[i] = sphi[i - 1] + phi[i]
        return smu, sphi

    n = 5000
    smu, sphi = brute(n)
    ds = DuSieve(threshold=100)
    for x in range(1, n + 1):
        assert ds.S_mu(x) == smu[x], x
        assert ds.S_phi(x) == sphi[x], x
    # 大数抽查: 用更大的阈值线性筛核对若干大点
    ds2 = DuSieve(threshold=10**6)
    big = [123456, 10**7, 10**8, 10**9]
    for b in big:
        if b <= 10**7:
            smu2, sphi2 = brute(b)
            assert ds2.S_mu(b) == smu2[b], b
            assert ds2.S_phi(b) == sphi2[b], b
    print("du-sieve: all tests passed")

```

**PyPy 提示**: 记忆化用 dict；分块用 while l<=n: r=n//(n//l) 模式。线性筛用数组实现比 list of prime 快。阈值 TH 取 1e6~2e6 平衡（PyPy 下 n^{2/3} 的 n 到 1e11 级别仍快）。递归深度 ≤ 因子数 log，安全。若内存紧，可只预处理到 n^{2/3} 的平方根量级。注意 S 的 memo 对每个 ⌊n/k⌋ 只存一次。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n^{2/3})（线性筛预处理 m=n^{2/3}）；不预处理 O(n^{3/4}) |
| 空间 | O(n^{2/3}) 表 + O(√n) memo |

### 局限

① 必须能构造合适的 g（要求 Σ(f*g) 与 Σg 易求）；② 不适用于任意函数（非积性函数需特殊构造）；③ 记忆化+分块代码易错（边界、负数）；④ 预处理阈值选择影响常数；⑤ 只给单个前缀和，不能支持区间查询改造（需前缀差）。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P4213 | 4 | 【模板】杜教筛(Sum)：同时求 μ 与 φ 前缀和，OI Wiki 模板 | [https://www.luogu.com.cn/problem/P4213](https://www.luogu.com.cn/problem/P4213) |
| Luogu | P3768 | 5 | 简单的数学题：莫比乌斯反演 + 杜教筛求 d²φ(d) 前缀和 | [https://www.luogu.com.cn/problem/P3768](https://www.luogu.com.cn/problem/P3768) |

## Pitfalls · 易错点

- 分块边界 r=n//(n//l) 写错导致死循环或漏段
- 忘记记忆化 → 复杂度退化 O(n^{3/4}) 甚至更差
- 对负数结果未取模/未修正（数论分块减出负数）
- f*g 前缀和算错（如 φ 的 n(n+1)/2 而非 n²）
- 线性筛阈值与递归阈值不一致导致边界值重复计算
- 递归层数深 + dict 命中率低导致 TLE（应扩大阈值）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/number-theory/du/](https://oi-wiki.org/math/number-theory/du/)
- OI Wiki ✓ [https://oi-wiki.org/math/number-theory/sqrt-decomposition/](https://oi-wiki.org/math/number-theory/sqrt-decomposition/)
- 论文 ✓ `任之洲 2016 集训队论文《积性函数求和的几种方法》`
