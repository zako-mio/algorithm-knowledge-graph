---
id: fibonacci
name: 斐波那契数列
group: G-C-10
stage: intermediate
priority: P0
depth_tier: deep
---

# 斐波那契数列

> F(n)=F(n-1)+F(n-2)，矩阵快速幂O(log n)求第n项，恒等式众多

<!-- 元信息: id=fibonacci · group=G-C-10 · stage=intermediate · priority=P0 · depth_tier=deep -->

## What · 是什么

斐波那契数列（Fibonacci sequence，OEIS A000045）定义 F_0=0, F_1=1, F_n=F_{n-1}+F_{n-2}：0, 1, 1, 2, 3, 5, 8, 13, 21, 34, …。它是组合/数论/算法题目的常客：可用矩阵快速幂或二进制倍增在 O(log n) 内求第 n 项（n 可达 2^63 甚至更大），拥有卡西尼恒等式、F_{m+n}=F_m F_{n+1}+F_{m-1}F_n、gcd(F_m,F_n)=F_gcd(m,n)、Pisano 周期等众多性质。相邻卢卡斯数列 L_n（L_0=2,L_1=1,L_n=L_{n-1}+L_{n-2}）常与其配对出现。

## Why · 为什么

### 直觉 · Intuition

递推 F_n=F_{n-1}+F_{n-2} 只依赖前两项，天然能写成 2×2 矩阵乘法 [F_n;F_{n-1}] = M·[F_{n-1};F_{n-2}]，其中 M=[[1,1],[1,0]]。于是 F_n 是 M^n 的某个分量，M^n 用快速幂 O(log n) 得到——把『每步加』变成『每步平方，指数翻倍』。更快的是二进制倍增：F_{2n}=F_n(2F_{n+1}-F_n)、F_{2n+1}=F_{n+1}²+F_n²，直接在 O(log n) 步里同时维护 (F_n,F_{n+1})。

### 原理 · Principle

① 矩阵形式：[[F_{n+1},F_n],[F_n,F_{n-1}]] = [[1,1],[1,0]]^n；② 倍恒等式（从卡西尼推导）：F_{2n}=F_n(2F_{n+1}-F_n)，F_{2n+1}=F_{n+1}²+F_n²，可递归按 n 的二进制位折叠；③ 通项公式（Binet）：F_n=(φ^n-ψ^n)/√5，φ=(1+√5)/2 为黄金比例，但浮点精度限制使其不适合作竞赛算法；④ 关键恒等式：卡西尼 F_{n-1}F_{n+1}-F_n²=(-1)^n；附加 F_{n+k}=F_k F_{n+1}+F_{k-1}F_n；gcd 性质 gcd(F_m,F_n)=F_{gcd(m,n)}；⑤ 模意义下数列以 Pisano 周期 π(m) 循环（周期 ≤ m²，且 π 对互素模数满足 lcm 关系，可经 CRT 分解）。

### 历史 · History

斐波那契（Leonardo Fibonacci）1202 年《计算之书》以兔子繁殖问题引入；Lucas 1878 年给出通项公式并命名卢卡斯数列；Carlini/Binet 更早给出解析式。卡西尼恒等式（Cassini, 1680）是最早的恒等式之一。矩阵快速幂求第 n 项是现代算法竞赛标准技巧，CP-Algorithms 与 OI Wiki 均有专章。

## How · 实现

### 伪代码

```python
# 矩阵快速幂: M=[[1,1],[1,0]], F_n = (M^n)[0][1]
mat_pow(M, n):
  R = I
  while n: R=R*M if n&1; M=M*M; n>>=1
  return R

# 二进制倍增 (更快, 无矩阵)
fib_pair(n):  # 返回 (F_n, F_{n+1})
  if n==0: return (0,1)
  (a,b) = fib_pair(n>>1)      # a=F_k, b=F_{k+1}, k=n//2
  c = a*(2*b - a)             # F_{2k}
  d = a*a + b*b               # F_{2k+1}
  return (d, c+d) if n&1 else (c, d)
```

### Python 实现

```python
def fib_matrix(n, mod=None):
    """矩阵快速幂求 F_n (F_0=0,F_1=1), O(log n)"""
    if n == 0:
        return 0

    def mul(A, B):
        m = mod
        return [
            [(A[0][0] * B[0][0] + A[0][1] * B[1][0]) % m if m else A[0][0] * B[0][0] + A[0][1] * B[1][0],
             (A[0][0] * B[0][1] + A[0][1] * B[1][1]) % m if m else A[0][0] * B[0][1] + A[0][1] * B[1][1]],
            [(A[1][0] * B[0][0] + A[1][1] * B[1][0]) % m if m else A[1][0] * B[0][0] + A[1][1] * B[1][0],
             (A[1][0] * B[0][1] + A[1][1] * B[1][1]) % m if m else A[1][0] * B[0][1] + A[1][1] * B[1][1]],
        ]

    M = [[1, 1], [1, 0]]
    R = [[1, 0], [0, 1]]
    while n:
        if n & 1:
            R = mul(R, M)
        M = mul(M, M)
        n >>= 1
    return R[0][1] % mod if mod else R[0][1]


def fib_pair(n, mod=None):
    """二进制倍增: 返回 (F_n, F_{n+1}), O(log n)"""
    if n == 0:
        return (0, 1) if not mod else (0 % mod, 1 % mod)
    a, b = fib_pair(n >> 1, mod)
    m = mod
    if m:
        c = a * ((2 * b - a) % m) % m
        d = (a * a + b * b) % m
    else:
        c = a * (2 * b - a)
        d = a * a + b * b
    if n & 1:
        return (d, (c + d) % m if m else c + d)
    return (c, d) if not m else (c % m, d % m)


def fib_big(n, mod=None):
    return fib_pair(n, mod)[0]


if __name__ == "__main__":

    def fib_iter(n):
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a

    # 三种实现与暴力迭代交叉验证
    for n in range(0, 300):
        want = fib_iter(n)
        assert fib_matrix(n) == want, n
        assert fib_big(n) == want, n
        assert fib_matrix(n, 10**9 + 7) == want % (10**9 + 7), n
        assert fib_big(n, 10**9 + 7) == want % (10**9 + 7), n

    # 大数: F_200 应为一固定值
    assert fib_big(200) == 280571172992510140037611932413038677189525
    # 已知边界
    assert fib_big(1) == 1 and fib_big(2) == 1 and fib_big(50) == 12586269025
    # 模意义大 n
    M = 998244353
    assert fib_big(10**18, M) == fib_matrix(10**18, M)
    print("All tests passed.")
```

**PyPy 提示**: PyPy 下倍增版常数远小于矩阵版（无嵌套循环）；若题目需要批量 F_1..F_n，直接用 O(n) 递推更优。矩阵乘法在 Python 中尽量展开为 2×2 标量式（如上），避免 list 嵌套循环。取模用局部变量 m 减少属性访问。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 矩阵/倍增 O(log n)；递推求前 n 项 O(n) |
| 空间 | O(log n) 递归栈（倍增）或 O(1) 迭代；矩阵 O(1) |

### 局限

Binet 公式因浮点误差不适合精确计算；递归倍增在 Python 默认深度下 log n 层没问题，但若 n 超大建议写迭代。模意义下若 m 巨大（>2^31），Python int 乘法会变慢但不会溢出。gcd(F_m,F_n)=F_gcd(m,n) 等恒等式只对自然数下标成立。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1962 | 4 | 【模板】斐波那契数列：矩阵快速幂求 F_n，n 可达 2^63 | [https://www.luogu.com.cn/problem/P1962](https://www.luogu.com.cn/problem/P1962) |
| Luogu | P4000 | 6 | 斐波那契数列：Pisano 周期+CRT 分解求超大 n 的 F_n mod p | [https://www.luogu.com.cn/problem/P4000](https://www.luogu.com.cn/problem/P4000) |
| Luogu | P1306 | 4 | 斐波那契公约数：gcd(F_n,F_m)=F_gcd(n,m) 应用 | [https://www.luogu.com.cn/problem/P1306](https://www.luogu.com.cn/problem/P1306) |

## Pitfalls · 易错点

- F_0=0, F_1=1 与部分题/语言『F_1=F_2=1』的偏移：矩阵/倍增代码下标必须与题目声明一致
- n 很大时递归写 fib(n)=fib(n-1)+fib(n-2) 会指数爆炸，必须用矩阵/倍增/记忆化
- 倍增时 (2*b - a) 可能为负，取模前需 % m 归一化
- 卡西尼恒等式 (-1)^n 在模意义下需注意符号
- 模数很大时 Python int 乘法开销上升，注意常数
- 求 F_n 与 F_{n+1} 混用：fib_pair 返回顺序是 (F_n,F_{n+1})

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/combinatorics/fibonacci/](https://oi-wiki.org/math/combinatorics/fibonacci/)
- CP-Algorithms ✓ [https://cp-algorithms.com/algebra/fibonacci-numbers.html](https://cp-algorithms.com/algebra/fibonacci-numbers.html)
- 书籍 ✓ `CPH ch21 Number theory (p207-216)`
