---
id: tree-decompose
name: 树分块
group: G-A-9
stage: advanced
priority: P3
depth_tier: brief
---

# 树分块

> 把树划分成 O(√n) 个块（关键点/块边界），块内暴力、块间预统计，配合树上莫队与 bitset 处理树上路径颜色统计、mex 等查询。

<!-- 元信息: id=tree-decompose · group=G-A-9 · stage=advanced · priority=P3 · depth_tier=brief -->

## What · 是什么

树分块（tree blocking/decomposition）是把序列分块思想搬到树上：将 n 个节点的树分成大小约 O(√n) 的块，定义块的关键点（块根），每个块内的点通过一次 DFS 属于某关键点；询问时在块内暴力跳、块之间利用预处理的信息（如到关键祖先路径上的颜色 bitset、块间的聚合值）快速回答。经典应用是树上莫队的预处理与『雪辉』（BZOJ4763）这类路径上颜色数/mex 统计。由于能被树分块解决的题目通常有更优做法（树剖、点分治等），相关题目较少，主要作方法论了解。

## Why · 为什么

### 直觉 · Intuition

序列分块能 O(√n) 平衡『暴力块内』与『预处理块间』，树分块同理：树上路径任意长，但把它拆成『两段从端点到关键点的暴力跳』+『关键点之间的一段跳』，前者 O(√n)、后者 O(√n)（块数），配合预处理的 bitset 让合并 O(1)。『菊花图可以卡掉朴素树分块』也说明其设计依赖树的结构（菊花图每点都是叶子，块间跳跃无收益）。

### 原理 · Principle

① 分块方式：参考树上莫队的块划分（如按 DFS 序分块，块大小约 √n，关键点为块内最浅点）。② 雪辉问题（BZOJ4763）：块内每个关键点预处理『它到祖先中每个关键点路径上的颜色 bitset』与『最近关键点祖先』，复杂度 O(n√n + nc/32)（c 为颜色数）。③ 回答查询：路径两端先暴力跳到所在块的关键点，再从关键点一块块向上跳直到 LCA 所在块，块内暴力；关键点间的 bitset 已预处理，剩余部分暴力过程中计算合并，单次 O(√n + c/32)。④ 数颜色用 bitset.count()，求 mex 用 _Find_first()。

### 历史 · History

树分块伴随树上莫队（Mo's algorithm on trees）发展，2009 年前后在 Codeforces/竞赛题中流行；OI Wiki 将树分块作为树上莫队前置方法论。『gty 的妹子树』一类题目的树分块做法可被菊花图卡，出题/做题时需注意。

## How · 实现

### 伪代码

```python
# 分块（以树上莫队风格为例）
欧拉序按块大小 B≈√n 划分，确定块与关键点
# 预处理
for 每个关键点 kp:
    预处理 kp 到各祖先关键点路径上的颜色 bitset
    预处理最近关键点祖先
# 查询路径 u..v:
    暴力跳 u,v 到所在块关键点，收集零散颜色
    关键点间用预处理的 bitset 合并
    块内/最后一段暴力，到 LCA
    ans = bitset.count() 或 _Find_first()
```

### Python 实现

```python
def block_tree_path_colors(n, parent, color, block_assign, keypoint_of, bitset_ancestor, u, v):
    """示意接口：树分块路径颜色查询的合并逻辑。
    教学示例仅演示分块思想，完整实现涉及块划分与 bitset 预处理。"""
    # 收集零散路径颜色（块内暴力跳）
    colors = set()
    while u != -1 and not keypoint_of[block_assign[u]]:
        colors.add(color[u])
        u = parent[u]
    while v != -1 and not keypoint_of[block_assign[v]]:
        colors.add(color[v])
        v = parent[v]
    # 关键点之间用预处理的 bitset 聚合（示意）
    if u != -1 and v != -1:
        for c in bitset_ancestor.get((u, v), set()):
            colors.add(c)
    return len(colors)

def tree_decompose_selfcheck():
    # 以链状树（0->1->...->8）演示分块正确性（简化模型）
    n = 9
    parent = [-1] + list(range(0, n - 1))   # parent[i]=i-1, parent[0]=-1
    color = [0, 1, 1, 2, 2, 2, 3, 3, 3]
    B = 3
    block_assign = [i // B for i in range(n)]
    def walk_colors(u, v):
        # 链上 u..v（u<=v）路径颜色集合：公共祖先即链上较浅点
        s = set()
        a, b = min(u, v), max(u, v)
        while b >= a:
            s.add(color[b]); b = parent[b]
        return s
    # 树分块核心：每个块预处理块内颜色集合
    block_colors = [set() for _ in range((n + B - 1) // B)]
    for i in range(n):
        block_colors[block_assign[i]].add(color[i])
    for u in range(n):
        for v in range(n):
            got = walk_colors(u, v)
            # 分块法：完整覆盖的块用预处理集合，两端零散部分块内暴力
            a, b = min(u, v), max(u, v)
            s2 = set()
            if a // B == b // B:            # 同一块：暴力
                for x in range(a, b + 1):
                    s2.add(color[x])
            else:
                for x in range(a, min((a // B + 1) * B, n)):        # 左零散
                    s2.add(color[x])
                for k in range(a // B + 1, b // B):                 # 整块（预统计）
                    s2 |= block_colors[k]
                for x in range((b // B) * B, b + 1):                # 右零散
                    s2.add(color[x])
            assert len(s2) == len(got), (u, v, s2, got)
    print('tree decompose block-color union consistent OK')

if __name__ == '__main__':
    tree_decompose_selfcheck()
```

**PyPy 提示**: bitset 用 Python int 位运算即可模拟（python int 天然大整数），count 用 bin(x).count('1')，mex 用位扫描；树上分块主体是路径跳跃，PyPy 性能可接受。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 单次查询 O(√n + c/32)（c 颜色数）；预处理 O(n√n + nc/32)；构造 O(n√n) |
| 空间 | O(n√n + nc/32)（关键点 bitset 存储） |

### 局限

可解决的题目范围窄（路径颜色统计/mex 类），且多数有更优解法；对菊花图等『块间跳跃无收益』的结构会退化；bitset 存储开销大；实现细节多，竞赛中低频出现。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| hydro | BZOJ4763 雪辉 | 7 | 树分块 + 关键点 bitset 预处理 + 路径颜色数/mex，树分块核心例题 | [https://hydro.ac/p/bzoj-P4763](https://hydro.ac/p/bzoj-P4763) |
| hydro | BZOJ4812 由乃打扑克 | 8 | 与 4763 类似，增加 bitset 16 位分组计数优化 | [https://hydro.ac/p/bzoj-P4812](https://hydro.ac/p/bzoj-P4812) |
| Luogu | P4074 | 7 | [WC2013] 糖果公园：树上莫队（依赖欧拉序分块），树分块思想在莫队中的应用 | [https://www.luogu.com.cn/problem/P4074](https://www.luogu.com.cn/problem/P4074) |

## Pitfalls · 易错点

- 朴素树分块在菊花图上退化，出题/评估复杂度时必须考虑树结构
- 关键点 bitset 预处理的『到祖先关键点』方向与路径方向需一致
- 块内暴力跳与块间跳的边界（是否已到 LCA 所在块）处理易错
- mex 查询用 _Find_first 而数颜色用 count，两者混用会得到错误结果
- 分块大小 B 需按 O(√n) 平衡预处理与查询代价，取错会超时

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/tree-decompose.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/tree-decompose.md)
- OI Wiki ✓ [https://oi-wiki.org/ds/tree-decompose/](https://oi-wiki.org/ds/tree-decompose/)
