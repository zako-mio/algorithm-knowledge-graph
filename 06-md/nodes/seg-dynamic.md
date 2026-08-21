---
id: seg-dynamic
name: 动态开点线段树
group: G-A-6
stage: advanced
priority: P1
depth_tier: standard
---

# 动态开点线段树

> 按需创建节点，支持大值域离散化无需预先开空间

<!-- 元信息: id=seg-dynamic · group=G-A-6 · stage=advanced · priority=P1 · depth_tier=standard -->

## What · 是什么

不再用 2p/2p+1 固定编号，而是用 ls[p]/rs[p] 显式记录子节点编号，仅在真正访问某子区间时才新建节点，使大值域(如 1e18)无需离散化即可直接建树。

## Why · 为什么

### 直觉 · Intuition

值域 1e18 时堆式 4N 数组开不下；但若实际只改/查了 Q 个点，真正用到的节点不过 O(Q log V) 个——那干脆用多少开多少。

### 原理 · Principle

全局维护节点池 ls/rs/sum 数组与计数器 tot，new_node() 每次追加一个新节点。update/query 递归时若 p==0 表示该子区间从未被创建，按需求新建(单点)或直接返回空值(查询)。区间修改仍可配懒标记，但 pushdown 时若子节点不存在要先 new_node。

### 历史 · History

动态开点线段树是显式节点结构（平衡树/主席树）思想在线段树上的应用，OI Wiki ds/seg 章节「动态开点线段树」小节介绍，广泛用于权值线段树与大值域问题。

## How · 实现

### 伪代码

```python
update(x,f,s,t,p): 若 !p 则 p=new_node(); sum[p]+=f; 若 s==t 返回; 按 m 递归 ls/rs
query(l,r,s,t,p): 若 !p 返回 0; 若 ⊆ 返回 sum[p]; 否则递归
```

### Python 实现

```python
import sys

# 动态开点线段树: 大值域(如 1e18)离散化或直接按需建点
MAXV = 1 << 60
tot = 0
ls = [0]
rs = [0]
sm = [0]


def new_node():
    global tot
    tot += 1
    ls.append(0)
    rs.append(0)
    sm.append(0)
    return tot


def update(x, f, s, t, p):
    # 单点修改: 位置 x 加 f
    if not p:
        p = new_node()
    sm[p] += f
    if s == t:
        return p
    m = s + ((t - s) >> 1)
    if x <= m:
        ls[p] = update(x, f, s, m, ls[p])
    else:
        rs[p] = update(x, f, m + 1, t, rs[p])
    return p


def query(l, r, s, t, p):
    # 区间查询 [l,r] 的和
    if not p or l > t or r < s:
        return 0
    if l <= s and t <= r:
        return sm[p]
    m = s + ((t - s) >> 1)
    res = 0
    if l <= m:
        res += query(l, r, s, m, ls[p])
    if r > m:
        res += query(l, r, m + 1, t, rs[p])
    return res


if __name__ == "__main__":
    sys.setrecursionlimit(1 << 20)
    root = new_node()
    root = update(3, 7, 1, MAXV, root)
    root = update(100, 4, 1, MAXV, root)
    print(query(1, 10, 1, MAXV, root))   # 7
    print(query(1, 200, 1, MAXV, root))  # 11

```

**PyPy 提示**: 节点池用并行列表 ls/rs/sum + 计数器 tot，避免对象数组开销；递归深度需 setrecursionlimit。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O((N+Q)log V) — V 为值域；只创建访问过的节点 |
| 空间 | O((N+Q)log V) — 节点池按需增长 |

### 局限

Python 全局可变列表(append)做节点池可行但常数大；值域过大应先离散化把 V 压到 n 量级再开 4N 静态数组更快；区间修改可用标记永久化免去 pushdown 时的 new_node 开销。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P13825 | 5 | 线段树1.5 动态开点模板：区间加+区间和，大值域直接开点 | [https://www.luogu.com.cn/problem/P13825](https://www.luogu.com.cn/problem/P13825) |

## Pitfalls · 易错点

- 递归时 p==0 必须先 new_node 再继续，否则写空指针
- 区间修改用懒标记时 pushdown 里也要 new 子节点，或改用标记永久化
- 值域能离散化就离散化：动态开点常数远大于静态 4N 数组

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/seg/#动态开点线段树](https://oi-wiki.org/ds/seg/#动态开点线段树)
- CP-Algorithms ✓ [https://cp-algorithms.com/data_structures/segment_tree.html](https://cp-algorithms.com/data_structures/segment_tree.html)
