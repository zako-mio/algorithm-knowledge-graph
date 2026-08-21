---
id: probability-basics
name: 概率基础
group: G-C-15
stage: intermediate
priority: P0
depth_tier: deep
---

# 概率基础

> 样本空间/事件域/概率空间三要素，古典概型与几何概型，概率公理与基本性质

<!-- 元信息: id=probability-basics · group=G-C-15 · stage=intermediate · priority=P0 · depth_tier=deep -->

## What · 是什么

概率基础是概率论的理论地基。研究随机现象需明确三个要素：样本空间 Ω（所有可能结果的集合）、事件域 F（所关心事件的集合，对补与可数并封闭）、概率函数 P（事件域到 [0,1] 的映射，满足规范性与可数可加性）。竞赛中的核心工具是古典概型 P(A)=#(A)/#(Ω)（有限等可能）与几何概型（无限情形用测度比）。它是一切概率DP、期望DP建模的理论基础。

## Why · 为什么

### 直觉 · Intuition

把随机试验的所有可能结果摆在一个集合里（样本空间），把关心的结果构成子集（事件），再给每个事件一个[0,1]的数表示发生可能性（概率）。有限等可能时，概率就是'数数'：有利结果数除以总结果数。

### 原理 · Principle

概率函数 P 满足两条公理（柯尔莫哥洛夫，1933）：①规范性 P(Ω)=1；②可数可加性：两两不交事件之并的概率等于各概率之和。由此推出单调性、容斥原理 P(A∪B)=P(A)+P(B)-P(AB)。古典概型是公理化定义在有限等可能样本空间的特例；几何概型将等可能推广到无限连续集，用长度/面积/体积之比定义概率。事件域对补、可数并封闭，这是为了保证概率运算有意义。

### 历史 · History

概率论起源于 17 世纪赌博问题的数学化（帕斯卡、费马）。早期基于直观的'等可能'古典定义存在循环定义漏洞（用'可能性'定义概率），且样本空间无限时产生歧义，典型如 Bertrand 悖论。1933 年苏联数学家柯尔莫哥洛夫出版《概率论基础》，首次给出公理化定义，终结了定义危机，使概率论成为严格数学分支。

## How · 实现

### 伪代码

```python
# 古典概型
P(A) = count(有利结果) / count(总结果)
# 要求: 有限个基本结果 + 每个结果等可能

# 几何概型
P(A) = measure(有利区域) / measure(总区域)
# measure 可为长度/面积/体积

# 容斥原理
P(A∪B) = P(A) + P(B) - P(A∩B)

# 判断事件域
# 空集∈F; A∈F ⇒ 补事件∈F; 可数并封闭
```

### Python 实现

```python
def classical_probability(favorable, total):
    """古典概型: P(A) = 有利样本点数 / 总样本点数"""
    assert total > 0, "样本空间不能为空"
    assert 0 <= favorable <= total
    return favorable / total


def uniform_probability(interval_len, subset_len):
    """几何概型(一维): P = 有利区间长度 / 总区间长度"""
    assert interval_len > 0 and 0 <= subset_len <= interval_len
    return subset_len / interval_len


def dice_greater_than_four():
    """掷骰子点数>4(即5或6)的概率: 古典概型 2/6"""
    return classical_probability(2, 6)


def two_dice_sum_7():
    """两枚骰子和为7: 有利6种(1,6)(2,5)(3,4)(4,3)(5,2)(6,1) / 总36"""
    cnt = 0
    for a in range(1, 7):
        for b in range(1, 7):
            if a + b == 7:
                cnt += 1
    return classical_probability(cnt, 36)


def inclusion_exclusion(pa, pb, pab):
    """容斥原理 P(A∪B) = P(A)+P(B)-P(A∩B)"""
    return pa + pb - pab


if __name__ == "__main__":
    # 掷骰子点数>4
    assert abs(dice_greater_than_four() - 1 / 3) < 1e-9
    # 两骰子和为7
    assert abs(two_dice_sum_7() - 1 / 6) < 1e-9
    # 硬币正面
    assert abs(classical_probability(1, 2) - 0.5) < 1e-9
    # 几何概型: [0,10]取[2,5]长3 -> 0.3
    assert abs(uniform_probability(10, 3) - 0.3) < 1e-9
    # 容斥: P(A)=0.5, P(B)=0.4, P(AB)=0.2 -> 0.7
    assert abs(inclusion_exclusion(0.5, 0.4, 0.2) - 0.7) < 1e-9
    print("probability-basics all tests passed")

```

**PyPy 提示**: 概率基础多为浮点运算，PyPy 对 double 浮点足够快。竞赛中常配合枚举计数（笛卡尔积/组合数），用 itertools.product 或组合公式直接算，避免逐样本模拟。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 古典概型计数 O(枚举量)；概率计算本身 O(1) |
| 空间 | O(1) |

### 局限

古典概型要求有限等可能；几何概型样本空间定义不明确会产出 Bertrand 悖论这类矛盾结果；等可能假设不成立时不能用古典概型（如抽卡概率）。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P2393 | 2 | yww 与校门外的树：浮点累加求期望的基础练习 | [https://www.luogu.com.cn/problem/P2393](https://www.luogu.com.cn/problem/P2393) |

## Pitfalls · 易错点

- 古典概型前提是等可能，不等可能（如不均匀骰子）时直接数数会错
- 几何概型中样本空间定义不清会导致 Bertrand 悖论式矛盾
- 容斥时忘减 P(AB) 导致重复计算
- 浮点累加用 double，避免 float 精度损失

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/probability/basic-conception/](https://oi-wiki.org/math/probability/basic-conception/)
- 书籍 ✓ `CPH ch24 Probability (p235-244)`
