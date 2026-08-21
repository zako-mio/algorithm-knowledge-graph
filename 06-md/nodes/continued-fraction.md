---
id: continued-fraction
name: 连分数
group: G-C-9
stage: advanced
priority: P2
depth_tier: standard
---

# 连分数

> 实数的有理逼近，渐近分数递推，Pell方程与Stern-Brocot基础

<!-- 元信息: id=continued-fraction · group=G-C-9 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

简单连分数是把实数 x 表示成 [a_0,a_1,a_2,...]=a_0+1/(a_1+1/(a_2+...)) 的形式，其中 a_0 为整数，a_1,a_2,... 为正整数。任意有理数对应有限简单连分数，任意实数对应（可能无限）简单连分数，无理数对应无限连分数。截断前 k+1 项得到第 k 个渐近分数 x_k=p_k/q_k，是实数 x 的最佳有理逼近。二次无理数（形如 (P+√D)/Q）的连分数是循环连分数。核心用途：求最大公约数（欧几里得算法的连分数解释）、丢番图逼近、佩尔方程、Stern-Brocot 树、线性丢番图方程、以及『找与直线最近整点』类问题。

## Why · 为什么

### 直觉 · Intuition

连分数就是把『带余除法』过程写成嵌套分数：a_0=⌊x⌋，余数 1/(x-a_0) 继续展开。渐近分数递推 p_k=a_k p_{k-1}+p_{k-2}, q_k=a_k q_{k-1}+q_{k-2} 与斐波那契数列同构。渐近分数是『分母不超过 q_k 的所有分数中最接近 x 的』——这就是丢番图逼近与最优有理逼近的根源。循环的二次无理数使连分数成为解二次方程的『数值迭代』。

### 原理 · Principle

① 递推：p_{-2}=0,p_{-1}=1; q_{-2}=1,q_{-1}=0; p_k=a_k p_{k-1}+p_{k-2}, q_k=a_k q_{k-1}+q_{k-2}。② 渐近分数差：p_{k-1}q_k-p_k q_{k-1}=(-1)^k，故相邻渐近分数互质且 |x-p_k/q_k|<1/(q_k q_{k+1})≤1/q_k^2。③ 偶下标渐近分数递增逼近 x，奇下标递减逼近（交错收敛）。④ 二次无理数连分数是循环的（Lagrange 定理），循环节可预判周期；纯循环连分数的渐近分数满足 p^2-Dq^2=±1（连接佩尔方程）。⑤ 复杂度：有理数 p/q 的连分数长度 O(log min(p,q))，等价于欧几里得算法步数。

### 历史 · History

连分数思想可追溯至古希腊（欧几里得算法隐含此结构），文艺复兴时期 Bombelli、Cataldi 等研究；17 世纪 Huygens 用连分数做天文齿轮比逼近；Lagrange（1770）证明二次无理数的循环性并用于解佩尔方程。现代数值分析中用连分数做高效有理逼近。

## How · 实现

### 伪代码

```python
# 实数 -> 连分数系数
def to_cf(x):
  a = []; 
  while x is not rational-exact:
    a.append(floor(x))
    x = 1 / (x - floor(x))

# 渐近分数递推
p_prev2, p_prev1 = 0, 1
q_prev2, q_prev1 = 1, 0
for a in coeffs:
  p = a*p_prev1 + p_prev2
  q = a*q_prev1 + q_prev2
  yield (p, q)
  p_prev2, p_prev1 = p_prev1, p
  q_prev2, q_prev1 = q_prev1, q
```

### Python 实现

```python
from fractions import Fraction
from math import isqrt


def frac_to_cf(x: Fraction):
    """有理数 -> 有限简单连分数系数列表."""
    a = []
    while x != 0:
        n = x.numerator // x.denominator
        a.append(n)
        x = x - n
        if x != 0:
            x = 1 / x
    return a


def cf_to_frac(a):
    """连分数系数 -> 有理数(精确)."""
    f = Fraction(a[-1])
    for k in range(len(a) - 2, -1, -1):
        f = Fraction(a[k]) + 1 / f
    return f


def convergents(coeffs):
    """返回所有渐近分数 (p_k, q_k)."""
    p_prev2, p_prev1 = 0, 1
    q_prev2, q_prev1 = 1, 0
    for a in coeffs:
        p = a * p_prev1 + p_prev2
        q = a * q_prev1 + q_prev2
        yield (p, q)
        p_prev2, p_prev1 = p_prev1, p
        q_prev2, q_prev1 = q_prev1, q


def sqrt_cf(D: int, n: int):
    """sqrt(D) 的前 n 个连分数系数 (D 非完全平方)."""
    r = isqrt(D)
    assert r * r != D
    P, Q = 0, 1
    a0 = r
    res = [a0]
    for _ in range(n - 1):
        P2 = a0 * Q - P
        Q2 = (D - P2 * P2) // Q
        a0 = (P2 + r) // Q2
        P, Q = P2, Q2
        res.append(a0)
    return res


if __name__ == "__main__":
    # 415/93 = 4 + 1/(2+1/(6+1/7)) = [4;2,6,7]
    cf = frac_to_cf(Fraction(415, 93))
    assert cf == [4, 2, 6, 7], cf
    assert cf_to_frac(cf) == Fraction(415, 93)

    # 黄金比例 phi = [1;1,1,1,...] 渐近分数 = 斐波那契比
    gold = [1] * 8
    cg = list(convergents(gold))
    assert cg[0] == (1, 1)
    assert cg[1] == (2, 1)
    assert cg[2] == (3, 2)
    assert cg[3] == (5, 3)
    assert cg[4] == (8, 5)

    # sqrt(2) = [1;2,2,2,...], 渐近分数 3/2,7/5,17/12 (佩尔解)
    c2 = sqrt_cf(2, 5)
    assert c2 == [1, 2, 2, 2, 2]
    cv = list(convergents(c2))
    assert cv[1] == (3, 2) and cv[1][0] ** 2 - 2 * cv[1][1] ** 2 == 1
    assert cv[3] == (17, 12)

    # 交叉验证: 随机有理数往返一致
    import random
    random.seed(11)
    for _ in range(200):
        x = Fraction(random.randint(1, 10**6), random.randint(1, 10**6))
        c = frac_to_cf(x)
        assert cf_to_frac(c) == x
        # 渐近分数逼近性质: |x - p/q| < 1/q^2
        for (p, q) in convergents(c):
            assert abs(x - Fraction(p, q)) < Fraction(1, q * q) or x == Fraction(p, q)
    print("All tests passed.")
```

**PyPy 提示**: 竞赛中常用 int 手写连分数（有理数版）避免 Fraction 常数。√D 展开每步整数运算 O(1)，n 个系数总 O(n)。涉及超大分母 q_k 时 Python 大整数无忧；PyPy 下同。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 有理数连分数 O(log min(p,q))；√D 展开每步 O(1) 整数运算，n 步 O(n) |
| 空间 | O(n) 存系数（渐进分数可流式 O(1) 空间） |

### 局限

浮点连分数展开对精度极敏感（浮点误差会在余数逼近 0 时失控），务必用有理数/整数实现。√D 的展开必须用整数 PQa 递推而非逐次 1/(x-⌊x⌋)。黄金比例等周期连分数无穷展开需人工设定截断次数。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P5179 | 4 | Fraction：用连分数/中间分数构造 a/b<p/q<c/d 的最小分母分数（OI Wiki 例题） | [https://www.luogu.com.cn/problem/P5179](https://www.luogu.com.cn/problem/P5179) |
| Luogu | P7739 | 7 | NOI2021 密码箱：连分数性质与矩阵乘法的综合应用（OI Wiki 例题） | [https://www.luogu.com.cn/problem/P7739](https://www.luogu.com.cn/problem/P7739) |
| Luogu | P2900 | 5 | Land Acquisition：Stern-Brocot/连分数思想在斜率优化上的体现（同类思想迁移题） | [https://www.luogu.com.cn/problem/P2900](https://www.luogu.com.cn/problem/P2900) |

## Pitfalls · 易错点

- 浮点展开丢精度：必须用有理数 Fraction 或整数 PQa
- 渐近分数递推初值 p_{-2}=0,p_{-1}=1,q_{-2}=1,q_{-1}=0 记错会导致全体错位
- 误差估计 \|x-p/q\|<1/q^2 的常数在不同表述下不同（渐近分数用 1/(q_k q_{k+1}) 更紧）
- 奇数/偶数下标渐近分数逼近方向相反，用于『找一侧最近分数』时需选对方向
- √D 展开中 P,Q 为负值要正确归一（Q 整除性由二次无理数性质保证，勿断言整除而用整除计算）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/number-theory/continued-fraction/](https://oi-wiki.org/math/number-theory/continued-fraction/)
- CP-Algorithms ✓ [https://cp-algorithms.com/algebra/continued-fractions.html](https://cp-algorithms.com/algebra/continued-fractions.html)
