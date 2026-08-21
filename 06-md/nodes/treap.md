---
id: treap
name: Treap(树堆)
group: G-A-8
stage: advanced
priority: P1
depth_tier: standard
---

# Treap(树堆)

> BST+堆随机优先级，旋转维护平衡，期望O(log n)

<!-- 元信息: id=treap · group=G-A-8 · stage=advanced · priority=P1 · depth_tier=standard -->

## What · 是什么

Treap（Tree + Heap，树堆）是一种弱平衡二叉搜索树。每个节点除权值 val 外附带随机优先级 priority：val 满足二叉搜索树性质（左小右大），priority 满足堆性质（小根/大根）。若 val 与 priority 都用同一值则退化成链，故 priority 必须随机。旋转版（旋转 Treap）通过左旋/右旋在插入删除时维持堆性质，所有操作期望 O(log n)。

## Why · 为什么

### 直觉 · Intuition

把「插入顺序」这个导致 BST 退化的因素，用随机优先级彻底打乱：树的结构等价于按 priority 从小到大的插入序列，而这等价于随机排列插入顺序，几乎必然接近理想平衡。priority 最小的节点永远是根。

### 原理 · Principle

期望深度证明：对权值升序第 i 个节点 x_i，其深度 = 祖先个数。定义指示变量 Y_{k,i}=1 当 x_k 是 x_i 祖先。引理：x_k 是 x_i 的祖先 ⇔ x_k 的 priority 是集合 X_{min(i,k)..max(i,k)} 中最小的，概率 = 1/(|i-k|+1)。由期望线性性 E(dep(x_i)) = Σ_{k≠i} 1/(|i-k|+1) = H_i + H_{n-i+1} - 2 ≤ 2 ln n = O(log n)。插入：先按 BST 规则下探插入叶子，再沿路比较 priority 左/右旋转上浮至堆性质恢复；删除：把节点旋转到叶子后剪除，或直接 BST 删除后调整。

### 历史 · History

Treap 由 Raimund Seidel 和 Cecilia Aragon 于 1989 年独立提出（1989 年论文 Randomized Search Trees）。1990s 随 C++ STL 等生态普及，是竞赛中期望平衡树的首选之一。旋转版强调简单，无旋版（FHQ）另成一支，见 fhq-treap。

## How · 实现

### 伪代码

```python
rotate_right(p):            # 右旋：p 的左儿子 q 上浮
  q = p.left; p.left = q.right; q.right = p; 更新size; return q
rotate_left(p):             # 左旋对称
  q = p.right; p.right = q.left; q.left = p; 更新size; return q

insert(p, val):
  if p 为空: return 新节点(priority=random())
  if val < p.val:
    p.left = insert(p.left, val)
    if p.left.pri < p.pri: p = rotate_right(p)
  else:
    p.right = insert(p.right, val)
    if p.right.pri < p.pri: p = rotate_left(p)
  更新 size; return p

delete(p, val):
  if val == p.val:
    if 左/右空: return 另一侧
    if p.left.pri < p.right.pri: p = rotate_right(p); p.right=delete(p.right,val)
    else: p = rotate_left(p); p.left=delete(p.left,val)
  elif val < p.val: p.left = delete(p.left,val)
  else: p.right = delete(p.right,val)
  更新 size; return p
```

### Python 实现

```python
import random

class Node:
    __slots__ = ('val', 'pri', 'left', 'right', 'size')
    def __init__(self, val, pri=None):
        self.val = val
        self.pri = pri if pri is not None else random.random()
        self.left = None
        self.right = None
        self.size = 1

class Treap:
    def __init__(self):
        self.root = None
        self.rng = random.Random(42)

    def _sz(self, n):
        return n.size if n else 0

    def _pull(self, n):
        n.size = 1 + self._sz(n.left) + self._sz(n.right)

    def _rotate_right(self, p):
        q = p.left
        p.left = q.right
        q.right = p
        self._pull(p)
        self._pull(q)
        return q

    def _rotate_left(self, p):
        q = p.right
        p.right = q.left
        q.left = p
        self._pull(p)
        self._pull(q)
        return q

    def _insert(self, p, val):
        if p is None:
            return Node(val, self.rng.random())
        if val < p.val:
            p.left = self._insert(p.left, val)
            if p.left.pri < p.pri:
                p = self._rotate_right(p)
        else:
            p.right = self._insert(p.right, val)
            if p.right.pri < p.pri:
                p = self._rotate_left(p)
        self._pull(p)
        return p

    def insert(self, val):
        self.root = self._insert(self.root, val)

    def _delete(self, p, val):
        if p is None:
            return None
        if val == p.val:
            if p.left is None:
                return p.right
            if p.right is None:
                return p.left
            if p.left.pri < p.right.pri:
                p = self._rotate_right(p)
                p.right = self._delete(p.right, val)
            else:
                p = self._rotate_left(p)
                p.left = self._delete(p.left, val)
        elif val < p.val:
            p.left = self._delete(p.left, val)
        else:
            p.right = self._delete(p.right, val)
        self._pull(p)
        return p

    def delete(self, val):
        self.root = self._delete(self.root, val)

    def search(self, val):
        n = self.root
        while n and n.val != val:
            n = n.left if val < n.val else n.right
        return n is not None

    def inorder(self):
        out = []
        def dfs(n):
            if n is None:
                return
            dfs(n.left)
            out.append(n.val)
            dfs(n.right)
        dfs(self.root)
        return out

    def height(self):
        def go(n):
            if n is None:
                return 0
            return 1 + max(go(n.left), go(n.right))
        return go(self.root)


def _is_heap(n, lo=-float('inf')):
    if n is None:
        return True
    if not lo <= n.pri:
        return False
    return _is_heap(n.left, n.pri) and _is_heap(n.right, n.pri)  # 小根堆：子 >= 父


def _is_bst(n, lo=-float('inf'), hi=float('inf')):
    if n is None:
        return True
    if not (lo < n.val < hi):
        return False
    return _is_bst(n.left, lo, n.val) and _is_bst(n.right, n.val, hi)


if __name__ == "__main__":
    t = Treap()
    n = 1000
    for _ in range(n):
        t.insert(random.randint(0, 100000))
    vals = t.inorder()
    assert vals == sorted(vals)
    assert _is_heap(t.root)
    assert t.height() <= 60, t.height()  # 期望 O(log n)
    s = set(vals)
    for v in list(s)[:len(s) // 2]:
        while t.search(v):
            t.delete(v)
        assert not t.search(v)
    assert _is_heap(t.root)
    assert t.inorder() == sorted(t.inorder())
    t2 = Treap()
    for i in range(10000):
        t2.insert(i)  # 有序插入也不退化
    assert t2.height() < 80, t2.height()
    assert t2.inorder() == list(range(10000))
    print("All tests passed.")
```

**PyPy 提示**: rotation treap 常数小但需维护父指针或按引用返回，Python 递归写法在随机树高 ~40 内安全；priority 用 random.random() 即可，避免 random.randint 开销。PyPy 下递归深度限制默认小，大规模可 sys.setrecursionlimit。实际比赛中 Python 更常用 FHQ-Treap（见 fhq-treap 节点）。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 所有操作期望 O(log n)（随机优先级下节点期望深度 2ln n）；最坏 O(n) 概率极小 |
| 空间 | O(n) |

### 局限

期望复杂度依赖随机数质量；最坏情形（priority 恰好单调）概率虽小仍非严格保证。不支持区间操作（区间翻转/区间加）——需无旋 Treap 或 Splay。重复元素需约定处理。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3369 | 4 | 普通平衡树模板：插入/删除/排名/前驱后继全操作 | [https://www.luogu.com.cn/problem/P3369](https://www.luogu.com.cn/problem/P3369) |
| LOJ | 104 | 4 | 普通平衡树（旋转 Treap 模板题） | [https://loj.ac/problem/104](https://loj.ac/problem/104) |
| LOJ | 105 | 5 | 文艺平衡树：区间翻转需无旋 Treap 分裂合并 | [https://loj.ac/problem/105](https://loj.ac/problem/105) |

## Pitfalls · 易错点

- priority 用固定值（如直接取 val）导致退化成链
- 旋转后忘记更新两个节点的 size，导致排名错误
- 删除双子节点时优先旋转左/右儿子顺序写反，破坏堆性质
- 把期望 O(log n) 当最坏 O(log n)，追求确定性请用替罪羊树

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/treap/](https://oi-wiki.org/ds/treap/)
- CP-Algorithms ✓ [https://cp-algorithms.com/data_structures/treap.html](https://cp-algorithms.com/data_structures/treap.html)
- 论文 ✓ `Seidel & Aragon, Randomized Search Trees (1989)`
