---
id: dmst
name: 最小树形图(DMST)
group: G-B-3
stage: advanced
priority: P2
depth_tier: standard
---

# 最小树形图(DMST)

> 有向图最小生成树，朱刘算法(Edmonds) O(VE)，缩环+入边修正

<!-- 元信息: id=dmst · group=G-B-3 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

最小树形图(Directed MST)问题：给有向图 G 和根 r，求一棵以 r 为根、能到达所有点的最小权『根向树形图』(每条非根点恰有一条入边，且从 r 出发可达)。经典算法是朱刘算法(Edmonds 算法)：每轮为每个非根点选最小入边，若不成环则已得最优；否则把选边形成的环缩成超级点，并把进入环的边权减去其终点原入边权(做修正)，再递归，直到无环。朴素实现 O(VE)，每轮收缩至少减少一个点。

## Why · 为什么

### 直觉 · Intuition

对每个点来说，最优解里它一定选了入边中最小的一条(入度约束独立)。但如果这样选边后出现了环，说明环内没有根，环上每点各选了一条入边——此时必须『破环』：放弃环上一条边。破环的代价就是进入环的替代边与环内被顶掉边的差值。朱刘算法把这个代价直接算在边权上(减 in[v])，使环缩成超级点后问题规模缩小，反复执行。

### 原理 · Principle

每轮：① 选每个非根点的最小入边 in[v]；② 若无环则 ∑in 即答案(根可达性检查)；③ 否则对每个环，把环内点缩成超级点；对每条跨环边 (u,v)，权修正为 w(u,v)−in[v](即『替换进入环的最小入边所需代价』)；④ 重复直到无环。正确性由『环内必弃一条边，弃边可等效为权修正』的交换论证保证。实现需注意根的处理与最终按缩点结构展开。

### 历史 · History

由朱永津和刘振宏于 1965 年(中国)独立提出，同年 J. Edmonds 也在西方发表同一算法，故称朱刘算法(Chu–Liu/Edmonds 算法)。1977 年 Tarjan 给出 O(m+n log n) 的堆优化版本(结合左偏树/并查集)。

## How · 实现

### 伪代码

```python
function chu_liu(n, edges, root):
  ans = 0
  while True:
    in_w[v]=INF, pre[v]=-1 for all v
    for (u,v,w) in edges: if u!=v and w<in_w[v]: in_w[v]=w, pre[v]=u
    in_w[root]=0
    if any i!=root and in_w[i]==INF: return None   # 根不可达
    find cycles via pre[] links (vis/id arrays)
    ans += sum(in_w)
    if no cycle: break
    assign new ids to super-nodes (环内同号)
    for (u,v,w) in edges:
      if u!=v:
        nu,nv = id[u],id[v]
        if nu!=nv: new_edges.add((nu,nv, w - in_w[v]))
    edges=new_edges; n=cnt; root=id[root]
  return ans
```

### Python 实现

```python
INF = 10**18


def chu_liu_edmonds(n, edges, root):
    """朱刘算法求最小树形图 (有向图, 从 root 出发可达所有点的最小生成树)。
    edges: list of (u, v, w)。返回最小总权或 None(不可达)"""
    ans = 0
    e = [(u, v, w) for u, v, w in edges]
    while True:
        in_w = [INF] * n
        pre = [-1] * n
        for u, v, w in e:
            if u != v and w < in_w[v]:
                in_w[v] = w
                pre[v] = u
        in_w[root] = 0
        for i in range(n):
            if i != root and in_w[i] == INF:
                return None
        cnt = 0
        id_arr = [-1] * n
        vis = [-1] * n
        for i in range(n):
            ans += in_w[i]
            v = i
            while vis[v] != i and id_arr[v] == -1 and v != root:
                vis[v] = i
                v = pre[v]
            if v != root and id_arr[v] == -1:
                u = pre[v]
                while u != v:
                    id_arr[u] = cnt
                    u = pre[u]
                id_arr[v] = cnt
                cnt += 1
        if cnt == 0:
            break
        for i in range(n):
            if id_arr[i] == -1:
                id_arr[i] = cnt
                cnt += 1
        new_edges = []
        for u, v, w in e:
            if u != v:
                nu, nv = id_arr[u], id_arr[v]
                if nu != nv:
                    new_edges.append((nu, nv, w - in_w[v]))
        e = new_edges
        n = cnt
        root = id_arr[root]
    return ans


if __name__ == "__main__":
    e = [(0, 1, 5), (1, 2, 3), (2, 0, 4)]  # 有向三角, root=0: 5+3=8
    assert chu_liu_edmonds(3, e, 0) == 8
    e2 = [(0, 1, 1), (0, 2, 2), (1, 2, 10)]  # 星形: 1+2=3
    assert chu_liu_edmonds(3, e2, 0) == 3
    e3 = [(0, 1, 1)]  # 2 不可达
    assert chu_liu_edmonds(3, e3, 0) is None
    e5 = [(0, 1, 5), (0, 2, 6), (1, 2, 1), (2, 1, 1)]  # 需缩环: 最小=6
    assert chu_liu_edmonds(3, e5, 0) == 6, chu_liu_edmonds(3, e5, 0)
    print("dmst OK")

```

**PyPy 提示**: 朴素朱刘 O(VE) 每轮重建边表，适合 n≤300, m≤n^2 的小数据；大规模(n≤1e5)须用 Tarjan 的堆优化版(左偏树+并查集)，实现复杂，竞赛一般只用到朴素版。注意 Python 中 INF 用 1e18 足够。缩环后 n 缩小，root 需映射为 id[root]，否则越界。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(VE)，每轮找最小入边 O(E)、缩环至多 n 轮 |
| 空间 | O(V+E) |

### 局限

1) 必须指定根，且根需能到达所有点，否则无解；2) 朴素版 O(VE) 只适合小数据(n≤500)，大数据需 Tarjan O(m+n log n) 堆优化(难写)；3) 边权修正 w−in[v] 依赖 in[v] 是本轮选中的入边权，实现中注意只对跨环边修正；4) 有重边时取最小入边自然处理。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P4716 | 4 | 【模板】最小树形图：朱刘算法标准模板题 | [https://www.luogu.com.cn/problem/P4716](https://www.luogu.com.cn/problem/P4716) |
| HDU | 2121 | 4 | Ice_cream's world II：虚根技巧求不定根最小树形图(超级源连 INF 边) | [http://acm.hdu.edu.cn/showproblem.php?pid=2121](http://acm.hdu.edu.cn/showproblem.php?pid=2121) |
| SPOJ | ADAMOLD | 4 | 最小树形图综合应用：构图后直接朱刘 | [https://www.spoj.com/problems/ADAMOLD/](https://www.spoj.com/problems/ADAMOLD/) |

## Pitfalls · 易错点

- 根不可达时误输出 0 而非无解，必须检查 in_w[i]==INF
- 缩环后忘记更新 root=id[root]，导致新图根越界
- 边权修正 w−in[v] 只对跨环边做，环内边已无效却未过滤导致重复计权
- 自环 (u==u) 在选最小入边时应跳过，否则破坏 in[v] 语义
- 用并查集/哈希标记超级点时与缩环 id 分配混淆

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/dmst/](https://oi-wiki.org/graph/dmst/)
- CP-Algorithms △ [https://cp-algorithms.com/graph/dmst.html](https://cp-algorithms.com/graph/dmst.html)
