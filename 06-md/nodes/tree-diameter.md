---
id: tree-diameter
name: 树的直径
group: G-B-7
stage: basic
priority: P0
depth_tier: deep
---

# 树的直径

> 树上最长简单路径，两次DFS或树形DP O(V)，负权边只能树形DP

<!-- 元信息: id=tree-diameter · group=G-B-7 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

树的直径指树上任意两结点间最长简单路径的长度(或该路径本身)。无负权边时可用两次 DFS/BFS：任选起点 y 找最远点 z，再从 z 找最远点 z'，dist(z,z') 即直径。有负权边时两次 DFS 失效，必须用树形 DP：记录每点向下最长与次长链，直径=max(d1[u]+d2[u])。正权树的所有直径中点重合。

## Why · 为什么

### 直觉 · Intuition

两次 DFS 的正确性基于'从任意点出发的最远点必是某条直径的端点'这一性质。树形 DP 则直接把'经过每个点的两条链之和'取最大：以 u 为根的子树中，直径要么在某个子树内部，要么是从 u 出发向下两条不共用首条边的链拼起来。

### 原理 · Principle

两次 DFS：反证法证明定理'从任意结点 y 出发 DFS 到达的最远结点 z 必为直径一端'。设直径 δ(s,t)，若 y 在直径上则 dist(y,z)>dist(y,t) ⇒ dist(s,z)>dist(s,t) 矛盾；y 不在直径上分两情形同理矛盾。因此第一次 DFS 得到直径端点 z，第二次从 z 得到另一端 z'。树形 DP：dp[u]=从 u 出发向下的最长链(方法2)，遍历子结点 v 时先用 d=max(d, dp[u]+dp[v]+w(u,v)) 更新答案再用 dp[v]+w 更新 dp[u]，保证两条链来自不同子树。

### 历史 · History

树直径问题是树上路径最优化最基础的模型。OI Wiki 明确'两次 DFS 或树形 DP 在 O(n) 求出直径'，并特别提醒负权边情形两次 DFS 的证明失效。直径性质(中点重合)源自树的凸性，广泛应用于树的中心/消防站选址(如 NOIP2007 树网的核)、直径上枚举优化等问题。

## How · 实现

### 伪代码

```python
# 两次 DFS (边权非负)
def dfs_farthest(u, parent):
  返回最远距离 dist 与结点 far
  for v in adj[u]:
    if v != parent:
      (d, f) = dfs_farthest(v, u)
      取 dist(u->v)+d 的最大者

z, _ = dfs_farthest(any_root, -1)
z2, diam = dfs_farthest(z, -1)
# diam 即直径长度; 记录前驱可回放路径

# 树形 DP (支持负权)
def dfs(u, p):
  d1 = d2 = 0   # 向下最长、次长(不同儿子方向)
  for v in adj[u]:
    if v == p: continue
    wv = dfs(v, u) + w(u,v)
    if wv > d1: d2, d1 = d1, wv
    elif wv > d2: d2 = wv
  ans = max(ans, d1 + d2)
  return d1
```

### Python 实现

```python
import sys
sys.setrecursionlimit(1 << 25)


def diameter_two_dfs(n, adj):
    """两次 DFS 求直径(边权非负)。
    返回 (长度, 路径)。
    """
    def farthest(start):
        dist = [-1] * n
        prev = [-1] * n
        stack = [(start, -1)]
        dist[start] = 0
        while stack:
            u, p = stack.pop()
            for v, w in adj[u]:
                if v != p and dist[v] == -1:
                    dist[v] = dist[u] + w
                    prev[v] = u
                    stack.append((v, u))
        far = max(range(n), key=lambda x: dist[x])
        return far, dist[far], prev

    z, _, _ = farthest(0)
    z2, diam, prev = farthest(z)
    # 回放路径
    path = []
    cur = z2
    while cur != -1:
        path.append(cur)
        cur = prev[cur]
    return diam, path


def diameter_tree_dp(n, adj):
    """树形 DP 求直径, 支持负权边。返回长度。"""
    ans = [0]
    visited = [False] * n

    def dfs(u, p):
        d1 = d2 = 0
        for v, w in adj[u]:
            if v == p:
                continue
            d = dfs(v, u) + w
            if d > d1:
                d2, d1 = d1, d
            elif d > d2:
                d2 = d
        ans[0] = max(ans[0], d1 + d2)
        return d1

    dfs(0, -1)
    return ans[0]


if __name__ == '__main__':
    # 链 0-1-2-3: 直径=3
    adj_chain = [[(1, 1)], [(0, 1), (2, 1)], [(1, 1), (3, 1)], [(2, 1)]]
    d, p = diameter_two_dfs(4, adj_chain)
    assert d == 3, d
    assert set(p) == {0, 1, 2, 3}, p
    assert diameter_tree_dp(4, adj_chain) == 3

    # 星型 0 连 1,2,3: 直径=2
    adj_star = [[(1, 1), (2, 1), (3, 1)], [(0, 1)], [(0, 1)], [(0, 1)]]
    d2, _ = diameter_two_dfs(4, adj_star)
    assert d2 == 2, d2
    assert diameter_tree_dp(4, adj_star) == 2

    # 负权边: 0-1(-5), 0-2(1), 1-3(2)
    # 最长简单路径: 1-3 = 2 (单边), 其余如 2-0-1-3 = -2, 0-2 = 1
    adj_neg = [[(1, -5), (2, 1)], [(0, -5), (3, 2)], [(0, 1)], [(1, 2)]]
    assert diameter_tree_dp(4, adj_neg) == 2
    # 两次 DFS 在此情形不保证正确, 故不断言

    print('chain diameter:', d)
    print('chain path    :', p)
    print('star diameter :', d2)
    print('negative-edge tree DP diameter:', diameter_tree_dp(4, adj_neg))
    print('All tree-diameter tests passed!')

```

**PyPy 提示**: 两次 DFS 用迭代栈避免递归深度问题; 树形 DP 需 sys.setrecursionlimit 或改为自底向上后序迭代。n=10^5 级数据 PyPy 的 list 邻接表比 dict 快很多。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 两次 DFS / 树形DP: O(N) |
| 空间 | O(N) — 邻接表 + dist 数组 + 递归栈 |

### 局限

两次 DFS 在有负权边时失效(证明依赖非负); 树形 DP 通用但难以直接回放整条路径(需额外记录最长/次长子结点); 直径'长度'与'路径'的求法不同, 输出路径须记录前驱。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | B4016 | 2 | 树的直径模板: 两次DFS或树形DP, n<=1e5 | [https://www.luogu.com.cn/problem/B4016](https://www.luogu.com.cn/problem/B4016) |
| Luogu | P1099 | 4 | 树网的核: NOIP2007, 直径上枚举+双指针, 直径性质应用 | [https://www.luogu.com.cn/problem/P1099](https://www.luogu.com.cn/problem/P1099) |
| Luogu | P3629 | 4 | 巡逻: APIO2010, 两次求直径(含负权变换), 直径路径标记 | [https://www.luogu.com.cn/problem/P3629](https://www.luogu.com.cn/problem/P3629) |

## Pitfalls · 易错点

- 负权边必须用树形 DP, 两次 DFS 会给出错误答案(证明依赖边权非负)
- d1/d2 更新顺序: 先算 d=d1+d2 再更新 d1/d2, 避免用同一儿子链拼自身(需两条不同方向链)
- 两次 DFS 找最远点用 max 时要留意 dist 初始值, 不连通时全部为 -1 需特判
- 输出路径时记录前驱, 第二次 DFS 的前驱数组从直径端点回溯
- n=1 单点树直径=0, 需单独处理(无向无环图中叶子度数<=1 定义下也无妨)

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/tree-diameter/](https://oi-wiki.org/graph/tree-diameter/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/tree-diameter.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/tree-diameter.md)
- 书籍 ✓ `CPH ch14 pp.143-150`
