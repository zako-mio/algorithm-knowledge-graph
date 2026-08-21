---
id: fast-output
name: 快速输出
group: G-E-1
stage: intermediate
priority: P1
depth_tier: standard
---

# 快速输出

> 整数快速输出：C++ 用 putchar/fwrite 攒缓冲；Python 用 '\n'.join(map(str, ...)) 一次 write，避免逐行 print() 慢

<!-- 元信息: id=fast-output · group=G-E-1 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

快速输出与快速读入配套。C++ 侧：把结果攒进大缓冲区，最后 fwrite 一次写出（或 putchar 逐字符）；Python 侧：不要逐行 print()，而是收集所有结果字符串后 `sys.stdout.write('\n'.join(map(str, ans)))` 一次输出（可补尾换行）。print() 每次调用都有格式化 + 缓冲刷新开销，10^5 行以上输出在 CPython 会明显变慢。交互题则相反，需要每次输出后主动 flush（见 flush-buffer 节点）。

## Why · 为什么

### 直觉 · Intuition

print() 的每次调用都有 Python 层开销（参数格式化、调用 print 函数、写流）；而 join 在 C 层把千万条字符串拼接成一块再一次 write，Python 层只做一次调用。输出量大时差距达到数倍到十几倍。

### 原理 · Principle

sys.stdout.write(s) 接收完整字符串；'\n'.join(iterable) 在 C 层完成拼接。map(str, nums) 惰性转字符串列表；join 需要 list 或可迭代。要点：把『每条结果换行』放在 join 的分隔符里，最后一次性写。C++ 对应：ostringstream / 手动字符缓冲 + fwrite，避免每次输出都做系统调用。注意 stdout 是块缓冲（非 tty 时 8KB），普通 print 不会每次系统调用，但 Python 层逐次 print 的开销仍大。

### 历史 · History

OI Wiki contest/io 页的 fwrite 输出、以及 Python 社区『用 join 代替逐行 print』的经验，都是 IO 优化的标准结论。现代 OJ 上 CPython 题目若输出 10^6 行，不 join 基本 TLE。

## How · 实现

### 伪代码

```python
# 批量输出模板
ans = []
for ...: ans.append(str(result))   # 或 ans.append(f'{x} {y}')
sys.stdout.write('\n'.join(ans))
# 需要结尾换行时
sys.stdout.write('\n'.join(ans) + '\n')

# 若结果已全是整数：
sys.stdout.write('\n'.join(map(str, nums)) + '\n')
```

### Python 实现

```python
import sys


def main():
    # 自测：用 StringIO 捕获 stdout 对比 join 与逐行输出结果一致
    import io
    nums = list(range(5))
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    sys.stdout.write('\n'.join(map(str, nums)) + '\n')
    sys.stdout = old
    assert buf.getvalue() == '0\n1\n2\n3\n4\n'
    # 多 token 每行：如 (i, i*i)
    buf = io.StringIO()
    sys.stdout = buf
    sys.stdout.write('\n'.join(f'{i} {i*i}' for i in range(3)) + '\n')
    sys.stdout = old
    assert buf.getvalue() == '0 0\n1 1\n2 4\n'
    # 空输出安全
    buf = io.StringIO()
    sys.stdout = buf
    sys.stdout.write('\n'.join(map(str, [])))
    sys.stdout = old
    assert buf.getvalue() == ''
    print("fast-output OK")


if __name__ == "__main__":
    main()

```

**PyPy 提示**: PyPy 的 print 比 CPython 快，但输出量仍建议 join 批量写；join 在 PyPy 下同样 C 层高效。注意 PyPy 的 sys.stdout.write 行为一致。生成器表达式给 join 会先物化为 list 再拼接，超大输出（10^7 行）时中间 list 内存翻倍，可用 list 推导 + 分块多次 write 折中。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 一次 write O(总输出字节)；join 拼接 O(总字节) |
| 空间 | O(总输出字节)（结果字符串整体驻留） |

### 局限

交互题不能批量输出（必须逐次 flush）；输出本身占内存，10^7 行级可分批 write 控制峰值。对浮点格式化的 join 注意精度一致（str 与 format 结果）。stdout 重定向到文件时是块缓冲，普通 print 也还行，但 Python 层逐次调用开销依然在。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3367 | 3 | 并查集模板：每次查询输出一行 Y/N，m 达 2e5 必须用 join 批量输出 | [https://www.luogu.com.cn/problem/P3367](https://www.luogu.com.cn/problem/P3367) |
| Luogu | P4779 | 4 | 最短路径标准版：输出 n 个距离，与快读配套使用 | [https://www.luogu.com.cn/problem/P4779](https://www.luogu.com.cn/problem/P4779) |

## Pitfalls · 易错点

- join 里漏加结尾换行，部分 OJ 严格判重会导致 WA
- 逐行 print() 在输出 10^6 行时在 CPython 会 TLE，忘记换 join
- map(str, nums) 里 nums 若含 float 会输出科学计数法，需先格式化
- 超大输出一次性 join 内存峰值高，分块处理
- 交互题误用批量输出 + 不 flush，会导致 ILE（见 flush-buffer）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/contest/io/](https://oi-wiki.org/contest/io/)
