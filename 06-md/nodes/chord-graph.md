---
id: chord-graph
name: 弦图
group: G-B-9
stage: advanced
priority: P3
depth_tier: brief
---

# 弦图

> 任意>3环都有弦的图，完美消除序列(MCS)使最大团/色数/独立集等NP难问题O(n+m)可解

<!-- 元信息: id=chord-graph · group=G-B-9 · stage=advanced · priority=P3 · depth_tier=brief -->

## What · 是什么

弦图（chordal graph）是任意长度大于 3 的环都含有一条弦（连接环上不相邻两点的边）的图。弦图的重要性在于：一般图上 NP 难的极大团/色数/最大独立集/最小团覆盖问题，在弦图上都有 O(n+m) 的线性算法。关键工具是完美消除序列（PES，perfect elimination ordering）：一个顶点序列 v1..vn 使得每个 vi 在 {vi..vn} 诱导子图中是单纯点（simplicial vertex，其邻域构成团）。判定弦图 + 求 PES 用最大势算法（MCS, Maximum Cardinality Search）O(n+m)，随后用 PES 可线性求出极大团、色数、最大独立集、最小团覆盖。

## Why · 为什么

### 直觉 · Intuition

『有弦』让弦图极其『稠密而规整』：单纯点的存在使我们可以反复『剥掉』一个点而不破坏结构（弦图的任意诱导子图仍是弦图，且至少有一个单纯点）。完美消除序列就是按『越晚加入的越接近团』的次序剥点，剥点过程就是所有团信息的编码，因此一个序列搞定四个 NP 难问题。

### 原理 · Principle

判定：图是弦图 ⇔ 存在完美消除序列（OI Wiki Lemma 8）。MCS 算法：逆序标号，每次选 label 最大的未标号点（label=与已标号点相邻数），用链表维护，每条边至多贡献 2 次故 O(n+m)。验证 PES：对每个 vi 取其后继中 rank 最小（最早出现）的邻点 c1，只需验证 c1 与其余后继邻点两两相连，O(n+m)。
应用：极大团 = {x} ∪ N(x)（x 为团中在 PES 上最前的点）；色数 = 团数 = max |{x}∪N(x)|（按 PES 从后往前贪心染色）；最大独立集 = 按 PES 从前往后选无冲突点；最小团覆盖 = 上述独立集各点对应团，均有线性算法。

### 历史 · History

弦图与完美消除序列理论成型于 1960s（Fulkerson-Gross、Rose 等），线性判定与 MCS 归功于 Tarjan & Yannakakis 1984（SIAM J. Comput. 13:566-579）。OI Wiki 弦图章节（graph/chord）系统给出定义、PES、MCS 与全部线性算法及证明，并以 SPOJ FISHNET、洛谷 P3196[HNOI2008]神奇的国度、P3852[TJOI2007]小朋友为习题。

## How · 实现

### 伪代码

```python
# MCS 求完美消除序列（逆序标号）
label = [0]*(n+1); order = []
for i in range(n, 0, -1):
    v = 取 label 最大的未标号点
    order.append(v); mark v
    for u in adj[v] 未标号: label[u] += 1
# 验证 PES: 对每个 vi, c1 = 后继中 rnk 最小的邻点
#   若存在后继邻点 u (u!=c1) 与 c1 不相邻 => 非弦图
# 用 PES 线性求极大团/色数/最大独立集/最小团覆盖
```

### Python 实现

```python
import sys
from collections import defaultdict, deque


def mcs_peo(n, adj):
    """最大势算法求 (可能的) 完美消除序列，返回 (逆序即 PES) 与 rnk。
    adj: list[set] 邻接表 (0-index)。
    注: 输出序列是否真正 PES 需后续验证（本函数仅做 MCS 选序）。
    """
    label = [0] * n
    used = [False] * n
    order = []
    buckets = defaultdict(set)  # label -> 点集
    for v in range(n):
        buckets[0].add(v)
    max_label = 0
    for _ in range(n):
        while max_label >= 0 and not buckets[max_label]:
            max_label -= 1
        if max_label < 0:
            break
        v = buckets[max_label].pop()
        used[v] = True
        order.append(v)
        for u in adj[v]:
            if not used[u]:
                buckets[label[u]].discard(u)
                label[u] += 1
                buckets[label[u]].add(u)
                if label[u] > max_label:
                    max_label = label[u]
    return order[::-1], {v: i for i, v in enumerate(order[::-1])}  # PES, rnk


def verify_peo(n, adj, peo, rnk):
    """验证 peo 是否为完美消除序列（O(n+m)）。"""
    for idx, v in enumerate(peo):
        later = [u for u in adj[v] if rnk[u] > rnk[v]]
        if not later:
            continue
        c1 = min(later, key=lambda u: rnk[u])
        for u in later:
            if u != c1 and u not in adj[c1]:
                return False
    return True


def is_chordal(n, edges):
    """判定无向图是否为弦图。"""
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    peo, rnk = mcs_peo(n, adj)
    return verify_peo(n, adj, peo, rnk)


def max_clique_size(n, edges):
    """弦图上色数 = 团数 = max |{x} ∪ N(x)|。"""
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    peo, rnk = mcs_peo(n, adj)
    best = 0
    for v in range(n):
        cnt = 1 + sum(1 for u in adj[v] if rnk[u] > rnk[v])
        best = max(best, cnt)
    return best


if __name__ == "__main__":
    sys.setrecursionlimit(10 ** 6)
    # 树是弦图（无环）
    tree = [(0, 1), (1, 2), (2, 3), (1, 4)]
    assert is_chordal(5, tree)
    # 4 环 C4 不是弦图（长度 4 无弦）
    c4 = [(0, 1), (1, 2), (2, 3), (3, 0)]
    assert not is_chordal(4, c4)
    # 加一条对角线的 C4 (三角化) 是弦图
    fan = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]
    assert is_chordal(4, fan)
    # K5 完全图是弦图, 色数=5
    k5 = [(i, j) for i in range(5) for j in range(i + 1, 5)]
    assert is_chordal(5, k5)
    assert max_clique_size(5, k5) == 5
    # 三角化 C4 最大团 3
    assert max_clique_size(4, fan) == 3
    print("chord-graph 自测通过：弦图判定(MCS+PES验证)与最大团数计算正确")

```

**PyPy 提示**: MCS 用 dict 桶代替链表（Python 无内置桶结构），O(n+m) 均摊。验证 PES 的 c1 取 rnk 最小邻点。n 大时 set 邻接表内存可控；完全图/稠密图注意邻接矩阵勿用。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | MCS 选序 O(n+m)，PES 验证 O(n+m)，团/色数/独立集均 O(n+m) |
| 空间 | O(n+m) |

### 局限

先决条件：图必须真的是弦图，否则 MCS 给出的序列不是 PES、算法结果无意义。稠密图（如完全图）仍需 O(n²) 边读入。PES 的贪心染色得到的是最少数色但不保证输出合法染色方案唯一。判定算法实现细节（链表 vs 桶）要保证 label 维护正确。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| SPOJ | FISHNET | 6 | Fishing Net：弦图判定模板题（MCS+PES 验证） | [https://www.spoj.com/problems/FISHNET/](https://www.spoj.com/problems/FISHNET/) |
| Luogu | P3196 | 6 | HNOI2008 神奇的国度：弦图求色数/团数 | [https://www.luogu.com.cn/problem/P3196](https://www.luogu.com.cn/problem/P3196) |
| Luogu | P3852 | 6 | TJOI2007 小朋友：弦图最大独立集/团覆盖 | [https://www.luogu.com.cn/problem/P3852](https://www.luogu.com.cn/problem/P3852) |

## Pitfalls · 易错点

- MCS 逆序标号的方向：输出的是 PES 而非标号顺序，别弄反
- 验证 PES 只需查 c1 与其余，不能对每个后继都 O(deg) 验证（退化为 O(nm)）
- 非弦图时 MCS 结果无意义，判定必须走验证步骤
- 团数公式 \|{x}∪N(x)\| 的 N(x) 只取 PES 上 rank 在 x 之后的点
- 桶/链表维护 label 时删旧桶要 discar（set）而非 remove（可能不存在）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/chord/](https://oi-wiki.org/graph/chord/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/chord.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/chord.md)
- 论文 ✓ `Tarjan & Yannakakis, SIAM J. Comput. 13 (1984) 566-579`
