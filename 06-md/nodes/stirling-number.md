---
id: stirling-number
name: 斯特林数
group: G-C-11
stage: advanced
priority: P2
depth_tier: standard
---

# 斯特林数

> 第一类 s(n,k)=将n个元素分成k个无标号非空轮换；第二类 S(n,k)=分成k个无标号非空子集；两类递推与幂/阶乘幂互转

<!-- 元信息: id=stirling-number · group=G-C-11 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

斯特林数（Stirling numbers）是组合计数的两大核心表。第二类斯特林数 S(n,k)={n\brace k}：将 n 个两两不同的元素划分为 k 个互不区分的非空子集的方案数。递推 S(n,k)=S(n−1,k−1)+k·S(n−1,k)，通项 S(n,k)=Σ_{i=0}^k (−1)^{k−i} i^n /(i!(k−i)!)。第一类斯特林数 s(n,k)=[n\atop k]：将 n 个两两不同的元素划分为 k 个互不区分的非空轮换（cyclic arrangement，环形排列，旋转视为相同、翻转视为不同）的方案数。递推 s(n,k)=s(n−1,k−1)+(n−1)·s(n−1,k)。两类都与幂/阶乘幂互转：x^n = Σ_k S(n,k)·x^{\underline{k}}（普通幂→下降幂）、x^{\overline{n}} = Σ_k s(n,k)·x^k（上升幂→普通幂）、x^n = Σ_k S(n,k)(−1)^{n−k}x^{\overline{k}}、x^{\underline{n}} = Σ_k s(n,k)(−1)^{n−k}x^k。同一行/同一列可用生成函数 O(n log n)（NTT/多项式）计算：行生成函数 ∏_{i=0}^{n−1}(x+i)=x^{\overline{n}}（第一类），列用 EGF (e^x−1)^k/k!（第二类）。

## Why · 为什么

### 直觉 · Intuition

想象给 n 个人分组：第二类问『分成 k 组（组不编号）有几种』——新来一个人，要么自己单开一组，要么挤进现有 k 组中的某一组，故 S(n,k)=S(n−1,k−1)+k·S(n−1,k)。第一类问『分成 k 个围桌转圈（桌子不编号、方向有意义）有几种』——新来一个人，要么自己坐一桌，要么插进 n−1 个人中某一个人的右手边（n−1 种位置），故 s(n,k)=s(n−1,k−1)+(n−1)·s(n−1,k)。两者是『无标号集合』与『无标号轮换』两种结构的计数，递推结构完全平行。

### 原理 · Principle

第二类通项由容斥得到：设 G_i=i^n（i 个有标号盒子允许空的方案），F_i=Σ_j C(i,j)F_j（i 个有标号非空盒），二项式反演得 F_i=Σ_j(−1)^{i−j}C(i,j)j^n；因无标号盒去标号除以 k!，得 S(n,k)=F_k/k!=Σ_{i=0}^k (−1)^{k−i}i^n/(i!(k−i)!)。第一类行生成函数 ∏_{i=0}^{n−1}(x+i) 由递推 s(n,k)=s(n−1,k−1)+(n−1)s(n−1,k) 推出：F_n(x)=Σ_k s(n,k)x^k 满足 F_n=x·F_{n−1}+(n−1)F_{n−1}。幂与阶乘幂的互转恒等式 x^n=Σ S(n,k)x^{\underline{k}} 组合意义：x^n 是 n 个有标号球放入 x 个有标号盒的方案数，按『用了几个非空盒』分层，非空盒作为有序集合有 (x)_k 种。

### 历史 · History

两类斯特林数以 James Stirling（1692–1770）命名，他在 1730 年《Methodus Differentialis》中系统研究；有趣的是第二类斯特林数（子集数）在 Stirling 著作与《具体数学》中都被先介绍，也比第一类常用得多（OI Wiki 专门注释）。第一类对应轮换/无符号版本 [n\atop k] 与含符号版本 s(n,k)=(-1)^{n-k}[n\atop k] 两种记号。现代竞赛中斯特林数配合 NTT 多项式可 O(n log n) 求整行/整列，是『生成函数换元』、组合恒等式、多项式快速求和的重要工具。

## How · 实现

### 伪代码

```python
# 两类斯特林数 DP (0-indexed 表)

def stirling2(n, k):   # S(n,k) 第二类, 可带模
  S = [[0]*(k+1) for _ in range(n+1)]
  S[0][0] = 1
  for i in range(1, n+1):
    for j in range(1, min(i,k)+1):
      S[i][j] = (S[i-1][j-1] + j * S[i-1][j]) % MOD
  return S[n][k]

def stirling1(n, k):   # s(n,k) 第一类(无符号), 可带模
  s = [[0]*(k+1) for _ in range(n+1)]
  s[0][0] = 1
  for i in range(1, n+1):
    for j in range(1, min(i,k)+1):
      s[i][j] = (s[i-1][j-1] + (i-1) * s[i-1][j]) % MOD
  return s[n][k]

# 同一行: 第二类用通项卷积 O(n log n); 第一类用上升幂 O(n log^2 n) 或上升幂 O(n log n)
```

### Python 实现

```python
from math import factorial, comb

MOD = 998244353


def stirling2_row(n, mod=MOD):
    """第二类斯特林数整行 S(n,0..n) O(n^2) DP, 返回 list."""
    row = [0] * (n + 1)
    row[0] = 1
    for i in range(1, n + 1):
        for j in range(i, 0, -1):
            row[j] = (row[j - 1] + j * row[j]) % mod
        row[0] = 0
    return row


def stirling1_row(n, mod=MOD):
    """第一类(无符号)斯特林数整行 s(n,0..n) O(n^2) DP. 检验行生成函数 x^{overline n}."""
    row = [0] * (n + 1)
    row[0] = 1
    for i in range(1, n + 1):
        for j in range(i, 0, -1):
            row[j] = (row[j - 1] + (i - 1) * row[j]) % mod
        row[0] = 0
    return row


def rising_factorial_row(n, mod=MOD):
    """上升幂 x^{overline n} 的展开系数 = 第一类无符号斯特林数整行(交叉验证)."""
    poly = [1]
    for i in range(n):
        # 乘 (x + i)
        nxt = [0] * (len(poly) + 1)
        for j, c in enumerate(poly):
            nxt[j] = (nxt[j] + c * i) % mod
            nxt[j + 1] = (nxt[j + 1] + c) % mod
        poly = nxt
    return poly


def stirling2_explicit(n, k):
    """第二类通项公式(精确小值)."""
    tot = 0
    for i in range(k + 1):
        tot += ((-1) ** (k - i)) * comb(k, i) * (i ** n)
    return tot // factorial(k)


def change_basis_pow_to_falling(n, mod=MOD):
    """x^n = sum_k S(n,k) x^{underline k} 的系数(第二类斯特林数)."""
    return stirling2_row(n, mod)


def brute_set_partition(n, k):
    """暴力: 将 n 个元素分成 k 个无标号非空子集(集合划分数) 用于验证."""
    if n == 0 and k == 0:
        return 1
    if n < k or k == 0:
        return 0
    # 递归 S(n,k) = S(n-1,k-1) + k*S(n-1,k)
    return brute_set_partition(n - 1, k - 1) + k * brute_set_partition(n - 1, k)


if __name__ == "__main__":
    # 已知小值: S(n,k) 第二类三角形行:
    # n=4: 1 7 6 1; n=5: 1 15 25 10 1
    # 第二类整行(含 S(n,0)): n=5 -> 0 1 15 25 10 1
    r2 = stirling2_row(5)
    assert r2 == [0, 1, 15, 25, 10, 1], r2
    # 第一类无符号整行(含 s(n,0)): n=4 -> 0 6 11 6 1 (= x(x+1)(x+2)(x+3))
    r1 = stirling1_row(4)
    assert r1 == [0, 6, 11, 6, 1], r1
    assert rising_factorial_row(4) == [0, 6, 11, 6, 1]
    assert stirling2_explicit(5, 2) == 15 and stirling2_explicit(5, 3) == 25
    for n in range(0, 7):
        for k in range(0, n + 1):
            assert stirling2_row(n)[k] == brute_set_partition(n, k), (n, k)
    print("stirling-number: all tests passed")

```

**PyPy 提示**: O(n^2) DP 建表：n=5000 时空皆可（25e6 ints，PyPy list 略大），n=1e4 建议压缩一维滚动。模素数取 NTT 可实现整行 O(n log n)；第一类整行 = 上升幂 x^\overline{n} 展开（分治乘 NTT O(n log^2 n) 或上升幂 O(n log n)）。两类互转（幂↔阶乘幂）实际是矩阵乘法，O(n^2) 即可完成一组基变换。列（固定 k）：第二类列 EGF (e^x−1)^k/k!，第一类列 EGF ln(1/(1-x))^k/k!。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 单值递推 O(n·k)；整行 O(n^2)；整行优化 O(n log n)（NTT） |
| 空间 | O(n·k) 表或 O(n) 滚动 |

### 局限

① 第一类『无符号』与『含符号』记号易混（含符号 s(n,k)=(-1)^{n-k}[n\atop k]）；② 无符号数值极大（≈(n-1)!量级），必须取模；③ 轮换与子集含义不同，别套错递推系数（k vs n−1）；④ 同一行用通项需要 NTT 依赖，纯 Python 只能 O(n^2)；⑤ 列生成函数需要多项式 exp/ln，复杂度前置要求高。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P5748 | 4 | 集合划分计数：贝尔数 B(n)=Σ S(n,k)，多项式 exp 求整行 O(n log n) | [https://www.luogu.com.cn/problem/P5748](https://www.luogu.com.cn/problem/P5748) |
| Luogu | P5408 | 5 | 第一类斯特林数·行：上升幂 x^\overline{n} 展开，OI Wiki shift 页例题 | [https://www.luogu.com.cn/problem/P5408](https://www.luogu.com.cn/problem/P5408) |
| UOJ | 540 | 6 | 联合省选 2020 组合数问题：斯特林数+多项式与组合数求和综合应用，OI Wiki 习题 | [https://uoj.ac/problem/540](https://uoj.ac/problem/540) |
| HDU | 3625 | 3 | Examining the Rooms：第一类斯特林数 + 容斥（允许若干房间打不开），OI Wiki 习题 | [https://acm.hdu.edu.cn/showproblem.php?pid=3625](https://acm.hdu.edu.cn/showproblem.php?pid=3625) |

## Pitfalls · 易错点

- 第一类无符号与含符号版本混淆（符号 = (-1)^{n-k}）
- 第二类系数是 k（塞进 k 个现成组），第一类是 n−1（n−1 个插入位），别写反
- 边界 S(0,0)=1, S(n,0)=0(n>0) 等记错
- 整行计算直接套列 EGF 导致复杂度错误
- 无符号第一类数值巨大，忘取模溢出

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/combinatorics/stirling/](https://oi-wiki.org/math/combinatorics/stirling/)
- oiwiki-raw ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/combinatorics/stirling.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/combinatorics/stirling.md)
- mathworld ✓ [http://mathworld.wolfram.com/StirlingNumberoftheSecondKind.html](http://mathworld.wolfram.com/StirlingNumberoftheSecondKind.html)
- CP-Algorithms ✓ [https://cp-algorithms.com/combinatorics/stirling_numbers.html](https://cp-algorithms.com/combinatorics/stirling_numbers.html)
