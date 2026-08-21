---
id: odt
name: 珂朵莉树/ODT
group: G-E-7
stage: advanced
priority: P1
depth_tier: standard
---

# 珂朵莉树/ODT

> 用平衡树维护颜色段均摊：区间赋值操作下split/assign均摊O(log)，起源CF896C；颜色段均摊，随机数据下区间赋值均摊 O(logn)，源自 CF896C

<!-- 元信息: id=odt · group=G-E-7 · stage=advanced · priority=P1 · depth_tier=standard -->

## What · 是什么

珂朵莉树(Chtholly Tree / ODT, Old Driver Tree)是一种用有序集合(set/map)维护'颜色段'的数据结构：将值相同的连续区间合并为一个节点(l, r, val)。核心操作 split(分裂区间) 和 assign(区间推平赋值)。在随机数据+区间赋值操作下均摊 O(log n)。

## Why · 为什么

### 直觉 · Intuition

线段树处理区间赋值需要懒标记，但有些操作(如'区间第 k 小'、'区间所有数的和')难以用标记维护。珂朵莉树直接维护每一段连续相同值的区间：赋值时把目标区间内的所有小段合并成一个大段。在随机数据下，段数被赋值操作不断压缩，均摊开销很小。

### 原理 · Principle

用 set/map 存储区间节点 {l, r, val}，按 l 排序。核心操作：①split(x): 找到包含 x 的区间 [l,r,val]，分裂为 [l,x-1,val] 和 [x,r,val]，返回后者迭代器 ②assign(l,r,val): split(r+1), split(l), 删除 [l,r] 内所有段，插入新段 [l,r,val] ③perform(l,r): split 提取后遍历段做操作。关键：split 先 r+1 再 l(防迭代器失效)。复杂度：assign 均摊 O(log n)(随机数据)；perform 最坏 O(段数)。

### 历史 · History

珂朵莉树起源于 Codeforces 896C(2017)，出题人用随机操作+区间推平+区间查询设计了此结构。因 CF896C 的角色名为 Chtholly 而得'珂朵莉树'之名，又称'老司机树'(ODT)。

## How · 实现

### 伪代码

```python
# set 存储 (l, r, val), 按 l 排序
split(x):
  it = lower_bound(x)
  if it.l == x: return it
  it--  # 找到包含 x 的区间
  [l, r, v] = *it
  erase(it)
  insert(l, x-1, v)
  return insert(x, r, v)  # 返回新段迭代器

assign(l, r, v):
  itr = split(r+1)
  itl = split(l)
  erase(itl, itr)  # 删除 [l,r] 内所有段
  insert(l, r, v)   # 插入新段
```

### Python 实现

```python
# Python 珂朵莉树实现
# 用 SortedList 或 bisect + list 模拟 set
import bisect


class ODTNode:
    __slots__ = ['l', 'r', 'v']
    def __init__(self, l, r, v):
        self.l = l
        self.r = r
        self.v = v


class ChthollyTree:
    """珂朵莉树: 用有序列表维护颜色段。"""
    def __init__(self, n, init_val=0):
        # 用 list 维护, 按 l 排序; 简化实现用线性查找
        self.nodes = [ODTNode(1, n, init_val)]
        self.n = n

    def split(self, x):
        """在 x 处分裂, 返回包含 x 的节点在 nodes 中的索引。"""
        for i, node in enumerate(self.nodes):
            if node.l <= x <= node.r:
                if node.l == x:
                    return i
                # 分裂 [l, r, v] -> [l, x-1, v] + [x, r, v]
                left = ODTNode(node.l, x - 1, node.v)
                right = ODTNode(x, node.r, node.v)
                self.nodes[i:i+1] = [left, right]
                return i + 1  # right 的索引
        return len(self.nodes)  # x 超出范围

    def assign(self, l, r, v):
        """区间推平: [l, r] 赋值为 v。"""
        # Python list 需先 split(l) 再 split(r+1): 先 split(l) 可能插入元素,
        # 后 split(r+1) 在更新后的列表上操作, 索引不会错位
        idx_l = self.split(l)
        idx_r = self.split(r + 1) if r < self.n else len(self.nodes)
        # 删除 [idx_l, idx_r) 的所有节点
        self.nodes[idx_l:idx_r] = [ODTNode(l, r, v)]

    def range_sum(self, l, r):
        """区间求和: [l, r] 的所有值之和。"""
        idx_l = self.split(l)
        idx_r = self.split(r + 1) if r < self.n else len(self.nodes)
        s = 0
        for i in range(idx_l, idx_r):
            node = self.nodes[i]
            s += node.v * (node.r - node.l + 1)
        return s


if __name__ == '__main__':
    ct = ChthollyTree(10, 1)  # [1,10] 初始全1
    ct.assign(1, 5, 2)   # [1,5]=2
    ct.assign(3, 7, 3)   # [3,7]=3
    print(f'Sum [1,10]: {ct.range_sum(1, 10)}')
    # [1,2]=2, [3,7]=3, [8,10]=1 => 2*2+3*5+1*3=4+15+3=22
    assert ct.range_sum(1, 10) == 22
    print(f'Sum [3,5]: {ct.range_sum(3, 5)}')
    # [3,5]=3 => 9
    assert ct.range_sum(3, 5) == 9
    ct.assign(4, 6, 0)
    print(f'Sum [1,10]: {ct.range_sum(1, 10)}')
    # [1,2]=2, [3,3]=3, [4,6]=0, [7,7]=3, [8,10]=1 => 4+3+0+3+3=13
    assert ct.range_sum(1, 10) == 13
    print('Chtholly Tree: all tests passed!')

```

**PyPy 提示**: Python 用 list 模拟 set 性能差(O(N) split)；PyPy 下 list 操作快但仍不如 C++ set。正式竞赛建议 C++ std::set 实现。Python 版适合理解原理和小规模验证。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | assign 均摊 O(log n)(随机数据); split O(log n)(set) / O(n)(list); range_sum O(段数) |
| 空间 | O(段数) — 段数在随机赋值下均摊 O(log n) |

### 局限

性能依赖随机数据(非随机构造数据可卡到 O(n) 段数)；split 先 r+1 再 l 的顺序必须遵守(防迭代器失效)；Python 用 list 实现性能差，仅适合学习。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Codeforces | 896C | 2400 | Willem, Chtholly and Seniorious: ODT 起源题, 随机区间操作 | [https://codeforces.com/problemset/problem/896/C](https://codeforces.com/problemset/problem/896/C) |

## Pitfalls · 易错点

- split 顺序: C++ 用 set 迭代器时必须先 split(r+1) 再 split(l)(防迭代器失效); Python 用 list 时须先 split(l) 再 split(r+1)(防索引错位)
- 非随机数据(如交替赋值不同段)可卡到 O(n) 段数 → TLE
- Python 用 list 模拟 set 的 split 是 O(n) 而非 C++ set 的 O(log n)
- mutable 关键字(C++): set 中的节点 val 用 mutable 修饰才能直接修改

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/misc/odt/](https://oi-wiki.org/misc/odt/)
- Wikipedia ✓ [https://en.wikipedia.org/wiki/Chtholly_tree](https://en.wikipedia.org/wiki/Chtholly_tree)
