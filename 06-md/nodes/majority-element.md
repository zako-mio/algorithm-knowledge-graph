---
id: majority-element
name: 主元素/Boyer-Moore投票
group: G-E-7
stage: intermediate
priority: P1
depth_tier: standard
---

# 主元素/Boyer-Moore投票

> 出现>n/2的元素：候选+计数消去法O(n)O(1)；在线流式处理

<!-- 元信息: id=majority-element · group=G-E-7 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

主元素问题：给 n 个元素序列，求出现次数严格大于 n/2 的元素(题目保证存在)。Boyer-Moore 多数投票算法用 val/cnt 两个变量在线扫描一遍即得候选，再扫描一遍验证，时空 O(n)/O(1)。离线做法可先排序取中位元素或 nth_element 找第 n/2+1 大。推广：出现次数 >n/3 的所有元素(LeetCode 229)需维护两个候选。

## Why · 为什么

### 直觉 · Intuition

主元素出现次数超过一半，那么'主元素和一个非主元素两两配对消去'后主元素必剩。于是维护一个候选 val 与计数 cnt：遇到相同元素 cnt+1，不同则 cnt-1，cnt 归零就换候选。消去配对的过程保证最终候选是主元素。

### 原理 · Principle

扫描：cnt==0 时令 val=x,cnt=1；否则 x==val 则 cnt++，否则 cnt--。每一步都可理解为把 val 与一个非 val 元素抵消。由于主元素多于一半，抵消过程中它永远不可能被消灭完，故最终 val 即主元素。算法只能给出'候选'，主元素是否存在需二次扫描计数验证。

### 历史 · History

算法 1981 年由 Boyer 和 Moore 提出(与 BM 字符串匹配算法同一作者)。OI Wiki 主元素页(多数投票算法)描述在线与离线两种做法，并列出洛谷 P2397(yyy loves Maths VI mode)与 LeetCode 229(多数元素II)为典型例题。

## How · 实现

### 伪代码

```python
# 第一遍: 找候选
val, cnt = None, 0
for x in a:
  if cnt == 0:
    val, cnt = x, 1
  elif x == val:
    cnt += 1
  else:
    cnt -= 1

# 第二遍: 验证 val 是否 > n/2
count = sum(1 for x in a if x == val)
return val if count > n // 2 else -1
```

### Python 实现

```python
def majority_element(nums):
    """Boyer-Moore 投票算法。返回出现>n/2的元素, 无则返回-1。"""
    val, cnt = None, 0
    for x in nums:
        if cnt == 0:
            val, cnt = x, 1
        elif x == val:
            cnt += 1
        else:
            cnt -= 1
    # 验证
    if nums.count(val) > len(nums) // 2:
        return val
    return -1


def majority_element_generalized(nums):
    """LeetCode 229: 找出所有出现超过 n/3 的元素。
    维护两个候选。
    """
    cand1 = cand2 = None
    c1 = c2 = 0
    for x in nums:
        if c1 == 0 and x != cand2:
            cand1, c1 = x, 1
        elif c2 == 0 and x != cand1:
            cand2, c2 = x, 1
        elif x == cand1:
            c1 += 1
        elif x == cand2:
            c2 += 1
        else:
            c1 -= 1
            c2 -= 1
    n = len(nums)
    ans = []
    for c in (cand1, cand2):
        if c is not None and nums.count(c) > n // 3 and c not in ans:
            ans.append(c)
    return ans


def majority_offline(nums):
    """离线做法: 排序取中位元素(nth_element 思想)。"""
    n = len(nums)
    mid = sorted(nums)[n // 2]
    return mid if nums.count(mid) > n // 2 else -1


if __name__ == '__main__':
    assert majority_element([1, 2, 3, 2, 2, 2, 5, 4, 2]) == 2
    assert majority_element([3, 3, 4, 2, 4, 4, 2, 4, 4]) == 4
    assert majority_element([1, 1, 1, 2, 2]) == 1
    assert majority_element([1, 2, 3]) == -1          # 无主元素
    assert majority_element([2, 2, 1, 1, 1, 2, 2]) == 2

    assert majority_element_generalized([3, 2, 3]) == [3]
    assert majority_element_generalized([1, 1, 1, 3, 3, 2, 2, 2]) == [1, 2]

    assert majority_offline([1, 2, 3, 2, 2, 2, 5, 4, 2]) == 2
    assert majority_offline([1, 2, 3]) == -1

    import random
    random.seed(5)
    for _ in range(200):
        n = random.randint(1, 30)
        arr = [random.randint(0, 5) for _ in range(n)]
        brute = [x for x in set(arr) if arr.count(x) > n // 2]
        got = majority_element(arr)
        assert (got == brute[0]) if brute else (got == -1)

    print('majority [1,2,3,2,2,2,5,4,2]:', majority_element([1, 2, 3, 2, 2, 2, 5, 4, 2]))
    print('no majority [1,2,3]          :', majority_element([1, 2, 3]))
    print('>n/3 elements [1,1,1,3,3,2,2,2]:', majority_element_generalized([1, 1, 1, 3, 3, 2, 2, 2]))
    print('Random brute-compare (200 cases): OK')
    print('All majority-element tests passed!')

```

**PyPy 提示**: 两个变量扫描, PyPy 近乎零开销; 注意第二遍用 count() 是 O(n) 内置 C 实现, 比 Python 手写循环快; 流式数据无法回放时可用双指针重复流代替二次扫描(流式存储受限时)。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(N) — 两次线性扫描 |
| 空间 | O(1) — 仅两个变量 |

### 局限

只能保证候选为主元素; 若序列无主元素必须二次扫描验证; 主元素定义>n/2 时只需单候选, 改为>n/3 需多候选推广且候选数有限; 流式数据无法缓存时二次验证需能重读流。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P2397 | 2 | yyy loves Maths VI (mode): 在线主元素, 题目要求不能开大数组, 投票算法正解 | [https://www.luogu.com.cn/problem/P2397](https://www.luogu.com.cn/problem/P2397) |
| LeetCode | 169 | 1 | 多数元素: Boyer-Moore 投票经典模板 | [https://leetcode.cn/problems/majority-element/](https://leetcode.cn/problems/majority-element/) |
| LeetCode | 229 | 2 | 多数元素II: 出现>n/3 的元素, 双候选推广 | [https://leetcode.cn/problems/majority-element-ii/](https://leetcode.cn/problems/majority-element-ii/) |

## Pitfalls · 易错点

- 不验证就输出候选: 无主元素时算法给出的是任意'占位'值, 必须二次计数验证
- cnt==0 更新候选时先后顺序: 先判 cnt==0 再判 x==val, 否则边界错
- Python 中 val 初始化 None 时与 0/False 比较需小心; 用对象哨兵或直接以首元素初始化更稳
- n/2 是整数除法, 出现次数要 > n//2 才满足'严格大于'
- >n/3 推广维护 2 个候选时, 处理 c1==0 且 x==cand2 的先后关系, 否则候选冲突

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/misc/main-element/](https://oi-wiki.org/misc/main-element/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/main-element.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/main-element.md)
- web ✓ [https://en.wikipedia.org/wiki/Boyer%E2%80%93Moore_majority_vote_algorithm](https://en.wikipedia.org/wiki/Boyer%E2%80%93Moore_majority_vote_algorithm)
