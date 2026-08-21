---
id: derangement
name: 错排问题
group: G-C-11
stage: intermediate
priority: P2
depth_tier: standard
---

# 错排问题

> D(n)=n!Σ_{k=0}^n (-1)^k/k! ≈ n!/e，无固定点（P_i≠i）排列数，递推 D_n=(n-1)(D_{n-1}+D_{n-2})

<!-- 元信息: id=derangement · group=G-C-11 · stage=intermediate · priority=P2 · depth_tier=standard -->

## What · 是什么

错位排列（derangement）是没有任何元素落在其『有序位置』的排列：1~n 的排列 P 满足 P_i ≠ i 对所有 i。它等价于没有不动点（没有长度 1 的轮换）的排列。记 D_n 为错排数，则有容斥公式 D_n = n!·Σ_{k=0}^n (-1)^k/k! = n! − n!/1! + n!/2! − … + (−1)^n，数列开头为 0,1,2,9,44,265（OEIS A000166）。极限性质：lim D_n/n! = 1/e，且 D_n = ⌊n!/e + 1/2⌋（取整表达式）。常用的两个递推：D_n = (n−1)(D_{n−1}+D_{n−2})（经典信封信纸问题）与 D_n = n·D_{n−1} + (−1)^n。典型应用：错排计数、含错排的组合 DP（如『恰好 k 人拿到自己帽子』= C(n,k)·D_{n−k}）、容斥思想的入门。

## Why · 为什么

### 直觉 · Intuition

『所有排列 n! 个，减掉至少有一个人在自己位置的』。用容斥：把『P_i=i』视作事件 A_i，被至少一个 A_i 覆盖的排列数 = Σ|A_i| − Σ|A_i∩A_j| + …，而 k 个固定位置共有的排列是 (n−k)! 个，选 k 个位置有 C(n,k) 种，故 D_n = Σ_k (−1)^k C(n,k)(n−k)! = n!Σ(−1)^k/k!。信封信纸版递推：把第 n 封信『先放对』再调整——要么前 n−1 全错排，第 n 封与前 n−1 任一封交换（D_{n−1}·(n−1)）；要么前 n−1 中恰好一封放对、其余错排，把放对的那封与第 n 封交换（D_{n−2}·(n−1)）。

### 原理 · Principle

容斥原理推导：全集 U 为 n! 个排列；S_i 为满足 P_i≠i 的排列。|∩_i S_i| = n! − Σ_k (−1)^{k−1} Σ_{a_1<…<a_k} |∩_i S̄_{a_i}| = n! − n!Σ_k (−1)^{k−1}/k! = n!Σ_{k=0}^n (−1)^k/k!。递推式 D_n=(n−1)(D_{n−1}+D_{n−2}) 的组合证明：构造 n 的错排有两种途径——(a) 取 n−1 的一个错排，把新元素 n 与任一元素 i 交换位置；(b) 取 n−2 的一个错排加一个『固定点 i』的排列，将 n 与 i 交换使其脱固定。每个 n 错排恰好被构造一次，故成立。另一递推 D_n = nD_{n−1} + (−1)^n 可由公式代入验证。

### 历史 · History

错排问题源于『关于排列的欧洲传说』（信件放错信封），也被称为 rencontres numbers（相遇数）。早期由 de Montmort（1708）与 Nicolas Bernoulli 研究，Euler 也独立处理过。『全部放错』的概率极限 1/e ≈ 0.3679 是随机排列无固定点的概率。OI Wiki《错位排列》页系统给出容斥推导、两个递推与取整公式；OEIS A000166 收录数列。竞赛中多作为容斥/递推经典题出现，也常见于概率与期望题。

## How · 实现

### 伪代码

```python
# D_n 错排数

def derangement_inclusion(n):
  # 容斥公式 O(n)
  D = 0
  for k in range(n+1):
    D += (-1)**k * fact(n) // fact(k)
  return D

def derangement_recurrence(n):
  # D_n = (n-1)(D_{n-1}+D_{n-2}), O(n)
  D0, D1 = 1, 0       # D_0=1, D_1=0
  if n == 0: return D0
  for i in range(2, n+1):
    D0, D1 = D1, (i-1)*(D1+D0)
  return D1

def derangement_mod(n, MOD):
  # 模意义 O(n)
  D0, D1 = 1%MOD, 0
  for i in range(2, n+1):
    D0, D1 = D1, (i-1)%MOD*(D1+D0)%MOD
  return D1
```

### Python 实现

```python
from math import factorial


def derangement_inclusion(n):
    """容斥公式 D(n) = n! * sum_{k=0}^{n} (-1)^k / k!  (精确整数)."""
    f = factorial(n)
    D = 0
    for k in range(n + 1):
        D += ((-1) ** k) * (f // factorial(k))
    return D


def derangement_recurrence(n):
    """递推 D(n) = (n-1)(D(n-1)+D(n-2)), D(0)=1, D(1)=0."""
    if n == 0:
        return 1
    d0, d1 = 1, 0  # D(0), D(1)
    for i in range(2, n + 1):
        d0, d1 = d1, (i - 1) * (d1 + d0)
    return d1


def derangement_mod(n, MOD=1000000007):
    """模意义错排数 O(n), 使用 D(n) = n*D(n-1) + (-1)^n 或二阶递推."""
    if n == 0:
        return 1 % MOD
    d0, d1 = 1 % MOD, 0
    for i in range(2, n + 1):
        d0, d1 = d1, (i - 1) * (d1 + d0) % MOD
    return d1


def exactly_k_fixed(n, k, MOD=1000000007):
    """恰好 k 个位置不动(其余错排)的方案数 = C(n,k) * D(n-k)."""
    num = 1
    for i in range(1, k + 1):
        num = num * (n - k + i) // i  # 精确 C(n,k)
    return num * derangement_recurrence(n - k)


def brute(n):
    """暴力枚举验证."""
    from itertools import permutations
    cnt = 0
    for p in permutations(range(1, n + 1)):
        if all(p[i] != i + 1 for i in range(n)):
            cnt += 1
    return cnt


if __name__ == "__main__":
    known = {0: 1, 1: 0, 2: 1, 3: 2, 4: 9, 5: 44, 6: 265}  # OEIS A000166
    for n, expect in known.items():
        assert derangement_inclusion(n) == expect
        assert derangement_recurrence(n) == expect
        assert derangement_mod(n) % 1000000007 == expect
    for n in range(1, 8):
        assert derangement_recurrence(n) == brute(n), n
    assert exactly_k_fixed(4, 2) == 6   # C(4,2)*D(2) = 6*1
    assert exactly_k_fixed(5, 1) == 5 * 9 == 45   # C(5,1)*D(4) = 5*9
    print("derangement: all tests passed")

```

**PyPy 提示**: O(n) 递推即可；注意 D(0)=1, D(1)=0 的边界。取模时 (i-1)*(d1+d0) 先 mod 再乘。n 大到 1e7 时纯 Python O(n) 循环会慢，可改用容斥公式 + 预计算阶乘逆元（O(n) 但更少乘法）或找规律；竞赛 n 通常 ≤1e6，O(n) 足够。n! 精确整数对 n≤20 用 factorial 即可。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n) 递推/容斥 |
| 空间 | O(1)（滚动）或 O(n)（表） |

### 局限

① 递推用除法/组合数需精确整数或模逆元；② n! 增长极快，精确计算仅限小 n；③ 『恰好 k 个不动』需组合数，别直接乘；④ D_n 的取整公式 ⌊n!/e+1/2⌋ 只在数学上成立，编程时仍用递推；⑤ 与全排列 n! 差异随 n 增大趋近比例 1/e，直觉上别把 D_n 当 n! 量级。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1595 | 2 | 信封问题（入门）：直接求 D(n)，n≤20 可用精确整数，OI Wiki 经典题 | [https://www.luogu.com.cn/problem/P1595](https://www.luogu.com.cn/problem/P1595) |
| Luogu | P4071 | 3 | SDOI2016 排列计数：恰好 m 个位置不动，答案 C(n,m)·D(n-m)，需预处理阶乘+错排 | [https://www.luogu.com.cn/problem/P4071](https://www.luogu.com.cn/problem/P4071) |
| Luogu | P1655 | 3 | 小朋友的球：第二类斯特林数与错排结合的综合计数题（高精度） | [https://www.luogu.com.cn/problem/P1655](https://www.luogu.com.cn/problem/P1655) |

## Pitfalls · 易错点

- D(0)=1、D(1)=0 边界记错
- 递推顺序写错（D_n 依赖 D_{n-1} 与 D_{n-2}）
- 『恰好 k 个位置不动』忘了乘 C(n,k)
- 取模除法直接整除导致错误
- 把 D_n 与 n! 混淆（n 个排列中错排比例约 1/e）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/combinatorics/derangement/](https://oi-wiki.org/math/combinatorics/derangement/)
- oiwiki-raw ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/combinatorics/derangement.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/combinatorics/derangement.md)
- CP-Algorithms ✓ [https://cp-algorithms.com/combinatorics/derangements.html](https://cp-algorithms.com/combinatorics/derangements.html)
- oeis ✓ [https://oeis.org/A000166](https://oeis.org/A000166)
