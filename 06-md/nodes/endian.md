---
id: endian
name: 字节序
group: G-E-7
stage: intermediate
priority: P2
depth_tier: standard
---

# 字节序

> 大端序/小端序差异，网络字节序转换，二进制文件读写时需注意

<!-- 元信息: id=endian · group=G-E-7 · stage=intermediate · priority=P2 · depth_tier=standard -->

## What · 是什么

字节序(Byte Order / Endianness)描述多字节对象在内存中的字节排列方式：小端序(Little Endian)从最低有效字节到最高有效字节存放，大端序(Big Endian)相反。例如 0x01234567 小端存 67 45 23 01，大端存 01 23 45 67。网络协议规定统一使用网络字节序(大端)；跨平台二进制文件/协议/内存映射(如 mmap 解析)若不转换字节序会产生错误数据。

## Why · 为什么

### 直觉 · Intuition

CPU 设计选择把低字节放低地址(小端, x86/ARM)或高字节放低地址(大端, Sun/PPC 传统, 网络)只是约定。跨端传输时，同一字节序列在两台机器上解读出的整数不同，因此必须有约定与转换工具(htonl/ntohl 等)。

### 原理 · Principle

小端序：地址递增方向先存低位字节(0x100:67, 0x101:45, 0x102:23, 0x103:01)。大端序反之。术语出自《格列佛游记》中关于'从小端还是大端剥鸡蛋'的政治讽刺。判断本机字节序可通过 memcpy 到字符数组观察首字节，或用 struct.pack('<I', 1)。

### 历史 · History

字节序术语'endian'源于 Swift《格列佛游记》的小人国纷争。OI Wiki 在 misc 页面介绍该概念，说明其在网络编程与二进制数据处理中的重要性。现代 x86/ARM 小端主导，但网络字节序仍固定大端，竞赛中解析二进制数据/位掩码题(如逆向题)会考到。

## How · 实现

### 伪代码

```python
# 判断本机字节序(小端返回 'little')
import sys
print(sys.byteorder)   # 'little' 或 'big'

# 整数 <-> 字节转换
import struct
# 小端编码
packed_le = struct.pack('<I', 0x01234567)
# 大端编码(网络字节序)
packed_be = struct.pack('>I', 0x01234567)

# 手工验证: 小端 67 45 23 01, 大端 01 23 45 67
```

### Python 实现

```python
import struct
import sys


def machine_endianness():
    """返回本机字节序: 'little' 或 'big'。"""
    return sys.byteorder


def little_endian_bytes(value):
    """将 int 编码为小端字节序列(演示)。"""
    return struct.pack('<I', value)


def big_endian_bytes(value):
    """将 int 编码为大端字节序列(网络字节序)。"""
    return struct.pack('>I', value)


def parse_binary_file(path, endian='<'):
    """按指定字节序读取二进制文件中的整数序列(演示)。
    endian: '<' 小端, '>' 大端。
    """
    with open(path, 'rb') as f:
        data = f.read()
    nums = []
    for i in range(0, len(data) - 3, 4):
        nums.append(struct.unpack(endian + 'I', data[i:i + 4])[0])
    return nums


def swap_endian32(x):
    """手工反转 32 位整数字节序(小端<->大端)。"""
    return ((x & 0x000000FF) << 24) | ((x & 0x0000FF00) << 8) | \
           ((x & 0x00FF0000) >> 8) | ((x & 0xFF000000) >> 24)


if __name__ == '__main__':
    val = 0x01234567
    le = little_endian_bytes(val)
    be = big_endian_bytes(val)

    assert machine_endianness() in ('little', 'big')
    # 标准验证: 小端序列首字节=低位 0x67, 大端首字节=高位 0x01
    assert le == b'\x67\x45\x23\x01', le
    assert be == b'\x01\x23\x45\x67', be

    # 双端互相转换一致
    assert struct.unpack('<I', le)[0] == val
    assert struct.unpack('>I', be)[0] == val
    assert swap_endian32(val) == 0x67452301
    assert swap_endian32(0x67452301) == val
    assert swap_endian32(swap_endian32(val)) == val

    # 字节序说明
    print('machine endian:', machine_endianness())
    print('0x%08X little-endian bytes: %s' % (val, le.hex()))
    print('0x%08X big-endian bytes   : %s' % (val, be.hex()))
    print('swap_endian32(0x%08X) = 0x%08X' % (val, swap_endian32(val)))

    # 写二进制文件再按不同字节序解析(模拟跨平台)
    import tempfile, os
    path = os.path.join(tempfile.gettempdir(), 'endian_demo.bin')
    with open(path, 'wb') as f:
        f.write(struct.pack('<I', 1))
        f.write(struct.pack('<I', 0x00FF00FF))
        f.write(struct.pack('<I', 0x80000000))
    le_nums = parse_binary_file(path, '<')
    be_nums = parse_binary_file(path, '>')
    assert le_nums == [1, 0x00FF00FF, 0x80000000], le_nums
    assert be_nums != le_nums  # 用错字节序会得到不同整数
    print('binary parse little-endian:', [hex(x) for x in le_nums])
    print('binary parse big-endian   :', [hex(x) for x in be_nums])
    os.remove(path)
    print('All endian tests passed!')

```

**PyPy 提示**: struct.pack/unpack 走 C 层, 性能良好; 解析大规模二进制用 mmap + memoryview 更快; 位运算交换字节序在 Python 大整数上也可用 int.to_bytes/from_bytes。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(K) — 转换/解析与数据规模线性 |
| 空间 | O(1) — 逐字节处理或 O(K) 缓冲 |

### 局限

跨平台代码需显式指定字节序(不要依赖 sys.byteorder 的默认行为); Python 的 struct 默认用本机字节序+对齐, 跨端需显式 < 或 >; 网络字节序固定大端, 与常见 x86 小端不同, 必须转换; 手写 swap 时注意掩码位宽(32/64)。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| LeetCode | 190 | 2 | 颠倒二进制位: 位运算逐位翻转, 字节序/位序理解基础 | [https://leetcode.cn/problems/reverse-bits/](https://leetcode.cn/problems/reverse-bits/) |
| LeetCode | 191 | 1 | 位1的个数: 无符号整数位操作, 与字节序无关的位计数 | [https://leetcode.cn/problems/number-of-1-bits/](https://leetcode.cn/problems/number-of-1-bits/) |
| AtCoder | abc333_a | 1 | 小模拟题: 演示位数与整数的直观关系 | [https://atcoder.jp/contests/abc333/tasks/abc333_a](https://atcoder.jp/contests/abc333/tasks/abc333_a) |

## Pitfalls · 易错点

- 网络字节序是固定的大端, 与 x86 小端不同, 网络协议解析必先 ntohl/ntohl 转换
- struct 默认按本机字节序与对齐填充, 跨平台必须显式 '<' '>' '!' (network=!)
- 手写 swap_endian 的掩码要按位宽写对(0xFF000000 等), 32 位与 64 位不同
- 二进制文件用错字节序解析出的整数'合理但错误', 无异常抛出, 需对照协议文档验证
- Python int 无符号化: 解析无符号整数用 struct 的 I/L, 别把高位当符号

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/misc/endianness/](https://oi-wiki.org/misc/endianness/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/endianness.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/endianness.md)
- web ✓ [https://en.wikipedia.org/wiki/Endianness](https://en.wikipedia.org/wiki/Endianness)
