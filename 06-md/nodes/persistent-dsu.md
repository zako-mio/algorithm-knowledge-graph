---
id: persistent-dsu
name: 可持久化并查集
group: G-A-4
stage: advanced
priority: P2
depth_tier: standard
---

# 可持久化并查集

> 用主席树（可持久化数组）存 fa/秩，支持历史版本回溯的并查集，O(log n)/操作

<!-- 元信息: id=persistent-dsu · group=G-A-4 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

可持久化并查集解决『并查集带回滚/历史版本查询』问题（如离线可撤销并查集、二分答案需要回到中间版本）。核心思路：用可持久化线段树（主席树）实现一个支持历史版本单点修改/查询的『可持久化数组』，fa[] 与 size[]（或秩）各用一棵主席树维护。因为路径压缩会修改大量节点导致版本复制开销巨大，所以可持久化并查集【只用启发式合并（按大小/秩），不做路径压缩】，每次操作 O(log n) 修改两个点（fa 一个点、size 一个点）。每个版本对应一组 (fa_ver, size_ver)；操作 2 直接令当前版本指向历史版本（O(1) 回退）。空间 O((n+m) log n)。

## Why · 为什么

### 直觉 · Intuition

普通并查集的数组每改一次就整体拷贝一份，太贵；但每次 merge 只改两个下标。主席树恰好‘共享没改的节点、只新建改动的 O(log n) 个路径节点’，让每个版本只多花 O(log n) 空间。回退就是把『当前指针』指回历史版本，连拷贝都不用。

### 原理 · Principle

① 建一棵值域 [1,n] 的主席树，叶子存 fa[i]=i；另一棵存 size（秩）。② find(x)：在当前版本树上反复查询 fa，沿树向上跳（不做路径压缩，深度由启发式合并保证 O(log n)）。③ union(a,b)：find 两棵，若同根则新版本直接复制当前版本；否则把 size 小的根挂到大根下，用主席树 modify 改一个 fa 叶子（O(log n) 新建路径节点）并改大根的 size。④ 回退到版本 k：roots[k] 直接复用。空间每个操作至多 O(log n) 新节点，总 O((n+m) log n)。正确性：启发式合并保证高度 O(log n)（无路径压缩），因此 find 是 O(log^2 n)（外层深度 log n，内层树查询 log n），可接受。

### 历史 · History

可持久化数据结构概念源于 1980 年代（Driscoll 等），主席树（可持久化线段树）由黄嘉泰（HJT）引入中国 OI 圈。OI Wiki 在《可持久化线段树》页『拓展：基于主席树的可持久化并查集』给出完整实现，并强调此时必须只用启发式合并。经典题 Luogu P3402『可持久化并查集』。

## How · 实现

### 伪代码

```python
class PersistSeg:  # 可持久化数组
  roots = [build([1..n])]   # 版本 0
  def get(ver, pos): query(roots[ver], 1, n, pos)
  def set(ver, pos, val):   # 返回新版本号
    newroot = modify(roots[ver], 1, n, pos, val)
    roots.append(newroot); return len(roots)-1

class PersistDSU:
  fa = PersistSeg(); sz = PersistSeg()
  vers = [(0,0)]            # (fa_ver, sz_ver)
  def find(x):
    while True:
      p = fa.get(vers[-1][0], x)
      if p == x: return x
      x = p
  def union(a, b):
    ra, rb = find(a), find(b)
    if ra == rb: vers.append(vers[-1]); return
    if sz.get(...ra) < sz.get(...rb): swap(ra, rb)
    v1 = fa.set(vers[-1][0], rb, ra)
    v2 = sz.set(vers[-1][1], ra, sz.get(...ra)+sz.get(...rb))
    vers.append((v1, v2))
  def rollback(k): vers.append(vers[k])  # O(1) 回退
```

### Python 实现

```python
class PersistSeg:
    """可持久化数组(主席树式): 支持对历史版本 O(log n) 单点查询/修改, 返回新版本根."""
    def __init__(self, n, init_list):
        self.n = n
        self.lc = [0]
        self.rc = [0]
        self.val = [0]
        # 初始版本 root=1
        self.roots = [self._build(1, n, init_list)]

    def _build(self, l, r, arr):
        p = len(self.val); self.val.append(0); self.lc.append(0); self.rc.append(0)
        if l == r:
            self.val[p] = arr[l - 1]
            return p
        m = (l + r) // 2
        self.lc[p] = self._build(l, m, arr)
        self.rc[p] = self._build(m + 1, r, arr)
        return p

    def _clone(self, p):
        self.lc.append(self.lc[p]); self.rc.append(self.rc[p]); self.val.append(self.val[p])
        return len(self.val) - 1

    def _query(self, p, l, r, pos):
        if l == r: return self.val[p]
        m = (l + r) // 2
        if pos <= m: return self._query(self.lc[p], l, m, pos)
        return self._query(self.rc[p], m + 1, r, pos)

    def _modify(self, p, l, r, pos, newval):
        q = self._clone(p)
        if l == r:
            self.val[q] = newval
            return q
        m = (l + r) // 2
        if pos <= m: self.lc[q] = self._modify(self.lc[p], l, m, pos, newval)
        else:       self.rc[q] = self._modify(self.rc[p], m + 1, r, pos, newval)
        return q

    def get(self, ver, pos): return self._query(self.roots[ver], 1, self.n, pos)
    def set(self, ver, pos, newval):
        newroot = self._modify(self.roots[ver], 1, self.n, pos, newval)
        self.roots.append(newroot)
        return len(self.roots) - 1


class PersistDSU:
    """可持久化并查集: 基于主席树(可持久化数组)存 fa 与 size(秩), 只按秩合并, 不做路径压缩.
    支持在历史版本上进行 union / 回退(回到任意历史版本), 查询连通性."""
    def __init__(self, n):
        self.n = n
        fa = list(range(1, n + 1))          # 1-indexed
        sz = [1] * (n + 1)                  # 秩/大小
        self.fa = PersistSeg(n, fa)
        self.sz = PersistSeg(n, sz)
        self.roots = [(0, 0)]               # (fa_ver, sz_ver) 时间轴

    def _find(self, x):
        ver, _ = self.roots[-1]
        while True:
            p = self.fa.get(ver, x)
            if p == x: return x
            x = p

    def _find_on(self, ver_fa, x):
        while True:
            p = self.fa.get(ver_fa, x)
            if p == x: return x
            x = p

    def find(self, x):
        return self._find(x)

    def union(self, a, b):
        ver_fa, ver_sz = self.roots[-1]
        ra, rb = self._find_on(ver_fa, a), self._find_on(ver_fa, b)
        if ra == rb:
            # 无变化, 复制当前版本
            self.roots.append((ver_fa, ver_sz))
            return False
        sa, sb = self.sz.get(ver_sz, ra), self.sz.get(ver_sz, rb)
        if sa < sb: ra, rb = rb, ra
        # rb 挂到 ra
        v1 = self.fa.set(ver_fa, rb, ra)
        v2 = self.sz.set(ver_sz, ra, sa + sb)
        self.roots.append((v1, v2))
        return True

    def rollback(self, version):
        self.roots.append(self.roots[version])
        return version

    def connected(self, a, b):
        return self.find(a) == self.find(b)

    def version_count(self):
        return len(self.roots) - 1


if __name__ == "__main__":
    import random
    random.seed(2024)
    n = 50
    pd = PersistDSU(n)
    naive = list(range(n + 1))
    def nfind(x):
        while naive[x] != x:
            naive[x] = naive[naive[x]]
            x = naive[x]
        return x
    ver_ops = [[]]           # 每个 pd 版本对应的存活 union 操作
    for t in range(300):
        op = random.random()
        if op < 0.5:
            a, b = random.randint(1, n), random.randint(1, n)
            r1 = pd.union(a, b)
            r2 = (nfind(a) != nfind(b))
            uops = ver_ops[-1][:]
            if r2: uops.append((a, b))
            ver_ops.append(uops)
            assert r1 == r2, (t, a, b)
            if r2: naive[nfind(a)] = nfind(b)
        elif op < 0.6:
            v = random.randint(0, pd.version_count())
            pd.rollback(v)
            naive = list(range(n + 1))
            for a, b in ver_ops[v]:
                ra, rb = nfind(a), nfind(b)
                if ra != rb: naive[ra] = rb
            ver_ops.append(ver_ops[v][:])
        else:
            a, b = random.randint(1, n), random.randint(1, n)
            assert pd.connected(a, b) == (nfind(a) == nfind(b)), (t, a, b)
    print("persistent-dsu: all tests passed")

```

**PyPy 提示**: 递归实现主席树节点克隆/修改时，函数调用次数 O(log n)×操作数，PyPy 下递归深 ~log n 没问题；但每次 modify 都深拷贝 lc/rc/val 三个 list 节点，建议用数组模拟节点池（self.lc/rc/val 三个 list 并行扩容）避免大量对象开销。回退用数组下标 O(1)。PyPy 下大数据建议将 find 写成迭代 while 而非递归。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | find/union 每操作 O(log^2 n)（深度 O(log n) × 树查询 O(log n)）；回退 O(1) |
| 空间 | O((n+m) log n) 节点 |

### 局限

① 不能路径压缩（会一次性修改过多点，破坏可持久化摊销），因此常数比普通并查集大很多；② 空间大，n,m 达 1e5 时节点约 (n+m)·20 个；③ find 是 log^2，若要 O(log) 可改用可持久化平衡树/二元提升但实现复杂；④ 只支持版本回溯，不适用于需要当前时刻动态删除的在线场景（那用线段树分治）。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3402 | 4 | 可持久化并查集模板：合并/回退到历史版本/查询连通性三操作 | [https://www.luogu.com.cn/problem/P3402](https://www.luogu.com.cn/problem/P3402) |
| Library Checker | Persistent Unionfind | 4 | Library Checker 可持久化并查集模板题 | [https://judge.yosupo.jp/problem/persistent_unionfind](https://judge.yosupo.jp/problem/persistent_unionfind) |

## Pitfalls · 易错点

- 忘了去路径压缩——这是最隐蔽的错误，加了路径压缩的‘可持久化’并查集不正确
- modify 要克隆整个路径节点再改，不能就地改共享节点（会污染其他版本）
- 合并时 size/秩 的更新位置（大根的 size 才累加）写错
- 回退后继续合并是基于回退后的版本，勿沿用旧 fa 版本号
- 数组版本号与‘操作数’对应错位（rollback 也产生新版本），测试要按版本号索引
- 递归 find 与递归 modify 混用时节点下标越界（节点池不足）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/persistent-seg/#拓展基于主席树的可持久化并查集](https://oi-wiki.org/ds/persistent-seg/#拓展基于主席树的可持久化并查集)
- OI Wiki ✓ [https://oi-wiki.org/ds/dsu/](https://oi-wiki.org/ds/dsu/)
- 书籍 ✓ `CPH ch14.2? (可持久化) —— 见 OI Wiki persistent-seg 参考`
