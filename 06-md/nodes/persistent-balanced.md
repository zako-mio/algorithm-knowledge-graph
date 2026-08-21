---
id: persistent-balanced
name: 可持久化平衡树
group: G-D-5
stage: advanced
priority: P2
depth_tier: standard
---

# 可持久化平衡树

> 可持久化无旋转Treap，函数式节点复用实现历史版本

<!-- 元信息: id=persistent-balanced · group=G-D-5 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

可持久化平衡树在 OI 中最常用的是可持久化无旋转 Treap（FHQ Treap）：利用其 Split/Merge 过程只修改路径上节点、且天然适合『复制沿途节点（path copying）』的特点，把每个操作（插入/删除/查询）都作用在某个历史版本上并产生新版本。因无旋转、无指针改动旧版本，Split/Merge 中每次新建节点即可保留全部历史。支持任意历史版本的插入/删除/求排名/求 k 小/前驱/后继。经典模板：Luogu P3835（可持久化平衡树）、P3919（可持久化数组）、P5055（可持久化文艺平衡树）。

## Why · 为什么

### 直觉 · Intuition

旋转 Treap（Splay/Treap）会物理改写树的形状，想持久化要复制大量受旋转影响的节点；而无旋转 FHQ Treap 的 merge/split 是『自顶向下』的，一次只沿一条路径走。仿照主席树的 path copying：split 过程中每经过一个节点就新建它的副本（拷贝 val/prio/左右儿子），再把修改后的儿子挂到副本上，旧版本节点分毫不动。于是每个版本就是一组节点引用，历史天然保留。

### 原理 · Principle

① FHQ Treap：节点存 val（键）、prio（随机优先级）、size；核心 split(x,k) 按键 k 把树裂成 <k 与 ≥k 两棵，merge(a,b) 按 prio 合并（prio 小的在上）；② 可持久化要点：split/merge 中每个『修改到』的节点都新建副本——split(x,k) 返回 (a,b) 且 a/b 中的路径节点全部是新建的；merge 同理，被改变儿子指针的节点要复制；③ 插入 = split → 新建单点 → merge；删除 = split → split → 抛弃要删的 → merge；排名/前驱/后继 = 沿树走（不修改无需复制）；④ 每个操作产生新根（append 到根数组），历史版本独立查询。空间 O(m log n)，时间 O(m log n)。

### 历史 · History

无旋转 Treap（FHQ Treap）由范浩强（2006 年冬令营论文《范浩强谈数据结构》）提出并在 OI 中普及，其『split/merge 自顶向下』特性天然适配可持久化。可持久化平衡树（特别是无旋 Treap 版本）成为 OI 处理历史版本有序集合的标配，OI Wiki 与洛谷模板 P3835 将其标准化。

## How · 实现

### 伪代码

```python
split(x, k):            # 返回 (<k 的树, >=k 的树)；路径节点全部新建
  if x 为空: return (0, 0)
  nw = 复制节点 x
  if val[x] < k:
    a, b = split(r[x], k)
    r[nw] = a; pull(nw); return (nw, b)
  else:
    a, b = split(l[x], k)
    l[nw] = b; pull(nw); return (a, nw)
merge(a, b):             # 按 prio 合并；被改儿子指针的节点要复制
  if a 空: return b
  if b 空: return a
  if prio[a] < prio[b]: nw=复制a; r[nw]=merge(r[a], b); pull(nw); return nw
  else:                  nw=复制b; l[nw]=merge(a, l[b]); pull(nw); return nw
insert(ver, k): a,b=split(root[ver],k); return merge(merge(a,newnode(k)),b)
erase(ver, k):  a,b=split(root[ver],k); c,d=split(b,k+1); return merge(a,merge(l[c],d))
```

### Python 实现

```python
import random


class PersistentTreap:
    """可持久化无旋转 Treap（FHQ）。支持基于任意历史版本做插入/删除/排名/k小/前驱/后继。
    所有数组 0 号均为空节点哨兵。ver 从 0 开始（空树）。"""

    def __init__(self):
        self.l = [0]; self.r = [0]; self.key = [0]
        self.prio = [0]; self.size = [0]
        self.vers = [0]

    def _newnode(self, k):
        idx = len(self.key)
        self.l.append(0); self.r.append(0); self.key.append(k)
        self.prio.append(random.random()); self.size.append(1)
        return idx

    def _pull(self, x):
        self.size[x] = self.size[self.l[x]] + self.size[self.r[x]] + 1

    def _split(self, x, k):
        """返回 (a, b): a 的键全部 < k, b 的键全部 >= k。路径节点新建。"""
        if x == 0:
            return 0, 0
        if self.key[x] < k:
            a, b = self._split(self.r[x], k)
            nw = self._newnode(self.key[x])
            self.l[nw] = self.l[x]; self.r[nw] = a
            self._pull(nw)
            return nw, b
        else:
            a, b = self._split(self.l[x], k)
            nw = self._newnode(self.key[x])
            self.l[nw] = b; self.r[nw] = self.r[x]
            self._pull(nw)
            return a, nw

    def _merge(self, a, b):
        if a == 0:
            return b
        if b == 0:
            return a
        if self.prio[a] < self.prio[b]:
            nw = self._newnode(self.key[a])
            self.l[nw] = self.l[a]; self.r[nw] = self._merge(self.r[a], b)
            self._pull(nw)
            return nw
        else:
            nw = self._newnode(self.key[b])
            self.r[nw] = self.r[b]; self.l[nw] = self._merge(a, self.l[b])
            self._pull(nw)
            return nw

    def insert(self, ver, k):
        a, b = self._split(self.vers[ver], k)
        root = self._merge(self._merge(a, self._newnode(k)), b)
        self.vers.append(root)
        return root

    def erase(self, ver, k):
        a, b = self._split(self.vers[ver], k)
        c, d = self._split(b, k + 1)
        if c:
            c = self._merge(self.l[c], self.r[c])
        root = self._merge(a, self._merge(c, d))
        self.vers.append(root)
        return root

    def rank(self, ver, k):
        """返回 < k 的元素个数 + 1"""
        x = self.vers[ver]; r = 0
        while x:
            if self.key[x] < k:
                r += self.size[self.l[x]] + 1
                x = self.r[x]
            else:
                x = self.l[x]
        return r + 1

    def kth(self, ver, k):
        x = self.vers[ver]
        while True:
            lsz = self.size[self.l[x]]
            if k <= lsz:
                x = self.l[x]
            elif k == lsz + 1:
                return self.key[x]
            else:
                k -= lsz + 1
                x = self.r[x]

    def pred(self, ver, k):
        r = self.rank(ver, k)
        return self.kth(ver, r - 1) if r >= 2 else None

    def succ(self, ver, k):
        r = self.rank(ver, k + 1)
        return self.kth(ver, r) if r <= self.size[self.vers[ver]] else None


if __name__ == '__main__':
    random.seed(23)
    pt = PersistentTreap()
    hist = [[]]  # hist[v] = 第 v 个版本的已排序元素列表（暴力参照）
    for step in range(300):
        cur = hist[-1]
        if not cur or random.random() < 0.6:
            k = random.randint(1, 15)
            pt.insert(len(hist) - 1, k)
            nv = sorted(cur + [k])
        else:
            k = random.choice(cur)
            pt.erase(len(hist) - 1, k)
            nv = list(cur); nv.remove(k)
        hist.append(nv)
    # 验证所有历史版本均正确且互不影响
    for vv in range(len(hist)):
        lst = hist[vv]
        for k in range(1, 16):
            assert pt.rank(vv, k) == 1 + sum(1 for x in lst if x < k), (vv, k)
        for idx in range(1, len(lst) + 1):
            assert pt.kth(vv, idx) == lst[idx - 1], (vv, idx)
        # 前驱=小于 k 的最大值；后继=大于 k 的最小值（严格）
        for k in range(1, 16):
            smallers = [x for x in lst if x < k]
            assert pt.pred(vv, k) == (smallers[-1] if smallers else None), (vv, k)
            biggers = [x for x in lst if x > k]
            assert pt.succ(vv, k) == (biggers[0] if biggers else None), (vv, k)
    print('persistent-balanced: All tests passed.')
```

**PyPy 提示**: 全部用数组（l/r/key/prio/size 五列 + vers 根数组）实现，PyPy 下 2e5 次操作可过。随机优先级用 random.random()（Python 自带）即可；可改用随机整数减少浮点比较。注意版本号=操作次数，需保证每次操作 append 一个根。查询操作（rank/kth/pred/succ）不建新版本（P3835 语义下查询不产生新版本）。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 插入/删除/排名/kth/前驱/后继均 O(log n)（split/merge 深度期望 log n） |
| 空间 | O(m log n) 节点（m 为操作次数；split 每次新建 O(log n)、merge 同） |

### 局限

随机化期望复杂度（prio 用真随机），最坏概率退化可忽略。每个操作都会新建 O(log n) 节点，m 大时空间压力明显（m=1e6 约 2e7 节点）。查询类操作不产生新版本——若题面要求『查询也算新版本』（如 P5055 文艺平衡树翻转）需按语义处理。区间操作（翻转/合并）需文艺平衡树版 split by size。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3835 | 5 | 【模板】可持久化平衡树：基于历史版本插入/删除/排名/k小/前驱/后继，最标准模板，OI Wiki 例题 | [https://www.luogu.com.cn/problem/P3835](https://www.luogu.com.cn/problem/P3835) |
| Luogu | P3919 | 3 | 【模板】可持久化线段树1（可持久化数组）：可持久化入门，理解版本与 path copying | [https://www.luogu.com.cn/problem/P3919](https://www.luogu.com.cn/problem/P3919) |
| Luogu | P5055 | 6 | 可持久化文艺平衡树：按 size split 的可持久化 FHQ，支持历史版本区间翻转，OI Wiki 练手题 | [https://www.luogu.com.cn/problem/P5055](https://www.luogu.com.cn/problem/P5055) |
| Codeforces | 702F | 6 | T-shirt：可持久化平衡树/线段树分治优化 DP，OI Wiki 练手题 | [https://codeforces.com/problemset/problem/702/F](https://codeforces.com/problemset/problem/702/F) |

## Pitfalls · 易错点

- split/merge 中必须『先复制节点再修改』，直接改原节点会破坏旧版本
- 复制节点时左右儿子指针要带过来（拷贝旧值），漏拷贝导致新版本缺子树
- 版本索引：insert/erase 各产生一个新版本（append 一次根），查询不 append；P3835 的版本编号=操作序号
- merge 后要 pull(size) 更新，遗忘会破坏 kth/rank
- delete 语义：split(b,k+1) 取恰等于 k 的中段，多键时只删一个；写成 split by k 边界错
- prio 比较方向与 merge 分支写反会破坏堆性质（小根堆 prio 在上）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/persistent-balanced/](https://oi-wiki.org/ds/persistent-balanced/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/persistent-balanced.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/persistent-balanced.md)
- 书籍 ✓ `范浩强《范浩强谈数据结构》（无旋 Treap）`
