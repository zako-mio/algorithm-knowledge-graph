---
id: schedule-one-machine
name: 单机调度
group: G-D-10
stage: advanced
priority: P2
depth_tier: standard
---

# 单机调度

> 单机作业排序使最大延迟/完工时间最优，按截止期贪心

<!-- 元信息: id=schedule-one-machine · group=G-D-10 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

单机调度（scheduling on one machine）问题：n 个作业在一台机器上依次加工，作业 i 耗时 t_i，若作业在等待 t 秒后才被处理则需付罚金 f_i(t)。目标是最小化总罚金 F(π)=Σ f_πi(等待时间)。特殊情形可精确求解：①线性罚函数 f_i(t)=c_i·t：按 c_i/t_i 非增排序（交换相邻两项分析最优条件）；②指数罚函数 f_i(t)=c_i·e^(αt)：按 (1−e^(αt_i))/c_i 非增排序；③相同单调增罚函数：按 t_i 非降排序。Livshits–Kladov 定理：排列法（交换相邻作业看罚金变化）仅适用于上述三类罚函数。若目标改为'最小化最大延迟'，则按截止期 d_i 非降排序（EDD 规则）贪心。

## Why · 为什么

### 直觉 · Intuition

相邻交换（permutation method）：若最优排列中相邻两个作业 i、j 交换后罚金不变差，则可推导出排序准则。对线性罚金 f=c·t，交换相邻两作业只影响这两项的罚金变化 Δ=c_i·t_j − c_j·t_i；要求 Δ≥0（最优排列中不交换更好），化简得 c_i/t_i ≥ c_j/t_j，故按 c/t 降序。直观：'代价系数/耗时'越大的作业越该先做。对截止期目标，直觉是先做截止期最早的作业（EDD）才能避免延迟累积。

### 原理 · Principle

相邻交换法证明全局最优：假设排列 π 最优，则任何相邻交换不降低目标；由此推出对所有相邻位置满足局部不等式，该不等式是传递的，故整个排列由该排序准则唯一确定，从而全局最优。线性情形：c_i·t_j ≥ c_j·t_i ⟺ c_i/t_i ≥ c_j/t_j。EDD（最早截止期优先）最小化最大延迟：若某排列中 d_i>d_j 却先做 i，交换后最大延迟不增。注意：'单机+最小化总完成时间'的经典结果是 SPT（最短加工时间优先）；不同目标对应不同排序规则，务必先看清目标函数。

### 历史 · History

单机排序是调度理论（Scheduling Theory）最基础的模型，起源可追溯至 1950s（Smith 1956 的加权完成时间排序，等价于线性罚函数 c_i/t_i 排序；Jackson 1955 提出 EDD 规则）。Livshits 与 Kladov 定理界定了相邻交换法适用的罚函数族。CP-Algorithms 的 schedule_one_machine 条目以线性/指数/单调三种罚函数系统介绍了这一经典问题。

## How · 实现

### 伪代码

```python
# 线性罚函数 f_i(t)=c_i*t, 最小化总罚金
sort jobs by (c_i / t_i) 降序   # 或按 c_i*t_j > c_j*t_i 比较器

# 相同单调罚函数(如均方差/总完成时间) => 按 t_i 升序 (SPT)
# 指数罚函数 => 按 (1-exp(a*t_i))/c_i 降序

# 最小化最大延迟 => 按 deadline d_i 升序 (EDD)
```

### Python 实现

```python
def schedule_linear(jobs):
    """单机+线性罚金 f_i(t)=c_i*t: 按 c/t 降序排.
    jobs: list of (t_i, c_i). 返回最优顺序列表.
    """
    return sorted(range(len(jobs)), key=lambda i: jobs[i][1] / jobs[i][0], reverse=True)


def total_penalty(jobs, order):
    """给定顺序的总罚金 (线性情形): sum c_i * (等待时间)"""
    time = 0
    total = 0
    for i in order:
        t, c = jobs[i]
        total += c * time
        time += t
    return total


def schedule_edd(jobs):
    """最小化最大延迟: EDD 按截止期升序.
    jobs: list of (duration, deadline). 返回顺序.
    """
    return sorted(range(len(jobs)), key=lambda i: jobs[i][1])


def max_lateness(jobs, order):
    """最大延迟 L_max = max(completion - deadline)"""
    time = 0
    L = 0
    for i in order:
        dur, ddl = jobs[i]
        time += dur
        L = max(L, time - ddl)
    return L


if __name__ == "__main__":
    # 线性罚金: 对拍暴力
    import itertools

    def brute_linear(jobs):
        return min(itertools.permutations(range(len(jobs))),
                   key=lambda o: total_penalty(jobs, o))

    jobs1 = [(2, 3), (3, 1), (1, 5), (4, 2)]
    ord1 = schedule_linear(jobs1)
    assert total_penalty(jobs1, ord1) == total_penalty(jobs1, brute_linear(jobs1))

    for _ in range(200):
        import random
        random.seed(0)
        n = random.randrange(1, 8)
        js = [(random.randrange(1, 8), random.randrange(1, 8)) for _ in range(n)]
        o = schedule_linear(js)
        assert total_penalty(js, o) == total_penalty(js, brute_linear(js)), js

    # EDD 最小化最大延迟: 对拍暴力
    def brute_edd(jobs):
        return min(itertools.permutations(range(len(jobs))),
                   key=lambda o: max_lateness(jobs, o))

    jobs2 = [(3, 6), (2, 5), (4, 9), (1, 2)]
    o2 = schedule_edd(jobs2)
    assert max_lateness(jobs2, o2) == max_lateness(jobs2, brute_edd(jobs2))

    for _ in range(200):
        n = random.randrange(1, 8)
        js = [(random.randrange(1, 8), random.randrange(1, 15)) for _ in range(n)]
        o = schedule_edd(js)
        assert max_lateness(js, o) == max_lateness(js, brute_edd(js)), js

    print("schedule-one-machine tests passed")

```

**PyPy 提示**: 排序直接内建 sort + key，O(n log n)。比较器若用自定义 cmp_to_key 会慢，尽量用 key 构造（如 c/t 浮点、或避免浮点用交叉乘）。大数据量下浮点 c/t 排序注意精度：用交叉乘法 comparator 更稳。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n log n)（一次排序） |
| 空间 | O(n) |

### 局限

仅适用于三类特殊罚函数（线性/指数/相同单调）；其他罚函数需一般整数规划/搜索；'最小化最大延迟'用 EDD，但若同时有准备时间等约束则复杂化；若作业可中断（preemptive）模型不同。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1248 | 4 | 加工生产调度：双机流水作业 Johnson 法则（见 schedule-two-machines） | [https://www.luogu.com.cn/problem/P1248](https://www.luogu.com.cn/problem/P1248) |
| Luogu | P2123 | 5 | 皇后游戏：相邻交换推排序比较器（线性罚函数思想的竞赛变体） | [https://www.luogu.com.cn/problem/P2123](https://www.luogu.com.cn/problem/P2123) |

## Pitfalls · 易错点

- 不同目标函数对应不同排序规则：线性罚金 c/t、EDD 用于最大延迟、SPT 用于总完成时间，勿混用
- 浮点除法排序在大数据下精度问题，改用交叉乘法比较
- 带常数项罚金（f_i(t)=c_i·t+d_i）先把常数项单独求和
- 作业可能被'可中断/抢占'模型改变结果
- 相邻交换法只在满足 Livshits–Kladov 前提时适用

## Sources · 信源

- CP-Algorithms ✓ [https://cp-algorithms.com/schedules/schedule_one_machine.html](https://cp-algorithms.com/schedules/schedule_one_machine.html)
- Wikipedia ✓ [https://en.wikipedia.org/wiki/Job_shop_scheduling](https://en.wikipedia.org/wiki/Job_shop_scheduling)
