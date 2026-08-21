---
id: frac-programming
name: 分数规划/01分数规划
group: G-E-7
stage: advanced
priority: P1
depth_tier: standard
---

# 分数规划/01分数规划

> 求Σa/Σb极值：二分答案→Σw_i(a_i-mid·b_i)≥0判定；Dinkelbach迭代法

<!-- 元信息: id=frac-programming · group=G-E-7 · stage=advanced · priority=P1 · depth_tier=standard -->

## What · 是什么

分数规划(Fractional Programming)用于求分式 Σ(a_i·w_i)/Σ(b_i·w_i) 的极值，其中 w_i∈{0,1} 表示选/不选第 i 个物品。核心方法：二分答案 mid，将分式判定转化为 Σw_i(a_i-mid·b_i)≥0 的线性判定问题，再用贪心/DP/MST/SPFA等求解判定。

## Why · 为什么

### 直觉 · Intuition

要求 Σa/Σb 的最大值。如果猜答案为 mid，则 Σa/Σb≥mid 等价于 Σa-mid·Σb≥0 即 Σ(a_i-mid·b_i)≥0。这样分式判定就变成了线性判定：每个物品的'净权值'为 a_i-mid·b_i，选若干使净权和≥0。二分 mid 即可逼近最优比值。

### 原理 · Principle

二分法：对答案 mid，判定是否存在选法使 Σw_i(a_i-mid·b_i)≥0。判定函数的设计取决于限制条件：①无限制→贪心选正净权值 ②恰好选 k 个→选净权值前 k 大 ③分母≥W→01背包(b_i为重量,a_i-mid·b_i为价值) ④生成树→MST(a_i-mid·b_i为边权) ⑤环→判负环(a_i-mid为边权)。Dinkelbach 迭代法：用上一轮的比值作新 mid 迭代直至收敛，收敛快但不保证最劣情况。

### 历史 · History

分数规划是运筹学经典方法。Dinkelbach(1967)提出迭代法。竞赛中常见于最优比率生成树(POJ2728)、最优比率环(负环判定)、01分数规划(LOJ149)。OI Wiki 系统整理了二分法和 Dinkelbach 两种解法。

## How · 实现

### 伪代码

```python
# 01分数规划: 选恰好k个, 最大化 Σa/Σb
# 二分法
lo, hi = 0, max_ratio_upper_bound
while hi - lo > eps:
  mid = (lo + hi) / 2
  # 计算每个物品净权值 c_i = a_i - mid * b_i
  # 选净权值前k大, 求和
  c = [(a[i] - mid * b[i]) for i in range(n)]
  c.sort(reverse=True)
  s = sum(c[:k])
  if s >= 0:  # mid 可行
    lo = mid
  else:
    hi = mid
return lo
```

### Python 实现

```python
def fractional_programming_01(a, b, k):
    """01分数规划: 从n个物品中选恰好k个, 最大化 Σa_i/Σb_i。
    二分答案法。
    a, b: 每个物品的两个权值
    k: 必须选的个数
    返回最大比值。
    """
    n = len(a)
    eps = 1e-7
    lo, hi = 0.0, max(a[i] / b[i] for i in range(n))
    for _ in range(100):  # 二分100次足够精度
        mid = (lo + hi) / 2
        # 净权值 c_i = a_i - mid * b_i
        c = [a[i] - mid * b[i] for i in range(n)]
        c.sort(reverse=True)
        s = sum(c[:k])  # 选前k大
        if s >= 0:
            lo = mid
        else:
            hi = mid
    return lo


def fractional_programming_unlimited(a, b):
    """分数规划: 无限制选, 最大化 Σa/Σb。
    贪心: 选所有正净权值物品。
    """
    eps = 1e-7
    lo, hi = 0.0, max(a[i] / b[i] for i in range(len(a))) if a else 0.0
    for _ in range(100):
        mid = (lo + hi) / 2
        s = sum(max(0, a[i] - mid * b[i]) for i in range(len(a)))
        if s >= 0:
            lo = mid
        else:
            hi = mid
    return lo


def dinkelbach_method(a, b, k):
    """Dinkelbach迭代法: 01分数规划。
    用上一轮比值作新mid, 迭代至收敛。
    通常比二分法收敛更快。
    """
    n = len(a)
    # 初始猜测: 选前k个的比值
    L = sum(a[:k]) / sum(b[:k])
    eps = 1e-7
    while True:
        c = [(a[i] - L * b[i], i) for i in range(n)]
        c.sort(reverse=True)
        selected = [c[j][1] for j in range(k)]
        new_L = sum(a[i] for i in selected) / sum(b[i] for i in selected)
        if abs(new_L - L) < eps:
            return new_L
        L = new_L


if __name__ == '__main__':
    # 测试01分数规划(选恰好k个)
    a = [1, 2, 3, 4]
    b = [1, 1, 1, 1]
    k = 2
    # 最优: 选a最大的两个(3,4), 比值=(3+4)/(1+1)=3.5
    result = fractional_programming_01(a, b, k)
    print(f'01 fractional programming (k={k}): {result:.6f}')
    assert abs(result - 3.5) < 1e-4

    # 测试Dinkelbach迭代法
    result2 = dinkelbach_method(a, b, k)
    print(f'Dinkelbach method: {result2:.6f}')
    assert abs(result2 - 3.5) < 1e-4

    # 测试无限制选
    a2 = [3, 1, 4, 1, 5]
    b2 = [2, 1, 3, 1, 2]
    result3 = fractional_programming_unlimited(a2, b2)
    print(f'Unlimited selection: {result3:.6f}')
    # 暴力验证: 选所有a/b>0的部分
    best = 0
    for mask in range(1, 1 << len(a2)):
        sa = sum(a2[i] for i in range(len(a2)) if mask & (1 << i))
        sb = sum(b2[i] for i in range(len(a2)) if mask & (1 << i))
        best = max(best, sa / sb)
    print(f'Brute force: {best:.6f}')
    assert abs(result3 - best) < 1e-4

    print('All fractional programming tests passed!')

```

**PyPy 提示**: PyPy 对浮点运算和排序优化尚可；但二分100次+每次排序 O(n log n) 的开销在 N>1e5 时可能偏慢；注意浮点精度 eps 设 1e-7 通常足够。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(log(V/eps) * T) — T为单次判定复杂度; 贪心判定O(n log n), 背包判定O(n*W), MST判定O(m log m) |
| 空间 | O(N) — 存净权值数组 |

### 局限

浮点精度问题: eps 太小可能死循环, 太大精度不够；Dinkelbach 法不保证最劣情况收敛速度(但实际通常快)；判定函数设计是难点(需根据限制条件灵活变型)。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| LOJ | 149 | 3 | 01分数规划模板: 选恰好k个最大化Σa/Σb, 贪心判定 | [https://loj.ac/p/149](https://loj.ac/p/149) |
| Luogu | P4377 | 4 | Talent Show G: 分母≥W限制, 01背包判定 | [https://www.luogu.com.cn/problem/P4377](https://www.luogu.com.cn/problem/P4377) |
| POJ | 2728 | 4 | Desert King: 最优比率生成树, MST判定 | [http://poj.org/problem?id=2728](http://poj.org/problem?id=2728) |

## Pitfalls · 易错点

- 浮点精度: 二分次数不够导致精度不足, 通常100次二分或 eps=1e-7 足够
- hi 上界估计: 应取 max(a_i/b_i) 而非随意大值, 避免无效二分区段
- 判定函数方向: 求最大值时 s>=0 则 lo=mid, 求最小值时方向相反
- Dinkelbach 不收敛: 某些构造数据下 Dinkelbach 可能退化, 二分法更稳定

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/misc/frac-programming/](https://oi-wiki.org/misc/frac-programming/)
- CP-Algorithms ✓ [https://cp-algorithms.com/others/maximum_average_segment.html](https://cp-algorithms.com/others/maximum_average_segment.html)
- 论文 ✓ [https://doi.org/10.1287/mnsc.13.7.492](https://doi.org/10.1287/mnsc.13.7.492)
