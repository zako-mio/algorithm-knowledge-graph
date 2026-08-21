---
id: persistent-block-array
name: 可持久化分块数组
group: G-D-5
stage: advanced
priority: P2
depth_tier: standard
---

# 可持久化分块数组

> 分块数组的每个版本保留一份块副本，单点修改 O(sqrt n) 拷贝、查询 O(sqrt n)，空间 O(n + V·B)

<!-- 元信息: id=persistent-block-array · group=G-D-5 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

可持久化分块数组 = 可持久化思想 + 分块数组。分块数组把长度 n 的数组分成 B≈√n 大小的若干块，修改/查询定位到块后暴力扫描。要让其支持「回到任意历史版本」：每个版本维护一个块指针列表，单点修改时只需复制被改的那一个块（大小 O(B)=O(√n)）并新建版本，其余块共享。查询在指定版本内定位块 O(1)、块内 O(B)。相比可持久化线段树 O(log n)/版本，它空间常数更小、实现更简单；相比每版本全量拷贝 O(n)/版本，它把单版本开销降到 O(√n)。

## Why · 为什么

### 直觉 · Intuition

普通数组改一个数要复制整份才得到新版本，太贵。分块数组把数组切成 B 大小的段，一次修改只影响一个段，所以新版本只需「复制被改的那个段 + 换一个指针」，其余段全部复用旧版本的。版本之间像一棵棵共用的树，块是共享节点，只有被改的块是新拷贝。

### 原理 · Principle

设块大小 B≈√n，块数 nb≈n/B。version 数组存 list，每个元素指向该版本的「块列表」（每个块是一个长度 B 的 list）。set(ver, idx, val)：定位块 b=idx//B，浅拷贝块列表（O(nb) 指针），深拷贝目标块（O(B) 元素），替换后追加为新版本。get(ver, idx)：在 versions[ver] 定位块内 O(1)。任意两个版本的差 = 从分叉点起每版被改的块。离线时可用版本树；在线时直接存全版本序列。由于只浅拷贝块指针数组，深拷贝一个块，单版本写开销 O(B+nb)=O(√n)，空间 O(n·B 初始 + V·√n)。

### 历史 · History

分块/块状数组思想在竞赛中由来已久（根号分治），OI Wiki 的分块页介绍了基础分块数组；可持久化分块数组页面在 OI Wiki 为占位空页（ds/persistent-block-array.md 内容为空），概念源自「可持久化数据结构」通用范式（保留历史版本，path copying）。竞赛中此结构用于需要版本回溯 + 单点修改/区间查询的题目，频率低于可持久化线段树，但实现门槛低、内存表现好。

## How · 实现

### 伪代码

```python
B = ceil(sqrt(n))
versions = []
# version 0: 把 arr 分成若干块
versions.append([arr[i:i+B] for i in range(0, n, B)])

def get(ver, idx):
    return versions[ver][idx // B][idx % B]

def set(ver, idx, val) -> new_version:
    blocks = list(versions[ver])            # 浅拷贝块指针列表 O(nb)
    b = idx // B
    nb = list(blocks[b])                    # 拷贝目标块 O(B)
    nb[idx % B] = val
    blocks[b] = nb
    versions.append(blocks)                 # 新版本
    return len(versions) - 1
```

### Python 实现

```python
import math


class PersistentBlockArray:
    def __init__(self, arr, block_size=None):
        self.n = len(arr)
        self.B = block_size or max(1, int(math.sqrt(self.n)))
        self.versions = []
        self.versions.append([arr[i:i + self.B] for i in range(0, self.n, self.B)])

    def get(self, ver, idx):
        return self.versions[ver][idx // self.B][idx % self.B]

    def set(self, ver, idx, val):
        blocks = list(self.versions[ver])
        b = idx // self.B
        nb = list(blocks[b])
        nb[idx % self.B] = val
        blocks[b] = nb
        self.versions.append(blocks)
        return len(self.versions) - 1

    def version_count(self):
        return len(self.versions)


def main():
    pba = PersistentBlockArray(list(range(9)), block_size=3)
    # 版本0: [0,1,2,3,4,5,6,7,8]
    v0 = 0
    assert pba.get(v0, 4) == 4
    # 版本1: 改 idx4 -> 99
    v1 = pba.set(v0, 4, 99)
    # 版本2: 在版本1基础上改 idx1 -> 50
    v2 = pba.set(v1, 1, 50)
    assert pba.get(v1, 4) == 99
    assert pba.get(v1, 1) == 1        # 版本1的 idx1 未被版本2影响
    assert pba.get(v2, 1) == 50
    assert pba.get(v2, 4) == 99       # 版本2继承版本1的改动
    assert pba.get(v0, 4) == 4        # 版本0不变
    # 共享检查：未改的块是同一个对象（节约空间）
    assert pba.versions[v0][0] is pba.versions[v1][0]
    assert pba.versions[v1][2] is pba.versions[v2][2]
    # 改过的块是新对象
    assert pba.versions[v0][1] is not pba.versions[v1][1]
    print("versions:", pba.version_count())
    print("v0:", [pba.get(v0, i) for i in range(9)])
    print("v1:", [pba.get(v1, i) for i in range(9)])
    print("v2:", [pba.get(v2, i) for i in range(9)])
    print("persistent-block-array OK")


if __name__ == "__main__":
    main()

```

**PyPy 提示**: PyPy 下 list 浅拷贝与切片是 C 层 memcpy 级操作，块拷贝开销可忽略；每版本浅拷贝块指针列表 O(nb) 次指针是主要常数，nb≈√n 时很小。若要更省空间，块指针列表也可做成可持久化数组（每次只复制 log 个节点），但竞赛中通常不需要。注意 Python 大递归不需要（本实现非递归）。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | get O(1) 定位 + O(1) 索引；set O(B + nb) = O(√n)；区间查询最坏 O(√n) |
| 空间 | O(n) 初始块 + O(V·√n) 每版本新增（V 为版本数）；未改块共享 |

### 局限

块大小 B 需折中：B 太大单次拷贝贵，B 太小块数多、指针列表浅拷贝贵，取 √n。仅适合「单点修改/单点查、或区间查询」场景；若需区间加区间和，块内须配懒标记且可持久化要连带复制，复杂度上升。Python 中若题目给的是「可持久化数组」模板题（如洛谷 P3834 类静态区间第 k 小），更标准做法是可持久化线段树，本结构更适合块状查询的题。版本数 V 大时总空间 O(V√n) 可能超限，需评估。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3919 | 4 | 可持久化线段树模板题（单点改+版本回溯），可作可持久化思想入门，理解 path copying | [https://www.luogu.com.cn/problem/P3919](https://www.luogu.com.cn/problem/P3919) |

## Pitfalls · 易错点

- set 里若直接改 versions[ver][b] 会污染旧版本——必须 copy 出新的块再改
- 浅拷贝块列表后，改 versions[ver][b]=nb 是安全的；但若误写成 versions[ver][b][i]=val 则会破坏旧版本
- 下标计算 idx//B 与 idx%B 易混；块号从 0 计
- 版本号是追加式单调递增，回溯时不能回收旧版本（可持久化语义），内存只增不减
- 把块大小设成 n 退化成全量拷贝；设成 1 退化成可持久化指针数组，两者都要避免

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/persistent-block-array.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/persistent-block-array.md)
- OI Wiki ✓ [https://oi-wiki.org/ds/block-array/](https://oi-wiki.org/ds/block-array/)
- OI Wiki ✓ [https://oi-wiki.org/ds/persistent/](https://oi-wiki.org/ds/persistent/)
