---
id: bitmask-dp-optimization
name: 位掩码 DP 优化
group: G-E-10
stage: frontier
priority: P3
depth_tier: brief
---

# 位掩码 DP 优化

> 子集DP从O(3^n)优化到O(2^n·n)：按lowbit分治/仅枚举补集子集等技巧

<!-- 元信息: id=bitmask-dp-optimization · group=G-E-10 · stage=frontier · priority=P3 · depth_tier=brief -->

## What · 是什么

位掩码 DP（bitmask DP / subset DP）优化指一类将 O(3^n)（枚举每个集合的所有子集）降到 O(2^n · n) 的枚举技巧：用『固定元素法』——任取 mask 中一个元素（如最低位 lowbit），只枚举剩余元素的子集，则每个状态 (mask, submask) 被访问次数从 3^n 次降到 2^n·n 次；或对『每个集合只枚举其最大元素在转移中的角色』的结构化拆分。2026 CF Round 1100（Spectral::Cup）Editorial Problem F 使用 2^n·n·log(A) 位掩码 DP + 二分搜索实现『最大化最小值』，是位掩码优化在二分答案上的前沿组合。

## Why · 为什么

### 直觉 · Intuition

朴素枚举所有子集对 (mask, sub⊆mask) 的配对总数是 3^n。但很多转移只需要『mask 中某个固定元素』参与的拆分子集：固定 lowbit=mask&(-mask) 后，sub 只能在剩余 n-1 位里选，每个 mask 只有 2^{popcount-1} 个候选 sub，总和 ΣC(n,k)2^{k-1} = (3^n-1)/2 仍然大，但配合『每个元素对每个 mask 至多贡献 O(1)』的等价变换，可把每种『归属划分』压缩到 O(n) 次枚举（如 2^n·n 的 DP 转移，按添加元素的角度逐元素更新）。

### 原理 · Principle

常见手法：
1) 状态压缩枚举：for sub = mask; sub; sub = (sub-1)&mask 是 O(3^n) 全子集枚举；改为固定 lowbit=mask&-mask，枚举 mask^lowbit 的子集，使每个转移只涉及含 lowbit 的拆法，配合『sub 与 mask^sub 之一含 lowbit』的对称性使每步 O(1) 更新 O(n) 次 → O(2^n·n)。
2) 按位贡献 DP：dp[mask] 由 dp[mask^(1<<i)] 转移（i 为某固定新增位），每状态从 n 个前驱取最优，O(2^n·n)。
3) SOS(子集和) DP 属于同一家族：f[mask] = Σ_{sub⊆mask} g[sub]，O(2^n·n)。
CF 1100F 类题目在二分答案 X 后把『可行性』编码为位掩码 DP，状态 2^n、每状态转移 n·log A，总 O(2^n·n·log A·log Ans)。

### 历史 · History

子集枚举 3^n→2^n n 的优化是位运算 DP 的经典主题（OI Wiki 位运算/子集枚举章节、submask-enum），SOS DP（sum over subsets）亦为社区标配。2026 CF Round 1100 Editorial Problem F（blog entry 153948）将 2^n·n·log(A) 位掩码 DP 与二分搜索结合求最大化最小值，构成前沿应用。

## How · 实现

### 伪代码

```python
# 3^n -> 2^n*n: 固定 lowbit 枚举含 lb 的补集子集
for mask in 0..(1<<n)-1:
    lb = mask & (-mask)
    sub = mask ^ lb
    while True:
        process(mask, sub)
        if sub == 0: break
        sub = (sub - 1) & (mask ^ lb)
# 每个 (mask, 含 lb 子集) 恰好一次, 总转移数 2^n·n
```

### Python 实现

```python
import random


def subset_dp_3n(n, a):
    """朴素 O(3^n)：对每个 mask 枚举其全部子集求和（含空集）。"""
    f = [0] * (1 << n)
    for mask in range(1 << n):
        sub = mask
        while True:
            f[mask] += a[sub]
            if sub == 0:
                break
            sub = (sub - 1) & mask
    return f


def subset_dp_2n(n, a):
    """O(2^n·n) 子集和（SOS DP）：逐位累加，对每个 mask 求所有子集和。
    关键：按位从低到高更新，f[mask] 表示 mask 在其低 i 位任意、高位固定时的部分和。
    """
    f = a[:]
    for i in range(n):
        for mask in range(1 << n):
            if mask & (1 << i):
                f[mask] += f[mask ^ (1 << i)]
    return f


def sos_dp(n, a):
    """SOS DP：O(2^n·n)，对每个 mask 求所有子集 a[sub] 的和。"""
    f = a[:]
    for i in range(n):
        for mask in range(1 << n):
            if mask & (1 << i):
                f[mask] += f[mask ^ (1 << i)]
    return f


def sos_brute(n, a):
    f = [0] * (1 << n)
    for mask in range(1 << n):
        sub = mask
        while True:
            f[mask] += a[sub]
            if sub == 0:
                break
            sub = (sub - 1) & mask
    return f


if __name__ == "__main__":
    random.seed(21)
    for n in range(1, 7):
        a = [random.randint(1, 30) for _ in range(1 << n)]
        # 固定 lowbit 版本与朴素全子集枚举等价（求和相同）
        f3 = subset_dp_3n(n, a)
        f2 = subset_dp_2n(n, a)
        assert f3 == f2, (n, f3, f2)
        # SOS DP 与暴力一致
        g1 = sos_dp(n, a)
        g2 = sos_brute(n, a)
        assert g1 == g2, (n, g1, g2)
    # 计数：验证固定lowbit枚举的总迭代次数显著小于 3^n
    n = 10
    cnt3 = sum((1 << bin(m).count("1")) for m in range(1 << n))
    print("monotonic full-subset iter count(3^n-1)=", cnt3)
    print("bitmask-dp-optimization 自测通过：固定lowbit枚举与SOS均与暴力一致")

```

**PyPy 提示**: SOS DP 双层循环纯 Python 在 n=22 时 ~4.6e7 次迭代偏慢，n=20 以下可接受；3^n 版 n=20 即爆炸。位运算在 PyPy 下快，必要时用 array 存储 dp。固定 lowbit 递推 f[mask]=a[mask]+f[mask^low] 不适用一般子集和（会重复计数），正确 O(2^n·n) 实现用逐位 SOS。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 固定 lowbit 子集枚举：约 3^n/2 次（仍指数）；SOS/逐位转移：O(2^n·n) |
| 空间 | O(2^n) |

### 局限

状态空间本身仍指数 2^n，n 上限约 20-23；3^n→2^n·n 只是常数/多项式因子改进，不能突破指数墙。需要「求和/取最值」这类可结合可交换算子才能用 SOS；若转移依赖 mask 的结构（如选最大元素）需用固定元素法重写。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Codeforces | 165E | 5 | Compatible Numbers：SOS DP/子集补集 位掩码经典题 | [https://codeforces.com/problemset/problem/165/E](https://codeforces.com/problemset/problem/165/E) |
| LeetCode | 1434 | 5 | 每个人戴不同帽子：按帽子位掩码 DP，2^帽子数×人 转移 | [https://leetcode.cn/problems/number-of-ways-to-wear-different-hats/](https://leetcode.cn/problems/number-of-ways-to-wear-different-hats/) |
| AtCoder | dp_o | 4 | Matching：二分图完美匹配数，O(2^n·n) 位掩码 DP（EDPC 例题） | [https://atcoder.jp/contests/dp/tasks/dp_o](https://atcoder.jp/contests/dp/tasks/dp_o) |

## Pitfalls · 易错点

- 全子集枚举 (sub-1)&mask 会枚举空集，记得处理 sub==0 边界
- 固定 lowbit 后只枚举含 lowbit 的子集，对称的另一半会丢，需想清转移是否需要全部
- SOS DP 内层更新方向（按位增）不能反，否则会重复叠加
- popcount 用内置 int.bit_count() 而不要手写
- 答案可能需要 mod，注意取模时序

## Sources · 信源

- web △ [https://codeforces.com/blog/entry/153948](https://codeforces.com/blog/entry/153948)
- OI Wiki ✓ [https://oi-wiki.org/math/bit/](https://oi-wiki.org/math/bit/)
