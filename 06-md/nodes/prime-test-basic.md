---
id: prime-test-basic
name: 素数判定(试除)
group: G-C-7
stage: basic
priority: P0
depth_tier: deep
---

# 素数判定(试除)

> O(sqrt(n))试除法判定素数，基础方法，大数用Miller-Rabin

<!-- 元信息: id=prime-test-basic · group=G-C-7 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

素数判定（试除法）：若 n<2 则非素数；否则检查 2 到 √n 范围内是否存在 n 的因数，存在则合数，不存在则素数。依据是若 n 有因数 d，则 n/d 也是因数，两者中较小者 ≤√n，故只需试除到 √n。复杂度 O(√n)。进一步可只试除 6k±1 形式的数（跳过 2,3 的倍数）以减少常数。对 n≤10^12 可接受；更大规模用 Miller-Rabin 概率检测。

## Why · 为什么

### 直觉 · Intuition

因数成对出现：若 d 整除 n，则 n/d 也整除 n，二者较小者不超过 √n。所以只要 [2,√n] 内没有因数，n 就是素数。就像检查一个数能否被拼成矩形——只有 1×n 的矩形说明它是素数。

### 原理 · Principle

设 n 的因数分解 n=a·b，则 min(a,b)≤√n。枚举 i 从 2 到 floor(√n)，若 n mod i==0 则 n 合数；遍历完毕无因数则素数。优化：先特判 2，之后只检查奇数，减半工作量；再进一步只检查 6k±1（因除 2,3 外所有素数落在 6 的两侧），工作量再减 1/3。

### 历史 · History

试除法是最古老的素数判定法，可追溯至古希腊埃拉托斯特尼筛法的思想。现代计算机竞赛中作为 n≤10^12 的标准方法，更大规模由 Miller-Rabin（1976/1980）取代。

## How · 实现

### 伪代码

```python
function isPrime(n):
  if n < 2: return false
  if n in {2,3}: return true
  if n mod 2==0 or n mod 3==0: return false
  i = 5
  while i*i <= n:
    if n mod i==0 or n mod (i+2)==0: return false
    i += 6
  return true
```

### Python 实现

```python
# 素数判定：试除法 O(sqrt n)，含 6k±1 优化
import sys

def is_prime(n: int) -> bool:
    """试除法判素数，6k±1 优化"""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

if __name__ == "__main__":
    # 自测
    primes = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47}
    for n in range(50):
        expected = n in primes
        assert is_prime(n) == expected, f"n={n} 期望{expected} 实得{is_prime(n)}"
    # 边界
    assert is_prime(0) is False
    assert is_prime(1) is False
    assert is_prime(2) is True
    assert is_prime(999999937) is True  # 10位素数
    assert is_prime(1000000000) is False
    print("prime-test-basic OK")

```

**PyPy 提示**: PyPy 下 while 循环 + 整数运算可被 JIT 编译为高效机器码，对 n≈10^12 的单次判定约毫秒级。CPython 同算法慢 5-10 倍。但无论如何试除法对 n>10^12 不够快，应转 Miller-Rabin。注意 i*i 可能溢出——Python 无此问题，C++ 需用 long long。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(√n)，6k±1 优化后约 O(√n/3) |
| 空间 | O(1) |

### 局限

1) 仅适用于 n≤10^12 量级，更大需 Miller-Rabin（O(k log n)）；2) 批量判定 1..n 是否素数应改用埃氏筛或线性筛；3) Python 中 i*i<=n 对极大 n 仍可行（int 无限精度），但循环次数过多会超时。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P5736 | 2 | 筛出区间内质数，单点判定用试除法 | [https://www.luogu.com.cn/problem/P5736](https://www.luogu.com.cn/problem/P5736) |
| Luogu | P3912 | 3 | 1..n 素数个数，n 大时应用筛法 | [https://www.luogu.com.cn/problem/P3912](https://www.luogu.com.cn/problem/P3912) |

## Pitfalls · 易错点

- 忘记处理 n<2 的边界（0,1,负数均非素数）
- i*i<=n 中 i 用 int 在 C++ 会溢出，需 long long；Python 无溢出但循环慢
- 把试除法用于 n>10^12 导致 TLE，应换 Miller-Rabin
- 批量判定用试除法而非筛法，复杂度退化为 O(n√n) 而非 O(n log log n)
- 只试除奇数但忘了先特判 2，导致 2 被误判为合数

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/number-theory/prime/](https://oi-wiki.org/math/number-theory/prime/)
- CP-Algorithms ✓ [https://cp-algorithms.com/algebra/primality_tests.html](https://cp-algorithms.com/algebra/primality_tests.html)
- 书籍 ✓ `CPH ch21 Number theory (p207-216)`
