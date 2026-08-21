---
id: space-optimization
name: 空间优化
group: G-E-7
stage: advanced
priority: P1
depth_tier: standard
---

# 空间优化

> 滚动数组/bitset压位/信息熵下界/利用数据特性(并查集单数组)等节省内存技巧

<!-- 元信息: id=space-optimization · group=G-E-7 · stage=advanced · priority=P1 · depth_tier=standard -->

## What · 是什么

空间优化指在算法空间复杂度之外，通过数据组织与存储技巧压内存的技巧集。常见手段：①滚动数组(DP 只依赖前一层时 2 数组滚动)；②bitset 压位(bool 数组每字节 1 位变 1 位)；③避免存储不必要数据(可持久化只存新增结点、稀疏图用邻接表不用邻接矩阵)；④利用数据特性(路径压缩+启发式合并的并查集用负数表示根，单数组实现)；⑤信息熵下界(存储 n 个等概率整数至少需 log2 n 位)用于设计紧凑存储方案。

## Why · 为什么

### 直觉 · Intuition

内存与时间在竞赛中常互相折算：能少存就少存，必要时用计算换存储。滚动数组的关键是'只需要保留最近若干层'；bitset 利用位运算在 O(n/word) 内并行处理；并查集单数组技巧把根与非根信息编码进同一个 int 的符号位。

### 原理 · Principle

滚动数组：若 dp[i] 仅依赖 dp[i-1]，用 dp[0],dp[1] 两行按 i 奇偶轮流使用，把 O(n*W) 压到 O(2W)；01背包再退化为一维逆序。bitset：用 Python 大整数或 bitset 库的 bit 级存取，布尔数组空间/8。并查集单数组：arr[x]<0 表示 x 是根且 -arr[x] 为子树大小，arr[x]>=0 表示父指针。信息熵：对均匀分布值域 [1,n]，任何编码至少 log2 n bit/个(Shannon 下界)，据此判断方案是否已达最优。

### 历史 · History

空间优化技巧由 OI Wiki 收录为专题页，覆盖信息熵下界、常见压空间手段与并查集单数组实现；国内 2022 国家集训队论文《浅谈信息学竞赛中的空间优化问题》(陈知轩)系统总结了该主题。典型的应用场景为内存极紧的大数据 DP 与布尔状态题。

## How · 实现

### 伪代码

```python
# 滚动数组: 斐波那契/DP 前层依赖
dp = [0]*2; dp[0] = 1
a, b = 1, 1
for i in range(2, n+1):
  a, b = b, a + b      # 只保留两层

# 01背包滚动: for w 逆序
dp = [0]*(W+1)
for wi, vi in items:
  for j in range(W, wi-1, -1):
    dp[j] = max(dp[j], dp[j-wi] + vi)

# bitset 压位: Python 大整数当 bool 数组
mask = 0
for i in range(n):
  if cond(i): mask |= 1 << i
# 判断第 k 位: (mask >> k) & 1
```

### Python 实现

```python
def fib_roll(n):
    """滚动数组求斐波那契 O(1) 空间。"""
    if n < 2:
        return n
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def knapsack01_roll(items, W):
    """01背包滚动数组 O(W) 空间。
    items: [(w,v), ...]; 返回最大价值。
    """
    dp = [0] * (W + 1)
    for w, v in items:
        for j in range(W, w - 1, -1):
            if dp[j - w] + v > dp[j]:
                dp[j] = dp[j - w] + v
    return dp[W]


def dsu_one_array(n):
    """单数组并查集: arr[x]<0 表示根(大小=-arr[x]), arr[x]>=0 表示父指针。"""
    parent = [-1] * n  # 全部为根, 大小为1

    def find(x):
        r = x
        while parent[r] >= 0:
            r = parent[r]
        # 路径压缩
        while parent[x] >= 0:
            nxt = parent[x]
            parent[x] = r
            x = nxt
        return r

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        # 启发式合并: 大小大的当根
        if parent[ra] > parent[rb]:  # 更小(更负) = 更大
            ra, rb = rb, ra
        parent[ra] += parent[rb]
        parent[rb] = ra

    return parent, find, union


def bitset_bool_array(n):
    """用 Python 大整数模拟 bitset: 每 bit 存一个 bool。"""
    mask = 0
    return mask


if __name__ == '__main__':
    # 斐波那契
    fibs = [fib_roll(i) for i in range(10)]
    assert fibs == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    # 01背包: 容量5, 物品(2,3),(3,4),(4,5) -> 最优 3+4=7
    items = [(2, 3), (3, 4), (4, 5)]
    assert knapsack01_roll(items, 5) == 7

    # 单数组并查集
    parent, find, union = dsu_one_array(6)
    union(0, 1)
    union(2, 3)
    union(3, 4)
    assert find(0) == find(1)
    assert find(2) == find(3) == find(4)
    assert find(0) != find(4)
    union(1, 4)
    assert find(0) == find(4)          # 现在 0 与 4 同集
    assert find(5) != find(0)          # 5 仍是孤立
    assert len({find(i) for i in range(6)}) == 2

    # bitset 演示
    m = 0
    for i in range(10):
        if i % 2 == 0:
            m |= 1 << i
    assert all(((m >> i) & 1) == (1 if i % 2 == 0 else 0) for i in range(10))

    print('fib roll   :', [fib_roll(i) for i in range(10)])
    print('knapsack01 :', knapsack01_roll(items, 5))
    print('dsu one-array:', parent, [find(i) for i in range(6)])
    print('All space-optimization tests passed!')

```

**PyPy 提示**: 滚动数组与 bitset 用大整数运算在 PyPy 上表现良好(大整数 bit 操作走 C 层); 单数组并查集注意负数编码, find 时父指针>=0 为根边界; PyPy 的大整数移位对 n>10^6 的 bitset 优化明显。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 各技巧均为原算法同阶时间; bitset 布尔运算 O(N/word) |
| 空间 | 滚动数组 O(2W)→O(W); bitset O(N/8); 单数组并查集 O(N) |

### 局限

滚动数组要求状态仅依赖最近若干层; bitset 位运算的 Python 大整数转 int 有开销; 信息熵下界说明压缩有理论极限, 不能用压缩超越信息量; 单数组并查集牺牲了可读性, 需严格记住编码。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P8353 | 5 | SDOI/SXOI2022 无处存储: 空间极紧的树上DP, 需滚动/复用数组的经典题 | [https://www.luogu.com.cn/problem/P8353](https://www.luogu.com.cn/problem/P8353) |
| Luogu | P8079 | 5 | WC2022 猜词: 信息熵选词, 交互题, 信息论思想应用 | [https://www.luogu.com.cn/problem/P8079](https://www.luogu.com.cn/problem/P8079) |
| QOJ | 6669 | 5 | Mapa: OI Wiki 空间优化页习题, 需位压缩/内存技巧 | [https://qoj.ac/problem/6669](https://qoj.ac/problem/6669) |

## Pitfalls · 易错点

- 01背包一维滚动必须逆序遍历容量, 正序会重复取同一物品(退化为完全背包)
- 单数组并查集 find 时用 parent[x]>=0 判断非根, 根的大小编码在负值, 合并时把更负的当根(更大集合)
- bitset 的 Python int 操作在超长时逐位转换有额外开销, 大数据建议用 array 或第三方 bitset
- 压缩存储后读改写需解压/重压缩, 谨防时间换空间的代价失控
- 信息熵下界只是理论, 不代表实现一定能达到; 不必要的数据(如可持久化整棵线段树)才是最大浪费

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/misc/space-optimization/](https://oi-wiki.org/misc/space-optimization/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/space-optimization.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/space-optimization.md)
- web ✓ [https://en.wikipedia.org/wiki/Information_theory](https://en.wikipedia.org/wiki/Information_theory)
