---
id: seg-lazy
name: 懒标记线段树
group: G-A-6
stage: intermediate
priority: P0
depth_tier: deep
---

# 懒标记线段树

> 区间修改+区间查询，lazy tag延迟下发均摊O(log n)

<!-- 元信息: id=seg-lazy · group=G-A-6 · stage=intermediate · priority=P0 · depth_tier=deep -->

## What · 是什么

在基础线段树上为每个节点增设懒标记(lazy tag)，区间修改时只更新被完全覆盖的节点并打标记、不下传，仅在下次访问其子节点前 pushdown 下传，从而把区间修改也从 O(n) 降为均摊 O(log n)。

## Why · 为什么

### 直觉 · Intuition

如果区间修改要逐个改叶子，复杂度退化到 O(n)。观察到：很多被修改的叶子在下次查询前根本不会被读到——那就不必立即改它们，只需在父节点「记账」，等到真正要用子节点时再把这个账分摊下去。

### 原理 · Principle

节点 p 维护区间和 d[p] 与待下传标记 b[p]。区间加 [l,r]+=c 时：若 [s,t]⊆[l,r]，则 d[p]+=(t-s+1)*c、b[p]+=c 直接返回；否则先 pushdown(把 b[p] 加到 d/b[2p]、d/b[2p+1] 并清零)，再递归子节点，最后 d[p]=d[2p]+d[2p+1] pushup。查询时同样在递归前 pushdown。标记「账」只在被访问时才结算，使每次区间操作只触碰 O(log n) 个节点。

### 历史 · History

懒标记/标记下传是线段树从「单点」走向「区间修改」的关键技术，与树状数组的差分思想异曲同工。其 pushdown/pullup 范式后来被推广到乘法标记、赋值标记、历史标记(Segment Beats)、标记永久化(李超树/可持久化)等众多变体，是全部线段树族区间操作结构的基础机制。

## How · 实现

### 伪代码

```python
pushdown(p): d[2p]+=b[p]*(m-s+1); d[2p+1]+=b[p]*(t-m); b[2p]+=b[p]; b[2p+1]+=b[p]; b[p]=0
update(l,r,c,s,t,p): 若⊆则 d[p]+=c*len,b[p]+=c; 否则 pushdown 后递归, pushup
query: 同 update 前置 pushdown
```

### Python 实现

```python
import sys

def build(s, t, p, a, d, b):
    if s == t:
        d[p] = a[s]
        return
    m = s + ((t - s) >> 1)
    build(s, m, p * 2, a, d, b)
    build(m + 1, t, p * 2 + 1, a, d, b)
    d[p] = d[p * 2] + d[p * 2 + 1]


def pushdown(p, s, m, t, d, b):
    # 将 p 的懒标记下传给两个子节点
    if b[p]:
        d[p * 2] += b[p] * (m - s + 1)
        d[p * 2 + 1] += b[p] * (t - m)
        b[p * 2] += b[p]
        b[p * 2 + 1] += b[p]
        b[p] = 0


def update(l, r, c, s, t, p, d, b):
    # 区间 [l,r] 每个数加上 c
    if l <= s and t <= r:
        d[p] += (t - s + 1) * c
        b[p] += c
        return
    m = s + ((t - s) >> 1)
    pushdown(p, s, m, t, d, b)
    if l <= m:
        update(l, r, c, s, m, p * 2, d, b)
    if r > m:
        update(l, r, c, m + 1, t, p * 2 + 1, d, b)
    d[p] = d[p * 2] + d[p * 2 + 1]


def query(l, r, s, t, p, d, b):
    if l <= s and t <= r:
        return d[p]
    m = s + ((t - s) >> 1)
    pushdown(p, s, m, t, d, b)
    res = 0
    if l <= m:
        res += query(l, r, s, m, p * 2, d, b)
    if r > m:
        res += query(l, r, m + 1, t, p * 2 + 1, d, b)
    return res


if __name__ == "__main__":
    sys.setrecursionlimit(1 << 20)
    n = 5
    a = [0, 10, 11, 12, 13, 14]
    d = [0] * (4 * n + 4)
    b = [0] * (4 * n + 4)
    build(1, n, 1, a, d, b)
    update(3, 5, 5, 1, n, 1, d, b)  # [3,5] 每个数+5
    print(query(4, 4, 1, n, 1, d, b))  # 18 (原13+5)
    print(query(1, 5, 1, n, 1, d, b))  # 75

```

**PyPy 提示**: PyPy 对本实现(递归+列表)JIT 友好，但深递归仍建议 sys.setrecursionlimit(1<<20)；大整数与列表访问均较 CPython 快；区间操作常数约为 C++ 的 5-15 倍，N>1e6 且时限 1s 的题易 TLE。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O((N+Q)log N) — 区间修改/查询均摊 O(log n) |
| 空间 | O(4N) — d 数组与 b 标记数组各 4N |

### 局限

Python 常数大，N=1e5、Q=1e5 的模板题在 1s 时限下 CPython 常需配合 sys.stdin 批量读入与 PyPy 才稳过；乘法+加法双标记要处理下传顺序(先乘后加)；区间赋值(覆盖)标记需用特殊初值区分「无标记」。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3373 | 4 | 区间加+区间乘+区间和，双标记下传顺序(先乘后加)经典题 | [https://www.luogu.com.cn/problem/P3373](https://www.luogu.com.cn/problem/P3373) |
| HDU | 6356 | 2200 | Glad You Came：区间取min+永久标记，线段树剪枝 | [https://acm.hdu.edu.cn/showproblem.php?pid=6356](https://acm.hdu.edu.cn/showproblem.php?pid=6356) |
| Codeforces | 438D | 2100 | The Child and Sequence：区间取模(chmin 变体)+单点修改，势能线段树入门 | [https://codeforces.com/problemset/problem/438D](https://codeforces.com/problemset/problem/438D) |

## Pitfalls · 易错点

- 双标记(加+乘)下传顺序必须先乘后加：apply mul 标记时 add 标记也要乘，否则数值错乱
- pushdown 前忘清零 b[p]=0 导致标记被重复下传，结果偏大
- 区间赋值(覆盖)标记初值选 0 会与「加 0」混淆，需用 -1/INF 或单独 bool 标记区分
- 标记数组未初始化为 0 导致随机脏数据
- 叶子节点(s==t)不应再 pushdown(无子节点)，否则数组越界

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/seg/](https://oi-wiki.org/ds/seg/)
- CP-Algorithms ✓ [https://cp-algorithms.com/data_structures/segment_tree.html](https://cp-algorithms.com/data_structures/segment_tree.html)
- 书籍 ✓ `CPH ch28 (Segment tree with lazy propagation)`
