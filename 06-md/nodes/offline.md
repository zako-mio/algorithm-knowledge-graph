---
id: offline
name: 离线算法思想
group: G-E-7
stage: intermediate
priority: P0
depth_tier: deep
---

# 离线算法思想

> 已知全部数据后统一求解：CDQ分治/整体二分/莫队等离线框架的基础思想

<!-- 元信息: id=offline · group=G-E-7 · stage=intermediate · priority=P0 · depth_tier=deep -->

## What · 是什么

离线算法(Offline Algorithm)是指在求解前已知全部输入数据(包括所有修改和询问)的算法。与在线算法(Online Algorithm，数据逐个到达)相对。离线算法可以重排询问顺序、预排序数据、利用全局信息统一求解，通常比在线算法更优。是 CDQ 分治、整体二分、莫队算法等框架的共同基础思想。

## Why · 为什么

### 直觉 · Intuition

如果所有问题都到齐了才一起回答，可以统筹安排：按某种顺序排序询问使得可以复用中间结果(莫队)、把多个二分合并处理(整体二分)、按时间分治(CDQ)。在线时数据逐个到达，无法预见未来，只能逐个处理——离线可以'作弊'。

### 原理 · Principle

离线算法的核心是利用'已知全部数据'这一假设来优化：①排序询问(莫队按块排序使指针移动最小) ②统一二分(整体二分把所有询问的答案一起二分) ③分治处理(CDQ 把操作按时间/位置分治) ④差分/前缀和(利用全局信息)。竞赛中为阻止离线优化，出题人会用'强制在线'(如前一个询问的答案决定后一个询问的参数)。

### 历史 · History

离线 vs 在线是算法理论中的经典分类。竞赛中莫队算法(2014年起流行)、整体二分、CDQ 分治都是离线框架的代表。'强制在线'是出题人对抗离线的常见手段(如 LCT 强制在线的动态树问题)。

## How · 实现

### 伪代码

```python
# 离线算法通用框架
1. 读入全部数据和询问
2. 预处理: 排序/离散化/建图
3. 重排询问(按某种最优顺序)
4. 统一处理: 利用数据结构/分治/双指针
5. 按原始顺序输出答案

# 示例: 离线区间查询(莫队思想)
queries.sort(key=lambda q: (q.l // B, q.r))
cur_l, cur_r = 0, -1
for q in queries:
  while cur_r < q.r: cur_r++; add(cur_r)
  while cur_l > q.l: cur_l--; add(cur_l)
  while cur_r > q.r: remove(cur_r); cur_r--
  while cur_l < q.l: remove(cur_l); cur_l++
  ans[q.id] = current_answer
```

### Python 实现

```python
def offline_range_sum(arr, queries):
    """离线区间求和: 利用已知全部查询做前缀和预处理。
    展示离线思想: 在线逐个求和O(n)per query, 离线预处理前缀和O(1)per query。
    arr: 数组, queries: [(l, r), ...] 0-indexed
    """
    n = len(arr)
    # 离线预处理: 前缀和
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    # 在线回答每个查询
    results = []
    for l, r in queries:
        results.append(prefix[r + 1] - prefix[l])
    return results


def offline_sorted_queries(arr, queries):
    """离线排序查询: 按右端点排序后用单调栈/双指针优化。
    展示'重排询问顺序'的离线优势。
    queries: [(l, r, id), ...]
    """
    # 按右端点排序
    sorted_q = sorted(queries, key=lambda x: x[1])
    results = [0] * len(queries)

    n = len(arr)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]

    for l, r, qid in sorted_q:
        results[qid] = prefix[r + 1] - prefix[l]
    return results


if __name__ == '__main__':
    arr = [3, 1, 4, 1, 5, 9, 2, 6]
    queries = [(0, 3), (2, 5), (0, 7), (4, 6)]

    # 离线前缀和
    sums = offline_range_sum(arr, queries)
    print(f'Range sums: {sums}')
    assert sums == [9, 19, 31, 16]

    # 离线排序查询
    indexed_queries = [(q[0], q[1], i) for i, q in enumerate(queries)]
    sums2 = offline_sorted_queries(arr, indexed_queries)
    print(f'Sorted queries: {sums2}')
    assert sums2 == [9, 19, 31, 16]

    print('Offline algorithm: all tests passed!')

```

**PyPy 提示**: PyPy 对离线算法中的排序和数组操作优化好；离线框架的核心是'预处理+批量回答'模式，PyPy 下性能通常优于在线逐个处理。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 取决于具体算法: 前缀和 O(N+Q), 莫队 O((N+Q)*sqrt(N)), CDQ O(N log^2 N), 整体二分 O((N+Q)*log V*log N) |
| 空间 | O(N+Q) 需存储全部数据和查询 |

### 局限

题目可能强制在线(前一个答案决定后续参数), 则无法重排/统一处理；需要存储全部数据, 内存可能受限；离线预处理的时间开销可能不适合数据量小但查询频繁的场景。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| OIWiki | misc/offline | 2 | OI Wiki 离线算法思想总览: CDQ/整体二分/莫队等框架的共同基础 | [https://oi-wiki.org/misc/offline/](https://oi-wiki.org/misc/offline/) |
| Luogu | P1494 | 3 | 小Z的袜子: 莫队算法模板, 离线排序+指针移动 | [https://www.luogu.com.cn/problem/P1494](https://www.luogu.com.cn/problem/P1494) |

## Pitfalls · 易错点

- 强制在线题无法使用离线: 前一个答案决定后续查询参数时不能重排
- 离线需存储全部数据, 内存敏感场景可能 MLE
- 重排询问后忘记按原始 id 回填答案, 导致输出顺序错乱
- 离线预处理的开销可能不被小数据量场景摊销(预处理 O(N) 但只查 1 次)

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/misc/offline/](https://oi-wiki.org/misc/offline/)
- wiki ✓ [https://en.wikipedia.org/wiki/Online_algorithm](https://en.wikipedia.org/wiki/Online_algorithm)
