---
id: balanced-ternary
name: 平衡三进制
group: G-C-18
stage: intermediate
priority: P3
depth_tier: brief
---

# 平衡三进制

> 用 {-1,0,1} 表示的三进制，负数无需符号位；2 进位成 Z 并高位加 1，用于天平称重等问题

<!-- 元信息: id=balanced-ternary · group=G-C-18 · stage=intermediate · priority=P3 · depth_tier=brief -->

## What · 是什么

平衡三进制（balanced/symmetric ternary）：数码为 -1(记 Z)、0、1，基仍为 3。十进制 5=1ZZ, 6=1Z0, 7=1Z1, 8=10Z, 9=100；负数即正数数码翻转（1↔Z），如 -1=Z, -5=Z11。转换：先写成普通三进制，从低位迭代，遇 2 变成 Z 并向高位进 1（即 x+=1 再继续），遇 3 变 0 进 1。反向：按位权 3^i 加权求和。应用：用一套 {1,3,9,...} 砝码称量任意整数质量的问题——称量方案等价于平衡三进制表示。

## Why · 为什么

### 直觉 · Intuition

普通三进制每位 {0,1,2}，2 与 -1 模 3 同余（2 ≡ -1 mod 3），所以把 2 写成 -1 并进一位，就是「用借位的方式编码负数」，让一个数字本身就能带符号。砝码问题：左盘放物、砝码可放两边，每个 3^k 砝码只有「左/右/不用」三态 → 天然对应 {-1,0,1}。

### 原理 · Principle

转换算法（普通三进制 → 平衡三进制）：对每个十进制数 x，循环 r=x%3, x//=3；若 r==2 则 r='Z' 且 x+=1；若 r==1 记 '1'；r==0 记 '0'。正确性：2·3^i ≡ -1·3^i (mod 3^(i+1))，把 2 替换为 Z(-1) 后向高位 +1 补偿，数值不变。负数直接翻转所有数码（每位的符号反转）。反向加权：digit·3^i 求和（Z=-1）。

### 历史 · History

对称/平衡三进制由数学家及早期计算机实践提出：苏联 1958 年建造的 Setun 计算机即采用平衡三进制。它在「用固定砝码称任意重量」的经典趣题中出现，OI Wiki 与 CP-Alg 均收录。竞赛中直接考的题极少，主要作为数制与构造技巧储备。

## How · 实现

### 伪代码

```python
def to_balanced_ternary(x):
    if x == 0: return '0'
    neg = x < 0
    x = abs(x)
    digits = []
    while x:
        r = x % 3; x //= 3
        if r == 2:
            digits.append('Z'); x += 1
        elif r == 1:
            digits.append('1')
        else:
            digits.append('0')
    s = ''.join(reversed(digits))
    return s.translate(str.maketrans('1Z', 'Z1')) if neg else s

def from_balanced_ternary(s):
    val, p = 0, 1
    for ch in reversed(s):
        val += {'0': 0, '1': 1, 'Z': -1}[ch] * p
        p *= 3
    return val
```

### Python 实现

```python
def to_balanced_ternary(x):
    if x == 0:
        return '0'
    neg = x < 0
    x = abs(x)
    digits = []
    while x:
        r = x % 3
        x //= 3
        if r == 2:
            digits.append('Z')
            x += 1
        elif r == 1:
            digits.append('1')
        else:
            digits.append('0')
    s = ''.join(reversed(digits))
    if neg:
        s = s.translate(str.maketrans('1Z', 'Z1'))
    return s


def from_balanced_ternary(s):
    val = 0
    p = 1
    mp = {'0': 0, '1': 1, 'Z': -1}
    for ch in reversed(s):
        val += mp[ch] * p
        p *= 3
    return val


def main():
    table = {0: '0', 1: '1', 2: '1Z', 3: '10', 4: '11', 5: '1ZZ',
             6: '1Z0', 7: '1Z1', 8: '10Z', 9: '100', -1: 'Z', -2: 'Z1',
             -3: 'Z0', -4: 'ZZ', -5: 'Z11'}
    for x, s in table.items():
        assert to_balanced_ternary(x) == s, (x, to_balanced_ternary(x))
        assert from_balanced_ternary(s) == x
    for x in range(-200, 201):
        assert from_balanced_ternary(to_balanced_ternary(x)) == x
    print("balanced-ternary OK")


if __name__ == "__main__":
    main()

```

**PyPy 提示**: 转换循环 O(log_3 x) 每步 % 与 //，PyPy 下很快。平衡三进制题极少，如出现多半是构造/数位题，注意 Python int 无符号位困扰。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 双向转换 O(log_3 \|x\|) |
| 空间 | O(log_3 \|x\|) |

### 局限

竞赛中直接考查频率低；砝码称重问题用平衡三进制建模后可能还需组合数学（计数不同称法数）。只支持整数，不处理小数。

## Pitfalls · 易错点

- 2→Z 后必须向高位进 1，漏加会导致结果偏小
- 负数翻转数码前先转绝对值再算，正负两处别弄反
- Z 只是 -1 的书写记号，别当成 ASCII 字符参与数值计算
- 循环退出条件：处理完 x==0 后若因进位又产生更高位要自然继续

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/math/numeral-sys/balanced-ternary/](https://oi-wiki.org/math/numeral-sys/balanced-ternary/)
- CP-Algorithms ✓ [https://cp-algorithms.com/algebra/balanced-ternary.html](https://cp-algorithms.com/algebra/balanced-ternary.html)
