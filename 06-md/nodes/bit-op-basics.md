---
id: bit-op-basics
name: 位运算基础
group: G-E-2
stage: basic
priority: P0
depth_tier: deep
---

# 位运算基础

> 按位与/或/异或/取反/移位，优先级陷阱（& 低于 ==、^ 低于比较），lowbit、置位/清位/翻转、补码表示，Python 无限位宽差异

<!-- 元信息: id=bit-op-basics · group=G-E-2 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

位运算基础：对整数二进制表示做逐位操作。运算符：&（与）、|（或）、^（异或）、~（取反）、<<（左移）、>>（右移）。核心事实：lowbit(x)=x&-x（取最低的 1）；置位 x|=(1<<k)；清位 x&=~(1<<k)；翻转 x^=(1<<k)；判断第 k 位 (x>>k)&1；popcount=x.bit_count()。Python 特有：int 无限位宽，~x=-(x+1)、-x=~x+1（补码性质），>> 对负数是算术移位（无限符号位）。竞赛核心：状态压缩（状压 DP）的所有基础。

## Why · 为什么

### 直觉 · Intuition

CPU 对位运算是一周期指令，比除法/模快得多。用位表示集合状态（第 i 位 = 元素 i 是否选中），一次位运算等价于一次集合操作。位运算优先级是著名陷阱，且 Python 与 C/C++ 相反：Python 中 `&` 高于比较运算符（`x & y == 0` 是 `(x&y)==0`），C/C++ 中 `==` 高于 `&`（`x & y == 0` 是 `x & (y==0)`），迁移语言时最容易踩坑。

### 原理 · Principle

补码：负数 = 其绝对值按位取反 + 1，即 -x = ~x + 1。因此 lowbit：x & -x = x & (~x+1)，恰好保留最低的 1。位运算优先级（Python，从高到低）：算术 + - < 移位 << >> < 与 & < 异或 ^ < 或 | < 比较 == < 赋值；所以 `1 << 1 + 1` 是 `1 << (1+1)`=4（+ 高于移位），`a & b == c` 是 `(a & b) == c`（& 高于比较）。而 C/C++ 中比较运算符高于位与：`x & y == 0` 会被解析为 `x & (y==0)`——跨语言必加括号。x>>k&1 判断第 k 位。x&-x 得 lowbit；x&(x-1) 消掉最低 1；x|(x-1) 把低 1 后的 0 全补 1；x^x=0、x^0=x、x^y^y=x（交换律/自反）。

### 历史 · History

位运算自计算机诞生即是最底层指令；补码表示使加减统一。CPH 第 10 章『Bit manipulation』与 OI Wiki math/bit 页、CP-Alg bit-manipulation 页都系统整理了这些操作。状压 DP（子集枚举、旅行商）使位运算成为竞赛高频基础，Python 选手因 int 无限位宽甚至可当大 bitset 用。

## How · 实现

### 伪代码

```python
lowbit(x)      = x & -x            # 最低位 1 的权值
置位第 k 位    x |= (1 << k)
清位第 k 位    x &= ~(1 << k)
翻转第 k 位    x ^= (1 << k)
判断第 k 位    (x >> k) & 1
popcount      x.bit_count()
消最低 1      x & (x-1)
是否为 2 的幂  x>0 and x&(x-1)==0
```

### Python 实现

```python
def main():
    # 基本运算
    assert (5 & 6) == 4
    assert (5 | 6) == 7
    assert (5 ^ 6) == 3
    assert ~5 == -6              # 补码取反
    assert ~(-5) == 4
    assert (1 << 10) == 1024
    assert (1024 >> 10) == 1
    # lowbit
    assert (8 & -8) == 8
    assert (5 & -5) == 1
    assert (12 & -12) == 4
    # 置位/清位/翻转/判位
    x = 0
    x |= (1 << 3)                # bit3=1 -> 8
    assert x == 8
    x &= ~(1 << 3)
    assert x == 0
    x ^= (1 << 2)
    assert x == 4
    assert ((x >> 2) & 1) == 1
    # popcount 与消 1
    assert (0b101101).bit_count() == 4
    assert (0b1100 & (0b1100 - 1)) == 0b1000
    # 2 的幂判断
    assert (8 > 0) and (8 & (8 - 1)) == 0
    assert not ((6 > 0) and (6 & (6 - 1)) == 0)
    # 优先级陷阱：Python 中 & 高于比较，C/C++ 相反
    assert (1 & 3 == 1) == True           # Python: (1&3)==1
    assert (1 & (3 == 1)) == 0            # C/C++ 语义: 1 & (3==1)
    assert (1 & 3) == 1
    assert (1 << 1 + 1) == 4                   # 加法高于移位
    # 自反性：异或性质
    y = 0b1010
    assert y ^ y == 0 and y ^ 0 == y
    print("bit-op-basics OK")


if __name__ == "__main__":
    main()

```

**PyPy 提示**: PyPy 位运算与 CPython 语义一致（无限位宽 int，负数算术右移）。bit_count()（Python 3.8+，PyPy 3.9+）用内置 popcount，比手写快。位运算单条极快，热循环里优先位运算替代 % 2 判断（x&1）、除以 2（x>>1）。注意 PyPy 的 ~ 与负号对超大 int 同样无限位宽。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 每个位运算 O(位数/字长)（Python int 约 O(wordsize)） |
| 空间 | O(1) |

### 局限

Python int 无限位宽导致负数的 >> 是算术移位（左边补符号位），与 C 的无符号行为不同；位运算只对整数有效。优先级陷阱是最大坑（且 Python 与 C/C++ 相反）：Python 中 `x & y == 0` 是 `(x&y)==0`，C/C++ 中是 `x & (y==0)`，跨语言代码务必加括号。Python 位运算结果 bit 数可变，做『固定宽度』掩码时要手动 & 全 1 掩码。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1100 | 2 | 高低位交换：把 32 位整数前 16 位与后 16 位互换，位运算/移位入门 | [https://www.luogu.com.cn/problem/P1100](https://www.luogu.com.cn/problem/P1100) |
| Luogu | P2114 | 4 | 起床困难综合症：若干位运算操作后求最大值，按位贪心经典，训练位运算性质 | [https://www.luogu.com.cn/problem/P2114](https://www.luogu.com.cn/problem/P2114) |
| LeetCode | 136 | 2 | 只出现一次的数字：用异或自反性 x^x=0 一次遍历找出唯一出现一次的数 | [https://leetcode.cn/problems/single-number/](https://leetcode.cn/problems/single-number/) |

## Pitfalls · 易错点

- 优先级：Python 中 `&` 高于比较（`x & y == 0` 即 `(x&y)==0`）；C/C++ 中相反（`x & y == 0` 是 `x & (y==0)`），跨语言迁移必加括号
- Python 中 `~5` 得 -6 而非 C 无符号语义，做固定宽度取反要 `~x & mask`
- 负数 `>>` 是算术移位，无限符号位扩展，可能与你预期不符
- `1 << 1 + 1` 等于 4：加法优先级高于移位；想表达 (1<<1)+1 要加括号
- 忘记 int 无限位宽：`x \| 0x80000000` 对负数等场景结果超 32 位
- 判断奇偶用 x&1 而不是 x%2（更快且语义一致）

## Sources · 信源

- cph ✓ [https://usaco.guide/CPH.pdf#page=105](https://usaco.guide/CPH.pdf#page=105)
- OI Wiki ✓ [https://oi-wiki.org/math/bit/](https://oi-wiki.org/math/bit/)
- CP-Algorithms ✓ [https://cp-algorithms.com/algebra/bit-manipulation.html](https://cp-algorithms.com/algebra/bit-manipulation.html)
