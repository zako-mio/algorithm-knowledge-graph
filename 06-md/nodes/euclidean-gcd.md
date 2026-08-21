---
id: euclidean-gcd
name: 欧几里得算法(GCD)
group: G-C-7
stage: basic
priority: P0
depth_tier: deep
---

# 欧几里得算法(GCD)

> 辗转相除法求最大公约数，O(log min(a,b))，数论基础工具

<!-- 元信息: id=euclidean-gcd · group=G-C-7 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

欧几里得算法（辗转相除法）利用 gcd(a,b)=gcd(b,a mod b) 反复取模，在 O(log min(a,b)) 时间内求出两个非负整数的最大公约数。由 gcd 可 O(1) 得到 lcm(a,b)=a*b/gcd(a,b)。对多数的 gcd 可两两归纳。更相减损术与 Stein 算法（二进制 GCD）针对大整数用减法/移位代替取模。

## Why · 为什么

### 直觉 · Intuition

gcd(a,b) 也是 b 和 a-b 的公因数（更相减损），反复把大数变小，最终得到最大公约数。取模 a mod b 本质上是「一次性减掉尽量多个 b」，比逐次减法更快收敛。每次 a mod b < a/2，规模至少减半，故对数复杂度。

### 原理 · Principle

证明 gcd(a,b)=gcd(b,a mod b)：a=bq+r，d|a 且 d|b 则 d|r=a-bq；反之 d|b 且 d|r 则 d|a。故两组数的公约数集合相同。算法：while b!=0: (a,b)=(b,a%b)；返回 a。最坏情形是斐波那契数列相邻项，需要 O(log min(a,b)) 次。

### 历史 · History

欧几里得算法记录于约公元前 300 年欧几里得《几何原本》第七卷，被公认为历史上最古老且仍被广泛使用的算法之一。Knuth 在 TAOCP 中详细分析了其最坏复杂度。OI Wiki 与 CP-Algorithms 均将其列为数论基础第一课。

## How · 实现

### 伪代码

```python
function gcd(a, b):
  while b != 0:
    a, b = b, a % b
  return a

function lcm(a, b):
  return a // gcd(a, b) * b   # 先除后乘防溢出
```

### Python 实现

```python
import math


def gcd_iter(a, b):
    """迭代版欧几里得算法"""
    while b != 0:
        a, b = b, a % b
    return a


def gcd_rec(a, b):
    """递归版"""
    return a if b == 0 else gcd_rec(b, a % b)


def lcm(a, b):
    return a // gcd_iter(a, b) * b


def gcd_multi(nums):
    """多数的最大公约数：两两归纳"""
    g = 0
    for x in nums:
        g = gcd_iter(g, x)
    return g


def gcd_stein(a, b):
    """Stein 算法（二进制 GCD），用移位/减法避免取模"""
    if a == 0:
        return b
    if b == 0:
        return a
    shift = 0
    while ((a | b) & 1) == 0:
        a >>= 1
        b >>= 1
        shift += 1
    while (a & 1) == 0:
        a >>= 1
    while b:
        while (b & 1) == 0:
            b >>= 1
        if a > b:
            a, b = b, a
        b -= a
    return a << shift


if __name__ == "__main__":
    assert gcd_iter(12, 18) == 6
    assert gcd_iter(1071, 462) == 21
    assert gcd_iter(0, 5) == 5
    assert gcd_iter(7, 7) == 7
    assert gcd_rec(252, 105) == 21
    assert gcd_multi([12, 18, 30]) == 6
    assert lcm(4, 6) == 12
    assert lcm(21, 6) == 42

    # 交叉验证 Stein 与辗转相除
    import random
    random.seed(42)
    for _ in range(2000):
        a = random.randint(0, 10**9)
        b = random.randint(0, 10**9)
        assert gcd_stein(a, b) == math.gcd(a, b), (a, b)
        assert gcd_iter(a, b) == math.gcd(a, b), (a, b)
        assert lcm(a, b) == math.lcm(a, b) or math.gcd(a, b) == 0, (a, b)

    print("All tests passed.")
```

**PyPy 提示**: Python 内置 math.gcd 是 C 实现，竞赛中直接使用内置最快（Python 3.9+ 支持多参数 math.gcd(*args)）。手写递归版在 gcd_rec 上注意大数时递归深度约 O(log n) 没问题，但迭代版仍略快。Stein 算法在 Python 小整数上通常不如内置取模快。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(log min(a,b)) 次取模；最坏为斐波那契相邻项 |
| 空间 | O(1) 迭代版；递归版 O(log min(a,b)) 栈深 |

### 局限

负数需先取绝对值（约定 gcd(a,b) 对非负整数定义）。对极大整数（上千位）取模昂贵，应使用更相减损术或 Stein 算法。lcm 计算必须先除后乘防止中间溢出。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1029 | 3 | 最大公约数和最小公倍数问题：枚举 + gcd/lcm 关系 a*b=g*l | [https://www.luogu.com.cn/problem/P1029](https://www.luogu.com.cn/problem/P1029) |
| Luogu | P4549 | 3 | 【模板】裴蜀定理：多数的 gcd 与 ax+by 最小正值 | [https://www.luogu.com.cn/problem/P4549](https://www.luogu.com.cn/problem/P4549) |
| Codeforces | 75C | 1700 | Modified GCD：gcd 的因子分解与区间查询（二分 gcd 的约数） | [https://codeforces.com/problemset/problem/75/C](https://codeforces.com/problemset/problem/75/C) |

## Pitfalls · 易错点

- gcd(0,b) 处理错误（应返回 b，Python 内置同样如此）
- lcm 先乘后除导致中间溢出（应先 a//gcd*b）
- 负数输入直接取模结果与数学约定不符（应先 abs）
- 把 lcm(a,b)=a*b/gcd 的浮点除法写成整数除法导致精度丢失
- 对多数的 lcm 不能像 gcd 那样简单两两合并（lcm 会指数爆炸，但数学上正确，需用大整数）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/number-theory/euclidean/](https://oi-wiki.org/math/number-theory/euclidean/)
- CP-Algorithms ✓ [https://cp-algorithms.com/algebra/euclid-algorithm.html](https://cp-algorithms.com/algebra/euclid-algorithm.html)
- 书籍 ✓ `CPH ch21 Number theory (p207-216)`
