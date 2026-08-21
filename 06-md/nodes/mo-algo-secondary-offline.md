---
id: mo-algo-secondary-offline
name: 二次离线莫队
group: G-D-7
stage: frontier
priority: P3
depth_tier: brief
---

# 二次离线莫队

> 单次转移非 O(1) 时把每次转移的贡献差分并再离线一次，用值域分块/扫描线批量处理，降低整体复杂度。

<!-- 元信息: id=mo-algo-secondary-offline · group=G-D-7 · stage=frontier · priority=P3 · depth_tier=brief -->

## What · 是什么

二次离线莫队（Mo's algorithm with secondary offline）处理「单次转移不是 O(1)」的莫队问题：普通莫队要求每次移动指针 O(1) 更新答案，但有些统计（如区间逆序对）单次转移需要 O(log n) 或更多。若每次转移的贡献可差分（写成 f(x, 1..r) - f(x, 1..l-1) 形式），就先把这些「前缀式」贡献离线存到对应端点上，再用一次扫描线/值域分块批量回答，使单次转移摊还接近 O(1)。典型代表：Luogu P5047（Ynoi，区间逆序对）、P5501（来者不拒去者不追）。

## Why · 为什么

### 直觉 · Intuition

莫队移动指针时，扩展右端点 r→r+1 需要知道「a[r+1] 在当前区间 [l,r] 内的排名/逆序贡献」，朴素做是 O(log n)。但把贡献写成 f(a[r+1], 1..r) - f(a[r+1], 1..l-1)，第一项可对每个 r 预处理（树状数组 O(n log n)），第二项只依赖前缀端点 l-1，把所有这样的项离线按端点存下来，再从左到右扫描前缀，用值域分块 O(√n) 插入 O(1) 查询（或树状数组 O(log n) 查询）批量回答。于是莫队指针移动时只需 O(1) 记账，真实代价集中到这一次扫描线上。

### 原理 · Principle

① 莫队移动的每次贡献写成「预处理项 + 离线项」：扩右 = f(r,r-1) - f(r,l-1)；扩左 = g(x,r) - g(x,x-1)；缩左 = -g(x,r) + g(x,x-1)；缩右 = -f(x,r-1) + f(x,l-1)；② 预处理项（f(x,x-1)、g(x,x-1)）用树状数组一遍 O(n log n) 求出；③ 离线项按端点 p 存入 rec[p]，扫描前缀时批量回答 f(x,p)/g(x,p)（用值域分块可做到 O(√n) 插入 + O(1) 查询，插入共 O(n)，查询共 O(n√m)）；④ 答案 = 当前询问的直接贡献累计 + 该询问的扫描线贡献（注意跨询问携带当前答案）。空间优化：把每段指针移动合并记录，空间从 O(n√m) 降到 O(m)。

### 历史 · History

二次离线莫队是 Ynoi 系列的标志性技巧，OI Wiki 以 P5047（Yuno loves sqrt technology II，区间逆序对）和 P5501 为例详细讲解。它把「莫队转移非 O(1)」这个痛点通过再离线一次解决，是根号算法的进阶形态。

## How · 实现

### 伪代码

```python
# 预处理 f_sp(x)=[0..x-1]中>a[x]的个数, g_sp(x)=[0..x-1]中<a[x]的个数
# 莫队移动时:
#   扩左 l--: cur -= g_sp[l]; rec[r] += (l, lt, +1)
#   扩右 r++: cur += f_sp[r]; rec[l-1] += (r, gt, -1)
#   缩左 l++: cur += g_sp[l]; rec[r] += (l, lt, -1)
#   缩右 r--: cur -= f_sp[r]; rec[l-1] += (r, gt, +1)
# 记录每个询问的 cur
# 扫描线: p=0..n 插入 a[0..p], 回答 rec[p] 中各项 f(x,p)/g(x,p), 累加到对应询问
# 最终 ans = 记录的cur + 扫描线累计贡献
```

### Python 实现

```python
class BIT:
    def __init__(self, n):
        self.n = n
        self.t = [0] * (n + 1)
    def add(self, i, x):
        i += 1
        while i <= self.n:
            self.t[i] += x
            i += i & -i
    def sum(self, i):
        if i < 0:
            return 0
        s = 0
        i += 1
        while i > 0:
            s += self.t[i]
            i -= i & -i
        return s


def mo_secondary_offline(n, arr, queries):
    """二次离线莫队：区间逆序对个数（完整实现）.
    转移差分:
      扩左 l--: +g(x,r) - g_sp(x)     (x=l, g_sp(x)=[0..x]中<a[x]的个数)
      扩右 r++: +f_sp(x) - f(x,l-1)   (x=r, f_sp(x)=[0..x-1]中>a[x]的个数)
      缩左 l++: -g(x,r) + g(x,l)
      缩右 r--: -f_sp(x) + f(x,l-1)
    queries: [(l,r,id)] 闭区间 0-indexed. 复杂度 O((n+q)sqrt n + n log n)."""
    import math
    block = max(1, int(math.sqrt(n)))
    qs = sorted(queries, key=lambda q: (q[0] // block, q[1] if (q[0]//block) % 2 == 0 else -q[1]))
    vals = sorted(set(arr))
    rank = {v: i for i, v in enumerate(vals)}
    a = [rank[v] for v in arr]
    V = len(vals)

    f_sp = [0] * n
    g_sp = [0] * n
    t = BIT(V)
    for x in range(n):
        f_sp[x] = x - t.sum(a[x])          # [0..x-1] 中 > a[x]
        g_sp[x] = t.sum(a[x] - 1)          # [0..x-1] 中 < a[x]
        t.add(a[x], 1)

    rec = [[] for _ in range(n + 1)]       # rec[p]: (x, typ, sign, proc); proc=处理顺序
    ans = [0] * len(queries)
    now = [0] * len(qs)                    # 直接项累计（按处理顺序）
    later_cap = [0] * len(qs)              # 扫描线累计（按处理顺序，先占位后填充）
    later_acc = [0] * len(qs)              # 扫描线前缀累计
    cur = 0
    l, r = 0, -1
    proc = 0
    for ql, qr, idx in qs:
        while l > ql:                      # 扩左
            l -= 1
            cur -= g_sp[l]
            rec[r].append((l, 1, +1, proc))
        while r < qr:                      # 扩右
            r += 1
            cur += f_sp[r]
            if l - 1 >= 0:
                rec[l - 1].append((r, 0, -1, proc))
        while l < ql:                      # 缩左
            cur += g_sp[l]
            rec[r].append((l, 1, -1, proc))
            l += 1
        while r > qr:                      # 缩右
            cur -= f_sp[r]
            if l - 1 >= 0:
                rec[l - 1].append((r, 0, +1, proc))
            r -= 1
        now[proc] = cur
        proc += 1

    t = BIT(V)
    run = 0
    for p in range(n + 1):
        if p < n:
            t.add(a[p], 1)
        for x, typ, sign, proc in rec[p]:
            if typ == 0:                   # gt(x,p): 前缀[0..p]中 > a[x]
                v = (p + 1) - t.sum(a[x])
            else:                          # lt(x,p): 前缀[0..p]中 < a[x]
                v = t.sum(a[x] - 1)
            later_acc[proc] += sign * v
    for i in range(len(qs)):
        run += later_acc[i]
        later_cap[i] = run
    for i, (_, _, idx) in enumerate(qs):
        ans[idx] = now[i] + later_cap[i]
    return ans


if __name__ == "__main__":
    arr = [5, 1, 3, 2, 4]
    qs = [(0, 4, 0), (1, 3, 1), (2, 4, 2)]
    def brute_inv(a, l, r):
        c = 0
        for i in range(l, r + 1):
            for j in range(i + 1, r + 1):
                if a[i] > a[j]:
                    c += 1
        return c
    res = mo_secondary_offline(5, arr, qs)
    for (l, r, i) in qs:
        b = brute_inv(arr, l, r)
        assert res[i] == b, (l, r, res[i], b)
        print(l, r, res[i])
    import random
    random.seed(41)
    for _ in range(400):
        n = random.randint(1, 10)
        a = [random.randint(1, 5) for _ in range(n)]
        m = random.randint(1, 12)
        qs = []
        for i in range(m):
            l = random.randrange(n); r = random.randrange(l, n)
            qs.append((l, r, i))
        got = mo_secondary_offline(n, a, qs)
        for (l, r, i) in qs:
            exp = brute_inv(a, l, r)
            assert got[i] == exp, (a, l, r, got[i], exp)
    print("mo_secondary_offline OK")

```

**PyPy 提示**: 值域分块实现「O(√n) 插入 + O(1) 排名查询」可压常数；若直接用树状数组，查询 O(log n) 会让总复杂度带 log；rec 用 list of list，Python 需注意每端点分桶开销；n=m=1e5 时扫描线查询次数 O(n√n)≈3e7，纯 Python 压力大，需 PyPy。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n√m + n√n)（值域分块）；若用树状数组 O((n√m)log n) |
| 空间 | O(n + m)（优化后） |

### 局限

要求每次转移的贡献可差分（写成前缀式）；实现细节多，正确性敏感（端点 -1 越界、符号、跨询问携带答案）；值域分块常数优化是过题关键；纯 Python 通过 P5047 难度极高，建议理解思想 + C++ 实现。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P5047 | 8 | [Ynoi2019] Yuno loves sqrt technology II：区间逆序对，二次离线莫队模板，OI Wiki 例题 | [https://www.luogu.com.cn/problem/P5047](https://www.luogu.com.cn/problem/P5047) |
| Luogu | P5501 | 8 | [LnOI2019] 来者不拒，去者不追：区间 Abbi 值（k*a_i 加权），二次离线莫队，OI Wiki 例题 2 | [https://www.luogu.com.cn/problem/P5501](https://www.luogu.com.cn/problem/P5501) |

## Pitfalls · 易错点

- 端点 l-1 可能为 -1，rec 下标越界（Python 负索引会静默错），必须跳过
- 答案必须跨询问携带（now 累计 + 每询问快照），不能每询问从 0 开始，否则丢 carry
- 扫描线贡献要按处理顺序前缀累计，最终 ans = now快照 + 累计扫描贡献
- 扩左/缩左用「小于」函数 g，扩右/缩右用「大于」函数 f，方向写反会错
- 空间优化：把整段指针移动合并成一条 rec，否则 O(n√m) 条记录在 n=1e5 时爆内存

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/mo-algo-secondary-offline.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/mo-algo-secondary-offline.md)
- OI Wiki △ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/code/mo-algo-secondary-offline/mo-algo-secondary-offline_1.cpp](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/code/mo-algo-secondary-offline/mo-algo-secondary-offline_1.cpp)
