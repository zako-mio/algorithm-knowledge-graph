---
id: big-integer
name: 高精度(大整数)
group: G-C-18
stage: intermediate
priority: P0
depth_tier: deep
---

# 高精度(大整数)

> 大整数加减乘除：Python 原生 int 无上限直接可用；C++/PyPy 需数组模拟，乘法 O(n^2) 可 Karatsuba/FFT 加速，压位优化常数

<!-- 元信息: id=big-integer · group=G-C-18 · stage=intermediate · priority=P0 · depth_tier=deep -->

## What · 是什么

高精度（bignum / arbitrary-precision arithmetic）：对超出内建整型位宽的大整数进行四则运算。C++ 需要手写（用 string/数组存储，从低位开始按竖式运算，或压位存 4~9 位一组）；Python 内建 int 是任意精度，直接支持任意大小的 + - * // % ** 与位运算，底层已做 Karatsuba/Toom/FFT 级优化，竞赛中几乎不用手写，但需了解 Python 大数的复杂度特性（乘法大数用 Karatsuba，更大用 Toom/FFT，比朴素 O(n^2) 快很多）。PyPy 的 int 同样是任意精度但内部实现不同，大数乘法性能与 CPython 有差异。核心知识：数组竖式算法、压位、快速乘法（Karatsuba、FFT/NTT）。

## Why · 为什么

### 直觉 · Intuition

数太大内建类型装不下时，用数组存每一位，把「竖式计算」程序化。Python 则把这件事内置了：int 对象不限长度，CPython 用 digit 数组（每个 digit 存 15/30 位）+ 支持多精度算术，所以 Python 选手只需知道什么时候会爆范围、大数运算多快。

### 原理 · Principle

1) 存储：C++ 用数组 a[]，a[i] 存第 i 位（低位在前），或压位：每格存 base=10^4/10^8/10^9 的一「位」，减少数组长度与进位次数。2) 加法：逐位相加+进位 O(n)。3) 减法：借位 O(n)。4) 乘法：朴素 O(n^2) 逐位卷积；Karatsuba 分治 T(n)=3T(n/2)+O(n)=O(n^1.585)；用 FFT/NTT 做卷积可到 O(n log n)。5) 除法：试商法，估商（如 double 估商 + 回退修正）O(n^2)。Python 内建 int 乘法对 2^64~2^2^30 范围分别走 grade-school、Karatsuba、Toom-Cook3、FFT（NTT）等不同算法。

### 历史 · History

任意精度算术自计算机早期即存在（如 1960 年代 LISP 的 bignum）；现代语言（Python、Java BigInteger、Golang math/big）普遍内置。竞赛语境下 C++ 选手长期手写模板；Karatsuba(1960)、Schönhage-Strassen(1971)、FFT 卷积（Rader/Bluestein 等）构成现代大数乘法演进。Python 3.11 起 CPython 引入渐进式大数乘法（deviation-based scaling），Python 3.12 引入幂运算的优化，大数性能持续改进。PyPy 使用 RPython 大整数实现，基准与大数乘法行为和 CPython 不同。

## How · 实现

### 伪代码

```python
# 竖式加法（压位，base=B），a,b 为低位在前数组
def add(a, b):
    c, carry, i = [], 0, 0
    while i < len(a) or i < len(b) or carry:
        v = carry
        if i < len(a): v += a[i]
        if i < len(b): v += b[i]
        c.append(v % B); carry = v // B; i += 1
    return c

# 竖式乘法 O(n*m)
def mul(a, b):
    c = [0] * (len(a) + len(b))
    for i, x in enumerate(a):
        carry = 0
        for j in range(len(b)):
            cur = c[i+j] + x*b[j] + carry
            c[i+j] = cur % B; carry = cur // B
        c[i+len(b)] += carry
    while len(c) > 1 and c[-1] == 0: c.pop()
    return c
```

### Python 实现

```python
BASE = 10000  # 压位基底：每格存 4 位十进制


def str_to_blocks(s):
    s = s.lstrip('0') or '0'
    blocks = []
    for i in range(len(s), 0, -4):
        blocks.append(int(s[max(0, i - 4):i]))
    return blocks


def blocks_to_str(b):
    if not b:
        return '0'
    res = str(b[-1])
    for x in reversed(b[:-1]):
        res += f'{x:04d}'
    return res


def add(a, b):
    i = carry = 0
    c = []
    while i < len(a) or i < len(b) or carry:
        v = carry
        if i < len(a):
            v += a[i]
        if i < len(b):
            v += b[i]
        c.append(v % BASE)
        carry = v // BASE
        i += 1
    return c


def sub(a, b):  # 要求 a >= b
    i = borrow = 0
    c = []
    while i < len(a) or borrow:
        v = a[i] - borrow - (b[i] if i < len(b) else 0)
        borrow = 0
        if v < 0:
            v += BASE
            borrow = 1
        c.append(v)
        i += 1
    while len(c) > 1 and c[-1] == 0:
        c.pop()
    return c


def mul(a, b):
    c = [0] * (len(a) + len(b))
    for i, x in enumerate(a):
        carry = 0
        for j in range(len(b)):
            cur = c[i + j] + x * b[j] + carry
            c[i + j] = cur % BASE
            carry = cur // BASE
        c[i + len(b)] += carry
    while len(c) > 1 and c[-1] == 0:
        c.pop()
    return c


def main():
    # 与内建 int 对拍验证压位四则
    import random
    random.seed(42)
    for _ in range(200):
        x = random.randint(0, 10**30)
        y = random.randint(0, 10**30)
        assert int(blocks_to_str(add(str_to_blocks(str(x)), str_to_blocks(str(y))))) == x + y
        if x >= y:
            assert int(blocks_to_str(sub(str_to_blocks(str(x)), str_to_blocks(str(y))))) == x - y
        assert int(blocks_to_str(mul(str_to_blocks(str(x)), str_to_blocks(str(y))))) == x * y
    # Python 内建大整数直接可用（竞赛常用）
    a = 10**500
    assert (a * a) == 10**1000
    assert len(str(2**1000)) == 302
    print("big-integer OK")


if __name__ == "__main__":
    main()

```

**PyPy 提示**: Python 选手直接内建 int：CPython 3.11+ 与 PyPy 都支持任意精度。大数乘法上 CPython 有 Karatsuba 与更高级算法，PyPy 的 RPython 大整数实现对于 1e5 位级乘法可能比 CPython 慢，但竞赛大数题通常 n≤10^4~10^5 位，两者都够。PyPy 下 int 转 str 对大数也快（Str 优化）。若真遇到 Python 手写高精度（少见，一般是需自定义输出格式或配合 NTT 的卷积题），竖式模板如上；压位时注意进位溢出（PyPy 也是 int 无上限，无溢出问题）。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 加/减 O(n)；朴素乘法 O(n·m)（压位后 O((n/4)^2)）；Karatsuba O(n^1.585)；FFT/NTT 乘法 O(n log n)；Python 内建乘法底层自适应 |
| 空间 | O(n) 存数字（压位后数组长度 n/4~n/9） |

### 局限

C++ 手写大数除法最易出错（试商/估商/修正），Python 直接用 // 与 % 无此烦恼。Python 内建 int 无上限但运算有常量差异：大数乘法 O(n^1.585)~O(n log n) 而非线性，需要乘 10^5 位级大数时仍会较慢。浮点转大整数注意精度（int(1e20) 与真值不同）。PyPy 与 CPython 的大数速度不同，极限题需实测。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1601 | 1 | A+B Problem（高精）：Python 直接 int 秒过，C++ 高精度加法入门 | [https://www.luogu.com.cn/problem/P1601](https://www.luogu.com.cn/problem/P1601) |
| Luogu | P1932 | 5 | A+B*A-B/A/B：高精度四则运算综合，Python 内建 int 一行解决 | [https://www.luogu.com.cn/problem/P1932](https://www.luogu.com.cn/problem/P1932) |
| Luogu | P1045 | 4 | 麦森数：2^p-1 求位数+末500位，Python 用 pow(2,p) 直接算，理解十进制位数=floor(p*log10(2))+1 | [https://www.luogu.com.cn/problem/P1045](https://www.luogu.com.cn/problem/P1045) |

## Pitfalls · 易错点

- Python 中 int(1e20) 是把 float 转 int，1e20 已超 float 精确表示范围，大数请用字符串/十进制字面量
- // 与 % 对负数语义是向下取整，需商向零取整的场合要自己调整
- C++ 手写高精度：反转存储（低位在前）后所有运算从 a[0] 开始；忘除前导零会输出多 0 或格式错误
- 压位输出必须用 %0{d} 补零（万进制补 4 位），否则 '1 0023' 会输出 '123'
- Python 做 10^5 位级大数乘法仍可能超时，需用 NTT/FFT（如 Python 的 numpy 或手写 NTT）
- 2^1000 之类超大数求十进制位数用 math.log10 会有浮点误差，安全做法是 len(str(x)) 或取整公式

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/bignum/](https://oi-wiki.org/math/bignum/)
- CP-Algorithms ✓ [https://cp-algorithms.com/algebra/big-integer.html](https://cp-algorithms.com/algebra/big-integer.html)
- web ✓ [https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)
