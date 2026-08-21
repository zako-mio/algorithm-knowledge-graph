---
id: py-lru-cache
name: lru_cache记忆化
group: G-E-3
stage: intermediate
priority: P0
depth_tier: deep
---

# lru_cache记忆化

> functools.lru_cache(None)装饰器一行实现函数记忆化，递归DP利器

<!-- 元信息: id=py-lru-cache · group=G-E-3 · stage=intermediate · priority=P0 · depth_tier=deep -->

## What · 是什么

functools.lru_cache(maxsize=None) 装饰器为函数自动加 LRU 缓存：以参数为键、返回值为值存储，重复调用直接命中缓存。maxsize=None 表示无限缓存，适合状态空间有限的递归 DP（如斐波那契、数位 DP、博弈 DP）。参数必须可哈希（int/str/tuple 可，list 不可）。是 Python 竞赛实现记忆化搜索最简洁的方式，一行装饰器替代手写 memo 字典。

## Why · 为什么

### 直觉 · Intuition

递归斐波那契 fib(40) 不缓存要算 10^8 次（指数爆炸），加缓存后每个 n 只算一次变成 O(n)。lru_cache 就是自动帮你建这个缓存字典——你只管写递归逻辑，缓存交给装饰器。

### 原理 · Principle

lru_cache 内部用字典以参数元组为键存储返回值。每次函数调用先查字典，命中则返回缓存值，未命中则计算后存入。maxsize 有限时用双向链表实现 LRU 淘汰。maxsize=None 时退化为纯字典（无淘汰），竞赛中几乎总是用 None（状态数有限）。typed=True 时区分 3 和 3.0（竞赛一般用默认 False）。线程安全（有锁，竞赛单线程无影响）。

### 历史 · History

functools.lru_cache 自 Python 3.2 引入。3.8 新增 @lru_cache 直接装饰函数（不传参）的简写。3.9 新增 @cache 等价于 @lru_cache(maxsize=None)。OI Wiki Python 页介绍了其在斐波那契递归中的应用。

## How · 实现

### 伪代码

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n < 2: return n
    return fib(n-1) + fib(n-2)
# 警告: 深递归仍需 setrecursionlimit
```

### Python 实现

```python
# lru_cache 记忆化（含自测）
import sys
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    """记忆化斐波那契，O(n)"""
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

@lru_cache(maxsize=None)
def grid_paths(m, n):
    """网格路径数: 从 (0,0) 到 (m,n) 只能向右或向下"""
    if m == 0 or n == 0:
        return 1
    return grid_paths(m - 1, n) + grid_paths(m, n - 1)

if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    # 斐波那契正确性
    assert fib(0) == 0 and fib(1) == 1 and fib(10) == 55
    assert fib(50) == 12586269025  # 无缓存会超时
    assert fib(100) == 354224848179261915075  # Python 大整数无溢出
    # 缓存命中信息
    info = fib.cache_info()
    assert info.hits > 0  # 有缓存命中
    # 网格路径
    assert grid_paths(3, 3) == 20  # C(6,3)=20
    assert grid_paths(10, 10) == 184756  # C(20,10)
    print(f"py-lru-cache OK (fib hits={fib.cache_info().hits})")

```

**PyPy 提示**: PyPy 下 lru_cache 同样有效。但注意：1) PyPy 递归调用本身慢，深递归即使记忆化也慢，能改迭代更好；2) PyPy 对类方法 lru_cache 有内存策略差异（list-of-ints 策略），一般无影响；3) 缓存占内存在 PyPy 更明显（每值开销大），状态数极大时需清理或换手写数组。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 首次计算各状态 O(1) 摊还；总计 O(状态数 × 转移数) |
| 空间 | O(状态数) 存缓存 |

### 局限

1) 参数必须可哈希——list 不行，传 list 需先 tuple()；2) 不控制递归深度，仍可能 RecursionError/segfault，须配 setrecursionlimit；3) 缓存随函数对象存活，多组数据需 fib.cache_clear() 清空；4) 状态数极大（>10^7）时内存爆炸，应改用数组迭代。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| LeetCode | 70 | 1 | f(n)=f(n-1)+f(n-2)，lru_cache 一行装饰器 | [https://leetcode.cn/problems/climbing-stairs/](https://leetcode.cn/problems/climbing-stairs/) |
| Luogu | P1048 | 2 | 0-1 背包记忆化搜索用 lru_cache 简化 | [https://www.luogu.com.cn/problem/P1048](https://www.luogu.com.cn/problem/P1048) |

## Pitfalls · 易错点

- 传 list 参数 → TypeError: unhashable type: 'list'，必须先 tuple()
- 不 cache_clear() 多组数据 → 答案串扰或内存累积
- 深递归 + lru_cache 仍可能 segfault，必须同时 setrecursionlimit + 线程栈
- 状态数 >10^7 时内存爆炸，应改用一维数组滚动迭代
- typed=True 时 f(3) 和 f(3.0) 分别缓存浪费空间，竞赛保持默认 False

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/lang/python/](https://oi-wiki.org/lang/python/)
- web ✓ [https://docs.python.org/3/library/functools.html#functools.lru_cache](https://docs.python.org/3/library/functools.html#functools.lru_cache)
