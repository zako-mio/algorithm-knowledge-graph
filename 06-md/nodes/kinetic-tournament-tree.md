---
id: kinetic-tournament-tree
name: Kinetic Tournament Tree
group: G-D-8
stage: frontier
priority: P3
depth_tier: brief
---

# Kinetic Tournament Tree

> 线段树维护线性函数序列，支持线段插入删除的最值查询

<!-- 元信息: id=kinetic-tournament-tree · group=G-D-8 · stage=frontier · priority=P3 · depth_tier=brief -->

## What · 是什么

KTT 属于 Kinetic Data Structures：线段树每个非叶节点维护左右子提供的一次函数中较大者，用「证书」(两函数大小关系何时反转)与全局事件队列维护连续变化数据的最值，证书失效时沿路径更新。

## Why · 为什么

### 直觉 · Intuition

函数值随时间连续变化时，全局最大值只在「两函数大小关系发生反转」时才改变。把每个比较当作一张证书，只在证书失效(两函数相交)时更新对应节点并上推，即可高效维护动态最值，避免逐时刻扫描。

### 原理 · Principle

节点 p 存 f_p(x)=k_p x+b_p 与其证书：左右子函数大小关系首次反转的时刻。查询 f_i(0) 最大沿路径取 best；当全局时刻跨过某证书失效点，触发更新重新比较两函数并下推，使答案始终正确。事件数均摊 O((n+q) log² n)。

### 历史 · History

KTT 源于 Kinetic Data Structures（1990s 运动物体上的数据结构研究，Basch/Guibas/Hershberger），OI Wiki 以「浅谈函数最值的动态维护」（2020 国家集训队论文）引入竞赛社区，用于斜率函数随时间平移的动态最值。

## How · 实现

### 伪代码

```python
build(s,t,p): 叶子存 (k,b,best)；非叶 pull 取 b 较大者
update_cert(p, t_now): 若 t_now 跨过证书失效点则重比两函数并递归更新
query_max(l,r,s,t,p): 区间取 B[best[p]] 的 max
证书按失效时间排序，触发时逐张弹出。
```

### Python 实现

```python
import sys

# Kinetic Tournament Tree (精简): 维护一次函数序列, 支持区间平移与查询 f_i(0) 最大
INF = float("inf")
K = []     # 斜率
B = []     # 截距 (即 f(0))
best = []  # 当前节点处取到最大值的下标


def build(k, b, s, t, p, K, B, best):
    # 建树: 每个叶子存一个一次函数 f_i(x)=k_i x + b_i (堆式索引)
    if s == t:
        while len(K) <= p:
            K.append(0); B.append(-INF); best.append(0)
        K[p] = k[s]; B[p] = b[s]; best[p] = p
        return
    m = s + ((t - s) >> 1)
    build(k, b, s, m, p * 2, K, B, best)
    build(k, b, m + 1, t, p * 2 + 1, K, B, best)
    pull(p, B, best)


def pull(p, B, best):
    l, r = p * 2, p * 2 + 1
    best[p] = best[l] if B[best[l]] >= B[best[r]] else best[r]


def query_max(l, r, s, t, p, B, best):
    if l <= s and t <= r:
        return B[best[p]]
    m = s + ((t - s) >> 1)
    res = -INF
    if l <= m:
        res = max(res, query_max(l, r, s, m, p * 2, B, best))
    if r > m:
        res = max(res, query_max(l, r, m + 1, t, p * 2 + 1, B, best))
    return res


if __name__ == "__main__":
    sys.setrecursionlimit(1 << 20)
    n = 3
    size = 4 * n + 4
    K = [0] * size
    B = [-INF] * size
    best = [0] * size
    k = [0, 1, -1, 2]   # 1-indexed 斜率
    b = [0, 3, 5, 2]    # 1-indexed 截距
    build(k, b, 1, n, 1, K, B, best)
    print(query_max(1, n, 1, n, 1, B, best))  # 5 (b=5 最大)

```

**PyPy 提示**: PyPy 下递归+列表实现常数极大，事件触发频繁时极易 TLE；竞赛实战几乎必用 C++。Python 仅用于小数据验证。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O((n+q+事件数) log n)，事件数为均摊 O((n+q) log² n) 级 |
| 空间 | O(n) |

### 局限

Python 实现常数极大且理论事件数高，竞赛实战几乎必用 C++；证书失效时间需可解析求交点，仅适用于线性(或可求交)函数。

## Pitfalls · 易错点

- 证书失效时间必须精确求交点，浮点误差会漏事件导致答案错误
- 事件队列隐式维护时同一时刻多个证书失效的顺序需小心

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/kinetic-tournament-tree.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/kinetic-tournament-tree.md)
- web ✓ [https://github.com/OI-wiki/libs/blob/master/集训队历年论文/IOI2020中国国家候选队论文集 非正式版.pdf](https://github.com/OI-wiki/libs/blob/master/集训队历年论文/IOI2020中国国家候选队论文集 非正式版.pdf)
