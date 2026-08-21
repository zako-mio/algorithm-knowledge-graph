---
id: dsu-on-tree
name: 启发式合并(dsu on tree)
group: G-B-7
stage: intermediate
priority: P1
depth_tier: standard
---

# 启发式合并(dsu on tree)

> 轻儿子清空+重儿子保留的树上离线统计，子树查询 O(n log n)

<!-- 元信息: id=dsu-on-tree · group=G-B-7 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

树上启发式合并（dsu on tree，又称 Sack）是一种离线处理「对每个子树查询某种统计量」的算法。核心套路：对节点 u，先递归处理所有轻儿子但清空其贡献，再递归处理重儿子并保留贡献，最后把 u 与所有轻儿子子树的节点重新加入统计，得到 u 的答案。利用轻重儿子「每个节点到根的轻边不超过 log n」的性质，总复杂度 O(n log n)，优于朴素 O(n^2) 且比树上莫队 O(n√m) 更优。适用于计数子树内不同元素个数、众数、出现次数等可加、可撤销的统计。

## Why · 为什么

### 直觉 · Intuition

子树统计最暴力的做法是对每个节点重扫一遍子树，共 O(n^2)。观察：父节点的答案是「子节点答案 + 自己 + 一些补充」，「重儿子」占了最大头，如果把重儿子的统计结果保留下来（而不是像轻儿子那样清空），那么父节点只需要再补上轻儿子的贡献即可。由于走轻边子树大小至少减半，任意节点被「重扫」的次数只有 O(log n) 次。本质是「把最大的那堆结果留着复用」。

### 原理 · Principle

先一遍 DFS 求出 siz 与重儿子（同 HLD）。对 u：①对每个轻儿子 v 执行 dfs(v) 并在返回后清空 cnt 的贡献；②对重儿子 dfs 并保留贡献；③重新遍历 u 的所有轻儿子子树，把每个节点加入 cnt；④加上 u 自身的贡献，得到 ans[u]。正确性：u 子树 = 重儿子子树 ∪ 各轻儿子子树 ∪ {u}，轻重都已覆盖。复杂度证明：轻边每次使子树大小至少减半，节点 x 被重新加入统计的次数 = 其到根轻边数 + 1 <= log n + 1，故总 O(n log n)。可用 HLD 的 dfn 序改为非递归实现（倒序 dfn 遍历 + 重链清空），常数更小。

### 历史 · History

该技巧由 Codeforces 社区命名并推广（cf blog 44351，作者为 dsu on tree 算法相关题解），OI Wiki 以「树上数颜色」问题引入，并总结「某些出题人设置的正解是 dsu on tree 的题」（如 CF741D）与「可水部分分的乱搞题」两类用途。名称中的 dsu 与并查集本身无关，取「按子树大小启发式合并」之意。

## How · 实现

### 伪代码

```python
dfs_size(u,f): siz[u]=1; 求重儿子 son[u]
add(u,f,delta): cnt[color[u]]+=delta; 若变0则总数--等（按需维护）
  for v in G[u], v!=f: add(v,u,delta)
dsu(u,f,keep):
  for v in G[u], v!=f and v!=son[u]: dsu(v,u,False)  # 轻儿子，不保留
  if son[u]: dsu(son[u],u,True)                        # 重儿子，保留
  for v in G[u], v!=f and v!=son[u]: add(v,u,+1)       # 补轻儿子
  add(u,f,+1); ans[u]=当前统计值
  if not keep: add(u,f,-1)                             # 整体清空
```

### Python 实现

```python
import sys

sys.setrecursionlimit(1 << 20)


def main():
    n = 8
    edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (5, 8)]
    color = [0, 1, 2, 1, 2, 1, 1, 2, 2]
    G = [[] for _ in range(n + 1)]
    for a, b in edges:
        G[a].append(b)
        G[b].append(a)

    siz = [0] * (n + 1)
    son = [0] * (n + 1)
    dfn = [0] * (n + 1)
    ordv = [0] * (n + 1)
    timer = 0

    def dfs_size(u, f):
        nonlocal timer
        timer += 1
        dfn[u] = timer
        ordv[timer] = u
        siz[u] = 1
        best = 0
        for v in G[u]:
            if v == f:
                continue
            dfs_size(v, u)
            siz[u] += siz[v]
            if siz[v] > best:
                best = siz[v]
                son[u] = v

    dfs_size(1, 0)

    cnt = [0] * 4
    cur = 0

    def add_node(x, delta):
        nonlocal cur
        c = color[x]
        cnt[c] += delta
        if delta == 1 and cnt[c] == 1:
            cur += 1
        if delta == -1 and cnt[c] == 0:
            cur -= 1

    def add_subtree(u, f, delta):
        add_node(u, delta)
        for v in G[u]:
            if v != f:
                add_subtree(v, u, delta)

    ans = [0] * (n + 1)

    def dsu(u, f, keep):
        for v in G[u]:
            if v != f and v != son[u]:
                dsu(v, u, False)
        if son[u]:
            dsu(son[u], u, True)
        for v in G[u]:
            if v != f and v != son[u]:
                add_subtree(v, u, 1)
        add_node(u, 1)
        ans[u] = cur
        if not keep:
            add_subtree(u, f, -1)

    dsu(1, 0, True)

    print("distinct colors per subtree:")
    for u in range(1, n + 1):
        print(f"  node {u}: {ans[u]}")
    # 手算校验：子树5={5,8} color[5]=1,color[8]=2 -> 2；子树3={3,6,7} color1,1,2 -> 2
    assert ans[5] == 2, ans[5]
    assert ans[3] == 2, ans[3]
    assert ans[1] == 2, ans[1]
    print("OK")


if __name__ == "__main__":
    main()

```

**PyPy 提示**: 递归实现深度可达 O(n)，PyPy 需加大 recursionlimit；add_subtree 在每次补轻儿子时递归整棵子树，节点总访问量 O(n log n)，PyPy 对这类高频小函数友好。若遇链状毒瘤树，可用 dfn 序迭代版（按 dfn 倒序遍历 + 每条重链独立清空）避免爆栈并减小常数。维护 cnt 用数组而非 dict，颜色需先离散化。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n log n) — 预处理 O(n)，主过程每个节点被重扫 O(log n) 次 |
| 空间 | O(n) — 树 + cnt + 答案数组 |

### 局限

只能离线；统计量须支持「加入/删除/合并」的增量维护（计数、和、出现次数等），若查询信息不可撤销（如只增不减的贪心标记）则不适用；不支持带修改。与树上莫队 O(n√m)、可持久化/树套树 O(n log n) 相比：DSU on tree 空间小、实现短，但修改与在线场景需换别的做法。统计数组要能 O(1) 更新，复杂的合并（如线段树合并）则另属 seg-merge。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Codeforces | 600E | 2100 | Lomsat gelral：子树众数之和，dsu on tree 最经典模板题 | [https://codeforces.com/problemset/problem/600/E](https://codeforces.com/problemset/problem/600/E) |
| Codeforces | 741D | 2600 | Arpa's letter-marked tree：路径回文判定(至多1个奇数字母)+子树最长链，正解即 dsu on tree | [https://codeforces.com/problemset/problem/741D](https://codeforces.com/problemset/problem/741D) |
| Luogu | U41492 | 3 | 树上数颜色：OI Wiki 引入例题，模板题 | [https://www.luogu.com.cn/problem/U41492](https://www.luogu.com.cn/problem/U41492) |

## Pitfalls · 易错点

- 轻儿子 dfs 后必须清空 cnt 再处理重儿子，否则重儿子统计被污染
- 清空时若用 memset 整数组会 O(n) 一次、n 次即 O(n^2)——正确做法是 add(u,f,-1) 逐点回滚，或只清空本次用过的位置（栈记录）
- ans[u] 的计算时机必须在「补完所有轻儿子 + 加上自身」之后，且清空要在记录 ans 之后
- keep 语义写反：重儿子 keep=True 保留，轻儿子 keep=False 清空；全树根节点 keep=True
- 颜色范围大需先离散化，否则 cnt 数组爆炸
- 误以为与并查集有关而想用 find/union——此处 dsu 只是名字，与并查集无关

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/dsu-on-tree/](https://oi-wiki.org/graph/dsu-on-tree/)
- oiwiki_raw ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/dsu-on-tree.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/dsu-on-tree.md)
- 书籍 ✓ `CPH ch18 pp173-182 (tree queries: merging maps)`
