---
id: centroid-decomposition
name: 点分治
group: G-B-7
stage: advanced
priority: P2
depth_tier: standard
---

# 点分治

> 重心递归分解，统计树上路径 O(n log n)，建点分树后支持带修

<!-- 元信息: id=centroid-decomposition · group=G-B-7 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

点分治（重心分解 / Centroid Decomposition）是树上的分治框架：每次取当前连通块的重心 rt，统计所有「经过 rt」的路径对答案的贡献，然后把 rt 删除，对其余每个连通块递归同样处理。由于重心保证每块至多 n/2，递归深度 O(log n)，每层每个节点被访问一次，总复杂度 O(n log n)（加上统计逻辑自身的代价）。「路径覆盖性质」保证任意一条树上的路径都恰好在其所在连通块第一次分解到某个重心时被统计一次，从而不重不漏。其变体点分树（centroid tree）把分治重心连成一棵 O(log n) 层的树，可在线处理带修改的路径距离类问题。

## Why · 为什么

### 直觉 · Intuition

树上的路径统计（如「距离=k 的点对数」）暴力是 O(n^2)。分治的思路：任选一点 rt，任意路径要么经过 rt（跨两个子树或一端在 rt），要么完全落在某个子树内。经过 rt 的可以在 O(n) 内统计，不经过的递归处理。如果每次都选「重心」，两边的子问题都减半，深度 O(log n)——这就是把普通枚举变成 O(n log n) 的关键。选根必须选重心，否则遇到链/菊花会退化成 O(n^2)。

### 原理 · Principle

求连通块重心需一次 DFS 计算 siz（含「向上」部分 n-siz[u]），取最大连通块最小的点。统计经过重心的路径：先枚举重心的每个子树 ch，DFS 收集该子树内所有节点到 rt 的距离集合，用数组 tf（之前已处理子树中出现的距离）查是否有 tf[k-dist]=true 完成配对，再把本次距离写入 tf（若直接改全局桶）。核心技巧：清空 tf 不能用 memset（会 O(n) 每层、O(n^2) 总），而应记录所有改动过的下标入队，最后逐个清回 0。之后递归每个未被标记删除的子连通块。每层 O(n)，总 O(n log n)。点分树则每次把「上一层的总大小 - 重心方向连通块大小」作为下一层 tot 求重心，只需一次 DFS，并将重心连成 O(log n) 高的新树，支持带修改（如「到某个点距离<=d 的权值和」）。

### 历史 · History

点分治是静态树上路径统计问题的标准解法，OI Wiki 以其处理「经过根节点的路径」为引子给出三题（P3806 距离为 k、P4178 距离<=k、P2664 颜色贡献），并指出国外称 centroid decomposition。CP-Algorithms 系统给出性质定理（重心存在性/路径覆盖/深度 O(log n)）与「统计恰好长为 K 的路径数」的完整实现。点分树（题目常称动态点分治）则是其带修改扩展。

## How · 实现

### 伪代码

```python
decompose(u):
  tot = 计算连通块大小（用当前块 dfs，忽略已删除点）
  rt = 求重心(u, tot)
  process(rt)            # 统计所有经过 rt 的路径
  removed[rt] = True
  for v in adj[rt], not removed[v]: decompose(v)
get_siz(u,f): siz[u]=1; for v!=f and not removed[v]: siz[u]+=get_siz(v,u)
get_centroid(u,tot,f):
  for v in adj[u], v!=f and not removed[v]:
    if siz[v]*2 > tot: return get_centroid(v,tot,u)
  return u
process(rt):  # 例：距离为 K 的点对数
  tf[0]=1; 记录已改下标
  for ch in adj[rt], not removed[ch]:
    dists = []
    dfs_dist(ch, rt, 1, dists)      # 到 rt 的距离
    for d in dists: ans += tf[K-d]
    for d in dists: tf[d]+=1; 记录
  清空 tf 只回滚记录过的下标
```

### Python 实现

```python
import sys
from collections import deque

sys.setrecursionlimit(1 << 22)


def main():
    n = 7
    edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)]
    K = 2
    G = [[] for _ in range(n + 1)]
    for a, b in edges:
        G[a].append(b)
        G[b].append(a)

    removed = [False] * (n + 1)
    siz = [0] * (n + 1)
    tf = {0: 1}
    touched = [0]
    ans = 0

    def get_size(u, f):
        siz[u] = 1
        for v in G[u]:
            if v != f and not removed[v]:
                siz[u] += get_size(v, u)
        return siz[u]

    def get_centroid(u, tot, f):
        for v in G[u]:
            if v != f and not removed[v] and siz[v] * 2 > tot:
                return get_centroid(v, tot, u)
        return u

    def collect(u, f, d, out):
        if d > K:
            return
        out.append(d)
        for v in G[u]:
            if v != f and not removed[v]:
                collect(v, u, d + 1, out)

    def decompose(u):
        nonlocal ans
        tot = get_size(u, 0)
        rt = get_centroid(u, tot, 0)
        # 统计经过 rt 且距离恰为 K 的点对
        for ch in G[rt]:
            if removed[ch]:
                continue
            dists = []
            collect(ch, rt, 1, dists)
            for d in dists:
                ans += tf.get(K - d, 0)
            for d in dists:
                tf[d] = tf.get(d, 0) + 1
                touched.append(d)
        # 回滚本层 tf（只清改动过的下标，避免 O(n^2)）
        for d in touched:
            tf[d] = 0
        touched.clear()
        tf[0] = 1
        touched.append(0)
        removed[rt] = True
        for v in G[rt]:
            if not removed[v]:
                decompose(v)

    decompose(1)
    print("pairs with distance =", K, ":", ans)
    # 手算：距离2的点对 (1,4),(1,5),(1,6),(1,7),(2,3),(4,5),(6,7) 共 7 对
    assert ans == 7, ans
    print("OK")


if __name__ == "__main__":
    main()

```

**PyPy 提示**: 递归 decompose 深度 O(log n) 安全，但 get_size/collect 深度可达连通块大小，PyPy 需 sys.setrecursionlimit(1<<22)；每层清空桶务必用 touched 列表回滚，不能整数组重置。dict 桶 vs 数组桶：值域小（如 K<=1e5）用数组更快，值域大用 dict。collect 中 d>K 剪枝可大幅减常数。整体常数约为 C++ 的 8-15 倍，n=1e5 时限紧时优先 PyPy + 迭代。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n log n) — 每层 O(n)，层数 O(log n)；统计桶操作为每层 O(n) 摊还；点分树建树 O(n log n) |
| 空间 | O(n) — 邻接表 + siz + removed + 距离桶 |

### 局限

只能统计「与路径/距离相关」的信息，且要能对「经过当前重心的路径」做子集划分；若统计需要支持任意删改（在线）需点分树。每次递归必须重新计算连通块 siz 否则重心不准会退化。统计桶若用数组需注意值域（距离可达 n）；边分治、虚树等是其不同变体。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3806 | 4 | 【模板】点分治 1：m 次询问距离恰为 k 的点对是否存在 | [https://www.luogu.com.cn/problem/P3806](https://www.luogu.com.cn/problem/P3806) |
| Luogu | P4178 | 5 | Tree：统计距离 <= k 的点对数，桶换成线段树/双指针维护区间 | [https://www.luogu.com.cn/problem/P4178](https://www.luogu.com.cn/problem/P4178) |
| Luogu | P2664 | 6 | 树上游戏：按颜色贡献分解 sum_i，点分治高阶例题 | [https://www.luogu.com.cn/problem/P2664](https://www.luogu.com.cn/problem/P2664) |
| Codeforces | 161D | 1800 | Distance in Tree：统计距离恰为 k 的点对数，点分治/树形 DP 均可 | [https://codeforces.com/problemset/problem/161/D](https://codeforces.com/problemset/problem/161/D) |

## Pitfalls · 易错点

- 选重心前必须重新计算当前连通块的 siz（包含向上部分），用旧全树 siz 判断会选错重心导致层数退化
- 清空 tf 用 memset 导致 O(n^2)：必须记录改动过的下标再逐个回滚
- 统计「经过重心」的路径时把同一子树内的两点直接配对（如 ch 内两点经过 rt 计数）会重复计算：需先查桶再更新，保证配对的两端来自不同子树
- removed[rt]=True 时机：在统计完所有经过 rt 的路径之后、递归子树之前
- 带边权时距离类型用 long，剪枝 d>K 要按边权判断
- 点分树中求每层 tot 用「上层 tot - 重心方向大小」，不要重跑全树 DFS

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/tree-divide/](https://oi-wiki.org/graph/tree-divide/)
- oiwiki_raw ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/tree-divide.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/tree-divide.md)
- CP-Algorithms ✓ [https://cp-algorithms.com/graph/centroid_decomposition.html](https://cp-algorithms.com/graph/centroid_decomposition.html)
