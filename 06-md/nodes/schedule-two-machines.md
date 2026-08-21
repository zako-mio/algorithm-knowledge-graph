---
id: schedule-two-machines
name: 双机调度(Johnson 法则)
group: G-D-10
stage: advanced
priority: P2
depth_tier: standard
---

# 双机调度(Johnson 法则)

> 两台流水机作业调度，Johnson 法则求最短完工时间

<!-- 元信息: id=schedule-two-machines · group=G-D-10 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

双机流水作业调度（two-machine flow shop scheduling）：n 个作业都需先在第一台机器加工 a_i 分钟、再在第二台机器加工 b_i 分钟（加工顺序两机一致），求使总完工时间（makespan）最小的作业排列。Johnson 法则：若 min(a_i, b_i) < min(a_j, b_j)，则 i 应排在 j 之前。实现：把所有作业按 min(a_i,b_i) 排序；a_i < b_i 的作业放前面（按 a 升序），其余放后面（按 b 降序）。正确性由相邻交换证明（交换相邻两作业，空闲时间不增 ⟺ min(a_i,b_{i+1}) ≤ min(b_i,a_{i+1})）。复杂度 O(n log n)。当机器数≥3 时问题变为 NP-hard。

## Why · 为什么

### 直觉 · Intuition

直觉：若某作业在第一台耗时小（a<b），应尽早开工（把它放前面），让第二台尽早有活干；若它在第二台耗时小（b<a），应尽量往后放。更精确地，把作业看成'哪台机器更省时'分成两组：第一组（a<b）按 a 升序排，第二组（b≤a）按 b 降序排，两组拼接。整体目标是最小化第二台机器的总空闲时间。

### 原理 · Principle

设 x_k 为第二台在第 k 个作业前的空闲时间，总空闲时间 F=Σx_k 与完工时间只差常数（第二台总加工时间固定）。由递推 x_k=max(Σa−Σb前序−Σx前序, 0) 可得 F=max_k(Σ_{i≤k} a_i − Σ_{i<k} b_i)。相邻交换：交换 j、j+1 前后只影响 K_j、K_{j+1}，最优条件化为 max(−a_{j+1}, −b_j) ≤ max(−b_{j+1}, −a_j) ⟺ min(a_j, b_{j+1}) ≤ min(b_j, a_{j+1})。该比较器满足传递性，排序即得最优。

### 历史 · History

Johnson 法则由 S. M. Johnson 于 1954 年在论文 'Optimal two- and three-stage production schedules with setup times included' 中提出，是调度理论史上最早的多机精确算法，成为 flow shop 调度的奠基结果。机器数超过 2 时转为 NP-hard 也是 Johnson 工作中确立的边界。

## How · 实现

### 伪代码

```python
# Johnson 法则
for 每个作业: 记 (a, b, id)
sort 作业 by min(a,b)
A = []  # 收集 a < b 的作业 (放前面)
B = []  # 收集 a >= b 的作业 (放后面)
for job in sorted:
    if job.a < job.b: A.append(job)
    else: B.append(job)
order = A + reversed(B)   # B 部分反转
# 计算完工时间:
t1 = t2 = 0
for job in order:
    t1 += job.a
    t2 = max(t2, t1) + job.b
makespan = t2
```

### Python 实现

```python
def johnson(jobs):
    """Johnson 法则求双机调度最优顺序.
    jobs: list of (a, b, id). 返回最优顺序的 id 列表.
    """
    sorted_by_min = sorted(range(len(jobs)), key=lambda i: min(jobs[i][0], jobs[i][1]))
    A, B = [], []
    for i in sorted_by_min:
        a, b, _ = jobs[i]
        (A if a < b else B).append(i)
    order = A + list(reversed(B))
    return order


def makespan(jobs, order):
    """给定顺序的双机完工时间"""
    t1 = t2 = 0
    for i in order:
        a, b, _ = jobs[i]
        t1 += a
        t2 = max(t2, t1) + b
    return t2


if __name__ == "__main__":
    import itertools, random
    random.seed(0)

    def brute(jobs):
        return min(itertools.permutations(range(len(jobs))),
                   key=lambda o: makespan(jobs, o))

    # 经典样例 (来自 CP-Alg 中文题解): 应使完工时间最小
    jobs1 = [(3, 2, 0), (5, 1, 1), (2, 4, 2), (1, 3, 3)]
    o = johnson(jobs1)
    assert makespan(jobs1, o) == makespan(jobs1, brute(jobs1))

    # 随机对拍
    for _ in range(300):
        n = random.randrange(1, 8)
        js = [(random.randrange(1, 8), random.randrange(1, 8), i) for i in range(n)]
        o = johnson(js)
        assert makespan(js, o) == makespan(js, brute(js)), js

    # 单作业边界
    assert johnson([(5, 3, 7)]) == [0]

    print("schedule-two-machines tests passed")

```

**PyPy 提示**: 排序 O(n log n) 用 key=min(a,b) 即可；分组 A/B 用列表 append。计算完工时间时注意第二台可能等待（max 处理）。大 n 纯 Python 无压力。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n log n) |
| 空间 | O(n) |

### 局限

仅适用于两机流水线且顺序一致（每作业两机顺序相同）；三台及以上机器 NP-hard；若有中间缓冲限制/抢占/并行机则模型不同。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1248 | 4 | 加工生产调度：Johnson 法则模板题，需输出作业编号 | [https://www.luogu.com.cn/problem/P1248](https://www.luogu.com.cn/problem/P1248) |

## Pitfalls · 易错点

- a==b 时归入哪组都行，但实现要一致（通常 a<b 一组，a>=b 另一组再反转）
- B 组必须反转（按 b 降序）才能匹配比较器
- 完工时间计算用 t2=max(t2,t1)+b，漏掉 max 会算错空闲
- 三机及以上不能直接套 Johnson
- 比较器 min(a_i,b_{i+1}) ≤ min(b_i,a_{i+1}) 的等价分组别记反

## Sources · 信源

- CP-Algorithms ✓ [https://cp-algorithms.com/schedules/schedule_two_machines.html](https://cp-algorithms.com/schedules/schedule_two_machines.html)
- Wikipedia ✓ [https://en.wikipedia.org/wiki/Job_shop_scheduling](https://en.wikipedia.org/wiki/Job_shop_scheduling)
