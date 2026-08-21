---
id: binary-heap
name: 二叉堆
group: G-A-3
stage: basic
priority: P0
depth_tier: deep
---

# 二叉堆

> 完全二叉树维护优先队列，数组实现O(1)查最值/O(log n)插入删除/O(n)建堆，对顶堆动态求中位数

<!-- 元信息: id=binary-heap · group=G-A-3 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

二叉堆(Binary Heap)是一棵完全二叉树，每个节点的权值不小于(大根堆)或不大于(小根堆)其儿子。堆性质保证根即为最值，O(1)查询。它支持三种操作：插入(末尾+向上调整sift up)、删除最值(根与末尾交换+向下调整sift down)、增减某点权值(相应向上/向下调整)，各O(log n)。用数组h存储时h[i]的两个儿子是h[2i]与h[2i+1]，根为h[1]。建堆有O(n)的向下调整法(从叶子逐个向下调整, 理解成每次合并两个已调整好的堆)与O(n log n)的逐元素向上调整法。堆是堆排序、Dijkstra优先队列、哈夫曼树、对顶堆(动态求中位数/第k大)等的基础。Python内置heapq实现小根堆(取负实现大根堆)。

## Why · 为什么

### 直觉 · Intuition

堆像'有序的排队'：不保证全队有序，只保证'队头永远是最值'。要得到这个保证，插队时只需把新元素一路'往上冒泡'，踢掉队头时把末尾拉来顶班再一路'往下沉淀'。完全二叉树保证树高log n，所以冒泡/沉淀都只走log n步。

### 原理 · Principle

两个核心调整：(1)向上调整(sift up): 插入到最下层最右叶子之后(仍是完全二叉树), 若比父节点大则交换, 重复至不满足或到根；(2)向下调整(sift down): 删根时把最后一个节点搬到根, 与其较大的儿子交换, 重复到底。完全二叉树结构+堆性质保证调整后全树仍满足堆性质。建堆的O(n)下界：从h[n//2]到h[1]逐个向下调整, 因每个节点调整代价正比于其高度, 总代价Σ高=O(n)(从叶往上合并两个已调好的堆)。数组索引: 根1, i的儿子2i/2i+1, 父⌊i/2⌋。堆性质很弱、二叉堆不唯一, 这正是一棵堆有多种形态的原因。

### 历史 · History

堆结构由J.W.J. Williams于1964年提出，作为堆排序(heapsort)的数据结构；同年Floyd给出O(n)建堆算法。二叉堆是最基础的优先队列实现，之后发展出左偏树、配对堆、二项堆等可合并变体。OI Wiki的binary-heap页、CPH ch4(p47)均有介绍。

## How · 实现

### 伪代码

```python
# 大根堆, h[1..n], 根1
sift_up(x):
  while x>1 and h[x]>h[x//2]:
    swap(h[x], h[x//2]); x//=2
sift_down(x):
  while 2*x<=n:
    t=2*x
    if t+1<=n and h[t+1]>h[t]: t+=1
    if h[x]>=h[t]: break
    swap(h[x], h[t]); x=t
insert(v): h[++n]=v; sift_up(n)
pop(): res=h[1]; h[1]=h[n--]; sift_down(1)
build_linear(): for i in n//2..1: sift_down(i)   # O(n)
```

### Python 实现

```python
class MaxHeap:
    """大根堆(数组实现).
    h[0]占位, 有效元素1..n; 支持push/pop/top/size.
    """
    def __init__(self, data=None):
        self.h = [0]
        if data:
            self.h.extend(data)
            self._build()
        else:
            self.h = [0]

    def _sift_up(self, x):
        h = self.h
        while x > 1 and h[x] > h[x // 2]:
            h[x], h[x // 2] = h[x // 2], h[x]
            x //= 2

    def _sift_down(self, x):
        h = self.h
        n = len(h) - 1
        while 2 * x <= n:
            t = 2 * x
            if t + 1 <= n and h[t + 1] > h[t]:
                t += 1
            if h[x] >= h[t]:
                break
            h[x], h[t] = h[t], h[x]
            x = t

    def _build(self):
        for i in range((len(self.h) - 1) // 2, 0, -1):
            self._sift_down(i)

    def push(self, v):
        self.h.append(v)
        self._sift_up(len(self.h) - 1)

    def pop(self):
        if len(self.h) == 1:
            raise IndexError("pop from empty heap")
        top = self.h[1]
        self.h[1] = self.h[-1]
        self.h.pop()
        if len(self.h) > 1:
            self._sift_down(1)
        return top

    def top(self):
        return self.h[1]

    def __len__(self):
        return len(self.h) - 1


class MinHeap:
    """小根堆: 用负值存入MaxHeap."""
    def __init__(self, data=None):
        self._h = MaxHeap([-v for v in data] if data else None)

    def push(self, v):
        self._h.push(-v)

    def pop(self):
        return -self._h.pop()

    def top(self):
        return -self._h.top()

    def __len__(self):
        return len(self._h)


def heap_sort(arr):
    """用二叉堆排序."""
    h = MaxHeap(arr)
    res = []
    while len(h):
        res.append(h.pop())
    return res


class MedianStream:
    """对顶堆: 动态维护流的中位数.
    小根堆存较大半区, 大根堆存较小半区, 中位数=小根堆顶.
    """
    def __init__(self):
        self.small = MaxHeap()   # 较小半区(大根堆)
        self.large = MinHeap()   # 较大半区(小根堆)

    def add(self, v):
        if len(self.small) == 0 or v <= self.small.top():
            self.small.push(v)
        else:
            self.large.push(v)
        self._rebalance()

    def _rebalance(self):
        while len(self.small) > len(self.large) + 1:
            self.large.push(self.small.pop())
        while len(self.large) > len(self.small):
            self.small.push(self.large.pop())

    def median(self):
        if len(self.small) == 0:
            return None
        if (len(self.small) + len(self.large)) % 2 == 1:
            return self.small.top()
        return self.small.top()  # 偶数时输出较小中位数


if __name__ == "__main__":
    import random

    # 堆性质与push/pop
    h = MaxHeap()
    for x in [3, 1, 4, 1, 5, 9, 2, 6]:
        h.push(x)
    assert h.top() == 9
    popped = [h.pop() for _ in range(len(h))]
    assert popped == sorted(popped, reverse=True), popped

    # 线性建堆
    h2 = MaxHeap([5, 3, 8, 1, 9, 2])
    assert h2.top() == 9
    assert [h2.pop() for _ in range(len(h2))] == sorted([5, 3, 8, 1, 9, 2],
                                                        reverse=True)

    # 堆排序
    arr = [random.randint(-100, 100) for _ in range(50)]
    assert heap_sort(arr) == sorted(arr, reverse=True)

    # 小根堆
    mh = MinHeap()
    for x in [4, 2, 8, 1, 7]:
        mh.push(x)
    assert mh.top() == 1

    # 对顶堆中位数: 插入 [1,2,3,4,5]
    ms = MedianStream()
    for v in [1, 2, 3, 4, 5]:
        ms.add(v)
    assert ms.median() == 3
    ms.add(6)
    assert ms.median() == 3  # 偶数长度输出较小中位数

    print("binary-heap: ALL TESTS PASSED")

```

**PyPy 提示**: 竞赛Python直接内置import heapq(小根堆, 大根堆用负值)。自定义堆注意数组用list, 索引从1开始便于2i/2i+1。堆排序在Python中远慢于内置sorted, 仅用于理解。对顶堆用heapq即可实现动态中位数。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 查最值O(1); 插入/删除/改权O(log n); 建堆O(n)(向下调整法)或O(n log n)(逐插入) |
| 空间 | O(n) — 数组存储 |

### 局限

堆不支持任意元素的查找/删除(需额外索引表); 只保证最值在根, 不是有序结构; 合并两个堆需O(n)(不可合并变体); 大根/小根堆语义易混。Python自定义堆性能不及heapq(C实现)。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3378 | 1 | 【模板】堆：插入/删除最小/查询最小三操作裸题, 可直接用heapq | [https://www.luogu.com.cn/problem/P3378](https://www.luogu.com.cn/problem/P3378) |
| Luogu | P1801 | 3 | 黑匣子：对顶堆动态维护第k小, k随查询递增 | [https://www.luogu.com.cn/problem/P1801](https://www.luogu.com.cn/problem/P1801) |
| SPOJ | RMID2 | 3 | Running Median Again：对顶堆维护中位数并支持删除 | [https://www.spoj.com/problems/RMID2/](https://www.spoj.com/problems/RMID2/) |

## Pitfalls · 易错点

- 索引从0还是1开始要统一: 根为1则儿子2i/2i+1, 根为0则儿子2i+1/2i+2, 混用必出错
- 向下调整需比较两个儿子取较大者, 且先判右儿子存在(t+1<=n)
- 删除最值时先与末尾交换再pop, 不要直接删根(会破坏完全二叉树结构)
- 建堆用向下调整法才O(n), 逐元素插入是O(n log n)
- heapq是最小堆, 取最大堆要push(-x)并在pop时取负

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/binary-heap/](https://oi-wiki.org/ds/binary-heap/)
- 书籍 ✓ `CPH ch4 p47`
