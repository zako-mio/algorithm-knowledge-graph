---
id: splay
name: Splay(伸展树)
group: G-A-8
stage: advanced
priority: P1
depth_tier: standard
---

# Splay(伸展树)

> 伸展操作将访问节点旋至根，均摊O(log n)，LCT基础

<!-- 元信息: id=splay · group=G-A-8 · stage=advanced · priority=P1 · depth_tier=standard -->

## What · 是什么

Splay 树（伸展树）由 Daniel Sleator 与 Robert Tarjan 于 1985 年发明，是一种自调整平衡二叉搜索树。每次访问（查找/插入/删除/查询）后，都通过伸展(splay)操作把被访问节点旋转到根，树结构随之自调整。任意连续 m 次操作总时间 O((m+n) log n)，即均摊 O(log n)，无需额外平衡信息、常数小，且是 LCT（Link-Cut Tree）的基础。

## Why · 为什么

### 直觉 · Intuition

「刚访问的节点很可能很快再次被访问」——把最近访问的节点提到根，使后续访问路径变短。长期看，频繁访问的节点总在浅层，低频节点在深层，天然满足访问局部性，无需维护任何高度/大小信息，纯靠旋转自适应。

### 原理 · Principle

伸展操作由三种基本步骤组成：①zig：x 的父节点 p 是根时，直接单旋 x；②zig-zig：x 与 p 同为左/右子时，先旋 p 再旋 x（连续同向双旋）；③zig-zag：x 与 p 方向相反时，先旋 x 再旋 x（两次单旋）。zig 仅在 x 深度为奇数时作为最后一步执行。每步使 x 离根更近。均摊分析用势能法：设势能 Φ = Σ log(size 子树)，一次 splay 的均摊代价为 O(log n)，从而 m 次操作均摊 O((m+n)log n)。访问路径上的所有节点信息沿路自下而上更新，因此 splay 到根可完成整条路径的信息维护（LCT 关键）。

### 历史 · History

1985 年由 Sleator 与 Tarjan 提出（论文 Self-Adjusting Binary Search Trees），开创自调整数据结构流派。1987 年用于网络流 Dinic 扩展；后来成为 LCT 的基础（1997 年 Sleator-Tarjan 提出动态树）。OI 界因其实现在数组模拟下简洁、支持区间操作而广为使用，LOJ/P3369 等模板皆以其为范例。

## How · 实现

### 伪代码

```python
rotate(x):           # 单旋：x 与父交换位置（左/右两种）
  y = fa[x]; z = fa[y]
  若 x 是 y 的右子: y.right = x.left; x.left = y
  否则:           y.left = x.right; x.right = y
  fa[x] = z; 更新 y.size, x.size; fa[y] = x
  (z 相应左右指针指向 x)

splay(x, goal=0):   # 将 x 旋到 goal 之下(默认根)
  while fa[x] != goal:
    y = fa[x]; z = fa[y]
    if z == goal: rotate(x)                # zig
    elif dir(x)==dir(y): rotate(y); rotate(x)  # zig-zig
    else: rotate(x); rotate(x)                  # zig-zag

insert(val):
  按 BST 找到空位插入 x; splay(x)

find(val):
  按 BST 找 x; splay(x)   # 不存在则 splay 最后访问节点

delete(val):
  splay(待删节点); 断开左右子树再合并

区间操作(l,r): 将 l-1 splay 到根，r+1 splay 到根右子，则 [l,r] 整体在 r+1 的左子树
```

### Python 实现

```python
class SplayTree:
    def __init__(self):
        self.val = [0]   # 哨兵0：占位；节点 1-indexed
        self.ch = [[0, 0]]
        self.fa = [0]
        self.size = [0]
        self.rev = [False]
        for v in (-10**18, 10**18):
            self._new(v)
        self.root = 1
        self.ch[1][1] = 2
        self.fa[2] = 1
        self._pull(1)

    def _new(self, v):
        self.val.append(v)
        self.ch.append([0, 0])
        self.fa.append(0)
        self.size.append(1)
        self.rev.append(False)
        return len(self.val) - 1

    def _pull(self, x):
        self.size[x] = 1 + self.size[self.ch[x][0]] + self.size[self.ch[x][1]]

    def _dir(self, x):
        f = self.fa[x]
        return 1 if self.ch[f][1] == x else 0

    def _push(self, x):
        if self.rev[x]:
            l, r = self.ch[x][0], self.ch[x][1]
            self.ch[x][0], self.ch[x][1] = r, l
            if l:
                self.rev[l] ^= True
            if r:
                self.rev[r] ^= True
            self.rev[x] = False

    def _rotate(self, x):
        y = self.fa[x]
        d = self._dir(x)
        z = self.fa[y]
        b = self.ch[x][d ^ 1]
        if z:
            self.ch[z][self._dir(y)] = x
        self.fa[x] = z
        self.ch[x][d ^ 1] = y
        self.fa[y] = x
        self.ch[y][d] = b
        if b:
            self.fa[b] = y
        self._pull(y)
        self._pull(x)

    def _splay_to(self, x, goal=0):
        path = []
        cur = x
        while cur and cur != goal:
            path.append(cur)
            cur = self.fa[cur]
        for node in reversed(path):
            self._push(node)
        while self.fa[x] != goal:
            y = self.fa[x]
            z = self.fa[y]
            if z and z != goal:
                if self._dir(x) == self._dir(y):
                    self._rotate(y)
                else:
                    self._rotate(x)
            self._rotate(x)
        if goal == 0:
            self.root = x

    def _splay(self, x):
        self._splay_to(x, 0)

    def _find_node(self, k):
        x = self.root
        while True:
            self._push(x)
            l = self.ch[x][0]
            if self.size[l] + 1 == k:
                return x
            if k <= self.size[l]:
                x = l
            else:
                k -= self.size[l] + 1
                x = self.ch[x][1]

    def _find(self, k):
        x = self._find_node(k)
        self._splay(x)
        return x

    def insert(self, val):
        x = self.root
        while True:
            self._push(x)
            if val < self.val[x]:
                if not self.ch[x][0]:
                    self.ch[x][0] = self._new(val)
                    self.fa[self.ch[x][0]] = x
                    self._splay(self.ch[x][0])
                    return
                x = self.ch[x][0]
            else:
                if not self.ch[x][1]:
                    self.ch[x][1] = self._new(val)
                    self.fa[self.ch[x][1]] = x
                    self._splay(self.ch[x][1])
                    return
                x = self.ch[x][1]

    def reverse_range(self, l, r):
        a = self._find(l - 1)
        b = self._find_node(r + 1)
        self._splay_to(b, a)
        node = self.ch[self.ch[self.root][1]][0]
        if node:
            self.rev[node] ^= True
            self._push(node)

    def inorder(self):
        out = []
        def dfs(x):
            if not x:
                return
            self._push(x)
            dfs(self.ch[x][0])
            out.append(self.val[x])
            dfs(self.ch[x][1])
        dfs(self.root)
        return out


if __name__ == "__main__":
    import random
    s = SplayTree()
    for v in [3, 1, 4, 1, 5, 9, 2, 6]:
        s.insert(v)
    mid = s.inorder()
    assert mid == sorted([-10**18, 10**18, 3, 1, 4, 1, 5, 9, 2, 6]), mid
    t = SplayTree()
    for v in [10, 20, 30, 40, 50]:
        t.insert(v)
    t.reverse_range(2, 4)
    got = t.inorder()[1:-1]
    assert got == [30, 20, 10, 40, 50], got
    rng = random.Random(3)
    base = list(range(1, 30))
    t2 = SplayTree()
    for v in base:
        t2.insert(v)
    exp = base[:]
    for step in range(200):
        l = rng.randint(2, len(base) - 1)
        r = rng.randint(l, len(base))
        t2.reverse_range(l, r)
        exp[l - 2:r - 1] = exp[l - 2:r - 1][::-1]
    assert t2.inorder()[1:-1] == exp
    print("All tests passed.")

```

**PyPy 提示**: Splay 用数组模拟时注意 0 作为空指针哨兵，所有 val 数组 1-indexed；_splay 收尾逻辑要保证最后一步是 zig/zig-zig（奇数深度时多旋一次）。区间操作借助 ±inf 两个哨兵避免 l-1/r+1 越界。PyPy 下整体常数较大，但均摊保证稳定。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 单次操作最坏 O(n)，m 次连续操作均摊 O(log n)（势能法证明） |
| 空间 | O(n) |

### 局限

单次操作无最坏保证，不适合实时性要求强的场景；代码较长易错（旋转/哨兵/下传顺序）。主要价值：LCT 基础、区间翻转/区间插入删除（序列 Splay）。纯平衡树需求下 Python 选手通常更愿用 FHQ-Treap。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3391 | 5 | 文艺平衡树：区间翻转，序列 Splay 经典题 | [https://www.luogu.com.cn/problem/P3391](https://www.luogu.com.cn/problem/P3391) |
| Luogu | P2042 | 7 | NOI2005 维护数列：区间插入/删除/翻转/最大子段和 | [https://www.luogu.com.cn/problem/P2042](https://www.luogu.com.cn/problem/P2042) |
| Luogu | P2596 | 6 | ZJOI2006 书架：按编号定位+splay到根 | [https://www.luogu.com.cn/problem/P2596](https://www.luogu.com.cn/problem/P2596) |
| LOJ | 105 | 5 | 文艺平衡树模板：区间翻转 splay 实现 | [https://loj.ac/problem/105](https://loj.ac/problem/105) |

## Pitfalls · 易错点

- splay 循环里把 zig-zig/zig-zag 分支顺序写错，导致旋转次数不对称
- 哨兵 -inf/+inf 未建立导致区间边界访问空节点
- 下传懒标记 push 时机错误：splay/旋转前未 push 路径上节点
- 删除后未 splay 导致均摊复杂度退化（每个操作后都必须伸展）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/splay/](https://oi-wiki.org/ds/splay/)
- 论文 ✓ `Sleator & Tarjan, Self-Adjusting Binary Search Trees, JACM 1985`
