---
id: cdq-divide
name: CDQ分治
group: G-E-7
stage: advanced
priority: P1
depth_tier: standard
---

# CDQ分治

> 分治处理点对问题：三维偏序/DP优化/动态转静态；陈丹琦(IOI2008)提出

<!-- 元信息: id=cdq-divide · group=G-E-7 · stage=advanced · priority=P1 · depth_tier=standard -->

## What · 是什么

CDQ分治是一种基于分治思想的算法框架，用于解决点对统计问题(如三维偏序)、优化1D/1D DP转移、以及将动态问题转化为静态问题。核心是：将点对(i,j)分为左半内部、右半内部、跨左右三类，递归处理前两类，额外处理跨类。

## Why · 为什么

### 直觉 · Intuition

统计满足条件的点对(i,j)时，暴力 O(n^2)。分治思路：按中点 mid 将序列分左右两半，点对被分为三类：全在左、全在右、跨左右。前两类递归解决，只需额外处理跨左右的部分——此时 i 恒在左、j 恒在右，一个维度(i<j)自动满足，问题降维。

### 原理 · Principle

solve(l,r) 处理 [l,r] 内所有点对：①取 mid=(l+r)/2 ②递归 solve(l,mid) 和 solve(mid+1,r) ③处理跨区间点对(l<=i<=mid, mid+1<=j<=r)。第三步因 i<j 已保证，降维后排序+双指针+树状数组解决。三维偏序：先按 a 排序(保证 a 维)，CDQ 分治保证 b 维(左<右)，树状数组处理 c 维。复杂度 T(n)=2T(n/2)+O(n log n)=O(n log^2 n)。

### 历史 · History

CDQ 分治由 IOI2008 金牌得主陈丹琦在高中时整理总结，因此得名。原始论文《CDQ分治》系统阐述了这一思想在三维偏序、DP优化、动态转静态三个方向的应用。

## How · 实现

### 伪代码

```python
# 三维偏序: 统计 a_i<=a_j, b_i<=b_j, c_i<=c_j 且 i!=j 的点对数
solve(l, r):
  if l == r: return
  mid = (l + r) / 2
  solve(l, mid)
  solve(mid + 1, r)
  # 处理跨区间: 左半 i, 右半 j
  # 已按 a 排序 => 左半 a <= 右半 a (同 a 时左在前)
  # 按 b 排序左右半, 双指针 + 树状数组查 c
  merge left[l..mid] and right[mid+1..r] by b
  j = l
  for i in left:
    while j <= r and right[j].b <= left[i].b:
      bit.add(right[j].c, 1); j++
    ans += bit.query(left[i].c)
  # 清空树状数组
```

### Python 实现

```python
import sys
sys.setrecursionlimit(1 << 20)


class BIT:
    """树状数组(单点修改+前缀查询)。"""
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 2)

    def add(self, i, v):
        while i <= self.n:
            self.tree[i] += v
            i += i & (-i)

    def query(self, i):
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s


def cdq_3d_partial_order(points):
    """三维偏序: 统计点对(i,j)满足 a_i<=a_j, b_i<=b_j, c_i<=c_j 且 i<j。
    points: [(a, b, c), ...]
    返回每个点作为 j 的合法 i 个数(含等号)。
    """
    n = len(points)
    if n == 0:
        return []
    # 离散化 c 值
    c_vals = sorted(set(p[2] for p in points))
    c_map = {v: i + 1 for i, v in enumerate(c_vals)}
    m = len(c_vals)

    # 按 a 排序(a 相同时按原始位置保证 i<j)
    arr = [(points[i][0], points[i][1], points[i][2], i) for i in range(n)]
    arr.sort(key=lambda x: (x[0], x[3]))

    ans = [0] * n
    bit = BIT(m)
    # 临时数组用于归并排序(按 b)
    tmp = [None] * n

    def cdq(l, r):
        if l == r:
            return
        mid = (l + r) // 2
        cdq(l, mid)
        cdq(mid + 1, r)
        # 处理跨区间: arr[l..mid] 为左, arr[mid+1..r] 为右
        # 按 b 排序: 归并(左半和右半内部已按 b 排好序)
        i, j, k = l, mid + 1, l
        while i <= mid and j <= r:
            if arr[i][1] <= arr[j][1]:
                tmp[k] = arr[i]
                k += 1
                i += 1
            else:
                tmp[k] = arr[j]
                k += 1
                j += 1
        while i <= mid:
            tmp[k] = arr[i]
            k += 1
            i += 1
        while j <= r:
            tmp[k] = arr[j]
            k += 1
            j += 1
        # tmp[l..r] 现在按 b 排序
        # 双指针+树状数组: 左半元素入树状数组, 右半元素查询
        # 重新分离左右(按 b 排序后的顺序)
        left_items = [tmp[x] for x in range(l, r + 1) if tmp[x][3] < arr[mid][3] or (tmp[x][3] <= mid)]
        # 简化: 直接用 tmp 数组, 用原始位置区分左右
        # 原始位置 <= mid 的为左半(已排序后), > mid 的为右半
        # 但 arr 已按 a 排序, 排序后位置和原始位置不一定对应
        # 需用原始 idx 判断: arr[l..mid] 的原始位置
        left_set = set(arr[x][3] for x in range(l, mid + 1))

        # 按 b 排序后的顺序处理
        added = []
        for x in range(l, r + 1):
            item = tmp[x]
            if item[3] in left_set:
                # 左半元素: 加入树状数组
                bit.add(c_map[item[2]], 1)
                added.append(item)
            else:
                # 右半元素: 查询
                ans[item[3]] += bit.query(c_map[item[2]])
        # 清空树状数组
        for item in added:
            bit.add(c_map[item[2]], -1)
        # 写回 arr (保持按 b 排序)
        for x in range(l, r + 1):
            arr[x] = tmp[x]

    cdq(0, n - 1)
    return ans


if __name__ == '__main__':
    # 测试三维偏序
    points = [(1, 1, 1), (2, 2, 2), (1, 2, 3), (2, 1, 3), (3, 3, 3)]
    result = cdq_3d_partial_order(points)
    print(f'3D partial order counts: {result}')
    # 验证: 暴力
    n = len(points)
    brute = [0] * n
    for j in range(n):
        for i in range(n):
            if i != j:
                if (points[i][0] <= points[j][0] and
                    points[i][1] <= points[j][1] and
                        points[i][2] <= points[j][2]):
                    brute[j] += 1
    print(f'Brute force counts:      {brute}')
    assert result == brute, f'Mismatch: {result} vs {brute}'
    print('CDQ 3D partial order: test passed!')

```

**PyPy 提示**: PyPy 对递归+排序+树状数组组合性能尚可；但 CDQ 分治层数多、常数大，N>1e5 时 Python 可能 TLE；建议 C++ 实现。Python 用于理解算法和验证小规模数据。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(N log^2 N) — 每层排序 O(N log N) 或归并 O(N log N), 共 log N 层 |
| 空间 | O(N) — 递归栈+树状数组+临时数组 |

### 局限

常数较大(Python 尤甚)；需要问题可降维(至少一个维度可由分治结构保证)；DP优化版需转移有序(中序遍历线段树性质)；动态转静态需操作可分治。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3810 | 4 | 三维偏序(mo): CDQ 分治模板题, a 排序+CDQ(b)+树状数组(c) | [https://www.luogu.com.cn/problem/P3810](https://www.luogu.com.cn/problem/P3810) |
| Luogu | P3157 | 5 | 动态逆序对: CDQ 分治处理时间+位置+值三维 | [https://www.luogu.com.cn/problem/P3157](https://www.luogu.com.cn/problem/P3157) |
| Luogu | P2487 | 5 | SDOI2011 拦截导弹: CDQ 优化二维 LIS DP | [https://www.luogu.com.cn/problem/P2487](https://www.luogu.com.cn/problem/P2487) |

## Pitfalls · 易错点

- a 相同时排序不稳定导致 i<j 不满足: 需用原始位置做 tiebreaker
- 树状数组用完不清空 → 跨层污染: 必须在每层结束后逆序清除
- DP优化版中转移顺序必须夹在 solve(l,mid) 和 solve(mid+1,r) 之间, 否则转移不完整
- 归并合并时顺序错误导致后续层 a 单调性被破坏

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/misc/cdq-divide/](https://oi-wiki.org/misc/cdq-divide/)
- CP-Algorithms ✓ [https://cp-algorithms.com/dynamic_programming/divide-and-conquer-dp.html](https://cp-algorithms.com/dynamic_programming/divide-and-conquer-dp.html)
