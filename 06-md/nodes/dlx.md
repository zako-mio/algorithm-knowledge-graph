---
id: dlx
name: Dancing Links(X算法)
group: G-A-14
stage: advanced
priority: P2
depth_tier: standard
---

# Dancing Links(X算法)

> 双向十字链表加速精确覆盖/重复覆盖问题的回溯搜索

<!-- 元信息: id=dlx · group=G-A-14 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

DLX（Dancing Links，舞蹈链）是 Donald Knuth 提出的用双向十字链表优化的 X 算法，用于高效求解精确覆盖问题（Exact Cover）及重复覆盖问题。精确覆盖：给定 01 矩阵，选择若干行使得每列恰好有一个 1。DLX 用四个指针域（上下左右）的循环双向链表表示矩阵中的 1，支持 O(1) 删除/恢复行列，配合'每次选元素最少列'的启发式回溯。数独、N皇后（行/列/对角建模）、八皇后类覆盖问题都转化为精确覆盖后用 DLX 秒解。

## Why · 为什么

### 直觉 · Intuition

精确覆盖的暴力枚举是 O(2^n) 选行 + O(nm) 校验，不可行。DLX 的聪明处：把 01 矩阵用十字链表组织，删一列时顺着链把该列所有相关行都摘掉（链式跳跃如'跳舞'），回溯时按逆序 O(1) 恢复。同时每步贪心选'1 最少的列'扩展，保证分支最少。难点不在链表本身而在建模：行=决策，列=状态/约束。

### 原理 · Principle

X 算法：①选一行 r 加入解集；②删除 r 以及 r 的 1 所在列相关的所有行列；③对剩余矩阵递归；④若空矩阵且上次删除行全 1 则成功。Dancing Links 将'删除/恢复行和列'用链表指针操作实现，恢复严格逆序（Knuth 的 remove/recover 对）。复杂度与矩阵中 1 的个数有关而与矩阵尺寸无关，实际接近 O(c^n)（c 略大于 1，n 为 1 个数），远优于 2^行数。数独建模：729 行（9×9×9 个 (r,c,w) 决策）× 324 列（行/列/宫/格四类约束各 81），共 2916 个 1。

### 历史 · History

Knuth 在 2000 年发表的论文《Dancing Links》（Millenial Perspective 系列）中提出，用'舞蹈'一词比喻链式节点被删除恢复时的跳跃。其思想源于 1970s 他设计的 Algorithm X，DLX 使其在数独求解等场景达到实用高性能，成为算法竞赛高级搜索题的标准技术。

## How · 实现

### 伪代码

```python
# 数据结构: 每个1一个节点, 记录上下左右邻接
# 列头 0..ncols 组成环形链表, size[c] 记录列c元素数
# first[r] 指向行r首元素

remove(c):
    摘除列头c(L/R指针)
    遍历c列每个元素i: 遍历i所在行每个元素j: 摘除j(U/D指针), size[col[j]]--

restore(c):  # 逆序恢复
    遍历c列反向, 再反向遍历行, 恢复指针与size

dance():
    if 链表空: 成功
    c = 元素最少的列
    remove(c)
    遍历c列每个元素i(选第row[i]行):
        遍历i行元素j: remove(col[j])
        dance()
        逆序恢复
    restore(c)
```

### Python 实现

```python
class DLX:
    """Dancing Links 精确覆盖: 选行使每列恰有一个1
    add_node(r, c) 中 r,c 为 1-based 行列号
    """
    def __init__(self, n_rows, n_cols):
        self.nc = n_cols
        self.L = []; self.R = []; self.U = []; self.D = []
        self.col = []; self.row = []
        self.size = [0] * (n_cols + 1)     # 每列元素数
        for i in range(n_cols + 1):        # 列头节点 0..n_cols
            self.L.append(i - 1); self.R.append(i + 1)
            self.U.append(i); self.D.append(i)
            self.col.append(i); self.row.append(-1)
        self.L[0] = n_cols; self.R[n_cols] = 0
        self.first = [-1] * (n_rows + 1)   # 每行首元素
        self.ans = []

    def add_node(self, r, c):
        """在 (r,c) 插入1"""
        assert 1 <= c <= self.nc
        idx = len(self.L)
        self.col.append(c); self.row.append(r)
        self.size[c] += 1
        # 垂直链: 插入到列头c下方
        self.U.append(self.U[c]); self.D.append(c)
        self.D[self.U[c]] = idx; self.U[c] = idx
        # 水平链: 插入到行首first[r]右方
        if self.first[r] == -1:
            self.first[r] = idx
            self.L.append(idx); self.R.append(idx)
        else:
            f = self.first[r]
            self.L.append(f); self.R.append(self.R[f])
            self.L[self.R[f]] = idx; self.R[f] = idx

    def remove(self, c):
        """删除列c及其相关行"""
        self.L[self.R[c]] = self.L[c]; self.R[self.L[c]] = self.R[c]
        i = self.D[c]
        while i != c:
            j = self.R[i]
            while j != i:
                self.U[self.D[j]] = self.U[j]; self.D[self.U[j]] = self.D[j]
                self.size[self.col[j]] -= 1
                j = self.R[j]
            i = self.D[i]

    def restore(self, c):
        """恢复列c(与remove严格逆序)"""
        i = self.U[c]
        while i != c:
            j = self.L[i]
            while j != i:
                self.size[self.col[j]] += 1
                self.U[self.D[j]] = j; self.D[self.U[j]] = j
                j = self.L[j]
            i = self.U[i]
        self.L[self.R[c]] = c; self.R[self.L[c]] = c

    def dance(self, k=0):
        """递归求解精确覆盖, 返回是否存在解, 答案在 self.ans"""
        if self.R[0] == 0:
            self.depth = k
            return True
        # 启发式: 选元素最少的列
        c = self.R[0]; i = self.R[0]
        while i != 0:
            if self.size[i] < self.size[c]:
                c = i
            i = self.R[i]
        self.remove(c)
        i = self.D[c]
        while i != c:
            self.ans.append(self.row[i])
            j = self.R[i]
            while j != i:
                self.remove(self.col[j])
                j = self.R[j]
            if self.dance(k + 1):
                return True
            j = self.L[i]
            while j != i:
                self.restore(self.col[j])
                j = self.L[j]
            self.ans.pop()
            i = self.D[i]
        self.restore(c)
        return False


def solve_exact_cover(matrix):
    """从01矩阵直接求解精确覆盖, 返回解行列表(1-based)或None"""
    nr, nc = len(matrix), len(matrix[0])
    dlx = DLX(nr, nc)
    for r in range(nr):
        for c in range(nc):
            if matrix[r][c]:
                dlx.add_node(r + 1, c + 1)
    if dlx.dance():
        return sorted(dlx.ans)
    return None


if __name__ == "__main__":
    # OI Wiki 精确覆盖例子: 答案行 1,4,5
    m = [
        [0, 0, 1, 0, 1, 1, 0],
        [1, 0, 0, 1, 0, 0, 1],
        [0, 1, 1, 0, 0, 1, 0],
        [1, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 1],
        [0, 0, 0, 1, 1, 0, 1],
    ]
    assert solve_exact_cover(m) == [1, 4, 5]

    # 无解: 最后一列无任何1
    m2 = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]
    assert solve_exact_cover(m2) is None

    # 多个合法解: 行[1,2,3]各覆盖一列, 行4单独覆盖所有列
    # 两种都合法精确覆盖; DLX按搜索顺序先找到 [1,2,3]
    m3 = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 1]]
    sol = solve_exact_cover(m3)
    assert sol in ([1, 2, 3], [4]), sol

    # 互补覆盖: 行[1,0]与[0,1]互补; 行[1,1]单独也覆盖两列
    # 两者皆合法, DLX先探索列1的行1 -> [1,2]
    m4 = [[1, 0], [0, 1], [1, 1]]
    sol = solve_exact_cover(m4)
    assert sol in ([1, 2], [3]), sol

    print("dlx all tests passed (exact cover examples)")

```

**PyPy 提示**: DLX 是链表密集操作，PyPy 下性能优于 CPython。递归深度 = 解大小，注意 setrecursionlimit。节点数多时（数独约 3000 节点）可用数组实现代替类对象避免开销。建模正确性比实现效率更重要。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 理论指数级，但实际与矩阵中 1 的个数相关而非矩阵规模；启发式选最少列后接近线性 |
| 空间 | O(1 的个数)，双向链表节点数 |

### 局限

建模是难点：需将问题抽象为'行=决策、列=约束'的 01 矩阵；重复覆盖问题需额外估价函数剪枝；矩阵 1 极多时节点数爆炸；纯 Python 在大规模（数千行）时仍偏慢。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P4929 | 3 | 【模板】舞蹈链(DLX)：精确覆盖模板题 | [https://www.luogu.com.cn/problem/P4929](https://www.luogu.com.cn/problem/P4929) |
| Luogu | P1784 | 3 | 数独：729行×324列精确覆盖建模经典题 | [https://www.luogu.com.cn/problem/P1784](https://www.luogu.com.cn/problem/P1784) |
| Luogu | P4205 | 5 | NOI2005 智慧珠游戏：旋转/翻转的精确覆盖建模（5280行） | [https://www.luogu.com.cn/problem/P4205](https://www.luogu.com.cn/problem/P4205) |

## Pitfalls · 易错点

- 建模错误最常见：行=决策、列=约束，约束之间须互相独立（如数独四类约束）
- remove 与 restore 必须严格逆序，指针错乱导致死循环
- 节点索引从列头节点 n_cols 之后开始分配，勿覆盖列头
- 无解判定：列无元素时该列无法覆盖，应快速失败
- 重复覆盖需额外最优性估价剪枝，直接套精确覆盖模板会漏解

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/search/dlx/](https://oi-wiki.org/search/dlx/)
- 论文 ✓ [https://arxiv.org/abs/cs/0011047](https://arxiv.org/abs/cs/0011047)
