---
id: search-pruning
name: 搜索剪枝优化
group: G-A-14
stage: intermediate
priority: P1
depth_tier: standard
---

# 搜索剪枝优化

> 可行性剪枝/最优性剪枝/搜索顺序优化，减少搜索量

<!-- 元信息: id=search-pruning · group=G-A-14 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

搜索剪枝是减少 DFS 搜索量的系列技术。DFS 时间复杂度过高，直接爆搜常超时；剪枝通过提前判断子树的'前途'，在扩展前砍掉无望分支。三大类：①可行性剪枝——当前部分解已违反约束（超容量、无法到达），整棵子树非法；②最优性剪枝——当前代价已差于已得最优解（或乐观上界也追不上），继续搜无意义；③搜索顺序优化——先搜更有希望的分支，让最优解更早出现，间接提升剪枝效率。此外还有记忆化（相同状态只算一次）、等效性剪枝（对称/重复分支只搜一个）。

## Why · 为什么

### 直觉 · Intuition

剪枝像'识途的老马'：走岔路之前就闻出前面是死胡同（可行性），或者就算走到头也不会比现有最好成绩好（最优性），干脆掉头。先搜最有可能成功的路（顺序优化），能更早拿到好成绩，让最优性剪枝更有力。

### 原理 · Principle

DFS 框架中，可行性剪枝在循环内判断 cur+next 是否超约束；最优性剪枝在进入递归前比较 now 与当前最优 ans，若 now 已不可能优于 ans 则 return。顺序优化通过按代价/密度排序候选，使最优解尽快出现——这本质是利用'找到好下界越快，剪枝越多'。等效性剪枝（如相同长度木棍只尝试第一个未用的）避免重复探索对称分支。极端法剪枝：若最理想情况（乐观估计）都无法满足，则实际更不可能。

### 历史 · History

剪枝思想伴随回溯法出现（见 backtracking 节点），并在 0/1 背包分支限界（Land & Doig, 1960）、N皇后优化中得到系统化。OI Wiki 以工作分配问题（n≤15）与 P1120 小木棍为经典教学例，总结出'极端法/调整法/数学方法'三类剪枝思路。

## How · 实现

### 伪代码

```python
def dfs(状态, 当前代价 now):
    # 最优性剪枝
    if now 已差于/不可能优于 ans: return
    # 可行性剪枝
    if 违反约束: return
    if 到达目标: ans = min(ans, now); return
    for 候选 c in 按优化顺序排列的候选集:
        if 可行:
            标记; dfs(下一状态); 撤销
    # 等效性剪枝: 相同候选只试第一个

# 优化顺序: 按代价/密度/影响力降序
```

### Python 实现

```python
def stick_break(lengths, k):
    """小木棍问题: 能否把 lengths 分成 k 组, 每组和相同
    返回目标单根长度(存在解)或 -1
    集中演示: 从长到短排序 + 可行性/最优性/等效性剪枝
    """
    total = sum(lengths)
    if total % k != 0:
        return -1
    target = total // k
    lengths = sorted(lengths, reverse=True)  # 搜索顺序优化: 先长后短
    n = len(lengths)
    used = [False] * n

    def dfs(remaining_groups, cur_sum, start):
        if remaining_groups == 0:
            return True
        if cur_sum == target:
            return dfs(remaining_groups - 1, 0, 0)
        for i in range(start, n):
            if used[i]:
                continue
            if cur_sum + lengths[i] > target:
                continue  # 可行性剪枝
            if i > 0 and not used[i - 1] and lengths[i] == lengths[i - 1]:
                continue  # 等效性剪枝: 相同长度只试第一个
            used[i] = True
            if dfs(remaining_groups, cur_sum + lengths[i], i + 1):
                return True
            used[i] = False
            if cur_sum == 0:
                return False  # 最长未用都放不下, 无解
            if cur_sum + lengths[i] == target:
                return False  # 恰好拼满却失败, 无解
        return False

    return target if dfs(k, 0, 0) else -1


def assignment_min_time(cost, n):
    """工作分配问题: n个人n份工作, 求最小总时间
    cost[i][j] = 第i人做第j份工作的时间
    最优性剪枝: 当前总时间超过已有最优即返回
    """
    used = [False] * n
    best = [float('inf')]

    def dfs(person, cur):
        if cur >= best[0]:
            return  # 最优性剪枝
        if person == n:
            best[0] = min(best[0], cur)
            return
        for j in range(n):
            if not used[j]:
                used[j] = True
                dfs(person + 1, cur + cost[person][j])
                used[j] = False

    dfs(0, 0)
    return best[0]


if __name__ == "__main__":
    # 小木棍
    assert stick_break([5, 5, 5, 5], 4) == 5
    assert stick_break([3, 5, 2, 8, 1, 4], 1) == 23  # 一根全拼
    assert stick_break([7, 7, 3, 3, 10, 10], 2) == 20
    assert stick_break([1, 1, 1], 2) == -1

    # 工作分配
    cost = [[9, 2, 7, 8],
            [6, 4, 3, 7],
            [5, 8, 1, 8],
            [7, 6, 9, 4]]
    assert assignment_min_time(cost, 4) == 13

    # 随机对拍小木棍
    import random
    random.seed(3)
    def brute_ok(lengths, k):
        total = sum(lengths)
        if total % k != 0:
            return False
        target = total // k
        n = len(lengths)
        used = set()
        def rec(groups):
            if all(g == target for g in groups):
                return True
            idx = min(range(k), key=lambda i: groups[i])
            for i, x in enumerate(lengths):
                if i in used:
                    continue
                if groups[idx] + x <= target:
                    used.add(i)
                    groups[idx] += x
                    if rec(groups):
                        return True
                    groups[idx] -= x
                    used.discard(i)
            return False
        return rec([0] * k)

    for _ in range(300):
        n = random.randint(1, 8)
        lens = [random.randint(1, 8) for _ in range(n)]
        k = random.randint(1, 3)
        total = sum(lens)
        if total % k == 0 and brute_ok(lens, k):
            assert stick_break(lens, k) == total // k, (lens, k)
        else:
            assert stick_break(lens, k) == -1, (lens, k)
    print("search-pruning all tests passed (300 random checks)")

```

**PyPy 提示**: 剪枝搜索常用递归+全局最优，PyPy 注意 setrecursionlimit。剪枝顺序影响巨大：可行性剪枝最廉价先做，最优性剪枝次之；排序预处理（从大到小/密度降序）能显著加速。相同长度候选用等效性剪枝避免指数浪费。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 最坏仍指数级；良好剪枝下可达实际多项式/近线性，但无法理论保证 |
| 空间 | O(搜索深度 + 资源标记) |

### 局限

剪枝本质是经验优化，无法保证 worst-case 提升；剪枝条件写错可能漏解；问题规模太大(深度/分支大)时即使剪枝仍超时；记忆化需状态可哈希且无后效性。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1120 | 4 | 小木棍：可行性+最优性+等效性剪枝综合题，剪枝极致训练 | [https://www.luogu.com.cn/problem/P1120](https://www.luogu.com.cn/problem/P1120) |
| OI Wiki | opt-example | 3 | 工作分配问题：最优性剪枝入门（n≤15） | [https://oi-wiki.org/search/opt/](https://oi-wiki.org/search/opt/) |

## Pitfalls · 易错点

- 最优性剪枝需保证乐观上界，否则误剪最优解
- 等效性剪枝(相同候选跳过)需配合排序才能正确去重
- 剪枝顺序应先廉价后昂贵(可行性→最优性→等效性)
- 边界条件(到达目标)要在剪枝之后判断，避免漏解
- 递归撤销遗漏会导致状态污染

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/search/opt/](https://oi-wiki.org/search/opt/)
- 书籍 ✓ `CPH ch5 p57-58 (backtracking/pruning)`
