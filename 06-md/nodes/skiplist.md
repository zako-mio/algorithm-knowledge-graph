---
id: skiplist
name: 跳表（Skip List）
group: G-A-10
stage: intermediate
priority: P3
depth_tier: brief
---

# 跳表（Skip List）

> 多层有序链表随机化，期望 O(log n) 查找/插入/删除，实现简单于平衡树

<!-- 元信息: id=skiplist · group=G-A-10 · stage=intermediate · priority=P3 · depth_tier=brief -->

## What · 是什么

跳表（Skip List）由 William Pugh 1989 年发明，是对有序链表的随机化改进：每个节点以概率 p 出现在更高层，形成多层的有序链表（底层是完整链表）。查找从顶层开始，逐层下降到最后一层，跳过大量节点，期望 O(log n)。插入/删除等价于一次查找+局部指针修改。期望空间 O(n)。相比 AVL/红黑树，跳表实现简单、无旋转、并发友好，因此被 Redis 用作有序集合 zset 的底层实现之一。Python 中 `sortedcontainers` 与 LeetCode 1206 即考察手写跳表。

## Why · 为什么

### 直觉 · Intuition

普通链表找元素像‘顺着单行道一个个问’；跳表在链表上加了几条‘高架桥’（高层链表），每条桥跳过更多节点。先坐高架（高层）快速靠近，再走地面（底层）精确定位——类似二分但结构是随机化分层的。

### 原理 · Principle

设每层节点以概率 p 升到下一层，最高层期望高度 O(log_p n)。查找：从最高层开始，在每层水平前进到‘最后一个 key<目标’的节点再下坠一层，到第 0 层后检查后继。插入：先记录各层‘需改前驱’的 update[]，随机生成节点层数 lv（几何分布，上限 MAXL），若 lv>当前层则提升表高，再逐层插入。删除同理。期望复杂度证明：从底层爬到 L(n) 层的期望步数上界 (L(n)-1)/p，之后水平步数期望 O(1/p)，故总 O(log n)。最坏（所有节点同层）退化为 O(n)。

### 历史 · History

William Pugh 于 1989 年在论文 “Skip lists: a probabilistic alternative to balanced trees” 中提出，作为平衡树的简单替代。后被 Redis、LevelDB（内存表）、并发无锁跳表广泛采用。OI Wiki《跳表》页给出完整实现与复杂度证明（期望空间 O(n)、期望时间 O(log n)、最坏 O(n)）。

## How · 实现

### 伪代码

```python
MAXL = 32; P = 0.5
def randomLevel():
  lv = 1
  while random() < P and lv < MAXL: lv += 1
  return lv
def find_prev(key):
  prev = []
  p = head
  for i in range(level-1, -1, -1):
    while p.nxt[i] and p.nxt[i].key < key: p = p.nxt[i]
    prev[i] = p
  return prev
def set(key, val):
  prev = find_prev(key)
  if prev[0].nxt[0].key == key: prev[0].nxt[0].val = val; return
  lv = randomLevel(); if lv>level: 补 head 指针, level=lv
  node = Node(key, val, lv)
  for i in range(lv): node.nxt[i]=prev[i].nxt[i]; prev[i].nxt[i]=node
```

### Python 实现

```python
import random


class SkipNode:
    __slots__ = ('key', 'val', 'nxt')
    def __init__(self, key, val, level):
        self.key = key
        self.val = val
        self.nxt = [None] * level


class SkipList:
    """跳表 (升序有序映射). 期望 O(log n) 查询/插入/删除, 期望 O(n) 空间.
    p=1/2 随机层数; 哨兵头节点层高 MAXL."""
    MAXL = 32
    P = 0.5

    def __init__(self):
        self.level = 1
        self.head = SkipNode(None, None, self.MAXL)
        self._len = 0

    def _random_level(self):
        lv = 1
        while random.random() < self.P and lv < self.MAXL:
            lv += 1
        return lv

    def _find_prev(self, key):
        """返回每一层中最后一个 key < 目标 的节点."""
        prev = [None] * self.level
        p = self.head
        for i in range(self.level - 1, -1, -1):
            while p.nxt[i] is not None and p.nxt[i].key < key:
                p = p.nxt[i]
            prev[i] = p
        return prev

    def get(self, key, default=None):
        p = self.head
        for i in range(self.level - 1, -1, -1):
            while p.nxt[i] is not None and p.nxt[i].key < key:
                p = p.nxt[i]
        nxt = p.nxt[0]
        return nxt.val if nxt is not None and nxt.key == key else default

    def __contains__(self, key):
        return self.get(key) is not None

    def set(self, key, value):
        prev = self._find_prev(key)
        nxt = prev[0].nxt[0]
        if nxt is not None and nxt.key == key:
            nxt.val = value
            return value
        lv = self._random_level()
        if lv > self.level:
            for i in range(self.level, lv):
                prev.append(self.head)
            self.level = lv
        node = SkipNode(key, value, lv)
        for i in range(lv):
            node.nxt[i] = prev[i].nxt[i]
            prev[i].nxt[i] = node
        self._len += 1
        return value

    def pop(self, key):
        prev = self._find_prev(key)
        nxt = prev[0].nxt[0]
        if nxt is None or nxt.key != key:
            return None
        for i in range(self.level):
            if prev[i].nxt[i] is nxt:
                prev[i].nxt[i] = nxt.nxt[i]
        self._len -= 1
        while self.level > 1 and self.head.nxt[self.level - 1] is None:
            self.level -= 1
        return nxt.val

    def __len__(self):
        return self._len

    def min_key(self):
        n = self.head.nxt[0]
        return n.key if n is not None else None


if __name__ == "__main__":
    sl = SkipList()
    # 基本操作
    for i in range(1000):
        sl.set(i, i * i)
    assert sl.get(500) == 250000
    assert sl.get(5000) is None
    assert sl.min_key() == 0
    assert len(sl) == 1000
    sl.set(500, -1)
    assert sl.get(500) == -1
    assert sl.pop(500) == -1 and sl.get(500) is None
    assert len(sl) == 999

    # 与 dict 交叉验证
    import random
    random.seed(99)
    d = {}
    sl2 = SkipList()
    for _ in range(20000):
        r = random.random()
        k = random.randint(-10**9, 10**9)
        if r < 0.5 or k not in d:
            d[k] = random.randint(0, 10**6)
            sl2.set(k, d[k])
        elif r < 0.7:
            del d[k]
            sl2.pop(k)
        else:
            assert sl2.get(k) == d[k], k
        assert len(sl2) == len(d), (len(sl2), len(d))
    for k, v in d.items():
        assert sl2.get(k) == v, k
    print("skiplist: all tests passed")

```

**PyPy 提示**: random() 调用频率高（每个插入一次层数采样），PyPy 下 random 模块足够快；若追求极速可用快速伪随机（如线性同余）替换。MAXL 设为 32（2^32 足够）；P 取 1/4 可降低内存。删除后要把表顶空层回收（while level>1 and head.nxt[level-1] is None: level-=1），否则后续遍历浪费。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 期望 O(log n) 查询/插入/删除；最坏 O(n) |
| 空间 | 期望 O(n)；最坏 O(n log n) |

### 局限

① 最坏情况退化 O(n)（构造出同层长链）；② Python 对象开销大，小数据不如 dict；③ 随机层数实现要保证几何分布质量；④ 不如平衡树提供严格最坏界，不适用于对时间上界极敏感的场景；⑤ 有序遍历（中序）仍需沿第 0 层线性走。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| LeetCode.cn | 1206 | 3 | 设计跳表：手写 search/add/erase 完整模板题 | [https://leetcode.cn/problems/design-skiplist/](https://leetcode.cn/problems/design-skiplist/) |
| book | Redis ZSET | 3 | Redis 有序集合基于跳表实现，体现实际工业应用 | [https://redis.io/docs/data-types/sorted-sets/](https://redis.io/docs/data-types/sorted-sets/) |

## Pitfalls · 易错点

- randomLevel 未设上限导致超高层节点（MAXL 截断）
- 插入时忘记录 update[]，导致新节点断链
- 提升表高时 head 新层指针未初始化（指向自己/None 要一致）
- 删除后未回收空顶层，查找时访问 None 越界
- 哨兵 head 的 nxt 数组长度与 MAXL 不符（应建满 MAXL 层）
- get/set 中 key 相等判断误用 < 导致相同 key 插入重复节点

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/skiplist/](https://oi-wiki.org/ds/skiplist/)
- 论文 ✓ [https://www.cl.cam.ac.uk/teaching/2005/Algorithms/skiplists.pdf](https://www.cl.cam.ac.uk/teaching/2005/Algorithms/skiplists.pdf)
- article ✓ [https://en.wikipedia.org/wiki/Skip_list](https://en.wikipedia.org/wiki/Skip_list)
