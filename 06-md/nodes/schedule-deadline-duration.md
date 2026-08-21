---
id: schedule-deadline-duration
name: 截止期限-工期调度
group: G-D-10
stage: advanced
priority: P3
depth_tier: brief
---

# 截止期限-工期调度

> 给定截止期限与工期求最优调度可行性，贪心+堆

<!-- 元信息: id=schedule-deadline-duration · group=G-D-10 · stage=advanced · priority=P3 · depth_tier=brief -->

## What · 是什么

截止期限-工期调度问题：给定 n 个作业，每个有截止期限 d_i 与工期 t_i（不可中断），要求构造一个调度使'按时完成的作业数最多'。贪心算法（CP-Algorithms 的 schedule-with-completion-duration）：将作业按截止期限 d_i 升序排序；从后往前扫描（或用最小堆维护当前已选作业）。标准实现：维护一个最小堆 q 存已选作业的工期；按 d 升序依次考虑，把作业压入堆，若当前总工期超过当前截止期 d_i，则弹出工期最大的作业（丢弃），重复直到堆中总工期 ≤ d_i。最终堆中的作业即按时完成的集合，它们按截止期升序即为调度顺序。复杂度 O(n log n)。

## Why · 为什么

### 直觉 · Intuition

直觉：截止期越早的作业越'紧急'，应先考虑；当装不下时（总工期超截止期），应优先放弃'最耗时'的作业——因为放弃一个耗时长的作业，能让其余更多作业按时完成。这类似背包贪心：在固定截止期前缀上，用最小堆维护已选集合，超限时删最大者。

### 原理 · Principle

按截止期排序后，若某个前缀 [1..k] 中选了 S 集合作业，其按任意顺序都能在各自截止期内完成的充要条件是：把 S 按（截止期或工期任意）排序后，对每个前缀累积时间 ≤ 对应截止期；等价于累积时间 ≤ max 覆盖下的可行性。贪心正确性（exchange argument）：假设最优解在考虑某作业 x 时，当前堆方案有 t 个作业，最优解至多也多一个——用最短工期替换可保持最优性。堆中维护最小工期（pop 最大工期）使'删除作业'时损失最小。最终堆元素即为最优按时完成集。

### 历史 · History

这是'作业调度 deadline 下的最大完成数'经典贪心问题，源于调度理论中单机 deadline 调度（Moore 1955 的 1|ΣU_j 算法：最小化误期作业数）。Moore–Hodgson 算法即'按截止期排序 + 超限时删除最长作业'，是最早的贪心+堆算法之一，CP-Algorithms 的 schedule-with-completion-duration 条目给出了直接的实现。

## How · 实现

### 伪代码

```python
# 最大化按时完成的作业数 (贪心+最小堆)
按 deadline d 升序排序
heap = 最小堆 (存已选作业的 duration)
time = 0
for (d, t) in sorted_jobs:
    time += t
    heappush(heap, t)
    if time > d:
        time -= heappop(heap)   # 丢掉工期最大的作业 (time 减最大)
# 注意: 这里是'删最大'即堆 pop 最大, 用最小堆存负值 或 最大堆
# 堆中元素 = 最优按时完成集合
# 输出: 这些作业按截止期升序调度
```

### Python 实现

```python
import heapq


def max_on_time_jobs(jobs):
    """给定 (duration, deadline), 返回最多能按时完成的作业数量.
    贪心: 按截止期升序, 最小堆存工期, 超期删最大工期.
    """
    jobs = sorted(jobs, key=lambda x: x[1])
    heap = []   # 存 (duration), 用最小堆配合负值实现'取最大'删除
    time = 0
    for dur, ddl in jobs:
        time += dur
        heapq.heappush(heap, -dur)
        if time > ddl:
            # 删掉工期最大的作业
            time += heapq.heappop(heap)  # 加上负值 = 减去最大 duration
    return len(heap)


def build_schedule(jobs):
    """返回 (数量, 已选作业的原始下标列表, 顺序按截止期升序)."""
    jl = sorted([(dur, ddl, idx) for idx, (dur, ddl) in enumerate(jobs)], key=lambda x: x[1])
    heap = []   # (-duration, idx)
    time = 0
    for dur, ddl, idx in jl:
        time += dur
        heapq.heappush(heap, (-dur, idx))
        if time > ddl:
            popped = heapq.heappop(heap)
            time += popped[0]  # +(-dur) 即减去 dur
    chosen = [i for (_, i) in heap]
    chosen.sort(key=lambda i: jobs[i][1])  # 按截止期升序调度
    return len(chosen), chosen


if __name__ == "__main__":
    import itertools

    def brute(jobs):
        n = len(jobs)
        best = 0
        for mask in range(1 << n):
            subset = [jobs[i] for i in range(n) if mask >> i & 1]
            subset.sort(key=lambda x: x[1])
            time = 0
            ok = True
            for dur, ddl in subset:
                time += dur
                if time > ddl:
                    ok = False
                    break
            if ok:
                best = max(best, len(subset))
        return best

    import random
    random.seed(0)
    # 经典样例
    jobs = [(3, 5), (2, 3), (4, 9), (1, 2), (3, 6)]
    assert max_on_time_jobs(jobs) == brute(jobs)

    for _ in range(500):
        n = random.randrange(1, 9)
        js = [(random.randrange(1, 6), random.randrange(2, 15)) for _ in range(n)]
        assert max_on_time_jobs(js) == brute(js), js

    # schedule 构建验证
    n, chosen = build_schedule(jobs)
    assert n == brute(jobs)
    assert len(chosen) == n
    # 验证可行性
    time = 0
    for i in chosen:
        time += jobs[i][0]
        assert time <= jobs[i][1]

    print("schedule-deadline-duration tests passed")

```

**PyPy 提示**: 用 heapq，Python 内建最小堆。实现'删最大'时存负值入堆即可。注意 time 与堆内负 duration 的符号处理。O(n log n) 在 PyPy 下可跑 1e5+。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n log n)（排序 + 堆操作） |
| 空间 | O(n) |

### 局限

目标是'最大化按时完成数'；若目标是最小化加权延迟或总延迟则需其他算法；作业不可中断假设重要（可中断时模型不同）；若要求输出具体调度顺序需记录索引并按截止期排序输出。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P2949 | 3 | Work Scheduling：按截止期排序 + 最小堆删最大工期的经典贪心模板 | [https://www.luogu.com.cn/problem/P2949](https://www.luogu.com.cn/problem/P2949) |
| Codeforces | 864E | 4 | Fire：带价值版本（删时删价值最小的），贪心+堆 + DP 变体 | [https://codeforces.com/problemset/problem/864/E](https://codeforces.com/problemset/problem/864/E) |

## Pitfalls · 易错点

- '删最大工期'需用最大堆（Python 用负值最小堆），删错成最小工期会错
- time 累积计算要与堆同步：压入时加、弹出最大时减对应值
- 按截止期排序必须升序；构建调度时同样按截止期输出
- deadline 从 1 开始计时时，前缀条件 time ≤ d_i 而非 <
- 带权（每个作业有不同价值）时要删价值最小的而非工期最大的

## Sources · 信源

- CP-Algorithms ✓ [https://cp-algorithms.com/schedules/schedule-with-completion-duration.html](https://cp-algorithms.com/schedules/schedule-with-completion-duration.html)
- Wikipedia ✓ [https://en.wikipedia.org/wiki/Scheduling_(production_processes)](https://en.wikipedia.org/wiki/Scheduling_(production_processes))
