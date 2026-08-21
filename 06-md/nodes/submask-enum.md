---
id: submask-enum
name: 子集枚举
group: G-E-2
stage: intermediate
priority: P1
depth_tier: standard
---

# 子集枚举

> 枚举位掩码所有子集的 O(3^n) 技巧：s=(s-1)&m 从大到小枚举，子集 DP（状压）核心

<!-- 元信息: id=submask-enum · group=G-E-2 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

子集枚举：给定掩码 m，枚举它的所有子掩码 s（s 的每一位都在 m 中）。核心代码：`s=m; while True: use(s); if s==0: break; s=(s-1)&m`，按子掩码从大到小遍历，每个 O(1)。配合外层枚举所有掩码 m，总复杂度 O(3^n)（因为对每个元素有三种状态：不在 m、在 m 不在 s、在 m 且在 s）。子集 DP（状压 DP，如集合覆盖、旅行商、图论划分）大量使用。

## Why · 为什么

### 直觉 · Intuition

s-1 会把最低的 1 变成 0、右边全变 1；再 & m 把 m 里没有的位切掉——于是 s=(s-1)&m 得到『比 s 小的下一个 m 的子掩码』。因为 m 之外那些位被清空，循环严格递减且不重复。

### 原理 · Principle

设当前 s，s-1 把最低 set bit 清为 0 并将更低位置 1；(s-1)&m 保留 m 中的位，得到下一个（比 s 小的最大的）子掩码。终止于 s==0（此时再 s=(0-1)&m = (-1)&m = m 回到起点，所以必须判 0 break）。复杂度：m 有 k 个 set bit 时有 2^k 个子掩码；全枚举所有 m，每个元素三种归属 → 3^n。子集 DP 形式：`for m in range(1<<n): for s=m; s; s=(s-1)&m: dp[m] = min(dp[m], dp[s] + cost(s, m-s))`。

### 历史 · History

CP-Alg 的 all-submasks 页系统介绍此技巧与 O(3^n) 证明（二项式定理 Σ C(n,k)·2^k = 3^n）；CPH 第 10 章位操作部分也讲了子集枚举。这是状压 DP 中最常用的套路之一，广泛用于集合划分、图论子集、覆盖问题。

## How · 实现

### 伪代码

```python
# 枚举 m 的所有子掩码（含 m，不含 0 除非额外处理）
def submasks(m):
    s = m
    while True:
        yield s
        if s == 0:
            break
        s = (s - 1) & m

# O(3^n)：所有掩码的所有子掩码
for m in range(1 << n):
    for s in submasks(m):
        ...
```

### Python 实现

```python
def submasks(m):
    s = m
    while True:
        yield s
        if s == 0:
            break
        s = (s - 1) & m


def main():
    # 子掩码完整性与有序性
    got = list(submasks(0b101))  # 5
    assert got == [0b101, 0b100, 0b001, 0], got
    assert sorted(got) == sorted([0b101, 0b100, 0b001, 0])
    # 数量 = 2^popcount(m)
    m = 0b1101
    lst = list(submasks(m))
    assert len(lst) == (1 << m.bit_count())
    # 每个子掩码都确实是 m 的子集
    for s in lst:
        assert (s & m) == s
        assert (s | m) == m
    # 全部元素只出现一次（无重复）
    assert len(set(lst)) == len(lst)
    # O(3^n) 规模验证：n=12 时总次数
    n = 12
    total = 0
    for mm in range(1 << n):
        for _ in submasks(mm):
            total += 1
    assert total == 3**n, (total, 3**n)
    # 经典子集 DP 小例：集合覆盖成本最小化（伪应用）
    # 把 {0,1,2} 划分成若干子集，成本=子集大小，求最小总成本覆盖全集
    full = (1 << 3) - 1
    INF = 10**9
    dp = [INF] * (1 << 3)
    dp[0] = 0
    for m in range(1, 1 << 3):
        # 枚举子集做划分：任选一个子集 s，成本 = popcount(s)，合并剩余
        for s in submasks(m):
            if s == 0:
                continue
            rem = m & ~s
            dp[m] = min(dp[m], dp[rem] + s.bit_count())
    assert dp[full] == 3  # 分成3个单元素
    print("submask-enum OK")


if __name__ == "__main__":
    main()

```

**PyPy 提示**: s=(s-1)&m 是纯整数运算，PyPy 下每迭代 2 次位运算+比较，非常快。子集 DP 的外层 3^n 循环在 n≤20 时可行（3^20≈3.5e9 太多，实际 n≤15~18）。PyPy 的 JIT 对内层小循环友好。注意枚举中生成器 yield 有开销，性能关键时可改内联 while 循环。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 单掩码子掩码枚举 O(2^popcount(m))；全掩码总 O(3^n) |
| 空间 | O(1) 额外；子集 DP 数组 O(2^n) |

### 局限

3^n 是硬顶：n>18 时 Python 全枚举超时，需其他技巧（如 SOS DP、meet-in-the-middle）。子掩码枚举从大到小（数值序），若需按大小/特定顺序需排序（增加开销）。不枚举 0 时（从 m 到 1）注意退出条件。集合覆盖等 NP 问题用子集 DP 只适用于小 n。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| AtCoder | ABC187F | 1600 | Close Group：图上划分团的最小覆盖，子集 DP+补图判定，CP-Alg 子集枚举引用题 | [https://atcoder.jp/contests/abc187/tasks/abc187_f](https://atcoder.jp/contests/abc187/tasks/abc187_f) |
| UVa | 11825 | 3 | Hackers' Crackdown：集合覆盖的经典子集 DP，CP-Alg 引用题 | [https://onlinejudge.org/external/118/11825.pdf](https://onlinejudge.org/external/118/11825.pdf) |

## Pitfalls · 易错点

- 循环必须处理 s==0 的退出，否则 s=(0-1)&m = m 死循环
- yield 生成器在超高频调用（3^n 规模）有开销，性能瓶颈时改内联 while
- 子掩码按数值递减，不要假设与按大小递增一致
- 子集 DP 中 rem = m & ~s 而非 m^s（语义等价但显式掩码更清晰），注意 ~s 在 Python 是无限位宽取反，&m 后安全
- 忘记 m 本身也是其子掩码（含全集）；空集 0 也是子掩码（通常单独处理）
- 3^n 复杂度对 n≥19 会超时，误估 n 上限

## Sources · 信源

- CP-Algorithms ✓ [https://cp-algorithms.com/algebra/all-submasks.html](https://cp-algorithms.com/algebra/all-submasks.html)
- cph ✓ [https://usaco.guide/CPH.pdf#page=105](https://usaco.guide/CPH.pdf#page=105)
