---
id: generating-function-basics
name: 生成函数基础
group: G-C-13
stage: advanced
priority: P2
depth_tier: standard
---

# 生成函数基础

> 形式幂级数环与生成函数框架：定义、加乘卷积、求导积分、逆元、复合、常见展开式，OGF/EGF 的前置

<!-- 元信息: id=generating-function-basics · group=G-C-13 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

生成函数基础=形式幂级数（formal power series）环 R[[x]] 上的运算框架 + 生成函数作为组合工具的总纲。形式幂级数 f=Σ_{n≥0} f_n x^n：加法=按项加；乘法=卷积 (fg)_n=Σ_{i=0}^n f_i g_{n−i}；形式导数 f'=Σ n f_n x^{n−1}；形式不定积分 ∫(x^k)=x^{k+1}/(k+1)；乘法逆元 f^{-1} 存在 ⟺ f_0≠0（系数递推 (f^{-1})_n = −f_0^{-1}Σ_{i>0} f_i (f^{-1})_{n−i}）；复合 f(g(x)) 在 g 常数项为 0 时良定义；复合逆 g 满足 f(g)=g(f)=x 需 f_0=0,f_1≠0（拉格朗日反演 [x^n]g(x)^k=k/n·[x^{n−k}]((x/f(x))^n)）。常见展开式（幂级数展开，形式恒等）：e^x=Σx^n/n!；(1+x)^a=Σ C(a,n)x^n；1/(1−x)=Σx^n；ln(1+x)=Σ(−1)^{n−1}x^n/n；sin/cos/arctan/arcsin 等。生成函数定义：A(x)=Σ a_n k_n(x)，核函数 k_n(x)=x^n 给 OGF、x^n/n! 给 EGF、1/n^x 给狄利克雷生成函数。

## Why · 为什么

### 直觉 · Intuition

把无限数列当『一个多项式』来运算，就把组合问题变成代数问题。形式幂级数不关心收敛——x 只是占位符，系数才是要算的东西。这样 e^x、1/(1−x) 这些『函数』在代数世界里只是满足特定卷积关系的系数流，可以安全地加减乘除求导积分。

### 原理 · Principle

R[[x]] 是环：加法交换群 + 卷积乘法（有 1，无零因子）。形式导数满足 Leibniz 法则、链式法则，形式积分是导数的右逆。逆元：1/(f)=g ⟺ f·g=1，逐系数解出 g_n=−f_0^{-1}Σ_{i=1}^n f_i g_{n−i}。复合 f(g(x)) 良定义需 g_0=0 使每个 x^n 只来自有限项。复合逆 + 拉格朗日反演：若 f(g)=x 且 f_0=0,f_1≠0，则 [x^n]g^k = k/n [x^{n−k}](x/f(x))^n，用于解隐含方程与生成函数系数。这些运算使『生成函数=工具』的整个框架自洽。

### 历史 · History

形式幂级数由 Cauchy（1821）与后来的形式分析学派确立严谨地位；Euler 用生成函数解分拆/递推问题；Laplace（1812）命名『生成函数』。OI Wiki《多项式与生成函数》页以『引入→形式幂级数环→运算→生成函数』完整编排，是 OGF/EGF、多项式全套算法的总入口。现代竞赛里生成函数 + NTT 是多项式计数的标准范式。

## How · 实现

### 伪代码

```python
# 形式幂级数运算 (系数列表 a, 低次在前)

def fadd(a,b): ...            # 按项加

def fmul(a,b):                # 卷积 O(n^2)
  c=[0]*(len(a)+len(b)-1)
  for i in range(len(a)):
    for j in range(len(b)): c[i+j]+=a[i]*b[j]
  return c

def fderiv(a): return [i*a[i] for i in range(1,len(a))]

def finteg(a): return [0]+[a[k]//(k+1) for k in range(len(a))]

def finv(a, n):               # 逆元, 需 a[0]!=0
  g=[pow(a[0],-1,MOD)]
  for k in range(1,n):
    s=sum(a[i]*g[k-i] for i in range(1,k+1))
    g.append((-s*pow(a[0],-1,MOD))%MOD)
  return g

def compose(f,g):             # f(g), 需 g[0]==0, O(n^2)
  res=[0]*len(f)
  for i in range(len(f)-1,-1,-1):
    res = fmul(res, g[:len(f)])
    res[0]+=f[i]
  return res[:len(f)]
```

### Python 实现

```python
MOD = 998244353


def fadd(a, b):
    n = max(len(a), len(b))
    return [((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)) % MOD for i in range(n)]


def fmul(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] = (c[i + j] + x * y) % MOD
    return c


def fderiv(a):
    return [(i * a[i]) % MOD for i in range(1, len(a))]


def finteg(a):
    out = [0]
    for k in range(len(a)):
        out.append(a[k] * pow(k + 1, MOD - 2, MOD) % MOD)
    return out


def finv(a, n):
    """模 MOD 下 a 的乘法逆元前 n 项, 需 a[0] != 0."""
    a = (a + [0] * n)[:n]
    inv0 = pow(a[0], MOD - 2, MOD)
    g = [inv0]
    for k in range(1, n):
        s = 0
        for i in range(1, k + 1):
            s = (s + a[i] % MOD * g[k - i]) % MOD
        g.append((-s * inv0) % MOD)
    return g


def fcompose(f, g, n):
    """f(g(x)) mod x^n, 要求 g[0]==0. O(n^2) Horner 形式."""
    g = (g + [0] * n)[:n]
    res = [0] * n
    for i in range(len(f) - 1, -1, -1):
        # res = res * g + f[i]
        nres = [0] * n
        for a in range(n):
            for b in range(n - a):
                nres[a + b] = (nres[a + b] + res[a] * g[b]) % MOD
        res = nres
        res[0] = (res[0] + f[i]) % MOD
    return res[:n]


def fpow_series(a, n):
    """exp 级数 e^a 前 n 项(朴素 O(n^2)), a[0] 应处理(标准做法 a[0]=0).
    实现: b' = a' * b."""
    a = (a + [0] * (n - len(a)))[:n]
    if a[0] != 0:
        raise ValueError("exp needs a[0]==0")
    b = [1]
    for k in range(1, n):
        s = 0
        for i in range(1, k + 1):
            s = (s + i * a[i] * b[k - i]) % MOD
        b.append(s * pow(k, MOD - 2, MOD) % MOD)
    return b


if __name__ == "__main__":
    # 逆元: 1/(1-x) = 1,1,1,...
    inv = finv([1, MOD - 1], 6)
    assert inv == [1, 1, 1, 1, 1, 1]
    # 1/(1-2x) = 1,2,4,8,...
    inv2 = finv([1, MOD - 2], 5)
    assert inv2 == [1, 2, 4, 8, 16]
    # 导数积分: d/dx (1,1,1,1) = (1,2,3)
    assert fderiv([1, 1, 1, 1]) == [1, 2, 3]
    # 复合: exp 的复合 e^{x}... 简单验证 f(x)=1+x 复合 g(x)=x^2: f(g)=1+x^2
    comp = fcompose([1, 1], [0, 0, 1], 5)
    assert comp == [1, 0, 1, 0, 0]
    # 幂级数 exp: exp(x) 系数 = 1/k!
    from math import factorial
    e = fpow_series([0, 1] + [0] * 6, 6)
    assert e == [pow(factorial(k), MOD - 2, MOD) for k in range(6)]
    # 常见展开: (1-x)^-1 与 (1-x)^-2 卷积
    assert fmul([1] * 4, [1] * 4)[:4] == [1, 2, 3, 4]
    print("generating-function-basics: all tests passed")

```

**PyPy 提示**: 朴素 O(n²) 运算适合 n≤2000 教学/小规模；实际竞赛 NTT 加速 O(n log n)。逆元迭代公式每步 O(n)，整体 O(n²)；牛顿迭代 O(n log n)。求导积分在模素数下需逆元。fcompose O(n³)（Horner + 内层卷积），竞赛需特殊算法（见 comp-rev）。Python 版注意全部取模与负号处理。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 加 O(n)；乘/逆/exp 朴素 O(n²)；NTT 优化 O(n log n) |
| 空间 | O(n) |

### 局限

① 形式幂级数『不收敛』的约定要与解析函数区分（不能随意代入 x 求值）；② 逆元需常数项非零；③ 复合需内函数常数项为 0；④ 复合/复合逆朴素实现慢，需专用算法；⑤ 模非素数时无逆元/阶乘逆元，需其他手法。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P5205 | 5 | 【模板】多项式开根：牛顿迭代/形式幂级数运算综合，OI Wiki elementary-func 例题 | [https://www.luogu.com.cn/problem/P5205](https://www.luogu.com.cn/problem/P5205) |
| LOJ | 172 | 4 | 多项式基础综合题（intro 页提及），练习加乘逆元等基础操作 | [https://loj.ac/p/172](https://loj.ac/p/172) |
| Luogu | P4512 | 5 | 【模板】多项式除法：余数与商，需要逆元，形式幂级数运算前置 | [https://www.luogu.com.cn/problem/P4512](https://www.luogu.com.cn/problem/P4512) |

## Pitfalls · 易错点

- 逆元忘检查常数项是否为 0
- 复合时内函数常数项非 0 导致系数定义不清
- 把形式幂级数当普通函数代入数值求值
- 求导/积分的系数平移（导数降一次，积分加 [0]）
- 取模运算中负数未转正

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/poly/fundamental/](https://oi-wiki.org/math/poly/fundamental/)
- oiwiki-intro ✓ [https://oi-wiki.org/math/poly/intro/](https://oi-wiki.org/math/poly/intro/)
- oiwiki-intro-raw ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/poly/intro.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/poly/intro.md)
- Wikipedia ✓ [https://en.wikipedia.org/wiki/Formal_power_series](https://en.wikipedia.org/wiki/Formal_power_series)
