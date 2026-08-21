---
id: dsu-application
name: 并查集应用（扩展域 / 带权 / 可撤销 / Kruskal 重构树）
group: G-D-9
stage: intermediate
priority: P1
depth_tier: deep
---

# 并查集应用（扩展域 / 带权 / 可撤销 / Kruskal 重构树）

> 并查集不只做连通性合并：扩展域（食物链）、带权（银河英雄传说）、按秩合并+可撤销（离线回退）、Kruskal 重构树（最小生成树转树上问题）、启发式合并（在线桥、连通时间）等，把连通性问题变成 O(α(n)) 或 O(log n) 的结构。

<!-- 元信息: id=dsu-application · group=G-D-9 · stage=intermediate · priority=P1 · depth_tier=deep -->

## What · 是什么

并查集（Disjoint Set Union / DSU）维护集合合并与『是否同一集合』查询。其应用远超基础连通性：① 扩展域并查集：把『关系』编码进多个维度（如食物链的三种动物关系，用 3 个域表达捕食/天敌/同类）；② 带权并查集：每个节点到父节点的权值（距离），路径压缩时同步累加，查询两节点间关系（银河英雄传说求两列间距）；③ 可撤销并查集：不用路径压缩、只按秩合并，记录操作历史支持回退（配合离线/时间线题目）；④ Kruskal 重构树：在 Kruskal 加边时新建代表边权的节点作为子树根，得到一棵满足『子树内任意两点连通时间 ≤ 根权值』的重构树，把『最小瓶颈/最早连通时间』问题转成树上倍增；⑤ 其他应用：每个边只覆盖一次的树上并查集（跳路径缩点）、按连通块合并方向维护统计等。

## Why · 为什么

### 直觉 · Intuition

并查集的本质是『维护等价类』，等价关系不止『连通』一种。许多问题里，元素之间的关系是可传递的，于是可以把每个关系维度映射为一个集合。扩展域是空间换思维：把每个元素的 n 种可能『身份』拆成 n 个点，关系就变成这些点之间的连通性。Kruskal 重构树更妙：把 Kruskal 加边的『时间轴』变成一棵树，边权即时间，树上祖先关系直接对应『连通时间先后』，于是离线+在线查询都能做。

### 原理 · Principle

① 扩展域：对每个元素 i 建立域 0..k-1，节点 (i, d) 表示『i 处于第 d 种身份』。关系如 a 吃 b 即 (a,0) 与 (b,1) 合并、(a,1) 与 (b,2)、(a,2) 与 (b,0) 同并。判断矛盾即检查冲突关系是否已同集。② 带权：parent + dist[x]（x 到 parent[x] 的权）；find 时 dist[x]+=dist[parent]，路径压缩后 dist[x] 为到根距离；两节点差 = dist 差。③ 可撤销：只按秩合并不路径压缩，并查集呈森林深度 O(log n)；用栈记录每次合并的 (x,y,rank_x) 可 O(1) 撤销。④ Kruskal 重构树：初始 n 个点权 0；加边 (u,v) 时若分属两集合，新建节点 w（权=边权），root(u)、root(v) 做 w 的儿子。性质：任意两点 LCA 权值 = 两点在原图的最小生成树上路径边权最大值 = 最早连通时间；倍增跳祖先查询满足权 ≤ 阈值的最浅祖先。⑤ 树上缩点（F 题）：f[x] 表示 x 到根路径第一个未覆盖点，覆盖后并查集向上合并，总复杂度 O(n α(n))。

### 历史 · History

并查集的思想可追溯至 20 世纪中叶，由 McIlroy 与 Morris（1950s）提出；『按秩合并 + 路径压缩』的反阿克曼复杂度由 Tarjan 与 van Leeuwen（1984）系统分析。Kruskal 重构树是并查集与最小生成树的结合，在 OI 中成为经典（Luogu P1967 货车运输、P4768 归程）。带权并查集广泛用于相对位置关系问题（P1196 银河英雄传说、P2024 食物链）。

## How · 实现

### 伪代码

```python
DSU:
    parent[], rank[]/size[]
    find(x): 路径压缩（带权时累加 dist）
    union(x,y): 按秩合并

# 扩展域（3 域食物链）：节点数 3n，域 0/1/2 = 同类/猎物/天敌
union((x,0),(y,1)); union((x,1),(y,2)); union((x,2),(y,0))

# Kruskal 重构树
for 边 (u,v,w) in 按 w 升序:
    if find(u)!=find(v):
        node = new(w); parent[node]=node
        parent[find(u)]=node; parent[find(v)]=node   # 连为儿子
query(u,v): LCA 权值

# 可撤销：
# union 时 push (x,y,rank) 到栈；rollback 时反向恢复
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
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        if self.sz[a] < self.sz[b]:
            a, b = b, a
        self.par[b] = a
        self.sz[a] += self.sz[b]
        return True

class RollbackDSU:
    """可撤销并查集：按秩合并 + 历史栈"""
    def __init__(self, n):
        self.par = list(range(n))
        self.depth = [1] * n
        self.hist = []
    def find(self, x):
        while self.par[x] != x:
            x = self.par[x]
        return x
    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            self.hist.append(None)
            return False
        if self.depth[a] < self.depth[b]:
            a, b = b, a
        self.hist.append((b, a, self.depth[a]))
        self.par[b] = a
        if self.depth[a] == self.depth[b]:
            self.depth[a] += 1
        return True
    def rollback(self):
        rec = self.hist.pop()
        if rec is None:
            return
        b, a, da = rec
        self.par[b] = b
        self.depth[a] = da

class WeightedDSU:
    """带权并查集：dist[x] 为 x 到根的距离（相对关系）"""
    def __init__(self, n):
        self.par = list(range(n))
        self.dist = [0] * n
    def find(self, x):
        if self.par[x] == x:
            return x
        r = self.find(self.par[x])
        self.dist[x] += self.dist[self.par[x]]
        self.par[x] = r
        return r
    def union(self, x, y, d):
        """使 dist[x] - dist[y] == d（d 可为负）"""
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return self.dist[x] - self.dist[y] == d
        self.par[rx] = ry
        self.dist[rx] = d + self.dist[y] - self.dist[x]
        return True
    def relation(self, x, y):
        self.find(x); self.find(y)  # 先压缩路径，dist 才准确
        return self.dist[x] - self.dist[y]

if __name__ == '__main__':
    # 基础连通性
    d = DSU(5)
    d.union(0, 1); d.union(1, 2)
    assert d.find(0) == d.find(2) and d.find(0) != d.find(3)
    print('DSU OK')
    # 带权：x-y=2, y-z=3 => x-z=5
    w = WeightedDSU(4)
    assert w.union(0, 1, 2)
    assert w.union(1, 2, 3)
    assert w.relation(0, 2) == 5
    assert w.union(0, 2, 5) is True
    assert w.union(0, 2, 6) is False
    print('WeightedDSU OK')
    # 可撤销
    r = RollbackDSU(4)
    r.union(0, 1); r.union(2, 3)
    assert r.find(0) == r.find(1)
    r.rollback()  # 撤销 (2,3)
    assert r.find(2) != r.find(3)
    assert r.find(0) == r.find(1)
    print('RollbackDSU OK')
```

**PyPy 提示**: find 用迭代 + 路径压缩（压缩祖父）避免递归栈溢出，PyPy 下性能良好；可撤销并查集深度 ≤ log n，find 不带路径压缩时深度也安全。n 达 1e6 时递归 find 会 RecursionError，务必用迭代。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 基础/带权/扩展域：find+union 均摊 O(α(n))；可撤销：O(log n)/次（深度界）；Kruskal 重构树：O(m log m) 排序 + O(m α(n))，树上倍增查询 O(log n) |
| 空间 | O(n)（Kruskal 重构树 O(n+m) 节点） |

### 局限

带权并查集要求关系是『可加且唯一』的（差分量），关系不满足结合律则不可用；可撤销并查集不能用路径压缩（会破坏历史栈）；Kruskal 重构树只适用于『连通时间/最小瓶颈权』这类单调合并场景；扩展域的状态数随关系维度指数增长，需控制域数量。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1196 | 3 | [NOI2002] 银河英雄传说：带权并查集经典题，维护到根的列距离 | [https://www.luogu.com.cn/problem/P1196](https://www.luogu.com.cn/problem/P1196) |
| Luogu | P2024 | 5 | [NOI2001] 食物链：扩展域（3 域）并查集经典题，三种关系编码 | [https://www.luogu.com.cn/problem/P2024](https://www.luogu.com.cn/problem/P2024) |
| Luogu | P3367 | 1 | 【模板】并查集：基础连通性模板 | [https://www.luogu.com.cn/problem/P3367](https://www.luogu.com.cn/problem/P3367) |
| Luogu | P1967 | 5 | [NOIP2013 提高] 货车运输：Kruskal 重构树 + 树上倍增查最小瓶颈权 | [https://www.luogu.com.cn/problem/P1967](https://www.luogu.com.cn/problem/P1967) |
| Luogu | P4768 | 7 | [NOI2018] 归程：Kruskal 重构树 + 最短路 + 阈值查询，重构树应用高峰 | [https://www.luogu.com.cn/problem/P4768](https://www.luogu.com.cn/problem/P4768) |

## Pitfalls · 易错点

- 可撤销并查集必须只按秩合并、不路径压缩，否则历史栈失效
- 带权并查集 union 的 dist 计算方向容易错，建议统一『dist[x]-dist[y]=d』并画图推导
- 扩展域节点数 = n×域数，数组开小是典型 RE/WA
- Kruskal 重构树查询是『两点 LCA』而不是 min(dist)，注意与倍增祖先权值比较的方向
- find 递归过深（n≥10^5 且未路径压缩）会爆栈，用迭代实现

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/topic/dsu-app.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/topic/dsu-app.md)
- CP-Algorithms ✓ [https://cp-algorithms.com/data_structures/disjoint_set_union.html](https://cp-algorithms.com/data_structures/disjoint_set_union.html)
