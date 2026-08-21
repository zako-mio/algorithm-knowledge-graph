---
id: sbt
name: Size Balanced Tree(SBT)
group: G-A-8
stage: advanced
priority: P2
depth_tier: standard
---

# Size Balanced Tree(SBT)

> 按子树size维护平衡，O(log n)操作

<!-- 元信息: id=sbt · group=G-A-8 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

Size Balanced Tree（SBT，大小平衡树）由中国 OI 选手陈启峰（chenqifeng）2007 年提出，是一种自平衡二叉搜索树。每个节点额外维护以自身为根的子树节点数 size，通过旋转维持「任意节点的 size 不小于其兄弟节点的所有子节点的 size」这一平衡条件，从而保证 O(log n) 的树高与操作复杂度，且能高效支持 rank/按 rank 取值的排名查询。

## Why · 为什么

### 直觉 · Intuition

只依赖 size 字段就能判定失衡：一个节点若被「孙子」超过，说明某侧子树过重。SBT 的平衡条件保证任意节点的左/右子树高度差被限制在常数倍内（实际最多 2 倍），因此树高 O(log n)。旋转发生在递归返回路径上，且一次旋转后失衡会向根传播，需要 loop 检查。

### 原理 · Principle

平衡条件（对任意节点 N）：size(N.left) ≥ size(N.right.left)，size(N.left) ≥ size(N.right.right)，size(N.right) ≥ size(N.left.left)，size(N.right) ≥ size(N.left.right)——即节点 size 不小于其兄弟的孙 size。维护操作 maintain(x)：插入发生在左子树且 size(左左) > size(右) 时右旋；size(左右) > size(右) 时先左旋左子树再右旋，递归 maintain 直到无需调整；右子树对称。由于每层至多常数次旋转、每操作路径 O(log n)，总复杂度 O(log n)。

### 历史 · History

SBT 由陈启峰于 2007 年在中国提出，最早在 2007 年 NOI 冬令营/集训队论文中系统阐述，之后成为中国竞赛圈常见的平衡树实现，以旋转直接、常数小、代码量适中著称。OI Wiki 设有专门页面介绍其性质与维护算法。

## How · 实现

### 伪代码

```python
maintain(x):               # 在插入/删除后调用恢复平衡
  if size(x.left) < size(x.right.left):        # 情况1：右子左孙过大
    右旋(right)?? 用旋转组合处理
  ...四种失衡形态(l/r 子孙过大)分别做旋转
  递归 maintain 左/右子树至稳定

insert(x, val):
  if val < x.val: insert(x.left, val)
  else: insert(x.right, val)
  push_up(x); maintain(x)

delete(x, val):   # 叶子直接删；单子顶替；双子用前驱/后继替换
  与 BST 删除一致，回溯 push_up + maintain
```

### Python 实现

```python
class SBT:
    def __init__(self):
        self.val = [0]
        self.ch = [[0, 0]]
        self.sz = [0]
        self.root = 0

    def _new(self, v):
        self.val.append(v)
        self.ch.append([0, 0])
        self.sz.append(1)
        return len(self.val) - 1

    def _pull(self, x):
        self.sz[x] = 1 + self.sz[self.ch[x][0]] + self.sz[self.ch[x][1]]

    def _rr(self, x):   # 右旋：x 的左儿子上浮
        y = self.ch[x][0]
        self.ch[x][0] = self.ch[y][1]
        self.ch[y][1] = x
        self._pull(x)
        self._pull(y)
        return y

    def _lr(self, x):   # 左旋：x 的右儿子上浮
        y = self.ch[x][1]
        self.ch[x][1] = self.ch[y][0]
        self.ch[y][0] = x
        self._pull(x)
        self._pull(y)
        return y

    def fix(self, x):
        """SBT 平衡维护（OI Wiki 四情形 + fixBalance 递归）"""
        if not x:
            return x
        l, r = self.ch[x][0], self.ch[x][1]
        if self.sz[l] < self.sz[self.ch[r][0]]:      # Case1: 右左孙子过大
            self.ch[x][1] = self._rr(r)
            x = self._lr(x)
            self.ch[x][0] = self.fix(self.ch[x][0])
            self.ch[x][1] = self.fix(self.ch[x][1])
            x = self.fix(x)
        elif self.sz[l] < self.sz[self.ch[r][1]]:    # Case2: 右右孙子过大
            x = self._lr(x)
            self.ch[x][0] = self.fix(self.ch[x][0])
            x = self.fix(x)
        elif self.sz[r] < self.sz[self.ch[l][0]]:    # Case3: 左左孙子过大
            x = self._rr(x)
            self.ch[x][1] = self.fix(self.ch[x][1])
            x = self.fix(x)
        elif self.sz[r] < self.sz[self.ch[l][1]]:    # Case4: 左右孙子过大
            self.ch[x][0] = self._lr(l)
            x = self._rr(x)
            self.ch[x][0] = self.fix(self.ch[x][0])
            self.ch[x][1] = self.fix(self.ch[x][1])
            x = self.fix(x)
        return x

    def _insert(self, x, v):
        if not x:
            return self._new(v)
        if v < self.val[x]:
            self.ch[x][0] = self._insert(self.ch[x][0], v)
        else:
            self.ch[x][1] = self._insert(self.ch[x][1], v)
        self._pull(x)
        return self.fix(x)

    def insert(self, v):
        self.root = self._insert(self.root, v)

    def _find(self, x, v):
        while x and self.val[x] != v:
            x = self.ch[x][0] if v < self.val[x] else self.ch[x][1]
        return x

    def search(self, v):
        return self._find(self.root, v) != 0

    def _erase(self, x, v):
        """删除：叶子直接删；单子顶替；双子用左子树最大节点(前驱)替换"""
        if not x:
            return 0
        if v < self.val[x]:
            self.ch[x][0] = self._erase(self.ch[x][0], v)
        elif v > self.val[x]:
            self.ch[x][1] = self._erase(self.ch[x][1], v)
        else:
            if not self.ch[x][0]:
                return self.ch[x][1]
            if not self.ch[x][1]:
                return self.ch[x][0]
            p = self.ch[x][0]
            while self.ch[p][1]:
                p = self.ch[p][1]
            self.val[x] = self.val[p]
            self.ch[x][0] = self._erase(self.ch[x][0], self.val[p])
        self._pull(x)
        return self.fix(x)

    def delete(self, v):
        self.root = self._erase(self.root, v)

    def kth(self, k):
        x = self.root
        while x:
            ls = self.sz[self.ch[x][0]]
            if k == ls + 1:
                return self.val[x]
            if k <= ls:
                x = self.ch[x][0]
            else:
                k -= ls + 1
                x = self.ch[x][1]
        raise ValueError("k out of range")

    def rank(self, v):
        """小于 v 的元素个数 + 1"""
        x = self.root
        r = 1
        while x:
            if v <= self.val[x]:
                x = self.ch[x][0]
            else:
                r += self.sz[self.ch[x][0]] + 1
                x = self.ch[x][1]
        return r

    def inorder(self):
        out = []
        def dfs(x):
            if not x:
                return
            dfs(self.ch[x][0])
            out.append(self.val[x])
            dfs(self.ch[x][1])
        dfs(self.root)
        return out


def balanced(t):
    def go(x):
        if not x:
            return True
        l, r = t.ch[x][0], t.ch[x][1]
        ok = t.sz[l] >= t.sz[t.ch[r][0]] and t.sz[l] >= t.sz[t.ch[r][1]] \
             and t.sz[r] >= t.sz[t.ch[l][0]] and t.sz[r] >= t.sz[t.ch[l][1]]
        return ok and go(l) and go(r)
    return go(t.root)


def height(t):
    def go(x):
        if not x:
            return 0
        return 1 + max(go(t.ch[x][0]), go(t.ch[x][1]))
    return go(t.root)


if __name__ == "__main__":
    import random
    random.seed(5)
    t = SBT()
    arr = []
    for _ in range(2000):
        v = random.randint(0, 100000)
        t.insert(v)
        arr.append(v)
    got = t.inorder()
    assert got == sorted(arr)
    assert balanced(t)
    assert height(t) <= 60, height(t)
    uniq = sorted(set(arr))
    for v in uniq[::7]:
        assert t.rank(v) == sum(1 for a in arr if a < v) + 1
    for k in [1, 3, 50, len(got) // 2, len(got)]:
        assert t.kth(k) == got[k - 1]
    removed = set(uniq[:len(uniq) // 2])
    for v in removed:
        while t.search(v):
            t.delete(v)
    got2 = t.inorder()
    expect2 = sorted(a for a in arr if a not in removed)
    assert got2 == expect2, (len(got2), len(expect2))
    assert balanced(t)
    assert height(t) <= 60
    print("All tests passed.")

```

**PyPy 提示**: SBT 维护代码略繁但无递归风险（平衡树高 ~log n），Python 可实现。旋转次数多但每次 O(1)；注意 _maintain 递归调用自身可能多层，但层数受 size 平衡限制。duplicate 处理同 BST（右子树允许等值）。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 插入/删除/查找/排名 O(log n)；维护旋转均摊 O(1) 次每次 O(log n) 递归 |
| 空间 | O(n) |

### 局限

实现较繁琐（四形态维护递归）；删除实现有陷阱（用前驱替换后需对左子树递归维护）；实际竞赛 Python 中用 FHQ-Treap 更简洁。SBT 无区间操作支持，无随机化、严格平衡保证但常数比红黑树小。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3369 | 4 | 普通平衡树：SBT 完整实现校验 | [https://www.luogu.com.cn/problem/P3369](https://www.luogu.com.cn/problem/P3369) |

## Pitfalls · 易错点

- _maintain 递归条件用错 size 关系（把 size(兄弟孙) 写成 size(兄弟)）
- 删除双子节点后漏掉对左子树的递归 maintain
- kth/rank 中 size 未及时 push_up 导致结果偏移
- 把 SBT 平衡条件与 AVL 高度条件混淆，误判失衡

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/sbt/](https://oi-wiki.org/ds/sbt/)
- 论文 ✓ `陈启峰《Size Balanced Tree》集训队论文 2007`
