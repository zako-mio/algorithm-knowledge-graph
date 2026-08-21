---
id: min-25-sieve
name: Min_25 筛
group: G-C-9
stage: frontier
priority: P3
depth_tier: brief
---

# Min_25 筛

> O(n^{3/4}/log n) 求积性函数前缀和，埃氏筛过程 + 有效点值压缩（Extended Eratosthenes Sieve）

<!-- 元信息: id=min-25-sieve · group=G-C-9 · stage=frontier · priority=P3 · depth_tier=brief -->

## What · 是什么

Min_25 筛（Extended Eratosthenes Sieve）在亚线性时间 O(n^{3/4}/log n)（或 Θ(n^{1-ε})）计算一类积性函数的前缀和。适用条件：① f(p) 是关于 p 的多项式（可拆成若干个完全积性函数 p^k 的线性组合）；② f(p^c) 可快速求值。思路分两阶段：① 求 Fprime(n)=Σ_{p≤n} f(p) 的全部有效点值（只在 n//i 处取值，共 O(√n) 个）——用 G 数组模拟埃氏筛，把每个完全积性部分分开筛；② 按 F_k(n)=Σ_{lpf(i)≥p_k} f(i) 的递推递归/迭代求 F_1(n)，答案 = F_1(n)+f(1)。相比杜教筛无需构造 g，可处理 f(p)=p-1（φ）、f(p^k)=p^k(p^k-1)（P5325）等。

## Why · 为什么

### 直觉 · Intuition

埃氏筛的每一步都在‘删合数’。若我们只关心质数上的 f(p) 之和，可以用数组 G 记录‘剩余未被删掉的数的 f 值之和’，每筛一个质数 p 就从 G 里减去 p 贡献的合数部分。所有需要的值只在 n//i 的 O(√n) 个点上出现，配合下标压缩即可在亚线性时间内跑完整个埃氏筛过程。第二阶段再用递归把合数部分的贡献按最小质因子枚举回来。

### 原理 · Principle

定义 G_k(n)=Σ_{i≤n, lpf(i)>p_k 或 i 为质数} g(i)（g 为完全积性部分）。边界 G_0(n)=Σ_{i=2}^n g(i)。转移：G_k(n)=G_{k-1}(n) − [p_k²≤n]·g(p_k)·(G_{k-1}(n/p_k) − G_{k-1}(p_{k-1}))。对所有 n//i 点值分别做，筛到 p_ℓ 后剩余即质数。Fprime(n)=Σ a_i·G^{(k)}(n) 对多项式各幂次合并。第二阶段：F_k(n)=Σ_{i≥k, p_i²≤n} Σ_{c≥1, p_i^{c+1}≤n} [f(p_i^c)F_{i+1}(n/p_i^c) + f(p_i^{c+1})] + Fprime(n) − Fprime(p_{k-1})。复杂度：Fprime 阶段 O(Σ√(n/x)/log…) = O(n^{3/4}/log n)；F_k 阶段对每个点枚举 p 的平方根范围。

### 历史 · History

Min_25 筛得名自日本网友 Min_25（hatenablog 博客，2020 年前后活跃），首次系统整理该思想（又称 Extended Eratosthenes Sieve）。其‘分块 G 数组’与洲阁筛第一部分的实现本质相同。中国 OI 圈经 Luogu P5325 模板题传播。OI Wiki《Min_25 筛》页给出完整推导、两种 F_k 求法（直接递推 / 后缀和优化）与复杂度证明（朱震霆 2018 集训队论文）。

## How · 实现

### 伪代码

```python
# 以 f(p)=p^2-p (即 P5325 f(p^k)=p^k(p^k-1)) 为例
# 阶段1: Fprime
w = 数论分块得到所有 n//i (O(sqrt n))
for 幂次 s in {1,2}:
  G_s[i] = sum_{2..w[i]} j^s   # 初始所有整数
  for k,p in primes:            # 埃筛
    if p*p > n: break
    for i: if w[i] < p*p: break
      G_s[i] -= p^s * (G_s[id(w[i]//p)] - sp_s[k-1])
Fprime[i] = G2[i] - G1[i]
# 阶段2: F_1(n)
def S(x, k):   # F_k(x)
  ans = Fprime(id(x)) - Fprime(p_{k-1})
  for i>=k, p_i*p_i <= x:
    pe = p_i
    for c>=1 while pe*p_i <= x:
      ans += f(pe)*S(x//pe, i+1) + f(pe*p_i)
      pe *= p_i
  return ans
ans = S(n, 0) + 1
```

### Python 实现

```python
"""Min_25 筛: O(n^{3/4}/log n) 求积性函数前缀和.
原理: 埃氏筛过程. 对 f(p^k) 可快速求值、f(p) 为多项式(完全积性函数线性组合)的积性函数 f.
流程:
  1. 数论分块得到所有有效点 w = n//i (O(sqrt n) 个);
  2. 用 G 数组模拟埃筛, 求 Fprime(n)=sum_{p<=n} f(p) 的所有有效点值;
  3. 递归/迭代求 F_k(n) = sum_{i<=n, lpf(i)>=p_k} f(i), 答案 = F_1(n)+1.
示例: f(p^k)=p^k(p^k-1) (Luogu P5325 模板).
"""
import math


class Min25:
    def __init__(self, n):
        self.n = n
        self.sqn = int(math.isqrt(n))
        self.primes = []
        self.sprime = []        # 前缀质数和的 1/2 次幂
        self.w = []             # 有效点值 n//i (去重)
        self.id1 = {}
        self.id2 = {}
        self.g = []             # g[id][k]: 第 k 次埃筛后剩余和(这里存一维滚动)
        self._sieve()
        self._g_vals = {}

    def _sieve(self):
        n = self.sqn
        is_p = [True] * (n + 1)
        is_p[0] = is_p[1] = False
        for i in range(2, int(n ** 0.5) + 1):
            if is_p[i]:
                for j in range(i * i, n + 1, i):
                    is_p[j] = False
        self.primes = [i for i in range(2, n + 1) if is_p[i]]

    def _id(self, x):
        if x <= self.sqn:
            return self.id1[x]
        return self.id2[self.n // x]

    def build(self, h, h2):
        """h(n)=sum_{i<=n, isprime} f(i) 所需的基础完全积性部分.
        这里固定演示 f(p)=p(p-1)=p^2-p, 拆成 p^2 与 p 两个完全积性函数.
        h/h2: 对应 1 与 i 的"所有整数前缀和"函数 (用于 G0).
        实际实现针对每个幂次单独跑一遍埃筛."""
        # 收集有效点
        l = 1
        w = []
        while l <= self.n:
            v = self.n // l
            w.append(v)
            if v <= self.sqn:
                self.id1[v] = len(w) - 1
            else:
                self.id2[l] = len(w) - 1
            l = self.n // v + 1
        self.w = w

        # 对 f(p)=p^2-p 的每个幂次分别跑埃筛: g2 (p^2) 和 g1 (p)
        # G0(v) = sum_{2<=i<=v} i^s, s=2 或 1
        m = len(w)
        g2 = [0] * m
        g1 = [0] * m
        for i, v in enumerate(w):
            g2[i] = (v * (v + 1) * (2 * v + 1) // 6) - 1   # sum_{2..v} i^2
            g1[i] = (v * (v + 1) // 2) - 1                 # sum_{2..v} i
        sp1 = [0]; sp2 = [0]
        for p in self.primes:
            sp1.append(sp1[-1] + p)
            sp2.append(sp2[-1] + p * p)
        self.sp1, self.sp2 = sp1, sp2
        self.sf = [0] * len(self.primes)   # sf[k] = Fprime(primes[k]) (0-based)
        for k, p in enumerate(self.primes):
            self.sf[k] = (sp2[k + 1] - sp1[k + 1])
        # 埃筛转移: 对第 k 个质数 p_k, g[v] -= p^s * (g[v/p] - sp[k-1])
        for k, p in enumerate(self.primes):
            pk2 = p * p
            if pk2 > self.n:
                break
            for i, v in enumerate(w):
                if v < pk2:
                    break
                g2[i] -= p * p * (g2[self._id(v // p)] - sp2[k])
                g1[i] -= p * (g1[self._id(v // p)] - sp1[k])
        # Fprime(v) = g2[v] - g1[v] = sum_{p<=v} (p^2 - p)
        self.g = [g2[i] - g1[i] for i in range(m)]
        self.g2, self.g1 = g2, g1

    def S(self, x, k):
        """F_{k}(x): sum_{i<=x, lpf(i)>=p_k} f(i). 递归(记忆化)."""
        if x <= 1 or self.primes[k - 1] > x:
            return 0
        if k == 0:
            ans = self.g[self._id(x)]
        else:
            ans = self.g[self._id(x)] - self.sf[k - 1]
        for i in range(k, len(self.primes)):
            p = self.primes[i]
            if p * p > x:
                break
            pe = p
            for e in range(1, 20):
                if pe * p > x:
                    break
                # 项1: f(p^e) * F_{i+1}(x / p^e)
                ans += (pe * (pe - 1)) * self.S(x // pe, i + 1)
                # 项2: f(p^{e+1})
                pe2 = pe * p
                ans += pe2 * (pe2 - 1)
                pe = pe2
        return ans

    def prefix_sum(self):
        """返回 sum_{i=1..n} f(i)."""
        return self.S(self.n, 0) + 1


def brute_prefix(n):
    def f(n):
        # f(p^k)=p^k(p^k-1), 积性
        res = 1
        d = 2
        x = n
        while d * d <= x:
            c = 0
            while x % d == 0:
                x //= d
                c += 1
            if c:
                res *= (d ** c) * (d ** c - 1)
            d += 1
        if x > 1:
            res *= x * (x - 1)
        return res
    return sum(f(i) for i in range(1, n + 1))


if __name__ == "__main__":
    for n in [10, 20, 100, 1000, 5000]:
        m = Min25(n)
        m.build(None, None)
        got = m.prefix_sum()
        exp = brute_prefix(n)
        assert got == exp, (n, got, exp)
    print("min-25-sieve: all tests passed (f(p^k)=p^k(p^k-1))")

```

**PyPy 提示**: 有效点压缩：id1[id(v)] for v≤√n，id2[n//v] for v>√n（v=n//i）。G 数组只开 O(√n)。每轮埃筛对 G 的全部点做一次（可用前缀和技巧只对受影响点更新）。递归 S 用 dict 记忆化（对每个 (x,k) 可能重复）。PyPy 下对 n=1e11 量级可跑；n 更大注意 G 数组与幂次计算的整数溢出（Python 无溢出但慢）。实现要点：对 f(p) 每个幂次单独跑一遍埃筛再合并。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n^{3/4}/log n)（Fprime 阶段）；F_k 直接递推 Θ(n^{1-ε})，后缀和优化同前 |
| 空间 | O(√n) |

### 局限

① 要求 f(p) 能写成低次多项式（完全积性线性组合）；② 要求 f(p^c) 快速可求；③ 实现细节多（下标压缩、幂次分离、递归边界）易错；④ 对任意积性函数不适用（需满足上述结构）；⑤ 常数较大，小 n 不如杜教筛。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P5325 | 5 | 【模板】Min_25 筛：f(p^k)=p^k(p^k-1)，模板题 | [https://www.luogu.com.cn/problem/P5325](https://www.luogu.com.cn/problem/P5325) |
| Luogu | P4213 | 4 | 杜教筛模板：φ/μ 前缀和（Min_25 亦可解，f(p)=p-1 / -1） | [https://www.luogu.com.cn/problem/P4213](https://www.luogu.com.cn/problem/P4213) |
| LibreOJ | 6053 | 5 | 简单的函数：f(p^k)=p xor c，OI Wiki 例题（需对 p=2 特判） | [https://loj.ac/p/6053](https://loj.ac/p/6053) |

## Pitfalls · 易错点

- 下标压缩 id1/id2 映射写错（v 与 n//v 混用）
- 对 f(p) 多项式各幂次分开筛后忘记合并
- G 数组只更新受 p 影响的点（w[i]<p² 提前 break）
- F_k 递归对 f(p^{e+1}) 项与 f(p^e)F_{i+1} 项重复/遗漏
- Fprime(p_{k-1}) 用质数和而非 Fprime 前缀（需 sf[] 数组）
- 递归 S 无记忆化导致指数级重复

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/number-theory/min-25/](https://oi-wiki.org/math/number-theory/min-25/)
- OI Wiki ✓ [https://oi-wiki.org/math/number-theory/du/](https://oi-wiki.org/math/number-theory/du/)
- 论文 ✓ `朱震霆 2018 集训队论文《一些特殊的数论函数求和问题》`
