---
id: virtual-tree
name: 虚树
group: G-B-7
stage: advanced
priority: P2
depth_tier: standard
---

# 虚树

> 把关键点及其 LCA 压缩成小树，DP 复杂度从 O(nq) 降到 O(Σk log k)

<!-- 元信息: id=virtual-tree · group=G-B-7 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

虚树（Virtual Tree）是对树的「关键点集」做的一种压缩表示：给定 k 个关键点，只保留它们两两的 LCA 作为辅助节点，再加上各 LCA 之间的祖先关系，形成一棵只含 O(k) 个节点的小树。由于原树中绝大多数节点对某次询问没有影响，虚树把「每次 O(n) 的树 DP」变成「O(k log k) 建树 + O(k) DP」，当多次询问且 Σ关键点远小于 n×q 时收益巨大。虚树中保留的边权是原树上的路径权（距离或路径最小值等），祖先关系与原来一致。

## Why · 为什么

### 直觉 · Intuition

很多树上 DP（如「切断根到关键点的路径最小代价」）每次询问要遍历整棵树，但真正会改变答案的只有关键点和它们的分岔口（LCA）。别的点只是「路上的过客」，可以浓缩成一条边。设想把关键点按 DFS 序排好，相邻两个关键点的 LCA 就是虚树的必要节点——所有关键点两两的 LCA 全集，恰好等于「相邻对」的 LCA 集合，这是 O(k) 而不是 O(k^2)。

### 原理 · Principle

构造：①关键点按 dfn 排序；②对排序后相邻两点求 LCA 加入集合 A；③A 去重后按 dfn 再排序；④用单调栈维护一条「当前链」建树：栈中相邻元素在虚树中也是父子，逐点入栈，遇到 LCA 不在栈顶时先弹栈到合适位置（弹栈前连边）再把 LCA 入栈，最后连接栈顶与当前点。一次排序+去重+单调栈，总 O(k log k)（含 LCA 的 O(log n) 或 O(1) RMQ）。也可用「对排序后的关键点相邻求 LCA 加入、排序去重、相邻连 LCA 边」的二次排序法。正确性：DFS 序相邻保证了相邻点间路径上无其他关键点，故连边不重不漏。边权 = 原树上两点距离（可用 dep 差分）。

### 历史 · History

虚树在 OI/ICPC 中广泛用于多次询问的关键点稀疏场景，OI Wiki 以「SDOI2011 消耗战」引入：n<=2.5e5, q<=5e5, Σk<=5e5，朴素 O(nq) 必死，虚树把它变成 O(Σk log n)。OI Wiki 给出二次排序+单调栈两种构造并证明正确性；CP-Algorithms 未单列虚树（常见于中国竞赛圈子），故以 OI Wiki 为权威源并交叉验证其性质。

## How · 实现

### 伪代码

```python
build_vtree(keys):
  k = keys 按 dfn 排序
  st = [1]                    # 栈内维护当前链，默认根节点1加入
  for x in k:
    if x == st[-1]: continue
    l = lca(x, st[-1])
    if l != st[-1]:
      while len(st) > 1 and dfn[st[-2]] >= dfn[l]:
        add_edge(st[-2], st[-1]); st.pop()
      if st[-1] != l:
        add_edge(l, st[-1]); st.pop(); st.append(l)
    st.append(x)
  while len(st) > 1:
    add_edge(st[-2], st[-1]); st.pop()
```

### Python 实现

```python
import sys

sys.setrecursionlimit(1 << 20)


class LCA:
    def __init__(self, n, G):
        self.n = n
        self.G = G
        self.depth = [0] * (n + 1)
        self.up = [[0] * (n + 1) for _ in range(17)]
        self.dfn = [0] * (n + 1)
        self.timer = 0
        self._dfs(1, 0)

    def _dfs(self, u, f):
        self.timer += 1
        self.dfn[u] = self.timer
        self.up[0][u] = f
        for i in range(1, 17):
            self.up[i][u] = self.up[i - 1][self.up[i - 1][u]]
        for v in self.G[u]:
            if v != f:
                self.depth[v] = self.depth[u] + 1
                self._dfs(v, u)

    def lca(self, a, b):
        if self.depth[a] < self.depth[b]:
            a, b = b, a
        diff = self.depth[a] - self.depth[b]
        i = 0
        while diff:
            if diff & 1:
                a = self.up[i][a]
            diff >>= 1
            i += 1
        if a == b:
            return a
        for i in range(16, -1, -1):
            if self.up[i][a] != self.up[i][b]:
                a = self.up[i][a]
                b = self.up[i][b]
        return self.up[0][a]


def build_vtree(n, G, lca_inst, keys):
    ks = sorted(keys, key=lambda x: lca_inst.dfn[x])
    st = [1]
    vt = {}
    for x in ks:
        if x == st[-1]:
            continue
        l = lca_inst.lca(x, st[-1])
        if l != st[-1]:
            while len(st) > 1 and lca_inst.dfn[st[-2]] >= lca_inst.dfn[l]:
                vt.setdefault(st[-2], []).append(st[-1])
                st.pop()
            if st[-1] != l:
                vt.setdefault(l, []).append(st[-1])
                st.pop()
                st.append(l)
        st.append(x)
    while len(st) > 1:
        vt.setdefault(st[-2], []).append(st[-1])
        st.pop()
    return vt


def main():
    n = 8
    edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (5, 8)]
    G = [[] for _ in range(n + 1)]
    for a, b in edges:
        G[a].append(b)
        G[b].append(a)
    lca_inst = LCA(n, G)
    vt = build_vtree(n, G, lca_inst, [4, 6, 7, 8])
    print("virtual tree edges:")
    for u, vs in sorted(vt.items()):
        for v in vs:
            print(f"  {u} -> {v}")
    # 手算：关键点 {4,6,7,8}；LCA(4,8)=2, LCA(6,7)=3, LCA(2,3)=1, LCA(7,8)=1
    # 虚树节点 {1,2,3,4,6,7,8}；边 2->4, 2->8, 3->6, 3->7, 1->2, 1->3
    expect = {(2, 4), (2, 8), (3, 6), (3, 7), (1, 2), (1, 3)}
    got = set()
    for u, vs in vt.items():
        for v in vs:
            got.add((u, v))
    assert got == expect, got
    print("OK")


if __name__ == "__main__":
    main()

```

**PyPy 提示**: LCA 用倍增法 O(log n)/次，PyPy 下二维 up 表内存大，n=2e5 时 17*2e5 个 int 的 list-of-list 可行但稍慢；可换 1D 展平数组或二进制提升迭代。单调栈建虚树对热路径友好。Σk 达 1e6 时尽量一次预处理 LCA（RMQ 欧拉序可做到 O(1) 查询）并复用。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 建树 O(k log k)（排序 + k 次 LCA），单次 DP O(k)；总 O(Σk log n) |
| 空间 | O(n) 预处理（倍增表）+ O(k) 虚树 |

### 局限

需要 LCA 预处理；DP 需以「关键点集合 + 虚树」为输入重构（原树上其他节点的信息要么压缩进边权，要么预先维护子树聚合值）；虚树默认以 1 为根，若询问不涉及根需自行加入虚拟根处理。边权若是路径最大值/min 需用倍增维护，不能只用深度差。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P2495 | 5 | 【SDOI2011】消耗战：切断根到关键点的最小代价，虚树+树形DP 模板题 | [https://www.luogu.com.cn/problem/P2495](https://www.luogu.com.cn/problem/P2495) |
| Luogu | P4103 | 6 | 【HEOI2014】大工程：虚树上求点对距离和/最小/最大距离 | [https://www.luogu.com.cn/problem/P4103](https://www.luogu.com.cn/problem/P4103) |
| Codeforces | 613D | 2600 | Kingdom and its Cities：保护关键点最小割/最少删除点，虚树经典题 | [https://codeforces.com/problemset/problem/613/D](https://codeforces.com/problemset/problem/613/D) |

## Pitfalls · 易错点

- 相邻关键点求 LCA 而不是全部两两求（两两是 O(k^2) 会 TLE）
- 排序/去重必须按 dfn，否则建出的父子关系错乱
- 单调栈弹栈连边时，若 lca 不在栈中要先入栈（否则丢掉分岔点）
- 重复关键点去重（同一 LCA 可能被多次加入）
- 边权 = 原树距离，别用 dfn 差；路径最小值需倍增预处理 min-up
- DP 时遍历虚树子树要用虚树邻接表，不能递归到原树非虚树节点

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/virtual-tree/](https://oi-wiki.org/graph/virtual-tree/)
- oiwiki_raw ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/virtual-tree.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/virtual-tree.md)
