---
id: manacher
name: Manacher 算法（O(n) 最长回文子串）
group: G-C-5
stage: intermediate
priority: P1
depth_tier: deep
---

# Manacher 算法（O(n) 最长回文子串）

> 利用回文的对称性维护『最右回文串』边界，O(n) 求出所有奇/偶长度回文半径数组 d1/d2，进而得到最长回文子串，是最重要的回文串线性算法。

<!-- 元信息: id=manacher · group=G-C-5 · stage=intermediate · priority=P1 · depth_tier=deep -->

## What · 是什么

Manacher 算法以每个位置 i 为中心，计算两个回文半径数组：d1[i] 表示以 i 为中心（字符中心）的最长奇数回文串半径，d2[i] 表示以 i 与 i+1 之间的『空』为中心的最长偶数回文串半径。利用已计算的回文串对称性，把每个新中心的初始半径『借用』自其镜像位置，再朴素扩展，总复杂度 O(n)。据此可求最长回文子串、统计回文子串个数、判断任意子串是否回文（需配合前缀后缀处理），也可经插入分隔符 '#' 把奇偶情况统一为只算 d1。

## Why · 为什么

### 直觉 · Intuition

朴素算法对每个中心 O(n) 扩展，总 O(n²)，浪费在于重复比较。Manacher 的洞察：若已知 [l,r] 是一个大回文串，那么其内部关于中心对称的位置互为镜像，i 的回文信息可『继承』镜像 j 的答案。唯一的困难是镜像回文可能超出大回文串边界，此时截断到边界再继续扩展。每次扩展失败都以 r 增大为代价，而 r 单调不减，故总扩展次数 O(n)。

### 原理 · Principle

维护当前最靠右的回文串边界 [l,r]（r 最大者）。对每个 i：① 若 i>r，朴素扩展，k 从 1（奇数）或 0（偶数）开始；② 若 i≤r，令镜像 j=l+(r-i)，初值 k=min(d[j], r-i+1)（奇）或 min(d2[l+r-i+1], r-i+1)（偶）——取 min 是为防止继承值超出 [l,r] 的可信范围；③ 在初值基础上继续朴素扩展；④ 更新 [l,r] 若扩展越过了 r。复杂度证明：每次朴素扩展的一步都使 r 增 1，而 r 从 0 单调增到 n，故朴素扩展总步数 O(n)，其余 O(1)。

### 历史 · History

算法由 Glenn K. Manacher 于 1975 年提出，是回文串处理的经典线性算法。CP-Algorithms 的《Finding all sub-palindromes in O(N)》与 OI Wiki 的中文版是权威教程；其『维护最右边界并镜像借用』的思想与 Z 函数（Z-algorithm）高度相似。常与字符串哈希、后缀数组的回文处理对比。

## How · 实现

### 伪代码

```python
# 奇数回文半径 d1
for i, l, r := 0, 0, -1; i < n; i++:
    k = 1 if i > r else min(d1[l + r - i], r - i + 1)
    while 0 <= i - k and i + k < n and s[i-k] == s[i+k]: k++
    d1[i] = k; k--
    if i + k > r: l, r = i - k, i + k

# 偶数回文半径 d2
for i, l, r := 0, 0, -1; i < n; i++:
    k = 0 if i > r else min(d2[l + r - i + 1], r - i + 1)
    while 0 <= i - k - 1 and i + k < n and s[i-k-1] == s[i+k]: k++
    d2[i] = k; k--
    if i + k > r: l, r = i - k - 1, i + k
```

### Python 实现

```python
def manacher_odd(s):
    n = len(s)
    d1 = [0] * n
    l, r = 0, -1
    for i in range(n):
        k = 1 if i > r else min(d1[l + r - i], r - i + 1)
        while i - k >= 0 and i + k < n and s[i - k] == s[i + k]:
            k += 1
        d1[i] = k
        k -= 1
        if i + k > r:
            l, r = i - k, i + k
    return d1

def manacher_even(s):
    n = len(s)
    d2 = [0] * n
    l, r = 0, -1
    for i in range(n):
        k = 0 if i > r else min(d2[l + r - i + 1], r - i + 1)
        while i - k - 1 >= 0 and i + k < n and s[i - k - 1] == s[i + k]:
            k += 1
        d2[i] = k
        k -= 1
        if i + k > r:
            l, r = i - k - 1, i + k
    return d2

def longest_palindrome(s):
    d1 = manacher_odd(s)
    d2 = manacher_even(s)
    best, pos, kind = 0, 0, 0
    for i, d in enumerate(d1):
        if 2 * d - 1 > best:
            best, pos, kind = 2 * d - 1, i, 1
    for i, d in enumerate(d2):
        if 2 * d > best:
            best, pos, kind = 2 * d, i, 2
    if kind == 1:
        return s[pos - d1[pos] + 1: pos + d1[pos]]
    return s[pos - d2[pos]: pos + d2[pos]]

def count_palindromes(s):
    return sum(d for d in manacher_odd(s)) + sum(d for d in manacher_even(s))

if __name__ == '__main__':
    cases = [
        ('abcba', 'abcba', 5),
        ('abacaba', 'abacaba', 7),
        ('abaxyzzyxf', 'xyzzyx', 6),
        ('forgeeksskeegfor', 'geeksskeeg', 10),
        ('abb', 'bb', 2),
    ]
    for s, exp, exp_len in cases:
        got = longest_palindrome(s)
        assert got == exp and len(got) == exp_len, (s, got, exp)
        print('%r -> %r (len %d)' % (s, got, len(got)))
    # 回文子串总数：s='aaa' => 6 (a,a,a,aa,aa,aaa)
    assert count_palindromes('aaa') == 6
    assert count_palindromes('abccba') == 9
    print('count OK')
    print('OK')
```

**PyPy 提示**: 双 while 循环在 PyPy 下效率高，n≤1e6 可在 ~1s 内完成；注意用局部变量缓存 s/d1 加速索引。字符串切片仅用于输出最长回文，勿在循环内频繁切片。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n)（每次朴素扩展使 r 增 1，总 O(n)） |
| 空间 | O(n)（两个半径数组，或统一分隔符法一个数组 O(n)） |

### 局限

d1/d2 的含义是『半径内字符数』而非『半径下标差』，容易混淆；统一分隔符法构造 2n+1 的新串，多一倍空间但实现统一；Manacher 只能回答『所有回文子串』这类与半径相关的问题，对『字典序第 k 大回文子串』等需结合后缀结构（后缀自动机/回文树）。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3805 | 3 | 【模板】Manacher：求最长回文子串长度，直接套 d1/d2 | [https://www.luogu.com.cn/problem/P3805](https://www.luogu.com.cn/problem/P3805) |
| Luogu | P4555 | 5 | [国家集训队] 最长双回文串：两个回文串拼起来最长，预处理每个位置左右最大回文半径 | [https://www.luogu.com.cn/problem/P4555](https://www.luogu.com.cn/problem/P4555) |
| UVa | 11475 Extend to Palindrome | 3 | 求最小补充使原串变回文：找最长后缀回文，Manacher 直接应用 | [https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=2470](https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=2470) |
| Codeforces | 1326D2 Labyrinth | 4 | 字符串前缀+后缀拼最长回文，Manacher 求中间段回文 | [https://codeforces.com/contest/1326/problem/D2](https://codeforces.com/contest/1326/problem/D2) |

## Pitfalls · 易错点

- d1/d2 半径定义：d1[i] 含中心字符，d2[i] 为配对字符数，算长度时 d1 用 2*d-1、d2 用 2*d
- 镜像下标：奇数用 l+r-i，偶数用 l+r-i+1，下标公式错则结果全错
- 初值截断用 r-i+1（奇/偶同）而不是 r-i，边界差 1 导致继承溢出
- 更新 [l,r] 的时机：i+k>r 才更新，且 l/r 赋值须用 k-1 后的位置
- 统一分隔符法记得处理分隔符与真实字符索引换算，答案要去掉 '#' 影响

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/string/manacher.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/string/manacher.md)
- CP-Algorithms ✓ [https://cp-algorithms.com/string/manacher.html](https://cp-algorithms.com/string/manacher.html)
- 书籍 ✓ `CPH ch26 String algorithms (p253-260)`
