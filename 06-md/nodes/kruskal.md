---
id: kruskal
name: Kruskal算法
group: G-B-3
stage: basic
priority: P0
depth_tier: deep
---

# Kruskal算法

> 最小生成树：把边按权值从小到大排序，并查集维护连通性，不成环则加入，O(E log E)；贪心+并查集的经典

<!-- 元信息: id=kruskal · group=G-B-3 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

Kruskal 算法求无向带权连通图的最小生成树（MST，边权和最小的生成子图；不连通图为生成森林）。流程：把全部边按权值非降排序；用并查集维护当前已加入的边形成的连通分量；从小到大遍历每条边 (u,v,w)，若 u、v 尚不连通（加入不成环）则选取该边并合并，直到选满 n−1 条边。时间复杂度 O(E log E)（排序主导）+ O(E α(n))（并查集近常数）。正确性由切边性质/循环不变式保证。

## Why · 为什么

### 直觉 · Intuition

贪心的朴素想法：'想要最便宜的树，当然优先要最便宜的边'，唯一的顾虑是便宜的边可能形成环。于是从小到大地尝试，只加不成环的边，直到 n−1 条。环的检测交给并查集（O(α(n))）。这个'最小边优先 + 防环'的贪心看似简单，但正确性需要切边性质支撑——任何横切一条最小边的割，最小生成树必含某条该割的边。

### 原理 · Principle

循环不变式：算法任意时刻已选边集 F 都包含于某棵 MST。基础：F=∅。归纳：设下一候选边 e=(u,v) 不成环（F+e 仍无环）。若 e 在某棵含 F 的 MST 中则直接加入成立。否则取一棵含 F 的 MST=T，在 T+e 的环上，除 e 外必有一条边 f 连接 T 中 u、v 路径（f∉F，因 F 无环且 e 不成环）。f 的权值：不会比 e 小（否则 f 会先于 e 被扫描到且不成环被加入，矛盾于 F 的归纳）；也不会比 e 大（否则 T+e−f 是更优生成树，矛盾于 T 是 MST）。故 w(f)=w(e)，T+e−f 仍是 MST 且含 F∪{e}，归纳成立。最终 F 为 MST。

### 历史 · History

Joseph Bernard Kruskal, Jr. 于 1956 年在论文《On the shortest spanning subtree of a graph and the traveling salesman problem》中提出该算法。与同年 Prim（与 Jarník 1930 独立发现）、以及 1926 年 Borůvka 的算法并称三大经典 MST 算法。并查集（disjoint-set union）为它提供了近线性的连通性维护，成为数据结构与贪心结合的代表作，被 OI Wiki 与 CP-Algorithms 收录为 MST 首选实现。

## How · 实现

### 伪代码

```python
class DSU: find / union
# 输入: n 个顶点, edges 为 (u,v,w) 列表
def kruskal(n, edges):
  sort edges by w 升序
  dsu = DSU(n); total = 0; cnt = 0
  for u, v, w in edges:
    if dsu.union(u, v):        # 不成环才成功合并
      total += w; cnt += 1
      if cnt == n - 1: break
  if cnt < n - 1: 不连通（图不连通）
  return total
```

### Python 实现

```python
class DSU:
    def __init__(self, n):
        self.par = list(range(n))
        self.sz = [1] * n

    def find(self, x):
        while self.par[x] != x:
            self.par[x] = self.par[self.par[x]]
            x = self.par[x]
        return x

    def union(self, a, b):
        """返回 True 表示成功合并（原不连通）。"""
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        if self.sz[a] < self.sz[b]:
            a, b = b, a
        self.par[b] = a
        self.sz[a] += self.sz[b]
        return True


def kruskal(n, edges):
    """返回 MST 边权和；图不连通（无法形成生成树）返回 None。
    edges: (u, v, w) 列表，顶点 0..n-1。
    """
    edges = sorted(edges, key=lambda e: e[2])
    dsu = DSU(n)
    total = 0
    cnt = 0
    for u, v, w in edges:
        if dsu.union(u, v):
            total += w
            cnt += 1
            if cnt == n - 1:
                break
    return total if cnt == n - 1 else None


if __name__ == "__main__":
    # 经典图：答案由 1+2+2+5 组成
    edges = [(0, 1, 4), (0, 2, 1), (1, 2, 2), (1, 3, 5), (2, 3, 8), (2, 4, 10), (3, 4, 2)]
    assert kruskal(5, edges) == 10

    # 暴力交叉验证（小图穷举所有生成树）
    import itertools

    def brute_mst(n, edges):
        best = None
        for r in range(len(edges) + 1):
            for combo in itertools.combinations(edges, r):
                if len(combo) != n - 1:
                    continue
                dsu = DSU(n)
                ok = True
                cost = 0
                for u, v, w in combo:
                    if not dsu.union(u, v):
                        ok = False
                        break
                    cost += w
                if ok:
                    best = cost if best is None else min(best, cost)
        return best

    import random
    random.seed(0)
    for _ in range(30):
        n = random.randint(2, 6)
        es = []
        for u in range(n):
            for v in range(u + 1, n):
                if random.random() < 0.6:
                    es.append((u, v, random.randint(1, 20)))
        got = kruskal(n, es)
        expect = brute_mst(n, es)
        assert got == expect, (n, es, got, expect)

    # 不连通情形
    assert kruskal(3, [(0, 1, 1)]) is None
    # 单点
    assert kruskal(1, []) == 0

    print("All tests passed.")
```

**PyPy 提示**: 排序用内置 sort（O(E log E)，PyPy 下快速）；并查集 find 用路径压缩（迭代写法避免递归栈），union by size 保树高 O(log n)。E=1e6、n=1e5 时排序约 1s，整体 2s 内可过。重边/自环由并查集自然处理（自环必不成环跳过）。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(E log E) 排序 + O(E α(n)) 并查集 ≈ O(E log E) |
| 空间 | O(E + n) |

### 局限

图不连通时只能得到生成森林（返回 None 或分别输出各分量）。只保证'一棵'MST，不处理唯一性/次小生成树（需额外逻辑）。稠密图（完全图）时 Kruskal 的 O(E log E) 不如 O(n^2) 的暴力 Prim。带权非负限制并非必需，负权也正确。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3366 | 2 | 【模板】最小生成树：Kruskal 直接套用，输出边权和（不连通输出 orz） | [https://www.luogu.com.cn/problem/P3366](https://www.luogu.com.cn/problem/P3366) |
| Luogu | P1195 | 3 | 口袋的天空：连成 k 棵棉花糖，Kruskal 提前终止条件 cnt==n-k（OI Wiki 例题） | [https://www.luogu.com.cn/problem/P1195](https://www.luogu.com.cn/problem/P1195) |
| LibreOJ | LOJ 2149 [SCOI2005] 繁忙的都市 | 3 | 求最大边权最小的生成树 = 最小瓶颈生成树，Kruskal 的性质（OI Wiki 习题） | [https://loj.ac/problem/2149](https://loj.ac/problem/2149) |

## Pitfalls · 易错点

- 排序必须按边权非降序，漏排序或不排序会直接错
- 并查集 union 返回是否合并成功，别在 union 失败时仍累加 total
- 提前终止条件是 cnt==n−1（MST 边数），不是遍历完所有边
- 不连通判定：遍历完 cnt<n−1 则返回 None/输出不连通提示
- 顶点编号从 0 开始要统一，读入 1-based 需减 1
- 边很多时排序用 key=lambda 而非 tuple 重排，避免结构体比较开销

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/mst/](https://oi-wiki.org/graph/mst/)
- CP-Algorithms ✓ [https://cp-algorithms.com/graph/mst_kruskal.html](https://cp-algorithms.com/graph/mst_kruskal.html)
- 书籍 ✓ `CPH ch15 Spanning trees, pp.143-146`
