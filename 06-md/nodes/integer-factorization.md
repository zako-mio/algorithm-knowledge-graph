---
id: integer-factorization
name: 大整数分解
group: G-C-9
stage: advanced
priority: P1
depth_tier: standard
---

# 大整数分解

> 将合数分解为质因子乘积，试除法为基础，大数用 Pollard-Rho，配套约数计数/枚举

<!-- 元信息: id=integer-factorization · group=G-C-9 · stage=advanced · priority=P1 · depth_tier=standard -->

## What · 是什么

整数分解（Integer Factorization）：把正整数 n 写成质因子乘积 n=∏p_i^{e_i}。基础算法是试除法（枚举 2..√n，O(√n)，配合素数表 O(√n/ln n)）；大整数（>1e14）用 Pollard-Rho + Miller-Rabin 组合（期望 O(n^{1/4})）。分解结果可进一步求：约数个数 τ(n)=∏(e_i+1)、约数和、枚举全部约数（DFS 组合因子幂）。分解是数论题的前置工具（约数类、RSA 类、公因数类）。Python 内建大整数便于实现 Pollard-Rho；1e12 内试除法+素数表足够。

## Why · 为什么

### 直觉 · Intuition

因数成对分布：每对 (d, n/d) 必有一个 ≤√n，所以试除法只需试到 √n。就像找钉子——最小的钉子头一定不会超过螺丝杆中间。大整数时 √n 太大（1e30 要试 1e15 次），于是用 Pollard-Rho 的随机轨道在期望 √(最小质因子) 步内‘撞出’一个因子，再用 Miller-Rabin 确认它是不是质数。

### 原理 · Principle

试除法正确性：循环 i 到 i²>n 时，若 n 未除尽必为素数（否则有 ≤√n 因子会整除剩余 n）。带素数表版：筛出 ≤√n 的素数后逐个试除。Pollard-Rho：找非平凡因子 d，递归分解 d 与 n/d，配合 Miller-Rabin 判素终止。约数计数：由唯一分解定理 τ(n)=∏(e_i+1)；枚举约数用 DFS 对每个 p_i 枚举 0..e_i 次幂。复杂度：试除 O(√n)，素数表 O(√n/ln n)，Pollard-Rho 期望 O(n^{1/4})。

### 历史 · History

质因数分解是数论最古老问题之一（欧几里得时代已有试除思想）；其困难性构成 RSA 公钥加密的安全基础（1977）。现代高效分解法含 Pollard-Rho(1975)、椭圆曲线法 ECM、二次筛/数域筛 QS/GNFS。OI 领域常用试除法+Pollard-Rho。CP-Algorithms factorization 页系统给出试除→轮式→素数表→Pollard-Rho 的梯度实现。

## How · 实现

### 伪代码

```python
def trial_division(n):
  res = []
  d = 2
  while d*d <= n:
    while n % d == 0: res.append(d); n //= d
    d += 1
  if n > 1: res.append(n)
  return res
# 素数表版
def trial_division_primes(n, primes):
  res = []
  for p in primes:
    if p*p > n: break
    while n % p == 0: res.append(p); n //= p
  if n > 1: res.append(n)
  return res
# 约数个数
def divisor_count(factors):
  from collections import Counter
  r = 1
  for e in Counter(factors).values(): r *= (e+1)
  return r
# 大数: factor(n) 见 pollard-rho 节点
```

### Python 实现

```python
from math import isqrt
from collections import Counter


def trial_division(n):
    """试除法分解: O(sqrt(n)). 适用于 n <= 1e7 左右."""
    res = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            res.append(d)
            n //= d
        d += 1
    if n > 1:
        res.append(n)
    return res


def trial_division_primes(n, primes):
    """带素数表的试除: O(sqrt(n)/ln n)."""
    res = []
    for p in primes:
        if p * p > n:
            break
        while n % p == 0:
            res.append(p)
            n //= p
    if n > 1:
        res.append(n)
    return res


def sieve_primes(limit):
    is_p = [True] * (limit + 1)
    is_p[0] = is_p[1] = False
    for i in range(2, isqrt(limit) + 1):
        if is_p[i]:
            for j in range(i * i, limit + 1, i):
                is_p[j] = False
    return [i for i in range(2, limit + 1) if is_p[i]]


def divisor_count_from_factors(factors):
    """由质因子列表求约数个数."""
    c = Counter(factors)
    res = 1
    for e in c.values():
        res *= (e + 1)
    return res


def divisors_from_factors(factors):
    """枚举全部约数 (升序)."""
    c = Counter(factors)
    res = [1]
    for p, e in c.items():
        cur = []
        pe = 1
        for _ in range(e + 1):
            for x in res:
                cur.append(x * pe)
            pe *= p
        res = cur
    return sorted(res)


if __name__ == "__main__":
    import random
    random.seed(6)

    def trial_factor(x):
        res = []
        d = 2
        while d * d <= x:
            while x % d == 0:
                res.append(d); x //= d
            d += 1
        if x > 1: res.append(x)
        return res

    # 试除法正确性
    for _ in range(500):
        n = random.randint(2, 10**6)
        assert trial_division(n) == trial_factor(n), n
    assert trial_division(360) == [2, 2, 2, 3, 3, 5]
    assert trial_division(1) == []
    assert divisor_count_from_factors(trial_division(360)) == 24   # 2^3*3^2*5 -> 4*3*2=24
    dvs = divisors_from_factors(trial_division(360))
    assert len(dvs) == 24 and sum(1 for x in range(1, 361) if 360 % x == 0) == 24
    assert sorted(x for x in range(1, 361) if 360 % x == 0) == dvs

    # 素数表试除
    primes = sieve_primes(10000)
    for _ in range(200):
        n = random.randint(2, 10**8)
        assert trial_division_primes(n, primes) == trial_factor(n), n
    print("integer-factorization: all tests passed")

```

**PyPy 提示**: 试除法 while d*d<=n 用乘法而非开方每次，避免浮点误差；d 每次 +1 可优化为只试奇数（处理 2 后 d 从 3 步长 2）。素数表用埃筛一次生成。Pollard-Rho 分解大整数时递归需注意 Python 递归深度（因子少，安全）。大数 1e18 分解实测（见自测）仅需数毫秒。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 试除 O(√n)；素数表 O(√n/ln n)；Pollard-Rho 期望 O(n^{1/4}) |
| 空间 | O(√n)（素数表）或 O(1) |

### 局限

① 试除法在 n>1e12 后不可行；② Pollard-Rho 对‘接近素数平方’（如 n=p²,p 巨大）也慢；③ 无严格最坏界；④ 需配套 Miller-Rabin 否则死循环；⑤ 分解结果含重复因子需用 Counter 合并。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P4718 | 4 | 最大质因子：完整 Pollard-Rho 分解模板 | [https://www.luogu.com.cn/problem/P4718](https://www.luogu.com.cn/problem/P4718) |
| Luogu | P1075 | 2 | 质因数分解入门：两个大质数之积的分解 | [https://www.luogu.com.cn/problem/P1075](https://www.luogu.com.cn/problem/P1075) |
| Luogu | P1072 | 3 | Hankson 的趣味题：分解质因数 + 约数枚举/计数 | [https://www.luogu.com.cn/problem/P1072](https://www.luogu.com.cn/problem/P1072) |

## Pitfalls · 易错点

- 试除到 i*i<=n 用 int 截断导致溢出（Python 无此问题但浮点 sqrt 有误差）
- 素数表试除时没在 p*p>n 处 break，浪费且可能越界
- 分解完 n 剩余 >1 忘加入结果（它就是最后一个质因子）
- Pollard-Rho 对素性判断缺失死循环
- 约数计数把指数直接相乘而非 (e+1)
- 结果未排序/去重导致比较与预期不一致

## Sources · 信源

- CP-Algorithms ✓ [https://cp-algorithms.com/algebra/factorization.html](https://cp-algorithms.com/algebra/factorization.html)
- OI Wiki ✓ [https://oi-wiki.org/math/number-theory/pollard-rho/](https://oi-wiki.org/math/number-theory/pollard-rho/)
- article ✓ [https://en.wikipedia.org/wiki/Integer_factorization](https://en.wikipedia.org/wiki/Integer_factorization)
