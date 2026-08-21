---
id: stern-brocot-tree
name: Stern-Brocot 树与 Farey 序列
group: G-D-10
stage: advanced
priority: P2
depth_tier: standard
---

# Stern-Brocot 树与 Farey 序列

> 生成所有既约正有理数的二叉搜索树：相邻分数插入中位分数 (a+c)/(b+d)，支持二分定位任意有理数与最优有理逼近，关联连分数与 Farey 序列

<!-- 元信息: id=stern-brocot-tree · group=G-D-10 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

Stern-Brocot 树是一棵以 0/1、1/0（表示 +∞）为边界、通过反复插入相邻分数中位分数 (a+c)/(b+d) 构造的无限二叉搜索树，包含全部正的最简有理数且每个恰好出现一次。每个节点对应一个三元组 ((a/b),(p/q),(c/d))，实际存储的分数是中间元素 p/q。三条基本性质：①单调性——第 k 阶 Stern-Brocot 序列单调递增；②最简性——相邻分数满足 bc−ad=1（因此由裴蜀定理所有分数互素）；③完全性——任意正有理数都在树上（否则搜索无限长，可证明每一步 a+b+c+d 严格增大而 p+q 有界，矛盾）。Stern-Brocot 树同时是分子分母的二叉搜索树、堆与笛卡尔树。每个分数 p/q 可由连分数 [t0;t1;…;tn;1] 表示，连分数系数恰好编码从根到该节点的路径（偶数项向右、奇数项向左）。Farey 序列 F(n) 是分母不超过 n 的 0..1 间既约分数按序排列，可从 Stern-Brocot 树裁剪得到，长度 L(n)=1+Σ_{k=1}^n φ(k)。矩阵视角：左/右子节点移动分别对应乘以 L=[[1,1],[0,1]] 与 R=[[1,0],[1,1]]。

## Why · 为什么

### 直觉 · Intuition

把分数看成实数轴上的点，每次在相邻两个分数之间插入一个中位分数，得到的序列单调且越来越密。如果把它组织成树（每个插入的分数作为两个边界的共同子节点），就成了一棵二叉搜索树：要找一个分数，比较当前分数与目标的大小，大往左小往右。关键洞察是相邻分数 a/b 与 c/d 之间一定满足 bc−ad=1（行列式为 1），这个性质在中位分数插入后保持，既保证最简性，也让'存在性'证明可行。

### 原理 · Principle

构造：第 0 阶序列为 0/1, 1/0；第 k+1 阶在相邻 (a/b,c/d) 间插入 (a+c)/(b+d)。单调性由 a/b < (a+c)/(b+d) < c/d（消分母即得）归纳保持。最简性：相邻分数行列式 bc−ad=1，中位数插入后 b(a+c)−a(b+d)=bc−ad=1 与 c(b+d)−d(a+c)=bc−ad=1 仍成立，故所有分数互素。完全性：任意 p/q 的搜索若无限，则每步 bx−ay≥1、cy−dx≥1，乘 (c+d)、(a+b) 相加并利用 bc−ad=1 得 p+q≥a+b+c+d，而每深入一层右侧严格增大，矛盾，故必有限步命中。快速查找：连续向右 t 次等价于左边界从 a/b 变为 (a+tc)/(b+td)，连续向左 t 次右边界变为 (ta+c)/(tb+d)，用连分数辗转相除 O(log min(p,q)) 得到路径的游程编码。

### 历史 · History

1858 年德国数学家 Moritz Stern 与 1861 年法国钟表匠 Achille Brocot 独立发现（Brocot 用于设计齿轮传动比的钟表领域；有些资料将更早的发现归于古希腊 Eratosthenes）。1816 年英国地质学家 John Farey 猜想 Farey 序列中每个分数都是邻居的中位分数，随后被 Cauchy 证明，但 Haros 于 1802 年已得出几乎相同的结论。CP-Algorithms 指出序列 [a1;a2;…;an;1] 的连分数表示中，渐近分数列即搜索边界序列。

## How · 实现

### 伪代码

```python
# 朴素查找: O(p+q), 每步一次中位数比较
bounds = (0/1, 1/0)
while True:
    m = mediant(l, r)
    if m == target: break
    if target < m: r = m; path += 'L'
    else:          l = m; path += 'R'

# 快速查找(目标分数已知): O(log min(p,q)), 连分数/辗转相除
res = []
right = True
while q:
    res.append((p // q, 'R' if right else 'L'))
    p, q = q, p % q
    right ^= 1
res[-1].first -= 1   # 最后一个系数减 1

# Farey 序列长度: L(n) = 1 + sum phi(k)
```

### Python 实现

```python
# -*- coding: utf-8 -*-
# Stern-Brocot 树：朴素查找（O(p+q) 路径串）
def stern_naive(p, q):
    """返回从根到 p/q 的路径串（'L'/'R'）。"""
    # 边界 (pa/pb, qa/qb) = (0/1, 1/0)
    pa, pb, qa, qb = 0, 1, 1, 0
    res = []
    while True:
        pm, qm = pa + qa, pb + qb
        if pm == p and qm == q:
            break
        if p * qm < pm * q:          # p/q < pm/qm -> 向左
            qa, qb = pm, qm
            res.append('L')
        else:                        # 否则向右
            pa, pb = pm, qm
            res.append('R')
    return ''.join(res)


# 快速查找：连分数/辗转相除得到游程编码（目标分数已知）
def stern_fast(p, q):
    """返回 [(次数, 方向)]，方向交替，复杂度 O(log min(p,q))。"""
    res = []
    right = True
    while q:
        res.append((p // q, 'R' if right else 'L'))
        p, q = q, p % q
        right ^= 1
    res[-1] = (res[-1][0] - 1, res[-1][1])   # 最后一个系数减 1
    return res


# Farey 序列长度 L(n) = 1 + sum_{k=1}^n phi(k)
def farey_len(n):
    phi = list(range(n + 1))
    for i in range(2, n + 1):
        if phi[i] == i:
            for j in range(i, n + 1, i):
                phi[j] -= phi[j] // i
    return 1 + sum(phi[1:])


if __name__ == '__main__':
    # 朴素与快速查找在随机互素小数据上对拍
    import random
    for _ in range(300):
        p = random.randint(1, 40)
        q = random.randint(1, 40)
        g = __import__('math').gcd(p, q)
        p, q = p // g, q // g          # 只有最简分数在树上
        a = stern_naive(p, q)
        b = []
        for cnt, dd in stern_fast(p, q):
            b.extend(dd * cnt)
        assert ''.join(b) == a, (p, q, b, a)
    # 已知小例子
    assert stern_naive(1, 2) == 'L'
    assert stern_naive(2, 1) == 'R'
    assert stern_naive(1, 1) == ''
    assert stern_naive(3, 5) == 'LRL'
    # Farey 序列长度 F(5)=11, F(6)=13, F(10)=33
    assert farey_len(5) == 11, farey_len(5)
    assert farey_len(6) == 13
    assert farey_len(10) == 33
    print('stern-brocot tests passed')

```

**PyPy 提示**: 朴素查找 O(p+q) 在 p,q 大时不可用；快速查找用整数除法无大整数开销，PyPy 下直接可跑。注意 Python 大整数乘法做分数比较时用交叉相乘 p*qm < pm*q 可避免浮点误差。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 朴素查找 O(p+q)；快速查找（连分数/辗转相除）O(log min(p,q))；未知目标需二分次数时 O(log²(p+q))；建前 n 层树 O(n²) |
| 空间 | O(1)（迭代）/ O(路径长) |

### 局限

Stern-Brocot 树在竞赛中多为数论背景或隐含考点（与连分数、Farey 序列、丢番图逼近联动）。朴素查找只能处理小分数；对无理数的有理逼近需注意左右端点距目标的距离比较（逼近误差并非严格递减）。完全性证明要求分数为正。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| UVa | 12995 | 3 | Farey Sequence 长度公式 L(n)=1+Σφ(k)，欧拉函数前缀和 | [https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=4386](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=4386) |
| AtCoder | ABC333-F | 5 | 题名 Bomb Game 2，涉及分数区间均分，可用 Stern-Brocot/分数序列思想辅助构造 | [https://atcoder.jp/contests/abc333/tasks/abc333_f](https://atcoder.jp/contests/abc333/tasks/abc333_f) |
| Luogu | P1966 | 4 | 火柴排队：排序序数与逆序对，排序思想与分数排序同源 | [https://www.luogu.com.cn/problem/P1966](https://www.luogu.com.cn/problem/P1966) |

## Pitfalls · 易错点

- 1/0 不是分数而是 +∞ 的记号，作为右边界参与中位数计算但不能输出
- 中位分数 (a+c)/(b+d) 的分子分母分别相加即可，不必约分（行列式性质保证互素）
- 朴素查找路径长度可达 O(p+q)（如 1/n 的情形），大分数必须用连分数快速查找
- 连分数编码最后一项系数要减 1（[t0;t1;…;tn;1] 中末尾的 1），漏掉会错位
- 对无理数逼近时近似序列误差不是严格递减的，结尾要比较左右端点距目标的距离
- Farey 序列含 0/1 与 1/1 两个端点，长度公式 1+Σφ 的 1 是端点 0/1

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/number-theory/stern-brocot/](https://oi-wiki.org/math/number-theory/stern-brocot/)
- CP-Algorithms ✓ [https://cp-algorithms.com/others/stern_brocot_tree_farey_sequences.html](https://cp-algorithms.com/others/stern_brocot_tree_farey_sequences.html)
