---
id: euler-path
name: 欧拉路/欧拉回路
group: G-B-8
stage: intermediate
priority: P1
depth_tier: standard
---

# 欧拉路/欧拉回路

> 经过每条边恰好一次的路径/回路：度数判定 + Hierholzer 算法 O(V+E)，支持有向/无向与字典序最小输出

<!-- 元信息: id=euler-path · group=G-B-8 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

欧拉路径（Eulerian path）是经过图中每条边恰好一次的路径，欧拉回路（Eulerian circuit）是每条边恰好一次的回路。存在欧拉回路（且非零度顶点连通）当且仅当所有顶点度数为偶数（无向）或每个顶点入度等于出度（有向）。存在欧拉路径（半欧拉图）当且仅当连通且恰有两个奇度顶点（无向）或有向图恰有两个顶点满足出度−入度=±1 而其余平衡。Hierholzer 算法：从起点开始沿剩余边任意行走并删除走过的边，用栈记录，当走到死胡同（度数耗尽）时回溯，最终把得到的路径反转即为欧拉路径/回路。经典应用：单词接龙（每个单词是边）、邮递员问题、中文一笔画、de Bruijn 序列构造。输出字典序最小的欧拉路需将边排序（复杂度加 O(E log E)）。

## Why · 为什么

### 直觉 · Intuition

每经过一个顶点一次，就会消耗一条进边和一条出边，所以总次数必须是偶数（有向图的入度=出度）。反过来，只要度数条件满足且连通，从任意非零度顶点出发贪心走，由于'进入顶点 v 时它剩余度数为奇/偶'的特点，永远不会在 v≠起点 处被卡死，最终会回到起点形成回路；把所有回路拼起来就是一条欧拉回路。Hierholzer 用栈模拟这个过程：沿边走到走不动，说明已回到起点或形成局部回路，弹栈记录，然后从栈顶（剩余度数非零的顶点）继续，即可在 O(E) 内完成。

### 原理 · Principle

判定：无向连通图欧拉回路 ⇔ 所有顶点度数为偶；欧拉路径 ⇔ 恰两个奇度顶点（其余偶）。有向连通图欧拉回路 ⇔ 入度=出度；欧拉路径 ⇔ 一个顶点出−入=1、一个入−出=1、其余平衡。证明方向：必要性（回路使度数成对）；充分性（从任意点出发沿边行走必回起点得回路，删除回路后剩余图仍满足条件，递归拼合）。Hierholzer 实现：维护 pos[v] 记录每个顶点边表中已用到的位置，栈 stack 中当前路径；取栈顶 v，若 v 仍有未用边则取一条推入下一顶点；否则把 v 弹出加入答案。每边恰好处理一次，故 O(V+E)。边排序可得到字典序最小的答案。有向/无向唯一区别是存储与删除方向（无向需同时删反向边）。

### 历史 · History

欧拉于 1736 年解决七桥问题（Königsberg）时奠定图论与欧拉路径概念，'一笔画'规则（奇度顶点≤2）即源于此。Hierholzer 算法由 Carl Hierholzer 于 1873 年给出（其同事整理发表），是目前最常用实现；Fleury 算法（1883）是另一类（贪心避免拆桥）但较慢。算法竞赛中欧拉路径是高频 P1 知识点（OI Wiki、CP-Algorithms 均有专章）。

## How · 实现

### 伪代码

```python
# 判定
非零度顶点组成的子图需连通（弱连通）
无向: 奇度顶点数 0 -> 回路, 2 -> 路径, 否则无
有向: 入度==出度全成立 -> 回路; 恰一个出-入=1 且一个入-出=1 -> 路径

# Hierholzer（迭代）
stack = [起点]; path = []
while stack:
    v = stack[-1]
    if v 仍有未用出边:
        (u,w) = 取下一条边; 删除它
        stack.append(w)
    else:
        path.append(v); stack.pop()
path 反转即为欧拉路径
# 若 path 长度 != 边数+1，图不连通无解
```

### Python 实现

```python
# -*- coding: utf-8 -*-
# Hierholzer 算法求有向图欧拉路径/回路（返回顶点序列；无解返回 None）
# 支持重边；字典序最小：把每个顶点的出边排序后依次取
def hierholzer_directed(edges, n):
    """edges: list of (u, v)。返回欧拉路径顶点序列（回路首尾相同）或 None。"""
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    outdeg = [0] * n
    for u, v in edges:
        adj[u].append(v)
        outdeg[u] += 1
        indeg[v] += 1
    for v in range(n):
        adj[v].sort()
    # 度数判定
    start = 0
    cnt_out_gt = cnt_in_gt = 0
    for v in range(n):
        if indeg[v] != outdeg[v]:
            if outdeg[v] - indeg[v] == 1:
                cnt_out_gt += 1
                start = v
            elif indeg[v] - outdeg[v] == 1:
                cnt_in_gt += 1
            else:
                return None
    if cnt_out_gt != cnt_in_gt or cnt_out_gt > 1:
        return None
    if cnt_out_gt == 0:          # 回路：从任意有边的顶点出发
        for v in range(n):
            if outdeg[v] > 0:
                start = v
                break
        else:
            return []
    # Hierholzer
    pos = [0] * n
    path = []
    stack = [start]
    while stack:
        v = stack[-1]
        if pos[v] < len(adj[v]):
            stack.append(adj[v][pos[v]])
            pos[v] += 1
        else:
            path.append(v)
            stack.pop()
    path.reverse()
    if len(path) - 1 != len(edges):   # 图不连通/未用完边
        return None
    return path


if __name__ == '__main__':
    # 三角形回路
    e = [(0, 1), (1, 2), (2, 0)]
    p = hierholzer_directed(e, 3)
    assert p is not None and len(p) == 4 and p[0] == p[-1], p
    # 链式欧拉路径 0->1->2
    p0 = hierholzer_directed([(0, 1), (1, 2)], 3)
    assert p0 == [0, 1, 2] or p0 == [0, 1, 2, None], p0
    assert p0 is not None and len(p0) == 3
    # 度数不平衡无解（0->1, 2->1）
    assert hierholzer_directed([(0, 1), (2, 1)], 3) is None
    # 链式欧拉路径：0->1, 1->2, 2->0, 0->3, 3->4
    e2 = [(0, 1), (1, 2), (2, 0), (0, 3), (3, 4)]
    p2 = hierholzer_directed(e2, 5)
    # 用边集合验证
    def valid_path(p, edges, n):
        if p is None:
            return False
        if len(edges) == 0:
            return len(p) == 0
        if len(p) - 1 != len(edges):
            return False
        from collections import Counter
        es = Counter((a, b) for a, b in zip(p, p[1:]))
        return es == Counter(edges)
    assert valid_path(p2, e2, 5)
    # 随机图对拍：暴力确认
    import random
    random.seed(0)
    for _ in range(200):
        n = random.randint(1, 6)
        m = random.randint(0, 12)
        edges = []
        for _ in range(m):
            edges.append((random.randrange(n), random.randrange(n)))
        got = hierholzer_directed(edges, n)
        # 暴力判定欧拉路径存在性
        indeg = [0] * n
        outdeg = [0] * n
        for u, v in edges:
            outdeg[u] += 1
            indeg[v] += 1
        d = [outdeg[i] - indeg[i] for i in range(n)]
        ok_deg = (all(x == 0 for x in d) or
                  (sum(1 for x in d if x == 1) == 1 and sum(1 for x in d if x == -1) == 1
                   and all(x in (0, 1, -1) for x in d)))
        # 弱连通性检查（忽略孤立点与自环）
        adj_u = [[] for _ in range(n)]
        for u, v in edges:
            adj_u[u].append(v); adj_u[v].append(u)
        seen = set()
        def dfs(x):
            seen.add(x)
            for y in adj_u[x]:
                if y not in seen: dfs(y)
        roots = [i for i in range(n) if indeg[i] + outdeg[i] > 0]
        if roots:
            dfs(roots[0])
        conn = set(roots) <= seen
        exists = ok_deg and conn
        if not exists:
            assert got is None, (edges, got)
        else:
            assert got is not None and valid_path(got, edges, n), (edges, got)
    print('euler-path tests passed')

```

**PyPy 提示**: 迭代式栈版本避免递归，PyPy 下 O(V+E) 直接可用；边排序加 O(E log E)。有向图用邻接表 + pos 指针，每边只访问一次。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(V+E)；输出字典序最小需 O(E log E) 排序 |
| 空间 | O(V+E) |

### 局限

必须判连通（删除孤立点后），否则度数满足也可能无欧拉路。无向图删除反向边时注意边表共享（存边编号而非仅邻接点）。若用邻接矩阵暴力找下一出边复杂度退化 O(VE)。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P2731 | 3 | 骑马修栅栏：无向图欧拉路模板，字典序最小输出，注意重边与边排序 | [https://www.luogu.com.cn/problem/P2731](https://www.luogu.com.cn/problem/P2731) |
| CSES | 1691 | 3 | Mail Delivery：无向图欧拉回路判定 + Hierholzer 输出方案 | [https://cses.fi/problemset/task/1691](https://cses.fi/problemset/task/1691) |
| CSES | 1693 | 3 | Teleporters Path：有向图欧拉路径判定 + Hierholzer | [https://cses.fi/problemset/task/1693](https://cses.fi/problemset/task/1693) |
| Codeforces | 508-D | 4 | Tanya and Password：所有长度为 2 子串拼回原串，转化为边集欧拉路径 | [https://codeforces.com/contest/508/problem/D](https://codeforces.com/contest/508/problem/D) |

## Pitfalls · 易错点

- 不判连通：度数满足但非连通图无欧拉路（孤立点要排除）
- 无向图删除边时必须同时删除反向边，否则可能重复走
- 欧拉回路起点可选任意非零度顶点；路径起点必须选出-入=1 的顶点
- 迭代式 Hierholzer 输出顺序是栈弹出序，需整体反转
- 重边：边排序/计数不能用 set 去重
- 有向图判连通时用弱连通（忽略方向）即可

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/euler/](https://oi-wiki.org/graph/euler/)
- CP-Algorithms ✓ [https://cp-algorithms.com/graph/euler_path.html](https://cp-algorithms.com/graph/euler_path.html)
- 书籍 ✓ `CPH ch19 pp183-190`
