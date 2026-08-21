---
id: common-mistakes
name: 常见错误避免
group: G-E-4
stage: basic
priority: P0
depth_tier: deep
---

# 常见错误避免

> int溢出/未初始化/运算符优先级/scanf格式符/变量重名shadow等竞赛高频错误清单

<!-- 元信息: id=common-mistakes · group=G-E-4 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

竞赛编程中高频出现的系统性错误清单，涵盖编译错误(CE)、运行时错误(RE)、答案错误(WA)三大类。核心包括：整数溢出、未初始化变量、运算符优先级、IO格式符不匹配、变量遮蔽(shadow)、多测不清空数组、混用同步/非同步IO等。

## Why · 为什么

### 直觉 · Intuition

竞赛调试时间宝贵，90%的 WA/RE 来自同一批已知陷阱。把这些陷阱列成清单并在提交前逐项排查，比从零调试高效得多——这是经验沉淀为检查表(checklist)的经典模式。

### 原理 · Principle

错误分三层：①编译器能抓的(CE/Warning)：拼写、缺分号、类型不匹配、=与==混淆、运算符优先级、未初始化局部变量、变量遮蔽 → 开 -Wall -Wextra -Wshadow 可全部捕获。②编译器抓不到的(WA)：多测不清数组、不开 long long、图编号 0/1 混用、大小于号打反、混用 sync/async IO → 需人工审查或对拍。③环境差异：%I64d 在 Linux 下无效、Windows rand() 上限低 → 需了解平台差异。

### 历史 · History

OI Wiki 的 common-mistakes 页面由多位选手贡献，系统整理了从初学到省选级别的常见错误。经典口诀'三年 OI 一场空，不开 long long 见祖宗'广为流传。

## How · 实现

### 伪代码

```python
# 提交前检查表
1. 编译: g++ -O2 -Wall -Wextra -Wshadow -fsanitize=undefined
2. 数据类型: 中间运算是否溢出? 涉及乘法→long long
3. 数组: 多测是否清空? 大小是否够? (4N for segtree)
4. IO: scanf加&? 格式符匹配? sync_with_stdio后不混用?
5. 边界: 0/1 indexed统一? 循环上界含不含?
6. 特判: n=0? n=1? 全相同?
```

### Python 实现

```python
import sys

# === 常见错误自检工具 ===
# 模拟竞赛中的高频错误检测

def check_overflow_example():
    """演示整数溢出: Python 无此问题但 C++ 会溢出。"""
    # C++: int a = 1e9, b = 1e9; long long c = a * b;  // 溢出!
    # 正确: long long c = (long long)a * b;
    a = 10**9
    b = 10**9
    # Python 自动大整数, 不会溢出
    print(f'a * b = {a * b}')  # 1000000000000000000


def check_operator_precedence():
    """演示运算符优先级陷阱。"""
    # C++: 1 << 1 + 1  =>  1 << (1+1) = 4,  而非 (1<<1)+1 = 3
    # Python 同样: << 优先级低于 +
    wrong = 1 << 1 + 1   # = 1 << 2 = 4
    right = (1 << 1) + 1  # = 2 + 1 = 3
    print(f'1<<1+1 = {wrong} (易误为3), 正确写法 (1<<1)+1 = {right}')


def check_uninit():
    """演示未初始化变量: C++ 局部变量未初始化为垃圾值。"""
    # C++: int a; if (a > 0) ...  // a 可能为任意值
    # Python: 直接 NameError, 更安全
    a = 0  # 显式初始化是好习惯
    print(f'a = {a} (显式初始化)')


def check_multitest_clear():
    """演示多测不清空数组导致 WA。"""
    # C++ 错误: int cnt[100005]; 多组数据间不清零
    # 正确: memset(cnt, 0, sizeof(cnt)); 或用 vector 重建
    T = 3
    for t in range(T):
        # 模拟: 每组数据用局部数组, 天然清空
        cnt = [0] * 10
        for i in range(5):
            cnt[i % 10] += 1
        print(f'Test {t}: cnt[0]={cnt[0]}')  # 每次都是1


def check_io_format():
    """演示 IO 格式符不匹配。"""
    # C++: long long x; scanf("%d", &x);  // 只读4字节, 溢出!
    # 正确: scanf("%lld", &x);
    # Python: input() + int() 无此问题
    line = '1234567890123'
    x = int(line)  # Python 自动处理大整数
    print(f'x = {x} (Python无格式符问题)')


if __name__ == '__main__':
    print('=== 1. 整数溢出 ===')
    check_overflow_example()
    print('=== 2. 运算符优先级 ===')
    check_operator_precedence()
    print('=== 3. 未初始化变量 ===')
    check_uninit()
    print('=== 4. 多测不清空 ===')
    check_multitest_clear()
    print('=== 5. IO格式符 ===')
    check_io_format()
    print('=== All checks passed ===')

```

**PyPy 提示**: Python 天然避免了 C++ 的大多数错误(溢出/格式符/未初始化)，但仍需注意：①递归深度(默认1000) ②列表越缘 ③多测不清空(用局部变量天然解决) ④float 精度问题(用 Decimal 或整数运算)。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 检查表审查 O(1) per submission；对拍 O(K*N) 取决于数据规模 |
| 空间 | O(1) 检查表本身无空间开销 |

### 局限

检查表无法覆盖逻辑错误(算法思路本身错)；环境差异类错误需在目标平台实测；Python 避免了 C++ 的大部分陷阱但引入了性能瓶颈(TLE)这一新问题。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| OIWiki | contest/common-mistakes | 1 | OI Wiki 常见错误完整清单：CE/Warning/WA/RE 四大类 | [https://oi-wiki.org/contest/common-mistakes/](https://oi-wiki.org/contest/common-mistakes/) |
| General | checklist | 0 | 提交前检查表：-Wall -Wshadow、long long、数组清空、IO格式符、边界特判 | [https://oi-wiki.org/contest/common-mistakes/](https://oi-wiki.org/contest/common-mistakes/) |

## Pitfalls · 易错点

- 三年OI一场空不开long long见祖宗：中间乘法运算 a*b 即使结果赋给 long long，若 a,b 均为 int 则乘法先在 int 域溢出
- 多测不清空数组：上一组数据的残留计数/标记导致当前组 WA
- ios::sync_with_stdio(false) 后混用 scanf/cin 导致缓冲区不同步，输出错乱
- 图论题节点编号 0-indexed 与题目 1-indexed 不一致，忘记 -1 导致越界或逻辑错
- 运算符优先级：1<<n+1 被解析为 1<<(n+1) 而非 (1<<n)+1，移位低于加减
- scanf 忘记 & 取地址符 → 段错误(RE)

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/contest/common-mistakes/](https://oi-wiki.org/contest/common-mistakes/)
