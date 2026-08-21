---
id: li-chao-tree
name: 李超线段树
group: G-D-8
stage: advanced
priority: P1
depth_tier: standard
---

# 李超线段树

> 线段树维护线段/直线集合，标记永久化求横坐标处最值

<!-- 元信息: id=li-chao-tree · group=G-D-8 · stage=advanced · priority=P1 · depth_tier=standard -->

## What · 是什么

李超线段树把「线段/直线集合」存进线段树：每个节点存一条当前区间内「最优」线段作永久化标记，插入新线段时在中点比较、把较优者留下、较劣者递归下传到唯一可能更优的子区间，查询时沿路径取所有标记的 max。

## Why · 为什么

### 直觉 · Intuition

两条直线最多在一个子区间相交，所以在某一半区间内哪条更优是确定的——可把较劣的那条只在它可能赢的那一半继续下传，另一条留在当前节点当标记。这保证每条线段每次只会递归到一个子区间。

### 原理 · Principle

节点 p 存直线 f_p。插入直线 g 到区间 [cl,cr]，比中点 m 处值：若 g(m)>f_p(m) 则交换 g 与 f_p(让 g 留下当标记)。再比端点：若 g 在左端点更优则 g 只可能在左半赢，递归左儿子；若在右端点更优则递归右儿子；左右端点 f_p 都更优则 g 无需下传。标记永久化——查询时沿根到叶路径对所有标记取 max，无需 pushdown。

### 历史 · History

李超线段树由李超在 2013-2014 年竞赛中提出并传播（CF 讨论与《算法竞赛进阶指南》收录），核心「中点比较+单侧递归」思想在 OI 社区成熟。

## How · 实现

### 伪代码

```python
upd(p,cl,cr,k,b): m=(cl+cr)/2; 若 g(m)>f(m) 交换 g,f; 若 g(左端)>f(左端) 递归左; 若 g(右端)>f(右端) 递归右
query: 沿路径对所有节点标记取 max
```

### Python 实现

```python
import sys

# 李超线段树: 维护线段集合, 查询某横坐标处纵坐标最大值
INF = float("inf")
K = [0]     # 斜率 (1-indexed, 下标 0 为占位)
B = [0]     # 截距
lc = [0]    # 左儿子
rc = [0]    # 右儿子
tot = 0


def new_node():
    global tot
    tot += 1
    K.append(0); B.append(-INF)
    lc.append(0); rc.append(0)
    return tot


def f(k, b, x):
    return k * x + b


def upd(p, cl, cr, k, b):
    # 在区间 [cl,cr] 插入直线 y=kx+b
    m = (cl + cr) >> 1
    if not lc[p]:
        lc[p] = new_node()
    if not rc[p]:
        rc[p] = new_node()
    if f(k, b, m) > f(K[p], B[p], m):
        k, K[p] = K[p], k
        b, B[p] = B[p], b
    if f(k, b, cl) > f(K[p], B[p], cl):
        upd(lc[p], cl, m, k, b)
    if f(k, b, cr) > f(K[p], B[p], cr):
        upd(rc[p], m + 1, cr, k, b)


def upd_seg(p, cl, cr, l, r, k, b):
    # 插入线段 y=kx+b, 定义域 [l,r]
    if l <= cl and cr <= r:
        upd(p, cl, cr, k, b)
        return
    m = (cl + cr) >> 1
    if l <= m:
        if not lc[p]:
            lc[p] = new_node()
        upd_seg(lc[p], cl, m, l, r, k, b)
    if r > m:
        if not rc[p]:
            rc[p] = new_node()
        upd_seg(rc[p], m + 1, cr, l, r, k, b)


def query(p, cl, cr, x):
    # 查询横坐标 x 处最大纵坐标
    res = f(K[p], B[p], x)
    m = (cl + cr) >> 1
    if x <= m and lc[p]:
        res = max(res, query(lc[p], cl, m, x))
    if x > m and rc[p]:
        res = max(res, query(rc[p], m + 1, cr, x))
    return res


if __name__ == "__main__":
    sys.setrecursionlimit(1 << 20)
    root = new_node()
    XR = 1 << 18
    upd_seg(root, 1, XR, 1, XR, 1, 0)        # y = x
    upd_seg(root, 1, XR, 1, XR, -1, 100)     # y = -x + 100
    print(query(root, 1, XR, 50))            # 50  (y=x 与 y=-x+100 交于 x=50)
    print(query(root, 1, XR, 1))             # 99

```

**PyPy 提示**: 标记永久化+单链递归 PyPy 常数小；斜率/截距用列表存。整数斜率建议交叉乘法避免浮点误差。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 插入直线 O(log C)；插入线段(定义域跨多区间)O(log² C)；查询 O(log C)。C 为横坐标值域 |
| 空间 | O(Q log C) — 动态开点按需建 |

### 局限

Python 浮点比较易出精度问题，整数斜率建议用分数/交叉乘法避免 eps；垂直线段(x0==x1)会除零，需特殊处理为定义域 [x,x] 的一次函数 f(x)=0·x+y1；查询横坐标超出已插入范围时返回 -INF 需判空。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P4097 | 5 | HEOI2013 Segment：插入线段+查询某 x 处纵坐标最大的线段编号，李超树模板 | [https://www.luogu.com.cn/problem/P4097](https://www.luogu.com.cn/problem/P4097) |

## Pitfalls · 易错点

- 垂直线段(x0==x1)除零，必须特判为定义域单点的一次函数
- 浮点斜率用 eps 比较精度不足，整数场景改交叉乘法
- 多条线段交点纵坐标相同时要按编号取较小者(题目要求)

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/li-chao-tree.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/li-chao-tree.md)
- OI Wiki ✓ [https://oi-wiki.org/ds/li-chao-tree/](https://oi-wiki.org/ds/li-chao-tree/)
- CP-Algorithms ✓ [https://cp-algorithms.com/geometry/convex_hull_trick.html](https://cp-algorithms.com/geometry/convex_hull_trick.html)
