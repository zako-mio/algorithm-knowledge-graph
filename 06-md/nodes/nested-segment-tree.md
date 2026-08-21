---
id: nested-segment-tree
name: 线段树嵌套(树套树)
group: G-D-8
stage: frontier
priority: P3
depth_tier: brief
---

# 线段树嵌套(树套树)

> seg-in-seg/seg-in-bit/seg-in-balanced 等多维信息维护结构

<!-- 元信息: id=nested-segment-tree · group=G-D-8 · stage=frontier · priority=P3 · depth_tier=brief -->

## What · 是什么

树套树是嵌套两层(或多层)数据结构维护多维信息：外层线段树管第一维，每个节点挂一棵内层树(线段树/BIT/平衡树)管第二维，支持二维单点修改+矩阵区域查询，复杂度 O(log² n)。

## Why · 为什么

### 直觉 · Intuition

一维用一棵线段树，二维就把每个外层节点(代表第一维的一段)再挂一棵内层线段树管第二维。修改走外层 O(log n) 个节点、每个内层再 O(log n)，共 O(log² n)。

### 原理 · Principle

外层节点 u 覆盖第一维区间，内层树维护该区间内第二维信息；单点修改 (x,y) 走外层 O(log n) 个节点、各在内层 O(log n) 更新；矩形查询对外层每个覆盖节点做一次内层区间查询后合并。内层树须动态开点，总空间 O(n log² n) 或按访问量分配。

### 历史 · History

树套树在 2000s 前后随多维/区间查询问题普及（区间第 k 大等），OI Wiki 在线段树章节以 seg-in-seg / seg-in-BIT 形式系统介绍；常作为主席树无法支持修改时的替代方案。

## How · 实现

### 伪代码

```python
update(x,y,val,s,t,p): 外层递归到含 x 的叶子路径，每个经过节点内层 update(y,val)
query(l1,r1,l2,r2,s,t,p): 外层若 ⊆ 则内层区间查 [l2,r2] 合并；否则按 mid 递归
内层均为动态开点。
```

### Python 实现

```python
import sys

# 线段树套线段树(精简): 外层维护 x 行, 内层每行一棵线段树维护 y 列前缀和
# 示例: 二维单点修改 + 矩阵求和 (动态开点内层)
MAXY = 1000


class InnerSeg:
    # 内层动态开点线段树
    def __init__(self):
        self.root = 0
        self.tot = 0
        self.ls = [0]; self.rs = [0]; self.s = [0]

    def _new(self):
        self.tot += 1
        self.ls.append(0); self.rs.append(0); self.s.append(0)
        return self.tot

    def update(self, p, l, r, y, f):
        if not p:
            p = self._new()
        self.s[p] += f
        if l == r:
            return p
        m = (l + r) >> 1
        if y <= m:
            self.ls[p] = self.update(self.ls[p], l, m, y, f)
        else:
            self.rs[p] = self.update(self.rs[p], m + 1, r, y, f)
        return p

    def query(self, p, l, r, ql, qr):
        if not p or qr < l or r < ql:
            return 0
        if ql <= l and r <= qr:
            return self.s[p]
        m = (l + r) >> 1
        return self.query(self.ls[p], l, m, ql, qr) + self.query(self.rs[p], m + 1, r, ql, qr)


if __name__ == "__main__":
    sys.setrecursionlimit(1 << 20)
    outer = [InnerSeg() for _ in range(8)]  # 外层堆式 n=4

    def upd(x, y, f, s, t, p):
        outer[p].root = outer[p].update(outer[p].root, 1, MAXY, y, f)
        if s == t:
            return
        m = (s + t) >> 1
        if x <= m:
            upd(x, y, f, s, m, p * 2)
        else:
            upd(x, y, f, m + 1, t, p * 2 + 1)

    def qry(x1, x2, y1, y2, s, t, p):
        if x1 <= s and t <= x2:
            return outer[p].query(outer[p].root, 1, MAXY, y1, y2)
        m = (s + t) >> 1
        res = 0
        if x1 <= m:
            res += qry(x1, x2, y1, y2, s, m, p * 2)
        if x2 > m:
            res += qry(x1, x2, y1, y2, m + 1, t, p * 2 + 1)
        return res

    n = 4
    upd(2, 3, 5, 1, n, 1)   # (2,3) += 5
    upd(2, 7, 4, 1, n, 1)  # (2,7) += 4
    print(qry(1, 4, 1, 10, 1, n, 1))  # 9

```

**PyPy 提示**: 两层递归+动态开点在 PyPy 下常数约为 C++ 10+ 倍；n,q≤1e5 的二维题 Python 常超时。建议先离散化，必要时内层用 BIT 或 dict 加速。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 单点修改/矩阵查询 O(log² n) |
| 空间 | O(n log n)（动态开点，单次修改新增 log² n 节点） |

### 局限

Python 常数极大、内存占用高，n=1e5 级二维操作几乎必 TLE/MLE，仅作学习；空间必须动态开点(静态建满树 O(n²) 不可行)。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3810 | 6 | 陌上花开：三维偏序，一维排序+树套树(或CDQ)维护后两维 | [https://www.luogu.com.cn/problem/P3810](https://www.luogu.com.cn/problem/P3810) |

## Pitfalls · 易错点

- 内层树必须动态开点，否则 O(n²) 空间爆内存
- 查询时外层跨多个节点需把各内层结果合并，注意合并顺序与重复计数

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/seg-in-seg.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/seg-in-seg.md)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/seg-in-bit.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/seg-in-bit.md)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/seg-in-balanced.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/seg-in-balanced.md)
