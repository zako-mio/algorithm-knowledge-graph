---
id: io-optimization
name: I/O优化策略
group: G-E-8
stage: basic
priority: P1
depth_tier: standard
---

# I/O优化策略

> 关闭同步/快读快写、Python 批量读入 sys.stdin.buffer，I/O 瓶颈识别与优化决策

<!-- 元信息: id=io-optimization · group=G-E-8 · stage=basic · priority=P1 · depth_tier=standard -->

## What · 是什么

I/O 优化指针对输入输出耗时优化读入读出的手段。C++ 侧：ios::sync_with_stdio(false) 关闭与 C 流同步、cin.tie(nullptr) 解除与 cout 关联、快读（getchar 手写整数解析）与 fread/fwrite 整块读写、mmap 映射（不推荐）。Python 侧：sys.stdin.buffer.read() 一次读完整个输入再 split 是最有效手段，输出用 '
'.join 一次 write；避免逐行 input()/print()。I/O 优化决策的核心是先判断瓶颈是不是 I/O（大数据量、高 TLE 率、逐字符读入时），再做针对性优化。

## Why · 为什么

### 直觉 · Intuition

默认的 cin/cout 每次都要与 C 缓冲同步（为了兼容 scanf/printf），输入时还要 flush cout——这些是安全性的代价而非性能需求。Python 的 input() 逐行调用且带解码，print() 逐次 flush，在高频读写下开销巨大。批量读写的思想：一次读入整块（一次系统调用）内存里解析，比上千次小读取快一个数量级。

### 原理 · Principle

C++ 关闭同步后 cin/cout 不再向 C 缓冲写，解除 tie 后输入不再触发 flush；快读把 getchar 的逐字符解析手动合并进位，fread 用 1MB 缓冲一次读入后指针扫描（gc 宏）。Python 最优套路：data = sys.stdin.buffer.read().split() 得到 bytes 列表一次解析；输出 out.append(...) 最后 sys.stdout.write('\n'.join(out))。原理是系统调用次数从 O(读入元素数) 降到 O(1)。评测环境的 I/O 文件是管道/文件，读入速率远高于终端交互场景。

### 历史 · History

OI Wiki 的 contest/io 页系统梳理 C++ 流同步优化、getchar/fread/mmap 三级快读方案与实现细节，并给出 Luogu P10815【模板】快速读入（n<=1e8）。Python 批量读入是语言特有优化，配合 PyPy 使用效果最佳。

## How · 实现

### 伪代码

```python
C++: ios::sync_with_stdio(false); cin.tie(nullptr);
快读: gc() 逐字符解析整数，fread 缓冲
Python: data = sys.stdin.buffer.read().split()
  it = iter(data); n = int(next(it)); ...
输出: sys.stdout.write('\n'.join(out))
```

### Python 实现

```python
import sys
import time


def slow_read():
    # 反例：逐行 input() 在 1e6 级数据上会很慢
    n = int(input())
    s = 0
    for _ in range(n):
        s += int(input())
    return s


def fast_read():
    data = sys.stdin.buffer.read().split()
    if not data:
        return 0
    n = int(data[0])
    s = sum(map(int, data[1:1 + n]))
    return s


def main():
    import io
    # 构造 1e6 个随机数的输入，测批量读入 vs 逐行
    n = 1000000
    import random
    random.seed(42)
    arr = [random.randint(0, 10 ** 9) for _ in range(n)]
    payload = str(n) + "\n" + "\n".join(map(str, arr)) + "\n"
    sys.stdin = io.TextIOWrapper(io.BytesIO(payload.encode()), encoding="utf-8")

    t0 = time.perf_counter()
    # 逐行读会非常慢，这里只做 1e4 行示范
    old = sys.stdin
    sys.stdin = io.StringIO(payload)
    s = 0
    n2 = int(sys.stdin.readline())
    for _ in range(n2):
        s += int(sys.stdin.readline())
    t1 = time.perf_counter()
    sys.stdin = old

    # 批量读入
    sys.stdin = io.TextIOWrapper(io.BytesIO(payload.encode()), encoding="utf-8")
    t2 = time.perf_counter()
    s2 = fast_read()
    t3 = time.perf_counter()
    sys.stdin = old

    print(f"line-by-line(1e6): {t1 - t0:.2f}s  sum={s}")
    print(f"buffer.read(1e6):  {t3 - t2:.2f}s  sum={s2}")
    assert s == s2
    print("OK (both sums equal)")


if __name__ == "__main__":
    main()

```

**PyPy 提示**: PyPy 下 sys.stdin.buffer.read().split() + map(int, ...) 是全 Python 方案里最快的读法；int(bytes) 在 PyPy 有 JIT 加速。输出用 bytes 拼接（b'\n'.join）比 str join 再编码略快。注意 C++ 的 mmap 不适用 Windows/CF 评测机，Python 也不建议模拟 mmap。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 读入整体 O(输入字节数)；系统调用从 O(n) 降到 O(1)（批量），解析仍 O(字节数) |
| 空间 | 批量读入需存整个输入 O(输入字节数)；fread 缓冲可 O(buffer 大小) |

### 局限

批量读入消耗内存 O(输入大小)，超大输入（几十 MB）要权衡；交互题禁止批量读入与快读（交互器依赖逐次 flush/读入，见 interaction-strategy）；Python 的批量读入不能用于需要边读边交互的场景。C++ 关同步后不能混用 cin 与 scanf（不保证顺序）。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P10815 | 2 | 【模板】快速读入：n<=1e8 求前缀和始终在 int 范围内，读入是唯一瓶颈 | [https://www.luogu.com.cn/problem/P10815](https://www.luogu.com.cn/problem/P10815) |
| 通用 | 大数据量题 | 2 | 读入 1e6 以上个整数且时限紧的题，先怀疑 I/O 瓶颈再优化算法 | [https://oi-wiki.org/contest/io/](https://oi-wiki.org/contest/io/) |
| LeetCode | 周赛（本地） | 1 | 单点输入场景无需优化；本地生成大数据自测时用批量读入验证性能 | [https://leetcode.cn/](https://leetcode.cn/) |

## Pitfalls · 易错点

- 逐行 input()/print() 在 1e6 级数据上常 TLE——第一优化永远是批量 read()
- int(bytes) 解析大数组时 map(int, data[1:]) 比列表推导更快且省内存
- 输出逐条 print() 会逐次 flush，应收集后一次 write
- C++ 关同步后误混 scanf/printf 导致顺序错乱
- 交互题用快读/批量读入导致 ILE（交互器等不到请求）
- 数据里有负数/前导零时快读实现必须正确处理符号

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/contest/io/](https://oi-wiki.org/contest/io/)
- oiwiki_raw ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/contest/io.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/contest/io.md)
