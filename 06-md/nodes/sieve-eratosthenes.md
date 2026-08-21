---
id: sieve-eratosthenes
name: 埃氏筛
group: G-C-7
stage: basic
priority: P0
depth_tier: deep
---

# 埃氏筛

> O(n log log n)筛素数，标记合数，基础素数筛法

<!-- 元信息: id=sieve-eratosthenes · group=G-C-7 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

埃拉托斯特尼筛法（Sieve of Eratosthenes）是最基础的素数筛法：从小到大遍历每个数，若是质数则把它的所有倍数标记为合数。算法结束后未被标记的数就是素数。时间复杂度 O(n log log n)。优化技巧包括只筛到 sqrt(n)、只处理奇数、位压缩存储、分段筛，以及用 bitset/vector<bool> 加速到实际快于线性筛。

## Why · 为什么

### 直觉 · Intuition

核心观察：质数的倍数一定是合数。所以遇到一个质数 p，就把 2p,3p,4p... 全部划掉；最终没被划掉的数没有任何小于自身的质因子，只能是质数。从 p² 开始划是因为小于 p² 的 p 的倍数早已被更小的质数划掉。

### 原理 · Principle

初始化 is_prime[2..n]=true。对 i 从 2 到 sqrt(n)：若 is_prime[i]，从 i² 开始以步长 i 将所有倍数标记为 false。剩下的 true 即为素数。复杂度推导：划掉操作总数为 sum_{p≤n} n/p = n·sum 1/p = O(n log log n)（Mertens 第二定理）。只筛到 sqrt(n) 不影响渐近复杂度但大幅减少常数。

### 历史 · History

筛法得名于古希腊数学家埃拉托斯特尼（Eratosthenes，公元前 3 世纪），他在测量地球周长之余发明了该系统筛素数的方法。近现代计算机诞生后，筛法成为计算素数表和数论算法的基础组件。OI Wiki 与 CP-Algorithms 均以埃氏筛作为数论筛法的开篇。

## How · 实现

### 伪代码

```python
is_prime[2..n] = true; is_prime[0]=is_prime[1]=false
for i = 2..floor(sqrt(n)):
  if is_prime[i]:
    for j = i*i, j <= n, j += i:
      is_prime[j] = false
primes = [i for i in 2..n if is_prime[i]]
```

### Python 实现

```python
from math import isqrt


def eratosthenes(n):
    """埃氏筛：返回 2..n 的所有素数（含 n）"""
    if n < 2:
        return []
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, isqrt(n) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(2, n + 1) if is_prime[i]]


def count_primes(n):
    """统计 1..n 中素数个数"""
    return len(eratosthenes(n))


def smallest_prime_factor(n):
    """埃氏筛变体：记录每个数的最小质因子（spf）"""
    if n < 2:
        return {}
    spf = list(range(n + 1))
    spf[0] = spf[1] = 0
    for i in range(2, isqrt(n) + 1):
        if spf[i] == i:  # i 是质数
            for j in range(i * i, n + 1, i):
                if spf[j] == j:
                    spf[j] = i
    return spf


if __name__ == "__main__":
    assert eratosthenes(1) == []
    assert eratosthenes(10) == [2, 3, 5, 7]
    assert eratosthenes(20) == [2, 3, 5, 7, 11, 13, 17, 19]
    assert count_primes(100) == 25
    assert count_primes(30) == 10

    # 与暴力素性检验交叉验证
    import math

    def is_prime_brute(x):
        if x < 2:
            return False
        for d in range(2, isqrt(x) + 1):
            if x % d == 0:
                return False
        return True

    for n in [2, 50, 100, 300]:
        sieved = set(eratosthenes(n))
        brute = {x for x in range(2, n + 1) if is_prime_brute(x)}
        assert sieved == brute

    spf = smallest_prime_factor(100)
    assert spf[15] == 3
    assert spf[49] == 7
    assert spf[97] == 97

    print("All tests passed.")
```

**PyPy 提示**: PyPy 下埃氏筛用 list[bool]（即 Python 小整数）约每秒 1e8 次标记，n=1e7 约 0.5-1s；CPython 约慢 3-5 倍。可用 bytearray 代替 list[bool] 显著提速并省内存。筛 1e8 内存占 100MB（bytearray），分段筛可进一步压缩。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n log log n) — 划掉所有质数倍数；只筛到 sqrt(n) 不影响渐近但减常数 |
| 空间 | O(n) — 布尔标记数组；位压缩可到 O(n/8) |

### 局限

每个合数会被多个质因子重复标记（12 被 2、3 各划一次），这是与线性筛的差距；n 超过 1e8 时内存和时间吃紧，需分段筛或位压缩。埃氏筛无法直接维护积性函数（需在线性筛框架内做）。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3383 | 3 | 【模板】线性筛素数：埃氏筛与线性筛均可 AC 的模板题 | [https://www.luogu.com.cn/problem/P3383](https://www.luogu.com.cn/problem/P3383) |
| Luogu | P1865 | 4 | A % B Problem：埃氏筛+前缀和统计区间素数个数 | [https://www.luogu.com.cn/problem/P1865](https://www.luogu.com.cn/problem/P1865) |
| SPOJ | PRIME1 | 3 | Prime Generator：区间筛（分段埃氏筛）输出 [m,n] 内素数 | [https://www.spoj.com/problems/PRIME1/](https://www.spoj.com/problems/PRIME1/) |

## Pitfalls · 易错点

- 标记起点从 i*2 而非 i*i 开始，浪费大量操作（正确做法从 i*i 开始）
- 忘记处理 n<2 的边界导致数组越界
- Python 用 list[int] 存布尔标记导致内存爆炸，应使用 list[bool] 或 bytearray
- 把 isqrt(n) 写成 sqrt 后用浮点比较产生精度误差
- 只标记到 n 而非 sqrt(n) 时忘记最后还要再遍历收集素数

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/number-theory/sieve/](https://oi-wiki.org/math/number-theory/sieve/)
- CP-Algorithms ✓ [https://cp-algorithms.com/algebra/sieve-of-eratosthenes.html](https://cp-algorithms.com/algebra/sieve-of-eratosthenes.html)
- 书籍 ✓ `CPH ch21 Number theory (p207-216)`
