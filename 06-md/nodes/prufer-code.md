---
id: prufer-code
name: Prüfer序列
group: G-B-7
stage: advanced
priority: P2
depth_tier: standard
---

# Prüfer序列

> 树与 n-2 长度序列的双射，证明 Cayley 公式 n^(n-2)，标号树计数利器

<!-- 元信息: id=prufer-code · group=G-B-7 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

Prüfer 序列把「n 个带标号节点的树」与「长度为 n-2、每个元素在 [1,n] 的整数序列」建立一一对应（双射）。构造（树→序列）：重复 n-2 次——选出当前编号最小的叶节点删去，把与它相连的节点编号写入序列。重建（序列→树）：由序列统计各点度数（每个数出现次数+1），重复从叶集取最小叶与序列当前位置连边并更新度数，最后剩余两点连边。序列中节点 v 的出现次数恰为 deg(v)-1。由此立得 Cayley 公式：n 个节点的完全图生成树数为 n^(n-2)，并可推广到给定度数序列的树计数 n-2 项排列数，以及「把 k 个连通块加边连成树」的方案数 n^(k-2)·∏s_i。

## Why · 为什么

### 直觉 · Intuition

为什么偏要删「编号最小」的叶？因为要保证编码可逆、不依赖选择顺序。每次删除都唯一确定，序列也就唯一；反过来给定序列和度数，每步「最小叶 + 下一个数」也唯一，于是编码解码互逆，形成双射。既然树和序列一一对应，数「n 个标号点的树」就等于数「长度 n-2 的序列」= n^(n-2)，组合计数因此变得极其简单。

### 原理 · Principle

树→序列用堆维护当前叶集（度数=1 的节点），每次取最小叶删去并记录其唯一邻居；邻居度数减到 1 则入堆，O(n log n)；线性版用指针 p：始终指向最小未删叶，删除后若新叶编号小于 p 立即处理否则 p 向后扫。序列→树：先由序列得到全部度数（初值 1，每个出现 +1），用堆取最小度 1 节点与序列当前位置连边（两边度数-1），结束后剩余两个度 1 节点互连。性质：每个 v 出现 deg(v)-1 次；n 号点（根）永不删除。应用：①Cayley n^(n-2)；②固定度数 d_1..d_n 的树数 = (n-2)! / ∏(d_i-1)!（序列中 d_i-1 个 i 的排列数）；③k 个连通块（大小 s_i）加 k-1 条边连成树的方案 = n^(k-2)·∏s_i。

### 历史 · History

Heinz Prüfer 于 1918 年提出该编码，最初即用于证明 Cayley 公式（n 个标号点完全图的生成树数 = n^(n-2)）。OI Wiki 的 prufer 页翻译自 e-maxx/CP-Algorithms 同源条目，给出构造/线性构造/重建/Cayley 与连通块加边推广；CP-Algorithms 单列 prufer_code 条目含双向线性算法与「使图连通加边方案数」。两源交叉一致。

## How · 实现

### 伪代码

```python
encode(tree):  # 树→序列, O(n log n)
  deg = 各点度数; leaf = 度1的点集(堆/最小优先)
  for i in 1..n-2:
    x = leaf.pop_min()
    y = x 的未删邻居
    code[i] = y
    deg[y] -= 1
    if deg[y] == 1: leaf.push(y)
decode(code):  # 序列→树, O(n log n)
  n = len(code)+2; deg[i]=1+code中出现次数
  leaf = 度1点集
  for y in code:
    x = leaf.pop_min(); 连边(x,y); deg[x]-=1; deg[y]-=1
    if deg[y]==1: leaf.push(y)
  最后连剩余两点
```

### Python 实现

```python
import heapq


def pruefer_encode(n, edges):
    adj = [[] for _ in range(n + 1)]
    deg = [0] * (n + 1)
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
        deg[a] += 1
        deg[b] += 1
    removed = [False] * (n + 1)
    leaves = [i for i in range(1, n + 1) if deg[i] == 1]
    heapq.heapify(leaves)
    code = []
    for _ in range(n - 2):
        x = heapq.heappop(leaves)
        removed[x] = True
        y = next(v for v in adj[x] if not removed[v])
        code.append(y)
        deg[y] -= 1
        if deg[y] == 1:
            heapq.heappush(leaves, y)
    return code


def pruefer_decode(code):
    n = len(code) + 2
    deg = [1] * (n + 1)
    for x in code:
        deg[x] += 1
    leaves = [i for i in range(1, n + 1) if deg[i] == 1]
    heapq.heapify(leaves)
    edges = []
    for y in code:
        x = heapq.heappop(leaves)
        edges.append((x, y))
        deg[x] -= 1
        deg[y] -= 1
        if deg[y] == 1:
            heapq.heappush(leaves, y)
    a, b = heapq.heappop(leaves), heapq.heappop(leaves)
    edges.append((a, b))
    return edges


def main():
    n = 7
    edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)]
    code = pruefer_encode(n, edges)
    print("prufer code =", code)
    assert sorted(code) == sorted([2, 2, 1, 3, 3]), code
    back = pruefer_decode(code)
    # 解码得到的树应仍是一棵连通且边集等价（同构意义上）的树
    assert len(back) == n - 1
    adj = [[] for _ in range(n + 1)]
    for a, b in back:
        adj[a].append(b)
        adj[b].append(a)
    seen = [False] * (n + 1)
    stack = [1]
    seen[1] = True
    cnt = 0
    while stack:
        u = stack.pop()
        cnt += 1
        for v in adj[u]:
            if not seen[v]:
                seen[v] = True
                stack.append(v)
    assert cnt == n, "not a tree"
    # Cayley: n=5 时生成树数应为 5^(5-2)=125，任意一棵树编码应长 3 且解码回 5 点
    code5 = pruefer_encode(5, [(1, 2), (2, 3), (3, 4), (4, 5)])
    assert len(code5) == 3
    print("OK")


if __name__ == "__main__":
    main()

```

**PyPy 提示**: heapq 版 O(n log n) 足够模板；线性版指针实现可避免堆开销，PyPy 下两者都可行，n=1e6 建议线性版。deg 用 list，堆操作 PyPy JIT 友好。注意标号从 1 开始与 CP-Algorithms 的 0 基实现不同，别混用。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 构造/重建 O(n log n)（堆）或 O(n)（线性指针版） |
| 空间 | O(n) — 度数数组 + 邻接表/堆 |

### 局限

n=1 时序列长度 0 无意义，需特判（约定 n>=2）。实际建树/存树用 Prüfer 序列并不划算（仅编码长度省了常数），其价值几乎全在组合计数与证明；度数序列计数要求所有 d_i>=1 且 Σ(d_i-1)=n-2。Cayley 公式的 n^(n-2) 在模非质数时需用一般整数幂。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P6086 | 3 | 【模板】Prüfer 序列：给树求序列、给序列建树，双向模板 | [https://www.luogu.com.cn/problem/P6086](https://www.luogu.com.cn/problem/P6086) |
| UVA | 10843 | 3 | Anne's game：Cayley 公式 n^(n-2) 直接应用 | [https://onlinejudge.org/external/108/10843.pdf](https://onlinejudge.org/external/108/10843.pdf) |
| Codeforces | 156D | 2600 | Clues：k 个连通块加边连成树的方案数 n^(k-2)*∏s_i | [https://codeforces.com/contest/156/problem/D](https://codeforces.com/contest/156/problem/D) |

## Pitfalls · 易错点

- n=1 无定义，特判输出（通常 0 或按题意）
- 删叶时找「未删邻居」：需在删除时标记 removed，否则可能指向已删点
- 解码时最后剩余两个点都要度数为 1 且直接连边，别漏最后一对
- 统计度数：初值 1（每个点至少度为 1），序列中每个出现 +1
- Cayley 公式在模运算下注意取模；度数序列计数分母是阶乘，模质数下用逆元
- 堆元素重复：度数减到 1 后若再入堆会产生重复节点，需先判断是否已删

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/prufer/](https://oi-wiki.org/graph/prufer/)
- oiwiki_raw ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/prufer.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/prufer.md)
- CP-Algorithms ✓ [https://cp-algorithms.com/graph/pruefer_code.html](https://cp-algorithms.com/graph/pruefer_code.html)
