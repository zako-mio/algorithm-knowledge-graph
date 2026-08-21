---
id: mo-modifiable
name: 带修莫队
group: G-D-7
stage: advanced
priority: P2
depth_tier: standard
---

# 带修莫队

> 给莫队加时间维，询问变三元组 (l,r,t)，块长 n^(2/3)，O(n^(5/3)) 支持单点修改的区间询问。

<!-- 元信息: id=mo-modifiable · group=G-D-7 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

带修莫队（Mo's algorithm with modifications / modifiable Mo）在普通莫队的基础上增加一维时间 t，把询问记作 (l, r, t)，其中 t 表示「该询问前已经执行了多少次修改」。状态由 (l, r, t) 三元组构成，双指针从二维变成三维：除 l、r 外，还要在时间轴上前进/回退，即应用或撤销第 t 个修改。适用于「区间询问 + 单点修改」的离线问题，例如区间不同数个数（带改）、区间 k 小（带改）等。块长取 n^(2/3) 时左右端点在块间移动与时间轴移动的代价平衡，总复杂度 O(n^(5/3))。

## Why · 为什么

### 直觉 · Intuition

普通莫队没法处理修改，因为指针只在一个维度上摆动。强行加一维时间后，把修改也当成指针的一次移动：从时间 t 到 t+1 等价于「把当前序列上第 t+1 次修改的位置的值更新」，代价也是 O(1)（仅当被修改位置在当前区间内时需要同步更新答案）。问题是时间维的移动次数不好控制——块长必须让「左右端点块内摆动代价」与「时间维乱序代价」同时被摊还。若把块长定为 n^(2/3)，则左右端点在块内摆动 O(n^(2/3))，块间换块时时间维最多单调扫 O(t)（每对块一次），总代价 O(n·(n^(2/3)) + (n/n^(2/3))²·t) = O(n^(5/3))（n,m,t 同阶）。

### 原理 · Principle

① 分块：块长 s=n^(2/3)，共 n^(1/3) 块；② 排序：第一关键字 l 所在块、第二关键字 r 所在块、第三关键字 t（可奇偶化）；③ 三维指针：先调整时间维（应用/回退修改），再调整 l、r 的普通莫队四 while；④ 修改应用：若修改位置 pos 在当前区间内，则先删除旧值再加入新值并同步答案，最后更新序列快照 cur[pos]=new；⑤ 回退同理反向。关键：必须先记录每个修改位置的旧值（change=(pos, old, new)），回退时才能正确还原。时间维移动与区间移动的前后顺序保持一致，否则旧值/新值与当前区间不匹配。

### 历史 · History

带修莫队是 OIer 对普通莫队的经典扩展，把莫涛算法与「时间戳」思想结合，最早流行于国内 OI 圈子（典型例题为「国家集训队」P1903 数颜色/维护队列）。其最优块长 n^(2/3) 与复杂度 O(n^(5/3)) 的证明由 OI Wiki 完整给出（对 f(s)=ms+n²t/s² 求导取极值）。与之类似的三维莫队思想也出现在「带修改树上莫队」（如 WC2013 糖果公园）中。

## How · 实现

### 伪代码

```python
block = int(pow(n, 2.0/3))
qs.sort(key=lambda q: (q.l//block, q.r//block, q.t))
changes = build_changes(arr, changes)   # 每个修改记 (pos, old, new)
cur = arr[:]        # 序列快照
l, r, tm = 0, -1, 0
for q in qs:
    while tm < q.t:            # 应用修改
        pos,old,new = changes[tm]
        if l<=pos<=r: remove(old); add(new)
        cur[pos] = new; tm += 1
    while tm > q.t:            # 回退修改
        tm -= 1; pos,old,new = changes[tm]
        if l<=pos<=r: remove(new); add(old)
        cur[pos] = old
    while l > q.l: add(cur[--l])       # 普通莫队四 while
    while r < q.r: add(cur[++r])
    while l < q.l: remove(cur[l++])
    while r > q.r: remove(cur[r--])
    ans[q.id] = ans_now
```

### Python 实现

```python


def build_changes(arr, changes):
    """为每个修改记录 (pos, old, new)，old=应用前该位置的值."""
    cur = list(arr)
    res = []
    for pos, newv in changes:
        res.append((pos, cur[pos], newv))
        cur[pos] = newv
    return res

def mo_modifiable(n, arr, queries, changes):
    changes = build_changes(arr, changes)  # 记录每个修改位置的旧值
    """带修莫队：区间不同数字个数（支持单点修改）.
    arr: 初始序列; queries: [(l,r,t,id)] 闭区间, t=该询问前已执行的修改数;
    changes: [(pos, new_val)] 修改操作（顺序执行）. 返回 ans 数组."""
    import math
    block = max(1, int(pow(n, 2.0 / 3)))
    qs = sorted(queries, key=lambda q: (q[0] // block, q[1] // block, q[2] if (q[1]//block) % 2 == 0 else -q[2]))
    cur = list(arr)
    cnt = [0] * (max(cur) + 1 if cur else 1)
    def ensure_size(v):
        while len(cnt) <= v: cnt.append(0)
    def add_val(v):
        nonlocal ans_now
        ensure_size(v)
        if cnt[v] == 0: ans_now += 1
        cnt[v] += 1
    def del_val(v):
        nonlocal ans_now
        cnt[v] -= 1
        if cnt[v] == 0: ans_now -= 1
    l, r, tm = 0, -1, 0
    ans_now = 0
    ans = [0] * len(queries)
    for ql, qr, qt, idx in qs:
        while tm < qt:
            pos, oldv, newv = changes[tm]
            if l <= pos <= r:
                del_val(oldv); add_val(newv)
            cur[pos] = newv
            tm += 1
        while tm > qt:
            tm -= 1
            pos, oldv, newv = changes[tm]
            if l <= pos <= r:
                del_val(newv); add_val(oldv)
            cur[pos] = oldv
        while l > ql:
            l -= 1; add_val(cur[l])
        while r < qr:
            r += 1; add_val(cur[r])
        while l < ql:
            del_val(cur[l]); l += 1
        while r > qr:
            del_val(cur[r]); r -= 1
        ans[idx] = ans_now
    return ans

if __name__ == "__main__":
    arr = [1, 2, 3, 4, 5]
    changes = [(2, 9), (0, 7)]
    # 询问: id0 在0次修改后查[0,4]; id1 在2次修改后查[0,4]; id2 在1次修改后查[1,3]
    queries = [(0, 4, 0, 0), (0, 4, 2, 1), (1, 3, 1, 2)]
    res = mo_modifiable(5, arr, queries, changes)
    assert res == [5, 5, 3], res
    # 交叉验证: 对每个询问按时间快照暴力
    import random, copy
    random.seed(11)
    for _ in range(150):
        n = random.randint(1, 10)
        a = [random.randint(1, 4) for _ in range(n)]
        t_cnt = random.randint(0, 5)
        ch = [(random.randrange(n), random.randint(1, 6)) for _ in range(t_cnt)]
        m = random.randint(1, 12)
        qs = []
        for i in range(m):
            l = random.randint(0, n - 1); r = random.randint(l, n - 1)
            t = random.randint(0, t_cnt)
            qs.append((l, r, t, i))
        got = mo_modifiable(n, a, qs, ch)
        for (l, r, t, i) in qs:
            snap = list(a)
            for j in range(t): snap[ch[j][0]] = ch[j][1]
            expect = len(set(snap[l:r + 1]))
            assert got[i] == expect, (a, ch, l, r, t, got[i], expect)
    print("mo_modifiable OK")

```

**PyPy 提示**: cnt 用 list + 离散化；add/del 函数尽量内联；排序第三关键字对 r 所在块奇偶化可优化时间维移动。注意把查询与修改分开存储，修改按下标直接顺序应用。O(n^(5/3)) 在纯 Python 下 n=1e5 时较吃力，建议 PyPy + 块长微调。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n^(5/3))（n,m,t 同阶；一般形式 O(n^(2/3)·m^(2/3)·t^(1/3))） |
| 空间 | O(n+m) |

### 局限

仅离线；修改必须可逆/可重放（回退时需要知道每个修改位置的旧值）；n,m,t 达 1e6 时 O(n^(5/3)) 无法承受（需更高级做法如回滚+分块或值域分块）。每个修改必须维护「位置是否在当前区间」判断，否则会污染答案。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1903 | 4 | 【模板】数颜色/维护队列：带修莫队区间不同数个数，OI Wiki 例题 | [https://www.luogu.com.cn/problem/P1903](https://www.luogu.com.cn/problem/P1903) |
| BZOJ | 2120 | 4 | 数颜色 原题（BZOJ 2120），P1903 同题 | [https://hydro.ac/p/bzoj-P2120](https://hydro.ac/p/bzoj-P2120) |
| Luogu | P2464 | 4 | [SDOI2008] 郁闷的小 J：区间内某值出现次数 + 单点改值，带修莫队维护每个值计数 | [https://www.luogu.com.cn/problem/P2464](https://www.luogu.com.cn/problem/P2464) |

## Pitfalls · 易错点

- 修改应用/回退顺序与区间调整顺序必须固定一致，否则旧值/新值与当前区间不匹配
- 回退修改时必须还原为「该位置应用前的旧值」，因此建 changes 时要记录 (pos, old, new)，不能只存 new
- 块长误用 √n 会导致时间维乱序代价 O(n²)，必须用 n^(2/3)
- 排序第三关键字不奇偶化时时间维在块间可能来回扫，常数大；若 m 远小于 n 块长应微调
- cnt 值域大时必须离散化；修改引入的新值也要能容纳（动态扩容或预离散化）

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/modifiable-mo-algo.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/modifiable-mo-algo.md)
- OI Wiki ✓ [https://oi-wiki.org/misc/modifiable-mo-algo/](https://oi-wiki.org/misc/modifiable-mo-algo/)
- 书籍 △ `CPH ch27（莫队变体概述）`
