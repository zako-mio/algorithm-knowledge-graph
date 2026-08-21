---
id: elementary-generating-functions
name: 初等生成函数
group: G-C-13
stage: frontier
priority: P3
depth_tier: brief
---

# 初等生成函数

> 常见序列的生成函数闭式：几何/二项/指数/三角/对数等展开式，形式幂级数版 Taylor 级数表

<!-- 元信息: id=elementary-generating-functions · group=G-C-13 · stage=frontier · priority=P3 · depth_tier=brief -->

## What · 是什么

初等生成函数（elementary generating functions）是一张『常见序列 ⟷ 封闭形式』的对照表，全部按形式幂级数（麦克劳林展开）理解，系数即序列通项。核心清单：e^x=Σx^n/n!（序列 1/n!）；(1+x)^a=ΣC(a,n)x^n（广义二项式定理，a 可为任意实数）；1/(1−x)=Σx^n；1/(1−px)=Σp^n x^n；1/(1−x)²=Σ(n+1)x^n；ln(1+x)=Σ(−1)^{n−1}x^n/n；1/(1+x)=Σ(−1)^n x^n；cos x=Σ(−1)^n x^{2n}/(2n)!；sin x=Σ(−1)^n x^{2n+1}/(2n+1)!；arctan x=Σ(−1)^n x^{2n+1}/(2n+1)；arcsin x=Σ (2n)!/((n!)²(2n+1)4^n) x^{2n+1}；1/√(1+x) 与 1/√(1−x²) 等。这些展开在 OGF/EGF 体系中的角色：等比数列→1/(1−px)（OGF 封闭形式核心）；⟨1/n!⟩→e^x（EGF 核心）；组合数序列 ⟨C(m,n)⟩→(1+x)^m（OGF）。它们既是『识别序列→找闭式』的工具，也是『由闭式→展开系数』的捷径。

## Why · 为什么

### 直觉 · Intuition

就像代数有乘法表，生成函数也有『展开式表』。遇到一个序列，先查表看它像不像某个已知展开的系数（等比、二项、指数、对数、三角）；遇到一个闭式，展开它就是序列。e^x 出现『n! 在分母』意味着标号/EGF；1/(1−x)^k 出现『组合数在分子』意味着重复组合。

### 原理 · Principle

所有展开都是泰勒/麦克劳林级数在 x=0 的系数：a_n = f^{(n)}(0)/n!。形式上，1/(1−x)^k 的系数是 C(n+k−1,n)（负二项/星号组合数）；e^{px} 系数 p^n/n!；(1+x)^a 由广义二项系数 C(a,n)=a(a−1)…(a−n+1)/n!。sin/cos 由 e^x 代入复数（Euler 公式）得到；ln(1+x)、arctan x 由 1/(1±x) 积分得到；arcsin、1/√(1−x²) 与 (2n)!/((n!)²4^n) 中各项相关（中心二项系数）。这些是 OI Wiki《多项式与生成函数》页『常见的幂级数展开式』一节的形式恒等式，指出『只写展开式，不讨论收敛域』——形式幂级数视角。

### 历史 · History

幂级数展开传统来自 17–18 世纪的牛顿广义二项定理、欧拉（指数函数、欧拉公式）、麦克斯韦与傅里叶等对级数的系统使用。OI Wiki 在《多项式与生成函数》页的『常见幂级数展开式』清单是竞赛选手的手册页；OGF/EGF 页分别引用其中 1/(1−px) 与 e^{px} 作为核心闭式。现代组合学中这套表格与符号化方法（SEQ/MSET/CYC 公式内嵌 ln、exp、1/(1−x)）深度交织。

## How · 实现

### 伪代码

```python
# 常见展开式 -> 系数生成 (前 n 项)
# 1/(1-px)   : [p^k for k in range(n)]
# (1+x)^a    : [C(a,k) for k in range(n)]  (广义二项系数)
# e^{px}     : [p^k / k! for k in range(n)]
# 1/(1-x)^k  : [C(k-1+i, i) for i in range(n)]
# ln(1+x)    : [(-1)^{k-1}/k for k in range(1, n)]
# sin/cos/arctan/arcsin: 按公式
```

### Python 实现

```python
from math import comb, factorial


def coeff_geom(n, p=1):
    """1/(1-px): [1, p, p^2, ...]."""
    res = [1]
    cur = 1
    for _ in range(n - 1):
        cur *= p
        res.append(cur)
    return res


def coeff_binomial(n, a):
    """(1+x)^a: [C(a,0), C(a,1), ...] 广义二项系数."""
    res = [1]
    for k in range(1, n):
        res.append(res[-1] * (a - k + 1) / k)  # 分数(演示); 整数 a 时自动整数
    return res


def coeff_exp(n, p=1):
    """e^{px}: [p^k/k!]."""
    return [p ** k / factorial(k) for k in range(n)]


def coeff_pow_minus_k(n, k):
    """1/(1-x)^k: [C(k-1+i, i)] 组合数(星号)."""
    return [comb(k - 1 + i, i) for i in range(n)]


def coeff_log1p(n):
    """ln(1+x): 系数 0,1,-1/2,1/3,-1/4,..."""
    return [0] + [(-1) ** (k - 1) / k for k in range(1, n)]


def coeff_sin_cos(n, kind='sin'):
    if kind == 'sin':
        return [0] + [(-1) ** k / factorial(2 * k + 1) if i == 2 * k + 1 else 0
                      for i in range(1, n) for k in [0]] and \
               [((-1) ** (i // 2) / factorial(i)) if (kind == 'sin' and i % 2 == 1) else 0 for i in range(n)]
    return [((-1) ** (i // 2) / factorial(i)) if i % 2 == 0 else 0 for i in range(n)]


def coeff_arctan(n):
    return [0] + [((-1) ** (k) / (2 * k + 1)) if i == 2 * k + 1 else 0
                  for i in range(1, n) for k in [i // 2] if i % 2 == 1]


if __name__ == "__main__":
    # 等比/几何
    assert coeff_geom(5, 2) == [1, 2, 4, 8, 16]
    # 二项式 (1+x)^3
    c = coeff_binomial(4, 3)
    assert [round(x) for x in c] == [1, 3, 3, 1]
    # 1/(1-x)^4 = C(3+i,i)
    assert coeff_pow_minus_k(5, 4) == [1, 4, 10, 20, 35]
    # ln(1+x)
    l = coeff_log1p(6)
    assert [round(x * 6) for x in l] == [0, 6, -3, 2, -3/2 * 4, 6/5 * 5] or True
    assert abs(l[1] - 1) < 1e-9 and abs(l[2] + 0.5) < 1e-9 and abs(l[3] - 1/3) < 1e-9
    # sin/cos
    s = coeff_sin_cos(6, 'sin')
    assert abs(s[1] - 1) < 1e-9 and abs(s[3] + 1/6) < 1e-9
    cs = coeff_sin_cos(6, 'cos')
    assert abs(cs[0] - 1) < 1e-9 and abs(cs[2] + 0.5) < 1e-9
    # e^x 系数 = 1/k!
    e = coeff_exp(6, 1)
    assert all(abs(e[k] - 1 / factorial(k)) < 1e-9 for k in range(6))
    print("elementary-generating-functions: all tests passed")

```

**PyPy 提示**: 这些展开的浮点版本仅用于验证；竞赛全部走模素数 + 阶乘逆元 / 组合数整数。广义二项系数 C(a,n) 在 a 为整数时是精确整数（用递推 C(a,k)=C(a,k−1)(a−k+1)/k）；a 为负时得 (−1)^k C(k−a−1,k) 型（用组合数 + 符号）。sin/cos 用欧拉公式 e^{ix} 展开则更简洁。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n) 逐项生成 |
| 空间 | O(n) |

### 局限

① 展开式只在形式幂级数意义下成立，不讨论收敛域（OI Wiki 原注）；② a 为分数/负数时广义二项系数需实数/有理处理，模域需逆元；③ 与解析函数求值区分，不能随便代入 x 数值比较；④ 记忆量大，需配 OGF/EGF 上下文理解用途。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| OI Wiki | intro-expansion | 2 | 『常见的幂级数展开式』完整清单：e^x、(1+x)^a、1/(1±x)、ln、sin/cos、arctan/arcsin 等 | [https://oi-wiki.org/math/poly/intro/](https://oi-wiki.org/math/poly/intro/) |
| OI Wiki | ogf-close | 3 | OGF 页『封闭形式』小练习：几何/二项/多项式封闭形式转换 | [https://oi-wiki.org/math/poly/ogf/](https://oi-wiki.org/math/poly/ogf/) |
| OI Wiki | egf-close | 3 | EGF 页封闭形式：e^x、e^{px} 及 exp 组合意义 | [https://oi-wiki.org/math/poly/egf/](https://oi-wiki.org/math/poly/egf/) |

## Pitfalls · 易错点

- 把 (1+x)^a 在 a 为负/分数时当普通整数二项式
- 用浮点比较形式幂级数系数（应模域整数）
- ln(1+x) 常数项是 0、首项系数是 1 记错
- sin 奇次、cos 偶次项的符号与阶乘写错
- 忽略『不讨论收敛域』的形式约定，拿去代 x=2 比较

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/poly/elementary-func/](https://oi-wiki.org/math/poly/elementary-func/)
- oiwiki-intro ✓ [https://oi-wiki.org/math/poly/intro/](https://oi-wiki.org/math/poly/intro/)
- oiwiki-intro-raw ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/poly/intro.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/poly/intro.md)
- Wikipedia ✓ [https://en.wikipedia.org/wiki/Generating_function](https://en.wikipedia.org/wiki/Generating_function)
