---
id: bit-tricks
name: 位运算技巧
group: G-E-2
stage: advanced
priority: P2
depth_tier: standard
---

# 位运算技巧

> 进阶位运算套路：lowbit、popcount、前导/后缀零、格雷码、交换/去重、集合交并差、mask 变换等妙用

<!-- 元信息: id=bit-tricks · group=G-E-2 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

位运算技巧合集：lowbit(x)=x&-x（树状数组、找最低 1）、popcount（x.bit_count()）、最高位 1 位置（bit_length-1）、x&(x-1) 消最低 1、x|(x-1) 补全低位的 0、判定 2 的幂、位掩码集合的交并差补（a&b, a|b, a&~b, ~a&mask）、格雷码、按位异或自反性、子集枚举（见 submask-enum）、SOS DP（高维前缀和）、二进制分组、Meet in the middle 等。这些技巧是状压 DP、树状数组、位集合运算、图论子集问题的『瑞士军刀』。

## Why · 为什么

### 直觉 · Intuition

位运算把『对集合的整批操作』压缩成一条指令。每个技巧背后是一条数论/集合性质：如 x&-x 得到最低位的权值是因为负数补码取反加一；x&(x-1) 删掉最低 1 因为减一会借位。掌握『何时用哪个』比记住代码更重要——看到『集合、状态、出现次数、子集、奇偶』就想到位操作。

### 原理 · Principle

1) lowbit(x)=x&-x：-x=~x+1，与 x 逐位与后只留最低位 1。2) x&(x-1)：x-1 把最低 1 位变 0 且低位置 1，与 x 与后删掉最低 1。3) bit_length()=最高位索引+1。4) x|x-1 或 x|(x+1) 处理低位补全。5) 判断 x 是 2 的幂：x>0 且 x&(x-1)==0。6) 集合操作：a&b 交集，a|b 并集，a&~b 差集，~a&mask 补集。7) 异或性质：x^y 可看作无进位加法；x^x=0；可用于找出现次数为奇数的元素。8) SOS DP：对每个集合求其所有子集的贡献，O(n·2^n)。

### 历史 · History

位技巧源自 C 系底层编程（Hacker's Delight 一书系统整理）；CPH 第 10 章、CP-Alg bit-manipulation 页、OI Wiki math/bit 页均有列表。lowbit 是树状数组核心，格雷码与子集枚举是状压的骨架。Python 因 int 无限位宽，位技巧直接可用且可处理任意大状态。

## How · 实现

### 伪代码

```python
lowbit(x)       = x & -x
popcount        = x.bit_count()
最高位索引      = x.bit_length() - 1
删最低 1        = x & (x-1)
是否 2 的幂     = x>0 and x&(x-1)==0
下一更大的含 m 的掩码(超集) = 见注释*
判断第 k 位      = (x >> k) & 1
集合: 交 a&b / 并 a|b / 差 a&~b / 补 ~a&mask
交换整数        = a ^= b; b ^= a; a ^= b  (不常用, 仅展示)
SOS DP: for i in range(n): for mask in 2^n: if mask&(1<<i): f[mask]+=f[mask^(1<<i)]
```

### Python 实现

```python
def main():
    # lowbit
    assert (12 & -12) == 4
    assert (10 & -10) == 2
    # popcount / 最高位
    assert (0b110110).bit_count() == 4
    assert (1 << 7).bit_length() - 1 == 7
    assert (0b1001).bit_length() - 1 == 3
    # 删最低 1 循环 = 枚举 set bit
    x = 0b1101
    bits = []
    y = x
    while y:
        low = y & -y
        bits.append(low)
        y &= y - 1
    assert bits == [1, 4, 8]
    # 2 的幂
    assert (1 > 0) and (1 & (1 - 1)) == 0
    assert not ((3 > 0) and (3 & (3 - 1)) == 0)
    # 集合运算
    a = 0b1011  # {0,1,3}
    b = 0b0110  # {1,2}
    assert (a & b) == 0b0010   # 交 {1}
    assert (a | b) == 0b1111   # 并
    assert (a & ~b) == 0b1001  # 差
    assert (~a & 0b1111) == 0b0100  # 补(4位掩码下)
    # 异或找单次
    arr = [5, 3, 5, 7, 3]
    acc = 0
    for v in arr:
        acc ^= v
    assert acc == 7
    # 格雷码（相邻差1位）
    def g(n):
        return n ^ (n >> 1)
    seq = [g(n) for n in range(8)]
    for p, q in zip(seq, seq[1:]):
        assert (p ^ q).bit_count() == 1
    print("bit-tricks OK")


if __name__ == "__main__":
    main()

```

**PyPy 提示**: PyPy 支持 bit_count/bit_length，位运算与 CPython 一致（无限位宽、负数算术右移）。热循环中位运算本身极快；若对海量 int 做 bit_count，可用内置（C 层）。PyPy 对生成器与迭代开销与 CPython 类似，集合运算多用位运算替代 set 对象（set 有哈希与分配开销）。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 各技巧单次 O(1)~O(位数)；SOS DP O(n·2^n) |
| 空间 | O(1)~O(2^n) |

### 局限

技巧虽多但各有适用面，别硬套；SOS DP 内存 2^n 对 n>22 紧张。Python 无限位宽下 ~x 是无限取反，补集运算必须 & mask。有些技巧（如 a^b 交换）在现代 Python 只是展示，无性能价值且降低可读性。异或找单数只适用『恰好一个出现奇数次』，两个以上需分组。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| LeetCode | 191 | 1 | 位 1 的个数：popcount，Python 直接 bit_count() 或 x&(x-1) 循环 | [https://leetcode.cn/problems/number-of-1-bits/](https://leetcode.cn/problems/number-of-1-bits/) |
| LeetCode | 136 | 2 | 只出现一次的数字：异或自反性，位运算经典 | [https://leetcode.cn/problems/single-number/](https://leetcode.cn/problems/single-number/) |
| Luogu | P1100 | 2 | 高低位交换：移位与掩码组合运用 | [https://www.luogu.com.cn/problem/P1100](https://www.luogu.com.cn/problem/P1100) |

## Pitfalls · 易错点

- Python 中 ~x 无限位宽取反，取补集必须 & 全 1 掩码
- x.bit_length() 对 0 返回 0，最高位索引要 -1 前先判 x>0
- 负数 lowbit 语义：Python 的 x&-x 对正数正确，负数会得正 lowbit 但注意按位取反
- a^b 交换变量在现代 Python 是坏味道（可读性差、无性能收益），别当技巧用
- SOS DP 的循环顺序（先 i 后 mask）不能颠倒，否则重复计数
- 集合补集结果依赖掩码宽度，忘掩码会得到无限宽大数

## Sources · 信源

- CP-Algorithms ✓ [https://cp-algorithms.com/algebra/bit-manipulation.html](https://cp-algorithms.com/algebra/bit-manipulation.html)
- cph ✓ [https://usaco.guide/CPH.pdf#page=105](https://usaco.guide/CPH.pdf#page=105)
- OI Wiki ✓ [https://oi-wiki.org/math/bit/](https://oi-wiki.org/math/bit/)
