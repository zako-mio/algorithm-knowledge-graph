---
id: z-function
name: Z函数
group: G-C-1
stage: intermediate
priority: P1
depth_tier: standard
---

# Z函数

> Z数组 z[i]=LCP(S, S[i..])，线性构造O(n)，用于匹配与周期判断

<!-- 元信息: id=z-function · group=G-C-1 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

Z 函数(扩展 KMP)：对字符串 s，z[i] = s 与后缀 s[i..n−1] 的最长公共前缀(LCP)长度，规定 z[0]=0。线性算法维护最右的 Z-box [l,r]，当 i≤r 时 z[i]=min(z[i−l], r−i+1) 可直接继承，否则暴力扩展。匹配文本 t 中模式 p：构造 p+'#'+t 求 Z，z[i+|p|+1]==|p| 即出现。Z 函数与 KMP 前缀函数本质互通(互为镜像)，但 Z 的直观是『与自身前缀匹配』，适合周期判断、整周期、本质不同子串增量计数等。

## Why · 为什么

### 直觉 · Intuition

若已知某个后缀区间 [l,r] 与整个字符串前缀完全相等，那对 i∈[l,r] 位置，s[i..] 与 s 的 LCP 至少等于 s[i−l..] 与 s 的 LCP 截断在 r−i+1 处——因为两段字符都在同一个『与前缀相同』的盒子 [l,r] 里。所以只需维护最靠右的盒子，多数 z[i] 可以 O(1) 复制，只有越界/超盒时暴力扩展，而每次扩展都会把 r 右移，总扩展 O(n)。

### 原理 · Principle

维护 [l,r] 使 s[l..r]=s[0..r−l](Z-box)。计算 z[i]：① i≤r 且 z[i−l]<r−i+1 → z[i]=z[i−l]；② 否则 z[i]=max(0,r−i+1) 后暴力 while 扩展 s[i+z[i]]==s[z[i]]；③ 若 i+z[i]−1>r 更新 l,r。线性性：暴力 while 每轮必使 r 增加≥1，总 O(n)。匹配应用与 KMP 的拼接法完全对称。

### 历史 · History

Z 算法最早由 Dan Gusfield 在其 1997 年著作《Algorithms on Strings, Trees, and Sequences》中系统介绍，因此常称 Z Algorithm；国内因与 KMP 功能相近称『扩展 KMP』。它本质上与 Morris–Pratt 前缀函数是同一数学结构的两种视角。

## How · 实现

### 伪代码

```python
function z_function(s):
  n=len(s); z=[0]*n; l=r=0
  for i in 1..n-1:
    if i<=r and z[i-l] < r-i+1:
      z[i] = z[i-l]
    else:
      z[i] = max(0, r-i+1)
      while i+z[i]<n and s[z[i]]==s[i+z[i]]: z[i]+=1
    if i+z[i]-1 > r: l=i; r=i+z[i]-1
  return z

function z_match(t, p):
  s = p + '#' + t; z = z_function(s)
  for i in |p|+1 .. |s|-1:
    if z[i]==|p|: record i-|p|-1
```

### Python 实现

```python
def z_function(s):
    """Z 函数: z[i] = LCP(s, s[i:]), z[0]=0, O(n)"""
    n = len(s)
    z = [0] * n
    l = r = 0
    for i in range(1, n):
        if i <= r and z[i - l] < r - i + 1:
            z[i] = z[i - l]
        else:
            z[i] = max(0, r - i + 1)
            while i + z[i] < n and s[z[i]] == s[i + z[i]]:
                z[i] += 1
        if i + z[i] - 1 > r:
            l, r = i, i + z[i] - 1
    return z


def z_match(text, pattern):
    """Z 算法匹配: pattern 在 text 中所有出现位置"""
    if not pattern:
        return list(range(len(text) + 1))
    s = pattern + '#' + text
    z = z_function(s)
    n = len(pattern)
    return [i - n - 1 for i in range(n + 1, len(s)) if z[i] == n]


def min_period_z(s):
    """Z 函数求最小整周期"""
    n = len(s)
    z = z_function(s)
    for i in range(1, n):
        if n % i == 0 and i + z[i] == n:
            return i
    return n


if __name__ == "__main__":
    assert z_function('aaaaa') == [0, 4, 3, 2, 1]
    assert z_function('aaabaab') == [0, 2, 1, 0, 2, 1, 0]
    assert z_function('abacaba') == [0, 0, 1, 0, 3, 0, 1]
    assert z_match('ababaab', 'aba') == [0, 2]
    assert z_match('aaaa', 'aa') == [0, 1, 2]
    assert min_period_z('abcabcabc') == 3
    assert min_period_z('abab') == 2
    assert min_period_z('abcd') == 4
    print("zfunc OK")

```

**PyPy 提示**: z_function 的 while 扩展总次数 O(n)，PyPy 下 n=1e6 约 0.3s。z 数组与 pi 数组可互相转换(镜像关系)，选一种记熟即可。整周期判断条件：i 从 1 开始找 n%i==0 且 i+z[i]==n 的最小 i；若用 KMP 视角则是 n−pi[n−1] 整除 n。注意 z[0] 约定为 0(有些资料令 z[0]=n，需看上下文)。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n) 构造；匹配 O(n+m) |
| 空间 | O(n+m) |

### 局限

1) 与 KMP 功能高度重叠，取一即可，但 Z 求『整周期』和『本质不同子串增量』更直接；2) 需哨兵 '#' 保证不越界到模式串内；3) 只处理单模式匹配；4) 内存 O(n+m) 拼接串，超大文本可用分段处理，但竞赛通常可接受。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P5410 | 3 | 【模板】扩展 KMP/exKMP(Z 函数)：标准 Z 函数模板题 | [https://www.luogu.com.cn/problem/P5410](https://www.luogu.com.cn/problem/P5410) |
| Codeforces | 126B | 3 | Password：Z/前缀函数求最长前缀后缀且出现中间的子串 | [https://codeforces.com/problemset/problem/126/B](https://codeforces.com/problemset/problem/126/B) |
| LeetCode | 2223 | 4 | Sum of Scores of Built Strings：Z 数组求和，Z 函数直接应用 | [https://leetcode.cn/problems/sum-of-scores-of-built-strings/](https://leetcode.cn/problems/sum-of-scores-of-built-strings/) |

## Pitfalls · 易错点

- z[0] 约定混乱(0 vs n)，必须统一
- z_box 更新条件 i+z[i]−1>r 写成 >= 导致少更新
- 继承分支 i<=r 但 z[i−l]≥r−i+1 时落入 else 暴力扩展，忘记 max(0,r−i+1) 初始化
- 匹配映射下标 i−n−1 与 KMP 的 i−2n 混淆
- 对空 pattern 特殊处理遗漏

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/string/z-func/](https://oi-wiki.org/string/z-func/)
- CP-Algorithms ✓ [https://cp-algorithms.com/string/z-function.html](https://cp-algorithms.com/string/z-function.html)
