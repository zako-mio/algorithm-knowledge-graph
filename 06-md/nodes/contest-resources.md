---
id: contest-resources
name: 学习资源与刷题路线
group: G-E-8
stage: intermediate
priority: P2
depth_tier: standard
---

# 学习资源与刷题路线

> OI Wiki/CPH 等教程、CF/AtCoder/Luogu 刷题路线、经典教材与进阶路径

<!-- 元信息: id=contest-resources · group=G-E-8 · stage=intermediate · priority=P2 · depth_tier=standard -->

## What · 是什么

本节点汇总算法竞赛的学习资源与训练路线，帮助按阶段系统提升：①权威教程：OI Wiki（中文百科全书）、CP-Algorithms（英文 e-maxx）、Competitive Programmer's Handbook / CPH（Antti Laaksonen）；②刷题平台：Codeforces（周赛/评级）、AtCoder（ABC/ARC，题目质量高）、Luogu（中文社区+真题）、QOJ/LibreOJ（集训队题）、LeetCode（面试向）；③经典教材：刘汝佳《算法竞赛入门经典》《训练指南》、李煜东《算法竞赛进阶指南》、CCF 中学生系列；④路线：OI Wiki roadmap 分语言基础→CSP-J/S→提高→省选→NOI 递进；⑤进阶：USACO Training、IOI 历年题、Codeforces Gym 区域赛题集。

## Why · 为什么

### 直觉 · Intuition

刷题贵精不贵多，关键是「选对题目梯度」和「有反馈地训练」。平台各有分工：CF 锻炼短时限竞速与 rating 对应实力，AtCoder 题目质量高适合练思维，Luogu 覆盖国内 OI 真题方便找专题，QOJ 存国外区域赛真题适合 ICPC 备赛。教材选 1-2 本精读胜过收藏十本。

### 原理 · Principle

训练要符合「最近发展区」：难度略高于当前水平才有效。CF 按 rating 选题（rating+100~200 区间），AtCoder 按 ABC C/D、ARC B/C 分级，Luogu 按难度标签（入门~省选）与题目关联（相关题单）。知识体系遵循 OI Wiki roadmap：先基础算法（枚举/递归/分治/排序）再数据结构（栈队列树）再进阶（DP/图论/字符串/数学），最后省选以上专题（网络流/多项式/计算几何）。ICPC 备赛额外练团队：区域赛题集、多校训练（HDU Multi-University Training Contest）、Wannafly Camp。

### 历史 · History

OI Wiki 的 contest/resources 页系统罗列国内外 OJ、教程资料与书籍清单，contest/roadmap 页给出从 C++ 基础到 NOI 的完整学习路线；contest/icpc 页列出区域赛季节（网络赛 8-9 月、区域赛 9-11 月、EC/CCPC Final 12 月、WF 次年）与训练资源（QOJ、CF Gym、HDU 多校）。

## How · 实现

### 伪代码

```python
学习路线(按 OI Wiki roadmap):
  语言基础 → 枚举/模拟/递归分治/排序 → 基础数据结构 → DP → 图论 → 数学 → 字符串 → 进阶专题
刷题节奏:
  CF: 按 rating±200 选题，参加周赛看 rating 变化
  AtCoder: ABC 每场 C/D + ARC B/C
  Luogu: 按题单/难度刷，官方题解对照
ICPC 团队训练:
  区域赛真题 + CF Gym + 多校训练，定时模拟赛
教材:
  CPH(入门) / 算法竞赛进阶指南(进阶) / OI Wiki(随时查)
```

### Python 实现

```python
import sys

def build_roadmap():
    # 把 OI Wiki roadmap 的学习路线建模成阶段清单
    roadmap = [
        {"stage": "CSP-J", "topics": ["枚举", "模拟", "递归分治", "排序", "基础字符串"],
         "platforms": ["Luogu", "AtCoder ABC-A/B"]},
        {"stage": "CSP-S/NOIP", "topics": ["DP", "数据结构(栈/队列/树)", "图论基础", "数论基础"],
         "platforms": ["Luogu", "CF Div2", "AtCoder ABC-C/D"]},
        {"stage": "省选", "topics": ["进阶DP", "线段树族", "图论进阶", "字符串", "组合计数"],
         "platforms": ["Luogu 省选题单", "CF Div1", "AtCoder ARC"]},
        {"stage": "NOI/ICPC", "topics": ["网络流", "多项式", "计算几何", "可持久化/分治结构", "生成函数"],
         "platforms": ["QOJ", "CF Gym", "USACO training"]},
    ]
    for r in roadmap:
        print(f"[{r['stage']}]  {' | '.join(r['topics'])}")
        print(f"    平台: {', '.join(r['platforms'])}")
    return len(roadmap)


def main():
    n = build_roadmap()
    assert n == 4
    print("OK")


if __name__ == "__main__":
    main()

```

**PyPy 提示**: 本节点无性能代码。训练时建议在 Luogu/CF 用 Python 提交前确认该题时限对 Python 是否宽容，必要时用 PyPy 提交（见 py-pypy 节点）。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 路线规划 O(1)；刷题本身按题目规模 |
| 空间 | O(1) |

### 局限

路线是通用指南，需按个人基础与目标赛段裁剪；不同平台题目难度标注口径不一（CF rating / AtCoder 分段 / Luogu 难度不直接可比）；ICPC 团队赛还要专门练配合与分工，纯个人刷题不够。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | 题单/难度标签 | 1 | 按难度与标签找专题训练，官方/民间题单聚合同类题 | [https://www.luogu.com.cn/problem/list](https://www.luogu.com.cn/problem/list) |
| AtCoder | ABC | 1 | ABC 每周一场，A-F 难度递进，适合稳定提升基础 | [https://atcoder.jp/contests/abc](https://atcoder.jp/contests/abc) |
| QOJ | 国际赛题集 | 3 | 收集国内外 OI/ICPC 竞赛真题，适合省选/ICPC 备赛模拟 | [https://qoj.ac](https://qoj.ac) |
| CF Gym | 区域赛存档 | 3 | 历年 ICPC 区域赛/多校题，团队模拟赛素材 | [https://codeforces.com/gyms](https://codeforces.com/gyms) |

## Pitfalls · 易错点

- 收藏大量教程但从不系统性刷题，知识不成体系
- 只刷自己擅长的题，逃避弱项（如组合计数/计算几何）
- 难度跳度过大（直接上 NOI 题）挫败感强且低效
- 忽视思维训练只背模板，遇到变式题束手无策
- ICPC 备赛只个人刷题不练团队配合与分工
- 把 LeetCode 当作竞赛刷题主力（面试题风格与竞赛差异大）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/contest/resources/](https://oi-wiki.org/contest/resources/)
- OI Wiki ✓ [https://oi-wiki.org/contest/roadmap/](https://oi-wiki.org/contest/roadmap/)
- OI Wiki ✓ [https://oi-wiki.org/contest/icpc/](https://oi-wiki.org/contest/icpc/)
