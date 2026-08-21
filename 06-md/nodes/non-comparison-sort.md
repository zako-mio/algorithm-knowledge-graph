---
id: non-comparison-sort
name: 非比较排序(计数/桶/基数)
group: G-A-1
stage: basic
priority: P1
depth_tier: standard
---

# 非比较排序(计数/桶/基数)

> 线性时间排序，依赖键值范围限制

<!-- 元信息: id=non-comparison-sort · group=G-A-1 · stage=basic · priority=P1 · depth_tier=standard -->

## What · 是什么

非比较排序（non-comparison sort）利用键值的离散结构突破 n log n 下界：计数排序（counting sort）O(n+w)，w 为值域；桶排序（bucket sort）把元素按值域均分进桶、桶内再用其他排序；基数排序（radix sort）按位（关键字）多次稳定排序，LSD 从低位到高位。三者均可稳定，前提是内层排序稳定。适用前提：键值可离散化、值域/位宽可控。

## Why · 为什么

### 直觉 · Intuition

比较排序每步只知道『谁大』，信息量少；计数排序直接把值当下标存次数，一次定位。桶排序假设数据分布均匀，每个桶只装少量元素，桶内排序成本低。基数排序把一个大值域拆成 k 个小数位，每轮只需对 0..9（或 0..255）计数，d 轮线性扫描。

### 原理 · Principle

计数排序三步骤：①统计每个值出现次数 cnt[v]；②对 cnt 求前缀和（得到每个值的最后排名）；③从右向左扫描原数组，按排名回填（从右向左保证稳定性——相同值中靠后的先被放置到更靠后位置，逆序保证相对顺序）。基数排序正确性依赖『稳定』：LSD 从低位开始，每一轮稳定排序保持上一轮的高位相对序。

### 历史 · History

计数排序思想源于 1954 年 Harold Seward 对打孔卡片机的排序；基数排序最早用于卡片排序机（Hollerith 机器），是首批能在线性时间处理整数数据的算法。桶排序 1956 年由 Robert W. Floyd 等提出。现代应用：浮点数/字符串按 MSD 基数排序、后缀数组构建等。

## How · 实现

### 伪代码

```python
counting_sort(a, w):                # a 中值 ∈ [0, w]
    cnt = [0]*(w+1)
    for v in a: cnt[v] += 1
    for i in range(1, w+1): cnt[i] += cnt[i-1]
    b = [0]*len(a)
    for v in reversed(a):               # 从右向左 → 稳定
        cnt[v] -= 1
        b[cnt[v]] = v
    return b

radix_sort_lsd(a, bits=32):
    for shift in 0,8,16,24:             # 每 8 位一轮
        b = counting_sort_by_key(a, key = (x>>shift) & 0xff)
        a = b
    return a
```

### Python 实现

```python
def counting_sort(a, w):
    """计数排序：a 中元素为 [0, w] 内整数，稳定"""
    cnt = [0] * (w + 1)
    for v in a:
        cnt[v] += 1
    for i in range(1, w + 1):
        cnt[i] += cnt[i - 1]
    b = [0] * len(a)
    for v in reversed(a):
        cnt[v] -= 1
        b[cnt[v]] = v
    return b


def bucket_sort(a, num_buckets=10):
    """桶排序：值域 [0,1) 的浮点数示例，桶内用内建排序"""
    buckets = [[] for _ in range(num_buckets)]
    for v in a:
        idx = min(int(v * num_buckets), num_buckets - 1)
        buckets[idx].append(v)
    out = []
    for b in buckets:
        b.sort()
        out.extend(b)
    return out


def radix_sort_lsd(a, digits=4, base=10):
    """LSD 基数排序：逐位稳定排序，digits 为最大位数，base 为基数"""
    a = list(a)
    for d in range(digits):
        # 按当前位做稳定计数排序（值域 base）
        cnt = [0] * base
        for x in a:
            cnt[(x // (base ** d)) % base] += 1
        for i in range(1, base):
            cnt[i] += cnt[i - 1]
        b = [0] * len(a)
        for x in reversed(a):
            key = (x // (base ** d)) % base
            cnt[key] -= 1
            b[cnt[key]] = x
        a = b
    return a


if __name__ == "__main__":
    import random
    for _ in range(200):
        arr = [random.randint(0, 200) for _ in range(random.randint(0, 100))]
        assert counting_sort(arr, 200) == sorted(arr), arr
        assert radix_sort_lsd(arr, digits=3, base=10) == sorted(arr), arr
    floats = [random.random() for _ in range(500)]
    bs = bucket_sort(floats)
    assert len(bs) == len(floats) and all(bs[i] <= bs[i + 1] for i in range(len(bs) - 1))
    assert max(abs(a - b) for a, b in zip(bs, sorted(floats))) < 1e-12
    print("计数/桶/基数排序正确性 OK（200 组随机 + 浮点桶）")
    print("计数排序示例:", counting_sort([4, 2, 2, 8, 3, 3, 1], 8))

```

**PyPy 提示**: 计数排序内存受值域 w 限制，w 大（如 1e9）不可行，此时用 dict 计数或换基数排序。PyPy 下循环比 CPython 快，计数/基数排序手写完全可行；但 Python 内建 sort 是 Timsort 且常数极优，除非卡常数或明确需要线性，否则内建即可。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 计数 O(n+w)；桶平均 O(n)（均匀分布）；基数 LSD O(d(n+base)) |
| 空间 | 计数 O(w)；桶 O(n)；基数 O(n+base) |

### 局限

计数排序要求值域小；桶排序对分布敏感（集中分布退化为 O(n^2)）；基数排序适合整数/可位拆解数据。三者都是『空间换时间』。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| OI-Wiki | basic/counting-sort | 3 | 计数排序稳定写法+前缀和 | [https://oi-wiki.org/basic/counting-sort/](https://oi-wiki.org/basic/counting-sort/) |
| OI-Wiki | basic/radix-sort | 3 | 基数排序 LSD/MSD | [https://oi-wiki.org/basic/radix-sort/](https://oi-wiki.org/basic/radix-sort/) |

## Pitfalls · 易错点

- 计数排序 w 必须为已知小值域，数据需先映射到 [0,w]；负数要偏移
- 从右向左回填是稳定性关键，写成正序会破坏稳定（元素相同部分会乱序）
- 基数排序 LSD 必须每轮都用稳定排序，否则低位序被覆盖、结果错误

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/basic/counting-sort/](https://oi-wiki.org/basic/counting-sort/)
- 书籍 ✓ `CPH ch3 p42`
- OI Wiki ✓ [https://oi-wiki.org/basic/radix-sort/](https://oi-wiki.org/basic/radix-sort/)
