---
id: stoer-wagner
name: Stoer-Wagner 全局最小割
group: G-B-5
stage: advanced
priority: P3
depth_tier: brief
---

# Stoer-Wagner 全局最小割

> 无向正权图的全局最小割（任意 s-t 划分的最小割）：最大邻接贪心合并 + 递归收缩，O(V³)（朴素）或 O(VE+V²log V)。

<!-- 元信息: id=stoer-wagner · group=G-B-5 · stage=advanced · priority=P3 · depth_tier=brief -->

## What · 是什么

Stoer-Wagner 算法求无向带权图的全局最小割（global minimum cut）：把点集分成两个非空集合 C 与 V\C，使跨集合边权和最小。与 s-t 最小割不同，它不指定源汇。算法通过「最大邻接点」贪心 + 合并（contract）递归地把图缩小：每次找一对点 (s,t) 满足 s 是先于 t 被加入集合 A 的最后一个点，则 w(A,t) 是某个 s-t 割的权（可作为候选），把 s、t 合并后继续，共 n-1 次，答案取所有候选割的最小值。复杂度 O(V³)（朴素实现）或 O(VE+V²log V)（堆优化）。

## Why · 为什么

### 直觉 · Intuition

全局最小割必有一条「把 t 从 s 所在的半边切出去」的割（或把 s,t 放一起）。Stoer-Wagner 每次「合并一对点」时都记录一个候选割：最后一次加入集合 A 的点 t 与其余点之间被切开的边权 w(A,t) 恰好是某个把 t 单独（连同其后加入顺序关系）切出的割的权。由于任意全局最小割要么切的是这对点要么不切，合并它们不会丢失最优解，重复 n-1 次覆盖所有可能。

### 原理 · Principle

① 构造序列 A：初始空，每次选 w(A,i)=Σ_{j∈A} d(i,j) 最大的未加入点加入，直到全部加入；设最后加入的是 t、倒数第二是 s；② 记录候选割 w(t)=w(A,t)（对任意 s，它都是 s-t 割的权，数学归纳 Lemma 1 证明）；③ 合并 s、t：删 (s,t) 边，把 t 的邻边权并入 s（d(s,k)+=d(t,k)），|V|-1；④ 重复直到只剩 1 点；⑤ 答案 = 所有候选 w(t) 最小值。关键性质：正权图上「最大邻接点」贪心顺序唯一，保证 w(A,t) 是合法割权。

### 历史 · History

由 Mechthild Stoer 与 Frank Wagner 于 1994/1995 年提出（OI Wiki 记 1995，CP-Alg 记 1994）。它比「跑 n² 次最大流」的朴素做法快得多；堆优化（斐波那契堆理论 O(VE+V²logV)，但常数大实际用二项堆/朴素）是竞赛常用形态。

## How · 实现

### 伪代码

```python
def stoer_wagner(d):   # d: 对称邻接矩阵, 无向带权
    best = INF; n = len(d)
    while n > 1:
        used = [False]*n
        A = []; wsum = [0]*n
        for _ in range(n):   # 最大邻接贪心
            sel = -1
            for i in range(n):
                if not used[i] and (sel==-1 or wsum[i]>wsum[sel]): sel=i
            used[sel]=True; A.append(sel)
            for i in range(n):
                if not used[i]: wsum[i] += d[sel][i]
        s,t = A[-2], A[-1]
        best = min(best, wsum[t])
        for i in range(n):   # 合并 s,t: d[s][i]+=d[t][i], d[i][s]=d[s][i]
            d[s][i] += d[t][i]; d[i][s] = d[s][i]
        # 删除 t：把 t 换成 n-1（行列交换）
        # ...（具体删除用原地数组交换实现）
        n -= 1
    return best
```

### Python 实现

```python
def stoer_wagner(d):
    """Stoer-Wagner 全局最小割（无向正权图）.
    d: 对称邻接矩阵（n×n）. 返回全局最小割容量. 复杂度 O(n^3)."""
    n = len(d)
    best = 10 ** 18
    # 用点列表管理当前收缩后的节点集合（合并时保留 s, 删除 t）
    idx = list(range(n))
    while len(idx) > 1:
        # 最大邻接贪心建序列 A
        used = [False] * len(idx)
        wsum = [0] * len(idx)
        seq = []
        for _ in range(len(idx)):
            sel = -1
            for i in range(len(idx)):
                if not used[i] and (sel == -1 or wsum[i] > wsum[sel]):
                    sel = i
            used[sel] = True
            seq.append(sel)
            for i in range(len(idx)):
                if not used[i]:
                    wsum[i] += d[idx[sel]][idx[i]]
        s, t = seq[-2], seq[-1]
        best = min(best, wsum[t])
        # 合并 s,t: 把 t 的边权并入 s, 删除 t
        ns, nt = idx[s], idx[t]
        for i in range(n):
            d[ns][i] += d[nt][i]
            d[i][ns] = d[ns][i]
        # 从 idx 删除 t
        idx.pop(t)
    return best


if __name__ == "__main__":
    # 三角形每条边权 1: 全局最小割 = 2（切一个点出去要切断两条边）
    d3 = [
        [0, 1, 1],
        [1, 0, 1],
        [1, 1, 0],
    ]
    assert stoer_wagner([row[:] for row in d3]) == 2
    # 四环 1-2-3-4-1 每条权 1: 最小割 = 2（切相邻两点）
    d4 = [
        [0, 1, 0, 1],
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [1, 0, 1, 0],
    ]
    assert stoer_wagner([row[:] for row in d4]) == 2
    # 随机小图与暴力枚举所有 2^(n-1) 划分交叉验证
    import random, itertools
    random.seed(9)
    for _ in range(60):
        n = random.randint(2, 7)
        d = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                w = random.randint(1, 8)
                d[i][j] = d[j][i] = w
        got = stoer_wagner([row[:] for row in d])
        # 暴力: 枚举所有非空真子集
        brute = 10 ** 18
        for mask in range(1, (1 << n) - 1):
            cut = 0
            for i in range(n):
                for j in range(i + 1, n):
                    if ((mask >> i) & 1) != ((mask >> j) & 1):
                        cut += d[i][j]
            brute = min(brute, cut)
        assert got == brute, (d, got, brute)
    print("All tests passed.")
```

**PyPy 提示**: 朴素 O(n³) 在 n=500 时约 1.25e8 次内层循环，PyPy 可过；合并点用「idx 列表 + 原矩阵累加」避免频繁重分配；找最大 wsum 每次 O(n)，整体 O(n²) 每轮，共 O(n³)。求最小割本身（点集划分）需另记 A 序列与 s/t 关系。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(V³)（朴素最大邻接）；O(VE + V²log V)（堆优化） |
| 空间 | O(V²) |

### 局限

只适用于无向正权图（负权/有向不适用）；O(V³) 在 V≥1000 时吃力；Python 版适合 n≤500；需要输出割集时需在合并时记录 s、t 归属。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P5632 | 5 | 【模板】Stoer-Wagner 算法：全局最小割模板，OI Wiki 例题 | [https://www.luogu.com.cn/problem/P5632](https://www.luogu.com.cn/problem/P5632) |
| SPOJ | COT - Classical | 4 | SPOJ 全局最小割类问题（CP-Alg 参考） | [https://www.spoj.com/problems/COT/](https://www.spoj.com/problems/COT/) |

## Pitfalls · 易错点

- 必须是无向正权图：有负权或非对称矩阵时最大邻接贪心性质失效
- 合并 s、t 时要把 t 的所有邻边权累加到 s（不是替换），并删掉 t 的行列
- 候选割 wsum[t] 在 s/t 合并前记录，不能合并后取
- 矩阵累加时保持对称性（d[s][i] 与 d[i][s] 同步更新）
- 求最小割的「点集划分」需要额外回溯记录（基础版只给容量）

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/stoer-wagner.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/stoer-wagner.md)
- CP-Algorithms ✓ [https://cp-algorithms.com/graph/stoer_wagner_mincut.html](https://cp-algorithms.com/graph/stoer_wagner_mincut.html)
