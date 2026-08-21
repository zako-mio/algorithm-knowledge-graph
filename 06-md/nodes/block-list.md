---
id: block-list
name: 块状链表
group: G-D-6
stage: advanced
priority: P2
depth_tier: standard
---

# 块状链表

> 链表+分块混合，节点指向数组，支持插入/删除/区间访问的O(√n)操作

<!-- 元信息: id=block-list · group=G-D-6 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

块状链表把普通链表升级为「链式数组」：每个链表节点内嵌一个大小约 √n 的定长数组。它保留了链表的插入/删除特性（指针连接），同时通过块内连续存储支持近似随机访问。当一个节点满（超过 2√n）时执行分裂，保证每块规模保持在 √n 量级，使按位置查找、插入、删除的复杂度均为 O(√n)。适合维护需要高频中间插入删除的序列（如 POJ2887 Big String 多次在 pos 处插入字符）。

## Why · 为什么

### 直觉 · Intuition

纯链表定位 O(n)、纯数组插入 O(n)。块状链表用『√n 个块，每块 √n 个元素』让定位只需遍历 O(√n) 个块、块内用 O(√n) 次拷贝完成插入；分裂保持块大小稳定，避免退化为长链表。

### 原理 · Principle

维护一个链表，每节点存一个长度 ≤2√n 的定长数组。查找第 k 个元素：沿链表累计 size 直到跨越，O(√n)。插入：定位后若块满则分裂该块（后 √n 个元素拷入新节点并拼接），再插入，O(√n)。删除：定位后块内删除元素，若块过小可与相邻合并（可选），O(√n)。块大小取固定常量（如 1000）即可，无需随 n 变化。

### 历史 · History

块状链表是 OI 中的经典序列数据结构，OI Wiki《块状链表》章节详细介绍分裂/插入/查找三操作，并用 POJ2887 Big String 作为例题。libstdc++ 的 rope（基于可持久化平衡树）实现同类功能且为 O(log n)，在 C++ OI 中可代替手写块状链表（2021 CCF 补充说明允许使用下划线开头库函数）。

## How · 实现

### 伪代码

```python
# 每节点: size + 定长数组 d[] + nxt 指针
class Node: nxt=None; size=0; d=[0]*MAXB

def find(k):          # 返回第 k 个元素 (0-index)
  p = head
  while k >= p.size:
    k -= p.size; p = p.nxt
  return p.d[k]

def split(x):         # 把节点 x 分裂为两个 ~B 大小的节点
  if x.size < 2*B: return
  y = Node()
  copy x.d[B..size-1] -> y.d
  y.size = x.size - B; x.size = B
  y.nxt = x.nxt; x.nxt = y

def insert(pos, val): # 在 pos 处插入 val
  p = locate(pos); shift; insert; split(p)

def erase(pos):       # 删除 pos 处元素
  p = locate(pos); remove; (可选)合并相邻小节点
```

### Python 实现

```python
B = 1000


class Node:
    __slots__ = ("size", "nxt", "d")

    def __init__(self):
        self.size = 0
        self.nxt = None
        self.d = []


class BlockList:
    """块状链表：支持按位置 find/insert/delete，均摊 O(√n)。
    B 为块大小常量。实现定位 + 满块分裂。
    """

    def __init__(self, init=""):
        self.head = Node()
        for ch in init:
            self.push_back(ch)

    def push_back(self, ch):
        if self.head is None:
            self.head = Node()
        p = self.head
        while p.nxt is not None:
            p = p.nxt
        p.d.append(ch)
        p.size += 1
        if p.size >= 2 * B:
            self.split(p)

    def _locate(self, pos):
        """返回 (节点, 块内下标)，定位第 pos 个元素(0-index)。"""
        p = self.head
        while p is not None and pos >= p.size:
            pos -= p.size
            p = p.nxt
        return p, pos

    def split(self, x):
        if x.size < 2 * B:
            return
        y = Node()
        y.d = x.d[B:]
        y.size = len(y.d)
        del x.d[B:]
        x.size = len(x.d)
        y.nxt = x.nxt
        x.nxt = y

    def find(self, pos):
        p, i = self._locate(pos)
        return p.d[i]

    def insert(self, pos, ch):
        if self._size() == 0:
            self.head = Node()
            self.head.d.append(ch)
            self.head.size = 1
            return
        if pos == self._size():
            self.push_back(ch)
            return
        p, i = self._locate(pos)
        p.d.insert(i, ch)
        p.size += 1
        self.split(p)

    def erase(self, pos):
        p, i = self._locate(pos)
        del p.d[i]
        p.size -= 1
        if p.size == 0:
            self._remove_node(p)

    def _remove_node(self, x):
        p = self.head
        if p is x:
            self.head = p.nxt
            return
        while p is not None and p.nxt is not x:
            p = p.nxt
        if p is not None:
            p.nxt = x.nxt

    def _size(self):
        p = self.head
        s = 0
        while p is not None:
            s += p.size
            p = p.nxt
        return s

    def to_str(self):
        p = self.head
        out = []
        while p is not None:
            out.extend(p.d)
            p = p.nxt
        return "".join(out)


if __name__ == "__main__":
    import random

    random.seed(7)
    bl = BlockList("hello")
    brute = list("hello")
    for _ in range(2000):
        op = random.random()
        if op < 0.45 and len(brute) > 0:
            pos = random.randrange(len(brute))
            bl.erase(pos)
            del brute[pos]
        elif op < 0.85:
            pos = random.randrange(len(brute) + 1)
            ch = chr(random.randint(97, 122))
            bl.insert(pos, ch)
            brute.insert(pos, ch)
        elif len(brute) > 0:
            pos = random.randrange(len(brute))
            assert bl.find(pos) == brute[pos], (pos, bl.find(pos), brute[pos])
    assert bl.to_str() == "".join(brute)
    # 大量插入使块分裂后依然正确
    for i in range(5000):
        bl.insert(i % (i + 1), "x")
    assert bl._size() == 5000 + len(brute)
    print("block-list 自测通过：2000+ 次随机 插入/删除/查找 与列表对拍一致")

```

**PyPy 提示**: PyPy 下每块用 list 即可；split 时用切片赋值比逐元素拷贝快。块大小常量按题目规模调（如 n=1e6 取 B≈1e3）。不需要维护合并逻辑也能通过多数题目；Python 若追求 O(log n) 可用内置 list 模拟更慢，直接手写块状链表更可控。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 查找/插入/删除均 O(√n)；分裂均摊 O(√n)（每插入 2√n 次触发一次） |
| 空间 | O(n) |

### 局限

定位需沿链表走 O(√n) 个节点，若块数变多退化为 O(n)；需严格控制块大小上限（满则分裂）否则退化成单块数组或长链表。Python 端随机访问较慢，适合插入/删除主导的题。rope（C++）可实现 O(log n) 但 Python 无内置等价物。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| POJ | 2887 | 4 | Big String：块状链表模板题，多次在 pos 处插入字符+单点查询（OI Wiki 例题） | [http://poj.org/problem?id=2887](http://poj.org/problem?id=2887) |
| Luogu | P4008 | 5 | NOI2003 文本编辑器：块状链表实现文本光标操作 | [https://www.luogu.com.cn/problem/P4008](https://www.luogu.com.cn/problem/P4008) |

## Pitfalls · 易错点

- 块满未分裂会退化为单数组，插入 O(n)
- 定位时累计 size 的下标边界（0-index 与 1-index 混淆）
- 删除后节点变空需从链表中移除，否则 to_str 出空块
- split 后 nxt 指针要正确拼接（y.nxt=x.nxt; x.nxt=y）
- 插入在末尾时 _locate 返回 None，需单独 push_back
- 多块拼接遍历时要处理 p 为 None（越界访问）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/block-list/](https://oi-wiki.org/ds/block-list/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/block-list.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/block-list.md)
