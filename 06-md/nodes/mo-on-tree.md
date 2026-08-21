---
id: mo-on-tree
name: 树上莫队
group: G-D-7
stage: advanced
priority: P2
depth_tier: standard
---

# 树上莫队

> 用欧拉括号序把树上路径压成序列，路径询问转化为序列区间询问后用莫队处理；LCA 不在区间时需临时加入。

<!-- 元信息: id=mo-on-tree · group=G-D-7 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

树上莫队（Mo's algorithm on trees）把树上的路径询问（如路径上不同颜色数、路径上某个值的出现次数）转化为序列区间询问，再用普通莫队求解。做法：DFS 生成括号序（进入节点 x 时记 st[x]、离开时记 ed[x]，序列长 2n），对任意路径 u→v（设 st[u]≤st[v]）：若 LCA(u,v)=u 则路径节点恰好在区间 [st[u], st[v]] 中出现一次；否则路径上除 LCA 外的节点在区间 [ed[u], st[v]] 中出现一次，LCA 需在回答时临时加入。莫队指针移动时对每个节点翻转出现状态（异或 1），状态为 1 的节点构成当前路径集合。

## Why · 为什么

### 直觉 · Intuition

括号序的关键性质：树上任意一条路径，其节点在括号序的某个连续区间中「恰好出现 1 次」，而不在路径上的节点出现 0 次或 2 次。这是因为括号序中一个节点的子树会整体出现在其两个括号之间；路径经过的节点相当于「未被完整括号包住」的节点。于是路径问题变成区间问题，莫队的双指针从「移动数组下标」变为「翻转节点状态」。LCA 是唯一的例外：当 LCA 不在区间端点时它出现 0 次，需要临时加入（翻转）再移出。

### 原理 · Principle

① 建括号序：DFS 记录 st/ed 与 euler 数组（长度 2n）；② LCA：倍增预处理 parent/up/dep，用于判断 LCA 归属与临时加入；③ 询问转化：对 (u,v) 若 st[u]≤st[v]，LCA=w；w==u 时区间取 [st[u],st[v]]，否则取 [ed[u],st[v]] 且标记 w 需临时加入；④ 莫队：按区间排序 + 奇偶化，指针移动对节点 toggle（出现次数 xor 1），维护 cnt[col] 与当前不同色数；⑤ 回答：若该询问有临时 LCA，先 toggle(w) 再记录再 toggle(w)。若还要支持修改，加时间维即「带修改树上莫队」（如 WC2013 糖果公园）。

### 历史 · History

树上莫队源自国内 OI 对莫队的扩展，把「括号序 + LCA」与莫队结合，代表题为 WC2013「糖果公园」（UOJ 58，支持带修树上路径询问），是 NOI 级难度的经典题。OI Wiki 完整收录括号序树上莫队及带修扩展。

## How · 实现

### 伪代码

```python
dfs(1): st[x]=len(euler); euler.append(x); for child: dfs; ed[x]=len(euler); euler.append(x)
preprocess LCA (倍增)
for (u,v,id) in queries:
    if st[u] > st[v]: swap
    w = lca(u,v)
    if w == u: conv = (st[u], st[v], -1)
    else:      conv = (ed[u], st[v], w)
sort by (l//block, r 奇偶化)
while moving pointers: toggle(euler[pos])
toggle(x): vis[x] ^= 1; if vis[x]: add col[x] else remove col[x]
answer: if w!=-1: toggle(w); ans[id]=cur; toggle(w)
```

### Python 实现

```python
def mo_on_tree(n, adj, col, queries):
    """树上莫队（括号序）：路径 u-v 上不同颜色的数量.
    adj: 邻接表 0-indexed; col: 各节点颜色; queries: [(u,v,id)].
    返回按 id 的答案列表."""
    import math, sys
    sys.setrecursionlimit(1 << 20)
    st = [0] * n; ed = [0] * n
    euler = []
    dep = [0] * n
    parent = [-1] * n
    def dfs(u, p):
        parent[u] = p
        st[u] = len(euler); euler.append(u)
        for w in adj[u]:
            if w != p:
                dep[w] = dep[u] + 1
                dfs(w, u)
        ed[u] = len(euler); euler.append(u)
    dfs(0, -1)
    # LCA 用倍增
    LOG = (n + 1).bit_length()
    up = [[-1] * n for _ in range(LOG)]
    up[0] = parent[:]
    for k in range(1, LOG):
        for v in range(n):
            mid = up[k-1][v]
            up[k][v] = up[k-1][mid] if mid != -1 else -1
    def lca(u, v):
        if dep[u] < dep[v]:
            u, v = v, u
        diff = dep[u] - dep[v]
        for k in range(LOG):
            if diff >> k & 1:
                u = up[k][u]
        if u == v:
            return u
        for k in range(LOG - 1, -1, -1):
            if up[k][u] != up[k][v]:
                u = up[k][u]; v = up[k][v]
        return parent[u]
    m2 = len(euler)
    block = max(1, int(math.sqrt(m2)))
    def conv(u, v):
        if st[u] > st[v]:
            u, v = v, u
        w = lca(u, v)
        if w == u:
            return (st[u], st[v], -1)
        return (ed[u], st[v], w)
    converted = []
    for u, v, idx in queries:
        l, r, w = conv(u, v)
        converted.append((l, r, w, idx))
    converted.sort(key=lambda q: (q[0] // block, q[1] if (q[0] // block) % 2 == 0 else -q[1]))
    vis = [0] * n            # 当前在集合中的次数
    cnt = [0] * (max(col) + 1)
    cur = 0
    def toggle(x):
        nonlocal cur
        if vis[x]:
            vis[x] = 0
            cnt[col[x]] -= 1
            if cnt[col[x]] == 0:
                cur -= 1
        else:
            vis[x] = 1
            if cnt[col[x]] == 0:
                cur += 1
            cnt[col[x]] += 1
    ans = [0] * len(queries)
    l = 0; r = -1
    for ql, qr, w, idx in converted:
        while l > ql:
            l -= 1; toggle(euler[l])
        while r < qr:
            r += 1; toggle(euler[r])
        while l < ql:
            toggle(euler[l]); l += 1
        while r > qr:
            toggle(euler[r]); r -= 1
        if w != -1:
            toggle(w)
        ans[idx] = cur
        if w != -1:
            toggle(w)
    return ans

if __name__ == "__main__":
    # 树: 0-1, 0-2, 1-3; 颜色 [1,2,2,3]
    n = 4
    adj = [[1, 2], [0, 3], [0], [1]]
    col = [1, 2, 2, 3]
    queries = [(0, 3, 0), (2, 3, 1), (1, 1, 2)]
    res = mo_on_tree(n, adj, col, queries)
    # 路径 0-3: 0,1,3 -> 颜色 {1,2,3}=3; 2-3: 2,0,1,3 -> {1,2,3}=3; 1-1: {2}=1
    assert res == [3, 3, 1], res
    # 随机交叉验证（小树暴力 BFS 路径）
    import random
    def brute(n, adj, col, u, v):
        # BFS 找路径
        from collections import deque
        par = [-1] * n
        par[u] = u
        q = deque([u])
        while q:
            x = q.popleft()
            if x == v:
                break
            for w in adj[x]:
                if par[w] == -1:
                    par[w] = x
                    q.append(w)
        path = []
        x = v
        while True:
            path.append(x)
            if x == u:
                break
            x = par[x]
        return len(set(col[i] for i in path))
    random.seed(17)
    for _ in range(100):
        n = random.randint(1, 8)
        adj = [[] for _ in range(n)]
        for i in range(1, n):
            p = random.randrange(i)
            adj[i].append(p); adj[p].append(i)
        col = [random.randint(1, 4) for _ in range(n)]
        for _q in range(20):
            u = random.randrange(n); v = random.randrange(n)
            got = mo_on_tree(n, adj, col, [(u, v, 0)])[0]
            exp = brute(n, adj, col, u, v)
            assert got == exp, (n, adj, col, u, v, got, exp)
    print("mo_on_tree OK")

```

**PyPy 提示**: 括号序长度 2n，块长按 2n 计算；LCA 倍增表用 list 数组加速；递归 DFS 深树注意 sys.setrecursionlimit，也可改迭代 DFS。Python 版适用于 n≤2e4 左右，更大建议 C++ 或 PyPy 微调。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n√n)（括号序莫队）；带修树上莫队 O(n^(5/3)) |
| 空间 | O(n log n)（倍增表）+ O(n) |

### 局限

需要实现 LCA（倍增/树剖），稍复杂；括号序区间长度可达 2n，块长与常数都翻倍；仅离线；路径统计必须支持 O(1) 的单点翻转更新（toggle）；若统计对翻转不可维护（如求路径上第 k 小）则不适用。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| UOJ | 58 | 6 | WC2013 糖果公园：带修改树上莫队，树上路径贡献 sum(val_c * w_cnt)，OI Wiki 树上莫队例题 | [https://uoj.ac/problem/58](https://uoj.ac/problem/58) |
| Luogu | SP10707 | 4 | COT2 - Count on a tree II：树上路径不同颜色数，括号序莫队模板 | [https://www.luogu.com.cn/problem/SP10707](https://www.luogu.com.cn/problem/SP10707) |
| Luogu | P4074 | 6 | [WC2013] 糖果公园 洛谷版，带修树上莫队 | [https://www.luogu.com.cn/problem/P4074](https://www.luogu.com.cn/problem/P4074) |

## Pitfalls · 易错点

- LCA 不在区间内的询问，必须临时 toggle(LCA) 记录答案后再 toggle 回来，否则答案少/多一个节点
- 括号序区间是 ed[u]..st[v]（LCA≠u 时），不要误用 st[u]..st[v]（会把 u 的子树整个算进去）
- toggle 状态维护的是出现次数奇偶，不是「是否加入」布尔——同一节点被指针扫过两次会抵消
- 块长按 2n（括号序长度）计算，不是按 n
- 深树递归 DFS 会爆栈，需 sys.setrecursionlimit 或迭代实现

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/mo-algo-on-tree.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/mo-algo-on-tree.md)
- OI Wiki ✓ [https://oi-wiki.org/misc/mo-algo-on-tree/](https://oi-wiki.org/misc/mo-algo-on-tree/)
- uoj ✓ [https://uoj.ac/problem/58](https://uoj.ac/problem/58)
