---
id: tree-centroid
name: 树的重心
group: G-B-7
stage: intermediate
priority: P1
depth_tier: standard
---

# 树的重心

> 删除后最大连通块大小不超过 n/2 的节点，点分治/重心分解基础

<!-- 元信息: id=tree-centroid · group=G-B-7 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

树的重心是满足如下性质的节点 v：删去 v 后，得到的每个连通分量（子树）大小都不超过整棵树节点数 n 的一半；等价地，在所有节点中 v 的「重量」（删去 v 后最大连通分量大小）最小。重心若不唯一则恰有两个且相邻（n 为偶数时存在），此时删去两重心之间的边会把树分成两个大小相等（各 n/2）的连通分量。重心也是「使所有节点到它的距离和最小」的节点。

## Why · 为什么

### 直觉 · Intuition

把树想成一堆节点。如果在某个节点处把所有分支的「重量」都压到 n/2 以内，那么从它出发往任何方向走一步，都会有超过一半的节点在反方向——因此它可以同时「钳住」所有子树。删去重心后每块至多 n/2，意味着递归分解时子问题的规模严格减半，这就是它成为分治基点的原因：重心的存在让「把问题劈成一半」成为可能。

### 原理 · Principle

求重心只需一次 DFS：任意定根后算出每棵子树大小 siz[u]，则删去 u 后各连通块大小 = 各儿子子树大小 siz[ch]，以及「向上」部分 n-siz[u]。若所有儿子子树与向上部分都 <= n/2，u 即重心（从根向儿子走，只要存在 siz[ch]*2 > n 就朝 ch 走，走到走不动即重心）。等价定义：到所有点距离和最小（换根 DP 可证：从 v 换到邻居 u 时距离和变化 Δ = n - 2·siz[u方向]）。这是点分治/重心分解中每次 O(n) 找重心的理论依据。

### 历史 · History

重心（centroid）的「每块至多一半」性质使其成为树上分治的基石，点分治在国外常称 centroid decomposition / 重心分解。OI Wiki 给出等价定义（最大连通块最小、距离和最小）及四条常用性质；CP-Algorithms 的 centroid decomposition 页在定理中证明每棵树至少一个、至多两个相邻的重心，并由此推出分治深度 O(log n)。

## How · 实现

### 伪代码

```python
dfs(u, fa): siz[u]=1
  for v in adj[u], v!=fa: dfs(v,u); siz[u]+=siz[v]
find_centroid(root):
  u = root, parent = -1
  while True:
    found = False
    for v in adj[u], v!=parent:
      if siz[v]*2 > n: parent=u; u=v; found=True; break
    if not found: return u
```

### Python 实现

```python
import sys

sys.setrecursionlimit(1 << 20)


def dfs(u, fa, adj, siz):
    siz[u] = 1
    for v in adj[u]:
        if v != fa:
            dfs(v, u, adj, siz)
            siz[u] += siz[v]


def find_centroid(n, adj, siz, root=1):
    u, parent = root, -1
    while True:
        moved = False
        for v in adj[u]:
            if v != parent and siz[v] * 2 > n:
                parent, u = u, v
                moved = True
                break
        if not moved:
            return u


def main():
    n = 7
    edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)]
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    siz = [0] * (n + 1)
    dfs(1, 0, adj, siz)
    c = find_centroid(n, adj, siz)
    # 校验：删去 c 后所有连通块 <= n/2
    seen = [False] * (n + 1)
    def count_block(start, ban):
        st = [start]
        seen[start] = True
        cnt = 0
        while st:
            u = st.pop()
            cnt += 1
            for v in adj[u]:
                if v != ban and not seen[v]:
                    seen[v] = True
                    st.append(v)
        return cnt
    blocks = []
    seen[c] = True
    for v in adj[c]:
        if not seen[v]:
            blocks.append(count_block(v, c))
    print("centroid =", c)
    print("block sizes after removal =", blocks)
    assert all(b * 2 <= n for b in blocks), "not a centroid!"
    print("OK")


if __name__ == "__main__":
    main()

```

**PyPy 提示**: 本实现两遍 DFS（求 siz + 找重心）递归深度 O(n)，PyPy 下需 sys.setrecursionlimit；菊花图/链最坏递归深度可能达 n，超过默认 1000 栈限制，务必先设大 limit 或用迭代栈。纯 Python 复杂度 O(n) 常数约是 C++ 的 5-10 倍，但 n<=1e6 求单个重心仍可接受。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n) — 一次 DFS 求子树大小，一次 DFS 找重心 |
| 空间 | O(n) — 邻接表 + siz 数组 |

### 局限

重心定义依赖「子树大小」，无根树需先定根；点分治中每次递归都要在连通块内重新求 siz（总大小变化），否则用旧 siz 判断会错。多个重心时（n 偶数且存在恰一分为二）题目可能要求输出全部或特殊处理。距离和最小定义在点带权时不再等价，需用带权重心。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1364 | 2 | 医院设置：带权重心 / 距离和最小，可直接换根 DP 或枚举 | [https://www.luogu.com.cn/problem/P1364](https://www.luogu.com.cn/problem/P1364) |
| Codeforces | 685B | 2200 | Kay and Snowflake：求每棵子树的重心，利用「子树重心在重儿子子树重心到根的路径上」性质 | [https://codeforces.com/problemset/problem/685/B](https://codeforces.com/problemset/problem/685/B) |
| Codeforces | 1406C | 1900 | Link Cut Centroids：利用双重心性质构造删边/加边使树只有一个重心 | [https://codeforces.com/contest/1406/problem/C](https://codeforces.com/contest/1406/problem/C) |
| POJ | 1655 | 2 | Balancing Act：模板题，删点后最大连通块最小 | [http://poj.org/problem?id=1655](http://poj.org/problem?id=1655) |

## Pitfalls · 易错点

- 只考虑儿子子树大小而漏掉「向上」部分 n-siz[u] 的判定（删根时没有向上部分，但非根节点有）
- 点分治递归时忘了重新计算当前连通块的 siz，直接用全树的 siz 判断重心导致层数退化为 O(n)
- 重心不唯一时直接返回一个会漏答案，需判断 n 是否偶数且存在平分边
- 递归深度过大：链状树（n=1e5）递归求 siz 会爆 Python 默认栈，必须提高 recursionlimit 或用迭代

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/tree-centroid/](https://oi-wiki.org/graph/tree-centroid/)
- oiwiki_raw ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/tree-centroid.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/tree-centroid.md)
- CP-Algorithms ✓ [https://cp-algorithms.com/graph/centroid_decomposition.html](https://cp-algorithms.com/graph/centroid_decomposition.html)
- 书籍 ✓ `CPH ch14 pp143-150 (Tree algorithms: centroid)`
