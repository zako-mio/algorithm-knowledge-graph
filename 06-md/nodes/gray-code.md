---
id: gray-code
name: 格雷码
group: G-C-18
stage: intermediate
priority: P2
depth_tier: standard
---

# 格雷码

> 相邻两数二进制仅一位不同的编码，G(n)=n^(n>>1)，逆变换 rev_g 逐位异或；用于汉密尔顿路径、汉诺塔、避免信号误判

<!-- 元信息: id=gray-code · group=G-C-18 · stage=intermediate · priority=P2 · depth_tier=standard -->

## What · 是什么

格雷码（Gray code）是一种二进制编码系统，其中任意两个相邻数字的二进制表示只有一位不同。0 起点：G(0)=000,G(1)=001,G(2)=011,G(3)=010,G(4)=110,G(5)=111,G(6)=101,G(7)=100。正向变换 G(n)=n^(n>>1)；逆变换（给定 g 恢复 n）：从高位向低位，n 的每一位 = g 对应位与前一位 n 异或，代码 `rev_g(g): n=0; while g: n^=g; g>>=1`。3 位格雷码序列构成三维立方体的汉密尔顿回路；也是汉诺塔的移动序列。CSP-S2 2019 D1T1 直接考正向变换。

## Why · 为什么

### 直觉 · Intuition

普通二进制从 3(011) 到 4(100) 要翻转 3 位，编码器/传感器若在边界抖动会误读。格雷码保证每走一步只翻 1 位，任何中间态都恰好是某个合法相邻值，错误被最小化。构造上：G(n)=n^(n>>1) 把二进制「相邻变化点」编码成 XOR，相邻 n 的差别只反映在最高变化位。

### 原理 · Principle

正向：设 n 二进制为 ...b_i b_{i-1}...，则 G 的第 i 位 = b_i ^ b_{i+1}（i+1 是更高一位），故 G(n)=n ^ (n>>1)。正确性：n 加 1 时末段连续的 1 翻转为 0 并把最低的 0 置 1；这一过程反映到 G(n) 上只改变一位（最高变化位），可严格证明相邻 G 恰差 1 位。逆变换：n_k=g_k, n_{k-1}=g_{k-1}^n_k=g_{k-1}^g_k, ...，即 n 的每一位是 g 的前缀异或，故 rev_g 循环 g>>=1 并异或累加。镜像构造：k 位格雷码由 k-1 位镜像翻转后在高位补 0/1 得到。

### 历史 · History

由贝尔实验室 Frank Gray 于 1940 年代提出，1953 年注册专利（Pulse Code Communication）。最初用于避免数字信号传输中的编码错误。竞赛中 CSP-S2 2019 D1T1 直接考查 G(n) 公式；也常用于状压/子集排列、汉诺塔的递归移动序列建模。

## How · 实现

### 伪代码

```python
def g(n):
    return n ^ (n >> 1)

def rev_g(gcode):
    n = 0
    while gcode:
        n ^= gcode
        gcode >>= 1
    return n

# 生成 k 位格雷码序列（镜像法，非必需）
def gray_sequence(k):
    seq = [0]
    for _ in range(k):
        seq += [x | (1 << len(seq)) for x in reversed(seq)]
    return seq
```

### Python 实现

```python
def g(n):
    return n ^ (n >> 1)


def rev_g(gcode):
    n = 0
    while gcode:
        n ^= gcode
        gcode >>= 1
    return n


def gray_sequence(k):
    seq = [0]
    for _ in range(k):
        size = len(seq)
        seq = seq + [x | size for x in reversed(seq)]
    return seq


def main():
    # 正向变换 + 相邻汉明距离恒为 1
    vals = [g(n) for n in range(16)]
    for a, b in zip(vals, vals[1:]):
        assert (a ^ b).bit_count() == 1, (a, b)
    assert vals == [0, 1, 3, 2, 6, 7, 5, 4, 12, 13, 15, 14, 10, 11, 9, 8]
    # 逆变换正确性
    for n in range(256):
        assert rev_g(g(n)) == n
    # 镜像法生成的序列与公式一致
    assert gray_sequence(4) == [g(n) for n in range(16)]
    print("gray-code OK")


if __name__ == "__main__":
    main()

```

**PyPy 提示**: 位运算 n^(n>>1) 与 while 循环在 PyPy 下均极快，无需特殊优化。超大 n（如 k 到 60 位）直接用 int 位运算，Python int 不限宽。注意 n 为负数时 ^ 与 >> 在 Python 是算术移位+无限位宽符号扩展，g() 公式只对非负 n 有意义。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 正向 O(1)；逆变换 O(位数)（每轮异或+移位）；生成 k 位序列 O(2^k) |
| 空间 | O(1)；生成序列 O(2^k) |

### 局限

只对非负整数定义；逆变换线性扫描位宽。格雷码本身在竞赛中直接考的题较少（CSP2019 为典型），更多作为构造/编码技巧与汉诺塔、超立方体问题的辅助。3 位以上序列长度 2^k 增长快，不能全量枚举超过 20 位。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P5657 | 4 | CSP-S2 2019 D1T1 格雷码：直接考 G(n)=n^(n>>1) 公式，但 k 达 64 需用 Python int 处理大数 | [https://www.luogu.com.cn/problem/P5657](https://www.luogu.com.cn/problem/P5657) |
| Luogu | P2119 | 3 | 魔法阵：位运算+计数辅助，非格雷码本体，可作位运算综合练习 | [https://www.luogu.com.cn/problem/P2119](https://www.luogu.com.cn/problem/P2119) |

## Pitfalls · 易错点

- Python 中 n^(n>>1) 对超大 k（如 64 位）直接用 int 即可，但 C++ 会溢出 unsigned long long 时要留意
- 逆变换勿写成从低位异或；正确是每次 g>>=1 累异或（等价于前缀异或从高位计算）
- k 位格雷码序列首项与末项也恰好差 1 位（环形性质），若题目要求循环也满足
- G(n) 不是普通二进制映射，不能直接当二进制做比较/加法
- n 为负时位运算语义不同，务必先转非负

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/numeral-sys/gray-code/](https://oi-wiki.org/math/numeral-sys/gray-code/)
- CP-Algorithms ✓ [https://cp-algorithms.com/algebra/gray-code.html](https://cp-algorithms.com/algebra/gray-code.html)
