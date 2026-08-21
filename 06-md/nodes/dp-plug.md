---
id: dp-plug
name: 插头DP（连通性状态压缩DP）
group: G-A-13
stage: advanced
priority: P2
depth_tier: standard
---

# 插头DP（连通性状态压缩DP）

> 轮廓线DP + 连通性编码，逐格转移，解决网格图的哈密顿回路/路径计数、生成树计数等问题

<!-- 元信息: id=dp-plug · group=G-A-13 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

插头DP（连通性状态压缩DP）是轮廓线DP的推广：在处理格子 (i,j) 时，轮廓线是已决策与未决策格子之间的分界线，状态记录轮廓线上每个位置'是否有插头（与相邻格的连接）'以及插头之间的连通性。一条回路问题时插头总是成对出现，合法状态构成括号序列。常用两种编码：括号表示（'(' ')' 配对）与最小表示（连通分量用最小可用数字标记）。多数回路问题只需要记录插头是否存在（如 Eat the Trees 多回路覆盖），而单回路问题（Formula 1、Ural 1519）必须区分连通性以禁止提前形成小环。状态可用哈希表/字典存储（合法状态稀疏），行末滚动 roll() 把最后一列左插头移到行首。转移分四类：左、上均有插头（合并或闭合）、恰有一个插头（延伸或转向）、均无插头（新建一对插头）、以及障碍格处理。

## Why · 为什么

### 直觉 · Intuition

逐行状压 DP 一行一行推进时，只能表达'该格是否被覆盖'，无法表达连线从哪里来、到哪里去。改为逐格推进并记录'轮廓线'上的连接状态：每个格子的下方与右侧是'出线'，左侧与上方是'入线'，一个格子决定了它 4 个方向中哪些存在连接。插头成对出现是因为每条线有两个端点，若某条线两端都落在已处理区域（提前成环），在单回路问题中就必须禁止。状态越小越好，用最小表示压缩掉编号顺序。

### 原理 · Principle

轮廓线宽度为 m+1：m 个上插头 + 1 个左插头。最小表示编码：把轮廓线上非零插头按出现顺序重新标号为 1,2,3…，保证同一连通块编号相同，是字典序最小的规范形。转移枚举：①lt,up 均存在：若 lt==up，说明左右两个插头本就同连通块，闭合会成环，仅当是最后一个格子且其余插头全 0 时接受（单回路）；否则合并两个连通块（把 b[i]==lt 全部改成 up）。②仅一个存在：该插头可向右或向下延伸（需对应格子开放）。③均不存在：若右、下格子均开放，新建一对插头。每次转移后对状态重新最小表示编码；行末 roll：要求轮廓线最后一格（左插头位）为 0，去掉后整体左移一位。多回路问题（Eat the Trees）不需要连通性编码，只需 0/1 位，直接位运算即可。

### 历史 · History

连通性状态压缩 DP 的经典发展来自对'一条回路覆盖棋盘'问题（如 Ural 1519 Formula 1、HDU 1693 Eat the Trees）的研究。中国竞赛圈由毛啸等选手在 2007 年前后系统总结推广（'插头DP'命名流行于国内 OI），OI Wiki 收录完整的三类问题模板（多回路、单回路、单路径）。单路径问题需额外记录独立插头（路径端点）的生成/消失次数（≤2），并将该信息编码进状态或外加一维。

## How · 实现

### 伪代码

```python
# 单回路覆盖 n*m 棋盘（最小表示 + 哈希表/字典）
cur = {encode(all-0轮廓): 1}
for i in 0..n-1:
  for j in 0..m-1:
    nxt = {}
    for state in cur:
      decode(state) -> b[]
      lt, up = b[j], b[j+1]
      if 障碍格: 若 lt==0 且 up==0 则直接保留; continue
      if lt and up:
        if lt==up:
          if 最后一格且其余全0: nxt[all-0] += val
        else: 合并连通块(把 lt 全部改成 up), 置 b[j]=b[j+1]=0
      elif lt or up:
        t = lt|up
        if 右格开放: 延伸 b[j+1]=t, b[j]=0
        if 下格开放: 延伸 b[j]=t, b[j+1]=0
      else:
        if 右与下均开放: b[j]=b[j+1]=新编号(成对新插头)
    cur = 最小表示去重合并后的 nxt
  行末 roll(): 要求 b[m]==0, 去掉 b[m] 并在头部补 0
答案 = cur 中全 0 状态的计数
```

### Python 实现

```python
# -*- coding: utf-8 -*-
# 插头DP 单回路覆盖 n*m 棋盘（含障碍），最小表示编码，返回方案数
from collections import defaultdict


def encode(b):
    """轮廓线数组 -> 最小表示整数编码（tuple）"""
    mp, out, nxt = {}, [], 1
    for x in b:
        if x == 0:
            out.append(0)
        else:
            if x not in mp:
                mp[x] = nxt
                nxt += 1
            out.append(mp[x])
    return tuple(out)


def plug_dp(n, m, open_cells):
    """open_cells: {(r,c)} 0-indexed 可走的格子。返回用一条回路覆盖所有开放格子的方案数。"""
    cur = {encode([0] * (m + 1)): 1}
    last_open = max(r * m + c for (r, c) in open_cells)
    for r in range(n):
        for c in range(m):
            idx = r * m + c
            is_cell = (r, c) in open_cells
            is_last = idx == last_open
            nxt = defaultdict(int)
            for state, val in cur.items():
                b = list(state)
                left, up = b[c], b[c + 1]
                if not is_cell:                     # 障碍格
                    if left == 0 and up == 0:
                        nxt[encode(b)] += val
                    continue
                if left and up:
                    if left == up:                  # 闭合：必须最后一格且其余全 0
                        if is_last:
                            bb = list(b); bb[c] = bb[c + 1] = 0
                            if all(x == 0 for x in bb):
                                nxt[encode(bb)] += val
                    else:                            # 合并两个连通块
                        bb = list(b); bb[c] = bb[c + 1] = 0
                        for i in range(m + 1):
                            if bb[i] == left:
                                bb[i] = up
                        nxt[encode(bb)] += val
                elif left or up:
                    t = left | up
                    if c + 1 < m and (r, c + 1) in open_cells:   # 向右延伸
                        bb = list(b); bb[c] = 0; bb[c + 1] = t
                        nxt[encode(bb)] += val
                    if r + 1 < n and (r + 1, c) in open_cells:   # 向下延伸
                        bb = list(b); bb[c] = t; bb[c + 1] = 0
                        nxt[encode(bb)] += val
                else:                               # 新建一对插头（成对生成）
                    if (c + 1 < m and (r, c + 1) in open_cells
                            and r + 1 < n and (r + 1, c) in open_cells):
                        bb = list(b); bb[c] = m + 1; bb[c + 1] = m + 1
                        nxt[encode(bb)] += val
            cur = nxt
        # 行末滚动：最后一列左插头必须为 0，去掉后整体左移一位
        roll = defaultdict(int)
        for state, val in cur.items():
            bb = list(state)
            if bb[m] != 0:
                continue
            del bb[m]
            bb.insert(0, 0)
            roll[encode(bb)] += val
        cur = roll
    return cur.get(encode([0] * (m + 1)), 0)


if __name__ == '__main__':
    def all_open(n, m):
        return {(r, c) for r in range(n) for c in range(m)}
    # 与暴力枚举对拍的小规模值
    assert plug_dp(2, 2, all_open(2, 2)) == 1
    assert plug_dp(2, 3, all_open(2, 3)) == 1
    assert plug_dp(3, 3, all_open(3, 3)) == 0   # 3x3 无单回路
    assert plug_dp(3, 4, all_open(3, 4)) == 2
    assert plug_dp(2, 4, all_open(2, 4)) == 1
    # 中心有障碍的 3x3：绕开中心仍有一条回路
    oc = all_open(3, 3) - {(1, 1)}
    assert plug_dp(3, 3, oc) == 1
    print('plug-dp tests passed')

```

**PyPy 提示**: 状态用字典/tuple 在 PyPy 下可用但常数较大；n,m≤12 全开格可跑，更大需手写哈希（链式前向星 + 状态数组），并用整数位编码替代 tuple。最小表示每次转移都要重新编码，注意用位运算加速。Python 只适合小棋盘或教学演示，正式题建议 C++。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n·m·S)（S 为合法状态数；单回路问题合法状态为括号序列数，远小于全状态；字典/哈希均摊 O(1)） |
| 空间 | O(S)（每层两张哈希表） |

### 局限

状态爆炸：m 增大状态数呈指数（连通性合法状态为卡特兰相关），一般 m≤10~12 才实用；Python 常数大，仅适合小棋盘。多条回路问题不需要连通性编码（比单回路简单）。含权值的最优回路/路径问题（如最大权回路）把计数改为取 max 即可，但要处理障碍与单格答案。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Ural | 1519 | 4 | Formula 1：单回路覆盖带障碍棋盘计数，插头DP经典模板题 | [https://acm.timus.ru/problem.aspx?space=1&num=1519](https://acm.timus.ru/problem.aspx?space=1&num=1519) |
| HDU | 1693 | 3 | Eat the Trees：多回路覆盖，只需 0/1 插头位，不需要连通性编码 | [https://acm.hdu.edu.cn/showproblem.php?pid=1693](https://acm.hdu.edu.cn/showproblem.php?pid=1693) |
| Luogu | P5056 | 5 | 【模板】插头DP：单回路计数，与 Ural 1519 同型 | [https://www.luogu.com.cn/problem/P5056](https://www.luogu.com.cn/problem/P5056) |
| Luogu | P3190 | 4 | HNOI2007 神奇游乐园：最大权单回路，状态计数改取 max | [https://www.luogu.com.cn/problem/P3190](https://www.luogu.com.cn/problem/P3190) |

## Pitfalls · 易错点

- 单回路问题必须区分插头连通性（最小表示/括号），否则会算入多个小环
- 左、上均有插头且同连通块时闭合会成环，只能允许在最后一个空格闭合
- 行末 roll 时若最后一列左插头非 0 则该状态非法，必须丢弃
- 障碍格必须延续状态（left==0 且 up==0 才合法），且不做插头生成
- 最小表示编码的重新标号必须从 1 开始且 0 保留（0 表示无插头）
- 新建一对插头时两者要用同一新编号（保证连通），否则合并判定出错
- m 较大时 Python 字典 + tuple 编码会超时/爆内存，需手写哈希与位编码

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/dp/plug/](https://oi-wiki.org/dp/plug/)
- 书籍 ✓ `OI Wiki 插头DP 三类模板（Eat the Trees / Formula 1 / 单路径）`
