---
id: py-bigint
name: Python大整数原生支持
group: G-E-3
stage: basic
priority: P0
depth_tier: deep
---

# Python大整数原生支持

> Python int无限精度，无需手写大数类；pow(a,b,mod)内置快速幂；2**512直接算

<!-- 元信息: id=py-bigint · group=G-E-3 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

Python 的 int 类型是任意精度整数（arbitrary-precision integer），无 32/64 位溢出限制，2**512 直接算出 155 位十进制数。内置 pow(a, b, mod) 实现模幂快速幂（O(log b)），是 C++ 需要 30 行手写的高频功能。这让 Python 在高精度运算题（麦森数、大数阶乘、组合数取模）中有天然优势，无需 BigInteger 库。

## Why · 为什么

### 直觉 · Intuition

C++ 的 int/long long 固定 64 位，超 2^63 溢出。Python 的 int 底层是动态扩展的数字数组（每 30 位存一段），自动按需扩展。所以 2**1000 不会溢出，只是变慢（位数越多乘法越贵）。pow(a,b,mod) 更聪明——它用快速幂+每步取模，中间值不爆炸，速度与手写一致。

### 原理 · Principle

CPython 的 int 用 PyLongObject 存储，30 位为一个 digit，数组长度随数值增长。小整数（-5~256）有单例缓存。运算在 C 层用 GMP 风格多精度算法。pow(a,b,mod) 在 C 层用二进制快速幂实现，每步 mod 保证中间值不超过 mod²（O(log b) 次乘法，每次 O(log mod)）。2**n 在 Python 中比逐次乘更高效（用移位优化）。

### 历史 · History

Python 2 有 int（C long）和 long（任意精度）两类型，3.0 起统一为 int（均任意精度）。pow(a,b,mod) 从 Python 2 起就内置。OI Wiki 明确指出 pow(a,b,mod) 是快速幂的高效实现，2**512 直接可算。

## How · 实现

### 伪代码

```python
# 任意精度运算
x = 2 ** 512          # 155 位，不溢出
# 模幂（快速幂内置）
res = pow(a, b, mod)   # == a**b % mod 但更快不爆内存
# 大阶乘
import math
fac = math.factorial(1000)  # 2568 位
# 大组合数取模
from math import comb
print(comb(100, 50))         # C(100,50) 精确值
```

### Python 实现

```python
# Python 大整数原生支持（含自测）
import math

def fast_pow_mod(a, b, mod):
    """手写快速幂，与 pow(a,b,mod) 对比验证"""
    result = 1
    a %= mod
    while b > 0:
        if b & 1:
            result = result * a % mod
        a = a * a % mod
        b >>= 1
    return result

if __name__ == "__main__":
    # 1) 大整数无溢出
    assert 2 ** 512 == 13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084096
    # 2) pow 内置快速幂与手写一致
    assert pow(12345, 67890, 1000000007) == fast_pow_mod(12345, 67890, 1000000007)
    # 3) 大阶乘
    assert math.factorial(10) == 3628800
    assert len(str(math.factorial(1000))) == 2568  # 1000! 有 2568 位
    # 4) 组合数
    assert math.comb(100, 50) == 100891344545564193334812497256
    # 5) pow(a,b,mod) 比 a**b % mod 快（不爆中间值）
    assert pow(7, 1000000, 10**9 + 7) == fast_pow_mod(7, 1000000, 10**9 + 7)
    print("py-bigint OK")

```

**PyPy 提示**: PyPy 大整数运算常数比 CPython 略大（内部实现不同），但对 pow(a,b,mod) 这种走底层 C 的仍快。2**n 在 PyPy 用移位优化同样高效。注意 PyPy 小整数有 list-strategy 优化（list 全是 int 时用紧凑数组），大整数列表无此优化。竞赛中优先用 math.factorial/comb/pow 内置函数。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | n 位大数加法 O(n)；乘法 O(n log n)~O(n²)；pow(a,b,mod) O(log b × 乘法) |
| 空间 | O(位数) |

### 局限

1) 大数运算比固定精度慢得多（10^6 位乘法秒级），需取模的务必用 pow(a,b,mod) 不用 a**b%mod（后者先算 a**b 爆内存）；2) 浮点仍 IEEE754 双精度，大数需用 int 不能用 float；3) 竞赛中输出超大整数（如 10^6 位）IO 也慢。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1045 | 4 | 2^P-1 的位数与后 500 位，Python int 直接算 | [https://www.luogu.com.cn/problem/P1045](https://www.luogu.com.cn/problem/P1045) |
| Luogu | P1604 | 3 | 大整数加法与进制转换 | [https://www.luogu.com.cn/problem/P1604](https://www.luogu.com.cn/problem/P1604) |
| LeetCode | 2 | 3 | 链表大数加法；面试应手写链表模拟 | [https://leetcode.cn/problems/add-two-numbers/](https://leetcode.cn/problems/add-two-numbers/) |

## Pitfalls · 易错点

- 用 a**b % mod 而非 pow(a,b,mod) → a**b 先算出天文数字爆内存
- 误以为 int 有 64 位上限 → Python int 无限精度，放心用
- 浮点大数运算丢失精度 → 必须用 int 不用 float
- math.comb 不取模直接算组合数 → 大组合数位数爆炸，需取模时手写 Lucas 或快速幂
- 输出极大整数时 print 也很慢，考虑格式化字符串批量输出

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/lang/python/](https://oi-wiki.org/lang/python/)
- web ✓ [https://docs.python.org/3/library/functions.html#pow](https://docs.python.org/3/library/functions.html#pow)
- web ✓ [https://docs.python.org/3/library/stdtypes.html#int](https://docs.python.org/3/library/stdtypes.html#int)
