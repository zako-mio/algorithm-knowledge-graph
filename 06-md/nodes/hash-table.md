---
id: hash-table
name: 哈希表（散列表）
group: G-A-10
stage: basic
priority: P0
depth_tier: deep
---

# 哈希表（散列表）

> key-value 映射，哈希函数+冲突处理（开链/开放寻址），期望 O(1) 插入/查找

<!-- 元信息: id=hash-table · group=G-A-10 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

哈希表（Hash Table / 散列表）以『key-value』形式存储数据：将任意类型的键 key 通过哈希函数 f(key) 映射到一个整型下标，从而把记录存到数组 a[f(key)] 上，实现平均 O(1) 的插入、删除与查找。核心三要素：① 哈希函数——要易于计算且让索引尽量均匀（常见取模大质数、字符串多项式哈希、双哈希）；② 冲突处理——不同 key 映射到同一槽位时的解决策略：开散列（拉链法，每个槽一条链表）与闭散列（开放寻址，线性/二次探查）；③ 装载因子——开散列期望链长 ≈ n/M。Python 内建 dict/set 即哈希表，竞赛中手写哈希表常用于『值域巨大需离散化/去重/快速查找』或『字符串映射』，以及替代 map 追求更低常数。

## Why · 为什么

### 直觉 · Intuition

把‘数组下标必须是连续整数’的限制打破：哈希函数把巨大的键空间（如 1e18 整数、任意字符串）压缩到一块合理大小的连续桶上。就像图书馆按书号首字母分区——同区多本书就摞在一起（链表），找书时先定位区域再在摞里翻。均匀性决定了性能：分布越均匀，每个桶越空，查找越快。

### 原理 · Principle

开散列（拉链法）：head[h] 存桶头，冲突节点用 next 指针串成链表，插入头插 O(1)，查找需扫描整条链，期望链长 n/M → 期望 O(1+n/M)，M 取大质数保证分布。字符串哈希：s 视作 127 进制数，x = Σ s_i·127^i，对 2^64 自然溢出取模（C++ unsigned long long）；对抗构造冲突可双哈希（两模数）。闭散列（线性探查）：冲突时查下一个槽位，查询沿探查序列走。注意：哈希只能保证高概率不冲突，可被构造卡到退化 O(n)（如取模质数选错被 2^p 倍数命中同槽）。

### 历史 · History

哈希思想可追溯至 1950 年代（Hans Peter Luhn 1953 提出 IBM 内部检索）；『散列』『拉链法』等术语 1953 年由 Peterson 系统化。1960s 开放寻址与双散列相继成熟。如今哈希表是现代编程语言内建映射/字典的标准实现。OI Wiki《哈希表》页给出拉链法与闭散列模板，以及字符串哈希的双哈希抗冲突方案。

## How · 实现

### 伪代码

```python
# 开散列(拉链法)
def hash(key): return (key % M + M) % M   # M 大质数
def get(key):
  for p in chain[hash(key)]:
    if p.key == key: return p.value
  return MISSING
def set(key, value):
  h = hash(key)
  for p in chain[h]:
    if p.key == key: p.value = value; return
  chain[h].prepend(key, value)
# 字符串哈希
def hash_str(s):
  h = 0
  for c in s: h = (h * B + ord(c)) % MOD   # B=131/13331, MOD 大质数
  return h
```

### Python 实现

```python
_MISS = object()


class HashTable:
    """哈希表(开散列/拉链法): key -> value.
    哈希函数取模大质数, 冲突用链表(数组实现, 避免 Python 对象开销)."""
    def __init__(self, mod=100003, seed=131):
        self.mod = mod
        self.seed = seed
        self.head = [None] * mod        # 每条链的链表头(索引)
        self.keys = []
        self.vals = []
        self.next = []
        self._live = set()              # 当前存活 key (支持删除)

    def _hash_int(self, k):
        return (k % self.mod + self.mod) % self.mod

    def _hash_str(self, s):
        h = 0
        for ch in s:
            h = (h * self.seed + ord(ch)) % self.mod
        return h

    def _hash(self, key):
        if isinstance(key, int): return self._hash_int(key)
        if isinstance(key, str): return self._hash_str(key)
        if isinstance(key, tuple): return self._hash_str(str(key))
        raise TypeError

    def set(self, key, value):
        h = self._hash(key)
        i = self.head[h]
        while i is not None:
            if self.keys[i] == key:
                self.vals[i] = value
                return value
            i = self.next[i]
        if key not in self._live:
            self.keys.append(key); self.vals.append(value); self.next.append(self.head[h])
            self.head[h] = len(self.keys) - 1
            self._live.add(key)
        return value

    def get(self, key, default=None):
        h = self._hash(key)
        i = self.head[h]
        while i is not None:
            if self.keys[i] == key:
                return self.vals[i]
            i = self.next[i]
        return default

    def __contains__(self, key):
        return self.get(key, _MISS) is not _MISS

    def __getitem__(self, key):
        v = self.get(key, None)
        if v is None: raise KeyError(key)
        return v

    def __setitem__(self, key, value):
        self.set(key, value)

    def __len__(self):
        return len(self._live)

    def __delitem__(self, key):
        if key in self._live:
            self._live.discard(key)


if __name__ == "__main__":
    ht = HashTable()
    # 整数键
    for i in range(2000):
        ht[i * 31 % 100000] = i
    assert ht.get(31 * 5 % 100000) == 5
    assert ht.get(9999999) is None
    # 字符串键
    ht["apple"] = 1; ht["banana"] = 2
    ht["apple"] = 3
    assert ht["apple"] == 3 and ht["banana"] == 2
    assert "apple" in ht and "pear" not in ht
    # 与 Python dict 交叉验证 (独立实例, 避免与上面初始插入重叠)
    import random
    random.seed(11)
    ht2, d = HashTable(), {}
    for _ in range(5000):
        k = random.randint(-10**9, 10**9)
        if random.random() < 0.3 and k in d:
            del d[k]
            del ht2[k]
        else:
            d[k] = random.randint(0, 10**6)
            ht2[k] = d[k]
    for k, v in d.items():
        assert ht2[k] == v, k
    assert len(ht2) == len(d), (len(ht2), len(d))
    print("hash-table: all tests passed")

```

**PyPy 提示**: PyPy 下 Python 内建 dict 本身极快，一般无需手写；若手写，用 list 数组+int 链表头（避免对象）更快。字符串哈希取模运算是瓶颈，B 与 MOD 取大质数（如 1e9+7）时注意 h*B 溢出为 Python 大整数（慢）；竞赛中常改双哈希/多质数并对 2^61-1 取模。勿用 random 做哈希函数（每次重跑结果不同）。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 期望 O(1) 插入/查找/删除（装载因子恒定时）；最坏 O(n) |
| 空间 | O(n+M) |

### 局限

① 期望保证非最坏保证：数据可被恶意构造（选模数同余序列）卡成 O(n)；② 字符串单哈希对构造数据有碰撞风险，需双哈希；③ 删除用墓碑/懒删在开放寻址中易引坑；④ 不能像 dict 保证遍历有序；⑤ 值域离散化、可持久化等需求应另选平衡树/线段树。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P4305 | 2 | JLOI2011 不重复数字：哈希表去重/判存在，OI Wiki 例题 | [https://www.luogu.com.cn/problem/P4305](https://www.luogu.com.cn/problem/P4305) |
| LeetCode.cn | 1 | 2 | 两数之和：哈希表 O(1) 查找互补数的经典入门 | [https://leetcode.cn/problems/two-sum/](https://leetcode.cn/problems/two-sum/) |
| LeetCode.cn | 706 | 2 | 设计哈希映射：手写开散列/闭散列结构模板题 | [https://leetcode.cn/problems/design-hashmap/](https://leetcode.cn/problems/design-hashmap/) |

## Pitfalls · 易错点

- 取模质数被命中（key 全是模数的倍数 → 全部同槽退化为链表）
- 负 key 直接 % 得到负下标，需 (k%M+M)%M
- 字符串哈希基准/base 未处理好（含 0 位、大小写边界）导致碰撞
- 删除后开放寻址查询断链（需墓碑或重排）
- 装载因子过高不扩容导致期望退化成 O(n)
- 哈希函数不可复现（用 random）导致相同输入不同结果

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/hash/](https://oi-wiki.org/ds/hash/)
- 书籍 ✓ `CPH ch2.3 (哈希表内建于 dict), ch26 字符串哈希`
- article ✓ [https://en.wikipedia.org/wiki/Hash_table](https://en.wikipedia.org/wiki/Hash_table)
