---
id: problem-types
name: 题型识别
group: G-E-8
stage: basic
priority: P0
depth_tier: deep
---

# 题型识别

> 传统题/交互题/提交答案题/通信题的识别与应对，评测结果类型(AC/WA/TLE/RE等)

<!-- 元信息: id=problem-types · group=G-E-8 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

题型识别指拿到题面后快速判断「这是什么类型的题」，从而决定应对流程与评测规则。四大类：①传统题——输入→程序→输出，黑盒评测，比较输出（忽略行末空白），有 TL/ML；②交互题——程序与评测程序问答（见 interaction-strategy）；③提交答案题——不交程序，交答案文件（.out），无限时间空间，可手玩或写程序生成；④通信题——两个程序通过受限通道协作（如 Channel 编解码，对答有限位）。评测结果类型：AC 接受、CE 编译错误、WA 答案错误、PE 格式错误、RE 运行错误（非零返回）、TLE 超时、MLE 超内存、OLE 输出超量。ICPC 需全部测试点 AC 才算过题，OI 逐测试点给分。

## Why · 为什么

### 直觉 · Intuition

不同类型题的「得分方式」完全不同：传统题程序输出对错一锤定音，提交答案题不存在 TLE/MLE（离线生成答案），交互题有次数限制与 flush 要求，通信题考察编码率。先识别题型能立刻告诉你「下一步该干嘛」：传统题直接写读入输出，提交答案题先看数据规模能不能手玩/暴力生成，交互题先封装询问函数并确保 flush。

### 原理 · Principle

传统题评测：编译后程序读 stdin，比较 stdout 与标准答案（Special Judge 时用特判程序）。交互题评测：interactor 与程序通过管道对话。提交答案题：评测器直接比对答案文件，因此可以写任意长时间/任意内存的生成程序，甚至人工构造。通信题：两段程序 A/B 共享部分信息（如 B 只拿到 A 发的 t 位信息），评测关心传递正确率。IOI/ICPC 环境的评测结果映射：Python 中 CE 少见、RE 常见于除零/越界/递归爆栈，MLE 常见于大数组/深递归。

### 历史 · History

OI Wiki 的 contest/problems 页完整分类传统题/交互题/提交答案题/通信题并给出评测结果枚举与 STDIO/Grader 交互的对比；contest/oi 页说明 OI 与 IOI 赛制下的得分规则（多点给分 vs 实时评测）。ICPC 赛制说明见 contest/icpc 页。

## How · 实现

### 伪代码

```python
题型判定流程:
  1. 题面有无 grader/交互函数/询问格式? → 交互题
  2. 是否要求提交 .out 答案文件而非源码? → 提交答案题
  3. 是否两个程序互相通信? → 通信题
  4. 否则 → 传统题
应对:
  传统题 → 正常读入输出，注意 TL/ML
  交互题 → 封装 ask()，flush，控次数
  提交答案题 → 写生成程序/暴力构造答案文件
  通信题 → 设计编码方案
```

### Python 实现

```python
import sys


def identify_problem_type(desc):
    """按题面特征启发式识别题型，返回 (类型, 关键注意点)。"""
    d = desc.lower()
    if "grader" in d or "交互" in d or ("? " in d and "!" in d):
        return ("interactive", "封装询问并 flush，控制询问次数")
    if ".out" in d or "答案文件" in d or ("输出文件" in d and "提交答案" in d):
        return ("output-only", "不交程序，生成答案文件，无 TL/ML")
    if "两个程序" in d or "通信" in d or "channel" in d:
        return ("communication", "设计编码/解码，关注信息量限制")
    return ("traditional", "常规读入输出，注意 TL/ML 与输出格式")


def main():
    samples = [
        ("给定 n 个数，求最大值，输出一个整数", "traditional"),
        ("交互题：每次询问一个数 x，评测程序回答 x 是否大于答案", "interactive"),
        ("提交答案题：输出 1.out .. 10.out 十个答案文件", "output-only"),
        ("通信题：程序 A 给程序 B 发送信息，两程序需协作", "communication"),
    ]
    for desc, expect in samples:
        typ, note = identify_problem_type(desc)
        print(f"{typ:14s} | {note}")
        assert typ == expect, (desc, typ)
    verdicts = {"AC": "Accepted", "WA": "Wrong Answer", "TLE": "Time Limit Exceeded",
                "RE": "Runtime Error", "MLE": "Memory Limit Exceeded", "OLE": "Output Limit Exceeded",
                "CE": "Compile Error", "PE": "Presentation Error"}
    print("\nverdict mapping:", len(verdicts), "kinds")
    assert len(verdicts) == 8
    print("OK")


if __name__ == "__main__":
    main()

```

**PyPy 提示**: Python 提交时 CE 基本不会出现（无编译概念），RE 常是 IndexError/ZeroDivisionError/递归深度超限（可 sys.setrecursionlimit），MLE 常是大二维 list 或深递归栈。识别 RE/MLE 从 Python 报错信息即可定位。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 题型识别 O(题面长度) 启发式；答题复杂度由题型决定 |
| 空间 | O(1) 识别开销 |

### 局限

题面识别是启发式（官方分类以题面说明为准，如有些交互题不在题面写「交互」二字但给出了 ask 接口）；提交答案题也可能混合（多档数据一部分可手玩一部分需程序）；OLE/PE 在现代 OJ 常被并入 WA。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Codeforces | 传统题 | 1 | 绝大多数 CF 题为传统题：输入输出格式固定，输出忽略行尾空白比较 | [https://codeforces.com/problemset](https://codeforces.com/problemset) |
| LOJ | 559 | 4 | 【ZQC 的迷宫】STDIO 交互题：迷宫寻路，交互与搜索结合 | [https://loj.ac/problem/559](https://loj.ac/problem/559) |
| NOI | 经典提交答案题 | 3 | 提交答案题：直接构造/程序生成答案文件，关注文件格式与特判评分 | [https://oi-wiki.org/contest/problems/](https://oi-wiki.org/contest/problems/) |

## Pitfalls · 易错点

- 把交互题当传统题写（读入后一次性输出）——直接 ILE
- 提交答案题还在写读入输出的主程序而不是生成答案文件
- 输出末尾多余空格/换行被严格格式题判 PE（现代 OJ 常容忍或并 WA）
- 忽视 OLE：调试日志忘删导致输出超量
- 通信题误用共享内存/额外输出，被判定格式违规
- 把 RE 当 WA 排查：先看评测返回的 verdict 再对症

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/contest/problems/](https://oi-wiki.org/contest/problems/)
- OI Wiki ✓ [https://oi-wiki.org/contest/interaction/](https://oi-wiki.org/contest/interaction/)
- OI Wiki ✓ [https://oi-wiki.org/contest/icpc/](https://oi-wiki.org/contest/icpc/)
