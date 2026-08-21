---
id: linked-list
name: 链表
group: G-A-10
stage: basic
priority: P1
depth_tier: standard
---

# 链表

> 节点指针串联，O(1) 插入删除，O(n) 随机访问，注意边界哨兵

<!-- 元信息: id=linked-list · group=G-A-10 · stage=basic · priority=P1 · depth_tier=standard -->

## What · 是什么

链表（Linked List）由节点经指针串联而成：单向链表每个节点含数据域与 next 指针；双向链表还有 pre 指针。特点：插入/删除已知节点 O(1)（只需改相邻指针），但随机访问/按值查找 O(n)。与数组互补——数组随机访问 O(1) 而中间插入删除 O(n)。竞赛中常用场景：需要频繁在中间插入删除的模拟（约瑟夫问题、队列安排、双向 BFS 队列）、邻接表实现（前向星/链式前向星本质也是数组链表）、以及链表+其他结构配合（跳表、LRU 缓存）。实现上建议用『哨兵节点』（head/tail 哑节点）避免边界特判；Python 中常用 list 模拟（pre/nxt 两个数组）获得更低常数与更好缓存。

## Why · 为什么

### 直觉 · Intuition

数组是‘门牌号连续的一排房子’，中间插一间必须把后面全部搬动；链表是‘一串用绳子拴住的箱子’，在任意两箱之间塞新箱只要解两根绳、栓两根绳，其他箱子纹丝不动。代价是找第 k 个箱子得从头数起。

### 原理 · Principle

单向插入 p 后：node.next=p.next; p.next=node。单向删除 p：用 p.next 的值覆盖 p，再跳过 p.next（无头删除技巧，需 p 非尾）。双向删除 p：p.pre.next=p.next; p.next.pre=p.pre。哨兵：head/tail 两个哑节点让首尾操作与普通一致，彻底消灭 if 空表判断。邻接表前向星：以数组存储，e[cnt].next=head[u], head[u]=cnt（头插），遍历 for(i=head[u]; i; i=e[i].next)。复杂度：已知节点插入/删除 O(1)，查找/随机访问 O(n)。

### 历史 · History

链表概念来自 1950 年代早期（Allen Newell/Herbert Simon 的 List Processing，IPL 语言 1956 年由 McCarthy 的 LISP 发扬光大，LISP 以‘list’为核心数据结构）。MIT 人工智能实验室的 LISP 语言让链表成为计算机科学基础数据结构。OI Wiki《链表》页给出单向/双向/循环链表与异或链表的完整实现。

## How · 实现

### 伪代码

```python
class Node: val; nxt; pre
# 双向链表 + 哨兵
head = Node(None); tail = Node(None)
head.nxt = tail; tail.pre = head
def insert_after(p, val):
  new = Node(val); new.nxt = p.nxt; p.nxt.pre = new
  p.nxt = new; new.pre = p; return new
def remove(p):
  p.pre.nxt = p.nxt; p.nxt.pre = p.pre  # O(1)
# 单向链表的无头删除
def delete_node_no_head(p):
  p.val = p.nxt.val; p.nxt = p.nxt.nxt
```

### Python 实现

```python
class Node:
    __slots__ = ('val', 'nxt', 'pre')
    def __init__(self, val):
        self.val = val
        self.nxt = None
        self.pre = None


class DoublyLinkedList:
    """双向链表 + 哨兵节点. O(1) 插入删除; 记录链表长度."""
    def __init__(self):
        self.head = Node(None)      # 哨兵头
        self.tail = Node(None)      # 哨兵尾
        self.head.nxt = self.tail
        self.tail.pre = self.head
        self._len = 0

    def __len__(self):
        return self._len

    def is_empty(self):
        return self._len == 0

    def _link(self, a, b):
        a.nxt = b
        b.pre = a

    def insert_after(self, node, val):
        """在 node 之后插入新节点, 返回新节点."""
        new = Node(val)
        self._link(new, node.nxt)
        self._link(node, new)
        self._len += 1
        return new

    def insert_before(self, node, val):
        return self.insert_after(node.pre, val)

    def push_back(self, val):
        return self.insert_before(self.tail, val)

    def push_front(self, val):
        return self.insert_after(self.head, val)

    def remove(self, node):
        """删除节点. O(1), 无需前驱指针(双向链表)."""
        self._link(node.pre, node.nxt)
        node.nxt = node.pre = None
        self._len -= 1
        return node.val

    def to_list(self):
        res, p = [], self.head.nxt
        while p is not self.tail:
            res.append(p.val)
            p = p.nxt
        return res

    def __iter__(self):
        p = self.head.nxt
        while p is not self.tail:
            yield p
            p = p.nxt


def delete_node_no_head(node):
    """单向链表"无头删除"技巧: 用下一个节点的值覆盖当前节点, 再删下一个.
    注意: 只能用于非尾节点."""
    node.val = node.nxt.val
    node.nxt = node.nxt.nxt


if __name__ == "__main__":
    ll = DoublyLinkedList()
    a = ll.push_back(10)
    b = ll.push_back(20)
    c = ll.push_back(30)
    assert ll.to_list() == [10, 20, 30]
    ll.insert_after(a, 15)
    assert ll.to_list() == [10, 15, 20, 30]
    ll.remove(b)
    assert ll.to_list() == [10, 15, 30]
    ll.push_front(5)
    assert ll.to_list() == [5, 10, 15, 30]
    assert len(ll) == 4

    # 与 Python list 模拟对比 (随机验证)
    import random
    random.seed(3)
    l2 = DoublyLinkedList()
    ref = []
    nodes = []
    for step in range(5000):
        r = random.random()
        if r < 0.35 or not ref:
            v = random.randint(0, 1000)
            if random.random() < 0.5:
                nodes.append(l2.push_back(v)); ref.append(v)
            else:
                nodes.insert(0, l2.push_front(v)); ref.insert(0, v)
        elif r < 0.7:
            i = random.randrange(len(ref))
            l2.remove(nodes[i]); del nodes[i]; del ref[i]
        else:
            i = random.randrange(len(ref))
            v = random.randint(0, 1000)
            nodes.insert(i + 1, l2.insert_after(nodes[i], v)); ref.insert(i + 1, v)
        if l2.to_list() != ref:
            print("MISMATCH at", step); break
    else:
        assert l2.to_list() == ref and len(l2) == len(ref)
        print("linked-list: all tests passed")

```

**PyPy 提示**: Python 对象式链表每个节点一个对象，开销大；竞赛大输入推荐用 list 模拟双向链表（pre/nxt/val 三个平行数组，下标即节点 id），常数是对象式的数倍。实现时要小心 0 下标哨兵，用 -1 表示空指针。删除时注意 list 数组中节点 id 复用问题（用 free list 或标 unused）。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 插入/删除(已知位置) O(1)；查找/随机访问 O(n) |
| 空间 | O(n) |

### 局限

① 随机访问慢（无下标）；② 对象式 Python 链表内存/常数大，大数据用数组模拟；③ 单向链表删除已知节点需要前驱，否则用‘覆盖下一个’技巧（不能删尾）；④ 循环/双向链表的边界（空表、单节点）易错；⑤ 慎用 Python 的 id() 做指针（GC 不稳定），用索引模拟。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1160 | 3 | 队列安排：链表模拟班级排座，支持中间插入删除，经典链表模拟题 | [https://www.luogu.com.cn/problem/P1160](https://www.luogu.com.cn/problem/P1160) |
| Luogu | P1996 | 1 | 约瑟夫问题：循环链表/模拟出队顺序 | [https://www.luogu.com.cn/problem/P1996](https://www.luogu.com.cn/problem/P1996) |
| LeetCode.cn | 146 | 3 | LRU 缓存：哈希表+双向链表，O(1) 访问与淘汰 | [https://leetcode.cn/problems/lru-cache/](https://leetcode.cn/problems/lru-cache/) |

## Pitfalls · 易错点

- 删除单链表节点无前驱（覆盖技巧不能用于尾节点）
- 空表/单节点时哨兵指针处理错导致悬垂
- 对象式链表 GC/内存开销大，大数据用数组模拟
- 双向链表修改指针时顺序错（先断后连的顺序）
- 循环链表遍历忘记判环 / 死循环
- 删除后重复释放/复用节点导致链表断裂

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/linked-list/](https://oi-wiki.org/ds/linked-list/)
- 书籍 ✓ `CPH ch2.1 (动态数组/链表)`
- article ✓ [https://en.wikipedia.org/wiki/Linked_list](https://en.wikipedia.org/wiki/Linked_list)
