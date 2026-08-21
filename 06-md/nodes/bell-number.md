---
id: bell-number
name: 贝尔数
group: G-C-11
stage: advanced
priority: P2
depth_tier: standard
---

# 贝尔数

> B(n) 将 n 个不同元素划分为任意个无标号非空子集的方案数，B_{n+1}=ΣC(n,k)B_k，EGF=e^{e^x-1}

<!-- 元信息: id=bell-number · group=G-C-11 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

贝尔数 B_n（以 Eric Temple Bell 命名，OEIS A000110）是基数为 n 的集合的划分方法总数：把 n 个两两不同的元素分成任意个（可多个）互不区分的非空子集的方案数。序列：B_0=1,B_1=1,B_2=2,B_3=5,B_4=15,B_5=52,B_6=203,…（如 B_3=5：{{1},{2},{3}},{{1},{2,3}},{{2},{1,3}},{{3},{1,2}},{{1,2,3}}）。关键恒等式：B_{n+1}=Σ_{k=0}^n C(n,k)B_k（考虑元素 n+1 与哪 k 个元素同块）；以及 B_n=Σ_{k=0}^n S(n,k)（第二类斯特林数之和）。指数生成函数 EGF：Σ_n B_n x^n/n! = e^{e^x−1}，据此可用多项式 exp O(n log n) 求前 n 项。贝尔三角形（Bell triangle）给出 O(n²) 递推：a_{n,0}=a_{n−1,n−1}，a_{n,m}=a_{n,m−1}+a_{n−1,m−1}，每行首项即贝尔数。模 p 时贝尔数可由 Touchard 同余 B_{n+p} ≡ B_n+B_{n+1} (mod p) 加速。

## Why · 为什么

### 直觉 · Intuition

贝尔数 = 把 n 个人分成若干『同组』（组不编号）的总方案，等价于把第二类斯特林数 S(n,k) 对组数 k 全部求和。递推 B_{n+1}=Σ C(n,k)B_k 的思路：让新元素 n+1 挑 k 个旧元素和它同组（C(n,k) 种挑法），剩下 n−k 个旧元素再任意划分（B_{n−k} 种），对 k 求和。EGF e^{e^x−1} 的组合意义：e^{e^x−1} 是『SET(SET≥1(...))』——把集合切成若干非空无序块，正是划分。

### 原理 · Principle

① B_n=Σ_k S(n,k) 直接来自第二类斯特林数定义。② 递推证明：B_{n+1} 中元素 n+1 所在的块大小为 k+1（即它和恰好 k 个其他元素同块），选这 k 个元素 C(n,k) 种，剩余 n−k 个元素任意划分 B_{n−k} 种，Σ 即得。③ EGF 推导：B_n 的 EGF 满足 B'(x)=e^x·B(x)（卷积递推的生成函数形式），解微分方程得 B(x)=exp(e^x+C)，由 B(0)=1 得 C=−1，即 e^{e^x−1}。④ 贝尔三角形每行首项=上一行末项，同行递推 a_{n,m}=a_{n,m−1}+a_{n−1,m−1}，数学归纳可证第 n 行恰为 B_n,…,B_{n+1} 的若干连续值。

### 历史 · History

贝尔数以美国数学家 Eric Temple Bell（1883–1960）命名，但他本人并未研究它——该数被称为 Bell numbers 是因为 Bell 著作中系统讨论了这些数（及 Bell 三角形）。数列最早出现在 Ramanujan 的笔记中，此前也有其他人独立发现。OI Wiki《贝尔数》页给出定义、递推、贝尔三角形与 EGF e^{e^x−1}；同页注明可用多项式 exp O(n log n) 求整行。竞赛中贝尔数作为『集合划分数』与第二类斯特林数、多项式 exp 结合出现（如 Luogu P5748）。

## How · 实现

### 伪代码

```python
# B(n) 贝尔数

def bell_sum_stirling(n, MOD):
  # 用第二类斯特林数行求和: O(n^2)
  S = [[0]*(n+1) for _ in range(n+1)]; S[0][0]=1
  for i in range(1, n+1):
    for j in range(1, i+1):
      S[i][j] = (S[i-1][j-1] + j*S[i-1][j]) % MOD
  return sum(S[n]) % MOD

def bell_triangle(n, MOD):
  # 贝尔三角形 O(n^2)
  row = [1]                       # 第0行
  for i in range(1, n+1):
    nxt = [row[-1]]               # 首项 = 上行末项
    for m in range(1, i+1):
      nxt.append((nxt[m-1] + row[m-1]) % MOD)
    row = nxt
  return row[0]                   # 每行首项是贝尔数

def bell_recurrence(n, MOD):
  # B_{n+1}=sum C(n,k) B_k: 需要组合数, O(n^2) 或 O(n)
```

### Python 实现

```python
MOD = 998244353


def bell_via_stirling(n, mod=MOD):
    """B(n) = sum_k S(n,k), 第二类斯特林数 O(n^2)."""
    row = [0] * (n + 1)
    row[0] = 1
    for i in range(1, n + 1):
        for j in range(i, 0, -1):
            row[j] = (row[j - 1] + j * row[j]) % mod
        row[0] = 0
    return sum(row) % mod


def bell_triangle(n, mod=MOD):
    """贝尔三角形 O(n^2), 返回 [B_0..B_n]."""
    bell = [1]
    row = [1]
    for i in range(1, n + 1):
        nxt = [row[-1]]
        for m in range(1, i + 1):
            nxt.append((nxt[m - 1] + row[m - 1]) % mod)
        row = nxt
        bell.append(row[0])
    return bell


def bell_recurrence(n, mod=MOD):
    """B_{n+1} = sum_k C(n,k) B_k, O(n^2) 预计算组合数."""
    C = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        C[i][0] = C[i][i] = 1
        for j in range(1, i):
            C[i][j] = (C[i - 1][j - 1] + C[i - 1][j]) % mod
    b = [0] * (n + 1)
    b[0] = 1
    for i in range(n):
        s = 0
        for k in range(i + 1):
            s = (s + C[i][k] * b[k]) % mod
        b[i + 1] = s
    return b[n]


def bell_egf_naive(n, mod=MOD):
    """由 EGF e^{e^x-1} 直接按系数递推(形式幂级数 exp) O(n^2):
    exp(A) 的系数 b_k 满足 k*b_k = sum_{j=0}^{k-1} (j+1)*a_{k-1-j}*b_j,
    其中 A(x)=e^x-1, a_j = 1/j!."""
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % mod
    inv = [1] * (n + 1)
    inv[n] = pow(fact[n], mod - 2, mod)
    for i in range(n, 0, -1):
        inv[i - 1] = inv[i] * i % mod
    a = [inv[i] for i in range(n + 1)]      # a_i = 1/i!  (e^x - 1 的非零项)
    b = [0] * (n + 1)
    b[0] = 1
    for k in range(1, n + 1):
        s = 0
        for j in range(k):
            s = (s + (k - j) * a[k - j] * b[j]) % mod   # (k-j)*a_{k-j}
        b[k] = s * pow(k, mod - 2, mod) % mod
    return [b[i] * fact[i] % mod for i in range(n + 1)]  # 还原成 B_n = n! * b_n


if __name__ == "__main__":
    known = {0: 1, 1: 1, 2: 2, 3: 5, 4: 15, 5: 52, 6: 203}
    for n, v in known.items():
        assert bell_via_stirling(n) % MOD == v, n
        assert bell_triangle(n)[n] % MOD == v
        assert bell_recurrence(n) % MOD == v
    egf_list = bell_egf_naive(6)
    for n, v in known.items():
        assert egf_list[n] % MOD == v, (n, egf_list[n])
    assert bell_triangle(6)[4] == 15
    print("bell-number: all tests passed")

```

**PyPy 提示**: n≤5000 用 O(n²) 递推（贝尔三角形或斯特林行）均可；n 更大需多项式 exp O(n log n)（需 NTT）。贝尔三角形实现简单且只用两行滚动。取模时注意负数与乘法溢出（Python 天然大整数无碍）。Touchard 同余 B_{n+p}≡B_n+B_{n+1} (mod p) 可用于模素数加速大索引。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n²) 递推；O(n log n) 多项式 exp（需 NTT） |
| 空间 | O(n) 滚动或 O(n²) 全表 |

### 局限

① B_n 增长超指数（渐近 ~ n^{-1/2}(n/log n)^n / ...），必须取模；② 无现成 NTT 环境时 O(n²) 是上限；③ EGF e^{e^x−1} 与 OGF 不同，还原系数要乘 n!；④ 递推 B_{n+1}=ΣC(n,k)B_k 每次 O(n) 需预计算组合数，整体 O(n²)。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P5748 | 4 | 集合划分计数：B(n)=ΣS(n,k)，多项式 exp 求 EGF e^{e^x−1} 前 n 项，OI Wiki 模板题 | [https://www.luogu.com.cn/problem/P5748](https://www.luogu.com.cn/problem/P5748) |
| OI Wiki | bell | 3 | 概念页：定义、递推、贝尔三角形与 EGF 完整推导 | [https://oi-wiki.org/math/combinatorics/bell/](https://oi-wiki.org/math/combinatorics/bell/) |
| UOJ | 540 | 6 | 联合省选 2020 组合数问题：贝尔数/斯特林数与多项式综合（OI Wiki stirling 习题交叉） | [https://uoj.ac/problem/540](https://uoj.ac/problem/540) |

## Pitfalls · 易错点

- EGF 系数是 B_n/n!，还原时忘乘 n!
- B_{n+1}=ΣC(n,k)B_k 中求和到 k=n 而非 k=n−1
- 贝尔三角形行内递推 a_{n,m}=a_{n,m−1}+a_{n−1,m−1} 的索引写错
- 把 B_n 与 p(n)（整数分拆）混淆——贝尔数是集合划分
- 模素数用 Touchard 同余时忽略要求 p 为素数

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/combinatorics/bell/](https://oi-wiki.org/math/combinatorics/bell/)
- oiwiki-raw ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/combinatorics/bell.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/combinatorics/bell.md)
- oeis ✓ [https://oeis.org/A000110](https://oeis.org/A000110)
- Wikipedia ✓ [https://en.wikipedia.org/wiki/Bell_number](https://en.wikipedia.org/wiki/Bell_number)
