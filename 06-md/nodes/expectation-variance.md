---
id: expectation-variance
name: 期望与方差
group: G-C-15
stage: intermediate
priority: P0
depth_tier: deep
---

# 期望与方差

> 离散/连续期望定义，期望线性性与乘积期望，方差/标准差，条件期望与全期望公式

<!-- 元信息: id=expectation-variance · group=G-C-15 · stage=intermediate · priority=P0 · depth_tier=deep -->

## What · 是什么

期望 E[X]=Σx_i·p_i（离散）或 ∫xf(x)dx（连续，需绝对收敛）描述随机变量的'平均'取值；方差 Var(X)=E[(X-E[X])²]=E[X²]-(E[X])² 描述离散程度，标准差 σ=√Var 是其算术平方根。核心性质：期望线性性 E(aX+b)=aE[X]+b、E(X+Y)=E[X]+E[Y]（无需独立性）；独立时 E(XY)=E[X]E[Y]。条件期望 E[X|Y=y] 与全期望公式 E[X]=E[E[X|Y]] 是期望DP与随机过程分析的基石。

## Why · 为什么

### 直觉 · Intuition

期望就是'按概率加权平均'：把每个取值乘以它发生的概率再求和。线性性是期望最强大的性质——复杂随机变量可以拆成简单部分分别算期望再相加，不用先求整体分布（如 n 个独立变量的和，直接求和各部分期望）。期望DP的核心：从某状态出发的期望 = 各转移概率×目标状态期望 + 本步代价。

### 原理 · Principle

期望线性性来自可数可加性：E[X+Y]=∫(x+y)dF=E[X]+E[Y]，不需要独立性。乘积期望需独立性：E(XY)=E[X]E[Y] 当 X,Y 独立（不独立时不成立，如 Y=X²）。方差性质：Var(aX+b)=a²Var(X)；Var(X+Y)=Var(X)+2Cov(X,Y)+Var(Y)，独立时协方差为 0 才可拆分。全期望公式 E[X]=E[E[X|Y]]：先把期望分层求（给定 Y 的条件期望），再对 Y 求期望，是解期望递归方程的标准手法（HDU 5984 Pocky 例题）。

### 历史 · History

期望概念源于 17 世纪荷兰数学家惠更斯对赌博问题的研究（1657 年《论赌博中的计算》），其'公平赌注'思想成为现代风险理论的源头。方差由英国统计学家高尔顿（1880s）与皮尔逊系统发展，与协方差、相关系数一起构成描述性统计的核心工具。

## How · 实现

### 伪代码

```python
# 期望(离散)
E[X] = sum x_i * p_i
# 期望(连续)
E[X] = ∫ x f(x) dx

# 线性性(无需独立)
E[aX+b] = a*E[X] + b
E[X+Y] = E[X] + E[Y]

# 独立时乘积期望
E[XY] = E[X]*E[Y]

# 方差
Var(X) = E[(X-E[X])^2] = E[X^2] - (E[X])^2
Var(aX+b) = a^2 Var(X)

# 全期望公式
E[X] = E[E[X|Y]] = sum_y P(Y=y) * E[X|Y=y]

# 期望DP逆推模板
f[target] = 0
for S in reverse order:
  f[S] = sum(p(S->next) * f[next]) + cost(S)
```

### Python 实现

```python
import math


def expectation_discrete(values, probs):
    """离散期望 E[X] = sum x_i p_i"""
    assert len(values) == len(probs)
    assert abs(sum(probs) - 1.0) < 1e-9, "概率之和必须为1"
    return sum(x * p for x, p in zip(values, probs))


def expectation_linear(ex, ey):
    """期望线性性: E[X+Y] = E[X]+E[Y] (无需独立)"""
    return ex + ey

def variance_discrete(values, probs):
    """方差 Var(X) = E[X^2] - (E[X])^2"""
    ex = expectation_discrete(values, probs)
    ex2 = expectation_discrete([x * x for x in values], probs)
    return ex2 - ex * ex


def std_dev(values, probs):
    """标准差 σ = sqrt(Var)"""
    return math.sqrt(variance_discrete(values, probs))


def expectation_product_independent(ex, ey):
    """独立时 E[XY] = E[X]E[Y]"""
    return ex * ey


def law_of_total_expectation(cond_ex, probs):
    """全期望公式 E[X]=E[E[X|Y]] = sum P(Y=y_i) E[X|Y=y_i]"""
    assert abs(sum(probs) - 1.0) < 1e-9
    return sum(e * p for e, p in zip(cond_ex, probs))


if __name__ == "__main__":
    # 骰子期望 = 3.5
    vals = list(range(1, 7)); probs = [1 / 6] * 6
    assert abs(expectation_discrete(vals, probs) - 3.5) < 1e-9
    # 骰子方差 = 35/12
    assert abs(variance_discrete(vals, probs) - 35 / 12) < 1e-9
    # 线性性: 两骰子总和期望 7
    assert abs(expectation_linear(3.5, 3.5) - 7.0) < 1e-9
    # 独立乘积期望: 两骰子乘积期望 = 3.5*3.5 = 12.25
    assert abs(expectation_product_independent(3.5, 3.5) - 12.25) < 1e-9
    # 全期望: E[X|H]=2, E[X|T]=4, 各1/2 -> 3
    assert abs(law_of_total_expectation([2, 4], [0.5, 0.5]) - 3.0) < 1e-9
    # 标准差
    assert abs(std_dev(vals, probs) - math.sqrt(35 / 12)) < 1e-9
    print("expectation-variance all tests passed")

```

**PyPy 提示**: 期望DP通常状态量 O(n)~O(n²)，浮点运算 PyPy 足够。高斯消元解有环期望方程组时注意 eps。多次累乘概率用 double，避免 float 精度灾难。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 期望DP O(状态数×转移数)；高斯消元 O(n³) |
| 空间 | O(状态数) |

### 局限

期望不存在的分布（非绝对收敛，如柯西分布）竞赛不出现；期望线性性成立但方差拆分需协方差为 0；期望DP存在环依赖时必须用高斯消元，状态多时不可行。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P4316 | 3 | 绿豆蛙的归宿：DAG上期望DP逆推，期望DP入门题 | [https://www.luogu.com.cn/problem/P4316](https://www.luogu.com.cn/problem/P4316) |
| Luogu | P1365 | 3 | WJMZBMR打osu! / Easy：组合长度平方期望的递推 | [https://www.luogu.com.cn/problem/P1365](https://www.luogu.com.cn/problem/P1365) |
| HDU | 5984 | 4 | Pocky：全期望公式 + 积分方程，期望DP高级应用 | [https://acm.hdu.edu.cn/showproblem.php?pid=5984](https://acm.hdu.edu.cn/showproblem.php?pid=5984) |

## Pitfalls · 易错点

- 期望线性性无需独立性，但乘积期望 E(XY)=E[X]E[Y] 需要独立，常被误用
- 方差不能简单拆分：Var(X+Y)=Var(X)+Var(Y) 仅在协方差为 0 时成立
- 期望DP逆推方向：目标状态期望=0，从目标倒推到起点
- 概率与期望混合时，'+1'（每步代价）容易漏加
- 浮点累乘误差：先乘再除易丢精度，用 double 并控制 eps

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/probability/exp-var/](https://oi-wiki.org/math/probability/exp-var/)
- 书籍 ✓ `CPH ch24 Probability (p235-244)`
