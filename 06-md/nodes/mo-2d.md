---
id: mo-2d
name: 二维莫队
group: G-D-7
stage: advanced
priority: P2
depth_tier: standard
---

# 二维莫队

> 莫队扩展到二维矩阵：状态为 (x1,y1,x2,y2) 子矩形，四方向整行/整列扩展，块长 n*q^(-1/4)，复杂度 O(n²*q^(3/4))。

<!-- 元信息: id=mo-2d · group=G-D-7 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

二维莫队（2D Mo's algorithm）把莫队从一维区间推广到二维矩形：每个状态是子矩形 (x1,y1)-(x2,y2)，指针沿四个方向扩展/收缩时一次移动一整行或一整列（O(1) 摊还的 add/remove 应用到行/列上的每个格子）。块长选 B=n·q^(-1/4)（n 为矩阵边长，q 为询问数），排序键为 (x1//B, y1//B, x2, y2)。适用问题如子矩阵内数值出现次数的平方和（BZOJ 2639 矩形计算）、子矩阵第 k 小数（P1527 矩阵乘法）。

## Why · 为什么

### 直觉 · Intuition

一维莫队每次移动一个下标代价 O(1)；二维里移动一条边界要处理一整行/列，代价 O(B)（行/列长）。四个边界指针 x1,x2,y1,y2 的移动次数分别约为 O(q·B)（行指针在块内摆动）、O(n⁴/B³)（列指针在块间来回）。令两者相等 q·B=n⁴·B⁻³ 得 B=n·q^(-1/4)，此时移动总代价 O(n²·q^(3/4))。这相当于把「块」从一维升级成二维网格，用均值不等式平衡四方向代价。

### 原理 · Principle

① 离散化矩阵值；② 块长 B=max(1, n·q^(-1/4))，注意可能为 0 需特判（OI Wiki 明确警告）；③ 排序：x1//B 第一、y1//B 第二、x2 第三、y2 第四（可奇偶化）；④ 维护：四组 while 分别调 add_row/remove_row/add_col/remove_col，每次移动整行/整列，行/列上的每个格子做 add/remove；⑤ 统计量 now=Σcnt[v]² 等可 O(1) 由格子增减更新。排序与指针移动顺序与普通莫队相同的「先扩后缩」约束。

### 历史 · History

二维莫队在国内 OI 圈被广泛使用，代表题 BZOJ 2639「矩形计算」（Hydro 收录）与「国家集训队」P1527「矩阵乘法」（洛谷收录，需配合值域分块求第 k 小）。OI Wiki 收录了完整介绍，明确给出块长推导 B=n·q^(-1/4) 及 B=0 特判的坑。

## How · 实现

### 伪代码

```python
B = max(1, int(n * q ** -0.25))
qs.sort(key=lambda q:(q.x1//B, q.y1//B, q.x2, q.y2))
X1=0; Y1=0; X2=-1; Y2=-1; now=0
for q in qs:
    while X1 > q.x1: X1--; add_row(X1, Y1, Y2)
    while X2 < q.x2: X2++; add_row(X2, Y1, Y2)
    while Y1 > q.y1: Y1--; add_col(Y1, X1, X2)
    while Y2 < q.y2: Y2++; add_col(Y2, X1, X2)
    while X1 < q.x1: remove_row(X1, Y1, Y2); X1++
    while X2 > q.x2: remove_row(X2, Y1, Y2); X2--
    while Y1 < q.y1: remove_col(Y1, X1, X2); Y1++
    while Y2 > q.y2: remove_col(Y2, X1, X2); Y2--
    ans[q.id] = now
```

### Python 实现

```python
def mo_2d(mat, queries):
    """二维莫队：子矩阵内数值平方和（p^2 贡献）.
    mat: 矩阵 (n 行 m 列); queries: [(x1,y1,x2,y2,id)] 闭区间 0-indexed.
    返回按 id 的答案."""
    import math
    n = len(mat); m = len(mat[0]) if mat else 0
    q = len(queries)
    B = max(1, int(n * q ** -0.25)) if q else max(1, int(n))
    B = max(B, 1)
    # 排序键: (x1//B, y1//B, x2, y2 奇偶化)
    qs = sorted(queries, key=lambda qq: (
        qq[0] // B, qq[1] // B,
        qq[2] if ((qq[0] // B + qq[1] // B) % 2 == 0) else -qq[2],
        qq[3] if ((qq[0] // B + qq[1] // B) % 2 == 0) else -qq[3],
    ))
    cnt = {}
    cur = 0
    ans = [0] * q
    x1 = y1 = x2 = 0; y2 = -1
    def add(v):
        nonlocal cur
        c = cnt.get(v, 0)
        cur += 2 * c + 1
        cnt[v] = c + 1
    def remove(v):
        nonlocal cur
        c = cnt[v]
        cur -= 2 * c - 1
        if c == 1:
            del cnt[v]
        else:
            cnt[v] = c - 1
    def add_row(r):
        for c in range(y1, y2 + 1):
            add(mat[r][c])
    def remove_row(r):
        for c in range(y1, y2 + 1):
            remove(mat[r][c])
    def add_col(c):
        for r in range(x1, x2 + 1):
            add(mat[r][c])
    def remove_col(c):
        for r in range(x1, x2 + 1):
            remove(mat[r][c])
    for a1, b1, a2, b2, idx in qs:
        while x1 > a1:
            x1 -= 1; add_row(x1)
        while x2 < a2:
            x2 += 1; add_row(x2)
        while y1 > b1:
            y1 -= 1; add_col(y1)
        while y2 < b2:
            y2 += 1; add_col(y2)
        while x1 < a1:
            remove_row(x1); x1 += 1
        while x2 > a2:
            remove_row(x2); x2 -= 1
        while y1 < b1:
            remove_col(y1); y1 += 1
        while y2 > b2:
            remove_col(y2); y2 -= 1
        ans[idx] = cur
    return ans

if __name__ == "__main__":
    mat = [[1, 2], [2, 3]]
    queries = [(0, 0, 1, 1, 0), (0, 0, 0, 1, 1), (1, 1, 1, 1, 2)]
    res = mo_2d(mat, queries)
    # 全矩阵: 1+2^2*2+3^2=1+8+9=18? 实际 p^2: 1^2+2^2+2^2+3^2=18
    assert res[0] == 6, res  # sum(cnt^2)=1+4+1
    assert res[1] == 2, res  # 1+1
    assert res[2] == 1, res
    import random
    random.seed(23)
    for _ in range(150):
        n = random.randint(1, 6); m = random.randint(1, 6)
        mat = [[random.randint(1, 4) for _ in range(m)] for _ in range(n)]
        qn = random.randint(1, 12)
        qs = []
        for i in range(qn):
            x1 = random.randrange(n); x2 = random.randrange(x1, n)
            y1 = random.randrange(m); y2 = random.randrange(y1, m)
            qs.append((x1, y1, x2, y2, i))
        got = mo_2d(mat, qs)
        for (x1, y1, x2, y2, i) in qs:
            cnt = {}
            for r in range(x1, x2 + 1):
                for c in range(y1, y2 + 1):
                    cnt[mat[r][c]] = cnt.get(mat[r][c], 0) + 1
            exp = sum(v * v for v in cnt.values())
            assert got[i] == exp, (mat, x1, y1, x2, y2, got[i], exp)
    print("mo_2d OK")

```

**PyPy 提示**: 值域大用离散化 + list 计数替代 dict（dict 的 get/del 常数大）；add/remove 内联到行/列循环；P1527 类题需要额外值域分块求 k 小，常数敏感，OI Wiki 建议块长直接设常数（n,q 最大时约 11）。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n²·q^(3/4) + q log q)（排序）；块长 B=n·q^(-1/4) |
| 空间 | O(n² + q) |

### 局限

纯 Python 下常数极大（每次移动扫整行/列），适合小矩阵（如 200×200）或 q 较小的场景；n=500 且 q=6e4 的 P1527 用 Python 很难通过；强制在线不支持；统计必须可 O(1) 随单格增减更新。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| BZOJ | 2639 | 5 | 矩形计算：子矩阵内数值出现次数平方和，二维莫队模板题，OI Wiki 例题 1 | [https://hydro.ac/p/bzoj-P2639](https://hydro.ac/p/bzoj-P2639) |
| Luogu | P1527 | 6 | [国家集训队] 矩阵乘法：子矩阵第 k 小数，二维莫队 + 值域分块，OI Wiki 例题 2 | [https://www.luogu.com.cn/problem/P1527](https://www.luogu.com.cn/problem/P1527) |

## Pitfalls · 易错点

- 块长 B=n*q^(-1/4) 在 n、q 取极端时可能为 0，必须特判 max(1,...)（OI Wiki 明确警告）
- 四个 while 同样要「先扩后缩」，否则矩形出现负面积/行被重复删除
- 移动一行/一列时循环区间要用当前的其他两个边界（Y1..Y2 / X1..X2），写错会整体错位
- 离散化矩阵值后再做 cnt 计数，注意矩阵元素范围可达 2e9
- P1527 还需值域分块，仅二维莫队不足以 O(1) 求 k 小；时间限制紧时块长设常数

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/mo-algo-2dimen.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/mo-algo-2dimen.md)
- OI Wiki ✓ [https://oi-wiki.org/misc/mo-algo-2dimen/](https://oi-wiki.org/misc/mo-algo-2dimen/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/code/mo-algo-2dimen/mo-algo-2dimen_1.cpp](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/code/mo-algo-2dimen/mo-algo-2dimen_1.cpp)
