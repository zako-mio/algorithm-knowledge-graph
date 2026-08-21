---
id: constant-opt
name: 常数优化
group: G-E-1
stage: intermediate
priority: P1
depth_tier: standard
---

# 常数优化

> 算法正确但常数过大超时的优化：局部性/循环展开（C++）、Python 局部变量绑定、避免属性访问、列表推导、预分配数组、用 int 位集等

<!-- 元信息: id=constant-opt · group=G-E-1 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

常数优化：不改变渐近复杂度，降低每步操作的实际耗时。C++ 侧：O2 优化开关、常量折叠、循环展开、代码布局、局部性（cache 友好）、用引用/数组避免 STL 开销。Python 侧（更关键）：把频繁使用的全局名/方法名绑定为局部变量（如 `append = lst.append`）、用列表推导代替显式循环、预分配数组、用 int 当位集、避免重复属性查找与函数调用、避免在热循环里用 dict/list 的慢操作、适当用 PyPy 特性。Python 常数优化的收益常是数量级的，可决定 TLE/AC。

## Why · 为什么

### 直觉 · Intuition

Python 每条语句都有解释器调度开销：名字查找（LOCAL/CELL/GLOBAL/BUILTIN 依次查）、属性访问（getattr）、函数调用（压栈）。热循环里这些微小开销叠加起来就是几倍差距。而列表推导、join、map 等在 C 层执行整段循环，解释器只跑一圈。

### 原理 · Principle

1) 局部变量快于全局：字节码 LOAD_FAST 快于 LOAD_GLOBAL；函数内 `x = 大量重复的对象` 并复用。2) 绑定方法：`push = stack.append` 后 `push(v)` 免去每次 `stack.append` 的属性查找。3) 列表推导：`[f(x) for x in it]` 在 C 层循环，快于 `for` + `append`（Python 层循环）。4) 预分配：`[0]*n` 一次性分配。5) 内建优先：`sum`, `max`, `min`, `sorted`, `count` 都是 C 循环。6) 局部性：顺序访问数组/列表比随机访问 cache 命中高；Python list 是连续内存的引用数组。7) 字符串拼接用 join 而非 +=。C++ 侧同理：连续内存、少分配、编译器优化。

### 历史 · History

OI Wiki 的 lang/optimizations 页介绍 C++ 的 O2、常量折叠、死代码消除、循环展开、代码布局；contest/common-tricks 页讲局部性原理。Python 社区则有长期积累的『性能技巧』清单（局部绑定、推导式、内建函数）。对纯 Python 选手，常数优化等同于『把 Python 写快』，重要性不亚于算法本身。

## How · 实现

### 伪代码

```python
# Python 核心技巧
# 1) 局部绑定热循环方法
push = out.append
for x in it:
    if cond: push(x)

# 2) 列表推导替代显式 append
squares = [x*x for x in data]   # C 层循环

# 3) 预分配
res = [0] * n

# 4) 内建优先
total = sum(data)

# 5) 字符串 join 而非 +=（在循环里）
s = ''.join(parts)

# 6) 局部变量引用模块函数
from math import sqrt
# 循环内用 sqrt(x)（全局已绑定）
```

### Python 实现

```python
import time


def slow_version(data):
    out = []
    for x in data:
        if x % 2 == 0:
            out.append(x * x)
    return out


def fast_version(data):
    out = []
    push = out.append
    for x in data:
        if x % 2 == 0:
            push(x * x)
    return out


def fast_version2(data):
    return [x * x for x in data if x % 2 == 0]


def main():
    data = list(range(1000))
    a = slow_version(data)
    b = fast_version(data)
    c = fast_version2(data)
    assert a == b == c
    # 预分配
    res = [0] * len(data)
    assert len(res) == len(data)
    # 内建 vs 手写循环结果一致
    assert sum(data) == sum(x for x in data)
    # 快速基准（仅展示，不比较严格耗时）
    import random
    big = list(range(10**6))
    t0 = time.perf_counter(); s = sum(big); t1 = time.perf_counter()
    # join 快于 += 拼串
    parts = [str(i) for i in range(1000)]
    s_join = ''.join(parts)
    assert s_join.startswith('0')
    print("constant-opt OK")


if __name__ == "__main__":
    main()

```

**PyPy 提示**: PyPy 的 JIT 会做循环优化与内联，局部绑定/推导式的收益比 CPython 小（JIT 已优化），但仍是良好习惯。PyPy 下字符串 join、int 大数、dict 等实现不同。PyPy 启动慢但循环快，CPU 密集任务在 PyPy 下可快 2-5 倍；IO 密集任务两边都需快读快出。对纯 Python 竞赛（如洛谷/牛客允许 Python），优先 PyPy3。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 渐近不变；常数通常可降 2~10 倍（CPython 场景收益大） |
| 空间 | 不变或略增（预分配/临时列表） |

### 局限

常数优化无法挽救错误的复杂度（TLE 根因仍要先看算法）；过度优化伤可读性且易引入 bug，先写清晰版本再对热路径优化。PyPy 与 CPython 性能特征不同，代码在两者间有差异；不要把 C++ 的优化思路（如循环展开）直接搬到 Python（解释器下收益小）。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P4779 | 4 | 最短路径标准版：Python 需 heap 局部绑定+快读快出+预分配，全套常数优化才能过 | [https://www.luogu.com.cn/problem/P4779](https://www.luogu.com.cn/problem/P4779) |

## Pitfalls · 易错点

- 在函数外（模块级）做热循环，变量走 GLOBAL 查找，慢；应放入函数内
- for i in range(len(a)): 里反复 a[i] 索引与属性查找，可先用局部变量/迭代
- 热循环里 `len(lst)` 每次调用，可提前 len_=len(lst) 或直接迭代
- 字符串循环拼接用 += 是 O(n^2) 陷阱，必须 join
- 过度微优化导致可读性差、难调试；先测量再优化（profile）
- 把 print 放在热循环里逐次调用是常见 TLE 原因，改用批量输出

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/lang/optimizations/](https://oi-wiki.org/lang/optimizations/)
- OI Wiki ✓ [https://oi-wiki.org/contest/common-tricks/](https://oi-wiki.org/contest/common-tricks/)
