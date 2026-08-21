---
id: construction
name: 构造题
group: G-A-1
stage: intermediate
priority: P1
depth_tier: standard
---

# 构造题

> 构造满足条件的解，需洞察问题结构

<!-- 元信息: id=construction · group=G-A-1 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

构造题（Construction）要求你构造出一个满足若干给定条件的解——可能是一个排列、一个图、一组数或一个操作序列。与「求解」类问题不同，构造题通常保证解一定存在，难点在于找到一个简洁、可证明正确、可编码实现的构造方案。构造题无通用套路，常依赖对问题结构的洞察与数学归纳。

## Why · 为什么

### 直觉 · Intuition

构造题的核心直觉是「找规律」：解往往具有某种周期、对称或递推结构。观察小规模数据（n=3,4,5）的可行构造，归纳出随 n 增长的推广规律，是破解构造题的最常用入口。

### 原理 · Principle

常见构造范式：(1) 归纳构造——小规模有解则按固定增量扩展到大 n；(2) 数论构造——利用互素/逆元/前缀和的模性质构造排列（如 CF 743C 的 1/x+1/y+1/z=2/n 用 n,n+1,n(n+1)）；(3) 对称/配对构造——图论中前后配对使各点度数和相等；(4) 自由变量法——题面自由度越高越容易找到简单构造。关键要求是构造必须带证明，不能只靠猜测。

### 历史 · History

构造题是各大竞赛的常客，Codeforces 的构造专场、AtCoder Grand Contest 的构造题、NOI 系列比赛的构造题屡见不鲜。OI Wiki 专门开设构造专题，强调其「高自由度、形式灵活、无通用解法」三大特点，并指出解题要思考问题规模增长对答案的影响。

## How · 实现

### 伪代码

```python
construct(n):
  # 找出规律（观察小规模解）
  if pattern_found(n):
    return build_by_pattern(n)
  else:
    return build_by_induction(n)  # 归纳扩展示例
  # 最后必须验证构造满足所有条件
```

### Python 实现

```python
def cf743c(n):
    """CF 743C Vladik and fractions: 构造 x,y,z 使 1/x+1/y+1/z = 2/n。
    经典构造: x=n, y=n+1, z=n*(n+1)。
    因为 1/n + 1/(n+1) + 1/(n*(n+1)) = (n+1+n+1)/(n*(n+1)) = 2(n+1)/(n(n+1)) = 2/n。
    注意 n=1 时无解（此时 y==z）。
    """
    if n == 1:
        return None
    return (n, n + 1, n * (n + 1))


def construct_prefix_sum_perm(n):
    """OI Wiki 例题（P3599 Task1 思路）:
    构造 1..n 的排列，使 n 个前缀和在模 n 意义下互不相同（n 为偶数时可行）。
    采用前缀和序列 0,1,-1,2,-2,... 反推排列。
    返回原排列（1-indexed 值）。
    """
    if n % 2 == 1:
        return None
    # 前缀和序列（模 n）: 0, 1, n-1, 2, n-2, ...
    pref = [0]
    for k in range(1, n // 2 + 1):
        pref.append(k)
        if n - k > 0:
            pref.append(n - k)
    pref = pref[:n]
    arr = [(pref[i + 1] - pref[i]) % n for i in range(n - 1)]
    arr.insert(0, n)  # 第一位固定为 n
    return arr


def verify_pref_perm(arr, n):
    """验证: 前 n 个前缀和模 n 互不相同, 且 arr 是 1..n 的排列"""
    assert sorted(arr) == list(range(1, n + 1)), "not a permutation"
    s, seen = 0, set()
    for x in arr:
        s = (s + x) % n
        seen.add(s)
    assert len(seen) == n, f"prefix sums not distinct: {len(seen)}"


if __name__ == "__main__":
    assert cf743c(2) == (2, 3, 6)
    assert cf743c(1) is None
    # 验证 1/2+1/3+1/6 == 2/2 == 1
    import fractions as fr
    assert fr.Fraction(1, 2) + fr.Fraction(1, 3) + fr.Fraction(1, 6) == 1

    for n in [4, 6, 8]:
        arr = construct_prefix_sum_perm(n)
        verify_pref_perm(arr, n)
    assert construct_prefix_sum_perm(5) is None

    print("All tests passed.")
```

**PyPy 提示**: 构造题的代码通常很短，PyPy/CPython 无差异。重点在于正确性证明与边界（如 n=1、n=4 等特例），写完后应自造小数据逐一验证所有条件。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 构造本身通常 O(n) 或 O(n log n)，与验证解需遍历解空间一致 |
| 空间 | O(n) — 存放构造出的解 |

### 局限

构造题无统一算法，必须具体问题具体分析；构造方案若未经证明，存在隐藏反例风险。当构造空间极小时需特别注意无解判定（如 CF 743C 的 n=1）。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Codeforces | 743C | 1600 | Vladik and fractions：数论型构造 1/x+1/y+1/z=2/n，标准答案 n,n+1,n(n+1)，n=1 无解 | [https://codeforces.com/problemset/problem/743/C](https://codeforces.com/problemset/problem/743/C) |
| Luogu | P3599 | 7 | Koishi Loves Construction：前缀和/前缀积模 n 互异的排列构造，OI Wiki 官方例题 | [https://www.luogu.com.cn/problem/P3599](https://www.luogu.com.cn/problem/P3599) |
| AtCoder | AGC032B | 1200 | Balanced Neighbors：构造使每个点邻点编号和相等的图，前后配对（对称构造） | [https://atcoder.jp/contests/agc032/tasks/agc032_b](https://atcoder.jp/contests/agc032/tasks/agc032_b) |

## Pitfalls · 易错点

- 构造方案缺乏证明，被隐藏样例/反例卡住——务必先证明再写码
- 忽略无解判定（如 n=1 时 y==z 非法）
- 归纳构造未处理规模跳变时的特例（如奇偶、合数/质数分界）
- 小规模观察规律后未验证推广到大 n 时是否仍成立

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/basic/construction/](https://oi-wiki.org/basic/construction/)
- Codeforces ✓ [https://codeforces.com/problemset/problem/743/C](https://codeforces.com/problemset/problem/743/C)
- AtCoder ✓ [https://atcoder.jp/contests/agc032/tasks/agc032_b](https://atcoder.jp/contests/agc032/tasks/agc032_b)
