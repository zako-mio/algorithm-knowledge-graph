---
id: dp-state
name: 状压DP
group: G-A-11
stage: intermediate
priority: P1
depth_tier: standard
---

# 状压DP

> 集合状态编码为二进制整数，适合小规模状态空间

<!-- 元信息: id=dp-state · group=G-A-11 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

状压DP(状态压缩DP)通过将状态集合编码为二进制整数来实现状态转移。当问题的状态可以用n位二进制表示(n个独立二元决策，如棋盘上每格放/不放)且n较小(通常<=20)时，用整数bitmask表示状态集合，利用位运算高效转移。典型问题包括棋盘国王放置、TSP旅行商等。

## Why · 为什么

### 直觉 · Intuition

当状态是一个「子集」（哪些元素被选中），用二进制整数的每一位表示对应元素是否被选(1=选,0=不选)。一个n位二进制数可以表示2^n种子集状态。状态转移时用位运算(&,|,^,<<,>>)高效操作子集。前提是n不能太大(2^n要可承受)。

### 原理 · Principle

核心位运算：S & (1<<i) 判断i是否在S中；S | (1<<i) 加入i；S ^ (1<<i) 翻转i；S & (S-1) 去掉最低位的1；枚举子集 for(T=S; T; T=(T-1)&S)。状态转移：f[S][i]表示已访问集合S且当前在i的最优值，f[S|1<<j][j]=min(f[S][i]+cost(i,j))。棋盘型：f[i][S]表示前i行、第i行状态S的方案数，检查S内部合法性和相邻行兼容性。

### 历史 · History

状压DP是竞赛中处理小规模状态空间的标准技术。其核心思想——将子集编码为整数、用位运算转移——在TSP(旅行商问题)、棋盘覆盖、集合划分等问题中广泛应用。OI Wiki以SCOI2005互不侵犯为教学题。

## How · 实现

### 伪代码

```python
# 棋盘国王放置(互不侵犯)
# 预处理每行合法状态(无相邻国王)
valid = [s for s in 0..2^n-1 if (s & (s<<1))==0]
# f[i][s][k] = 前i行第i行状态s放k个国王
for i in 2..N:
  for s in valid:
    for ps in valid:  # 上一行状态
      if (s & ps)==0 and (s & (ps<<1))==0 and (s & (ps>>1))==0:
        f[i][s][k] += f[i-1][ps][k-cnt(s)]
```

### Python 实现

```python
def kings_placement(N, K):
    """SCOI2005 互不侵犯: N×N棋盘放K个国王互不攻击的方案数
    国王攻击8个方向相邻格
    N: 棋盘边长 (1<=N<=9)
    K: 国王数量 (1<=K<=N*N)
    返回: 合法方案数
    """
    # 预处理每行合法状态(同一行内无相邻国王)
    valid = []
    cnt = []  # 各合法状态的国王数
    for s in range(1 << N):
        if (s & (s << 1)) == 0:  # 无相邻
            valid.append(s)
            cnt.append(bin(s).count('1'))

    # f[i][s_idx][k] = 前i行, 第i行状态为valid[s_idx], 共放k个国王
    f = [[[0] * (K + 1) for _ in range(len(valid))] for _ in range(N + 1)]

    # 初始化第1行
    for si, s in enumerate(valid):
        if cnt[si] <= K:
            f[1][si][cnt[si]] = 1

    for i in range(2, N + 1):
        for si, s in enumerate(valid):
            for pi, ps in enumerate(valid):  # 上一行状态
                # 兼容性检查: 上下不相邻, 对角不相邻
                if (s & ps) != 0:
                    continue
                if (s & (ps << 1)) != 0:
                    continue
                if (s & (ps >> 1)) != 0:
                    continue
                for k in range(cnt[si], K + 1):
                    f[i][si][k] += f[i - 1][pi][k - cnt[si]]

    ans = 0
    for si in range(len(valid)):
        ans += f[N][si][K]
    return ans


def tsp(n, dist):
    """状压DP求TSP(旅行商问题)最短路径
    n: 城市数 (n<=15)
    dist: 距离矩阵 dist[i][j]
    返回: 从0出发经过所有城市回到0的最短路径
    """
    INF = float('inf')
    f = [[INF] * n for _ in range(1 << n)]
    f[1][0] = 0  # 从城市0出发, 只访问了0

    for S in range(1, 1 << n):
        if not (S & 1):
            continue  # 必须包含城市0
        for i in range(n):
            if not (S & (1 << i)):
                continue
            if f[S][i] == INF:
                continue
            for j in range(n):
                if S & (1 << j):
                    continue  # j已访问
                ns = S | (1 << j)
                nd = f[S][i] + dist[i][j]
                if nd < f[ns][j]:
                    f[ns][j] = nd

    ans = INF
    for i in range(1, n):
        if f[(1 << n) - 1][i] + dist[i][0] < ans:
            ans = f[(1 << n) - 1][i] + dist[i][0]
    return ans


if __name__ == "__main__":
    # 互不侵犯: 3x3棋盘放2个国王
    # 答案应为16
    assert kings_placement(3, 2) == 16, f"Expected 16, got {kings_placement(3, 2)}"
    # 1x1放1个 = 1
    assert kings_placement(1, 1) == 1

    # TSP: 4个城市
    dist = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    # 0->1->3->2->0 = 10+25+30+15 = 80
    assert tsp(4, dist) == 80, f"Expected 80, got {tsp(4, dist)}"

    print("All tests passed.")

```

**PyPy 提示**: PyPy对位运算和列表访问优化好。N=9的棋盘状压DP约0.1s。TSP n=15约0.5s(2^15*15*15≈7M次操作)。注意f表大小2^n*n。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 棋盘型: O(N * \|valid\|² * K)；TSP: O(2^n * n²) |
| 空间 | 棋盘型: O(N * \|valid\| * K)；TSP: O(2^n * n) |

### 局限

状态空间2^n在n>20时不可承受(2^20=1M)。棋盘型N<=9。TSP n<=15。Python对2^20级别的状态枚举较慢，需PyPy。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| LOJ | 2153 | 3 | SCOI2005 互不侵犯：棋盘状压DP模板题 | [https://loj.ac/problem/2153](https://loj.ac/problem/2153) |
| Luogu | P1879 | 3 | USACO玉米田：棋盘状压DP，兼容性检查 | [https://www.luogu.com.cn/problem/P1879](https://www.luogu.com.cn/problem/P1879) |
| LeetCode | 943 | 4 | 最短超串：TSP状压DP变形 | [https://leetcode.cn/problems/find-the-shortest-superstring/](https://leetcode.cn/problems/find-the-shortest-superstring/) |

## Pitfalls · 易错点

- 合法状态预处理：棋盘同行不能有相邻国王 s&(s<<1)==0
- 兼容性检查：上下行间检查 s&ps==0(竖向) 和 s&(ps<<1)==0 且 s&(ps>>1)==0(对角)
- 枚举子集的写法 for(T=S; T; T=(T-1)&S) 不能写成 T--
- TSP中f[S][i]的S必须包含i，否则状态无意义

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/dp/state/](https://oi-wiki.org/dp/state/)
- CP-Algorithms ✓ [https://cp-algorithms.com/dynamic_programming/profile-dynamics.html](https://cp-algorithms.com/dynamic_programming/profile-dynamics.html)
