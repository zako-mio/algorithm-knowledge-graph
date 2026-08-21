---
id: mo-rollback
name: 回滚莫队
group: G-D-7
stage: advanced
priority: P2
depth_tier: standard
---

# 回滚莫队

> 只增不删的莫队变体：同块询问暴力，跨块询问左端点每问重置回滚，处理「删除难、增加易」的区间统计，O(n√m)。

<!-- 元信息: id=mo-rollback · group=G-D-7 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

回滚莫队（Rollback Mo's algorithm）处理一类「增加元素容易、删除元素困难（或无法实现）」的区间询问问题，例如区间最大重要度（值×出现次数取 max）、区间 mex、区间内只出现一次的数等。其核心思想是：既然只能 add 不能（或很难）remove，那就干脆不删——左端点每次从块右边界 +1 处重新开始，右端点单调增加，同块内的询问直接暴力扫描。这样每次指针移动只有 add 操作，代价摊还后仍为 O(n√m)。

## Why · 为什么

### 直觉 · Intuition

把块内所有询问的右端点按升序处理，右指针只增不减（每次 add 都容易）；左指针呢？如果也让它在块内来回移动就会遇到删除。解决办法：把左指针「重置」回块右边界 +1，从左往右暴力扩展——虽然每个询问都要重新扫一遍左段（≤ 块长 s），但右段不重复，于是单块总代价 O(s·q_块 + n)，跨块累加得 O(n√m)。删除问题被彻底绕开：回滚前保存快照，回答完再把左端点的增量撤销（回滚），不真正执行删除。

### 原理 · Principle

① 分块：块长 s=n/√m（或 √n）；② 排序：l 所在块为第一关键字、r 升序为第二关键字；③ 处理每块：若询问 l、r 同块则直接暴力扫描回答；否则先只增地扩展右端点到 r（右指针单调不减，saved_best 记录当前最优），再从左端 l 到块右边界 R 暴力向左扩展（临时计数 cc 与右部 cnt 合并），得到答案后丢弃临时部分——左端点重置回 R+1，实现「回滚」；④ 复杂度：右端点在块内单调，总 O((n/s)·n)，左端点每次 ≤s，总 O(m·s)，取 s=n/√m 平衡得 O(n√m)。

### 历史 · History

回滚莫队在国内 OI 圈流传，常以 JOISC 2014 Day1「历史研究」（LOJ 2874，区间最大重要度）作为代表题。OI Wiki 收录了完整介绍并引用 Parsnip 的博客《回滚莫队及其简单运用》。它本质上是「只用一个方向操作」的分块暴力 + 莫队排序，与只删不增的回滚莫队对称存在。

## How · 实现

### 伪代码

```python
block = n / sqrt(m)
qs.sort(key=lambda q: (q.l//block, q.r))
for blk in blocks:
    R = 块右边界; cur_r = R; saved_best = 0
    for q in qs where q.l//block == blk:
        if q.r <= R:            # 同块暴力
            cc = {}; best = 0
            for i in [q.l..q.r]: cc[a[i]]++; best = max(best, f(a[i],cc))
            ans[q.id] = best
        else:                   # 跨块: 只增
            while cur_r < q.r: cur_r++; cnt[a[cur_r]]++; saved_best=max(...)
            best = saved_best; cc = {}
            for i in [R..q.l 递减]: cc[a[i]]++; best = max(best, f(a[i], cnt+cc))
            ans[q.id] = best     # 不写回 cnt, 即回滚
```

### Python 实现

```python
def mo_rollback(n, arr, queries):
    """回滚莫队（只增不删）：区间最大重要度 = max(值 * 出现次数).
    查询闭区间 [l,r] 0-indexed, 返回按 id 的答案."""
    import math
    block = max(1, int(math.sqrt(n)))
    qs = sorted(queries, key=lambda q: (q[0] // block, q[1]))
    ans = [0] * len(queries)
    maxv = max(arr) if arr else 0
    for blk in range((n + block - 1) // block):
        R = min(n - 1, (blk + 1) * block - 1)
        cnt = [0] * (maxv + 1)          # 永久计数（右部 [R+1, cur_r]）
        cur_r = R
        saved_best = 0
        for l, r, idx in qs:
            if l // block != blk:
                continue
            if r <= R:
                cc = [0] * (maxv + 1)
                best = 0
                for i in range(l, r + 1):
                    cc[arr[i]] += 1
                    best = max(best, arr[i] * cc[arr[i]])
                ans[idx] = best
            else:
                while cur_r < r:
                    cur_r += 1
                    cnt[arr[cur_r]] += 1
                    saved_best = max(saved_best, arr[cur_r] * cnt[arr[cur_r]])
                base = saved_best
                cc = [0] * (maxv + 1)
                best = base
                for i in range(R, l - 1, -1):   # 向左扩展 [l, R]
                    cc[arr[i]] += 1
                    best = max(best, arr[i] * (cc[arr[i]] + cnt[arr[i]]))
                ans[idx] = best
    return ans

if __name__ == "__main__":
    arr = [1, 3, 1, 2, 3, 3]
    qs = [(0, 5, 0), (1, 3, 1), (2, 2, 2)]
    res = mo_rollback(6, arr, qs)
    for (l, r, i) in qs:
        cc = {}
        for v in arr[l:r + 1]:
            cc[v] = cc.get(v, 0) + 1
        best = max(v * c for v, c in cc.items())
        assert res[i] == best, (l, r, res[i], best)
    import random
    random.seed(13)
    for _ in range(300):
        n = random.randint(1, 12)
        a = [random.randint(1, 5) for _ in range(n)]
        m = random.randint(1, 15)
        qs = []
        for i in range(m):
            l = random.randint(0, n - 1); r = random.randint(l, n - 1)
            qs.append((l, r, i))
        got = mo_rollback(n, a, qs)
        for (l, r, i) in qs:
            cc = {}
            for v in a[l:r + 1]:
                cc[v] = cc.get(v, 0) + 1
            best = max(v * c for v, c in cc.items())
            assert got[i] == best, (a, l, r, got[i], best)
    print("mo_rollback OK")

```

**PyPy 提示**: 每次询问左段暴力会重复扫 O(s) 个元素，Python 常数较大；用 list 计数 + 值域离散化；对 maxv 大时 cnt/cc 数组可复用但注意清零开销。m 远小于 n 时块长取 n/√m 更优。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(n√m)（每块右指针 O(n)，左指针每问 O(s)，s=n/√m 最优） |
| 空间 | O(n+m) |

### 局限

仅适用于「增加容易、删除困难/不可行」的统计（若删除也 O(1) 则普通莫队即可）；要求统计函数对单点增加是「单调可更新」的（如 max 类）；强制在线不行；若统计是「删除容易、增加难」，需对称地用只删不增的回滚莫队。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| LOJ | 2874 | 5 | JOISC 2014 Day1 历史研究：区间最大重要度（值×出现次数），回滚莫队模板题，OI Wiki 例题 | [https://loj.ac/p/2874](https://loj.ac/p/2874) |
| Luogu | AT1219 | 5 | 历史研究 原题（AtCoder 移植），与 LOJ 2874 同题 | [https://www.luogu.com.cn/problem/AT1219](https://www.luogu.com.cn/problem/AT1219) |
| Luogu | P4137 | 4 | Rmq Problem / mex：区间 mex，回滚莫队按出现次数维护 | [https://www.luogu.com.cn/problem/P4137](https://www.luogu.com.cn/problem/P4137) |
| BZOJ | 4241 | 5 | 历史研究 原题（BZOJ 4241） | [https://hydro.ac/p/bzoj-P4241](https://hydro.ac/p/bzoj-P4241) |

## Pitfalls · 易错点

- 跨块询问的左段临时计数必须「只读」右部 cnt：把临时 cc 与 cnt 合并算答案，但绝不写回 cnt，否则下一个询问的右指针增量被污染
- saved_best 必须在同一块内跨询问保留，跨块时重置为 0
- 同块询问（r<=R）直接暴力，不能走右指针扩展逻辑（否则右指针被卡在块内）
- 若重要度=值×次数，值域大时必须离散化，f(v,cnt)=v*cnt 也按离散后值映射
- 左端点回滚后 cur_l 应复位为 R+1；实现时用临时循环替代真实左指针即可

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/rollback-mo-algo.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/rollback-mo-algo.md)
- OI Wiki ✓ [https://oi-wiki.org/misc/rollback-mo-algo/](https://oi-wiki.org/misc/rollback-mo-algo/)
- 博客 △ [https://www.cnblogs.com/Parsnip/p/10969989.html](https://www.cnblogs.com/Parsnip/p/10969989.html)
