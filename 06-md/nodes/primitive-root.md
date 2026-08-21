---
id: primitive-root
name: 原根
group: G-C-8
stage: advanced
priority: P1
depth_tier: standard
---

# 原根

> 模 p 下阶为 φ(p) 的元素 g，其幂次跑遍全部既约剩余系，是 NTT、离散对数与离散根的基础；最小原根 O(φ^(1/4) log^2) 求解

<!-- 元信息: id=primitive-root · group=G-C-8 · stage=advanced · priority=P1 · depth_tier=standard -->

## What · 是什么

模 m 的既约剩余系关于乘法构成一个有限群（模 m 的单位群）。若元素 g 满足 gcd(g,m)=1，且存在最小正整数 n 使 g^n≡1 (mod m)，则称 n 为 g 模 m 的阶 δ_m(g)。若 δ_m(g)=φ(m)，则称 g 为模 m 的原根（primitive root），此时 g 的幂次 {g^0,g^1,...,g^(φ(m)-1)} 恰好遍历全部与 m 互素的剩余类，即单位群为循环群。竞赛中最重要的情形是模奇素数 p：原根 g 的幂次遍历 1..p-1 全部非零剩余，因此 x≡g^k (k 为离散对数) 把乘法结构化为加法结构。

## Why · 为什么

### 直觉 · Intuition

把模 p 的乘法表想象成一个钟面，阶就是 g 的幂回到 1 所需步数。若这个步数恰好等于非零剩余的总数 p-1，那么 g 每走一步都踩到一个新数，最终走满整个钟面——这样的 g 就是原根。原根相当于给全部非零剩余一个对数坐标，乘法变加法。

### 原理 · Principle

原根判定定理：若已知 φ(m) 的全部素因子 q_1..q_s，则 g 是模 m 原根 ⟺ 对所有 q_i 有 g^(φ(m)/q_i) ≢ 1 (mod m)。必要性：若 g^d≡1 对某个真因子 d 成立则阶小于 φ(m)。充分性：由阶整除 φ(m)，若阶是 φ(m) 的真因子，则 φ(m)/阶 含某素因子 q_i，且 g^(φ(m)/q_i)≡1，矛盾。因此只需对 φ(m) 的素因子做幂次检验（O(φ(m) 的素因子个数·log)）。原根个数为 φ(φ(m))；原根存在当且仅当 m=1,2,4,p^e,2p^e（p 为奇素数）。

### 历史 · History

高斯的《算术研究》(1801) 系统证明原根存在定理与构造理论。最小原根的渐进上界由 Burgess 等研究（素数 p 的最小原根 O(p^(1/4+ε))），是纯数论与算法数论长期关注的问题。现代应用：NTT 常用素数 998244353=119·2^23+1 的原根 3，离散对数 BSGS 也以原根为底。

## How · 实现

### 伪代码

```python
# 分解 phi(m) 的素因子
factors = 分解 phi(m) 的互异素因子集合
# 从小到大枚举 g，用原根判定定理检验
def primitive_root(m):
  if m == 2: return 1
  if m == 4: return 3
  phi = 计算 phi(m)
  factors = 分解 phi 的素因子
  for g in range(2, m):
    if all(pow(g, phi//q, m) != 1 for q in factors):
      return g
  return -1  # 不存在
```

### Python 实现

```python
from math import isqrt, gcd


def factorize_distinct(n):
    """n 的互异素因子（用于判定用）"""
    res = set()
    d = 2
    while d * d <= n:
        if n % d == 0:
            res.add(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        res.add(n)
    return sorted(res)


def phi_single(n):
    res = n
    d = 2
    while d * d <= n:
        if n % d == 0:
            res = res // d * (d - 1)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        res = res // n * (n - 1)
    return res


def primitive_root(m):
    """返回模 m 的最小原根，不存在返回 -1。
    存在条件：m = 1,2,4,p^e,2p^e (p 奇素数)。
    """
    if m == 2:
        return 1
    if m == 4:
        return 3
    phi = phi_single(m)
    factors = factorize_distinct(phi)
    for g in range(2, m):
        if gcd(g, m) != 1:
            continue
        if all(pow(g, phi // q, m) != 1 for q in factors):
            return g
    return -1


if __name__ == "__main__":
    # 暴力验证：g 的幂次是否恰好遍历全部与 m 互素的剩余
    def brute_primitive(m):
        phi = phi_single(m)
        for g in range(1, m):
            if gcd(g, m) != 1:
                continue
            seen = set()
            cur = 1
            for _ in range(phi):
                seen.add(cur)
                cur = cur * g % m
            if len(seen) == phi:
                return g
        return -1

    for m in [2, 3, 4, 5, 7, 11, 13, 17, 29, 73, 997, 1009]:
        assert primitive_root(m) == brute_primitive(m), m

    # 经典 NTT 素数
    assert primitive_root(998244353) == 3   # 119*2^23+1
    assert primitive_root(167772161) == 3   # 5*2^25+1
    assert primitive_root(469762049) == 3   # 7*2^26+1

    # 不存在原根的模数
    assert primitive_root(8) == -1
    assert primitive_root(12) == -1

    print("All tests passed.")
```

**PyPy 提示**: 求最小原根从小到大枚举 g，最坏枚举约 O(p^(1/4+ε)) 次（平均约几次到几十次），每次检验约 log(p) 次快速幂（每次 O(log p)）。总复杂度 O(p^(1/4) log^2 p)，对 p≈1e9 的 NTT 素数毫秒级可出。PyPy 下 pow 内置即为快速幂，无需自写。注意 g 需满足 gcd(g,m)=1（对素数模自动成立，跳过即可）。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 分解 φ(m) 的素因子 O(√φ)；判定每个候选 g 需 O(ω(φ)·log p) 次快速幂；总 O(p^(1/4+ε) log^2 p) 期望 |
| 空间 | O(1) |

### 局限

只对存在原根的模数 m=1,2,4,p^e,2p^e 有定义。对素数幂 p^e (e≥2) 判定条件与素模相同（仍以 φ(p^e) 的素因子检验），但最小原根可能不是素模下的最小原根。枚举 g 从 2 开始会跳过 g=1（恒非原根，正确）。合数 m 时需显式检查 gcd(g,m)=1。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P6091 | 6 | 【模板】原根：求模 n 的全部原根，先判存在性（2,4,p^e,2p^e）再求最小原根后用性质枚举全部 | [https://www.luogu.com.cn/problem/P6091](https://www.luogu.com.cn/problem/P6091) |
| AtCoder | AGC 034 F? 相关模板 / NTT 前置 | 6 | NTT 卷积模板：998244353 的原根 3 用于 3^(n-1) 型 Wn，验证原根在卷积加速中的直接用途 | [https://atcoder.jp/contests/practice2/tasks/practice2_convolution](https://atcoder.jp/contests/practice2/tasks/practice2_convolution) |
| LibreOJ | LOJ 130 | 6 | 树链剖分/NTT 类综合题：以原根为基础的多项式变换，体现原根作为 NTT 基座 | [https://loj.ac/p/130](https://loj.ac/p/130) |

## Pitfalls · 易错点

- 判定定理对 φ(m) 的每个素因子 q 检查 g^(φ/q)≢1，而非检查 g^q≢1
- 枚举 g 时忽略 gcd(g,m)≠1 的候选（对合数 m 必须检查）
- 忘记原根存在性前提（m 必须是 2,4,p^e,2p^e），直接对 m=8 枚举会死循环或误判
- pow(g, phi//q, m) 用 m 做模数而非 phi，若用 phi 当模数结果是错的
- phi_single 分解时若中途 n 被除尽，最后 n>1 分支处理大素因子（else 漏了会少一个因子）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/number-theory/primitive-root/](https://oi-wiki.org/math/number-theory/primitive-root/)
- CP-Algorithms ✓ [https://cp-algorithms.com/algebra/primitive-root.html](https://cp-algorithms.com/algebra/primitive-root.html)
- 书籍 ✓ `CPH ch21 数论 (原根/离散对数前置，p.215)`
