---
id: boyer-moore
name: Boyer-Moore
group: G-C-1
stage: advanced
priority: P2
depth_tier: standard
---

# Boyer-Moore

> 坏字符+好后缀双规则从后往前匹配，平均子线性 O(n/m)~O(n)，最坏 O(nm)

<!-- 元信息: id=boyer-moore · group=G-C-1 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

Boyer–Moore(BM)字符串匹配算法：从模式串末尾向前匹配，失配时用两条启发式规则决定滑动距离——① 坏字符规则：对齐失配位置文本字符与模式中最后一次出现的同字符；② 好后缀规则：利用已匹配后缀，把模式滑动到使该后缀能匹配的下一个位置。BM 在典型文本上表现优于 KMP(平均可跳过多个字符，达到亚线性)，是许多实际文本搜索库(如 grep 早期版本)的核心；但在最坏情况下 O(n·m)。Python 内置 str.find 使用优化过的 Two-Way 算法(线性且常数小)。

## Why · 为什么

### 直觉 · Intuition

KMP 从模式头匹配，BM 反其道从尾部匹配。尾部匹配能更快暴露失配：若尾部字符根本不在模式里，一次就能跳过整个模式长度 m；即使不匹配也能通过『坏字符表』算出最少滑多远。再叠加『好后缀』：尾部已匹配的一段后缀，若能对齐到模式中靠前的相同后缀，就可以利用重叠继续，比只跳一个字符更激进。两条规则取最大值，保证不丢失匹配。

### 原理 · Principle

坏字符表 delta1[c]：字符 c 在模式中最靠右位置与末尾的距离(不在模式中则=m)。好后缀表 delta2[k]：已匹配后缀长度为 k 时，需使模式滑动到能让该后缀(或其 border 部分)重新对齐的位置；用『强后缀规则』构造 O(m)。主循环从后往前比对，失配时 i += max(delta1[text[i+j]], delta2[已匹配长度])。平均复杂度通常远低于线性(文本字符越随机越接近 O(n/m))，最坏 O(nm)(如模式为重复串且每次只前移 1)。

### 历史 · History

Robert S. Boyer 与 J Strother Moore 于 1977 年发表经典论文《A fast string searching algorithm》。其后 Horspool(1980)、Sunday(1990) 简化出仅用坏字符的变体，实践中速度常更快且实现简单；BM 及其变体长期是 Unix grep 等工具的选择。

## How · 实现

### 伪代码

```python
function boyer_moore(text, pattern):
  m=|pattern|; build bad[char]=last position
  build gs[] strong good-suffix table
  s=0
  while s <= n-m:
    j=m-1
    while j>=0 and pattern[j]==text[s+j]: j-=1
    if j<0: record s; s += gs[0]
    else: s += max(gs[j+1], j - bad.get(text[s+j], -1))
  return occurrences
```

### Python 实现

```python
def boyer_moore(text, pattern):
    """Boyer-Moore 字符串匹配 (坏字符 + 强好后缀), 返回所有出现位置。
    平均子线性 (亚 O(n)), 最坏 O(n*m)。"""
    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n + 1))
    if m > n:
        return []
    # 坏字符: 字符在模式中最后出现的位置 (0-based)
    bad = {c: pattern.rfind(c) for c in set(pattern)}
    # 强好后缀表 (Wikipedia/CLRS 标准构造)
    shift = [0] * (m + 1)
    bpos = [0] * (m + 1)
    i, j = m, m + 1
    bpos[i] = j
    while i > 0:
        while j <= m and pattern[i - 1] != pattern[j - 1]:
            if shift[j] == 0:
                shift[j] = j - i
            j = bpos[j]
        i -= 1
        j -= 1
        bpos[i] = j
    j = bpos[0]
    for i in range(m + 1):
        if shift[i] == 0:
            shift[i] = j
        if i == j:
            j = bpos[j]
    res = []
    s = 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            res.append(s)
            s += shift[0]
        else:
            s += max(shift[j + 1], j - bad.get(text[s + j], -1))
    return res


def horspool(text, pattern):
    """Horspool (仅坏字符, 对齐尾字符), 实现简单、竞赛实用"""
    m = len(pattern)
    n = len(text)
    if m == 0:
        return list(range(n + 1))
    if m > n:
        return []
    last = {pattern[idx]: m - 1 - idx for idx in range(m - 1)}
    res = []
    i = 0
    while i <= n - m:
        if text[i:i + m] == pattern:
            res.append(i)
        i += last.get(text[i + m - 1], m)
    return res


if __name__ == "__main__":
    t = "HERE IS A SIMPLE EXAMPLE"
    p = "EXAMPLE"
    assert boyer_moore(t, p) == [17]
    assert boyer_moore('ababaab', 'aba') == [0, 2]
    assert boyer_moore('aaaa', 'aa') == [0, 1, 2]
    assert horspool('ababaab', 'aba') == [0, 2]
    print("bm OK")

```

**PyPy 提示**: 竞赛中用 BM 的机会不多：Python 内置 str.find 用 C 实现更快；显式 BM 的价值在于理解思想与应付『要求不用内置』的场景。Horspool 实现仅 10 行且实战速度优于完整 BM(省掉好后缀表的构建开销)。最坏情形(如 pattern='aaa...a', text 全 'a')退化 O(nm)，务必知晓——若题目可能构造此类数据应改用 KMP/Z。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 平均 O(n·(1/m)+…)≈亚线性，最坏 O(n·m) |
| 空间 | O(m+\|Σ\|) 预处理 |

### 局限

1) 最坏 O(nm) 可被构造数据卡死，安全做法是 KMP/Z(线性) 或 Python 内置 str.find；2) 好后缀表构建实现繁琐易错(本节点提供强后缀标准版)；3) 只适用于单模式；4) 小字母表+重复串模式退化严重；5) 竞赛多数场景用内置/哈希即可，BM 多用于了解原理。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| LeetCode | 28 | 2 | Find the Index of the First Occurrence in a String：可用 BM 思想/内置实现，匹配入门 | [https://leetcode.cn/problems/find-the-index-of-the-first-occurrence-in-a-string/](https://leetcode.cn/problems/find-the-index-of-the-first-occurrence-in-a-string/) |
| SPOJ | NAJPF | 3 | Pattern Find：求模式串所有出现位置，多算法(KMP/BM/Hash)验证 | [https://www.spoj.com/problems/NAJPF/](https://www.spoj.com/problems/NAJPF/) |
| HDU | 1686 | 2 | Oulipo：模式出现次数计数，KMP 模板，可对比 BM | [http://acm.hdu.edu.cn/showproblem.php?pid=1686](http://acm.hdu.edu.cn/showproblem.php?pid=1686) |

## Pitfalls · 易错点

- 坏字符表存『距离』还是『位置』混淆——存位置时公式用 j−bad[c]，存距离时直接 bad[c]
- 好后缀强表构造(i,j 与 bpos 游标)极易写错，务必用标准模板并随机对拍
- 完全匹配后 s+=shift[0] 而不是 +1，否则会漏掉重叠出现
- 把最坏 O(nm) 当成线性用在大数据上导致 TLE
- Horspool 跳距应看 text[i+m−1](尾部字符)，不是失配字符

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/string/bm/](https://oi-wiki.org/string/bm/)
- CP-Algorithms ✓ [https://cp-algorithms.com/string/prefix-function.html](https://cp-algorithms.com/string/prefix-function.html)
