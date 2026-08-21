---
id: stern-brocot
name: Stern-Brocot树/Farey序列
group: G-E-7
stage: advanced
priority: P2
depth_tier: standard
---

# Stern-Brocot树/Farey序列

> 枚举所有既约分数的二元搜索树：二分逼近实数，求最优分数逼近

<!-- 元信息: id=stern-brocot · group=G-E-7 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

Stern–Brocot 树是枚举全部正的最简分数的二叉搜索树。以三元组 (0/1, 1/1, 1/0) 为根，每个节点 (a/b, p/q, c/d) 的左右子为 (a/b, (a+p)/(b+q), p/q) 与 (p/q, (p+c)/(q+d), c/d)。相邻分数满足 bc-ad=1。应用：在树上二分逼近实数，找分母不超过某上限的最优分数逼近；Farey 序列(分母≤n 的 [0,1] 最简分数)是它的有限前缀；与连分数紧密相关，可 O(log(p+q)) 定位分数。

## Why · 为什么

### 直觉 · Intuition

两个相邻分数 a/b 与 c/d 之间永远插一个中位分数 (a+c)/(b+d)，它必然是最简的(bc-ad=1 保证互素)。反复在区间内插中位分数，就稠密地填满了 (0,∞) 的所有最简分数。查找某个实数 x 的最优逼近 = 在树上按大小二分走到某个精度，每走一步取当前区间端点的中位数。

### 原理 · Principle

单调性：a/b < (a+c)/(b+d) < c/d 恒成立(消分母即证)。最简性：bc-ad=1(行列式)在乘法 L=[[1,1],[0,1]], R=[[1,0],[1,1]] 下保持为1，由裴蜀定理知分子分母互素。完全性：任意 p/q 按二叉搜索路径必在有限步到达(否则 p+q 会增长矛盾)。分数查找快速算法把连续同向移动合并为 O(log(p+q))；无理数逼近取到边界时比较左右端点距离。

### 历史 · History

Moritz Stern(1858)与 Achille Brocot(1861)独立发现。Calkin–Wilf 树是其兄弟结构(非二叉搜索但同层分数相同、编号为位逆序置换)。Farey 序列与连分数、Ford 圆几何相关联。CP-Algorithms 与 OI Wiki 均有完整页面，OI Wiki 还给出 UVa 10077、LOJ 6685 等经典习题与 AtCoder ABC333G 等二分逼近题。

## How · 实现

### 伪代码

```python
# 分数逼近: 在 (a/b, c/d) 区间中位数逼近 x, 分母上限 D
# 朴素: 每次比较中位数与 x
a, b, c, d = 0, 1, 1, 0      # 0/1 与 1/0
while True:
  p, q = a + c, b + d        # 中位分数
  if b + d > D: break        # 分母超限
  if p / q < x:
    a, b = p, q              # 取右半
  elif p / q > x:
    c, d = p, q              # 取左半
  else:
    a, b, c, d = p, q, p, q  # 恰好命中
# 比较 (a/b) 与 (c/d) 谁更接近 x
```

### Python 实现

```python
def find_fraction(x, D):
    """在分母<=D 的最简分数中, 二分逼近实数 x。
    返回 (p, q) 为最佳逼近(比较左右边界距离)。
    """
    a, b, c, d = 0, 1, 1, 0  # 区间 (a/b, c/d)
    while True:
        p, q = a + c, b + d
        if q > D:
            break
        if p < x * q:
            a, b = p, q
        elif p > x * q:
            c, d = p, q
        else:
            a, b = p, q
            c, d = p, q
            break
    # 比较左右边界哪个更接近 x
    lv = abs(a - x * b) * d   # 交叉乘比较 |a/b - x| 与 |c/d - x|
    rv = abs(c - x * d) * b
    if lv <= rv:
        return a, b
    return c, d


def farey_sequence(n):
    """生成第 n 阶 Farey 序列([0,1] 分母<=n 的最简分数升序)。"""
    a, b, c, d = 0, 1, 1, n
    res = [(a, b)]
    while c <= n:
        k = (n + b) // d
        a, c, b, d = c, k * c - a, d, k * d - b
        res.append((a, b))
    return res


def stern_diatomic(n):
    """Stern 双原子序列 a_n (OEIS A002487):
    a0=0,a1=1, a2n=a_n, a2n+1=a_n+a_{n+1}。
    用 fusc 迭代实现。
    """
    if n == 0:
        return 0
    a, b = 1, 0
    while n:
        if n & 1:
            b += a
        else:
            a += b
        n >>= 1
    return b


if __name__ == '__main__':
    # 3/4 = 0.75, 分母<=4 最佳逼近应为 3/4 本身
    assert find_fraction(0.75, 4) == (3, 4)
    # 无理数 sqrt(2)≈1.4142, 分母<=10 的最佳逼近
    import math
    sq2 = math.sqrt(2)
    p, q = find_fraction(sq2, 10)
    # 已知分母<=10 的最佳为 17/12? 分母超界; 手动枚举验证
    best_p, best_q, best_err = 0, 1, float('inf')
    for dd in range(1, 11):
        pp = round(sq2 * dd)
        if abs(pp / dd - sq2) < best_err:
            best_p, best_q, best_err = pp, dd, abs(pp / dd - sq2)
    assert p == best_p and q == best_q, (p, q, best_p, best_q)

    # Farey 序列
    f4 = farey_sequence(4)
    expected = [(0, 1), (1, 4), (1, 3), (1, 2), (2, 3), (3, 4), (1, 1)]
    assert f4 == expected, f4
    assert len(farey_sequence(5)) == 11  # 1+sum_{k<=5} phi(k)=1+10

    # Stern 双原子序列
    sd = [stern_diatomic(i) for i in range(16)]
    assert sd == [0, 1, 1, 2, 1, 3, 2, 3, 1, 4, 3, 5, 2, 5, 3, 4], sd

    # 分数逼近: 1/pi 或任意有理数
    assert find_fraction(1 / 3, 20) == (1, 3)
    assert find_fraction(0.1, 50) in ((1, 10), (1, 10))

    print('sqrt(2) best frac (denom<=10):', find_fraction(sq2, 10))
    print('Farey(4):', f4)
    print('Stern diatomic [0..15]:', sd)
    print('All stern-brocot tests passed!')

```

**PyPy 提示**: 分数逼近用交叉相乘比较避免浮点精度问题(整数比较); Farey 递推为纯整数 O(n); 分母 D 极大时二分逼近注意 p,q 增长用 Python 大整数无溢出。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 分数查找朴素 O(P+Q)；快速合并同向移动 O(log(P+Q))；Farey 序列生成 O(\|F_n\|)=O(N²) |
| 空间 | O(1) 逼近; O(N²) Farey 序列存储 |

### 局限

逼近无理数时只保证收敛到任意精度, 但要输出'分母<=D 的最优逼近'需在边界比较左右端点距离; 朴素查找最坏 O(p+q) 分母大时不可用; 需结合连分数知识获得 O(log min(p,q)) 的定位; 非 [0,∞] 值域要预先伸缩。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| AtCoder | ABC333G | 4 | Nearest Fraction: Stern-Brocot树二分求分母<=N的最佳分数逼近, 现代经典 | [https://atcoder.jp/contests/abc333/tasks/abc333_g](https://atcoder.jp/contests/abc333/tasks/abc333_g) |
| Luogu | P8058 | 4 | BalkanOI2003 Farey序列: Farey序列构造/二分应用 | [https://www.luogu.com.cn/problem/P8058](https://www.luogu.com.cn/problem/P8058) |
| UVa | 10077 | 3 | The Stern-Brocot Number System: 在树上输出LR路径定位分数 | [https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=33&page=show_problem&problem=1018](https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=33&page=show_problem&problem=1018) |

## Pitfalls · 易错点

- 中位分数 (a+c)/(b+d) 在分母超限时即为最佳逼近的候选, 需与两端点比距离, 别直接返回中位数
- 交叉相乘比较距离: \|a/b - x\| 与 \|c/d - x\| 用 abs(a-x*b)*d 与 abs(c-x*d)*b, 别用浮点除法
- 区间初始为 (0/1, 1/0), 1/0 是无穷大记号, 分母为0 不是错误, 求 q 前判断
- Farey 递推 k=(n+b)//d 的下取整必须精确, 别四舍五入
- Stern 双原子序列的递推 a2n=a_n 是基于编号从1开始, 与 Calkin-Wilf 编号对应, 下标从0开始需特判

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/number-theory/stern-brocot/](https://oi-wiki.org/math/number-theory/stern-brocot/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/number-theory/stern-brocot.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/number-theory/stern-brocot.md)
- CP-Algorithms ✓ [https://cp-algorithms.com/others/stern_brocot_tree_farey_sequences.html](https://cp-algorithms.com/others/stern_brocot_tree_farey_sequences.html)
- web ✓ [https://en.wikipedia.org/wiki/Stern%E2%80%93Brocot_tree](https://en.wikipedia.org/wiki/Stern%E2%80%93Brocot_tree)
