---
id: interactive-debug
name: 交互题调试
group: G-E-4
stage: advanced
priority: P3
depth_tier: brief
---

# 交互题调试

> 交互题对拍困难，需模拟交互过程；封装输入输出函数；静态查错能力重要

<!-- 元信息: id=interactive-debug · group=G-E-4 · stage=advanced · priority=P3 · depth_tier=brief -->

## What · 是什么

交互题(interactive problem)中选手程序与评测器(grader)通过标准输入输出交替通信。调试难点在于无法简单对拍——需模拟交互过程、封装 IO 函数、依赖静态查错和 grader 本地调试。

## Why · 为什么

### 直觉 · Intuition

普通题可对拍(同一输入两解比对)，交互题的输出会改变后续输入，无法简单对拍。

### 原理 · Principle

①封装 ask/answer 函数，所有交互经统一通道 ②每次输出后 fflush(stdout) 刷新缓冲区 ③用题目提供的 grader 头文件本地模拟评测器 ④多测时即使提前知道答案也须读完所有输入(否则 ILE) ⑤尽量一遍写对，培养静态查错能力。

### 历史 · History

IOI 早期已有交互题，2019年 NOI 系列连续出现两道(P5208/P5473)标志其回归。

## How · 实现

### 伪代码

```python
ask(x): print('? x'); flush(); return int(input())
answer(r): print('! r'); flush()
main: 二分/枚举 -> ask -> 判断 -> answer
```

### Python 实现

```python
import sys

def ask(x):
    """向评测器提问: x 是不是答案的一部分?"""
    print(f'? {x}', flush=True)
    resp = sys.stdin.readline().strip()
    return resp

def answer(val):
    """向评测器提交最终答案。"""
    print(f'! {val}', flush=True)

# 示例: 猜一个1~100之间的数(类似CF679A)
# 评测器回答 'yes'/'no'
def solve_guessing_game():
    lo, hi = 1, 100
    # 二分猜数
    while lo < hi:
        mid = (lo + hi) // 2
        resp = ask(mid)
        if resp == 'yes':
            answer(mid)
            return
        elif resp == 'too_small':
            lo = mid + 1
        else:  # too_large
            hi = mid - 1
    answer(lo)

# 本地自测: 模拟评测器
if __name__ == '__main__':
    # 模拟: 答案是42, 评测器回答 'too_small'/'too_large'/'yes'
    # 实际竞赛中由评测器回答, 这里仅演示封装结构
    print('Interactive debug template loaded.')
    print('ask(x): prints ?x, flush, reads response')
    print('answer(v): prints !v, flush')
    print('Rule: always flush after print; read all input for multi-test.')

```

**PyPy 提示**: 交互题 IO 频繁，PyPy 的 sys.stdin.readline 性能足够；不要用 input()(慢且可能不刷新)；每轮 print 必须 flush=True。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 取决于交互次数限制(通常 O(log N) 或 O(sqrt N)) |
| 空间 | O(1) 通常 |

### 局限

无法传统对拍；需手写 grader 模拟器；多测未读完输入导致 ILE；交互次数超限导致 WA/PLE。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Codeforces | 679A | 1600 | Bear and Prime 100: 50以内质数枚举判定质合数 | [https://codeforces.com/problemset/problem/679/A](https://codeforces.com/problemset/problem/679/A) |
| Codeforces | 843B | 2100 | Interactive LowerBound: 随机撒点+链表遍历 | [https://codeforces.com/problemset/problem/843/B](https://codeforces.com/problemset/problem/843/B) |

## Pitfalls · 易错点

- 忘记 fflush(stdout) → ILE (Idleness Limit Exceeded)
- 多测时提前知道答案就 return → 未读完输入 → ILE
- 交互次数超限 → WA (Codeforces) / PLE (UVa)
- 用快读(input优化)可能吞掉评测器输出导致交互错乱

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/contest/interaction/](https://oi-wiki.org/contest/interaction/)
