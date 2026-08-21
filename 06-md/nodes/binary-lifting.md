---
id: binary-lifting
name: 倍增
group: G-A-1
stage: intermediate
priority: P1
depth_tier: standard
---

# 倍增

> 预处理2^k次幂跳跃，用于ST表/LCA/稀疏表等

<!-- 元信息: id=binary-lifting · group=G-A-1 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

倍增（Binary Lifting）是一种「成倍增长」的预处理思想：预先计算状态在跳 1、2、4、8... 步之后的结果，利用任意整数可写成若干个 2 的幂之和这一性质，将 O(n) 的暴力递推压缩为 O(log n) 的单次查询。经典应用包括：树上倍增求 LCA、RMQ 的 ST 表、函数迭代 f^m(x)（m 可达 10^18）、快速幂等。

## Why · 为什么

### 直觉 · Intuition

倍增对应一个朴素直觉：你想让一个人一次跳 13 级台阶，与其一格格跳 13 次，不如先预处理出「跳 1、2、4、8 级」各到达哪里，然后 13 = 8+4+1，只跳三次。预处理量只有 log 级，查询也只要 log 级，这就是倍增的威力。

### 原理 · Principle

设 f[k][x] 表示从状态 x 出发做 2^k 次操作后的状态，预处理满足 f[k][x]=f[k-1][f[k-1][x]]（先跳 2^(k-1) 再跳 2^(k-1)）。查询时把目标步数 m 按二进制拆位，从低位到高位逐个应用对应 k 的转移表即可。用于 LCA 时再配合「从大往小试探跳到不同的祖先」的标准倍增思路。

### 历史 · History

倍增思想最早被用于快速幂（每步平方），后被推广到稀疏表（Sparse Table，用于 O(1) RMQ）与树上 LCA（Tarjan 提出的倍增式 LCA 成为树上问题最常用的工具之一）。李煜东《算法竞赛进阶指南》0x06 节系统阐述了倍增范式，OI Wiki 也专辟「倍增」基础专题。

## How · 实现

### 伪代码

```python
# 预处理
LOG = floor(log2(max_m)) + 1
f[0][x] = next_state(x)
for k in 1..LOG:
  for x in all_states:
    f[k][x] = f[k-1][f[k-1][x]]

# 查询跳 m 步（可附带累计值 sum）
cur = start; res = identity
for k in 0..LOG:
  if m >> k & 1:
    res = combine(res, sum[k][cur])
    cur = f[k][cur]

# LCA(u, v):
# 先把深度深的提到同深度，再一起往上跳，最后差一步时返回父亲
```

### Python 实现

```python
def build_lifting(n, nxt):
    """n 个节点，nxt[i]=i 走一步到的节点（函数图）。
    返回 f[k][i]：i 跳 2^k 步后的节点。
    """
    LOG = 1
    while (1 << LOG) <= n:
        LOG += 1
    f = [[nxt[i] for i in range(n)] for _ in range(LOG)]
    for k in range(1, LOG):
        fk, fk1 = f[k], f[k - 1]
        for i in range(n):
            fk[i] = fk1[fk1[i]]
    return f


def jump(f, x, m):
    """从 x 出发跳 m 步（函数图可反复走）。
    表不够深时按需向上扩展（m 可能大于 2^LOG）。
    """
    k = 0
    while m:
        if m & 1:
            while k >= len(f):
                last = f[-1]
                f.append([last[last[i]] for i in range(len(last))])
            x = f[k][x]
        m >>= 1
        k += 1
    return x


class TreeLCA:
    """树上倍增 LCA。parent 用邻接表 adj 建树，root 为根。"""

    def __init__(self, n, adj, root=0):
        LOG = 1
        while (1 << LOG) <= n:
            LOG += 1
        self.LOG = LOG
        self.up = [[0] * n for _ in range(LOG)]
        self.depth = [0] * n
        # BFS/DFS 求 parent 与 depth
        stack = [root]
        self.up[0][root] = root
        order = [root]
        seen = [False] * n
        seen[root] = True
        while order:
            u = order.pop()
            for v in adj[u]:
                if not seen[v]:
                    seen[v] = True
                    self.up[0][v] = u
                    self.depth[v] = self.depth[u] + 1
                    order.append(v)
        for k in range(1, LOG):
            for i in range(n):
                self.up[k][i] = self.up[k - 1][self.up[k - 1][i]]

    def lca(self, u, v):
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        diff = self.depth[u] - self.depth[v]
        u = jump(self.up, u, diff)
        if u == v:
            return u
        for k in range(self.LOG - 1, -1, -1):
            if self.up[k][u] != self.up[k][v]:
                u = self.up[k][u]
                v = self.up[k][v]
        return self.up[0][u]


if __name__ == "__main__":
    # 函数图测试: 0->1->2->3->4->4
    nxt = [1, 2, 3, 4, 4]
    f = build_lifting(5, nxt)
    assert jump(f, 0, 0) == 0
    assert jump(f, 0, 3) == 3
    assert jump(f, 0, 100) == 4
    assert jump(f, 2, 1) == 3

    # 树测试: 0-1, 0-2, 1-3, 1-4
    adj = [[] for _ in range(5)]
    for u, v in [(0, 1), (0, 2), (1, 3), (1, 4)]:
        adj[u].append(v)
        adj[v].append(u)
    t = TreeLCA(5, adj, 0)
    assert t.lca(3, 4) == 1
    assert t.lca(3, 2) == 0
    assert t.lca(1, 2) == 0
    assert t.lca(4, 4) == 4

    print("All tests passed.")
```

**PyPy 提示**: Python 中 LOG×n 的二维 list 是主要内存开销，n=1e6 时 20×1e6 个 Python int 约 560MB，建议用 array('i') 或分块存储。树上倍增查询每步 O(LOG)，PyPy 下 n=1e5 可轻松通过。跳 m 步用 while m 拆位比 for k 快。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 预处理 O(n log n)，单次查询/跳跃 O(log n) |
| 空间 | O(n log n) — 存储 2^k 级跳转表 |

### 局限

倍增要求转移是「可叠加」的（函数迭代、RMQ 的可合并性等），否则无法合并两段信息。步数上限决定 LOG，需注意 m 可达 10^18 时 LOG 取 60+。空间占用是主要瓶颈，n 极大时考虑重链剖分（O(n) 空间）替代。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3379 | 4 | 【模板】最近公共祖先：树上倍增 LCA 的标准模板题 | [https://www.luogu.com.cn/problem/P3379](https://www.luogu.com.cn/problem/P3379) |
| Luogu | P3865 | 4 | 【模板】ST表：倍增思想在 RMQ 区间最值上的应用 | [https://www.luogu.com.cn/problem/P3865](https://www.luogu.com.cn/problem/P3865) |
| AtCoder | abc146_f | 1100 | Sugoroku：倒推最短路+倍增式贪心跳，或直接模拟贪心 | [https://atcoder.jp/contests/abc146/tasks/abc146_f](https://atcoder.jp/contests/abc146/tasks/abc146_f) |
| Luogu | P3128 | 5 | USACO15DEC 最大流：倍增 LCA 配合树上差分求路径覆盖次数 | [https://www.luogu.com.cn/problem/P3128](https://www.luogu.com.cn/problem/P3128) |

## Pitfalls · 易错点

- LOG 开得不够导致跳转越界（m 可达 10^18 时应取 60+）
- f[k][x]=f[k-1][f[k-1][x]] 的合并顺序写反
- LCA 跳到同深度后忘记判断 u==v 就直接进入二进制试探
- 拆分 m 时位运算优先级错误：if m & (1<<k) 应写 if (m >> k) & 1
- Python 中 LOG×n 二维表内存爆炸，需用 array 或换重链剖分

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/basic/binary-lifting/](https://oi-wiki.org/basic/binary-lifting/)
- 书籍 ✓ `李煜东《算法竞赛进阶指南》0x06 倍增`
