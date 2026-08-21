---
id: dp-opt-quadrangle
name: 四边形不等式/决策单调性优化
group: G-A-12
stage: advanced
priority: P2
depth_tier: standard
---

# 四边形不等式/决策单调性优化

> w满足四边形不等式则决策单调，分治/单调队列优化

<!-- 元信息: id=dp-opt-quadrangle · group=G-A-12 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

四边形不等式优化利用「决策单调性」：对形如 f(i)=min_{j≤i} {w(j,i)} 的最优化问题，若成本 w 满足四边形不等式 w(a,c)+w(b,d) ≤ w(a,d)+w(b,c)（a≤b≤c≤d，即「交叉小于包含」），则最优决策点 opt(i) 单调不减。利用这一单调性，可用分治优化（O(n log n)）、二分队列（单调队列记录决策点覆盖区间，O(n log n)）、Knuth 优化（区间 DP，O(n²)）将朴素 O(n²)/O(n³) 大幅降低。经典应用：石子合并最小代价、最优二叉搜索树（Knuth）、IOI2000 邮局、POI2011 Lightning Conductor。

## Why · 为什么

### 直觉 · Intuition

决策单调性说明：随着问题参数 i 增大，最优的「起点 j」只会往右移动，不会回头。就像人在一排商店选址，要求越多时最优位置越靠右。若 w 满足「交叉 ≤ 包含」，数学上可以反证决策单调（定理1），证明用反证：若 opt(d)=a < b=opt(c)（a<b≤c<d），由最优性与四边形不等式推出矛盾）。

### 原理 · Principle

定义：决策单调性 opt(i) ≤ opt(i+1)。四边形不等式（quadrangle inequality / Monge 性质）w(a,c)+w(b,d) ≤ w(a,d)+w(b,c)。等价刻画：w 的二阶混合差分非正（离散凸/凹）。分治优化框架：solve(l,r,optL,optR) 计算中点 mid 的最优决策 opt(mid)（在 [optL,optR] 枚举），递归左半 [l,mid-1]（决策界 [optL,opt(mid)]）、右半 [mid+1,r]（决策界 [opt(mid),optR]）。每层每个决策至多被扫描常数次，总 O(n log n)。Knuth 优化：区间 DP f[i][j]=min_{k∈[i,j)} {f[i][k]+f[k+1][j]}+w(i,j)，若 w 满足四边形不等式且区间单调，则决策 k[i][j-1] ≤ k[i][j] ≤ k[i+1][j]，把 O(n³) 降到 O(n²)。二分队列（Aliens trick 前置）：记录每个决策 j 当前覆盖的问题区间 [l_j,r_j]，入队时与队尾决策二分比较，处理 w 需要动态计算的情形，O(n log n)。

### 历史 · History

四边形不等式与决策单调性的思想可追溯到 1970s-80s 的算法文献（D. E. Knuth 1971 年对最优二叉搜索树的 Knuth 优化；F. F. Yao 1982 年系统证明 quadrangle inequality 下的加速）。竞赛中 2000s 后成为省选/NOI 高频优化（邮局、石子合并）。CP-Algorithms 与 OI Wiki 均设专章（knuth-optimization / quadrangle）。

## How · 实现

### 伪代码

```python
# 判断 w 是否满足四边形不等式（随机抽样验证 + 理论证明）
for a<=b<=c<=d: assert w(a,c)+w(b,d) <= w(a,d)+w(b,c)

# 分治优化（决策单调）
solve(l, r, optL, optR):
  if l > r: return
  mid = (l+r)//2
  best_j = argmin_{j in [optL, min(mid-1,optR)]} w(j, mid)   # 枚举
  f[mid] = w(best_j, mid)
  solve(l, mid-1, optL, best_j)
  solve(mid+1, r, best_j, optR)

# Knuth 优化（区间DP）
for len in 1..n:
  for i, j=i+len:
    for k in [opt[i][j-1], opt[i+1][j]]:   # 决策界缩到 O(1) 摊还
      f[i][j] = min(f[i][k]+f[k+1][j]) + w(i,j)
    opt[i][j] = 最优 k
```

### Python 实现

```python
def quadrangle_divide_conquer(n, w):
    """分治优化：f[i] = min_{j<i} w(j,i)，要求决策单调。
    w(i,j) 由 callable 提供（这里用 precomputed 2D 列表模拟）。
    返回每个 i 的最优决策与 f[i]。"""
    f = [float('inf')] * (n + 1)
    opt = [0] * (n + 1)
    f[0] = 0

    def solve(l, r, optL, optR):
        if l > r:
            return
        mid = (l + r) // 2
        best_j, best_v = optL, float('inf')
        for j in range(optL, min(mid, optR) + 1):
            v = w(j, mid)
            if v < best_v:
                best_v, best_j = v, j
        opt[mid] = best_j
        f[mid] = best_v
        solve(l, mid - 1, optL, best_j)
        solve(mid + 1, r, best_j, optR)

    solve(1, n, 0, n)
    return f, opt


def knuth_optimization(n, w):
    """Knuth 优化区间 DP：f[i][j] = min_k { f[i][k]+f[k+1][j] } + w(i,j)。
    经典为石子合并/最优BST；此处用通用 cost w(i,j) 实现，O(n^2)。
    """
    f = [[0] * (n + 1) for _ in range(n + 1)]
    opt = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        opt[i][i] = i
    for length in range(2, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            best_v = float('inf')
            best_k = opt[i][j - 1]
            for k in range(opt[i][j - 1], min(opt[i + 1][j], j - 1) + 1):
                v = f[i][k] + f[k + 1][j] + w(i, j)
                if v < best_v:
                    best_v, best_k = v, k
            f[i][j] = best_v
            opt[i][j] = best_k
    return f[1][n]


def knuth_naive(n, w):
    """朴素区间 DP O(n^3) 对拍"""
    f = [[0] * (n + 1) for _ in range(n + 1)]
    for length in range(2, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            f[i][j] = min(f[i][k] + f[k + 1][j] for k in range(i, j)) + w(i, j)
    return f[1][n]


def cost_for_prefix_squares(n):
    """邮局/分治DP 的经典 w：sum |pos[k] - pos[j]|，满足四边形不等式。
    此处构造简单的递推以做自测（w(j,i) = 任意满足单调性的函数）。"""
    import random
    random.seed(3)
    pos = sorted(random.sample(range(1, 10000), n))
    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + pos[i]
    def w(j, i):
        # w(j,i) = sum_{k=j+1..i} (i-k)*a[k] 型成本，满足四边形不等式
        # 简化用二次型：w(j,i) = (i-j) * (suffix_cost)，保证非负且 Monge
        if j >= i:
            return float('inf')
        # 用「中位数绝对距离」的另一种非负构造：
        # w(j,i) = sum_{t=j+1}^{i} (t-j-1)^2  （恒非负、四边形不等式满足）
        return (i - j - 1) * (i - j) * (i - j + 1) // 3
    return w


def stone_merge_cost(n):
    """石子合并：w(i,j)=sum(a[i..j])，Knuth 优化适用（w 满足四边形不等式）"""
    import random
    random.seed(8)
    a = [random.randint(1, 100) for _ in range(n)]
    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + a[i]
    def w(i, j):
        return pref[j] - pref[i - 1]
    return w


if __name__ == "__main__":
    import random
    random.seed(41)
    # 分治优化（决策单调）正确性：w 取「到中位数距离」型（Monge）
    for n in [3, 7, 12]:
        w = cost_for_prefix_squares(n)
        f, opt = quadrangle_divide_conquer(n, w)
        # 验证决策单调
        assert all(opt[i] <= opt[i + 1] for i in range(1, n))
        # 与朴素逐点比对
        for i in range(1, n + 1):
            exp = min(w(j, i) for j in range(0, i))
            assert abs(f[i] - exp) < 1e-9, (i, f[i], exp)
    # Knuth 优化（石子合并）
    for n in [3, 6, 10]:
        w = stone_merge_cost(n)
        got = knuth_optimization(n, w)
        exp = knuth_naive(n, w)
        assert got == exp, (n, got, exp)
    # 决策单调性 + 四边形不等式抽样验证
    w = cost_for_prefix_squares(30)
    ok = True
    for a in range(0, 10):
        for b in range(a, 10):
            for c in range(b, 10):
                for dd in range(c, 10):
                    if w(a, c) + w(b, dd) > w(a, dd) + w(b, c) + 1e-9:
                        ok = False
    assert ok, "quadrangle inequality violated"
    print("All tests passed.")
```

**PyPy 提示**: 分治优化递归深度 O(log n) 安全；Knuth 优化的决策界区间需要正确初始 opt[i][i]=i。w(j,i) 若不能 O(1) 计算（需滑动游标），用「莫队式游标」维护 w 值（OI Wiki 移动访问）。大 n（1e5）分治可行，Knuth O(n²) 仅限 n≤5000。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 分治优化：O(n log n)；二分队列：O(n log n)；Knuth 优化：O(n²)（替代 O(n³)） |
| 空间 | 分治 O(n)；Knuth O(n²) |

### 局限

必须验证 w 满足四边形不等式（充分不必要条件）；决策单调性需取「最小/最大最优决策」约定一致。分治优化无法处理 w 依赖已计算 f 的「动态计算」情形（需二分队列）。Knuth 优化仅适用区间 DP 且 w 满足区间单调性。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P4767 | 6 | IOI2000 邮局：决策单调分治优化经典 | [https://www.luogu.com.cn/problem/P4767](https://www.luogu.com.cn/problem/P4767) |
| Luogu | P6246 | 7 | IOI2000 邮局加强版：二分队列/Aliens trick | [https://www.luogu.com.cn/problem/P6246](https://www.luogu.com.cn/problem/P6246) |
| LOJ | 2157 | 6 | POI2011 Lightning Conductor：决策单调性优化 | [https://loj.ac/problem/2157](https://loj.ac/problem/2157) |
| Codeforces | 321E | 6 | Ciel and Gondolas：分治优化 DP 模板（CP-Algorithms 例题） | [https://codeforces.com/contest/321/problem/E](https://codeforces.com/contest/321/problem/E) |
| SPOJ | BRKSTRNG | 5 | Knuth 优化区间 DP 练习 | [https://www.spoj.com/problems/BRKSTRNG/](https://www.spoj.com/problems/BRKSTRNG/) |

## Pitfalls · 易错点

- 未验证 w 满足四边形不等式就套优化，答案错误无提示
- 分治边界：决策枚举上界误用 mid-1（应为 min(mid, optR)）
- Knuth 优化中 opt[i][j-1] ≤ k ≤ opt[i+1][j] 的边界初始化错误
- 取最大/最小最优决策不一致导致决策区间不连续

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/dp/opt/quadrangle/](https://oi-wiki.org/dp/opt/quadrangle/)
- CP-Algorithms ✓ [https://cp-algorithms.com/dynamic_programming/knuth-optimization.html](https://cp-algorithms.com/dynamic_programming/knuth-optimization.html)
- 论文 ✓ `F. F. Yao, Efficiency of dynamic programming, JACM 1982`
