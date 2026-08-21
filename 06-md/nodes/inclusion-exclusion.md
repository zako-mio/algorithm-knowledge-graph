---
id: inclusion-exclusion
name: 容斥原理
group: G-C-11
stage: intermediate
priority: P1
depth_tier: standard
---

# 容斥原理

> \|A1∪A2∪...\|=sum(-1)^k S(k)，多集合并集计数与莫比乌斯反演基础

<!-- 元信息: id=inclusion-exclusion · group=G-C-11 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

容斥原理（Inclusion-Exclusion）：对有限集族 {S_i}，|∪S_i|=Σ_{m>=1}(-1)^{m-1}Σ|∩_{选 m 个}S_i|。每个元素恰好被计 1 次（由二项式定理证明）。推论：交集 |∩S_i|=|U|-|∪补集|；一般化：若 f(S)=Σ_{T⊆S}g(T) 则 g(S)=Σ_{T⊆S}(-1)^{|S|-|T|}f(T)（子集反演），其数论版本即莫比乌斯反演。应用：不定方程带上下界计数（插板+容斥）、错排 D_n=n!Σ(-1)^i/i!、数论中 gcd=k 数对计数（倍数容斥，倒推）、欧拉函数公式推导、min-max 容斥（期望版）、染色/排列禁忌位置计数等。

## Why · 为什么

### 直觉 · Intuition

先全都要(并集), 但加多了要减, 减多了要加, 交替进行——'容'与'斥'。每个元素属于 m 个集合, 贡献 ΣC(m,i)(-1)^{i-1}=1, 恰好一次。

### 原理 · Principle

元素 x 出现在 m 个 S_i 中, 被计数次数=Σ_{i=1}^m C(m,i)(-1)^{i-1}=1-(1-1)^m=1。补集形式把'至少满足'转成'全不满足'。子集反演 g(S)=Σ(-1)^{|S|-|T|}f(T) 是组合莫比乌斯反演; 数论取整除偏序即为 μ 反演。min-max 容斥把 max 表达成各子集 min 的交替和, 因期望线性成立 E[max]=Σ(-1)^{|T|-1}E[min]。

### 历史 · History

容斥原理由 De Moivre 与 Poisson 等 18-19 世纪数学家系统化, 是组合计数的基础工具。OI Wiki 的 inclusion-exclusion 页面与 CP-Algorithms 的 inclusion-exclusion 页面均收录并给出错排、数论、min-max 等应用, 后者还有 UVA/SPOJ/TopCoder 练习列表。

## How · 实现

### 伪代码

```python
# 模板: 求满足全部限制的计数
全集 = 无限制的计数方案
def f(mask):  # 对 mask 内限制'放水'后的计数
    ...
ans = sum( (-1)^{|mask|} * f(mask) for mask in range(1<<n) )

# 数论: gcd=k 数对倒推
f[N..1] 从大到小:
    f[k] = (N//k)^2 - sum_{i=2, i*k<=N} f[i*k]
```

### Python 实现

```python
import sys
sys.setrecursionlimit(10000)


def comb_mod(n, k, mod=998244353):
    """O(k) 计算组合数 C(n,k) mod p (n 可能很大, k 小)。"""
    if k < 0 or k > n:
        return 0
    num, den = 1, 1
    for i in range(k):
        num = num * ((n - i) % mod) % mod
        den = den * (i + 1) % mod
    return num * pow(den, mod - 2, mod) % mod


def solve_linear_diophantine_count(m, b):
    """容斥: 不定方程 sum x_i = m, 0<=x_i<=b_i 的非负整数解数.
    全集(无上界)方案数 C(m+n-1, n-1), 容斥枚举违反上界的子集. O(2^n)."""
    n = len(b)
    total = 0
    for mask in range(1 << n):
        s = m
        bits = 0
        for i in range(n):
            if mask >> i & 1:
                s -= b[i] + 1
                bits += 1
        if s < 0:
            continue
        ways = comb_mod(s + n - 1, n - 1)
        if bits & 1:
            total -= ways
        else:
            total += ways
    return total % 998244353


def brute_equation(m, b):
    """暴力枚举验证。"""
    n = len(b)

    def rec(i, rem):
        if i == n:
            return 1 if rem == 0 else 0
        c = 0
        for x in range(0, min(b[i], rem) + 1):
            c += rec(i + 1, rem - x)
        return c

    return rec(0, m)


def derangements(n, mod=998244353):
    """错排数 D_n = n! sum_{i=0}^n (-1)^i / i! (容斥)."""
    fact = 1
    for i in range(2, n + 1):
        fact = fact * i % mod
    invs = [1] * (n + 1)
    for i in range(1, n + 1):
        invs[i] = pow(i, mod - 2, mod)
    # 容斥公式
    res = 0
    for i in range(n + 1):
        t = fact * pow(invs[i], 1, mod) % mod
        # 简化: D_n = n! * sum (-1)^i / i!
        sign = -1 if i & 1 else 1
        # 用分数形式
    # 直接递推 D_n = (n-1)(D_{n-1}+D_{n-2}) 作为参考
    D = [1, 0]
    for i in range(2, n + 1):
        D.append((i - 1) * (D[i - 1] + D[i - 2]) % mod)
    # 容斥形式
    factn = fact
    res2 = 0
    for i in range(n + 1):
        c = comb_mod(n, i) * factn % mod * pow(pow(i, mod - 2, mod) if i else 1, 1, mod) % mod
        # C(n,i)*(n-i)! = n!/i!
        res2 = res2 + (-1 if i & 1 else 1) * (factn * pow(i, mod - 2, mod) % mod if i else factn)
    res2 = res2 % mod
    return D[n], res2


def gcd_pair_count(N):
    """容斥: 数对 (x,y), 1<=x,y<=N, gcd 恰为 k 的个数 f(k), 从 N 倒推. O(N log N)."""
    f = [0] * (N + 1)
    for k in range(N, 0, -1):
        f[k] = (N // k) * (N // k)
        for i in range(2 * k, N + 1, k):
            f[k] -= f[i]
    return f


if __name__ == "__main__":
    import random
    # 不定方程计数对拍
    for _ in range(100):
        n = random.randint(1, 5)
        m = random.randint(0, 8)
        b = [random.randint(0, 5) for _ in range(n)]
        a = solve_linear_diophantine_count(m, b)
        bb = brute_equation(m, b)
        assert a == bb, (m, b, a, bb)
    # 错排 D_n
    D, R = derangements(6)
    assert D == 265, D  # D_6 = 265
    # gcd 数对: f(1) 即互质有序对数 = 1 + 2*sum_{i=2}^N phi(i)
    f = gcd_pair_count(10)
    assert f[1] == 63, f[1]  # 有序互质对 (1<=x,y<=10, gcd=1)
    # 手工: 集合容斥 3 个集合
    # |A∪B∪C| = |A|+|B|+|C|-|AB|-|AC|-|BC|+|ABC|
    print("inclusion-exclusion tests passed")

```

**PyPy 提示**: O(2^n) 枚举子集对 n<=20 可接受; 数论倍数容斥 O(N log N)(调和级数) 1e6 可过。组合数用 O(k) 乘除或预计算阶乘+逆元。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 枚举子集 O(2^n × 单次 f 复杂度); 数论容斥 O(N log N); 错排 O(n) |
| 空间 | O(2^n) 或 O(N) |

### 局限

限制条件多(n>25)时 2^n 枚举爆炸, 需用更巧的计数(如多项式/DP); 交集计数若本身难算, 容斥也救不了; 模意义下组合数需预处理逆元; 数论容斥适合小值域(值域大则用 μ 前缀和/杜教筛)。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P2158 | 3 | SDOI2008 仪仗队: 互质点对计数(容斥/欧拉函数) | [https://www.luogu.com.cn/problem/P2158](https://www.luogu.com.cn/problem/P2158) |
| Luogu | P2398 | 3 | GCD SUM: 倍数容斥/莫比乌斯反演经典 | [https://www.luogu.com.cn/problem/P2398](https://www.luogu.com.cn/problem/P2398) |
| AtCoder | abc331_g | 5 | Collect Them All: min-max 容斥+期望的进阶综合题 | [https://atcoder.jp/contests/abc331/tasks/abc331_g](https://atcoder.jp/contests/abc331/tasks/abc331_g) |

## Pitfalls · 易错点

- 交集与并集公式搞反(并集容斥 vs 交集取补)
- 符号 (-1)^{m-1} 或 (-1)^{\|mask\|} 用错
- 数论容斥倒推顺序错误(应从大到小, f 用 f[i*k])
- 模意义组合数忘预计算逆元/阶乘
- min-max 容斥只在期望线性时可用(依赖线性期望), 忘记条件

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/combinatorics/inclusion-exclusion-principle/](https://oi-wiki.org/math/combinatorics/inclusion-exclusion-principle/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/combinatorics/inclusion-exclusion-principle.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/combinatorics/inclusion-exclusion-principle.md)
- CP-Algorithms ✓ [https://cp-algorithms.com/combinatorics/inclusion-exclusion.html](https://cp-algorithms.com/combinatorics/inclusion-exclusion.html)
- 书籍 ✓ [https://cses.fi/book/book.pdf](https://cses.fi/book/book.pdf)
