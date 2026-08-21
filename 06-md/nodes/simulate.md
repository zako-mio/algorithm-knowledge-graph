---
id: simulate
name: 模拟
group: G-A-1
stage: basic
priority: P0
depth_tier: deep
---

# 模拟

> 按题意直接模拟过程，考察代码实现能力

<!-- 元信息: id=simulate · group=G-A-1 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

模拟（Simulation）是用计算机忠实再现题目描述的操作流程：把题面中文字描述的规则翻译为程序逻辑，逐条执行，最终得到答案。它不依赖高深算法，主要考察读题准确性、状态建模与代码实现能力。模拟题通常码量大、操作多、逻辑分支繁杂，是最容易出现低级 bug 的题型。

## Why · 为什么

### 直觉 · Intuition

模拟的本质是「照做」：题目描述了某个世界如何运转（虫爬井、机器人走迷宫、扑克洗牌），你只需要忠实地把这个流程一步步翻译成代码。难点不在想算法，而在「不把题意理解错」和「把复杂流程写得不乱」。

### 原理 · Principle

核心方法论：(1) 把题面中的每条规则抽象成状态与状态转移（当前状态用什么变量表示、一步操作改变哪些状态）；(2) 复杂规则统一化——例如时间统一换算成秒、方向统一用数字编号、坐标统一按 1 开始索引，减少概念混淆；(3) 按函数/结构体模块化拆分流程，便于单步调试；(4) 关注边界条件（越界、循环终止条件、恰好完成 vs 超出的判定）。

### 历史 · History

模拟是最古老的问题解决方式之一，从最初级的信息学入门题到 NOIP/NOI 的高分题（如「猪国杀」）都以模拟为骨架。OI Wiki 将模拟列为基础算法的首要内容，并总结出「先写流程图再写代码、模块化、统一转化概念、分块调试」四条实战经验。

## How · 实现

### 伪代码

```python
simulate():
  init state          # 按题意初始化所有变量
  while not done:     # 循环直到满足终止条件
    op = read_next()  # 读取下一步操作
    apply(op, state)  # 按规则更新状态
    check_done()      # 检查是否达到目标
  output(state)       # 输出答案
```

### Python 实现

```python
import sys

def climbing_worm(n, u, d):
    """OI Wiki 例题：蠕虫爬井。
    井深 n，每次爬 u 英寸，休息时下滑 d 英寸，问爬出井口最少爬几次。
    注意：若某次爬完刚好到顶也算成功。
    """
    pos = 0
    cnt = 0
    while True:
        cnt += 1
        pos += u
        if pos >= n:
            break
        pos -= d
    return cnt


def stone_scissors_cloth(a, b, turns):
    """NOIP2014 生活大爆炸版石头剪刀布（简化）:
    a 出拳序列, b 出拳序列, 循环出 turns 局, 返回 (a胜数, b胜数)。
    0=石头 1=剪刀 2=布。
    """
    win = [[0, 1, 2], [2, 0, 1], [1, 2, 0]]  # win[x][y]=1 表示 x 赢 y
    sa = sb = 0
    la, lb = len(a), len(b)
    for i in range(turns):
        x, y = a[i % la], b[i % lb]
        if win[x][y] == 1:
            sa += 1
        elif win[x][y] == 2:
            sb += 1
    return sa, sb


if __name__ == "__main__":
    assert climbing_worm(6, 3, 1) == 3, climbing_worm(6, 3, 1)
    assert climbing_worm(10, 2, 1) == 9, climbing_worm(10, 2, 1)

    sa, sb = stone_scissors_cloth([0], [1], 5)
    assert (sa, sb) == (5, 0), (sa, sb)
    sa, sb = stone_scissors_cloth([0, 1], [1, 0], 4)
    assert (sa, sb) == (2, 2), (sa, sb)

    print("All tests passed.")
```

**PyPy 提示**: PyPy 与 CPython 在模拟题上差别不大，瓶颈主要在代码逻辑而非解释器。复杂模拟（如多对象状态）注意用类或字典组织状态，避免散落全局变量。循环体内避免低效操作（如大量 list.pop(0)）。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 取决于模拟步数：一次操作 O(1) 时总 O(总操作数)；需反复遍历对象的模拟可能 O(N×M) |
| 空间 | O(状态规模) — 通常为常数级或 O(N) |

### 局限

模拟没有通用套路，每次都要根据具体题面建模；状态复杂时易漏边界条件。若操作数极大（10^18 级）则纯模拟不可行，需寻找周期/数学规律（此时转向数学推导或倍增）。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Kattis | climbingworm | 1 | OI Wiki 官方例题：蠕虫爬井，最简单直白的循环模拟，注意恰好到顶也算成功 | [https://open.kattis.com/problems/climbingworm](https://open.kattis.com/problems/climbingworm) |
| UOJ | UOJ#15 | 4 | NOIP2014 生活大爆炸版石头剪刀布：按约定规则模拟多局博弈，考察状态打表与取模循环 | [https://uoj.ac/problem/15](https://uoj.ac/problem/15) |
| LibreOJ | LOJ#2885 | 8 | SDOI2010 猪国杀：大型复杂模拟题，状态繁多，是检验模块化与分块调试能力的经典题 | [https://loj.ac/problem/2885](https://loj.ac/problem/2885) |

## Pitfalls · 易错点

- 读题不全/漏条件，导致模拟规则与题面不符——动手前先把所有规则列成清单
- 循环终止条件错误：『恰好到达 vs 超过』『循环节 vs 一次性』判断不清
- 下标/坐标从 1 还是 0 开始混乱，导致 off-by-one
- 时间、方向等量未统一单位/编号，导致概念混淆（应抽取成统一格式）
- 一次性把整段逻辑写出来，出错后难以定位——应模块化并分块调试

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/basic/simulate/](https://oi-wiki.org/basic/simulate/)
- kattis ✓ [https://open.kattis.com/problems/climbingworm](https://open.kattis.com/problems/climbingworm)
