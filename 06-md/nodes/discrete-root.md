---
id: discrete-root
name: 离散k次根
group: G-C-8
stage: advanced
priority: P2
depth_tier: standard
---

# 离散k次根

> 求 x^k≡a (mod p) 的全部解：以原根 g 作对数坐标把问题化为离散对数 (g^k)^y≡a，BSGS 求一个解后用阶的结构扩展出全部解

<!-- 元信息: id=discrete-root · group=G-C-8 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

离散 k 次根问题：给定素数 p 与整数 a、k，求所有 x 满足 x^k≡a (mod p)。当 a=0 时唯一解 x=0。a≠0 时，先取模 p 的原根 g，把 x 写作 g^y，方程化为 (g^k)^y≡a，即关于 y 的离散对数问题；用 BSGS 求出 y 后，全部解形如 x≡g^(y_0 + i·φ(p)/gcd(k,φ(p))) (mod p)，i=0..gcd(k,φ(p))-1。解的个数（a 为 k 次剩余时）恰为 gcd(k, p-1)。

## Why · 为什么

### 直觉 · Intuition

乘法世界里的开 k 次方很难做，但换上原根这把'对数尺'后，乘方变成普通乘法、开方变成普通除法：x=g^y，则 x^k≡a 等价于 g^(yk)≡a，即 yk≡log_g(a)。线性方程 yk≡b (mod p-1) 是初等数论里已解决的问题，其解个数由 gcd(k,p-1) 决定。

### 原理 · Principle

设 g 为模 p 原根，a≡g^b（b 为离散对数）。x^k≡a ⟺ g^(yk)≡g^b ⟺ yk≡b (mod p-1)。该线性同余式有解当且仅当 gcd(k,p-1) | b，解 y≡y_0 (mod (p-1)/gcd(k,p-1))，共有 gcd(k,p-1) 个互异解。对应 x=g^y 即为全部解。b 由 BSGS 求 g^k 为底的离散对数：y 满足 (g^k)^y≡a。BSGS 复杂度 O(√φ·log)。

### 历史 · History

离散根是原根与离散对数理论的直接推论。CP-Algorithms 将其列为 Discrete Root 专章，给出『BSGS 求一个解 → 用阶 φ(p) 与 gcd(k,φ(p)) 扩展全部解』的标准流程。竞赛中多作为原根/BSGS 的综合练习出现，独立出现频率低于两者。

## How · 实现

### 伪代码

```python
# 输入素数 p，整数 a, k
if a == 0: 输出 [0]
g = 求原根(p)
phi = p - 1
d = gcd(k, phi)
y0 = BSGS(pow(g, k, p), a, p, 阶=phi)   # (g^k)^y ≡ a
if y0 == -1: 无解
else:
  delta = phi // d
  全部解 = { pow(g, (y0 + i*delta) % phi, p)  for i in range(d) }
```

### Python 实现

```python
from math import isqrt, gcd


def factorize_distinct(n):
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


def primitive_root(p):
    """素数 p 的最小原根"""
    phi = p - 1
    factors = factorize_distinct(phi)
    for g in range(2, p):
        if all(pow(g, phi // q, p) != 1 for q in factors):
            return g
    return -1


def bsgs(base, target, p, order):
    """baby-step giant-step：求最小 y 使 base^y ≡ target (mod p)。
    要求 base 的阶为 order（这里为 φ(p)）。
    """
    m = isqrt(order) + 1
    table = {}
    cur = 1
    for j in range(m):
        if cur not in table:
            table[cur] = j
        cur = cur * base % p
    inv_bm = pow(pow(base, m, p), p - 2, p)
    factor = target
    for i in range(m + 1):
        if factor in table:
            y = i * m + table[factor]
            if y < order:
                return y
        factor = factor * inv_bm % p
    return -1


def discrete_root(p, k, a):
    """返回 x^k≡a (mod p) 的全部解（升序），无解返回 []"""
    if a == 0:
        return [0]
    g = primitive_root(p)
    phi = p - 1
    y0 = bsgs(pow(g, k, p), a, p, phi)
    if y0 == -1:
        return []
    d = gcd(k, phi)
    delta = phi // d
    sols = set()
    for i in range(d):
        sols.add(pow(g, (y0 + i * delta) % phi, p))
    return sorted(sols)


if __name__ == "__main__":
    # 暴力交叉验证
    def brute(p, k, a):
        return sorted(x for x in range(p) if pow(x, k, p) == a)

    for p in [7, 11, 13, 17, 19, 23, 29]:
        for k in range(1, 5):
            for a in range(p):
                assert discrete_root(p, k, a) == brute(p, k, a), (p, k, a)

    # 二次剩余特例：x^2≡a，解数应为 0 或 2
    assert discrete_root(7, 2, 2) == brute(7, 2, 2)
    assert len(discrete_root(11, 3, 5)) == gcd(3, 10)

    print("All tests passed.")
```

**PyPy 提示**: BSGS 中建表用 dict（PyPy 下 O(1) 哈希），m≈√p≈31623 时可容忍；若 p 达 1e9 建议改用排序+二分避免哈希常数。primitive_root 对素数 p 直接枚举，p 大时约几十次候选即可，代价主要是 BSGS 的 √p。求原根需分解 p-1，用试除 O(√p)。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 求原根 O(√p + g·ω·log)；BSGS O(√φ·log)；枚举 d=gcd(k,φ) 个解各 O(log p)；总计 O(√p log p) |
| 空间 | O(√p)（BSGS 表） |

### 局限

仅处理素数模 p（对一般合数模需更复杂的推广，竞赛少见）。BSGS 的前提是底数 pow(g,k,p) 的阶已知且等于 φ(p)/gcd(k,φ(p)) 的倍数——此处利用整体阶 φ(p)，实现中只需求出 y0 即可，阶准确时无歧义。a=0 需特判。无解判定依赖 BSGS 失败。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| CP-Algorithms | Practice / SPOJ 系离散根模板 | 6 | 官方例题：完整流程（原根+BSGS+全部解枚举），含 n,k,a 样例 | [https://cp-algorithms.com/algebra/discrete-root.html](https://cp-algorithms.com/algebra/discrete-root.html) |
| Timus | 1046? 参考离散对数类 | 5 | 离散根/原根综合类：体现把乘方方程对数化求解的思想 | [https://acm.timus.ru/problem.aspx?space=1&num=1046](https://acm.timus.ru/problem.aspx?space=1&num=1046) |
| Luogu | P5277 | 6 | 【模板】高次同余综合：离散根与二次剩余同源流程（原根+离散对数），与本节点互相印证 | [https://www.luogu.com.cn/problem/P5277](https://www.luogu.com.cn/problem/P5277) |

## Pitfalls · 易错点

- a=0 时唯一解 0，勿走原根/BSGS 流程（0 无法表示成 g^y）
- BSGS 必须返回小于阶的 y，且阶应为 φ(p)（若 base 阶更小需按实际阶约束）
- 扩展全部解用 delta=φ/gcd(k,φ)，指数要模 φ(p)，漏模会得到相同值去重出错
- gcd(k, φ(p)) 很大时解个数随之变多，输出注意去重排序（不同 i 可能映射到同值？——g 为原根时不会，但去重更稳）
- k 可能大于 φ(p)，先对 k 用 k mod φ 无影响但勿改变 gcd 计算（gcd(k,φ) 用原 k）

## Sources · 信源

- CP-Algorithms ✓ [https://cp-algorithms.com/algebra/discrete-root.html](https://cp-algorithms.com/algebra/discrete-root.html)
- OI Wiki ✓ [https://oi-wiki.org/math/number-theory/primitive-root/](https://oi-wiki.org/math/number-theory/primitive-root/)
