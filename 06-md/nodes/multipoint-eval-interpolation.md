---
id: multipoint-eval-interpolation
name: 多点求值与插值
group: G-C-12
stage: frontier
priority: P3
depth_tier: brief
---

# 多点求值与插值

> O(n log^2 n)多项式多点求值与插值，基于分治与NTT

<!-- 元信息: id=multipoint-eval-interpolation · group=G-C-12 · stage=frontier · priority=P3 · depth_tier=brief -->

## What · 是什么

多点求值：给定 n 次多项式 f(x) 与 n 个点 x_1..x_n，求所有 f(x_i)。朴素 O(n^2)。分治解法：把点分成两半 X0,X1，构造 g0(x)=∏_{x∈X0}(x-x_i)，则 f 在 X0 上的取值 f mod g0 计算，即 f(x)≡f mod g0 (mod 对 X0 内点成立)，递归到规模一半。T(n)=2T(n/2)+O(n log n)=O(n log^2 n)。插值是其逆问题：给 n+1 个点求 n 次多项式，同样分治：f=f0·M1+f1·M0，M0=∏_{左半}(x-x_i)，M1=∏_{右半}(x-x_i)，递归+NTT 乘法，O(n log^2 n)。两者都依赖分段积多项式(segment tree product tree)与 NTT。

## Why · 为什么

### 直觉 · Intuition

若 f 的某些取值只与'余数'有关：f(x) ≡ f(x) mod g(x) 当 g(x)=0。构造 g 为一半点的 (x-x_i) 乘积，那么在那些点上 f 的值就等于 f mod g 的值，而 f mod g 的次数减半。分治下去每层规模减半。

### 原理 · Principle

分治求值: 建立线段树, 每个节点存该区间点的 M(x)=∏(x-x_i)(用 NTT 自底向上乘出)。递归: f 对左子区间用 f mod M_left, 右子区间用 f mod M_right; 叶子返回 f(x_i)。分治插值: 先求 M(x)=∏(x-x_i), 用多点求值求 M'(x_i); 递归求左右插值多项式 f0,f1, 再组合 f=f0·M1+f1·M0。复杂度均为 O(n log^2 n)。

### 历史 · History

多点求值与快速插值是多项式算法'快包'的标准成员, 1970s 由多项式的 gcd/乘积树技巧演进, 现代统一框架见于 Modern Computer Algebra(von zur Gathen & Gerhard)。OI Wiki 的 poly/multipoint-eval-interpolation 页面收录 O(n log^2 n) 做法。属于前沿/高级内容, 常作为多项式全家桶压轴。

## How · 实现

### 伪代码

```python
# 多点求值
build product tree: 节点 M(l,r)=∏_{i in [l,r)} (x-x_i)   # 自底向上 NTT
solve(f, node):
    f = f mod M[node]
    if leaf: return f(x_l)
    return solve(f, left) + solve(f, right)

# 插值
M = product tree root;  g_i = M'(x_i) via multipoint eval
solve2(ys, node):
    if leaf: return y_i / g_i  (常数)
    f0 = solve2(ys_left, left); f1 = solve2(ys_right, right)
    return f0*M_right + f1*M_left
```

### Python 实现

```python
import sys
sys.setrecursionlimit(100000)
MOD = 998244353
ROOT = 3


def mod_pow(a, b, mod=MOD):
    r = 1
    while b:
        if b & 1:
            r = r * a % mod
        a = a * a % mod
        b >>= 1
    return r


def ntt(a, invert=False):
    n = len(a)
    a = a[:]
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    h = 2
    while h <= n:
        w_h = mod_pow(ROOT, (MOD - 1) // h)
        if invert:
            w_h = mod_pow(w_h, MOD - 2)
        for i in range(0, n, h):
            w = 1
            for j in range(i, i + h // 2):
                u = a[j]
                v = a[j + h // 2] * w % MOD
                a[j] = (u + v) % MOD
                a[j + h // 2] = (u - v) % MOD
                w = w * w_h % MOD
        h <<= 1
    if invert:
        inv_n = mod_pow(n, MOD - 2)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD
    return a


def poly_mul(a, b):
    if not a or not b:
        return []
    need = len(a) + len(b) - 1
    n = 1
    while n < need:
        n <<= 1
    fa = a[:] + [0] * (n - len(a))
    fb = b[:] + [0] * (n - len(b))
    fa = ntt(fa)
    fb = ntt(fb)
    for i in range(n):
        fa[i] = fa[i] * fb[i] % MOD
    fa = ntt(fa, True)
    return fa[:need]


def poly_inv(a, n):
    res = [pow(a[0], MOD - 2, MOD)]
    m = 1
    while m < n:
        m2 = min(m * 2, n)
        t = poly_mul(a[:m2], res)
        t = t[:m2]
        t[0] = (2 - t[0]) % MOD
        for i in range(1, len(t)):
            t[i] = (-t[i]) % MOD
        res = poly_mul(res, t)[:m2]
        m = m2
    return res


def poly_divmod(f, g):
    n, m = len(f), len(g)
    if n < m:
        return [], f[:]
    fr = f[::-1][:n - m + 1]
    gr = g[::-1]
    igr = poly_inv(gr, n - m + 1)
    qrev = poly_mul(fr, igr)[:n - m + 1]
    q = qrev[::-1]
    qg = poly_mul(q, g)
    r = [(f[i] - qg[i]) % MOD for i in range(m - 1)]
    return q, r


def poly_mod(f, g):
    _, r = poly_divmod(f, g)
    return r


class SegTreePoly:
    """分治树: 每个节点存 prod (x - x_i)."""

    def __init__(self, xs):
        self.xs = xs
        self.n = len(xs)
        self.tree = [None] * (4 * self.n)

    def build(self, node, l, r):
        if r - l == 1:
            self.tree[node] = [(-self.xs[l]) % MOD, 1]
            return
        mid = (l + r) // 2
        self.build(node * 2, l, mid)
        self.build(node * 2 + 1, mid, r)
        self.tree[node] = poly_mul(self.tree[node * 2], self.tree[node * 2 + 1])[:r - l + 1]


def multipoint_eval_recursive(f, tree, node, l, r):
    """分治多点求值: 返回 f(x_l)..f(x_{r-1})"""
    if r - l == 1:
        return [poly_eval_naive(f, tree.xs[l]) % MOD]
    mid = (l + r) // 2
    fl = poly_mod(f, tree.tree[node * 2])
    fr = poly_mod(f, tree.tree[node * 2 + 1])
    return multipoint_eval_recursive(fl, tree, node * 2, l, mid) + \
        multipoint_eval_recursive(fr, tree, node * 2 + 1, mid, r)


def poly_eval_naive(f, x):
    r = 0
    for c in reversed(f):
        r = (r * x + c) % MOD
    return r


def multipoint_eval(f, xs):
    """O(n log^2 n) 多点求值(教学用分治+NTT, 小规模)。"""
    if not xs:
        return []
    tree = SegTreePoly(xs)
    tree.build(1, 0, tree.n)
    return multipoint_eval_recursive(f[:], tree, 1, 0, tree.n)


def multipoint_eval_naive(f, xs):
    return [poly_eval_naive(f, x) for x in xs]


if __name__ == "__main__":
    import random
    for _ in range(20):
        deg = random.randint(1, 6)
        f = [random.randint(0, MOD - 1) for _ in range(deg + 1)]
        xs = [random.randint(0, 10) for _ in range(random.randint(1, 6))]
        a = multipoint_eval(f, xs)
        b = multipoint_eval_naive(f, xs)
        assert a == b, (f, xs, a, b)
    # 手工: f(x)=x^2+1 在 0,1,2
    f = [1, 0, 1]
    assert multipoint_eval(f, [0, 1, 2]) == [1, 2, 5]
    print("multipoint-eval tests passed")

```

**PyPy 提示**: Python 实现 O(n log^2 n) 需高效 NTT + 大量多项式取模, 常数极大, 1e5 级基本不可行(教学版仅供小规模验证)。实际竞赛中 Python 慎用, 通常转 C++。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n log^2 n) |
| 空间 | O(n log n)(分治栈/乘积树) |

### 局限

需要可靠 NTT + 多项式取模(带余除法用逆元)作为子程序, 实现复杂; Python 常数过大, 实际用途受限; 插值还要求所有 x_i 两两不同(否则 M' 有零点, 无逆)。纯 Python 仅供小规模学习验证。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Library Checker | multipoint_evaluation | 5 | 多点求值模板题, 权威验证平台 | [https://judge.yosupo.jp/problem/multipoint_evaluation](https://judge.yosupo.jp/problem/multipoint_evaluation) |
| Library Checker | polynomial_interpolation | 5 | 多项式插值模板题 | [https://judge.yosupo.jp/problem/polynomial_interpolation](https://judge.yosupo.jp/problem/polynomial_interpolation) |
| Luogu | P5050 | 5 | 多项式多点求值(国内模板题) | [https://www.luogu.com.cn/problem/P5050](https://www.luogu.com.cn/problem/P5050) |

## Pitfalls · 易错点

- 乘积树每节点 M 次数要对应区间长度+1, 截断错误
- 递归取模后忘记保留叶子处 f 的次数边界
- 插值要求 x_i 互异, 否则 M' 不可逆
- 取模多项式时先确保 deg f >= deg g, 处理商为零的情形
- NTT 长度补零错误导致乘积树数值错位

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/poly/multipoint-eval-interpolation/](https://oi-wiki.org/math/poly/multipoint-eval-interpolation/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/poly/multipoint-eval-interpolation.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/poly/multipoint-eval-interpolation.md)
