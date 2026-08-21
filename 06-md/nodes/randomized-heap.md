---
id: randomized-heap
name: 随机化堆
group: G-A-3
stage: intermediate
priority: P3
depth_tier: brief
---

# 随机化堆

> 随机合并的可并堆，期望O(log n)

<!-- 元信息: id=randomized-heap · group=G-A-3 · stage=intermediate · priority=P3 · depth_tier=brief -->

## What · 是什么

随机化堆（Randomized Heap）是一种极简的可并堆：满足堆性质的二叉树，合并时随机选择把另一个堆挂到当前根的左儿子还是右儿子。所有操作（插入、取最小、删最小、合并、删任意元素）都归约为 merge，期望 O(log n)。它不维护任何额外信息（无 dist/rank/势能），代码只有十几行，是竞赛手写可并堆时的最快选择之一。缺点是复杂度依赖随机化（期望保证而非最坏保证），且合并会随机破坏树的平衡。

## Why · 为什么

### 直觉 · Intuition

左偏树保证 O(log n) 靠维护 dist 约束；配对堆靠精心设计的合并顺序；随机化堆则把平衡问题交给概率：合并时随机决定递归进哪个子树，使每个节点被访问的期望次数受限于树的期望高度 E[h] ≤ log(n+1)。随机使深度路径期望对数，最坏退化（一直随机到一边）的概率被指数压制。

### 原理 · Principle

① 堆性质：父值 ≤ 子值（小根堆）；② merge(t1,t2)：若 t1 空返回 t2，若 t2 值更小则交换使 t1 为小根；随机交换 t1 左右儿子，然后 t1.l = merge(t1.l, t2)；③ 其他操作全部归约：insert = merge(root, 单点)；delete-min = merge(root.l, root.r)；④ 期望分析：记 h(T) 为根到叶的随机路径长，E[h(T)] ≤ log(n+1)（归纳：h = 1 + (h(L)+h(R))/2，用 log 的凹性/AM-GM），且 P(h(T) > (c+1)log n) < 1/n^c，即超出期望的概率随 n 的幂次快速衰减。

### 历史 · History

随机化堆思想源于 e-maxx（俄语算法库）与 G. Gambosi、Geppetti 等对随机优先队列的研究；CP-Algorithms 收录了标准实现（源自 e-maxx.ru 翻译）。其『随机合并选边』思想与 Treap 的随机优先级一脉相承，属于随机化数据结构家族。

## How · 实现

### 伪代码

```python
merge(a, b):
  if a 为空: return b
  if b 为空: return a
  if val(b) < val(a): swap(a, b)
  if random_bit(): swap(a.l, a.r)   # 随机选择合并进左子树
  a.l = merge(a.l, b)
  return a
insert(root, v) = merge(root, Node(v))
find_min(root)  = root.val
delete_min(root) = merge(root.l, root.r)
# 删除任意节点: 需父指针，merge(其子) 后从父链剖出
```

### Python 实现

```python
import heapq
import random


class Node:
    __slots__ = ('val', 'l', 'r')

    def __init__(self, val):
        self.val = val
        self.l = None
        self.r = None


def merge(a, b):
    """随机化合并两个堆，返回新根。期望 O(log n)"""
    if a is None:
        return b
    if b is None:
        return a
    if b.val < a.val:
        a, b = b, a
    if random.getrandbits(1):
        a.l, a.r = a.r, a.l
    a.l = merge(a.l, b)
    return a


def insert(root, val):
    return merge(root, Node(val))


def pop_min(root):
    if root is None:
        return None, None
    return merge(root.l, root.r), root.val


if __name__ == '__main__':
    random.seed(3)
    h = None
    ref = []
    for _ in range(8000):
        op = random.random()
        if op < 0.55 or not ref:
            v = random.randint(0, 100000)
            h = insert(h, v)
            heapq.heappush(ref, v)
        else:
            h, m = pop_min(h)
            r = heapq.heappop(ref)
            assert m == r, (m, r)
        if h is None:
            assert not ref
    # 双堆合并
    h1 = h2 = None
    r1, r2 = [], []
    for v in [4, 2, 8, 1]:
        h1 = insert(h1, v); r1.append(v)
    for v in [9, 3, 0, 5]:
        h2 = insert(h2, v); r2.append(v)
    h = merge(h1, h2)
    out = []
    while h is not None:
        h, m = pop_min(h)
        out.append(m)
    assert out == sorted(r1 + r2), (out, r1, r2)
    print('randomized heap: All tests passed.')
```

**PyPy 提示**: 代码极短，PyPy 下是手写可并堆中最快的之一。用 random.getrandbits(1) 而非 random.random()<0.5 少一次比较。注意随机种子若被卡（对拍/特殊 hack）可能退化，但常规题目无碍。若怕随机退化可改为随机权重选边。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | merge/insert/delete-min 期望 O(log n)；最坏无保证（但退化概率 < 1/n^c） |
| 空间 | O(n) 节点；无额外辅助信息 |

### 局限

复杂度是期望而非最坏保证，理论上存在恶意卡数据导致退化（实践中 OI/ICPC 较少针对随机化卡）。不支持高效 decrease-key（需删除+插入）。合并随机可能使某棵树偏向一边，多次 merge 后深度期望仍对数但常数略大。Python 下若在意最坏复杂度，左偏树（非均摊 O(log n)）更稳妥。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3377 | 3 | 【模板】左偏树（可并堆）：可并堆模板题，随机化堆可作为替代实现（O(n log n) 期望） | [https://www.luogu.com.cn/problem/P3377](https://www.luogu.com.cn/problem/P3377) |
| Luogu | P1090 | 2 | 【NOIP2004】合并果子：合并堆/取最小场景，可并堆与 heapq 均可求解 | [https://www.luogu.com.cn/problem/P1090](https://www.luogu.com.cn/problem/P1090) |

## Pitfalls · 易错点

- 随机交换左右儿子必须在递归前完成且每次合并都随机，漏掉会退化为链
- 删除任意节点需要父指针，且剖出后要把子树 merge 回父链，细节易错
- 期望复杂度不等于最坏复杂度：数据量极大或可被构造卡时优先左偏树
- random 种子固定会使对拍结果可复现但对恶意数据更脆弱
- 大根堆/小根堆方向写反（比较符方向）在 merge 里交换逻辑易混

## Sources · 信源

- CP-Algorithms ✓ [https://cp-algorithms.com/data_structures/randomized_heap.html](https://cp-algorithms.com/data_structures/randomized_heap.html)
- OI Wiki ✓ [https://oi-wiki.org/ds/leftist-tree/](https://oi-wiki.org/ds/leftist-tree/)
