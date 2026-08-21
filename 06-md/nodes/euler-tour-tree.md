---
id: euler-tour-tree
name: Euler Tour Tree（ETT，欧拉游览树）
group: G-D-4
stage: advanced
priority: P2
depth_tier: standard
---

# Euler Tour Tree（ETT，欧拉游览树）

> 把树映射为欧拉游览序列，将动态树的连边/断边/换根转化为序列的拆分与合并操作，用平衡树维护序列，适合维护子树信息（如子树最值）。

<!-- 元信息: id=euler-tour-tree · group=G-D-4 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

ETT 是一种动态树数据结构：对一棵树做 DFS，访问节点或遍历有向边时记录一次，得到欧拉游览表示（Euler Tour Representation, ETR）序列（长度 3n-2，若把点视作自环）。原树的结构与序列结构一一对应，因此『树上连边』等价于『把两个序列拼接』，『断边』等价于『把序列拆开』，『换根』等价于『把序列旋转』。用一个支持区间拆分/合并与区间修改查询的平衡树（Splay 或非旋 Treap）维护序列，所有动态树操作都能在 O(log n) 完成。相比 LCT 更擅长维护子树信息（子树最值、子树和），因为子树在 ETR 中是连续区间。

## Why · 为什么

### 直觉 · Intuition

LCT 的实链剖分本质是『动态的路径剖分』，天然适合路径问题；而子树信息需要另一套虚子树维护，很麻烦。ETT 换个思路：子树在 DFS 序（欧拉序）里就是一段连续区间，若能让动态加删边只改序列，子树查询就退化为区间查询——这用任何区间数据结构都能做。代价是需要支持序列的『切割/拼接』（可裂可合的平衡树），于是得到 ETT。

### 原理 · Principle

① 欧拉游览序列：DFS 进入一个点时记录该点（含回到该点），遍历每条有向边 (u→v) 与 (v→u) 时各记录一次，最终序列长度为 3n-2；把点 u 看作自环 (u,u)，整个序列可视为一条欧拉回路。② MakeRoot(u)：把序列从 (u,u) 处断开，分成前后两段再互换拼接（欧拉回路是环，旋转不改变树结构）。③ Insert(u,v)（加边）：在 T1 的 (u,u) 处断开成 L1^1,L1^2，在 T2 的 (v,v) 处断开成 L2^1,L2^2，按 L1^2,L1^1,[(u,v)],L2^2,L2^1,[(v,u)] 拼接。④ Delete(u,v)（删边）：拆成 L1,[(u,v)],L2,[(v,u)],L3，删边后两棵新树对应 L2 和 L1·L3。⑤ 子树查询：ETR 中 u 的整棵子树（不含 u 上方）对应以 (u,u) 开头的一段连续区间，用区间求和/最值即可。实现通常用非旋 Treap 支持 Split/Merge。

### 历史 · History

树的欧拉回路表示思想来自有向图欧拉回路（Euler tour），2007 年前后在动态树研究中被系统化，OI Wiki 与 CP-Algorithms 均有教程。在学术上，Euler Tour Trees 与 Self-Adjusting Top Trees 同为维护动态森林的重要方法；竞赛中常作为 LCT 的『子树信息友好』替代或与 LCT 互补。

## How · 实现

### 伪代码

```python
# 用非旋 Treap 维护 ETR 序列
# 序列元素 = 节点访问（进入/自环/有向边）。为简洁，以下用节点自环表示法。

MakeRoot(u):
    L = treap_of(u 所在树)
    split L at 元素(u) -> L1, L2   # L1 含 (u,u) 及之前，L2 其余
    return merge(L2, L1)

Insert(u, v):  # u∈T1, v∈T2，连边 (u,v)
    (L1a, L1b) = split_at_u(L1)
    (L2a, L2b) = split_at_v(L2)
    return merge(merge(L1b, L1a), 边(u,v), L2b, L2a, 边(v,u))

Delete(u, v):  # 删边 (u,v)，序列中出现 [(u,v)] 与 [(v,u)]
    split L -> L1, [uv], L2, [vu], L3
    return (merge(L1, L3), L2)   # 两棵新树

QuerySubtree(u):
    return range_query(区间 [first(u), last(u)])
```

### Python 实现

```python
import random

class TreapNode:
    __slots__ = ('key', 'prio', 'left', 'right', 'sz', 'val', 'sm')
    def __init__(self, key, val):
        self.key = key
        self.prio = random.random()
        self.left = self.right = None
        self.sz = 1
        self.val = val
        self.sm = val

def _sz(t):
    return t.sz if t else 0

def _sm(t):
    return t.sm if t else 0

def _pull(t):
    if t:
        t.sz = 1 + _sz(t.left) + _sz(t.right)
        t.sm = t.val + _sm(t.left) + _sm(t.right)

def split(t, k):
    """按前 k 个元素切开，返回 (左, 右)"""
    if not t:
        return None, None
    if _sz(t.left) >= k:
        a, b = split(t.left, k)
        t.left = b
        _pull(t)
        return a, t
    else:
        a, b = split(t.right, k - _sz(t.left) - 1)
        t.right = a
        _pull(t)
        return t, b

def merge(a, b):
    if not a or not b:
        return a or b
    if a.prio > b.prio:
        a.right = merge(a.right, b)
        _pull(a)
        return a
    else:
        b.left = merge(a, b.left)
        _pull(b)
        return b

def build_seq(keys):
    t = None
    for k in keys:
        t = merge(t, TreapNode(k, 0))
    return t

def pos_of(root, key):
    """返回 key 首次出现的位置（0 基）"""
    def walk(t, key, acc):
        if not t:
            return None
        if t.key == key:
            return acc + _sz(t.left)
        r = walk(t.left, key, acc)
        if r is not None:
            return r
        return walk(t.right, key, acc + _sz(t.left) + 1)
    return walk(root, key, 0)

def euler_tour_tree_selfcheck():
    random.seed(1)
    # 树: 1-2, 1-3；节点集合做 ETR 的简化模型：每个节点出现一次
    # 用『节点自环』序列直接验证 MakeRoot/Insert/Delete 的位置不变式
    # 完整 ETR 需要 (u,u),(u->v),(v->u) 三元素/边，此处给出可运行的简化自测：
    # 以 entry 序列 [1,2,3] 表示树，验证序列操作正确性
    root = build_seq([1, 2, 3])
    assert _sz(root) == 3
    assert pos_of(root, 2) == 1
    # MakeRoot(2): 序列旋转 -> [2,3,1]
    p = pos_of(root, 2)
    a, b = split(root, p)
    root = merge(b, a)
    assert pos_of(root, 1) == 2
    print('ETT sequence ops OK')

if __name__ == '__main__':
    euler_tour_tree_selfcheck()
```

**PyPy 提示**: 非旋 Treap 递归 Split/Merge 在 PyPy 下 n~1e5 可行但常数偏大；可用 __slots__ 减少内存、把随机数预生成避免 random 开销；深度受堆随机化控制，一般不会爆递归栈。若需极致性能可改 FHQ Treap 迭代版或用 pypy 跑。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 每次动态树操作 = O(1) 次序列 Split/Merge + O(1) 次区间查询，平衡树操作均摊/期望 O(log n) |
| 空间 | O(n)（ETR 长度 3n-2，即 O(n) 个节点） |

### 局限

需要序列支持可裂可合与区间操作，平衡树实现复杂；子树信息区间化是强项，但路径信息（如路径 xor）在 ETR 中并非连续区间，不如 LCT 自然；ETR 序列长度 3n-2 使常数略大于 LCT；换根后子树区间端点需要额外记录。Python 实现仅适合教学与小数据。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P2147 | 4 | [SDOI2008] 洞穴勘测：ETT 可解连通性/加删边模板，与 LCT 解法对比 | [https://www.luogu.com.cn/problem/P2147](https://www.luogu.com.cn/problem/P2147) |
| LOJ | 2230 | 6 | [BJOI2014] 大融合：子树大小查询，ETT 的子树区间特性直接可用 | [https://loj.ac/p/2230](https://loj.ac/p/2230) |
| hydro | bzoj-P3786 星际探索 | 7 | 路径加/换根/子树查询综合题，ETT 区间操作经典应用 | [https://hydro.ac/p/bzoj-P3786](https://hydro.ac/p/bzoj-P3786) |

## Pitfalls · 易错点

- ETR 长度为 3n-2，用点自环表示的简化实现会丢边信息，仅作教学
- Insert/Delete 的序列拼接顺序必须严格按欧拉回路拼接规则，顺序错导致树结构错误
- 换根 (MakeRoot) 本质是旋转欧拉回路，必须在 (u,u) 处断开再拼
- 查询子树要先定位 first(u)/last(u) 的区间端点，端点定位错误会得到错误区间
- Treap 递归深度依赖随机优先级，随机种子固定可复现但需保证平衡

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/ett.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/ett.md)
- OI Wiki △ [https://oi-wiki.org/ds/ett/](https://oi-wiki.org/ds/ett/)
