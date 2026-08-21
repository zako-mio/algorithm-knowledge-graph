---
id: seg-beats
name: 吉司机线段树(Segment Beats)
group: G-D-8
stage: frontier
priority: P2
depth_tier: standard
---

# 吉司机线段树(Segment Beats)

> 区间取 min/max 等操作利用势能标记，均摊高效维护复杂区间信息

<!-- 元信息: id=seg-beats · group=G-D-8 · stage=frontier · priority=P2 · depth_tier=standard -->

## What · 是什么

Segment Beats 是一种维护区间最值操作(区间 chmin/chmax)的懒标记线段树：每个节点记录最大值 mx1、严格次大值 mx2、最大值个数 cntm，当新值 x 满足 mx2<x<mx1 时可直接打标记(O(1))，否则暴力递归下传。用势能分析保证总复杂度 O(m log n)。

## Why · 为什么

### 直觉 · Intuition

区间取 min 只影响「大于 x」的数；若当前区间里所有数都 ≤x 直接跳过，若次大值都 <x 说明只有最大值会变——这时一个标记就够；只有当 x≤次大值、无法确定影响范围时才被迫向下递归。这种「能懒则懒、不能就暴力」配合势能分析得到均摊高效。

### 原理 · Principle

节点维护 mx1/mx2/cntm/sum。chmin(l,r,x)：若 mx1≤x 跳过；若 mx2<x<mx1 则 sum+=cntm*(x-mx1)、mx1=x 打标记返回；若 x≤mx2 则 pushdown 后递归左右子节点再 pull。复杂度用势能函数(不同最大值段数)分析为 O(m log n)。可进一步推广到区间 chmax、区间加、历史最值。

### 历史 · History

Segment Beats 由吉如一提出，2014-2015 年在 Codeforces（Blog entry 57319）与 UOJ 发布，故名吉司机线段树；核心的势能分析保证区间取 min/max 均摊 O((n+m) log n)。

## How · 实现

### 伪代码

```python
apply_tag(p,x): 若 mx1[p]>x: sum+=cntm*(x-mx1); mx1=x
chmin(l,r,x,s,t,p): 若 mx1≤x 返回; 若 ⊆且 mx2<x: apply_tag; 否则 pushdown 递归 pull
```

### Python 实现

```python
import sys

# 区间 chmin(a_i, x) + 区间 max/sum 查询 (Segment Tree Beats)
INF = 1 << 60
mx1 = []   # 最大值
mx2 = []   # 严格次大值
cntm = []  # 最大值个数
sm = []    # 区间和


def build(a, s, t, p):
    if s == t:
        mx1[p] = a[s]; mx2[p] = -INF; cntm[p] = 1; sm[p] = a[s]
        return
    m = s + ((t - s) >> 1)
    build(a, s, m, p * 2); build(a, m + 1, t, p * 2 + 1)
    pull(p)


def pull(p):
    l, r = p * 2, p * 2 + 1
    sm[p] = sm[l] + sm[r]
    if mx1[l] > mx1[r]:
        mx1[p] = mx1[l]; cntm[p] = cntm[l]
        mx2[p] = max(mx2[l], mx1[r])
    elif mx1[l] < mx1[r]:
        mx1[p] = mx1[r]; cntm[p] = cntm[r]
        mx2[p] = max(mx1[l], mx2[r])
    else:
        mx1[p] = mx1[l]; cntm[p] = cntm[l] + cntm[r]
        mx2[p] = max(mx2[l], mx2[r])


def apply_tag(p, x):
    # chmin: 把当前最大值 mx1 限制为 x (仅当 mx1 > x)
    if mx1[p] <= x:
        return
    sm[p] += (x - mx1[p]) * cntm[p]
    mx1[p] = x


def pushdown(p):
    if mx1[p * 2] > mx1[p]:
        apply_tag(p * 2, mx1[p])
    if mx1[p * 2 + 1] > mx1[p]:
        apply_tag(p * 2 + 1, mx1[p])


def chmin(l, r, x, s, t, p):
    # 把 [l,r] 中 > x 的数变为 x
    if r < s or t < l or mx1[p] <= x:
        return
    if l <= s and t <= r and mx2[p] < x:
        apply_tag(p, x)
        return
    m = s + ((t - s) >> 1)
    pushdown(p)
    chmin(l, r, x, s, m, p * 2)
    chmin(l, r, x, m + 1, t, p * 2 + 1)
    pull(p)


def qmax(l, r, s, t, p):
    if l <= s and t <= r:
        return mx1[p]
    m = s + ((t - s) >> 1); pushdown(p); res = -INF
    if l <= m:
        res = max(res, qmax(l, r, s, m, p * 2))
    if r > m:
        res = max(res, qmax(l, r, m + 1, t, p * 2 + 1))
    return res


if __name__ == "__main__":
    sys.setrecursionlimit(1 << 20)
    n = 5
    a = [0, 10, 11, 12, 13, 14]
    k = 4 * n + 4
    for v in (mx1, mx2, cntm, sm):
        v.extend([0] * k)
    build(a, 1, n, 1)
    chmin(1, 5, 12, 1, n, 1)  # 所有>12的变12
    print(qmax(1, 5, 1, n, 1))  # 12

```

**PyPy 提示**: 递归+多条件分支 PyPy 常数较大；mx1/mx2/cntm 用三个平行列表存、局部变量化可加速。n,q=1e5 时 Python 常接近时限，必要时用数组而非对象。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 区间 chmin 均摊 O(log n)（整体 O(m log n)）；区间 chmax/加同理 |
| 空间 | O(4N) — 多维护 mx1/mx2/cntm/sum |

### 局限

Python 实现常数极大，n,m=1e5 在 1s 时限几乎必 TLE，仅适合学习/小数据；实际竞赛用 C++。标记下传涉及多种标记(加/chmin/chmax)时顺序极易写错，需严格按 apply 优先级处理。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| HDU | 5306 | 2400 | Gorgeous Sequence：区间取min+区间max/sum，Segment Beats 标准模板题 | [https://acm.hdu.edu.cn/showproblem.php?pid=5306](https://acm.hdu.edu.cn/showproblem.php?pid=5306) |
| LOJ | 6565 | 2700 | 最假女选手：区间加/chmax/chmin + 三种最值查询，多标记 Segment Beats | [https://loj.ac/p/6565](https://loj.ac/p/6565) |

## Pitfalls · 易错点

- mx2 必须是严格次大值(等于 mx1 的不算)，否则 chmin 标记会误伤
- 多种标记(加+chmin+chmax)并存时 apply/pushdown 顺序极易错，需逐种分析偏序关系
- 忘记在叶子节点特判导致 mx2 仍为 -INF 参与比较出错

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/seg-beats.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/seg-beats.md)
- web ✓ [https://atcoder.jp/contests/abc430/editorial/14433](https://atcoder.jp/contests/abc430/editorial/14433)
- web △ [https://codeforces.com/blog/entry/57319](https://codeforces.com/blog/entry/57319)
