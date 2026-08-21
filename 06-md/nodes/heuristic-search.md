---
id: heuristic-search
name: 启发式搜索
group: G-A-14
stage: intermediate
priority: P1
depth_tier: standard
---

# 启发式搜索

> 估价函数引导分支选择，可行性/最优性剪枝

<!-- 元信息: id=heuristic-search · group=G-A-14 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

启发式搜索是在普通搜索算法（DFS/BFS）基础上引入启发式函数（估价函数）的搜索范式。启发式函数基于已有信息对每个分支的选择做估价，从而：①优先探索更有希望的节点；②用'乐观上界'（贪心估计）对无望的分支做最优性剪枝；③对违反约束的分支做可行性剪枝。A*、IDA*、分支限界法都是启发式搜索的具体形态。

## Why · 为什么

### 直觉 · Intuition

暴力搜索像'所有路口都试'，启发式搜索像'有地图的人'：先走看起来更接近目标的岔路（优先搜索），并提前知道哪些路已经不可能赢（剪枝）。估价函数 h 回答'从这还能走多远/还能拿多少'，用它判断这条分支值不值得继续。

### 原理 · Principle

启发式搜索的剪枝两类：①可行性剪枝——当前状态已违反约束（超容量/越界），子树全部非法，直接返回；②最优性剪枝——用乐观上界 cur_v + 剩余最佳可能 与当前最优 best 比较，若 cur_v + optimistic_upper_bound ≤ best，则这条分支不可能刷新最优解，整棵子树剪掉。核心要求是估价'乐观'（不低估剩余价值），否则会误剪掉真正的最优解。估价越接近真实，剪枝越有效。A* 的可采纳性（admissible）正是这一原则在最短路径上的形式化。

### 历史 · History

启发式搜索源自 1950s-1970s 的人工智能研究（Shakey 机器人项目、GPS 通用问题求解器）。A* 由 Hart、Nilsson 与 Raphael 于 1968 年提出；分支限界法（branch and bound）由 Land 与 Doig 于 1960 年提出。OI Wiki 以 0/1 背包（P1048 采药）作为启发式剪枝入门例。

## How · 实现

### 伪代码

```python
# 启发式搜索 DFS 框架
best = -inf

def dfs(状态, 当前代价):
    if 违反约束(可行性剪枝): return
    if 乐观上界(当前+剩余最好) <= best (最优性剪枝): return
    if 达到目标: best = max(best, 当前代价); return
    for 每个选择:
        做选择
        dfs(下一状态)
        撤销

# 关键: 估价函数 h 必须乐观(不低估), 否则误剪
```

### Python 实现

```python
def knapsack_branch_bound(values, weights, capacity):
    """0/1背包启发式搜索(分支限界): 返回最大价值
    估价: 按价值密度降序 + 后缀价值作为乐观上界剪枝
    """
    n = len(values)
    items = sorted(zip(values, weights), key=lambda x: x[0] / x[1], reverse=True)
    v = [x[0] for x in items]
    w = [x[1] for x in items]
    suffix_best = [0] * (n + 1)  # 后缀最优价值(乐观上界)
    for i in range(n - 1, -1, -1):
        suffix_best[i] = suffix_best[i + 1] + v[i]
    best = 0

    def dfs(i, cur_v, cur_w):
        nonlocal best
        if cur_w > capacity:     # 可行性剪枝
            return
        if cur_v > best:
            best = cur_v
        if i == n:
            return
        if cur_v + suffix_best[i] <= best:  # 最优性剪枝(乐观上界)
            return
        dfs(i + 1, cur_v + v[i], cur_w + w[i])  # 选
        dfs(i + 1, cur_v, cur_w)                 # 不选

    dfs(0, 0, 0)
    return best


if __name__ == "__main__":
    def knapsack_bruteforce(values, weights, capacity):
        n = len(values)
        best = 0
        for mask in range(1 << n):
            vv = ww = 0
            for i in range(n):
                if mask >> i & 1:
                    vv += values[i]
                    ww += weights[i]
            if ww <= capacity and vv > best:
                best = vv
        return best

    # 基础用例
    assert knapsack_branch_bound([60, 100, 120], [10, 20, 30], 50) == 220
    assert knapsack_branch_bound([10, 20], [5, 10], 5) == 10
    assert knapsack_branch_bound([1, 1], [1, 1], 1) == 1

    # 随机对拍暴力
    import random
    random.seed(1)
    for _ in range(200):
        n = random.randint(1, 10)
        values = [random.randint(1, 20) for _ in range(n)]
        weights = [random.randint(1, 15) for _ in range(n)]
        cap = random.randint(1, 30)
        a = knapsack_branch_bound(values, weights, cap)
        b = knapsack_bruteforce(values, weights, cap)
        assert a == b, (values, weights, cap, a, b)

    print("heuristic-search all tests passed (200 random checks)")

```

**PyPy 提示**: 启发式剪枝搜索常用递归+全局最优值，PyPy 下注意递归深度限制。剪枝顺序影响巨大：先按'更有希望'的顺序扩展能更快逼近 best，使最优性剪枝更早生效。上界计算用浮点需谨慎，最好整数化避免浮点误差。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 最坏仍指数级；实际取决于估价函数质量，接近 O(答案路径·分支) 时最佳 |
| 空间 | O(深度)（DFS 框架） |

### 局限

估价函数必须'乐观'否则误剪正确解；剪枝收益难以理论保证（无 worst-case 优势）；估价函数设计依赖问题结构，通用性差；纯 Python 在 n 大时仍慢。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1048 | 2 | NOIP2005 采药：0/1背包启发式剪枝入门题 | [https://www.luogu.com.cn/problem/P1048](https://www.luogu.com.cn/problem/P1048) |
| Luogu | P1120 | 4 | 小木棍：可行性+最优性剪枝综合应用经典题 | [https://www.luogu.com.cn/problem/P1120](https://www.luogu.com.cn/problem/P1120) |

## Pitfalls · 易错点

- 估价函数不乐观（高估剩余价值上界反而低估）会误剪最优解
- 最优性剪枝要用乐观上界而非实际可达值
- 剪枝顺序：先搜更有希望的分支能更快收紧 best
- 浮点估价的精度问题：优先用整数/有理数上界

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/search/heuristic/](https://oi-wiki.org/search/heuristic/)
- 书籍 ✓ `CPH ch5 p58 (Pruning the search)`
