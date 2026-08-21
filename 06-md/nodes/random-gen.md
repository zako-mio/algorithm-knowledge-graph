---
id: random-gen
name: 随机数据生成
group: G-E-4
stage: basic
priority: P0
depth_tier: deep
---

# 随机数据生成

> 对拍用随机数据生成器：mt19937/random模块，testlib generator框架

<!-- 元信息: id=random-gen · group=G-E-4 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

随机数据生成器是对拍（stress testing）的核心组件：用确定种子的伪随机数生成器产生符合题目约束的测试数据，喂给待测解和暴力解，反复运行直到发现不一致的输出。Python 中用 random.Random(seed) 或 random.SystemRandom()，C++ 中用 mt19937。

## Why · 为什么

### 直觉 · Intuition

人脑设计的测试数据容易遗漏边界，随机生成器可以穷尽大量组合，在有限时间内覆盖到人想不到的 corner case。固定种子保证可复现——一旦发现错误，同一种子可重现调试。

### 原理 · Principle

伪随机数生成器(PRNG)基于确定性算法生成统计上近似均匀的序列。梅森缠绕器(MT19937)周期达 2^19937-1，Python random 模块底层即用 MT19937。对拍流程：①写暴力解(正确但慢) ②写生成器(产生合法输入) ③写对拍脚本(循环: 生成→两解各跑→比对输出→不一致则停) ④发现差异后用同种子复现调试。

### 历史 · History

MT19937 由松本真・西村拓士(1998)提出，因其周期为梅森素数 M19937=2^19937-1 而得名。C++11 起以 std::mt19937 标准化。对拍(stress testing)是竞赛选手定位 WA/TLE 的标准方法论，testlib 框架为其提供了系统化支持。

## How · 实现

### 伪代码

```python
# 生成器
gen():
  n = randint(1, MAXN)
  print(n)
  for i in range(n):
    print(randint(1, MAXV))

# 对拍循环
for seed in range(100000):
  gen(seed)          # 固定种子生成数据
  out1 = run(solution)   # 待测解
  out2 = run(brute)     # 暴力解
  if out1 != out2:
    print(seed); break   # 记录失败种子
```

### Python 实现

```python
import random
import subprocess
import sys
import os

def gen_input(seed, max_n=20, max_val=100):
    """用固定种子生成一组测试数据(数组求和题示例)。"""
    rng = random.Random(seed)
    n = rng.randint(1, max_n)
    arr = [rng.randint(1, max_val) for _ in range(n)]
    lines = [str(n)]
    lines.append(' '.join(map(str, arr)))
    return '\n'.join(lines) + '\n'

def brute_solve(data):
    """暴力解: 直接求和。"""
    lines = data.strip().split('\n')
    n = int(lines[0])
    arr = list(map(int, lines[1].split()))
    return str(sum(arr))

def fast_solve(data):
    """待测解: 同样求和(这里用内置sum做演示)。"""
    lines = data.strip().split('\n')
    n = int(lines[0])
    arr = list(map(int, lines[1].split()))
    return str(sum(arr))

def stress_test(max_iters=1000):
    """对拍主循环: 随机生成数据 -> 两解各跑 -> 比对输出。"""
    for seed in range(max_iters):
        data = gen_input(seed)
        out_fast = fast_solve(data)
        out_brute = brute_solve(data)
        if out_fast != out_brute:
            print(f'MISMATCH at seed={seed}')
            print(f'Input:\n{data}')
            print(f'Fast:   {out_fast}')
            print(f'Brute:  {out_brute}')
            return False
    print(f'All {max_iters} tests passed!')
    return True


if __name__ == '__main__':
    # 演示生成器输出
    print('=== Generator demo (seed=42) ===')
    print(gen_input(42), end='')
    print('=== Stress test ===')
    stress_test(500)

```

**PyPy 提示**: PyPy 对 random.Random 的 MT19937 实现性能与 CPython 接近；subprocess 调用外部程序是瓶颈，建议对拍时直接在进程内 import 两个解函数而非 subprocess；max_iters 可设 10000+ 充分覆盖。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 生成 O(N) per case；对拍 O(K*N) 其中 K=迭代次数；整体取决于暴力解复杂度 |
| 空间 | O(N) per generated case |

### 局限

生成器必须严格满足题目约束(值域/图连通性等)，否则产生非法数据导致误报；暴力解必须绝对正确否则对拍无意义；随机数据可能无法覆盖某些需要特殊构造的 case(如完全图、链)，需辅以构造性数据。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Codeforces | blog/61587 | 0 | Don't use rand(): CF 经典博客，推荐 mt19937 替代 rand() | [https://codeforces.com/blog/entry/61587](https://codeforces.com/blog/entry/61587) |
| OIWiki | misc/random | 1 | OI Wiki 随机数生成全谱：rand/mt19937/LCG/xorshift/splitmix | [https://oi-wiki.org/misc/random/](https://oi-wiki.org/misc/random/) |

## Pitfalls · 易错点

- Python random.seed(0) 可复现，但跨 Python 版本序列可能不同(CPython 实现细节)；对拍双方须用同版本
- rand()%n 不均匀(n 不整除 RAND_MAX 时低位偏多)；Python random.randint 内部已做均匀化
- Windows 下 C++ rand() 上限仅 2^15-1，需 (rand()<<15\|rand()) 拼接；Python 无此问题
- 对拍时忘记 fflush(stdout) 导致交互式对拍死锁；纯输出式对拍无此问题

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/misc/random/](https://oi-wiki.org/misc/random/)
- OI Wiki ✓ [https://oi-wiki.org/tools/testlib/generator/](https://oi-wiki.org/tools/testlib/generator/)
- 博客 ✓ [https://codeforces.com/blog/entry/61587](https://codeforces.com/blog/entry/61587)
