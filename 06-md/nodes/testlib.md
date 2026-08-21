---
id: testlib
name: testlib对拍框架
group: G-E-9
stage: intermediate
priority: P1
depth_tier: standard
---

# testlib对拍框架

> testlib.h：generator/validator/checker/interactor四件套，出题与对拍的标准库，与Polygon完全兼容

<!-- 元信息: id=testlib · group=G-E-9 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

Testlib是C++编写算法竞赛出题/评测相关程序的辅助库，仅由testlib.h一个头文件组成。它提供四个核心组件：Generator(数据生成器，用rnd产生可复现随机数据)、Validator(校验器，检查生成数据是否符合题目范围与格式)、Checker(评测器/Special Judge，判断选手输出正确性)、Interactor(交互器，用于交互题)。Testlib的随机数生成器rnd以命令行参数为种子哈希，保证相同参数在任何平台产生相同输出(跨平台可复现)，避免了rand()/srand的不可控。它被ROI、ICPC区域赛、所有Codeforces round使用，与Codeforces的Polygon出题平台完全兼容。testlib源自2005年由testlib.pas移植，一直维护至今。

## Why · 为什么

### 直觉 · Intuition

自己写数据生成器最怕'这次能跑下次不能'——rand()跨平台/跨时间不确定。testlib把随机源绑定到命令行参数，让'同一命令永远同一数据'，还顺手提供了大量开箱即用的随机函数(rnd.next各种类型、生成串、生成树模板)，以及严格的读入校验readInt(l,r)来拦下越界输出。出题人省心，评测也安全。

### 原理 · Principle

核心组件：(1)Generator: registerGen(argc,argv,1)初始化后可用rnd.next(范围/模式串)、rnd.wnext(偏移期望)、shuffle()等；种子=命令行参数哈希，如'g 100'与'g.exe 100'输出相同，'g 100 0'则不同。禁止混用rand()/srand(会编译报错)。(2)Validator: registerValidation()后用inf.readInt(l,r)、inf.readEoln()、inf.readEof()等严格按题面格式读取，非法即判Fail，保护评测。(3)Checker: registerTestlibCmd(argc,argv)后用inf/ouf/ans三个流，readInt/readDouble/ensuref等检查输出，quitf(_ok/_wa/_fail)返回结果；常用封装readAns函数同时校验选手与标准输出，返回_fail而非_wa以区分'数据问题'与'选手错误'。(4)Interactor: registerInteraction(argc,argv)读写stdout/ouf与选手交互，只支持CF形式(两程序交互)。内置checker如ncmp/rcmp4/wcmp/yesno可直接用。

### 历史 · History

testlib于2005年由Mike Mirzayanov从testlib.pas移植为C++版本，是Codeforces体系的基石，随Codeforces生态不断演进(新增opts命令行解析、各类生成器模板等)。OI Wiki的testlib/系列页面与Codeforces官方博客均提供完整教程。

## How · 实现

### 伪代码

```python
# generator.cpp (数据生成器)
#include "testlib.h"
registerGen(argc, argv, 1);
int n = opt<int>("n");         // 命名参数 -n10
int m = opt<int>(1);            // 位置参数
cout << n << ' ' << m << endl;
for (...) cout << rnd.next(1, n) << endl;  // 可复现随机

# validator.cpp (数据校验器)
registerValidation();
int n = inf.readInt(1, 1e5, "n"); inf.readEoln();
inf.readEof();

# checker.cpp (评测器)
registerTestlibCmd(argc, argv);
int pans = ouf.readInt(1, 2e9, "sum");
int jans = ans.readInt();
if (pans == jans) quitf(_ok, "correct");
else quitf(_wa, "expected %d found %d", jans, pans);

# 编译+运行
 g++ gen.cpp -o gen   && ./gen -n10 > in.txt
 g++ val.cpp -o val   && ./val < in.txt
 g++ chk.cpp -o chk   && ./chk in.txt out.txt ans.txt
```

### Python 实现

```python
"""Testlib 使用模式参考(Python版通用模板).
注意: testlib是C++库, 本文件给出可复现随机生成器/校验器的Python等价物,
并说明C++侧核心API. 自测验证核心思想.
"""
import random
import sys

# ---------- 对应 testlib 的 rnd.next() 语义 ----------
def next_int(a, b=None, seed_argv=None):
    """可复现随机整数: 以参数为种子, 同参数同结果(等价rnd.next)."""
    if seed_argv is not None:
        random.seed(str(seed_argv))
    if b is None:
        return random.randrange(a)          # [0,a)
    return random.randint(a, b)             # [a,b]


def gen_tree(n, seed):
    """生成随机树(等价testlib的rnd.wnext建树模板)."""
    random.seed(seed)
    edges = []
    for i in range(2, n + 1):
        p = random.randint(1, i - 1)        # 父节点
        edges.append((p, i))
    return edges


# ---------- 对应 testlib 的 validator 严格读入 ----------
def validate_int(inp, lo, hi, name):
    """严格校验整数范围, 越界抛出异常(等价inf.readInt(l,r,name))."""
    try:
        v = int(inp)
    except ValueError:
        raise ValueError(f"invalid {name}: '{inp}'")
    if not (lo <= v <= hi):
        raise ValueError(f"{name}={v} out of range [{lo},{hi}]")
    return v


# ---------- 对应 testlib 的 checker 判定 ----------
def checker_compare(pans, jans, eps=0):
    """返回(_ok/_wa)语义: True=AC."""
    if eps == 0:
        return pans == jans
    return abs(pans - jans) <= eps


if __name__ == "__main__":
    # 可复现性测试: 同种子同结果
    a = next_int(100, 200, seed_argv=(42,))
    b = next_int(100, 200, seed_argv=(42,))
    assert a == b
    c = next_int(100, 200, seed_argv=(42, 0))
    assert a != c  # 参数不同结果不同(种子=参数哈希)

    # 树生成: 边数=n-1
    edges = gen_tree(10, seed=7)
    assert len(edges) == 9

    # 校验器
    assert validate_int("5", 1, 10, "n") == 5
    try:
        validate_int("99", 1, 10, "n")
        assert False
    except ValueError:
        pass

    # checker
    assert checker_compare(3, 3)
    assert not checker_compare(3, 4)
    assert checker_compare(0.5, 0.5001, eps=1e-3)

    print("testlib(Python参考): ALL TESTS PASSED")

```

**PyPy 提示**: testlib.h仅支持C++(GCC/VC++/Clang, C++11+)。Python出题者可参考其'可复现随机'与'严格校验'思想自行实现; C++提交时需将testlib.h与源码同目录#include引用。Polygon上直接选择内置checker即可。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 生成/校验/评测均为输入规模线性 |
| 空间 | O(1)~O(n), 取决于题目数据规模 |

### 局限

仅C++可用; 禁止与srand/rand混用; interactor只支持CF形式(不支持NOI式'选手写函数'交互); 部分OJ(如早期SYZOJ/Lemon)需要修改版testlib。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| OI Wiki | testlib 简介 | 0 | testlib四件套概览与Polygon兼容性说明 | [https://oi-wiki.org/tools/testlib/](https://oi-wiki.org/tools/testlib/) |
| OI Wiki | generator 教程 | 0 | rnd用法、生成树模板、命名参数opts | [https://oi-wiki.org/tools/testlib/generator/](https://oi-wiki.org/tools/testlib/generator/) |
| OI Wiki | checker 教程 | 0 | readAns函数范式、_fail/_wa区分、内置checker列表 | [https://oi-wiki.org/tools/testlib/checker/](https://oi-wiki.org/tools/testlib/checker/) |

## Pitfalls · 易错点

- 使用testlib后禁止调用srand/rand(编译报错), 随机一律走rnd
- checker中读选手输出务必限定范围(readInt(l,r)), 否则可能RE
- 用readAns统一读标准/选手输出, 使标准输出非法时返回_fail而非_wa
- 避免在readAns中使用全局ensure(会误判_fail), 用stream.ensuref
- 数据文件末尾要有换行; 大数据用printf提高生成速度

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/tools/testlib/](https://oi-wiki.org/tools/testlib/)
- github ✓ [https://github.com/MikeMirzayanov/testlib](https://github.com/MikeMirzayanov/testlib)
