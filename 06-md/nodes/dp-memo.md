---
id: dp-memo
name: 记忆化搜索
group: G-A-11
stage: basic
priority: P0
depth_tier: deep
---

# 记忆化搜索

> 自顶向下DFS+缓存，DP的递归实现方式

<!-- 元信息: id=dp-memo · group=G-A-11 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

记忆化搜索（Memoization）是 DP 的自顶向下递归实现：从最终状态（答案）出发递归，每进入一个子问题先查缓存，命中则直接返回，未命中则递归计算后存入缓存。与自底向上递推（for 循环填表）等价但更直观——转移方程直接对应递归式。Python 中用 functools.lru_cache(maxsize=None) 装饰器一行实现，或手写 memo 字典。优点是只计算需要的状态（稀疏状态空间友好），缺点是递归栈开销与溢出风险。

## Why · 为什么

### 直觉 · Intuition

自底向上填表需要先想清楚计算顺序，复杂状态（如数位 DP、博弈 DP、带维度的树形 DP）很难确定顺序。记忆化搜索反过来：从答案状态出发「需要什么就算什么」，递归自然表达依赖关系，缓存避免重复。就像查地图——你不用把整本地图背下来，只查你问的那条路，查过就记住。

### 原理 · Principle

记忆化搜索 = 递归 + 缓存字典。进入函数：if 状态 in memo: return memo[状态]；否则计算（含递归子调用）后 memo[状态]=结果; return 结果。只计算从答案状态可达的状态，跳过不可达状态（递推会全算）。代价是递归调用开销（Python 每帧 ~1μs）和栈溢出风险。状态必须可哈希（int/tuple 可，list 需 tuple）。在 Python 中 lru_cache 自动管理缓存。

### 历史 · History

记忆化（memoization）术语由 Donald Michie 1968 年提出。Python functools.lru_cache 自 3.2 提供。OI Wiki Python 页以 lru_cache+斐波那契为例展示。记忆化与递推两种 DP 实现方式长期并存，记忆化在状态稀疏或转移顺序难定时更优。

## How · 实现

### 伪代码

```python
# 记忆化搜索模板（手写 memo）
memo = {}
def solve(state):
    if state in memo: return memo[state]
    if base_case(state): return base_value
    result = combine(solve(s1), solve(s2), ...)
    memo[state] = result
    return result
# Python 简写: @lru_cache(maxsize=None)
@lru_cache(maxsize=None)
def solve(state):
    if base: return val
    return combine(solve(s1), ...)
```

### Python 实现

```python
# 记忆化搜索：斐波那契 + 网格路径数（含自测）
import sys
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    """记忆化斐波那契 O(n)"""
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

@lru_cache(maxsize=None)
def unique_paths(m, n):
    """从 (1,1) 到 (m,n) 只能向右或向下的路径数
    答案 = C(m+n-2, m-1)。记忆化搜索自顶向下"""
    if m == 1 or n == 1:
        return 1
    return unique_paths(m - 1, n) + unique_paths(m, n - 1)

if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    # 斐波那契
    assert fib(0) == 0 and fib(1) == 1 and fib(10) == 55
    assert fib(100) == 354224848179261915075
    # 缓存命中
    assert fib.cache_info().hits > 0
    # 网格路径数: C(m+n-2, m-1)
    assert unique_paths(1, 1) == 1
    assert unique_paths(3, 3) == 6       # C(4,2)=6
    assert unique_paths(3, 7) == 28      # C(8,2)=28
    assert unique_paths(10, 10) == 48620  # C(18,9)=48620
    print(f"dp-memo OK (fib hits={fib.cache_info().hits})")

```

**PyPy 提示**: PyPy 下记忆化搜索递归调用比 CPython 慢且栈更重。lru_cache 本身快（C 实现）。若状态数大且转移简单，PyPy 下自底向上递推（for 循环填表）远优于记忆化——JIT 优化循环不优化递归。状态稀疏或转移顺序难定时仍用记忆化，但务必 setrecursionlimit + 线程栈。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(可达状态数 × 每状态转移数)，只算需要的状态 |
| 空间 | O(可达状态数) 缓存 + O(递归深度) 栈 |

### 局限

1) 递归深度受栈限制，需 setrecursionlimit + 可能线程栈；2) Python 递归调用开销大（每帧~1μs），状态多时递推更快；3) 参数必须可哈希；4) 多组数据需 cache_clear()。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1048 | 2 | 0-1 背包记忆化搜索 dp(i,remain) | [https://www.luogu.com.cn/problem/P1048](https://www.luogu.com.cn/problem/P1048) |
| Luogu | P2602 | 5 | 数位 DP 统计各数字出现次数 | [https://www.luogu.com.cn/problem/P2602](https://www.luogu.com.cn/problem/P2602) |

## Pitfalls · 易错点

- 不设 setrecursionlimit → 深递归 RecursionError 或 segfault
- 参数传 list → TypeError unhashable，需先 tuple()
- 多组数据不 cache_clear() → 答案串扰
- 状态数大用记忆化 → 递归调用开销累积超时，应改递推
- PyPy 下深递归记忆化 → segfault，改递推或加线程栈

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/dp/memo/](https://oi-wiki.org/dp/memo/)
- web ✓ [https://docs.python.org/3/library/functools.html#functools.lru_cache](https://docs.python.org/3/library/functools.html#functools.lru_cache)
- 书籍 ✓ `CPH ch7 p75 (DP section)`
