---
id: rabin-karp
name: Rabin-Karp
group: G-C-1
stage: intermediate
priority: P1
depth_tier: standard
---

# Rabin-Karp

> 基于滚动哈希的字符串匹配，O(n+m)期望，多模式匹配友好

<!-- 元信息: id=rabin-karp · group=G-C-1 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

Rabin–Karp 算法基于字符串哈希做匹配：计算模式哈希 hp，再计算文本每个长度为 m 的子串哈希，O(1) 滚动(利用前缀哈希差分)逐一比较，出现哈希相同的位置再确认(防碰撞)。总复杂度 O(n+m) 期望，最坏 O(nm)(全部哈希相等时)。它最擅长的是单文本多模式的匹配：对多个不同长度的模式分别维护哈希集合即可。也可扩展为允许 k 次失配的匹配(哈希+二分找失配点)、最长公共子串二分等。

## Why · 为什么

### 直觉 · Intuition

暴力比较子串是 O(m) 每次；哈希把『子串相等』转成『哈希值相等』，而滚动哈希能在常数时间从窗口滑到下一个窗口。就像给每个 m 长窗口盖数字戳，数字相同才怀疑内容相同。由于哈希比较是 O(1)，全部窗口比较一次就 O(n)。

### 原理 · Principle

利用字符串哈希(见 string-hash 节点)：h[i+1]=h[i]·base+val(s[i]) mod M。模式哈希 hp 一次算好；文本窗口哈希 cur=(h[i+m]−h[i]·base^m) mod M，O(1) 得。相等即命中(期望正确)。多模式：把所有模式哈希放入集合，扫描文本每个位置的所有可能匹配长度即可，或多模式按长度分组(见 OI-wiki)。Rabin 指纹概念由 Richard Karp 与 Michael Rabin 于 1987 年正式提出。

### 历史 · History

Karp 与 Rabin 在 1987 年论文《Efficient randomized pattern-matching algorithms》中提出，核心是『随机哈希做指纹』的随机化思想，之后被广泛应用于子串查找、重复检测、生物信息等领域。Rabin–Karp 的价值不仅在于匹配，更在于把子串比较降为 O(1)。

## How · 实现

### 伪代码

```python
function rabin_karp(text, pattern):
  precompute prefix hashes h[] and base powers
  hp = hash(pattern)
  for i in 0..n-m:
    cur = sub_hash(text, i, i+m)
    if cur == hp: record i
```

### Python 实现

```python
def rabin_karp_double(text, pattern):
    """双哈希 Rabin-Karp (推荐, 防碰撞), 返回所有匹配起始位置"""
    b1, m1 = 131, 1000000007
    b2, m2 = 137, 1000000009

    def build(s):
        h1 = [0] * (len(s) + 1)
        h2 = [0] * (len(s) + 1)
        p1 = [1] * (len(s) + 1)
        p2 = [1] * (len(s) + 1)
        for i, ch in enumerate(s):
            h1[i + 1] = (h1[i] * b1 + ord(ch)) % m1
            h2[i + 1] = (h2[i] * b2 + ord(ch)) % m2
            p1[i + 1] = p1[i] * b1 % m1
            p2[i + 1] = p2[i] * b2 % m2
        return h1, h2, p1, p2

    if not pattern:
        return list(range(len(text) + 1))
    n, m = len(text), len(pattern)
    if m > n:
        return []
    h1, h2, p1, p2 = build(text)
    t1, t2, _, _ = build(pattern)
    hp1, hp2 = t1[m], t2[m]
    res = []
    for i in range(n - m + 1):
        c1 = (h1[i + m] - h1[i] * p1[m]) % m1
        c2 = (h2[i + m] - h2[i] * p2[m]) % m2
        if c1 == hp1 and c2 == hp2:
            res.append(i)
    return res


if __name__ == "__main__":
    assert rabin_karp_double('ababaab', 'aba') == [0, 2]
    assert rabin_karp_double('aaaa', 'aa') == [0, 1, 2]
    assert rabin_karp_double('hello', 'xyz') == []
    print("rabin-karp OK")

```

**PyPy 提示**: Rabin–Karp 的瓶颈是每窗口两次取模，PyPy 下 n=1e6 约 1s 左右。做多模式匹配时把模式哈希放进 set/dict 再对每个文本位置查，无需构建 AC 自动机。若担心碰撞可用双哈希(本模板已内置)。若匹配大量重复串，可先比较长度再比较哈希减少误判确认成本。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n+m) 期望(预处理 O(n+m)，每窗口 O(1))，最坏 O(n·m) |
| 空间 | O(n+m) |

### 局限

1) 期望线性，最坏 O(nm)(全部哈希碰撞)；2) 单模式匹配不如 KMP/Z 确定性好，且 Python 内置 str.find 更快；3) 哈希碰撞概率依赖模数，必须双哈希或大素数；4) 模式 m 很大时 base^m 需预存避免反复算；5) 非二进制文本(任意字符集)同样适用但注意字符值域。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| SPOJ | NAJPF | 3 | Pattern Find：模式匹配所有出现，Rabin-Karp/KMP 均可 | [https://www.spoj.com/problems/NAJPF/](https://www.spoj.com/problems/NAJPF/) |
| Codeforces | 1200E | 4 | Compress Words：滚动哈希比较前后缀重叠 | [https://codeforces.com/contest/1200/problem/E](https://codeforces.com/contest/1200/problem/E) |
| LeetCode | 1044 | 4 | Longest Duplicate Substring：二分+滚动哈希，Rabin-Karp 思路 | [https://leetcode.cn/problems/longest-duplicate-substring/](https://leetcode.cn/problems/longest-duplicate-substring/) |

## Pitfalls · 易错点

- 忘记先比较长度再比哈希，等长但哈希相同仍需二次确认防误报
- base^m 每次现场幂算导致 O(n log m)，应预处理
- 用单哈希在大数据上碰撞，务必双哈希
- m>n 边界未处理，range(n−m+1) 为空但模式哈希仍计算
- 滚动窗口的 h[i+m]−h[i]·base^m 取模前忘补 +mod

## Sources · 信源

- CP-Algorithms ✓ [https://cp-algorithms.com/string/rabin-karp.html](https://cp-algorithms.com/string/rabin-karp.html)
- OI Wiki ✓ [https://oi-wiki.org/string/hash/](https://oi-wiki.org/string/hash/)
