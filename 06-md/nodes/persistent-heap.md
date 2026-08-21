---
id: persistent-heap
name: 可持久化堆
group: G-D-5
stage: advanced
priority: P2
depth_tier: standard
---

# 可持久化堆

> 可持久化可并堆(左偏树)，常用于k短路问题

<!-- 元信息: id=persistent-heap · group=G-D-5 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

可持久化堆（Persistent Heap）通常指可持久化左偏树：把左偏树的 merge 改为 path copying 版本——每次递归合并时新建节点副本、复用未改动的旧节点，从而保留每个历史版本，支持在任意历史版本上继续操作。由于左偏树的时间复杂度非均摊（单次 merge 严格 O(log n)），持久化后单次操作保证 O(log n)，不会像斐波那契/配对堆那样退化。最经典应用是 k 短路问题（Yen 思想之外的 Eppstein/A* 变体在 OI 中常用『可持久化左偏树』维护候选边集）以及各种『从历史状态分裂出新堆』的场景。OI Wiki 提供参考实现。

## Why · 为什么

### 直觉 · Intuition

普通左偏树 merge 会原地改写沿途节点的右儿子与 dist，破坏旧版本。可持久化只需在 merge 里『遇到要改的节点就新建一个副本再改』，旧节点保持原样；未改的子树直接用旧指针共享。因为每次 merge 只动 O(log n) 个节点，m 次操作总空间 O(m log n)。关键前提：左偏树复杂度是非均摊的（每次 merge O(log n)），所以共享+复制的版本不会像配对堆那样失去均摊保证。

### 原理 · Principle

① 左偏树性质：dist(节点)=dist(右儿子)+1，左偏使 merge 递归深度 O(log n)；② 可持久化 merge(x,y)：若 x 空返回 y；取值小的做新根，但用 new_node 复制 x 得 p（拷贝 val/左儿子/右儿子/dist）；③ p.r = merge(p.r, y)（递归），若左偏性质破坏则交换 p 的左右儿子；更新 dist[p]；④ 返回 p 作为新版本根，旧版本 x 仍完整可用；⑤ 插入/删除同理（插入=merge 单点，删根=merge 左右儿子），每次操作 O(log n) 新建节点，空间 O(m log n)。

### 历史 · History

可持久化堆源于对 Dijkstra/最短路径树与 k 短路的需求：Eppstein 1998 年提出用可持久化堆加速 k 短路。OI 中因『k 短路』『图上第 k 小路径和』等题目普及（如 Luogu P2505 等）。左偏树因其非均摊复杂度成为可持久化堆的标准载体，OI Wiki 将其作为 k 短路预处理的核心工具。

## How · 实现

### 伪代码

```python
merge(x, y):
  if x==0: return y
  if y==0: return x
  if val[x] > val[y]: swap(x, y)
  p = ++cnt                       # 新建节点副本
  lc[p] = lc[x]; v[p] = v[x]; dist[p] = dist[x]
  rc[p] = merge(rc[x], y)         # 递归合并 x 的右儿子与 y
  if dist[lc[p]] < dist[rc[p]]: swap(lc[p], rc[p])
  dist[p] = dist[rc[p]] + 1
  return p
pop(x) = merge(lc[x], rc[x])     # 删除根，产生新版本
insert(x, v) = merge(x, new_node(v))
```

### Python 实现

```python
import heapq
import random


class PersistentLeftistHeap:
    """可持久化左偏树（小根堆）。merge 采用 path copying，保留全部历史版本。"""

    def __init__(self):
        self.val = [0]
        self.l = [0]
        self.r = [0]
        self.dist = [-1]

    def _newnode(self, v):
        idx = len(self.val)
        self.val.append(v); self.l.append(0); self.r.append(0); self.dist.append(0)
        return idx

    def merge(self, x, y):
        """合并两个堆（版本根 x, y），返回新版本根。不改动旧版本。"""
        if x == 0:
            return y
        if y == 0:
            return x
        if self.val[x] > self.val[y]:
            x, y = y, x
        nw = self._newnode(self.val[x])
        self.l[nw] = self.l[x]
        self.r[nw] = self.merge(self.r[x], y)
        if self.dist[self.l[nw]] < self.dist[self.r[nw]]:
            self.l[nw], self.r[nw] = self.r[nw], self.l[nw]
        self.dist[nw] = self.dist[self.r[nw]] + 1
        return nw

    def pop(self, x):
        """删除堆顶，返回 (新版本根, 原堆顶值)；空堆返回 (0, None)"""
        if x == 0:
            return 0, None
        return self.merge(self.l[x], self.r[x]), self.val[x]

    def top(self, x):
        return None if x == 0 else self.val[x]


if __name__ == '__main__':
    random.seed(24)
    PL = PersistentLeftistHeap()
    cur = 0
    vers = [cur]
    refs = [[]]
    # 随机演化，保留全部版本
    for step in range(500):
        if not refs[-1] or random.random() < 0.6:
            v = random.randint(0, 50)
            cur = PL.merge(cur, PL._newnode(v))
            ref = sorted(refs[-1] + [v])
        else:
            cur = PL.pop(cur)[0]
            ref = refs[-1][1:]
        vers.append(cur)
        refs.append(ref)
    # 逐个版本重建验证：历史版本互不影响
    for vi in range(len(vers)):
        h = vers[vi]
        out = []
        while h:
            out.append(PL.top(h))
            h = PL.pop(h)[0]
        assert out == sorted(refs[vi]), (vi, out, refs[vi])
    print('persistent-heap: All tests passed.')
```

**PyPy 提示**: 用数组（val/l/r/dist 四列）实现，PyPy 下可支撑 2e5+ 规模。k 短路等场景中 merge 是热点，注意递归深度 O(log n) 安全；若递归慢可改迭代合并（但持久化需记录路径副本，实现更繁琐）。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | merge/insert/pop 均 O(log n)（非均摊，可持久化后仍是严格 O(log n)） |
| 空间 | O(m log n) 节点（m 次 merge 操作，每次新建 O(log n)） |

### 局限

前提是左偏树（非均摊复杂度）；配对堆/斐波那契堆因均摊分析无法直接持久化。不支持 O(1) decrease-key。空间 O(m log n) 在操作极多时压力大。k 短路应用还需配合最短路树、边集的『树上第 k 小』选取逻辑，实现较综合。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P2505 | 5 | 【SDOI2010】魔法猪学院：k 短路，可持久化堆维护候选（也可 A*）的经典应用场景 | [https://www.luogu.com.cn/problem/P2505](https://www.luogu.com.cn/problem/P2505) |
| Luogu | P3377 | 3 | 【模板】左偏树：先掌握非持久化左偏树，再套 path copying 即可持久化 | [https://www.luogu.com.cn/problem/P3377](https://www.luogu.com.cn/problem/P3377) |
| POJ | 2449 | 4 | Remmarguts' Date：k 短路模板题（经典 A*+估价 或 可持久化堆维护） | [https://vjudge.net/problem/POJ-2449](https://vjudge.net/problem/POJ-2449) |

## Pitfalls · 易错点

- merge 里必须新建节点再改，直接改原节点会破坏历史版本
- 复制节点时 val/l/r/dist 四字段要全拷贝，遗漏 dist 会导致左偏性质判断错误
- 递归终止条件 x==0 or y==0 直接返回另一侧（无需新建），漏判会多建节点/死递归
- k 短路中每次 pop 后还要把该节点的『备用边』merge 进候选堆，容易漏合并
- 非均摊复杂度是可持久化的前提：配对堆/斐波那契堆直接持久化复杂无保证
- pop 返回 (新根, 值) 顺序写反是高频低级错误

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/persistent-heap/](https://oi-wiki.org/ds/persistent-heap/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/persistent-heap.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/persistent-heap.md)
- 书籍 ✓ `Eppstein 1998, Finding the k shortest paths`
