---
id: dsu-basic
name: 并查集(路径压缩+按秩合并)
group: G-A-4
stage: basic
priority: P0
depth_tier: deep
---

# 并查集(路径压缩+按秩合并)

> 近 O(1) 合并/查询集合，路径压缩 + 按大小/按秩合并，均摊 O(α(n))；模板题 P3367，Kruskal 最小生成树基石

<!-- 元信息: id=dsu-basic · group=G-A-4 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

并查集（Disjoint Set Union, DSU / Union-Find）：管理互不相交集合的森林结构。每个元素一个节点，树根代表集合；支持 ①查询 find(x) 返回 x 所在集合代表（根），用于判断两元素是否同集合；②合并 unite(x,y) 把两元素所在集合合并。两大优化：**路径压缩**（find 时把路径上节点直接连到根，下次 O(1)）与**按大小/按秩合并**（把小集合/浅树合并到大集合/深树下，防止退化）。两者结合后单次操作均摊 O(α(n))（反阿克曼函数，极小常数）。模板题 Luogu P3367。也是 Kruskal 最小生成树、判环、离线连通性、带权并查集的基础。

## Why · 为什么

### 直觉 · Intuition

集合用树存，根做代表。找集合 = 一路向上爬到根；合并 = 把一棵树的根挂到另一棵树的根下。问题：若总是『长得高』的树挂到『矮』的下面，树会越来越深，find 退化成链 O(n)。两个优化各堵一个坑：按大小合并保证树高 O(log n)（小并大，每个节点向上翻倍，最多 log n 次换父）；路径压缩在查询时顺手把沿途节点拉平，均摊接近 O(1)。

### 原理 · Principle

pa[x] 存父节点，根 pa[x]==x。find 递归/迭代：`if pa[x]!=x: pa[x]=find(pa[x])`（递归路径压缩）或迭代版（每次 pa[x]=pa[pa[x]] 路径减半）。unite(x,y)：rx=find(x), ry=find(y)；若同根返回；按大小合并则 size[rx]<size[ry] 交换，令 pa[ry]=rx, size[rx]+=size[ry]。复杂度证明（Tarjan 1984）：仅路径压缩最坏 O(m log n)，平均 O(mα(n))；仅启发式合并 O(m log n)；两者结合 O(mα(n))。势能法证明见 OI Wiki dsu-complexity 页。空间 O(n)。

### 历史 · History

并查集思想可追溯到 1959 年前后的等价类合并；路径压缩与按秩合并的复杂度分析由 Tarjan 等人在 1970-80 年代完成（Ackermann 函数反函数首次出现在并查集分析）。CPH 第 4 章（p53）作为基础数据结构介绍。OI Wiki ds/dsu 与 CP-Alg dsu 页均有详细讨论。Kruskal 算法、离线 RMQ、带权并查集（食物链 P2024）等均构建其上。

## How · 实现

### 伪代码

```python
class Dsu:
    pa  = [0..n-1]   # 父节点，根指向自己
    sz  = [1]*n      # 集合大小（按大小合并）

    def find(x):                       # 递归路径压缩
        if pa[x] != x:
            pa[x] = find(pa[x])
        return pa[x]

    def unite(a, b):
        ra, rb = find(a), find(b)
        if ra == rb: return
        if sz[ra] < sz[rb]: ra, rb = rb, ra   # 小的挂到大下
        pa[rb] = ra
        sz[ra] += sz[rb]
```

### Python 实现

```python
class Dsu:
    def __init__(self, n):
        self.pa = list(range(n))
        self.sz = [1] * n

    def find(self, x):
        if self.pa[x] != x:
            self.pa[x] = self.find(self.pa[x])
        return self.pa[x]

    def find_iter(self, x):
        # 迭代路径压缩（避免递归爆栈，链式毒瘤数据安全）
        while self.pa[x] != x:
            self.pa[x] = self.pa[self.pa[x]]  # 路径减半
            x = self.pa[x]
        return x

    def unite(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.sz[ra] < self.sz[rb]:
            ra, rb = rb, ra
        self.pa[rb] = ra
        self.sz[ra] += self.sz[rb]

    def same(self, a, b):
        return self.find(a) == self.find(b)


def main():
    dsu = Dsu(10)
    assert not dsu.same(0, 1)
    dsu.unite(0, 1)
    dsu.unite(1, 2)
    assert dsu.same(0, 2)
    assert not dsu.same(0, 3)
    dsu.unite(3, 4)
    dsu.unite(4, 2)
    assert dsu.same(3, 0)
    # 连通块数量
    roots = {dsu.find(i) for i in range(10)}
    assert len(roots) == 6  # 0..4 连成一块，5..9 各自
    # 与朴素对拍：随机合并验证 same 一致性
    import random
    random.seed(0)
    n = 200
    d = Dsu(n)
    comp = list(range(n))  # 朴素等价类

    def union_naive(a, b):
        ca, cb = comp[a], comp[b]
        for i in range(n):
            if comp[i] == cb:
                comp[i] = ca

    for _ in range(500):
        a, b = random.randrange(n), random.randrange(n)
        d.unite(a, b)
        union_naive(a, b)
        assert d.same(a, b) == (comp[a] == comp[b])
    print("dsu-basic OK")


if __name__ == "__main__":
    main()

```

**PyPy 提示**: 递归 find 在链状毒瘤数据下会爆递归栈（PyPy 默认递归上限约 1000），竞赛中建议用迭代版 find_iter（路径减半）或 sys.setrecursionlimit(1<<20)。PyPy 对 while 循环友好。P3367 数据 n,m 达 1e5~2e5，Python 直接过。若需极致，可用『路径压缩+按大小』并用迭代 find；不要同时维护 rank 与 size 两套（选其一即可）。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 单次 find/unite 均摊 O(α(n)) ≈ O(1)；m 次操作 O(m·α(n)) |
| 空间 | O(n) |

### 局限

并查集无法以较低复杂度分离集合（不可逆），只支持合并+查询。离线场景可配合线段树分治做『撤销』（但那需只启发式合并不用路径压缩）。只判连通时用启发式即可；需维护集合内其他信息（带权、大小、边权）需扩展结构。Python 递归 find 可能爆栈，务必迭代版。路径压缩+按秩合并不可直接可持久化（大量指针修改），可持久化并查集用只启发式合并。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3367 | 3 | 【模板】并查集：路径压缩+按大小合并直接过，OI Wiki 参考实现题 | [https://www.luogu.com.cn/problem/P3367](https://www.luogu.com.cn/problem/P3367) |
| Luogu | P2820 | 3 | 局域网：Kruskal 最小生成树用并查集判环/连通 | [https://www.luogu.com.cn/problem/P2820](https://www.luogu.com.cn/problem/P2820) |
| Luogu | P2024 | 6 | 食物链：带权并查集（维护模 3 关系），并查集进阶经典 | [https://www.luogu.com.cn/problem/P2024](https://www.luogu.com.cn/problem/P2024) |

## Pitfalls · 易错点

- find 忘记路径压缩导致树退化成链，大数据 TLE
- unite 时不判同根直接连会形成自环/环路，size 计数错误
- 按大小合并时把大集合挂到小集合下，树高退化 O(n)
- 递归 find 在毒瘤数据爆栈，用迭代路径减半或加大 recursionlimit
- 忘记初始化 pa[i]=i（根指向自己），find 死循环或返回错误
- 多组测试用例时未重建 Dsu 对象，残留上一组的状态
- 只维护 rank 不维护 size 时，合并要严格按秩，别混用

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/dsu/](https://oi-wiki.org/ds/dsu/)
- CP-Algorithms ✓ [https://cp-algorithms.com/data_structures/disjoint_set_union.html](https://cp-algorithms.com/data_structures/disjoint_set_union.html)
- 书籍 ✓ `CPH ch4 p53`
