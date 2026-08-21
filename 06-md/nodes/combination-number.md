---
id: combination-number
name: 组合数
group: G-C-10
stage: basic
priority: P0
depth_tier: deep
---

# 组合数

> C(n,m) 计算：杨辉递推/阶乘逆元预处理/Lucas，竞赛计数核心

<!-- 元信息: id=combination-number · group=G-C-10 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

组合数 C(n,m)（二项式系数）表示从 n 个不同元素取 m 个元素的方案数，公式 C(n,m)=n!/(m!(n-m)!)，规定 m>n 时为 0。竞赛中的计算方式分档：①杨辉三角递推 C(n,m)=C(n-1,m-1)+C(n-1,m)，O(n^2) 预处理任意模数，适合 n<=5000；②阶乘+逆元：预处理阶乘与逆元阶乘 O(n)，查询 O(1)，要求模数为质数且 n<mod（费马小定理求逆）；③Lucas 定理：n,m 很大而模数为小质数 p 时，C(n,m) ≡ C(n/p,m/p)·C(n%p,m%p) (mod p)，复杂度 O(p + log_p n)；④大质数幂/任意模数用 exLucas 或质因数分解+CRT。插板法（星条）是其最常用的组合恒等式应用。

## Why · 为什么

### 直觉 · Intuition

直接算 n!/(m!(n-m)!) 会爆整数且慢。观察到递推式 C(n,m)=C(n-1,m)+C(n-1,m-1) 与杨辉三角一致——于是先铺一张三角表 O(n^2)，之后任意查。在模质数 p 下，n! 的逆元可用 (n!)^{-1}=((n+1)!)^{-1}·(n+1) 反向推得，配合阶乘表做到 O(1) 单点查询。Lucas 的直觉：把 n,m 写成 p 进制，每一位上分别取组合数再相乘——把「大数取模组合数」拆成「小范围组合数」。

### 原理 · Principle

预处理：fac[i]=i! mod p；ifac[n]=pow(fac[n], p-2, p)；反向 ifac[i]=ifac[i+1]*(i+1) mod p。查询 C(n,m)=fac[n]*ifac[m]*ifac[n-m] mod p，要求 m<=n< p。Lucas：若 n<m 返回 0；否则 C(n,m)=C(n//p,m//p)*C(n%p,m%p) mod p，递归或迭代；需预处理 0..p-1 的阶乘。杨辉递推任意模数（只做加法），但空间 O(n^2)。常用恒等式：C(n,0)+..+C(n,n)=2^n；C(n,k)=C(n,n-k)；范德蒙德恒等式 ΣC(n,i)C(m,k-i)=C(n+m,k)；朱世杰 Σ_{i=k}^n C(i,k)=C(n+1,k+1)；C(n,k)=n/k·C(n-1,k-1)。插板法：x1+..+xk=n 的正整数解 C(n-1,k-1)、非负解 C(n+k-1,k-1)。

### 历史 · History

组合数研究历史悠久（13 世纪杨辉三角、帕斯卡 17 世纪形式化），二项式定理由牛顿推广到非自然数指数。CP-Algorithms 的 binomial-coefficients 页系统给出杨辉三角、模大质数（阶乘逆元）、模质数幂（p 因子拆分 g/c）、任意模数（CRT）、大 n 小模数（Lucas）等全套方法；OI Wiki 的 combination 页覆盖定义/插板法/恒等式/二项式反演。两源交叉一致。

## How · 实现

### 伪代码

```python
预处理(模质数p, n<=N):
  fac[0]=1; for i=1..N: fac[i]=fac[i-1]*i%p
  ifac[N]=pow(fac[N], p-2, p)
  for i=N..1: ifac[i-1]=ifac[i]*i%p
查询 C(n,m): m<0或m>n 返回0; 否则 fac[n]*ifac[m]%p*ifac[n-m]%p
Lucas(n,m,p): n<m -> 0; 否则 C(n%p,m%p)*Lucas(n//p,m//p,p)%p
杨辉(任意模): C[i][j]=C[i-1][j-1]+C[i-1][j]
```

### Python 实现

```python
import sys

MOD = 10 ** 9 + 7


def precompute(n, mod=MOD):
    fac = [1] * (n + 1)
    for i in range(1, n + 1):
        fac[i] = fac[i - 1] * i % mod
    ifac = [1] * (n + 1)
    ifac[n] = pow(fac[n], mod - 2, mod)
    for i in range(n, 0, -1):
        ifac[i - 1] = ifac[i] * i % mod
    return fac, ifac


def comb_fact(n, m, fac, ifac, mod=MOD):
    if m < 0 or m > n:
        return 0
    return fac[n] * ifac[m] % mod * ifac[n - m] % mod


def comb_pascal(n, m):
    # O(min(m, n-m)) 直接算（n 较小、单次查询时）
    if m < 0 or m > n:
        return 0
    m = min(m, n - m)
    num = den = 1
    for i in range(1, m + 1):
        num = num * (n - i + 1) // i
    return num


def lucas(n, m, p, fac_p):
    # fac_p 为模 p 下 0..p-1 的阶乘表；p 为质数
    def small_comb(a, b):
        if b < 0 or b > a:
            return 0
        return fac_p[a] * pow(fac_p[b], p - 2, p) % p * pow(fac_p[a - b], p - 2, p) % p

    if m == 0:
        return 1
    if n % p < m % p:
        return 0
    return small_comb(n % p, m % p) * lucas(n // p, m // p, p, fac_p) % p


def main():
    N = 200000
    fac, ifac = precompute(N)
    # 校验: C(10,3)=120, C(10,7)=120, C(10,0)=1, C(10,11)=0
    assert comb_fact(10, 3, fac, ifac) == 120
    assert comb_fact(10, 7, fac, ifac) == 120
    assert comb_fact(10, 0, fac, ifac) == 1
    assert comb_fact(10, 11, fac, ifac) == 0
    assert comb_pascal(10, 3) == 120
    # Lucas: p=1000000007 大质数时 Lucas 退化为普通公式
    fac7 = [1] * 7
    for i in range(1, 7):
        fac7[i] = fac7[i - 1] * i % 7
    assert lucas(13, 5, 7, fac7) == 6  # C(13,5)=1287, 1287 % 7 = 6
    print("comb_fact C(10,3)=", comb_fact(10, 3, fac, ifac))
    print("comb_pascal C(10,3)=", comb_pascal(10, 3))
    print("Lucas C(13,5) mod 7 =", lucas(13, 5, 7, fac7))
    # 插板法：x+y+z=10 非负解数 = C(12,2)=66
    assert comb_fact(12, 2, fac, ifac) == 66
    print("OK")


if __name__ == "__main__":
    main()

```

**PyPy 提示**: 预计算 O(n) 阶乘逆元在 PyPy 下快；pow(..., mod-2, mod) 幂运算是唯一大开销但 O(log mod) 可接受。Lucas 递归深度 O(log_p n) 很小。多组查询复用预计算的 fac/ifac 表。若模数非质数，需 exLucas（质因数分解+CRT）。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 杨辉 O(n^2) 预处理 O(1) 查询；阶乘逆元 O(n) 预处理 O(1) 查询；Lucas O(p) 预处理(小阶乘表)+O(log_p n) 查询；直接公式单点 O(min(m,n-m)) |
| 空间 | 杨辉 O(n^2)；阶乘逆元 O(n) |

### 局限

阶乘逆元法要求 mod 为质数且 n<mod（否则阶乘含 mod 因子不可逆）；Lucas 仅适用于质数模数；杨辉表空间大仅限 n<=~5000。任意模数需 exLucas/质数幂拆分+CRT。Python 大数据（n 达 1e7）预计算 O(n) 内存 ~80MB 需注意。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P2822 | 4 | 组合数问题：杨辉递推 + 二维前缀和统计 C(n,m)%k==0 的个数 | [https://www.luogu.com.cn/problem/P2822](https://www.luogu.com.cn/problem/P2822) |
| Luogu | P3807 | 3 | 【模板】卢卡斯定理：大 n 小质数模数下求组合数 | [https://www.luogu.com.cn/problem/P3807](https://www.luogu.com.cn/problem/P3807) |
| AtCoder | ABC156 D | 3 | Bouquet：2^n - C(n,a) - C(n,b) 组合数求与应用 | [https://atcoder.jp/contests/abc156/tasks/abc156_d](https://atcoder.jp/contests/abc156/tasks/abc156_d) |
| Codeforces | 1716C | 1700 | 组合计数与 DP 结合的典型：先选组合再分配 | [https://codeforces.com/contest/1716/problem/C](https://codeforces.com/contest/1716/problem/C) |

## Pitfalls · 易错点

- 忘记特判 m<0 或 m>n 直接返回 0（数组越界/答案错）
- 阶乘逆元法在 n>=mod 时阶乘含 mod 因子，逆元不存在，必须换 Lucas
- Lucas 中 n%p < m%p 时直接返回 0（每位组合数有 0 则整体 0）
- 预计算表越界：组合查询 n 超过预计算上限
- 杨辉递推用 int 溢出（未取模时）；取模运算中减法结果变负需 +mod
- 幂运算 pow(x, p-2, p) 忘记 mod 三参形式，直接 pow 会爆

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/combinatorics/combination/](https://oi-wiki.org/math/combinatorics/combination/)
- oiwiki_raw ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/combinatorics/combination.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/combinatorics/combination.md)
- CP-Algorithms ✓ [https://cp-algorithms.com/combinatorics/binomial-coefficients.html](https://cp-algorithms.com/combinatorics/binomial-coefficients.html)
- 书籍 ✓ `CPH ch22 Combinatorics (p217-226)`
