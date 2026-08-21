---
id: fhq-treap
name: 无旋Treap(FHQ Treap)
group: G-A-8
stage: advanced
priority: P1
depth_tier: standard
---

# 无旋Treap(FHQ Treap)

> 按值/按秩分裂合并，无需旋转，可持久化友好

<!-- 元信息: id=fhq-treap · group=G-A-8 · stage=advanced · priority=P1 · depth_tier=standard -->

## What · 是什么

FHQ Treap（无旋 Treap / 分裂合并 Treap，由范浩强提出）在随机优先级 Treap 基础上用分裂(split)与合并(merge)代替旋转维护堆性质。split 按值或按子树大小把树切成两棵，merge 按 priority 决定根，均不改变中序顺序。由此天然支持区间操作（区间翻转/区间加）、可持久化、可并堆等旋转 Treap 难以实现的功能，所有操作期望 O(log n)。

## Why · 为什么

### 直觉 · Intuition

旋转本质是把节点上浮调整，而分裂-合并等价于把子树整体重新拼接：按值分裂把小于 x 的部分摘出来，再与另一棵按 priority 合并回去——拼接顺序由 priority 决定，等价于旋转逐步到位。因为不物理旋转节点，历史版本不会因原地修改而被破坏，可持久化极自然。

### 原理 · Principle

split(cur, key, &a, &b)：若 cur.val <= key（按值）则 a 的右半包含 cur 右子树递归分裂，反之 b 的左半递归；同时保留节点本身，不修改其子指针，故可持久化。merge(a, b)：若 a.pri < b.pri 则 a.right = merge(a.right, b) 返回 a，否则 b.left = merge(a, b.left) 返回 b。所有插入/删除/区间操作均可分解为两次 split + 一次 merge + 再合并。区间翻转：按 rank split 出 [l,r]，在中间树根打懒标记，再 merge 回去。期望复杂度证明同旋转 Treap（节点期望深度 O(log n)）。

### 历史 · History

无旋 Treap 由范浩强在其论文/讲解中推广（2010s），中文竞赛圈普遍称 FHQ-Treap。因其实现简洁、支持区间操作与可持久化，成为 OI/Python 竞赛中最受欢迎的平衡树。OI Wiki《平衡树》与《文艺平衡树》均以其为模板。

## How · 实现

### 伪代码

```python
split_val(cur, val, &a, &b):      # 按值：a 含 <=val，b 含 >val
  if cur 为空: a=b=null; return
  if cur.val <= val:
    a = cur
    split_val(cur.right, val, cur.right, b)
    push_up(cur)
  else:
    b = cur
    split_val(cur.left, val, a, cur.left)
    push_up(cur)

split_rank(cur, k, &a, &b):       # 按秩：a 含前 k 个
  if cur 为空: a=b=null; return
  if size(cur.left) + 1 <= k:
    a = cur
    split_rank(cur.right, k - size(cur.left) - 1, cur.right, b)
    push_up(cur)
  else:
    b = cur
    split_rank(cur.left, k, a, cur.left)
    push_up(cur)

merge(a, b):
  if a 为空 or b 为空: return a or b
  if a.pri < b.pri:
    a.right = merge(a.right, b); push_up(a); return a
  else:
    b.left = merge(a, b.left); push_up(b); return b

insert(val): x,y = split_val(root,val); root = merge(merge(x,Node(val)), y)
delete(val): a,b = split_val(root,val-1); c,d = split_val(b,val); c = split_rank(c,size(c)-1)[0]; root = merge(merge(a,c), d)
区间翻转(l,r): a,b = split_rank(root,l-1); b,c = split_rank(b,r-l+1); b.rev ^= 1; root = merge(merge(a,b),c)
```

### Python 实现

```python
import random

class Node:
    __slots__ = ('val', 'pri', 'left', 'right', 'size', 'rev')
    def __init__(self, val, pri=None):
        self.val = val
        self.pri = pri if pri is not None else random.random()
        self.left = None
        self.right = None
        self.size = 1
        self.rev = False

def sz(n):
    return n.size if n else 0

def pull(n):
    if n:
        n.size = 1 + sz(n.left) + sz(n.right)

def push(n):
    if n and n.rev:
        n.left, n.right = n.right, n.left
        if n.left:
            n.left.rev ^= True
        if n.right:
            n.right.rev ^= True
        n.rev = False

def split_val(cur, val):
    """返回 (a, b): a 含 val<=key 的节点，b 含 >key 的节点。"""
    if cur is None:
        return None, None
    push(cur)
    if cur.val <= val:
        a, b = split_val(cur.right, val)
        cur.right = a
        pull(cur)
        return cur, b
    else:
        a, b = split_val(cur.left, val)
        cur.left = b
        pull(cur)
        return a, cur

def split_rank(cur, k):
    """返回 (a, b): a 为前 k 个节点的树。"""
    if cur is None:
        return None, None
    push(cur)
    if sz(cur.left) + 1 <= k:
        a, b = split_rank(cur.right, k - sz(cur.left) - 1)
        cur.right = a
        pull(cur)
        return cur, b
    else:
        a, b = split_rank(cur.left, k)
        cur.left = b
        pull(cur)
        return a, cur

def merge(a, b):
    if a is None or b is None:
        return a or b
    if a.pri < b.pri:
        push(a)
        a.right = merge(a.right, b)
        pull(a)
        return a
    else:
        push(b)
        b.left = merge(a, b.left)
        pull(b)
        return b

def insert(root, val):
    a, b = split_val(root, val)
    return merge(merge(a, Node(val)), b)

def delete(root, val):
    a, b = split_val(root, val - 1)   # a = < val
    c, d = split_val(b, val)          # c = == val 的所有副本, d = > val
    c = split_rank(c, sz(c) - 1)[0]   # 丢弃最右副本，删一个
    return merge(merge(a, c), d)

def reverse_range(root, l, r):
    a, b = split_rank(root, l - 1)
    b, c = split_rank(b, r - l + 1)
    if b:
        b.rev ^= True
    return merge(merge(a, b), c)

def inorder(n):
    out = []
    if n:
        push(n)
        out.extend(inorder(n.left))
        out.append(n.val)
        out.extend(inorder(n.right))
    return out

def _is_heap(n, lo=-float('inf')):
    if n is None:
        return True
    if not lo <= n.pri:
        return False
    return _is_heap(n.left, n.pri) and _is_heap(n.right, n.pri)  # 小根堆：子 >= 父


def _check_bst(n, lo=-float('inf'), hi=float('inf')):
    if n is None:
        return True
    if not (lo < n.val <= hi):
        return False
    return _check_bst(n.left, lo, n.val) and _check_bst(n.right, n.val, hi)


if __name__ == "__main__":
    rng = random.Random(7)
    root = None
    arr = []
    for _ in range(500):
        v = rng.randint(0, 1000)
        root = insert(root, v)
        arr.append(v)
    assert _is_heap(root)
    assert inorder(root) == sorted(arr)
    for _ in range(100):
        v = rng.choice(list(sorted(set(arr))))
        root = delete(root, v)
        arr.remove(v)
    assert inorder(root) == sorted(arr)
    # 区间翻转
    seq = list(range(1, 11))
    root = None
    for x in seq:
        root = insert(root, x)
    root = reverse_range(root, 2, 5)  # 翻转 [2,5]
    got = inorder(root)
    expect = [1, 5, 4, 3, 2, 6, 7, 8, 9, 10]
    assert got == expect, got
    root = reverse_range(root, 1, 10)
    assert inorder(root) == expect[::-1]
    print("All tests passed.")
```

**PyPy 提示**: FHQ-Treap 递归深度等于树高期望 ~O(log n)，PyPy 默认递归上限可能不足，建议模块头 sys.setrecursionlimit(1<<25)。priority 用 random.random()。区间操作记得先 push 后 split/merge。Python 版本比 Splay 常数更小、更好写，是平衡树问题首选。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | split/merge/insert/delete/区间操作均期望 O(log n) |
| 空间 | O(n)；可持久化版本额外 O(版本数×log n) |

### 局限

期望复杂度依赖随机数；最坏理论 O(n) 概率极小。可持久化时每次修改产生 O(log n) 新节点，空间开销上升。区间操作需 push 懒标记与 rank 分裂配合，标记下传时序错误会造成中序错乱。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3369 | 4 | 普通平衡树：FHQ 分裂合并模板题 | [https://www.luogu.com.cn/problem/P3369](https://www.luogu.com.cn/problem/P3369) |
| Luogu | P3391 | 5 | 文艺平衡树：区间翻转，rank 分裂+懒标记 | [https://www.luogu.com.cn/problem/P3391](https://www.luogu.com.cn/problem/P3391) |
| LOJ | 105 | 5 | 文艺平衡树官方模板，区间翻转完整实现 | [https://loj.ac/problem/105](https://loj.ac/problem/105) |
| Luogu | P3835 | 6 | 可持久化平衡树：版本回溯，每次操作开新根 | [https://www.luogu.com.cn/problem/P3835](https://www.luogu.com.cn/problem/P3835) |

## Pitfalls · 易错点

- split 后忘记 push_up 更新 size，导致 rank 分裂越界
- 区间操作前未 push 懒标记就 split，翻转信息丢失或错位
- delete 用 split_val(val) 与 split_val(val-1) 时 val-1 对离散化值域错误（应 split 两次同 val）
- 可持久化时复用旧节点而不 clone，导致旧版本被修改（非持久化正确性）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/treap/](https://oi-wiki.org/ds/treap/)
- OI Wiki ✓ [https://oi-wiki.org/ds/treap/#无旋-treap](https://oi-wiki.org/ds/treap/#无旋-treap)
- 书籍 ✓ `范浩强 无旋Treap 讲解（FHQ 论文/博客，2010s）`
