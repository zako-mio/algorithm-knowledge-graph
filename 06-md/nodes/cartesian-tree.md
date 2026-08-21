---
id: cartesian-tree
name: 笛卡尔树（Cartesian Tree）
group: G-A-9
stage: intermediate
priority: P1
depth_tier: deep
---

# 笛卡尔树（Cartesian Tree）

> 键满足 BST 性质、值满足堆性质的二叉树，用单调栈 O(n) 构建；把 RMQ 转成树上 LCA，可 O(n)~O(1) 求区间最值，也是 Treap 的理论基础。

<!-- 元信息: id=cartesian-tree · group=G-A-9 · stage=intermediate · priority=P1 · depth_tier=deep -->

## What · 是什么

笛卡尔树是每个节点由二元组 (k, w) 构成的二叉树：k 满足二叉搜索树（BST）性质，w 满足堆性质。若所有 k 与 w 都互不相同，则结构唯一。竞赛中典型取法：数组下标为 k（BST 键），数组值为 w（小根堆权）——此时每棵子树对应原数组的一个连续区间，且子树根是该区间的值最小的元素。构建可用单调栈 O(n) 完成。重要推论：区间 [l,r] 的最小值 = 下标 l 与 r 在笛卡尔树上的 LCA 的值，于是 RMQ 可转成 O(1) 的树上 LCA 查询。Treap 本质是 k 有序、w 随机的笛卡尔树。

## Why · 为什么

### 直觉 · Intuition

把『区间最值』这种二维信息（下标+值）折叠成树：BST 维度保留下标顺序，堆维度保留值的大小关系，两者合起来恰好让『下标连续区间的最小值』对应『树上一段子树的根』。笛卡尔树的每个节点代表『以它为最小值的最大连续区间』，这正是单调栈能在线性时间内构建它的原因——单调栈本来就在维护『以当前值为最小/最大的区间』。

### 原理 · Principle

① 唯一性：k 与 w 均互异时，对 k 排序后以 w 最小者为根，左子树由左侧元素递归构成、右子树由右侧元素递归构成，结构唯一。② 单调栈构建：按 k 升序（即数组从左到右）依次插入。新插入节点必然位于右链（从根一路向右）最右端。从栈顶向下比较 w，弹出所有 w>当前 w 的节点，弹完的栈顶 x（满足 w_x < w_u）接为 u 的左子树根，并把 u 挂到 x 的右儿子。每个节点进出栈一次，O(n)。③ RMQ 转化：因为 w 满足小根堆，下标 l、r 的 LCA 是包含 l 与 r 的子树中最小 w 的节点，其 w 恰为区间 [l,r] 的最小值。④ Treap 关联：Treap 即 k 有序、w 随机的笛卡尔树。

### 历史 · History

笛卡尔树由 Jean Vuillemin 于 1980 年在论文《A Unifying Look at Data Structures》中提出并命名（致敬笛卡尔坐标系，因它在下标×值平面上直观）。它统一了多个数据结构：Treap、单调栈与 RMQ 的 LCA 方法（Bender & Farach-Colton 的 O(n)~O(1) RMQ 经由笛卡尔树转 LCA）。HDU 1506（Largest Rectangle in a Histogram）是经典例题。

## How · 实现

### 伪代码

```python
# 单调栈 O(n) 构建（下标 1..n，值 w[]，小根堆）
stk = []
for i in 1..n:
    k = len(stk)
    while k > 0 and w[stk[k-1]] > w[i]: k -= 1
    if k > 0: rs[stk[k-1]] = i        # 右链上找到更小的祖先，i 为右儿子
    if k < len(stk): ls[i] = stk[k]   # i 的左儿子 = 被弹掉的栈顶
    stk = stk[:k] + [i]
root = stk[0]
```

### Python 实现

```python
def build_cartesian(w):
    """按值构建小根堆笛卡尔树（下标即 BST 键）。
    返回 (left[], right[])；下标 0..n-1。"""
    n = len(w)
    left = [-1] * n
    right = [-1] * n
    stk = []
    for i in range(n):
        last = -1
        while stk and w[stk[-1]] > w[i]:
            last = stk.pop()
        if stk:
            right[stk[-1]] = i
        if last != -1:
            left[i] = last
        stk.append(i)
    return left, right, stk[0]

def build_lca_binary_lifting(left, right, root):
    """简单倍增 LCA（仅供自测；竞赛 O(1) 可用欧拉序+ST 表）"""
    n = len(left)
    parent = [-1] * n
    for i in range(n):
        if left[i] != -1:
            parent[left[i]] = i
        if right[i] != -1:
            parent[right[i]] = i
    LOG = max(1, n.bit_length())
    up = [[-1] * n for _ in range(LOG)]
    up[0] = parent[:]
    for k in range(1, LOG):
        for v in range(n):
            mid = up[k - 1][v]
            up[k][v] = up[k - 1][mid] if mid != -1 else -1
    depth = [-1] * n
    stack = [(root, 0)]
    while stack:
        v, d = stack.pop()
        depth[v] = d
        for c in (left[v], right[v]):
            if c != -1:
                stack.append((c, d + 1))
    def lca(a, b):
        if depth[a] < depth[b]:
            a, b = b, a
        diff = depth[a] - depth[b]
        bit = 0
        while diff:
            if diff & 1:
                a = up[bit][a]
            diff >>= 1
            bit += 1
        if a == b:
            return a
        for k in range(LOG - 1, -1, -1):
            if up[k][a] != up[k][b]:
                a = up[k][a]; b = up[k][b]
        return parent[a]
    return lca

def cartesian_rmq_check():
    import random
    for _ in range(50):
        n = random.randint(1, 30)
        a = [random.randint(1, 100) for _ in range(n)]
        left, right, root = build_cartesian(a)
        # 验证 BST 结构：中序遍历 = 原下标顺序
        order = []
        def dfs(u):
            if u == -1:
                return
            dfs(left[u]); order.append(u); dfs(right[u])
        dfs(root)
        assert order == list(range(n))
        # 验证堆性质
        ok = True
        for i in range(n):
            for c in (left[i], right[i]):
                if c != -1 and a[c] < a[i]:
                    ok = False
        assert ok
        # 验证 RMQ 等价性（随机区间）
        lca = build_lca_binary_lifting(left, right, root)
        for _ in range(20):
            l = random.randint(0, n - 1)
            r = random.randint(l, n - 1)
            mn = min(a[l:r + 1])
            got = a[lca(l, r)]
            assert got == mn, (a, l, r, got, mn)
    print('cartesian tree RMQ equivalence OK (50 random cases)')

if __name__ == '__main__':
    left, right, root = build_cartesian([3, 2, 1, 6, 0, 5])
    print('root =', root)
    assert root == 4  # 值 0 最小
    cartesian_rmq_check()
```

**PyPy 提示**: 单调栈构建用 list 模拟栈 O(n)；倍增 LCA 的 up 表用 list of list，n≤1e6 时内存 O(n log n) 偏大，竞赛中如需 O(1) RMQ 可改用欧拉序 + ST 表或 Tarjan 离线。PyPy 下 build_cartesian 循环性能良好。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 构建 O(n)；LCA 倍增 O(log n)/查询，欧拉序+ST 表可 O(1) 查询；子树区间最值一次 DFS O(n) |
| 空间 | O(n)（树）；倍增 LCA O(n log n) |

### 局限

要求 k 与 w 均互异，否则结构不唯一需额外规则；大根堆/小根堆方向须与题目一致；构建完成后直接做 RMQ 需额外 LCA 结构，常数大于 ST 表；对随机数据直接 DFS 找最小值期望 O(log n) 但最坏 O(n)。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P5854 | 3 | 【模板】笛卡尔树：单调栈 O(n) 构建模板题 | [https://www.luogu.com.cn/problem/P5854](https://www.luogu.com.cn/problem/P5854) |
| Luogu | P1377 | 4 | BZOJ/谷 TJOI：二叉搜索树插入序还原，可用笛卡尔树理解插入结构与 BST | [https://www.luogu.com.cn/problem/P1377](https://www.luogu.com.cn/problem/P1377) |
| HDU | 1506 Largest Rectangle in a Histogram | 3 | 笛卡尔树经典题：枚举子树根（区间最小高度）×子树宽度求最大矩形 | [https://acm.hdu.edu.cn/showproblem.php?pid=1506](https://acm.hdu.edu.cn/showproblem.php?pid=1506) |
| Luogu | P3865 | 4 | ST 表模板题，可对比笛卡尔树+LCA 的 O(n)~O(1) 做法 | [https://www.luogu.com.cn/problem/P3865](https://www.luogu.com.cn/problem/P3865) |

## Pitfalls · 易错点

- 构建时弹栈条件方向（小根堆用 >，大根堆用 <）写反会得到错误结构
- 新节点接右儿子前必须确保栈内仍有元素，k==0 时不可接
- 弹出的栈顶是左儿子、未弹出的栈顶是父节点——两者都不可少，漏一步树就断
- RMQ 转化取的是 LCA 的『值』不是下标（虽然本实现下标即值索引）
- 多个相等 w 时结构不唯一，需预先用稳定性或约定处理

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/cartesian-tree.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/cartesian-tree.md)
- OI Wiki ✓ [https://oi-wiki.org/ds/cartesian-tree/](https://oi-wiki.org/ds/cartesian-tree/)
