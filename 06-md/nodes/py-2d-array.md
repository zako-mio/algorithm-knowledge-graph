---
id: py-2d-array
name: 二维列表正确创建
group: G-E-3
stage: basic
priority: P0
depth_tier: deep
---

# 二维列表正确创建

> [[0]*n for _ in range(m)]创建独立行；[[0]*n]*m会导致所有行共享同一对象（引用陷阱）

<!-- 元信息: id=py-2d-array · group=G-E-3 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

Python 创建二维列表的正确方式是 [[0]*n for _ in range(m)]（列表推导式，每行独立对象）。错误方式 [[0]*n]*m 会让所有行指向同一个一维列表对象，修改一行其他行同步变化（引用陷阱）。根源：Python 赋值只传引用，[obj]*m 把同一对象复制 m 次引用。切片拷贝二维列表也只是浅拷贝，行仍共享。深拷贝需 copy.deepcopy 或逐行推导式重建。

## Why · 为什么

### 直觉 · Intuition

[0]*n 对不可变 int 是安全的（int 不可变，改不了）。但 [[0]*n]*m 是把同一个 [0]*n 列表对象的引用复制 m 次——就像把同一张纸抄 m 份地址，改一处全变。列表推导式 [[0]*n for _ in range(m)] 每次循环都新建一个 [0]*n，是 m 张独立的纸。

### 原理 · Principle

Python 中 [expr]*m 创建长度 m 的列表，元素均为同一对象引用（expr 只求值一次）。当 expr 是不可变值（int/str/tuple）时安全（无法原地修改）。当 expr 是可变对象（list）时危险：[[0]*3]*3 得 [[0,0,0],[0,0,0],[0,0,0]]，但三行 id 相同，改 vis[0][0] 则三行第 0 列全变。列表推导式 [[0]*3 for _ in range(3)] 每次迭代新建 [0]*3，三行 id 不同，独立修改。可用 id(x) 验证：错误法三行 id 相同，正确法三行 id 不同。

### 历史 · History

这是 Python 最经典的坑之一。OI Wiki Python 页用 id() 函数验证展示了引用陷阱：vis=[[0]*3]*3 改一行全变，引出列表推导式正确写法。几乎所有 Python 初学者都踩过此坑。

## How · 实现

### 伪代码

```python
# 正确：列表推导式，每行独立
grid = [[0]*n for _ in range(m)]
# 错误：引用陷阱，所有行共享
# grid = [[0]*n]*m  # 别这么做！
# 读入二维矩阵
mat = [[int(x) for x in input().split()] for _ in range(n)]
# 深拷贝
import copy
mat2 = copy.deepcopy(mat)
```

### Python 实现

```python
# 二维列表正确创建（含自测）
import copy

def make_wrong(m, n):
    """错误：引用陷阱"""
    return [[0] * n] * m

def make_right(m, n):
    """正确：列表推导式"""
    return [[0] * n for _ in range(m)]

if __name__ == "__main__":
    # 1) 引用陷阱演示
    wrong = make_wrong(3, 3)
    wrong[0][0] = 1
    # 错误法：改一行全行变
    assert wrong[0] == [1, 0, 0] and wrong[1] == [1, 0, 0] and wrong[2] == [1, 0, 0]

    # 2) 正确法：各行独立
    right = make_right(3, 3)
    right[0][0] = 1
    assert right[0] == [1, 0, 0]
    assert right[1] == [0, 0, 0]  # 不受影响
    assert right[2] == [0, 0, 0]

    # 3) id 验证
    assert id(right[0]) != id(right[1]) != id(right[2])  # 三行不同对象
    assert id(wrong[0]) == id(wrong[1]) == id(wrong[2])  # 错误法三行同一对象

    # 4) 浅拷贝陷阱：切片只拷贝外层
    shallow = right[:]
    shallow[0][0] = 99
    assert right[0][0] == 99  # 内层行仍共享！

    # 5) 深拷贝正确
    deep = copy.deepcopy(right)
    deep[0][0] = 0
    assert right[0][0] == 99  # 不受影响
    print("py-2d-array OK")

```

**PyPy 提示**: PyPy 下引用陷阱完全相同（语义一致）。注意 PyPy 对全 int 二维列表有 list-strategy 优化（紧凑存储），但语义不受影响。创建大二维列表（如 1000×1000）用 [[0]*n for _ in range(m)] 在 PyPy 比 CPython 快。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(m×n) 创建 |
| 空间 | O(m×n) |

### 局限

1) [0]*n 对 int 安全但 [[obj]*n]*m 对可变 obj 不安全，必须推导式；2) 浅拷贝（切片）二维列表内层仍共享，需 deepcopy 或逐行推导重建；3) 极大二维列表（>10^4×10^4）内存压力，考虑一维展开或 bytearray。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1683 | 2 | 二维矩阵读入，列表推导式标准写法 | [https://www.luogu.com.cn/problem/P1683](https://www.luogu.com.cn/problem/P1683) |
| LeetCode | 73 | 4 | 复制矩阵记录零位置，浅拷贝会串扰 | [https://leetcode.cn/problems/set-matrix-zeroes/](https://leetcode.cn/problems/set-matrix-zeroes/) |

## Pitfalls · 易错点

- [[0]*n]*m 引用陷阱：改一行全变（最常见 Python 坑）
- 以为切片 grid[:] 能深拷贝二维列表——内层行仍共享
- [[0]*n]*m 在 int 时看似没问题（因 int 不可变），但一旦嵌套 list 就出错
- 读入矩阵用 [[input().split()]*n] 还是陷阱，应用推导式
- 极大二维列表用 list 不如用 1D 数组 + 索引 i*n+j 省 list 开销

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/lang/python/](https://oi-wiki.org/lang/python/)
- web ✓ [https://docs.python.org/3/tutorial/datastructures.html#nested-list-comprehensions](https://docs.python.org/3/tutorial/datastructures.html#nested-list-comprehensions)
