---
id: ext-euclidean
name: 扩展欧几里得
group: G-C-7
stage: intermediate
priority: P0
depth_tier: deep
---

# 扩展欧几里得

> 求ax+by=gcd(a,b)的一组整数解，模逆元与线性方程的基础

<!-- 元信息: id=ext-euclidean · group=G-C-7 · stage=intermediate · priority=P0 · depth_tier=deep -->

## What · 是什么

扩展欧几里得算法（EXGCD）在欧几里得算法递归过程中同时维护系数，求出一元二次不定方程 ax+by=gcd(a,b) 的一组整数解 (x,y)。它是求解模逆元（ax≡1 mod m）、线性同余方程、模意义下的除法、线性丢番图方程的通解结构的基础工具。

## Why · 为什么

### 直觉 · Intuition

每次递归 gcd(a,b)->gcd(b,a%b) 时，方程也从 ax+by=g 变成 b·x'+(a mod b)·y'=g。既然能递归求出 (x',y')，通过 a mod b = a - (a//b)·b 把等式展开比对系数，就能把 (x',y') 回代成 (x,y)。递归到底 b=0 时取 x=1,y=0 即得 g=a。

### 原理 · Principle

由 a·y' + b·(x' - (a//b)·y') = g 比对得：x=y', y=x'-(a//b)·y'。算法返回 (g,x,y)。解不唯一：所有解为 (x + t·b/g, y - t·a/g)（t∈Z）。求 ax≡1 mod m 的逆元即解 ax+my=1，有解当且仅当 gcd(a,m)=1。

### 历史 · History

扩展欧几里得算法是对欧几里得算法的自然推广，是丢番图方程理论的算法化表达，早在数论经典（如欧几里得《几何原本》关于最大公约数的部分）中已有思想雏形，现代形式在计算数论与密码学（RSA）中广泛使用。OI Wiki 与 CP-Algorithms 均给出递归与迭代两种实现。

## How · 实现

### 伪代码

```python
# 返回 (g, x, y) 满足 a*x + b*y = g = gcd(a,b)
def exgcd(a, b):
  if b == 0:
    return a, 1, 0
  g, x, y = exgcd(b, a % b)
  return g, y, x - (a // b) * y

# 迭代版: 维护两行等式 ax+by=a1, ax1+by1=b1
# 每轮 (x,x1)<-(x1, x-q*x1), (y,y1)<-(y1, y-q*y1), (a1,b1)<-(b1, a1-q*b1)
```

### Python 实现

```python
def exgcd(a, b):
    """返回 (g, x, y) 满足 a*x + b*y = g = gcd(a,b)"""
    if b == 0:
        return a, 1, 0
    g, x, y = exgcd(b, a % b)
    return g, y, x - (a // b) * y


def exgcd_iter(a, b):
    """迭代版扩展欧几里得"""
    x0, x1 = 1, 0
    y0, y1 = 0, 1
    a0, b0 = a, b
    while b0:
        q = a0 // b0
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
        a0, b0 = b0, a0 - q * b0
    return a0, x0, y0


def mod_inverse(a, m):
    """求 a 在模 m 下的逆元；无解时返回 None。
    等价于解 a*x + m*y = gcd(a,m)，要求 gcd(a,m)==1。
    """
    g, x, _ = exgcd(a, m)
    if g != 1:
        return None
    return x % m


def solve_linear_congruence(a, b, m):
    """求解 a*x ≡ b (mod m) 的最小非负整数解；无解返回 None。"""
    g, x0, _ = exgcd(a, m)
    if b % g != 0:
        return None
    x0 = (x0 * (b // g)) % m
    # 所有解 x = x0 + t*(m/g)
    step = m // g
    return x0 % step  # 最小非负代表元（模 m/g 意义下唯一）


if __name__ == "__main__":
    g, x, y = exgcd(240, 46)
    assert g == 2 and 240 * x + 46 * y == 2, (g, x, y)
    g2, x2, y2 = exgcd_iter(240, 46)
    assert g2 == 2 and 240 * x2 + 46 * y2 == 2

    g, x, y = exgcd(30, 12)
    assert g == 6 and 30 * x + 12 * y == 6

    # 模逆元测试
    assert mod_inverse(3, 7) == 5      # 3*5=15 ≡ 1 mod 7
    assert mod_inverse(4, 11) == 3     # 4*3=12 ≡ 1 mod 11
    assert mod_inverse(2, 4) is None   # gcd=2 ≠ 1 无解
    assert (mod_inverse(3, 7) * 3) % 7 == 1

    # 线性同余方程: 14x ≡ 30 (mod 100)
    sol = solve_linear_congruence(14, 30, 100)
    assert sol is not None and (14 * sol - 30) % 100 == 0
    # 3x ≡ 4 mod 7 => x=6 (3*6=18≡4)
    sol2 = solve_linear_congruence(3, 4, 7)
    assert sol2 == 6, sol2

    import random
    for _ in range(1000):
        a = random.randint(1, 10**6)
        m = random.randint(1, 10**6)
        if __import__('math').gcd(a, m) == 1:
            inv = mod_inverse(a, m)
            assert (a * inv) % m == 1, (a, m, inv)

    print("All tests passed.")
```

**PyPy 提示**: 递归版 exgcd 在 a,b 达 10^18 时递归深度约 100 层无压力。Python 的 int 无溢出，可直接处理大数。迭代版避免递归开销，PyPy 下略快。注意返回的 x 可能为负，需 x % m 规约到 [0,m)。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(log min(a,b)) — 与欧几里得算法相同的迭代次数 |
| 空间 | O(log min(a,b)) 递归栈；迭代版 O(1) |

### 局限

只能处理方程右侧是 gcd 的倍数的情形（b % g != 0 时无解）。求解模逆元要求 gcd(a,m)=1，否则需先约去公因子。返回的 x 可能是负数或绝对值大，记得取模规约。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1082 | 4 | 【模板】同余方程 ax≡1(mod b)：扩展欧几里得求逆元模板题 | [https://www.luogu.com.cn/problem/P1082](https://www.luogu.com.cn/problem/P1082) |
| Luogu | P5656 | 6 | 【模板】二元一次不定方程：求 ax+by=c 通解与最值解 | [https://www.luogu.com.cn/problem/P5656](https://www.luogu.com.cn/problem/P5656) |
| Luogu | P1516 | 5 | 青蛙的约会：化为线性同余方程用 exgcd 求最小非负整数解 | [https://www.luogu.com.cn/problem/P1516](https://www.luogu.com.cn/problem/P1516) |

## Pitfalls · 易错点

- 递归返回的 (x,y) 回代公式写错（正确：x=y', y=x'-(a//b)·y'）
- 求逆元时忘记先判断 gcd(a,m)==1，导致返回无意义的解
- 把解 x 直接返回负数而不取模规约（应 x % m）
- 处理 b%g!=0 的无解情形遗漏（求线性同余方程时）
- 通解参数化时用错步长（步长为 m/g 不是 m）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/number-theory/euclidean/](https://oi-wiki.org/math/number-theory/euclidean/)
- CP-Algorithms ✓ [https://cp-algorithms.com/algebra/extended-euclid-algorithm.html](https://cp-algorithms.com/algebra/extended-euclid-algorithm.html)
- 书籍 ✓ `CPH ch21 Number theory (p207-216)`
