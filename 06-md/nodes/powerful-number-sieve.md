---
id: powerful-number-sieve
name: Powerful Number 筛
group: G-C-9
stage: frontier
priority: P3
depth_tier: brief
---

# Powerful Number 筛

> O(n^{3/4}) 求积性函数前缀和，基于 PN 分解 f=g*h，h 仅在 PN 处非零

<!-- 元信息: id=powerful-number-sieve · group=G-C-9 · stage=frontier · priority=P3 · depth_tier=brief -->

## What · 是什么

Powerful Number（PN）筛是杜教筛的扩展，求一类积性函数前缀和。PN 定义：n 的每个质因子指数 e_i≥2（即不存在质因子只出现一次）。性质：① 所有 PN 可写成 a²b³；② n 以内 PN 至多 O(√n) 个。算法：构造积性函数 g，满足 g(p)=f(p) 且 G(n)=Σg 易求（常用杜教筛）。令 h=f/g（Dirichlet 卷积除法），则 h(p)=0，且 h 只在 PN 处非零。于是 F(n)=Σ_{d≤n, d 为 PN} h(d)·G(⌊n/d⌋)。步骤：枚举全部 PN（DFS 素数指数≥2）、递推求 h(p^c)（用 f(p^c)=Σ_{i=0}^c g(p^i)h(p^{c-i}) 反推）、O(1)/杜教筛求 G(⌊n/d⌋)，累加。复杂度 O(√n·(log n)) + G 查询成本；用杜教筛求 G 时为 O(n^{2/3})。典型例：f(p^k)=p^k(p^k-1)，取 g=id·φ。

## Why · 为什么

### 直觉 · Intuition

杜教筛要求构造的 g 让 f*g 好算。PN 筛换了个角度：让 g 与 f 在‘质数点上完全一致’（g(p)=f(p)），于是两者的差异函数 h=f/g 在质数上为 0。积性函数的‘质数点相同’意味着 h 只在那些‘处处高次’的数（Powerful Number）上有值——而这样的数只有 O(√n) 个！把 f 的前缀和拆成 h(d)·G(n/d) 累加，G 用杜教筛，两边都是亚线性。

### 原理 · Principle

① 构造 g 满足 g(p)=f(p)、g 积性、G(n) 易求；② h=f/g（卷积除法）：h(p)=f(p)-g(p)=0，且 h 为积性 → h 仅在 PN 处非零；③ F(n)=Σ_{d≤n} h(d)G(⌊n/d⌋)=Σ_{d PN} h(d)G(⌊n/d⌋)；④ h(p^c) 由 f(p^c)=Σ_{i=0}^c g(p^i)h(p^{c-i}) 反推（h(p)=0 打底）；⑤ 枚举 PN：DFS 每个素数指数≥2，乘积≤n。性质证明：PN 可写 a²b³（指数 2 或 3 归并）；数量 O(√n)（Σ_{a≤√n} (n/a²)^{1/3} 积分）。复杂度：枚举 O(√n) 个 PN，每个查 G O(1)/杜教筛。

### 历史 · History

Powerful Number 筛是杜教筛思想的进一步发展，常见于中国 OI 圈高端数论题。名称源于 Powerful Number 的既有数学概念。OI Wiki《Powerful Number 筛》页系统给出构造 g 的两种 h(p^c) 求法（直接公式 vs 枚举反推）、PN 枚举与复杂度分析，例题 Luogu P5325（Min_25 模板亦可解）与 LibreOJ 6053。

## How · 实现

### 伪代码

```python
# 步骤
1. 线性筛 sqrt(n) 内素数
2. 构造 g (g(p)=f(p), G 易求, 常用杜教筛)
3. 对每个素数 p 递推 h(p^c):
   h(p^c) = f(p^c) - sum_{i=1..c} g(p^i)*h(p^{c-i})   # h(p)=0
4. DFS 枚举所有 PN d: 每个素数指数>=2 累乘
   ans += h(d) * G(n // d)
def dfs(idx, d, hval):
  if idx == len(primes): ans += hval*G(n//d); return
  dfs(idx+1, d, hval)            # 不含 primes[idx]
  p = primes[idx]; pe = p*p
  for e in 2..:                  # 指数>=2
    if pe > n//d: break
    dfs(idx+1, d*pe, hval*h(p^e))
    pe *= p
# 例: f(p^k)=p^k(p^k-1), g=id*phi -> h(p^k)=(k-1)(p-1)p^k
```

### Python 实现

```python
"""Powerful Number 筛: 求积性函数 f 前缀和.
核心: 构造积性函数 g, g(p)=f(p) 且 G(n) 易求 (一般杜教筛). 
定义 h = f/g (Dirichlet 卷积除法), 则 h 仅在 Powerful Number 处非零.
F(n) = sum_{d PN, d<=n} h(d) * G(n//d).
PN 个数 O(sqrt n). 这里演示 f(p^k)=p^k(p^k-1) (P5325 模板): g = id*phi, 
G(n) = sum i*phi(i), 由 (id*phi)*id = id^2 得杜教筛递推.
"""
import math


class PNSieve:
    def __init__(self, n):
        self.n = n
        self.sqn = int(math.isqrt(n))
        self.primes = []
        self._sieve()
        # 杜教筛 G(n)=sum i*phi(i) 的记忆化
        self.phi_prefix = {}
        self._precompute_phi()

    def _sieve(self):
        m = self.sqn
        is_p = [True] * (m + 1)
        is_p[0] = is_p[1] = False
        for i in range(2, int(m ** 0.5) + 1):
            if is_p[i]:
                for j in range(i * i, m + 1, i):
                    is_p[j] = False
        self.primes = [i for i in range(2, m + 1) if is_p[i]]

    def _precompute_phi(self):
        m = self.sqn
        phi = list(range(m + 1))
        for i in range(2, m + 1):
            if phi[i] == i:
                for j in range(i, m + 1, i):
                    phi[j] -= phi[j] // i
        s = 0
        self.phi_pre = [0] * (m + 1)
        for i in range(1, m + 1):
            s += i * phi[i]
            self.phi_pre[i] = s

    def G(self, n):
        """G(n) = sum_{i<=n} i*phi(i). 杜教筛: (id*phi)*id = id^2."""
        if n <= self.sqn:
            return self.phi_pre[n]
        if n in self.phi_prefix:
            return self.phi_prefix[n]
        ans = n * (n + 1) * (2 * n + 1) // 6   # sum i^2
        l = 2
        while l <= n:
            r = n // (n // l)
            ans -= (r * (r + 1) // 2 - (l - 1) * l // 2) * self.G(n // l)
            l = r + 1
        self.phi_prefix[n] = ans
        return ans

    def h_pk(self, p, k):
        """h(p^k). 由 f(p^k)=p^k(p^k-1), g=id*phi, f=g*h 反推.
        已知 h(p^k) = (k-1)(p-1)*p^k (OI Wiki 推导结果)."""
        if k == 1:
            return 0
        return (k - 1) * (p - 1) * (p ** k)

    def run(self):
        """DFS 枚举所有 Powerful Number d<=n, 累加 h(d)*G(n//d)."""
        self.ans = 0

        def dfs(idx, d, hval):
            if idx >= len(self.primes):
                self.ans += hval * self.G(self.n // d)
                return
            # 不引入 primes[idx] 的分支
            dfs(idx + 1, d, hval)
            # 引入 primes[idx] 的 >=2 次方 (PN 要求每个质因子指数>=2)
            p = self.primes[idx]
            pe = p * p
            for k in range(2, 40):
                if pe > self.n // d:
                    break
                h_pk = self.h_pk(p, k)
                dfs(idx + 1, d * pe, hval * h_pk)
                pe *= p
        dfs(0, 1, 1)
        return self.ans


def brute_prefix(n):
    def f(x):
        res = 1
        d = 2
        y = x
        while d * d <= y:
            c = 0
            while y % d == 0:
                y //= d; c += 1
            if c:
                res *= (d ** c) * (d ** c - 1)
            d += 1
        if y > 1:
            res *= y * (y - 1)
        return res
    return sum(f(i) for i in range(1, n + 1))


if __name__ == "__main__":
    for n in [10, 30, 100, 1000, 5000, 100000]:
        ps = PNSieve(n)
        got = ps.run()
        exp = brute_prefix(n)
        assert got == exp, (n, got, exp)
    print("powerful-number-sieve: all tests passed")

```

**PyPy 提示**: DFS 遍历 PN 时用迭代/栈避免深递归（素数个数 log 量级，安全）。h(p^c) 可预计算二维表（p 与指数）供 DFS 查。G 用杜教筛（记忆化 dict），n//d 的取值又是 ⌊n/k⌋ 形式，可复用杜教筛的 memo。PyPy 下注意 dict 键为大整数时哈希开销。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(√n·log n) 预处理 h(p^c) + O(√n) PN 枚举 × G 查询（杜教筛时总 O(n^{2/3})） |
| 空间 | O(√n) |

### 局限

① 需构造合适的 g（g(p)=f(p) 且 G 易求），对 f 的结构有要求；② 若 G 用杜教筛则总复杂度受杜教筛限制；③ h(p^c) 递推易错（卷积方向）；④ 枚举 PN 的 DFS 细节（指数上界 pe≤n/d）需注意；⑤ 对非 PN 支撑的 f（f 在质数点本身复杂）不适用。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P5325 | 5 | 【模板】Min_25 筛：f(p^k)=p^k(p^k-1)，PN 筛亦可解（g=id·φ） | [https://www.luogu.com.cn/problem/P5325](https://www.luogu.com.cn/problem/P5325) |
| LibreOJ | 6053 | 5 | 简单的函数：构造 g 处理 f(p)=p xor c 的 PN 筛解法 | [https://loj.ac/p/6053](https://loj.ac/p/6053) |

## Pitfalls · 易错点

- h(p) 应为 0 而误算为 f(p)（卷积除法反推时从 h(p)=0 起）
- h(p^c) 反推漏了 Σ_{i=1..c} 的 g(p^i)h(p^{c-i}) 项
- DFS 枚举 PN 时包含质因子指数=1 的数（非 PN）
- G(n//d) 未用杜教筛 memo 导致重复计算
- 指数循环上界写成 pe≤n 而非 pe≤n//d
- g 选择错误（g(p)≠f(p)）导致 h 不只在 PN 非零

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/number-theory/powerful-number/](https://oi-wiki.org/math/number-theory/powerful-number/)
- OI Wiki ✓ [https://oi-wiki.org/math/number-theory/du/](https://oi-wiki.org/math/number-theory/du/)
- article ✓ [https://www.cnblogs.com/wallbreaker5th/p/13901487.html](https://www.cnblogs.com/wallbreaker5th/p/13901487.html)
