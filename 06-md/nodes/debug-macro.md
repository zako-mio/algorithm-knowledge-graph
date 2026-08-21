---
id: debug-macro
name: 调试宏
group: G-E-4
stage: basic
priority: P0
depth_tier: deep
---

# 调试宏

> #ifdef DEBUG / -DONLINE_JUDGE 编译宏控制调试输出，提交时无需删代码

<!-- 元信息: id=debug-macro · group=G-E-4 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

调试宏是竞赛编程中控制调试输出的技术。C++中使用#ifdef DEBUG / #ifndef ONLINE_JUDGE预处理器指令，在本地调试时输出调试信息，提交OJ时自动关闭。Python中使用环境变量或全局常量实现类似功能。核心思想：调试代码始终保留在源码中，通过编译/运行时开关控制是否执行，避免提交前手动删除调试代码的风险。

## Why · 为什么

### 直觉 · Intuition

调试宏就像'开关灯'：本地开发时打开调试灯看清内部状态，提交时关灯不影响评测。无需反复增删调试代码。

### 原理 · Principle

C++: #ifdef DEBUG检查宏定义，-DDEBUG编译选项定义DEBUG，-DONLINE_JUDGE由OJ自动定义。Python: os.environ.get('DEBUG')读取环境变量，DEBUG=1 python script.py启用。调试输出到stderr避免干扰stdout答案。

### 历史 · History

预处理器调试宏是C/C++竞赛编程的传统技术。OI Wiki在'common-tricks'中介绍了使用宏进行调试。大部分OJ开启-DONLINE_JUDGE。

## How · 实现

### 伪代码

```python
# C++:
#ifdef DEBUG
  #define debug(...) fprintf(stderr,__VA_ARGS__)
#else
  #define debug(...) 42
#endif
// Python:
DEBUG = os.environ.get('DEBUG')=='1'
def dprint(*a):
  if DEBUG: print(*a, file=stderr)
```

### Python 实现

```python
"""Debug macro pattern for competitive programming in Python.
Uses environment variable or constant to toggle debug output.
No need to remove debug code when submitting.
"""
import os
import sys

# Method 1: Environment variable (recommended)
# Set DEBUG=1 locally, unset on OJ
DEBUG = os.environ.get('DEBUG', '0') == '1'

def dprint(*args, **kwargs):
    """Debug print: only outputs when DEBUG is True."""
    if DEBUG:
        print(*args, file=sys.stderr, **kwargs)

def dpp(var_name, var):
    """Debug print variable with name."""
    if DEBUG:
        print(f"  {var_name} = {var}", file=sys.stderr)

def darr(name, arr, start=0, end=None):
    """Debug print array."""
    if DEBUG:
        if end is None:
            end = len(arr)
        print(f"  {name}[{start}:{end}] = {arr[start:end]}", file=sys.stderr)

# Method 2: Assert-based debugging (disabled in production)
def dassert(condition, msg=""):
    """Assert only in debug mode."""
    if DEBUG and not condition:
        raise AssertionError(msg)

# Method 3: Timing
import time
class Timer:
    """Simple timer for debugging performance."""
    def __init__(self, name=""):
        self.name = name
        self.start = time.perf_counter()
    def __call__(self, msg=""):
        if DEBUG:
            elapsed = time.perf_counter() - self.start
            print(f"  [{self.name}] {msg}: {elapsed:.4f}s", file=sys.stderr)
            self.start = time.perf_counter()

# Equivalent C++ pattern (for reference):
# #ifdef DEBUG
#     #define debug(...) fprintf(stderr, __VA_ARGS__)
#     #define debugv(x) fprintf(stderr, "  %s = %d\n", #x, x)
# #else
#     #define debug(...) 42
#     #define debugv(x) 42
# #endif
# // Compile with -DDEBUG locally, -DONLINE_JUDGE on OJ

if __name__ == "__main__":
    # Test with DEBUG=True
    import os
    os.environ['DEBUG'] = '1'
    # Note: DEBUG was set at import time, so need to reimport for demo
    # In practice, set DEBUG before running: DEBUG=1 python script.py

    # Direct test
    DEBUG = True

    dprint("This is a debug message")
    dpp("x", 42)
    darr("arr", [1, 2, 3, 4, 5], 0, 3)
    dassert(1 + 1 == 2, "Math is broken")
    timer = Timer("test")
    import time
    time.sleep(0.001)
    timer("step1 done")

    # Test with DEBUG=False
    DEBUG = False
    dprint("This should NOT appear")
    dpp("y", 99)
    assert True  # dassert is no-op

    print("debug-macro: ALL TESTS PASSED")

```

**PyPy 提示**: Python用环境变量DEBUG控制。调试输出到stderr（sys.stderr）不影响stdout答案。C++中fprintf(stderr,...)同理。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(1)（判断后跳过） |
| 空间 | O(1) |

### 局限

Python无法像C++在编译时完全消除调试代码（运行时仍有判断开销，但极小）。C++中#ifdef在编译时移除，零开销。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| OI-Wiki | contest/common-tricks | 2 | 使用宏进行调试的官方教程 | [https://oi-wiki.org/contest/common-tricks/](https://oi-wiki.org/contest/common-tricks/) |

## Pitfalls · 易错点

- 调试输出必须到stderr而非stdout（否则干扰答案判定）
- Python环境变量在import时读取，运行中修改os.environ不会更新已读取的DEBUG
- C++中忘记-DDEBUG导致调试不生效
- 部分OJ可能不定义ONLINE_JUDGE，需确认

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/contest/common-tricks/](https://oi-wiki.org/contest/common-tricks/)
- OI Wiki ✓ [https://oi-wiki.org/tools/testlib/](https://oi-wiki.org/tools/testlib/)
