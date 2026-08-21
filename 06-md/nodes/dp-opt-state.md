---
id: dp-opt-state
name: 状态设计优化
group: G-A-12
stage: intermediate
priority: P2
depth_tier: standard
---

# 状态设计优化

> 改变状态定义降低维度/状态数，题目特异性优化

<!-- 元信息: id=dp-opt-state · group=G-A-12 · stage=intermediate · priority=P2 · depth_tier=standard -->

## What · 是什么

状态设计优化（状态定义优化）不是通用的转移加速套路，而是通过重新设计 DP 状态的维度与含义来减少状态总数或转移代价。常见手法：(1) 交换答案与状态——当某维值域小、另一维巨大时，把'值'当状态、把'原状态'当 DP 值（如大容量背包：容量 1e18 但总价值小，状态改为'价值 j 的最小体积'）；(2) 压缩冗余状态——布尔状态压成位集（如 n<=20 的哈密顿回路 O(n^2 2^n) 压到 O(n 2^n/w)）；(3) 对调答案与第一维（如 LCS 中把'前缀长度'与'LCS 值'对调，配合贪心）。这类优化题目特异性强，需结合数据范围分析哪一维是瓶颈。

## Why · 为什么

### 直觉 · Intuition

DP 复杂度 = 状态数 × 转移数。瓶颈常在某一维过大。若发现'过大的一维'其实只是用来承载一个值域很小的量（答案、价值、LCS 长度），就把这个小的量变成状态，把过大的维变成 DP 值——谁小谁是状态。

### 原理 · Principle

以 0-1 背包为例：状态 (前 i 件, 容量 j) 容量 1e18 不可行；改定义 f[i][j]=选前 i 件价值恰为 j 的最小体积，价值总量 sum w <=1e3 可行，转移 f[i][j]=min(f[i-1][j], f[i-1][j-w_i]+v_i)，复杂度 O(n·sum w)。核心是'维度对调'保持转移正确性。哈密顿回路版用位集把 n 个 bool 结果压成一个 int，配合邻接矩阵位压缩，把 n^2 系数降为 n/w。

### 历史 · History

状态设计优化散见于各类 OI 教材与题解，OI Wiki 的 dp/opt/state 页面以 LCS、哈密顿回路、超大容量背包三个例题系统讲解'对调维度''压缩布尔态'两类思想。这是竞赛中'从数据范围反推状态设计'的核心技巧，与 DP 常规优化并列。

## How · 实现

### 伪代码

```python
# 例1: 超大容量背包 (容量 1e18, 总价值<=1e3)
# 状态: f[j] = 价值恰为 j 的最小体积
INF = inf; f[0]=0; f[1..W]=INF
for (v_i, w_i) in items:
    for j in range(W, w_i-1, -1):
        f[j] = min(f[j], f[j-w_i] + v_i)
ans = max{ j : f[j] <= C }   # 容量 C 内最大可达价值

# 例2: n<=20 哈密顿回路判定
# dp[mask] 为 int 位集, 第 i 位=以 i 结尾可达; 邻接矩阵也压成位集
for mask in range(1<<n):
    for i in bits(mask):            # 末尾 i
        reach = adj[i] & ~mask      # 可从 i 扩展的点
        for j in bits(reach):
            dp[mask|(1<<j)] |= 1<<j
```

### Python 实现

```python
import bisect


def dp_opt_bit_hamiltonian(adj):
    """状态设计优化(Hamiltonian 判定, n<=20) 的位压缩版:
    常规 O(n^2 2^n) 用位集压缩为 O(n 2^n / w).
    这里用 Python int 作为位集: dp[mask] 的第 i 位 = 能否以 i 结尾访问 mask."""
    n = len(adj)
    dp = [0] * (1 << n)
    for s in range(n):
        dp[1 << s] |= 1 << s  # 可从任意点出发
    for mask in range(1 << n):
        ends = dp[mask]
        if not ends:
            continue
        # 遍历可作为末端的点 i (dp[mask] 的置位)
        m = ends
        while m:
            lb = m & -m
            i = lb.bit_length() - 1
            # 从 i 扩展到相邻且不在 mask 中的 j
            reach = adj[i] & ~mask
            r = reach
            while r:
                lj = r & -r
                dp[mask | lj] |= lj
                r ^= lj
            m ^= lb
    full = (1 << n) - 1
    return dp[full] != 0


def hamiltonian_brute(adj):
    """暴力回溯验证小数据。"""
    n = len(adj)

    def rec(v, visited, count):
        if count == n:
            return True
        for u in range(n):
            if (adj[v] >> u) & 1 and not (visited >> u) & 1:
                if rec(u, visited | (1 << u), count + 1):
                    return True
        return False

    for s in range(n):
        if rec(s, 1 << s, 1):
            return True
    return False


def random_graph(n, p):
    adj = [0] * n
    for i in range(n):
        for j in range(n):
            if i != j and random.random() < p:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
    return adj


if __name__ == "__main__":
    import random
    for _ in range(60):
        n = random.randint(2, 7)
        g = random_graph(n, 0.5)
        a = dp_opt_bit_hamiltonian(g)
        b = hamiltonian_brute(g)
        assert a == b, (g, a, b)
    # 路径图: 0-1-2-... 存在哈密顿路径
    n = 6
    adj = [0] * n
    for i in range(n - 1):
        adj[i] |= 1 << (i + 1)
        adj[i + 1] |= 1 << i
    assert dp_opt_bit_hamiltonian(adj) is True
    # 完全二分 K3,3 无边不成图? 构造孤立点: 无哈密顿
    adj = [0] * 5
    assert dp_opt_bit_hamiltonian(adj) is False
    print("dp_opt state-design (bit-hamiltonian) tests passed")

```

**PyPy 提示**: 位集压缩在 PyPy 上 int 操作快；遍历 bits 用 (x&-x) 逐位取最低位，比逐位测试快。超大背包场景 Python 直接可过 O(n·sum w)。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 因题目而异: 对调维度后由小维度决定; 位压缩版 O(n 2^n / w) |
| 空间 | 由新状态规模决定 |

### 局限

无通用模板，每个题需重新设计状态，题目特异性强。对调维度要求'答案/价值'值域足够小，否则退化。位压缩要求布尔型 DP 且 n 小(<=~22)。转移必须与新状态语义一致，改状态时漏改转移是最常见错误。Python 位集 2^22 以上内存压力大。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| AtCoder | dp_q | 3 | Flowers: 线段树/BIT 优化+状态维度合理设置 | [https://atcoder.jp/contests/dp/tasks/dp_q](https://atcoder.jp/contests/dp/tasks/dp_q) |
| Luogu | P1081 | 4 | NOIP2012 开车旅行: 倍增优化 DP 的状态设计 | [https://www.luogu.com.cn/problem/P1081](https://www.luogu.com.cn/problem/P1081) |
| Luogu | P1613 | 3 | 跑路: 二进制倍增状态+最短路, 状态设计巧思 | [https://www.luogu.com.cn/problem/P1613](https://www.luogu.com.cn/problem/P1613) |

## Pitfalls · 易错点

- 对调维度后忘记同步修改转移方程(用错下标)
- 布尔状态位压缩时忘记按 w 取整(CPU 字长)
- 容量/价值值域判断错误导致状态仍过大
- 状态语义歧义: 是'恰好'还是'不超过', 初始化 INF/0 混用

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/dp/opt/state/](https://oi-wiki.org/dp/opt/state/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/dp/opt/state.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/dp/opt/state.md)
