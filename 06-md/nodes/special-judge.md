---
id: special-judge
name: Special Judge
group: G-E-9
stage: intermediate
priority: P2
depth_tier: standard
---

# Special Judge

> 多解/浮点/构造题的专用评测器：testlib checker编写范式，_ok/_wa/_fail三态与readAns模式

<!-- 元信息: id=special-judge · group=G-E-9 · stage=intermediate · priority=P2 · depth_tier=standard -->

## What · 是什么

Special Judge(SPJ/checker)是答案不唯一或需精度判定时，替代'逐字符比对'的自定义评测程序。适用场景：构造类题目(输出任意合法方案)、浮点精度题(|diff|<1e-3)、最优化题(输出比标准更优也可)、要求格式特殊或输出需重新计算的题。主流OJ(CF/洛谷/UOJ)要求用testlib.h编写checker：registerTestlibCmd后通过inf(输入)、ouf(选手输出)、ans(标准输出)三个流读取，quitf(_ok/_wa/_fail)返回结果——_fail表示'标准输出/数据有问题'，用于与选手错误区分。核心范式是写readAns(InStream&)统一读取并校验选手与标准输出。其他OJ(Lemon/Cena/HUSTOJ等)有各自的spj编写接口(文件读写与退出码约定)。

## Why · 为什么

### 直觉 · Intuition

普通题对答案'一模一样'即AC；SPJ题答案不唯一，只能'程序判程序'。checker就像裁判：读输入和双方答案，按规则判定选手是否'合理合法'。用testlib是因为它把'读流、报错、终止'封装好，还强制范围检查避免选手恶意输出导致评测器崩掉。

### 原理 · Principle

testlib checker要点：(1)registerTestlibCmd(argc,argv)初始化；(2)inf读输入、ouf读选手输出、ans读标准输出；(3)读选手输出必须限定范围readInt(l,r)/readDouble，防止越界与恶意输入导致RE；(4)判浮点用abs(pans-jans)<1e-3（需处理NaN）；(5)写readAns(stream)函数复用读取逻辑：对ouf校验非法返回_wa，对ans校验非法返回_fail（用stream.quitf而非全局quitf）；(6)比较后quitf(_ok,...)或quitf(_wa,...)；选手输出比标准输出更优时返回_fail（数据/标程问题）。内置checker可直接用：ncmp(整数)、rcmp4/6/9(浮点精度)、wcmp(字符串)、yesno(YES/NO)。运行方式: ./checker input output answer。非testlib的OJ如HUSTOJ用退出码0=AC/1=WA, Lemon用argv传分值与报告文件。

### 历史 · History

Special Judge随OJ发展而生：早期HDU/HUSTOJ等用简单退出码约定，后来testlib统一了CF生态，成为事实标准。OI Wiki的special-judge页整理了Testlib、Lemon、Cena、CCR、Arbiter、HUSTOJ、QDUOJ、HDOJ、SYZOJ2、牛客、DOMJudge各平台写法。

## How · 实现

### 伪代码

```python
# testlib checker 范式
#include "testlib.h"
registerTestlibCmd(argc, argv);

double pans = ouf.readDouble(), jans = ans.readDouble();
if (isnan(pans)) quitf(_wa, "nan output");
if (abs(pans - jans) < 1e-3)
  quitf(_ok, "Good job");
else
  quitf(_wa, "expected %f found %f", jans, pans);

# 运行: ./checker <input> <output> <answer>
```

### Python 实现

```python
"""Special Judge 参考实现(Python通用版).
自测: 模拟多解/浮点精度/构造题判定.
"""
import math
import sys

OK, WA, FAIL = "_ok", "_wa", "_fail"


class Judge:
    """极简testlib-like判定器: 读取/判定/退出三态."""
    def __init__(self):
        self.verdict = OK
        self.msg = ""

    def quitf(self, verdict, msg=""):
        self.verdict = verdict
        self.msg = msg

    # 模拟 ouf.readDouble / ensuref
    def read_double(self, text):
        try:
            v = float(text.strip())
        except ValueError:
            self.quitf(WA, f"cannot parse '{text}'")
            return None
        if math.isnan(v):
            self.quitf(WA, "nan output is forbidden")
        return v


def judge_float(pans, jans, eps=1e-3):
    """浮点精度判定: |pans-jans|<=eps 即AC."""
    if math.isnan(pans) or math.isnan(jans):
        return WA
    return OK if abs(pans - jans) <= eps else WA


def judge_construction(constraint_ok, solution_valid):
    """构造题: 只校验选手输出的合法性, 与标程无关."""
    if not solution_valid:
        return WA
    return OK


def judge_better(pans, jans):
    """最优化题: 选手不劣于标程才算对(更优返回_fail表示数据问题)."""
    if pans > jans:
        return FAIL      # 选手比标程更优: 说明标程不是最优, 数据/标程问题
    if pans == jans:
        return OK
    return WA


if __name__ == "__main__":
    # 浮点: 1e-4误差 OK, 1e-2误差 WA
    assert judge_float(0.5001, 0.5, eps=1e-3) == OK
    assert judge_float(0.51, 0.5, eps=1e-3) == WA
    assert judge_float(math.nan, 0.5) == WA

    # 构造题: 合法性即AC
    assert judge_construction(True, True) == OK
    assert judge_construction(True, False) == WA

    # 最优化题: 更优->_fail, 持平->_ok, 更差->_wa
    assert judge_better(5, 5) == OK
    assert judge_better(4, 5) == WA
    assert judge_better(6, 5) == FAIL

    # 简易Judge对象
    j = Judge()
    j.read_double("abc")
    assert j.verdict == WA

    print("special-judge: ALL TESTS PASSED")

```

**PyPy 提示**: 编写checker时注意NaN/Inf的显式处理, 防止'输出NaN即AC'的漏洞; 选手输出readInt必须限定范围。非testlib平台先确认其spj接口(退出码/文件约定)再写。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(输入/输出规模) |
| 空间 | O(输出规模) |

### 局限

checker自身不能有RE(部分OJ把spj RE当系统错误); 读取选手输出必须校验格式与范围; testlib仅C++; 各OJ接口差异需适配。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| OI Wiki | Special Judge | 0 | Testlib/Lemon/Cena/HUSTOJ/DOMJudge等各平台spj写法汇总 | [https://oi-wiki.org/tools/special-judge/](https://oi-wiki.org/tools/special-judge/) |
| OI Wiki | Checker教程 | 0 | readAns范式、_fail/_wa区分、内置checker(ncmp/rcmp4/wcmp/yesno) | [https://oi-wiki.org/tools/testlib/checker/](https://oi-wiki.org/tools/testlib/checker/) |
| Codeforces | Testlib库 | 0 | testlib.h源码与checkers/目录内置checker实现 | [https://github.com/MikeMirzayanov/testlib](https://github.com/MikeMirzayanov/testlib) |

## Pitfalls · 易错点

- 选手输出浮点NaN必须判WA, 否则'输出NaN即AC'漏洞
- 读选手输出务必限定范围readInt(l,r), 防越界/恶意输入导致RE
- 标准输出非法应返回_fail而非_wa(用stream.quitf在readAns中)
- 选手输出比标程更优时返回_fail(标程不是最优), 不能判WA
- checker不应检查多余空白字符(testlib默认容错)

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/tools/special-judge/](https://oi-wiki.org/tools/special-judge/)
- OI Wiki ✓ [https://oi-wiki.org/tools/testlib/checker/](https://oi-wiki.org/tools/testlib/checker/)
