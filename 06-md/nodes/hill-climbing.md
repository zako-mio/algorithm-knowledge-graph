---
id: hill-climbing
name: 爬山算法
group: G-E-5
stage: advanced
priority: P2
depth_tier: standard
---

# 爬山算法

> 局部择优启发式搜索，每次在当前最优解附近找更优解；易陷入局部最优，单峰函数有效

<!-- 元信息: id=hill-climbing · group=G-E-5 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

爬山算法（hill climbing）是一种局部择优的启发式搜索：在当前最优解 x 的邻域内生成候选解 x'，若 x' 比 x 更优则转移到 x'，否则保持 x。它是深度优先搜索的启发式改进，利用反馈信息（目标函数值）引导搜索。对单峰函数（只有一个峰）保证收敛到最优；对多峰函数极易陷入局部最优。竞赛中常用于无法写出精确解的毒瘤计算几何/数学题（如求球心、费马点），实现上通常引入温度参数——初始步长大，随迭代次数逐渐缩小（类比兔子醉酒爬山逐渐清醒），以便先粗后细地逼近最优。

## Why · 为什么

### 直觉 · Intuition

想象一只喝醉的兔子在山上跳：每次朝它认为更高的地方跳（往往只是不准确的趋势），可能一次跳到山顶，也可能跳过头翻过山脊。兔子逐渐清醒、跳跃幅度变小，最终落在某个山顶。温度参数就是'清醒程度'：温度高时跳得远（快速靠近目标区域），温度低时跳得近（精细收敛）。如果函数只有一座山（单峰），无论怎么跳最终都在山顶附近。

### 原理 · Principle

正确性（在单峰函数上）来自：只要邻域足够密、步长衰减足够慢，候选解序列沿函数值单调不减的方向移动，最终收敛到唯一峰顶。但收敛速度与步长衰减参数强相关：温度系数 d∈[0.985,0.999] 越接近 1 收敛越慢但越不易跳过头。在多峰函数上不保证最优，这是爬山与模拟退火/随机化的本质区别——爬山只接受更优解，永不接受劣解，因此被困在最近的局部最优。多次爬山（不同初始状态/参数）取全局最优可缓解。

### 历史 · History

爬山思想源自 1950s 人工只能的启发式搜索（Newell 与 Simon 的问题求解程序），是局部搜索/局部最优化的最早形式。1975 年后被遗传算法等元启发式继承。在竞赛界它因实现简单、在解析解难写的几何/计算问题中效果尚可而流行，OI-Wiki 的 hill-climbing 条目总结了经典应用（球形空间产生器、费马点）。

## How · 实现

### 伪代码

```python
def hill_climb(初始解 x0):
    x = x0
    T = 初始温度(大步长)          # 例如 10000
    d = 0.99                       # 降温系数 [0.985,0.999]
    while T > 终止阈值:
        x' = 在 x 附近随机生成候选  # 步长与 T 成正比
        if f(x') 更优:
            x = x'
        T = T * d
    return x
# 多次运行取全局最优
best = max(hill_climb(随机初始) for _ in range(k))
```

### Python 实现

```python
import math
import random


def hill_climb_sphere(points, iters=3000):
    """爬山求 n 维点集的重心/费马式最优点(示例: 最小化到各点距离平方和 => 重心).
    points: list of (x1,...,xn)
    返回最优点的坐标(近似). 用温度衰减缩小步长.
    """
    n_dim = len(points[0])
    # 初始解: 重心
    x = [sum(p[i] for p in points) / len(points) for i in range(n_dim)]

    def f(px):
        return sum((px[i] - p[i]) ** 2 for p in points for i in range(n_dim))

    T = 100.0
    while T > 1e-6:
        # 邻域: 每维加一个高斯/均匀扰动, 幅度与温度相关
        x2 = [x[i] + random.uniform(-1, 1) * T for i in range(n_dim)]
        if f(x2) < f(x):
            x = x2
        T *= 0.995
    return x


def hill_climb_unimodal():
    """单峰函数 f(x)=-(x-3.7)^2, 从远处出发应爬到 x≈3.7"""
    x = random.uniform(-50, 50)
    T = 50.0
    while T > 1e-4:
        x2 = x + random.uniform(-1, 1) * T
        if -(x2 - 3.7) ** 2 > -(x - 3.7) ** 2:
            x = x2
        T *= 0.995
    return x


if __name__ == "__main__":
    # 单峰验证
    random.seed(0)
    xs = [hill_climb_unimodal() for _ in range(50)]
    assert all(abs(v - 3.7) < 0.3 for v in xs), xs

    # 球心: 一个 n 维球面上的点集, 最小化到各点距离的平方差 => 重心近似
    # 构造: 单位球心 (1,2), 半径 3, 取 8 个点
    center = (1.0, 2.0)
    points = []
    for ang in range(8):
        a = ang * 3.14159 / 4
        points.append((center[0] + 3 * math.cos(a), center[1] + 3 * math.sin(a)))
    # 用欧氏距离平方和最小化 => 重心 (1,2)
    res = hill_climb_sphere(points)
    assert abs(res[0] - 1.0) < 0.5 and abs(res[1] - 2.0) < 0.5, res

    print("hill-climbing tests passed")

```

**PyPy 提示**: 爬山主要开销是大量次函数求值；纯 Python 下控制迭代次数（几千~几万次）即可。数学函数用 math 库；向量操作可向量化或减少重复计算。参数调优（初始温度/降温系数/终止阈值/邻域幅度）需要实际压测。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(迭代次数 × 单次函数求值)；迭代次数由温度参数决定（如 T0=10000, d=0.99 约 920 步），多次爬山再乘 k |
| 空间 | O(状态大小) |

### 局限

多峰函数不保证最优，易困局部最优；无法给出正确性证明，只能概率/实验验证；参数敏感需调参；对高维、非光滑、噪声函数效果差。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P4035 | 3 | 球形空间产生器：单峰函数，爬山求 n 维球心，初始重心+温度衰减 | [https://www.luogu.com.cn/problem/P4035](https://www.luogu.com.cn/problem/P4035) |
| Hydro | bzoj-P3680 | 3 | 吊打XXX：求带权费马点，爬山/模拟退火模板 | [https://hydro.ac/p/bzoj-P3680](https://hydro.ac/p/bzoj-P3680) |

## Pitfalls · 易错点

- 只接受更优解 => 必困局部最优，多峰问题慎用
- 温度系数太小收敛过快会停在半山腰；太大则来回震荡不收敛
- 单峰函数的判断（可三分/解析求解时优先精确解）
- 初始点选择对结果影响大，多随机初值取最优
- 步长与函数尺度不匹配（量级悬殊）时需归一化坐标

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/misc/hill-climbing/](https://oi-wiki.org/misc/hill-climbing/)
- Wikipedia ✓ [https://en.wikipedia.org/wiki/Hill_climbing](https://en.wikipedia.org/wiki/Hill_climbing)
