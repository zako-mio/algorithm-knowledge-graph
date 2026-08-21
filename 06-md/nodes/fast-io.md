---
id: fast-io
name: 快速读入
group: G-E-1
stage: basic
priority: P0
depth_tier: deep
---

# 快速读入

> 整数快速读入：C++ 用 getchar/fread；Python 用 sys.stdin.buffer.read().split() 批量读入 + map(int,...)，比逐行 input() 快 5-20 倍

<!-- 元信息: id=fast-io · group=G-E-1 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

快速读入是 IO 优化的核心。对 C++：scanf 已不慢，但 10^6 级整数用 getchar()/fread 手写解析可再快数倍。对 Python（CPython 尤甚）：input() 逐行读 10^5~10^6 行会直接 TLE，必须用 `sys.stdin.buffer.read().split()` 一次性读全部字节并切分，再用 map(int, tokens) 转换。这是 Python 竞赛的『保命』模板，几乎所有大规模输入题都应默认使用。进阶可手写字节级解析循环（快读函数）或配合内存映射。PyPy 的 input() 相对快，但 read() 批量读仍是上限解法。

## Why · 为什么

### 直觉 · Intuition

每次 input() 都触发：系统调用 → 读一行 → 字节解码成 str → 剥离换行。10^6 次 input() 就是 10^6 次系统调用。而 read() 一次把整个文件读入内存（1 次系统调用），split() 在 C 层按空白切分，map(int) 在 C 层转换——整条链路都不经过 Python 层循环，所以数量级更快。

### 原理 · Principle

sys.stdin.buffer 是 BufferedIOBase，read() 返回 bytes；bytes.split() 无参按任意 ASCII 空白切分为 bytes 列表；int(b) 可直接解析 bytes（Python 3）。组合起来 `it = iter(sys.stdin.buffer.read().split()); n = int(next(it))` 逐 token 取用，或 `arr = list(map(int, data))` 全量转 int。手写快读：循环逐字节判断 48<=c<=57 累加 num=num*10+(c-48)，处理符号位与空白分隔，把『解码+切分+转换』压成一次 C 层遍历，进一步省掉 split 产生的临时对象。C++ 侧 fread 一次读入大缓冲区后自行解析是同样的思想。

### 历史 · History

OI Wiki 的 contest/io 页系统介绍了 C++ 的 ios::sync_with_stdio(false)、getchar/fread/mmap 三级快读；lang/python 页强调 Python 用 input().split() 与列表推导式。Python 快读模板（read().split() + map(int)）是社区长期验证的标准写法，对大数据输入是必选而非可选项。

## How · 实现

### 伪代码

```python
# 模板1：read().split() + 迭代器取 token（推荐）
import sys
data = sys.stdin.buffer.read().split()
it = iter(data)
n = int(next(it))
a = [int(next(it)) for _ in range(n)]

# 模板2：全量转 int
nums = list(map(int, sys.stdin.buffer.read().split()))

# 模板3：手写字节级快读（最大性能，可选）
def fast_ints():
    data = sys.stdin.buffer.read()
    num = 0; sign = 1; innum = False; out = []
    for c in data:
        if 48 <= c <= 57:
            num = num * 10 + (c - 48); innum = True
        else:
            if innum:
                out.append(sign * num); num = 0; sign = 1; innum = False
            if c == 45: sign = -1
    if innum: out.append(sign * num)
    return out
```

### Python 实现

```python
import sys


def solve(data_lines):
    import io
    sys.stdin = io.StringIO(data_lines)
    data = sys.stdin.buffer.read().split() if hasattr(sys.stdin, 'buffer') else sys.stdin.read().split()
    it = iter(data)
    n = int(next(it))
    a = [int(next(it)) for _ in range(n)]
    return sum(a)


def fast_ints():
    data = sys.stdin.buffer.read()
    num = 0
    sign = 1
    innum = False
    out = []
    for c in data:
        if 48 <= c <= 57:
            num = num * 10 + (c - 48)
            innum = True
        else:
            if innum:
                out.append(sign * num)
                num = 0
                sign = 1
                innum = False
            if c == 45:
                sign = -1
    if innum:
        out.append(sign * num)
    return out


def main():
    # 自测模板1（StringIO 注入）
    assert solve("5\n1 2 3 4 5\n") == 15
    assert solve("3\n10  20\n30") == 60
    # 手写快读：换行/空格/负数混排
    import io
    saved = sys.stdin
    sys.stdin = io.TextIOWrapper(io.BytesIO(b"4  -2 33 -100\n"))
    got = fast_ints()
    sys.stdin = saved
    assert got == [4, -2, 33, -100]
    print("fast-io OK")


if __name__ == "__main__":
    main()

```

**PyPy 提示**: PyPy 的 input() 实现比 CPython 快很多（内建缓冲与行缓冲优化），但 read().split() 仍是 IO 瓶颈的最优解。PyPy 下 bytes.split() 与 int(bytes) 均可用。手写快读在 PyPy 下收益小于 CPython（PyPy 字节循环不算慢），且代码略长，普通题用模板1即可；只有 IO 量极大（10^7 级 token）才考虑手写。注意：PyPy 读 sys.stdin.buffer.read() 后 int(b) 支持 bytes 参数，无需先 decode。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | read()+split()+map 全程 C 层 O(总字节数)，常数极小；手写快读单遍 O(总字节数) |
| 空间 | O(总输入字节) 存全部 token；手写快读 O(输出 token 数) |

### 局限

一次性 read() 要求输入全部就绪——交互题不可用（须逐行交互+flush）。内存：10^7 级 token 的 split 会生成大量 bytes 对象，内存峰值高，可改用逐行 readline 或手写快读避免中间对象。读浮点不用此套路（float() 可解析 bytes，但大浮点输入建议逐行）。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1001 | 1 | A+B Problem：快读模板的起点，验证 read().split() 基本用法 | [https://www.luogu.com.cn/problem/P1001](https://www.luogu.com.cn/problem/P1001) |
| Luogu | P4779 | 4 | 单源最短路径(标准版)：n,m 达 1e5，Python 必须配快读+快出否则必 TLE | [https://www.luogu.com.cn/problem/P4779](https://www.luogu.com.cn/problem/P4779) |

## Pitfalls · 易错点

- 交互题误用 read() 一次性读入会死等，必须逐行读+flush
- input() 逐行读 10^6 行在 CPython 直接 TLE，必须换 read().split()
- sys.stdin.buffer.read() 返回 bytes，int(b) 可直接用；若先 .decode() 再 split 会多一次拷贝
- next(it) 超界抛 StopIteration，大量 token 时注意别多取
- 手写快读漏处理负数符号、或对非数字字符（如行末 CRLF 的 \r）判定错误
- read() 空输入时 split() 返回空列表，直接 next 会崩，需判空

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/contest/io/](https://oi-wiki.org/contest/io/)
- OI Wiki ✓ [https://oi-wiki.org/lang/python/](https://oi-wiki.org/lang/python/)
