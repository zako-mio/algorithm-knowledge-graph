---
id: dsu-weighted
name: 带权/扩展域并查集
group: G-A-4
stage: intermediate
priority: P1
depth_tier: standard
---

# 带权/扩展域并查集

> 在并查集边上维护权值/种类关系，支持相对距离查询与冲突判定，O(α(n))

<!-- 元信息: id=dsu-weighted · group=G-A-4 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

带权并查集（weighted union-find）在普通并查集的每个节点上额外记录一个『到父节点的边权』weight[x]，使每条树边承载任意可结合代数结构（模 3 加法群、异或、普通整数距离等）。经典应用：食物链式『种类关系』（模 3 群：x 与 y 同类/吃/被吃），以及扩展域并查集（把每个元素拆成多个状态点，用普通并查集维护状态集合）。二者等效：模数小的种类关系常用扩展域（好写、不易错），一般关系用带权。注意：路径压缩时需沿路径累加边权；按秩/大小合并时需推导新连边的权值。与普通并查集复杂度同为近似 O(1)/操作（路径压缩+启发式合并，反阿克曼 O(α(n))）。

## Why · 为什么

### 直觉 · Intuition

把每个集合当成一棵‘势能树’：根是参照物，weight[x] 表示 x 相对根的势差。想知道 x,y 的关系，先让它们都找到自己的根，用根对齐两个势差即可相减；合并时只要算准新加的那条边的势差，使两棵树的势能标尺对齐。扩展域视角：把每个物体的全部可能状态（如 A/B/C 三类）拆成独立节点，『在同一集合』即『处于同一种关系』。

### 原理 · Principle

带权并查集满足不变式：对集合内任意 x，weight[x] 恒等于从 x 到当前根的势差（find 时先递归得到根的势差并累加到自身，即路径压缩维护）。查询关系 diff(x,y)=weight[x]-weight[y]；合并 x,y（声称差为 d）时，设 rx,ry 为根，需解 weight[rx'] 使 (wx + w_rx') - wy ≡ d，其中 w_rx' 是新连边权；若 rx,ry 已同根则检查 (wx-wy)%M==d 判断是否冲突。模 M 下全部运算取模。正确性依赖模运算下『差恒定』与并查集的传递性；路径压缩只改结构不改相对差。

### 历史 · History

并查集由 Galler 与 Fisher 1964 年提出；带权/种类并查集是 OI 圈的常见改造，食物链（NOI2001）使它成为经典模板题。OI Wiki 在《并查集》页『拓展操作』一节系统给出带权并查集（Unionfind with Potential 模板）与扩展域并查集两种做法，并强调『可持久化并查集、线段树分治+并查集』中只用启发式合并不做路径压缩的取舍。

## How · 实现

### 伪代码

```python
class WeightedDSU:
  # weight[x]: x 到根(势差), 模 MOD
  def find(x):
    if parent[x] != x:
      r, w = find(parent[x])
      weight[x] = (weight[x] + w) % MOD
      parent[x] = r
    return parent[x], weight[x]
  def diff(x, y):  # 需同根
    return (weight[x] - weight[y]) % MOD
  def merge(x, y, d):  # 声明 x 相对 y 差为 d
    rx, wx = find(x); ry, wy = find(y)
    if rx == ry: return (wx - wy) % MOD == d % MOD  # 冲突?
    # 把 rx 挂到 ry: 新边权 w 使 wx + w - wy = d => w = d + wy - wx
    parent[rx] = ry; weight[rx] = (d + wy - wx) % MOD
    return True
```

### Python 实现

```python
class WeightedDSU:
    """带权并查集：维护每个节点到其根的距离/相对关系.
    weight[x] = 从 x 到 root 的"势差"(自定义运算, 例如模 MOD 意义下的差/异或/距离).
    这里默认支持模 MOD 加法群 (食物链式 种类关系), 也支持普通距离.
    """
    def __init__(self, n, MOD=1):
        self.parent = list(range(n))
        self.weight = [0] * n   # 到根节点的权值(取模 MOD 或普通)
        self.size = [1] * n
        self.MOD = MOD

    def find(self, x):
        # 路径压缩: 递归累加权值
        if self.parent[x] != x:
            r, w = self.find(self.parent[x])
            self.weight[x] = (self.weight[x] + w) % self.MOD
            self.parent[x] = r
        return self.parent[x], self.weight[x]

    def related(self, x, y):
        return self.find(x)[0] == self.find(y)[0]

    def diff(self, x, y):
        """x 相对 y 的差(带权值), 要求 x,y 同根. 返回 weight[x] - weight[y] (mod MOD)"""
        rx, wx = self.find(x)
        ry, wy = self.find(y)
        assert rx == ry
        return (wx - wy) % self.MOD

    def merge(self, x, y, d):
        """声明: x 相对 y 的差为 d, 即 weight[x] - weight[y] == d (mod MOD).
        若 x,y 已同根则返回 False(冲突), 否则合并返回 True."""
        rx, wx = self.find(x)
        ry, wy = self.find(y)
        if rx == ry:
            return (wx - wy) % self.MOD == d % self.MOD
        # 把 rx 的根接到 ry 的根.  需要: weight[rx] = wx' 使 wx'+wx - wy == d
        # => 从 x 走: weight[x]=wx 相对 rx, 若令 rx 相对 ry 为 w, 则 x 相对 y = wx + w - wy = d
        # => w = d + wy - wx
        w = (d + wy - wx) % self.MOD
        if self.size[rx] < self.size[ry]:
            self.parent[rx] = ry
            self.weight[rx] = w
            self.size[ry] += self.size[rx]
        else:
            self.parent[ry] = rx
            # 此时 ry 接到 rx: 需要 y 相对 rx 的权 = wy', 使 wx - (wy'+wy)=d => wy' = wx - wy - d
            self.weight[ry] = (wx - wy - d) % self.MOD
            self.size[rx] += self.size[ry]
        return True


if __name__ == "__main__":
    # 测试 1: 模 3 食物链式关系 (P2024 风格)
    dsu = WeightedDSU(6, MOD=3)
    # 1 吃 2 (x相对y差为1), 2 吃 3, 则 1 吃 3 (差2 = -1)
    assert dsu.merge(0, 1, 1)
    assert dsu.merge(1, 2, 1)
    assert dsu.diff(0, 2) == 2   # 1 吃 3
    # 3 与 1 同类? 1-3差=2 ≠0, 冲突
    assert dsu.diff(0, 2) != 0
    # 声明 3 与 0 同类 -> 冲突(已经 0 吃 3)
    assert not dsu.merge(0, 2, 0)
    # 测试 2: 普通距离 (银河英雄传说式, MOD=1 无取模)
    d2 = WeightedDSU(4, MOD=1 << 60)
    assert d2.merge(0, 1, 5)      # weight[0]-weight[1]=5
    assert d2.diff(0, 1) == 5
    assert d2.merge(2, 0, 3)      # weight[2]-weight[0]=3
    assert d2.diff(2, 1) == 8
    # 测试 3: 随机与暴力交叉验证
    import random
    random.seed(42)
    for trial in range(400):
        n = random.randint(2, 10)
        d = WeightedDSU(n, MOD=1009)
        val = [random.randrange(1009) for _ in range(n)]
        for step in range(150):
            x, y = random.randrange(n), random.randrange(n)
            dd = random.randrange(1009)
            related = d.related(x, y)
            if not related:
                rx = d.find(x)[0]
                comp = [j for j in range(n) if d.find(j)[0] == rx]
            got = d.merge(x, y, dd)
            if related:
                assert got == ((val[x] - val[y]) % 1009 == dd)
            else:
                assert got == True
                delta = (dd - ((val[x] - val[y]) % 1009)) % 1009
                for j in comp:
                    val[j] = (val[j] + delta) % 1009
        for i in range(n):
            for j in range(n):
                if d.related(i, j):
                    assert d.diff(i, j) == (val[i] - val[j]) % 1009, (trial, i, j)
    print("dsu-weighted: all tests passed")

```

**PyPy 提示**: 递归 find 在深层链上可能 RecursionError，PyPy 递归深度默认 ~1000；链深≈集合大小，路径压缩后均摊极小。可在 find 内改写成 while+栈的迭代版，或直接用 sys.setrecursionlimit(1e6)。模 M 的运算尽量用整型取模；若 MOD=0 表示普通整数差（不取模），注意 Python 负号取模结果为负，需 (wx-wy) 直接比较即可。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 均摊 O(α(n)) 每次操作（路径压缩+按大小合并）；无启发式合并时 O(log n) |
| 空间 | O(n) |

### 局限

① 只能维护『可合并的势差』（群/半群运算），不支持按位拆分外的复杂运算；② 扩展域空间为状态数×n（食物链需 3n）；③ 合并方向需细心，反向挂边时权值符号易错，建议固定『小挂大』并现场推导权值；④ 冲突判定仅在同根时有效，非同根合并永远成功（即使直觉上‘矛盾’——因为尚未建立关系）。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P2024 | 3 | NOI2001 食物链：带权(模3) 或 扩展域(3n) 双解法，种类关系冲突判定 | [https://www.luogu.com.cn/problem/P2024](https://www.luogu.com.cn/problem/P2024) |
| Luogu | P1196 | 3 | NOI2002 银河英雄传说：维护到根的距离与列大小，带权并查集典型 | [https://www.luogu.com.cn/problem/P1196](https://www.luogu.com.cn/problem/P1196) |
| AtCoder | ABC396 E | 3 | Min of Restricted Sum：异或关系逐位拆成带权并查集，求最小和 | [https://atcoder.jp/contests/abc396/tasks/abc396_e](https://atcoder.jp/contests/abc396/tasks/abc396_e) |
| Library Checker | Unionfind with Potential | 3 | 带权并查集模板（Library Checker 平台），OI Wiki 参考实现来源 | [https://judge.yosupo.jp/problem/unionfind_with_potential](https://judge.yosupo.jp/problem/unionfind_with_potential) |

## Pitfalls · 易错点

- 路径压缩时忘记把父节点到根的权累加到自己身上
- 合并时新连边权计算符号反了（要现场从 diff 定义推导，别背公式）
- 模 M 下 diff 取负需 %M 归一化；Python 负数取模与数学意义一致但直接减可能为负
- 扩展域并查集要把每个元素拆成 n*k 个状态并正确映射合并对
- 只按秩/大小合并时，若忽略 weight 的更新会导致后续查询全错
- find 递归过深在极端数据下爆栈（用迭代或调大递归上限）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/dsu/](https://oi-wiki.org/ds/dsu/)
- OI Wiki ✓ [https://oi-wiki.org/ds/dsu/#带权并查集](https://oi-wiki.org/ds/dsu/#带权并查集)
- 书籍 ✓ `CPH ch15.2 Disjoint Set Union`
