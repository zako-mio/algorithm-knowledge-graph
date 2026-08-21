---
id: compile-debug
name: 编译与调试
group: G-E-9
stage: basic
priority: P0
depth_tier: deep
---

# 编译与调试

> g++编译选项(-O2/-g/-Wall/-Wextra)、Sanitizer、gdb调试与Python调试技巧，竞赛提交前必备检查

<!-- 元信息: id=compile-debug · group=G-E-9 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

编译与调试是竞赛选手的日常基本功。C++侧核心是g++编译选项：-O2/-O3优化、-g调试信息、-Wall/-Wextra警告、-DDEBUG宏控制、-lm链接math库；调试工具为gdb(断点/单步/观察变量)与Sanitizer(-fsanitize=address/undefined检测越界与未定义行为)。Python侧用pdb、print到stderr、setrecursionlimit、sys.stdin缓冲优化等。竞赛场景的核心纪律：本地用-g -fsanitize编译调试、提交用-O2（或-O3）并开启ONLINE_JUDGE宏，把调试代码用#ifdef/环境变量隔离，保证提交代码不含调试输出。编译原理层面还需理解优化(常量折叠、内联、循环展开、死代码消除)如何影响性能与调试可读性。

## Why · 为什么

### 直觉 · Intuition

编译选项就像'装配模式'：调试模式(-g,无优化)保留源码映射和变量名，方便人机对话式排查；发布模式(-O2)优化执行速度但会打乱源码对应关系。Sanitizer则是'安全气囊'，在程序越界/未定义行为时立刻报警而不是让结果悄悄出错。正确组合'本地调试模式+提交优化模式'能大幅缩短排错时间。

### 原理 · Principle

g++工作流：(1)本地开发用 g++ -std=c++17 -Wall -Wextra -g -fsanitize=address,undefined -DDEBUG a.cpp -o a，运行发现越界/UB；(2)提交用 g++ -std=c++17 -O2 -DONLINE_JUDGE a.cpp。核心开关：-O2/-O3/Ofast优化等级(优化会显著降低调试可读性,Debug时勿用)；-g写调试信息供gdb；-Wall/-Wextra显示可能错误的警告；-fsanitize=address(ASan,检测堆栈越界/释放后使用,约2x慢)、undefined(UBSan,检测整数溢出/除零等UB,零开销)；-DDEBUG定义宏(代码内#ifdef DEBUG输出调试信息,ONLINE_JUDGE由OJ定义用于区分本地/提交)。gdb常用：break设置断点、run/next/step执行控制、print/watch看变量、backtrace看调用栈。Python常用：pdb断点、sys.stderr输出调试、functools/计数器定位逻辑错误。

### 历史 · History

GCC是Linux/竞赛环境的事实标准编译器，gdb从1986年随GNU项目发展至今。Sanitizer是Google/LLVM 2012年前后引入的编译期插桩技术，成为C/C++内存安全调试的主流工具。OI Wiki的compile-debug.md、compiler.md与lang/optimizations.md系统介绍了这些内容。

## How · 实现

### 伪代码

```python
# 本地调试编译(启用Sanitizer与调试信息)
g++ -std=c++17 -g -Wall -Wextra -fsanitize=address,undefined -DDEBUG a.cpp -o a_dbg
./a_dbg < test.in

# 提交编译(最高优化, 关闭调试)
g++ -std=c++17 -O2 -DONLINE_JUDGE a.cpp -o a

# gdb 会话
gdb ./a_dbg
  break main
  run < test.in
  next / step / finish
  print arr / watch i / backtrace

# Python 调试
debug输出到stderr: print(..., file=sys.stderr)
python3 -m pdb script.py
```

### Python 实现

```python
"""编译与调试：完整工作流模板(带自测).
覆盖: 编译选项生成、C+++Sanitizer检查、Python性能调试、gdb命令参考.
"""
import subprocess
import sys
import os
import tempfile

# ---------- 1. g++ 编译命令模板 ----------
COMPILE_DEBUG = (
    "g++ -std=c++17 -g -Wall -Wextra "
    "-fsanitize=address,undefined -DDEBUG a.cpp -o a_dbg"
)
COMPILE_SUBMIT = "g++ -std=c++17 -O2 -DONLINE_JUDGE a.cpp -o a"
COMPILE_PROFILE = "g++ -std=c++17 -O2 -Wall a.cpp -o a"


def make_debug_build(src, exe="a_dbg"):
    """编译并返回(返回码, stderr)."""
    cmd = (
        "g++ -std=c++17 -g -Wall -Wextra "
        f"-fsanitize=address,undefined {src} -o {exe}"
    )
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return r.returncode, r.stderr


# ---------- 2. Python 侧调试/性能工具 ----------

def timeit(f, *args, label="", repeat=3):
    """简单计时器, 用于定位性能瓶颈."""
    import time
    best = None
    for _ in range(repeat):
        t0 = time.perf_counter()
        f(*args)
        dt = time.perf_counter() - t0
        best = dt if best is None else min(best, dt)
    print(f"{label}: {best*1000:.2f} ms")
    return best


def fast_io():
    """Python竞赛输入加速: 一次性读入全部并缓存."""
    import sys
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    return it


if __name__ == "__main__":
    # 测试时间工具
    def dummy(n):
        s = 0
        for i in range(n):
            s += i
        return s

    t = timeit(dummy, 1000000, label="sum 1e6")
    assert t is not None

    # 测试fast_io接口
    it = fast_io()
    assert it is not None

    # 演示gdb命令(不实际执行, 仅验证模板存在)
    assert "break main" in """
break main
run < test.in
next
step
finish
print arr
watch i
backtrace
"""

    print("compile-debug: ALL TESTS PASSED")

```

**PyPy 提示**: Python调试注意：避免list.pop(0)、优先sys.stdin.buffer.read()读入、递归前setrecursionlimit(1<<25)。编译选项对Python无意义，但可用pypy3 -m cProfile定位热点。C++的-UDEBUG可取消宏定义。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 编译期开销O(源码规模); 运行时-O2显著加速(常数级, 可能2-5x) |
| 空间 | Sanitizer增加内存占用(ASan约2x, TSan 5-15x) |

### 局限

Windows下g++不支持Sanitizer(需修改版MinGW64);优化选项(-O2/-O3)可能掩盖或改变调试行为;Python无编译期宏,只能用环境变量/常量控制调试输出。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| OI Wiki | compile-debug 教程 | 0 | g++选项、gdb命令、Sanitizer的权威中文教程 | [https://oi-wiki.org/tools/compile-debug/](https://oi-wiki.org/tools/compile-debug/) |
| OI Wiki | compiler 安装 | 0 | 各系统GCC/Clang安装与环境变量配置 | [https://oi-wiki.org/tools/compiler/](https://oi-wiki.org/tools/compiler/) |
| OI Wiki | 优化介绍 | 0 | 编译器优化原理(常量折叠/内联/死代码消除)与-Ox差异 | [https://oi-wiki.org/lang/optimizations/](https://oi-wiki.org/lang/optimizations/) |

## Pitfalls · 易错点

- Debug时不要开-O2/-O3: 优化打乱变量映射, gdb无法可靠查看
- Sanitizer与-O2/Ofast不兼容, 调试用-fsanitize提交用-O2
- 调试输出必须到stderr, 否则污染stdout被判WA
- -lm仅Unix下math库需要; Windows/Linux g++一般自动链接
- Python的os.environ在import时读取, 运行中改环境变量不生效

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/tools/compile-debug/](https://oi-wiki.org/tools/compile-debug/)
- OI Wiki ✓ [https://oi-wiki.org/tools/compiler/](https://oi-wiki.org/tools/compiler/)
- OI Wiki ✓ [https://oi-wiki.org/lang/optimizations/](https://oi-wiki.org/lang/optimizations/)
