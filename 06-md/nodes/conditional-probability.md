---
id: conditional-probability
name: 条件概率
group: G-C-15
stage: intermediate
priority: P1
depth_tier: standard
---

# 条件概率

> P(B\|A)=P(AB)/P(A)，概率乘法公式、全概率公式与贝叶斯公式，事件独立性

<!-- 元信息: id=conditional-probability · group=G-C-15 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

条件概率刻画'已知某事件发生时另一事件发生的概率'。定义 P(B|A)=P(AB)/P(A)（需 P(A)>0）。由定义直接推出概率乘法公式 P(AB)=P(A)P(B|A)；当一组事件 A_i 两两不交且并为全集时，全概率公式 P(B)=ΣP(A_i)P(B|A_i) 把复杂事件拆成互斥子情形；贝叶斯公式 P(A_i|B)=P(A_i)P(B|A_i)/P(B) 由'果'反推'因'。这是概率DP与期望DP建模最常用的工具。

## Why · 为什么

### 直觉 · Intuition

知道了一点额外信息，概率就要更新。抽卡连抽 50 发无六星后，单抽出六星的条件概率不再等于初始概率。全概率公式'分情况求和'：事件 B 的发生要归因于互斥的几类情形，按类加权求和。贝叶斯公式是'已知结果问原因'：看到 B 发生了，反推它来自哪个原因的概率。

### 原理 · Principle

条件概率 P(·|A) 本身就是一个概率函数（满足规范性、可加性）。概率乘法公式来自条件概率定义变形。全概率公式依赖划分（partition）性质：A_1..A_n 两两不交且并集为 Ω，则 B 可按 B=∪(B∩A_i) 拆为互斥事件。贝叶斯公式分子分母同时应用乘法公式与全概率公式。独立性 P(AB)=P(A)P(B) 意味着条件概率退化为无条件概率。注意：两两独立推不出相互独立（OI Wiki 正四面体骰子反例）。

### 历史 · History

条件概率概念可追溯到 18 世纪贝叶斯（Thomas Bayes）的著作（1763 年死后出版），提出反推原因的公式；皮埃尔-西蒙·拉普拉斯后来将其一般化并独立推导。全概率公式与贝叶斯公式一起构成现代统计推断（贝叶斯学派）的数学基石。

## How · 实现

### 伪代码

```python
# 条件概率
P(B|A) = P(A∩B) / P(A)   # 要求 P(A)>0

# 概率乘法公式
P(A∩B) = P(A) * P(B|A)
P(A∩B∩C) = P(A)*P(B|A)*P(C|AB)

# 全概率公式 (A1..An 为 Ω 的一个划分)
P(B) = sum_i P(A_i) * P(B|A_i)

# 贝叶斯公式
P(A_i|B) = P(A_i)*P(B|A_i) / sum_j P(A_j)*P(B|A_j)

# 独立性判定
独立 ⇔ P(AB) = P(A)*P(B)
```

### Python 实现

```python
def conditional_probability(p_ab, p_a):
    """P(B|A) = P(AB) / P(A)"""
    assert p_a > 0, "条件事件概率必须为正"
    return p_ab / p_a


def multiplication_formula(p_a, p_b_given_a):
    """概率乘法公式: P(AB) = P(A)P(B|A)"""
    return p_a * p_b_given_a


def total_probability(partitions_p, cond_p):
    """全概率公式: P(B) = sum P(A_i)P(B|A_i)
    partitions_p 为划分事件概率, 必须和为1
    """
    assert len(partitions_p) == len(cond_p)
    assert abs(sum(partitions_p) - 1.0) < 1e-9, "划分概率之和必须为1"
    return sum(p * c for p, c in zip(partitions_p, cond_p))


def bayes(prior, likelihood):
    """贝叶斯公式: 由结果B反推各原因的概率
    prior=[P(A1)..P(An)], likelihood=[P(B|A1)..P(B|An)]
    返回后验概率列表与 P(B)
    """
    evidence_p = total_probability(prior, likelihood)
    posterior = [p * l / evidence_p for p, l in zip(prior, likelihood)]
    return posterior, evidence_p


def independence_check(p_ab, p_a, p_b):
    """事件独立判定: P(AB) == P(A)P(B)"""
    return abs(p_ab - p_a * p_b) < 1e-9


if __name__ == "__main__":
    # 骰子: A=偶点(1/2), AB=可被6整除即{6}(1/6)
    # P(B|A) = (1/6)/(1/2) = 1/3, 其中B=点数可被3整除
    assert abs(conditional_probability(1 / 6, 1 / 2) - 1 / 3) < 1e-9
    assert abs(multiplication_formula(0.5, 1 / 3) - 1 / 6) < 1e-9

    # 全概率: 两工厂各占50%产量, 次品率2%/3% -> P(次品)=2.5%
    ev = total_probability([0.5, 0.5], [0.02, 0.03])
    assert abs(ev - 0.025) < 1e-9

    # 贝叶斯: 抽到次品来自工厂1的概率 = 0.5*0.02/0.025 = 0.4
    post, evidence = bayes([0.5, 0.5], [0.02, 0.03])
    assert abs(evidence - 0.025) < 1e-9
    assert abs(post[0] - 0.4) < 1e-9

    # 独立性: 两骰子各掷出6 独立
    assert independence_check(1 / 36, 1 / 6, 1 / 6)
    # 不独立: A=骰子=6(1/6), B=骰子为奇数(1/2), 两者不可能同时发生
    assert not independence_check(0, 1 / 6, 1 / 2)

    print("conditional-probability all tests passed")

```

**PyPy 提示**: 条件概率/全概率/贝叶斯多为少量浮点运算，PyPy 无性能瓶颈。若需精确避免浮点误差，可用 fractions.Fraction 处理有理数概率。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 全概率/贝叶斯 O(n)，n 为划分事件数 |
| 空间 | O(1) |

### 局限

条件事件 P(A) 必须为正；划分事件必须两两不交且并为全集，否则全概率公式失效；两两独立不等于相互独立。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1030 | 2 | 求先序排列：递归划分思想与全概率的'划分'同构 | [https://www.luogu.com.cn/problem/P1030](https://www.luogu.com.cn/problem/P1030) |
| OI Wiki | bayes-example | 2 | 正四面体骰子证明两两独立不蕴含相互独立 | [https://oi-wiki.org/math/probability/conditional-probability/](https://oi-wiki.org/math/probability/conditional-probability/) |

## Pitfalls · 易错点

- 条件概率中 P(A) 必须大于 0，P(A)=0 时条件概率无定义
- 全概率公式要求划分事件两两不交且并集为全集，缺一不可
- 事件两两独立推不出相互独立（正四面体骰子反例）
- 贝叶斯公式的'证据' P(B) 需用全概率公式计算，勿直接当已知数

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/probability/conditional-probability/](https://oi-wiki.org/math/probability/conditional-probability/)
- 书籍 ✓ `CPH ch24 Probability (p235-244)`
