---
id: bidirectional
name: 双向搜索/Meet in the Middle
group: G-A-14
stage: intermediate
priority: P1
depth_tier: standard
---

# 双向搜索/Meet in the Middle

> 从两端同时搜索或折半枚举，O(2^{n/2})降低指数

<!-- 元信息: id=bidirectional · group=G-A-14 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

双向搜索包含两种紧密相关的技术：①双向同时搜索（bidirectional BFS/DFS）：从起点和终点同时开始搜索，两端状态相遇即得解，把搜索半径从 d 降到约 d/2；②Meet in the Middle（折半搜索）：把搜索过程分成两半，分别枚举两半所有状态，再合并结果，把 O(2^n) 降到 O(2^{n/2})。两者共同思路：指数减半。适用状态空间大、单端搜索爆炸的问题。

## Why · 为什么

### 直觉 · Intuition

一个球从山顶滚到底比两个球从两端同时滚要慢——搜索树的分支是乘法增长，把深度减半就是给指数开平方根。MITM 就像把一把锁劈两半分别配钥匙：每一半的尝试次数都少得多，再找配对。

### 原理 · Principle

设搜索树分支因子为 b，单端搜到深度 d 需展开约 b^d 个节点。双向同时搜索两端各展开约 b^{d/2}，相遇时总节点数约 2b^{d/2}，远小于 b^d。MITM 对 O(2^n) 的暴力枚举：把 n 个元素拆成两半，每半枚举 2^{n/2} 种组合，一半排序后对另一半逐个二分查找/哈希配对，总复杂度 O(n·2^{n/2})。前提：问题可分两半且可合并（如子集和的补集配对、灯光状态按半段枚举）。

### 历史 · History

双向搜索是图论经典技巧（1970s 常见于 AI 搜索文献）；Meet in the Middle 在密码学中早有类似思想（如中间相遇攻击，1977 Diffie-Hellman 相关），后成为算法竞赛折半枚举的标准方法。OI Wiki 将两页内容合并介绍。

## How · 实现

### 伪代码

```python
# 双向BFS
queue qs=[start], qg=[goal]
dists={start:0}, distg={goal:0}
while qs and qg:
  扩展较小的一边
  对邻居v: 若v在另一边已出现 -> 相遇, 距离=dist[u]+1+dist_other[v]
  否则标记并入队

# Meet in the Middle (子集和)
把数组分成两半 A, B
枚举A的所有子集和 -> sums_A (排序)
枚举B的所有子集和 -> 对每个查 target-s 是否在 sums_A
```

### Python 实现

```python
from collections import deque


def bidirectional_bfs(start, goal, neighbors):
    """双向BFS: 求边权为1的最短步数, 不可达返回-1
    neighbors(u) 返回u的邻居列表(无向图)
    """
    if start == goal:
        return 0
    qs, qg = deque([start]), deque([goal])
    dists, distg = {start: 0}, {goal: 0}
    while qs and qg:
        if len(qs) <= len(qg):   # 优先扩展较小的一边
            q, dist, other = qs, dists, distg
        else:
            q, dist, other = qg, distg, dists
        for _ in range(len(q)):
            u = q.popleft()
            for v in neighbors(u):
                if v not in dist:
                    dist[v] = dist[u] + 1
                    if v in other:
                        return dist[v] + other[v]  # 相遇
                    q.append(v)
    return -1


def gen_subset_sums(xs):
    """枚举所有子集和"""
    sums = []
    for mask in range(1 << len(xs)):
        s = 0
        for i, v in enumerate(xs):
            if mask >> i & 1:
                s += v
        sums.append(s)
    return sums


def meet_in_middle_subset_sum(arr, target):
    """MITM 子集和: 是否存在子集和 == target
    复杂度 O(2^(n/2) * n), 适用于 n<=40
    """
    half = len(arr) // 2
    sums_a = sorted(gen_subset_sums(arr[:half]))
    for s in gen_subset_sums(arr[half:]):
        need = target - s
        lo, hi = 0, len(sums_a)
        while lo < hi:
            mid = (lo + hi) // 2
            if sums_a[mid] < need:
                lo = mid + 1
            else:
                hi = mid
        if lo < len(sums_a) and sums_a[lo] == need:
            return True
    return False


if __name__ == "__main__":
    # 链图 0-1-2-3-4
    def neighbors(u):
        m = {0: [1], 1: [0, 2], 2: [1, 3], 3: [2, 4], 4: [3]}
        return m[u]
    assert bidirectional_bfs(0, 4, neighbors) == 4
    assert bidirectional_bfs(0, 0, neighbors) == 0
    assert bidirectional_bfs(0, 3, neighbors) == 3

    # MITM 子集和
    assert meet_in_middle_subset_sum([3, 5, 2, 8, 1, 4], 9) is True   # 5+4
    assert meet_in_middle_subset_sum([3, 5, 2, 8, 1, 4], 10) is True  # 8+2
    assert meet_in_middle_subset_sum([3, 5, 2, 8, 1, 4], 99) is False
    assert meet_in_middle_subset_sum([2, 4, 6, 8], 10) is True        # 2+8 / 4+6

    print("bidirectional all tests passed")

```

**PyPy 提示**: MITM 的 2^(n/2) 枚举常用位运算 + 列表生成，PyPy 快。子集和配对可用 dict 存前半段状态最小值（如 P2962 灯光题），比二分更快。双向BFS用 dict 作距离表，PyPy 字典操作较快。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 双向BFS: O(b^{d/2})；MITM: O(2^{n/2})（含排序则 O(2^{n/2}·n)） |
| 空间 | 双向BFS: O(b^{d/2}) 双端距离表；MITM: O(2^{n/2}) 存一半状态 |

### 局限

双向同时搜索要求目标状态已知且可逆（反向也能扩展）；MITM 要求问题能拆成两半并合并，且两半的枚举量都要 2^{n/2} 可控（n≤40 左右）；配对阶段需要能高效判定'互补'。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1379 | 3 | 八数码难题：双向BFS经典例题（目标状态固定123804765） | [https://www.luogu.com.cn/problem/P1379](https://www.luogu.com.cn/problem/P1379) |
| Luogu | P2962 | 4 | USACO09NOV Lights：折半枚举+状态合并，n≤35 | [https://www.luogu.com.cn/problem/P2962](https://www.luogu.com.cn/problem/P2962) |

## Pitfalls · 易错点

- 双向BFS须交替/按大小扩展两边，单边一直扩展到相遇可能退化为普通BFS
- MITM 拆半后要保证两半互补可判定（子集和查 target-s 而非 s 自身）
- 目标状态必须可从终点反向扩展（无向图OK，有向图需反图）
- 一半状态枚举量 2^(n/2) 也要存下，内存随 n 指数增长

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/search/bidirectional/](https://oi-wiki.org/search/bidirectional/)
- 书籍 ✓ `CPH ch4 p91 (bidirectional BFS)`
