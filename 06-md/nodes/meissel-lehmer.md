---
id: meissel-lehmer
name: Meissel–Lehmer 素数计数
group: G-C-9
stage: frontier
priority: P3
depth_tier: brief
---

# Meissel–Lehmer 素数计数

> 亚线性 O(n^{2/3}/log²n) 计算 π(x)（≤x 素数个数），递归容斥 φ(x,a) + P₂

<!-- 元信息: id=meissel-lehmer · group=G-C-9 · stage=frontier · priority=P3 · depth_tier=brief -->

## What · 是什么

Meissel–Lehmer 算法在亚线性时间内计算素数计数函数 π(x)=#{p≤x}。思想：定义 φ(x,a)=所有≤x 且最小质因子>p_a 的数的个数，P_k(x,a)=恰有 k 个可重质因子且都>p_a 的数的个数。取 a=π(x^{1/3})，有 π(x)=φ(x,a)+a−1−P₂(x,a)。其中 φ 用递归/容斥（φ(x,b)=φ(x,b−1)−φ(⌊x/p_b⌋,b−1)）配合『普通叶子/特殊叶子』终止条件优化；P₂ 枚举质数对 (p,q) 用 π 前缀表求和。整体 O(x^{2/3}/log²x) 时间、O(x^{1/3}log³x) 空间（取 y=x^{1/3}）。更进一步的 Lehmer 公式与 Lagarias-Miller-Odlyzko (LMO) 变体达到 O(x^{2/3}/log²x) 级别。竞赛/科研中用于 n 极大（如 1e18）的素数计数。

## Why · 为什么

### 直觉 · Intuition

直接数质数要筛到 x，太慢。换个思路：所有 ≤x 的数 = 质数 ∪ 合数。合数必有 ≤√x 的小质因子。φ(x,a) 数出‘不含任何小质因子(≤p_a)的数’——这些只剩 1、质数(>p_a) 和两个较大质数的乘积。于是 π(x) ≈ φ(x,a) 加上漏掉的、再减掉多算的，通过 P₂ 精确修正。递归时用容斥逐步剥掉质因子 p_1..p_a，类似‘埃氏筛的计数版本’。

### 原理 · Principle

φ(x,b)=φ(x,b−1)−φ(⌊x/p_b⌋,b−1)（能被 p_b 整除的数排除）。递归终止条件 2：b=0 且 n≤y，或 n>y 时停止，把叶子分成‘普通叶子’(n≤y, 贡献 μ(n)⌊x/n⌋) 与‘特殊叶子’(n>y, 贡献 μ(n)φ(x/n, π(δ(n))−1))，从而 S₀ 用 Möbius 前缀 O(y loglog x) 求，S 再拆 S₁,S₂,S₃（按 p 与 x^{1/3},x^{1/4} 分界）用 π 表分块求。P₂(x,a)=Σ_{y<p≤√x}(π(x/p)−π(p)+1)。最终 π(x)=S₀+S+a−1−P₂。总复杂度取 y=x^{1/3}log³x loglog x：O(x^{2/3}/log²x)。

### 历史 · History

1893 年 Ernst Meissel 用类似方法手工计算 π(10^9)；1959 年 Derrick Lehmer 改进并计算 π(10^10) 以内的素数。1980s Lagarias, Miller 与 Odlyzko 提出更快的 LMO 方法。经典函数 count_primes（kactl/模板）实现 Lehmer 版：π(x)=φ(x,a)+a−1−P₂。OI Wiki《Meissel–Lehmer》页基于论文 Computing π(x): the Meissel, Lehmer, Lagarias, Miller, Odlyzko method 详细推导。

## How · 实现

### 伪代码

```python
# 经典 Lehmer 版 (可查表工程实现):
phi(x, s):   # 最小质因子>p_s 的数个数
  if s == 0: return x
  if s == 1: return x - x//2
  if s == 2: return x - x//2 - x//3 + x//6
  if x < primes[s-1]**2: return pi(x) - s + 1
  return phi(x, s-1) - phi(x//primes[s-1], s-1)

pi(x):
  if x < N: return pi_arr[x]          # 预筛表
  a = pi(x**(1/3)); b = pi(isqrt(x))
  ans = phi(x, a) + a - 1 - P2(x, a)  # P2 枚举质数对
  return ans
# P2(x,a) = sum_{p in (p_a, sqrt(x)]} (pi(x//p) - pi(p) + 1)
```

### Python 实现

```python
"""Meissel-Lehmer 亚线性求 pi(x): 素数个数.
实现经典递归版 (用于中小 x 教学; 工程级加速见 OI Wiki 分块优化):
  pi(x) = phi(x, a) + a - 1 - P2(x, a),  a = pi(x^{1/3}), y = x^{1/3}
配合 phi(x, a) 递归 + P2 双素数对计数."""
import math


def sieve_primes(limit):
    is_p = [True] * (limit + 1)
    if limit >= 0: is_p[0] = False
    if limit >= 1: is_p[1] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if is_p[i]:
            for j in range(i * i, limit + 1, i):
                is_p[j] = False
    return [i for i in range(2, limit + 1) if is_p[i]]


class MeisselLehmer:
    def __init__(self, maxn=10**8):
        # 预筛到 maxn, 供 pi 查询
        self.primes = sieve_primes(maxn)
        self.pi_arr = [0] * (maxn + 1)
        j = 0
        for i in range(maxn + 1):
            while j < len(self.primes) and self.primes[j] <= i:
                j += 1
            self.pi_arr[i] = j

    def phi(self, x, a):
        """<=x 且最小质因子 > p_a 的数的个数."""
        if a == 0:
            return x
        if a == 1:
            return x - x // 2
        if a == 2:
            return x - x // 2 - x // 3 + x // 6
        if x < self.primes[a - 1] ** 2:
            # 小 x: 直接数
            return self.pi_small(x) - a + 1
        # 递归: phi(x,a) = phi(x,a-1) - phi(x/p_a, a-1)
        return self.phi(x, a - 1) - self.phi(x // self.primes[a - 1], a - 1)

    def pi_small(self, x):
        if x < len(self.pi_arr):
            return self.pi_arr[x]
        raise ValueError("x too large")

    def pi(self, x):
        if x < len(self.pi_arr):
            return self.pi_arr[x]
        return self.pi_sublinear(x)

    def pi_sublinear(self, x):
        # 主定理: 取 y=x^{1/3}, a=pi(y)
        y = int(x ** (1.0 / 3.0))
        while (y + 1) ** 3 <= x: y += 1
        while y ** 3 > x: y -= 1
        a = self.pi_small(y)
        # P2(x,a) = sum_{p in (y, sqrt x], p<=q, pq<=x} 1
        p2 = 0
        lo = y + 1
        hi = int(math.isqrt(x))
        if lo <= hi:
            primes_in = [p for p in self.primes if lo <= p <= hi]
            for p in primes_in:
                p2 += self.pi_small(x // p) - self.pi_small(p) + 1
        phi_xa = self.phi(x, a)
        return phi_xa + a - 1 - p2


if __name__ == "__main__":
    ml = MeisselLehmer(10**6)
    # 已知 pi 值
    known = {0: 0, 1: 0, 2: 1, 3: 2, 10: 4, 100: 25, 1000: 168,
             10000: 1229, 100000: 9592, 10**6: 78498}
    for x, v in known.items():
        assert ml.pi_small(x) == v, (x, ml.pi_small(x), v)
        assert ml.pi(x) == v, (x, ml.pi(x), v)
    # 跨阈值的亚线性分支 (x > 10^6 走 phi/P2 路径), 用独立筛验证
    for x in [2 * 10**6, 5 * 10**6]:
        cnt = len(sieve_primes(x))
        got = ml.pi(x)
        assert got == cnt, (x, got, cnt)
    print("meissel-lehmer: all tests passed")

```

**PyPy 提示**: 预筛表 pi_arr 到 1e6~1e7 用一次埃筛（数组 int）。phi 递归深度 ≤ a ≈ log x，安全。P2 枚举 (y,√x] 内质数，对每个 p 查 pi(x//p)（大 x 时 x//p 超出表 → 需要亚线性分支递归，工程实现会缓存）。注意 x^{1/3} 用整数立方根（while 修正）避免浮点误差。大 x 时 pi 查询自身递归，务必 memo。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(x^{2/3}/log²x)；预处理 O(N)（N=筛表上限） |
| 空间 | O(x^{1/3}log³x)（y=x^{1/3} 取法） |

### 局限

① 实现复杂，φ 递归与 P₂ 的边界/终止条件易错；② 需要 π 表支持子查询，递归+记忆化；③ 只求 π(x)，不能推广到其他积性函数前缀和（那用杜教筛/Min_25/PN）；④ 浮点根号误差需整数修正；⑤ 工程模板（如 kactl count_primes）已高度优化，手写易被常数超越。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P5901 | 4 | 素数个数（模板）：求 ≤1e11 素数个数，Meissel-Lehmer/DP 筛模板题 | [https://www.luogu.com.cn/problem/P5901](https://www.luogu.com.cn/problem/P5901) |
| HDU | 5901 Count primes | 5 | Count primes：求 π(1e11) 级素数个数，Meissel-Lehmer 经典题 | [https://acm.hdu.edu.cn/showproblem.php?pid=5901](https://acm.hdu.edu.cn/showproblem.php?pid=5901) |

## Pitfalls · 易错点

- φ 递归终止条件用错导致指数级展开
- x^{1/3}、√x 用浮点算导致边界差 1
- P2 枚举质数对时对 p 的上界/下界（p>p_a）弄错
- pi 查询超表未递归/未记忆化导致递归爆炸
- Möbius 前缀 S₀ 的容斥符号 μ(n) 写错
- 预筛表 N 太小导致频繁触发亚线性递归（常数差）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/number-theory/meissel-lehmer/](https://oi-wiki.org/math/number-theory/meissel-lehmer/)
- 论文 ✓ [https://dl.acm.org/doi/abs/10.1090/s0025-5718-96-00674-6](https://dl.acm.org/doi/abs/10.1090/s0025-5718-96-00674-6)
- 书籍 ✓ `kactl / count_primes 模板（Meissel-Lehmer 工程实现）`
