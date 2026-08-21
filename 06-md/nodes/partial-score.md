---
id: partial-score
name: 骗分/部分分
group: G-E-8
stage: basic
priority: P0
depth_tier: deep
---

# 骗分/部分分

> OI 赛制按数据范围分档拿分：暴力/特殊性质部分分，namespace 分治提交

<!-- 元信息: id=partial-score · group=G-E-8 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

在 OI 赛制（一次提交、按测试点多点给分）中，正解之外按数据范围或特殊性质拿部分分的策略统称「骗分」。常见手段：①小数据暴力（n 小直接枚举/DFS）；②特殊性质点（如无环→树、权值相等→简单公式、输入小→打表）；③最朴素的正确算法（O(n^2) 换满数据的部分分）；④多个部分分版本共存时按输入特征分支（用 namespace 封装不同子任务，main 里按条件调用），一份代码拿多个子任务分。OI Wiki 以 NOI 2018 屠龙勇士的 40 分部分分代码为例展示 namespace 分治写法。

## Why · 为什么

### 直觉 · Intuition

OI 的得分是累加的：满分 100 分由若干测试点构成，正解拿 100，暴力至少拿 20-40。与其花 3 小时追一个解不出的正解，不如 30 分钟写暴力先锁 30 分，剩余时间再优化。部分分策略的本质是「把确定性能拿到的分数先拿进兜里」，这是 OI 赛制区别于 ICPC（必须全对）的核心心法。

### 原理 · Principle

每个测试点对应数据范围或特殊条件，题目数据范围通常分层（如 n<=10 暴力、n<=500 O(n^2)、n<=1e5 正解）。因此一个程序里可同时实现多个复杂度档位，运行时读入数据规模判断用哪档：namespace 隔离各档实现避免命名冲突，main 读入特征后分派。子任务分=该档数据规模对应的所有测试点分数。注意必须保证每档实现在该档数据下是正确的（含边界），否则连部分分也拿不到。

### 历史 · History

OI Wiki 的 contest/common-tricks 页以「善用 namespace」小节给出 NOI2018 屠龙勇士 40 分部分分代码（按 n==1&&m==1、p[1]==1 等条件分派 namespace::solve），并系统介绍打表、随机化、对拍等技巧，是「骗分学」的权威总结。

## How · 实现

### 伪代码

```python
namespace subtask1 {  # n<=100 暴力
  void solve() { 暴力枚举/DFS }
}
namespace subtask2 {  # 特殊性质: 无环
  void solve() { 特殊算法 }
}
namespace full { void solve() { 正解 } }
main():
  read(n)
  if n <= 100: subtask1::solve()
  elif 满足无环性质: subtask2::solve()
  else: full::solve()
```

### Python 实现

```python
import sys


def subtask_brute(n, a):
    # 暴力档：n<=1000，O(n^2) 直接算
    ans = 0
    for i in range(n):
        for j in range(i + 1, n):
            if a[i] > a[j]:
                ans += 1
    return ans


def subtask_special(n, a):
    # 特殊性质档：元素两两不同 且 只有相邻两元素会逆序（假设）
    cnt = 0
    for i in range(n - 1):
        if a[i] > a[i + 1]:
            cnt += 1
    return cnt


def full_solve(n, a):
    # 正解档：O(n log n) 归并排序数逆序对
    tmp = [0] * n

    def merge(lo, hi):
        if hi - lo <= 1:
            return 0
        mid = (lo + hi) // 2
        res = merge(lo, mid) + merge(mid, hi)
        i, j, k = lo, mid, lo
        while i < mid and j < hi:
            if a[i] <= a[j]:
                tmp[k] = a[i]; i += 1
            else:
                tmp[k] = a[j]; j += 1
                res += mid - i
            k += 1
        while i < mid:
            tmp[k] = a[i]; i += 1; k += 1
        while j < hi:
            tmp[k] = a[j]; j += 1; k += 1
        a[lo:hi] = tmp[lo:hi]
        return res

    return merge(0, n)


def main():
    # 典型部分分程序：读入规模，按档分派
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        # 无输入时自测三档结果一致（小数据验证）
        test_a = [3, 2, 1, 5, 4]
        b1 = subtask_brute(5, test_a[:])
        f1 = full_solve(5, test_a[:])
        print(f"brute={b1} full={f1}")
        assert b1 == f1
        print("OK (self-test)")
        return
    n = data[0]
    a = data[1:]
    special = all(a[i] != a[j] for i in range(n) for j in range(i + 1, n)) and n <= 200
    if n <= 1000 and not special:
        print(subtask_brute(n, a))
    elif special:
        print(subtask_special(n, a))
    else:
        print(full_solve(n, a))


if __name__ == "__main__":
    main()

```

**PyPy 提示**: OI 中部分分程序可能被用在很大的暴力数据上，O(n^2) 档建议 PyPy；多档并存时每档都要独立可跑，善用参数化读入（是否读第二行等）避免档间读入错位。namespace 在 Python 中用「函数/类 + 模块级命名」模拟即可。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 各档复杂度不同：暴力 O(n^2)、特殊性质 O(n)、正解 O(n log n)——由输入规模分派 |
| 空间 | O(n) 或按档 |

### 局限

部分分策略只在 OI/IOI 按测试点给分的赛制有效；ICPC 全对才得分，写部分分纯属浪费时间。子任务判定条件必须能从输入判断（题目需保证），且各档实现都要正确。同一测试点不会同时匹配两档，分派顺序需确定。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| NOI | 2018 屠龙勇士 | 7 | OI Wiki 引用的 40 分部分分例题：按 n/m/特判 分 namespace 分派 | [https://www.luogu.com.cn/problem/P4774](https://www.luogu.com.cn/problem/P4774) |
| CSP-S | 常见套路 | 2 | 数据范围分档：n<=20 状压/搜索、特殊性质无环/相等、大范围正解 | [https://oi-wiki.org/contest/common-tricks/](https://oi-wiki.org/contest/common-tricks/) |
| IOI | 子任务制 | 2 | IOI 赛制按子任务给分，暴力+特殊性质分档是最低保障 | [https://oi-wiki.org/contest/oi/](https://oi-wiki.org/contest/oi/) |

## Pitfalls · 易错点

- 暴力的边界处理不严谨，把暴力档的分也丢了
- 分档条件写错（如 special 判定用全量 O(n^2) 检查导致本身 TLE）
- 多档读入不一致：某档不读的部分若也被读走，后续档数据错位
- OI 赛制一次提交：未充分自测就交，浪费唯一机会
- 把部分分策略用在 ICPC（全对才得分）上浪费了时间
- 打表/暴力数据过大导致 MLE/OLE

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/contest/common-tricks/](https://oi-wiki.org/contest/common-tricks/)
- OI Wiki ✓ [https://oi-wiki.org/contest/oi/](https://oi-wiki.org/contest/oi/)
