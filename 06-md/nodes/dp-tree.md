---
id: dp-tree
name: 树形DP
group: G-A-11
stage: intermediate
priority: P0
depth_tier: deep
---

# 树形DP

> 树上递归DP，DFS后序传递子树最优解到父节点

<!-- 元信息: id=dp-tree · group=G-A-11 · stage=intermediate · priority=P0 · depth_tier=deep -->

## What · 是什么

树形DP是在树结构上进行的动态规划。利用树固有的递归性质，通常通过DFS后序遍历：先递归处理所有子树得到子问题的最优解，再将子树结果合并（向上传递）给父节点。典型问题包括没有上司的舞会（最大独立集）、树的直径、换根DP等。

## Why · 为什么

### 直觉 · Intuition

树上的每个节点都可以看作子树的根。要解决以 u 为根的问题，只需先解决 u 的所有子节点 v 的子问题，再把各子问题的解按某种规则合并到 u。这天然符合DFS后序遍历的顺序——先深入到叶节点（边界），再回溯时合并。

### 原理 · Principle

基本范式：f(u, state) 表示以 u 为根的子树在某个状态下的最优解。DFS(u) 遍历 u 的所有子节点 v，递归调用 DFS(v) 后，将 f(v, *) 合并到 f(u, *)。转移方程随问题而定：如最大独立集 f(u,0)=sum max(f(v,0),f(v,1)), f(u,1)=sum f(v,0)+val[u]。换根DP(二次扫描)：第一次DFS预处理子树信息，第二次DFS用父节点信息推导换根后的值。

### 历史 · History

树形DP是竞赛中的核心DP类型之一。其基本思想源于树的后序遍历——先处理子树再合并到根。换根DP（二次扫描/重新根DP）是树形DP的重要扩展，用于解决「不指定根、根的选择影响答案」的问题。OI Wiki以P1352(没有上司的舞会)为经典教学题。

## How · 实现

### 伪代码

```python
dfs(u, parent):
  f[u][0] = 0; f[u][1] = val[u]
  for v in children(u):
    if v == parent: continue
    dfs(v, u)
    f[u][0] += max(f[v][0], f[v][1])
    f[u][1] += f[v][0]
  # f[u][0] = u不选, f[u][1] = u选
  answer = max(f[root][0], f[root][1])
```

### Python 实现

```python
import sys
from collections import defaultdict


def tree_independent_set(n, edges, val):
    """树上最大权独立集 (没有上司的舞会)
    n: 节点数 (1-indexed)
    edges: [(u, v), ...] 无向边
    val: [val_1, val_2, ..., val_n] 各节点权值
    返回: 最大权独立集的权值和
    """
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    f = [[0, 0] for _ in range(n + 1)]
    visited = [False] * (n + 1)

    def dfs(u):
        visited[u] = True
        f[u][0] = 0       # u 不选
        f[u][1] = val[u]  # u 选
        for v in adj[u]:
            if visited[v]:
                continue
            dfs(v)
            f[u][0] += max(f[v][0], f[v][1])
            f[u][1] += f[v][0]

    dfs(1)  # 以节点 1 为根
    return max(f[1][0], f[1][1])


def reroot_dp(n, edges):
    """换根DP: 求使得所有节点深度和最大的根节点 (POI2008 STA)
    返回: (最佳根节点, 最大深度和)
    """
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    sz = [0] * (n + 1)  # 子树大小
    f = [0] * (n + 1)   # 以 i 为根时的深度和

    def dfs1(u, fa):
        sz[u] = 1
        f[u] = 0
        for v in adj[u]:
            if v == fa:
                continue
            dfs1(v, u)
            sz[u] += sz[v]
            f[u] += f[v] + sz[v]  # v 子树所有点深度+1

    dfs1(1, 0)

    best_node, best_val = 1, f[1]

    def dfs2(u, fa):
        nonlocal best_node, best_val
        for v in adj[u]:
            if v == fa:
                continue
            # 换根: u -> v
            f[v] = f[u] - sz[v] + (n - sz[v])
            if f[v] > best_val:
                best_val = f[v]
                best_node = v
            dfs2(v, u)

    dfs2(1, 0)
    return best_node, best_val


if __name__ == "__main__":
    sys.setrecursionlimit(10000)

    # P1352 没有上司的舞会 示例
    # 节点1权值1, 节点2权值1, 节点3权值1
    # 边: 1-2, 2-3 (链)
    # 选1和3 -> 权值2
    n = 3
    edges = [(1, 2), (2, 3)]
    val = [0, 1, 1, 1]  # 0号不用, 1-indexed
    result = tree_independent_set(n, edges, val)
    assert result == 2, f"Expected 2, got {result}"

    # 换根DP测试: 3节点链 1-2-3, 求深度和最大的根
    # root=1: depths 0,1,2 -> sum=3; root=2: 1,0,1 -> sum=2; root=3: 2,1,0 -> sum=3
    n2 = 3
    edges2 = [(1, 2), (2, 3)]
    root, depth_sum = reroot_dp(n2, edges2)
    assert depth_sum == 3, f"Expected depth_sum=3, got {depth_sum}"

    print("All tests passed.")

```

**PyPy 提示**: PyPy递归性能优于CPython但深递归仍需sys.setrecursionlimit。树形DP的Python递归在n>1e5时可能栈溢出，可改用sys.setrecursionlimit(1<<20)或手写栈迭代。PyPy对defaultdict(list)建图效率好。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n) — 每个节点访问一次，转移按度数均摊 |
| 空间 | O(n) — 邻接表+DP数组+递归栈 |

### 局限

Python递归深度默认1000，n>1000必须setrecursionlimit。n>1e5的树可能栈溢出。换根DP的第二次DFS需正确传递父节点信息。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1352 | 2 | 没有上司的舞会：树上最大权独立集，树形DP入门模板 | [https://www.luogu.com.cn/problem/P1352](https://www.luogu.com.cn/problem/P1352) |
| Luogu | P3478 | 2 | POI2008 STA-Station：换根DP模板，求深度和最大的根 | [https://www.luogu.com.cn/problem/P3478](https://www.luogu.com.cn/problem/P3478) |
| HDU | 2196 | 3 | Computer：树形DP求每个节点最远距离，需换根+次远维护 | [https://acm.hdu.edu.cn/showproblem.php?pid=2196](https://acm.hdu.edu.cn/showproblem.php?pid=2196) |

## Pitfalls · 易错点

- 忘记sys.setrecursionlimit导致RecursionError，Python默认仅1000
- 建无向图时DFS未跳过父节点(fa)导致死循环
- 换根DP第二次DFS时忘记恢复/传递父节点状态，导致答案错误
- 树形DP状态设计时遗漏某些维度（如是否选当前节点），导致后效性

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/dp/tree/](https://oi-wiki.org/dp/tree/)
- 书籍 ✓ `CPH ch10 p105`
