---
id: segment-tree-offline
name: 线段树分治(离线)
group: G-D-8
stage: advanced
priority: P1
depth_tier: standard
---

# 线段树分治(离线)

> 将时间轴建成线段树，把只存在于某时段的信息离线分发到节点

<!-- 元信息: id=segment-tree-offline · group=G-D-8 · stage=advanced · priority=P1 · depth_tier=standard -->

## What · 是什么

线段树分治：把「时间」建成线段树，每条只在时段 [l,r) 存在的信息用区间修改分发到 O(log n) 个线段树节点的 vector；再从根分治 DFS，进入节点时合并其信息、回溯时撤销，叶节点处即为该时刻的答案。常用于「不支持删除但支持撤销」的结构模拟删除、或分色计算。

## Why · 为什么

### 直觉 · Intuition

一条信息在某时段存在 = 它在该时段的每个时刻都有贡献。把这时段拆成 O(log n) 个线段树节点区间，每个节点收集它负责时段内所有信息；分治到节点时把这些信息一次性合并，回溯时整体撤销——避免了逐时刻增删。

### 原理 · Principle

update(l,r,obj) 把 obj push 到覆盖 [l,r) 的 O(log n) 个节点。solve(i,l,r)：记录栈顶位置 lvl，把节点 i 的所有信息合并进当前状态(用栈保存可撤销)；若叶节点 l==r 则记录答案；否则递归左右子；最后撤销到 lvl。信息结构须支持 O(1)/O(T) 撤销(如可撤销并查集按秩合并不路径压缩)。总复杂度 O(n log n·(T+M))。

### 历史 · History

线段树分治（time-segment tree）把时间轴建树做离线分治，CF 社区与 OI Wiki「线段树分治」章节均有介绍，常用于「不支持删除的并查集」在时间线上的应用。

## How · 实现

### 伪代码

```python
update(l,r,obj,i): 若 ⊆ 则 tree[i].push(obj); 否则按 mid 递归
solve(i,l,r): lvl=sta.size(); 合并 tree[i] 所有信息; 若叶 记录答案 否则 递归左右; 撤销到 lvl
```

### Python 实现

```python
import sys

# 线段树分治(离线): 时间轴建线段树, 把存在时段的信息分发到节点, 分治+撤销
# 这里以可撤销并查集判断二分图为例 (P5787)
fa = []
siz = []
stk = []  # 撤销栈


def init(n):
    global fa, siz
    fa = list(range(n + 1))
    siz = [1] * (n + 1)


def find(x):
    while fa[x] != x:
        x = fa[x]
    return x


def union(x, y):
    x, y = find(x), find(y)
    if x == y:
        stk.append((-1, -1, -1, -1))  # 无变化
        return True  # 已连通
    if siz[x] > siz[y]:
        x, y = y, x
    fa[x] = y
    siz[y] += siz[x]
    stk.append((x, y, siz[x], siz[y]))
    return True


def undo(top):
    # 撤销栈顶到 top 大小
    while len(stk) > top:
        x, y, sx, sy = stk.pop()
        if x == -1:
            continue
        fa[x] = x
        siz[y] = sy


if __name__ == "__main__":
    sys.setrecursionlimit(1 << 20)
    init(6)
    union(1, 2)
    union(3, 4)
    print(find(1) == find(2))  # True
    snap = len(stk)
    union(2, 3)
    print(find(1) == find(3))  # True
    undo(snap)
    print(find(1) == find(3))  # False  (已撤销)

```

**PyPy 提示**: 可撤销并查集（按秩合并不路径压缩）+栈记录 PyPy 常数可控；n,q=1e5 级可过，注意递归深度。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n log n·(T(n)+M(n))) — T 为单次合并/撤销，M 为信息并计算 |
| 空间 | O(n log n) — 每条信息分发到 O(log n) 个节点 |

### 局限

Python 撤销栈与并查集常数大，n=1e5 时限 1s 易 TLE，建议 PyPy；可撤销并查集不能路径压缩(否则无法撤销)，只能按秩合并，单次 find/union 变 O(log n)；递归深度 log n 但配合栈撤销需小心顺序。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P5787 | 6 | 二分图模板：边在时段[l,r)存在，种类并查集+线段树分治判二分图 | [https://www.luogu.com.cn/problem/P5787](https://www.luogu.com.cn/problem/P5787) |

## Pitfalls · 易错点

- 可撤销并查集用路径压缩会无法 O(1) 撤销，必须按秩合并
- 撤销栈顺序必须与合并严格相反(后进先出)，否则状态错乱
- 信息合并不满足交换律时分发顺序需额外处理

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/topic/segment-tree-offline.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/topic/segment-tree-offline.md)
- 书籍 ✓ `CPH ch28 (offline segment tree)`
