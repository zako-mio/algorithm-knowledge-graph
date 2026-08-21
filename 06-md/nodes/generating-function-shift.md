---
id: generating-function-shift
name: 生成函数平移
group: G-C-13
stage: frontier
priority: P3
depth_tier: brief
---

# 生成函数平移

> 多项式平移 f(x+c) 与连续点值平移 f(0..n)→f(c..c+n)，Taylor公式/二项式定理/Lagrange插值法，O(n log n)

<!-- 元信息: id=generating-function-shift · group=G-C-13 · stage=frontier · priority=P3 · depth_tier=brief -->

## What · 是什么

生成函数平移（shift）是多项式/幂级数的高级操作，两大主题：① 多项式平移 f(x)↦f(x+c)：已知 f(x) 的系数求 f(x+c) 的系数，有分治法 O(n log² n)、Taylor 公式法（用 f^{(t)}(c) 表达 [x^t]f(x+c)=f^{(t)}(c)/t!）、二项式定理法（三种殊途同归，均归约为卷积 A_0(x)B_0(x) 其中 A_0[i]=f_{n−i}(n−i)!、B_0[i]=c^i/i!）。② 连续点值平移：已知 f(0),f(1),…,f(n)（连续点值）求 f(c),f(c+1),…,f(c+n)，用 Lagrange 插值公式法 O(n log n)（构造 A_0[i]=f(i)(−1)^{n−i}/(i!(n−i)!)、B_0[i]=1/(c−n+i)，[x^{n+t}](A_0B_0) 还原 f(c+t)）。典型应用：同一行第一类无符号斯特林数（上升幂 x^{\overline n} 的平移）、模素数阶乘 n!、二项式系数前缀和、调和数、整式递推等。

## Why · 为什么

### 直觉 · Intuition

『平移』把问题从『系数空间』搬去『点值空间』再搬回。f(x+c) 的系数和 f 在点 c 处的高阶导联系起来（Taylor 展开），而高阶导系数又是 f 系数与阶乘的卷积——于是平移=一个卷积。连续点值平移则反其道：有 n+1 个连续点值就能确定整个多项式，Lagrange 插值把 f(c+t) 写成带 1/(c+t−i) 核的和，该核可化成卷积。所以两类平移本质都是『把求和写成卷积』。

### 原理 · Principle

多项式平移（Taylor 公式法）：f(x+c)=Σ_t f^{(t)}(c)x^t/t!，而 f^{(t)}(c)=Σ_{i=t}^n f_i·i!·c^{i−t}/(i−t)!。令 A_0(x)=Σ f_{n−i}(n−i)!x^i、B_0(x)=Σ c^i/i!·x^i，则 [x^{n−t}](A_0B_0)=Σ_{i=0}^{n−t} f_{i+t}(i+t)!·c^i/i! = t![x^t]f(x+c)，故一个卷积得全部系数。连续点值平移（Lagrange 插值法）：f(x)=Σ_i f(i)·x!/((x−n−1)!(x−i))·(−1)^{n−i}/(i!(n−i)!)，取 x=c+t 并令 A_0、B_0 如上，[x^{n+t}](A_0B_0) 与 f(c+t) 差一个含阶乘的因子，得 O(n log n) 单次卷积完成 n+1 个点值。条件 c>n 时 B_0 分母无零；一般情况分类讨论。

### 历史 · History

多项式平移是『简单情况的多项式复合』，历史上由分治（Bernoulli 式）与 Taylor/二项式技巧分别给出；OI Wiki《多项式平移》页系统整理三种方法与 Lagrange 插值法，并把『同一行第一类无符号斯特林数』『模素数阶乘』『二项式系数前缀和』列为应用。现代 O(n log n) 上升幂算法（如 Bostan–Gaudry–Schost 线）也依赖平移思想。竞赛中 shift 是处理斯特林数整行、阶乘快速求值的隐藏利器。

## How · 实现

### 伪代码

```python
# 多项式平移 f(x+c) mod x^n (Taylor/二项式定理法, 卷积归约)
# 输入 f[0..n-1], 常数 c; 输出 g[0..n-1] = f(x+c)
# A[i] = f[n-1-i]*(n-1-i)!   (i=0..n-1)
# B[i] = c^i / i!            (i=0..n-1)
# C = A * B (卷积) -> C[n-1-k] = k! * g[k]  =>  g[k] = C[n-1-k] / k!

# 连续点值平移 f(c),f(c+1),...,f(c+n): (c>n)
# A[i] = f(i)*(-1)^{n-i}/(i!*(n-i)!)
# B[i] = 1/(c-n+i)
# D = A * B; f(c+t) = D[n+t] * (c+t)! / ((c+t-n-1)!)
```

### Python 实现

```python
MOD = 998244353


def _precompute_factorials(n, mod=MOD):
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % mod
    inv = [1] * (n + 1)
    inv[n] = pow(fact[n], mod - 2, mod)
    for i in range(n, 0, -1):
        inv[i - 1] = inv[i] * i % mod
    return fact, inv


def _conv(a, b, mod=MOD):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] = (c[i + j] + x * y) % mod
    return c


def poly_shift(f, c, mod=MOD):
    """多项式平移 f(x+c) 的前 len(f) 项. O(n^2) 朴素卷积(演示)."""
    n = len(f)
    fact, invf = _precompute_factorials(n, mod)
    A = [f[n - 1 - i] * fact[n - 1 - i] % mod for i in range(n)]
    powc = [1] * n
    for i in range(1, n):
        powc[i] = powc[i - 1] * c % mod
    B = [powc[i] * invf[i] % mod for i in range(n)]
    C = _conv(A, B)
    g = [0] * n
    for k in range(n):
        g[k] = C[n - 1 - k] * invf[k] % mod
    return g


def shift_verify(f, c):
    """直接展开验证 (x+c)^k."""
    from math import comb
    g = [0] * len(f)
    for k, fk in enumerate(f):
        for i in range(k + 1):
            g[i] += fk * comb(k, i) * (c ** (k - i))
    return [v % MOD for v in g]


def point_shift(f_points, c, mod=MOD):
    """连续点值平移: 已知 f(0..n), 求 f(c..c+n). c > n 版本. O(n^2) 朴素."""
    n = len(f_points) - 1
    fact, invf = _precompute_factorials(c + n, mod)
    A = []
    for i in range(n + 1):
        A.append(f_points[i] % mod * (1 if (n - i) % 2 == 0 else mod - 1) % mod
                 * invf[i] % mod * invf[n - i] % mod)
    # B[i] = 1/(c-n+i), i=0..2n
    B = [0] * (2 * n + 1)
    for i in range(2 * n + 1):
        denom = (c - n + i) % mod
        B[i] = pow(denom, mod - 2, mod)
    D = _conv(A, B)
    out = []
    for t in range(n + 1):
        val = D[n + t]
        # val = (c+t)! / ((c+t-n-1)!) * f(c+t)
        val = val * fact[c + t] % mod * invf[c + t - n - 1] % mod
        out.append(val)
    return out


def _eval_shift_poly(f, c):
    """对多项式 f(系数) 在点 x 求值."""
    val = 0
    for i in range(len(f) - 1, -1, -1):
        val = val * c + f[i]
    return val


if __name__ == "__main__":
    # 多项式平移: f = 1 + 2x + x^2, c = 1 => (x+1)^2 + 2(x+1) + 1 = x^2+4x+4
    f = [1, 2, 1]
    g = poly_shift(f, 1)
    assert g == [4, 4, 1], g
    assert g == shift_verify(f, 1)
    # 随机验证: f(x)=3x^3+2x+5, c=2
    f2 = [5, 2, 0, 3]
    g2 = poly_shift(f2, 2)
    assert g2 == shift_verify(f2, 2)
    # 连续点值平移: 取 f(x)=x^2, 点值 0,1,4; 平移 c=4 => f(4..6)=16,25,36
    pts = [_eval_shift_poly([0, 0, 1], i) for i in range(3)]  # 0,1,4
    moved = point_shift(pts, 4)
    assert moved == [16, 25, 36], moved
    print("generating-function-shift: all tests passed")

```

**PyPy 提示**: 本实现用朴素卷积 O(n²) 教学；竞赛需 NTT O(n log n)。多项式平移求 A/B 后一次卷积。连续点值平移注意 c>n 的分母非零条件（模素数下可用逆元处理分母为零的特殊情形分类讨论）。阶乘预计算到 c+t 上限。PyPy 大 n 用 NTT 库。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 朴素 O(n²)；NTT 优化 O(n log n)（一次卷积） |
| 空间 | O(n) |

### 局限

① 连续点值平移的 Lagrange 法要求 c>n（分母 x−i≠0），否则需特殊处理；② 依赖 NTT/多项式乘法，纯 Python 慢；③ 多项式平移 Taylor 法的卷积是『逆序』技巧，容易下标错位；④ 只对多项式（有限次）成立，一般幂级数需 truncate。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P5408 | 5 | 第一类斯特林数·行：上升幂 x^\overline n 求法，OI Wiki shift 页应用（同符号化方法） | [https://www.luogu.com.cn/problem/P5408](https://www.luogu.com.cn/problem/P5408) |
| Luogu | P5282 | 6 | 【模板】快速阶乘算法：连续点值平移 O(√n log n)，OI Wiki shift 页例题 | [https://www.luogu.com.cn/problem/P5282](https://www.luogu.com.cn/problem/P5282) |
| LOJ | 166 | 5 | 拉格朗日插值 2：连续点值平移模板，OI Wiki shift 页例题 | [https://loj.ac/p/166](https://loj.ac/p/166) |
| Luogu | P5702 | 6 | 调和级数求和：连续点值平移/整式递推应用，OI Wiki shift 页例题 | [https://www.luogu.com.cn/problem/P5702](https://www.luogu.com.cn/problem/P5702) |

## Pitfalls · 易错点

- 卷积下标错位：A 是逆序 f，C[n-1-k]=k!·g[k] 的索引关系写错
- 连续点值平移分母 c-n+i 为零未处理
- 阶乘预计算范围不足（需到 c+t）
- c 为负/模数时 (c-n+i) 的模处理
- 只验证 f(x+c) 而忘 f 本身有常数项时的符号

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/poly/shift/](https://oi-wiki.org/math/poly/shift/)
- oiwiki-raw ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/poly/shift.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/poly/shift.md)
- oiwiki-comp-rev ✓ [https://oi-wiki.org/math/poly/comp-rev/](https://oi-wiki.org/math/poly/comp-rev/)
