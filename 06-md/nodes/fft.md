---
id: fft
name: FFT(快速傅里叶变换)
group: G-C-12
stage: advanced
priority: P1
depth_tier: standard
---

# FFT(快速傅里叶变换)

> O(n log n)计算多项式乘法，基于DFT与蝴蝶操作，NTT为模意义版本

<!-- 元信息: id=fft · group=G-C-12 · stage=advanced · priority=P1 · depth_tier=standard -->

## What · 是什么

快速傅里叶变换（FFT）把多项式从系数表示转为在单位根处的点值表示（DFT），利用单位根性质分治加速，在 O(n log n) 内完成多项式乘法：系数→点值（正变换）→逐点相乘→点值→系数（逆变换）。核心是蝴蝶操作（奇偶分治+旋转因子），实现分递归与迭代（位逆序置换+倍增合并）两种。FFT 用复数运算，存在浮点误差；模意义版本是 NTT。应用远超多项式乘法：大整数乘法、所有可能和/差、循环相关与自相关、卷积型 DP 加速、字符串匹配（与 pattern 反转卷积）等。

## Why · 为什么

### 直觉 · Intuition

朴素乘法把每个系数对乘一遍 O(n^2)。换个角度：多项式在 n 个点上的取值（点值）可以逐点相乘来得到乘积的点值，而求 n 个点的点值+还原系数都能用分治加速——因为取单位根时奇偶项平方重合，能成对复用，这就是'快速'的来源。

### 原理 · Principle

DFT 是线性变换，取 n=2^k 次单位根 ω_n=e^{-2πi/n}。分治：f(x)=G(x^2)+x·H(x^2)，由 ω_n^{k+n/2}=-ω_n^k 得 f(ω^k)=G(ω^{2k})+ω^k H(ω^{2k})，f(ω^{k+n/2})=G(ω^{2k})-ω^k H(ω^{2k})，一次算出两点。递归深度 log n，总 O(n log n)。逆变换取共轭根再除 n。迭代版先用位逆序置换把输入排成可自底向上合并的顺序，每层做蝶形。

### 历史 · History

FFT 的思想源于 Fourier(1807)，离散版本 DFT 用于信号处理。Cooley & Tukey 1965 提出分治 FFT 算法（思想可追溯至 Gauss），被列为计算数学十大算法之一。OI/ACM 中 2000 年代起成为多项式全家桶的基石，OI Wiki 与 CP-Algorithms 均有系统教程。

## How · 实现

### 伪代码

```python
# 迭代 FFT (in-place), n=2^k
bit_reverse_permute(a)      # 位逆序置换
for h in 2,4,8,...,n:        # 合并区间长度
    wn = exp(-2πi/h)        # 旋转因子
    for i in step h:
        w = 1
        for j in i..i+h/2-1:
            u = a[j]; v = a[j+h/2]*w
            a[j] = u+v; a[j+h/2] = u-v
            w *= wn
# 逆变换: 根取共轭, 最后整体除以 n
```

### Python 实现

```python
import cmath
import math
import random


def fft_recursive(a, invert=False):
    """递归 FFT。a: list[complex], 长度必须是 2 的幂。
    invert=False: DFT; invert=True: IDFT(由调用方负责除以 n)."""
    n = len(a)
    if n == 1:
        return a[:]
    w_n = cmath.exp(complex(0, -2 * math.pi / n)) if not invert else cmath.exp(complex(0, 2 * math.pi / n))
    a_even = fft_recursive(a[0::2], invert)
    a_odd = fft_recursive(a[1::2], invert)
    w = 1 + 0j
    out = [0j] * n
    half = n // 2
    for k in range(half):
        t = w * a_odd[k]
        out[k] = a_even[k] + t
        out[k + half] = a_even[k] - t
        w *= w_n
    return out


def fft_recursive_rounded(a, invert=False):
    """带归一化的递归 FFT 封装: invert 时自动除以 n. 返回新列表。"""
    out = fft_recursive(a, invert)
    if invert:
        n = len(a)
        out = [x / n for x in out]
    return out


def bit_reverse_permute(a):
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]


def fft_iterative(a, invert=False):
    """迭代 FFT(位逆序置换 + 蝴蝶操作). 原地修改. 长度须为 2 的幂."""
    n = len(a)
    a = a[:]
    bit_reverse_permute(a)
    h = 2
    while h <= n:
        angle = -2 * math.pi / h
        if invert:
            angle = -angle
        w_h = cmath.exp(complex(0, angle))
        for i in range(0, n, h):
            w = 1 + 0j
            for j in range(i, i + h // 2):
                u = a[j]
                v = a[j + h // 2] * w
                a[j] = u + v
                a[j + h // 2] = u - v
                w *= w_h
        h <<= 1
    if invert:
        for i in range(n):
            a[i] /= n
    return a


def poly_multiply_fft(a, b):
    """FFT 多项式乘法(返回实部圆整的整数系数). 支持小规模正数系数."""
    n = 1
    need = len(a) + len(b) - 1
    while n < need:
        n <<= 1
    fa = [complex(x, 0) for x in a] + [0j] * (n - len(a))
    fb = [complex(x, 0) for x in b] + [0j] * (n - len(b))
    fa = fft_iterative(fa, False)
    fb = fft_iterative(fb, False)
    for i in range(n):
        fa[i] *= fb[i]
    fc = fft_iterative(fa, True)
    return [int(round(fc[i].real)) for i in range(need)]


def poly_multiply_naive(a, b):
    res = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            res[i + j] += x * y
    return res


if __name__ == "__main__":
    # 自测: 与朴素卷积对拍(小规模)
    for _ in range(50):
        la = random.randint(1, 8)
        lb = random.randint(1, 8)
        a = [random.randint(0, 9) for _ in range(la)]
        b = [random.randint(0, 9) for _ in range(lb)]
        assert poly_multiply_fft(a, b) == poly_multiply_naive(a, b), (a, b)
    # OI-wiki 引入样例: (5x^2+3x+7)(7x^2+2x+1)
    A = [7, 3, 5]
    B = [1, 2, 7]
    assert poly_multiply_fft(A, B) == [7, 17, 60, 31, 35], poly_multiply_fft(A, B)
    # 递归版与迭代版一致
    x = [complex(random.randint(-5, 5), random.randint(-5, 5)) for _ in range(8)]
    assert all(abs(fft_recursive(x)[k] - fft_iterative(x)[k]) < 1e-9 for k in range(8))
    # 单位复根校验: 插值还原
    y = fft_iterative(x, False)
    z = fft_iterative(y, True)
    assert all(abs(z[k] - x[k]) < 1e-9 for k in range(8))
    # 多项式乘法样例: (5x^2+3x+7)(7x^2+2x+1)=35x^4+31x^3+60x^2+17x+7
    assert poly_multiply_fft([7, 3, 5], [1, 2, 7]) == [7, 17, 60, 31, 35]
    print("FFT tests passed")

```

**PyPy 提示**: Python 纯循环 FFT 常数大，1e5 长度乘法可能 TLE（复杂度 O(n log n) 但每次迭代有 Python 开销与复数对象）。教学正确。竞赛中 Python 建议：能取模就用 NTT；不能取模时可用 numpy 的 FFT（numpy 未内置不可用则手写递归版）。分块卷积（块内朴素/FFT）可缓解。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n log n) 多项式乘法 |
| 空间 | O(n) |

### 局限

浮点误差: 系数较大(如 1e9 量级且 n 大)时圆整可能错, 需要 NTT/拆系数 FFT(three-FFT / 任意模数)。长度必须是 2 的幂, 需补齐。Python 纯实现性能差, N=1e5 级可能 TLE, 应改用 NTT 或 numpy。递归版在 Python 有递归深度限制, 需 sys.setrecursionlimit 或改迭代。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3803 | 3 | 多项式乘法模板题(FFT/NTT 均可), 入门必做 | [https://www.luogu.com.cn/problem/P3803](https://www.luogu.com.cn/problem/P3803) |
| HDU | 1402 | 3 | A * B Problem Plus: 大整数乘法, 经典 FFT 应用 | [http://acm.hdu.edu.cn/showproblem.php?pid=1402](http://acm.hdu.edu.cn/showproblem.php?pid=1402) |
| Codeforces | 553E | 6 | Kyoya and Train: FFT 优化 DP 转移的卷积结构 | [https://codeforces.com/contest/553/problem/E](https://codeforces.com/contest/553/problem/E) |

## Pitfalls · 易错点

- 忘记把长度补齐到 2 的幂(且需 >= degA+degB+1)
- 逆变换忘记除以 n(每个点都要除)
- 浮点圆整用 round 而非 int 截断(负数系数会错)
- 位逆序置换实现写错(标准翻转循环易错)
- 复数旋转因子方向搞反(正负号), 导致结果共轭

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/poly/fft/](https://oi-wiki.org/math/poly/fft/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/poly/fft.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/poly/fft.md)
- CP-Algorithms ✓ [https://cp-algorithms.com/algebra/fft.html](https://cp-algorithms.com/algebra/fft.html)
