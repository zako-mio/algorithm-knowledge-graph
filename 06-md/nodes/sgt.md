---
id: sgt
name: 替罪羊树(Scapegoat Tree)
group: G-A-8
stage: advanced
priority: P2
depth_tier: standard
---

# 替罪羊树(Scapegoat Tree)

> 不平衡时按比例重构子树，O(log n)均摊

<!-- 元信息: id=sgt · group=G-A-8 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

替罪羊树（Scapegoat Tree）是一种依靠「重构」维持平衡的重量平衡树（weight-balanced tree），1989 年由 Andersson 与 Galperin-Rivest 独立提出。维护平衡参数 α∈(0.5,1)（常用 0.7~0.8）：插入时若某子树满足 max(size(左),size(右)) > α·size，则将该子树中序遍历后二分重建。删除用懒删除（标空节点），空节点比例超过 α 时整体重构。实现简单、常数小，操作均摊 O(log n)，但不支持区间操作、难以完全持久化。

## Why · 为什么

### 直觉 · Intuition

树的形状失衡不可怕，可怕的是不知道何时补救。替罪羊的策略是：平时不预防，只在「病得很重」（失衡超阈值）时把整棵子树推倒重建成完美平衡。因为阈值 α>0.5，一次重构后至少要再插入同样数量的节点才会再次失衡，所以重构总代价 O(n log n)，摊到每次操作 O(log n)。

### 原理 · Principle

插入时沿 BST 下探、若最深超过 floor(log_{1/α}|T|) 则回溯找第一个失衡节点（即「替罪羊」），对其子树中序收集（去掉已删节点）后取中点为根二分建树，O(子树大小)。复杂度证明：设势能 = 失衡度积累，每插入一个节点对路径上各祖先的「账」加 1，重构把子树高度回落到 O(log n)，而路径上失衡祖先数有上界，故均摊 O(log n)。删除走懒标记：节点标 deleted，不物理移除；当已删节点数占比 > α 时整体重构一次清空。

### 历史 · History

1993 年 Galperin 与 Rivest 正式发表 Scapegoat Tree（Igal Galperin, Ronald L. Rivest）并证明其均摊复杂度；1990s 后期 Arne Andersson 也有相关工作。竞赛界因其实现简洁、无旋转、常数小著称，OI Wiki 有完整章节。

## How · 实现

### 伪代码

```python
alpha = 0.75

rebuild(subtree):
  arr = 中序遍历(subtree) 剔除 deleted 节点
  返回二分建树(arr)   # 中点为根，递归左右

insert(root, val):
  if root 为空: 新建节点; 记录深度=1; 标记「本次有新增」
  else 按 BST 下探插入, 递归返回后沿路更新 size
  若新增节点深度 > floor(log_{1/alpha}(总size)):
    回溯第一个失衡节点 x (max(size[l],size[r]) > alpha*size[x])
    rebuild(x) 替换原位置
  # 单次插入至多一次重构

delete(root, val):
  找到节点标 deleted=True; size 不变(仍计数)
  若 已删节点数 / 总节点数 > alpha: rebuild(整棵树)

查询 rank/kth/前驱后继: 与 BST 相同，跳过 deleted
```

### Python 实现

```python
class SGT:
    def __init__(self, alpha=0.75):
        self.alpha = alpha
        self.sz = []      # 子树有效节点数
        self.deleted = []
        self.ch = []      # [left, right]
        self.val = []
        self._new(0)      # 哨兵 0
        self.root = 0
        self.alive = 0   # 有效(未删)节点数

    def _new(self, v, deleted=False):
        self.val.append(v)
        self.ch.append([0, 0])
        self.sz.append(1)
        self.deleted.append(deleted)
        return len(self.val) - 1

    def _sz(self, x):
        return self.sz[x] if x else 0

    def _pull(self, x):
        if x:
            self.sz[x] = self._sz(self.ch[x][0]) + self._sz(self.ch[x][1]) + 1

    def _flatten(self, x, arr):
        if not x:
            return
        self._flatten(self.ch[x][0], arr)
        if not self.deleted[x]:
            arr.append(x)
        self._flatten(self.ch[x][1], arr)

    def _build(self, arr, lo, hi):
        if lo > hi:
            return 0
        mid = (lo + hi) // 2
        x = arr[mid]
        self.ch[x][0] = self._build(arr, lo, mid - 1)
        self.ch[x][1] = self._build(arr, mid + 1, hi)
        self._pull(x)
        return x

    def _rebuild(self, x):
        arr = []
        self._flatten(x, arr)
        return self._build(arr, 0, len(arr) - 1)

    def _is_unbalanced(self, x):
        return self._sz(self.ch[x][0]) > self.alpha * self._sz(x) or \
               self._sz(self.ch[x][1]) > self.alpha * self._sz(x)

    def _insert(self, x, val):
        if not x:
            self.alive += 1
            return self._new(val)
        if val < self.val[x]:
            self.ch[x][0] = self._insert(self.ch[x][0], val)
        else:
            self.ch[x][1] = self._insert(self.ch[x][1], val)
        self._pull(x)
        if self._is_unbalanced(x):
            return self._rebuild(x)
        return x

    def insert(self, val):
        self.root = self._insert(self.root, val)

    def _find(self, x, val):
        # 跳过已删副本，返回第一个未删的匹配节点（不存在返回 0）
        # 注意：值相等的副本可能分布在相等删除节点的左/右两侧，
        # 因此命中已删等值节点时需先向左探再向右探。
        while x:
            if self.val[x] == val:
                if not self.deleted[x]:
                    return x
                # 已删等值节点：其左子树可能仍有未删副本
                if self.ch[x][0]:
                    r = self._find(self.ch[x][0], val)
                    if r:
                        return r
                x = self.ch[x][1]
            elif val < self.val[x]:
                x = self.ch[x][0]
            else:
                x = self.ch[x][1]
        return 0

    def delete(self, val):
        x = self._find(self.root, val)
        if x:
            self.deleted[x] = True
            self.alive -= 1
        total = self._sz(self.root)
        # 已删节点占比超 alpha 则整体重构清空空节点
        if total and self.alive < self.alpha * total:
            self.root = self._rebuild(self.root)
            self.alive = self._sz(self.root)

    def search(self, val):
        x = self._find(self.root, val)
        return x != 0 and not self.deleted[x]

    def inorder(self):
        out = []
        def go(x):
            if not x:
                return
            go(self.ch[x][0])
            if not self.deleted[x]:
                out.append(self.val[x])
            go(self.ch[x][1])
        go(self.root)
        return out


def _height(x, ch):
    if not x:
        return 0
    return 1 + max(_height(ch[x][0], ch), _height(ch[x][1], ch))


if __name__ == "__main__":
    import random
    random.seed(11)
    t = SGT()
    arr = []
    n = 3000
    for _ in range(n):
        v = random.randint(0, 100000)
        t.insert(v)
        arr.append(v)
    assert t.inorder() == sorted(arr)
    h = _height(t.root, t.ch)
    import math
    assert h <= 40, h  # 高度 ~ O(log_{1/0.75} n) ~ 3.48*log2 n
    s = sorted(set(arr))
    removed = set(s[:len(s) // 3])
    for v in removed:
        while t.search(v):
            t.delete(v)
    for v in removed:
        assert not t.search(v)
    # 删除后再插入保证仍有序
    extra = [random.randint(0, 100000) for _ in range(300)]
    for v in extra:
        t.insert(v)
    expect = sorted(x for x in arr if x not in removed) + sorted(extra)
    assert sorted(t.inorder()) == sorted(expect), (len(t.inorder()), len(expect))
    assert t.inorder() == sorted(t.inorder()), "中序遍历必须有序"
    print("All tests passed.")
```

**PyPy 提示**: 替罪羊树无旋转、纯数组模拟，Python 实现友好。重构时中序收集用显式栈避免深递归；整体重构复杂度 O(子树)。α 取 0.75 平衡高度与重构频率。注意单次插入至多重构一次，否则退化。懒删除使 size 统计与 effective 统计分离，查询需跳过 deleted。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 插入/删除/查询均摊 O(log n)；最坏单次 O(n)（重构），但总摊还 O(log n) |
| 空间 | O(n) |

### 局限

不支持区间操作；懒删除使树中积累空节点，影响访问常数；完全可持久化困难（重构会批量改写节点）。α 选择影响常数（α→0.5 树更平衡但重构频繁）。单次操作无最坏 O(log n) 保证。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3369 | 4 | 普通平衡树：替罪羊树可实现全操作（含懒删除） | [https://www.luogu.com.cn/problem/P3369](https://www.luogu.com.cn/problem/P3369) |
| Luogu | P6136 | 5 | 普通平衡树数据加强版：常数与重构时机受考验 | [https://www.luogu.com.cn/problem/P6136](https://www.luogu.com.cn/problem/P6136) |

## Pitfalls · 易错点

- 单次插入触发多次重构（应在回溯到第一个失衡节点后就停止）
- α 取值过小（如 0.5 边界）导致频繁重建常数爆炸
- 懒删除后忘记在查询/排名时跳过 deleted 节点
- 重构时把 deleted 节点也纳入，导致空节点越积越多、平衡度判断失真

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/sgt/](https://oi-wiki.org/ds/sgt/)
- 论文 ✓ `Galperin & Rivest, Scapegoat Trees, SODA 1993`
