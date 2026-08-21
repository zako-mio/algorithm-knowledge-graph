---
id: newton-method
name: 牛顿迭代法
group: G-C-16
stage: advanced
priority: P2
depth_tier: standard
---

# 牛顿迭代法

> 用切线迭代求函数零点：x_{i+1}=x_i−f(x_i)/f'(x_i)，平方收敛，用于求平方根/整数平方根/高精度开方及多项式牛顿迭代基础

<!-- 元信息: id=newton-method · group=G-C-16 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

牛顿迭代法（Newton–Raphson）求 f(x)=0 的近似根：给定初值 x0，反复迭代 x_{i+1}=x_i−f(x_i)/f'(x_i)（即过 (x_i,f(x_i)) 的切线与 x 轴交点），收敛率是平方级（每轮有效位数翻倍）。要求 f 连续可微、初值足够接近根。典型应用：①浮点平方根：f(x)=x²−n ⇒ x_{i+1}=(x_i+n/x_i)/2，按 eps 停止；②整数平方根 isqrt(n)（求最大 x 使 x²≤n）：整数迭代并加入'若上轮在减小而这轮要增大则停止'的防振荡条件；③高精度大整数开方（BigInteger）：初值取 2^{⌈bit/2⌉} 可大幅加速（10^1000 时 60ms vs 120ms）。多项式牛顿迭代（形式幂级数求逆/开方/exp）是更高级延伸。

## Why · 为什么

### 直觉 · Intuition

几何意义：在曲线上一点作切线，切线与 x 轴的交点通常比当前点更接近根。对平滑函数，越接近根切线越准，误差的平方被压缩（泰勒展开一阶近似误差是 (x−r)² 量级），所以每步有效位数翻倍。

### 原理 · Principle

由导数定义 f'(x_i)≈(f(x_i)−0)/(x_i−x_{i+1})（切线与 x 轴交点为 x_{i+1}）解得递推式。收敛分析：设 r 为根，误差 e_i=x_i−r，泰勒展开 f(r)=f(x_i)+f'(x_i)(r−x_i)+O((r−x_i)²) 且 f(r)=0，代入迭代式得 e_{i+1}≈(f''/(2f'))e_i²，平方收敛。求平方根：f=x²−n，f'=2x，代入得 x_{i+1}=(x_i+n/x_i)/2（即巴比伦/海伦公式）。整数版终止条件：整数除法可能让 x 在根附近振荡，加入 decreased 标记：若上轮 x 减小且本轮要增大则停止，或 x==nx 停止。大整数版初值 x0=2^{bits/2}（bits=位数），保证二次收敛起点靠近根。

### 历史 · History

牛顿法由 Isaac Newton 于 1664-1671 年发明（求解非线性方程），Joseph Raphson 几年后独立给出更简单的递推形式且更早发表，故常称 Newton–Raphson。其高精度开方与多项式形式幂级数迭代在计算机代数与算法竞赛（多项式全家桶）中广泛使用（OI Wiki、CP-Algorithms 均有专页）。

## How · 实现

### 伪代码

```python
# 浮点平方根
def sqrt_newton(n):
    x = 1
    while True:
        nx = (x + n / x) / 2
        if abs(x - nx) < eps: break
        x = nx
    return x

# 整数平方根
def isqrt_newton(n):
    x = 1; decreased = False
    while True:
        nx = (x + n // x) // 2
        if x == nx or (nx > x and decreased): break
        decreased = nx < x
        x = nx
    return x
```

### Python 实现

```python
# -*- coding: utf-8 -*-
# 牛顿迭代：浮点平方根 / 整数平方根 / 通用零点

def sqrt_newton(n, eps=1e-15):
    """浮点 sqrt，平方收敛。"""
    if n < 0:
        raise ValueError('n must be >= 0')
    x = 1.0
    while True:
        nx = (x + n / x) / 2
        if abs(x - nx) < eps:
            return nx
        x = nx


def isqrt_newton(n):
    """整数平方根：最大 x 使 x*x <= n。防振荡版本。"""
    if n < 0:
        raise ValueError('n must be >= 0')
    if n < 2:
        return n
    x = 1
    decreased = False
    while True:
        nx = (x + n // x) // 2
        if x == nx or (nx > x and decreased):
            return x
        decreased = nx < x
        x = nx


def newton_root(f, fp, x0, eps=1e-12, max_iter=200):
    """通用牛顿迭代：f 为函数，fp 为其导数，x0 初值。"""
    x = x0
    for _ in range(max_iter):
        fx = f(x)
        d = fp(x)
        if d == 0:
            break
        nx = x - fx / d
        if abs(nx - x) < eps:
            return nx
        x = nx
    return x


if __name__ == '__main__':
    import math
    import random
    random.seed(0)
    for _ in range(300):
        n = random.randint(0, 10**12)
        assert isqrt_newton(n) == math.isqrt(n), (n, isqrt_newton(n), math.isqrt(n))
        f = float(n)
        assert abs(sqrt_newton(f) - math.sqrt(f)) < 1e-9, n
    # 特殊值
    assert isqrt_newton(0) == 0
    assert isqrt_newton(1) == 1
    assert sqrt_newton(4) == 2.0
    assert abs(sqrt_newton(2) - math.sqrt(2)) < 1e-12
    # 通用零点：解 x^2 - 3 = 0（取正根），用 x0=1
    r = newton_root(lambda x: x * x - 3, lambda x: 2 * x, 1.0)
    assert abs(r - math.sqrt(3)) < 1e-9, r
    # 立方根：x^3 - 8 = 0
    r2 = newton_root(lambda x: x ** 3 - 8, lambda x: 3 * x * x, 1.5)
    assert abs(r2 - 2.0) < 1e-9, r2
    print('newton-method tests passed')

```

**PyPy 提示**: 整数版用整数除法 O(1) 每步，log 次迭代，PyPy 处理 10^18 与 Python int 任意精度均可。大整数开方（几千位）建议 BigInteger 初值 2^{bits//2} 加速。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 平方收敛：约 O(log log(1/eps)) 次迭代，每次 O(1)（或大整数乘法 O(M(b))） |
| 空间 | O(1) |

### 局限

需初值靠近根且 f' 不为 0；振荡/不收敛时可能发散（如初值选在极值点）。整数版终止条件依赖整数除法舍入。通用零点求多个根需多次取不同初值。多项式牛顿迭代是形式幂级数范畴，另有专题。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| LeetCode | 69 | 2 | x 的平方根：整数平方根（牛顿或二分）模板题 | [https://leetcode.cn/problems/sqrtx/](https://leetcode.cn/problems/sqrtx/) |
| UVa | 10428 | 4 | The Roots：多项式求根（牛顿/数值方法组合），需精度控制 | [https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=16&page=show_problem&problem=1369](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=16&page=show_problem&problem=1369) |

## Pitfalls · 易错点

- 浮点版初值 x=1 对 n 远大于 1 或小于 1 的收敛略慢，但平方收敛仍快；对 n=0 单独处理避免除零
- 整数版 must 处理 x==nx 与振荡（decreased 标志），否则死循环
- f'(x)=0 时迭代发散，需要容错
- 大整数开方不设好初值会显著变慢；bits 按 2 的对数取整
- eps 过小可能导致浮点震荡不终止，限制迭代次数

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/numerical/newton/](https://oi-wiki.org/math/numerical/newton/)
- CP-Algorithms ✓ [https://cp-algorithms.com/num_methods/roots_newton.html](https://cp-algorithms.com/num_methods/roots_newton.html)
