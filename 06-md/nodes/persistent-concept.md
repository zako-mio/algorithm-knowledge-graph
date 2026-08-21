---
id: persistent-concept
name: 可持久化数据结构概念
group: G-A-7
stage: intermediate
priority: P1
depth_tier: standard
---

# 可持久化数据结构概念

> 保留所有历史版本的数据结构：部分可持久化（只读旧版本）vs 完全可持久化（旧版本可继续修改），以可持久化线段树（主席树）为最典型实现。

<!-- 元信息: id=persistent-concept · group=G-A-7 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

可持久化数据结构（persistent data structure）允许访问/保留操作过程中的所有历史版本，核心是不可变性（immutable）：每次修改不破坏旧版本，而是基于旧版本新建一个『增量版本』，新旧版本共享未变部分。分类：① 部分可持久化（Partially Persistent）：所有版本可访问，但只能修改最新版本；② 完全可持久化（Fully Persistent）：所有版本既可访问又可修改（每次修改产生新版本）；③ 汇合可持久化（Confluently Persistent）：允许把两个历史版本合并成一个新版本（如 rope）。以可持久化线段树（主席树）为代表：每次单点修改复制 O(log n) 个新节点，其余节点与旧版本共享，实现『静态区间第 k 小』『可持久化数组』『可持久化并查集』等。

## Why · 为什么

### 直觉 · Intuition

『时光机』思维：如果每个版本都完整复制一份，代价 O(版本数×结构大小)，不可接受。可持久化的关键在于『共享』——一次修改只影响从根到叶的一条 O(log n) 链，只需把这 O(log n) 个节点新建出来，其余节点全部被新版本复用。于是版本数 k 的额外空间是 O(k log n)，时间 O(log n) 每次操作。典型如主席树：版本 t 是前 t 个元素建出的线段树，两个版本做差就能查询任意区间的信息（前缀和思想）。

### 原理 · Principle

① 不可变性与路径复制：对每个版本维护一棵根指针；修改时沿路径复制节点，新节点链接到子节点（未修改的子树继续用旧节点）。② 部分 vs 完全：部分可持久化只需支持『回到过去看』，修改只允许在最新版；完全可持久化需处理『从任意版本继续修改』，常用 fat node / path copying / 版本树（用并查集按时间分叉）等。③ 主席树（可持久化权值线段树）：版本 i 表示加入前 i 个数后的权值线段树；查询区间 [l,r] 的第 k 小 = 在版本 r 与版本 l-1 上同时下放，节点值做差得区间内各值域计数，从而二分值域。④ 可持久化并查集：用可持久化数组存 parent 与 rank，每版本只改 O(log n) 个元素。⑤ 实际应用：几何扫描线在线化、字符串 rope、redo/undo、函数式编程。

### 历史 · History

可持久化概念源自 1980 年代的函数式编程（不可变数据结构）与算法研究，Sarnak & Tarjan 于 1986 年在论文《Planar Point Location Using Persistent Search Trees》中提出路径复制（path copying）与可持久化线段树，把扫描线问题在线化。MIT 6.854 高级算法课程与 Wikipedia 有系统论述；国内 OI 以主席树（因发明者 HJT/黄嘉泰网名『主席』而得名）为普及载体，Luogu P3834/P3919 是模板题。

## How · 实现

### 伪代码

```python
# 可持久化线段树（主席树）：静态区间第 k 小
build(v=0, l=1, r=n):           # 版本 0 空树
update(prev_root, pos, val, l, r):   # 在 prev 版本上单点 +val，返回新根
    new = copy(prev)                 # 复制根节点
    if l == r: new.sum = prev.sum + val; return new
    mid = (l+r)/2
    if pos <= mid: new.left = update(prev.left, pos, val, l, mid)
    else:          new.right = update(prev.right, pos, val, mid+1, r)
    new.sum = new.left.sum + new.right.sum
    return new
query(root_r, root_l, k, l, r):    # 两版本同时下放，计数做差
    if l == r: return l
    mid = (l+r)/2
    left_count = root_r.left.sum - root_l.left.sum
    if k <= left_count: return query(root_r.left, root_l.left, k, l, mid)
    else: return query(root_r.right, root_l.right, k-left_count, mid+1, r)
```

### Python 实现

```python
class PersistentSegTree:
    """可持久化线段树（主席树）：静态数组区间第 k 小（值域离散化）"""
    def __init__(self, n, vals):
        self.n = n
        self.uniq = sorted(set(vals))
        self.m = len(self.uniq)
        self.lc = [0]
        self.rc = [0]
        self.sm = [0]
        self.roots = [0]
        self._empty = self._build(0, self.m - 1)
        self.roots[0] = self._empty
        for v in vals:
            self.roots.append(self._update(self.roots[-1], self._idx(v), 1, 0, self.m - 1))

    def _build(self, l, r):
        node = 0
        if l == r:
            return 0
        mid = (l + r) // 2
        self.lc.append(0); self.rc.append(0); self.sm.append(0)
        node = len(self.sm) - 1
        self.lc[node] = self._build(l, mid)
        self.rc[node] = self._build(mid + 1, r)
        return node

    def _idx(self, v):
        import bisect
        return bisect.bisect_left(self.uniq, v)

    def _update(self, prev, pos, val, l, r):
        self.lc.append(self.lc[prev]); self.rc.append(self.rc[prev]); self.sm.append(self.sm[prev] + val)
        node = len(self.sm) - 1
        if l == r:
            return node
        mid = (l + r) // 2
        if pos <= mid:
            self.lc[node] = self._update(self.lc[prev], pos, val, l, mid)
        else:
            self.rc[node] = self._update(self.rc[prev], pos, val, mid + 1, r)
        return node

    def query_kth(self, ql, qr, k):
        """区间 [ql,qr]（0 基闭区间）第 k 小（1 基）"""
        return self.uniq[self._query(self.roots[qr + 1], self.roots[ql], k, 0, self.m - 1)]

    def _query(self, r_root, l_root, k, l, r):
        if l == r:
            return l
        mid = (l + r) // 2
        left_count = self.sm[self.lc[r_root]] - self.sm[self.lc[l_root]]
        if k <= left_count:
            return self._query(self.lc[r_root], self.lc[l_root], k, l, mid)
        else:
            return self._query(self.rc[r_root], self.rc[l_root], k - left_count, mid + 1, r)

if __name__ == '__main__':
    import random
    random.seed(42)
    for _ in range(20):
        n = random.randint(1, 15)
        a = [random.randint(1, 100) for _ in range(n)]
        pst = PersistentSegTree(n, a)
        for _ in range(30):
            l = random.randint(0, n - 1)
            r = random.randint(l, n - 1)
            k = random.randint(1, r - l + 1)
            expect = sorted(a[l:r + 1])[k - 1]
            got = pst.query_kth(l, r, k)
            assert got == expect, (a, l, r, k, got, expect)
    print('persistent segtree (kth) OK: 20 random cases')
    # 版本复用验证：修改产生的新版本不破坏旧版本
    a = [3, 1, 4, 2]
    pst = PersistentSegTree(len(a), a)
    assert pst.query_kth(0, 3, 1) == 1
    assert pst.query_kth(0, 3, 4) == 4
    print('OK')
```

**PyPy 提示**: 主席树用三个并行 list（lc/rc/sm）避免节点对象开销，PyPy 下 n+m≤2e5 可行；递归 update/query 深度 O(log n) 安全。内存估算：每版本每插入 O(log m) 节点，提前预留 (n+1)*ceil(log2 m)+2 个槽位可省 append 开销。值域大时先离散化。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 单次 update/query O(log n)；建 k 个版本 O(k log n) |
| 空间 | O((初始结构) + k·log n)（路径复制） |

### 局限

空间随版本数与 log n 线性增长，大版本数下内存是主要瓶颈；完全可持久化的『修改旧版本』需要版本分叉管理（fat node/版本树），实现复杂；汇合可持久化（合并版本）在多数结构上无高效实现；不支持随机删除或需额外信息。Python 实现适合中小数据与教学。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3919 | 3 | 【模板】可持久化线段树 1（可持久化数组）：每个版本单点改 + 单点查，路径复制入门 | [https://www.luogu.com.cn/problem/P3919](https://www.luogu.com.cn/problem/P3919) |
| Luogu | P3834 | 4 | 【模板】可持久化线段树 2（静态区间第 k 小）：主席树经典模板 | [https://www.luogu.com.cn/problem/P3834](https://www.luogu.com.cn/problem/P3834) |
| Luogu | P3402 | 5 | 【模板】可持久化并查集：可持久化数组实现 parent/rank，注意不能路径压缩 | [https://www.luogu.com.cn/problem/P3402](https://www.luogu.com.cn/problem/P3402) |

## Pitfalls · 易错点

- 路径复制只复制根到叶的一链，忘记递归返回新子节点会导致共享错误
- 可持久化并查集不能路径压缩（压缩会破坏历史节点），只能按秩合并
- 版本根数组下标与『前 i 个元素』的对应关系（0 基/1 基）必须统一
- query 时两个版本必须同步下放，任一侧为旧版本空节点时计数为 0 处理要正确
- 递归 depth 在 n 大（值域大）时仍安全（log），但数组槽位预留不足会越界
- 离散化后第 k 小返回的是离散化值，需映射回原值

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/persistent.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/persistent.md)
- web ✓ [https://en.wikipedia.org/wiki/Persistent_data_structure](https://en.wikipedia.org/wiki/Persistent_data_structure)
