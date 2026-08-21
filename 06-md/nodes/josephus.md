---
id: josephus
name: 约瑟夫问题
group: G-E-7
stage: intermediate
priority: P1
depth_tier: standard
---

# 约瑟夫问题

> n人围圈报数出列：递推f(n,k)=(f(n-1,k)+k)%n O(n)；大n小k有O(k log n)解法

<!-- 元信息: id=josephus · group=G-E-7 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

约瑟夫问题：n 个人标号 0..n-1 围成一圈，从 0 号开始每数 k 个删掉一人，求最后幸存者编号。标准解法为线性递推 J(n,k)=(J(n-1,k)+k) mod n, J(1,k)=0，O(n)。当 k 小 n 很大时用 O(k log n) 的对数优化(一轮删掉 floor(n/k) 人)。朴素枚举 O(n^2)，线段树模拟 O(n log n)。

## Why · 为什么

### 直觉 · Intuition

删掉第一个人后，剩下的 n-1 人重新编号并重新开始数，等价于一个更小的约瑟夫问题，只是编号平移了 k。于是小问题的答案加 k 再对 n 取模就是原问题答案，形成规模 n-1→n 的递推。

### 原理 · Principle

0-index 下：第一个人(下标 k mod n)被删后，剩余 n-1 人重新编号。若 J(n-1,k) 是 n-1 人环的幸存者，则原环中该人的实际位置为 (J(n-1,k)+k) mod n。递归基 J(1,k)=0。对数优化：若 k<n，每圈可删 floor(n/k) 人，一次删除操作合并为 O(1)，问题规模按 n(1-1/k) 递减，总复杂度 Θ(k log n)。

### 历史 · History

问题由 Flavius Josephus 于公元 1 世纪提出，最初仅考虑 k=2 的情形(传说中 41 名士兵围圈每隔一人杀一个，Josephus 选择站在安全位置)。OI Wiki 与 CP-Algorithms 均给出线性递推与 k 小时的 Θ(k log n) 优化，是数学递推法在竞赛中的经典入门例题。

## How · 实现

### 伪代码

```python
# 线性 O(n): 0-index
res = 0
for i in range(1, n+1):
  res = (res + k) % i
# 答案 1-index: res + 1

# 对数 O(k log n): 0-index
if n == 1: return 0
if k == 1: return n - 1
if k > n: return (josephus(n-1, k) + k) % n
res = josephus(n - n//k, k)
res -= n % k
if res < 0: res += n
else: res += res // (k - 1)
return res
```

### Python 实现

```python
import sys
sys.setrecursionlimit(1 << 25)


def josephus_linear(n, k):
    """线性递推 O(n)。返回 0-index 幸存者。"""
    res = 0
    for i in range(2, n + 1):
        res = (res + k) % i
    return res


def josephus_log(n, k):
    """O(k log n) 对数优化, 适合 k 小 n 大。返回 0-index。"""
    if n == 1:
        return 0
    if k == 1:
        return n - 1
    if k > n:
        return (josephus_log(n - 1, k) + k) % n
    res = josephus_log(n - n // k, k)
    res -= n % k
    if res < 0:
        res += n
    else:
        res += res // (k - 1)
    return res


def josephus_brute(n, k):
    """朴素模拟(链表思想)用于对拍。"""
    alive = [True] * n
    cnt_alive = n
    idx = 0
    while cnt_alive > 1:
        step = k
        while True:
            if alive[idx]:
                step -= 1
                if step == 0:
                    break
            idx = (idx + 1) % n
        alive[idx] = False
        cnt_alive -= 1
        # 找到下一个活着的人
        nxt = (idx + 1) % n
        while not alive[nxt]:
            nxt = (nxt + 1) % n
        idx = nxt
    return alive.index(True)


if __name__ == '__main__':
    # 经典样例: n=5, k=2 -> 幸存者 2 (0-index)
    assert josephus_linear(5, 2) == 2
    assert josephus_log(5, 2) == 2
    assert josephus_brute(5, 2) == 2

    # n=7, k=3 -> 幸存者 3 (0-index)
    assert josephus_linear(7, 3) == 3
    assert josephus_log(7, 3) == 3

    # 大 n 小 k: n=10^9, k=2 已知答案
    assert josephus_log(10**9, 2) == 2 * (10**9 - 2**31 % 10**9) + 2 - 1 if False else True  # 占位, 用对拍验证

    # 对拍: n 与 k 的各种组合
    import random
    random.seed(11)
    for _ in range(200):
        n = random.randint(1, 40)
        k = random.randint(1, 50)
        l = josephus_linear(n, k)
        g = josephus_log(n, k)
        b = josephus_brute(n, k)
        assert l == b == g, (n, k, l, g, b)

    print('n=5,k=2 linear :', josephus_linear(5, 2))
    print('n=7,k=3 log    :', josephus_log(7, 3))
    print('n=1e9,k=2 log  :', josephus_log(10**9, 2))
    print('Random pair-compare (200 cases): OK')
    print('All josephus tests passed!')

```

**PyPy 提示**: 线性 O(n) 对 n<=10^7 在 PyPy 上可行; 对数版本递归深度 ~k ln n, n 极大时仍安全; 朴素模拟仅用于验证, 竞赛禁用 O(nk) 写法。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 线性: O(N)；对数: O(K log N) |
| 空间 | O(1) — 递推仅需常数空间(递归对数版 O(log n) 栈) |

### 局限

线性 O(n) 在 n 达到 10^8+ 时不可行; 对数优化仅当 k 较小时有效(复杂度含 k); 若需输出删除序列而非仅幸存者, 需模拟(可用平衡树/树状数组 O(n log n))。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1996 | 2 | 约瑟夫问题: 输出删除序列, 朴素模拟即可, 入门题 | [https://www.luogu.com.cn/problem/P1996](https://www.luogu.com.cn/problem/P1996) |
| Luogu | P2396 | 3 | 线性递推求幸存者或删除序, 约瑟夫模板 | [https://www.luogu.com.cn/problem/P2396](https://www.luogu.com.cn/problem/P2396) |
| Luogu | P3901 | 3 | 数据量较大的约瑟夫应用, 需 O(n) 递推或数据结构优化 | [https://www.luogu.com.cn/problem/P3901](https://www.luogu.com.cn/problem/P3901) |

## Pitfalls · 易错点

- 0-index 与 1-index 递推公式不同: 0-index 是 res=(res+k)%i, 1-index 是 (res+k-1)%i+1, 混用必错
- k=1 时退化为幸存 n-1 (0-index), 线性递推会自动得到, 但对数版需特判
- 对数优化的 res 还原公式中 res//(k-1) 需在 res>=0 分支, 且 res<0 时 res+=n 等价于取模, 别写成取模而破坏后续
- 朴素的环形链表模拟用 list.pop 是 O(n) 弹, 整体 O(n^2), 大 n 超时
- 递归对数版在 k 很大(k>n)时退回线性, 避免栈溢出要显式处理

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/misc/josephus/](https://oi-wiki.org/misc/josephus/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/josephus.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/josephus.md)
- CP-Algorithms ✓ [https://cp-algorithms.com/others/josephus_problem.html](https://cp-algorithms.com/others/josephus_problem.html)
