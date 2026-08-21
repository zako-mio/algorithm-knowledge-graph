---
id: numeral-system
name: 数制转换
group: G-C-18
stage: basic
priority: P2
depth_tier: standard
---

# 数制转换

> 任意进制间转换：整数除基取余法、小数乘基取整法，2/8/16 快速互转；Python int(x,base) 与 format() 内置支持

<!-- 元信息: id=numeral-system · group=G-C-18 · stage=basic · priority=P2 · depth_tier=standard -->

## What · 是什么

数制转换：给定一个数，在其基数为 b1 的表示与基数为 b2 的表示之间转换。整数部分用「除基取余法」（不断除以目标进制取余数，逆序输出）；小数部分用「乘基取整法」。2、8、16 进制间由于 2^3=8、2^4=16，可直接按位分组快速转换（3 位一组 ↔ 8 进制，4 位一组 ↔ 16 进制）。大数进制转换（如十进制 10^1000 转 2 进制）用数组模拟除法或直接 Python 大整数。Python 内置：int('101',2)、format(x,'b/o/x')、bin/oct/hex；任意进制 2~36 用 int(s, base)。

## Why · 为什么

### 直觉 · Intuition

一个数 = Σ 位×基数^i。转 k 进制：反复除以 k，每次得到的余数就是最低位，商继续除，最后商为 0 停止，逆序拼起来。原理：整除运算把「当前最低位」剥下来，高位整体下移一位。转回十进制：把表示当作多项式求值（霍纳法）value = value*base + digit。

### 原理 · Principle

整数除基取余：n 在 k 进制下表示为 a_k...a_1a_0，n = q0*k + a0（a0=n mod k），q0=floor(n/k) 继续分解，直至商为 0，余数逆序。小数乘基取整：0.25 转二进制，0.25*2=0.5 取整 0，0.5*2=1.0 取整 1 → .01。2↔8/16：8=2^3，所以 (101110)2 按 3 位一组 101 110 → 5 6 → 0o56；16 同理 4 位一组。大数场景用 Python int 直接中转：dec_str 转任意进制可 int(s, b1) → 再自定义 divmod 循环取余到 b2，但 Python 选手一般直接 int() + 自写 to_base 输出。

### 历史 · History

进位制思想自古即有（十进制源于自然计数，六十进制源自巴比伦），计算机以二进制为底，八进制/十六进制因便于阅读保留。OI Wiki 数制页系统性介绍除基取余、乘基取整与 2/8/16 快速互转。竞赛中数制转换作为基础技巧在模拟题、字符串题中高频出现。

## How · 实现

### 伪代码

```python
DIGITS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def to_base(x, b):
    if x == 0: return '0'
    res = ''
    while x:
        res = DIGITS[x % b] + res
        x //= b
    return res

def from_base(s, b):
    val = 0
    for ch in s:
        val = val * b + DIGITS.index(ch)
    return val
```

### Python 实现

```python
DIGITS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def to_base(x, b):
    if x == 0:
        return '0'
    res = ''
    while x:
        res = DIGITS[x % b] + res
        x //= b
    return res


def from_base(s, b):
    val = 0
    for ch in s:
        val = val * b + DIGITS.index(ch)
    return val


def main():
    # 与内置校验
    assert to_base(255, 16) == 'FF'
    assert to_base(8, 2) == '1000'
    assert from_base('FF', 16) == 255
    assert from_base('1000', 2) == 8
    assert int('101', 2) == 5
    assert int('ff', 16) == 255
    assert format(255, 'b') == '11111111'
    assert format(255, 'o') == '377'
    assert format(255, 'x') == 'ff'
    # 大数：10^30 转 36 进制再转回
    big = 10**30
    assert from_base(to_base(big, 36), 36) == big
    # 2↔8/16 快速互转一致性
    x = 0b10111001
    assert to_base(x, 8) == format(x, 'o') == '271'
    assert to_base(x, 16).lower() == format(x, 'x') == 'b9'
    for b in range(2, 37):
        assert from_base(to_base(12345, b), b) == 12345
    print("numeral-system OK")


if __name__ == "__main__":
    main()

```

**PyPy 提示**: Python 内置 int(s,base) 与 format() 支持 2/8/16 及 2~36；这些在 PyPy 下同速。自定义 to_base 循环 O(log x)，PyPy 无差别。超大进制（>36）需自定义字母表，Python 无内置。负数先取绝对值处理符号。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 除基取余 O(log_b x) 轮（大整数除法本身 O(n^2) 级别）；2↔8/16 按位分组 O(n) |
| 空间 | O(log_b x) |

### 局限

Python int(s,base) 只支持 2~36；10^5 位级大数逐位除基取余在 Python 中较慢（大数除法 O(n^2)），必要时用分治/分组技巧（先转大进制再转目标进制）。小数转换有精度问题，浮点转二进制需谨慎。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1015 | 4 | 回文数：任意进制 n 进制下大整数加法+回文判断，综合数制转换与高精度 | [https://www.luogu.com.cn/problem/P1015](https://www.luogu.com.cn/problem/P1015) |
| Luogu | P1143 | 2 | 进制转换模板：n 进制转十进制再转 m 进制 | [https://www.luogu.com.cn/problem/P1143](https://www.luogu.com.cn/problem/P1143) |

## Pitfalls · 易错点

- 除基取余的余数要逆序输出，直接顺序拼接是错的
- x==0 时输出 '0' 而不是空串
- from_base 若字符不在 DIGITS 中会 ValueError，输入需校验或忽略大小写
- Python int('0x..',16) 可带前缀，但 int('ff',16) 不能大写混入前缀；format 与 int 的字母大小写注意
- 负数处理：先取绝对值，最后补符号；除基取余对负数的 % 语义不同

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/numeral-sys/base/](https://oi-wiki.org/math/numeral-sys/base/)
- Wikipedia ✓ [https://en.wikipedia.org/wiki/Numeral_system](https://en.wikipedia.org/wiki/Numeral_system)
