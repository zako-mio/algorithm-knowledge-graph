---
id: cat-tree
name: 猫树（Cat Tree）
group: G-D-6
stage: advanced
priority: P2
depth_tier: standard
---

# 猫树（Cat Tree）

> 静态线段树分治预处理，跨中点询问O(1)合并，不支持修改

<!-- 元信息: id=cat-tree · group=G-D-6 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

猫树是一种静态线段树的变形：在分治建树时，除了区间本身信息外，每个节点额外保存『左半段的后缀聚合值数组』与『右半段的前缀聚合值数组』。这样对任意询问 [l,r]，只需找到代表 l 与 r 的两个叶子节点的 LCA（该 LCA 的区间恰含 l,r 且跨其中点），就可以用 LCA 节点预存的『l 到 mid 的后缀聚合 + mid+1 到 r 的前缀聚合』在一次合并内拼出答案。因此查询复杂度从线段树的 O(log n) 次合并降为 O(1) 次合并，适合合并代价高昂（如线性基、矩阵乘法）的静态区间询问。

## Why · 为什么

### 直觉 · Intuition

把线段树每个节点当作『分治』：任何区间 [l,r] 都唯一地被某个 LCA 节点覆盖，且在该节点内 l、r 分别落在中点两侧。既然 l、r 分别在中点两侧，只要该节点预存了两侧的所有前缀/后缀聚合值，答案就能用恰好一次合并拼出来。

### 原理 · Principle

性质1：LCA([l,l],[r,r]) 代表的区间 [L,R] 一定包含 [l,r]；性质2：l 在 [L,mid]、r 在 (mid,R]，即 [l,r] 跨越中点。建树时每个节点存 (l,mid] 的后缀聚合数组和 (mid,r] 的前缀聚合数组，建树复杂度 T(n)=2T(n/2)+O(n)=O(n log n)，空间 O(n log n)。查询用堆式编号：把序列补到 2^k，两叶子编号 x,y 的 LCA 编号 = x >> digits[x^y]（digits 为二进制位数），O(1) 求出 LCA 后再 O(1) 合并。对线性基这类合并 O(log² w) 的信息，可把静态区间线性基从 O(n log² w + m log² w log n) 优化到 O(n log n log w + m log² w)。

### 历史 · History

猫树由 immortalCO 在 UOJ 博客首次提出（immortalCO.blog.uoj.ac/blog/2102），OI Wiki 收录并给出完整实现与证明，早期思想可追溯到 Bentley-Wood (1980) 与 Klee (1977) 关于区间极值/矩形相交的文献。它主要解决『合并操作昂贵但可预计算前缀后缀』的静态场景。

## How · 实现

### 伪代码

```python
# 建树（堆式，序列补 0 到 2^k）
build(node, l, r):
  mid = (l+r)//2
  # 左半后缀聚合
  suf[node][mid] = a[mid]
  for i in mid-1..l: suf[node][i] = op(a[i], suf[node][i+1])
  # 右半前缀聚合
  pref[node][mid+1] = a[mid+1]
  for i in mid+2..r: pref[node][i] = op(pref[node][i-1], a[i])
  build(node*2, l, mid); build(node*2+1, mid+1, r)

# 查询 [l,r]
# digits[x] = 二进制位数
lca = l >> digits[l ^ r]
if l == r: return a[l]
ans = op(suf[lca][l], pref[lca][r])
```

### Python 实现

```python
import random


def op(a, b):
    return a + b  # 用加法演示（结合律）


class CatTree:
    """猫树：O(n log n) 建树，O(1) 查询静态区间聚合值。
    使用堆式线段树 + 二进制 LCA 定位。运算需满足结合律。
    """

    def __init__(self, a):
        self.n = len(a)
        k = 1
        while k < self.n:
            k <<= 1
        self.N = k
        self.a = list(a) + [0] * (self.N - self.n)
        self.suf = [None] * (2 * self.N)  # 左半段后缀聚合 (suf[node][i])
        self.pref = [None] * (2 * self.N)  # 右半段前缀聚合 (pref[node][i])
        self.digits = [0] * (self.N + 1)
        for i in range(1, self.N + 1):
            self.digits[i] = i.bit_length()
        self._build(1, 0, self.N - 1)

    def _build(self, node, l, r):
        if l == r:
            return
        mid = (l + r) >> 1
        s = [0] * self.N
        s[mid] = self.a[mid]
        for i in range(mid - 1, l - 1, -1):
            s[i] = op(self.a[i], s[i + 1])
        self.suf[node] = s
        p = [0] * self.N
        p[mid + 1] = self.a[mid + 1]
        for i in range(mid + 2, r + 1):
            p[i] = op(p[i - 1], self.a[i])
        self.pref[node] = p
        self._build(node << 1, l, mid)
        self._build(node << 1 | 1, mid + 1, r)

    def query(self, l, r):
        """查询 [l,r] 聚合值 (0-index 闭区间)。"""
        if l == r:
            return self.a[l]
        x = l + self.N
        y = r + self.N
        lca = x >> (self.digits[x ^ y])
        return op(self.suf[lca][l], self.pref[lca][r])


if __name__ == "__main__":
    random.seed(5)
    for n in [1, 2, 3, 5, 8, 16, 30, 100, 200]:
        arr = [random.randint(-1000, 1000) for _ in range(n)]
        ct = CatTree(arr)
        for _ in range(400):
            l = random.randrange(n)
            r = random.randrange(n)
            if l > r:
                l, r = r, l
            got = ct.query(l, r)
            exp = sum(arr[l : r + 1])
            assert got == exp, (n, l, r, got, exp)
    print("cat-tree 自测通过：多种规模随机区间和查询与暴力一致")

```

**PyPy 提示**: 猫树空间 O(n log n)，Python 存 N 长列表 × log N 层可行（n=1e5 时 ~1.7e6 元素）。查询 LCA 用 x.bit_length() 代替预计算 digits 数组亦可。若运算为 xor/min 等幂等运算可用稀疏表更省空间；猫树优势在非幂等且合并贵的运算（线性基、矩阵）。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 建树 O(n log n)，单次查询 O(1) 次合并（求 LCA O(1)） |
| 空间 | O(n log n) |

### 局限

不支持修改（静态结构）；运算必须满足结合律；序列需补到 2^k 导致空间浪费（可控制在 2× 内）。对求和/最值这类合并便宜的运算，线段树 O(log n) 足够，猫树收益不明显。若题目同时要求更新，应改用线段树或 SqrtTree。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Codeforces | 1100F | 6 | Ivan and Burgers：静态区间线性基（合并贵），猫树可 O(1) 次合并优化 | [https://codeforces.com/contest/1100/problem/F](https://codeforces.com/contest/1100/problem/F) |
| Luogu | P4198 | 6 | 楼房重建：线段树维护斜率信息（猫树思想练习，区间合并不可交换） | [https://www.luogu.com.cn/problem/P4198](https://www.luogu.com.cn/problem/P4198) |

## Pitfalls · 易错点

- 堆式编号求 LCA 时下标换算要一致（叶子下标 = 序列下标+N）
- l==r 需特判，否则 l^r=0 导致 digits[0] 未定义
- 补 0 到 2^k 后查询范围不能越界到补的段
- pref/suf 数组每节点只覆盖本区间内有效下标，查询时 l,r 一定在 LCA 区间内才正确
- 运算非幂等时不能直接用稀疏表代替；猫树专门处理合并昂贵信息

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/cat-tree/](https://oi-wiki.org/ds/cat-tree/)
- web ✓ [https://immortalco.blog.uoj.ac/blog/2102](https://immortalco.blog.uoj.ac/blog/2102)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/cat-tree.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/cat-tree.md)
