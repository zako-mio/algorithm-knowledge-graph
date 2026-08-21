---
id: leftist-tree
name: 左偏树(可并堆)
group: G-A-3
stage: advanced
priority: P1
depth_tier: standard
---

# 左偏树(可并堆)

> 支持O(log n)合并的可并堆，利用偏侧树高

<!-- 元信息: id=leftist-tree · group=G-A-3 · stage=advanced · priority=P1 · depth_tier=standard -->

## What · 是什么

左偏树（Leftist Tree）是一种可并堆（mergeable heap）：在二叉堆的堆性质（父节点值 ≤ 子节点值，小根堆）之上，额外维护每个节点的 dist（到子树中最近『外节点』——即子节点数小于 2 的节点——经过的边数），并保证『左偏性质』：每个节点左儿子的 dist ≥ 右儿子的 dist。因此每个节点的 dist 等于其右儿子 dist 加一，且根的 dist 为 O(log n)。核心操作 merge 将两棵左偏树在 O(log n + log m) 内合并，其他操作（插入=与单点合并、删根=合并左右儿子、删任意节点=合并儿子+自底向上 pushup）都归约为 merge。由于每次递归使其中一个根 dist 减一，复杂度有保证。它是竞赛中实现可并堆（如 k 短路、树上合并堆）的最常用结构，也可持久化。

## Why · 为什么

### 直觉 · Intuition

普通二叉堆的合并要重建整个数组是 O(n) 的。左偏树把堆改成指针二叉树，并刻意让『右边变短』——dist 小的永远是右儿子。合并时就递归合并右儿子与另一个堆，保证递归深度不超过两个根的 dist 之和，即 O(log n)。左偏性质是空间换深度：树整体可能很不平衡（甚至一条左链），但每次操作的递归深度被 dist 限制住。

### 原理 · Principle

① 定义 dist：外节点（子节点数<2）dist=0，空节点 dist=-1，节点 dist=右儿子 dist+1；② 左偏性质：左儿子 dist ≥ 右儿子 dist（等价于节点 dist=右儿子 dist+1）；③ 关键性质：dist 为 x 的二叉树至少有 2^x-1 个节点（所有二叉树都满足），故 n 个节点的树 dist ≤ ⌈log(n+1)⌉；④ merge(x,y)：取值小的根为新根，递归合并 x 右儿子与 y，合并后若不满足左偏性质则交换左右儿子，更新 dist。每次递归其中一个堆的根 dist 减 1，故 O(log n+log m)。

### 历史 · History

可并堆家族经历了从左偏树（Leftist Tree，Knuth 归功于 Crane，1972）到二项堆、配对堆、斐波那契堆的演进。左偏树胜在实现简单、非均摊复杂度保证，是 OI 中最常用的可并堆，OI Wiki 与黄源河《左偏树的特点及其应用》系统讲述了其应用。

## How · 实现

### 伪代码

```python
dist(空)=-1, dist(外节点)=0, dist(x)=dist(right(x))+1
merge(x, y):
  if x 为空: return y
  if y 为空: return x
  if val(x) > val(y): swap(x, y)   # 取小根为根
  right(x) = merge(right(x), y)
  if dist(left(x)) < dist(right(x)): swap(left(x), right(x))
  dist(x) = dist(right(x)) + 1
  return x
insert(root, v) = merge(root, new_node(v))
pop_min(root)   = merge(left(root), right(root))
```

### Python 实现

```python
import heapq
import random
import sys
sys.setrecursionlimit(1000000)


class Node:
    __slots__ = ('val', 'l', 'r', 'dist')

    def __init__(self, val):
        self.val = val
        self.l = None
        self.r = None
        self.dist = 0   # 外节点 dist=0，空节点视为 -1


def _d(x):
    return -1 if x is None else x.dist


def merge(x, y):
    """合并两棵左偏树（小根堆），返回新根。O(log n + log m)"""
    if x is None:
        return y
    if y is None:
        return x
    if x.val > y.val:
        x, y = y, x
    x.r = merge(x.r, y)
    if _d(x.l) < _d(x.r):
        x.l, x.r = x.r, x.l
    x.dist = _d(x.r) + 1
    return x


def insert(root, val):
    return merge(root, Node(val))


def pop_min(root):
    """删除并返回堆顶。返回 (新根, 原堆顶值)；空堆返回 (None, None)"""
    if root is None:
        return None, None
    return merge(root.l, root.r), root.val


if __name__ == '__main__':
    # 与 heapq 交叉验证（随机操作序列）
    random.seed(1)
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
    for v in [3, 1, 4, 1, 5, 9, 2, 6]:
        h1 = insert(h1, v); r1.append(v)
    for v in [7, 0, 8, 5, 2]:
        h2 = insert(h2, v); r2.append(v)
    h = merge(h1, h2)
    r = sorted(r1 + r2)
    out = []
    while h is not None:
        h, m = pop_min(h)
        out.append(m)
    assert out == r, (out, r)
    print('leftist tree: All tests passed.')
```

**PyPy 提示**: Python 指针式左偏树常数偏大，2e5 规模需 PyPy 并尽量压缩节点（__slots__）、用数组模拟节点（val/l/r/dist 四列表）替代对象可提升 2-3 倍。合并时每次比较 val 前先判空；要支持找堆顶必须配并查集（左偏树深度可达 O(n)，不能暴力跳父）。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | merge O(log n + log m)；insert/pop O(log n)；删除任意节点 O(log n)（均非均摊） |
| 空间 | O(n) 节点存储；递归栈 O(log n) |

### 局限

左偏树的深度没有保证（可以是一条左链），因此『找某个点所在堆的堆顶』必须用并查集维护，不能跳父节点。不支持 O(1) 的 decrease-key（需删除+插入，O(log n)）。dist 定义不同写法（空节点 -1 vs 0）易混。若需持久化请用 persistent-heap 的 path-copying 版本。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3377 | 3 | 【模板】左偏树（可并堆）：合并/删根/查最小值，需并查集找堆顶，经典模板题 | [https://www.luogu.com.cn/problem/P3377](https://www.luogu.com.cn/problem/P3377) |
| Luogu | P1456 | 3 | Monkey King：合并+删根+改值再插回，可并堆基础应用 | [https://www.luogu.com.cn/problem/P1456](https://www.luogu.com.cn/problem/P1456) |
| Luogu | P2713 | 3 | 罗马游戏：多堆合并、删除最小值、找所在堆顶，OI Wiki 例题 | [https://www.luogu.com.cn/problem/P2713](https://www.luogu.com.cn/problem/P2713) |
| Luogu | P1552 | 4 | 【APIO2012】派遣：树上每个节点维护左偏树与子树合并、贪心弹出，树上可并堆应用 | [https://www.luogu.com.cn/problem/P1552](https://www.luogu.com.cn/problem/P1552) |
| LOJ | 2107 | 5 | 【JLOI2015】城池攻占：树上堆合并+整体加减标记+lazy，可并堆+标记技巧 | [https://loj.ac/problem/2107](https://loj.ac/problem/2107) |

## Pitfalls · 易错点

- 找堆顶必须用并查集：左偏树深度可能 O(n)，直接跳父会 TLE/爆栈
- merge 前先判断两堆是否已在同一堆中（若已在则直接返回，否则死循环）
- dist 定义要统一：OI Wiki 用空节点 dist=-1（代码免判空），用 dist=0 的定义则空节点必须特判
- 用对象实现时递归深度可能到 O(n)（左链），需 sys.setrecursionlimit；竞赛中建议数组模拟
- 删除任意节点需要 parent 指针和自底向上 pushup，只 merge 左右儿子会破坏该节点父节点的左偏性质
- pop_min 返回值顺序写反（先返回新根后返回值）；空堆需特判

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/leftist-tree/](https://oi-wiki.org/ds/leftist-tree/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/leftist-tree.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/leftist-tree.md)
- OI Wiki ✓ [https://oi-wiki.org/ds/heap/](https://oi-wiki.org/ds/heap/)
