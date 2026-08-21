---
id: binary-tree-dp-trick
name: 二叉化树 DP Trick
group: G-E-10
stage: frontier
priority: P3
depth_tier: brief
---

# 二叉化树 DP Trick

> 多叉树添加虚节点链转为二叉树，使 O(n²) 树形 DP 的合并复杂度成立

<!-- 元信息: id=binary-tree-dp-trick · group=G-E-10 · stage=frontier · priority=P3 · depth_tier=brief -->

## What · 是什么

二叉化树 DP Trick 指：当树形 DP 的复杂度依赖『每个节点合并所有儿子的子树背包』且儿子数很多时，通过插入虚节点（值为中性/不可选）把多叉树转化为二叉树，使得每个节点至多两个『孩子』，从而让 O(子树大小×子树大小) 的合并复杂度（树上背包的经典 O(n²) 总复杂度）在形式上严格成立、更易分析与实现。本质是把『逐个合并多子』改写成『链式二叉化合并』，把本来需要仔细论证的 ∑ size_x·size_y 上界变成显式的二叉树形态。2026 CF Round 1100（Spectral::Cup）Editorial Problem I 作为前沿例题使用了该 trick。

## Why · 为什么

### 直觉 · Intuition

多叉节点一次合并 k 个儿子会让复杂度变成所有儿子两两组合，难以论证；而二叉树每个节点只有两个儿子，树上背包的合并 O(size_l × size_r) 累加后恰好是 O(n²)（每个点对在其 LCA 处被计一次）。二叉化就是用『虚链』把多叉掰成二叉，把复杂论证翻译成简单形态。

### 原理 · Principle

设原多叉节点 u 有儿子 v1..vk。构造：以 u 为链头，依次把 v1 作为 u 的左儿子，然后新增虚节点 w1 作为 u 的右儿子，v2 作为 w1 的左儿子，再新增 w2 作为 w1 的右儿子……即『左儿子=真实儿子，右儿子=下一个虚节点』，末尾虚节点右儿子为空。虚节点的 DP 值设为对答案无影响的恒等值（如不选任何物品、代价为 0）。转化后每个节点度 ≤2，树大小 O(n)，树上背包合并总复杂度严格 O(n²)（对 CF Round 1100 一类题目，配合每个状态维度即可套用）。

### 历史 · History

二叉化（binarization）是树形 DP 的经典技巧，在『树上背包』的复杂度论证（如 OI Wiki dp/tree 章节，CTSC1997 选课 O(nm) 论证）中常隐含使用；显式『加虚节点成链』的写法在 2026 CF Round 1100 Spectral::Cup Editorial Problem I（blog entry 153948）中被作为关键 trick 提出，标志其在省选/CF 高频题目中的前沿复用。

## How · 实现

### 伪代码

```python
# 多叉树二叉化: u 的儿子 v1..vk 转为链
def binarize(u, children):
    cur = u
    for v in children:
        left[cur] = v
        if v is not last:
            nxt = new_node(虚值)
            right[cur] = nxt
            cur = nxt
    right[cur] = null
# 按二叉树跑树上背包合并, 复杂度 O(∑ size_l*size_r)=O(n²)
```

### Python 实现

```python
import sys


def binarize_tree(n, children):
    """多叉树 -> 二叉树（加虚节点）。
    children: list[list[int]] 每个节点的真实儿子（1-indexed 节点号）。
    返回: left[], right[] （0 表示空），虚节点从 n+1 开始编号。
    结构：真实儿子放左子，右侧用虚节点串成链，保持原父子关系。
    """
    left = [0] * (2 * n + 5)
    right = [0] * (2 * n + 5)
    new_id = n + 1
    for u in range(1, n + 1):
        if not children[u]:
            continue
        left[u] = children[u][0]
        cur = u
        for v in children[u][1:]:
            right[cur] = new_id
            left[new_id] = v
            cur = new_id
            new_id += 1
    return left, right


def verify_binary(n, children, left, right):
    """验证二叉化后每个真实节点的儿子集合与原多叉一致。"""
    for u in range(1, n + 1):
        got = []
        # 从 u 沿左子取真实儿子，沿右子链收集
        c = u
        seen = set()
        # u 的左子是真实儿子
        if left[u]:
            got.append(left[u])
        r = right[u]
        while r:
            if left[r]:
                got.append(left[r])
            r = right[r]
        assert sorted(got) == sorted(children[u]), (u, got, children[u])
    print("二叉化验证通过：所有真实节点的儿子集合一致")


if __name__ == "__main__":
    sys.setrecursionlimit(10 ** 6)
    # 例1: 三叉节点
    children = {1: [2, 3, 4], 2: [], 3: [5], 4: [], 5: []}
    left, right = binarize_tree(5, children)
    verify_binary(5, children, left, right)
    # 例2: 链式多叉
    children2 = {1: [2, 3, 4, 5], 2: [], 3: [], 4: [], 5: [6, 7], 6: [], 7: []}
    left2, right2 = binarize_tree(7, children2)
    verify_binary(7, children2, left2, right2)
    print("binary-tree-dp-trick 自测通过：二叉化结构正确")

```

**PyPy 提示**: 二叉化后递归层数与节点数同阶，需 setrecursionlimit；树上背包三层循环（节点×容量×子容量），PyPy 下 n≤500 可过，更大时考虑常数优化或 C++。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 二叉化本身 O(n)；转化后树上背包合并总复杂度 O(n²)（严格） |
| 空间 | O(n)（left/right 数组，虚节点 ≤ n-1 个） |

### 局限

虚节点需设定对 DP 无影响的恒等状态（通常『选 0 个/代价 0』），实现时要保证虚节点不会贡献非法答案；虚链使树长 O(n)，若 DP 状态与深度相关需留意。仅当 DP 确实是『背包合并』型（状态量=子树规模）时复杂度论证才成立。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P2014 | 4 | CTSC1997 选课：树上背包经典题（OI Wiki dp/tree 例题，二叉化思想隐含于复杂度论证） | [https://www.luogu.com.cn/problem/P2014](https://www.luogu.com.cn/problem/P2014) |

## Pitfalls · 易错点

- 虚节点的 DP 值必须设恒等中性值，否则污染答案
- 二叉化后实节点仍要通过右链找到所有真实儿子，遍历别漏
- 虚节点本身不参与状态计数，空间开 2n 足够
- 与『左儿子右兄弟』表示法区分：本 trick 是动态加虚节点而非复用原边

## Sources · 信源

- web △ [https://codeforces.com/blog/entry/153948](https://codeforces.com/blog/entry/153948)
- OI Wiki ✓ [https://oi-wiki.org/dp/tree/](https://oi-wiki.org/dp/tree/)
