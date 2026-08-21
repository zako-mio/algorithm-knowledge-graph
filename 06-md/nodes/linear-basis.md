---
id: linear-basis
name: 线性基
group: G-C-14
stage: intermediate
priority: P0
depth_tier: deep
---

# 线性基

> 异或空间基，O(n log max)插入，求最大/最小/第k小异或值

<!-- 元信息: id=linear-basis · group=G-C-14 · stage=intermediate · priority=P0 · depth_tier=deep -->

## What · 是什么

线性基是线性空间的一组基（极大线性无关组）。竞赛中常用异或线性基（GF(2)域上的基）：给定一组数，构造一组基使得任意数的子集异或都能由基的子集异或表示。性质：基中任意非空子集异或不为0；基中各数二进制最高位不同。支持查询最大/最小/第k小异或值、判断某数能否被异或表出、求异或值排名等。

## Why · 为什么

### 直觉 · Intuition

线性基好比'异或空间'的坐标系。给定一组数，它们能异或出的所有值构成一个'空间'，线性基就是这个空间的最小'坐标轴'集——用最少的基向量表示所有可能的异或值。

### 原理 · Principle

贪心插入：对每个数从高位到低位扫描，若该位为1且基中该位为空则存入，否则异或消去该位。查询最大异或时从高位到低位贪心：若异或后变大则异或。求第k小需先将基化简为行简化阶梯形。

### 历史 · History

线性基源于线性代数的基概念。OI Wiki将异或线性基作为GF(2)域上线性空间的应用。高斯消元法也可构造线性基，结果为行简化阶梯形。

## How · 实现

### 伪代码

```python
insert(x):
  for i in bits-1..0:
    if x>>i&1:
      if basis[i]==0: basis[i]=x; return True
      x ^= basis[i]
  return False

max_xor(start):
  ans = start
  for i in bits-1..0:
    if ans^basis[i] > ans: ans^=basis[i]
  return ans
```

### Python 实现

```python
class XorBasis:
    """XOR linear basis over GF(2). Supports max/min/kth XOR queries."""
    def __init__(self, bits=60):
        self.basis = [0] * bits
        self.bits = bits
        self.size = 0

    def insert(self, x):
        """Insert x into the basis. Returns True if rank increased."""
        for i in range(self.bits - 1, -1, -1):
            if not (x >> i & 1):
                continue
            if self.basis[i] == 0:
                self.basis[i] = x
                self.size += 1
                return True
            x ^= self.basis[i]
        return False

    def max_xor(self, start=0):
        """Maximum XOR of any subset, starting from given value."""
        ans = start
        for i in range(self.bits - 1, -1, -1):
            if (ans ^ self.basis[i]) > ans:
                ans ^= self.basis[i]
        return ans

    def min_xor(self):
        """Minimum nonzero XOR of any subset."""
        for i in range(self.bits):
            if self.basis[i] != 0:
                return self.basis[i]
        return 0

    def contains(self, x):
        """Check if x can be represented as XOR of some subset."""
        for i in range(self.bits - 1, -1, -1):
            if (x >> i & 1) and self.basis[i]:
                x ^= self.basis[i]
        return x == 0

    def kth_xor(self, k):
        """k-th smallest XOR value (1-indexed). Requires reduction first."""
        self._reduce()
        ans = 0
        cnt = 0
        for i in range(self.bits):
            if self.basis[i]:
                if (k >> cnt) & 1:
                    ans ^= self.basis[i]
                cnt += 1
        return ans

    def _reduce(self):
        """Reduce basis to simplified row echelon form."""
        for i in range(self.bits - 1, -1, -1):
            if self.basis[i]:
                for j in range(i + 1, self.bits):
                    if self.basis[j] & (1 << i):
                        self.basis[j] ^= self.basis[i]

if __name__ == "__main__":
    xb = XorBasis(20)
    for x in [633, 211, 169, 841, 1008]:
        xb.insert(x)
    assert xb.max_xor() > 0
    assert xb.contains(633)
    assert xb.contains(633 ^ 211)
    assert not xb.contains(633 ^ 211 ^ 999)  # 999 not in span
    # Empty basis
    xb2 = XorBasis(10)
    assert xb2.max_xor(5) == 5  # start value when basis empty
    assert xb2.min_xor() == 0
    # k-th XOR
    xb3 = XorBasis(10)
    for x in [1, 2, 4]:
        xb3.insert(x)
    xb3._reduce()
    # All XOR values: 0,1,2,3,4,5,6,7 sorted
    assert xb3.kth_xor(1) == 1
    assert xb3.kth_xor(2) == 2
    assert xb3.kth_xor(4) == 4
    print("linear-basis: ALL TESTS PASSED")

```

**PyPy 提示**: 位运算在PyPy上很快。bits取60覆盖long long范围。求第k小需先_reduce化简。Python大整数位运算无溢出问题。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 插入O(log maxV)，查询O(log maxV) |
| 空间 | O(log maxV) |

### 局限

仅适用于GF(2)域（异或）。实数线性基需不同实现。第k小查询需先化简基。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3812 | 4 | 子集异或最大值模板题 | [https://www.luogu.com.cn/problem/P3812](https://www.luogu.com.cn/problem/P3812) |
| Luogu | P4151 | 6 | 线性基+图论求路径异或最大值 | [https://www.luogu.com.cn/problem/P4151](https://www.luogu.com.cn/problem/P4151) |
| Luogu | P3212 | 7 | 线性基在概率期望中的应用 | [https://www.luogu.com.cn/problem/P3212](https://www.luogu.com.cn/problem/P3212) |

## Pitfalls · 易错点

- 插入顺序不影响基的大小（rank），但影响基的具体值
- 求第k小前必须调用_reduce化简为简化阶梯形
- 空基的最大异或查询返回start值本身
- min_xor返回最小非零异或值，空集异或为0不计

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/linear-algebra/basis/](https://oi-wiki.org/math/linear-algebra/basis/)
- 洛谷 ✓ [https://www.luogu.com.cn/problem/P3812](https://www.luogu.com.cn/problem/P3812)
