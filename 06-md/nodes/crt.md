---
id: crt
name: 中国剩余定理(CRT)
group: G-C-8
stage: intermediate
priority: P0
depth_tier: deep
---

# 中国剩余定理(CRT)

> 求解同余方程组，将模互素的大模数分解为小模数合并，exCRT处理不互素

<!-- 元信息: id=crt · group=G-C-8 · stage=intermediate · priority=P0 · depth_tier=deep -->

## What · 是什么

中国剩余定理（CRT）求解一元线性同余方程组 x ≡ a_i (mod n_i)（i=1..k，模数两两互素），并保证在模 N=∏n_i 下有唯一解。解法：令 N_i=N/n_i，求 N_i 在模 n_i 下的逆元 inv_i，则 x ≡ Σ a_i·N_i·inv_i (mod N)。应用极广：大数取模分解（把模合数拆成互素因子再合并）、exLucas、组合数取模、『物不知数』类问题、公钥密码。模数不互素时用扩展 CRT（exCRT）：两两用扩展欧几里得合并方程。

## Why · 为什么

### 直觉 · Intuition

『物不知数』：三三数之剩二、五五数之剩三、七七数之剩二，问物几何？思想是构造一个『只对第 i 个模数贡献、对其他模数贡献 0』的基函数：N_i=N/n_i 整除除 n_i 外所有模数，故 N_i≡0 (mod n_j)(j≠i)；乘以逆元后 a_i·N_i·inv_i ≡ a_i (mod n_i) 且 ≡0 (mod n_j)。把 k 个这样的项相加即得解。这就是『分解成单方程的解再线性组合』。

### 原理 · Principle

① 两两互素保证 N_i 在模 n_i 下有逆元（gcd(N_i,n_i)=1）；② 解 x_0=Σ a_i·N_i·inv_i (mod N)；③ 唯一性：若 x,y 都是解则 x-y≡0 (mod n_i) 全成立，由互素得 x≡y (mod N)；④ exCRT（不互素）：合并两个方程 x≡a₁(n₁), x≡a₂(n₂) → 存在 p,q 使 a₁+p·n₁ = a₂+q·n₂，即 n₁·p - n₂·q = a₂-a₁，用扩展欧几里得求 p 得特解 x'，新方程 x≡x' (mod lcm(n₁,n₂))；反复合并 k-1 次；⑤ Garner 算法是数值稳定的变体（不要求质数，只要求两两互素），适合 k 较大的 CRT 合并。

### 历史 · History

问题最早见《孙子算经》（约公元 3-5 世纪）『物不知数』，宋朝秦九韶 1247 年《数书九章》『大衍求一术』给出完整系统解法，比欧洲（Gauss 1801《算术研究》）早约 500 年，故称中国剩余定理。明朝程大位《算法统宗》的口诀『三人同行七十稀…』即具体实例。现代被用于 RSA 加速、数论变换等。

## How · 实现

### 伪代码

```python
# CRT (模数两两互素)
def crt(a, n):        # a: 余数列表, n: 模数列表
  N = prod(n)
  x = 0
  for i in range(k):
    Ni = N // n[i]
    inv = mod_inverse(Ni, n[i])
    x += a[i] * Ni * inv
  return x % N

# exCRT (任意模数)
# 反复合并 (x mod cur_m) 与 (a_i mod n_i)
def ex_crt(a, n):
  x, m = 0, 1
  for ai, ni in zip(a, n):
    g, p, q = exgcd(m, ni)
    if (ai - x) % g: return None
    m2 = m // g * ni
    x = (x + (ai-x)//g * p % (ni//g) * m) % m2
    m = m2
  return x % m
```

### Python 实现

```python
from math import gcd


def egcd(a, b):
    """扩展欧几里得: 返回 (g, x, y) 使 a*x+b*y=g"""
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1


def mod_inverse(a, m):
    """a 在模 m 下逆元 (gcd(a,m)==1)"""
    g, x, _ = egcd(a, m)
    assert g == 1, "no inverse"
    return x % m


def crt(a, n):
    """CRT: 模数两两互素. 返回 x (0<=x<N) 满足 x≡a_i (mod n_i)."""
    N = 1
    for ni in n:
        N *= ni
    x = 0
    for ai, ni in zip(a, n):
        Ni = N // ni
        inv = mod_inverse(Ni, ni)
        x = (x + ai * Ni * inv) % N
    return x


def ex_crt(a, n):
    """exCRT: 任意模数(不要求互素). 无解返回 None; 否则返回最小非负解."""
    x, m = 0, 1
    for ai, ni in zip(a, n):
        g, p, _ = egcd(m, ni)
        if (ai - x) % g != 0:
            return None
        m2 = m // g * ni
        # (ai - x)/g * p 是 (m/g) 逆元的系数
        t = (ai - x) // g * p % (ni // g)
        x = (x + t * m) % m2
        m = m2
    return x % m


if __name__ == "__main__":
    # 物不知数: x≡2(3), x≡3(5), x≡2(7) => 最小 23
    assert crt([2, 3, 2], [3, 5, 7]) == 23
    # 另例: x≡1(2),2(3),3(5) => 最小解 23
    assert crt([1, 2, 3], [2, 3, 5]) == 23

    # CRT 与暴力枚举交叉验证 (互素模数)
    import random
    random.seed(83)

    def brute(a, n):
        N = 1
        for ni in n:
            N *= ni
        for x in range(N):
            if all(x % ni == ai for ai, ni in zip(a, n)):
                return x
        return None

    for _ in range(300):
        n = []
        while True:
            cand = random.randint(2, 12)
            if all(gcd(cand, x) == 1 for x in n):
                n.append(cand)
                if len(n) == 3:
                    break
        a = [random.randrange(ni) for ni in n]
        assert crt(a, n) == brute(a, n), (a, n)

    # exCRT 与暴力验证 (含不互素)
    for _ in range(400):
        n = [random.randint(2, 12), random.randint(2, 12), random.randint(2, 12)]
        a = [random.randrange(ni) for ni in n]
        sol = ex_crt(a, n)
        if sol is None:
            # 验证确实无解
            assert brute(a, n) is None, (a, n)
        else:
            assert all(sol % ni == ai for ai, ni in zip(a, n)), (a, n, sol)

    # 与 CRT 一致 (互素情形)
    a = [2, 3, 2]; n = [3, 5, 7]
    assert ex_crt(a, n) == crt(a, n) == 23
    # 无解情形: x≡1(2), x≡0(4) -> 无解
    assert ex_crt([1, 0], [2, 4]) is None
    print("All tests passed.")
```

**PyPy 提示**: 大模数乘法用 Python int 无溢出；egcd 递归深度小（O(log m)）。k 很大时迭代乘法 N 可能到 1e18 甚至更大，Python 可处理；C++ 需 __int128。exCRT 合并中 t=(ai-x)//g*p%(ni//g) 是关键防溢出写法，PyPy 下同理。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | CRT: O(k·log max(n_i))（每次求逆）；exCRT: O(k·log max(n_i)) |
| 空间 | O(k) |

### 局限

CRT 要求模数两两互素；不互素必须用 exCRT。a_i 需规范到 0≤a_i<n_i。乘积 N 很大时注意 Python 大整数（或 C++ __int128）。exCRT 两两合并要求每一步 gcd 检查无解。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1495 | 3 | 【模板】中国剩余定理（CRT）/曹冲养猪：CRT 标准模板 | [https://www.luogu.com.cn/problem/P1495](https://www.luogu.com.cn/problem/P1495) |
| Luogu | P4777 | 4 | 【模板】扩展中国剩余定理：exCRT 标准模板（模数不互素） | [https://www.luogu.com.cn/problem/P4777](https://www.luogu.com.cn/problem/P4777) |
| Luogu | P2480 | 6 | SDOI2010 古代猪文：CRT 合并 exLucas 的经典综合题（OI Wiki 例题） | [https://www.luogu.com.cn/problem/P2480](https://www.luogu.com.cn/problem/P2480) |

## Pitfalls · 易错点

- 用 CRT 前忘记检查模数两两互素（不互素用 exCRT）
- 求逆对象搞混：是对 N_i=N/n_i 求模 n_i 逆元，不是对 a_i
- a_i 未规范到 [0,n_i) 导致结果偏移
- exCRT 合并时 (ai-x) 可能为负，Python % 是余数语义需 % m2 归一
- 乘积 N 溢出（C++）或浮点；Python int 无此问题
- 无解判断：两两合并时 gcd 不整除 (a2-a1) 即无解

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/number-theory/crt/](https://oi-wiki.org/math/number-theory/crt/)
- CP-Algorithms ✓ [https://cp-algorithms.com/algebra/chinese-remainder-theorem.html](https://cp-algorithms.com/algebra/chinese-remainder-theorem.html)
- 书籍 ✓ `CPH ch21 Number theory (p207-216)`
