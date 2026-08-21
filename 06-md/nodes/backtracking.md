---
id: backtracking
name: 回溯法
group: G-A-14
stage: basic
priority: P0
depth_tier: deep
---

# 回溯法

> DFS+撤销操作，走不通就回头，排列/组合/棋盘类问题

<!-- 元信息: id=backtracking · group=G-A-14 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

回溯法（backtracking）是深度优先搜索的一种系统化变体：构造问题的解空间树，用 DFS 遍历；到达不满足约束的分支（边界条件）就'剪枝回头'，探索另一条链；到达目标状态则记录解。核心是'试探-标记-递归-撤销'四步，通过撤销操作保证搜索空间互不污染。排列、组合、子集、N皇后、数独、迷宫计数等问题都用回溯法。

## Why · 为什么

### 直觉 · Intuition

把解想象成一步步做选择：放第一个皇后在第几列？第二个在第几列？……每步做选择时如果发现当前部分选择已经非法（如皇后冲突），就立刻放弃继续往下走，回到上一步换一个选择——这就是'走不通就回头'。撤销操作让上层选择改变时下层状态是干净的。

### 原理 · Principle

解空间是 n 叉树（每层一次选择），DFS 遍历所有叶节点即遍历所有候选解。回溯法在遍历中维护'当前路径'与'已用资源'（如列、对角线占用）。约束剪枝发生在扩展前：若当前部分解已不可能满足约束，则其子树全部不可行，可直接跳过。空间开销 O(深度)，与候选解数量无关，这是相对全量枚举的优势。N皇后用列/两条对角线三个布尔数组将判定复杂度降为 O(1)。

### 历史 · History

回溯法的思想可追溯到 19 世纪，N皇后问题最早由高斯 1850 年左右提出并研究。现代算法教材中，回溯是分支限界法（branch and bound）的姊妹技巧，1970s 由 Horowitz 与 Sahni 等人在算法教科书中系统整理。

## How · 实现

### 伪代码

```python
def backtrack(path, 已用资源):
    if 到达目标(解):
        记录解; return
    if 不可行/边界条件:
        return  # 剪枝
    for 每个候选选择 c:
        if 选择 c 合法:
            做出选择(标记资源)
            backtrack(path + [c])
            撤销选择(清除标记)
```

### Python 实现

```python
def solve_nqueens(n):
    """N皇后问题: 返回所有解, 每个解是长度n的列表, 第i行皇后所在列(1-based)
    用列/主对角线/副对角线三个布尔数组实现 O(1) 冲突判定
    """
    col = [False] * n
    diag1 = [False] * (2 * n - 1)  # r-c 偏移
    diag2 = [False] * (2 * n - 1)  # r+c
    board = [0] * n
    ans = []

    def dfs(r):
        if r == n:
            ans.append(board[:])
            return
        for c in range(n):
            if not col[c] and not diag1[r - c + n - 1] and not diag2[r + c]:
                col[c] = diag1[r - c + n - 1] = diag2[r + c] = True
                board[r] = c + 1
                dfs(r + 1)
                col[c] = diag1[r - c + n - 1] = diag2[r + c] = False

    dfs(0)
    return ans


def permutations(arr):
    """回溯求全排列(去重版)"""
    n = len(arr)
    used = [False] * n
    path = []
    res = []

    def dfs():
        if len(path) == n:
            res.append(path[:])
            return
        for i in range(n):
            if used[i]:
                continue
            if i > 0 and arr[i] == arr[i - 1] and not used[i - 1]:
                continue  # 去重: 相同元素按顺序使用
            used[i] = True
            path.append(arr[i])
            dfs()
            path.pop()
            used[i] = False

    dfs()
    return res


def verify(board):
    """验证N皇后解合法"""
    n = len(board)
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j]:
                return False
            if abs(board[i] - board[j]) == abs(i - j):
                return False
    return True


if __name__ == "__main__":
    assert len(solve_nqueens(1)) == 1
    assert len(solve_nqueens(4)) == 2
    s8 = solve_nqueens(8)
    assert len(s8) == 92
    assert all(verify(sol) for sol in s8)
    assert s8[0] == [1, 5, 8, 6, 3, 7, 2, 4]  # 字典序第一个解

    # 全排列: [1,1,2] 去重后 3 种
    perms = permutations([1, 1, 2])
    assert len(perms) == 3
    assert sorted(perms) == sorted([[1, 1, 2], [1, 2, 1], [2, 1, 1]])

    print("backtracking all tests passed")

```

**PyPy 提示**: N皇后等回溯题纯 Python 可过（n≤13 常用），再大需剪枝或位运算优化。PyPy 的递归开销略高，深递归可用 sys.setrecursionlimit。位运算状态压缩（列/对角线的位掩码）能显著提速。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 最坏 O(分支数^深度)，实际靠剪枝大幅减少；N皇后上界 O(n!) |
| 空间 | O(深度 + 资源标记数组)，与候选解数量无关 |

### 局限

回溯是指数级算法，仅适合 n≤20 左右的选择空间；分支因子大且剪枝弱时退化近纯枚举；递归深度受系统限制（Python 默认 1000）。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1219 | 3 | USACO Checker Challenge：N皇后模板，输出前3解+总数 | [https://www.luogu.com.cn/problem/P1219](https://www.luogu.com.cn/problem/P1219) |
| Luogu | P1605 | 2 | 迷宫：回溯计数，每格最多经过一次 | [https://www.luogu.com.cn/problem/P1605](https://www.luogu.com.cn/problem/P1605) |

## Pitfalls · 易错点

- 撤销操作必须在递归返回后执行，否则污染后续分支（最经典bug）
- N皇后两条对角线的索引映射：r-c 需偏移，r+c 直接；范围 2n-1
- 排列去重：相同元素需'按序使用'（used[i-1] 检查），否则重复解
- 边界条件与目标条件都要写，避免死循环或漏解
- 记录解时必须复制 path（path[:]），否则引用同一对象

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/search/backtracking/](https://oi-wiki.org/search/backtracking/)
- 书籍 ✓ `CPH ch5 p57 (backtracking)`
