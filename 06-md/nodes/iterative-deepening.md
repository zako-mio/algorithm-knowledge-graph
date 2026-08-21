---
id: iterative-deepening
name: 迭代加深(IDDFS)
group: G-A-14
stage: intermediate
priority: P1
depth_tier: standard
---

# 迭代加深(IDDFS)

> 逐步增加DFS深度限制，DFS方式实现BFS效果，空间优

<!-- 元信息: id=iterative-deepening · group=G-A-14 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

迭代加深搜索（Iterative Deepening Depth-First Search, IDDFS）每次限制搜索深度 d 做一次 DFS，若没找到解就把 d 加一重来。它用 DFS 的方式实现了 BFS 的'逐层搜索'效果：保证第一次找到的解是最优解（步数最少），而空间复杂度只有 O(深度) 而非 BFS 的 O(分支数^深度)。适合状态空间巨大、单个状态又大、且要最优解的搜索问题。

## Why · 为什么

### 直觉 · Intuition

BFS 用队列逐层展开，答案在最深层时队列可能塞满整层节点（指数级）。迭代加深每轮只做一次限深的 DFS，一轮只走一条路径；重复搜索前面层看似浪费，但当分支因子大时，前面层的节点数相比最后层可忽略，'白跑'的代价很小，换来的是空间从指数降到线性。

### 原理 · Principle

设分支因子 b、目标深度 d。IDDFS 的 DFS 每轮展开约 b^d 个节点（最后一层），前面 d-1 轮合计约 b^{d-1}+b^{d-2}+...+1 < b^d/(b-1)。总工作量约 b^d·b/(b-1)，与 BFS 同阶，但空间 O(d) 远小于 BFS 的 O(b^d)。当分支因子 b 大时 b/(b-1)→1，重复搜索的额外开销趋近于 0。这就是'为什么迭代加深可近似看成 BFS'的原因。若存在解在深度 d 内，第 d 轮必能找到，且因逐层递增必为最短解。

### 历史 · History

迭代加深概念源于 20 世纪 60-70 年代的 AI 搜索（与 IDA* 同源），被用作内存受限环境下替代 BFS 的标准策略。Korf 在 1985 年系统分析了迭代加深的复杂度（与 BFS 同阶但线性空间），并推广为 IDA*。

## How · 实现

### 伪代码

```python
def IDDFS(root, limit_max):
    for limit in 0..limit_max:
        if DFS(root, depth=0, limit) 找到:
            return 解
    return 无解

def DFS(u, d, limit):
    if 是目标: return True
    if d == limit: return False
    for v in 邻居(u):
        if DFS(v, d+1, limit): return True
    return False
```

### Python 实现

```python
def id_dfs(start, is_goal, neighbors, max_depth=30):
    """迭代加深DFS: 找从start到目标的最短路径
    is_goal(u) 判目标, neighbors(u) 返回邻居
    返回: 路径列表或 None
    """
    path = [start]

    def dfs(u, d, limit):
        if is_goal(u):
            return True
        if d == limit:
            return False
        for v in neighbors(u):
            if v in path:      # 避免环
                continue
            path.append(v)
            if dfs(v, d + 1, limit):
                return True
            path.pop()
        return False

    for limit in range(max_depth + 1):
        if dfs(start, 0, limit):
            return path
    return None


if __name__ == "__main__":
    # 目标在深度3, 分支因子2的树
    tree = {
        'a': ['b', 'c'],
        'b': ['d', 'e'],
        'c': ['f', 'g'],
        'd': ['h', 'i'],
        'e': [], 'f': [], 'g': [], 'h': [], 'i': []
    }
    def neighbors(u): return tree.get(u, [])
    def is_goal(u): return u == 'h'

    path = id_dfs('a', is_goal, neighbors)
    assert path == ['a', 'b', 'd', 'h'], path

    # 目标在根: 深度0
    assert id_dfs('a', lambda u: u == 'a', neighbors) == ['a']
    # 无解
    assert id_dfs('a', lambda u: u == 'zzz', neighbors, max_depth=3) is None

    print("iterative-deepening all tests passed")

```

**PyPy 提示**: 迭代加深的每轮 DFS 都重新从根走，PyPy 下递归调用开销需注意；分支因子大时工作量大。可用 path 列表做显式栈避免 'v in path' 的 O(d) 查找（用 set 或标记数组）。深递归需 sys.setrecursionlimit。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(b^d)，与 BFS 同阶（b 分支因子, d 目标深度） |
| 空间 | O(d) 递归栈，优于 BFS 的 O(b^d) |

### 局限

分支因子大或深度无上界时仍可能超时；每轮重搜带来常数倍开销；需保证'深度内必有解'才能保证最优性；有环图要防环（路径判重）。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1763 | 4 | 埃及分数：深度无上界+无限分支，迭代加深+剪枝经典题 | [https://www.luogu.com.cn/problem/P1763](https://www.luogu.com.cn/problem/P1763) |
| UVA | 1343 | 4 | The Rotation Game：旋转游戏，迭代加深+剪枝 | [https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=24&page=show_problem&problem=4089](https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=24&page=show_problem&problem=4089) |

## Pitfalls · 易错点

- 必须逐层递增深度，否则无法保证最优性
- 有环状态需路径判重，否则可能死循环
- max_depth 设置过小会漏解，需按问题上界设置
- 每轮重搜的常数开销在分支因子小时相对明显，此时 BFS 更合适

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/search/iterative/](https://oi-wiki.org/search/iterative/)
- 书籍 ✓ `CPH ch5 p58 (Iterative deepening)`
