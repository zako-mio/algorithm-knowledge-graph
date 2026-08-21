---
id: mod-shortest-path
name: 同余最短路
group: G-B-2
stage: advanced
priority: P3
depth_tier: brief
---

# 同余最短路

> 利用同余类建图求最小权值，模数优化

<!-- 元信息: id=mod-shortest-path · group=G-B-2 · stage=advanced · priority=P3 · depth_tier=brief -->

## What · 是什么

同余最短路是一类『用最短路求解模意义下最优值』的建模技巧：把问题状态压缩成模 K 的剩余类 0..K-1，用权值最小的那个数为模数，构造状态转移边（如 i → (i+y) mod K 边权 y），跑单源最短路求出每个同余类能凑到的最小值 d_i，再结合整除计数回答『有多少/最小/最大可拼出的数』。典型：给定若干面额，问能拼出多少种金额、最小不可拼金额、拼出模 K 余 p 的最小值等。

## Why · 为什么

### 直觉 · Intuition

以 P3403 跳楼机为例：操作 2、3 每次改变楼层数 y,z，设 x 为最小操作（模数）。关注 p mod x = i 的『最小可达楼层』d_i，则 (i+y) mod x 的楼层 = d_i+y，这正是一条带权边。于是 x 个剩余类构成图，最短路即得每个同余类的最小值，答案 Σ (h-d_i)/x +1。选取最小面额做模数可最小化图大小（OI Wiki 强调）。

### 原理 · Principle

① 选最小数 min(a) 作模数，状态 i∈[0,mod)；② 对每个其他面额 v 建边 i → (i+v)%mod 权 v；③ 从 0 跑最短路（无负权，Dijkstra 即可）得 d_i=模 mod 余 i 的最小可达值；④ 对特殊只含两类边权的图可退化到 O(mod) 环扫描；⑤ 计数：答案=Σ_i ((H-d_i)/mod +1) 当 d_i≤H。本质是把『无限拼凑』问题投影到有限剩余系上。

### 历史 · History

该方法在竞赛中随 P3403『跳楼机』、P2662『牛场围栏』、『墨墨的等式』等题传播，OI Wiki 单独成章（同余最短路）。其思想源自数论中『用同余压缩状态』与最短路算法的结合，近年在 Arc084B（Small Multiple）等 AtCoder 题中亦有体现。

## How · 实现

### 伪代码

```python
# 求每个模 mod 剩余类的最小可达值
def mod_sp(a, H):
  mod = min(a)
  d[0]=0; 其余 INF
  建边: for v in a[1:]: for i in 0..mod-1: add(i,(i+v)%mod, v)
  dijkstra -> d[]
  ans = sum((H-d[i])//mod + 1 for i if d[i]<=H)
  return ans
```

### Python 实现

```python
import heapq


def count_reachable_H(a, H):
    """给定可重复使用面额 a, 统计 [1,H] 中可被拼出的金额个数."""
    a = list(a)
    mod = min(a)
    INF = float('inf')
    d = [INF] * mod
    d[0] = 0
    pq = [(0, 0)]
    while pq:
        dist, u = heapq.heappop(pq)
        if dist > d[u]:
            continue
        for v in a:
            if v == mod:
                continue
            nu = (u + v) % mod
            nd = dist + v
            if nd < d[nu]:
                d[nu] = nd
                heapq.heappush(pq, (nd, nu))
    ans = 0
    for i in range(mod):
        if d[i] <= H:
            ans += (H - d[i]) // mod + 1
    return ans - 1  # 去掉金额 0 (d_0=0 恒可达, 不在 [1,H] 内)


if __name__ == "__main__":

    def brute(a, H):
        ok = [False] * (H + 1)
        ok[0] = True
        for x in range(1, H + 1):
            for v in a:
                if v <= x and ok[x - v]:
                    ok[x] = True
                    break
        return sum(1 for x in range(1, H + 1) if ok[x])

    # 交叉验证
    import random
    random.seed(71)
    for _ in range(200):
        k = random.randint(1, 4)
        a = [random.randint(1, 9) for _ in range(k)]
        H = random.randint(0, 60)
        # 有 1 则所有数可拼, 结果=H
        if 1 in a:
            assert count_reachable_H(a, H) == H, (a, H)
        else:
            assert count_reachable_H(a, H) == brute(a, H), (a, H)

    # 确定用例: 面额 4,6,9, H=20
    a = [4, 6, 9]
    assert count_reachable_H(a, 20) == brute(a, 20)
    print("All tests passed.")
```

**PyPy 提示**: 模数取最小面额 mod≤1e5；边数 mod·(k-1) 可达 1e7，稀疏图用邻接表+heapq。若只有两类边权可用 O(mod) 环扫描替代 Dijkstra（OI Wiki 实现 2）。PyPy 下 Dijkstra 于 1e5 点 1e7 边需注意常数。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(mod·k·log mod) 建图+Dijkstra；两类边权特化 O(mod) |
| 空间 | O(mod·k) |

### 局限

模数=最小面额，故 mod 不能太大（≤1e5 为宜）。H 极大（2^63）时中间用大整数即可。要求面额≥0；若存在 1 元面额则答案退化为 H，无需建图。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3403 | 5 | 跳楼机：OI Wiki 官方例题，同余最短路入门 | [https://www.luogu.com.cn/problem/P3403](https://www.luogu.com.cn/problem/P3403) |
| Luogu | P2371 | 6 | 国家集训队 墨墨的等式：区间计数版同余最短路 | [https://www.luogu.com.cn/problem/P2371](https://www.luogu.com.cn/problem/P2371) |
| Luogu | P2662 | 6 | 牛场围栏：最小不可拼数，同余最短路应用 | [https://www.luogu.com.cn/problem/P2662](https://www.luogu.com.cn/problem/P2662) |

## Pitfalls · 易错点

- 模数必须选最小面额，否则图过大/错误
- 面额含 1 时直接输出 H，别建图
- d[i] 用 INF 初始化，统计时若 d[i]>H 则该项贡献 0
- 两类边权特化时要证明环结构（gcd(x,y) 个环）再用 O(mod)
- H 是金额上界而非数量，别混淆

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/graph/mod-shortest-path/](https://oi-wiki.org/graph/mod-shortest-path/)
- web ✓ [https://atcoder.jp/contests/arc084/tasks/arc084_b](https://atcoder.jp/contests/arc084/tasks/arc084_b)
