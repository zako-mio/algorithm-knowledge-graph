---
id: dp-tree-knapsack
name: 树上背包
group: G-A-11
stage: intermediate
priority: P1
depth_tier: standard
---

# 树上背包

> 树形DP+背包结合，依赖关系物品选择

<!-- 元信息: id=dp-tree-knapsack · group=G-A-11 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

树上背包是树形DP与背包DP的结合：物品之间存在树形依赖关系（选子节点必须先选父节点），在树上做分组背包式转移。状态f(u,j)表示以u为根的子树中选j个物品的最优值。DFS遍历子树时将每个子树视为一个「组」做背包合并。

## Why · 为什么

### 直觉 · Intuition

每棵子树是一个独立的「组」：从子树v中选k个物品，等价于分组背包中从一组里选一种方案。合并子树时，对当前容量j枚举分配给子树v的数量k，类似分组背包的转移。

### 原理 · Principle

状态转移：f(u,j)=max{f(u,j-k)+f(v,k)}，其中v是u的子节点，j为分配的容量。DFS(u)时初始f(u,0)=0,f(u,1)=val[u]（选u本身），然后逐个合并子树v：对当前已合并的容量j倒序枚举，对每个j枚举分给v的容量k。时间复杂度O(nm)，证明依赖子树大小乘积求和为O(n²)级别。

### 历史 · History

树上背包是树形DP的重要应用，OI Wiki将其放在树形DP页面中。经典问题P2014(CTSC1997选课)是教学题。其复杂度证明(子树合并背包为O(nm))是树形DP的经典分析。

## How · 实现

### 伪代码

```python
dfs(u):
  f[u][1] = val[u]  # 选u自己
  for v in children(u):
    dfs(v)
    # 合并子树v (分组背包)
    for j in current_size down to 1:
      for k in 1..min(size[v], j-1):
        f[u][j] = max(f[u][j], f[u][j-k] + f[v][k])
```

### Python 实现

```python
import sys
from collections import defaultdict


def tree_knapsack(n, parents, values, m):
    """树上背包 (CTSC1997 选课)
    n: 课程数 (0号是虚拟根)
    parents: [p1, p2, ...] 每个节点的父节点(先修课), 0表示无先修
    values: [v1, v2, ...] 每门课的学分
    m: 最多选m门课
    返回: 最多学分
    """
    adj = defaultdict(list)
    for i in range(1, n + 1):
        adj[parents[i]].append(i)  # 父->子

    INF = float('-inf')
    f = [[0] * (m + 1) for _ in range(n + 1)]
    size = [0] * (n + 1)

    def dfs(u):
        f[u][0] = 0
        if u >= 1:
            f[u][1] = values[u]
            size[u] = 1
        else:
            size[u] = 0
        for v in adj[u]:
            dfs(v)
            # 合并子树v (倒序枚举u的容量, 含0)
            for j in range(min(size[u], m), -1, -1):
                for k in range(1, min(size[v], m - j) + 1):
                    if f[u][j] + f[v][k] > f[u][j + k]:
                        f[u][j + k] = f[u][j] + f[v][k]
            size[u] += size[v]

    dfs(0)  # 从虚拟根开始
    return max(f[0][j] for j in range(m + 1))


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    # P2014 选课 示例
    # 4门课, 先修关系: 课1无先修, 课2先修1, 课3先修1, 课4先修2
    # 学分: 课1=4, 课2=2, 课3=3, 课4=2
    # 选3门课
    n = 4
    parents = [0, 0, 1, 1, 2]  # parents[i] = 节点i的父(0号虚拟根)
    values = [0, 4, 2, 3, 2]   # 0号虚拟根值为0
    m = 3
    ans = tree_knapsack(n, parents, values, m)
    # 选课1,2,4 -> 4+2+2=8 或 选课1,2,3 -> 4+2+3=9
    assert ans == 9, f"Expected 9, got {ans}"

    # 选2门
    ans2 = tree_knapsack(n, parents, values, 2)
    # 选课1,3 -> 4+3=7
    assert ans2 == 7, f"Expected 7, got {ans2}"

    print("All tests passed.")

```

**PyPy 提示**: PyPy递归+三维数组在n,m=300时约0.1s。注意size数组维护和倒序枚举防止重复转移。n,m>500时需注意空间O(nm)。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(nm) — 子树合并背包总转移次数 |
| 空间 | O(nm) — f表; 可滚动优化第二维 |

### 局限

f表O(nm)空间在n,m>500时约1M个元素，Python可能慢。递归深度需setrecursionlimit。复杂度证明依赖子树大小乘积求和。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P2014 | 2 | CTSC1997 选课：树上背包经典模板题，先修课依赖关系 | [https://www.luogu.com.cn/problem/P2014](https://www.luogu.com.cn/problem/P2014) |
| LOJ | 2546 | 4 | JSOI2018 潜入行动：树上背包+状压，背包容量为k的限制 | [https://loj.ac/problem/2546](https://loj.ac/problem/2546) |

## Pitfalls · 易错点

- 合并子树时容量j必须倒序枚举(类似0-1背包)，否则同一子树会重复选取
- size数组维护：合并子树v后size[u]+=size[v]，倒序上界需用合并前的size[u]
- 虚拟根(0号)的处理：无先修课的节点挂在虚拟根下，选0号不消耗容量
- f[u][j+k]的转移中k的范围是1..min(size[v], m-j)，j+k不能超过m

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/dp/tree/](https://oi-wiki.org/dp/tree/)
- CP-Algorithms ✓ [https://cp-algorithms.com/dynamic_programming/knapsack.html](https://cp-algorithms.com/dynamic_programming/knapsack.html)
