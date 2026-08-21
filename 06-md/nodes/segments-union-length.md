---
id: segments-union-length
name: 线段并集长度
group: G-D-2
stage: advanced
priority: P2
depth_tier: standard
---

# 线段并集长度

> 扫描线求一维/二维线段并集长度，离散化+区间合并

<!-- 元信息: id=segments-union-length · group=G-D-2 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

给定 n 条线段（在一维数轴上），求它们的并集总长度。Klee 算法（1977）O(n log n)：把所有端点排序，从左到右扫描，维护『当前打开的线段数 c』——遇到左端点 c+1，遇到右端点 c-1；当 c>0 时累加相邻坐标差。该算法已被证明是渐进最优的。一维线段并集是区间合并/扫描线的基础；二维推广为矩形面积并（见扫描线节点）。应用：覆盖长度统计、区间调度、图形填充、以及『合并区间』类问题。

## Why · 为什么

### 直觉 · Intuition

想象一条线从负无穷扫到正无穷。线段像门帘一样：左端点挂上（c+1），右端点取下（c-1）。只要 c>0 就说明『当前这段被覆盖』，把它计入长度。排序端点保证我们能逐段判断覆盖状态。为什么 O(n log n) 最优？因为任何算法都要知道端点的大小顺序，排序下界就是 Ω(n log n)。

### 原理 · Principle

① 对每条线段生成两个事件 (坐标, 类型)，左端为 'open'，右端为 'close'，整体排序。② 遍历事件：若当前坐标 x_i 与前一个 x_{i-1} 不同且 c>0，累加 x_i-x_{i-1}；然后根据事件类型更新 c。③ 关键细节：同一坐标有多个事件时，若某处既有关也有开，先算长度再更新不会错（因为 c 变化只影响后续区间）；但更稳妥的写法是先处理完同坐标所有事件（因为右端点闭合后 c 减少，同一坐标处开/关顺序决定是否计入 [x,x] 零长度段，实际无影响）。④ 正确性：c>0 ⟺ 该开区间被至少一条线段覆盖。⑤ 变体：合并区间输出（排序+贪心合并），双指针扫描。

### 历史 · History

Klee 于 1977 年提出该 O(n log n) 算法并证明最优（可归约到排序下界）。CP-Algorithms 收录（'Length of the union of segments'），是『扫描线思想』的最简单入门。广泛见于覆盖类问题，是矩形面积并（二维）的前置概念。

## How · 实现

### 伪代码

```python
# 线段并集长度 (Klee 算法)
def union_length(segs):
  events = []
  for (l, r) in segs:
    events.append((l, False))   # 左端
    events.append((r, True))    # 右端
  sort(events)
  result = 0; c = 0
  for i in range(2n):
    if i>0 and events[i].x > events[i-1].x and c > 0:
      result += events[i].x - events[i-1].x
    if events[i].is_close: c -= 1
    else: c += 1
  return result
```

### Python 实现

```python
def union_length(segs):
    """正确实现: 同坐标事件批处理."""
    events = []
    for l, r in segs:
        if l > r:
            l, r = r, l
        events.append((l, 1))
        events.append((r, -1))
    events.sort()
    result = 0.0
    c = 0
    prev_x = None
    i = 0
    n = len(events)
    while i < n:
        x = events[i][0]
        # 先累加 [prev_x, x] 这段 (若被覆盖)
        if prev_x is not None and c > 0:
            result += (x - prev_x)
        # 批处理所有同坐标事件
        while i < n and events[i][0] == x:
            c += events[i][1]
            i += 1
        prev_x = x
    return result


def brute(segs):
    """暴力: 合并区间求并长 (用于交叉验证)."""
    segs = sorted((min(a, b), max(a, b)) for a, b in segs)
    if not segs:
        return 0.0
    merged = [list(segs[0])]
    for l, r in segs[1:]:
        if l <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], r)
        else:
            merged.append([l, r])
    return sum(r - l for l, r in merged)


if __name__ == "__main__":
    # [0,3] 与 [2,5] 并 = [0,5] = 5
    assert abs(union_length([(0, 3), (2, 5)]) - 5.0) < 1e-9
    # 分离: [0,1] [3,4] = 2
    assert abs(union_length([(0, 1), (3, 4)]) - 2.0) < 1e-9
    # 完全包含: [0,5] [1,2] = 5
    assert abs(union_length([(0, 5), (1, 2)]) - 5.0) < 1e-9
    # 端点相接: [0,1] [1,3] = 3
    assert abs(union_length([(0, 1), (1, 3)]) - 3.0) < 1e-9
    # 单条
    assert abs(union_length([(10, 20)]) - 10.0) < 1e-9
    # 空
    assert union_length([]) == 0.0

    # 随机交叉验证
    import random
    random.seed(4)
    for _ in range(500):
        n = random.randint(0, 10)
        segs = []
        for _ in range(n):
            a = random.randint(-10, 10)
            b = random.randint(-10, 10)
            segs.append((a, b))
        got = union_length(segs)
        exp = brute(segs)
        assert abs(got - exp) < 1e-9, (segs, got, exp)
    print("All tests passed.")
```

**PyPy 提示**: 事件排序 O(n log n)，扫描 O(n)。整数坐标可全程 int。同坐标事件批处理避免误算（先算长度再更新计数是 Klee 原版写法，批处理版更直观）。大 n 时用 list.sort 即可。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n log n)（排序主导）；排序下界保证渐进最优 |
| 空间 | O(n) |

### 局限

只处理一维；二维推广为矩形面积并需线段树（见扫描线）。重叠严重时也 O(n log n) 无差。若只需合并区间输出（而非总长），排序+贪心即可，不必事件扫描。浮点坐标下端点相等判定用排序天然解决。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1496 | 3 | 火烧赤壁：线段覆盖总长度（一维扫描线/Klee 算法） | [https://www.luogu.com.cn/problem/P1496](https://www.luogu.com.cn/problem/P1496) |
| Luogu | P1908 | 4 | 逆序对：二维数点/扫描线思想（OI Wiki 扫描线章节例题，与线段并同源） | [https://www.luogu.com.cn/problem/P1908](https://www.luogu.com.cn/problem/P1908) |
| Luogu | P5490 | 3 | 【模板】扫描线：一维线段并的二维推广（矩形面积并） | [https://www.luogu.com.cn/problem/P5490](https://www.luogu.com.cn/problem/P5490) |

## Pitfalls · 易错点

- 同坐标多个事件时处理顺序：若先更新计数再算长度，同坐标开/关会漏计/重复计零长度段，应批处理
- 事件类型用 (l,1)/(r,-1) 而非布尔，避免排序时右端在左端前的歧义
- 浮点坐标累加误差：用 double 无碍，但大规模累加注意精度
- l>r 的非法输入未交换
- 空输入返回 0
- 端点相接（[0,1],[1,3]）并入一个区间，别算成重复

## Sources · 信源

- CP-Algorithms ✓ [https://cp-algorithms.com/geometry/length-of-segments-union.html](https://cp-algorithms.com/geometry/length-of-segments-union.html)
- OI Wiki ✓ [https://oi-wiki.org/geometry/scanning/](https://oi-wiki.org/geometry/scanning/)
