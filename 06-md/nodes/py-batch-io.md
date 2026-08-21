---
id: py-batch-io
name: Python批量读入
group: G-E-3
stage: basic
priority: P0
depth_tier: deep
---

# Python批量读入

> sys.stdin.read().split()一次性读入全部输入再map(int,...)，避免逐行input()超时

<!-- 元信息: id=py-batch-io · group=G-E-3 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

Python 批量读入：用 sys.stdin.read() 一次性读取全部标准输入为字符串，再 .split() 按空白符切分为字符串列表，最后 map(int, ...) 转为整数迭代器。相比逐行 input()，省去了大量函数调用与字符串解码开销，对 10^5~10^6 级输入有 5-20 倍加速。是 Python 竞赛解决 IO 瓶颈的核心手段。也可用 sys.stdin.buffer.read() 读字节再 split 略快。

## Why · 为什么

### 直觉 · Intuition

input() 每次调用都触发一次系统级 readline + 解码 + 末尾换行剥离，调用 10^6 次就是 10^6 次系统调用开销。而 read() 一次读完所有内容到内存，split() 在 C 层一次性扫描切分，map(int,...) 在 C 层逐个转换——整条链路都在 C 层运行，Python 解释器循环几乎不参与，故极快。

### 原理 · Principle

sys.stdin 是 TextIOWrapper，read() 返回整个缓冲区字符串。str.split() 无参时按任意空白符（空格/制表/换行）切分，返回 list。map(int, lst) 返回惰性迭代器，按需转换。组合 data=sys.stdin.read().split(); a=list(map(int,data)) 一次拿到全部整数。读取字节更快：data=sys.stdin.buffer.read().split() 得到 bytes 列表，int(b) 可直接解析 bytes。

### 历史 · History

Python 在 OI 早期因 input() 慢而声名狼藉。批量读入模式在社区（OI Wiki、洛谷题解）中普及后，Python 通过大输入测试成为可能。PyPy 的 input() 相对快但 read() 仍更优。

## How · 实现

### 伪代码

```python
import sys
data = sys.stdin.read().split()    # 一次性读全部
it = iter(data)
# 按需取数: next(it) 取下一个 token
n = int(next(it))
a = [int(next(it)) for _ in range(n)]
# 或全部转 int: nums = list(map(int, data))
```

### Python 实现

```python
# Python 批量读入模板（含自测）
import sys

def solve(data_lines):
    """模拟从字符串输入求解: 第一行n, 第二行n个数求和"""
    import io
    sys.stdin = io.StringIO(data_lines)
    data = sys.stdin.read().split()
    it = iter(data)
    n = int(next(it))
    total = 0
    for _ in range(n):
        total += int(next(it))
    return total

def main_template():
    """竞赛通用模板：一次性读入全部 token"""
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    n = int(next(it))
    a = [int(next(it)) for _ in range(n)]
    print(sum(a))

if __name__ == "__main__":
    # 自测：模拟输入 "5\n1 2 3 4 5\n"
    inp = "5\n1 2 3 4 5\n"
    assert solve(inp) == 15
    # 多行混合空白也正确
    inp2 = "3\n10  20\n30"
    assert solve(inp2) == 60
    # 空输入安全
    assert solve("0\n") == 0
    print("py-batch-io OK")

```

**PyPy 提示**: PyPy 下 input() 已比 CPython 快不少（有优化），但 sys.stdin.buffer.read().split() 仍是 IO 上限解法。注意 PyPy 读 bytes 后 int(b) 支持 bytes 参数。极大输入（>10^7 个数）注意内存，必要时分块读。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(N) 读取+切分+转换，常数极小（C 层完成） |
| 空间 | O(N) 存全部 token 字符串/整数 |

### 局限

1) 一次性 read() 需全部输入就绪，交互题不能用（交互题需逐行 fflush）；2) 输入量 >10^7 token 时内存压力大，可改 sys.stdin.readline() 逐行；3) 读全部到内存若题目流式处理会浪费。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1001 | 1 | 批量读入模板起点 | [https://www.luogu.com.cn/problem/P1001](https://www.luogu.com.cn/problem/P1001) |
| Luogu | P2439 | 3 | sys.stdin.read().split() 读二维矩阵 | [https://www.luogu.com.cn/problem/P2439](https://www.luogu.com.cn/problem/P2439) |

## Pitfalls · 易错点

- 交互题误用 read() 一次性读全部——交互题必须逐行交互并 fflush(stdout)
- next(it) 取超 token 时抛 StopIteration，大输入调试难定位；建议加边界检查
- 用 input() 逐行读 10^6 行在 CPython 直接 TLE，必须改 read()
- 忘记 sys.stdin.buffer.read() 返回 bytes，直接 .split() 得 bytes 列表需 int(b) 而非 int(str)
- 读到的 data 不转 int 就参与算术运算导致 TypeError（split 返回 str）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/lang/python/](https://oi-wiki.org/lang/python/)
- web ✓ [https://docs.python.org/3/library/sys.html#sys.stdin](https://docs.python.org/3/library/sys.html#sys.stdin)
