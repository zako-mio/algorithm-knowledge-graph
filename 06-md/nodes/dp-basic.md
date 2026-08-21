---
id: dp-basic
name: 动态规划基础
group: G-A-11
stage: basic
priority: P0
depth_tier: deep
---

# 动态规划基础

> 最优子结构/无后效性/子问题重叠，状态定义与转移方程

<!-- 元信息: id=dp-basic · group=G-A-11 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

动态规划（Dynamic Programming, DP）将原问题分解为重叠子问题，用状态描述子问题、用状态转移方程描述子问题间关系，按序求解避免重复计算。三要素：最优子结构（原问题最优解含子问题最优解）、无后效性（已解子问题不受后续决策影响）、子问题重叠（同一子问题被多次需要，可缓存）。DP 的本质是在状态构成的 DAG 上求最长/短路。

## Why · 为什么

### 直觉 · Intuition

以数字三角形为例：从顶到底最大路径和。暴力枚举所有路径是 2^r 指数级。但观察：到每个点 (i,j) 的最优路径只取决于到上一层 (i-1,j-1) 和 (i-1,j) 的最优值——这就是子问题。把每个点「从顶到该点的最大和」存下来，逐层往下推，只需 O(r²)。这就是 DP：把重复计算的子问题结果存起来，用小问题答案拼出大问题答案。

### 原理 · Principle

DP 四步法：①阶段划分——把问题分成有序的阶段；②状态定义——dp[i] 或 dp[i][j] 描述阶段 i 的子问题；③状态转移——找出 dp[i] 由哪些更小状态转移而来（决策）；④按阶段顺序求解。图论视角：每个状态是 DAG 节点，决策是边，dp 值是节点权重，转移是边松弛。LCS 转移：dp[i][j] = dp[i-1][j-1]+1 (A_i=B_j) 否则 max(dp[i-1][j], dp[i][j-1])。

### 历史 · History

术语 'dynamic programming' 由 Richard Bellman 1950s 提出（'programming' 指表格法，非编程）。Bellman 用它解决最优控制问题。算法竞赛中 DP 是核心范式，OI Wiki 以数字三角形（IOI1994）为入门例题，CPH 第7章系统讲解。

## How · 实现

### 伪代码

```python
# 数字三角形 DP
def dp(triangle):
    r = len(triangle)
    f = [row[:] for row in triangle]  # f[i][j] = 从顶到(i,j)最大和
    for i in range(1, r):
        for j in range(i + 1):
            best = f[i-1][j] if j < i else -inf
            if j > 0: best = max(best, f[i-1][j-1])
            f[i][j] += best
    return max(f[r-1])
```

### Python 实现

```python
# 动态规划基础：数字三角形 + LCS（含自测）

def triangle_dp(triangle):
    """数字三角形: 从顶到底路径最大和
    triangle[i] 是长度 i+1 的列表"""
    r = len(triangle)
    if r == 0:
        return 0
    f = [row[:] for row in triangle]  # f[i][j] = 从顶到 (i,j) 的最大和
    for i in range(1, r):
        for j in range(i + 1):
            # 只能从左上 (i-1,j-1) 或正上 (i-1,j)
            up_left = f[i - 1][j - 1] if j > 0 else float('-inf')
            up = f[i - 1][j] if j < i else float('-inf')
            f[i][j] += max(up_left, up)
    return max(f[r - 1])

def lcs_length(a, b):
    """最长公共子序列长度, O(nm)"""
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[n][m]

if __name__ == "__main__":
    # 数字三角形 (IOI1994 示例)
    tri = [
        [7],
        [3, 8],
        [8, 1, 0],
        [2, 7, 4, 4],
        [4, 5, 2, 6, 5],
    ]
    assert triangle_dp(tri) == 30  # 7→3→8→7→5
    # LCS
    assert lcs_length("abcde", "acde") == 4
    assert lcs_length("AGGTAB", "GXTXAYB") == 4  # GTA
    # 单元素
    assert triangle_dp([[42]]) == 42
    print("dp-basic OK")

```

**PyPy 提示**: DP 二维数组在 PyPy 下若全 int 可享 list-strategy 紧凑存储，比 CPython 快且省内存。嵌套循环 JIT 友好，LCS O(nm) 在 PyPy 快 5-10 倍。注意大二维表 (>5000×5000) 内存约 200MB，PyPy 可能更高，需改滚动数组。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 数字三角形 O(r²)；LCS O(nm)；LIS O(n²) 或 O(n log n) |
| 空间 | 通常 O(状态数)，滚动优化 O(转移维度) |

### 局限

1) 不满足最优子结构/无后效性的问题不能用 DP；2) 状态空间爆炸时需优化（状压/滚动/单调队列等）；3) 状态定义错误导致整个解错——这是 DP 最难点。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1216 | 2 | DP 最经典入门题：从顶到底路径最大和 | [https://www.luogu.com.cn/problem/P1216](https://www.luogu.com.cn/problem/P1216) |
| Luogu | P2782 | 4 | 最长不下降子序列 O(n log n)，bisect 维护 d 数组 | [https://www.luogu.com.cn/problem/P2782](https://www.luogu.com.cn/problem/P2782) |
| Luogu | P2196 | 4 | DAG 最长路，拓扑序 DP | [https://www.luogu.com.cn/problem/P2196](https://www.luogu.com.cn/problem/P2196) |

## Pitfalls · 易错点

- 状态定义不当——没有正确刻画子问题，导致转移方程写不出或错误
- 不满足无后效性（后续决策影响已算子问题）→ 需扩充状态维度消除后效
- 转移方程遗漏决策（如 LCS 只考虑了匹配忘记跳过）
- 二维数组未正确独立创建（引用陷阱）导致结果串扰
- 忽略边界/初始状态（如 dp[0][0] 未正确设置）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/dp/basic/](https://oi-wiki.org/dp/basic/)
- CP-Algorithms ✓ [https://cp-algorithms.com/dynamic_programming/intro-to-dp.html](https://cp-algorithms.com/dynamic_programming/intro-to-dp.html)
- 书籍 ✓ `CPH ch7 p75`
