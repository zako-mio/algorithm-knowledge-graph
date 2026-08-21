---
id: bst
name: 二叉搜索树基础
group: G-A-8
stage: intermediate
priority: P1
depth_tier: standard
---

# 二叉搜索树基础

> 左<根<右性质，期望O(log n)操作，最坏O(n)退化

<!-- 元信息: id=bst · group=G-A-8 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

二叉搜索树（Binary Search Tree, BST）是满足「左子树所有节点值 < 根节点值 < 右子树所有节点值」的二叉树。中序遍历得到有序序列。支持查找、插入、删除、前驱/后继、排名/按排名取值等操作，每个操作的时间与树高 h 成正比，最优情形 O(log n)，最坏（退化成链）O(n)。

## Why · 为什么

### 直觉 · Intuition

每次比较都把候选空间减半：小于当前节点向左，大于向右，与二分查找同理。理想的满二叉树高度 O(log n)，所以查询像二分一样快；但插入顺序若有序，树会退化成一维链表，比较次数退化为 O(n)。

### 原理 · Principle

删除分三情况：无子节点直接删；单子节点让子顶替；双子节点用左子树最大值（前驱）或右子树最小值（后继）替换后删除，保证中序性质不变。排名 = 左子树 size + 1；按排名反查沿 size 分支递归。所有操作依赖递归下探，复杂度等于路径长度（树高）。

### 历史 · History

BST 是平衡树家族的原型，源自 1960 年代二叉搜索思想。1962 年 Adelson-Velsky 与 Landis 提出 AVL 树，此后 Splay(1985)、Treap(1989)、替罪羊树(1989)等先后出现，皆以维持 BST 有序性为基座。OI Wiki《二叉搜索树》为当前通用教程。

## How · 实现

### 伪代码

```python
insert(root, val):
  if root 为空: 返回新节点
  if val < root.val: root.left = insert(root.left, val)
  else if val > root.val: root.right = insert(root.right, val)
  else: 已存在，直接返回
  更新 root.size，返回 root

delete(root, val):
  if root 为空: 返回 None
  if val < root.val: root.left = delete(root.left, val)
  elif val > root.val: root.right = delete(root.right, val)
  else:
    若左/右子树为空 → 返回另一侧
    否则找左子树最大节点(前驱)代替之，删前驱
  更新 root.size，返回 root

search/rank/kth 沿左右分支递归即可
```

### Python 实现

```python
class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.size = 1

class BST:
    def __init__(self):
        self.root = None

    @staticmethod
    def _sz(n):
        return n.size if n else 0

    def _pull(self, n):
        n.size = 1 + self._sz(n.left) + self._sz(n.right)

    def insert(self, val):
        self.root = self._insert(self.root, val)

    def _insert(self, n, val):
        if n is None:
            return Node(val)
        if val < n.val:
            n.left = self._insert(n.left, val)
        else:
            n.right = self._insert(n.right, val)
        self._pull(n)
        return n

    def search(self, val):
        n = self.root
        while n and n.val != val:
            n = n.left if val < n.val else n.right
        return n is not None

    def delete(self, val):
        self.root = self._delete(self.root, val)

    def _delete(self, n, val):
        if n is None:
            return None
        if val < n.val:
            n.left = self._delete(n.left, val)
        elif val > n.val:
            n.right = self._delete(n.right, val)
        else:
            if n.left is None:
                return n.right
            if n.right is None:
                return n.left
            p = n.left
            while p.right:
                p = p.right
            n.val = p.val
            n.left = self._delete(n.left, p.val)
        self._pull(n)
        return n

    def kth(self, k):
        n = self.root
        while n:
            ls = self._sz(n.left)
            if k == ls + 1:
                return n.val
            if k <= ls:
                n = n.left
            else:
                k -= ls + 1
                n = n.right
        raise ValueError("k out of range")

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


def _check_bst_property(n, lo, hi):
    if n is None:
        return True
    if not (lo < n.val < hi):
        return False
    return _check_bst_property(n.left, lo, n.val) and _check_bst_property(n.right, n.val, hi)


if __name__ == "__main__":
    import random
    random.seed(1)
    t = BST()
    for _ in range(200):
        t.insert(random.randint(0, 1000))
    vals = t.inorder()
    assert vals == sorted(vals)
    k = random.randint(1, len(vals))
    assert t.kth(k) == vals[k - 1]
    for v in set(vals):
        while t.search(v):
            t.delete(v)
        assert not t.search(v)
    assert t.inorder() == []
    t = BST()
    for i in range(500):   # 1000 会触发行链递归上限
        t.insert(i)
    assert _check_bst_property(t.root, -1, 500)
    assert t.kth(250) == 249
    print("All tests passed.")
```

**PyPy 提示**: Python 实现 BST 建议显式用 while 而非深度递归（深度可能 O(n) 触发递归上限）；删除用前驱替换法时注意递归删除前驱的边界。竞赛中裸 BST 常被卡退化，Python 选手更应直接上 FHQ-Treap 或直接用内置 sortedcontainers/平衡树库，或离线离散化+树状数组。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 查找/插入/删除/排名 O(h)；理想 h=O(log n)，最坏 h=O(n) |
| 空间 | O(n) |

### 局限

对有序插入序列退化成链，全部操作退化 O(n)。无自平衡机制，竞赛中几乎不裸用，而是作为理解平衡树（Treap/Splay/AVL/替罪羊树）的前置概念。重复元素需约定左闭右开或计数合并。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| LeetCode.cn | 700 | 1 | BST 最基础查找：沿分支下探 | [https://leetcode.cn/problems/search-in-a-binary-search-tree/](https://leetcode.cn/problems/search-in-a-binary-search-tree/) |
| LeetCode.cn | 450 | 3 | 删除的三种情况与前驱/后继替换 | [https://leetcode.cn/problems/delete-node-in-a-bst/](https://leetcode.cn/problems/delete-node-in-a-bst/) |
| Luogu | P3369 | 4 | 普通平衡树模板：裸 BST 会被卡，需平衡化 | [https://www.luogu.com.cn/problem/P3369](https://www.luogu.com.cn/problem/P3369) |

## Pitfalls · 易错点

- 删除双子节点时直接删根导致子树丢失，必须用前驱/后继替换
- 把「期望 O(log n)」当成「最坏 O(log n)」，忽略有序插入退化
- 递归深度在退化树上可到 n，Python 超递归上限 RecursionError
- 重复元素处理不一致（按 < / <= 分支），导致查找遗漏或死循环

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/bst/](https://oi-wiki.org/ds/bst/)
- 书籍 ✓ `CLRS《算法导论》ch12 二叉搜索树`
