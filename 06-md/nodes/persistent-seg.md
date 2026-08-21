---
id: persistent-seg
name: 可持久化线段树(主席树)
group: G-D-5
stage: advanced
priority: P0
depth_tier: deep
---

# 可持久化线段树(主席树)

> 函数式线段树按版本共享节点，支持历史版本查询与区间k小值

<!-- 元信息: id=persistent-seg · group=G-D-5 · stage=advanced · priority=P0 · depth_tier=deep -->

## What · 是什么

可持久化线段树（Persistent Segment Tree，中文俗称『主席树』）是保存每次修改后历史版本的线段树。核心思想是 path copying：每次点修改只新建 O(log n) 个『被改路径』上的新节点，未变子树直接复用旧节点指针，因此 m 次修改的总节点数 O(m log n)。权值线段树版（每个叶子代表一个值域桶，维护区间内该值出现的次数）配合前缀和差分，可在 O(log n) 回答区间第 k 小/第 k 大、区间 ≤x 的个数、静态/动态区间众数类查询。经典应用：POJ 2104 K-th Number（区间第 k 小）、Luogu P3834/P2633 等。是竞赛中最常考的可持久化结构。

## Why · 为什么

### 直觉 · Intuition

『保存历史版本』最笨的办法是每改一次就复制整棵树——空间爆掉。但线段树每次修改只碰一条从根到叶的路径（O(log n) 个节点），其余节点完全不动。于是每次只复制这条路径：新根 + 沿途新节点，指向未修改的旧子树。这样每版只花 O(log n) 空间，历史版本们像一棵『时间树』共享大量节点。区间第 k 小则靠值域计数 + 前缀差分：第 r 版减第 l-1 版得到 [l,r] 的值域计数。

### 原理 · Principle

① 动态开点：节点存 ls/rs（左右儿子编号）与 cnt（该值域内出现次数），不用堆式存储；② 建空树（或直接只建根）O(n) 或懒惰；③ update(pos, root)：新建当前节点并拷贝 prev 的 ls/rs/cnt，cnt+1，递归到 pos 所在子区间建新链，O(log n)；④ 每个前缀 i 保存一个根 rt[i]（插入 a[i] 后）；⑤ query(l, r, k)：同时下钻 rt[r] 与 rt[l-1]，比较左子节点 cnt 之差，若 k ≤ 左差则去左否则去右并 k 减去左差，O(log n)；⑥ 空间：n 次修改至多 (n log n + n) 节点，开 2^5×n 保险。支持区间 ≤x 计数、历史版本查询、可持久化并查集等扩展。

### 历史 · History

可持久化线段树因 2012 年国家集训队黄嘉泰（网名 HJT 谐音『主席』）的讲义而流行于 OI，故俗称主席树。其思想（函数式线段树、path copying）源于 1980 年代的函数式编程与可持久化数据结构研究（Driscoll 等）。区间第 k 小问题是静态数据结构领域的经典问题，主席树是目前 OI 中最常用的在线解法（还有整体二分/树套树/莫队离线替代）。

## How · 实现

### 伪代码

```python
ls[], rs[], cnt[], tot=0; rt[0]=build();
update(prev, l, r, pos):
  cur = ++tot; ls[cur]=ls[prev]; rs[cur]=rs[prev]; cnt[cur]=cnt[prev]+1
  if l<r:
    mid=(l+r)//2
    if pos<=mid: ls[cur]=update(ls[prev], l, mid, pos)
    else:        rs[cur]=update(rs[prev], mid+1, r, pos)
  return cur
query(u, v, l, r, k):   # 用 [1,l-1] 与 [1,r] 两根差分
  if l==r: return l
  left = cnt[ls[v]] - cnt[ls[u]]
  if k<=left: return query(ls[u], ls[v], l, mid, k)
  else:       return query(rs[u], rs[v], mid+1, r, k-left)
```

### Python 实现

```python
from bisect import bisect_left


class PersistentSegTree:
    """可持久化权值线段树（主席树）。构造 O(n log n)，查询第 k 小 O(log n)。
    arr: 原序列。支持 kth(l, r, k) 返回区间 [l,r]（1 索引含端点）第 k 小值。"""

    def __init__(self, arr):
        self.vals = sorted(set(arr))
        self.ls = [0]
        self.rs = [0]
        self.cnt = [0]
        self.roots = [self._build(0, len(self.vals) - 1)]
        for x in arr:
            self.roots.append(
                self._update(self.roots[-1], 0, len(self.vals) - 1,
                             bisect_left(self.vals, x)))

    def _build(self, l, r):
        idx = len(self.ls)
        self.ls.append(0); self.rs.append(0); self.cnt.append(0)
        if l < r:
            mid = (l + r) // 2
            self.ls[idx] = self._build(l, mid)
            self.rs[idx] = self._build(mid + 1, r)
        return idx

    def _update(self, prev, l, r, pos):
        idx = len(self.ls)
        self.ls.append(self.ls[prev])
        self.rs.append(self.rs[prev])
        self.cnt.append(self.cnt[prev] + 1)
        if l < r:
            mid = (l + r) // 2
            if pos <= mid:
                self.ls[idx] = self._update(self.ls[prev], l, mid, pos)
            else:
                self.rs[idx] = self._update(self.rs[prev], mid + 1, r, pos)
        return idx

    def kth(self, l, r, k):
        """区间 [l,r]（1 索引含端点）第 k 小值"""
        return self.vals[self._kth(self.roots[l - 1], self.roots[r],
                                  0, len(self.vals) - 1, k)]

    def _kth(self, u, v, l, r, k):
        if l == r:
            return l
        mid = (l + r) // 2
        left = self.cnt[self.ls[v]] - self.cnt[self.ls[u]]
        if k <= left:
            return self._kth(self.ls[u], self.ls[v], l, mid, k)
        return self._kth(self.rs[u], self.rs[v], mid + 1, r, k - left)


if __name__ == '__main__':
    import random

    def brute(a, l, r, k):
        return sorted(a[l - 1:r])[k - 1]

    a = [1, 5, 2, 6, 3, 7, 4]
    pst = PersistentSegTree(a)
    assert pst.kth(2, 5, 2) == 3      # [5,2,6,3] 排序 [2,3,5,6] 第2小=3
    assert pst.kth(1, 7, 4) == 4
    assert pst.kth(3, 7, 5) == 7

    random.seed(21)
    for _ in range(200):
        n = random.randint(1, 12)
        arr = [random.randint(-20, 20) for _ in range(n)]
        pt = PersistentSegTree(arr)
        for _ in range(20):
            l = random.randint(1, n)
            r = random.randint(l, n)
            k = random.randint(1, r - l + 1)
            assert pt.kth(l, r, k) == brute(arr, l, r, k), (l, r, k, arr)
    print('persistent-seg: All tests passed.')
```

**PyPy 提示**: 竞赛模板多用数组模拟（ls/rs/cnt 三个 list + 全局 tot），比对象快 2-3 倍。节点上限开 (n<<5)+5 或 n*20。离散化用 bisect。递归查询深度 O(log n) 安全；若 n=1e6 或需频繁构建注意常数。注意 Python 递归每层两次 list 索引，PyPy 下 1e5 规模（约 2e6 节点）可行。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 构建 O(n log n)；单次更新/查询 O(log n) |
| 空间 | O(n log n) 节点（约 20n）；另有 O(n) 根数组与 O(n) 离散化数组 |

### 局限

只支持『点修改 + 区间统计』类的可持久化：区间加等区间修改需打标记（标记也要可持久化，较复杂）。静态区间第 k 小的在线替代还有划分树/整体二分；动态修改需树套树（主席树套 BIT）。大常数 + O(n log n) 空间在 n≥1e6 时要小心。若查询只针对前缀（[1,r]）可退化为普通权值线段树。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3834 | 4 | 【模板】可持久化线段树 2（主席树）：静态区间第 k 小，最标准模板题 | [https://www.luogu.com.cn/problem/P3834](https://www.luogu.com.cn/problem/P3834) |
| Luogu | P2633 | 5 | Count on a tree：树上路径第 k 小，按 DFS 序建主席树 + 树上差分（u+v-lca-fa[lca]） | [https://www.luogu.com.cn/problem/P2633](https://www.luogu.com.cn/problem/P2633) |
| Luogu | P3919 | 3 | 【模板】可持久化线段树 1（可持久化数组）：历史版本查询与修改，入门题 | [https://www.luogu.com.cn/problem/P3919](https://www.luogu.com.cn/problem/P3919) |
| POJ | 2104 | 4 | K-th Number：区间第 k 小的经典鼻祖题，主席树标准解法 | [https://vjudge.net/problem/POJ-2104](https://vjudge.net/problem/POJ-2104) |
| Luogu | P3567 | 5 | 【POI2014】KUR-Couriers：区间众数/过半元素，主席树二分值域查找出现次数>一半的值 | [https://www.luogu.com.cn/problem/P3567](https://www.luogu.com.cn/problem/P3567) |

## Pitfalls · 易错点

- 动态开点：不能像普通线段树用 x*2/x*2+1 堆式存储，必须显式存 ls/rs
- update 必须先拷贝 prev 的全部字段（ls/rs/cnt）再改一个分支，漏拷贝导致历史被破坏
- 离散化后查询返回的是值域下标，输出前要映射回原值
- 空间：节点上限不足（< n*log n）会 RE/内存溢出，OI 惯例开 n<<5
- 区间 [l,r] 用 rt[r] 与 rt[l-1] 两根差分，用成 rt[l] 会答案错误
- 第 k 大 = 第 (len-k+1) 小，转换易混；k 必须 ≤ r-l+1 否则越界

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/persistent-seg/](https://oi-wiki.org/ds/persistent-seg/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/persistent-seg.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/persistent-seg.md)
- 书籍 ✓ `CPH ch28 pp271-273`
