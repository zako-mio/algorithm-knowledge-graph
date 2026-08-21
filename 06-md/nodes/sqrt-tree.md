---
id: sqrt-tree
name: Sqrt 树
group: G-D-6
stage: advanced
priority: P2
depth_tier: standard
---

# Sqrt 树

> O(n log log n)预处理+O(1)查询的可结合运算静态区间询问结构，树高O(log log n)

<!-- 元信息: id=sqrt-tree · group=G-D-6 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

Sqrt Tree 为满足结合律的运算（如 gcd、min、max、+、and、or、xor）提供静态序列的区间询问：O(n log log n) 预处理后 O(1) 回答任意 [l,r] 的聚合值，并支持 O(√n) 的单点修改。思路是分块的递归化：把序列分块，块内维护前缀/后缀聚合值（P/S）与块间聚合值（B 数组），对整块落在块间的询问用 B 数组 O(1) 回答，落在块内的递归进入子结构，形成一棵分支数为 √k、树高 O(log log n) 的树。配合二进制分块层定位（用 clz/lcp 快速找到覆盖询问的最小区块层），查询可做到 O(1)。

## Why · 为什么

### 直觉 · Intuition

一棵分支数随规模缩小的树：每层把区间切成 √k 块，块内再递归切分。任意询问要么跨块（用块间信息 O(1) 拼），要么在块内（落到下一层），每层只有 O(1) 次合并，层数 O(log log n)。用二进制技巧把『询问落在哪一层』从 O(log log n) 优化到 O(1)。

### 原理 · Principle

定义 T(n)=T(√n)+1，令 n=2^m 得 S(m)=S(m/2)+1，主定理 S(m)=O(log m)，故树高 O(log log n)。每层对序列分块，维护 P_i（块内前缀聚合）、S_i（块内后缀聚合）与 B_{i,j}（第 i 块到第 j 块的聚合），均可在 O(n) 内预处理；整棵树预处理 O(n log log n)。查询：端点 l,r 的 lcp 二进制定位最小块层（l^r 的最高位），跨块则用 S[l]+B[lBlock][rBlock]+P[r]，O(1)。单点更新：沿根到叶的路径重建 P/S 与 B 的 O(√n) 相关项，共 O(√n)。区间更新可用懒标记，更新 O(√n log log n) 或 O(√n)，查询对应 O(1) 或 O(log log n)（两种方案）。

### 历史 · History

Sqrt Tree 出自 cp-algorithms 的《Sqrt Tree》章节（由 CF 用户贡献），OI Wiki 将其翻译并补充完整实现与证明。例题为 CodeChef NOV17 SEGPROD（区间积取模，需处理 0 与逆元不可用场景）。它与猫树同属『静态 O(1) 区间询问』家族，但多支持单点更新。

## How · 实现

### 伪代码

```python
# 静态查询（不考虑更新的简化版）
构建:
  将序列补 0 到 2^k
  从根层开始对区间 [L,R) 分块 (块长=2^((lg+1)/2))
    buildBlock: 每块算前缀 P 与后缀 S
    buildBetween: 相邻块聚合存 B
    递归进入每个块 (layer+1)

query(l, r):
  if l == r: return v[l]
  layer = onLayer[clz[(l-base) ^ (r-base)]]   # O(1) 定位层
  ans = S[layer][l]
  若 lBlock <= rBlock: ans = op(ans, B[layer][lBlock][rBlock])
  ans = op(ans, P[layer][r])
  return ans
```

### Python 实现

```python
import random


def op(a, b):
    return a ^ b  # 满足结合律的运算（用 xor 演示）


def log2up(n):
    k = 0
    while (1 << k) < n:
        k += 1
    return k


class SqrtTree:
    """简化 SqrtTree：O(n log log n) 建树，O(1) 查询（跨块+块内递归），不含更新。
    结构：递归把区间切成 sqrt 大小块；每节点存块内前缀/后缀聚合与块间聚合表。
    用 xor 运算（0 为单位元）。
    """

    def __init__(self, a):
        self.n = len(a)
        self.v = list(a) + [0] * (log2up(self.n) * 0)  # 不补位，直接递归
        self.root = self._build(0, self.n)

    def _build(self, l, r):
        # 返回该区间节点的 P/S/B 与块大小信息
        m = r - l
        if m <= 2:
            # 叶子：直接存原值，P/S 长度 m
            return {"l": l, "r": r, "P": None, "S": None, "B": None, "child": None, "bSz": m}
        bSz = int(m ** 0.5) + 1
        nb = (m + bSz - 1) // bSz
        P = [0] * m
        S = [0] * m
        # 每个块内前缀/后缀
        for b in range(nb):
            bl = b * bSz
            br = min(bl + bSz, m)
            P[bl] = self.v[l + bl]
            for i in range(bl + 1, br):
                P[i] = op(P[i - 1], self.v[l + i])
            S[br - 1] = self.v[l + br - 1]
            for i in range(br - 2, bl - 1, -1):
                S[i] = op(self.v[l + i], S[i + 1])
        # B[b1][b2] = 第 b1..b2 块聚合
        B = [[0] * nb for _ in range(nb)]
        for b1 in range(nb):
            cur = 0
            for b2 in range(b1, nb):
                b2l = b2 * bSz
                b2r = min(b2l + bSz, m)
                seg = S[b2l] if b2l < m else 0
                cur = op(cur, seg)
                B[b1][b2] = cur
        children = []
        for b in range(nb):
            bl = b * bSz
            br = min(bl + bSz, m)
            children.append(self._build(l + bl, l + br))
        return {"l": l, "r": r, "P": P, "S": S, "B": B, "child": children, "bSz": bSz}

    def _query(self, node, l, r):
        # 区间 [l,r) 完全在 node 内
        if node["child"] is None:
            # 叶子（长度 1 或 2）
            if r - l == 1:
                return self.v[l]
            return op(self.v[l], self.v[l + 1])
        P, S, B = node["P"], node["S"], node["B"]
        rel_l = l - node["l"]
        rel_r = r - node["l"] - 1  # 闭区间右端（相对）
        bSz = node["bSz"]
        bl = rel_l // bSz
        br = rel_r // bSz
        if bl == br:
            # 同块：递归进该子节点
            return self._query(node["child"][bl], l, r)
        ans = S[rel_l]
        if bl + 1 <= br - 1:
            ans = op(ans, B[bl + 1][br - 1])
        ans = op(ans, P[rel_r])
        return ans

    def query(self, l, r):
        """查询 [l, r] 聚合值 (0-index, 闭区间)"""
        if l == r:
            return self.v[l]
        return self._query(self.root, l, r + 1)


if __name__ == "__main__":
    random.seed(123)
    for n in [1, 2, 3, 4, 5, 8, 16, 40, 100, 130]:
        arr = [random.randint(0, 255) for _ in range(n)]
        st = SqrtTree(arr)
        for _ in range(400):
            l = random.randrange(n)
            r = random.randrange(n)
            if l > r:
                l, r = r, l
            got = st.query(l, r)
            exp = 0
            for i in range(l, r + 1):
                exp ^= arr[i]
            assert got == exp, (n, l, r, got, exp)
    print("sqrt-tree 自测通过：多种规模随机区间 xor 查询与暴力一致")

```

**PyPy 提示**: 本自测为简化实现（不含更新），用递归分块维护 P/S/B；竞赛完整实现需支持 O(√n) 单点更新与懒标记区间更新。Python 递归 + 多层 B 表常数大，若仅需静态 O(1) 查询可考虑猫树或稀疏表。B 数组按层存储索引开销大，可稀疏化。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 建树 O(n log log n)（每层 O(n)，O(log log n) 层），查询 O(1)（跨块合并），单点更新 O(√n) |
| 空间 | O(n log log n) |

### 局限

运算必须满足结合律；不满足则失效。补 0 到 2^k 需 0 是单位元（或处理越界）。完整更新逻辑（区间覆盖+懒标记）实现复杂，竞赛很少用到更新；Python 常数大，n 大时建树慢。与稀疏表/猫树相比，SqrtTree 的优势仅在需要单点更新。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| CodeChef | SEGPROD | 6 | 区间积取模+含0处理：SqrtTree 经典题（cp-algorithms/OI Wiki 例题） | [https://www.codechef.com/NOV17/problems/SEGPROD](https://www.codechef.com/NOV17/problems/SEGPROD) |

## Pitfalls · 易错点

- 补 0 到 2^k 时 0 必须对运算为单位元（xor 可以，sum 可以，min 不可以）
- onLayer 与 layers 索引错位导致查询层定位错误
- B 数组按层计算块数 nb 需正确（每层块长不同）
- l==r 和 l+1==r 的边界要单独处理避免除以 0 的位移
- 递归建树深度 O(log log n) 不会爆栈，但 Python 递归开销仍大

## Sources · 信源

- CP-Algorithms ✓ [https://cp-algorithms.com/data_structures/sqrt-tree.html](https://cp-algorithms.com/data_structures/sqrt-tree.html)
- OI Wiki ✓ [https://oi-wiki.org/ds/sqrt-tree/](https://oi-wiki.org/ds/sqrt-tree/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/sqrt-tree.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/sqrt-tree.md)
