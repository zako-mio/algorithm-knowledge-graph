---
id: egf
name: EGF(指数生成函数)
group: G-C-13
stage: advanced
priority: P2
depth_tier: standard
---

# EGF(指数生成函数)

> 序列 a 的指数生成函数 F̂(x)=Σ a_n x^n/n!，乘法=二项式卷积，标号结构计数工具，e^{e^x-1} 等

<!-- 元信息: id=egf · group=G-C-13 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

指数生成函数（exponential generating function，EGF）把序列 a 编码为 F̂(x)=Σ_n a_n x^n/n!。加减仍按项；乘法变为二项式卷积：F̂(x)Ĝ(x)=Σ_n x^n/n! · Σ_{i=0}^n C(n,i) a_i b_{n−i}，即新系数 c_n=Σ C(n,i)a_i b_{n−i}。这种『除以 n!』编码专为标号（labeled）结构设计：把 n 个有标号元素切成两块大小 i 和 n−i 时，分块有 C(n,i) 种选法，恰被 EGF 乘法的二项式系数吸收。常用封闭形式：⟨1,1,1,…⟩→e^x；等比 ⟨1,p,p²,…⟩→e^{px}；阶乘 ⟨n!⟩→1/(1−x)；贝尔数 B_n→e^{e^x−1}；错排 D_n→e^{−x}/(1−x)；第二类斯特林数（固定 k）→(e^x−1)^k/k!；第一类斯特林数（固定 k）→ln(1/(1−x))^k/k!。标号与无标号的对照：OGF 处理无标号（多重集），EGF 处理标号（排列、划分、标号树）。e^x 的组合意义是『按大小分块』的核心，exp 对应 SET 构造（无序标号集合）。

## Why · 为什么

### 直觉 · Intuition

无标号结构合并时『大小相加』即可（OGF 乘法）；但标号结构（元素各不相同）合并时，两块的元素要先从 n 个标号中挑选再各自排列，出现 C(n,i) 因子。EGF 的除以 n! 恰好把这个因子吸收进乘法：F̂Ĝ 的第 n 项自动带 C(n,i)。于是『标号结构的并/笛卡尔积』在 EGF 下依然是简单乘法，就像 OGF 对无标号结构一样。e^x 是『任意标号集合的平凡选择』的生成函数。

### 原理 · Principle

乘法公式推导：Σ_i a_i x^i/i! · Σ_j b_j x^j/j! = Σ_n x^n Σ_{i+j=n} a_i b_j/(i!j!) = Σ_n x^n/n! · Σ_i C(n,i) a_i b_{n−i}（因 n!/(i!(n−i)!)=C(n,i)）。标号结构的并（SET）与指数 exp 的关系：SET(B)=∪_k B^k/k!（无序分块要去掉 k! 种顺序），对应 EGF exp(B̂(x))。贝尔数 B_n 即 SET(SET≥1(原子))：一个集合划分 = 若干非空块的无序集合 ⇒ EGF=exp(e^x−1)。错排 EGF=e^{−x}/(1−x) 由容斥 D_n=n!Σ(−1)^k/k! 直接写出。

### 历史 · History

EGF 由 Laplace（1812）引入生成函数概念时即有雏形，组合意义在标号结构计数中由 Rényi、Riordan（*An Introduction to Combinatorial Analysis*, 1958）系统发展；Flajolet & Sedgewick 的 *Analytic Combinatorics*（2009）把 EGF 与符号化方法整合为标号体系。OI Wiki《指数生成函数》页给出定义、二项式卷积、封闭形式与 exp 的组合意义（SET 构造）。竞赛中 EGF 用于集合划分、排列统计、标号树、多项式 exp 等。

## How · 实现

### 伪代码

```python
# EGF 运算 (存储系数为 a_n/n! 的普通列表? 更常用存原始 a_n 并配 n!)
# 约定: 存原始序列 a, 运算时除以阶乘

def egf_mul_coeff(a, b):   # 返回原始系数 c_n = sum C(n,i) a_i b_{n-i}
  c = [0]*(len(a)+len(b)-1)
  for i in range(len(a)):
    for j in range(len(b)):
      c[i+j] += comb(i+j, i) * a[i] * b[j]
  return c

def exp_series(n, p=1):    # e^{px} 前 n 项, 原始系数 p^k
  return [p**k for k in range(n)]

def bell_egf(n):           # B_n 由 e^{e^x-1} 得 (需多项式 exp)
  ...

def derangement_egf(n):    # e^{-x}/(1-x) 的原始系数 = 错排 D_n
  a = exp_series(n, -1)    # e^{-x}: 系数 (-1)^k
  b = [1]*n                # 1/(1-x): 系数 1
  return egf_mul_coeff(a, b)
```

### Python 实现

```python
from math import comb, factorial


def egf_mul_coeff(a, b):
    """EGF 乘法(二项式卷积) 返回原始序列 c_n = sum_i C(n,i) a_i b_{n-i}."""
    c = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            c[i + j] += comb(i + j, i) * ai * bj
    return c


def egf_mul_from_hat(a_hat, b_hat):
    """若输入已是 a_n/n! 形式, 乘法直接卷积, 返回也是 b_n/n! 形式."""
    c_hat = [0] * (len(a_hat) + len(b_hat) - 1)
    for i, x in enumerate(a_hat):
        for j, y in enumerate(b_hat):
            c_hat[i + j] += x * y
    return c_hat


def derangement_egf(n):
    """错排 EGF e^{-x}/(1-x) = sum D_n x^n/n!. 返回 D_0..D_{n-1}."""
    a = [(-1) ** k for k in range(n)]     # e^{-x}
    b = [factorial(k) for k in range(n)]   # 1/(1-x) 是 n! 的 EGF
    c = egf_mul_coeff(a, b)
    return c


def bell_egf_naive(n, mod=998244353):
    """由 e^{e^x-1} 求贝尔数前 n 项(朴素 O(n^2) 多项式 exp)."""
    inv = [0] * (n + 1)
    for k in range(1, n + 1):
        inv[k] = pow(k, mod - 2, mod)
    a = [0] * (n + 1)
    for k in range(1, n + 1):
        a[k] = pow(inv[k], 1, mod)  # a_k = 1/k! = 对应 e^x-1 的 EGF 系数(除常数)
    # 构建 e^x-1 的 EGF 系数 (1, 1/1!, 1/2!, ...)
    a = [0] * (n + 1)
    f = [1] * (n + 1)
    for k in range(1, n + 1):
        f[k] = f[k - 1] * k % mod
    invf = [1] * (n + 1)
    invf[n] = pow(f[n], mod - 2, mod)
    for k in range(n, 0, -1):
        invf[k - 1] = invf[k] * k % mod
    for k in range(1, n + 1):
        a[k] = invf[k]
    # exp(a), a 常数项=0, 返回 b_hat (B_k/k!)
    b_hat = [0] * (n + 1)
    b_hat[0] = 1
    for k in range(1, n + 1):
        s = 0
        for j in range(k):
            s = (s + (k - j) * a[k - j] * b_hat[j]) % mod
        b_hat[k] = s * inv[k] % mod
    return [b_hat[k] * f[k] % mod for k in range(n + 1)]


if __name__ == "__main__":
    # EGF 乘法: 1/(1-x) (系数全1) * 自己 => c_n = sum C(n,i) = 2^n
    c = egf_mul_coeff([1, 1, 1, 1], [1, 1, 1, 1])
    assert c[:4] == [1, 2, 4, 8]
    # e^{-x}/(1-x): D_n
    d = derangement_egf(7)
    assert d[:6] == [1, 0, 1, 2, 9, 44]
    # 贝尔数 EGF
    b = bell_egf_naive(6)
    assert b[:7] == [1, 1, 2, 5, 15, 52, 203]
    # 二项式卷积直接与 C 匹配
    assert egf_mul_coeff([1, 1], [1, 1]) == [1, 2, 2]   # C(2,1)=2
    print("egf: all tests passed")

```

**PyPy 提示**: 朴素二项式卷积 O(n²)；大规模需 NTT + 除法阶乘。存系数用原始 a_n 但运算记得乘 C 因子，或存 a_n/n! 形式直接卷积再还原。多项式 exp 需要牛顿迭代/分治，纯 Python 仅演示 O(n²)。取模时二项式卷积用组合数模版预计算。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 二项式卷积 O(n²)；NTT 加速 O(n log n) |
| 空间 | O(n) |

### 局限

① EGF 乘法要乘二项式系数，不能直接普通卷积（除非用 a_n/n! 形式）；② 与 OGF 对应不同结构体系，混用会出错；③ exp/ln 操作需要多项式算法支持；④ 系数还原需阶乘，模素数时用阶乘逆元。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P5748 | 4 | 集合划分计数：B_n 的 EGF=e^{e^x−1}，多项式 exp 求整列，EGF 核心应用 | [https://www.luogu.com.cn/problem/P5748](https://www.luogu.com.cn/problem/P5748) |
| Luogu | P4389 | 6 | 付公主的背包：EGF/OGF 乘积取对数差分的生成函数技巧（OI Wiki symbolic-method 例题） | [https://www.luogu.com.cn/problem/P4389](https://www.luogu.com.cn/problem/P4389) |
| LOJ | 6268 | 5 | 分拆数（标号/无标号对照学习 EGF vs OGF） | [https://loj.ac/p/6268](https://loj.ac/p/6268) |

## Pitfalls · 易错点

- 把 EGF 乘法当普通卷积（漏 C(n,i) 因子）
- 还原系数时忘乘 n!
- 标号结构误用 OGF（应 EGF）
- 多项式 exp 常数项必须为 0
- e^{e^x−1} 与 e^x 区分不清

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/poly/egf/](https://oi-wiki.org/math/poly/egf/)
- oiwiki-raw ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/poly/egf.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/poly/egf.md)
- oiwiki-intro ✓ [https://oi-wiki.org/math/poly/intro/](https://oi-wiki.org/math/poly/intro/)
- Wikipedia ✓ [https://en.wikipedia.org/wiki/Generating_function#Exponential_generating_function](https://en.wikipedia.org/wiki/Generating_function#Exponential_generating_function)
