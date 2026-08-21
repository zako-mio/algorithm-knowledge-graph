---
id: kmp
name: KMP算法
group: G-C-1
stage: intermediate
priority: P0
depth_tier: deep
---

# KMP算法

> 线性时间字符串匹配，前缀函数(pi数组)避免回溯，O(n+m)

<!-- 元信息: id=kmp · group=G-C-1 · stage=intermediate · priority=P0 · depth_tier=deep -->

## What · 是什么

KMP(Knuth–Morris–Pratt)算法是线性时间字符串匹配算法。核心是前缀函数 pi[i]：字符串 s 的子串 s[0..i] 的最长相等真前缀与真后缀长度(也称 border)。匹配时把模式 p 与文本 t 拼接为 p+'#'+t，计算前缀函数，当 pi[i]=|p| 即出现一次匹配。关键性质：失配时 j 跳回 pi[j−1] 而非重置，使得文本指针永不回溯，整体 O(n+m)。除匹配外，前缀函数还可求字符串最小周期、统计每个前缀出现次数、构造 KMP 自动机等。

## Why · 为什么

### 直觉 · Intuition

朴素匹配每失配一次就从头对齐，浪费了已匹配部分的『重叠』信息。KMP 发现：失配时，已匹配后缀中若有某个前缀再次出现(border)，那下一轮可以直接从这个重叠位置开始，而不是从模式头重来。前缀函数记录了每个位置最长的这种重叠长度，失配时沿 pi 链回跳即可——好比『根据已走的路决定下一步从哪继续』。

### 原理 · Principle

定义 pi[i]=max{k: s[0..k−1]=s[i−k+1..i], k<i+1}。递推：pi[i+1]≤pi[i]+1(前缀函数至多+1)；失配时 j=pi[j−1] 得到次长 border。线性性论证：外层 i 增 n 次，j 每次 while 回跳至少减 1，而 j 总共最多增 n 次(每轮 i 增时 j 至多+1)，故 while 总执行 O(n) 次。匹配阶段等价于对 p+'#'+t 求前缀函数，其中 '#' 保证 pi 值不超过 |p|，pi[i]=|p| ⇔ 以 i 结尾处 p 出现。

### 历史 · History

由 Donald Knuth、James Morris 与 Vaughan Pratt 于 1977 年共同发表(论文 'Fast pattern matching in strings')。前缀函数思想可追溯至更早，但 KMP 是首个线性匹配算法，并启发了 Z 函数、自动机、AC 自动机等字符串工具。

## How · 实现

### 伪代码

```python
function prefix_function(s):
  pi[0..n-1]=0
  for i in 1..n-1:
    j = pi[i-1]
    while j>0 and s[i]!=s[j]: j = pi[j-1]
    if s[i]==s[j]: j += 1
    pi[i] = j
  return pi

function kmp_match(text, pattern):
  cur = pattern + '#' + text
  pi = prefix_function(cur)
  for i in |pattern|+1 .. |cur|-1:
    if pi[i]==|pattern|: record i - 2*|pattern|
```

### Python 实现

```python
def prefix_function(s):
    """前缀函数 pi[i] = s[:i+1] 的最长相等真前后缀长度, O(n)"""
    n = len(s)
    pi = [0] * n
    for i in range(1, n):
        j = pi[i - 1]
        while j > 0 and s[i] != s[j]:
            j = pi[j - 1]
        if s[i] == s[j]:
            j += 1
        pi[i] = j
    return pi


def kmp_match(text, pattern):
    """KMP 字符串匹配: 返回 pattern 在 text 中的所有出现起始位置 (0-index)"""
    if not pattern:
        return list(range(len(text) + 1))
    cur = pattern + '#' + text
    pi = prefix_function(cur)
    n = len(pattern)
    res = []
    for i in range(n + 1, len(cur)):
        if pi[i] == n:
            res.append(i - 2 * n)
    return res


def min_period(s):
    """最小周期: n % (n - pi[n-1]) == 0 时存在"""
    n = len(s)
    k = n - prefix_function(s)[n - 1]
    return k if n % k == 0 else n


if __name__ == "__main__":
    assert prefix_function('aabaaab') == [0, 1, 0, 1, 2, 2, 3]
    assert prefix_function('abcabcd') == [0, 0, 0, 1, 2, 3, 0]
    assert kmp_match('ababaab', 'aba') == [0, 2]
    assert kmp_match('aaaa', 'aa') == [0, 1, 2]
    assert kmp_match('hello', 'xyz') == []
    assert min_period('abcabcabc') == 3
    assert min_period('abab') == 2
    assert min_period('abcd') == 4
    print("kmp OK")

```

**PyPy 提示**: Python 的 str.find / str.index 底层是 C 优化过的(通常用 Two-Way/BM 类算法)，实际做题时单次匹配优先用内置 str.find；但 KMP 的价值在于：(1) 求前缀函数做周期/border 分析，(2) 求所有出现位置需要自己实现时，(3) 在线流式匹配/自动机。PyPy 下循环版前缀函数 n=1e6 约 0.5s，可用。注意拼接 p+'#'+t 后下标换算(i−2n)易错。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n+m) 线性(匹配加预处理) |
| 空间 | O(n+m) 拼接串，或 O(n) 若流式处理 |

### 局限

1) 只做完全匹配，不能处理通配符/模糊匹配(需 AC 自动机/KMP自动机扩展)；2) 单个模式求所有出现用 Python 内置 str.find 循环也够快，KMP 显式实现主要用于学理与周期分析；3) 拼接 '#' 需保证不出现在 p,t 中(一般用 0 或哨兵字符)；4) 求最小周期时若 n%k!=0 则最小周期是 n(不可压缩)。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3375 | 2 | 【模板】KMP 字符串匹配：求所有出现位置 + 输出前缀函数，最标准模板 | [https://www.luogu.com.cn/problem/P3375](https://www.luogu.com.cn/problem/P3375) |
| Luogu | P4391 | 2 | Radio Transmission：用前缀函数求最小周期(周期串分析) | [https://www.luogu.com.cn/problem/P4391](https://www.luogu.com.cn/problem/P4391) |
| Codeforces | 126B | 3 | Password：求既是前缀又是后缀且出现在中间的最长子串，前缀函数经典应用 | [https://codeforces.com/problemset/problem/126/B](https://codeforces.com/problemset/problem/126/B) |

## Pitfalls · 易错点

- 拼接下标换算错误(i−2n 易错，务必在 p+'#'+t 的坐标下理解)
- 前缀函数 while 回跳条件写成 s[i]!=s[j] 与 s[i]==s[j] 逻辑颠倒
- 忘记 pi[0]=0，或从 i=0 开始循环导致越界
- 把匹配阶段误用完整 pi 数组而在 p 内部(含 # 之前)也统计出现
- 最小周期判断条件应为 n%(n−pi[n−1])==0，而非直接取 n−pi[n−1]

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/string/kmp/](https://oi-wiki.org/string/kmp/)
- CP-Algorithms ✓ [https://cp-algorithms.com/string/prefix-function.html](https://cp-algorithms.com/string/prefix-function.html)
- 书籍 ✓ `CPH ch26 String algorithms (p253-260)`
