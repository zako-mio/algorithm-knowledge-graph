---
id: sieve-linear
name: 线性筛(欧拉筛)
group: G-C-7
stage: intermediate
priority: P0
depth_tier: deep
---

# 线性筛(欧拉筛)

> O(n)筛素数，每个合数只被最小质因子筛一次，可同时求积性函数

<!-- 元信息: id=sieve-linear · group=G-C-7 · stage=intermediate · priority=P0 · depth_tier=deep -->

## What · 是什么

线性筛（Linear Sieve / Euler Sieve）保证每个合数只被它的最小质因子筛掉一次，从而总时间复杂度严格 O(n)。与埃氏筛（一个合数被多个质因子重复标记）相比，线性筛在 O(n) 内同时求出每个数的最小质因子，并可在筛的过程中顺带计算各种积性函数（欧拉函数 phi、莫比乌斯函数 mu、约数个数 d、约数和 sigma 等），是数论中最高效、最常用的筛法。

## Why · 为什么

### 直觉 · Intuition

埃氏筛浪费在对 12=2×2×3 既被 2 划又被 3 划。线性筛规定「只允许最小的质因子来划掉一个合数」：每个合数 n 只由 n/min_prime × min_prime 产生，且当内层质数 p 已经是 i 的最小质因子（i%p==0）时立即 break，防止更大的质数再来划 n。这样每个数恰被标记一次。

### 原理 · Principle

外层 i 从 2 到 n：若 i 未被标记则加入素数表；随后用素数表里的每个 p 标记 i×p（p≤i 的最小质因子）：若 i%p==0，标记后 break（因为更大的 p' 的 i×p' 会由 (i×p')/(p') 这个更小的数乘上其最小质因子 p' 标记）。标记的同时维护积性函数：i%p==0 时 f[i×p]=f[i]×p 类公式，否则 f[i×p]=f[i]×f[p]。

### 历史 · History

线性筛由计算机科学家在 20 世纪中期系统化（常归功于对埃氏筛的优化探索），在中国算法圈常称「欧拉筛」。其同时求最小质因子与积性函数的能力使它在 MO 数论（莫比乌斯反演、欧拉函数前缀和）中成为标准预处理工具。OI Wiki 与 CP-Algorithms 均给出详细实现与正确性证明。

## How · 实现

### 伪代码

```python
pri = []; not_prime[0..n] = false; phi[0..n] = 0
for i = 2..n:
  if not not_prime[i]:
    pri.append(i); phi[i] = i-1
  for p in pri:
    if i*p > n: break
    not_prime[i*p] = true
    if i % p == 0:
      phi[i*p] = phi[i] * p     # p 已是最小质因子
      break
    else:
      phi[i*p] = phi[i] * (p-1) # 互质, 积性
```

### Python 实现

```python
def linear_sieve_phi(n):
    """线性筛: 同时求出素数表 pri 和欧拉函数 phi[1..n]"""
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
    return pri, phi


def linear_sieve_mu(n):
    """线性筛莫比乌斯函数 mu"""
    pri = []
    not_prime = [False] * (n + 1)
    mu = [0] * (n + 1)
    mu[1] = 1
    for i in range(2, n + 1):
        if not not_prime[i]:
            pri.append(i)
            mu[i] = -1
        for p in pri:
            if i * p > n:
                break
            not_prime[i * p] = True
            if i % p == 0:
                mu[i * p] = 0
                break
            mu[i * p] = -mu[i]
    return pri, mu


def is_prime_simple(x, pri):
    """用素数表判断 x 是否为素数（x 较小）"""
    import math
    if x < 2:
        return False
    for p in pri:
        if p * p > x:
            break
        if x % p == 0:
            return x == p
    return True


if __name__ == "__main__":
    pri, phi = linear_sieve_phi(100)
    assert pri[:10] == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    assert 97 in pri
    assert 91 not in pri
    # 欧拉函数已知值: phi(12)=4, phi(9)=6, phi(1)=1, phi(97)=96
    assert phi[12] == 4
    assert phi[9] == 6
    assert phi[1] == 1
    assert phi[97] == 96

    # 与埃氏筛交叉验证素数集合（用 n=500 重跑一遍线性筛）
    pri500, _ = linear_sieve_phi(500)
    from math import isqrt
    n = 500
    s = [True] * (n + 1)
    s[0] = s[1] = False
    for i in range(2, isqrt(n) + 1):
        if s[i]:
            for j in range(i * i, n + 1, i):
                s[j] = False
    expected = {i for i in range(2, n + 1) if s[i]}
    assert set(pri500) == expected

    # 暴力验证欧拉函数
    def phi_brute(x):
        return sum(1 for k in range(1, x + 1) if __import__('math').gcd(k, x) == 1)
    for x in range(1, 50):
        assert phi[x] == phi_brute(x), (x, phi[x], phi_brute(x))

    print("All tests passed.")
```

**PyPy 提示**: PyPy 下线性筛 n=1e7 约 1-2s，与埃氏筛相当但还附带积性函数表。Python 内层 for p in pri 的 Python 级循环是瓶颈（比 C 慢），n>1e7 时建议用字节级优化或 numpy 向量化（若 OJ 允许）。mu 数组仅需 int 小值，可用 array('b') 省内存。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n) — 每个合数恰被最小质因子筛一次 |
| 空间 | O(n) — 素数表 + not_prime + 函数表 |

### 局限

Python 的线性筛常数较大（内层 Python 循环），n 超 1e8 时仍会超时/超内存；此时应寻求数论分块+杜教筛等亚线性方法。线性筛需要至少一个积性函数需要维护时才有优势，纯筛素数时埃氏筛+位压缩常数更小。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3383 | 3 | 【模板】线性筛素数：线性筛/埃氏筛均可，检验基础实现 | [https://www.luogu.com.cn/problem/P3383](https://www.luogu.com.cn/problem/P3383) |
| Luogu | P2568 | 6 | GCD：线性筛预处理欧拉函数前缀和求 sum gcd=素数 的对数 | [https://www.luogu.com.cn/problem/P2568](https://www.luogu.com.cn/problem/P2568) |
| Luogu | P2158 | 4 | 仪仗队：线性筛欧拉函数求和，互素对数计数 | [https://www.luogu.com.cn/problem/P2158](https://www.luogu.com.cn/problem/P2158) |

## Pitfalls · 易错点

- 忘记在内层 if i%p==0 时 break，导致合数被重复标记（退化为非线性）
- break 条件写反（i%p!=0 时 break），产生漏筛
- i*p 可能溢出 int（Python 无此问题，但乘法仍要趁早判断 >n 再 break）
- 维护积性函数时分不清 i%p==0 与互质两分支的公式
- phi[1]=1 漏初始化导致后续累加错位

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/number-theory/sieve/](https://oi-wiki.org/math/number-theory/sieve/)
- CP-Algorithms ✓ [https://cp-algorithms.com/algebra/prime-sieve-linear.html](https://cp-algorithms.com/algebra/prime-sieve-linear.html)
- 书籍 ✓ `CPH ch21 Number theory (p207-216)`
