---
id: interaction-strategy
name: 交互题策略
group: G-E-8
stage: intermediate
priority: P2
depth_tier: standard
---

# 交互题策略

> 交互次数优化、二分交互、随机撒点、flush 时机、STDIO vs Grader 模式

<!-- 元信息: id=interaction-strategy · group=G-E-8 · stage=intermediate · priority=P2 · depth_tier=standard -->

## What · 是什么

交互题中程序与评测程序（interactor）一问一答完成任务，得分优劣常取决于查询/交互次数。关键要素：①输出后必须 flush（C++ fflush(stdout) / endl，Python sys.stdout.flush()），否则交互器收不到请求导致 Idleness Limit Exceeded（ILE）；②STDIO 交互（CF/AtCoder/ICPC，问写标准输出、读标准输入）与 Grader 交互（IOI/APIO 的 CMS 平台，实现指定函数调用辅助函数）；③次数优化：二分查找（判定一个单调属性）、随机撒点（链表/分布未知时）、三分/倍增；④读入所有数据再回答（多组数据时即使已知答案也要读完，否则 ILE）；⑤静态查错能力要求高（无法方便对拍）。

## Why · 为什么

### 直觉 · Intuition

交互器像真人裁判：你不发话它不回答。每问一次都有代价（题目给的询问上限），所以策略就是「用最少的确定性/概率性询问逼近答案」。标准套路：把交互建模成「对单调谓词的查询」→ 二分 O(log n) 次；无法直接二分 → 先用随机采样缩小范围再精确定位。flush 是「把话说出去」，不 flush 就像话憋在嗓子眼，交互器只能干等。

### 原理 · Principle

STDIO 交互基于管道：stdout 默认行缓冲/全缓冲，必须 flush 才能立即送达。Grader 交互通过函数返回值传输，无 flush 问题但语言受限（通常仅 C++/Pascal）。次数上限：CF 上超过询问限制判 Wrong Answer（错误说明里带原因），UVa 判 Protocol Limit Exceeded。经典策略：①确定型——二分查找（单调集合），O(log n)；②概率型——先随机撒 k 个点收集分布信息，再沿贪心/边界前进（如 CF843B 随机撒 1000 点逼近链表目标值）；③验证质数——一次问 19 个数（含平方）即可判定。

### 历史 · History

交互题自上世纪 IOI 已有，2019 年 NOI 系列连续出现（WC2019 I 君的商店、NOI2019 I 君的探险）标志其回归。OI Wiki 的 contest/interaction 页以 CF679A、CF843B、APIO2016 Gap、CF750F 等为例讲解 flush 时机、随机撒点、次数限制与特殊错误（ILE/PLE/PV），contest/problems 页区分 STDIO 与 Grader 两种交互方式并比较优劣。

## How · 实现

### 伪代码

```python
STDIO 二分示例（猜 1..n 中的数）:
  lo,hi = 1,n
  while lo<hi:
    mid=(lo+hi)//2
    print('?', mid); sys.stdout.flush()
    ans = int(input())
    if ans == '>=': lo = mid+1  else: hi = mid
  print('!', lo); sys.stdout.flush()
随机撒点(CF843B式):
  若 n 小则全询问；否则随机问 1000 个点取最优起点，再沿 next 指针走
```

### Python 实现

```python
import sys


def guess_number(n):
    # 经典二分交互：交互器答案是 ans，我们问 '? x' 得到 x>=ans 与否
    # 这里用闭包模拟交互器便于自测
    secret = 42
    assert 1 <= secret <= n

    def ask(x):
        print(f"? {x}", flush=True)
        return x >= secret

    lo, hi = 1, n
    cnt = 0
    while lo < hi:
        mid = (lo + hi) // 2
        cnt += 1
        if ask(mid):
            hi = mid
        else:
            lo = mid + 1
    print(f"! {lo}", flush=True)
    assert lo == secret, lo
    return cnt


def guess_prime_style():
    # CF679A 风格：一次问 19 个数（质数 + 质数平方）判定 n 是否为质数
    import random
    n = random.choice([2, 3, 5, 97, 100, 143])
    candidates = [2, 3, 4, 5, 7, 9, 11, 13, 17, 19, 23, 25, 29, 31, 37, 41, 43, 47, 49]
    yes = 0
    for x in candidates:
        if n % x == 0:
            yes += 1
    is_prime = yes <= 1 and n >= 2
    # 自测：100=2^2*5^2 应判合数；143=11*13 合数；97 质数
    expected = n in (2, 3, 5, 97)
    assert is_prime == expected, (n, is_prime)
    return n, is_prime


def main():
    cnt = guess_number(1000)
    print(f"binary search used {cnt} queries, result correct")
    assert cnt <= 11  # log2(1000) ~ 10
    for _ in range(200):
        guess_prime_style()
    print("prime-style random tests OK")
    print("OK")


if __name__ == "__main__":
    main()

```

**PyPy 提示**: 交互题 Python 需注意：print(..., flush=True) 每次询问都会系统调用，次数上限内可接受；不要用 sys.stdin.buffer.read() 批量读入（会阻塞等待全部数据，交互器不回发造成死锁）。Grader 交互通常不提供 Python 版 grader 或头文件，需按题目给定接口实现，Python 在 CMS/IOI 环境支持有限，优先 C++。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 查询次数：二分 O(log n)，随机撒点 O(k + 期望长度)，其他策略按题 |
| 空间 | O(n) 或 O(k) |

### 局限

Grader 交互语言受限（CMS 通常只支持 C++/Pascal），Python 参赛者尽量选 STDIO 交互题；随机化策略有概率失败需按题目容错设计；交互题无法像普通题那样用对拍验证，正确性依赖静态推演与本地模拟交互器；交互次数耗尽后果严重（WA/ILE），实现要一遍对。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Codeforces | 679A | 1400 | Bear and Prime 100：一次问 19 个质数及质数平方判定质合数，入门交互题 | [https://codeforces.com/problemset/problem/679/A](https://codeforces.com/problemset/problem/679/A) |
| Codeforces | 843B | 1800 | Interactive LowerBound：随机撒 1000 点逼近链表目标值，随机化交互 | [https://codeforces.com/problemset/problem/843/B](https://codeforces.com/problemset/problem/843/B) |
| UOJ | 206 | 5 | 【APIO2016】Gap：Grader 交互，分段/交互次数优化求最大间隔 | [https://uoj.ac/problem/206](https://uoj.ac/problem/206) |
| Codeforces | 750F | 2400 | New Year and Finding Roots：7 层完全二叉树上定位根，次数紧张需精妙策略 | [https://codeforces.com/problemset/problem/750/F](https://codeforces.com/problemset/problem/750/F) |

## Pitfalls · 易错点

- 每次输出后忘 flush()——ILE 或死等
- 多组数据下提前 break 不读完剩余输入，下一轮读入错位
- 查询次数超过限制被判 WA，需预计算上限并留余量
- STDIO 交互里用批量读入 sys.stdin.buffer.read() 导致阻塞死锁
- 随机化未设种子被 hack（CF 上用 random_shuffle 需 srand）
- 交互格式错误（多换行/少空格）被判 PE/PV；输出猜测前没有终止标志（!）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/contest/interaction/](https://oi-wiki.org/contest/interaction/)
- OI Wiki ✓ [https://oi-wiki.org/contest/problems/](https://oi-wiki.org/contest/problems/)
