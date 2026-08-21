---
id: complexity
name: 时间/空间复杂度分析
group: G-A-1
stage: basic
priority: P0
depth_tier: deep
---

# 时间/空间复杂度分析

> 渐近符号(O/Theta/Omega)与复杂度分析方法

<!-- 元信息: id=complexity · group=G-A-1 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

复杂度分析用渐近符号描述算法运行时间（时间复杂度）与额外空间（空间复杂度）随输入规模增长的规律。核心符号有大 O（上界）、大 Omega（下界）、大 Theta（紧界）、小 o、小 omega。分析方法包括循环计数、递归的主定理（Master Theorem）、均摊分析，以及常数与低阶项的省略。它是判断算法能否通过数据范围约束的第一道关卡。

## Why · 为什么

### 直觉 · Intuition

复杂度回答一个关键问题：数据翻 10 倍，我的程序要慢多少？O(n) 程序线性变慢，O(n²) 程序慢 100 倍，而 O(log n) 几乎不受影响。通过量级而不是具体秒数衡量，是因为真实运行时间依赖机器，而「增长趋势」是机器无关、可比较的。

### 原理 · Principle

O(f(n))：存在常数 c,n0 使 n≥n0 时 T(n)≤c·f(n)，表示上界；Omega 表示下界；Theta 表示上下界同阶（夹逼）。计算要点：(1) 循环层数×每层量级相乘；(2) 递归用主定理 T(n)=aT(n/b)+f(n)，比较 f(n) 与 n^(log_b a) 三种情形；(3) 只保留最高阶项、丢弃系数与低阶项；(4) 竞赛中默认分析最坏复杂度。

### 历史 · History

渐近分析源于 19 世纪数学中的 Bachmann–Landau 符号（大 O 由 Bachmann 1894 年引入，Landau 推广）。Donald Knuth 在《计算机程序设计艺术》中将其引入计算机算法分析并规范了定义，此后成为算法教科书的通用语言。OI Wiki 与 CPH 都将复杂度分析列为算法竞赛的第一课。

## How · 实现

### 伪代码

```python
# 常见循环分析
for i in range(n):        # O(n)
  ...
for i in range(n):        # 两层嵌套
  for j in range(n):      # O(n^2)
    ...
for i in range(n):        # 二分
  i = i * 2               # O(log n)

# 主定理 Master Theorem: T(n) = a T(n/b) + f(n)
# 情形1: f(n)=O(n^(log_b a - e))   => T(n)=Theta(n^(log_b a))
# 情形2: f(n)=Theta(n^(log_b a))   => T(n)=Theta(n^(log_b a) log n)
# 情形3: f(n)=Omega(n^(log_b a + e)) 且 af(n/b)<=cf(n) => T(n)=Theta(f(n))
```

### Python 实现

```python
import math


def count_basic_ops(n):
    """演示: 三层循环 n*n*m 的操作数 = n^2*m"""
    m = 10
    cnt = 0
    for i in range(n):
        for j in range(n):
            for k in range(m):
                cnt += 1
    return cnt


def analyze_binary_search_loops(n):
    """演示 O(log n): 每次循环规模减半"""
    cnt = 0
    while n > 1:
        n //= 2
        cnt += 1
    return cnt  # ~ log2(初始n)


def master_theorem_case(a, b, f_is_polynomially_less, f_is_theta_of_nlogba):
    """主定理判断封装（教学演示）
    nlogba = log_b(a)
    """
    if f_is_polynomially_less:
        return "Theta(n^{log_b a})"
    if f_is_theta_of_nlogba:
        return "Theta(n^{log_b a} log n)"
    return "Theta(f(n))"


if __name__ == "__main__":
    assert count_basic_ops(50) == 50 * 50 * 10
    assert analyze_binary_search_loops(1024) == 10
    assert analyze_binary_search_loops(1) == 0

    # 主定理示例: T(n)=2T(n/2)+1  => n^(log2 2)=n^1, f(n)=1 是多项式地更小
    assert master_theorem_case(2, 2, True, False) == "Theta(n^{log_b a})"
    # T(n)=T(n/2)+log n  => n^(log2 1)=n^0=1, f(n)=log n 是 Theta(n^0 log n)
    assert master_theorem_case(1, 2, False, True) == "Theta(n^{log_b a} log n)"

    # 排序复杂度对比表（教学用）
    import json
    table = {
        "O(1)": 1,
        "O(log n)": math.log2(10**6),
        "O(n)": 10**6,
        "O(n log n)": 10**6 * math.log2(10**6),
        "O(n^2)": 10**12,
    }
    print(json.dumps({k: int(v) for k, v in table.items()}))
    print("All tests passed.")
```

**PyPy 提示**: 复杂度分析本身与语言无关，但估计常数时要知道 Python 慢：约 1e8 次简单运算/秒（CPython），PyPy 约 2-5e8 次。竞赛中 Python 程序通常把操作数限制在 1e7-1e8 内。O(n) 与 O(n log n) 的区别在 Python 下更早显现，应优先选低常数实现。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 分析对象本身无复杂度；方法：循环计数、主定理、均摊分析 |
| 空间 | 额外数组/递归栈深度计入空间复杂度，与输入规模同阶存储记 O(n) |

### 局限

渐近分析忽略常数与具体机器，某些常数巨大的低阶算法可能实际更慢；最坏复杂度不反映平均表现（如快排最坏 O(n²) 但平均 O(n log n)）；且复杂度相同的两种实现常数可能相差数倍，需实测。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1226 | 2 | 快速幂：O(log b) 与暴力 O(b) 的复杂度对比，数据范围 b≤2^31 逼你选对算法 | [https://www.luogu.com.cn/problem/P1226](https://www.luogu.com.cn/problem/P1226) |
| Luogu | B3612 | 1 | 求区间和：O(n+m) 前缀和 vs O(nm) 暴力，复杂度的直接教材 | [https://www.luogu.com.cn/problem/B3612](https://www.luogu.com.cn/problem/B3612) |
| Luogu | P3379 | 4 | LCA模板：O(n log n) 预处理 + O(log n) 查询 vs 暴力 O(n) 查询的对比 | [https://www.luogu.com.cn/problem/P3379](https://www.luogu.com.cn/problem/P3379) |

## Pitfalls · 易错点

- 把 O(n+m) 写成 O(n) 或 O(m) 而忽略另一项在部分数据下的主导作用
- 递归复杂度不会用主定理，只凭直觉猜测（如误把 T(n)=T(n/2)+log n 判成 O(n)）
- 把均摊 O(1) 与单次操作最坏 O(1) 混淆
- 忽视 Python 常数因子，理论上 O(n log n) 的实现在 Python 下超时
- 把常量规模循环当 O(n)（与输入规模无关的 N 次固定循环是 O(1)）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/basic/complexity/](https://oi-wiki.org/basic/complexity/)
- 书籍 ✓ `CPH ch2 p27`
