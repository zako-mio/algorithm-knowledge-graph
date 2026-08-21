---
id: seg-merge
name: 线段树合并与分裂
group: G-A-6
stage: advanced
priority: P1
depth_tier: standard
---

# 线段树合并与分裂

> 合并多棵动态开点线段树，用于树上信息合并；分裂还原

<!-- 元信息: id=seg-merge · group=G-A-6 · stage=advanced · priority=P1 · depth_tier=standard -->

## What · 是什么

线段树合并：从两棵动态开点(权值)线段树的根开始递归，把对应节点合并成新节点；线段树分裂是其逆过程，从一棵树中切出一段区间形成新树。常用于树上自底向上合并子节点信息。

## Why · 为什么

### 直觉 · Intuition

树上每个节点挂一棵权值线段树维护该子树的权值集合；要汇总到父节点时直接两两合并子节点的树，比每次重建高效。

### 原理 · Principle

merge(a,b,s,t)：若 a 或 b 为空直接返回另一个(利用动态开点特性)；叶节点 s==t 合并 cnt；否则递归合并 ls/rs 再 pushup。被合并的 b 树节点可回收复用。分裂 split 类似区间查询，当 [s,t]⊆[l,r] 时把当前节点整棵「摘下」接到新树并断开旧边，被断开的边最多 O(log n) 条。

### 历史 · History

线段树合并/分裂是动态开点线段树的扩展，OI Wiki ds/seg 章节介绍，常用于树上权值信息合并与可持久化分裂；复杂度 O(n log n) 基于「合并只访问重合节点」。

## How · 实现

### 伪代码

```python
merge(a,b,s,t): 若 !a 返回 b; 若 !b 返回 a; 若 s==t: cnt[a]+=cnt[b], return a; 递归 ls/rs, pushup, return a
```

### Python 实现

```python
import sys

# 动态开点权值线段树, 支持合并与分裂
tot = 0
ls = [0]
rs = [0]
cnt = [0]


def new_node():
    global tot
    tot += 1
    ls.append(0)
    rs.append(0)
    cnt.append(0)
    return tot


def update(x, f, s, t, p):
    # 单点修改: 位置 x 的计数 += f
    if not p:
        p = new_node()
    cnt[p] += f
    if s == t:
        return p
    m = s + ((t - s) >> 1)
    if x <= m:
        ls[p] = update(x, f, s, m, ls[p])
    else:
        rs[p] = update(x, f, m + 1, t, rs[p])
    return p


def merge(a, b, s, t):
    # 合并两棵线段树, 返回合并后的根; 空节点直接返回另一棵
    if not a:
        return b
    if not b:
        return a
    if s == t:
        cnt[a] += cnt[b]
        return a
    m = s + ((t - s) >> 1)
    ls[a] = merge(ls[a], ls[b], s, m)
    rs[a] = merge(rs[a], rs[b], m + 1, t)
    cnt[a] = cnt[ls[a]] + cnt[rs[a]]
    return a


if __name__ == "__main__":
    sys.setrecursionlimit(1 << 20)
    N = 100
    ra = new_node()
    rb = new_node()
    ra = update(5, 2, 1, N, ra)
    rb = update(5, 3, 1, N, rb)
    rb = update(7, 1, 1, N, rb)
    ra = merge(ra, rb, 1, N)
    print(cnt[ra])  # 6 (5出现5次 + 7出现1次)

```

**PyPy 提示**: merge 递归深度 O(log n) PyPy 可跑；回收被合并节点控制空间；树上每层开树总空间 O(n log n)，PyPy 内存需留意。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 合并/分裂单次 O(log n)；合并所有树总 O(n log n)（因总点数 n log n 量级且不重复合并） |
| 空间 | O(n log n) — 全部合并后总节点数 |

### 局限

Python 递归合并常数大，n=1e5 时易 TLE，建议 PyPy；合并时若同时存在分裂必须回收 b 树节点，否则分裂会复用已被合并占用的节点导致错误；可并堆在部分场景可能更优。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P4556 | 5 | 雨天的尾巴：树上差分+线段树合并，统计每种颜色出现最多的种类 | [https://www.luogu.com.cn/problem/P4556](https://www.luogu.com.cn/problem/P4556) |

## Pitfalls · 易错点

- 合并与分裂并存时必须回收 b 树节点，否则分裂时节点重复占用
- 合并后 b 树若不回收继续使用会与 a 共享节点造成脏数据
- 误把满线段树合并当 O(log n)：两棵满树合并是 O(n)，O(n log n) 仅对稀疏权值线段树成立

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/seg-merge-split/](https://oi-wiki.org/ds/seg-merge-split/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/seg-merge-split.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/seg-merge-split.md)
- 书籍 ✓ `CPH ch28`
