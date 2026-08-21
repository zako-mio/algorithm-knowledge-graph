---
id: random-shuffle
name: 随机打乱防hack
group: G-E-5
stage: intermediate
priority: P2
depth_tier: standard
---

# 随机打乱防hack

> shuffle打乱输入顺序防止构造数据卡哈希/快排；CF hack常见反制手段

<!-- 元信息: id=random-shuffle · group=G-E-5 · stage=intermediate · priority=P2 · depth_tier=standard -->

## What · 是什么

随机打乱（random shuffle）是一种'防 hack'预处理：在算法执行前用随机数生成器打乱输入顺序，使确定性构造的'最坏数据'（针对固定顺序/固定哈希/固定枢纽的快排、固定 base 的字符串哈希、固定遍历顺序的算法）失效。在 Codeforces 的 hack 机制下，选手代码若对输入顺序、哈希 base、随机种子敏感，就会被构造数据卡掉；shuffle 或随机化参数能让攻击者无法预知代码行为。经典场景：随机化快速排序（随机选枢纽避免 O(n²) 退化）、随机 base/模数的字符串哈希（防碰撞构造）、随机增量法（见 random-technique）、std::random_shuffle 防止按特定顺序触发的退化分支。

## Why · 为什么

### 直觉 · Intuition

构造数据之所以能卡掉算法，是因为攻击者知道你代码里的固定行为（如快排总是取第一个元素、哈希 base 固定为 131）。如果把顺序或参数随机化，攻击者针对'你的固定行为'构造的数据就不再有针对性——他无法预知哪个顺序/哪个 base 会让程序退化。本质是把'固定输入上的最坏情况'转化为'概率很小的随机事件'。

### 原理 · Principle

正确性来自概率分析：对任意固定的输入序列，随机打乱后落在'使算法退化'的那一小撮排列上的概率很低（例如随机化快排，任给输入，坏枢纽出现的概率被控制在某个常数以下，期望 O(n log n)）。关键要求：①随机种子必须每次运行不同（用系统时间/随机设备），否则攻击者可复现；②shuffle 必须均匀（Fisher–Yates），否则仍可预测；③随机范围要足够（如 base 从大范围随机选）。注意 shuffle 只对'对顺序敏感'的算法有效，不改变算法本身的正确性。

### 历史 · History

随机化排序的研究可追溯到 1960s（Hoare 的快速排序随机化建议，1975 后正式分析）；Fisher–Yates shuffle 于 1938 年提出，是现代均匀随机排列的标准方法。'防 hack'实践随 Codeforces 的 hack 机制（2009+）而流行，成为 OI/ICPC 社区的反构造技巧。

## How · 实现

### 伪代码

```python
import random
random.seed()  # 默认系统熵
arr = [...]
random.shuffle(arr)  # Fisher-Yates 均匀洗牌
# 或固定种子便于复现: random.seed(1234)

# 随机化快排: 每次随机选 pivot 或先 shuffle
# 随机哈希 base: base = random.randrange(2**20, 2**30)
# 注意: 防 hack 需每轮不同种子
```

### Python 实现

```python
import random


def randomized_quicksort_median(a):
    """随机化快排: 随机选枢纽避免最坏情况"""
    if len(a) <= 1:
        return a[:]
    pivot = a[random.randrange(len(a))]
    lo = [x for x in a if x < pivot]
    eq = [x for x in a if x == pivot]
    hi = [x for x in a if x > pivot]
    return randomized_quicksort_median(lo) + eq + randomized_quicksort_median(hi)


def fisher_yates_shuffle(arr):
    """手动 Fisher-Yates: 验证均匀性"""
    a = arr[:]
    for i in range(len(a) - 1, 0, -1):
        j = random.randrange(i + 1)
        a[i], a[j] = a[j], a[i]
    return a


def sort_with_shuffle(arr, seed=None):
    """防 hack: 先 shuffle 再排序 (快排类算法消除最坏情况)"""
    rng = random.Random(seed)
    a = arr[:]
    rng.shuffle(a)
    a.sort()
    return a


if __name__ == "__main__":
    random.seed(42)

    # 随机化快排正确性
    for _ in range(200):
        n = random.randrange(1, 40)
        a = [random.randrange(10) for _ in range(n)]
        assert randomized_quicksort_median(a) == sorted(a)

    # shuffle+sort 与排序一致
    for _ in range(100):
        n = random.randrange(1, 50)
        a = [random.randrange(100) for _ in range(n)]
        assert sort_with_shuffle(a, seed=7) == sorted(a)

    # Fisher-Yates 均匀性: 统计每个元素到各位置频率近似均匀
    n = 6
    cnt = [[0] * n for _ in range(n)]
    trials = 20000
    for _ in range(trials):
        p = fisher_yates_shuffle(list(range(n)))
        for pos, val in enumerate(p):
            cnt[val][pos] += 1
    for v in range(n):
        for pos in range(n):
            assert abs(cnt[v][pos] / trials - 1.0 / n) < 0.02, (v, pos)

    # 不同种子结果不同(防 hack 的关键)
    a = list(range(50))
    s1 = sort_with_shuffle(a, seed=1)
    s2 = sort_with_shuffle(a, seed=2)
    assert s1 == s2 == sorted(a)  # 排序结果相同但执行顺序不同

    print("random-shuffle tests passed")

```

**PyPy 提示**: Python 内置 random.shuffle 已是 Fisher–Yates 均匀洗牌，直接用即可。若需复现性，用 random.Random(seed) 实例或 random.seed()。PyPy 下 random 与 CPython 行为一致。注意：防 hack 要每次运行换种子（不要固定 seed，否则可被针对）。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | shuffle O(n)；洗牌后算法复杂度同原算法（随机化快排期望 O(n log n)） |
| 空间 | O(1) 额外（原地 shuffle） |

### 局限

只对顺序/参数敏感的算法有效；不改变算法正确性，只是降低最坏情况的概率；若攻击者能复现你的种子（如固定 seed），仍可被卡；对不依赖顺序的算法无意义。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3809 | 3 | 后缀排序模板：可配合随机哈希/随机化实践，但标准题主考 SA 倍增 | [https://www.luogu.com.cn/problem/P3809](https://www.luogu.com.cn/problem/P3809) |
| Luogu | U461211 | 4 | 字符串 Hash（数据加强）：随机 base/双哈希防卡，直接对应 anti-hash | [https://www.luogu.com.cn/problem/U461211](https://www.luogu.com.cn/problem/U461211) |

## Pitfalls · 易错点

- 固定种子/忘调 srand => 随机化名存实亡，可被 hack
- random_shuffle 在旧标准下不是均匀的，用 std::shuffle 或 Fisher-Yates
- shuffle 不能'修复'算法本身的逻辑错误
- 对内存/缓存敏感问题，shuffle 反而可能使局部性变差
- OI/ICPC 正式赛一般不 hack，但防构造仍是稳健习惯

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/misc/random/](https://oi-wiki.org/misc/random/)
- Wikipedia ✓ [https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle](https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle)
