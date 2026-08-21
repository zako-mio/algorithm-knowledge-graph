---
id: euler-totient
name: 欧拉函数
group: G-C-7
stage: intermediate
priority: P0
depth_tier: deep
---

# 欧拉函数

> phi(n)表示1~n中与n互素的数个数，积性函数，欧拉定理基础

<!-- 元信息: id=euler-totient · group=G-C-7 · stage=intermediate · priority=P0 · depth_tier=deep -->

## What · 是什么

欧拉函数（Euler's totient function）φ(n) 表示 1 到 n 中与 n 互素的正整数个数。核心公式 φ(n)=n·∏(1-1/p_i)（p_i 是 n 的相异质因子）。它是积性函数，可在线性筛中 O(n) 预处理全部 φ(1..n)。欧拉定理：gcd(a,m)=1 时 a^φ(m)≡1 (mod m)，是费马小定理的推广，也是模逆元与指数降幂的理论基础。

## Why · 为什么

### 直觉 · Intuition

在 1..n 中统计与 n 互素的数：先假设全部 n 个都互素，然后剔除含质因子 p 的倍数（占 1/p），被多个质因子重复剔除的用容斥修正，最终得到 n·(1-1/p1)·(1-1/p2)·...。对质数 p 有 φ(p)=p-1；对 p^k 有 φ(p^k)=p^k-p^(k-1)。

### 原理 · Principle

积性：gcd(a,b)=1 时 φ(ab)=φ(a)φ(b)。由唯一分解定理结合积性与素数幂公式推得 φ(n)=n·∏(1-1/p_i)。欧拉定理证明基于简化剩余系的乘法封闭性：{a·x mod m | gcd(x,m)=1} 仍遍历全部 φ(m) 个剩余类，乘积相等得 a^φ(m)≡1。线性筛求 φ：i%p==0 时 φ[i·p]=φ[i]·p；互质时 φ[i·p]=φ[i]·(p-1)。

### 历史 · History

欧拉函数得名于莱昂哈德·欧拉，他于 18 世纪研究了与 n 互素的数计数问题并证明欧拉定理（费马小定理的推广）。它深入参与数论结构（单位群、循环群、原根）、密码学（RSA 中计算 φ(n)）与竞赛数论（欧拉反演、莫比乌斯反演前置）。OI Wiki 与 CP-Algorithms 均专章讲解。

## How · 实现

### 伪代码

```python
# 单个数 O(sqrt n) 质因数分解法
def phi(n):
  res = n
  for i in 2..isqrt(n):
    if n % i == 0:
      res = res // i * (i - 1)
      while n % i == 0: n //= i
  if n > 1: res = res // n * (n - 1)
  return res

# 线性筛预处理 1..n 的 phi
phi[1]=1
for i in 2..n:
  if not not_prime[i]: pri.append(i); phi[i]=i-1
  for p in pri:
    if i*p>n: break
    not_prime[i*p]=true
    if i % p == 0: phi[i*p]=phi[i]*p; break
    else: phi[i*p]=phi[i]*(p-1)
```

### Python 实现

```python
from math import isqrt, gcd


def phi_single(n):
    """O(sqrt n) 求单个欧拉函数值"""
    res = n
    i = 2
    while i * i <= n:
        if n % i == 0:
            res = res // i * (i - 1)
            while n % i == 0:
                n //= i
        i += 1
    if n > 1:
        res = res // n * (n - 1)
    return res


def phi_table_linear(n):
    """线性筛预处理 1..n 的欧拉函数，返回 (phi, pri)"""
    pri = []
    not_prime = [False] * (n + 1)
    phi = [0] * (n + 1)
    phi[1] = 1
    for i in range(2, n + 1):
        if not not_prime[i]:
            pri.append(i)
            phi[i] = i - 1
        for p in pri:
            if i * p > n:
                break
            not_prime[i * p] = True
            if i % p == 0:
                phi[i * p] = phi[i] * p
                break
            phi[i * p] = phi[i] * (p - 1)
    return phi, pri


def euler_theorem_pow(a, b, m):
    """欧拉定理降幂: a^b mod m。
    当 gcd(a,m)=1 时 a^b ≡ a^(b mod phi(m))。
    """
    if gcd(a, m) == 1:
        return pow(a, b % phi_single(m), m)
    # 非互素时需用扩展欧拉定理（此处演示仅互素情形）
    return pow(a, b, m)


if __name__ == "__main__":
    # 已知值
    assert phi_single(1) == 1
    assert phi_single(2) == 1
    assert phi_single(12) == 4      # 1,5,7,11
    assert phi_single(9) == 6       # 1,2,4,5,7,8
    assert phi_single(7) == 6
    assert phi_single(36) == 12
    assert phi_single(97) == 96

    # 暴力交叉验证
    def phi_brute(x):
        return sum(1 for k in range(1, x + 1) if gcd(k, x) == 1)
    for x in range(1, 200):
        assert phi_single(x) == phi_brute(x), x

    phi_tab, pri = phi_table_linear(200)
    for x in range(1, 200):
        assert phi_tab[x] == phi_brute(x), x

    # 欧拉定理验证
    assert euler_theorem_pow(2, 100, 9) == pow(2, 100 % phi_single(9), 9)
    assert pow(3, phi_single(14), 14) == 1  # gcd(3,14)=1

    # n = sum_{d|n} phi(d) 性质
    for n in [1, 2, 12, 30, 100]:
        total = sum(phi_single(d) for d in range(1, n + 1) if n % d == 0)
        assert total == n, (n, total)

    print("All tests passed.")
```

**PyPy 提示**: 单个数 O(sqrt n) 的 phi 在 n≤1e12 时可接受（约 1e6 次循环），n 更大需 Pollard-Rho。批量用线性筛 O(n)，PyPy 下 n=1e7 约 1.5s。欧拉定理降幂时 phi_single 只调一次，注意 m 很大时 phi 计算本身成为瓶颈。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 单个数 O(sqrt n)；批量线性筛 O(n)；欧拉定理降幂 O(log b + sqrt m) |
| 空间 | 单个数 O(1)；批量 O(n) |

### 局限

φ(n) 对合数模不保证 b 次幂直接降幂正确（需扩展欧拉定理分段处理）。质因数分解大数是瓶颈（Pollard-Rho）。欧拉函数值与质因子分布相关，不能从 φ(n) 直接反推 n 的分解（仅当知道因子结构时可还原）。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P2158 | 4 | 仪仗队：可视线计数 = 1 + sum_{i=2}^n φ(i)，线性筛预处理欧拉函数 | [https://www.luogu.com.cn/problem/P2158](https://www.luogu.com.cn/problem/P2158) |
| Luogu | P2398 | 5 | GCD SUM：欧拉反演 gcd(i,j)=sum_{d\|i,d\|j}φ(d)，OI Wiki 官方例题 | [https://www.luogu.com.cn/problem/P2398](https://www.luogu.com.cn/problem/P2398) |
| SPOJ | ETF | 3 | Euler Totient Function：多组查询单个 φ(n)，质因数分解求法 | [https://www.spoj.com/problems/ETF/](https://www.spoj.com/problems/ETF/) |
| Luogu | P2568 | 6 | GCD：线性筛欧拉函数前缀和，sum gcd(i,j)=素数 | [https://www.luogu.com.cn/problem/P2568](https://www.luogu.com.cn/problem/P2568) |

## Pitfalls · 易错点

- 质因数分解时 while 循环去除重复因子后忘记处理 n>1 的剩余大质因子
- res = res // i * (i-1) 与 res = res * (i-1) // i 的取整顺序（先除后乘防溢出）
- 线性筛求 phi 时 i%p==0 分支用错公式（应乘 p 而非 p-1）
- phi[1]=1 漏初始化
- 欧拉定理只对 gcd(a,m)=1 成立，其他情形需扩展欧拉定理

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/number-theory/euler-totient/](https://oi-wiki.org/math/number-theory/euler-totient/)
- CP-Algorithms ✓ [https://cp-algorithms.com/algebra/phi-function.html](https://cp-algorithms.com/algebra/phi-function.html)
- 书籍 ✓ `CPH ch21 Number theory (p207-216)`
