---
id: planar-graph
name: 平面图
group: G-B-9
stage: advanced
priority: P3
depth_tier: brief
---

# 平面图

> 可嵌入平面的图：欧拉公式V-E+F=2、对偶图转最短路/最小割、稀疏边数\|E\|≤3\|V\|-6

<!-- 元信息: id=planar-graph · group=G-B-9 · stage=advanced · priority=P3 · depth_tier=brief -->

## What · 是什么

平面图（planar graph）是能画在平面上且除顶点外无边相交的图。核心工具与性质：(1) 欧拉公式 V-E+F=2（连通平面图），推论 |E|≤3|V|-6（简单平面图，故平面图稀疏）；(2) 对偶图：每个面对应一个点、每条边对应对偶边，把平面图最小割问题转化为对偶图最短路问题；(3) 判定：Kuratowski 定理（不含与 K5 或 K3,3 同胚的子图 ⇔ 平面）与 Wagner 定理（不可收缩到 K5/K3,3），线性判定算法有 Hopcroft-Tarjan、Boyer-Myrvold、LR 算法（实现复杂，竞赛极少手写，多用库）；(4) 四色定理、Fáry 定理、极大平面图（三角剖分）、外平面图等。

## Why · 为什么

### 直觉 · Intuition

平面性给图强加了稀疏性（边数 O(V)）与『面』结构。欧拉公式把边、点、面的数量锁死，于是许多稠密图算法在平面图上变快；对偶图把『割』与『路』互换——平面图上横跨 s-t 割的边集，正对应对偶图中一条 s*-t* 路径，所以最小割=对偶最短路。

### 原理 · Principle

欧拉公式：对连通平面图 V-E+F=2；k 连通分支时为 V-E+F=k+1。由面次数≥3 得 2E≥3F，代入欧拉公式得 E≤3V-6。对偶图构造：每个面取点，公共边界边连对偶边（割边连自环）；对偶图必连通，连通图满足 G**≅G。最小割→最短路：选使 s,t 共面的嵌入，加射线把外部面分成 f+,f-，则 G 的 s-t 边割集 ↔ G* 中 f+ 到 f- 的路径（权相等），用 Dijkstra 求最短路即得最小割（需保证存在使 s,t 共面的嵌入）。

### 历史 · History

平面图与欧拉公式是最古老图论结果之一（Euler 1752，多面体公式）；Kuratowski (1930) 与 Wagner (1937) 给出禁用子图刻画；Hopcroft-Tarjan (1974) 给出首个线性平面性判定算法，Boyer-Myrvold (1999)、LR 算法改进之。OI Wiki planar 章节（graph/planar）整理全部内容，并给出 Luogu P3209 平面图判定、P4001 狼抓兔子（最小割=对偶最短路经典题）、P4073[WC2013]平面图等习题。

## How · 实现

### 伪代码

```python
# 对偶图最短路求平面 s-t 最小割
G* = build_dual(G)
s_t_cut = shortest_path(G*, s*, t*)
# 欧拉公式计数: V-E+F=2, 推论 E≤3V-6
```

### Python 实现

```python
import math


def euler_check(V, E, F):
    """连通平面图欧拉公式 V - E + F == 2。"""
    return V - E + F == 2


def max_edges(V):
    """简单平面图边数上界 3V - 6 (V>=3)。"""
    return max(0, 3 * V - 6)


def dual_of_triangulation_edges(V):
    """极大平面图（三角剖分）: E = 3V - 6, F = 2V - 4。"""
    return 3 * V - 6, 2 * V - 4


def planar_mincut_via_dual(n, edges, s, t):
    """平面图最小割 -> 对偶图最短路（示意：接受对偶图已按面构造好）。
    本函数演示转化思想而非完整嵌入算法。
    说明：竞赛中通常题目直接给出平面嵌入，可手工按面建对偶图再跑 Dijkstra。
    """
    raise NotImplementedError(
        "完整实现需先构造平面嵌入与面表（复杂）。实战：P4001 狼抓兔子 直接建对偶网格图。"
    )


if __name__ == "__main__":
    # K4 四面体: V=4, E=6, F=4
    assert euler_check(4, 6, 4)
    # K5: V=5, E=10 > 3*5-6=9 非平面
    assert 10 > max_edges(5)
    # K3,3: V=6, E=9, 面次至少4 => E<=2V-4=8, 9>8 非平面
    assert 9 > 2 * 6 - 4
    # 极大平面图 三角剖分
    assert dual_of_triangulation_edges(6) == (12, 8)
    print("planar-graph 自测通过：欧拉公式/边数上界/三角剖分性质正确")

```

**PyPy 提示**: 平面图题目主要用『对偶图最短路』与『欧拉公式计数』两类；对偶图构造依赖平面嵌入，Python 端可直接建网格/按面建模，无需手写平面性判定（用库如 networkx 的 boyer_myrvold）。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 欧拉公式/边数计算 O(1)；对偶图最短路径 O(E log E)；平面性判定 O(V+E)（线性算法实现复杂） |
| 空间 | O(V+E) |

### 局限

最小割=对偶最短路仅在存在使 s,t 共面的平面嵌入时成立，需先验证（(V, E∪{(s,t)}) 可平面）；对偶图依赖具体嵌入，同一图不同嵌入对偶可不同构。平面性判定线性算法几乎不手写（竞赛中给嵌入）。Python 处理大量网格对偶图注意 I/O 常数。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P4001 | 5 | ICPC-Beijing 2006 狼抓兔子：平面图最小割=对偶图最短路经典题（OI Wiki 例题） | [https://www.luogu.com.cn/problem/P4001](https://www.luogu.com.cn/problem/P4001) |
| Luogu | P3209 | 6 | HNOI2010 平面图判定：利用哈密顿圈+边二分图判定（OI Wiki 例题） | [https://www.luogu.com.cn/problem/P3209](https://www.luogu.com.cn/problem/P3209) |
| Luogu | P3249 | 6 | HNOI2016 矿区：平面图点定位+对偶图（OI Wiki 习题） | [https://www.luogu.com.cn/problem/P3249](https://www.luogu.com.cn/problem/P3249) |

## Pitfalls · 易错点

- 欧拉公式要求连通；不连通用 V-E+F=k+1
- E≤3V-6 仅对简单图（无重边自环）且 V≥3
- K3,3 判非平面要用面次数≥4 的 2E≥4F，不能套 3V-6
- 最小割→最短路要求 s,t 共面的嵌入，缺失则转化不成立
- 对偶图是对具体嵌入定义的，别对『可平面图』（未给嵌入）直接建对偶

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/planar/](https://oi-wiki.org/graph/planar/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/planar.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/graph/planar.md)
- CP-Algorithms △ [https://cp-algorithms.com/geometry/planar.html](https://cp-algorithms.com/geometry/planar.html)
