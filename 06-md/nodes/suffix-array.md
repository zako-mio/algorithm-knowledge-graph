---
id: suffix-array
name: 后缀数组
group: G-C-3
stage: advanced
priority: P1
depth_tier: standard
---

# 后缀数组

> SA+rank+height数组，对字符串所有后缀排序，配合LCP做子串统计与匹配

<!-- 元信息: id=suffix-array · group=G-C-3 · stage=advanced · priority=P1 · depth_tier=standard -->

## What · 是什么

后缀数组（Suffix Array, SA）是字符串 S 的所有后缀按字典序排序后得到的起始下标数组：sa[i] 表示字典序第 i 小的后缀的起始位置。配套数组：rank/rk[i] 表示后缀 i 的排名（sa 与 rk 互逆：sa[rk[i]]=rk[sa[i]]=i）；height[i]=lcp(sa[i], sa[i-1]) 表示排序后相邻两个后缀的最长公共前缀（height[1]=0）。SA 与 SAM/后缀树可互相转化。经典构造：朴素 O(n²log n) 直接排序所有后缀；倍增法 O(n log n)（可用基数排序 O(n log n)，排序比较用 O(n log²n)）；SA-IS/DC3 达到 O(n)。核心应用：子串匹配（SA 上二分）、不同子串数 n(n+1)/2 − Σ height、LCP(RMQ 区间最小值)、出现次数统计、最长公共子串、循环同构/最小表示、结合并查集/单调栈做区间统计（品酒大会等）。

## Why · 为什么

### 直觉 · Intuition

把'所有后缀'按字典序排序后，具备相同前缀的后缀会相邻——这是 height 数组与 LCP 区间最小值定理的基础。想找某个子串的所有出现位置，只需在 SA 上二分；想知道两个后缀的 LCP，只需查它们排名之间 height 的区间最小值（RMQ）。倍增思想：排序长度 1 的子串 → 用两个长度 w/2 的排名拼成长度 w 的关键字对 → 再排序 → 长度翻倍，直到 w≥n，因为后缀由前缀完全决定，排序长度 ≥n 的子串即等价于排序后缀。

### 原理 · Principle

倍增法正确性：长度 w 的子串 s[i..i+w-1] 由 (s[i..i+w/2-1], s[i+w/2..i+w-1]) 拼接，若前一半的排名已对（长度 w/2 的子串排序正确），则二元组 (rk[i], rk[i+w/2]) 的字典序即长度 w 子串的字典序。i+w/2 越界时视为 -inf（更小）。用基数排序（按第二关键字再按第一关键字计数排序）每次 O(n)，共 O(log n) 轮，总 O(n log n)。height 的 O(n) 求法依赖引理 height[rk[i]] ≥ height[rk[i-1]]−1：因为后缀 i-1 与它排名前一位的 LCP 为 h，则删掉首字符后后缀 i 与其相邻后缀至少有 h−1 的公共前缀；用此性质暴力跳，k 最多减 n 次加 2n 次，总 O(n)。

### 历史 · History

后缀数组由 Udi Manber 与 Gene Myers 于 1990 年提出，用于字符串匹配与数据压缩；1993 年 Giegerich 与 Kurtz 将其与后缀树联系起来。倍增构造法、height/LCP 的线性算法以及'罗穗骞论文'（2004，后缀数组——处理字符串的有力工具）让 SA 成为中国竞赛选手的标配技能。后续 SA-IS（Nong-Zhang-Chan 2009）与 DC3（Kärkkäinen–Sanders 2003）提供线性构造。

## How · 实现

### 伪代码

```python
# 倍增法求 SA (O(n log n), 排序用计数/基数)
sa[i]=i; rk[i]=s[i];  # 长度1排序
for w=1; w<n; w<<=1:
    # 按 (rk[i], rk[i+w]) 双关键字基数排序
    # 第二关键字: 越界(i+w>n)排最前
    # 第一关键字: rk[i]
    更新 sa 与 rk (去重相同子串)
# 若 rk 值域已达 [1..n] 即所有后缀排名不同, 可提前退出

# O(n) 求 height
for i=1..n:
    k = max(0, k-1)
    while s[i+k] == s[sa[rk[i]-1]+k]: k+=1
    height[rk[i]] = k
```

### Python 实现

```python
def build_sa(s):
    """倍增法求后缀数组(含复杂度 O(n log^2 n) 的简单实现 + 可换基数).
    s: 字符串, 返回 sa (0-index, sa[i] 为第 i 小后缀起始下标)
    """
    n = len(s)
    sa = list(range(n))
    rk = [ord(c) for c in s]
    k = 1
    tmp = [0] * n
    while True:
        # 双关键字: (rk[i], rk[i+k]) 排序, 越界第二关键字视为 -1
        sa.sort(key=lambda x: (rk[x], rk[x + k] if x + k < n else -1))
        # 重新排名
        tmp[sa[0]] = 0
        classes = 1
        for i in range(1, n):
            cur = (rk[sa[i]], rk[sa[i] + k] if sa[i] + k < n else -1)
            pre = (rk[sa[i - 1]], rk[sa[i - 1] + k] if sa[i - 1] + k < n else -1)
            if cur != pre:
                classes += 1
            tmp[sa[i]] = classes - 1
        rk, tmp = tmp, rk
        if classes == n:
            break
        k <<= 1
    return sa


def build_rank_height(s, sa):
    """由 sa 求 rk 与 height (height[i]=lcp(sa[i],sa[i-1]), height[0]=0)."""
    n = len(s)
    rk = [0] * n
    for i in range(n):
        rk[sa[i]] = i
    height = [0] * n
    h = 0
    for i in range(n):
        if rk[i] == 0:
            continue
        j = sa[rk[i] - 1]
        while i + h < n and j + h < n and s[i + h] == s[j + h]:
            h += 1
        height[rk[i]] = h
        if h:
            h -= 1
    return rk, height


def count_distinct_substrings(s, sa, height):
    """不同子串数 = n(n+1)/2 - sum(height[1:])"""
    n = len(s)
    return n * (n + 1) // 2 - sum(height[1:])


def lcp_min_query(s, sa, height):
    """返回一个函数: lcp(i,j) = min(height[rk[i]+1 .. rk[j]]) 用 RMQ(ST 表)."""
    import math
    n = len(s)
    rk = [0] * n
    for i in range(n):
        rk[sa[i]] = i
    LOG = n.bit_length()
    st = [[0] * n for _ in range(LOG)]
    st[0] = height[:]
    for k in range(1, LOG):
        span = 1 << (k - 1)
        for i in range(n - (1 << k) + 1):
            st[k][i] = min(st[k - 1][i], st[k - 1][i + span])

    def query(a, b):
        if a == b:
            return n - a
        l, r = rk[a], rk[b]
        if l > r:
            l, r = r, l
        # min height[l+1..r]
        L = r - l
        k = L.bit_length() - 1
        return min(st[k][l + 1], st[k][r - (1 << k) + 1])

    return query


if __name__ == "__main__":
    s = "ababa"
    sa = build_sa(s)
    rk, h = build_rank_height(s, sa)
    # 后缀: 0:ababa 1:baba 2:aba 3:ba 4:a
    # 排序: a(4) aba(2) ababa(0) ba(3) baba(1) => sa=[4,2,0,3,1]
    assert sa == [4, 2, 0, 3, 1], sa
    assert rk == [2, 4, 1, 3, 0], rk
    # height: [_, lcp(a,aba)=1, lcp(aba,ababa)=3, lcp(ababa,ba)=0, lcp(ba,baba)=2]
    assert h == [0, 1, 3, 0, 2], h

    # 不同子串数: n(n+1)/2 - sum(h[1:]) = 15 - (1+3+0+2)=9
    assert count_distinct_substrings(s, sa, h) == 9

    # 验证 lcp RMQ
    q = lcp_min_query(s, sa, h)
    assert q(0, 2) == 3  # ababa 与 aba 的 LCP=aba (3)
    assert q(1, 3) == 2  # baba 与 ba 的 LCP=ba (2)
    assert q(0, 4) == 1  # ababa 与 a 的 LCP=1

    # 与暴力 LCP 对拍
    def brute_lcp(a, b):
        cnt = 0
        while a + cnt < len(s) and b + cnt < len(s) and s[a + cnt] == s[b + cnt]:
            cnt += 1
        return cnt

    for a in range(len(s)):
        for b in range(len(s)):
            assert q(a, b) == brute_lcp(a, b), (a, b)

    # 随机串对拍
    import random
    random.seed(0)
    for _ in range(50):
        n = random.randrange(1, 15)
        t = ''.join(random.choice('abc') for _ in range(n))
        sa2 = build_sa(t)
        # 检查排序正确性
        suff = [t[i:] for i in range(n)]
        assert [t[i:] for i in sa2] == sorted(suff)
        r2, h2 = build_rank_height(t, sa2)
        # 检查 height 与暴力 LCP 一致
        for i in range(1, n):
            a, b = sa2[i - 1], sa2[i]
            bl = 0
            while a + bl < n and b + bl < n and t[a + bl] == t[b + bl]:
                bl += 1
            assert h2[i] == bl, (t, sa2, i, h2[i], bl)

    print("suffix-array tests passed")

```

**PyPy 提示**: 倍增法用 Python 的 sort(key=...) 是 O(n log²n)（比较 O(log n) 轮），n≤1e5 在 PyPy 下可跑但偏慢；追求 O(n log n) 需手写基数排序（计数排序两遍）。height 用 while 暴力 O(n) 摊销，注意列表索引与切片开销。大串建议 PyPy 或 C++。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 倍增 O(n log²n)（朴素 sort）或 O(n log n)（基数排序）；height O(n)；LCP RMQ 预处理 O(n log n)、查询 O(1) |
| 空间 | O(n) |

### 局限

SA 构造本身不解决所有问题：求两后缀 LCP 需额外 RMQ；出现次数、区间统计等问题需再结合数据结构；字符集为整数时需离散化；Python 下大串常数大。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3809 | 3 | 后缀排序模板：倍增法直接输出 sa | [https://www.luogu.com.cn/problem/P3809](https://www.luogu.com.cn/problem/P3809) |
| Luogu | P2178 | 5 | NOI2015 品酒大会：height + 并查集/单调栈 求 LCP≥r 的对数统计 | [https://www.luogu.com.cn/problem/P2178](https://www.luogu.com.cn/problem/P2178) |
| Luogu | P2870 | 4 | Best Cow Line：串+分隔符+反串拼一起求 SA，O(1) 比较首尾取字符 | [https://www.luogu.com.cn/problem/P2870](https://www.luogu.com.cn/problem/P2870) |
| Luogu | P2852 | 4 | Milk Patterns：出现至少 k 次的最长子串=height 中连续 k-1 个最小值最大 | [https://www.luogu.com.cn/problem/P2852](https://www.luogu.com.cn/problem/P2852) |

## Pitfalls · 易错点

- 下标从 1 还是 0：OI Wiki 用 1-index，CP-Alg 用 0-index，转换易错
- 倍增时第二关键字越界必须视为 -inf（更小），否则排序错
- 重新排名去重时（两子串相同则同排名）忘记处理会破坏后续排序
- height[i]=lcp(sa[i],sa[i-1])，height[1]=0；RMQ 求 lcp(i,j) 要查区间 [min(rk)+1, max(rk)]
- 建 height 时 rk[i]==0 要跳过（无前一名）
- n(n+1)/2 可能溢出 int（Python 无此问题）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/string/sa/](https://oi-wiki.org/string/sa/)
- CP-Algorithms ✓ [https://cp-algorithms.com/string/suffix-array.html](https://cp-algorithms.com/string/suffix-array.html)
- 书籍 ✓ `CPH ch26 (p253-260) String algorithms`
