---
id: py-recursion-limit
name: 递归栈限制设置
group: G-E-3
stage: basic
priority: P0
depth_tier: deep
---

# 递归栈限制设置

> sys.setrecursionlimit(1<<20)避免深递归栈溢出；Python默认递归深度仅1000

<!-- 元信息: id=py-recursion-limit · group=G-E-3 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

Python 默认递归深度上限仅 1000（CPython），深递归（如 DFS、树形 DP）会抛 RecursionError。用 sys.setrecursionlimit(N) 可提高上限。但 setrecursionlimit 只是改了 Python 层检查阈值，底层 C 栈若溢出仍会段错误（segfault），尤其在 PyPy 上更常见。终极方案是放线程里设 threading.stack_size 后运行，或改用迭代（手写栈）。

## Why · 为什么

### 直觉 · Intuition

Python 解释器用 C 栈跟踪每次函数调用。默认 1000 层保护防止 C 栈溢出导致进程崩溃。竞赛中 DFS 可能递归 10^5-10^6 层，必须放宽。但放宽太多可能让 C 栈溢出直接 segfault（无 Python 异常可捕获），所以还需配合增大线程栈。

### 原理 · Principle

sys.setrecursionlimit(limit) 设置解释器允许的最大递归深度。超限抛 RecursionError（3.5+）。但实际 C 栈大小由操作系统/线程决定（Linux 默认 8MB，每帧约 1-4KB → 物理上限约 2000-8000 层）。突破物理上限需用 threading.stack_size(N) 创建大栈线程运行递归函数。PyPy 每帧栈更大，setrecursionlimit 后更易 segfault。

### 历史 · History

CPython 早期递归上限 1000，3.0 前超限抛 RuntimeError，3.5+ 改为 RecursionError 子类。OI Wiki 提到竞赛需 setrecursionlimit。社区长期流传线程栈方案解决 segfault。

## How · 实现

### 伪代码

```python
import sys, threading
sys.setrecursionlimit(1 << 25)
# 方案1: 直接调（可能 segfault 若 C 栈不够）
# main()
# 方案2: 放线程里增大栈
def run(): main()
threading.stack_size(256 << 20)  # 256MB
th = threading.Thread(target=run)
th.start(); th.join()
```

### Python 实现

```python
# 递归栈限制设置（含自测）
import sys
import threading

def deep_sum(n):
    """递归求 1+2+...+n"""
    if n == 0:
        return 0
    return n + deep_sum(n - 1)

def run_with_big_stack(func, *args, stack_mb=256):
    """在大栈线程中运行 func，避免 C 栈溢出 segfault"""
    result = [None]
    def wrapper():
        result[0] = func(*args)
    threading.stack_size(stack_mb * (1 << 20))
    th = threading.Thread(target=wrapper)
    th.start()
    th.join()
    return result[0]

if __name__ == "__main__":
    # 默认限制 1000，递归 1001 层应抛 RecursionError
    try:
        deep_sum(2000)
        raised = False
    except RecursionError:
        raised = True
    assert raised, "默认限制应拦截深递归"

    # 放宽限制
    sys.setrecursionlimit(1 << 20)
    assert deep_sum(100000) == 100000 * 100001 // 2

    # 更深递归放线程大栈运行
    sys.setrecursionlimit(1 << 25)
    val = run_with_big_stack(deep_sum, 500000, stack_mb=512)
    assert val == 500000 * 500001 // 2
    print("py-recursion-limit OK")

```

**PyPy 提示**: PyPy 每调用帧占 C 栈更多（约 4-8KB vs CPython ~1KB），setrecursionlimit 后极易 segfault。务必用 threading.stack_size + 线程方案。另外 PyPy 递归调用本身比迭代慢很多（JIT 不优化递归），能改迭代就改。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | setrecursionlimit O(1)；线程创建约 0.1ms |
| 空间 | 线程栈按设定值分配（如 256MB） |

### 局限

1) setrecursionlimit 设过高但 C 栈不足时直接 segfault（无法捕获）；2) 线程方案需 join 等待，交互题需注意；3) PyPy 递归即使不栈溢出也慢，优先改迭代。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1683 | 3 | 树退化链时 DFS 深度 1e5，须 setrecursionlimit | [https://www.luogu.com.cn/problem/P1683](https://www.luogu.com.cn/problem/P1683) |
| Luogu | P5661 | 3 | CSP-J Python 选手常因未设递归上限 RE | [https://www.luogu.com.cn/problem/P5661](https://www.luogu.com.cn/problem/P5661) |

## Pitfalls · 易错点

- 只设 setrecursionlimit 不增大 C 栈 → segfault（尤其在 PyPy）
- 设了 limit 但线程栈不够大，仍 segfault；须二者配合
- 交互题用线程方案可能导致输出缓冲乱序，需在 join 后统一输出
- PyPy 下深递归即使不崩溃也极慢，应优先改写成迭代（手写栈）
- 忘了 setrecursionlimit 导致正常大小的树 DFS 在 Python 抛 RecursionError

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/lang/python/](https://oi-wiki.org/lang/python/)
- web ✓ [https://docs.python.org/3/library/sys.html#sys.setrecursionlimit](https://docs.python.org/3/library/sys.html#sys.setrecursionlimit)
- web ✓ [https://docs.python.org/3/library/threading.html#threading.stack_size](https://docs.python.org/3/library/threading.html#threading.stack_size)
