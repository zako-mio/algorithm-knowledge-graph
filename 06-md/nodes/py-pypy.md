---
id: py-pypy
name: PyPy差异与注意事项
group: G-E-3
stage: basic
priority: P0
depth_tier: deep
---

# PyPy差异与注意事项

> PyPy JIT加速循环但递归反而更慢；大整数/内存差异；部分库不可用；递归限stack需手动设

<!-- 元信息: id=py-pypy · group=G-E-3 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

PyPy 是 Python 的替代实现，用 JIT（即时编译）把热点 Python 代码编译为机器码，对密集数值循环加速 3-10 倍，是 Python 竞赛在 OJ 上赶超时限的主要手段。但与 CPython 存在关键差异：1) 递归调用更慢且每帧栈更大，深递归易 segfault；2) 首次运行有 JIT 预热开销（短程序可能更慢）；3) 大整数运算常数略大；4) 部分 C 扩展库不可用或需 cffi 适配；5) 内存占用通常更高。竞赛选手需了解差异以正确选择策略。

## Why · 为什么

### 直觉 · Intuition

CPython 是纯解释器，每条字节码都查表执行，循环慢。PyPy 先解释运行，发现热点后用 tracing JIT 把热点路径编译成机器码，之后跑机器码飞快。但 JIT 不能优化一切：递归调用涉及帧对象创建无法内联，反而因 PyPy 帧更重而更慢；短程序 JIT 还没预热就结束了。

### 原理 · Principle

PyPy 的 JIT 基于 tracing：记录热点循环执行轨迹，生成优化机器码。对纯整数 for 循环（如筛法、DP 递推）加速显著。局限：递归无法被 trace（每次帧对象类型不同）；大整数因 PyPy 内部 bigint 实现与 CPython 不同（策略：小整数走 list-of-int 策略，大整数走 bigint 对象）；C 扩展需通过 cffi 而非 ctypes/cpython.h；启动有 ~0.5s 预热。

### 历史 · History

PyPy 项目始于 2007 年，PyPy 团队持续维护。各 OJ（洛谷、Codeforces）先后提供 PyPy3 提交选项，成为 Python 选手标配。PyPy 7+ 支持 Python 3.6+ 语法，当前支持到 Python 3.11。

## How · 实现

### 伪代码

```python
# PyPy 竞速要点
# 1. 循环密集→PyPy 快
for i in range(n): a[i] = b[i] + c[i]  # PyPy ~5x faster
# 2. 递归→PyPy 慢，改迭代或加线程栈
# 3. 输入大→sys.stdin.buffer.read().split()
# 4. 浮点→PyPy 有时更快有时更慢，需实测
# 5. 大整数→pow(a,b,mod) 走底层仍快
```

### Python 实现

```python
# PyPy 差异自测（CPython/PyPy 均可运行此文件）
import sys

def is_pypy():
    """检测当前是否 PyPy"""
    return hasattr(sys, 'pypy_version_info')

def loop_benchmark(n):
    """纯整数循环，PyPy 应明显快于 CPython"""
    s = 0
    for i in range(n):
        s += i * i % 1000000007
    return s

def recursive_sum(n):
    """递归求和，PyPy 可能更慢且需大栈"""
    if n == 0:
        return 0
    return n + recursive_sum(n - 1)

if __name__ == "__main__":
    # 循环正确性
    assert loop_benchmark(100) == sum(i * i % 1000000007 for i in range(100))
    # 递归正确性（小规模）
    assert recursive_sum(500) == 500 * 501 // 2
    # 大整数一致性
    assert 2 ** 512 == pow(2, 512)
    assert pow(2, 100, 1000000007) == 2 ** 100 % 1000000007
    # 平台检测
    runtime = 'PyPy' if is_pypy() else 'CPython'
    print(f"py-pypy OK (running on {runtime})")

```

**PyPy 提示**: PyPy 核心差异速查：①循环快 3-10x（JIT）；②递归慢且栈重，必须 threading.stack_size + 线程或改迭代；③启动有 ~0.5s 预热，极短任务可能比 CPython 慢；④大整数乘除常数略大但 pow(a,b,mod) 仍快；⑤C 扩展（numpy 等）可能不可用，需 cffi 替代；⑥内存占用高 1.5-3 倍；⑦默认递归上限可能不同，务必 setrecursionlimit。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 循环密集型 O(N) 常数减 3-10 倍；递归型可能持平或更慢 |
| 空间 | 内存占用比 CPython 高 1.5-3 倍 |

### 局限

1) JIT 预热使极短程序（<100ms）可能比 CPython 慢；2) 部分 OJ 的 PyPy 版本旧（如 3.6），新语法（walrus := 等）不可用；3) C 扩展库（numpy/scipy）通常不可用；4) 递归不仅慢还更易 segfault；5) 浮点运算行为可能有微小差异（NaN/inf 处理）。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P4779 | 4 | Dijkstra 密集循环，PyPy 提交比 CPython 快数倍 | [https://www.luogu.com.cn/problem/P4779](https://www.luogu.com.cn/problem/P4779) |
| AtCoder | ABC 双语言选项 | 2 | 递归题选 CPython，循环题选 PyPy3 | [https://atcoder.jp/](https://atcoder.jp/) |

## Pitfalls · 易错点

- 递归题在 PyPy 提交→segfault 或 TLE，应改 CPython 提交或改迭代
- 设了 setrecursionlimit 但不设线程栈→PyPy 更易 segfault
- 以为 PyPy 总更快→短程序 JIT 未预热反而更慢
- 用 numpy 等第三方库→PyPy 环境可能无该库
- 大整数循环在 PyPy 常数大，小整数循环才被策略优化

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/lang/python/](https://oi-wiki.org/lang/python/)
- web ✓ [https://www.pypy.org/features.html](https://www.pypy.org/features.html)
- web ✓ [https://docs.python.org/3/library/sys.html](https://docs.python.org/3/library/sys.html)
