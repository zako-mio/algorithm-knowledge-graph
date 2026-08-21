---
id: ogf
name: OGF(普通生成函数)
group: G-C-13
stage: advanced
priority: P2
depth_tier: standard
---

# OGF(普通生成函数)

> 序列 a 的普通生成函数 F(x)=Σ a_n x^n，加法=按项加、乘法=卷积，封闭形式 1/(1-px) 等比等

<!-- 元信息: id=ogf · group=G-C-13 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

普通生成函数（ordinary generating function，OGF）把序列 a 编码为形式幂级数 F(x)=Σ_n a_n x^n。a 可为有限或无限序列，x^n 的系数就是 a_n（系数即通项）。基本运算：加减=对应项系数相加减；乘法（卷积）= F(x)G(x)=Σ_n x^n Σ_{i=0}^n a_i b_{n−i}，即新序列 c_n=Σ a_i b_{n−i}。常用封闭形式：⟨1,1,1,…⟩→1/(1−x)；等比数列 ⟨1,p,p²,…⟩→1/(1−px)；⟨1,2,3,…⟩→1/(1−x)²；⟨0,1,1,…⟩→x/(1−x)；⟨1,0,1,0,…⟩→1/(1−x²)；⟨C(m,n)⟩→(1+x)^m；⟨C(m+n,n)⟩→1/(1−x)^{m+1}；⟨n²⟩→x(1+x)/(1−x)³。OGF 适用于『无标号/多重集』类组合（整数分拆 ∏1/(1−x^k)、组合数、路径数等），与 EGF（标号结构）互补。配套操作：位移（乘 x 幂）、求导/积分、复合、逆等。

## Why · 为什么

### 直觉 · Intuition

把数列写成一个『无限次多项式』，加减乘等代数操作就变成对整条数列的操作。比如『硬币问题』：用 1 分、2 分凑 n 分的方案数，就是 (1+x+x²+…)(1+x²+x⁴+…) 中 x^n 的系数——每个币种贡献一个几何级数因子，乘法自动做卷积。OGF 让『数数组』变成『算代数式』。

### 原理 · Principle

形式幂级数观点：我们只关心系数，不关心收敛域；F(x)=Σ a_n x^n 中 x 是形式变元。加法/乘法定义为系数运算（卷积），使序列空间成为环 R[[x]]。封闭形式的推导是代数等式而非分析等式：如 F=Σ x^n 满足 F·x+1=F ⟹ F=1/(1−x)。OGF 对『可分解为独立部件』的结构自然：若结构由部件组合而成且部件大小相加，总 OGF = 各部件的 OGF 之积（与 symbolic method 的 SEQ/MSET 构造衔接）。

### 历史 · History

生成函数思想由 Euler（18 世纪）用于分拆数与解析数论；Laplace、Cauchy 等发展。『生成函数』术语来自 Laplace（1812）。OGF 是组合数学『符号化方法』（Flajolet & Sedgewick, *Analytic Combinatorics*, 2009）的无标号基石。OI Wiki《普通生成函数》页给出定义、运算与封闭形式小练习；《多项式与生成函数》页给出形式幂级数环的严格框架。竞赛中 OGF 广泛用于背包计数、递推数列、线性递推求解。

## How · 实现

### 伪代码

```python
# 多项式/形式幂级数 OGF 运算 (系数列表, 低次在前)

def add(a, b): return [(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))]

def mul(a, b):
  c = [0]*(len(a)+len(b)-1)
  for i,x in enumerate(a):
    for j,y in enumerate(b): c[i+j] += x*y
  return c

def diff(a):   # 求导
  return [i*a[i] for i in range(1, len(a))]

def integ(a):  # 积分 (x^k -> x^{k+1}/(k+1))
  return [0] + [a[k-1]//k for k in range(1, len(a)+1)]

def shift(a, d): return [0]*d + a    # 乘 x^d

def geometric(seq_len, p): return [p**i for i in range(seq_len)]  # 1/(1-px)
```

### Python 实现

```python
from math import comb


def ogf_add(a, b):
    n = max(len(a), len(b))
    return [((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)) for i in range(n)]


def ogf_mul(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    return c


def ogf_scale(a, k):
    return [x * k for x in a]


def geometric_series(n, p=1):
    """1/(1-px) 的前 n 项: [1, p, p^2, ...]."""
    res = [1]
    cur = 1
    for _ in range(n - 1):
        cur *= p
        res.append(cur)
    return res


def closed_1_minus_x2(n):
    """1/(1-x^2) 的前 n 项: [1,0,1,0,1,...]."""
    return [1 if i % 2 == 0 else 0 for i in range(n)]


def ogf_binom_fixed_m(n, m):
    """(1+x)^m 的前 n 项: [C(m,0), C(m,1), ...]."""
    return [comb(m, k) for k in range(min(n, m + 1))]


def ogf_inv_1_minus_x_km1(n, m):
    """1/(1-x)^{m+1} 的前 n 项: [C(m,0), C(m+1,1), ..., C(m+i,i)]."""
    return [comb(m + i, i) for i in range(n)]


def closed_form_multiplication(n):
    """验证 (1-x)^-2 = sum (k+1)x^k: 用乘法自检 1/(1-x)^2 系数."""
    a = geometric_series(n)
    b = ogf_mul(a, a)
    return b


if __name__ == "__main__":
    # 封闭形式(取前若干项) 验证
    assert geometric_series(6) == [1, 1, 1, 1, 1, 1]
    assert geometric_series(5, 2) == [1, 2, 4, 8, 16]
    assert closed_1_minus_x2(6) == [1, 0, 1, 0, 1, 0]
    # 1/(1-x)^2 = 1,2,3,4,...
    sq = closed_form_multiplication(6)
    assert sq[:6] == [1, 2, 3, 4, 5, 6]
    # 等比 * 等比 = 卷积
    assert ogf_mul(geometric_series(4), [1, 3]) == [1, 4, 4, 4, 3]
    # (1+x)^m 展开
    assert ogf_binom_fixed_m(6, 3) == [1, 3, 3, 1]
    # 1/(1-x)^4 系数 = C(3+i, i)
    assert ogf_inv_1_minus_x_km1(5, 3) == [comb(3, 0), comb(4, 1), comb(5, 2), comb(6, 3), comb(7, 4)]
    # OI Wiki 小练习: a=<0,1,1,1,...> => x/(1-x)
    x_over_1mx = ogf_mul([0, 1], geometric_series(6))
    assert x_over_1mx[:6] == [0, 1, 1, 1, 1, 1]
    print("ogf: all tests passed")

```

**PyPy 提示**: 朴素卷积 O(n²)，n≤2000 可直接；大规模用 NTT/FFT。形式幂级数取模运算注意系数取 mod 与乘法逆元（1/(1−px) 在有限域需 p 可逆）。位移用列表拼接比循环快。Python 做 OGF 演示以教育为主，实际竞赛大 n 用 NTT 库/C++。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 加法 O(n)；卷积 O(n²)（朴素）/ O(n log n)（NTT） |
| 空间 | O(n) |

### 局限

① 形式幂级数是『系数对象』，收敛性无关但运算需谨慎（如 (1−x)^{-1} 有限域上要求 1−x 可逆）；② 朴素卷积太慢需 NTT；③ OGF 与 EGF 不要混用（同序列两种编码不同）；④ 某些无穷和没有简单封闭形式。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3028 | 4 | 食物：经典 OGF 乘法计数（BZOJ P3028），OI Wiki ogf 页例题 | [https://www.luogu.com.cn/problem/P3028](https://www.luogu.com.cn/problem/P3028) |
| Luogu | P3027 | 4 | CEOI2004 Sweet：生成函数 + 容斥求区间系数和，OI Wiki ogf 页例题 | [https://www.luogu.com.cn/problem/P3027](https://www.luogu.com.cn/problem/P3027) |
| LOJ | 6268 | 5 | 分拆数：OGF ∏1/(1−x^k) 的系数（符号化方法视角） | [https://loj.ac/p/6268](https://loj.ac/p/6268) |

## Pitfalls · 易错点

- 把 OGF 当普通函数求值（形式幂级数不能随便代 x=0.5）
- 卷积实现忘记初始化长度
- 封闭形式 1/(1−px) 的 p 写成 1
- 系数下标偏移（a_0 对应 x^0）
- 无标号用 EGF 或用 OGF 处理标号结构（应各自对应）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/poly/ogf/](https://oi-wiki.org/math/poly/ogf/)
- oiwiki-raw ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/poly/ogf.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/poly/ogf.md)
- oiwiki-intro ✓ [https://oi-wiki.org/math/poly/intro/](https://oi-wiki.org/math/poly/intro/)
- Wikipedia ✓ [https://en.wikipedia.org/wiki/Generating_function](https://en.wikipedia.org/wiki/Generating_function)
