---
id: quadratic-residue
name: 二次剩余
group: G-C-8
stage: advanced
priority: P2
depth_tier: standard
---

# 二次剩余

> 求 x^2≡a (mod p) 的解：Euler 判别法判定存在性，Cipolla 算法 O(log p) 求根（引入 F_p[x]/(x^2-g) 扩域），Tonelli-Shanks 亦可用

<!-- 元信息: id=quadratic-residue · group=G-C-8 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

二次剩余：对奇素数 p 与整数 a（p∤a），若存在 x 使 x^2≡a (mod p)，称 a 为模 p 的二次剩余（QR），否则为二次非剩余（QNR）。Euler 判别法：a 是二次剩余 ⟺ a^((p−1)/2)≡1 (mod p)；非剩余 ⟺ ≡−1。Cipolla 算法：随机选 b 使 w=b^2−a 为非剩余，则在扩域 F_p[√w] 中 (b+√w)^((p+1)/2) 的『实数部分』即为一个根。当 p≡3 (mod 4) 有简单公式 x≡a^((p+1)/4)；p≡1 (mod 4) 用 Cipolla 或 Tonelli-Shanks。

## Why · 为什么

### 直觉 · Intuition

开平方在有限域里不是总能开。先用 Euler 判别法『探测』是否存在根（把 (p−1)/2 次方看成奇偶性检查）。Cipolla 的精妙之处：在实数域里负数没有平方根，但在扩域 F_p[√w] 里 √w 像虚数 i 一样存在——把 (b+√w) 做 (p+1)/2 次快速幂，虚部恰好消失，剩下的实部就是解。

### 原理 · Principle

设 g 为 p 的一个二次非剩余（随机试探：一半数是非剩余）。在环 R=F_p[t]/(t^2−g) 中，令 (b+t)^((p+1)/2)=u+v·t。可以证明 v=0 且 u^2≡a 当 b^2−g=a。验证：设 t^2=g，t^p = t·t^(p−1) = t·g^((p−1)/2) = t·(−1) = −t（因 g 非剩余），故 (b+t)^p = b^p + t^p = b−t，于是 (b+t)^((p+1)/2)^2 = (b+t)^(p+1) = (b+t)^p(b+t) = (b−t)(b+t) = b^2−t^2 = b^2−g = a。因此 (b+t)^((p+1)/2) 是 a 的平方根。该值恰为无 t 项元素（虚部系数为 0）。Tonelli-Shanks：p−1=m·2^n，把 a 写成 t^2·g^e 的形式迭代降 2 阶。

### 历史 · History

二次剩余与 Legendre 符号（Legendre, 1798）、Jacobi 符号、二次互反律（Gauss, 1796 证明）构成经典数论章节。Euler 判别法得名于 Euler。现代算法由 Cipolla（1903，基于扩域）与 Tonelli（1891）、Shanks（1972，基于 2-Sylow 结构）给出，被 OI Wiki 与 CP-Algorithms 收录，用于求解高次同余与某些几何计数问题。

## How · 实现

### 伪代码

```python
# 判定存在性（a≡0 时解 x=0）
def is_quadratic_residue(a, p):
  return a == 0 or pow(a, (p-1)//2, p) == 1
# Cipolla 求根
def cipolla(a, p):
  if a == 0: return 0
  if not is_quadratic_residue(a, p): return -1
  while True:
    b = random(0..p-1)
    w2 = (b*b - a) % p
    if pow(w2, (p-1)//2, p) == p-1: break  # w2 非剩余
  # 在 R=F_p[t]/(t^2-w2) 中快速幂 (b+t)^((p+1)//2)
  return 复数快速幂的实部
```

### Python 实现

```python
import random


def is_quadratic_residue(a, p):
    """a 是否为模 p 二次剩余（a=0 视为剩余）"""
    return a == 0 or pow(a, (p - 1) // 2, p) == 1


def cipolla(a, p):
    """求 x 使 x^2≡a (mod p)，p 为奇素数。返回一个根或 -1（无解）。
    另一个根为 p - x。
    """
    if a == 0:
        return 0
    if not is_quadratic_residue(a, p):
        return -1

    # 找一个 b 使 w2 = b^2 - a 为二次非剩余
    while True:
        b = random.randrange(0, p)
        w2 = (b * b - a) % p
        if w2 != 0 and pow(w2, (p - 1) // 2, p) == p - 1:
            break

    # 扩域元素 (u, v) 表示 u + v*t，其中 t^2 = w2
    def mul(x, y):
        u1, v1 = x
        u2, v2 = y
        return ((u1 * u2 + v1 * v2 * w2) % p,
                (u1 * v2 + v1 * u2) % p)

    base = (b % p, 1)  # b + t
    res = (1, 0)
    e = (p + 1) // 2
    while e:
        if e & 1:
            res = mul(res, base)
        base = mul(base, base)
        e >>= 1
    x = res[0] % p  # 虚部应为 0
    assert (x * x - a) % p == 0
    return x


if __name__ == "__main__":
    for p in [7, 11, 13, 17, 19, 23, 29, 31, 101, 1009, 9973]:
        for a in range(p):
            if a == 0:
                assert cipolla(0, p) == 0
                continue
            if is_quadratic_residue(a, p):
                x = cipolla(a, p)
                assert x * x % p == a, (p, a, x)
            else:
                assert cipolla(a, p) == -1, (p, a)
        # 特殊 p：p≡3 mod 4 直接用公式验证
    for p in [7, 11, 19, 23, 31, 1009]:
        assert (p % 4 == 3)
        a = (p - 1) * (p - 1) % p  # 平方数
        if a == 0:
            continue
        x = pow(a, (p + 1) // 4, p)
        assert x * x % p == a

    print("All tests passed.")
```

**PyPy 提示**: 找非剩余 b 的期望次数为 2（一半候选非剩余），每次 pow 为 O(log p)。总复杂度 O(log p)。p=1e9+7 下随机取数即可，务必用固定种子保证可复现调试。乘法的扩域 2×2 模运算常数略大但整体仍是 O(log p)。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | Euler 判别 O(log p)；Cipolla O(log p)（含期望 2 次非剩余试探）；Tonelli-Shanks O(log^2 p) |
| 空间 | O(1) |

### 局限

只对奇素数模 p 定义；p=2 平凡（x≡a mod 2）。a=0 特判。Cipolla 找到非剩余 b 后必须保证 w2≠0。算法返回一个根，另一个根是 p−x（p=2 时相同）。若题目要全部解或模数为素数幂/合数，需要先解模每个素因子幂再 CRT 合并（OJ Wiki 提 Atkin 算法等）。随机算法有概率性但失败概率指数小，可重试。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P5491 | 5 | 【模板】二次剩余：Cipolla 算法求 x^2≡n 的解，含无解判定，OI Wiki 习题 | [https://www.luogu.com.cn/problem/P5491](https://www.luogu.com.cn/problem/P5491) |
| Timus | 1132 Square Root | 5 | Square Root：多组查询二次剩余模板（OI Wiki 习题引用） | [https://acm.timus.ru/problem.aspx?space=1&num=1132](https://acm.timus.ru/problem.aspx?space=1&num=1132) |
| SPOJ | MODSQRT | 6 | 多组二次剩余模板：含 p≡1 mod 4 情形，Cipolla/Tonelli-Shanks 验证 | [https://www.spoj.com/problems/MODSQRT/](https://www.spoj.com/problems/MODSQRT/) |

## Pitfalls · 易错点

- Euler 判别法只对 p∤a 成立，a=0 必须先特判
- Cipolla 的非剩余判定用 w2^(（p−1)/2)≡p−1，不是 ≡1
- 随机 b 时若 w2==0（即 b^2≡a）则 b 本身已是根，但仍可继续算法（此时 t 项退化），稳妥做法是直接返回 b
- 扩域快速幂的模乘是 2 维，注意乘法分配律写对 (u1*v2+v1*u2)
- 结果可能落在 [0,p)，有的题要求输出两个根（x 和 p−x），注意排序去重（x=0 时两者相同）
- p≡1 mod 4 时无简单公式，必须走 Cipolla/Tonelli-Shanks

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/number-theory/quad-residue/](https://oi-wiki.org/math/number-theory/quad-residue/)
- CP-Algorithms △ [https://cp-algorithms.com/algebra/sieve-of-eratosthenes.html](https://cp-algorithms.com/algebra/sieve-of-eratosthenes.html)
- 书籍 ✓ `CPH 数论部分（平方根模 p 简要提及）`
