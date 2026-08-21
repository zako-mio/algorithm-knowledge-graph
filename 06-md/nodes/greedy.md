---
id: greedy
name: 贪心算法
group: G-A-1
stage: basic
priority: P0
depth_tier: deep
---

# 贪心算法

> 每步取局部最优，需证明最优子结构与交换论证

<!-- 元信息: id=greedy · group=G-A-1 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

贪心算法（greedy algorithm）每一步都做当前看起来最优的选择，不回头（不可回退），并证明这种局部最优能拼出全局最优。适用于有『最优子结构』的问题。证明方法：邻项交换（反证/交换论证）、归纳法。经典模型：按某关键字排序后依次选择（离线）、每步取最大/最小并更新（在线，常配优先队列）、后悔法（先假设全做，不行再反悔换出最差的）。与 DP 的区别：贪心不保存中间状态、不可回退；DP 保存并回退。

## Why · 为什么

### 直觉 · Intuition

『贪心的人目光短浅：每一步都选当下最好的』。只有在『局部最优能推出全局最优』的问题上才成立。判断标志：决策之间有交换性/单调性，使得先选哪个顺序都不影响后续最优结构。

### 原理 · Principle

邻项交换法：若任意相邻两元素交换后答案不会变好，则当前顺序已最优（国王游戏 P1080 的经典推导：比较 max(b[i+1], a[i]*b[i]) 与 max(b[i], a[i+1]*b[i+1]) 得到排序规则）。归纳法：证明 F(n+1) 可由 F(n) 的最优解经贪心一步得到。后悔法：先全做，超限时用堆换出收益最小的（P2949 工作调度）。正确性必须证明，不能只凭直觉。

### 历史 · History

贪心思想古已有之（找零钱、Dijkstra），1960s 起算法教科书系统整理。『matroid 理论』（Edmonds 1971）给出了贪心最优的代数刻画：独立系统为拟阵当且仅当贪心对所有权重最优。竞赛中贪心与『排序+优先队列』两大套路覆盖多数入门贪心题。

## How · 实现

### 伪代码

```python
# 模型1 排序后选择（离线）：按规则排序，然后依序贪心选取
# 模型2 每步取最优（在线）：用堆/优先队列维护候选
# 模型3 后悔法：
for 每个决策（按截止时间排序）:
    先接受它（push 进堆）
    if 超限: ans -= 堆中最小的；pop 它
```

### Python 实现

```python
import heapq


def merge_fruits(a):
    """P1090 合并果子：每次合并两堆最小，总代价最小（Huffman 树）"""
    heapq.heapify(a)
    cost = 0
    while len(a) > 1:
        x = heapq.heappop(a)
        y = heapq.heappop(a)
        cost += x + y
        heapq.heappush(a, x + y)
    return cost


def interval_scheduling(tasks):
    """活动安排：按结束时间升序，贪心选最早结束且不冲突的活动"""
    tasks.sort(key=lambda t: t[1])
    cnt, last_end = 0, -1
    for s, e in tasks:
        if s >= last_end:
            cnt += 1
            last_end = e
    return cnt


def work_scheduling(jobs):
    """P2949 Work Scheduling（后悔法）：jobs=(deadline, profit)，求最大收益"""
    jobs.sort()
    q = []
    total = 0
    for d, p in jobs:
        heapq.heappush(q, p)
        total += p
        if len(q) > d:               # 时间超限：反悔换出收益最小的
            total -= heapq.heappop(q)
    return total


if __name__ == "__main__":
    assert merge_fruits([2, 3, 4, 6]) == 29
    assert merge_fruits([1, 2, 9]) == 15
    assert interval_scheduling([(1, 3), (2, 5), (3, 9), (4, 6), (5, 7), (6, 9)]) == 3
    assert work_scheduling([(2, 100), (1, 19), (2, 27), (1, 25), (1, 15)]) == 127
    assert work_scheduling([(4, 20), (1, 10), (1, 40), (1, 30)]) == 60
    import random
    for _ in range(200):
        n = random.randint(1, 9)
        jobs = [(random.randint(1, 5), random.randint(1, 50)) for _ in range(n)]
        # 暴力验证后悔法
        from itertools import combinations
        best = 0
        for mask in range(1 << n):
            pick = [jobs[i] for i in range(n) if mask >> i & 1]
            pick.sort()
            ok = True
            for k, (d, p) in enumerate(pick, 1):
                if k > d:
                    ok = False
                    break
            if ok:
                best = max(best, sum(p for _, p in pick))
        assert work_scheduling(jobs) == best, (jobs, work_scheduling(jobs), best)
    print("贪心（合并果子/活动安排/工作调度后悔法）正确性 OK（200 组暴力对照）")
    print("P1090 示例:", merge_fruits([1, 2, 9]))

```

**PyPy 提示**: 贪心题在 PyPy 下的瓶颈常在排序与堆操作：heapq 已 C 优化直接可用。注意 deadline 可能很大（1e9），排序用 deadline 做 key；后悔法堆里只存收益值即可。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 通常 O(n log n)（排序/堆） |
| 空间 | O(n) |

### 局限

必须证明贪心正确性，否则极易写出『看起来对』的假贪心。不可用于无最优子结构或反例可构造的问题；不确定时优先考虑 DP 或对拍验证。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1080 | 5 | 邻项交换贪心模板 | [https://www.luogu.com.cn/problem/P1080](https://www.luogu.com.cn/problem/P1080) |
| Luogu | P2949 | 4 | 后悔法/反悔贪心 | [https://www.luogu.com.cn/problem/P2949](https://www.luogu.com.cn/problem/P2949) |
| Luogu | P1090 | 3 | Huffman 优先队列 | [https://www.luogu.com.cn/problem/P1090](https://www.luogu.com.cn/problem/P1090) |

## Pitfalls · 易错点

- 不证明就写贪心：必须邻项交换/归纳/反例验证，否则是赌博
- 混淆离线（排序后选择）与在线（边选边更新）两种模型，套错模板
- 后悔法里超限判断用 len(q)>deadline 而非 >=，取决于题意（能否做 deadline 个任务）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/basic/greedy/](https://oi-wiki.org/basic/greedy/)
- 书籍 ✓ `CPH ch6 p67`
- OI Wiki ✓ [https://www.luogu.com.cn/problem/P1090](https://www.luogu.com.cn/problem/P1090)
