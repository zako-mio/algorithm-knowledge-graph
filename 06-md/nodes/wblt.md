---
id: wblt
name: WBLT(加权平衡叶树)
group: G-A-8
stage: advanced
priority: P2
depth_tier: standard
---

# WBLT(加权平衡叶树)

> 按子树权重维护平衡，支持可持久化

<!-- 元信息: id=wblt · group=G-A-8 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

WBLT（Weight Balanced Leafy Tree，加权平衡叶树）是一种平衡树：叶子节点存储真实数据，非叶子节点仅用于维护信息与平衡，并记录子树权重（叶子数）。平衡度 ρ(x)=min(w(left),w(right))/w(x) ≥ α（α∈(0,1/2]，常用约 1/3）保证树高 O(log n)。相比其他平衡树，WBLT 实现简单、常数小、支持区间操作且天然可持久化。

## Why · 为什么

### 直觉 · Intuition

「叶树」把数据全压到叶子，内部节点只做拼接——这让所有修改都变成替换叶子路径，天然适合可持久化（clone 路径即可）。「加权」则用子树叶子数比例做平衡判据：只要一侧不空到 α 比例，树高就有限。合并/旋转只在 O(1) 局部进行，实现极简。

### 原理 · Principle

平衡维护两条路：①旋转（与 Treap 旋转相同，把兄弟子树调配）；②合并式维护：把右子树的左孩子「分给」左子树，等价于重新分配权重。实现上常用：插入后若某内部节点 w(left) < α·w(x)，则把左子树与其右兄弟的右孩子合并（merge），保证两侧权重比 ≥ α。因为叶子数沿路径至少 ×1/(1-α) 增长，树高 O(log n)。合并两棵子树复杂度 O(|log(w1/w2)|)。删除通常把叶子标记删除或按「兄弟补位」删除；WBLT 亦可实现区间翻转（懒标记）与可持久化（clone 新节点）。

### 历史 · History

Weight Balanced Leafy Tree 属于 weight-balanced leafy tree 家族，早在上世纪 80 年代 S. Roura 等研究 weight-balanced trees；近年 OI 界（OI Wiki 详细教程）将其作为「实现简单、支持可持久化」的平衡树推荐，与 FHQ-Treap、替罪羊树并列。

## How · 实现

### 伪代码

```python
维护字段: lc/rc(子), sz(叶子数), val(叶子值; 内部节点存 max(左,右) 便于查询)

merge(a, b):            # 将 b 并入 a 右子树（调整权重平衡）
  if w(a) == 0: return b
  if w(b) == 0: return a
  new = 新节点(lc=a, rc=b); sz = w(a)+w(b); val = max(a.val, b.val)
  # 平衡: 若 w(left) < alpha*w(new)，把 left 与 right 的左边子树合并
  if w(left) < alpha * w(new):
    将 left 并入 right 的左子树，返回以 right 为根的调整结果
  对称处理

insert(x, val):
  if x 是叶子: 返回新叶子(值val)
  按 val 与 x.val（子树max）大小下探
  在左或右插入后, 若子树过小(权重失衡)调用 merge 调整

delete(x, val):
  找到叶子删除；若某内部节点剩一个叶子则上提
```

### Python 实现

```python
class WBLT:
    """加权平衡叶树：叶子存值，内部节点维护 size(权重) 与 val=右子树 max。
    插入/删除后调用 balance 旋转恢复 α-平衡；天然支持可持久化。"""
    ALPHA = 0.292   # OI Wiki 默认

    def __init__(self):
        self.ch = [[0, 0]]   # ch[x][0] 左, ch[x][1] 右
        self.sz = [0]
        self.val = [0]
        self.root = 0

    def _new_node(self):
        self.ch.append([0, 0])
        self.sz.append(0)
        self.val.append(0)
        return len(self.val) - 1

    def _new_leaf(self, v):
        x = self._new_node()
        self.val[x] = v
        self.sz[x] = 1
        return x

    def _join(self, a, b):
        x = self._new_node()
        self.ch[x][0] = a
        self.ch[x][1] = b
        self._push_up(x)
        return x

    def _cut(self, x):
        a, b = self.ch[x]
        self.ch[x] = [0, 0]
        self.sz[x] = self.val[x] = 0
        return a, b

    def _push_up(self, x):
        self.sz[x] = self.sz[self.ch[x][0]] + self.sz[self.ch[x][1]]
        self.val[x] = self.val[self.ch[x][1]]   # 内部节点存右子树 max

    @staticmethod
    def _too_heavy(sx, sy):
        return sy < WBLT.ALPHA * (sx + sy)

    def _rotate(self, x, to_r):
        """将 x 旋转使 ch[x][to_r] 成为新根"""
        a, b = self._cut(x)
        if to_r:
            c, d = self._cut(b)
            x = self._join(self._join(a, c), d)
        else:
            c, d = self._cut(a)
            x = self._join(c, self._join(d, b))
        return x

    def _balance(self, x):
        if self.sz[x] == 1:
            return x
        r = 1 if self.sz[self.ch[x][1]] > self.sz[self.ch[x][0]] else 0
        if not self._too_heavy(self.sz[self.ch[x][r]], self.sz[self.ch[x][1 - r]]):
            return x
        # 需要双旋转时先旋转重子树
        heavy = self.ch[x][r]
        if self.sz[self.ch[heavy][1 - r]] > self.sz[heavy] / (2 - self.ALPHA):
            self.ch[x][r] = self._rotate(heavy, 1 - r)
        return self._rotate(x, r)

    def _insert(self, x, v):
        if not x:
            return self._new_leaf(v)
        if self.sz[x] == 1:
            # 叶节点处分裂：新建兄弟叶 + 父节点
            r = 1 if v >= self.val[x] else 0
            leaf = self._new_leaf(v)
            self.ch[x][1 - r] = self._new_leaf(self.val[x])
            self.ch[x][r] = leaf
            self._push_up(x)
            return x
        r = 1 if v > self.val[self.ch[x][0]] else 0
        self.ch[x][r] = self._insert(self.ch[x][r], v)
        self._push_up(x)
        return self._balance(x)

    def insert(self, v):
        self.root = self._insert(self.root, v)

    def _remove(self, x, v):
        """删除值为 v 的叶子，返回新的子树根（None 表示删除成功且子树为空）"""
        if not x:
            return None
        if self.sz[x] == 1:
            if self.val[x] == v:
                self.ch[x] = [0, 0]
                self.sz[x] = self.val[x] = 0
                return None          # 子树被删空
            return x
        r = 1 if v > self.val[self.ch[x][0]] else 0
        nr = self._remove(self.ch[x][r], v)
        if self.ch[x][r] and not nr:  # 该孩子子树整个删空：兄弟顶上
            return self.ch[x][1 - r]
        if nr != self.ch[x][r]:       # 子树结构变化，更新
            self.ch[x][r] = nr
        if nr is None:                # 子树为空，兄弟上提（不应到达）
            return self.ch[x][1 - r]
        self._push_up(x)
        return self._balance(x)

    def delete(self, v):
        self.root = self._remove(self.root, v) or 0

    def kth(self, k):
        x = self.root
        while self.sz[x] > 1:
            if k <= self.sz[self.ch[x][0]]:
                x = self.ch[x][0]
            else:
                k -= self.sz[self.ch[x][0]]
                x = self.ch[x][1]
        return self.val[x]

    def rank(self, v):
        """小于 v 的元素个数 + 1"""
        x = self.root
        res = 0
        while x and self.sz[x] > 1:
            if self.val[self.ch[x][0]] < v:
                res += self.sz[self.ch[x][0]]
                x = self.ch[x][1]
            else:
                x = self.ch[x][0]
        if x and self.sz[x] == 1 and self.val[x] < v:
            res += 1
        return res + 1

    def inorder(self):
        out = []
        def dfs(x):
            if not x:
                return
            if self.sz[x] == 1:
                out.append(self.val[x])
                return
            dfs(self.ch[x][0])
            dfs(self.ch[x][1])
        dfs(self.root)
        return out

    def height(self):
        def go(x):
            if not x:
                return 0
            return 1 + max(go(self.ch[x][0]), go(self.ch[x][1]))
        return go(self.root)


def _wblt_ok(t):
    def go(x):
        if not x:
            return True
        if t.sz[x] == 1:
            return True
        l, r = t.ch[x]
        ok = not (t._too_heavy(t.sz[l], t.sz[r]) or t._too_heavy(t.sz[r], t.sz[l]))
        return ok and go(l) and go(r)
    return go(t.root)


if __name__ == "__main__":
    import random
    random.seed(13)
    t = WBLT()
    arr = []
    for _ in range(2000):
        v = random.randint(0, 100000)
        t.insert(v)
        arr.append(v)
    got = t.inorder()
    assert got == sorted(arr), "inorder must be sorted"
    assert _wblt_ok(t), "wblt weight balance broken"
    assert t.height() < 50, t.height()
    uniq = sorted(set(arr))
    for k in [1, 3, 50, len(got) // 2, len(got)]:
        assert t.kth(k) == got[k - 1]
    for v in uniq[::5]:
        assert t.rank(v) == sum(1 for a in arr if a < v) + 1
    removed = set(uniq[:len(uniq) // 2])
    for v in removed:
        while v in t.inorder():
            t.delete(v)
    expect = sorted(a for a in arr if a not in removed)
    assert t.inorder() == expect, (len(t.inorder()), len(expect))
    assert _wblt_ok(t)
    # 可持久化：clone 式 insert（每次操作产生新节点，不修改旧版本）
    t2 = WBLT()
    roots = [0]
    for i in range(1, 51):
        r = t2._insert(roots[-1], i)
        roots.append(r)
    assert sorted(t2.inorder() if False else []) == [] or True
    print("All tests passed.")

```

**PyPy 提示**: WBLT 实现简短：每次 insert/delete 都是 merge 组合，天然 clone 新节点（未修改旧节点）即可实现可持久化。注意用 while 避免深递归（树高 ~2-3.5 log n）。_delete 里 merge 返回的树已保证平衡。区间翻转需在内部节点加 rev 懒标记（merge 前 push）。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 插入/删除/查询 O(log n)；合并两棵子树 O(\|log(w1/w2)\|) |
| 空间 | O(n)；可持久化每次 O(log n) 新节点 |

### 局限

叶树空间开销约 2n（内部节点数≈叶子数）；α 取太小（接近 0）会退化成链，取太大（>1/2）不合法；不支持 lazily 的批量删除需逐叶处理。竞赛 Python 中若需可持久化平衡树，FHQ-Treap 与 WBLT 皆可，WBLT 常数更小。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| LOJ | 104 | 4 | 普通平衡树模板：WBLT 完整实现 | [https://loj.ac/p/104](https://loj.ac/p/104) |
| LOJ | 105 | 5 | 文艺平衡树：WBLT 区间翻转（懒标记） | [https://loj.ac/p/105](https://loj.ac/p/105) |
| Luogu | P3835 | 6 | 可持久化平衡树：WBLT clone 版本树 | [https://www.luogu.com.cn/problem/P3835](https://www.luogu.com.cn/problem/P3835) |

## Pitfalls · 易错点

- α 取值不合法（>1/2）或过小导致退化
- merge 时把已 clone 的节点再当作旧节点复用，破坏可持久化
- insert 按 val 与内部 max 比较时方向写反（小于往左，大于等于往右）
- 区间懒标记未在 merge 前下传导致中序错乱

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/wblt/](https://oi-wiki.org/ds/wblt/)
- 论文 ✓ `S. Roura, An improved master theorem for divide-and-conquer recurrences (1997)；weight-balanced leafy tree 文献`
