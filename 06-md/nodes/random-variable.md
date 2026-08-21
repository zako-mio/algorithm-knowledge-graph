---
id: random-variable
name: 随机变量
group: G-C-15
stage: advanced
priority: P2
depth_tier: standard
---

# 随机变量

> 随机变量是样本空间到实数的函数，离散/连续型分布与分布函数、密度函数，随机变量独立性

<!-- 元信息: id=random-variable · group=G-C-15 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

随机变量 X 是定义在样本空间 Ω 上的实值函数 X:Ω→R，且满足可测性条件（对任意 t，{ω:X(ω)≤t}∈F）。按值域是否可数分为离散型（用分布列 P{X=x_i}=p_i 刻画）与连续型（用密度函数 f(x) 刻画，F(x)=∫f(x)dx）。分布函数 F(x)=P(X≤x) 与随机变量一一对应。它是把'事件'代数化、从而能用函数工具（求和/积分）处理随机现象的桥梁，是概率DP建模的核心建模工具。

## Why · 为什么

### 直觉 · Intuition

把随机结果'编码'成数字：掷骰子的点数、抽到红球的个数。这样随机现象就变成'一个数字怎么取'，可以用分布来描述；后续的期望、方差都建立在这个数字函数上。连续型单点概率为 0，因此用密度函数描述'落在小区间内的可能性'。

### 原理 · Principle

分布函数 F(x)=P(X≤x) 具有右连续性、单调递增、F(-∞)=0、F(+∞)=1；满足这些性质的函数都能对应某个随机变量，故分布函数与随机变量一一对应。离散型用分布列求和，连续型用密度积分。示性函数 I_A 把事件编码成 0/1 随机变量，其期望恰为 P(A)，这是'概率转期望'的桥梁。随机变量独立用分布函数定义 P(X≤x,Y≤y)=P(X≤x)P(Y≤y)，因为连续型取单点概率为 0，中学的 P(X=α) 定义不适用。

### 历史 · History

随机变量概念由法国概率学家逐步形式化，20 世纪初被纳入测度论框架（勒贝格积分、柯尔莫哥洛夫公理）。分布函数、密度函数是苏联/法国概率学派的标准工具，是现代概率论（包括马尔可夫链、随机过程）的语言基础。

## How · 实现

### 伪代码

```python
# 离散型: 分布列
X 取 x_i 的概率为 p_i, 要求 sum p_i = 1

# 连续型: 密度函数
P(a < X <= b) = ∫_a^b f(x) dx
F(x) = ∫_{-∞}^x f(t) dt

# 示性函数 (事件->0/1随机变量)
I_A(ω) = 1 if ω∈A else 0
E[I_A] = P(A)

# 独立性 (用分布函数定义)
X⊥Y ⇔ F(x,y) = F_X(x)F_Y(y) 对所有x,y
```

### Python 实现

```python
import math


def bernoulli_pmf(p, k):
    """伯努利分布 P(X=k), k∈{0,1}, X 表示单次试验成功次数"""
    assert 0 <= p <= 1 and k in (0, 1)
    return p if k == 1 else (1 - p)


def binomial_pmf(n, p, k):
    """二项分布 P(X=k)=C(n,k)p^k(1-p)^(n-k)
    X 表示 n 次独立试验中成功次数
    """
    assert 0 <= k <= n and 0 <= p <= 1
    return math.comb(n, k) * (p ** k) * ((1 - p) ** (n - k))


def cdf_empirical(data, x):
    """经验分布函数: F(x) = P(X<=x) 的样本估计"""
    return sum(1 for v in data if v <= x) / len(data)


def indicator_expectation(p_a):
    """示性函数期望 E[I_A]=P(A)"""
    return p_a


def independence_by_cdf(p_xy, p_x, p_y):
    """按分布函数判定独立: F(x,y) == F_X(x)F_Y(y)"""
    return abs(p_xy - p_x * p_y) < 1e-9


if __name__ == "__main__":
    # 伯努利: p=0.3
    assert abs(bernoulli_pmf(0.3, 1) - 0.3) < 1e-9
    assert abs(bernoulli_pmf(0.3, 0) - 0.7) < 1e-9

    # 二项: 掷3次硬币恰2次正面 = C(3,2)(1/2)^3 = 3/8
    assert abs(binomial_pmf(3, 0.5, 2) - 0.375) < 1e-9
    # 二项分布概率和=1
    assert abs(sum(binomial_pmf(5, 0.3, k) for k in range(6)) - 1.0) < 1e-9

    # 经验分布: 样本 [1,2,2,3]
    data = [1, 2, 2, 3]
    assert abs(cdf_empirical(data, 2) - 0.75) < 1e-9

    # 示性函数期望
    assert abs(indicator_expectation(0.4) - 0.4) < 1e-9

    # 独立性: 独立时 P(x,y)=P(x)P(y)
    assert independence_by_cdf(0.3 * 0.4, 0.3, 0.4)
    assert not independence_by_cdf(0.3, 0.3, 0.4)

    print("random-variable all tests passed")

```

**PyPy 提示**: 竞赛中二项分布组合数用 math.comb(PyPy3.8+支持) 或自写预组合数表；概率求和注意用 double。连续型分布(如正态)竞赛少用，均匀分布/指数分布可直接闭式积分。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 分布列/概率计算 O(枚举取值数) |
| 空间 | O(取值数) |

### 局限

连续型随机变量单点概率为 0，不能用 P(X=x) 思考；分布函数才是严格定义。竞赛题几乎只用离散型随机变量，连续型仅出现在概率论理论题。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1030 | 2 | 递归构造练习（建模前先理解随机变量表达） | [https://www.luogu.com.cn/problem/P1030](https://www.luogu.com.cn/problem/P1030) |

## Pitfalls · 易错点

- 连续型随机变量 P(X=x)=0，判断独立性必须用分布函数而非单点概率
- 分布列概率之和必须为 1，建模时常忽略归一化
- 示性函数 E[I_A]=P(A) 是'概率转期望'的关键，方向勿搞反
- 两随机变量独立则其任意函数也独立，但 f(X,y) 与 f(X,Y) 分布未必相同

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/probability/random-variable/](https://oi-wiki.org/math/probability/random-variable/)
- 书籍 ✓ `CPH ch24 Probability (p235-244)`
