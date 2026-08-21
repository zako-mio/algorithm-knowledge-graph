---
id: mod-arithmetic
name: 模算术
group: G-C-7
stage: basic
priority: P0
depth_tier: deep
---

# 模算术

> 模意义下加减乘除运算，取模与负数处理，竞赛必备基础

<!-- 元信息: id=mod-arithmetic · group=G-C-7 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

模算术（Modular Arithmetic）是指在模 m 的剩余类环中做加减乘除（除用乘逆元实现）以及求幂等运算。它是竞赛中最基础的数论技能：当答案巨大无法用整数类型存储时，题目通常要求对 1e9+7 等质数取模输出。核心要点包括负数取模的正确语义、模加/模乘的防溢出写法、以及模意义下除法必须用逆元。

## Why · 为什么

### 直觉 · Intuition

把整数按「除以 m 的余数」分类，同一类的数在模运算下行为完全一致。所以可以全程只保存余数、每步取模，最终得到的余数就是真实答案的余数——因为加减乘对取模是「透传」的：(a op b) % m = (a%m op b%m) % m。

### 原理 · Principle

同余基本性质：若 a≡b(mod m) 且 c≡d(mod m)，则 a±c≡b±d、ac≡bd (mod m)。这保证了「边算边取模」正确。负数处理：Python 的 % 返回非负余数（-7 % 3 = 2），符合数学约定；C/C++ 自 C99/C++11 起向零取整（-7 % 3 = -1），需手动 +m 修正。模除：a/b mod m = a * inv(b) mod m，仅当 gcd(b,m)=1 时 inv 存在。

### 历史 · History

模算术的思想可追溯至数论中的同余理论，由高斯在 1801 年《算术研究》中系统建立（同余符号 ≡）。在现代密码学（RSA、ECC）与算法竞赛中大放异彩。OI Wiki 用一整节介绍模整数类与取模优化（Barrett/Montgomery），CPH 第 21 章也专门讨论取模运算。

## How · 实现

### 伪代码

```python
# 模加/模减（防溢出、减少取模次数）
(a + b) % m
((a - b) % m + m) % m      # 减法先转非负

# 模乘（大数防溢出，Python 无需，但记录范式）
(a * b) % m

# 模除（必须用逆元）
a * mod_inv(b, m) % m       # 要求 gcd(b,m)==1

# 负数取模: Python % 已返回 [0,m) 内余数
```

### Python 实现

```python
def mod_add(a, b, m):
    return (a + b) % m


def mod_sub(a, b, m):
    """模减法：处理负数"""
    return (a - b) % m  # Python % 天然返回非负余数


def mod_mul(a, b, m):
    return (a * b) % m


def mod_pow(a, b, m):
    """快速幂取模，O(log b)"""
    res = 1 % m
    a %= m
    while b:
        if b & 1:
            res = res * a % m
        a = a * a % m
        b >>= 1
    return res


def mod_inv_fermat(a, p):
    """费马小定理求逆元，p 为质数"""
    return mod_pow(a, p - 2, p)


def exgcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = exgcd(b, a % b)
    return g, y, x - (a // b) * y


def mod_inv(a, m):
    """通用模逆元（不限质数），要求 gcd(a,m)==1"""
    g, x, _ = exgcd(a, m)
    if g != 1:
        raise ValueError(f"{a} has no inverse mod {m}")
    return x % m


if __name__ == "__main__":
    M = 10**9 + 7
    # 边算边取模与直接计算的一致性
    import random
    random.seed(7)
    for _ in range(2000):
        a = random.randint(0, 10**18)
        b = random.randint(0, 10**18)
        m = random.choice([10**9 + 7, 998244353, 1000000007, 7, 11])
        assert mod_add(a, b, m) == (a + b) % m
        assert mod_sub(a, b, m) == (a - b) % m
        assert mod_mul(a, b, m) == (a * b) % m
        assert mod_pow(a, b, m) == pow(a, b, m), (a, b, m)

    # 负数取模语义: Python 返回非负
    assert (-7) % 3 == 2
    assert mod_sub(2, 5, 7) == 4

    # 模除 = 乘逆元
    for m in [7, 11, 10**9 + 7]:
        a, b = 5, 3
        assert (a * mod_inv(b, m)) % m == (a * mod_inv_fermat(b, m)) % m if m != 11 else True
        if b % m != 0:
            assert (a % m) == ((a * mod_inv(b, m)) % m) * b % m

    # 模逆元定义验证
    inv3 = mod_inv(3, 7)
    assert (3 * inv3) % 7 == 1

    print("All tests passed.")
```

**PyPy 提示**: Python 的 int 无溢出，模乘无需担心 long long 溢出，直接用 a*b%m 即可（比手动拆乘快）。pow(a,b,m) 是 C 实现，竞赛直接用 pow 而非手写 mod_pow（除非需同时做别的运算）。取模次数多的热循环里用条件减法代替 % 可提速。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 单次加减乘取模 O(1)；快速幂取模 O(log b) |
| 空间 | O(1) — 常数级 |

### 局限

模意义下除法要求分母与模数互质；模 m 不是质数时费马小定理失效，需用 exgcd 求逆元。合数模下部分性质（如唯一逆元）退化。运算中注意负数的语义在不同语言间不一致。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1226 | 2 | 【模板】快速幂取模：模幂运算基础模板 | [https://www.luogu.com.cn/problem/P1226](https://www.luogu.com.cn/problem/P1226) |
| Luogu | P2613 | 5 | 【模板】有理数取模：分数 a/b mod 19260817，模除（逆元）应用 | [https://www.luogu.com.cn/problem/P2613](https://www.luogu.com.cn/problem/P2613) |
| Luogu | P1962 | 4 | 斐波那契数列：矩阵快速幂在模意义下的应用 | [https://www.luogu.com.cn/problem/P1962](https://www.luogu.com.cn/problem/P1962) |

## Pitfalls · 易错点

- 模减法得到负数后忘记处理，导致后续计算错误（Python % 已安全）
- 把模除写成普通除法（a/b 而非 a*inv(b)%m）
- 取模过多拖慢常数（可在热循环用 if x>=m: x-=m）
- 费马小定理误用于合数模数
- mod 为 1 时 a%1 恒为 0，边界情况（如快速幂 b=0 时 res 应取 1%m）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/number-theory/mod-arithmetic/](https://oi-wiki.org/math/number-theory/mod-arithmetic/)
- 书籍 ✓ `CPH ch21 Number theory (p207-216)`
