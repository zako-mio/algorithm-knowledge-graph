---
id: hld
name: 树链剖分(HLD)
group: G-B-7
stage: intermediate
priority: P1
depth_tier: deep
---

# 树链剖分(HLD)

> 重链剖分把树剖为若干重链，配合线段树 O(log^2 n) 维护路径/子树信息，亦可 O(log n) 求 LCA

<!-- 元信息: id=hld · group=G-B-7 · stage=intermediate · priority=P1 · depth_tier=deep -->

## What · 是什么

重链剖分（Heavy-Light Decomposition）是一种把树线性化的技术：为每个节点选出子树最大的儿子作为「重儿子」（重子结点），到重儿子的边为「重边」，其余为「轻边」；若干首尾相接的重边组成一条「重链」。两遍 DFS 后每个节点获得 dfn（DFS 序，重边优先）与 top（所在链顶端），使得：同一重链上 dfn 连续（可用线段树维护区间）、任意节点到根至多经过 O(log n) 条轻边（即 O(log n) 条重链）。于是「树上两点路径」可拆成 O(log n) 个连续 dfn 区间，「子树」恰为一个连续区间，都能交给线段树处理。

## Why · 为什么

### 直觉 · Intuition

树上的路径是「弯的」，线段树只能处理「直的」区间。重链剖分的聪明之处：专门挑出那些最大的分支（重儿子）连成粗链，保证从任意叶子爬到根只需要切换 O(log n) 次链——每次都跳过一整条连续段。这样把一条曲折路径切成几段直线，每段在 dfs 序上连续，就能用线段树批量改查。轻边的「每走一条子树至少减半」性质正是 O(log n) 的来源。

### 原理 · Principle

第一次 DFS 记录 fa/dep/siz/重儿子 son（siz 最大的儿子）；第二次 DFS 沿重儿子优先分配 dfn 并记录 top（重儿子继承父亲 top，轻儿子开新链）。性质：①任意路径到根的轻边数 <= log n（走轻边子树至少减半）；②一条重链在 dfn 上连续。路径查询 (u,v)：若 top[u]!=top[v]，取较深的链顶跳到其父节点并处理 [dfn[top], dfn[u]] 区间，重复至同链后处理 [dfn[u], dfn[v]] 的直区间。共 O(log n) 段 × 线段树 O(log n) = O(log^2 n)。子树修改/查询即直接操作 [dfn[u], dfn[u]+siz[u]-1] 单区间 O(log n)。重链剖分的 LCA 也自然可得：反复跳深链顶直到两节点同链，取较浅者。

### 历史 · History

HLD 由 Sleator 与 Tarjan 引入（与 Splay/LCT 同源思想），是静态树上路径问题最常用的处理框架。OI Wiki 将其列为图论-树上算法核心条目，CP-Algorithms 给出路径最大值/和/染色三种典型应用，均以「最多 O(log n) 条重链」为核心证明。其地位类似树状数组之于序列：不是最强的（LCT 更强），但实现简单、常数小、无需修改形态，是竞赛最常用工具之一。

## How · 实现

### 伪代码

```python
dfs1(u,f): fa[u]=f; dep[u]=dep[f]+1; siz[u]=1
  for v in G[u], v!=f: dfs1(v,u); siz[u]+=siz[v]; if siz[v]>siz[son[u]]: son[u]=v
dfs2(u,ftop): top[u]=ftop; dfn[u]=++idx; rnk[idx]=u
  if son[u]: dfs2(son[u],ftop)
  for v in G[u], v!=fa[u] and v!=son[u]: dfs2(v,v)
path_update(u,v,val): 线段树区间加
  while top[u]!=top[v]:
    if dep[top[u]]<dep[top[v]]: swap(u,v)
    seg_update(dfn[top[u]], dfn[u], val); u=fa[top[u]]
  if dep[u]>dep[v]: swap(u,v)
  seg_update(dfn[u], dfn[v], val)
```

### Python 实现

```python
import sys

sys.setrecursionlimit(1 << 22)


def dfs1(u, f, G, fa, dep, siz, son):
    fa[u] = f
    dep[u] = dep[f] + 1
    siz[u] = 1
    for v in G[u]:
        if v == f:
            continue
        dfs1(v, u, G, fa, dep, siz, son)
        siz[u] += siz[v]
        if son[u] == 0 or siz[v] > siz[son[u]]:
            son[u] = v


idx = 0


def dfs2(u, ftop, G, fa, son, top, dfn, rnk):
    global idx
    idx += 1
    top[u] = ftop
    dfn[u] = idx
    rnk[idx] = u
    if son[u]:
        dfs2(son[u], ftop, G, fa, son, top, dfn, rnk)
    for v in G[u]:
        if v != fa[u] and v != son[u]:
            dfs2(v, v, G, fa, son, top, dfn, rnk)


def build(o, l, r, a, dfn, rnk, sumv, addv):
    if l == r:
        sumv[o] = a[rnk[l]]
        return
    m = (l + r) >> 1
    build(o * 2, l, m, a, dfn, rnk, sumv, addv)
    build(o * 2 + 1, m + 1, r, a, dfn, rnk, sumv, addv)
    sumv[o] = sumv[o * 2] + sumv[o * 2 + 1]


def pushdown(o, l, r, sumv, addv):
    if addv[o]:
        m = (l + r) >> 1
        lc, rc = o * 2, o * 2 + 1
        addv[lc] += addv[o]
        addv[rc] += addv[o]
        sumv[lc] += addv[o] * (m - l + 1)
        sumv[rc] += addv[o] * (r - m)
        addv[o] = 0


def update(o, l, r, ql, qr, val, sumv, addv):
    if ql <= l and r <= qr:
        addv[o] += val
        sumv[o] += val * (r - l + 1)
        return
    pushdown(o, l, r, sumv, addv)
    m = (l + r) >> 1
    if ql <= m:
        update(o * 2, l, m, ql, qr, val, sumv, addv)
    if qr > m:
        update(o * 2 + 1, m + 1, r, ql, qr, val, sumv, addv)
    sumv[o] = sumv[o * 2] + sumv[o * 2 + 1]


def query(o, l, r, ql, qr, sumv, addv):
    if ql <= l and r <= qr:
        return sumv[o]
    pushdown(o, l, r, sumv, addv)
    m = (l + r) >> 1
    res = 0
    if ql <= m:
        res += query(o * 2, l, m, ql, qr, sumv, addv)
    if qr > m:
        res += query(o * 2 + 1, m + 1, r, ql, qr, sumv, addv)
    return res


def path_add(u, v, val, n, G, fa, dep, siz, son, top, dfn, sumv, addv):
    while top[u] != top[v]:
        if dep[top[u]] < dep[top[v]]:
            u, v = v, u
        update(1, 1, n, dfn[top[u]], dfn[u], val, sumv, addv)
        u = fa[top[u]]
    if dep[u] > dep[v]:
        u, v = v, u
    update(1, 1, n, dfn[u], dfn[v], val, sumv, addv)


def path_sum(u, v, n, fa, dep, top, dfn, sumv, addv):
    res = 0
    while top[u] != top[v]:
        if dep[top[u]] < dep[top[v]]:
            u, v = v, u
        res += query(1, 1, n, dfn[top[u]], dfn[u], sumv, addv)
        u = fa[top[u]]
    if dep[u] > dep[v]:
        u, v = v, u
    res += query(1, 1, n, dfn[u], dfn[v], sumv, addv)
    return res


def main():
    n = 6
    edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6)]
    G = [[] for _ in range(n + 1)]
    for a, b in edges:
        G[a].append(b)
        G[b].append(a)
    fa = [0] * (n + 1)
    dep = [0] * (n + 1)
    siz = [0] * (n + 1)
    son = [0] * (n + 1)
    top = [0] * (n + 1)
    dfn = [0] * (n + 1)
    rnk = [0] * (n + 1)
    dfs1(1, 0, G, fa, dep, siz, son)
    dfs2(1, 1, G, fa, son, top, dfn, rnk)
    a = [0] + [10] * n
    sumv = [0] * (4 * n + 4)
    addv = [0] * (4 * n + 4)
    build(1, 1, n, a, dfn, rnk, sumv, addv)
    path_add(2, 6, 5, n, G, fa, dep, siz, son, top, dfn, sumv, addv)
    # 路径 2-1-3-6：节点 2,1,3,6 各 +5
    s = path_sum(2, 6, n, fa, dep, top, dfn, sumv, addv)
    print("path sum 2->6 =", s)
    assert s == 4 * (10 + 5), "wrong!"
    # 子树 2 (节点2,4,5) 之和
    sub = query(1, 1, n, dfn[2], dfn[2] + siz[2] - 1, sumv, addv)
    print("subtree sum of 2 =", sub)
    assert sub == 10 * 3 + 5, "wrong!"
    print("OK")


if __name__ == "__main__":
    main()

```

**PyPy 提示**: 递归 dfs1/dfs2 深度可达 n，PyPy 下务必 sys.setrecursionlimit(1<<22) 或用迭代；路径操作 while 循环的每一跳都调用递归线段树，PyPy JIT 对两层递归栈热循环友好，但纯 Python 的 O(log^2 n) 常数约为 C++ 的 10 倍以上，n=q=1e5 时限 2s 的题在 CPython 容易 TLE，建议 PyPy + 全部 sys.stdin.buffer 读入。线段树可用数组迭代版进一步减常数。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O((n+q) log n) 建树+预处理；单次路径修改/查询 O(log^2 n)（两跳 O(log n) × 线段树 O(log n)）；单次子树修改/查询 O(log n)；求 LCA O(log n) |
| 空间 | O(n) 树结构 + O(n) 线段树数组(4n) |

### 局限

仅支持静态树（无形态修改），有动态加边/换根需 LCT。路径上维护的信息需可在线段树区间上合并（和/最大/最小/gcd 等半群量）；若信息与方向有关（如边权路径最小值需先转点权）要仔细处理 dfn 区间端点。Python 常数大，是 O(log^2 n) 结构里最容易 TLE 的一类题。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3384 | 3 | 【模板】轻重链剖分：路径/子树 加+求和，四合一模板题 | [https://www.luogu.com.cn/problem/P3384](https://www.luogu.com.cn/problem/P3384) |
| Luogu | P3178 | 3 | 【模板】树链剖分：单点改/子树加/路径和，无懒标记简化版 | [https://www.luogu.com.cn/problem/P3178](https://www.luogu.com.cn/problem/P3178) |
| SPOJ | QTREE | 4 | Query on a tree：边权转点权 + 路径最大值，经典入门题 | [https://www.spoj.com/problems/QTREE/](https://www.spoj.com/problems/QTREE/) |

## Pitfalls · 易错点

- 两遍 DFS 忘把 siz 较大的儿子选为重儿子时重边定义错误，复杂度退化为 O(n^2) 路径
- path_add/path_sum 的 while 循环中比较的是 dep[top[u]] 而非 dep[u]，写错会导致死循环
- 处理同一条链的最后一段时注意区间端点 u<=v（按 dep 交换后再 update）
- 子树操作区间是 [dfn[u], dfn[u]+siz[u]-1]，漏了 -1 会多算/少算一个节点
- 线段树 pushdown 时乘的区间长度写错（左右子区间长度分别为 m-l+1 与 r-m）
- 递归层数深：Python 默认 recursionlimit=1000 在链树上必爆栈

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/hld/](https://oi-wiki.org/graph/hld/)
- oiwiki_raw ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/hld.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/hld.md)
- CP-Algorithms ✓ [https://cp-algorithms.com/graph/hld.html](https://cp-algorithms.com/graph/hld.html)
- 书籍 ✓ `CPH ch18 pp173-182 (Tree algorithms: tree queries)`
