---
id: main-lorentz
name: Main-Lorentz（重串查找）
group: G-C-6
stage: frontier
priority: P3
depth_tier: brief
---

# Main-Lorentz（重串查找）

> 分治 + Z 函数找出字符串所有平方串（重串）的压缩表示，O(n log n)，用于周期结构统计

<!-- 元信息: id=main-lorentz · group=G-C-6 · stage=frontier · priority=P3 · depth_tier=brief -->

## What · 是什么

重串（repetition/tandem repeat）：形如 xx（两个相同串相连）的子串，用一对下标 (i,j) 表示 s[i..j]=两个相同字符串。问题：找出 s 的所有重串（或最长/任意一个）。重串总数可达 O(n²)（如全 'a' 串），但可用 Crochemore 三元组 (i,p,r) 压缩表示（i 起点，p 循环节长度，r 循环次数）或本原重串（原串本身不是重串）表达，数量 O(n log n)。Main–Lorentz 算法（1982）核心是分治：把串分为左右两半 u、v，递归处理左右两半内的重串，再计算跨越中点的'交叉重串'。找交叉重串：固定中间字符位置 cntr（左偏/右偏），用 Z 函数 O(1) 求 k1（向左匹配长度）、k2（向右匹配长度），满足 l1≤k1, l2≤k2 的 (l1,l2) 组合对应恰好一个重串，用四元组 (cntr,l,k1,k2) 输出。复杂度由主定理 O(n log n)。

## Why · 为什么

### 直觉 · Intuition

分治时，跨中点的重串中点恰好落在分割线上：若重串是 xx，其'中间'（x 与 x 的交界）附近必跨过中点。对固定 cntr（重串右半首字符在左半/右半的位置），左半向左延伸与右半向右延伸的匹配长度 k1、k2 决定所有可能的重串长度组合。Z 函数能 O(1) 给出某个边界内最长的匹配长度。

### 原理 · Principle

设 s=u+v，|u|≈|v|。对左偏重串：重串中点字符（右半第一个字符）在 u 中，固定 cntr∈[0,|u|)，重串长 2l=2(|u|−cntr)。计算 k1=max k 使 u[cntr−k..cntr−1]=u[|u|−k..|u|−1]（用 reversed(u) 的 Z），k2=max k 使 u[cntr..cntr+k−1]=v[0..k−1]（用 v+'#'+u 的 Z）。则满足 l1≤k1、l2≤k2、l1+l2=l 的每对 (l1,l2) 给出一个重串。右偏重串对称处理。所有 (cntr,l,k1,k2) 组合即压缩表示；若需展开全部 (i,j) 则可能 O(n²)（算法本身给出压缩形式）。复杂度 T(n)=2T(n/2)+O(n)=O(n log n)。

### 历史 · History

Main–Lorentz 算法由 Michael Main 与 Richard J. Lorentz 于 1982 年发表（查找所有重串），是字符串周期/重复结构研究（repetitions，Kolpakov–Kucherov 证明本原重串数 O(n log n)）的算法竞赛化版本。OI Wiki 与 CP-Algorithms 均有'Finding repetitions'专页（源自 e-maxx 俄文翻译）。Fibonacci 串可达到 O(n log n) 个三元组的下界。

## How · 实现

### 伪代码

```python
# Main-Lorentz 分治
find_repetitions(s, shift):
    if |s|==1: return
    nu = |s|//2; nv = |s|-nu
    u = s[:nu]; v = s[nu:]
    find_repetitions(u, shift)
    find_repetitions(v, shift+nu)
    z1 = z(reversed(u)); z2 = z(v+'#'+u)
    z3 = z(reversed(u)+'#'+reversed(v)); z4 = z(v)
    for cntr in 0..|s|-1:
        if cntr < nu:  # 左偏
            l = nu - cntr; k1 = z1[nu-cntr]; k2 = z2[nv+1+cntr]
        else:          # 右偏
            l = cntr-nu+1; k1 = z3[nu+1+nv-1-(cntr-nu)]; k2 = z4[(cntr-nu)+1]
        if k1+k2 >= l:
            for l1 in max(1,l-k2)..min(l,k1):
                (若左偏且 l1==l: break)
                l2 = l-l1
                pos = shift + (左偏? cntr-l1 : cntr-l-l1+1)
                记录重串 (pos, pos+2l-1)
```

### Python 实现

```python
# -*- coding: utf-8 -*-
# Main-Lorentz：O(n log n) 求所有重串的压缩四元组，并展开为 (起点,终点)

def z_function(s):
    n = len(s)
    z = [0] * n
    l = r = 0
    for i in range(1, n):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] - 1 > r:
            l, r = i, i + z[i] - 1
    return z


def get_z(z, i):
    return z[i] if 0 <= i < len(z) else 0


def find_repetitions(s, shift=0, out=None):
    """把所有重串 (start, end) 加入 out（压缩表示：对每个 cntr 枚举 l1）。"""
    if out is None:
        out = []
    n = len(s)
    if n == 1:
        return out
    nu = n // 2
    nv = n - nu
    u, v = s[:nu], s[nu:]
    ru, rv = u[::-1], v[::-1]
    find_repetitions(u, shift, out)
    find_repetitions(v, shift + nu, out)
    z1 = z_function(ru)
    z2 = z_function(v + '#' + u)
    z3 = z_function(ru + '#' + rv)
    z4 = z_function(v)
    for cntr in range(n):
        if cntr < nu:
            l = nu - cntr
            k1 = get_z(z1, nu - cntr)
            k2 = get_z(z2, nv + 1 + cntr)
        else:
            l = cntr - nu + 1
            k1 = get_z(z3, nu + 1 + nv - 1 - (cntr - nu))
            k2 = get_z(z4, (cntr - nu) + 1)
        if k1 + k2 >= l:
            for l1 in range(max(1, l - k2), min(l, k1) + 1):
                if cntr < nu and l1 == l:
                    break
                l2 = l - l1
                pos = shift + (cntr - l1 if cntr < nu else cntr - l - l1 + 1)
                out.append((pos, pos + 2 * l - 1))
    return out


def brute_reps(s):
    """暴力：所有偶数长子串 s[i:i+len] = x+x。"""
    n = len(s)
    res = set()
    for length in range(2, n + 1, 2):
        half = length // 2
        for i in range(n - length + 1):
            if s[i:i + half] == s[i + half:i + length]:
                res.add((i, i + length - 1))
    return res


if __name__ == '__main__':
    for s in ['acababaee', 'abaaba', 'aaaaaa', 'abcabcabc', 'abababab', 'aabbaabb']:
        got = set(find_repetitions(s))
        exp = brute_reps(s)
        assert got == exp, (s, got, exp)
    import random
    random.seed(3)
    for _ in range(150):
        n = random.randint(1, 22)
        s = ''.join(random.choice('ab') for _ in range(n))
        got = set(find_repetitions(s))
        exp = brute_reps(s)
        assert got == exp, (s, got, exp)
    print('main-lorentz tests passed')

```

**PyPy 提示**: Z 函数 4 次 + 分治递归，Python 实现 O(n log n) 适合中等规模（≤1e5）；大 n 建议 C++。递归深度 log n 无栈问题。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n log n)（主定理）；展开全部 (i,j) 最坏 O(n²) |
| 空间 | O(n) |

### 局限

算法输出压缩表示（cntr,l,k1,k2），展开全部重串位置会退化到 O(n²)。需预先掌握 Z 函数。仅适用于等长重复（重串），非等周期结构需其他工具。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Codeforces | 963-D | 6 | Frequency of String：重串/周期结构应用（Main-Lorentz 变体），难度较高 | [https://codeforces.com/problemset/problem/963/D](https://codeforces.com/problemset/problem/963/D) |
| Luogu | P5044 | 7 | IOI2018 meeting 相关后缀结构题，涉及周期；仅作难度参考 | [https://www.luogu.com.cn/problem/P5044](https://www.luogu.com.cn/problem/P5044) |

## Pitfalls · 易错点

- Z 函数下标与切片偏移极易错（nu/nv/cntr 组合），务必与暴力对拍
- 左偏与右偏的 l、k1、k2 公式不同，不能混用
- l1 枚举边界 max(1,l-k2)..min(l,k1)，左偏时 l1==l 要 break 避免空 l2
- 输出位置 pos 要加 shift（分治偏移）
- 重串总个数可能 O(n²)，需要压缩表示或只求最长/计数

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/string/main-lorentz/](https://oi-wiki.org/string/main-lorentz/)
- CP-Algorithms ✓ [https://cp-algorithms.com/string/main_lorentz.html](https://cp-algorithms.com/string/main_lorentz.html)
