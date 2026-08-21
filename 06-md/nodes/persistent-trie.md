---
id: persistent-trie
name: 可持久化 Trie
group: G-D-5
stage: advanced
priority: P1
depth_tier: standard
---

# 可持久化 Trie

> 保存历史版本的Trie，支持区间异或最值等查询

<!-- 元信息: id=persistent-trie · group=G-D-5 · stage=advanced · priority=P1 · depth_tier=standard -->

## What · 是什么

可持久化 Trie（Persistent Trie）是可持久化思想在 Trie 上的应用：每次插入一个数/串时，沿插入路径复制新节点、复用未改动的子树，保存每个版本的根，从而支持『任意历史版本』的查询。竞赛中最常见的是可持久化 01-Trie：维护每个前缀插入数的二进制位统计，支持『在区间 [l,r] 中选一个数 x 与给定值异或的最大值』——用两版根差分出区间内的计数，贪心走与 x 相反位（有则走）。经典例题：Luogu P4735 最大异或和（维护可持久化前缀异或和）。

## Why · 为什么

### 直觉 · Intuition

普通 01-Trie 能求『整个集合里与 x 异或最大』的数；加上区间限制 [l,r] 后，用可持久化：每个前缀 i 建一棵插入了前 i 个数的 01-Trie 版本。查询时第 r 版与第 l-1 版的计数差分，就像主席树的『值域计数相减』，得到 [l,r] 内的位统计，再贪心逐位取相反位。因为位数固定（如 30 位），每次插入只动 O(B) 个节点。

### 原理 · Principle

① 01-Trie 节点存 ch[2]（0/1 儿子）与 cnt（子树中数的个数）；② 可持久化插入：新根先拷贝旧根，沿二进制位逐位：该位旧儿子做新儿子并 cnt+1，未走的位直接复用旧指针；③ 每插入一个数保存新根 root[i]；④ 查询 max xor in [l,r]：同时走 u=root[l-1] 与 v=root[r]，对位 b，优先走与 x 相反的位（看 cnt[ch[v][want]]-cnt[ch[u][want]]>0），否则走同向位，累加贡献 2^b；⑤ 复杂度：插入/查询 O(B)（B 为位数，通常 30），空间 O(nB)。前缀异或和技巧：求 a_p..a_n 异或和 = s[p-1]^s[n]，配合可持久化 Trie 可转化为区间异或最值（P4735 正是如此）。

### 历史 · History

可持久化 Trie 与可持久化线段树同源于函数式数据结构与 path copying 思想（1980s 可持久化数据结构研究）。在 OI 中因 P4735『最大异或和』等题普及。与主席树（可持久化权值线段树）是『区间查询 + 版本差分』思想的一体两面，常被放在同一章节学习。

## How · 实现

### 伪代码

```python
ch[cur][2], cnt[cur]; roots=[0]
insert(prev_root, x):
  new_root = 拷贝 prev_root 的根并 cnt+1
  node = prev_root; cur = new_root
  for b in 30..0:
    bit = (x>>b)&1
    old_child = ch[node][bit]
    新建节点拷贝 old_child 的 ch 与 cnt，cnt+1
    ch[cur][bit] = 新节点
    node = old_child; cur = 新节点
  roots.append(new_root)
query(l, r, x):   # [l,r] 内与 x 异或最大
  u = roots[l-1]; v = roots[r]; ans = 0
  for b in 30..0:
    bit = (x>>b)&1; want = bit^1
    if cnt[ch[v][want]] - cnt[ch[u][want]] > 0:
      ans |= 1<<b; u = ch[u][want]; v = ch[v][want]
    else:
      u = ch[u][bit]; v = ch[v][bit]
  return ans
```

### Python 实现

```python
class PersistentTrie:
    """可持久化 01-Trie：支持前缀版本与区间异或最大值查询。
    用法: pt = PersistentTrie(B); 对每个 x 调 pt.add(x);
    pt.max_xor_in(l, r, x) 返回 max_{i in [l,r]}(arr[i] ^ x)。"""

    def __init__(self, B=30):
        self.B = B
        self.ch = [[0, 0]]
        self.cnt = [0]
        self.roots = [0]

    def add(self, x):
        old = self.roots[-1]
        new_root = len(self.ch)
        self.ch.append([self.ch[old][0], self.ch[old][1]])
        self.cnt.append(self.cnt[old] + 1)
        cur, node = new_root, old
        for b in range(self.B, -1, -1):
            bit = (x >> b) & 1
            old_child = self.ch[node][bit]
            nxt = len(self.ch)
            self.ch.append([self.ch[old_child][0], self.ch[old_child][1]])
            self.cnt.append(self.cnt[old_child] + 1)
            self.ch[cur][bit] = nxt
            cur, node = nxt, old_child
        self.roots.append(new_root)
        return new_root

    def max_xor_in(self, l, r, x):
        """区间 [l,r]（1 索引含端点，按插入顺序）内与 x 异或的最大值"""
        u, v = self.roots[l - 1], self.roots[r]
        ans = 0
        for b in range(self.B, -1, -1):
            bit = (x >> b) & 1
            want = bit ^ 1
            c = self.cnt[self.ch[v][want]] - self.cnt[self.ch[u][want]]
            if c > 0:
                ans |= 1 << b
                u = self.ch[u][want]
                v = self.ch[v][want]
            else:
                u = self.ch[u][bit]
                v = self.ch[v][bit]
        return ans


if __name__ == '__main__':
    import random

    def brute(arr, l, r, x):
        return max(x ^ v for v in arr[l - 1:r])

    arr = [1, 2, 3, 4, 5]
    pt = PersistentTrie(4)
    for x in arr:
        pt.add(x)
    assert pt.max_xor_in(1, 5, 0) == 5 ^ 0  # 5
    assert pt.max_xor_in(2, 4, 3) == brute(arr, 2, 4, 3)

    random.seed(22)
    for _ in range(300):
        B = 4
        pt = PersistentTrie(B)
        n = random.randint(1, 12)
        arr = [random.randint(0, 31) for _ in range(n)]
        for x in arr:
            pt.add(x)
        for _ in range(20):
            l = random.randint(1, n)
            r = random.randint(l, n)
            x = random.randint(0, 31)
            assert pt.max_xor_in(l, r, x) == brute(arr, l, r, x), (l, r, x, arr)
    print('persistent-trie: All tests passed.')
```

**PyPy 提示**: ch 用两列 list 存储（ch0/ch1 分开）或 [[0,0]] 列表均可，PyPy 下后者可接受。B 取 30（值域 2^31）或题目要求位数。构建/查询都是纯循环无递归，性能好；n=1e5 时节点约 n*(B+2) 个，内存注意预分配或动态 list。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 插入/查询均 O(B)（B=位数，通常 30）；构建 n 个数 O(nB) |
| 空间 | O(nB) 节点（每个插入新建 B+1 个节点）+ O(n) 根数组 |

### 局限

主要用于『区间异或最值 / 区间与某数异或极值』类问题，若查询是普通字符串/字典序类则适用性不同。位数 B 固定时有效；若值域巨大（如 64 位）空间翻倍。只能静态前缀版本（在线前缀）；若要支持区间任意可持久化需平衡树/其他结构。与主席树一样大常数，n 巨大时注意内存。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P4735 | 5 | 最大异或和：可持久化 01-Trie 维护前缀异或和，区间异或最值，OI Wiki 例题 | [https://www.luogu.com.cn/problem/P4735](https://www.luogu.com.cn/problem/P4735) |
| Luogu | P5283 | 6 | 【十二省联考2019】异或粽子：可持久化 Trie + 堆取前 k 大异或和，综合难题 | [https://www.luogu.com.cn/problem/P5283](https://www.luogu.com.cn/problem/P5283) |
| SPOJ | XORX | 4 | 区间异或极值经典题，可持久化 Trie 模板练习 | [https://www.spoj.com/problems/XORX/](https://www.spoj.com/problems/XORX/) |

## Pitfalls · 易错点

- 插入时新节点必须完整拷贝旧儿子路径（ch 与 cnt），漏拷贝 cnt 会让计数错误
- 查询差分 u=roots[l-1]、v=roots[r] 写错索引导致区间错
- 贪心选择相反位时若 cnt 差为 0 必须退回同向位，不能跳过该位
- 前缀异或和的区间转换（P4735 中 [l,r] 下标要对应到 s[l-1..r-1]）容易差一
- B 位选择不足（如值域 2^31 却用 B=30 少一位）导致高位丢失
- ch 数组初始化 [0,0] 指向节点 0（空节点），cnt[0]=0 必须保证 0 号节点计数为 0

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/persistent-trie/](https://oi-wiki.org/ds/persistent-trie/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/persistent-trie.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/persistent-trie.md)
