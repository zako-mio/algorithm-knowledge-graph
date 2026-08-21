---
id: trie
name: Trie 字典树
group: G-C-2
stage: intermediate
priority: P0
depth_tier: deep
---

# Trie 字典树

> 树形结构存储多字符串公共前缀，插入/查询 O(\|S\|)，是 AC 自动机与可持久化 Trie 的基础

<!-- 元信息: id=trie · group=G-C-2 · stage=intermediate · priority=P0 · depth_tier=deep -->

## What · 是什么

Trie（字典树）用树形结构存储多个字符串：根到某个节点的路径代表一个字符串前缀，每个节点有指向后继字符的转移表（next[26] 或其他字符集）。插入一个字符串即从根沿字符逐层下走，缺节点就新建；在终点打上结束标记。支持：插入 O(|S|)、查询某字符串是否存在 O(|S|)、统计以某前缀开头的数量（节点维护 cnt）、按位插入整数的 01-Trie（异或极值/异或和）。是 AC 自动机、可持久化 Trie、字典序排序、单词自动补全的基础。总节点数 ≤ 模式串总长度之和，空间 O(Σ|s_i|·字符集)。

## Why · 为什么

### 直觉 · Intuition

词典按首字母分页、同首字母再按第二个字母分……Trie 就是把‘字典的分层结构’物化成树：所有字符串共享公共前缀节点，查询时顺着字母逐层翻页，一次比较一个字符，绝不回头。字符串越长查询越‘顺路’。

### 原理 · Principle

定义转移函数 δ(u,c)：从节点 u 读入字符 c 到达的节点。插入 s 时从根起反复 u=δ(u,c) 并必要时新建节点，结束时 exist[u]=true。查询同样走 δ，最后检查 exist。为支持前缀统计，每个节点记录经过次数 cnt（每次插入路径上 cnt++）。01-Trie：把整数按二进制位（高位到低位或低位到高位）逐位插入，可 O(logV) 求异或最大值（贪心沿反位走）、维护异或和、全局加一（低位建树交换左右子）。正确性：公共前缀共享路径，查询逐字符比较必然唯一。

### 历史 · History

Trie 概念源于 1912 年（René de la Briandais 更早，1960 年 Edward Fredkin 正式命名 trie，取自 retrieval）。因能快速检索字典词条而广泛用于拼写检查、前缀匹配。OI Wiki《字典树》页给出模板及应用（检索字符串、维护异或极值、维护异或和、01-Trie 合并）；CPH ch26 也作为字符串算法基础收录。

## How · 实现

### 伪代码

```python
class TrieNode: ch=[None]*26; cnt=0; end=False
class Trie:
  def insert(s):
    p = root
    for c in s:
      i = ord(c)-ord('a')
      if p.ch[i] is None: p.ch[i] = TrieNode()
      p = p.ch[i]; p.cnt += 1
    p.end = True
  def exists(s):
    p = walk(s)
    return p is not None and p.end
  def count_prefix(s): return walk(s).cnt if walk(s) else 0
```

### Python 实现

```python
class TrieNode:
    __slots__ = ('ch', 'cnt', 'end')
    def __init__(self):
        self.ch = [None] * 26
        self.cnt = 0        # 经过该节点的字符串个数
        self.end = False    # 是否有字符串在此结束


class Trie:
    """字典树: 支持小写字符串的插入/查询/前缀统计/删除."""
    def __init__(self):
        self.root = TrieNode()

    def insert(self, s):
        p = self.root
        for ch in s:
            i = ord(ch) - ord('a')
            if p.ch[i] is None:
                p.ch[i] = TrieNode()
            p = p.ch[i]
            p.cnt += 1
        p.end = True

    def _find_node(self, s):
        p = self.root
        for ch in s:
            i = ord(ch) - ord('a')
            if p.ch[i] is None:
                return None
            p = p.ch[i]
        return p

    def exists(self, s):
        p = self._find_node(s)
        return p is not None and p.end

    def count_prefix(self, s):
        """以 s 为前缀的字符串个数."""
        p = self._find_node(s)
        return p.cnt if p is not None else 0

    def startswith(self, s):
        return self._find_node(s) is not None

    def remove(self, s):
        """删除一个 s (若存在). 递减 cnt, 清除 end 标记."""
        p = self.root
        path = [self.root]
        for ch in s:
            i = ord(ch) - ord('a')
            if p.ch[i] is None:
                return
            p = p.ch[i]
            path.append(p)
        if not p.end:
            return
        for node in path[1:]:
            node.cnt -= 1
        p.end = False


if __name__ == "__main__":
    words = ["apple", "app", "apply", "banana", "ban"]
    t = Trie()
    for w in words:
        t.insert(w)
    assert t.exists("apple") and t.exists("ban")
    assert not t.exists("ap") and not t.exists("applepie")
    assert t.count_prefix("ap") == 3        # app, apple, apply
    assert t.count_prefix("ban") == 2
    assert t.count_prefix("ba") == 2
    assert t.count_prefix("zz") == 0
    assert t.startswith("appl")

    t.remove("app")
    assert not t.exists("app")
    assert t.count_prefix("ap") == 2
    t.remove("apple")
    assert t.count_prefix("ap") == 1
    assert t.exists("apply")

    # 与 Python 暴力方法交叉验证
    import random
    random.seed(5)
    store = []
    t2 = Trie()
    for _ in range(2000):
        n = random.randint(1, 8)
        s = ''.join(random.choice('abcdefghij') for _ in range(n))
        store.append(s)
        t2.insert(s)
    for _ in range(300):
        n = random.randint(1, 6)
        pre = ''.join(random.choice('abcdefghij') for _ in range(n))
        expected = sum(1 for x in store if x.startswith(pre))
        assert t2.count_prefix(pre) == expected, (pre, expected, t2.count_prefix(pre))
    print("trie: all tests passed")

```

**PyPy 提示**: 节点用 list 存 26 个引用开销不小；大输入（总长 1e6 以上）用数组模拟：tr[node][26] 用扁平 list 或 list of list，节点号连续分配。删除用递减 cnt 保留结构即可；若需真正释放节点可用 free list。01-Trie 建议固定深度（如 31 位）避免进位问题。递归遍历会深，遍历用栈。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 插入/查询 O(\|S\|)；前缀统计 O(\|S\|) |
| 空间 | O(Σ\|s_i\| × 字符集) 节点 |

### 局限

① 全 26 字符集每节点 26 个指针，内存大（总长 1e6 时 ~26M 引用）；字符集大时可改 map 或 child list（用空间换查找 log）；② 只支持前缀查询，后缀查询需反转字符串或建后缀结构；③ Python 对象式实现常数大，大数据必须数组模拟；④ 不支持区间查询（需可持久化/前缀和），删除后内存不回收。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P2580 | 2 | 于是他错误的点名开始了：Trie 插入+查询，OI Wiki 例题 | [https://www.luogu.com.cn/problem/P2580](https://www.luogu.com.cn/problem/P2580) |
| Luogu | P4551 | 3 | 最长异或路径：树上任意两点异或路径 -> 01-Trie 贪心求最大异或对 | [https://www.luogu.com.cn/problem/P4551](https://www.luogu.com.cn/problem/P4551) |
| LeetCode.cn | 208 | 2 | 实现 Trie（前缀树）：insert/search/startsWith 模板题 | [https://leetcode.cn/problems/implement-trie-prefix-tree/](https://leetcode.cn/problems/implement-trie-prefix-tree/) |

## Pitfalls · 易错点

- 存在查询误用‘走过节点即可’而忽略 end 标记（如查 apple 误认 app）
- 字符集下标映射出错（大小写、非小写字母需映射表）
- 前缀统计 cnt 更新位置（应在子节点而非父节点）写错
- 对象式 Trie 内存爆炸；递归深度过深（长字符串）
- 删除实现把整个子树剪掉导致其他字符串丢失（应只递减 cnt）
- 01-Trie 位数不足导致高位置 0 与进位问题

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/string/trie/](https://oi-wiki.org/string/trie/)
- CP-Algorithms ✓ [https://cp-algorithms.com/string/aho_corasick.html](https://cp-algorithms.com/string/aho_corasick.html)
- 书籍 ✓ `CPH ch26 String algorithms p253-260`
