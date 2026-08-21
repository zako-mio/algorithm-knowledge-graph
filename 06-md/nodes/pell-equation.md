---
id: pell-equation
name: 佩尔方程
group: G-C-9
stage: frontier
priority: P3
depth_tier: brief
---

# 佩尔方程

> x^2-Dy^2=1 的整数解，连分数法求解，最小解递推通项

<!-- 元信息: id=pell-equation · group=G-C-9 · stage=frontier · priority=P3 · depth_tier=brief -->

## What · 是什么

佩尔方程指不定方程 x^2-Dy^2=1（狭义 Pell 方程），其中 D 为正整数且不是完全平方数；广义 Pell 方程形如 x^2-Dy^2=N（N≠0）。解的全体与实二次整数环 x+y√D 的单位元一一对应：x+y√D 的范数恰为 x^2-Dy^2。全部整数解由基本解（fundamental solution，第一象限内 x+y√D 最小的正整数解）通过 x_k+y_k√D=(x_1+y_1√D)^k 生成，再取 ± 与倒数（对称性）即得全体解。求解用连分数：对 √D 做 PQa 展开，第一个循环节末尾（Q_k=1）处取渐近分数即得基本解。

## Why · 为什么

### 直觉 · Intuition

把方程解 (x,y) 看成二次整数 z=x+y√D。范数 N(z)=x^2-Dy^2 保持乘法（Brahmagupta 恒等式），于是『解×解=解』——知道一组解就能用乘法幂出无穷多解。佩尔方程求基本解，本质是找实二次整数环里最小的非平凡单位元。连分数之所以相关：√D 的渐近分数 p_k/q_k 是 √D 的最佳有理逼近，且恰好在循环节末尾出现 p_k^2-Dq_k^2=±1。

### 原理 · Principle

① 基本解存在性：对 √D 做简单连分数展开，其循环节长度 ℓ；若 ℓ 为偶数，第 ℓ 个余项的渐近分数 (A_{ℓ-1},B_{ℓ-1}) 即基本解；若 ℓ 为奇数，则 A_{2ℓ-1}+B_{2ℓ-1}√D=(A_{ℓ-1}+B_{ℓ-1}√D)^2，据此直接从 ℓ 处的渐近分数平方得到基本解。② 通解：x_k+y_k√D=±(x_1+y_1√D)^k，k∈Z。③ 负佩尔方程 x^2-Dy^2=-1 有解当且仅当循环节长度 ℓ 为奇数。④ PQa 算法：递推 P_{k+1}=a_kQ_k-P_k, Q_{k+1}=(D-P_{k+1}^2)/Q_k, a_{k+1}=⌊(P_{k+1}+√D)/Q_{k+1}⌋ 从 (P_0,Q_0)=(0,1) 起步，直到 (-1)^k Q_k=1。⑤ 广义方程 x^2-Dy^2=N 先求各等价类基本解，再乘上 Pell 方程解的幂生成全类。

### 历史 · History

方程以英国数学家 John Pell（17 世纪）命名，但归功实属误传——解法主要来自印度数学家 Bhāskara II（12 世纪，Chakravala 算法）和 Fermat/Euler 时代的数学。欧拉曾将方法误归于 Pell 而得名。中国古代『百鸡问题』与『牛吃草问题』也被视为佩尔方程原型。Lagrange 证明了佩尔方程总有非平凡解。

## How · 实现

### 伪代码

```python
# 用连分数（PQa）求 Pell 方程 x^2-Dy^2=1 的基本解
def pell_fundamental(D):
  assert not is_square(D)
  a0 = int(sqrt(D)); P, Q = 0, 1; a = a0
  # 递推渐近分数 p/q (注意: 与标准连分数符号对齐)
  # 用标准连分数求第 k 个渐近分数
  p_prev2, p_prev1 = 0, 1
  q_prev2, q_prev1 = 1, 0
  for k in range(...):   # 直到 Q==1 且 k>0
    p = a*p_prev1 + p_prev2
    q = a*q_prev1 + q_prev2
    # 检测循环节末尾
    P_next = a*Q - P; Q_next = (D - P_next^2)//Q
    P, Q, a = P_next, Q_next, (P_next + int(sqrt(D)))//Q_next
    if Q == 1 and k >= 1:
      return (p, q)
# 注意: 若循环节 ℓ 为奇数，(p,q) 满足 p^2-Dq^2=-1，取 (p^2+Dq^2, 2pq)
```

### Python 实现

```python
import math


def pell_fundamental(D: int):
    """返回 Pell 方程 x^2-Dy^2=1 的基本解 (x1,y1).
    D 为正且非完全平方数.
    原理: 对 sqrt(D) 做连分数(PQa)展开, 找到循环节长度 ell;
    基本解是第 ell-1 个渐近分数; ell 为奇数时该渐近分数满足
    x^2-Dy^2=-1, 平方后得到 +1 基本解."""
    r = math.isqrt(D)
    assert r * r != D, "D must not be a perfect square"
    P, Q, a = 0, 1, r
    p_pp, p_p = 0, 1   # p_{-2}, p_{-1}
    q_pp, q_p = 1, 0   # q_{-2}, q_{-1}
    convs = []
    k = 0
    while True:
        p = a * p_p + p_pp
        q = a * q_p + q_pp
        convs.append((p, q))
        p_pp, p_p = p_p, p
        q_pp, q_p = q_p, q
        P2 = a * Q - P
        Q2 = (D - P2 * P2) // Q
        P, Q = P2, Q2
        a = (P2 + r) // Q
        k += 1
        if Q == 1 and k >= 1:
            x, y = convs[k - 1]
            if x * x - D * y * y == 1:
                return (x, y)
            return (x * x + D * y * y, 2 * x * y)


def pell_solutions(D, n):
    """返回前 n 组 x^2-Dy^2=1 的正整数解."""
    x1, y1 = pell_fundamental(D)
    res = []
    x, y = 1, 0
    for _ in range(n):
        # x_k + y_k*sqrt(D) = (x1+y1*sqrt(D))^k
        x, y = x * x1 + D * y * y1, x * y1 + y * x1
        res.append((x, y))
    return res


if __name__ == "__main__":
    # D=2: 3^2-2*2^2=1 => 基本解 (3,2)
    assert pell_fundamental(2) == (3, 2)
    # D=3: 2^2-3*1^2=1 => (2,1)
    assert pell_fundamental(3) == (2, 1)
    # D=5: 9^2-5*4^2=81-80=1 => (9,4)
    assert pell_fundamental(5) == (9, 4)
    # D=7: 8^2-7*3^2=64-63=1 => (8,3)
    assert pell_fundamental(7) == (8, 3)
    # D=13: 649^2-13*180^2 = 421201-421200=1
    assert pell_fundamental(13) == (649, 180)
    # D=14: 15^2-14*4^2=225-224=1
    assert pell_fundamental(14) == (15, 4)
    # D=41: 2049^2-41*320^2=1
    assert pell_fundamental(41) == (2049, 320)

    # 通解自测: D=2 前 4 组解
    sols = pell_solutions(2, 4)
    expected = [(3, 2), (17, 12), (99, 70), (577, 408)]
    assert sols == expected, sols

    # 随机交叉验证: 暴力枚举小范围找最小解
    import random
    random.seed(7)
    for _ in range(40):
        D = random.randint(2, 80)
        if math.isqrt(D) ** 2 == D:
            continue
        x1, y1 = pell_fundamental(D)
        assert x1 * x1 - D * y1 * y1 == 1, (D, x1, y1)
        brute = None
        for x in range(1, 200000):
            y2 = x * x - 1
            if y2 % D == 0:
                y = math.isqrt(y2 // D)
                if y * y == y2 // D and y > 0:
                    brute = (x, y)
                    break
        if brute is not None:
            assert brute == (x1, y1), (D, brute, (x1, y1))
    print("All tests passed.")
```

**PyPy 提示**: D 很大时基本解 x1,y1 会指数增长（约 e^{O(√D)}），Python 大整数可处理，C++ 需 __int128 或高精。PQa 每步 O(1) 大整数乘法，循环节长度 O(√D)。用 math.isqrt 而非 float sqrt 避免精度丢失。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 连分数循环节 O(√D) 步，每步大整数乘法；实际瓶颈在大整数位数 |
| 空间 | O(√D)（仅存当前三项即可 O(1) 额外空间） |

### 局限

D 不能是完全平方数；基本解可能极大，超 long long 需 Python 大整数。负佩尔方程无解的判断没有简单判据（需要整个循环节长度）。竞赛中佩尔方程多与连分数结合出题，P3 低频。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| SPOJ | PELL2 | 4 | Pell (Mid pelling)：求 x^2-Dy^2=1 最小解，经典连分数/PQa 模板（OI Wiki 例题） | [https://www.spoj.com/problems/PELL2/](https://www.spoj.com/problems/PELL2/) |
| SPOJ | EQU2 | 5 | Yet Another Equation：广义佩尔方程 x^2-Dy^2=N（OI Wiki 例题） | [https://www.spoj.com/problems/EQU2/](https://www.spoj.com/problems/EQU2/) |

## Pitfalls · 易错点

- 忘记处理循环节长度为奇数的情况（当前得到的是 -1 解，需平方得到 +1 基本解）
- 用 float 求 √D 丢精度，必须用 math.isqrt
- D 为完全平方数时方程退化（退化为 (x+ky)(x-ky)=1），直接判掉
- 把连分数的渐近分数下标对错：基本解出现在循环节末尾，不是任何位置
- y=0 的平凡解 (±1,0) 要单独处理，正解要求 y>0

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/number-theory/pell-equation/](https://oi-wiki.org/math/number-theory/pell-equation/)
- Wikipedia ✓ [https://en.wikipedia.org/wiki/Pell%27s_equation](https://en.wikipedia.org/wiki/Pell%27s_equation)
