---
id: stress-test
name: 对拍/压力测试
group: G-E-4
stage: basic
priority: P0
depth_tier: deep
---

# 对拍/压力测试

> 生成随机数据→暴力/正解分别运行→比对输出找bug，竞赛调试核心手段

<!-- 元信息: id=stress-test · group=G-E-4 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

对拍（压力测试）是竞赛调试的核心手段：编写数据生成器产生随机测试数据，分别运行暴力解法（保证正确但慢）和待测解法（可能含bug），比对两者输出。若输出不同则找到bug。OI Wiki推荐使用testlib库编写高质量数据生成器，确保可复现（相同参数相同输出）。对拍可自动化循环执行直到发现错误或达到足够测试次数。

## Why · 为什么

### 直觉 · Intuition

对拍就像'双盲实验'：用两个独立的方法解决同一问题，如果结果一致则更有信心。结果不一致时，刚好找到了bug。

### 原理 · Principle

三组件：数据生成器（gen）、暴力解法（brute）、待测解法（solve）。循环：gen生成数据→分别跑brute和solve→diff比较输出→不一致则保存数据用于调试。

### 历史 · History

对拍是竞赛选手的基本功。OI Wiki在'common-tricks'和'testlib'页面详细介绍了对拍方法。testlib库的generator确保跨平台可复现。

## How · 实现

### 伪代码

```python
while True:
  gen > test.in
  brute < test.in > a.out
  solve < test.in > b.out
  if diff(a.out, b.out):
    print('Found bug!'); break
```

### Python 实现

```python
"""Stress testing template for competitive programming.
Generates random data, runs both brute-force and optimized solutions,
compares outputs to find bugs.
"""
import subprocess
import random
import sys
import os
import tempfile

# ============ In-process stress test (Python) ============

def stress_test(solve_func, brute_func, gen_func, tests=10000, verbose=True):
    """Run stress test comparing solve_func vs brute_func.
    gen_func() returns test input.
    Returns True if all tests pass.
    """
    for t in range(tests):
        data = gen_func()
        try:
            ans1 = solve_func(data)
        except Exception as e:
            if verbose:
                print(f"Test {t}: solve crashed on {data}: {e}")
            return False
        ans2 = brute_func(data)
        if ans1 != ans2:
            if verbose:
                print(f"MISMATCH on test {t}!")
                print(f"  Input:  {data}")
                print(f"  Solve:  {ans1}")
                print(f"  Brute:  {ans2}")
            return False
    if verbose:
        print(f"All {tests} stress tests passed!")
    return True

# ============ Subprocess stress test (for compiled programs) ============

def stress_test_subprocess(gen_exe, solve_exe, brute_exe, tests=1000):
    """Stress test using subprocess for compiled programs.
    gen_exe: data generator (outputs to stdout)
    solve_exe: optimized solution (reads stdin, writes stdout)
    brute_exe: brute-force solution (reads stdin, writes stdout)
    """
    for t in range(tests):
        # Generate input
        gen_proc = subprocess.run([gen_exe], capture_output=True, text=True)
        input_data = gen_proc.stdout
        # Run both solutions
        solve_proc = subprocess.run([solve_exe], input=input_data,
                                    capture_output=True, text=True)
        brute_proc = subprocess.run([brute_exe], input=input_data,
                                    capture_output=True, text=True)
        if solve_proc.stdout != brute_proc.stdout:
            print(f"MISMATCH on test {t}!")
            print(f"Input:\n{input_data}")
            print(f"Solve output:\n{solve_proc.stdout}")
            print(f"Brute output:\n{brute_proc.stdout}")
            # Save the failing test case
            with open("failing_test.in", "w") as f:
                f.write(input_data)
            return False
    print(f"All {tests} subprocess stress tests passed!")
    return True

# ============ Python-only subprocess stress test ============

def stress_test_python(gen_script, solve_script, brute_script, tests=1000):
    """Stress test for Python solutions using subprocess.
    Each script is a .py file path.
    gen_script outputs test data to stdout.
    solve_script and brute_script read from stdin, write to stdout.
    """
    for t in range(tests):
        gen_proc = subprocess.run(
            [sys.executable, gen_script],
            capture_output=True, text=True
        )
        input_data = gen_proc.stdout
        solve_proc = subprocess.run(
            [sys.executable, solve_script],
            input=input_data, capture_output=True, text=True
        )
        brute_proc = subprocess.run(
            [sys.executable, brute_script],
            input=input_data, capture_output=True, text=True
        )
        if solve_proc.stdout != brute_proc.stdout:
            print(f"MISMATCH on test {t}!")
            print(f"Input:\n{input_data}")
            print(f"Solve: {solve_proc.stdout!r}")
            print(f"Brute: {brute_proc.stdout!r}")
            with open("failing_test.in", "w") as f:
                f.write(input_data)
            return False
    print(f"All {tests} Python stress tests passed!")
    return True

if __name__ == "__main__":
    # Example: stress test a sorting function
    def gen():
        n = random.randint(1, 20)
        return [random.randint(-100, 100) for _ in range(n)]

    def solve(data):
        return sorted(data)

    def brute(data):
        # Simple bubble sort
        arr = data[:]
        for i in range(len(arr)):
            for j in range(len(arr) - 1 - i):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

    ok = stress_test(solve, brute, gen, 1000)
    assert ok
    print("stress-test: ALL TESTS PASSED")

```

**PyPy 提示**: Python subprocess对拍适合慢算法。对于C++程序，编译后用subprocess调用exe更快。也可用shell脚本while循环+diff。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 每次测试=gen+brute+solve的时间 |
| 空间 | 取决于数据规模 |

### 局限

暴力解法必须保证正确。数据生成器需覆盖边界情况。大数据可能超时。无法发现两个解法都有相同bug的情况。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| OI-Wiki | contest/common-tricks | 2 | 官方对拍教程与模板 | [https://oi-wiki.org/contest/common-tricks/](https://oi-wiki.org/contest/common-tricks/) |

## Pitfalls · 易错点

- 数据生成器质量决定测试效果：需覆盖边界（n=1, n=最大值, 全相同等）
- testlib的rnd保证跨平台可复现，Python random需固定seed
- 暴力解法本身可能有bug
- 浮点比较需设置epsilon
- 两个解法可能有相同的错误（巧合一致）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/contest/common-tricks/](https://oi-wiki.org/contest/common-tricks/)
- OI Wiki ✓ [https://oi-wiki.org/tools/testlib/generator/](https://oi-wiki.org/tools/testlib/generator/)
