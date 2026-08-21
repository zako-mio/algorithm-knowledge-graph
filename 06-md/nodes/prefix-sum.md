---
id: prefix-sum
name: 前缀和与差分
group: G-A-1
stage: basic
priority: P0
depth_tier: deep
---

# 前缀和与差分

> O(1)区间和查询/O(1)区间修改，一维与多维

<!-- 元信息: id=prefix-sum · group=G-A-1 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

前缀和（Prefix Sum）与差分（Difference）是一对互逆的预处理技巧。前缀和 S[i]=a[1]+...+a[i] 使任意区间 [l,r] 的和能在 O(1) 时间由 S[r]-S[l-1] 得到；差分 D[i]=a[i]-a[i-1] 使对区间 [l,r] 加一个常数 v 只需 D[l]+=v、D[r+1]-=v 两次 O(1) 操作，最后做一次前缀和恢复。二者推广到二维（容斥公式）、多维（逐维处理）、树上（点差分/边差分）仍保持高效。

## Why · 为什么

### 直觉 · Intuition

前缀和是「累加账本」：先花 O(n) 把账记好，之后问任意一段的总额只需翻一页。差分是「打补丁」：在补丁的开始处记 +v，结束之后记 -v，最后一次性结算，就能把大量区间加操作压缩成 O(1) 每笔。二者互为逆运算，一维差分数组做一遍前缀和就还原原数组。

### 原理 · Principle

一维：S[i]=S[i-1]+a[i]，区间和=S[r]-S[l-1]。二维前缀和由容斥原理：S[i][j]=a[i][j]+S[i-1][j]+S[i][j-1]-S[i-1][j-1]，子矩阵和=S[x2][y2]-S[x1-1][y2]-S[x2][y1-1]+S[x1-1][y1-1]。一维差分：D[l]+=v,D[r+1]-=v。二维差分矩形加：四个角点 +v/-v。树上点差分：D[x]+=v,D[y]+=v,D[lca]-=v,D[fa(lca)]-=v；边差分：D[x]+=v,D[y]+=v,D[lca]-=2v，最后做子树和。

### 历史 · History

前缀和思想源自古典的级数求和，但在算法竞赛中由组合数学与计算几何的贡献广泛传播，成为所有高级数据结构（树状数组、线段树）的思维基石。OI Wiki 将前缀和/差分作为基础算法专题，CPH (Competitive Programmer's Handbook) 第 4 章也将其列为第一个优化技巧。

## How · 实现

### 伪代码

```python
# 一维前缀和
S[0] = 0
for i in 1..n: S[i] = S[i-1] + a[i]
range_sum(l, r) = S[r] - S[l-1]

# 一维差分（区间加）
for each (l, r, v):
  D[l] += v; D[r+1] -= v
for i in 1..n: a[i] = a[i-1] + D[i]

# 二维前缀和
for i in 1..m, j in 1..n:
  S[i][j] = a[i][j] + S[i-1][j] + S[i][j-1] - S[i-1][j-1]
sub_sum(x1,y1,x2,y2) = S[x2][y2]-S[x1-1][y2]-S[x2][y1-1]+S[x1-1][y1-1]
```

### Python 实现

```python
def prefix_sum_1d(a):
    """一维前缀和，返回 S 其中 S[0]=0"""
    n = len(a)
    S = [0] * (n + 1)
    for i in range(n):
        S[i + 1] = S[i] + a[i]
    return S


def range_sum(S, l, r):
    """查询区间 [l,r] 和（1-indexed）"""
    return S[r] - S[l - 1]


def difference_1d(n, ops):
    """一维差分：n 长度数组，ops=[(l,r,v)] 全部区间加，返回最终数组（1-indexed）"""
    D = [0] * (n + 2)
    for l, r, v in ops:
        D[l] += v
        D[r + 1] -= v
    a = [0] * (n + 1)
    for i in range(1, n + 1):
        a[i] = a[i - 1] + D[i]
    return a[1:]


def prefix_sum_2d(a):
    """二维前缀和，a 为 m×n 矩阵，返回 (m+1)×(n+1) 的 S"""
    m, n = len(a), len(a[0])
    S = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            S[i][j] = a[i - 1][j - 1] + S[i - 1][j] + S[i][j - 1] - S[i - 1][j - 1]
    return S


def sub_sum_2d(S, x1, y1, x2, y2):
    """子矩阵和，坐标 1-indexed"""
    return S[x2][y2] - S[x1 - 1][y2] - S[x2][y1 - 1] + S[x1 - 1][y1 - 1]


def difference_2d(m, n, rect_ops):
    """二维差分矩形加：rect_ops=[(x1,y1,x2,y2,v)]，返回最终矩阵"""
    D = [[0] * (n + 2) for _ in range(m + 2)]
    for x1, y1, x2, y2, v in rect_ops:
        D[x1][y1] += v
        D[x1][y2 + 1] -= v
        D[x2 + 1][y1] -= v
        D[x2 + 1][y2 + 1] += v
    a = [[0] * n for _ in range(m)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            a[i - 1][j - 1] = (D[i][j]
                               + (a[i - 2][j - 1] if i > 1 else 0)
                               + (a[i - 1][j - 2] if j > 1 else 0)
                               - (a[i - 2][j - 2] if i > 1 and j > 1 else 0))
    return a


if __name__ == "__main__":
    a = [1, 2, 3, 4, 5]
    S = prefix_sum_1d(a)
    assert range_sum(S, 2, 4) == 9      # 2+3+4
    assert range_sum(S, 1, 5) == 15
    assert range_sum(S, 3, 3) == 3

    res = difference_1d(5, [(1, 3, 2), (2, 4, 1)])
    assert res == [2, 3, 3, 1, 0], res

    M = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    S2 = prefix_sum_2d(M)
    assert sub_sum_2d(S2, 2, 2, 3, 3) == 28  # 5+6+8+9
    assert sub_sum_2d(S2, 1, 1, 1, 1) == 1
    assert sub_sum_2d(S2, 1, 1, 3, 3) == 45

    M2 = difference_2d(3, 3, [(1, 1, 2, 2, 5)])
    assert M2 == [[5, 5, 0], [5, 5, 0], [0, 0, 0]], M2

    print("All tests passed.")
```

**PyPy 提示**: PyPy 下二维前缀和的嵌套循环是热点，n=1e3 时 1e6 次内层操作约 0.1s，n=5e3 时注意内存（int 对象开销大），建议用 array 模块或 numpy（若 OJ 允许）。差分数组是 O(1) 更新、最终一次还原，PyPy 表现良好。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 一维：预处理 O(n)，单次查询/修改 O(1)；二维：预处理 O(mn)，单次查询/修改 O(1)；k 维逐维法 O(kN) |
| 空间 | 一维 O(n)，二维 O(mn)，k 维 O(N) |

### 局限

前缀和只支持静态查询（离线修改全部完成后统一查询）；若修改与查询交错，需树状数组/线段树。多维前缀和用容斥时项数以 2^k 爆炸，维度高时应用逐维法（SOS DP）。差分只能做区间整体加减，不能处理区间赋值/乘。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1387 | 3 | 最大正方形：二维前缀和+二分/枚举，OI Wiki 官方例题 | [https://www.luogu.com.cn/problem/P1387](https://www.luogu.com.cn/problem/P1387) |
| Luogu | P3397 | 3 | 地毯：二维差分区覆盖计数，矩形加的标准应用 | [https://www.luogu.com.cn/problem/P3397](https://www.luogu.com.cn/problem/P3397) |
| Luogu | P3128 | 5 | USACO15DEC 最大流：树上点差分+LCA，路径计数经典题 | [https://www.luogu.com.cn/problem/P3128](https://www.luogu.com.cn/problem/P3128) |
| Luogu | B3612 | 1 | 求区间和：一维前缀和最基础模板题 | [https://www.luogu.com.cn/problem/B3612](https://www.luogu.com.cn/problem/B3612) |
| AtCoder | joi2007ho_a | 800 | 最大の和：一维前缀和求固定长度最大子段和 | [https://atcoder.jp/contests/joi2007ho/tasks/joi2007ho_a](https://atcoder.jp/contests/joi2007ho/tasks/joi2007ho_a) |

## Pitfalls · 易错点

- 区间查询边界搞混：区间 [l,r] 是 S[r]-S[l-1]，不是 S[r]-S[l]（off-by-one）
- 差分数组需开到 n+2 防 D[r+1] 越界，尤其是 r=n 时
- 二维前缀和公式漏掉减 S[i-1][j-1]（重复加）
- 二维差分四个角点的正负号记错
- 树上差分点权 vs 边权公式混淆：点权 lca 减一次+fa(lca) 减一次，边权 lca 减两次

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/basic/prefix-sum/](https://oi-wiki.org/basic/prefix-sum/)
- 书籍 ✓ `CPH ch4 p45`
