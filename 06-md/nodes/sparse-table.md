---
id: sparse-table
name: ST表(稀疏表)
group: G-A-5
stage: basic
priority: P0
depth_tier: deep
---

# ST表(稀疏表)

> 倍增预处理O(n log n) O(1)回答可重复贡献问题(RMQ/GCD)，不支持修改

<!-- 元信息: id=sparse-table · group=G-A-5 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

ST 表(Sparse Table，稀疏表)解决静态数组的『可重复贡献问题』：区间最值(RMQ)、区间 GCD/按位与/按位或等。预处理 st[k][i] = 从 i 开始长度为 2^k 的区间答案，倍增递推 st[k][i]=opt(st[k−1][i], st[k−1][i+2^(k−1)])，O(n log n) 时间空间。查询 [l,r]：取 k=⌊log2(r−l+1)⌋，答案为 opt(st[k][l], st[k][r−2^k+1])——两个区间可以重叠(幂等性质 opt(x,x)=x)，O(1) 回答。优点：实现极简、查询最快。缺点：不支持修改、只能处理幂等(可重复贡献)运算，不能做区间和。

## Why · 为什么

### 直觉 · Intuition

把每个位置的 1,2,4,8,… 长区间答案都存下来(倍增)。查询时用两个 2^k 长的区间完整覆盖 [l,r](允许重叠)，因为『重叠不影响答案』(min(min(a),min(a))=min(a))。就像用两块大积木拼出任意长度的尺子。log 表预处理后 O(1) 定位。

### 原理 · Principle

可重复贡献运算 opt 满足幂等 opt(x,x)=x 与结合律。预处理 st[k][i]=opt over a[i..i+2^k−1]，递推合并两半。查询区间长 len，k=⌊log₂len⌋，两区间 [l,l+2^k−1] 与 [r−2^k+1,r] 并覆盖 [l,r]，答案 opt(st[k][l],st[k][r−2^k+1])。正确性依赖幂等性：重叠部分被算两次仍正确。RMQ、GCD、AND、OR 均满足；区间和/积不满足幂等，不能直接用(需划分不重叠区间会退化 O(log n)，可改用线段树或稀疏表变体)。

### 历史 · History

稀疏表技术源于倍增(以 2 的幂为步长跳跃)思想，在 RMQ 问题上由 Mikkel Thorup 等理论工作与 1990 年代竞赛普及。它与 LCA 的倍增法、二进制提升(Binary Lifting)是同一思路的不同载体。静态 RMQ 的 O(1) 查询至今由 ST 表在竞赛中统治。

## How · 实现

### 伪代码

```python
build(a):
  log[1]=0; log[i]=log[i//2]+1
  st[0] = a
  for k=1..log[n]:
    st[k][i] = opt(st[k-1][i], st[k-1][i+2^(k-1)]) for i in 0..n-2^k
query(l,r):
  k = log[r-l+1]
  return opt(st[k][l], st[k][r-2^k+1])
```

### Python 实现

```python
import math


class SparseTable:
    """ST 表: O(n log n) 预处理, O(1) 查询可重复贡献问题 (RMQ/GCD/AND/OR)。不支持修改。"""
    def __init__(self, a, op=min):
        self.n = len(a)
        self.op = op
        self.log = [0] * (self.n + 1)
        for i in range(2, self.n + 1):
            self.log[i] = self.log[i // 2] + 1
        self.st = [a[:]]
        j = 1
        while (1 << j) <= self.n:
            prev = self.st[-1]
            half = 1 << (j - 1)
            cur = [op(prev[i], prev[i + half]) for i in range(self.n - (1 << j) + 1)]
            self.st.append(cur)
            j += 1

    def query(self, l, r):
        """[l, r] 闭区间, 0-based。要求 op 可重复贡献(幂等)+结合律。"""
        k = self.log[r - l + 1]
        return self.op(self.st[k][l], self.st[k][r - (1 << k) + 1])


if __name__ == "__main__":
    import random
    a = [random.randint(-1000, 1000) for _ in range(30)]
    st = SparseTable(a, min)
    for _ in range(3000):
        l = random.randint(0, len(a) - 1)
        r = random.randint(l, len(a) - 1)
        assert st.query(l, r) == min(a[l:r + 1])
    stg = SparseTable([abs(x) for x in a], math.gcd)
    import functools
    for _ in range(500):
        l = random.randint(0, len(a) - 1)
        r = random.randint(l, len(a) - 1)
        assert stg.query(l, r) == functools.reduce(math.gcd, [abs(x) for x in a[l:r + 1]])
    print("sparse OK")

```

**PyPy 提示**: st 用 list-of-lists(每层一个 list)，n=1e5 时约 n·log n≈1.7M 个 int，PyPy 内存约 50MB 内可接受。查询是纯索引+op，常数极小，适合海量查询(10^7 次)。log 表用整数数组而非 math.log2(浮点精度问题)。若只查 RMQ 可只存 min。注意 st[k] 长度递减，越界时直接用 st[-1] 层数不足需按实际长度初始化。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 预处理 O(n log n)，查询 O(1) |
| 空间 | O(n log n) |

### 局限

1) 只支持静态(无修改)；2) 只支持幂等/可重复贡献运算(RMQ/GCD/AND/OR)，不支持区间和；3) 内存 O(n log n) 对大 n(>1e6) 有压力(可用两遍扫描优化但少见)；4) 与线段树相比不支持在线修改与合并非幂等信息；5) log 表需整型避免浮点误差。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3865 | 2 | 【模板】ST 表：区间最大值，n=1e5 海量查询，ST 表标准模板 | [https://www.luogu.com.cn/problem/P3865](https://www.luogu.com.cn/problem/P3865) |
| Luogu | P2880 | 2 | USACO Balanced Lineup：区间最大−最小，两个 ST 表 | [https://www.luogu.com.cn/problem/P2880](https://www.luogu.com.cn/problem/P2880) |
| CSES | 1647 | 2 | Static Range Minimum Queries：ST 表/稀疏表 O(1) 查询模板 | [https://cses.fi/problemset/task/1647](https://cses.fi/problemset/task/1647) |

## Pitfalls · 易错点

- 把 ST 表用于区间和(非幂等)，重叠会重复计数给出错误答案
- log 表漏掉 log[1]=0，或对 len=1 的区间查询 k 越界
- 预处理循环条件 (1<<j)<=n 漏等号导致最后一层不足
- 修改数组后继续用旧 ST 表(不支持修改，必须重建)
- 用 math.log2 求 k 受浮点误差影响，应查整数 log 表

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/sparse-table/](https://oi-wiki.org/ds/sparse-table/)
- CP-Algorithms ✓ [https://cp-algorithms.com/data_structures/sparse-table.html](https://cp-algorithms.com/data_structures/sparse-table.html)
- 书籍 ✓ `CPH ch9 p93`
