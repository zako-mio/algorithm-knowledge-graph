---
id: simulated-annealing
name: 模拟退火
group: G-E-5
stage: advanced
priority: P2
depth_tier: standard
---

# 模拟退火

> 以概率e^(-ΔE/T)接受劣解跳出局部最优；初始温度/降温系数/终止温度三参数；卡时技巧clock()；Metropolis准则

<!-- 元信息: id=simulated-annealing · group=G-E-5 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

模拟退火（Simulated Annealing, SA）是一种随机化元启发式优化算法，灵感来自金属退火：将金属缓慢加热再以适宜速度冷却以消除内应力。算法把目标函数视为'能量函数'E，从一个随机状态出发，每一步在邻域随机生成新状态；新状态更优则无条件接受；更差则以概率 e^(-ΔE/T) 接受（Metropolis 准则），其中 ΔE 是能量差（≥0），T 是当前温度。温度初始为较大值 T0，每步乘以降温系数 d（略小于 1），直到低于终止温度 Tk。因能以一定概率接受劣解，SA 可以跳出局部最优，在'方案数量极大甚至无穷且非单峰'的问题中非常有效。最终答案通常取整个过程中遇到的最优状态，而非结束时状态。

## Why · 为什么

### 直觉 · Intuition

爬山算法的问题是面对非最优解直接丢弃，因此困在局部最优。退火的思想是'高温时允许乱跳'：温度高时接受劣解的概率 e^(-ΔE/T) 大，系统能翻过能量壁垒到达别处的山；随着温度降低，接受劣解概率变小，最终在某个低处'结晶'。这模拟了金属降温时原子逐渐有序化的过程。直观看：T 大 → 贪心弱、探索强；T 小 → 贪心强、收敛快。

### 原理 · Principle

Metropolis 准则：新状态能量 E_next 比当前 E 差 ΔE=E_next−E 时，以概率 exp(−ΔE/T) 接受，对应 Boltzmann/Gibbs 分布；ΔE 越小或 T 越大接受概率越高。理论（Kirkpatrick 1983；统计力学中退火调度）保证：在'温度下降足够慢'的理想条件下，系统以概率 1 收敛到全局最优（等价于模拟退火到 Gibbs 分布的样本）。竞赛中无法满足无限慢降温，故为启发式，正确率靠调参与卡时保证。算法状态：维护 s_best（全程最优）与 E_best。参数：T0（初始温度，大）、d（降温系数，常取 0.985~0.999）、Tk（终止温度，接近 0）；迭代次数 ≈ log_{1/d}(T0/Tk)。

### 历史 · History

模拟退火由 S. Kirkpatrick、C. D. Gelatt 与 M. P. Vecchi 于 1983 年发表于《Science》，以及稍早的 Černý（1985）独立提出，是组合优化中最重要的元启发式之一。其数学基础来自统计力学（Metropolis 算法，1953）。在 ICPC/CCPC 中成为处理几何/调参题、难写精确解的题目（费马点、TSP 近似、参数拟合）的标准随机化手段，OI-Wiki 与 CP-Algorithms 均有专门条目。

## How · 实现

### 伪代码

```python
# 通用 SA 框架 (求最小化 E)
T = T0; u = 0.99; Tk = 1e-4
s = 随机初始状态; E = E(s)
s_best, E_best = s, E
while T > Tk:
    s_next = 在 s 邻域随机生成
    E_next = E(s_next)
    if E_next < E 或 random() < exp(-(E_next-E)/T):
        s, E = s_next, E_next
        if E < E_best: s_best, E_best = s, E
    T *= u
return s_best, E_best
```

### Python 实现

```python
import math
import random


class SA:
    """通用模拟退火框架: 最小化 energy 函数.
    用户需实现: initial_state(), neighbor(s), energy(s)
    """

    def __init__(self, initial_state, energy, neighbor,
                 T0=1000.0, u=0.999, Tk=1e-6):
        self.energy = energy
        self.neighbor = neighbor
        self.T0, self.u, self.Tk = T0, u, Tk

    def run(self, state):
        E = self.energy(state)
        best_s, best_E = state, E
        T = self.T0
        while T > self.Tk:
            nxt = self.neighbor(state)
            nE = self.energy(nxt)
            dE = nE - E
            if dE < 0 or random.random() < math.exp(-dE / T):
                state, E = nxt, nE
                if E < best_E:
                    best_s, best_E = state, E
            T *= self.u
        return best_s, best_E


def tsp_sa(cities, iters=None):
    """TSP 近似解: 状态=访问顺序, 邻域=交换两个城市位置.
    返回 (best_tour, best_dist)
    """
    n = len(cities)

    def dist(i, j):
        return math.hypot(cities[i][0] - cities[j][0], cities[i][1] - cities[j][1])

    tour = list(range(n))
    random.shuffle(tour)

    def energy(t):
        return sum(dist(t[i], t[(i + 1) % n]) for i in range(n))

    def neighbor(t):
        nt = t[:]
        a, b = random.sample(range(n), 2)
        nt[a], nt[b] = nt[b], nt[a]
        return nt

    sa = SA(tour, energy, neighbor, T0=100, u=0.999, Tk=1e-3)
    best_t, best_d = sa.run(tour)
    return best_t, best_d


if __name__ == "__main__":
    random.seed(1)

    # 1) 单峰二次函数: 应逼近全局最小点 x*=2
    def e1(x):
        return (x - 2.0) ** 2

    sa = SA(50.0, e1, lambda x: x + random.uniform(-3, 3), T0=30, u=0.99, Tk=1e-3)
    s, E = sa.run(50.0)
    assert abs(s - 2.0) < 0.05, s

    # 2) 有局部最优的震荡函数: f(x)=sin(x) + 0.1x, 区间 [0,20]
    # 期望 SA 能找到接近全局最优的点(约 1.57 附近 sin 最大)
    def e2(x):
        return -(math.sin(x) + 0.1 * x)

    sa2 = SA(3.0, e2, lambda x: min(20, max(0, x + random.uniform(-2, 2))),
             T0=10, u=0.995, Tk=1e-3)
    s2, _ = sa2.run(3.0)
    # 全局最大在 x≈1.57 (sin峰) 或接近 20 处; 允许 SA 找到任一峰(近似)
    # 这里用多次运行确保找到 sin 主峰
    best = None
    for _ in range(30):
        r, _ = SA(5.0, e2, lambda x: min(20, max(0, x + random.uniform(-2, 2))),
                  T0=10, u=0.995, Tk=1e-3).run(5.0)
        val = -(e2(r))
        if best is None or val > best:
            best = val
    assert best > 0.95, best  # sin 主峰值约 1.157

    # 3) TSP 小实例: 正方形四顶点, 最优=周长 4
    cities = [(0, 0), (1, 0), (1, 1), (0, 1)]
    best_t, best_d = tsp_sa(cities)
    assert best_d < 4.01, best_d  # 应收敛到正方形周长 4

    print("simulated-annealing tests passed")

```

**PyPy 提示**: SA 是'卡时'算法：主循环用 while 时钟 < 时限 反复跑多轮取最优（如 while time() < 0.9*limit: run()）。PyPy 下大量浮点 exp/random 调用注意用 math.exp 与 random 模块即可，若要更快要换成 C++。参数：T0 取目标函数量级、u 越接近 1 越精确但越慢；分块模拟退火（把值域分多段各跑一遍取最优）可处理多峰。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(迭代次数 × 单次能量计算)，迭代次数 ≈ log_{1/u}(T0/Tk)，竞赛常用卡时控制；可分块/多轮 |
| 空间 | O(状态大小) |

### 局限

启发式，无严格正确率保证（理论收敛需无限慢降温）；对邻域设计敏感（bad neighbor 生成则效率低）；参数多（T0/u/Tk/轮数）需调；高维连续问题效果波动；结果需大量随机验证（跑多轮取最优）才可信。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1337 | 3 | 平衡点/吊打XXX：带权费马点，SA 模板题，能量=加权距离和 | [https://www.luogu.com.cn/problem/P1337](https://www.luogu.com.cn/problem/P1337) |
| Luogu | P2503 | 4 | HAOI2006 均分数据：把数据分组使各组和的方差最小，SA/分块 | [https://www.luogu.com.cn/problem/P2503](https://www.luogu.com.cn/problem/P2503) |
| Luogu | P4035 | 3 | 球形空间产生器：与爬山通用，也可用 SA 解（单峰） | [https://www.luogu.com.cn/problem/P4035](https://www.luogu.com.cn/problem/P4035) |

## Pitfalls · 易错点

- Metropolis 接受概率用错符号（ΔE 取负）会反向接受
- ΔE 未取非负值 / T 为 0 时 exp 除零崩溃
- 答案应取全程最优 best_s 而非最终状态
- u 太大(≈1)收敛极慢易 TLE；太小退火不充分仍困局部最优
- 不卡时、不跑多轮，单次运行结果不可靠

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/misc/simulated-annealing/](https://oi-wiki.org/misc/simulated-annealing/)
- CP-Algorithms ✓ [https://cp-algorithms.com/num_methods/simulated_annealing.html](https://cp-algorithms.com/num_methods/simulated_annealing.html)
- Wikipedia ✓ [https://en.wikipedia.org/wiki/Simulated_annealing](https://en.wikipedia.org/wiki/Simulated_annealing)
