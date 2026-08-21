---
id: idastar
name: IDA*算法
group: G-A-14
stage: intermediate
priority: P1
depth_tier: standard
---

# IDA*算法

> 迭代加深+A*剪枝，限制路径成本而非深度

<!-- 元信息: id=idastar · group=G-A-14 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

IDA*（Iterative Deepening A*）是把迭代加深与 A* 结合的搜索算法：每次迭代做一次限阈值的 DFS，阈值是路径成本估计 f=g+h 而非深度。初始阈值取 h(起点)；DFS 中若某分支 f>阈值则剪掉并记录其最小超限值，迭代结束后阈值更新为该最小值继续下一轮。它结合了 A* 的启发剪枝与迭代加深的线性空间，不需要判重和排序，空间需求极小，适合 15数码、埃及分数等状态爆炸但路径不太长的问题。

## Why · 为什么

### 直觉 · Intuition

A* 用优先队列按 f 排序，要存下整个 open 表（内存大）。IDA* 改用 DFS 并只限制'这条路径的 f 值上限'：超出阈值就掉头，一轮搜完若没找到，把阈值抬高到刚才所有被卡住分支的最小 f，再来一轮。像'水深探测'：先看能走到多深（f 上限），够不到就加深一点。

### 原理 · Principle

一次迭代对 f=g+h>C 的分支剪枝。因 h 可采纳（乐观），若存在长度≤C 的解，本轮必找到；否则记录所有被剪分支的 min(f)，下一轮阈值设为该值，保证阈值单调上升且不漏解（OI Wiki 的 Search 子算法正是返回未探索节点的最小 f）。与 A* 相比优点：无需判重/排序、DFS 空间 O(路径长度)；缺点：每次放宽阈值都要从头重搜（重复搜索）。埃及分数题中深度无上界、每层无限分支，只能用 IDA* 类思想，并用剩余分数下界做剪枝（h=(a/b - c/d)/(1/(e+1))）。

### 历史 · History

IDA* 由 Richard Korf 于 1985 年在《深度优先迭代加深：内存有限下的最优搜索》中提出，是 A* 与迭代加深的经典合成，长期是 15数码等滑动谜题的最优求解标准算法，启发式搜索领域里程碑工作。

## How · 实现

### 伪代码

```python
def IDA*(start):
    limit = h(start)
    while True:
        t = DFS(start, g=0, limit)
        if t == FOUND: return 解
        if t == INF: return 无解
        limit = t   # 阈值提升到最小超限值

def DFS(u, g, limit):
    f = g + h(u)
    if f > limit: return f        # 返回超限值
    if u == 目标: return FOUND
    nxt_min = INF
    for v in children(u):
        t = DFS(v, g+cost(u,v), limit)
        if t == FOUND: return FOUND
        nxt_min = min(nxt_min, t)
    return nxt_min
```

### Python 实现

```python
GOAL = "123804765"


def manhattan(state):
    """曼哈顿距离(可采纳启发)"""
    d = 0
    for i, ch in enumerate(state):
        if ch != '0':
            gi = GOAL.index(ch)
            d += abs(i // 3 - gi // 3) + abs(i % 3 - gi % 3)
    return d


def neighbors(state):
    i = state.index('0')
    r, c = i // 3, i % 3
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            j = nr * 3 + nc
            lst = list(state)
            lst[i], lst[j] = lst[j], lst[i]
            yield ''.join(lst)


def solvable(state):
    s = [int(c) for c in state if c != '0']
    inv = sum(1 for i in range(len(s)) for j in range(i + 1, len(s)) if s[i] > s[j])
    return (inv - 7) % 2 == 0  # 目标123804765逆序数为7(奇)


def ida_star(start):
    """IDA* 解8数码: 返回最少步数; 不可解返回 None"""
    if not solvable(start):
        return None
    limit = manhattan(start)
    found = [None]

    def dfs(u, g, prev):
        f = g + manhattan(u)
        if f > limit:
            return f          # 返回超限值用于提升阈值
        if u == GOAL:
            found[0] = g
            return -1         # FOUND 哨兵
        nxt_min = float('inf')
        for v in neighbors(u):
            if v == prev:
                continue      # 不走回头路(8数码中无意义)
            t = dfs(v, g + 1, u)
            if t == -1:
                return -1
            nxt_min = min(nxt_min, t)
        return nxt_min

    while True:
        t = dfs(start, 0, None)
        if t == -1:
            return found[0]
        if t == float('inf'):
            return None
        limit = t


if __name__ == "__main__":
    assert ida_star(GOAL) == 0
    r = ida_star("283104765")
    assert r is not None and r >= 0
    assert ida_star("123804756") is None  # 不可解

    # 与 BFS 对拍随机可解状态
    import collections, random
    def bfs_ans(start, maxd=25):
        if start == GOAL:
            return 0
        q = collections.deque([(start, 0)])
        seen = {start}
        while q:
            u, d = q.popleft()
            if d >= maxd:
                continue
            for v in neighbors(u):
                if v not in seen:
                    if v == GOAL:
                        return d + 1
                    seen.add(v)
                    q.append((v, d + 1))
        return None

    random.seed(7)
    tested = 0
    while tested < 30:
        s = GOAL
        for _ in range(random.randint(1, 10)):
            nb = list(neighbors(s))
            s = random.choice(nb)
        b = bfs_ans(s)
        if b is None:
            continue
        a = ida_star(s)
        assert a == b, (s, a, b)
        tested += 1
    print(f"idastar all tests passed ({tested} BFS-cross-validated)")

```

**PyPy 提示**: IDA* 递归+字符串状态在 PyPy 下可行但 15数码会慢；注意深递归 setrecursionlimit。每轮重搜开销大，阈值增量设计（每次 +1 或跳增）影响性能。可保存状态为整数编码加速哈希。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 与 A* 同阶(取决于启发质量)，最坏 O(b^d) 指数；每轮阈值重搜带来常数开销 |
| 空间 | O(路径长度) DFS 栈，远优于 A* 的 open 表 |

### 局限

阈值每轮重搜造成重复工作；需要可采纳启发否则无最优性；路径很长时迭代轮数多；状态空间巨大(如15数码难例)仍可能超时。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1763 | 4 | 埃及分数：深度无上界+每层无限分支，IDA*+下界剪枝经典 | [https://www.luogu.com.cn/problem/P1763](https://www.luogu.com.cn/problem/P1763) |
| UVA | 1343 | 4 | The Rotation Game：旋转游戏，IDA*典型应用 | [https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=24&page=show_problem&problem=4089](https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=24&page=show_problem&problem=4089) |

## Pitfalls · 易错点

- 阈值更新必须取所有被剪分支的最小超限 f，否则可能漏解
- h 不乐观(高估)会误剪最优解
- DFS 需防环(8数码用不走回头路即可，一般问题需 visited 或路径判重)
- 'FOUND'与'无解'哨兵值要区分，勿混用
- 每轮重搜开销大，阈值增量与启发质量直接决定性能

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/search/idastar/](https://oi-wiki.org/search/idastar/)
- 书籍 ✓ `CPH ch5 p58 (IDA* 相关: 迭代加深+剪枝)`
