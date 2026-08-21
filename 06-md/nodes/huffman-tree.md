---
id: huffman-tree
name: 哈夫曼树
group: G-A-3
stage: intermediate
priority: P1
depth_tier: standard
---

# 哈夫曼树

> 最优前缀编码树，贪心构造，WPL最小

<!-- 元信息: id=huffman-tree · group=G-A-3 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

哈夫曼树（Huffman Tree，又称霍夫曼树）是给定一组带权叶节点时，带权路径长度 WPL = Σ(wᵢ·lᵢ)（wᵢ 为叶权值，lᵢ 为叶到根路径长度）最小的二叉树。哈夫曼算法（Huffman Coding）用贪心构造它：每次取权值最小的两棵树合并成一棵权值等于二者之和的新树，重复至只剩一棵树。由此得到的编码是前缀编码（任一编码不是另一编码的前缀），解码唯一，且对给定频率分布平均码长最短，是最优前缀编码。应用包括文件压缩（DEFLATE 的 Huffman 阶段）、网络编码、竞赛中『k 叉哈夫曼』与『k 短路合并』等变形。

## Why · 为什么

### 直觉 · Intuition

频率高的字符应得到短编码，频率低的应得到长编码，就像把最少用的东西放在仓库最远的架子上。哈夫曼算法每次把两个最小的叶子合并，等价于：最深的叶子（码最长）给频率最小的字符。用反证可证：在一棵最优编码树中，两个权值最小的叶子一定是最深的，且让它们做兄弟不会破坏最优性，从而贪心合并合法。

### 原理 · Principle

① 初始化：n 个权值构成 n 棵单节点树；② 选取：从集合中选根权值最小的两棵作为左右子树，新根权值为二者之和；③ 删除与加入：删去两棵树，加入新树；④ 重复至集合只剩一棵。正确性：先证引理『最优前缀编码树中两个最小权叶节点总是最深且可调整为兄弟而不劣』（交换最深处叶子 a 与最小叶 c 后 WPL 减少，矛盾；再做兄弟调整不增 WPL），再对 n 归纳证明哈夫曼算法得到最优树。WPL 计算：合并过程中每次两棵子树合并，其权值和被计入最终 WPL——等价于把每个内部节点的权值累加（每个内部节点权值 = 下方叶子路径的贡献）。

### 历史 · History

1952 年 David A. Huffman 在 MIT 的『信息论』课程作业中发明该算法（课程由 Fano 讲授），当时他 25 岁。算法的核心贪心证明成为经典。后来 Fano 与 Shannon 的次优编码方法被超越。现代应用：DEFLATE（gzip/zlib）、JPEG、MP3 等均采用（近似）哈夫曼编码。

## How · 实现

### 伪代码

```python
# 构造哈夫曼树/求最小 WPL (用小根堆)
def huffman_wpl(weights):
  heap = min_heap(weights)
  total = 0
  while len(heap) > 1:
    a = pop_min(heap); b = pop_min(heap)
    total += a + b
    push(heap, a + b)
  return total

# 构造编码
def huffman_codes(freq):  # freq: dict char->weight
  heap = [[w, [sym, '']] for sym, w in freq.items()]
  heapify(heap)
  while len(heap) > 1:
    lo = pop(heap); hi = pop(heap)
    for item in lo[1:]: item[1] = '0' + item[1]
    for item in hi[1:]: item[1] = '1' + item[1]
    push(heap, [lo[0]+hi[0]] + lo[1:] + hi[1:])
  return sorted(heap[0][1:])  # [(char, code), ...]
```

### Python 实现

```python
import heapq
import collections


def huffman_wpl(weights):
    """给定叶权值列表，返回最小带权路径长度 WPL"""
    if not weights:
        return 0
    heap = list(weights)
    heapq.heapify(heap)
    total = 0
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        total += a + b
        heapq.heappush(heap, a + b)
    return total


def huffman_codes(freq):
    """给定 {符号: 频率} 字典，返回 [(符号, 二进制编码)]（按符号排序）"""
    if len(freq) == 1:
        return [(next(iter(freq)), '0')]
    heap = [[w, [s, '']] for s, w in freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for item in lo[1:]:
            item[1] = '0' + item[1]
        for item in hi[1:]:
            item[1] = '1' + item[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heap[0][1:])


if __name__ == '__main__':
    # 经典例子: 频率 {a:45, b:13, c:12, d:16, e:9, f:5}
    freq = {'a': 45, 'b': 13, 'c': 12, 'd': 16, 'e': 9, 'f': 5}
    codes = huffman_codes(freq)
    wpl_by_codes = sum(len(c) * freq[s] for s, c in codes)
    wpl_direct = huffman_wpl(list(freq.values()))
    assert wpl_by_codes == wpl_direct == 224, (wpl_by_codes, wpl_direct)
    # 前缀无歧义检查
    cs = sorted(c for _, c in codes)
    for i in range(len(cs)):
        for j in range(len(cs)):
            if i != j and cs[j].startswith(cs[i]):
                raise AssertionError('存在前缀冲突')
    print('huffman: WPL =', wpl_direct, '; codes =', codes)
    print('huffman: All tests passed.')
```

**PyPy 提示**: 实现即小根堆贪心，heapq 是 C 实现，性能无忧。注意 k 叉哈夫曼（如合并 n 个数每次取 k 个）需先补 (n-k) mod (k-1) 个 0 权值节点使最后一次恰好取满 k 个。存储上无需真建树，WPL 直接累加合并值即可。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 构造 O(n log n)（n 次堆操作）；单字符编码 O(log n) 解码（按树走） |
| 空间 | O(n) 堆；树结构 O(n) |

### 局限

哈夫曼编码是最优前缀编码，但不保证最优定长块编码（如算术编码/ANS 在非整数码长场景更优）；符号之间假设相互独立（对联合分布不做建模）。竞赛中常见『合并果子』类题目即每次取最小两个合并，等价于求 WPL，不要与堆排混淆。编码长度对单个符号最坏可达 O(n)。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1090 | 2 | 【NOIP2004】合并果子：每次合并两堆求最小总代价，WPL 模板，贪心+小根堆 | [https://www.luogu.com.cn/problem/P1090](https://www.luogu.com.cn/problem/P1090) |
| Luogu | P2168 | 4 | 【NOI2015】荷马史诗：k 叉哈夫曼树求最小 WPL，需补 0 权节点使 k 叉树满 | [https://www.luogu.com.cn/problem/P2168](https://www.luogu.com.cn/problem/P2168) |
| Luogu | P2827 | 4 | 蚯蚓：合并类贪心变形，思想与每次取最小两数合并一致（配合整体加标记） | [https://www.luogu.com.cn/problem/P2827](https://www.luogu.com.cn/problem/P2827) |

## Pitfalls · 易错点

- 合并果子类题 WPL 直接累加每次合并的权值和，不要额外乘以深度（内部节点权值已隐含路径贡献）
- k 叉哈夫曼：先补足 0 权叶子使 (n-1) mod (k-1) == 0，否则最后一次合并不满 k 个导致次优
- 单个符号时编码特殊处理（给 0）否则构造不出编码
- 频率相等时编码不唯一（多种最优树），题目若要求字典序需规定合并顺序（如优先合并下标小/字符序小的）
- 解码时不能只用码长，必须沿树从根走二进制位，否则无法区分分支

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/huffman-tree/](https://oi-wiki.org/ds/huffman-tree/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/huffman-tree.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/huffman-tree.md)
- 书籍 ✓ `CPH ch6 (Greedy) p68-69 huffman-like; CLRS ch16.3 Huffman codes`
