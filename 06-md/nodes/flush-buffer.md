---
id: flush-buffer
name: 缓冲区刷新
group: G-E-1
stage: basic
priority: P1
depth_tier: standard
---

# 缓冲区刷新

> 交互题必须每次输出后刷新缓冲区：C++ fflush(stdout)/std::endl，Python sys.stdout.flush() 或 print(..., flush=True)，否则 Idleness limit exceeded

<!-- 元信息: id=flush-buffer · group=G-E-1 · stage=basic · priority=P1 · depth_tier=standard -->

## What · 是什么

缓冲区刷新（flush）：程序输出先进入用户态缓冲区，由系统按块（如 4/8KB）或行缓冲刷出。普通题依赖程序结束时统一刷新即可；但**交互题**中，评测机等你输出后再给输入，你的输出若滞留在缓冲区，对方永远收不到 → 超时（Idleness Limit Exceeded, ILE）。因此交互题每次输出『询问/答案』后必须显式刷新：C++ `fflush(stdout)` 或 `std::endl`；Python `sys.stdout.flush()` 或 `print(x, flush=True)`。

## Why · 为什么

### 直觉 · Intuition

普通批处理题：评测机读文件，文件在程序结束时就写完了，所以无所谓何时刷新。交互题：评测机与你的程序『对话』，你发一句、它回一句，你发的话必须立刻送达对方——而输出缓冲区会把它扣住直到攒够一块或程序结束，双方死等。

### 原理 · Principle

stdout 默认对终端行缓冲、对管道/文件全缓冲（4KB/8KB 一块）。Python 的 print 写 TextIO 后内容先进 BufferWriter，flush 才真正 write 到 fd。交互题协议：你输出一行后评测程序读取该行并依据它产生输入行。若不 flush，评测程序读不到你的行，卡在 read，直到你的程序结束才 flush → 直接 ILE。多组数据时若已能提前得到答案，仍要读完所有输入避免读入混乱。Python 用 flush=True 或 sys.stdout.flush()；C++ 关 sync 后 std::endl 强制 flush、'
' 不刷。

### 历史 · History

交互题是 OI/ICPC 的常见题型（如 Codeforces 交互题、UOJ APIO2016 Gap）。OI Wiki contest/interaction 页明确警告：『选手每一次输出后都需要刷新缓冲区，否则会引起 Idleness limit exceeded 错误』，并指出不要使用快读（会破坏逐行交互读入的节奏）。Python 交互模板用 print(..., flush=True) 是社区标准。

## How · 实现

### 伪代码

```python
# Python 交互模板
def ask(x):
    print(f'? {x}', flush=True)     # 每次输出必 flush
    return int(input())

ans = ask(42)
print(f'! {ans}', flush=True)       # 最终答案也要 flush

# C++ 对应
# cout << "? " << x << endl;  或  printf(...); fflush(stdout);
```

### Python 实现

```python
import sys


def main():
    # 自测：模拟评测机交互（猜数字）
    import io
    log = []

    def fake_judge(q):
        """模拟评测机：对每次询问立即给回应"""
        log.append(q)
        if q < 50:
            return 'higher'
        if q > 50:
            return 'lower'
        return 'equal'

    # 手动模拟：输出立即 flush（此处直接写 log 模拟）
    lo, hi = 1, 100
    res = None
    for _ in range(10):
        mid = (lo + hi) // 2
        r = fake_judge(mid)
        if r == 'higher':
            lo = mid + 1
        elif r == 'lower':
            hi = mid - 1
        else:
            res = mid
            break
    assert res == 50
    # 验证 flush=True 存在（print 关键字参数合法性）
    import contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        print('? 3', flush=True)
    assert buf.getvalue() == '? 3\n'
    # sys.stdout.flush 可调用
    assert callable(sys.stdout.flush)
    print("flush-buffer OK")


if __name__ == "__main__":
    main()

```

**PyPy 提示**: PyPy 的 print 与 sys.stdout.flush 行为与 CPython 一致；flush=True 同样适用。交互题中 PyPy 的 input() 逐行读没问题（禁止用 read() 一次读）。注意 PyPy 对 buffered output 的块大小可能不同，但显式 flush 后无差别。交互题绝不要用 sys.stdin.buffer.read()（会读尽所有输入，破坏交互）。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | flush 是系统调用，每次 O(1) 但开销存在；交互题询问次数受限（如 100 次内）时无碍 |
| 空间 | O(1) |

### 局限

只在交互题必须；普通题频繁 flush 反而拖慢（批量输出用 join 一次写）。部分交互题评测机允许一次输出多行询问再统一读答案（queries in batch），仍需在输出块后 flush 一次。交互读入不能用快读 read()；若题目含多组数据且程序提前知道答案，仍必须读完所有输入再输出。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Codeforces | 679A | 1600 | Bear and Prime 100：交互猜质因子，经典入门交互题，输出后必须 flush | [https://codeforces.com/problemset/problem/679/A](https://codeforces.com/problemset/problem/679/A) |

## Pitfalls · 易错点

- 漏 flush 导致 ILE（Idleness Limit Exceeded），是最常见交互题失误
- print(..., end='') 后再 print 第二次输出同一行时，两段都要在同一 flush 前拼接或用 flush=True
- C++ 关 sync_with_stdio(false) 后 ' ' 不刷缓冲区，必须 std::endl 或显式 fflush
- 交互题误用 sys.stdin.buffer.read() 一次性读入会死等或读乱
- 批量输出多个询问时要在所有输出后只 flush 一次，别每条都 flush（减少系统调用），但每条之间不可依赖对方先回

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/contest/interaction/](https://oi-wiki.org/contest/interaction/)
- OI Wiki ✓ [https://oi-wiki.org/contest/problems/](https://oi-wiki.org/contest/problems/)
