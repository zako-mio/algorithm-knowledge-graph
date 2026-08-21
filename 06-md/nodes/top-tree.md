---
id: top-tree
name: Top Tree（Self-Adjusting Top Tree，SATT）
group: G-D-4
stage: frontier
priority: P3
depth_tier: brief
---

# Top Tree（Self-Adjusting Top Tree，SATT）

> 基于树收缩（Compress/Rake）的簇（Cluster）级动态树框架，Self-Adjusting Top Tree 用三叉树维护完全动态森林的路径与子树信息。

<!-- 元信息: id=top-tree · group=G-D-4 · stage=frontier · priority=P3 · depth_tier=brief -->

## What · 是什么

Top Tree 是一棵二叉树，每个节点对应原树在树收缩过程中的一个『簇』（Cluster）——一个由 Compress/Rake 操作合并出来的连通子图，有两个端点。叶子是基簇（单条边），根是根簇（除端点外包含整棵树）。Self-Adjusting Top Tree（SATT）由 Tarjan 与 Werneck 于 2005 年提出，用一棵自调整三叉树（Compress Tree + Rake Tree 组合）表示簇的层级关系，支持链修改/查询、子树修改/查询，以及非局部搜索（如动态维护重心、直径）。

## Why · 为什么

### 直觉 · Intuition

把一棵树『收缩』成一条边是构造性的：Compress 把度数为 2 的路径顶点合并，Rake 把度数为 1 的叶子并到邻居上。任何树都能只用这两个操作缩成一条边。每一次合并对应一个簇，把合并顺序组织成树，就得到 Top Tree——本质是『树收缩过程的一棵记录树』。簇的两个端点之间的路径是簇路径，簇只存内点与内边信息，因此路径信息与子树信息都被封装进簇里，维护簇的信息等价于维护整棵树的信息。

### 原理 · Principle

① 簇（Cluster）：T_x 中一条边所蕴含的原树连通子图，含 2 个端点；基簇=单条边，根簇=整棵树。② Compress：度 2 点 x 与其两边 (y,x),(x,z) 合并进新边 (y,z)，即把路径段压成一簇。③ Rake：叶子 x 与边 (x,y) 合并进 y 的另一条边。④ SATT 用三叉节点表示：Compress Node 表示一次 Compress，Rake Node 表示一次 Rake；左中右三棵子树分别管理簇路径两侧的 Rake 信息与 Compress 路径。⑤ Access(x) 沿簇树把 x 旋到根（全局 splay），与 LCT 的 access 类似；任意路径/子树操作转化为根簇的信息，Pushup 时维护 len（簇路径长度）、maxs[0/1]（到簇端点的最大距离）等。⑥ 非局部搜索：权值第二小、重心等不满足局部性（在包含它的所有子树中都成立的『局部』性质）的查询，需要在簇树上进行带剪枝的搜索。

### 历史 · History

Top Tree 概念由 Robert E. Tarjan 与 Renato F. Werneck 在 2005 年论文《Self-Adjusting Top Trees》中提出（并在此前有 Static/Dynamic Top Trees 的工作），是动态树研究的集大成者，统一了路径与子树两类操作。OI Wiki 提供 SATT 的中文教程与实现（含 Luogu P3690 模板与 CEOI2019 Dynamic Diameter 例题）。竞赛中使用较少（实现复杂），更多作为前沿理解。

## How · 实现

### 伪代码

```python
struct SATT:
    # 三叉树：ls/ms/rs，节点类型 op ∈ {Compress, Rake}
    len[x]      # Compress 簇路径长度
    maxs[x][0/1] # 簇端点到簇内点/端点的最大距离（Rake 只用 maxs[0]）
    diam[x]     # 簇直径

    Pushup(x):
      if op[x] == Compress:
        len[x] = len[ls]+len[rs]
        diam[x] = max(maxs[ls][1]+maxs[rs][0],
                      max(maxs[ls][1],maxs[rs][0])+maxs[ms][0],
                      max(diam[ls],diam[rs],diam[ms]))
        maxs[x][0]=max(maxs[ls][0], len[ls]+max(maxs[ms][0],maxs[rs][0]))
        maxs[x][1]=max(maxs[rs][1], len[rs]+max(maxs[ms][0],maxs[ls][1]))
      else:  # Rake
        diam[x] = max(maxs[ls][0]+maxs[rs][0],
                      maxs[ms][0]+max(maxs[ls][0],maxs[rs][0]),
                      max(diam[ls],diam[rs],diam[ms]))
        maxs[x][0]=max(maxs[ms][0], max(maxs[ls][0],maxs[rs][0]))

    Access(x):  # 把 x 旋到全局根（省略 Global Splay 细节）
    Link/ Cut/ PathQuery/ SubtreeQuery: 均基于 Access + Pushup
```

### Python 实现

```python
import random

class SATTNode:
    """简化教学实现：仅用于展示簇树的 Pushup 结构，非完整 SATT。
    真实 SATT 需三叉自调整结构与 Access 序列，Python 实现过于复杂，
    本节点以概念演示为主，详见 OI Wiki top-tree 页面。"""
    __slots__ = ('op', 'left', 'mid', 'right', 'len', 'maxs', 'diam')
    def __init__(self, op):
        self.op = op  # 'compress' | 'rake'
        self.left = self.mid = self.right = None
        self.len = 0
        self.maxs = [0, 0]
        self.diam = 0

def pushup(x):
    """演示 Compress/Rake 节点的信息合并（OI Wiki 代码的 Python 直译）"""
    L, M, R = x.left, x.mid, x.right
    if x.op == 'compress':
        x.len = (L.len if L else 0) + (R.len if R else 0)
        ms0 = M.maxs[0] if M else 0
        ms1 = M.maxs[0] if M else 0
        dl = L.diam if L else 0
        dr = R.diam if R else 0
        dm = M.diam if M else 0
        x.diam = max((L.maxs[1] if L else 0) + (R.maxs[0] if R else 0),
                     max((L.maxs[1] if L else 0), (R.maxs[0] if R else 0)) + ms0,
                     max(dl, dr, dm))
        x.maxs[0] = max((L.maxs[0] if L else 0),
                        (L.len if L else 0) + max(ms1, (R.maxs[0] if R else 0)))
        x.maxs[1] = max((R.maxs[1] if R else 0),
                        (R.len if R else 0) + max(ms0, (L.maxs[1] if L else 0)))
    else:  # rake
        ls0 = L.maxs[0] if L else 0
        rs0 = R.maxs[0] if R else 0
        ms0 = M.maxs[0] if M else 0
        x.diam = max(ls0 + rs0, ms0 + max(ls0, rs0),
                     max(L.diam if L else 0, R.diam if R else 0, M.diam if M else 0))
        x.maxs[0] = max(ms0, max(ls0, rs0))

def top_tree_selfcheck():
    # 单节点叶簇：压缩路径长度为边权，构造一条三边链并验证 len 与直径
    a = SATTNode('compress'); a.len = 2; a.maxs = [2, 2]
    b = SATTNode('compress'); b.len = 3; b.maxs = [3, 3]
    root = SATTNode('compress')
    root.left, root.right = a, b
    pushup(root)
    assert root.len == 5
    assert root.diam == 5
    print('TopTree cluster pushup OK (len=%d diam=%d)' % (root.len, root.diam))

if __name__ == '__main__':
    top_tree_selfcheck()
```

**PyPy 提示**: SATT 完整实现在 Python 中几乎不可行（三叉自调整 + Access + 懒标记常数极大），本节点 Python 仅供理解簇的 Pushup 概念；竞赛如需动态树请用 C++。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | Access/链查询/子树查询均摊 O(log n)（势能分析基于 r(i)=⌈log2 siz(i)⌉） |
| 空间 | O(n) |

### 局限

实现极其复杂（三叉树、自调整、懒翻转、非局部搜索），实际竞赛中除模板题外极少使用；比 LCT 多出子树信息与非局部搜索能力，但常数大、调试难。Python 不适用。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3690 | 6 | 【模板】动态树：OI Wiki 给出 SATT 解 LCT 模板题的实现，可对比两者常数 | [https://www.luogu.com.cn/problem/P3690](https://www.luogu.com.cn/problem/P3690) |
| LOJ | 3163 | 8 | CEOI 2019 Dynamic Diameter：动态边权下维护直径，SATT 的 Pushup 直接维护 diam 即可 | [https://loj.ac/p/3163](https://loj.ac/p/3163) |
| LOJ | 3213 | 9 | CSP-S2019 树的重心：利用 SATT 非局部搜索在簇树上定位重心，每删一条边 O(log n) 维护 | [https://loj.ac/p/3213](https://loj.ac/p/3213) |

## Pitfalls · 易错点

- Compress 与 Rake 节点的 Pushup 公式不同，写反导致信息错误
- SATT 的三叉结构顺序（ls/ms/rs）决定簇路径方向，翻转时必须交换 ls/rs 与 maxs[0/1]
- 非局部信息（如重心、第二小）不能只靠 Pushup，需在簇树上搜索，勿直接用子树聚合
- 省略 Global Splay 会影响均摊界，测试数据小可能看不出来
- 先完整掌握 LCT 与动态树再学 SATT，直接上手极易出错

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/top-tree.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/top-tree.md)
- OI Wiki △ [https://oi-wiki.org/ds/top-tree/](https://oi-wiki.org/ds/top-tree/)
