---
id: random-technique
name: 随机化技巧
group: G-E-5
stage: intermediate
priority: P1
depth_tier: standard
---

# 随机化技巧

> 随机覆盖目标元素/随机命中目标集合/随机打乱消除最坏情况，概率上界分析

<!-- 元信息: id=random-technique · group=G-E-5 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

随机化技巧（randomized techniques）是利用随机性把算法从'最坏情况'拉到'高概率高效'的一类方法总称。常见模式：(1) 用随机集合覆盖目标元素——重复多次随机撒网，只要一次命中目标解即成功，如随机染色配 2-SAT、随机选边配贪心；(2) 用随机元素命中目标集合——随机选元素期望命中目标集合中的元素，配合重复控制失败率；(3) 随机化输入顺序消除构造数据的最坏情况——如随机增量法（最小圆覆盖）、随机化快排/哈希 base；(4) 随机化用于哈希（随机权值集合哈希、随机模数/基数防卡）。核心是概率分析：重复 k 次后失败率 ≤ (1-p)^k，令其 ≤ ε 得 k = -logε / p。

## Why · 为什么

### 直觉 · Intuition

很多问题的难点在于'不知道哪一个是关键对象'（关键元素/关键边/目标解）。既然无法确定，就随机猜：每次猜中的概率为 p，重复几次后'全没猜中'的概率指数下降，从而以极高概率成功。另一种直觉是'把输入搅乱'：很多构造数据针对的是固定顺序/固定哈希，随机化后最坏输入出现的概率极低，期望复杂度就是平均复杂度。

### 原理 · Principle

概率上界分析是硬核：若单次成功概率 p>0，独立重复 k 次则失败率 ≤ (1-p)^k，故 k = O(log(1/ε)/p) 次保证 1-ε 正确率。技巧在于构造'成功事件'使其概率不太小（如 1/2、1/4 常数级），这样重复次数就是 O(log) 级。随机化哈希的合理性来自：一个固定的集合哈希值在 {0,1}^64 上服从均匀分布（独立随机变量的异或和仍均匀），因此对特定输入出错的概率是 2^-64 量级。注意：随机化算法的正确率是'对所有输入都能以高概率正确'，而非'随机数据上的正确'——这是它与普通启发式的本质区别。

### 历史 · History

随机化算法思想萌芽于 1970s（Rabin 的素性测试、Solovay–Strassen 的随机素性判定），1976 年 Rabin-Miller、1987 年 Adleman 等推动随机化在算法设计中的正式地位；Karp 与 Luby 等奠定了随机化算法的复杂度理论（RP/BPP 类）。在竞赛中，随机增量法（最小圆覆盖，1975 由 Preparata 与 Shamos 的框架内成熟）、随机化快速排序、随机哈希防卡成为标准武器，OI-Wiki 的 rand-technique 一节系统总结了竞赛视角的分类。

## How · 实现

### 伪代码

```python
# 通用模式: 随机覆盖目标
repeat k 次:
    s = 随机生成的候选(撒网)
    if s 命中目标解:
        输出 s, 成功退出
输出失败 (概率 <= epsilon)

# k 的选取: 单次成功概率 p => k = ceil(-log(eps)/p)
# 通常取 p 尽量大的常数, 使 k = O(log n)

# 随机增量法(最小圆覆盖)骨架:
pts = 随机打乱的输入点
C = 初始圆(前两点)
for p in pts:
    if p 不在 C 内:
        C = 经过 p 的最小圆 (递归调用, 增量式)

```

### Python 实现

```python
import random


def random_cover_test():
    """演示'随机覆盖目标'模式: 在 0..N-1 中有一个隐藏的目标元素 x,
    每次等概率随机猜一个, 猜中即成功. 返回猜中所需的期望轮数近似."""
    N = 1000
    target = random.randrange(N)
    rounds = 0
    while True:
        rounds += 1
        if random.randrange(N) == target:
            return rounds


def k_for_epsilon(p, eps):
    """给定单次成功概率 p, 需要重复多少次保证失败率 <= eps"""
    import math
    return math.ceil(math.log(eps) / math.log(1 - p))


def min_circle_rand(points):
    """随机增量法求最小圆覆盖: O(n) 期望.
    points: (x,y) 列表, 返回 (cx, cy, r^2)
    """
    import random as rnd
    pts = list(points)
    rnd.shuffle(pts)

    def circle_from_3(a, b, c):
        (x1, y1), (x2, y2), (x3, y3) = a, b, c
        d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
        if abs(d) < 1e-12:
            return None
        ux = ((x1 * x1 + y1 * y1) * (y2 - y3) + (x2 * x2 + y2 * y2) * (y3 - y1) + (x3 * x3 + y3 * y3) * (y1 - y2)) / d
        uy = ((x1 * x1 + y1 * y1) * (x3 - x2) + (x2 * x2 + y2 * y2) * (x1 - x3) + (x3 * x3 + y3 * y3) * (x2 - x1)) / d
        r2 = (ux - x1) ** 2 + (uy - y1) ** 2
        return (ux, uy, r2)

    def circle_2(a, b):
        (x1, y1), (x2, y2) = a, b
        return ((x1 + x2) / 2, (y1 + y2) / 2, ((x1 - x2) ** 2 + (y1 - y2) ** 2) / 4)

    def in_circle(p, c):
        if c is None:
            return False
        cx, cy, r2 = c
        return (p[0] - cx) ** 2 + (p[1] - cy) ** 2 <= r2 + 1e-9

    n = len(pts)
    if n == 0:
        return (0, 0, 0)
    c = None
    # 增量: 外层维护圆, 内部维护'圆过当前点'的圆
    for i in range(n):
        if not in_circle(pts[i], c):
            c = circle_2(pts[0], pts[i]) if False else None
            # 圆过 pts[i]: 再扫前面
            c = (pts[i][0], pts[i][1], 0.0)
            for j in range(i):
                if not in_circle(pts[j], c):
                    c = circle_2(pts[i], pts[j])
                    for k in range(j):
                        if not in_circle(pts[k], c):
                            c3 = circle_from_3(pts[i], pts[j], pts[k])
                            if c3 is not None:
                                c = c3
    return c


if __name__ == "__main__":
    # 期望轮数验证: 单次 1/1000, 期望 1000 轮
    trials = 2000
    total = 0
    for _ in range(trials):
        total += random_cover_test()
    avg = total / trials
    assert 700 < avg < 1300, avg

    # 重复次数: 单次 p=1/2, 要 1e-6 失败率 => 约 20 次
    k = k_for_epsilon(0.5, 1e-6)
    assert 18 <= k <= 21, k

    # 最小圆覆盖: 3 个点共线/三角形
    pts = [(0, 0), (1, 0), (0.5, 0.5)]
    c = min_circle_rand(pts)
    # 三点外接圆
    assert abs(c[0] - 0.5) < 1e-6 and abs(c[1] - 0.0) < 1e-6

    # 大点集: 圆内所有点
    import random as rnd
    rnd.seed(42)
    pts2 = []
    for _ in range(300):
        ang = rnd.random() * 6.28318
        pts2.append((0.5 + 0.4 * ang, 0.5 + 0.4 * ang))  # 沿直线(共线)退化
    c2 = min_circle_rand(pts2)
    for p in pts2:
        assert (p[0] - c2[0]) ** 2 + (p[1] - c2[1]) ** 2 <= c2[2] + 1e-6, p

    print("random-technique tests passed")

```

**PyPy 提示**: random 模块在 PyPy 下与 CPython 行为一致但更快。竞赛中随机化常用 time 或随机种子初始化；若需可复现，固定 seed。注意 Python 的 random.shuffle 是就地 O(n)，随机增量法在纯 Python 下 O(n) 期望但常数来自浮点运算，点集 1e5 量级仍可行。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 各模式不同：随机覆盖/命中 O(重复次数 × 单次判定)；随机增量法 O(n) 期望（因打乱后外层点被圆外点约束概率小）；重复次数一般为 O(log(1/ε)/p) |
| 空间 | 通常 O(n) |

### 局限

是概率算法：以极小概率出错（一般可接受）；重复次数与时间预算需平衡；某些问题即使随机也无法构造高概率事件（p 太小）；在正式 OI 中随机化方案需要自造大随机数据压测调参。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1742 | 3 | 最小圆覆盖：随机增量法，O(n) 期望复杂度，随机化消除最坏情况 | [https://www.luogu.com.cn/problem/P1742](https://www.luogu.com.cn/problem/P1742) |
| UOJ | 207 | 5 | 共价大爷游长沙：随机权值哈希 + LCT 维护边必经判定 | [https://uoj.ac/problem/207](https://uoj.ac/problem/207) |
| CSES | 1685 | 4 | New Flight Routes：随机选汇源点对贪心连边构造强连通方案 | [https://cses.fi/problemset/task/1685](https://cses.fi/problemset/task/1685) |

## Pitfalls · 易错点

- 随机化≠启发式：必须能给出失败概率上界，否则不叫随机化算法
- 重复次数不足导致正确率过低；k=-logε/p 要算对
- 种子固定/不随机化（如 srand 忘调用）会让随机算法退化为确定算法且可被构造数据攻击
- 随机增量法必须先 shuffle，否则仍保留最坏情况 O(n^2)
- 随机哈希值域小（如 mod 1e9+7 单哈希）碰撞率在大量比较时不可忽略，用 2^64/双模

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/misc/rand-technique/](https://oi-wiki.org/misc/rand-technique/)
- OI Wiki ✓ [https://oi-wiki.org/geometry/random-incremental/](https://oi-wiki.org/geometry/random-incremental/)
- 书籍 ✓ `CLRS ch5 (随机化算法与概率分析), CPH 附录`
