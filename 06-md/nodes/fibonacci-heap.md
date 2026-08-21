---
id: fibonacci-heap
name: 斐波那契堆
group: G-A-3
stage: advanced
priority: P3
depth_tier: brief
---

# 斐波那契堆

> 均摊O(1)decrease-key，理论最优堆，实现复杂

<!-- 元信息: id=fibonacci-heap · group=G-A-3 · stage=advanced · priority=P3 · depth_tier=brief -->

## What · 是什么

斐波那契堆（Fibonacci Heap）是支持合并（merge O(1)）、插入（O(1)）、取最小（O(1)）与理论最优的 decrease-key（均摊 O(1)）的堆结构，delete-min 均摊 O(log n)。它是一组满足堆性质的树的集合（森林），用『松弛二项堆』的结构：允许树非完全二项式，通过懒惰删除（把最小根从根表中提出、合并等操作推迟）和标记（mark）机制控制势能。decrease-key 均摊 O(1) 使 Dijkstra、Prim 等算法在理论上达到 O(V log V + E)（Dijkstra 配斐波那契堆为 O(E + V log V)）。但因常数巨大、实现复杂，实践几乎总是用配对堆或二叉堆。

## Why · 为什么

### 直觉 · Intuition

斐波那契堆把『快速插入/合并/减键』押在懒惰策略上：插入只是把节点放进根表，O(1)；decrease-key 只是把节点从父树上割下来放进根表，并给父打上『已失去一个儿子』的标记，O(1)。delete-min 才做整理：把最小根移除、儿子全部提升为根，再按度数合并同度数的根（consolidate），最后扫描找新最小，均摊 O(log n)。势能=根表中树的棵数 + 被标记节点的个数；只要每棵树度数与斐波那契数列相关，就能证明删除时根数受限。

### 原理 · Principle

① 节点域：val, degree, marked, parent, child（循环链）, left, right（循环链）；② insert/merge：直接链入根表，O(1)；③ decrease-key(x,v)：x 值变小，若违反堆性质则把 x 从父节点处割下（_cut）链入根表，并对父做级联割除（_cascading_cut：父若已标记则也被割下并递归），均摊 O(1)；④ delete-min：移除最小根，把它的所有儿子提升为根，然后 consolidate——用桶按 degree 合并同度树，使根表变为『每度一棵』，再从根表扫描最小，均摊 O(log n)。势能分析：φ = t（根表树数）+ 2·m（标记数），consolidate 中每合并一次 t 减 1 释放势能抵掉 O(1) 工作；级联割除每次释放标记能量。度数界依赖『丢失最多一个儿子』的 mark 规则，保证子树大小以斐波那契数增长。

### 历史 · History

Michael L. Fredman 与 Robert E. Tarjan 于 1987 年在 JACM 发表『Fibonacci heaps and their uses in improved network optimization algorithms』。decrease-key O(1) 使 Dijkstra O(E + V log V)、Prim O(E + V log V)、最小生成树（Fredman-Tarjan）显著提升。因常数大，实践中配对堆与二叉堆更常用；CLRS 第 19 章有完整实现与分析。

## How · 实现

### 伪代码

```python
insert(x): 新节点链入根表; 更新 min; O(1)
merge(H1,H2): 两个根表拼成环; 更新 min; O(1)
find_min(): return min
pop_min():
  r = min
  将 r 的所有儿子提升进根表 (parent=None)
  从根表摘除 r
  consolidate(): 按 degree 用桶合并同度树
  扫描根表取新 min
  return r.val
decrease_key(x, newv):
  x.val = newv
  if x.parent 非空 and x.val < x.parent.val:
    cut(x, x.parent)          # 割下 x 入根表
    cascading_cut(x.parent)   # 父若已标记则递归割
  if x.val < min.val: min = x
```

### Python 实现

```python
import heapq
import math
import random


class FibNode:
    __slots__ = ('val', 'degree', 'marked', 'parent', 'child', 'left', 'right')

    def __init__(self, val):
        self.val = val
        self.degree = 0
        self.marked = False
        self.parent = None
        self.child = None
        self.left = self.right = self   # 循环双向链表


class FibonacciHeap:
    """斐波那契堆（小根堆）。支持 insert/merge/取最小/pop_min/decrease-key，均摊复杂度。"""

    def __init__(self):
        self.min = None
        self.size = 0

    def insert(self, val):
        node = FibNode(val)
        self.size += 1
        if self.min is None:
            self.min = node
        else:
            self._root(node)
            if node.val < self.min.val:
                self.min = node
        return node

    def merge(self, other):
        if other.min is None:
            return self
        if self.min is None:
            return other
        a, b = self.min, other.min
        ar, br = a.right, b.right
        a.right, br.left = br, a
        b.right, ar.left = ar, b
        self.size += other.size
        if b.val < a.val:
            self.min = b
        return self

    def _root(self, node):
        m = self.min
        node.left, node.right = m, m.right
        m.right.left, m.right = node, node

    def pop_min(self):
        if self.min is None:
            return None
        r = self.min
        # 收集根表中其余根
        roots = []
        x = r.right
        while x is not r:
            roots.append(x)
            x = x.right
        # 收集 r 的所有儿子并提升为根
        kids = []
        child = r.child
        if child is not None:
            first, c = child, child
            while True:
                kids.append(c)
                c.parent = None
                c.marked = False
                nxt = c.right
                c.right = c.left = c
                c = nxt
                if c is first:
                    break
        self.size -= 1
        if not roots and not kids:
            self.min = None
            return r.val
        alln = roots + kids
        for i in range(len(alln)):
            alln[i].left = alln[(i - 1) % len(alln)]
            alln[i].right = alln[(i + 1) % len(alln)]
        self.min = min(alln, key=lambda nd: nd.val)
        self._consolidate()
        return r.val

    def _consolidate(self):
        cap = int(math.log(max(self.size, 2), 1.618)) + 2
        buckets = [None] * (cap + 1)
        nodes = []
        start = self.min
        x = start
        while True:
            nodes.append(x)
            x = x.right
            if x is start:
                break
        for w in nodes:
            x = w
            d = x.degree
            while buckets[d] is not None:
                y = buckets[d]
                if x.val > y.val:
                    x, y = y, x
                self._absorb(y, x)
                buckets[d] = None
                d += 1
            buckets[d] = x
        self.min = None
        for b in buckets:
            if b is None:
                continue
            if self.min is None:
                self.min = b
            elif b.val < self.min.val:
                self.min = b

    def _absorb(self, y, x):
        """把根 y 合并为 x 的儿子"""
        y.left.right = y.right
        y.right.left = y.left
        y.parent = x
        if x.child is None:
            x.child = y
            y.left = y.right = y
        else:
            c = x.child
            y.left, y.right = c, c.right
            c.right.left, c.right = y, y
        x.degree += 1
        y.marked = False

    def decrease_key(self, node, new_val):
        if new_val > node.val:
            raise ValueError('decrease-key 只能减小')
        node.val = new_val
        p = node.parent
        if p is not None and node.val < p.val:
            self._cut(node, p)
            self._cascading_cut(p)
        if node.val < self.min.val:
            self.min = node

    def _cut(self, node, parent):
        if node.right is node:
            parent.child = None
        else:
            node.left.right = node.right
            node.right.left = node.left
            if parent.child is node:
                parent.child = node.right
        parent.degree -= 1
        node.parent = None
        node.marked = False
        self._root(node)

    def _cascading_cut(self, node):
        p = node.parent
        if p is None:
            return
        if not node.marked:
            node.marked = True
        else:
            self._cut(node, p)
            self._cascading_cut(p)


if __name__ == '__main__':
    from collections import Counter
    random.seed(31)
    for trial in range(10):
        fh = FibonacciHeap()
        ref = Counter()
        nodes = []
        active = set()
        for step in range(3000):
            op = random.random()
            if sum(ref.values()) == 0 or op < 0.5:
                v = random.randint(0, 1000000)
                nd = fh.insert(v)
                ref[v] += 1
                nodes.append(nd)
                active.add(id(nd))
            elif op < 0.6 and len(active) > 0:
                cands = [nd for nd in nodes if id(nd) in active]
                nd = random.choice(cands)
                old = nd.val
                nv = old - random.randint(0, min(old, 10000))
                fh.decrease_key(nd, nv)
                ref[old] -= 1
                if ref[old] == 0:
                    del ref[old]
                ref[nv] += 1
            else:
                exp = min(ref)
                got = fh.pop_min()
                assert got == exp, (trial, step, got, exp)
                ref[exp] -= 1
                if ref[exp] == 0:
                    del ref[exp]
                for nd in nodes:
                    if id(nd) in active and nd.val == got:
                        active.discard(id(nd))
                        break
    # merge 验证
    f1, f2 = FibonacciHeap(), FibonacciHeap()
    r1, r2 = [], []
    for v in [3, 1, 4]:
        f1.insert(v); r1.append(v)
    for v in [2, 5, 0]:
        f2.insert(v); r2.append(v)
    f1.merge(f2)
    r = sorted(r1 + r2)
    out = []
    while f1.min is not None:
        out.append(f1.pop_min())
    assert out == r, (out, r)
    print('fibonacci heap: All tests passed.')
```

**PyPy 提示**: Python 实现斐波那契堆常数极大，竞赛基本不用（直接用二叉堆 heapq 或配对堆）。仅用于理解理论与 Dijkstra 最优复杂度证明。若必须用，用数组模拟节点（val/degree/marked/parent/child/lr 多列表）并避免对象属性访问开销。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | insert/find-min/merge/decrease-key 均摊 O(1)；delete-min 均摊 O(log n)；全部均摊 |
| 空间 | O(n) 节点；无额外辅助空间 |

### 局限

实现复杂、常数巨大，OI/ICPC 实践中几乎从不使用（配对堆是更好的实践替代）。所有复杂度是均摊的，不可持久化。mark 规则（每个节点最多失去一个儿子）是正确性的关键，漏写会导致势能分析失效、复杂退化。Python 中 heapq 的 C 实现常数小到让斐波那契堆在一切规模下都显得多余。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P4779 | 3 | 【模板】单源最短路径：Dijkstra 标准模板（用斐波那契堆可达理论 O(E+V log V)，实践中 heapq 足够） | [https://www.luogu.com.cn/problem/P4779](https://www.luogu.com.cn/problem/P4779) |
| Luogu | P3366 | 3 | 【模板】最小生成树：Prim+decrease-key 场景（斐波那契堆理论最优，Kruskal 通常更省心） | [https://www.luogu.com.cn/problem/P3366](https://www.luogu.com.cn/problem/P3366) |

## Pitfalls · 易错点

- decrease-key 是斐波那契堆的价值所在，若题面只要 insert/pop_min，二叉堆更快
- mark 标记与级联割除逻辑错误会导致度数势能分析失败、复杂度退化为 O(n)
- consolidate 的桶容量要足够（按 φ 对数估计），数组越界在 Python 直接 IndexError
- 删除最小根后儿子全部提升为根，此时要重新扫描最小，别漏了 min 指针更新
- 循环双向链表的链接顺序极易写错（merge/absorb/cut 都是指针体操）
- 均摊数据结构不可持久化；Python 的 __slots__ 虽省内存但调试指针更痛苦

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/heap/](https://oi-wiki.org/ds/heap/)
- CP-Algorithms ✓ [https://cp-algorithms.com/data_structures/randomized_heap.html](https://cp-algorithms.com/data_structures/randomized_heap.html)
- 书籍 ✓ `CLRS ch19 Fibonacci Heaps; Fredman & Tarjan 1987`
- 书籍 ✓ `CPH ch10 Dijkstra (uses heap, notes fib heap)`
