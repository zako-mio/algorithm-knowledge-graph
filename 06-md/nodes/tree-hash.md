---
id: tree-hash
name: 树哈希
group: G-B-7
stage: advanced
priority: P3
depth_tier: brief
---

# 树哈希

> 把子树哈希成多重集函数值，判定有根/无根树同构

<!-- 元信息: id=tree-hash · group=G-B-7 · stage=advanced · priority=P3 · depth_tier=brief -->

## What · 是什么

树哈希把一棵（有根）子树映射成一个哈希值，用于快速判断树（或子树）同构：设 h_x = f({ h_v | v ∈ sons(x) })，f 是多重集的哈希函数（与儿子顺序无关），则两棵有根树同构当且仅当对应根哈希值相等（忽略碰撞）。常用 f 形如 (c + Σ g(h_v)) mod 2^64，其中 g 用 xor-shift 之类的映射。无根树同构需用「以每个点为根求哈希再取多重集哈希」或「只对重心求哈希」来处理。

## Why · 为什么

### 直觉 · Intuition

判断树同构本质是比较「儿子的形状集合」，与儿子顺序无关——所以不能简单拼接儿子哈希，必须用对顺序不敏感的多重集哈希（加法和取 g 都满足交换律）。把无穷种树结构压缩成一个 64 位整数，就能用字典比较代替逐层递归比较。无根树则先找重心（一棵树最多两个重心），以重心为根比较哈希即可规避「根的选择」带来的偏差。

### 原理 · Principle

多重集哈希 f(S)=(c+Σ_{x∈S} g(x)) mod m 之所以难卡，是因为 g 采用 xor-shift 等「扰乱」函数而非朴素多项式（朴素异或哈希有已知碰撞，OI Wiki 明确指出不建议用多项式）。要防针对性构造，可在映射前后异或随机常数。换根 DP：第二遍把父节点的贡献减去即可 O(n) 得到所有点为根的哈希。无根树同构：①求出每个点为根的哈希放进多重集再哈希比较；②或只比较重心的哈希（重心最多 2 个，取较小者）。

### 历史 · History

OI Wiki 的 tree-hash 页介绍「一种好写且卡不掉的树哈希」（源自 peehs-moorhsum 的 UOJ 博客），并以 UOJ #763 树哈希、BJOI2015 树的同构（Luogu P5043）、HDU 6647 括号序列等为例题。树哈希在字符串哈希之后发展，主要用于树的同构判定与带换根的 DP 哈希比较。

## How · 实现

### 伪代码

```python
hash(u): h[u] = 1 + Σ g(h[v])   # g 为 xor-shift 随机映射
  return h[u]
isomorphic(a,b):  # 有根
  return hash_of(a) == hash_of(b)
无根树: 对两树各自求所有点为根的 h，比较多重集哈希（或只比较重心哈希）
```

### Python 实现

```python
import sys
import random

sys.setrecursionlimit(1 << 20)

MASK = (1 << 64) - 1


def g(x):
    x = ((x >> 16) ^ x) * 0x45d9f3b & MASK
    x = ((x >> 16) ^ x) * 0x45d9f3b & MASK
    x = ((x >> 16) ^ x) & MASK
    return x


def tree_hash(n, edges, root=1):
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    h = [0] * (n + 1)

    def dfs(u, f):
        s = 1
        for v in adj[u]:
            if v != f:
                dfs(v, u)
                s = (s + g(h[v])) & MASK
        h[u] = s

    dfs(root, 0)
    return h[root]


def all_root_hashes(n, edges):
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    h = [0] * (n + 1)

    def dfs(u, f):
        s = 1
        for v in adj[u]:
            if v != f:
                dfs(v, u)
                s = (s + g(h[v])) & MASK
        h[u] = s

    dfs(1, 0)

    # 换根：h_to[v] = 以 v 为根时整棵树的哈希
    h_to = [0] * (n + 1)
    h_to[1] = h[1]

    def reroot(u, f):
        for v in adj[u]:
            if v != f:
                h_to[v] = (1 + g((h_to[u] - g(h[v])) & MASK)) & MASK
                reroot(v, u)

    reroot(1, 0)
    return h_to


def main():
    # 两棵同构的树（第二棵是镜像）：应判定同构
    t1 = [(1, 2), (1, 3), (2, 4)]
    t2 = [(1, 2), (1, 3), (3, 4)]
    h1 = all_root_hashes(4, t1)
    h2 = all_root_hashes(4, t2)
    same = sorted(h1[1:]) == sorted(h2[1:])
    print("t1 all-root hashes =", h1[1:])
    print("t2 all-root hashes =", h2[1:])
    print("isomorphic (as unordered trees)?", same)
    assert same
    # 一棵不同的树：应不同构
    t3 = [(1, 2), (1, 3), (1, 4)]
    h3 = all_root_hashes(4, t3)
    assert sorted(h1[1:]) != sorted(h3[1:])
    print("OK")


if __name__ == "__main__":
    main()

```

**PyPy 提示**: 换根 DP 两次 DFS 深度 O(n)，PyPy 需加大 recursionlimit。64 位掩码算术在 PyPy 下比 CPython 快；随机常数需在运行期固定（如用 seed）保证同一次运行可复现。g 函数用位移异或乘法对 JIT 友好。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 单根 O(n)，全部点为根（换根）O(n)；无根比较 O(n log n)（排序） |
| 空间 | O(n) |

### 局限

哈希碰撞理论存在，重大比赛可双模/双函数降低风险；朴素异或哈希或多项式哈希有已知构造碰撞，勿用；无根树同构若只比较重心哈希，需保证重心唯一性或特殊处理双重心。碰撞时是误判（不同构判成同构），正确性非严格保证。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P5043 | 3 | 【BJOI2015】树的同构：无根树同构判定，全部点为根哈希后比较 | [https://www.luogu.com.cn/problem/P5043](https://www.luogu.com.cn/problem/P5043) |
| UOJ | 763 | 3 | 树哈希：模板题，以 1 为根 DFS 即可 | [https://uoj.ac/problem/763](https://uoj.ac/problem/763) |
| HDU | 6647 | 5 | Bracket Sequences on Tree：本质不同括号序列计数，换根哈希+多重集排列 | [https://acm.hdu.edu.cn/showproblem.php?pid=6647](https://acm.hdu.edu.cn/showproblem.php?pid=6647) |

## Pitfalls · 易错点

- f 必须对儿子顺序不敏感（用加/异或/取 g 和），直接拼接儿子哈希（拼接后比较）会被儿子顺序不同的同构树误判
- 朴素 xor 哈希与多项式哈希有已知碰撞，被卡风险高
- 无根树直接以固定根比较会漏同构（根的位置不同），需换根或重心
- 32 位可能碰撞更多，用 64 位掩码或双模数
- 换根减除时 (h_to[u] - g(h[v])) 需 & MASK 防负值

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/tree-hash/](https://oi-wiki.org/graph/tree-hash/)
- oiwiki_raw ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/tree-hash.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/tree-hash.md)
