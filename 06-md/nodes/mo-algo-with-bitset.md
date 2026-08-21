---
id: mo-algo-with-bitset
name: 莫队 + bitset
group: G-D-7
stage: advanced
priority: P2
depth_tier: standard
---

# 莫队 + bitset

> 莫队维护区间状态 + bitset 存储权值出现信息，转移后位运算加速判定/统计类问题（如区间集合并、交、对称差）。

<!-- 元信息: id=mo-algo-with-bitset · group=G-D-7 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

莫队 + bitset（Mo's algorithm with bitset）把 bitset 与莫队结合：莫队负责把区间状态（如「哪些权值出现过」）O(1) 地维护成一个 bitset，查询时用位运算（与/或/异或/取反）批量完成常规数据结构难以维护的判定与统计。典型应用：求若干区间的交集元素个数、区间内是否存在两个数的和/差/积/商为某值等（Ynoi 系列大量采用）。

## Why · 为什么

### 直觉 · Intuition

莫队擅长维护「区间内某个集合」，bitset 擅长「把集合的判定一次性做完」。把两者结合：莫队指针移动时只维护当前区间每个权值的出现次数，并把「出现过的权值」映射到位集；一次查询可能需要多个区间的信息（如三个区间求并集），普通莫队要重复扫描，而 bitset 可以 O(1) 位运算合并多个区间。空间与时间各取其长。

### 原理 · Principle

① 权值离散化后，插入位置用「权值 + 当前出现次数」重编码，使同权值不同出现次数占不同位，避免 bitset 无法区分多重计数；② 莫队维护每个权值出现次数与当前区间 bitset；③ 指针移动顺序必须「先扩后缩」，否则区间长度为负时会在 bitset 中插入负数位（bitset 无法处理负数下标）；④ 多询问分组：bitset 空间 O(n×bitset_len) 过大，将询问分块（每块约 n/64 个）分别处理，保证空间恰好够；⑤ 回答用位运算：如三个区间并集大小 = len1+len2+len3 - popcount(并集)。

### 历史 · History

bitset 与莫队的结合主要在 Ynoi（由乃的 XX）系列题目中发扬光大，OI Wiki 以「Ynoi2016 掉进兔子洞」（P4688，三区间交集）为例详细讲解，并列出习题（P3674 小清新人渣的本愿、P5355 由乃的玉米田、P5313）。这些题目以高常数、卡常著称。

## How · 实现

### 伪代码

```python
cnt[v]   # 权值 v 出现次数
b        # bitset: 位 = 权值重编码(权值 + 累计出现次数)
add(v): cnt[v]++; b.set(encode(v, cnt[v]))
remove(v): b.reset(encode(v, cnt[v])); cnt[v]--
# 指针移动（先扩后缩）...
# 回答：把各区间 bitset 做按位或/与，用 popcount 求答案
# 分组：由于一个询问可能涉及多个区间，将询问按块分批，每批重建 bitset
```

### Python 实现

```python
# 说明：Python 无内建 bitset，可用 int 位运算模拟（1<<i 置位、bit_count 统计）。
# 骨架函数：演示 莫队维护“出现过的权值集合” + 三区间交集判定。
# 完整 Ynoi 题（如 P4688）还需：分组控制空间 + 出现次数重编码占位。
def mo_bitset_intersection(n, arr, queries):
    """莫队+bitset 骨架：求三个区间 交集元素个数（判定部分，含多重次数降级为集合）.
    queries: [(l1,r1,l2,r2,l3,r3,id)]. 返回按 id 的交集大小.
    注意：为可运行演示，这里把"出现次数"简化为"出现集合"（去重），
    完整 bitset 重编码见 OI Wiki 参考代码（值+次数 联合编码）。"""
    import math
    block = max(1, int(math.sqrt(n)))
    # 展平三条区间, 每条跑一次莫队收集集合
    intervals = []
    for i, (l1, r1, l2, r2, l3, r3, idx) in enumerate(queries):
        intervals += [(l1, r1, (idx, 0)), (l2, r2, (idx, 1)), (l3, r3, (idx, 2))]
    qs = sorted(intervals, key=lambda q: (q[0] // block, q[1] if (q[0]//block) % 2 == 0 else -q[1]))
    cnt = [0] * (max(arr) + 1 if arr else 1)
    present = set()
    l, r = 0, -1
    collected = {}
    for a, b, k in qs:
        while l > a:
            l -= 1
            cnt[arr[l]] += 1
            present.add(arr[l])
        while r < b:
            r += 1
            cnt[arr[r]] += 1
            present.add(arr[r])
        while l < a:
            cnt[arr[l]] -= 1
            if cnt[arr[l]] == 0:
                present.discard(arr[l])
            l += 1
        while r > b:
            cnt[arr[r]] -= 1
            if cnt[arr[r]] == 0:
                present.discard(arr[r])
            r -= 1
        collected[k] = set(present)
    ans = [0] * len(queries)
    for i, (l1, r1, l2, r2, l3, r3, idx) in enumerate(queries):
        ans[idx] = len(collected[(idx, 0)] & collected[(idx, 1)] & collected[(idx, 2)])
    return ans


if __name__ == "__main__":
    arr = [1, 2, 2, 3, 1]
    qs = [(0, 4, 0, 2, 2, 4, 0), (0, 1, 0, 4, 1, 3, 1)]
    res = mo_bitset_intersection(5, arr, qs)
    assert res == [2, 1], res
    import random
    random.seed(31)
    for _ in range(80):
        n = random.randint(1, 10)
        a = [random.randint(1, 4) for _ in range(n)]
        m = random.randint(1, 10)
        qs = []
        for i in range(m):
            def gen():
                x = random.randrange(n); y = random.randrange(x, n)
                return x, y
            l1, r1 = gen(); l2, r2 = gen(); l3, r3 = gen()
            qs.append((l1, r1, l2, r2, l3, r3, i))
        got = mo_bitset_intersection(n, a, qs)
        for (l1, r1, l2, r2, l3, r3, i) in qs:
            s1 = set(a[l1:r1+1]); s2 = set(a[l2:r2+1]); s3 = set(a[l3:r3+1])
            assert got[i] == len(s1 & s2 & s3), (a, l1, r1, l2, r2, l3, r3, got[i])
    print("All tests passed.")
```

**PyPy 提示**: Python 把大整数当位集：置位 x \| (1<<i)，统计用 int.bit_count()（PyPy3 支持）比 bin().count('1') 快；真实 Ynoi 题还需询问分组控制空间，且高度卡常，Python 极难通过，此骨架仅供理解思路（去重集合版可运行验证）。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O((n+q)√n + 分组数×位运算批量合并) |
| 空间 | O(n + 批数×bitset长度) |

### 局限

bitset 长度 = 权值种类×最大出现次数，n 大时需分组（Ynoi 典型 1e5 需分 ~60 批）；Python 无内建 bitset，int 模拟常数大，绝大多数 Ynoi 题 Python 无法 AC（需 C++/C 卡常）；指针移动顺序错误会导致 bitset 负下标。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P4688 | 6 | [Ynoi2016] 掉进兔子洞：三区间交集元素个数，莫队+bitset 模板，OI Wiki 例题 | [https://www.luogu.com.cn/problem/P4688](https://www.luogu.com.cn/problem/P4688) |
| Luogu | P3674 | 6 | 小清新人渣的本愿：区间内是否存在 a±b=k / a*b=k，bitset 移位+与，OI Wiki 习题 | [https://www.luogu.com.cn/problem/P3674](https://www.luogu.com.cn/problem/P3674) |
| Luogu | P5355 | 7 | [Ynoi2017] 由乃的玉米田：a/b=k 除法需根号分治，OI Wiki 习题 | [https://www.luogu.com.cn/problem/P5355](https://www.luogu.com.cn/problem/P5355) |

## Pitfalls · 易错点

- bitset 无法区分重复权值：必须用「权值重编码（值+出现次数）」占位，否则丢多重计数
- 指针移动顺序必须先扩后缩，否则区间为负导致插入负数位（bitset 下标越界）
- 单个大 bitset 空间 1e5×bitset 长度会爆内存：必须将询问按块分批
- Python 的 int.bit_count() 比 bin().count() 快；位宽很大时 int 运算本身开销高
- 合并多个区间 bitset 时注意是「或」还是「与」：三区间交集用与，多个单区间集合用或

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/mo-algo-with-bitset.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/mo-algo-with-bitset.md)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/code/mo-algo-with-bitset/mo-algo-with-bitset_1.cpp](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/code/mo-algo-with-bitset/mo-algo-with-bitset_1.cpp)
