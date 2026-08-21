---
id: rbtree
name: 红黑树
group: G-A-8
stage: advanced
priority: P3
depth_tier: brief
---

# 红黑树

> 弱平衡BST，C++ std::map底层，竞赛中少用

<!-- 元信息: id=rbtree · group=G-A-8 · stage=advanced · priority=P3 · depth_tier=brief -->

## What · 是什么

红黑树（Red-Black Tree）是一种自平衡二叉搜索树，每个节点有红/黑颜色，满足五条性质：①节点非红即黑；②根为黑；③NIL 叶子为黑；④红节点的子节点为黑（红节点不连续）；⑤任意节点到其所有后代 NIL 路径的黑节点数相等（黑高相等）。由此保证最长路径不超过最短路径的 2 倍，树高 ≤ 2·log2(n+1)，插入/删除均严格 O(log n)。是 4 阶 B 树（2-3-4 树）的二叉表示。C++ std::map/std::set 与 Java TreeMap 的底层实现。

## Why · 为什么

### 直觉 · Intuition

黑高约束（性质⑤）保证从根到任何叶子的黑色节点一样多；性质④禁止两个连续红节点，因此最长路径（红黑交替）至多是最短路径（全黑）的 2 倍，树高 O(log n)。相比 AVL 的高度差 ≤1，红黑树允许更大的不平衡，因此旋转更少、写入性能好，特别适合频繁插入删除的实现（如 STL）。

### 原理 · Principle

插入：新节点着红，可能破坏性质④（父红叔红→变色并向上递归；父红叔黑→旋转）。删除：删除黑色节点会破坏黑高，用「双黑」处理，分四种情形（兄弟红/兄弟黑且侄子全黑/侄子有红）分别旋转+变色。平衡维护分为插入 2 情形、删除 4 情形。由于 2-3-4 树视角，红黑树等价于把 3/4 节点编码成带红色孩子的二叉节点。

### 历史 · History

红黑树由 Rudolf Bayer 于 1972 年提出（原称 symmetric binary B-trees），1978 年由 Leonidas J. Guibas 与 Robert Sedgewick 正式命名并完善。因实现平衡代价低、删除友好，成为 C++ STL map/set、Java TreeMap、Linux 内核（CFS 调度器、epoll 红黑树）等工业级标准。竞赛中因实现复杂且 std::map 已内置，OI 界极少手写。

## How · 实现

### 伪代码

```python
性质检查: 根黑 / 红父黑子 / 黑高一致

insert(z):
  BST 插入，z 着红
  while z 的父 p 为红:
    u = p 的兄弟(叔)
    if u 为红:  p,u 变黑，g 变红，z=g   # 变色上移
    else:
      if z 与 p 不在同一侧: 旋转 p，z=p  # LR/RL
      p 变黑，g 变红，旋转 g             # LL/RR
  根染黑

delete(z):
  标准 BST 删除；若删的是黑节点引入双黑，按四情形
  (兄弟红转 / 兄弟黑侄子全黑变红上移 / 侄子红旋转) 处理
```

### Python 实现

```python
class RBNode:
    __slots__ = ('val', 'red', 'left', 'right', 'parent')
    def __init__(self, val):
        self.val = val
        self.red = True
        self.left = None
        self.right = None
        self.parent = None


class RBTree:
    def __init__(self):
        self.NIL = RBNode(None)
        self.NIL.red = False
        self.root = self.NIL

    def _leaf(self, v):
        n = RBNode(v)
        n.left = n.right = self.NIL
        return n

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left is not self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is self.NIL:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right is not self.NIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is self.NIL:
            self.root = y
        elif x is x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def insert(self, v):
        z = self._leaf(v)
        y = self.NIL
        x = self.root
        while x is not self.NIL:
            y = x
            x = x.left if v < x.val else x.right
        z.parent = y
        if y is self.NIL:
            self.root = z
        elif v < y.val:
            y.left = z
        else:
            y.right = z
        self._insert_fix(z)

    def _insert_fix(self, z):
        while z.parent.red:
            p = z.parent
            g = p.parent
            if p is g.left:
                u = g.right
                if u.red:                  # 叔红：变色上移
                    p.red = u.red = False
                    g.red = True
                    z = g
                else:                      # 叔黑：旋转
                    if z is p.right:       # LR -> 转 LL
                        z = p
                        self._left_rotate(z)
                    p = z.parent
                    p.red = False
                    g.red = True
                    self._right_rotate(g)
            else:                          # 对称：p 是右孩子
                u = g.left
                if u.red:
                    p.red = u.red = False
                    g.red = True
                    z = g
                else:
                    if z is p.left:        # RL -> 转 RR
                        z = p
                        self._right_rotate(z)
                    p = z.parent
                    p.red = False
                    g.red = True
                    self._left_rotate(g)
        self.root.red = False

    def _transplant(self, u, v):
        if u.parent is self.NIL:
            self.root = v
        elif u is u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _minimum(self, x):
        while x.left is not self.NIL:
            x = x.left
        return x

    def delete(self, v):
        z = self._find(v)
        if z is self.NIL:
            return
        y = z
        y_red = y.red
        if z.left is self.NIL:
            x = z.right
            self._transplant(z, z.right)
        elif z.right is self.NIL:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_red = y.red
            x = y.right
            if y.parent is z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.red = z.red
        if not y_red:
            self._delete_fix(x)

    def _delete_fix(self, x):
        while x is not self.root and not x.red:
            if x is x.parent.left:
                w = x.parent.right
                if w.red:                       # 情形1：兄弟红
                    w.red = False
                    x.parent.red = True
                    self._left_rotate(x.parent)
                    w = x.parent.right
                if not w.left.red and not w.right.red:   # 情形2：侄子全黑
                    w.red = True
                    x = x.parent
                else:                           # 情形3/4：侄子有红
                    if not w.right.red:
                        w.left.red = False
                        w.red = True
                        self._right_rotate(w)
                        w = x.parent.right
                    w.red = x.parent.red
                    x.parent.red = False
                    w.right.red = False
                    self._left_rotate(x.parent)
                    x = self.root
            else:                               # 对称
                w = x.parent.left
                if w.red:
                    w.red = False
                    x.parent.red = True
                    self._right_rotate(x.parent)
                    w = x.parent.left
                if not w.right.red and not w.left.red:
                    w.red = True
                    x = x.parent
                else:
                    if not w.left.red:
                        w.right.red = False
                        w.red = True
                        self._left_rotate(w)
                        w = x.parent.left
                    w.red = x.parent.red
                    x.parent.red = False
                    w.left.red = False
                    self._right_rotate(x.parent)
                    x = self.root
        x.red = False

    def _find(self, v):
        x = self.root
        while x is not self.NIL:
            if v == x.val:
                return x
            x = x.left if v < x.val else x.right
        return self.NIL

    def search(self, v):
        return self._find(v) is not self.NIL

    def inorder(self):
        out = []
        def dfs(x):
            if x is self.NIL:
                return
            dfs(x.left)
            out.append(x.val)
            dfs(x.right)
        dfs(self.root)
        return out

    def height(self):
        def go(x):
            if x is self.NIL:
                return 0
            return 1 + max(go(x.left), go(x.right))
        return go(self.root)


def _rb_valid(t):
    if t.root is t.NIL:
        return True, 0
    if t.root.red:
        return False, 0
    bh = None
    def go(x):
        nonlocal bh
        if x is t.NIL:
            return 1
        if x.red and (x.left.red or x.right.red):
            return None                      # 红不连续
        l = go(x.left)
        r = go(x.right)
        if l is None or r is None or l != r:
            return None                      # 黑高不一致
        return l + (0 if x.red else 1)
    b = go(t.root)
    return b is not None, b or 0


if __name__ == "__main__":
    import random
    random.seed(17)
    t = RBTree()
    arr = []
    for _ in range(2000):
        v = random.randint(0, 100000)
        t.insert(v)
        arr.append(v)
    assert t.inorder() == sorted(arr)
    ok, bh = _rb_valid(t)
    assert ok, "RB property broken"
    assert t.height() <= 2 * bh + 2, (t.height(), bh)
    # 有序插入也保持平衡
    t2 = RBTree()
    for i in range(3000):
        t2.insert(i)
    ok2, bh2 = _rb_valid(t2)
    assert ok2 and t2.height() < 40
    # 删除一半
    uniq = sorted(set(arr))
    removed = set(uniq[:len(uniq) // 2])
    for v in removed:
        while t.search(v):
            t.delete(v)
    expect = sorted(a for a in arr if a not in removed)
    assert t.inorder() == expect
    ok3, _ = _rb_valid(t)
    assert ok3
    print("All tests passed.")
```

**PyPy 提示**: 红黑树在 Python 中实现复杂（父指针+NIL 哨兵+双黑修复），性能与可读性都不如 FHQ-Treap。竞赛 Python 直接用内置 sortedcontainers 或 bisect 即可，勿手写。此节点用于理解 std::map 与 2-3-4 树思想。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 查找/插入/删除严格 O(log n)（树高 ≤2·log2(n+1)） |
| 空间 | O(n) |

### 局限

实现与调试成本远高于其他平衡树；仅提供单点操作，无区间操作/可持久化扩展；竞赛中手写红黑树几乎无必要（std::map 已内置）。理解价值大于实用价值。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3369 | 4 | 普通平衡树：红黑树完整实现（OI Wiki 提供） | [https://www.luogu.com.cn/problem/P3369](https://www.luogu.com.cn/problem/P3369) |
| Luogu | P6136 | 5 | 普通平衡树加强版：考验删除修复情形覆盖 | [https://www.luogu.com.cn/problem/P6136](https://www.luogu.com.cn/problem/P6136) |

## Pitfalls · 易错点

- NIL 哨兵不统一（每节点独立 NIL 或全局 NIL 混用）导致父指针错误
- 插入修复把 LR/RL 的中间旋转顺序写反
- 删除双黑修复漏掉兄弟红的情形导致黑高失衡
- 把黑高性质误当成「路径黑节点数」而忽略 NIL 叶子计数

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/rbtree/](https://oi-wiki.org/ds/rbtree/)
- 书籍 ✓ `CLRS《算法导论》ch13 红黑树`
