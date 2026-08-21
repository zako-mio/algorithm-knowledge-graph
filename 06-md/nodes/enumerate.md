---
id: enumerate
name: 枚举与暴力
group: G-A-1
stage: basic
priority: P0
depth_tier: deep
---

# 枚举与暴力

> 系统枚举所有可能，常结合剪枝优化

<!-- 元信息: id=enumerate · group=G-A-1 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

枚举（enumerate）/暴力（brute force）：系统性地把解空间的所有候选尝试一遍，逐个判定是否满足条件。要点：①给出解空间（要枚举哪些要素）；②减少枚举空间（合理上下界）；③选择合适的枚举顺序（如求最大素数从大到小）。优化路径：缩小枚举范围 → 消除冗余顺序 → 用桶/哈希把 O(n^2) 降为 O(n)（如两数之和）。位运算枚举子集、DFS 回溯（排列/组合）是其重要分支。

## Why · 为什么

### 直觉 · Intuition

枚举是『笨但正确』的保底策略，也是所有算法正确性验证的对拍基准。核心思维：把『猜答案』变成系统化的试错——先想清楚可能的情况有哪些，再想怎么不重不漏地扫完。

### 原理 · Principle

不重不漏：枚举次序与边界保证每个候选恰好被评估一次。复杂度 = 候选数 × 单次判定代价。常见降维：排序+双指针、哈希桶（空间换时间）、前缀和、剪枝。OI Wiki 经典例：和为 0 的数对——先枚举两数 O(n^2)，通过限制 j<i 减半，再用桶 met[] 记录已见值降为 O(n)。

### 历史 · History

枚举是算法的最朴素形式，计算机早期即用于穷举（如毕达哥拉斯三元组、素数判定）。现代竞赛中枚举常作为对拍基准与状态空间的 DFS 展开；子集枚举用位运算、排列枚举用递归回溯，是回溯/剪枝/搜索的基石。

## How · 实现

### 伪代码

```python
# 两数之和为0：从 O(n^2) 到 O(n)
met = set()
ans = 0
for x in a:
    if -x in met: ans += 1     # 存在互补 → 数对
    met.add(x)

# 枚举子集（位运算）
for mask in range(1 << n):
    subset = {i for i in range(n) if mask >> i & 1}

# 排列枚举（递归回溯）
def dfs(perm):
    if len(perm) == n: 处理(perm); return
    for x in 可选集合: dfs(perm + [x])
```

### Python 实现

```python
def count_zero_pairs_naive(a):
    """两数之和为 0 的数对个数（暴力 O(n^2)）"""
    n = len(a)
    ans = 0
    for i in range(n):
        for j in range(i + 1, n):
            if a[i] + a[j] == 0:
                ans += 1
    return ans


def count_zero_pairs_hash(a):
    """哈希优化 O(n)：统计 i<j 且 a[i]+a[j]==0 的数对（含多个 0 的情形）"""
    from collections import Counter
    cnt = Counter()
    ans = 0
    for x in a:
        ans += cnt[-x]
        cnt[x] += 1
    return ans


def subsets(nums):
    """枚举全部子集（位运算）"""
    n = len(nums)
    out = []
    for mask in range(1 << n):
        out.append([nums[i] for i in range(n) if mask >> i & 1])
    return out


def permutations(nums):
    """枚举全部排列（递归回溯）"""
    n = len(nums)
    res = []
    def dfs(path, used):
        if len(path) == n:
            res.append(path[:])
            return
        for i in range(n):
            if not used[i]:
                used[i] = True
                path.append(nums[i])
                dfs(path, used)
                path.pop()
                used[i] = False
    dfs([], [False] * n)
    return res


if __name__ == "__main__":
    import random
    for _ in range(200):
        a = [random.randint(-15, 15) for _ in range(random.randint(1, 60))]
        assert count_zero_pairs_naive(a) == count_zero_pairs_hash(a), a
    assert len(subsets([1, 2, 3])) == 8
    assert len(permutations([1, 2, 3])) == 6
    p = permutations([1, 2, 3])
    assert p[0] == [1, 2, 3] and p[-1] == [3, 2, 1]
    print("枚举（两数和O(n)/子集/排列）正确性 OK（200 组暴力对照）")
    a = [4, 3, -3, 2, -4, 0, 0]
    print(f"a={a} 和为0数对(哈希): {count_zero_pairs_hash(a)}")
    print("3元素子集:", subsets([1, 2, 3]))

```

**PyPy 提示**: 枚举性能瓶颈在层数：Python 内层循环慢，n 大时优先用数学/剪枝缩减候选。子集枚举 1<<n 适合 n≤22（PyPy 下可到 ~24）；排列 n! 适合 n≤10。回溯剪枝（可行性/最优性剪枝）是暴力上台阶的核心。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(候选数 × 判定代价)，如两数和 O(n^2)→O(n)，子集 O(2^n)，排列 O(n!) |
| 空间 | O(1)~O(n) |

### 局限

指数级候选规模限制 n 的取值（2^n / n! 必须很小）。仅当解空间可枚举且判定便宜时实用；否则需要剪枝、记忆化或更优算法。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| OI-Wiki | basic/enumerate | 2 | 枚举与暴力讲解 | [https://oi-wiki.org/basic/enumerate/](https://oi-wiki.org/basic/enumerate/) |
| Luogu | P1706 | 2 | 全排列/组合枚举模板 | [https://www.luogu.com.cn/problem/P1706](https://www.luogu.com.cn/problem/P1706) |
| CPH | ch5 p57 | 2 | 生成子集与排列 | [https://cses.fi/book/book.pdf](https://cses.fi/book/book.pdf) |

## Pitfalls · 易错点

- 枚举范围不收敛：解空间定得过大（如全量 1..1e9 而非合理边界）
- 重复计数：无序数对写成有序导致 ans 多一倍（先限制次序再乘系数）
- 递归回溯忘记还原状态（used[i]/path 未 pop）产生错误解

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/basic/enumerate/](https://oi-wiki.org/basic/enumerate/)
- 书籍 ✓ `CPH ch5 p57`
- OI Wiki ✓ [https://www.luogu.com.cn/problem/P1706](https://www.luogu.com.cn/problem/P1706)
