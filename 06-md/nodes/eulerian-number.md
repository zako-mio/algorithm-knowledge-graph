---
id: eulerian-number
name: 欧拉数
group: G-C-11
stage: frontier
priority: P3
depth_tier: brief
---

# 欧拉数

> A(n,m)=恰好 m 个『上升』(P_i<P_{i+1})的排列数，递推 (n-m)A(n-1,m-1)+(m+1)A(n-1,m)，Worpitzky 恒等式

<!-- 元信息: id=eulerian-number · group=G-C-11 · stage=frontier · priority=P3 · depth_tier=brief -->

## What · 是什么

欧拉数（Eulerian number）A(n,m) 统计 1..n 的排列中恰好有 m 个『上升』（相邻元素满足 p_i<p_{i+1}）的排列个数。注意与欧拉常数 e、Euler number（切比雪夫）区分。小表：A(1,0)=1；A(2,0)=1,A(2,1)=1；A(3,0)=1,A(3,1)=4,A(3,2)=1（即 123/132/213/231/312 各含上升数 2/1/1/1/1，321 含 0）。递推（m≥1, m<n, n>0）：A(n,m)=(n−m)·A(n−1,m−1)+(m+1)·A(n−1,m)；边界 A(n,0)=1（纯降序），A(n,m)=0 当 m≥n 或 n=0。经典恒等式：Worpitzky 恒等式 x^n=Σ_m A(n,m)·C(x+m,n)（把普通幂表为二项式系数带权组合）；以及 Σ_m A(n,m)=n!。欧拉数的行生成函数满足 ∑_m A(n,m)x^m = Σ_{k=0}^n k!·S(n+1,k+1)(x−1)^{n−k} 的等价格式。

## Why · 为什么

### 直觉 · Intuition

考虑在 n−1 的排列中插入新元素 n。n 是最大的数，把它插到某个上升位之前或排列最前时，上升数不变；插到别处（下降位、块中间、末尾）则上升数 +1。于是从 A(n−1,m−1) 到 A(n,m)（上升数增 1）有 n−m 种插入位（总 n 个位置减去 m−1+1 个保持位）；从 A(n−1,m) 到 A(n,m)（保持）有 m+1 种（m 个上升前 + 最前）。这就是递推的组合来源。

### 原理 · Principle

递推严格推导：将 n 插入 n−1 元排列的 n 个可能位置。保持上升数不变的位置 = 排列开头的 1 个 + 每个上升 p_{i−1}<p_i 的 p_i 之前（共 m 个）⇒ m+1 个。其余 n−(m+1) 个位置（下降/中间/末尾）使上升数 +1 ⇒ 从 A(n−1,m−1) 转移的系数是 n−(m−1)−1 = n−m。叠加即得递推。Worpitzky 恒等式 x^n=Σ_m A(n,m)C(x+m,n) 用插值/组合计数证明，是把幂函数展开到二项式基的桥梁，也是欧拉数与幂求和、生成函数联系的枢纽。所有行和为 n! 直接由『恰有若干上升』对排列全集划分得到。

### 历史 · History

欧拉数由 Euler 在研究幂级数与 ζ 函数时发现（18 世纪），命名『Eulerian number』区别于 Euler number。Worpitzky 恒等式由 Worpitzky 在 1883 年给出。欧拉数三角形（1 / 1 1 / 1 4 1 / 1 11 11 1 / …）是组合三角家族成员，与伯努利数、幂和公式密切相关。OI Wiki《欧拉数》页给出定义、小表、递推与 Python/C++ 实现，习题含 CF1349F（Slime and Sequences）、P7511。竞赛中多作为排列统计与多项式恒等变形工具。

## How · 实现

### 伪代码

```python
def eulerian_number(n, m):
  if m >= n or n == 0: return 0
  if m == 0: return 1
  return (n-m)*eulerian_number(n-1, m-1) + (m+1)*eulerian_number(n-1, m)

# 整行: 用一维 DP
#   row[m] 表示 A(当前行, m)
#   nxt[m] = (n-m)*row[m-1] + (m+1)*row[m]
```

### Python 实现

```python
MOD = 998244353


def eulerian_row(n, mod=MOD):
    """欧拉数整行 A(n,0..n-1), O(n^2) DP."""
    if n == 0:
        return []
    row = [1]          # n=1: A(1,0)=1
    for i in range(2, n + 1):
        m_len = i
        nxt = [0] * m_len
        nxt[0] = 1
        for m in range(1, m_len):
            left = (i - m) * (row[m - 1] if m - 1 < len(row) else 0)
            right = (m + 1) * (row[m] if m < len(row) else 0)
            nxt[m] = (left + right) % mod
        row = nxt
    return row


def eulerian_recur(n, m, memo=None):
    """单值递推(记忆化)."""
    if memo is None:
        memo = {}
    if m >= n or n == 0:
        return 0
    if m == 0:
        return 1
    key = (n, m)
    if key in memo:
        return memo[key]
    v = (n - m) * eulerian_recur(n - 1, m - 1, memo) + (m + 1) * eulerian_recur(n - 1, m, memo)
    memo[key] = v
    return v


def eulerian_worpitzky(n, x):
    """Worpitzky: x^n = sum_m A(n,m) * C(x+m, n). 验证版: 小 n 数值."""
    from math import comb, factorial

    return sum(eulerian_row(n)[m] * comb(x + m, n) for m in range(n))


def count_ascent(perm):
    return sum(1 for i in range(len(perm) - 1) if perm[i] < perm[i + 1])


def brute(n):
    from itertools import permutations
    cnt = [0] * n
    for p in permutations(range(1, n + 1)):
        cnt[count_ascent(p)] += 1
    return cnt


if __name__ == "__main__":
    from math import factorial
    # 已知小表
    assert eulerian_row(1) == [1]
    assert eulerian_row(2) == [1, 1]
    assert eulerian_row(3) == [1, 4, 1]
    assert eulerian_row(4) == [1, 11, 11, 1]
    assert eulerian_row(5) == [1, 26, 66, 26, 1]
    for n in range(1, 7):
        assert eulerian_row(n) == brute(n), (n, eulerian_row(n), brute(n))
        assert sum(eulerian_row(n)) == factorial(n)   # 行和为 n!
        for m in range(n):
            assert eulerian_recur(n, m) == eulerian_row(n)[m]
    # Worpitzky 恒等式数值验证 (x 取 3..7)
    for x in range(3, 8):
        for n in range(1, 5):
            assert eulerian_worpitzky(n, x) == x ** n, (n, x)
    print("eulerian-number: all tests passed")

```

**PyPy 提示**: 整行 O(n²) DP 用一维滚动数组，n≤5000 可过。单值递推记忆化避免指数爆炸。注意 m 取值范围 0..n−1（行长度 n）。模素数时直接取模；精确小值用 Python int 无碍。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 单值 O(n²)（记忆化实际 O(n·m)）；整行 O(n²) |
| 空间 | O(n) 滚动 |

### 局限

① A(n,m) 仅定义 m<n；② 与欧拉数 Euler number（正割数/切比雪夫）名字冲突易混淆；③ 无直接闭合公式，只能递推/生成函数；④ n 大需生成函数 + NTT（行生成函数与幂和联系）。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P7511 | 6 | 三到六：欧拉数/排列统计综合，OI Wiki 习题 | [https://www.luogu.com.cn/problem/P7511](https://www.luogu.com.cn/problem/P7511) |
| Codeforces | 1349F1 | 5 | Slime and Sequences (Easy)：与上升序列计数的联系，OI Wiki 习题（注：勿调 CF API） | [https://codeforces.com/problemset/problem/1349/F1](https://codeforces.com/problemset/problem/1349/F1) |
| UOJ | 593 | 7 | 新年的军队：欧拉数/伯努利数高级综合，OI Wiki 习题 | [https://uoj.ac/problem/593](https://uoj.ac/problem/593) |

## Pitfalls · 易错点

- m 范围误取到 n（A(n,n)=0 但表长为 n）
- 递推系数 n−m 与 m+1 写反
- 把 Eulerian number 当 Euler number（正割数）
- 整行 DP 时行长度变化导致越界（m−1/m 的边界处理）
- n=0 时返回空行而非 [1]

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/combinatorics/eulerian/](https://oi-wiki.org/math/combinatorics/eulerian/)
- oiwiki-raw ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/combinatorics/eulerian.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/math/combinatorics/eulerian.md)
- Wikipedia ✓ [https://en.wikipedia.org/wiki/Eulerian_number](https://en.wikipedia.org/wiki/Eulerian_number)
