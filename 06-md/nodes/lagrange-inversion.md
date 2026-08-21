---
id: lagrange-inversion
name: 拉格朗日反演
group: G-C-12
stage: frontier
priority: P3
depth_tier: brief
---

# 拉格朗日反演

> O(n log n)求复合逆的系数，生成函数计数的高级工具

<!-- 元信息: id=lagrange-inversion · group=G-C-12 · stage=frontier · priority=P3 · depth_tier=brief -->

## What · 是什么

拉格朗日反演（Lagrange Inversion）给出形式幂级数复合逆系数的闭式：若 f(x)=Σ_{k>=1} f_k x^k 且 f_1≠0，则 f 有唯一复合逆 g（即 f(g(x))=x）。对任意形式幂级数（或形式 Laurent 级数）Φ 有 [x^n]Φ(f(x))=[x^{n-1}]Φ(x)·g'(x)/g(x)·(x/g(x))^n。特例 [x^n] f(x)^k = (k/n)[x^{n-k}](x/g(x))^n。利用该公式可在 O(n log n)（NTT 加速幂与导数）内求复合逆的前 n 项。是生成函数计数（树、平面二叉树、带标号组合结构等）的高级工具，用于求解'自指方程'的显式系数。

## Why · 为什么

### 直觉 · Intuition

复合逆 g 满足 g(f(x))=x，直接解 g 的系数是耦合方程组。拉格朗日反演说：g 的第 n 项可以从 f 的某次幂的特定系数直接读出——因为代换 g 相当于'重新参数化'，留数/围道思想把系数变成幂的系数。

### 原理 · Principle

形式留数 res(f)=[x^{-1}]f 满足链式法则 res(Φ(f(x))f'(x))=ord(f)·res(Φ)。令 g=f^{<-1>}，则 [x^n]Φ(f)=res(Φ(f)/x^{n+1})。代换 x→g(x)，利用 g'(x)dx 的链式性质与 res 的换元公式，得 [x^n]Φ(f(x))=res(Φ(x)g'(x)/g(x)^{n+1})=[x^{-1}]Φ(x)g'(x)/g(x)^{n+1}。再令 Φ(x)=x^k 并整理 g'(x)/g(x)^{n+1}=(1/n)(1/g(x)^n)'，得到常用形式。

### 历史 · History

拉格朗日反演由 Joseph-Louis Lagrange 在 1770 年提出（解 Kepler 方程时），后经 Bürmann 推广。是解析组合学（Analytic Combinatorics，Flajolet & Sedgewick）的标准工具。OI Wiki 的 poly/lagrange-inversion 页面给出形式 Laurent 级数框架下的严谨推导。

## How · 实现

### 伪代码

```python
# 求 f 的复合逆 g 前 n 项
# 用 [x^n]g(x) = (1/n)[x^{n-1}](x/f(x))^n
inv_f = inverse(f/x, n)      # 幂级数逆
for n in 1..N:
    g[n] = (1/n) * [x^{n-1}] (inv_f)^n   # 幂用 NTT 快速幂
# 或者逐项解 f(g)=x(朴素)
```

### Python 实现

```python
MOD = 998244353


def lagrange_inversion_naive(f, n):
    """拉格朗日反演(朴素 O(n^3), 教学验证版):
    f(x) = sum_{k>=1} f_k x^k, f_1 != 0. 求复合逆 g 使 f(g(x)) = x, 前 n 项.
    公式: [x^n] g(x) = 1/n * [x^{n-1}] (x/f(x))^n.
    这里用幂级数除法直接解 g: f(g(x)) = x 逐项确定 g 系数。"""
    f = f[:n]
    assert f[0] == 0 and f[1] != 0
    g = [0] * n
    g[1] = pow(f[1], MOD - 2, MOD)
    # f(g(x)) = sum f_k g(x)^k = x
    # 逐项: [x^n] sum_{k>=1} f_k g(x)^k = delta_{n,1}
    for m in range(2, n):
        # 未知 g[m], 贡献来自 k=1 项: f_1 * g[m] * x^m
        # 已知项: sum_{k>=2} f_k [x^m] g(x)^k + f_1*[x^m] g(x) 中 g_m 未知
        # 用递推: f_1 g_m + sum_{k>=2} f_k [x^m] g^k = 0
        s = 0
        for k in range(2, n):
            # [x^m] g^k, 只含 g_0..g_{m-1} (因为 k>=2, g_1>=1 次)
            c = coeff_pow(g, k, m)
            s = (s + (f[k] if k < len(f) else 0) * c) % MOD
        g[m] = (-s * pow(f[1], MOD - 2, MOD)) % MOD
    return g


def coeff_pow(g, k, m):
    """[x^m] g(x)^k, g[0]=0, 用卷积逐层。O(k*m^2) 教学版。"""
    cur = [1]
    for _ in range(k):
        new = [0] * (len(cur) + len(g) - 1)
        for i, x in enumerate(cur):
            if x == 0:
                continue
            for j, y in enumerate(g):
                new[i + j] = (new[i + j] + x * y) % MOD
        cur = new
        if len(cur) > m + 1:
            cur = cur[:m + 1]
    return cur[m] if m < len(cur) else 0


def compose_verify(g, f, n):
    """验证 f(g(x)) = x mod x^n。"""
    # g 已是 f 的复合逆, 验证 f(g) 用逐项合成
    cur = [1]
    res = [0] * n
    for k in range(n):
        if k == 0:
            cur = [1]
        else:
            new = [0] * (len(cur) + len(g) - 1)
            for i, x in enumerate(cur):
                if x == 0:
                    continue
                for j, y in enumerate(g):
                    if i + j < n:
                        new[i + j] = (new[i + j] + x * y) % MOD
            cur = new[:n]
        c = f[k] if k < len(f) else 0
        if c:
            for i in range(min(len(cur), n)):
                res[i] = (res[i] + c * cur[i]) % MOD
    return res


if __name__ == "__main__":
    # 例: f(x) = x + x^2, 复合逆满足 g + g^2 = x
    # g(x) = x - x^2 + 2x^3 - 5x^4 + ... (Catalan 数相关)
    f = [0, 1, 1]
    g = lagrange_inversion_naive(f, 10)
    # 验证 f(g(x)) = x
    c = compose_verify(g, f, 10)
    assert c == [0, 1, 0, 0, 0, 0, 0, 0, 0, 0], c
    assert g[0] == 0 and g[1] == 1 and g[2] == MOD - 1, g  # x - x^2 + ...
    # 例: f(x) = x - x^2/2, 复合逆 g + g^2/2 = x
    inv2 = (MOD + 1) // 2
    f2 = [0, 1, (-inv2) % MOD]
    g2 = lagrange_inversion_naive(f2, 8)
    c2 = compose_verify(g2, f2, 8)
    assert c2 == [0, 1, 0, 0, 0, 0, 0, 0], c2
    print("lagrange-inversion tests passed")

```

**PyPy 提示**: 朴素逐项解 O(n^3) 教学用; 真正 O(n log n) 需要 NTT 快速幂+幂级数逆, Python 常数大, 大规模不现实。教学版演示 f(g(x))=x 验证。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 朴素 O(n^3); NTT 版 O(n log n) |
| 空间 | O(n) |

### 局限

要求 f(0)=0 且 f'(0)≠0(否则无复合逆); 公式中 g'(x)/g(x) 在 g(0)=0 处是形式 Laurent 级数, 需按定义处理; 朴素实现慢, 大规模需全套 NTT 多项式库; Python 仅适合小规模教学验证。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P4277 | 6 | 拉格朗日反演类模板(复合逆系数), 前沿训练 | [https://www.luogu.com.cn/problem/P4277](https://www.luogu.com.cn/problem/P4277) |
| AtCoder | abc236_h | 6 | 生成函数+容斥类: 拉格朗日反演思路的高难应用 | [https://atcoder.jp/contests/abc236/tasks/abc236_h](https://atcoder.jp/contests/abc236/tasks/abc236_h) |
| Luogu | P4482 | 6 | 组合结构计数: 树/二叉树等生成函数反演应用 | [https://www.luogu.com.cn/problem/P4482](https://www.luogu.com.cn/problem/P4482) |

## Pitfalls · 易错点

- f(0)≠0 或 f'(0)=0 时无复合逆还硬算
- 留数/链式换元公式中 ord(g) 因子遗漏
- [x^n]f^k 公式中的 k/n 系数漏乘
- 形式 Laurent 级数的负次项处理错误
- 朴素逐项法只到小规模, 大规模需 NTT 库

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/poly/lagrange-inversion/](https://oi-wiki.org/math/poly/lagrange-inversion/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/poly/lagrange-inversion.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/poly/lagrange-inversion.md)
