---
id: simpson-integration
name: Simpson 积分（自适应辛普森法）
group: G-C-16
stage: advanced
priority: P2
depth_tier: standard
---

# Simpson 积分（自适应辛普森法）

> 用二次函数逐段逼近被积函数的数值积分法，自适应地细分区间以保证精度，适合无法解析求积的定积分。

<!-- 元信息: id=simpson-integration · group=G-C-16 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

Simpson 积分是一种数值积分方法：把积分区间切成若干小段，每一段用一条过该段左端点、中点、右端点的二次函数（抛物线）近似原函数，再用二次函数的解析积分公式求和。关键变体是『自适应辛普森法』：递归地判断某段与二次函数是否足够相似，相似则直接用辛普森公式返回，不相似则从中点一分为二递归求解，从而在保证精度的前提下自动控制细分数量，避免固定步长过大/过小的问题。

## Why · 为什么

### 直觉 · Intuition

很多函数找不到初等原函数（如椭圆积分、非初等的被积函数），或者解析计算过于复杂。辛普森的核心直觉：任何『看起来顺滑』的曲线在小区间上都可以被一段抛物线近似，抛物线积分恰好有闭式公式，于是『抛物线积分之和』就逼近真实积分；分段越细、函数越平滑，逼近越好。自适应的意义在于——函数平滑的地方少切几刀，剧烈变化的地方多切几刀，把计算力花在刀刃上。

### 原理 · Principle

二次函数 f(x)=ax^2+bx+c 在区间 [l,r] 上的积分恰为 (r-l)(f(l)+f(r)+4f((l+r)/2))/6，这就是辛普森公式。普通辛普森法把 [a,b] 分成 2n 等份，交替叠加 f 的加权（端点权 1、奇数点权 4、偶数点权 2），复杂度 O(n)。误差为 -(1/90)((r-l)/2)^5·f^(4)(ξ)，即对三阶多项式精确、对更高次多项式有与步长五次方成正比的误差。自适应版本比较『整段积分』与『拆成两段的积分之和』，若差值足够小（≤15·eps）则认为该段足够像二次函数并返回带误差校正项的值（+Δ/15），否则递归细分，同时用深度上限 step 防止无限递归。

### 历史 · History

托马斯·辛普森（Thomas Simpson）于 1743 年在论文中发表此公式，因而得名（实际该思想可追溯到更早，但以他的名字流传）。它属于牛顿-柯特斯公式族（Newton–Cotes formulas，用等距节点多项式插值再积分）。OI Wiki 与 CP-Algorithms 均指出自适应版本的误差校正常数 15 的由来与优势在 Gander/Gautschi 的经典论文中有系统论述。

## How · 实现

### 伪代码

```python
function simpson(l, r):
    mid = (l + r) / 2
    return (r - l) * (f(l) + 4*f(mid) + f(r)) / 6

function asr(l, r, eps, ans, step):        # ans 为整段辛普森值
    mid = (l + r) / 2
    fl = simpson(l, mid)
    fr = simpson(mid, r)
    if |fl + fr - ans| <= 15 * eps and step < 0:
        return fl + fr + (fl + fr - ans) / 15   # 加误差校正
    return asr(l, mid, eps/2, fl, step-1) + asr(mid, r, eps/2, fr, step-1)

function calc(l, r, eps):
    return asr(l, r, eps, simpson(l, r), 12)
```

### Python 实现

```python
import math

def simpson(f, l, r):
    mid = (l + r) / 2.0
    return (r - l) * (f(l) + 4.0 * f(mid) + f(r)) / 6.0

def asr(f, l, r, eps, ans, step):
    mid = (l + r) / 2.0
    fl = simpson(f, l, mid)
    fr = simpson(f, mid, r)
    if abs(fl + fr - ans) <= 15.0 * eps and step < 0:
        return fl + fr + (fl + fr - ans) / 15.0
    return asr(f, l, mid, eps / 2.0, fl, step - 1) + asr(f, mid, r, eps / 2.0, fr, step - 1)

def adaptive_simpson(f, l, r, eps=1e-6):
    return asr(f, l, r, eps, simpson(f, l, r), 12)

if __name__ == '__main__':
    f = lambda x: math.sin(x) / x if x != 0 else 1.0  # Si(1) 无初等原函数
    v = adaptive_simpson(f, 1e-9, 1.0, 1e-9)
    print('integral sin(x)/x on (0,1] =', round(v, 9))
    assert abs(v - 0.946083070) < 1e-7
    g = lambda x: x * x                # 二次函数应精确
    print('integral x^2 on [0,2] =', adaptive_simpson(g, 0.0, 2.0, 1e-9))
    assert abs(adaptive_simpson(g, 0.0, 2.0, 1e-9) - 8.0 / 3.0) < 1e-9
    print('OK')
```

**PyPy 提示**: 递归自适应会深递归，PyPy 默认递归深度限制为 1000 层，step 上限给到 ~50 就够（本题 12 足够），一般不会爆栈；追求常数时可改手写栈迭代，但竞赛中用自适应辛普森的场景递归完全可接受。函数求值开销是主导，PyPy 下闭包/浮点性能均可，注意 f 内避免 int 除法。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 普通辛普森 O(n)；自适应辛普森取决于函数光滑度，每次递归分两半，实际层数 ≤ 深度上限，通常视为 O(迭代次数)，对光滑函数远优于固定步长 |
| 空间 | O(递归深度)，即 O(step) |

### 局限

对剧烈振荡、存在尖峰/间断、或在区间端点为奇异（如 1/sqrt(x)）的函数精度差甚至发散，自适应判断会反复细分直到深度上限；辛普森公式对高振荡函数本质失效，应改用专门方法（如解析处理奇异点、变换换元）。误差估计依赖 f^(4) 存在，阶跃函数下不成立。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P4525 | 3 | 自适应辛普森法模板题，直接在给定区间上 calc 即可 | [https://www.luogu.com.cn/problem/P4525](https://www.luogu.com.cn/problem/P4525) |
| HDU | HDU1724 Ellipse | 3 | 椭圆积分无法解析求原函数，是自适应辛普森经典入门题 | [https://acm.hdu.edu.cn/showproblem.php?pid=1724](https://acm.hdu.edu.cn/showproblem.php?pid=1724) |
| Luogu | P4207 | 6 | NOI2005 月下柠檬树：投影面积分段为圆锥台侧面 + 直线梯形，用自适应辛普森求和 | [https://www.luogu.com.cn/problem/P4207](https://www.luogu.com.cn/problem/P4207) |

## Pitfalls · 易错点

- 直接比较 \|fl+fr-ans\|<=eps 而不用 15*eps 和 /15 误差校正项，精度会系统性偏差
- step（递归深度）必须带，否则病态函数无限细分直至 RecursionError
- 被积函数在端点无定义（如除 0）需特殊处理（如取极限值），否则浮点除零或 NaN
- eps 传得过小导致递归过深；实用中双精度下 eps~1e-9 已是极限
- 对周期/振荡函数误用辛普森会给出看似合理的错误值，务必先画图或做解析估计

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/numerical/integral.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/numerical/integral.md)
- CP-Algorithms ✓ [https://cp-algorithms.com/num_methods/simpson-integration.html](https://cp-algorithms.com/num_methods/simpson-integration.html)
