---
id: dp-dynamic
name: 动态DP（DDP）
group: G-A-13
stage: advanced
priority: P2
depth_tier: standard
---

# 动态DP（DDP）

> 带点权/边权修改的树上DP，用广义矩阵乘法（max,+）把转移写成矩阵，树链剖分+线段树/LCT维护单点修改后 O(log²n) 或 O(log n) 更新答案

<!-- 元信息: id=dp-dynamic · group=G-A-13 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

动态DP（Dynamic DP, DDP）解决'支持单点权值修改、每次修改后求树上 DP 答案'的问题，经典模板是树的最大权独立集（MIS）带点权修改（洛谷 P4719）。核心思想：把 DP 转移方程写成 2×2 广义矩阵乘法形式 C[i][j]=max_k(A[i][k]+B[k][j])（max,+ 半环上矩阵乘法，满足结合律），然后用树链剖分把每一条重链的转移矩阵放进线段树，重链内路径上的矩阵乘积用线段树区间乘维护；单点修改只影响该点到根路径上 O(log n) 条重链的链头矩阵，每次用线段树单点修改 + 链头向上跳，总 O(log²n)。LCT 版本可做到 O(log n)。著名的树上带修问题：保卫王国（NOIP2018 加强版矩阵做法）、SDOI2017 切树游戏。关键：广义矩阵乘法满足结合律即可用线段树/矩阵快速幂维护区间积。

## Why · 为什么

### 直觉 · Intuition

直接暴力：每次修改后重跑 O(n) DP 太慢。观察树上 DP：一个点权改变，影响沿父链传播，但重链上的转移是'线性的'（max,+ 矩阵），可以把链上的传播打包成矩阵乘积，一次算完。树链剖分保证任意点到根的路径被切成 O(log n) 段重链，每段用线段树快速求乘积，于是单点修改的传播被压缩成 O(log n) 次矩阵区间乘。

### 原理 · Principle

以最大权独立集为例。设 f_{i,0}=不选 i 的最大答案，f_{i,1}=选 i 的最大答案，DP 方程 f_{i,0}=Σ max(f_son,0,f_son,1)，f_{i,1}=w_i+Σ f_son,0。重剖后对每个点定义 g_{i,0}、g_{i,1}：分别表示只考虑轻儿子子树时 f_{i,0}、f_{i,1} 的'轻儿子贡献'（含自身权值），则 f_i = 矩阵×f_重儿子。具体：\[\begin{bmatrix}g_{i,0}&g_{i,0}\\g_{i,1}&-\infty\end{bmatrix}\times\begin{bmatrix}f_{son,0}\\f_{son,1}\end{bmatrix}=\begin{bmatrix}f_{i,0}\\f_{i,1}\end{bmatrix}\]，乘法用 max,+。整条重链从链头到链尾的矩阵乘积（线段树区间乘，注意顺序）给出链头状态关于链尾端 f 的线性关系，答案=max(f_{root,0},f_{root,1})。修改点 i 的权值：更新 g_{i,1} 与线段树中 i 的矩阵；沿链头向上跳，用链头旧/新矩阵的差量更新父节点的 g 矩阵，O(log n) 次线段树单点修改，每次 O(log n)，总 O(log²n)。

### 历史 · History

动态DP（DDP）技术由猫锟在 WC2018 的课件中系统介绍并在中国 OI 圈广泛传播。广义矩阵乘法思想更早用于最大子段和（线段树区间维护矩阵，如 SPOJ GSS3）与 NOIP2018 保卫王国。树剖+线段树 O(log²n) 与 LCT O(log n) 两种实现并存；DDP 也被推广到仙人掌、基环树及动态规划套动态规划等场景。

## How · 实现

### 伪代码

```python
# 预处理
1. DFS 求出 f[i][0/1], g[i][0/1]（g 只含轻儿子贡献）
2. 树链剖分，每条重链建线段树维护 2x2 矩阵（max,+ 乘）
   记录 End[i] = i 所在重链的链尾
3. 初始化：每点矩阵 [[g0,g0],[g1,-inf]]

# 修改点 x 权值为 w
1. 更新 g[x][1], 线段树单点更新 x 的矩阵
2. while x != 0:
    top = 链头[x]
    old = 线段树查询 [dfn[top], dfn[End[top]]] 乘积
    线段树单点更新 x 矩阵（链内传播）
    new = 线段树查询同区间乘积
    用 new-old 的差量更新 fa[top] 的 g 矩阵与线段树
    x = fa[top]

# 查询答案
ans = max(线段树查询 [dfn[root链头], dfn[End[root链头]]] 乘积的 f0, f1)
```

### Python 实现

```python
# -*- coding: utf-8 -*-
# 动态DP：树的最大权独立集 + 单点改权，树剖 + 线段树（max,+ 矩阵）
# 仅为教学/验证实现，n 较小。大 n 请用 C++ 或 PyPy + 优化。
import sys
sys.setrecursionlimit(10**6)

NEG = -10**15


def mat_mul(A, B):
    """广义矩阵乘: C[i][j] = max_k A[i][k]+B[k][j]"""
    return [[max(A[i][0] + B[0][j], A[i][1] + B[1][j]) for j in range(2)]
            for i in range(2)]


def build_ddp(n, w, edges):
    """edges: list of (u,v) 1-indexed。返回 (初始答案, 修改函数 update(i, neww))"""
    adj = [[] for _ in range(n + 1)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    par = [0] * (n + 1)
    order = []
    stack = [(1, 0)]
    while stack:
        u, p = stack.pop()
        order.append(u)
        par[u] = p
        for v in adj[u]:
            if v != p:
                stack.append((v, u))
    size = [1] * (n + 1)
    son = [0] * (n + 1)
    for u in reversed(order):
        mx = 0
        for v in adj[u]:
            if v != par[u]:
                size[u] += size[v]
                if size[v] > mx:
                    mx, son[u] = size[v], v
    # f[0]=不选, f[1]=选（不含点权累加时用于验证）
    f0 = [0] * (n + 1)
    f1 = [0] * (n + 1)
    for u in reversed(order):
        f1[u] = w[u]
        for v in adj[u]:
            if v != par[u]:
                f1[u] += f0[v]
                f0[u] += max(f0[v], f1[v])
    ans0 = max(f0[1], f1[1])

    # 重链剖分 dfn
    dfn = [0] * (n + 1)
    top = [0] * (n + 1)
    end = [0] * (n + 1)
    cnt = 0
    cur_w = [0] * (n + 1)      # dfn -> 节点
    # 迭代法避免递归深
    def decompose():
        nonlocal cnt
        st = [(1, 1)]
        while st:
            u, tp = st.pop()
            while u:
                top[u] = tp
                cnt += 1
                dfn[u] = cnt
                cur_w[cnt] = u
                for v in adj[u]:
                    if v != par[u] and v != son[u]:
                        st.append((v, v))
                u = son[u]
    decompose()
    # 每条重链链尾 = 该链 dfs 序最后
    for u in range(1, n + 1):
        # 找链尾：沿重儿子走到底
        t = u
        while son[t]:
            t = son[t]
        end[dfn[u]] = dfn[t] if top[t] == top[u] else dfn[u]
        # 简化：记录每条重链的尾节点编号
    chain_tail = {}
    for u in range(1, n + 1):
        t = u
        while son[t]:
            t = son[t]
        chain_tail[top[u]] = t

    # g 矩阵：只含轻儿子贡献
    gmat = [[[NEG, NEG], [NEG, NEG]] for _ in range(n + 1)]
    for u in range(1, n + 1):
        g0 = 0
        g1 = w[u]
        for v in adj[u]:
            if v != par[u] and v != son[u]:
                g0 += max(f0[v], f1[v])
                g1 += f0[v]
        gmat[u] = [[g0, g0], [g1, NEG]]

    # 线段树：按 dfn 存矩阵
    size_t = 1
    while size_t < n:
        size_t <<= 1
    tree = [[[NEG, NEG], [NEG, NEG]] for _ in range(2 * size_t)]
    for i in range(1, n + 1):
        tree[size_t + i - 1] = gmat[cur_w[i]]
    for i in range(size_t - 1, 0, -1):
        tree[i] = mat_mul(tree[i * 2], tree[i * 2 + 1])   # 左×右（链方向）

    def seg_update(pos, mat):
        p = size_t + pos - 1
        tree[p] = mat
        p >>= 1
        while p:
            tree[p] = mat_mul(tree[p * 2], tree[p * 2 + 1])
            p >>= 1

    def seg_query(l, r):
        # 保持链方向：左段 × 右段（链头方向为左）
        L = None
        R = None
        l += size_t - 1
        r += size_t - 1
        while l <= r:
            if l & 1:
                L = tree[l] if L is None else mat_mul(L, tree[l])
                l += 1
            if not (r & 1):
                R = tree[r] if R is None else mat_mul(tree[r], R)
                r -= 1
            l >>= 1
            r >>= 1
        if L is None:
            return R if R is not None else [[0, NEG], [NEG, 0]]
        if R is None:
            return L
        return mat_mul(L, R)

    def answer():
        t = chain_tail[top[1]]
        m = seg_query(dfn[1], dfn[t])
        return max(m[0][0], m[1][0])

    def update(x, neww):
        nonlocal w
        w[x] = neww
        u = x
        while u:
            tp = top[u]
            tail = chain_tail[tp]
            old = seg_query(dfn[tp], dfn[tail])
            # 重算 u 的 g1
            g0 = 0
            g1 = w[u]
            for v in adj[u]:
                if v != par[u] and v != son[u]:
                    g0 += max(f0[v], f1[v])
                    g1 += f0[v]
            gmat[u] = [[g0, g0], [g1, NEG]]
            seg_update(dfn[u], gmat[u])
            new = seg_query(dfn[tp], dfn[tail])
            # 更新链头对父节点的贡献（f0/f1 为链尾端状态，这里用链头状态推导）
            # 链头节点 tp 的父节点 ftp：其轻儿子 tp 贡献变化 = new-old（f0/f1 变化）
            ftp = par[tp]
            if ftp == 0:
                return
            d0 = (new[0][0] + (NEG if False else 0)) - (old[0][0])
            d1 = (new[1][0] + 0) - (old[1][0])
            f0_old_tp = old[0][0]
            f1_old_tp = old[1][0]
            f0_new_tp = new[0][0]
            f1_new_tp = new[1][0]
            # 更新 ftp 的轻儿子贡献与 f0/f1 参考值（用于后续 g 重算）
            for v in adj[ftp]:
                if v == tp:
                    # f0[v], f1[v] 缓存更新
                    pass
            f0[tp] = f0_new_tp
            f1[tp] = f1_new_tp
            u = ftp
        return

    return ans0, update, answer


if __name__ == '__main__':
    # 小树暴力验证
    n, w = 5, [0, 1, 2, 3, 4, 5]
    edges = [(1, 2), (1, 3), (2, 4), (2, 5)]
    ans0, update, answer = build_ddp(n, w, edges)

    def brute(w, edges):
        adj = [[] for _ in range(n + 1)]
        for u, v in edges:
            adj[u].append(v); adj[v].append(u)
        best = 0
        for mask in range(1 << n):
            ok = True
            for u, v in edges:
                if (mask >> (u - 1)) & 1 and (mask >> (v - 1)) & 1:
                    ok = False
                    break
            if ok:
                val = sum(w[i + 1] for i in range(n) if (mask >> i) & 1)
                best = max(best, val)
        return best

    assert ans0 == brute(w, edges), (ans0, brute(w, edges))
    # 随机修改验证
    import random
    random.seed(0)
    for _ in range(20):
        x = random.randint(1, n)
        nw = random.randint(0, 10)
        update(x, nw)
        assert answer() == brute(w, edges), (x, nw, answer(), brute(w, edges))
    print('dp-dynamic tests passed')

```

**PyPy 提示**: Python 实现 DDP 常数很大，树剖+线段树各操作叠加，n=1e5 会超时；教学演示可用，正式比赛请 C++。若坚持 Python，需把矩阵写成 4 个标量避免嵌套列表，并用迭代式 DFS 避免递归栈溢出。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 预处理 O(n log n)（剖分 + 建线段树）；单点修改 O(log²n)（LCT 版 O(log n)）；查询 O(log n) |
| 空间 | O(n) |

### 局限

依赖树剖分/LCT，实现复杂、易错（矩阵乘顺序、链尾记录、差量更新）。仅适用于'转移可写成矩阵'的 DP（线性结构），非线性 DP 无法 DDP。Python 常数过大。广义矩阵乘法只在 max,+ 等可结合结构上成立。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P4719 | 4 | 【模板】动态DP：树最大权独立集 + 单点改权，DDP 模板题 | [https://www.luogu.com.cn/problem/P4719](https://www.luogu.com.cn/problem/P4719) |
| LibreOJ | 2955 | 5 | NOIP2018 保卫王国：强制选/不选某些点的最小支配，矩阵转移 DDP | [https://loj.ac/p/2955](https://loj.ac/p/2955) |
| LibreOJ | 2269 | 6 | SDOI2017 切树游戏：带修改的树 DP（xor 卷积 + FWT），DDP 进阶题 | [https://loj.ac/p/2269](https://loj.ac/p/2269) |
| SPOJ | GSS3 | 3 | Can you answer these queries III：单点改 + 最大子段和，线段树维护 max,+,+ 矩阵（非树上但同思想） | [https://www.spoj.com/problems/GSS3/](https://www.spoj.com/problems/GSS3/) |

## Pitfalls · 易错点

- 矩阵乘法顺序：链上按深度方向是'祖先矩阵 × 子孙矩阵'，线段树合并必须保持顺序（区间左端为链头方向）
- g 矩阵只统计轻儿子贡献，重儿子贡献由矩阵乘法自动传播，两者混淆会错
- 修改时沿链头向上传播差量，若忘记更新父节点对链头轻儿子的贡献缓存会失步
- End[i]（链尾）记录错误导致区间乘积范围错；链尾要沿重儿子走到底
- 广义矩阵乘法中的 -∞ 元素必须足够小且不参与 max 污染
- 树剖的 dfn 按重儿子优先编号，线段树建树用 dfn 映射回节点
- 实现后必须与小规模暴力对拍（特别是修改多次后的答案）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/dp/dynamic/](https://oi-wiki.org/dp/dynamic/)
- 书籍 ✓ `猫锟 WC2018 课件；NOIP2018 保卫王国 矩阵做法`
