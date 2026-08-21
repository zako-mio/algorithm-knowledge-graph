---
id: vandermonde-convolution
name: 范德蒙德卷积
group: G-C-10
stage: advanced
priority: P2
depth_tier: standard
---

# 范德蒙德卷积

> C(n+m,k)=sum C(n,i)C(m,k-i)，组合恒等式的重要工具

<!-- 元信息: id=vandermonde-convolution · group=G-C-10 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

范德蒙德卷积（Vandermonde's convolution）是组合数学最重要的求和恒等式之一：Σ_{i=0}^{k} C(n,i)·C(m,k-i) = C(n+m,k)。它把『从 n+m 中选 k 个』拆成『先从 n 中选 i 个、再从 m 中选 k-i 个』。常用推论：Σ C(n,i)² = C(2n,n)；Σ C(n,i)C(n,i-1)=C(2n,n-1)；Σ C(n,i)C(m,i)=C(n+m,m)；Σ_{i=-r}^{s} C(n,r+i)C(m,s-i)=C(n+m,r+s)。它是化简组合和、证明组合恒等式、推导路径计数问题的标准武器。

## Why · 为什么

### 直觉 · Intuition

把 n+m 个物品看成『前 n 个』和『后 m 个』两组。要选出 k 个，无非是：从前组选 i 个（C(n,i)），再从后组选 k-i 个（C(m,k-i)），i 从 0 到 k 全枚举即不重不漏。二项式定理视角：(1+x)^n(1+x)^m=(1+x)^{n+m}，比较 x^k 系数立刻得到等式——两边展开再卷积。

### 原理 · Principle

① 代数证明：Σ_k C(n+m,k)x^k = (1+x)^{n+m} = (1+x)^n(1+x)^m = (Σ_r C(n,r)x^r)(Σ_s C(m,s)x^s)，比较 x^k 系数即得 Σ_{r=0}^k C(n,r)C(m,k-r)=C(n+m,k)；② 组合意义证明：从 n+m 的集合拆成两个大小 n、m 的子集，从 n 中取 i 个 + 从 m 中取 k-i 个，枚举 i 计数所有选法；③ 网格路径视角：从 (0,0) 到 (n,m) 共 C(n+m,m) 条路径，按前 n 步中向右步数 i 分段可得推论 4 Σ C(n,i)C(m,i)=C(n+m,m)。核心洞察：卷积求和与『拆集合』一一对应。

### 历史 · History

该恒等式以法国数学家 Alexandre-Théophile Vandermonde（1772）命名，但他本人并未直接发表；现代形式见于 19 世纪组合学文献。它被广泛应用于概率论（超几何分布归一性）、代数（卷积）、以及竞赛中的组合恒等式推导。OI Wiki 单独成章并给出二项式定理与组合意义双证明。

## How · 实现

### 伪代码

```python
# 直接验证: 求 sum_{i=0..k} C(n,i)*C(m,k-i)
def vandermonde(n, m, k):
  return sum(comb(n,i)*comb(m,k-i) for i in range(max(0,k-m), min(n,k)+1))
# 结论: 等于 comb(n+m, k)
```

### Python 实现

```python
def comb(n, k):
    """组合数 C(n,k) (不取模, 逐项整除保证精度)"""
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    r = 1
    for i in range(1, k + 1):
        r = r * (n - k + i) // i
    return r


def vandermonde_sum(n, m, k):
    """暴力求和 Σ_i C(n,i)*C(m,k-i), 验证用"""
    lo = max(0, k - m)
    hi = min(n, k)
    return sum(comb(n, i) * comb(m, k - i) for i in range(lo, hi + 1))


def vandermonde(n, m, k):
    """恒等式结果 C(n+m,k)"""
    return comb(n + m, k)


def corollary_sum_sq(n):
    """推论: Σ C(n,i)^2 = C(2n,n)"""
    return sum(comb(n, i) * comb(n, i) for i in range(n + 1))


if __name__ == "__main__":
    # 与暴力求和交叉验证 (含 n<m, k 边界)
    for n in range(0, 12):
        for m in range(0, 12):
            for k in range(0, n + m + 2):
                assert vandermonde_sum(n, m, k) == vandermonde(n, m, k), (n, m, k)
    # 经典特例
    assert vandermonde(5, 3, 4) == comb(8, 4) == 70
    assert vandermonde(4, 4, 4) == 70 == comb(8, 4)
    # 推论 3: Σ C(n,i)^2 = C(2n,n)
    for n in range(0, 10):
        assert corollary_sum_sq(n) == comb(2 * n, n), n
    # 推论 4: Σ C(n,i)C(m,i) = C(n+m,m)
    for n in range(0, 8):
        for m in range(0, 8):
            s = sum(comb(n, i) * comb(m, i) for i in range(0, min(n, m) + 1))
            assert s == comb(n + m, m), (n, m)
    print("All tests passed.")
```

**PyPy 提示**: 竞赛中通常不直接暴力求和，而是作为恒等式化简链的一步（如把 Σ 化为单个组合数后再用预计算阶乘 O(1) 求）。大 n 取模用阶乘+逆元；需要 n,m 到 1e7 且多次询问时可考虑 Lucas 定理组合使用。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(1)（公式本身）；暴力求和 O(min(n,k)-max(0,k-m)+1) |
| 空间 | O(1) |

### 局限

恒等式仅对组合数定义域内成立（C(n,k)=0 当 k>n 或 k<0），实现时枚举范围要裁剪。取模时若 n+m 超大且模数非质需要 exLucas。恒等式面向『化简』而非直接计算，单独使用价值在识别与套用。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Codeforces | 785D | 5 | Anton and School - 2：括号序列计数化简用到范德蒙德卷积 | [https://codeforces.com/problemset/problem/785/D](https://codeforces.com/problemset/problem/785/D) |
| Luogu | P2791 | 7 | 幼儿园篮球题：OI Wiki 习题，组合恒等式+卷积化简的综合题 | [https://www.luogu.com.cn/problem/P2791](https://www.luogu.com.cn/problem/P2791) |

## Pitfalls · 易错点

- 枚举 i 范围未裁剪（i 超过 n 或 k-i 超过 m 时对应项为 0）
- 把 C(n,i)C(m,i)=C(n+m,m)（推论4）与 C(n,i)C(n,i)=C(2n,n)（推论3）混淆
- 模意义下 C(n+m,k) 中 n+m 可能超过预计算上限导致越界
- 忘记 i 从 max(0,k-m) 开始（下界裁剪）导致少算/数组越界
- 公式面向化简，套用时先确认题目求和形式是否真匹配 Σ_i C(a,i)C(b,c-i)

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/combinatorics/vandermonde-convolution/](https://oi-wiki.org/math/combinatorics/vandermonde-convolution/)
- CP-Algorithms △ [https://cp-algorithms.com/combinatorics/stars_and_bars.html](https://cp-algorithms.com/combinatorics/stars_and_bars.html)
- web ✓ [https://www.cut-the-knot.org/arithmetic/algebra/VandermondeConvolution.shtml](https://www.cut-the-knot.org/arithmetic/algebra/VandermondeConvolution.shtml)
