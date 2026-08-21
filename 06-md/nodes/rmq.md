---
id: rmq
name: RMQ 专题（区间最值查询）
group: G-D-9
stage: intermediate
priority: P1
depth_tier: deep
---

# RMQ 专题（区间最值查询）

> Range Minimum/Maximum Query：静态区间最值。ST 表 O(n log n) 预处理 O(1) 查询；另有 Four Russians、±1RMQ 与基于笛卡尔树的 O(n)~O(1) 解法，动态版本用线段树。

<!-- 元信息: id=rmq · group=G-D-9 · stage=intermediate · priority=P1 · depth_tier=deep -->

## What · 是什么

RMQ（Range Minimum/Maximum Query）问题：给定数组，回答若干次『区间 [l,r] 的最小/最大值』。核心方法谱系：① 线段树：O(n) 建树 O(log n) 查询，支持动态修改，最通用；② ST 表（Sparse Table）：预处理每个点起长度 2^k 的区间最值，O(n log n) 时间 O(n log n) 空间，查询 O(1)（取两个覆盖区间的重叠最值），只适用于静态；③ Four Russians：ST 表 + 分块，预处理 O(n log log n)；④ 加减 1RMQ（±1RMQ）：相邻元素差为 ±1 时用二进制状压 + 查表做到 O(n) 预处理 O(1) 查询；⑤ 笛卡尔树法：把 RMQ 转成笛卡尔树上 LCA，再转 ±1RMQ 得 O(n)~O(1)。竞赛常用 ST 表（静态）与线段树（动态）。

## Why · 为什么

### 直觉 · Intuition

区间最值满足『区间可合并』：两个相邻区间的最值的 min 还是并区间的最值。ST 表把每个位置出发的所有 2^k 长度区间的答案都存下来，查询时用两个长度恰为『2 的幂且覆盖 [l,r]』的区间取 min 即可——因为 min 是幂等运算，重叠不影响结果。线段树则是把区间按中点递归划分，任何区间都能分解为 O(log n) 个树上节点。±1RMQ 的洞察：差分序列只有 ±1 两种，块内形态（长度为 log n 的 ±1 模式）总共只有 2^log n ≈ n 种，于是可以穷举所有形态预计算答案查表，把块内查询变 O(1)。

### 原理 · Principle

① ST 表：st[k][i] = 区间 [i, i+2^k-1] 的最值；st[0][i]=a[i]；st[k][i]=min(st[k-1][i], st[k-1][i+2^(k-1)])。查询 [l,r]：k=⌊log2(r-l+1)⌋，ans=min(st[k][l], st[k][r-2^k+1])。② 线段树：区间 min + 单点/区间改。③ 笛卡尔树转 RMQ：区间 [l,r] 的 min 等于 l 与 r 在笛卡尔树（按下标 BST、值小根堆）上的 LCA 的值；树上 LCA 可经欧拉序转 ±1RMQ 实现 O(1)。④ Four Russians：块大小 S，块间建 ST 表，块内建零散 ST 表，S=log n 时预处理 O(n log log n)。

### 历史 · History

RMQ 是计算几何与数据结构的基础问题。ST 表方法由 Bentley 与 Saxe（1980）等人系统性研究；Four Russians 命名源于四位俄罗斯计算机学家提出的针对算法改进的框架（本质是把小规模暴力预处理 + 查表）；±1RMQ 的 O(n)~O(1) 解法结合了分块与状压（Bender & Farach-Colton 2000 的 LCA→RMQ→±1RMQ 链）。CP-Algorithms 与 OI Wiki 均有系统章节；国内 Luogu P3865 是 ST 表模板题。

## How · 实现

### 伪代码

```python
# ST 表（静态 O(1) 查询）
LOG = ⌊log2 n⌋
for i in 1..n: st[0][i] = a[i]
for k in 1..LOG:
    for i in 1..n-2^k+1:
        st[k][i] = min(st[k-1][i], st[k-1][i+2^(k-1)])
query(l, r):
    k = floor_log2(r-l+1)
    return min(st[k][l], st[k][r-2^k+1])
```

### Python 实现

```python
from math import log2

def build_sparse_table(a):
    n = len(a)
    LOG = n.bit_length()
    st = [[0] * n for _ in range(LOG)]
    st[0] = a[:]
    for k in range(1, LOG):
        half = 1 << (k - 1)
        prev = st[k - 1]
        cur = st[k]
        for i in range(n - (1 << k) + 1):
            cur[i] = prev[i] if prev[i] <= prev[i + half] else prev[i + half]
    return st

def rmq_min(st, l, r):
    length = r - l + 1
    k = length.bit_length() - 1
    a = st[k][l]
    b = st[k][r - (1 << k) + 1]
    return a if a <= b else b

class SegTreeMin:
    def __init__(self, a):
        n = len(a)
        self.n = n
        self.t = [10 ** 18] * (4 * n + 5)
        self._build(a, 1, 0, n - 1)

    def _build(self, a, p, l, r):
        if l == r:
            self.t[p] = a[l]
            return
        m = (l + r) // 2
        self._build(a, p * 2, l, m)
        self._build(a, p * 2 + 1, m + 1, r)
        self.t[p] = min(self.t[p * 2], self.t[p * 2 + 1])

    def update(self, pos, val, p=1, l=0, r=None):
        if r is None:
            r = self.n - 1
        if l == r:
            self.t[p] = val
            return
        m = (l + r) // 2
        if pos <= m:
            self.update(pos, val, p * 2, l, m)
        else:
            self.update(pos, val, p * 2 + 1, m + 1, r)
        self.t[p] = min(self.t[p * 2], self.t[p * 2 + 1])

    def query(self, ql, qr, p=1, l=0, r=None):
        if r is None:
            r = self.n - 1
        if ql <= l and r <= qr:
            return self.t[p]
        m = (l + r) // 2
        ans = 10 ** 18
        if ql <= m:
            ans = min(ans, self.query(ql, qr, p * 2, l, m))
        if qr > m:
            ans = min(ans, self.query(ql, qr, p * 2 + 1, m + 1, r))
        return ans

if __name__ == '__main__':
    a = [5, 2, 7, 1, 9, 3, 8]
    st = build_sparse_table(a)
    seg = SegTreeMin(a)
    queries = [(1, 4), (0, 6), (2, 5), (4, 4)]
    for l, r in queries:
        s = rmq_min(st, l, r)
        g = seg.query(l, r)
        brute = min(a[l:r + 1])
        assert s == g == brute, (l, r, s, g, brute)
        print('RMQ[%d,%d]=%d' % (l, r, s))
    # 动态更新测试
    seg.update(3, 0)
    assert seg.query(0, 6) == 0
    print('OK')
```

**PyPy 提示**: ST 表用 list-of-list 即可，预分配可减少内存碎片；查询的 bit_length 计算开销可接受。线段树递归在 PyPy 下 n~2e5 可行，大数据建议把 _build/_query 改迭代或用数组。PyPy 对 while 循环友好，ST 表构建用 for 也可。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | ST 表：预处理 O(n log n)，查询 O(1)；线段树：O(n) 建，O(log n) 查询；Four Russians：O(n log log n) 预处理 O(1) 查询；±1RMQ/笛卡尔树法：O(n) 预处理 O(1) 查询 |
| 空间 | ST 表 O(n log n)；线段树 O(n)；Four Russians O(n log log n)；±1RMQ O(n) |

### 局限

ST 表不支持修改（静态），需动态用线段树；基于状压与笛卡尔树的 O(n)~O(1) 方法常数大、仅适合理论或极大规模随机数据；±1RMQ 只适用于差分 ±1 的序列（其他序列需先转）。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3865 | 2 | 【模板】ST 表：静态区间最大值的 ST 表模板题 | [https://www.luogu.com.cn/problem/P3865](https://www.luogu.com.cn/problem/P3865) |
| SPOJ | RMQ - Range Minimum Query | 3 | 经典 RMQ 模板，ST 表/线段树均可，注意 SPOJ 访问需代理 | [https://www.spoj.com/problems/RMQ/](https://www.spoj.com/problems/RMQ/) |
| CodeChef | Chef And Array | 4 | CP-Algorithms RMQ 页引用的练习，综合区间最值 + 计数 | [https://www.codechef.com/](https://www.codechef.com/) |

## Pitfalls · 易错点

- ST 表查询长度不是 2 的幂时，取 min(st[k][l], st[k][r-2^k+1])，两个区间必须都覆盖查询区间，缺一不可
- LOG 取 n.bit_length() 已够（2^LOG > n），少一层会数组越界
- 线段树数组开 4n；区间查询递归不判空会访问越界节点
- min/max 混淆、闭开区间（0 基/1 基）不统一是常见 WA
- 静态数据误用线段树虽不犯错但多一个 log；动态数据用 ST 表则直接错

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/topic/rmq.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/topic/rmq.md)
- CP-Algorithms ✓ [https://cp-algorithms.com/sequences/rmq.html](https://cp-algorithms.com/sequences/rmq.html)
- CP-Algorithms ✓ [https://cp-algorithms.com/graph/rmq_linear.html](https://cp-algorithms.com/graph/rmq_linear.html)
- 书籍 ✓ `CPH ch9`
