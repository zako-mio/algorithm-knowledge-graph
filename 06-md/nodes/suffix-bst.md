---
id: suffix-bst
name: 后缀平衡树
group: G-C-3
stage: frontier
priority: P3
depth_tier: brief
---

# 后缀平衡树

> 用平衡BST维护后缀排序，支持动态插入删除字符的后缀结构

<!-- 元信息: id=suffix-bst · group=G-C-3 · stage=frontier · priority=P3 · depth_tier=brief -->

## What · 是什么

后缀平衡树（Suffix Balanced Tree）是用平衡二叉搜索树维护字符串所有后缀的字典序有序集合的数据结构：树中每个节点对应一个后缀，中序遍历即后缀数组。特点：支持在字符串**开头**动态插入/删除字符（前端动态维护），复杂度 O(log n) 每次插入/删除；不依赖字符集大小；若用可持久化平衡树则可持久化。构造方法有四档：①暴力比较后缀大小，单次 O(n) 比较，总 O(n² log n)；②利用 cS 与 S 的关系：先比较首字符，若相同则比较去掉首字符后的两个串（它们已在树中），用平衡树求排名 O(log n)，单次插入 O(log² n)；③给每个节点维护实数区间 tag（根对应 (0,1)，左子树 (l,tag)，右子树 (tag,r)），O(1) 比较两个节点后缀大小，总 O(n log n)；④先建后缀数组再建平衡树。经典应用：维护字符串尾部插入/删除+询问串出现次数（用反串后缀平衡树）。

## Why · 为什么

### 直觉 · Intuition

后缀数组是静态的，但若字符串要动态变化（尤其头部加/删字符），SA 需要重排。后缀平衡树用 BST 动态维护'后缀的字典序排列'：新后缀 cS 与已有后缀比较时，先比首字符 c，若相同则比较 S——而 S 已经在树中，可用其排名 O(log n) 定位。tag 技巧更妙：给每个节点分配一个 (0,1) 内的实数，子节点在父节点区间内取中点，于是两节点大小比较退化为 tag 大小比较 O(1)。

### 原理 · Principle

正确性（做法3）：若 tag 满足 tag_i < tag_j ⟺ 后缀 i < 后缀 j，则树中比较两后缀就是比较 tag。构造保证：中序遍历顺序即 tag 递增；根取 0.5，左子树取 (0,0.5) 内、右子树取 (0.5,1) 内，递归二分区间，因此子树内 tag 保持与中序一致的偏序。实数精度：用期望树高 O(log n) 的替罪羊树/Treap，tag 用 64 位浮点或 128 位定点（根取 (0, 2^64) 大区间）可避免冲突。头插/头删：插入 cS 就是插入一个节点；删除 cS 即删节点。对'尾部增删'问题可维护反串的后缀平衡树。

### 历史 · History

后缀平衡树由陈立杰（2011 国家集训队论文《重量平衡树和后缀平衡树在信息学奥赛中的应用》）系统介绍，是结合平衡树与后缀结构的动态后缀数据结构的代表，属于 NOI/集训队层面较新/较深的知识点。

## How · 实现

### 伪代码

```python
# 做法3: 实数 tag 后缀平衡树 (插入 cS)
def insert(node cS):
    在 BST 中按 tag 二分找到位置
    若首字符不同 => 直接比出大小
    若相同 => 比较 tag[S] (S 已在树中)
    创建节点, 分配 tag = 父区间中点
    (树高失衡时按需重构, 如替罪羊)

# 中序遍历 => 后缀数组
# 头删: 直接删对应节点
# 问串 t 出现次数: 排名(t) - 排名(t的前驱) (用后缀平衡树)
```

### Python 实现

```python
import random


class ScapegoatNode:
    __slots__ = ("ch", "tag", "val", "k")

    def __init__(self, val, tag, k):
        self.ch = [None, None]   # 0=left, 1=right
        self.tag = tag           # 实数区间中点 (做法3: O(1) 比较)
        self.val = val           # 当前后缀字符串 (存储, 简化)
        self.k = k               # 插入序号 => 对应原串位置


class SuffixBST:
    """做法3 (tag) 后缀平衡树, 用替罪羊(重构)保持平衡.
    演示: 只支持在开头插入字符 (动态维护后缀集合), 中序遍历=后缀数组.
    注意: 实际 O(1) 比较应直接比较 tag; 此处存储字符串仅用于可读性.
    """

    def __init__(self):
        self.root = None
        self.s = ""
        self.k = 0

    def _insert(self, node, val, lo, hi):
        if node is None:
            return ScapegoatNode(val, (lo + hi) / 2, self.k)
        if val < node.val:
            node.ch[0] = self._insert(node.ch[0], val, lo, node.tag)
        else:
            node.ch[1] = self._insert(node.ch[1], val, node.tag, hi)
        return self._rebalance(node)

    def _rebalance(self, node):
        def size(x):
            if x is None:
                return 0
            return 1 + size(x.ch[0]) + size(x.ch[1])
        l, r = size(node.ch[0]), size(node.ch[1])
        if max(l, r) > 0.8 * (l + r + 1):
            return self._rebuild(node)
        return node

    def _rebuild(self, node):
        def collect(x, out):
            if x is None:
                return
            collect(x.ch[0], out)
            out.append(x)
            collect(x.ch[1], out)
        arr = []
        collect(node, arr)
        return self._build(arr, 0.0, 1.0)

    def _build(self, arr, lo, hi):
        if not arr:
            return None
        mid = len(arr) // 2
        nd = arr[mid]
        nd.tag = (lo + hi) / 2
        nd.ch[0] = self._build(arr[:mid], lo, nd.tag)
        nd.ch[1] = self._build(arr[mid + 1:], nd.tag, hi)
        return nd

    def insert_char(self, c):
        """在字符串开头插入字符 c (新增一个后缀)."""
        self.s = c + self.s
        self.root = self._insert(self.root, self.s, 0.0, 1.0)
        self.k += 1

    def inorder(self):
        """中序遍历 => 后缀数组 (按字典序的后缀起始位置列表)."""
        out = []

        def dfs(x):
            if x is None:
                return
            dfs(x.ch[0])
            out.append(x)
            dfs(x.ch[1])
        dfs(self.root)
        return [(len(self.s) - 1 - nd.k) for nd in out]


if __name__ == "__main__":
    random.seed(3)
    for _ in range(200):
        n = random.randrange(1, 30)
        t = ''.join(random.choice('abc') for _ in range(n))
        sb = SuffixBST()
        for c in t:
            sb.insert_char(c)
        order = sb.inorder()
        s = sb.s
        expected = sorted(range(len(s)), key=lambda i: s[i:])
        assert order == expected, (s, order, expected)

    sb = SuffixBST()
    for c in "abab":   # 头插 => 最终串 "baba"
        sb.insert_char(c)
    s = sb.s
    order = sb.inorder()
    assert order == sorted(range(len(s)), key=lambda i: s[i:]), (s, order)

    print("suffix-bst tests passed")

```

**PyPy 提示**: tag 用浮点在高插入量时可能精度耗尽，需用大整数区间 (0, 2^64) 或定点数；替罪羊重构使期望 O(log n)。Python 下仅小规模演示可行，竞赛级动态后缀结构建议 C++。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 做法1 O(n² log n)；做法2 O(n log² n)；做法3/4 O(n log n)；插入/删除单次 O(log n) |
| 空间 | O(n) |

### 局限

实现复杂（需平衡树 + tag 区间 + 重构）；实数 tag 精度需谨慎处理；仅在字符串头部动态增删时有优势；多数竞赛题用静态 SA/SAM 即可，后缀平衡树属于小众深水区。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P6164 | 5 | 后缀平衡树模板：维护串尾部插删+查询出现次数（转反串后缀平衡树） | [https://www.luogu.com.cn/problem/P6164](https://www.luogu.com.cn/problem/P6164) |
| Luogu | P3809 | 3 | 后缀排序模板：后缀平衡树中序遍历即为 SA（静态对比） | [https://www.luogu.com.cn/problem/P3809](https://www.luogu.com.cn/problem/P3809) |

## Pitfalls · 易错点

- tag 浮点精度耗尽导致比较错误，用大区间/定点数
- 只支持头部增删；尾部增删需转反串
- 插入用字符串暴力比较（做法1）会退化 O(n²)，要用 tag/排名优化
- 树失衡后 tag 区间会耗尽，需重构重新分配
- 与后缀数组互为中序遍历，别把方向搞反

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/string/suffix-bst/](https://oi-wiki.org/string/suffix-bst/)
- Wikipedia ✓ [https://en.wikipedia.org/wiki/Suffix_array](https://en.wikipedia.org/wiki/Suffix_array)
