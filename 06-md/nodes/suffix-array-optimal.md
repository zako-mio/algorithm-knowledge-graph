---
id: suffix-array-optimal
name: 最优原地后缀数组
group: G-C-3
stage: frontier
priority: P3
depth_tier: brief
---

# 最优原地后缀数组

> 线性时间O(n)且O(1)额外空间构造后缀数组的变体(SA-IS等)

<!-- 元信息: id=suffix-array-optimal · group=G-C-3 · stage=frontier · priority=P3 · depth_tier=brief -->

## What · 是什么

最优原地后缀数组（Optimal In-Place Suffix Sorting）指在 O(n) 时间、O(1) 额外空间内构造后缀数组的一类算法，代表有 SA-IS（Nong–Zhang–Chan 2009）与 DC3（Kärkkäinen–Sanders 2003）。SA-IS 是诱导排序（induce sort）型线性算法：先给每个位置标记 S 型/L 型（相对下一字符大小），找出 LMS 子串，递归排序 LMS 子串，再两次诱导（对 L 型与 S 型桶进行诱导排序）得到完整 SA。O(1) 空间版本通过原地重命名原串代替 S/L 桶、用 SA 数组自身做桶与计数器实现（OI-Wiki sa-optimal-inplace 条目）。通常竞赛只需 O(n log n) 倍增，O(n) 构造仅在时限极紧或刻意追求时使用。

## Why · 为什么

### 直觉 · Intuition

SA-IS 的直觉：字符的相对类型（S/L）携带了大量信息——L 型后缀（下一个字符更小）整体字典序小于同首字符的 S 型后缀；若知道所有 LMS 子串的顺序，就能'诱导'出所有后缀的完整顺序。诱导排序就像撒种子再传播：把已排序的 LMS 放入对应桶尾/桶头，然后从桶尾向左扫（诱导 L 型）、从桶头向右扫（诱导 S 型），每个桶按顺序被填满。原地化则利用'桶就是 SA 数组本身'，用符号位/计数器就地管理空位，省去额外数组。

### 原理 · Principle

正确性：对任意后缀 i，其排名可由'它属于某个已排序的 LMS 前缀区间'诱导得出——L 型后缀严格排在同首字符的 S 型后缀之前，且按首字符分桶后，每桶内 L 型从左到右、S 型从右到左依次诱导填充，因为相邻字符串的比较在桶内可由位置 i+1 的排名决定。递归：LMS 子串的字典序排序等价于对 LMS 位置构成的'缩小串'递归做 SA-IS，故整体 T(n)=T(|LMS|)+O(n)=O(n)。原地 O(1) 空间：用重命名后的串值存桶头/桶尾索引，用 SA 的负值/特殊符号存 UNIQUE/MULTIPLE 标记与内部计数器，避免额外数组。

### 历史 · History

DC3 由 Kärkkäinen 与 Sanders 于 2003 年提出；SA-IS 由 Nong、Zhang 与 Chan 于 2009 年提出，成为应用最广的线性 SA 构造。O(1) 额外空间的原地后缀排序由 Franceschini–Muthukrishnan（2007）理论奠基，OI-Wiki 的 sa-optimal-inplace 条目整理了基于 SA-IS 的原地实现，属于'前沿/进阶'专题。

## How · 实现

### 伪代码

```python
# SA-IS 概要 (O(n) 时间, O(n) 空间版本)
1. 分类: 对 i 标记 type[i] = S 或 L (S[i]>S[i+1] 为 L 型)
2. 找出所有 LMS 位置 (L 后面紧跟 S)
3. 递归: 对 LMS 子串序列构造'缩小串', 递归求其 SA
4. 用缩小串的 SA 得 LMS 的排序
5. 诱导排序:
   - 将 LMS 放入对应字符桶的桶尾 (从大到小)
   - 从左到右扫 SA, 对每个 L 型位置诱导其后继
   - 从右到左扫 SA, 对每个 S 型位置诱导其后继
6. 得到完整 SA
# 原地版: 用重命名串代替桶, SA 数组内做标记与计数器
```

### Python 实现

```python
def sa_is(s, upper):
    """SA-IS 线性后缀数组 (ACL 移植, 教学注释版).
    s: 整数列表 (值域 [0, upper]), 无哨兵; 返回 0-index sa.
    """
    n = len(s)
    if n == 0:
        return []
    if n == 1:
        return [0]
    if n == 2:
        return [0, 1] if s[0] < s[1] else [1, 0]
    sa = [0] * n
    ls = [0] * n
    for i in range(n - 2, -1, -1):
        ls[i] = ls[i + 1] if s[i] == s[i + 1] else (s[i] < s[i + 1])
    sum_l = [0] * (upper + 1)
    sum_s = [0] * (upper + 1)
    for i in range(n):
        if not ls[i]:
            sum_s[s[i]] += 1
        else:
            sum_l[s[i] + 1] += 1
    for i in range(upper + 1):
        sum_s[i] += sum_l[i]
        if i < upper:
            sum_l[i + 1] += sum_s[i]

    def induce(lms):
        for i in range(n):
            sa[i] = -1
        buf = sum_s[:]
        for d in lms:
            if d == n:
                continue
            sa[buf[s[d]]] = d
            buf[s[d]] += 1
        buf = sum_l[:]
        sa[buf[s[n - 1]]] = n - 1
        buf[s[n - 1]] += 1
        for i in range(n):
            v = sa[i]
            if v >= 1 and not ls[v - 1]:
                sa[buf[s[v - 1]]] = v - 1
                buf[s[v - 1]] += 1
        buf = sum_l[:]
        for i in range(n - 1, -1, -1):
            v = sa[i]
            if v >= 1 and ls[v - 1]:
                buf[s[v - 1] + 1] -= 1
                sa[buf[s[v - 1] + 1]] = v - 1

    lms_map = [-1] * (n + 1)
    m = 0
    for i in range(1, n):
        if not ls[i - 1] and ls[i]:
            lms_map[i] = m
            m += 1
    lms = []
    for i in range(1, n):
        if not ls[i - 1] and ls[i]:
            lms.append(i)
    induce(lms)
    if m:
        sorted_lms = []
        for v in sa:
            if lms_map[v] != -1:
                sorted_lms.append(v)
        rec_s = [0] * m
        rec_upper = 0
        rec_s[lms_map[sorted_lms[0]]] = 0
        for i in range(1, m):
            l = sorted_lms[i - 1]
            r = sorted_lms[i]
            end_l = lms[lms_map[l] + 1] if lms_map[l] + 1 < m else n
            end_r = lms[lms_map[r] + 1] if lms_map[r] + 1 < m else n
            same = True
            if end_l - l != end_r - r:
                same = False
            else:
                while l < end_l:
                    if s[l] != s[r]:
                        break
                    l += 1
                    r += 1
                if l == n or s[l] != s[r]:
                    same = False
            if not same:
                rec_upper += 1
            rec_s[lms_map[sorted_lms[i]]] = rec_upper
        rec_sa = sa_is(rec_s, rec_upper)
        for i in range(m):
            sorted_lms[i] = lms[rec_sa[i]]
        induce(sorted_lms)
    return sa


def build_sa_sais(text):
    """对字符串 text 构造后缀数组 (字符映射到整数, 无哨兵)."""
    if not text:
        return []
    vals = [ord(c) - 96 for c in text]
    return sa_is(vals, max(26, max(vals)))


if __name__ == "__main__":
    def naive_sa(t):
        return sorted(range(len(t)), key=lambda i: t[i:])

    for t in ["ababa", "banana", "mississippi", "a", "aaaa", "abcabc",
              "adbdabddbcbbdcadabcac", "dbccddadbddbccadabdcdadacdbbb"]:
        sa = build_sa_sais(t)
        assert sa == naive_sa(t), (t, sa, naive_sa(t))

    import random
    random.seed(1)
    for _ in range(500):
        n = random.randrange(1, 30)
        t = ''.join(random.choice('abcd') for _ in range(n))
        sa = build_sa_sais(t)
        assert sa == naive_sa(t), (t, sa, naive_sa(t))

    print("suffix-array-optimal (SA-IS) tests passed")

```

**PyPy 提示**: SA-IS 递归实现细节极多（LMS 子串比较、递归串规约、诱导桶边界），Python 写法常数大；原地 O(1) 空间版实现极其复杂，竞赛中几乎不写，仅作理论了解。实际需要 O(n) 构造时用 C++ 模板。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n)（含递归，T(n)=T(n/2)+O(n)）；原地版同样 O(n) 时间 O(1) 额外空间 |
| 空间 | 非原地 O(n)；原地版 O(1) 额外空间（SA 数组本身即工作区） |

### 局限

实现复杂度极高、易错；递归深度与桶/哨兵边界细节多；Python 下常数大，通常不如优化过的 O(n log n) 倍增；原地 O(1) 版本仅适合研究与极限优化场景。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3809 | 3 | 后缀排序模板：倍增可过，O(n) 构造用于极限优化对比 | [https://www.luogu.com.cn/problem/P3809](https://www.luogu.com.cn/problem/P3809) |

## Pitfalls · 易错点

- L/S 类型定义方向（S[i]<S[i+1] 为 S 型）不要搞反
- 哨兵必须是全局最小且唯一，递归子问题同样需要
- LMS 子串比较须考虑 LMS 边界（到下一个 LMS 即停）
- 诱导顺序：先 L 后 S，且桶方向（L 从左、S 从右）不能错
- 原地版符号位/计数器管理极易越界，务必逐字节对拍

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/string/sa-optimal-inplace/](https://oi-wiki.org/string/sa-optimal-inplace/)
- OI Wiki ✓ [https://oi-wiki.org/string/sa/](https://oi-wiki.org/string/sa/)
