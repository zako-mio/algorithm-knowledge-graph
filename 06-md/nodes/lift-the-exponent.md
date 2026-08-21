---
id: lift-the-exponent
name: LTE引理
group: G-C-9
stage: advanced
priority: P2
depth_tier: standard
---

# LTE引理

> Lift the Exponent引理，求v_p(a^n-b^n)的公式，简化幂次整除问题

<!-- 元信息: id=lift-the-exponent · group=G-C-9 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

升幂引理（Lifting The Exponent Lemma，LTE）给出 p 进赋值 ν_p(x^n-y^n) 的精确公式，其中 ν_p(n) 表示 n 中素因子 p 的最高幂次。设 p 为素数，p∤x 且 p∤y。三部分结论：① (n,p)=1 时，若 p|x-y 则 ν_p(x^n-y^n)=ν_p(x-y)；若 p|x+y 且 n 为奇数则 ν_p(x^n+y^n)=ν_p(x+y)。② p 为奇素数且 p|x-y（或 p|x+y、n 奇）时，ν_p(x^n-y^n)=ν_p(x-y)+ν_p(n)。③ p=2 时，若 2|x-y 且 n 为偶数，ν_2(x^n-y^n)=ν_2(x-y)+ν_2(x+y)+ν_2(n)-1；若 4|x-y 则 ν_2(x^n+y^n)=ν_2(x+y)，ν_2(x^n-y^n)=ν_2(x-y)+ν_2(n)。应用：快速计算大幂次差的因子数量、判定整除性、求『最小 n 使某数整除 x^n-y^n』等数论题，常配合快速幂与质因数分解。

## Why · 为什么

### 直觉 · Intuition

x^n-y^n=(x-y)(x^{n-1}+x^{n-2}y+...+y^{n-1})。第一因子 x-y 贡献 ν_p(x-y)；第二因子在 x≡y (mod p) 时『恰好』≡n·x^{n-1} (mod p)，即贡献再加 ν_p(n)。p=2 的偶数 n 情况特殊，因为二项式系数 C(n,k) 在 p=2 时的 2-进赋值行为不同，需要把 n=2^a·odd 分解，逐层用 x^{2^i}+y^{2^i}≡2 (mod 4) 提取。这就是『升幂』：n 每多一个因子 p，整个式子的 p 次幂就『升』一级。

### 原理 · Principle

① ν_p 定义：p^ν_p(n)∥n（整除但不整除更高次）。② 核心分解 x^n-y^n=(x-y)Σx^i y^{n-1-i}，当 x≡y(mod p) 时和式 ≡n·x^{n-1}≠0(mod p)（因 p∤x 且 (n,p)=1）。③ 奇素数 p：用二项式展开可证若 p|x-y 则 ν_p(x^p-y^p)=ν_p(x-y)+1，归纳到 x^n-y^n 得 ν_p(x-y)+ν_p(n)。④ p=2：n 偶时 x^n-y^n=(x-y)(x+y)∏_{i≥1}(x^{2^i}+y^{2^i})，而 x^{2^i}+y^{2^i}≡2(mod 4) 每个贡献恰好 1 个因子 2，加上 (x+y) 的 ν_2 与 (x-y) 的 ν_2，再减 1（重叠修正）。⑤ 与 Hensel 引理相关（p 进提升解）。

### 历史 · History

LTE 引理的思想萌芽见于 Lucas（1878）的整除性研究（p=2 情形有轻微错误）；2006 年罗马尼亚数学家 Mihai Manea 给出系统的现代表述，主要用于奥林匹克数论。此后在数学竞赛圈（AoPS 论坛）广泛流传得名。LTE 是欧拉定理/费马小定理之外处理幂次整除问题的利器，也出现在算法竞赛数论题中。

## How · 实现

### 伪代码

```python
# 计算 v_p(x^n - y^n)
def vp(x):        # 计算 x 中 p 的幂次
  cnt = 0
  while x % p == 0:
    cnt += 1; x //= p
  return cnt

def lte(x, y, n, p):
  # 前提: p 不整除 x 和 y
  if p | (x - y):
    if p == 2 and n % 2 == 0:
      return vp(x-y) + vp(x+y) + vp(n) - 1
    return vp(x-y) + vp(n)
  if p | (x + y) and n % 2 == 1:
    if p == 2 and n == 1: return vp(x+y)
    return vp(x+y) + vp(n)
  return 0
```

### Python 实现

```python
def vp_of(n: int, p: int) -> int:
    """p 进赋值 v_p(n)."""
    cnt = 0
    while n % p == 0:
        cnt += 1
        n //= p
    return cnt


def lte(x: int, y: int, n: int, p: int) -> int:
    """LTE: 计算 v_p(x^n - y^n). 前提 p∤x, p∤y, n>=1."""
    assert n >= 1
    if p == 2:
        if n % 2 == 1:
            # 奇数 n: 2|x-y => v2(x^n-y^n)=v2(x-y); 2|x+y => v2(x^n+y^n)=v2(x+y)
            if (x - y) % 2 == 0:
                return vp_of(x - y, 2)
            if (x + y) % 2 == 0:
                return vp_of(x + y, 2)
            return 0
        else:
            # 偶数 n
            if (x - y) % 2 == 0:
                return vp_of(x - y, 2) + vp_of(x + y, 2) + vp_of(n, 2) - 1
            if (x + y) % 2 == 0:
                return vp_of(x + y, 2) + vp_of(n, 2)
            return 0
    # p 奇素数
    if (x - y) % p == 0:
        return vp_of(x - y, p) + vp_of(n, p)
    if (x + y) % p == 0:
        if n % 2 == 0:
            # n 偶数且 p|x+y: x^n-y^n ≡ (-y)^n-y^n ≡ 0 (mod p)
            return vp_of(x + y, p) + vp_of(n, p)
        return 0  # n 奇数且 p|x+y: x^n-y^n ≡ -2y^n (mod p), p∤2y
    return 0


def brute_vp(x, y, n, p):
    """直接计算 v_p(x^n-y^n) 作为对照 (仅小范围)."""
    v = abs(x) ** n - abs(y) ** n if x >= 0 and y >= 0 else None
    return None


if __name__ == "__main__":
    # 例1: v_3(10^5 - 7^5)  10-7=3 | => v3(3)+v3(5)=1+0=1
    assert lte(10, 7, 5, 3) == 1
    # 例2: v_3(10^6 - 7^6)  10-7=3,6 偶? n=6 -> 奇p: v3(3)+v3(6)=1+1=2
    assert lte(10, 7, 6, 3) == 2
    # 例3: v_7(10^3 - 3^3): 10-3=7 => v7(7)+v7(3)=1+0=1
    assert lte(10, 3, 3, 7) == 1
    # 例4: v_2(5^4 - 1^4): 5-1=4 => v2(4)+v2(6)+v2(4)-1 = 2+1+2-1=4
    assert lte(5, 1, 4, 2) == 4
    # 例5: v_2(5^3 - 3^3): 5-3=2, n 奇 => v2(2)=1
    assert lte(5, 3, 3, 2) == 1

    # 随机暴力交叉验证 (仅测满足 LTE 前提的用例: p|x-y 或 p|x+y)
    import random
    random.seed(42)
    cnt = 0
    while cnt < 400:
        x = random.randint(2, 40)
        y = random.randint(2, 40)
        if x == y:
            continue
        n = random.randint(1, 6)
        p = random.choice([2, 3, 5, 7])
        if x % p == 0 or y % p == 0:
            continue
        # 只保留满足 LTE 前提的用例 (p|x-y 或 p|x+y)
        if (x - y) % p != 0 and (x + y) % p != 0:
            continue
        val = abs(x ** n - y ** n)
        expected = vp_of(val, p)
        got = lte(x, y, n, p)
        assert got == expected, (x, y, n, p, got, expected)
        cnt += 1
    print("All tests passed.")
```

**PyPy 提示**: 大指数不要直接 pow 求 x^n（会溢出）；LTE 公式全是 O(log n) 内的整除/赋值运算。需要求幂时用 pow(x,n) 前先看是否必要，或用因数分解判断。PyPy 下 vp_of 的整除循环非常快。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(log n + log max(\|x\|,\|y\|))（赋值计算 + 判定） |
| 空间 | O(1) |

### 局限

前提 p∤x,p∤y 必须满足，否则公式不适用（需先提取公共因子）。p=2 的公式是最容易记错的：偶数 n 多一个 v_p(x+y)-1 修正项。LTE 只给 v_p 的精确值，求『整除性/因子数』需配合素数分解。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3934 | 7 | [Ynoi Easy Round 2016] 炸脖龙 I：欧拉降幂+LTE 处理指数塔 (2^2^2^... mod m) | [https://www.luogu.com.cn/problem/P3934](https://www.luogu.com.cn/problem/P3934) |
| Luogu | P5091 | 5 | 【模板】扩展欧拉定理：超大指数 a^b mod m，与 LTE 的 v_p 处理互补（指数塔题前置） | [https://www.luogu.com.cn/problem/P5091](https://www.luogu.com.cn/problem/P5091) |
| Codeforces | 1114C | 3 | Trailing Loves (or L'oeufs?!)：n! 中因子 p 的个数，v_p 赋值思想与 LTE 同一体系 | [https://codeforces.com/problemset/problem/1114/C](https://codeforces.com/problemset/problem/1114/C) |

## Pitfalls · 易错点

- 忘记 p∤x 且 p∤y 的前提（不满足时先提取公共素因子再套公式）
- p=2 且 n 为偶数时漏掉 -1 修正项
- 把 ν_p(x-y)+ν_p(n) 错记成 ν_p(x-y)·ν_p(n) 或仅 ν_p(n)
- p\|x+y 的情况忘记要求 n 为奇数
- 直接 pow 计算大幂次导致溢出；应只用公式
- x^n-y^n 的符号/绝对值：v_p 对负值同样适用，先取绝对值

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/number-theory/lift-the-exponent/](https://oi-wiki.org/math/number-theory/lift-the-exponent/)
- Wikipedia ✓ [https://en.wikipedia.org/wiki/Lifting-the-exponent_lemma](https://en.wikipedia.org/wiki/Lifting-the-exponent_lemma)
