---
id: two-sat
name: 2-SAT
group: G-B-4
stage: intermediate
priority: P1
depth_tier: deep
---

# 2-SAT

> 2-适定性问题：布尔方程(a∨b)型约束，建蕴含图+SCC判定，用SCC反拓扑序赋解O(V+E)

<!-- 元信息: id=two-sat · group=G-B-4 · stage=intermediate · priority=P1 · depth_tier=deep -->

## What · 是什么

2-SAT(Satisfiability)问题是判定n个布尔变量能否满足m个'两个变量的析取式'约束的问题，如(x1∨x3)、(¬x2∨x3)等。k-SAT在k>2时是NP完全问题，而2-SAT有多项式算法。解法核心是建蕴含图：每个变量x拆成真、假两个节点，每个约束(a∨b)等价于蕴含对(¬a→b)和(¬b→a)，然后求强连通分量(SCC)：若某变量的真节点与假节点在同一SCC则无解；否则有解，且取'所在SCC编号更小(反拓扑序更靠后)'的节点为真即为一组解。由于每条蕴含边同时建一条逆否边，蕴含图满足对称性，保证该取法正确。复杂度O(V+E)。

## Why · 为什么

### 直觉 · Intuition

蕴含图把'如果a成立那么b必然成立'翻译成有向边a→b。若从x=true能推出x=false，同时从x=false又能推出x=true(在同一SCC)，则矛盾无解。取解时利用对称性：在SCC收缩后的DAG上，自底向上贪心选节点——选一个节点就要否掉它的矛盾对，由于DAG无环，这种选法不会冲突，等价于取SCC编号小者。

### 原理 · Principle

建图规则：(¬a∨b) → 边 a→b 和 ¬b→¬a；(a∨b) → 边 ¬a→b 和 ¬b→a；(¬a∨¬b) → 边 a→¬b 和 b→¬a。每条约束产生两条蕴含边(成对对称)。随后用Tarjan/Kosaraju求SCC并缩点：若同一变量x与其否定¬x在同一SCC则无解。判定可行后赋解：Tarjan求得的SCC编号是从栈底到栈顶(后序遍历)的，编号越小越接近DAG叶子(反拓扑序靠后)；对每个变量x，取scc[x]<scc[¬x]的节点置真(即选编号更小的节点)。该贪心基于图对称性保证可构造出一组满足所有约束的解。

### 历史 · History

2-SAT问题源于逻辑与布尔可满足性研究。k-SAT(k>2)是NP完全(Schaefer定理等)，而2-SAT可在线性时间求解，由Krom(1967)提出，后由Aspvall、Plass与Tarjan(1979)给出基于强连通分量的线性算法。OI Wiki的2-sat.md、CP-Algorithms的2SAT页及CPH ch20(pp191-204)均有完整介绍。伍昱2003年国家集训队论文《由对称性解2-sat问题》深入阐述了基于DAG对称性的求解方法。

## How · 实现

### 伪代码

```python
# 建图: 变量i(0-based)节点 i 表示x_i为真, i+n 表示x_i为假
# 约束 (a OR b): a,b为带符号文字, 正=var节点, 负=var+n节点
def add_clause(a, b):
  add_edge(neg(a), b)   # ¬a -> b
  add_edge(neg(b), a)   # ¬b -> a
# 判解: Tarjan SCC
# 无解 iff scc[id(x)] == scc[id(not x)]
# 赋值: val[x] = scc[id(x)] > scc[id(not x)]  (取SCC编号小者/反拓扑序靠后)
#   等价于 若 id(x)的scc编号 < id(not x)的scc编号 则 x=true
```

### Python 实现

```python
import sys

sys.setrecursionlimit(1 << 25)


def solve_two_sat(n, clauses):
    """求解2-SAT.
    n: 变量个数(0..n-1)
    clauses: list[(a, b)], a/b为文字: 正数表示变量i, 负数表示¬i (i为1..n)
    return: (bool, list[int]|None) 是否可行 + 每组变量赋值(True/False)
    """
    # 节点: var i(1..n) -> 真节点 2*i, 假节点 2*i+1
    def node(x):  # 文字x(带符号)到节点编号
        v = abs(x)
        return 2 * v + (0 if x > 0 else 1)

    def neg(x):  # 文字取反
        return -x

    N = 2 * n + 2
    g = [[] for _ in range(N)]
    rg = [[] for _ in range(N)]

    def add_edge(u, v):
        g[u].append(v)
        rg[v].append(u)

    for a, b in clauses:
        add_edge(node(neg(a)), node(b))   # ¬a -> b
        add_edge(node(neg(b)), node(a))   # ¬b -> a

    # Kosaraju SCC
    visited = [False] * N
    order = []

    def dfs(u):
        visited[u] = True
        for v in g[u]:
            if not visited[v]:
                dfs(v)
        order.append(u)

    for i in range(N):
        if not visited[i]:
            dfs(i)

    comp = [-1] * N

    def rdfs(u, cid):
        comp[u] = cid
        for v in rg[u]:
            if comp[v] == -1:
                rdfs(v, cid)

    cid = 0
    for u in reversed(order):
        if comp[u] == -1:
            rdfs(u, cid)
            cid += 1

    for i in range(1, n + 1):
        if comp[2 * i] == comp[2 * i + 1]:
            return False, None  # x与其否定同SCC, 无解

    # 赋值: 取SCC编号更大者为真 (Kosaraju cid与Tarjan同语义: 大cid=反拓扑序靠前)
    # 更通用的做法: 取拓扑序在后者为真, 此处用 comp 编号比较
    val = [False] * (n + 1)
    for i in range(1, n + 1):
        val[i] = comp[2 * i] > comp[2 * i + 1]
    return True, val[1:]


if __name__ == "__main__":
    # 测试1: (x1∨x2), (¬x1∨x3), (¬x2∨¬x3): 有解
    clauses1 = [(1, 2), (-1, 3), (-2, -3)]
    ok, val = solve_two_sat(3, clauses1)
    assert ok, "should be satisfiable"
    # 验证约束
    def check(val, clauses):
        for a, b in clauses:
            fa = val[abs(a) - 1] if a > 0 else not val[abs(a) - 1]
            fb = val[abs(b) - 1] if b > 0 else not val[abs(b) - 1]
            if not (fa or fb):
                return False
        return True

    assert check(val, clauses1), f"assignment {val} violates"

    # 测试2: (x1∨x1) 且 (¬x1∨¬x1): 无解
    clauses2 = [(1, 1), (-1, -1)]
    ok2, val2 = solve_two_sat(1, clauses2)
    assert not ok2, "should be unsatisfiable"

    # 测试3: (x1∨x2), (¬x1∨¬x2): 有解(x1=true,x2=false 或反之)
    clauses3 = [(1, 2), (-1, -2)]
    ok3, val3 = solve_two_sat(2, clauses3)
    assert ok3 and check(val3, clauses3), (val3, clauses3)

    print("two-sat: ALL TESTS PASSED")

```

**PyPy 提示**: SCC用迭代或提高递归限制均可。建图时注意变量下标从1开始、节点编号2*i与2*i+1，防止越界。Kosaraju与Tarjan的SCC编号方向不同，赋解比较大小前需确认语义(取拓扑序靠后者为真)。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(V+E) — 建图O(n+m) + SCC O(n+m) |
| 空间 | O(V+E) — 蕴含图(2n节点,2m边) |

### 局限

仅适用于每个约束为二元析取式的2-SAT；一般k-SAT(k>2)为NP完全不可解。蕴含图需保证对称性(每条约束两条蕴含边成对)，否则取解贪心会失效。只求可行性或一组解，不保证解唯一。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P4782 | 3 | 【模板】2-SAT：建蕴含图+SCC判定可行性并输出一组解 | [https://www.luogu.com.cn/problem/P4782](https://www.luogu.com.cn/problem/P4782) |
| HDU | 3062 | 3 | Party：夫妻二选一+矛盾约束，经典2-SAT可行性判定 | [https://acm.hdu.edu.cn/showproblem.php?pid=3062](https://acm.hdu.edu.cn/showproblem.php?pid=3062) |
| Luogu | P5782 | 4 | 和平委员会：两党代表会议，输出一组合法方案 | [https://www.luogu.com.cn/problem/P5782](https://www.luogu.com.cn/problem/P5782) |

## Pitfalls · 易错点

- 每条约束必须建两条对称蕴含边，只建一条会导致对称性破坏、贪心赋解出错
- 变量节点与否定节点下标映射错误(如1-based/0-based混用)是最常见bug
- 判定无解条件：x与¬x在同一SCC，注意是'所在SCC编号相同'而非'有边可达'
- 取解用SCC编号比较方向需与所用SCC算法的编号语义匹配(Kosaraju与Tarjan相反)
- 自环约束如(a∨a)退化为强制a=true, (¬a∨¬a)退化为强制a=false，建图时同样处理

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/2-sat/](https://oi-wiki.org/graph/2-sat/)
- CP-Algorithms ✓ [https://cp-algorithms.com/graph/2SAT.html](https://cp-algorithms.com/graph/2SAT.html)
- 书籍 ✓ `CPH ch20 pp191-204`
