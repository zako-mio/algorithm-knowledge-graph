---
id: pairing-heap
name: 配对堆
group: G-A-3
stage: advanced
priority: P2
depth_tier: standard
---

# 配对堆

> 均摊O(1)插入/O(log n)删除，Fibonacci堆的简单替代

<!-- 元信息: id=pairing-heap · group=G-A-3 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

配对堆（Pairing Heap）是一种基于势能分析的可并堆：一棵满足堆性质的多叉树，用『儿子-兄弟』表示法存储。它只维护堆性质，不维护树的任何大小/深度/排名额外信息，因此结构极其简单灵活。所有操作归约为两个：meld（合并两个堆，O(1)：小根做根、大根挂为第一个儿子）与 delete-min（删除根后把儿子们先两两配对合并、再从右往左依次合并，均摊 O(log n)）。它还支持 O(log n) 均摊的 decrease-key（把节点从父链上割下来再与根合并）。是 Fibonacci 堆的实践替代品：实现简单、常数小、平均性能优秀，但因为是均摊复杂度，无法持久化。

## Why · 为什么

### 直觉 · Intuition

合并只需把大根挂成小根的儿子，O(1)。难点在删除最小值：根没了，儿子们散成森林，必须按特定顺序合并回去。若从左到右逐个合并会退化 O(n)——因为合并越往后树越深。『两步走』：先把儿子两两配对合并（树的形状变矮），再从右往左合并，这样每次 delete-min 的均摊代价是对数的。

### 原理 · Principle

① 儿子-兄弟表示：每个节点存第一个儿子 child 和下一个兄弟 sibling；② meld(x,y)：小根做根，大根 y 插到 x 儿子链头（y.sibling = x.child; x.child = y），O(1)；③ delete-min：取出根，对其儿子链调用 merges——两两一组 meld 配对，然后新产生的堆从右往左挨个 meld；④ decrease-key(x,v)：把 x 从父的儿子链中剖出（更新父的 child/sibling），与根 meld。均摊复杂度由势能分析保证：Iacono 证明 meld O(1)、decrease-key O(log n)；Pettie 给出 O(2^(2√(log log n))) 的上界，delete-min 均摊 O(log n)。与斐波那契堆不同，它不维护 mark/degree 等额外信息。

### 历史 · History

1986 年 Fredman、Sedgewick、Sleator、Tarjan 在论文『The pairing heap: a new form of self-adjusting heap』中提出，受 Splay 树『自调整』思想启发，试图作为斐波那契堆（1987，更早发表）的简单替代。后来证明其某些操作无法达到斐波那契堆的全部均摊界（decrease-key 下界 Ω(log log n)），但实践速度极快，被广泛用于需要 merge 的场景。

## How · 实现

### 伪代码

```python
meld(x, y):
  if x 为空: return y
  if y 为空: return x
  if val(x) > val(y): swap(x, y)
  y.sibling = x.child   # 大根挂为小根的第一个儿子
  x.child = y
  return x
insert(root, v) = meld(root, new_node(v))
find_min(root)  = root.val
merges(first):  # 合并一个儿子的兄弟链
  if first 为空 or first.sibling 为空: return first
  y = first.sibling; c = y.sibling
  first.sibling = y.sibling = None
  return meld(merges(c), meld(first, y))
delete_min(root) = (merges(root.child), root.val)
```

### Python 实现

```python
import heapq
import random


class Node:
    __slots__ = ('val', 'ch', 'sib')

    def __init__(self, val):
        self.val = val
        self.ch = None
        self.sib = None


def meld(a, b):
    """合并两个配对堆，返回新根。O(1) 均摊"""
    if a is None:
        return b
    if b is None:
        return a
    if a.val > b.val:
        a, b = b, a
    b.sib = a.ch
    a.ch = b
    return a


def insert(root, val):
    return meld(root, Node(val))


def _pairs(first):
    """两两配对合并儿子链，再自右向左合并（删除最小值核心）"""
    if first is None or first.sib is None:
        return first
    a, b = first, first.sib
    rest = b.sib
    a.sib = b.sib = None
    return meld(_pairs(rest), meld(a, b))


def pop_min(root):
    """删除最小值。返回 (新根, 原最小值)；空堆返回 (None, None)"""
    if root is None:
        return None, None
    return _pairs(root.ch), root.val


def decrease_key(root, node, new_val):
    """把 node 的值减小为 new_val（须保证 new_val <= node.val）"""
    if new_val > node.val:
        raise ValueError('decrease_key 只能减小')
    node.val = new_val
    # 若 node 是根则直接返回
    # 本实现为无父指针的简化版：此处仅演示；完整实现需 fa 指针把 node 从父链剖出后 meld(root, node)
    return root


if __name__ == '__main__':
    random.seed(2)
    h = None
    ref = []
    for _ in range(5000):
        op = random.random()
        if op < 0.5 or not ref:
            v = random.randint(0, 100000)
            h = insert(h, v)
            heapq.heappush(ref, v)
        else:
            h, m = pop_min(h)
            r = heapq.heappop(ref)
            assert m == r, (m, r)
        if h is None:
            assert not ref
    # 双堆合并验证
    h1 = h2 = None
    r1, r2 = [], []
    for v in [9, 3, 7, 1, 5]:
        h1 = insert(h1, v); r1.append(v)
    for v in [8, 2, 6, 0, 4]:
        h2 = insert(h2, v); r2.append(v)
    h = meld(h1, h2)
    r = sorted(r1 + r2)
    out = []
    while h is not None:
        h, m = pop_min(h)
        out.append(m)
    assert out == r, (out, r)
    print('pairing heap: All tests passed.')
```

**PyPy 提示**: 实现极简，常数小，PyPy 下 5e5-1e6 规模可过。decrease-key 需维护父指针（区分该节点是父的 child 还是 sibling 两种剖出情况）。均摊复杂度无法持久化（见限制）。儿子链用单链表即可，两两配对注意先存 rest 再拆边。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | insert/find-min/meld 均摊 O(1)；delete-min 均摊 O(log n)；decrease-key 均摊 O(log n)（上界 O(2^(2√(log log n)))） |
| 空间 | O(n) 节点；无额外辅助信息 |

### 局限

所有复杂度均为均摊（势能分析），因此无法持久化。decrease-key 的均摊下界 Ω(log log n)，达不到斐波那契堆的 O(1)。不同操作的均摊界不能简单取各最优。若不维护父指针则 decrease-key 需先知道节点位置（如 Dijkstra 中在入堆时记录）。OI 竞赛中大多数『只需 merge+insert+pop_min』的场景用左偏树更稳（非均摊），配对堆更适合常数敏感的场合。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3378 | 2 | 【模板】堆：基础堆操作模板，可用配对堆实现（插入/取最小/删最小） | [https://www.luogu.com.cn/problem/P3378](https://www.luogu.com.cn/problem/P3378) |
| AtCoder | abc138_f | 3 | Coordinate-like 堆应用练习：配对堆适合快速合并场景的入门 | [https://atcoder.jp/contests/abc138/tasks/abc138_f](https://atcoder.jp/contests/abc138/tasks/abc138_f) |

## Pitfalls · 易错点

- delete-min 若直接从左到右合并儿子会退化成 O(n)，必须『两两配对 + 从右往左』
- 儿子链表按插入时间排序：最左是最新儿子；删最小前的配对顺序写错会破坏均摊界
- decrease-key 剖出节点时需区分该节点是父节点的 child 还是 sibling，漏判会断链
- 均摊结构不支持持久化，误用持久化思路会得到错误复杂度
- _pairs 递归在儿子链长时深度 O(n)（但配对后每层减半），需注意 Python 递归深度
- meld 后 min 指针（若有缓存）需更新，否则 find_min 返回旧值

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/pairing-heap/](https://oi-wiki.org/ds/pairing-heap/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/pairing-heap.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/pairing-heap.md)
- OI Wiki ✓ [https://oi-wiki.org/ds/heap/](https://oi-wiki.org/ds/heap/)
- 书籍 ✓ `Fredman, Sedgewick, Sleator, Tarjan, The pairing heap: a new form of self-adjusting heap, 1986`
