---
id: avl
name: AVL树
group: G-A-8
stage: advanced
priority: P2
depth_tier: standard
---

# AVL树

> 严格平衡(高度差<=1)，旋转维护

<!-- 元信息: id=avl · group=G-A-8 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

AVL 树是最早发明的自平衡二叉搜索树（1962 年，Adelson-Velsky 与 Landis）。每个节点维护子树高度 h，保证任意节点左右子树高度差 |h(left)-h(right)| ≤ 1（该差称为平衡因子，常用 right-left 表示，取值 ∈{-1,0,1}）。插入/删除后通过四种旋转（LL/RR/LR/RL）恢复平衡，树高严格 O(log n)，所有操作严格 O(log n)。

## Why · 为什么

### 直觉 · Intuition

二叉树平衡意味着树高低。AVL 把「高度差不超 1」作为硬约束，最坏树高约为 1.44·log2(n+2)（设 f_n 为高 n 的最小节点数，f_n=f_{n-1}+f_{n-2}+1，即 Fibonacci 型递归），保证查找像二分一样快且无随机性。插入只需沿插入路径回溯，发现平衡因子出界就旋转一次即可恢复。

### 原理 · Principle

四种失衡形态（以插入后第一个失衡节点 A 判断）：LL——左子树高且 A.left 的左子树更高，右旋 A；RR——右子树高且 A.right 的右子树更高，左旋 A；LR——左子树高但 A.left 的右子树更高，先左旋 A.left 再右旋 A；RL——右子树高但 A.right 的左子树更高，先右旋 A.right 再左旋 A。删除后可能需沿路径多次旋转（至多 O(log n) 次）。平衡因子更新顺序：旋转后先更新子树节点高度再更新新根。

### 历史 · History

1962 年由 G. M. Adelson-Velsky 与 E. M. Landis 在苏联提出，是最早的平衡树，名字即两位作者缩写。作为数据结构教科书（CLRS/算法导论）的经典内容，也用于内存数据库（如早期的 Java TreeMap 之前、C++ 部分实现）等场景。竞赛中因实现较繁、常数较大，如今 Python 选手多用 FHQ-Treap，但理解 AVL 有助于掌握旋转与平衡因子思想。

## How · 实现

### 伪代码

```python
get_balance(x) = height(x.right) - height(x.left)

insert(x, val):            # 与 BST 一致，返回后更新高度
  ... 普通 BST 插入 ...
  height[x] = 1 + max(height(left), height(right))
  bf = get_balance(x)
  if bf > 1 and val > x.right.val:  return left_rotate(x)      # RR
  if bf > 1 and val <= x.right.val: x.right=right_rotate(x.right); return left_rotate(x)  # RL
  if bf < -1 and val <= x.left.val: return right_rotate(x)     # LL
  if bf < -1 and val > x.left.val:  x.left=left_rotate(x.left); return right_rotate(x)    # LR
  return x

delete 类似：BST 删除后更新高度、按 bf 四种旋转（且需向根持续检查）
```

### Python 实现

```python
class AVLNode:
    __slots__ = ('val', 'left', 'right', 'h')
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.h = 1

class AVL:
    def __init__(self):
        self.root = None

    @staticmethod
    def _h(n):
        return n.h if n else 0

    def _pull(self, n):
        n.h = 1 + max(self._h(n.left), self._h(n.right))

    def _bf(self, n):
        return self._h(n.right) - self._h(n.left)

    def _rr(self, a):
        b = a.right
        a.right = b.left
        b.left = a
        self._pull(a)
        self._pull(b)
        return b

    def _rl(self, a):
        b = a.left
        a.left = b.right
        b.right = a
        self._pull(a)
        self._pull(b)
        return b

    def _balance(self, n):
        bf = self._bf(n)
        if bf > 1:
            if self._bf(n.right) >= 0:      # RR
                return self._rr(n)
            n.right = self._rl(n.right)     # RL
            return self._rr(n)
        if bf < -1:
            if self._bf(n.left) <= 0:       # LL
                return self._rl(n)
            n.left = self._rr(n.left)       # LR
            return self._rl(n)
        return n

    def _insert(self, n, val):
        if n is None:
            return AVLNode(val)
        if val < n.val:
            n.left = self._insert(n.left, val)
        else:
            n.right = self._insert(n.right, val)
        self._pull(n)
        return self._balance(n)

    def insert(self, val):
        self.root = self._insert(self.root, val)

    def _min(self, n):
        while n.left:
            n = n.left
        return n

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
            m = self._min(n.right)          # 后继替换
            n.val = m.val
            n.right = self._delete(n.right, m.val)
        self._pull(n)
        return self._balance(n)

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
        return self._h(self.root)


def _is_avl(n):
    if n is None:
        return True, 0
    ok_l, hl = _is_avl(n.left)
    ok_r, hr = _is_avl(n.right)
    ok = ok_l and ok_r and abs(hl - hr) <= 1
    return ok, 1 + max(hl, hr)


def _is_bst(n, lo=-float('inf'), hi=float('inf')):
    if n is None:
        return True
    if not (lo < n.val <= hi):
        return False
    return _is_bst(n.left, lo, n.val) and _is_bst(n.right, n.val, hi)


if __name__ == "__main__":
    import random
    random.seed(9)
    t = AVL()
    arr = []
    for _ in range(3000):
        v = random.randint(0, 100000)
        t.insert(v)
        arr.append(v)
    assert t.inorder() == sorted(arr)
    ok, _ = _is_avl(t.root)
    assert ok, "AVL balance broken"
    # 树高上界验证：1.44*log2(n+2)
    import math
    n = len(arr)
    bound = 1.44 * math.log2(n + 2) + 1
    assert t.height() <= bound, (t.height(), bound)
    # 有序插入也不退化
    t2 = AVL()
    for i in range(2000):
        t2.insert(i)
    ok, _ = _is_avl(t2.root)
    assert ok and t2.height() < 30
    # 删除一半
    uniq = sorted(set(arr))
    removed = set(uniq[:len(uniq) // 2])
    for v in removed:
        while t.search(v):
            t.delete(v)
    expect = sorted(a for a in arr if a not in removed)
    assert t.inorder() == expect
    ok, _ = _is_avl(t.root)
    assert ok, "AVL broken after deletes"
    assert t.inorder() == sorted(t.inorder())
    print("All tests passed.")
```

**PyPy 提示**: AVL 用递归实现时每次 _balance 返回新根，注意 Python 递归深度受树高限制（~1.44 log n，安全）。平衡因子计算用 right-left 约定需与旋转方向一致。删除用后继替换后递归删除，注意 _delete 内部更新。实际竞赛若追求简洁请用 FHQ-Treap。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 查找/插入/删除严格 O(log n)（树高 ≤1.44 log n） |
| 空间 | O(n) |

### 局限

插入至多一次旋转，删除至多 O(log n) 次旋转（仍 O(log n)）；常数比 Treap/FHQ 略大；实现需维护高度与平衡因子，代码量大于 FHQ。无区间操作支持。竞赛 Python 场景优先级不高，属理论理解型结构。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3369 | 4 | 普通平衡树：AVL 全操作实现 | [https://www.luogu.com.cn/problem/P3369](https://www.luogu.com.cn/problem/P3369) |
| LeetCode.cn | 110 | 2 | 判断平衡二叉树：高度差校验即 AVL 平衡条件 | [https://leetcode.cn/problems/balanced-binary-tree/](https://leetcode.cn/problems/balanced-binary-tree/) |

## Pitfalls · 易错点

- LL 与 LR、RR 与 RL 判断混淆（需看失衡子树自身平衡因子方向）
- 旋转后未先更新旧子树高度再更新新根高度，导致高度错误连锁失衡
- 删除后用左子树最大值替换但未递归删除它（残留副本）
- 平衡因子用 int 缓存但旋转后忘记刷新

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/avl/](https://oi-wiki.org/ds/avl/)
- 书籍 ✓ `CLRS《算法导论》ch13 红黑树 / ch12 二叉搜索树（AVL 思想）`
