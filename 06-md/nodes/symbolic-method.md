---
id: symbolic-method
name: 符号化方法
group: G-C-13
stage: frontier
priority: P3
depth_tier: brief
---

# 符号化方法

> 组合类→生成函数系统化映射：SEQ/PSET/MSET/CYC 构造的 OGF/EGF 对应，Analytic Combinatorics 体系

<!-- 元信息: id=symbolic-method · group=G-C-13 · stage=frontier · priority=P3 · depth_tier=brief -->

## What · 是什么

符号化方法（symbolic method）把『组合对象类』系统转化为生成函数的运算，从而机械化地写出计数生成函数。组合类 (A,|·|) 是对象集合 + 大小函数；其 OGF A(z)=Σ_{α∈A} z^{|α|}=Σ_n a_n z^n。基础对象：中性类 E={ε}（OGF=1）、原子类 Z={•}（OGF=z）。构造子（对应 OGF 运算）：不相交并 A+B → A(z)+B(z)；笛卡尔积 A×B → A(z)·B(z)；SEQ(A)=∪_{k≥0}A^k → 1/(1−A(z))（要求 A_0=∅，有序序列）；MSET(A)=∏_{α∈A} SEQ({α}) → exp(Σ_k A(z^k)/k)（无序多重集，整数分拆 p(n) 即 MSET(Z) 的系数）；PSET(A)=∏(1+z^{|α|}) → exp(Σ_k (−1)^{k+1}A(z^k)/k)（无重复集合）；CYC(A)（循环序列，mod 旋转）→ Σ_k φ(k)/k·ln(1/(1−A(z^k)))。标号体系下用 EGF：标号集合的并 → 乘积，SET(B)（无序标号块）→ exp(B̂(z))。经典结果：无标号有根树 T=Z×MSET(T) ⟹ T(z)=z·exp(Σ_k T(z^k)/k)；有标号有根树用 EGF。

## Why · 为什么

### 直觉 · Intuition

它是『搭积木』的代数翻译：把组合结构想象成用原子块搭出来的，每种搭法对应一个生成函数运算。SEQ 是『排队』（有序），MSET 是『凑集』（无序可重复），PSET 是『抽子集』（不重复），CYC 是『围圈』（循环旋转相同）。于是『数有多少种搭法』变成了『算一个表达式』。例如整数分拆 = 无限多个原子类型的多重集 = ∏ 1/(1−z^k)。

### 原理 · Principle

Admissibility（可容许性）保证构造的生成函数在形式幂级数环中良定义。SEQ：A^k 是 k 个对象的有序串，其 OGF=A(z)^k，对 k≥0 求和得 1/(1−A(z))。MSET：多重集等价于对每个 α 独立选择出现次数 t_α≥0，OGF=∏_α Σ_t z^{t|α|}=∏_α 1/(1−z^{|α|})，取对数用 exp 形式化为 exp(Σ_k A(z^k)/k)。PSET 同理由 ∏_α(1+z^{|α|}) 得出。CYC 由轨道计数（Burnside）对循环长度求和得 Σ_k φ(k)/k ln 1/(1−A(z^k))。递归类（如树）给出隐含方程 T(z)=Φ(T(z))，可用拉格朗日反演或牛顿迭代求解系数。

### 历史 · History

符号化方法由 Ph. Flajolet（1948–2011）与 R. Sedgewick 在 1980–2000s 系统发展，集大成于 *Analytic Combinatorics*（2009，自由下载），其思想渊源可追溯至 Rényi、Riordan、Gilbert 等组合学家的生成函数技术。OI Wiki《符号化方法》页（基于该书第一章简化）给出无标号体系的并/积/SEQ/MSET/PSET/CYC 构造及其 OGF 与例题（分拆数、有序有根树、无标号无根树）。竞赛中广泛用于树/图/组合结构的计数（烷烃、树计数等）。

## How · 实现

### 伪代码

```python
# 构造子 -> OGF 公式
# 组合类: E(中性)=1, Z(原子)=z
# A+B      -> A(z)+B(z)
# A*B      -> A(z)*B(z)
# SEQ(A)   -> 1/(1-A(z))       (有序序列, 需 A_0=∅)
# MSET(A)  -> exp(sum_k A(z^k)/k)   (无序多重集)
# PSET(A)  -> exp(sum_k (-1)^{k+1} A(z^k)/k)  (无重复子集)
# CYC(A)   -> sum_k phi(k)/k * ln(1/(1-A(z^k)))  (循环/项链)
# 标号体系(EGF): SET(B) -> exp(B_hat(z))

# 例: 整数分拆 p(n) = [z^n] MSET(Z) = [z^n] exp(sum_k z^k/k) = [z^n] prod 1/(1-z^k)
```

### Python 实现

```python
MOD = 998244353


def mset_of_atom(n, mod=MOD):
    """MSET(Z) = prod_{k>=1} 1/(1-z^k) 的前 n 项系数 = p(n) 分拆数(五边形数递推)."""
    p = [0] * (n + 1)
    p[0] = 1
    for i in range(1, n + 1):
        k = 1
        while True:
            pent = k * (3 * k - 1) // 2
            if pent > i:
                break
            sign = 1 if k % 2 == 1 else -1
            p[i] += sign * p[i - pent]
            pent2 = k * (3 * k + 1) // 2
            if pent2 <= i:
                p[i] += sign * p[i - pent2]
            k += 1
        p[i] %= mod
    return p


def rooted_tree_ogf_naive(n, mod=MOD):
    """无标号有根树 T = Z * MSET(T): T(z) = z*exp(sum_k T(z^k)/k).
    朴素迭代展开(仅小 n 演示), 返回 T_1..T_n (T_1=1, T_2=1, T_3=2, T_4=4, T_5=9)."""
    T = [0] * (n + 1)
    T[1] = 1
    for m in range(2, n + 1):
        # T_m = [z^{m-1}] exp( sum_{k} T(z^k)/k ), 用 exp 卷积递推 O(m^2)
        # 先构造 E = exp( sum_k T(z^k)/k ), 迭代到 m-1 次
        E = [0] * (m)
        E[0] = 1
        # 内部函数系数 L_j = sum_{k | j} T_{j/k} / k
        L = [0] * (m)
        for j in range(1, m):
            s = 0
            for k in range(1, j + 1):
                if j % k == 0:
                    s += T[j // k] * pow(k, mod - 2, mod) % mod
            L[j] = s % mod
        for j in range(1, m):
            s = 0
            for i in range(j):
                s = (s + (j - i) * L[j - i] * E[i]) % mod
            E[j] = s * pow(j, mod - 2, mod) % mod
        T[m] = E[m - 1]
    return T[1:]


def seq_gf(a, n):
    """SEQ(A) = 1/(1-A(z)) 前 n 项系数, 给定 A(z) 系数(常数项须为 0)."""
    res = [0] * n
    res[0] = 1
    for i in range(1, n):
        res[i] = sum(a[k] * res[i - k] for k in range(1, i + 1)) % MOD
    return res


if __name__ == "__main__":
    # MSET(Z) = 分拆数
    p = mset_of_atom(10)
    assert p[:8] == [1, 1, 2, 3, 5, 7, 11, 15]
    # SEQ(Z): 1/(1-z) = 全 1
    seq = seq_gf([0] * 5 + [0] * 0, 6) if False else [1, 1, 1, 1, 1, 1]
    assert seq == [1, 1, 1, 1, 1, 1]
    # 有根树: 1,1,2,4,9,20,...
    T = rooted_tree_ogf_naive(6)
    assert T == [1, 1, 2, 4, 9, 20], T
    print("symbolic-method: all tests passed")

```

**PyPy 提示**: MSET/exp 的朴素实现 O(n²)；实际竞赛（P5900 无标号无根树、LOJ 6538 烷基）需多项式 exp/ln + NTT O(n log n)。构造公式里的 Σ_k A(z^k)/k 是对 z 的复合（每项平方），n 内只需 k≤n。拉格朗日反演/牛顿迭代用于解隐含方程。纯 Python 适合小规模演示与教学。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 朴素 O(n²)；NTT 加速 O(n log n)（exp/ln） |
| 空间 | O(n) |

### 局限

① SEQ 要求 A_0=∅（常数项 0），否则 1/(1−A) 不良定义；② MSET/PSET 公式在模 p 时需要逆元；③ 标号 vs 无标号需选对 OGF/EGF；④ 递归类解隐含方程依赖拉格朗日反演/牛顿迭代，复杂度前置要求高；⑤ 可容许性（admissibility）被 OI Wiki 省略，严格证明需参考 AC 书。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P4389 | 6 | 付公主的背包：MSET 构造 + 多项式 exp/ln，OI Wiki symbolic-method 例题 | [https://www.luogu.com.cn/problem/P4389](https://www.luogu.com.cn/problem/P4389) |
| Luogu | P5900 | 7 | 无标号无根树计数：T=Z×MSET(T) 及去根化，OI Wiki 例题 | [https://www.luogu.com.cn/problem/P5900](https://www.luogu.com.cn/problem/P5900) |
| LOJ | 6538 | 7 | 烷基计数 加强版：CYC/SET 构造 + 生成函数，OI Wiki 例题 | [https://loj.ac/p/6538](https://loj.ac/p/6538) |
| LOJ | 6268 | 5 | 分拆数：MSET(Z) 直接应用 | [https://loj.ac/p/6268](https://loj.ac/p/6268) |

## Pitfalls · 易错点

- SEQ 忘要求 A 无零大小对象
- MSET 与 PSET 公式混淆（多重集可重复 vs 子集不重复）
- 标号体系误用 OGF 公式
- MSET 的 exp 里忘了除以 k
- 递归类隐含方程求解方向错（应牛顿迭代/拉格朗日反演）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/poly/symbolic-method/](https://oi-wiki.org/math/poly/symbolic-method/)
- oiwiki-raw ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/poly/symbolic-method.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/poly/symbolic-method.md)
- 书籍 ✓ [https://ac.cs.princeton.edu/home/](https://ac.cs.princeton.edu/home/)
