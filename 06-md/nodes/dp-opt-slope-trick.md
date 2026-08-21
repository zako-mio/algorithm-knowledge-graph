---
id: dp-opt-slope-trick
name: Slope Trick
group: G-A-12
stage: advanced
priority: P2
depth_tier: standard
---

# Slope Trick

> 维护凸函数的斜率/拐点序列，简化凸DP转移

<!-- 元信息: id=dp-opt-slope-trick · group=G-A-12 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

Slope Trick 是一种针对一维凸函数 DP 的优化技术：当 DP 中每一层的状态函数 f_i(x) 关于 x 是凸函数时，不直接维护 f_i 本身，而是维护其斜率序列（差分 Δf(x)=f(x+1)-f(x)）的变化。由于凸函数斜率单调，只需记录斜率发生变化的拐点位置（通常用堆/双堆维护），就能在 O(log n) 或 O(1) 完成每层转移。适用于 min/max 卷积、加 |x-a| 型凸函数、前后缀最小化、平移截取等变换，典型应用如 P4331(数字序列)、CF865D(股票)、USACO Landscaping。

## Why · 为什么

### 直觉 · Intuition

凸函数像一条斜率单调不减的折线，整条函数信息完全由'拐点'决定。多数 DP 变换（加绝对值、取 min、平移、夹断）只让折线斜率的某些段 +1/-1 或在某处插入/删除拐点，斜率序列变化极少。于是维护一组有序拐点（最大堆+最小堆的'双堆'结构）即可表示整条函数，转移变成堆操作。

### 原理 · Principle

令 f_i(x) 表示第 i 层的凸函数，维护其斜率变化集合 S={x_1<=x_2<=...}（斜率在 x_k 处 +1）。三种核心变换：(1) 加 |x-a| 等价于在 a 处插入拐点；(2) 前缀最小化 g(x)=min_{y<=x} f(y) 等价于删掉正斜率段（右堆全部并入左堆）；(3) 平移 f(x-c) 等价于左右堆整体加减。最小值位置在左右堆顶之间，最小值=f(min 处)。若函数是凹函数（最大化），把堆反转。

### 历史 · History

Slope Trick 由 xudyh 在 2016 年前后推广到 OI/ACM 社区，常出现在 Codeforces（如 CF 1209H）与 AtCoder 高难段。OI Wiki 的 dp/opt/slope-trick 页面系统整理了凸函数变换与双堆维护，USACO Guide 亦收录。其数学根源是凸分析中的次梯度与共轭思想。

## How · 实现

### 伪代码

```python
# 求弱增序列 b 使 sum|a_i-b_i| 最小 (核心模型)
# f(x) = 已选前缀使 b_last<=x 的最小代价, 凸函数用斜率堆维护
# 每步加入 a_i: 左堆(存负值)为斜率<=0 部分拐点, 右堆为斜率>=0 部分拐点
l = MaxHeap()   # 斜率从 0 降到 -1 的拐点(存负值以用最小堆实现)
r = MinHeap()   # 斜率从 0 升到 +1 的拐点
cost = 0
for a_i in A:
    # 加 |x-a_i|: 双堆各插入 a_i
    l.push(a_i); r.push(a_i)
    # 前缀最小化: 把右堆顶移到左堆
    if l.top > r.top:
        cost += l.pop - r.top      # 更新代价
        l.push(r.pop)
    # 若维护的是严格递增版 b_i-b_{i-1}>=1: 先做 b_i'=b_i-i 转弱增
return cost
```

### Python 实现

```python
import heapq, random


def min_cost_nondecreasing(a):
    """Slope Trick: 求非递减序列 b, 最小化 sum|a_i - b_i| (弱增版).
    用最大堆维护拐点, 返回最小代价。"""
    heap = []  # 最大堆(存负数)
    cost = 0
    for x in a:
        heapq.heappush(heap, -x)
        heapq.heappush(heap, -x)
        mx = -heapq.heappop(heap)
        cost += mx - x
    return cost


def brute_nondecreasing(a):
    """暴力枚举(仅小数据对拍): b 非递减, b_i 在 [min(a), max(a)] 取整数值。"""
    n = len(a)
    lo, hi = min(a), max(a)

    def rec(i, last):
        if i == n:
            return 0
        best = float("inf")
        for v in range(last, hi + 1):
            best = min(best, abs(a[i] - v) + rec(i + 1, v))
        return best

    return rec(0, lo)


if __name__ == "__main__":
    # 与暴力对拍(小数据)
    for _ in range(300):
        n = random.randint(1, 6)
        a = [random.randint(-6, 6) for _ in range(n)]
        c1 = min_cost_nondecreasing(a)
        c2 = brute_nondecreasing(a)
        assert c1 == c2, (a, c1, c2)
    # 手工样例
    assert min_cost_nondecreasing([2, 1]) == 1
    assert min_cost_nondecreasing([3, 2, 1]) == 2
    assert min_cost_nondecreasing([1, 2, 3]) == 0
    # BalticOI2004 Sequence(P4331) 严格递增版: b'_i = b_i - i 转弱增
    a = [6, 9, 12, 14]
    a2 = [x - i for i, x in enumerate(a)]  # 严格递增->弱增
    print("严格递增样例(P4331思想) min cost =", min_cost_nondecreasing(a2))
    print("slope_trick tests passed")

```

**PyPy 提示**: Python 用 heapq 的负数技巧实现最大堆即可，O(n log n) 对 1e5 可过（PyPy 更快）。若要还原具体最优序列 b_i，需额外记录；通常竞赛题只问最小代价。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n log n) 每个元素两次堆插入一次弹出；若斜率值域小可用计数/链表优化到 O(n) |
| 空间 | O(n) |

### 局限

前提是状态函数必须凸/凹，非凸不可直接用；题目往往需要先证明凸性（用四边形不等式或交换论证）。拐点类型（整数斜率段 vs 连续）不同维护方式不同。严格递增约束要先减下标转弱增。P4331 需要输出方案时还要求从堆中重建序列，比只求代价复杂。Python 在 1e6 级需注意 heapq 常数。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P4331 | 4 | BalticOI2004 Sequence: 严格递增序列距 a_i 最小, 先转弱增再 slope trick | [https://www.luogu.com.cn/problem/P4331](https://www.luogu.com.cn/problem/P4331) |
| Codeforces | 865D | 4 | Buy Low Sell High: 股票买卖最大利润, 凹函数双堆维护 | [https://codeforces.com/problemset/problem/865/D](https://codeforces.com/problemset/problem/865/D) |
| AtCoder | ARC123 D | 4 | 凹凸性质转换+双堆, 经典 slope trick 练习 | [https://atcoder.jp/contests/arc123/tasks/arc123_d](https://atcoder.jp/contests/arc123/tasks/arc123_d) |

## Pitfalls · 易错点

- 忘记先把严格递增转成弱增(减下标)会直接判错
- 最大堆用负数实现时, top 比较要取负号
- 前缀最小化时注意方向: 维护斜率<=0 部分要用最大堆, 搞反堆类型会错
- 未证明凸性就套用, 非凸情况结果错误
- 凹函数(最大化)时堆的取相反数处理易漏

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/dp/opt/slope-trick/](https://oi-wiki.org/dp/opt/slope-trick/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/dp/opt/slope-trick.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/dp/opt/slope-trick.md)
- web ✓ [https://usaco.guide/adv/slope-trick](https://usaco.guide/adv/slope-trick)
