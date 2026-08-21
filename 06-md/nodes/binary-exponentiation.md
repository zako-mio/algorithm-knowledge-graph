---
id: binary-exponentiation
name: 快速幂
group: G-C-7
stage: basic
priority: P0
depth_tier: deep
---

# 快速幂

> O(log n)计算a^n，二进制取幂，模意义下核心工具

<!-- 元信息: id=binary-exponentiation · group=G-C-7 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

快速幂（Binary Exponentiation / Exponentiation by Squaring）利用指数的二进制表示，把 n 次连乘压缩为 O(log n) 次乘法：a^n = a^(2^k1)·a^(2^k2)·...，其中 2^ki 是 n 二进制中为 1 的位。它适用于任何乘法满足结合律的对象（整数、模、矩阵、置换），是模幂、矩阵快速幂、定长路径计数等高级算法的根基。

## Why · 为什么

### 直觉 · Intuition

想算 3^13，暴算要 12 次乘法。但 13 = 1101₂ = 8+4+1，而 3^8、3^4、3^1 可以靠「每次平方」只用 3 次得到（3,9,81,6561），最后 6561×81×3 两次乘法，共 5 次。核心洞察：平方把指数翻倍，翻倍是「成倍成长」。

### 原理 · Principle

迭代版：res 初始为 1（乘法的单位元）；while n>0：若 n 为奇数 res*=a；a*=a（平方）；n//=2。循环体内只做 O(log n) 次乘法。模意义下每步取模即可（取模不干扰乘法）。递归版：a^n = (a^(n//2))² 或再乘 a。矩阵快速幂把整数乘法换成矩阵乘法，可计算斐波那契 F_n、递推式、定长路径数等。

### 历史 · History

「平方取幂」技巧在古代数学中已有雏形（印度公元前 200 年的数学文献记载了计算 2^n 的平方展开法），现代算法分析中它是计算复杂度理论的典型教材案例。OI Wiki 与 CP-Algorithms 均将其列为模算术的首个工具，是 RSA 加密（模幂）的核心运算。

## How · 实现

### 伪代码

```python
# 迭代版（最常用）
def powmod(a, b, m):
  res = 1 % m
  a %= m
  while b > 0:
    if b & 1:
      res = res * a % m
    a = a * a % m
    b >>= 1
  return res

# 矩阵快速幂
mat_pow(M, k): # M 为方阵
  R = 单位矩阵
  while k: R = R*M if k&1; M = M*M; k>>=1
  return R
```

### Python 实现

```python
def mod_pow(a, b, m):
    """快速幂: a^b mod m, O(log b)"""
    res = 1 % m
    a %= m
    while b:
        if b & 1:
            res = res * a % m
        a = a * a % m
        b >>= 1
    return res


def mat_mul(A, B, m):
    """矩阵乘法 (mod m)"""
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        Ai, C_i = A[i], C[i]
        for k in range(n):
            if Ai[k]:
                aik = Ai[k]
                Bk = B[k]
                for j in range(n):
                    C_i[j] = (C_i[j] + aik * Bk[j]) % m
    return C


def mat_pow(M, k, m):
    """矩阵快速幂"""
    n = len(M)
    R = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    while k:
        if k & 1:
            R = mat_mul(R, M, m)
        M = mat_mul(M, M, m)
        k >>= 1
    return R


def fib(n, m):
    """矩阵快速幂求斐波那契第 n 项 (F_0=0,F_1=1)"""
    if n == 0:
        return 0
    M = [[1, 1], [1, 0]]
    P = mat_pow(M, n - 1, m)
    return P[0][0] % m


def fib_iter_verify(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


if __name__ == "__main__":
    M = 10**9 + 7
    # 与内置 pow 交叉验证
    import random
    random.seed(99)
    for _ in range(2000):
        a = random.randint(0, 10**9)
        b = random.randint(0, 10**12)
        m = random.choice([10**9 + 7, 998244353, 1000000007, 97])
        assert mod_pow(a, b, m) == pow(a, b, m), (a, b, m)

    assert mod_pow(3, 13, 10**9) == 3**13 % (10**9)
    assert mod_pow(2, 10, 1000) == 24

    # 矩阵快速幂求斐波那契
    for n in range(0, 30):
        assert fib(n, M) == fib_iter_verify(n) % M, n
    assert fib(50, M) == 12586269025 % M

    print("All tests passed.")
```

**PyPy 提示**: 整数取模直接 pow(a,b,m)（C 实现）最快；矩阵乘法是 Python 热点，i-k-j 循环顺序（先固定 i,k）利用缓存并减少取模次数（每行累加后再取模），PyPy 下 100 阶矩阵 log 次乘可过。大矩阵考虑 numpy（若 OJ 允许）。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(log b) 次乘法；矩阵快速幂 O(n³ log b)（n 为矩阵阶数） |
| 空间 | O(1) 整数版；O(n²) 矩阵版 |

### 局限

要求运算满足结合律（矩阵、置换、函数复合均可，但需注意非交换对象的结果顺序）。对超大指数可用扩展欧拉定理先降幂。Python 大整数乘法本身不是 O(1)，n 极大时需考虑位数影响。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1226 | 2 | 【模板】快速幂：a^b mod p 标准模板 | [https://www.luogu.com.cn/problem/P1226](https://www.luogu.com.cn/problem/P1226) |
| Luogu | P1962 | 4 | 斐波那契数列：矩阵快速幂求 F_n，n 可达 2^63 | [https://www.luogu.com.cn/problem/P1962](https://www.luogu.com.cn/problem/P1962) |
| Luogu | P1045 | 5 | 麦森数：高精度快速幂求 2^P−1，OI Wiki 官方例题 | [https://www.luogu.com.cn/problem/P1045](https://www.luogu.com.cn/problem/P1045) |

## Pitfalls · 易错点

- res 初始化为 1 但未 % m，当 m=1 时返回错误（应 1%m）
- 指数 b 为 0 时处理（任何数的 0 次幂=1，注意 0^0 约定）
- 矩阵乘法顺序错误（非交换）
- 模意义下大数相乘在 C/C++ 中溢出（Python 无此问题）
- 递归版在 b 很大时递归深度仅 O(log b)，但 Python 默认递归限制可能不够（迭代版更稳）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/binary-exponentiation/](https://oi-wiki.org/math/binary-exponentiation/)
- CP-Algorithms ✓ [https://cp-algorithms.com/algebra/binary-exp.html](https://cp-algorithms.com/algebra/binary-exp.html)
- 书籍 ✓ `CPH ch21 Number theory (p207-216)`
