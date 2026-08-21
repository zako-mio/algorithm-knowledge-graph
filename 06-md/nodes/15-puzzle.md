---
id: 15-puzzle
name: 15谜题可解性判定
group: G-E-7
stage: advanced
priority: P2
depth_tier: standard
---

# 15谜题可解性判定

> N-puzzle可解性判定：逆序对数奇偶性+空格行距，不可解则无解

<!-- 元信息: id=15-puzzle · group=G-E-7 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

15-puzzle(数字滑块谜题, N-puzzle) 是 4x4 方盘放 15 个编号方块加一个空格的滑块游戏，每步将空格与相邻方块交换，目标按序排列。求解可判定性问题：给定一个盘面能否还原？判定法则：奇数阶(m 为奇数)盘面可解 ⇔ 逆序对数为偶数；偶数阶(m 为偶数)盘面可解 ⇔ 逆序对奇偶性与(空格所在行距底行的距离)奇偶性相同。最优解为 NP 困难，可解性判定与搜索(如 A*)是两个不同层面的问题。

## Why · 为什么

### 直觉 · Intuition

每交换一次空格与相邻方块，逆序对奇偶性必翻转，而空格移动改变了其在网格中的行列。把盘面状态看成排列，还原目标排列的逆序对数为 0(偶)。对所有可还原状态，'逆序对奇偶性'与'空格位置奇偶性'存在不变量，判据正是检查两个不变量是否匹配。

### 原理 · Principle

Johnson & Story(1879)证明 m,n≥2 的 m×n 滑块盘可解性：构造可还原盘面的生成集合，论证所有偶数排列可解。Archer(1999)用哈密顿路径给出另一证明。判据实现：把方块按行主序读成序列(忽略空格)，数逆序对数；对偶数阶盘，再加空格所在行距底行的距离(从 1 数起)贡献的奇偶。奇偶匹配则可解。

### 历史 · History

15-puzzle 由 Noyes Chapman 发明，1880s 风靡一时，是最古老的滑块类游戏。可解性由 Johnson & Story 于 1879 年证明，群理论角度可证其状态组为交错群 A_15。OI Wiki 与 CP-Algorithms 均收录其可解性判定与 A* 搜索解法，是最优解(至多 80 步)与 NP 困难性研究的经典对象。

## How · 实现

### 伪代码

```python
# 判定 m 行 n 列 N-puzzle 是否可解
board = 二维数组(空格=0)
seq = 行主序读入所有非零数字
inv = 数 seq 逆序对数
if n 为奇数:          # 列数(空格所在行横向移动不改变奇偶)
  return inv % 2 == 0
else:                 # 偶数阶
  blank_row = 空格所在行(0-index, 距底= m-1-blank_row)
  return (inv + (m - 1 - blank_row)) % 2 == 0
```

### Python 实现

```python
def inversions(seq):
    """归并排序求逆序对数。"""
    seq = list(seq)
    n = len(seq)
    tmp = [0] * n

    def merge_sort(l, r):
        if r - l <= 1:
            return 0
        mid = (l + r) // 2
        cnt = merge_sort(l, mid) + merge_sort(mid, r)
        i, j, k = l, mid, l
        while i < mid and j < r:
            if seq[i] <= seq[j]:
                tmp[k] = seq[i]
                i += 1
            else:
                tmp[k] = seq[j]
                cnt += mid - i
                j += 1
            k += 1
        while i < mid:
            tmp[k] = seq[i]
            i += 1
            k += 1
        while j < r:
            tmp[k] = seq[j]
            j += 1
            k += 1
        seq[l:r] = tmp[l:r]
        return cnt

    return merge_sort(0, n)


def is_solvable(board):
    """判断 m 行 n 列 N-puzzle 是否可解。
    board: list[list[int]], 0 表示空格。
    """
    m = len(board)
    n = len(board[0])
    seq = []
    blank_row = -1
    for i in range(m):
        for j in range(n):
            if board[i][j] == 0:
                blank_row = i
            else:
                seq.append(board[i][j])
    inv = inversions(seq)
    if n % 2 == 1:
        return inv % 2 == 0
    # 偶数阶: 逆序对奇偶性 与 空格距底行距离奇偶性 相同
    dist_from_bottom = m - 1 - blank_row
    return (inv + dist_from_bottom) % 2 == 0


def solved_board(m, n):
    """生成目标盘面(空格在右下)。"""
    b = [[(i * n + j + 1) % (m * n) for j in range(n)] for i in range(m)]
    return b


if __name__ == '__main__':
    # 目标盘面必可解
    assert is_solvable(solved_board(4, 4)) is True
    assert is_solvable(solved_board(3, 3)) is True

    # 3x3 已知可解盘
    ok33 = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    assert is_solvable(ok33) is True
    # 3x3 已知不可解盘(交换1和2)
    bad33 = [[2, 1, 3], [4, 5, 6], [7, 8, 0]]
    assert is_solvable(bad33) is False

    # 4x4 目标盘
    ok44 = solved_board(4, 4)
    assert is_solvable(ok44) is True
    # 4x4 交换两个非空格数字应不可解(逆序奇偶变化)
    bad44 = [row[:] for row in ok44]
    bad44[0][0], bad44[0][1] = bad44[0][1], bad44[0][0]
    assert is_solvable(bad44) is False

    # 空格位置对偶数阶有影响: 目标盘移动空格到第0行
    moved = [row[:] for row in ok44]
    # 把空格从(3,3)移到(0,0), 其余数字循环移位保持合法
    vals = [v for row in ok44 for v in row if v != 0]
    it = iter(vals)
    newb = [[0] * 4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            if (i, j) == (0, 0):
                continue
            newb[i][j] = next(it)
    # 这种整盘平移不改变逆序数, 但空格行距变了 -> 奇偶可能改变
    print('3x3 ok=', is_solvable(ok33), ' bad=', is_solvable(bad33))
    print('4x4 ok=', is_solvable(ok44), ' bad=', is_solvable(bad44))
    print('4x4 moved blank to top-left:', is_solvable(newb))
    print('All 15-puzzle solvability tests passed!')

```

**PyPy 提示**: 逆序对用归并排序 O(n log n) 最稳; 若方盘数字序列很短(如 8-puzzle)直接用冒泡计数也可; 判定本身只关心奇偶, 可仅累计奇偶省时间。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(M*N) 读取 + O(M*N log(M*N)) 逆序对(归并) |
| 空间 | O(M*N) |

### 局限

仅判定可解性, 不给出还原方案; 求最少步数是 NP 困难(15-puzzle 最优解至多 80 步); 判定公式依赖盘面尺寸奇偶, 混用会判错; 部分题目(如 POJ 1077 Eight)要求输出方案, 需 A*/IDA* 搜索。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| HackerRank | n-puzzle | 4 | N Puzzle: A* 搜索求解 15-puzzle, 需要可解性判定+启发式 | [https://www.hackerrank.com/challenges/n-puzzle](https://www.hackerrank.com/challenges/n-puzzle) |
| POJ | 1077 | 4 | Eight: 8-puzzle 搜索, 可解性判定(3x3 逆序对奇偶)必备 | [http://poj.org/problem?id=1077](http://poj.org/problem?id=1077) |
| Codeforces | 645A | 3 | Amity Assessment: 3x3 滑块可解性判定(小规模奇偶性) | [https://codeforces.com/problemset/problem/645/A](https://codeforces.com/problemset/problem/645/A) |

## Pitfalls · 易错点

- 逆序对计算要跳过空格(0), 把空格算进去会得到错误奇偶
- 奇偶阶判据不同: 奇数阶只看逆序对, 偶数阶要加空格行距(距底行)奇偶
- 行主序读盘面: 空格不参与逆序, 但位置要单独记录
- 把空格放到正确位置不算入逆序(空格不是数字), 读入时 if val != 0 才 append
- 判可解≠可解路径, 别在判定题里用 BFS 全状态(4x4 状态空间 16!/2 巨大)

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/misc/15-puzzle/](https://oi-wiki.org/misc/15-puzzle/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/15-puzzle.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/15-puzzle.md)
- CP-Algorithms ✓ [https://cp-algorithms.com/others/15-puzzle.html](https://cp-algorithms.com/others/15-puzzle.html)
- web ✓ [https://en.wikipedia.org/wiki/15_puzzle](https://en.wikipedia.org/wiki/15_puzzle)
