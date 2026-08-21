---
id: amortized-analysis
name: 均摊分析
group: G-A-1
stage: intermediate
priority: P1
depth_tier: standard
---

# 均摊分析

> 聚合法/势能法/记账法分析均摊复杂度

<!-- 元信息: id=amortized-analysis · group=G-A-1 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

均摊分析（Amortized Analysis）评价的是一系列操作的总成本除以操作次数，即每次操作的均摊代价，而非单次操作的最坏代价。它不引入概率，保证最坏意义下的平均性能。三种主要方法：聚合分析（算总账平均）、记账法（为未来昂贵操作提前存钱）、势能法（用势能函数度量状态蕴含的能量）。典型例子：动态数组（vector）扩容、栈的 multi-pop、并查集、splay 树。

## Why · 为什么

### 直觉 · Intuition

均摊分析回答：「单个操作偶尔很贵，但平均下来贵不贵？」动态数组扩容时单次插入可能 O(n)，但扩容只在 2 的幂次发生，历史上那些便宜的插入已经「存够了钱」。均摊视角把昂贵操作的成本平摊到一系列便宜操作上。

### 原理 · Principle

聚合分析：直接求 n 次操作总成本再除以 n。记账法：每次操作预付均摊价，便宜操作把多付的钱存起来支付未来贵操作，需证明总存款恒非负。势能法：定义势能函数 Phi(S)，均摊代价 c_hat = c + Phi(S')-Phi(S)，若 Phi 非负且初始为 0，则总实际成本 <= 总均摊成本。以动态数组（容量 m、元素 n）为例，Phi=2n-m，插入均摊代价恒为 3（O(1)）。

### 历史 · History

均摊分析的概念源自数据结构理论，经典教材（CLRS《算法导论》第 17 章）系统建立了聚合、记账、势能三种方法。势能法后来成为分析 splay 树、并查集按秩合并、Fib heap 等复杂数据结构的标准工具。OI Wiki 与 CPH 均在复杂度章节介绍其应用。

## How · 实现

### 伪代码

```python
# 势能法通用框架
# 定义势能函数 Phi(状态)，要求 Phi(初始)=0 且 Phi(状态)>=0
# 每次操作均摊代价 = 实际代价 + Phi(操作后) - Phi(操作前)
# 若均摊代价 = O(T(n))，则 n 次操作总时间 = O(n*T(n))

# 动态数组插入（容量 m, 元素数 n）
# Phi = 2n - m
# 普通插入: 实际 1, Phi 增 2        => 均摊 3
# 扩容插入: 实际 n+1, Phi 减 (n-2) => 均摊 3

# 栈 multi-pop: Phi = |S| (栈中元素数)
# push: 实际 1, Phi 增 1  => 均摊 2
# pop:  实际 1, Phi 减 1  => 均摊 0
# multi-pop(k): 实际 k, Phi 减 k => 均摊 0
```

### Python 实现

```python
def dynamic_array_total_cost(ops):
    """模拟动态数组（倍增扩容），返回总实际成本。
    ops: 1=insert（追加一个元素）
    验证均摊分析结论：n 次 insert 总成本 O(n)。
    """
    cap = 1
    size = 0
    total = 0
    for op in ops:
        assert op == 1
        total += 1  # 写入新元素
        if size == cap:
            total += size  # 复制旧元素到新数组
            cap *= 2
        size += 1
    return total


def potential_vector(n):
    """用势能法 Phi=2n-m 计算 n 次插入的总均摊成本（应=3n）"""
    cap = 1
    size = 0
    phi = 2 * size - cap
    amortized_total = 0
    for _ in range(n):
        real = 1
        if size == cap:
            real += size
            cap *= 2
        size += 1
        phi_new = 2 * size - cap
        amortized_total += real + (phi_new - phi)
        phi = phi_new
    return amortized_total


def stack_multi_pop_total(n_push, pops):
    """栈 push 后 multi-pop，返回总实际成本（应 <= 2*n_push + len(pops)）。"""
    total = n_push  # 每次 push 成本 1
    stack_size = n_push
    for k in pops:
        popped = min(stack_size, k)
        total += popped
        stack_size -= popped
    return total


if __name__ == "__main__":
    for n in [1, 2, 3, 4, 7, 8, 16, 100, 1000]:
        ops = [1] * n
        real = dynamic_array_total_cost(ops)
        # 真实总成本应 < 4n（翻倍扩容的总复制成本 < 2n）
        assert real <= 4 * n, (n, real)
        am = potential_vector(n)
        assert am == 3 * n, (n, am)

    # 栈 multi-pop: 10 次 push + 若干 multi-pop
    total = stack_multi_pop_total(10, [3, 2, 5, 1])
    assert total == 10 + (3 + 2 + 5 + 0), total
    # 无论 multi-pop 怎么调，总成本 <= 2*10
    assert stack_multi_pop_total(10, [8, 8, 8]) == 10 + 10

    print("All tests passed.")
```

**PyPy 提示**: 均摊分析是理论工具，本身不产生运行时开销。但理解其结论可指导实现：如动态数组倍增扩容在 PyPy 的 list 中已内建，勿手写 O(n) 的 list.insert(0)。并查集、单调栈等数据结构的均摊性质保证 Python 实现在大数据下仍稳定。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 单次最坏可能 O(n)，但均摊代价 O(1)；n 次操作总时间 O(n) |
| 空间 | O(n) — 数据结构本身的空间 |

### 局限

均摊分析给出的是序列级保证，不承诺单次操作的实时性；不适用于需要每个操作都严格快的实时系统。且势能函数选择需要技巧，选择不当会得到过松或错误的界。均摊结论不能直接用于「每次操作必须 O(1)」的强实时场景。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1886 | 3 | 滑动窗口/单调队列：队列入队出队各一次，均摊 O(1) 达到 O(n) 总复杂度 | [https://www.luogu.com.cn/problem/P1886](https://www.luogu.com.cn/problem/P1886) |
| Luogu | P3865 | 4 | ST表模板：预处理均摊 O(n log n)，查询 O(1) | [https://www.luogu.com.cn/problem/P3865](https://www.luogu.com.cn/problem/P3865) |
| Luogu | P5788 | 3 | 单调栈：每个元素至多入栈出栈一次，均摊 O(n)（最坏单步可 O(n) 但总 O(n)） | [https://www.luogu.com.cn/problem/P5788](https://www.luogu.com.cn/problem/P5788) |

## Pitfalls · 易错点

- 把均摊 O(1) 误当单次最坏 O(1)，在实时性要求高的场景用错
- 势能法忘记要求 Phi(初始)=0 且恒非负，导致证明无效
- 聚合分析中把不同操作类型的数量搞混（如 n 次操作里含 k 次昂贵操作时只算总操作 n）
- 误把平均复杂度（随机输入的期望）当成均摊复杂度（最坏输入下的序列平均）

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/basic/amortized-analysis/](https://oi-wiki.org/basic/amortized-analysis/)
- 书籍 ✓ `CPH ch8 p87`
- 书籍 ✓ `CLRS《算法导论》ch17 均摊分析`
