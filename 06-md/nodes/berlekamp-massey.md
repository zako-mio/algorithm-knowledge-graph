---
id: berlekamp-massey
name: Berlekamp-Massey
group: G-C-12
stage: advanced
priority: P2
depth_tier: standard
---

# Berlekamp-Massey

> O(n^2)求序列最短线性递推式，配合NTT加速求第n项

<!-- 元信息: id=berlekamp-massey · group=G-C-12 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

Berlekamp-Massey（BM）算法输入长为 n 的序列 a_0..a_{n-1}，输出最短线性递推式（阶数 m），满足 Σ_{j=0}^m r_j a_{i-j}=0（r_0=1）对所有 i>=m 成立。算法增量式：从左到右扫描，当前递推对 a_i 预测失败时，用'上次失败点'构造修正项调整系数。复杂度 O(n·m)，最坏 O(n²)。BM 是'黑盒线性递推'的前半：任给一个可由低阶递推生成的序列（如矩阵快速幂某分量的前 2d 项），BM 求出递推式后，配合 Fiduccia/Bostan-Mori 在 O(m log m log k) 内求出任意第 k 项，从而绕过矩阵幂。也用于矩阵最小多项式、稀疏矩阵秩/行列式/解方程组（配合随机投影+Schwartz-Zippel）。

## Why · 为什么

### 直觉 · Intuition

维护一个'当前最短递推'。每看到新项，若预测准就继续；预测错了，就记下这次误差，用历史上某次失败的信息拼出一个修正递推，加进去。和'在线纠错'一样。

### 原理 · Principle

设当前递推 F 对前 i-1 项成立，预测 a_i 得 tmp，误差 Δ=a_i-tmp。若 Δ≠0：找到上次失败位置 k 及其误差 Δ_k（当时用了递推 G 的记录 last），构造 G'=(0..0, Δ/Δ_k, -(Δ/Δ_k)·last)（前面 i-k-1 个 0），则 F+G' 对新点误差为零且阶数合适。若 F 阶数可以更小则保留更新 last=k。数学上保证最终得到最短递推。

### 历史 · History

Berlekamp(1968) 为 BCH 码译码提出，Massey(1969) 联系到 LFSR 并命名，故称 Berlekamp-Massey。后进入 OI/ACM 作为线性递推黑盒的核心。OI Wiki 的 math/berlekamp-massey 页面给出参考实现与矩阵应用。

## How · 实现

### 伪代码

```python
v=[]; last=[]; k=-1; delta=0
for i in range(n):
    tmp = sum(v[j]*a[i-j-1])
    if a[i]==tmp: continue
    if k<0: k=i; delta=a[i]-tmp; v=[0]*(i+1); continue
    u=v[:]; val=(a[i]-tmp)/delta
    if len(v)<len(last)+i-k: v.extend(zeros)
    v[i-k-1]+=val
    for j: v[i-k+j]-=val*last[j]
    if len(u)-i<len(last)-k: last=u; k=i; delta=a[i]-tmp
r = [1] + [-v[j]]
return r   # sum r_j a_{i-j}=0
```

### Python 实现

```python
MOD = 998244353


def berlekamp_massey(a, mod=MOD):
    """求序列 a 的最短线性递推式.
    返回 r[0..m], 满足 sum_{j=0}^m r_j a_{i-j} = 0 (r_0=1), 即 a_i = -sum_{j=1}^m r_j a_{i-j}."""
    v = []  # 当前递推系数(长度 m)
    last = []  # 上次调整时的系数
    k = -1
    delta = 0
    for i in range(len(a)):
        tmp = 0
        for j in range(len(v)):
            tmp = (tmp + a[i - j - 1] * v[j]) % mod
        if a[i] == tmp:
            continue
        if k < 0:
            k = i
            delta = (a[i] - tmp) % mod
            v = [0] * (i + 1)
            continue
        u = v[:]
        val = (a[i] - tmp) * pow(delta, mod - 2, mod) % mod
        if len(v) < len(last) + i - k:
            v += [0] * (len(last) + i - k - len(v))
        v[i - k - 1] = (v[i - k - 1] + val) % mod
        for j in range(len(last)):
            v[i - k + j] = (v[i - k + j] - val * last[j]) % mod
            if v[i - k + j] < 0:
                v[i - k + j] += mod
        if len(u) - i < len(last) - k:
            last = u
            k = i
            delta = (a[i] - tmp) % mod
    # 转成 r_0=1 的形式
    v = [(mod - x) % mod for x in v]
    r = [1] + v
    return r


def verify_recurrence(a, r, mod=MOD):
    """验证递推 r 对序列 a 成立: sum r_j a_{i-j} = 0 对 i>=len(r)-1."""
    m = len(r) - 1
    for i in range(m, len(a)):
        s = 0
        for j in range(len(r)):
            s = (s + r[j] * a[i - j]) % mod
        if s != 0:
            return False
    return True


def gen_fib(n):
    a = [0, 1]
    for i in range(2, n):
        a.append((a[i - 1] + a[i - 2]) % MOD)
    return a


if __name__ == "__main__":
    import random
    # Fibonacci
    fib = gen_fib(30)
    r = berlekamp_massey(fib)
    assert r == [1, MOD - 1, MOD - 1], r  # F_n = F_{n-1} + F_{n-2}
    assert verify_recurrence(fib, r)
    # 常数序列
    const = [7] * 10
    r2 = berlekamp_massey(const)
    assert verify_recurrence(const, r2)
    # 随机序列: 递推阶数 m 不会超过 len(a)
    for _ in range(30):
        n = random.randint(4, 25)
        a = [random.randint(0, MOD - 1) for _ in range(n)]
        r = berlekamp_massey(a)
        assert verify_recurrence(a, r), (a, r)
    # 手工: a_n = 2*a_{n-1} + 3*a_{n-2}, a0=1,a1=2
    a = [1, 2]
    for i in range(2, 20):
        a.append((2 * a[i - 1] + 3 * a[i - 2]) % MOD)
    r3 = berlekamp_massey(a)
    assert verify_recurrence(a, r3)
    assert r3[1] == MOD - 2 and r3[2] == MOD - 3, r3
    print("Berlekamp-Massey tests passed")

```

**PyPy 提示**: 朴素 O(n²) 内层是 Python 列表循环, n=1e5 且阶数大时慢; 若序列确实有低阶递推, BM 会在得到足够项后稳定, 可用截断(只处理前 2m 项)。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n·m), 最坏 O(n²) |
| 空间 | O(n) |

### 局限

数值不稳定(实数下误差放大), 通常只在模素数下使用; 需要足够多项(至少 2m, 一般给 2d 项)才能恢复递推; 若序列无低阶递推, BM 会输出阶数接近 n 的'假递推'(能 fit 但不真)。配合黑盒求第 k 项需再连 Fiduccia/Bostan-Mori。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Library Checker | find_linear_recurrence | 4 | BM 模板题, 权威验证 | [https://judge.yosupo.jp/problem/find_linear_recurrence](https://judge.yosupo.jp/problem/find_linear_recurrence) |
| Luogu | P5487 | 5 | BM 求递推+线性递推求第 k 项完整链路 | [https://www.luogu.com.cn/problem/P5487](https://www.luogu.com.cn/problem/P5487) |
| Codeforces | 1102E | 3 | 较简单的递推/序列类: 配合 BM 思想入门 | [https://codeforces.com/problemset/problem/1102E](https://codeforces.com/problemset/problem/1102E) |

## Pitfalls · 易错点

- 随机序列也输出递推式(可能阶数=n, 需意识到不是真递推)
- 模数下除法要用逆元(费马小定理)
- 更新 last 的条件比较搞反(何时替换旧失败点)
- 输出 r 前忘记把 v 取反/补 r0=1
- 项数不足 2m 时恢复的递推不可靠

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/berlekamp-massey/](https://oi-wiki.org/math/berlekamp-massey/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/berlekamp-massey.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/berlekamp-massey.md)
