---
id: stars-and-bars
name: 插板法(Stars and Bars)
group: G-C-10
stage: intermediate
priority: P0
depth_tier: deep
---

# 插板法(Stars and Bars)

> 将n个相同物品分给k组的方案数C(n+k-1,k-1)，整数拆分计数

<!-- 元信息: id=stars-and-bars · group=G-C-10 · stage=intermediate · priority=P0 · depth_tier=deep -->

## What · 是什么

插板法（Stars and Bars）是一类把『n 个相同物品分给 k 组』的计数问题转化为组合数的技巧。核心结论：x_1+x_2+...+x_k=n 的正整数解（每组至少 1 个）有 C(n-1,k-1) 组；非负整数解（允许空组）有 C(n+k-1,k-1)=C(n+k-1,n) 组；带下界 x_i≥a_i 时先把 ∑a_i 个物品预先分掉，转化为非负解，答案 C(n-∑a_i+k-1, n-∑a_i)。它是多重集组合数、不定方程计数、货币/称重/投球等『相同物品+有区分盒子』计数问题的通用工具。

## Why · 为什么

### 直觉 · Intuition

把 n 个星（★）排成一列，n-1 个空隙；要分成 k 组就在其中选 k-1 个空隙插入隔板，方案数 C(n-1,k-1)。允许空组时『先借 k 个物品』垫底使每组非空，插完板再还回去——借用后等价于在 n+k 个物品的 n+k-1 个空隙插 k-1 块板，故 C(n+k-1,k-1)。名字 Stars（星=物品）and Bars（杠=隔板）由此而来。

### 原理 · Principle

设第 i 组分得 x_i 个，问题即不定方程 x_1+...+x_k=n 的解数。① 正整数解：C(n-1,k-1)；② 非负整数解：令 y_i=x_i+1≥1，Σy_i=n+k，得 C(n+k-1,k-1)；③ 一般下界：令 x_i'=x_i-a_i≥0，Σx_i'=n-∑a_i，得 C(n-∑a_i+k-1, k-1)。统一视角是『先满足下界再分配剩余』。它等价于多重集 {n_1·a_1,...,n_k·a_k} 中选 r 个元素的方案数（x_i≤n_i 时用容斥剔除上界）。

### 历史 · History

方法本身源于组合数学对『投球问题（balls into boxes）』与『不定方程正整数解』的经典处理，Stars and Bars 这一名称在 W. Feller 的《概率论及其应用》中普及，现代竞赛数学中作为计数基础出现在 CP-Algorithms 与 OI Wiki 组合计数入门。

## How · 实现

### 伪代码

```python
# 直接套组合数
# 非负解 x1+..+xk=n:
ans = C(n+k-1, k-1)
# 正整数解:
ans = C(n-1, k-1)
# 带下界 a_i:
ans = C(n - sum(a) + k - 1, k - 1)

# 组合数建议预计算阶乘+逆元 (模质数) 或逐项乘除 (不取模)
```

### Python 实现

```python
MOD = 10**9 + 7


def comb_precompute(maxn, mod):
    """预计算 0..maxn 阶乘与逆元, 返回 lambda comb(n,k)"""
    fact = [1] * (maxn + 1)
    for i in range(1, maxn + 1):
        fact[i] = fact[i - 1] * i % mod
    invf = [1] * (maxn + 1)
    invf[maxn] = pow(fact[maxn], mod - 2, mod)
    for i in range(maxn, 0, -1):
        invf[i - 1] = invf[i] * i % mod

    def comb(n, k):
        if k < 0 or k > n:
            return 0
        return fact[n] * invf[k] % mod * invf[n - k] % mod

    return comb


def stars_bars(n, k, lower=None, mod=None):
    """x_1+..+x_k = n 的解数.
    lower: 可选下界列表 a_i (长度 k); mod: 取模 (需为质数)"""
    if lower is None:
        lower = [0] * k
    rem = n - sum(lower)
    if rem < 0:
        return 0
    n_ = rem + k - 1
    k_ = k - 1
    if n_ < 0 or k_ < 0:
        return 0
    if mod:
        return comb_precompute(n_, mod)(n_, k_)
    # 不取模: 逐项乘除 (n_ 可能较大, 逐项整数除法保精度)
    k_ = min(k_, n_ - k_)
    r = 1
    for i in range(1, k_ + 1):
        r = r * (n_ - k_ + i) // i
    return r


if __name__ == "__main__":
    # 非负解 x+y+z=5: 枚举验证
    cnt = 0
    for x in range(6):
        for y in range(6 - x):
            z = 5 - x - y
            cnt += 1
    assert cnt == stars_bars(5, 3) == 21
    # 正整数解 x+y+z=5: (1,1,3)(1,2,2)(1,3,1)(2,1,2)(2,2,1)(3,1,1) => 6
    assert stars_bars(5, 3, lower=[1, 1, 1]) == 6 == comb_precompute(10, MOD)(4, 2)
    # 下界 a=[2,1,0], n=7: rem=4, C(4+3-1,2)=C(6,2)=15
    assert stars_bars(7, 3, lower=[2, 1, 0]) == 15
    # 模版与非模版一致
    assert stars_bars(100, 5, mod=MOD) == stars_bars(100, 5) % MOD
    # 边界: 空组全给 k=1
    assert stars_bars(5, 1) == 1
    print("All tests passed.")
```

**PyPy 提示**: 大规模时阶乘+逆元数组 O(maxn) 预处理后每个询问 O(1)，PyPy 下注意 pow(fact, MOD-2, MOD) 一次调用即可；非取模大组合数逐项整除在 n 达 1e6 时可用；若需处理组合数超模数，改用 exLucas。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 单次组合数 O(k) 或 O(min(k,n))；预处理后 O(1) |
| 空间 | O(1) 单次；O(maxn) 预处理 |

### 局限

只适用于『物品不可区分、盒子可区分』。物品可区分时方案数是 k^n（每个物品独立选盒子）而非插板；盒子不可区分是整数拆分（partition）问题，不是插板公式。k 或 n 很大且模数为合数时组合数需 exLucas。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Codeforces | 451E | 5 | Devu and Flowers：上界限制的整数和计数，插板法+容斥（CP-Alg 例题） | [https://codeforces.com/problemset/problem/451/E](https://codeforces.com/problemset/problem/451/E) |
| Codeforces | 553A | 4 | Kyoya and Coloured Balls：组合计数用插板法分段（CP-Alg Practice） | [https://codeforces.com/problemset/problem/553/A](https://codeforces.com/problemset/problem/553/A) |
| Codeforces | 1288C | 4 | Two Arrays：单调序列计数转化为带可重复组合/插板（CP-Alg Practice） | [https://codeforces.com/problemset/problem/1288/C](https://codeforces.com/problemset/problem/1288/C) |

## Pitfalls · 易错点

- 把非负解 C(n+k-1,k-1) 与正整数解 C(n-1,k-1) 搞混——先确认每组是否允许为空
- 下界不为 1 时忘记『先扣掉 ∑a_i』再插板
- n<∑a_i 时答案为 0（下界超额）
- 『盒子不可区分』时不能用插板公式（那是 partition）
- 模数非质时不能直接逆元求组合数
- k=0 或 n=0 的边界：非负解 x_1+..+x_k=0 恰 1 组（全 0）

## Sources · 信源

- CP-Algorithms ✓ [https://cp-algorithms.com/combinatorics/stars_and_bars.html](https://cp-algorithms.com/combinatorics/stars_and_bars.html)
- OI Wiki ✓ [https://oi-wiki.org/math/combinatorics/combination/](https://oi-wiki.org/math/combinatorics/combination/)
- 书籍 ✓ `CPH ch22 Combinatorics (p217-226)`
