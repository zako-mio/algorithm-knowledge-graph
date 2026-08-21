---
id: mo-algorithm
name: 莫队算法（普通莫队）
group: G-D-7
stage: intermediate
priority: P1
depth_tier: standard
---

# 莫队算法（普通莫队）

> 离线区间询问：按 l 所在块排序 + 奇偶化 r，双指针 O(1) 转移，O(n√n) 处理多类可差分区间的询问。

<!-- 元信息: id=mo-algorithm · group=G-D-7 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

莫队（Mo's algorithm）是一类离线算法：把所有区间询问离线存储，按「左端点所在块的编号为第一关键字、右端点为第二关键字」排序，然后维护当前区间 [cur_l, cur_r] 的答案，用四个 while 循环 O(1) 地向目标区间移动双指针，每移动一步用 add/remove 更新答案。适用于任何「从一个区间 O(1) 扩展到相邻区间」的统计问题，例如区间不同数个数、区间众数、区间内数值和、区间逆序对（配合二次离线）等。其本质是把询问视为平面上的点 (l,r)，沿曼哈顿距离较小的顺序在点之间转移，从而摊还移动代价。

## Why · 为什么

### 直觉 · Intuition

把所有询问排序后，相邻询问的区间高度相似：左端点在同一个块内来回摆动（每次移动 ≤ 块长 s），右端点在同一块内单调递增（整块扫过一遍至多移动 n 次）。把这两部分代价分别摊还：左端点总移动 O(m·s)，右端点总移动 O((n/s)·n)。取 s=√n 时两者平衡，得到 O(n√n)。奇偶化排序进一步把右端点在相邻块间的回程复用，常数提升约 30%。

### 原理 · Principle

① 分块：序列按块长 s 分块，s 一般取 √n 或 n/√m；② 排序：l 所在块号第一关键字，r 第二关键字（奇数块 r 升序、偶数块 r 降序即奇偶化）；③ 维护：四个 while 循环分别处理 l--, r++, l++, r-- 四种扩展/收缩，每次调用 O(1) 的 add(v)/remove(v) 更新答案；④ 移动顺序必须保持「先扩后缩」（l-- 和 r++ 在前，l++ 和 r-- 在后），否则会出现区间长度为负、元素被删除但从未加入的脏状态。复杂度：分块 O(n log n)，双指针总移动 O(n√n)（n,m 同阶）。

### 历史 · History

莫队算法由莫涛（2010 年代国内 OI 选手）提出并归纳总结，他在 Codeforces 高手圈流传的做法基础上系统化整理而成；OI Wiki 明确记载「莫队算法是由莫涛提出的算法……莫涛是第一个对莫队算法进行详细归纳总结的人」。经 OIer/ACMer 集体改造衍生出带修莫队、树上莫队、回滚莫队、二次离线等变体。它是一类「优雅的暴力」，其时间复杂度上界已被证明对任意排序方式都是渐近最优的（n,m 同阶时处理全部询问至少 O(n√n)）。

## How · 实现

### 伪代码

```python
block = int(sqrt(n))
qs.sort(key=lambda q: (q.l//block, q.r if (q.l//block)%2==0 else -q.r))
cur_l, cur_r, ans_now = 0, -1, 0
for q in qs:
    while cur_l > q.l: cur_l--; add(a[cur_l])       # 先扩
    while cur_r < q.r: cur_r++; add(a[cur_r])
    while cur_l < q.l: remove(a[cur_l]); cur_l++   # 后缩
    while cur_r > q.r: remove(a[cur_r]); cur_r--
    ans[q.id] = ans_now
```

### Python 实现

```python
def mo_algorithm(n, arr, queries):
    """普通莫队：区间不同数字个数.
    n: 序列长度; arr: 序列(0-indexed); queries: [(l,r,id)] 闭区间.
    返回 ans 数组（按查询 id）."""
    import math
    block = max(1, int(math.sqrt(n)))
    qs = sorted(queries, key=lambda q: (q[0] // block, q[1] if (q[0]//block) % 2 == 0 else -q[1]))
    cnt = [0] * (max(arr) + 1 if arr else 1)
    cur_l, cur_r, cur = 0, -1, 0
    ans = [0] * len(queries)
    for l, r, idx in qs:
        while cur_l > l:
            cur_l -= 1
            if cnt[arr[cur_l]] == 0: cur += 1
            cnt[arr[cur_l]] += 1
        while cur_r < r:
            cur_r += 1
            if cnt[arr[cur_r]] == 0: cur += 1
            cnt[arr[cur_r]] += 1
        while cur_l < l:
            cnt[arr[cur_l]] -= 1
            if cnt[arr[cur_l]] == 0: cur -= 1
            cur_l += 1
        while cur_r > r:
            cnt[arr[cur_r]] -= 1
            if cnt[arr[cur_r]] == 0: cur -= 1
            cur_r -= 1
        ans[idx] = cur
    return ans

if __name__ == "__main__":
    arr = [1, 2, 1, 3, 2]
    queries = [(0, 4, 0), (1, 3, 1), (0, 0, 2), (2, 4, 3)]
    res = mo_algorithm(5, arr, queries)
    assert res == [3, 3, 1, 3], res
    # 与暴力交叉验证
    import random
    random.seed(7)
    for _ in range(200):
        n = random.randint(1, 12)
        a = [random.randint(1, 5) for _ in range(n)]
        m = random.randint(1, 15)
        qs = []
        for i in range(m):
            l = random.randint(0, n - 1); r = random.randint(l, n - 1)
            qs.append((l, r, i))
        got = mo_algorithm(n, a, qs)
        for (l, r, i) in qs:
            expect = len(set(a[l:r + 1]))
            assert got[i] == expect, (a, l, r, got[i], expect)
    print("mo_algo OK")

```

**PyPy 提示**: cnt 用 list 而非 dict（值域大时先离散化）；add/remove 尽量内联到 while 循环中避免函数调用开销；Python 下莫队的瓶颈是四个 while 的 Python 层循环，建议用 PyPy 运行（纯 Python 下 n=m=1e5 时约 3e7 次指针移动，CPython 会超时，PyPy 可过）。块长可微调为 n//sqrt(m)。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n√n)（n,m 同阶；一般形式 O(n·m/√S + mS)，S 取 n/√m 时 O(n√m)） |
| 空间 | O(n+m) |

### 局限

仅支持离线（必须提前知道全部询问）；要求转移可 O(1) 完成（否则考虑二次离线莫队）；无法处理强制在线或带修改的场景（带修改需带修莫队）。纯 Python 实现常数较大，n,m 达 1e6 时容易 TLE，需 PyPy + 微调块长。区间内无法 O(1) 维护的统计（如动态最值）不适用普通莫队，可考虑回滚莫队。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1494 | 3 | 【模板】小 Z 的袜子：区间内取两个同色数的概率，组合数转移 add/remove 为 O(1)，OI Wiki 莫队模板例题 | [https://www.luogu.com.cn/problem/P1494](https://www.luogu.com.cn/problem/P1494) |
| Luogu | P1972 | 3 | HH 的项链：区间不同数个数模板，莫队/树状数组均可 | [https://www.luogu.com.cn/problem/P1972](https://www.luogu.com.cn/problem/P1972) |
| CSES | Distinct Values Queries | 3 | CSES 区间不同数个数，莫队可直接过 | [https://cses.fi/problemset/task/1734](https://cses.fi/problemset/task/1734) |
| Luogu | CF617E | 3 | XOR and Favorite Number：区间内 xor 为 k 的对数，前缀 xor 后莫队维护桶，经典莫队+xor | [https://www.luogu.com.cn/problem/CF617E](https://www.luogu.com.cn/problem/CF617E) |

## Pitfalls · 易错点

- 四个 while 的先后顺序不能乱改：必须「先扩后缩」（l--/r++ 在前，l++/r-- 在后），否则 l>r+1 时会出现「删除未加入的元素」的脏状态（OI Wiki 证明 24 种排列仅 6 种正确）
- 块长选错会严重劣化：m 与 √n 同阶时若把块长误设为 √n，复杂度从 O(n^(5/4)) 退化为 O(n√n)
- 奇偶化排序的 key 里 r 的取反符号必须与块号奇偶绑定，写错会导致 r 指针来回震荡
- cnt 数组下标越界：值域大时必须先离散化
- Python 中不要用 dict 的 get 做 add/remove 核心路径（常数大），优先 list + 离散化

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/mo-algo.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/mo-algo.md)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/mo-algo-intro.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/mo-algo-intro.md)
- 书籍 ✓ `CPH ch27 pp261-269`
- CP-Algorithms ✓ [https://cp-algorithms.com/data_structures/sqrt_decomposition.html](https://cp-algorithms.com/data_structures/sqrt_decomposition.html)
