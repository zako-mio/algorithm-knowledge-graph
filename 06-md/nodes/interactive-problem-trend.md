---
id: interactive-problem-trend
name: 交互题兴起趋势
group: G-E-10
stage: frontier
priority: P3
depth_tier: brief
---

# 交互题兴起趋势

> ICPC 2024-2025南京连续出交互题，NOI/WC恢复交互题，交互题成为高频新题型

<!-- 元信息: id=interactive-problem-trend · group=G-E-10 · stage=frontier · priority=P3 · depth_tier=brief -->

## What · 是什么

交互题（interactive problem）趋势：一类要求程序与评测器在线问答（query/answer 协议）的题型。2024-2025 年 ICPC 南京站连续两届出现交互题（2024 Problem K、2025 Problem A），NOI/WC 系列（如 P5208[WC2019]I 君的商店、P5473[NOI2019]I 君的探险）也恢复交互题，使其成为区域赛与国赛高频新题型。交互题考核『信息论式提问策略』（最小化询问次数）、随机化、二分/三分/倍增与构造，特别能测试选手对评测协议（flush、IO 格式、询问预算）的严谨把握。OI Wiki 专门设有《交互题》章节（contest/interaction）讲解特殊错误、调试与例题。

## Why · 为什么

### 直觉 · Intuition

普通题『读入-计算-输出』一次成型，交互题是『问一句-答一句』的在线博弈：你的算法必须聪明地在有限询问次数内逼近答案。出题人用交互题来考察『信息增益』思维——每次询问如何最大化排除的信息量——这与信息论、二分、随机化的思想高度契合，且天然防住『背模板/背题解』的 AI 与选手。

### 原理 · Principle

三类经典交互范式：
1) 二分/倍增型：值域内询问『是否 ≥x』类谓词，O(log V) 次逼近；
2) 信息压缩型：设计一次性提出多个问题、一次性读回答案（batch query），如 CF679A 用 19 个质数问数是否整除，O(1) 常数轮；
3) 随机化型：无法确定性定位时用随机撒点（CF843B 随机化链表定位）。
评测协议要求：每次输出后必须 flush（否则 Idleness limit exceeded）；错误交互会得 Wrong Answer/Protocol Violation；要正确读入全部数据避免读入混乱。

### 历史 · History

上个世纪 IOI 就已涉及交互题；2019 年 NOI 系列连续出现 WC2019 I 君的商店、NOI2019 I 君的探险两道交互题，OI Wiki 指出这可能代表交互题回归 NOI 系列。2024 ICPC 南京 Problem K、2025 ICPC 南京 Problem A（袋鼠交互题）连续两年在区域赛最高舞台出现，标志交互题在 ACM/ICPC 体系成为稳定高频题型。

## How · 实现

### 伪代码

```python
# 交互题一般范式（二分型）:
lo, hi = 1, V
while lo < hi:
    mid = (lo + hi) // 2
    print(ask(mid)); flush()
    if response(): hi = mid
    else: lo = mid + 1
print(answer(lo)); flush()
```

### Python 实现

```python
import sys


def interactive_guess_prime():
    """CF679A Bear and Prime 100 交互模板：
    每次输出一个数并 flush，读回 'yes'/'no'，问完 19 个数后判定质数/合数。
    本函数封装标准交互协议的 I/O 约定。
    """
    primes = [2, 3, 4, 5, 7, 9, 11, 13, 17, 19,
              23, 25, 29, 31, 37, 41, 43, 47, 49]
    cnt = 0
    for q in primes:
        print(q)
        sys.stdout.flush()          # 关键：必须 flush
        ans = input().strip()
        if ans == 'yes':
            cnt += 1
            if cnt == 2:
                return 'composite'
    return 'prime'


if __name__ == "__main__":
    # 本地无评测器时仅验证 I/O 流程（不实际运行询问）
    print("interactive-problem-trend: 交互题 I/O 协议模板（flush 必须，否则 Idleness limit exceeded）")
    print("关键点: 每轮输出后 flush；batch 询问可一次问多个；多组数据需读全部输入")

```

**PyPy 提示**: PyPy 交互注意：print 后必须 sys.stdout.flush()；禁用输出缓冲；询问次数预算须精确计数。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 取决于询问轮数与每轮计算，通常 O(询问次数 × 单问处理) |
| 空间 | O(1) ~ O(n) |

### 局限

本地无法直接调试，需写 checker/对拍器或模拟评测器；交互格式错误代价高（一次 WA/PV）；Python 用 input()/print() 需注意首尾空白与 flush。趋势节点为题型综述，复杂度无统一模板。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| ICPC | 2024 Nanjing K | 7 | 2024 ICPC 南京站交互题：连续两年区域赛交互题首例 | [https://codeforces.com/gym/105484/attachments/download/28234/contest-en.pdf](https://codeforces.com/gym/105484/attachments/download/28234/contest-en.pdf) |
| ICPC | 2025 Nanjing A | 7 | 2025 ICPC 南京站 Problem A（袋鼠交互题）：query/answer 协议，可问 n+m+10 次 | [https://sua.ac/wiki/2025-icpc-nanjing/contest-en.pdf](https://sua.ac/wiki/2025-icpc-nanjing/contest-en.pdf) |
| Codeforces | 679A | 3 | Bear and Prime 100：19 次询问判定 100 内是否质数（OI Wiki 例题） | [https://codeforces.com/problemset/problem/679/A](https://codeforces.com/problemset/problem/679/A) |
| Codeforces | 843B | 4 | Interactive LowerBound：随机化交互定位链表（OI Wiki 例题） | [https://codeforces.com/problemset/problem/843/B](https://codeforces.com/problemset/problem/843/B) |

## Pitfalls · 易错点

- 每次输出后必须 sys.stdout.flush()，否则 ILE
- 多组数据时即使提前知道答案也要读完所有输入
- 不要用快读/缓冲读破坏交互时序
- 询问次数超限会 WA（CF）/ PLE（UVa）；格式错 PV
- 随机化交互需正确初始化随机种子，防 hack

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/contest/interaction/](https://oi-wiki.org/contest/interaction/)
- web ✓ [https://sua.ac/wiki/2025-icpc-nanjing/contest-en.pdf](https://sua.ac/wiki/2025-icpc-nanjing/contest-en.pdf)
- web △ [https://codeforces.com/gym/105484/attachments/download/28234/contest-en.pdf](https://codeforces.com/gym/105484/attachments/download/28234/contest-en.pdf)
