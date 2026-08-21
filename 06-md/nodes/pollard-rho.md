---
id: pollard-rho
name: Pollard–Rho 大整数分解
group: G-C-9
stage: advanced
priority: P1
depth_tier: standard
---

# Pollard–Rho 大整数分解

> 期望 O(n^{1/4}) 找合数非平凡因子，生日悖论+伪随机序列环检测，配 Miller-Rabin 递归分解

<!-- 元信息: id=pollard-rho · group=G-C-9 · stage=advanced · priority=P1 · depth_tier=standard -->

## What · 是什么

Pollard–Rho 是随机化的大整数分解算法，用于快速找到一个合数 N 的非平凡因子（不一定是质因子）。核心：用伪随机序列 x_{i+1}=f(x_i)=(x_i²+c) mod N，观察序列模 N 的最小质因子 p 上会出现环（生日悖论：模 p 的重复期望 O(√p) 次迭代）；一旦 x_i≡x_j (mod p)，则 gcd(|x_i-x_j|,N) 是 N 的非平凡因子。用 Floyd 或 Brent 判环检测重复，配合倍增累积减少 gcd 次数。期望 O(N^{1/4})。实际使用中常与 Miller-Rabin 配合：先判素（是素直接返回），否则 Pollard-Rho 找一个因子 d 再递归分解 d 与 N/d。完整大整数分解（如 RSA 模数 2^128 内的数）是 OI/密码学/CTF 的基础工具。

## Why · 为什么

### 直觉 · Intuition

在 [2,√N] 中随机猜因子概率太小。但生日悖论告诉我们：随机往 p 个桶里丢球，约 √p 次就会出现重复。我们对最小质因子 p 做‘伪随机模 p 轨道’，轨道一旦闭合就抓到 p 的‘指纹’（x_i-x_j 被 p 整除），再通过 gcd 把 p 从 N 里抠出来。序列长得像希腊字母 ρ（先绕圈再入环），因此叫 rho。

### 原理 · Principle

对合数 N，取最小质因子 p。迭代 f 模 N 的序列在模 p 下是自映射（若 x≡y mod p 则 f(x)≡f(y) mod p），模 p 轨道期望 O(√p) 步重复。Floyd 判环：双指针 a,b 分别每次走 1/2 步，直到同点。Brent 判环：倍增步长，平均调用 f 更少（比 Floyd 快 ~24%）。倍增优化：把若干个 |x_i-x_j| 乘起来一次性 gcd，减少 gcd 次数（gcd 是瓶颈），k 取 128 左右。若 gcd=N 表示整体模 N 成环，换 c 重试。边界：N 是素数会死循环（先用 Miller-Rabin 排除）；N=4 等需特判。期望复杂度 O(√p)=O(N^{1/4})。

### 历史 · History

John Pollard 1975 年提出（论文 “A Monte Carlo method for factorization”），1978 年 Brent 改进为 Brent 判环。生日悖论思想的应用典范。与 Miller-Rabin 组合是 RSA 分解、离散对数等数论问题在 OI/密码学中的标配。OI Wiki《Pollard-Rho 算法》页与 CP-Algorithms factorization 页均给出完整实现。

## How · 实现

### 伪代码

```python
def pollard_rho(n):
  if n%2==0: return 2
  while True:
    c = randint(1, n-1)
    y = randint(0, n-1); r = 1; q = 1; g = 1; m = 128
    while g == 1:
      x = y
      for _ in range(r): y = f(y,c,n)
      k = 0
      while k < r and g == 1:
        ys = y
        for _ in range(min(m, r-k)):
          y = f(y,c,n); q = q*abs(x-y) % n
        g = gcd(q, n); k += m
      r <<= 1
    if g == n:   # 回退逐个检查
      g = 1
      while g == 1:
        ys = f(ys,c,n); g = gcd(abs(x-ys), n)
      if g == n: continue
    return g

def factor(n):
  if is_prime(n): return [n]
  d = pollard_rho(n)
  return factor(d) + factor(n//d)
```

### Python 实现

```python
import random
from math import gcd
import random


def is_prime_mr(n, bases=None):
    """Miller-Rabin 素性测试.
    - bases=None 时使用确定性基底: [2,325,9375,28178,450775,9780504,1795265022],
      对 < 2^64 的所有整数确定性正确.
    - bases 可传入自定义基底列表 (如随机基底做概率测试).
    小整数直接试除/特判."""
    if n < 2: return False
    small = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for p in small:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    if bases is None:
        bases = [2, 325, 9375, 28178, 450775, 9780504, 1795265022]
    for a in bases:
        a %= n
        if a == 0:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        ok = False
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                ok = True
                break
        if not ok:
            return False
    return True




def _f(x, c, n):
    return (x * x + c) % n


def pollard_rho(n, seed=None):
    """Pollard-Rho: 返回 n 的一个非平凡因子 (n 为合数). 期望 O(n^{1/4}).
    使用 Brent 判环 + 倍增 gcd 累积优化. 可能失败返回 n (需换 c 重试)."""
    if n % 2 == 0: return 2
    if n % 3 == 0: return 3
    if seed is not None:
        random.seed(seed)
    while True:
        c = random.randint(1, n - 1)
        y, r, q = random.randint(0, n - 1), 1, 1
        g = 1
        m = 128
        while g == 1:
            x = y
            for _ in range(r):
                y = _f(y, c, n)
            k = 0
            while k < r and g == 1:
                ys = y
                for _ in range(min(m, r - k)):
                    y = _f(y, c, n)
                    q = q * abs(x - y) % n
                g = gcd(q, n)
                k += m
            r <<= 1
        if g == n:
            # 回退逐个检查 (Brent 经典做法)
            g = 1
            while g == 1:
                ys = _f(ys, c, n)
                g = gcd(abs(x - ys), n)
            if g == n:
                continue   # 换 c 重试
        return g


def factor(n, trials=8):
    """完整分解 n, 返回 (质因子列表, 含重复). 递归 Miller-Rabin + Pollard-Rho."""
    factors = []
    def rec(m):
        if m == 1: return
        if is_prime_mr(m):
            factors.append(m)
            return
        for _ in range(trials):
            d = pollard_rho(m)
            if 1 < d < m:
                rec(d)
                rec(m // d)
                return
        # 极端情况: 换随机种子再试
        d = pollard_rho(m, seed=random.randint(1, 10**9))
        rec(d)
        rec(m // d)
    rec(n)
    factors.sort()
    return factors


def factor_counter(n):
    """返回 {质因子: 次数}."""
    from collections import Counter
    return dict(Counter(factor(n)))


if __name__ == "__main__":
    import time
    # 小因子快速检验
    assert factor(48) == [2, 2, 2, 2, 3]
    assert factor(100) == [2, 2, 5, 5]
    assert factor(9973) == [9973]
    assert factor(2**20) == [2] * 20

    # 确定性随机验证 (与试除法对比)
    def trial_factor(x):
        res = []
        d = 2
        while d * d <= x:
            while x % d == 0:
                res.append(d)
                x //= d
            d += 1
        if x > 1: res.append(x)
        return res

    import random
    random.seed(888)
    for _ in range(400):
        n = random.randint(2, 10**9)
        got = factor(n)
        assert got == trial_factor(n), (n, got, trial_factor(n))

    # 大整数: 两个 10^9 量级素数之积 (~10^18, 超出 2^64)
    p = 1000000007
    q = 1000000009
    n = p * q
    t0 = time.time()
    fs = factor(n)
    dt = time.time() - t0
    assert sorted(fs) == sorted([p, q]), fs
    print(f"factor({p}*{q}) -> {fs} in {dt:.3f}s")

    # 三次方与大质因子混合
    n2 = 2**31 - 1   # 2147483647 是梅森素数
    assert factor(n2) == [n2]
    n3 = (2**31 - 1) * 3 * 3
    assert factor(n3) == [3, 3, 2147483647]
    print("pollard-rho: all tests passed")

```

**PyPy 提示**: 乘法和取模用内建，\|x-y\| 用 abs 避免大数符号问题。gcd 用 math.gcd（C 实现）。随机 c 失败时换 c 重试，不要无限循环。递归 factor 深度 ≤ 因子数。对 2^64 内整数 Python 大整数无溢出问题；更大数建议用 gmpy2（is_prime/pow/gcd 加速 5-50x）。Brent+倍增实现中 m=128 是常见调优值。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 期望 O(N^{1/4})（单因子）；完整分解需递归 × 因子个数 |
| 空间 | O(1)（递归栈 O(因子数)） |

### 局限

① 对素数无效（需 Miller-Rabin 前置）；② 极端坏数据（多重小因子/全同因子如 2^64）可能多次失败换 c，但仍快；③ 概率算法无严格最坏上界；④ 大整数（>2^128）Python 原生慢，需 gmpy2；⑤ 找出的因子是非平凡因子而非质因子，需递归分解。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P4718 | 4 | 【模板】Pollard-Rho 算法：Miller-Rabin + Pollard-Rho 求最大质因子，OI Wiki 模板 | [https://www.luogu.com.cn/problem/P4718](https://www.luogu.com.cn/problem/P4718) |
| Luogu | P1075 | 2 | 质因数分解：小数据试除即可，验证分解正确性 | [https://www.luogu.com.cn/problem/P1075](https://www.luogu.com.cn/problem/P1075) |
| CP-Algorithms | Integer factorization | 3 | factorization 页：试除/轮式/Floyd/Brent 全套实现 | [https://cp-algorithms.com/algebra/factorization.html](https://cp-algorithms.com/algebra/factorization.html) |

## Pitfalls · 易错点

- 忘记对素数/小整数做前置 Miller-Rabin 与特判，导致死循环
- N=4 时 Floyd 两步特判（先跳两步再判环）
- gcd==N 时未换 c 重试而是当成因子返回
- Brent 实现中 q 未重置/未在正确时机检查 gcd
- 用整除代替 gcd 判断（N 太大不可行）
- 递归 factor 对 1 未处理导致无限递归

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/number-theory/pollard-rho/](https://oi-wiki.org/math/number-theory/pollard-rho/)
- CP-Algorithms ✓ [https://cp-algorithms.com/algebra/factorization.html](https://cp-algorithms.com/algebra/factorization.html)
- 论文 ✓ [https://doi.org/10.1007/BF01933190](https://doi.org/10.1007/BF01933190)
