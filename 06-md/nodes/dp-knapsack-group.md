---
id: dp-knapsack-group
name: 分组背包
group: G-A-11
stage: intermediate
priority: P1
depth_tier: standard
---

# 分组背包

> 物品分组，每组最多选一件

<!-- 元信息: id=dp-knapsack-group · group=G-A-11 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

分组背包是0-1背包的变式：物品被分为若干组，每组最多只能选一件物品。状态转移从「在所有物品中选一件」变为「从当前组中选一件」——对每一组做一次0-1背包即可。核心是三层循环的顺序：组别→容量→组内物品。

## Why · 为什么

### 直觉 · Intuition

每组最多选一件意味着组内物品互斥。枚举组时，对每个容量j，从该组所有物品中选最优的一件放入（或不选），等价于一个组内的小型0-1背包。

### 原理 · Principle

状态转移：f(j)=max{f(j), f(j-w[g][i])+v[g][i]}，其中g为组号，i为组内物品编号。循环顺序：外层枚举组k，中层倒序枚举容量j（保证每组只选一件），内层枚举组内物品i。正确性：倒序枚举容量使得同一组内至多有一个物品被选中（因为f(j-w)仍来自上一组的状态）。

### 历史 · History

分组背包是四大背包模型之一（0-1、完全、多重、分组），常出现在有互斥选择的场景中（如主件-附件问题可转化为分组背包）。OI Wiki以P1757(通天之分组背包)为教学题。

## How · 实现

### 伪代码

```python
# groups[k] = [(w, v), ...] 第k组的物品列表
for k in 1..num_groups:
  for j in W down to 0:
    for (w, v) in groups[k]:
      if j >= w:
        f[j] = max(f[j], f[j-w] + v)
```

### Python 实现

```python
def group_knapsack(W, groups):
    """分组背包
    W: 背包容量
    groups: [[(w1,v1),(w2,v2),...], ...] 每组物品列表
    返回: 最大价值
    """
    f = [0] * (W + 1)
    for group in groups:
        for j in range(W, -1, -1):  # 倒序枚举容量
            for w, v in group:
                if j >= w and f[j - w] + v > f[j]:
                    f[j] = f[j - w] + v
    return f[W]


def group_knapsack_with_count(W, groups):
    """分组背包(带选择计数版本, 用于验证)"""
    f = [0] * (W + 1)
    chosen = [[] for _ in range(W + 1)]
    for gi, group in enumerate(groups):
        new_f = f[:]  # 复制, 确保每组只选一件
        new_chosen = [c[:] for c in chosen]
        for j in range(W, -1, -1):
            for idx, (w, v) in enumerate(group):
                if j >= w and f[j - w] + v > new_f[j]:
                    new_f[j] = f[j - w] + v
                    new_chosen[j] = chosen[j - w] + [(gi, idx)]
        f = new_f
        chosen = new_chosen
    return f[W], chosen[W]


if __name__ == "__main__":
    # 测试: 容量10, 3组物品
    # 组1: (w=3,v=4),(w=4,v=5) -> 选w=3,v=4 或 w=4,v=5
    # 组2: (w=2,v=3),(w=5,v=6) -> 选w=5,v=6
    # 组3: (w=1,v=1) -> 选w=1,v=1
    W = 10
    groups = [
        [(3, 4), (4, 5)],
        [(2, 3), (5, 6)],
        [(1, 1)]
    ]
    ans = group_knapsack(W, groups)
    # 最优: 组1选(4,5)=5, 组2选(5,6)=6, 组3不选(容量=9不够10) 或组3选(1,1)
    # 4+5+1=10, 价值5+6+1=12
    assert ans == 12, f"Expected 12, got {ans}"

    # 验证每组只选一件
    _, chosen = group_knapsack_with_count(W, groups)
    group_ids = [g for g, _ in chosen]
    assert len(group_ids) == len(set(group_ids)), "每组应最多选一件"

    # 边界
    assert group_knapsack(0, [[(1, 1)]]) == 0
    assert group_knapsack(1, [[(1, 5)]]) == 5

    print("All tests passed.")

```

**PyPy 提示**: PyPy对三层循环优化好，组数*W*平均组大小=1e7时约0.5s。注意内层物品循环不要倒序(容量倒序即可)。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(W * sum of group sizes) = O(W * n) 其中n为总物品数 |
| 空间 | O(W) — 一维滚动数组 |

### 局限

三层循环在W大(>1e5)且组数多时Python可能TLE。主件-附件问题可转化为分组背包但需先分析依赖结构。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1757 | 2 | 通天之分组背包：分组背包模板题 | [https://www.luogu.com.cn/problem/P1757](https://www.luogu.com.cn/problem/P1757) |
| Luogu | P1064 | 3 | 金明的预算方案：主件-附件问题转化为分组背包 | [https://www.luogu.com.cn/problem/P1064](https://www.luogu.com.cn/problem/P1064) |

## Pitfalls · 易错点

- 循环顺序错误：必须 组→容量(倒序)→组内物品，容量倒序保证每组只选一件
- 组内物品循环不需倒序（因为容量已倒序，同一物品不会被重复取）
- 空组或组内物品重量全超W时应跳过
- 主件-附件问题中不买主件也是一种选择，需加入虚拟选项

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/dp/knapsack/](https://oi-wiki.org/dp/knapsack/)
- CP-Algorithms ✓ [https://cp-algorithms.com/dynamic_programming/knapsack.html](https://cp-algorithms.com/dynamic_programming/knapsack.html)
