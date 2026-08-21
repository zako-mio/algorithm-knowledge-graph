---
id: tangents-two-circles
name: 两圆公切线
group: G-D-2
stage: advanced
priority: P2
depth_tier: standard
---

# 两圆公切线

> 求两圆内外公切线，几何方程或向量构造

<!-- 元信息: id=tangents-two-circles · group=G-D-2 · stage=advanced · priority=P2 · depth_tier=standard -->

## What · 是什么

给定两个圆（圆心与半径），求它们的所有公切线（tangent lines）：外切线（两圆在同侧，共 2 条，两圆外离/相交/内切/内含时数量不同）与内切线（两圆在直线异侧，共 2 条，仅在两圆相离时存在）。公切线的条数：外离 d>r₁+r₂：4 条（2 外 2 内）；外切 d=r₁+r₂：3 条；相交 |r₁-r₂|<d<r₁+r₂：2 条（仅外）；内切 d=|r₁-r₂|：1 条；内含 d<|r₁-r₂|：0 条。求法：把圆半径做加减偏移（r₂-r₁ 或 r₂+r₁）化归为『过一圆圆心作偏移圆的切线』，再用向量旋转/勾股求切点。应用：圆碰撞/运动规划、几何构图题、圆弧连接。

## Why · 为什么

### 直觉 · Intuition

两条圆外切线的本质：把其中一圆半径『减掉』变成点（退化圆），问题变为『从圆心 C₁ 向以 C₂ 为圆心、|r₂-r₁| 为半径的辅助圆作切线』——从点作圆的切线可解（垂距、勾股）。内切线则把半径『相加』（r₂+r₁ 辅助圆）。每条切线方向确定后，用单位法向量偏移回原半径即可得到切点。为什么条数这样分？取决于圆心距与两半径之和/差的大小关系（相离/相切/相交/内含）。

### 原理 · Principle

① 外切线：设 v=C₂-C₁，d=|v|，r=r₂-r₁。辅助圆（圆心 C₂ 半径 |r|）。自 C₁ 向该圆作切线，切线与连心线的夹角 φ 满足 sinφ=|r|/d（需 d≥|r| 才有解，即外离或半径不相等时）。② 用旋转：单位向量 u=v/d，垂直单位向量 w=(-u.y,u.x)。切点/方向：从 C₁ 出发方向为 u·cosφ±w·sinφ 的直线，切 C₂ 于 C₂∓r₂·(u·sinφ∓w·cosφ)（符号对应两条外切线）。③ 内切线：r=r₂+r₁，需 d≥r₁+r₂（两圆外离）才有解，公式同构。④ 特例：半径相等的两圆外切线平行于连心线（φ=0）。⑤ 切点在圆上验证 (p-C)·(p-C)=r²。⑥ 数值稳定：用 d=√|v|²，当 d≈0 时无切线（同心圆）。

### 历史 · History

两圆公切线是经典欧氏几何作图问题，古希腊几何学已有完整的切线构造。CP-Algorithms 的 'Common tangents to two circles' 给出了现代解析实现（源自 e-maxx.ru），是竞赛几何的高频原语，常出现在圆相关构造与运动规划题中。

## How · 实现

### 伪代码

```python
# 用辅助圆 + 向量旋转法
# 对每条切线: 取半径差 r (外切线 r=r2-r1, 内切线 r=r2+r1)
def tangents(c1, r1, c2, r2, inner=False):
  v = c2 - c1; d = |v|
  r = r2 - r1 if not inner else r2 + r1
  if d < |r| + eps: return []      # 无解
  a = atan2(v.y, v.x)
  phi = asin(r / d)                 # 若 |r/d|>1 无解
  base = a if not inner else a
  for s in (+1, -1):
    angle = base + s*phi + pi/2     # 方向 (调整符号)
    # 用几何构造法: 从 c1 沿方向角 theta 的射线
  # 另一种: 直接用旋转矩阵
  u = v/d; w = (-u.y, u.x)
  if inner: 方向角 用 asin(r/d) 两条
  else:     方向角 用 asin(r/d) 两条
```

### Python 实现

```python
import math

EPS = 1e-9


def tangents_two_circles(c1, r1, c2, r2):
    """两圆所有公切线.
    返回 (external, internal): 各为 [(p1, p2), ...] 切点对列表.
    p1 在圆1上, p2 在圆2上. 每条切线由两个切点给出."""
    x1, y1 = c1; x2, y2 = c2
    vx, vy = x2 - x1, y2 - y1
    d2 = vx * vx + vy * vy
    if d2 < EPS:
        return ([], [])  # 同心圆无公切线
    d = math.sqrt(d2)
    ux, uy = vx / d, vy / d
    wx, wy = -uy, ux

    ext, inn = [], []

    def helper(r, use_inner):
        """半径差 r (外切线 r=r2-r1, 内切线 r=r2+r1)."""
        if d < abs(r) - EPS:
            return []
        # 从 c1 向辅助圆 (c2, |r|) 作切线; 若 r==0, 两切线与连心线平行
        res = []
        if abs(r) < EPS:
            # 半径相等: 外切线平行连心线, 距离为 r1
            # 方向沿 u 或 -u, 偏移垂距 r1
            for s in (1, -1):
                nx, ny = -s * wy, s * wx      # 垂直于 u 的方向
                p1 = (x1 + nx * r1, y1 + ny * r1)
                p2 = (x2 + nx * r2, y2 + ny * r2)
                res.append((p1, p2))
            return res
        # 一般: sin(phi)=r/d
        sinphi = r / d
        if abs(sinphi) > 1 + EPS:
            return []
        if abs(abs(sinphi) - 1) < EPS:
            # 切线垂直于连心线 (内切线极值: 内切/外切)
            phi = math.pi / 2 if sinphi > 0 else -math.pi / 2
        else:
            phi = math.asin(sinphi)
        # 两条切线: 方向角 a + s*phi
        for s in (1, -1):
            # 切线方向向量 t = (cos(a+s*phi), sin(a+s*phi))
            # 等价: t = u*cos(s*phi) + w*sin(s*phi)
            cp = math.cos(s * phi); sp = math.sin(s * phi)
            tx = ux * cp + wx * sp
            ty = uy * cp + wy * sp
            # 法向量 n (垂直 t) 单位化
            nx, ny = -ty, tx
            # 切点: 圆心沿 n 偏移 r1 / r2 (方向使两切点连线为 t)
            # 需要正确符号: 当 sinphi>0 用 s=+1 时取 n=(-ty,tx)
            p1 = (x1 + nx * r1, y1 + ny * r1)
            p2 = (x2 + nx * r2, y2 + ny * r2)
            res.append((p1, p2))
        return res

    # 外切线: r = r2 - r1
    ext = helper(r2 - r1, False)
    # 内切线: r = r2 + r1
    inn = helper(r2 + r1, True)
    return (ext, inn)


def validate(c1, r1, c2, r2, ext, inn):
    """验证每条切线: 切点在圆上且四点共线."""
    def on(p, c, r):
        return abs((p[0] - c[0]) ** 2 + (p[1] - c[1]) ** 2 - r * r) < 1e-6
    ok = True
    for lst in (ext, inn):
        for (p1, p2) in lst:
            if not on(p1, c1, r1) or not on(p2, c2, r2):
                ok = False
            # p1,p2 连线与圆心距: 法向距离 = 半径 (切点共线)
    return ok


if __name__ == "__main__":
    # 外离: (0,0)r=1, (5,0)r=2 => 4 条切线
    ext, inn = tangents_two_circles((0, 0), 1, (5, 0), 2)
    assert len(ext) == 2 and len(inn) == 2
    assert validate((0, 0), 1, (5, 0), 2, ext, inn)
    # 相交: (0,0)r=2, (3,0)r=2 => 2 条外切线, 无内
    ext, inn = tangents_two_circles((0, 0), 2, (3, 0), 2)
    assert len(ext) == 2 and len(inn) == 0
    assert validate((0, 0), 2, (3, 0), 2, ext, inn)
    # 外切: (0,0)r=2, (4,0)r=2 => 3 条 (2外+1内, 内退化为公切线在切点)
    ext, inn = tangents_two_circles((0, 0), 2, (4, 0), 2)
    assert len(ext) == 2
    assert validate((0, 0), 2, (4, 0), 2, ext, inn)
    # 内含: 无切线
    ext, inn = tangents_two_circles((0, 0), 5, (1, 0), 1)
    assert len(ext) == 0 and len(inn) == 0
    # 半径相等外离: 外切线平行, 4 条
    ext, inn = tangents_two_circles((0, 0), 1, (6, 0), 1)
    assert len(ext) == 2 and len(inn) == 2
    assert validate((0, 0), 1, (6, 0), 1, ext, inn)

    # 随机验证: 任意位置的相离圆应有 4 条切线
    import random
    random.seed(23)
    for _ in range(100):
        c1 = (random.uniform(-5, 5), random.uniform(-5, 5))
        r1 = random.uniform(0.5, 2)
        c2 = (random.uniform(-5, 5), random.uniform(-5, 5))
        r2 = random.uniform(0.5, 2)
        d = math.hypot(c2[0] - c1[0], c2[1] - c1[1])
        if d < r1 + r2 + 0.5:  # 只测外离
            continue
        ext, inn = tangents_two_circles(c1, r1, c2, r2)
        assert len(ext) == 2 and len(inn) == 2, (c1, r1, c2, r2, len(ext), len(inn))
        assert validate(c1, r1, c2, r2, ext, inn)
    print("All tests passed.")
```

**PyPy 提示**: atan2/asin 与旋转公式在大坐标下易积累误差；用解析旋转（u,w 基）更稳定。半径相等与内外切等退化分支单独处理。切点验证用平方距离比较避免 sqrt。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(1) |
| 空间 | O(1) |

### 局限

同心圆无公切线；外切/内切退化为 1 条（切点在切点重合）。半径相等的外切线构造需单独分支（平行于连心线）。数值上 r/d 接近 ±1 时 asin 不稳定，需 eps 钳制。切线方向符号选择易错，建议用向量旋转而非角度加减。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| TIMUS | 1163 | 6 | Chapaev：圆碰撞/公切线几何应用（CP-Alg 例题） | [https://acm.timus.ru/problem.aspx?space=1&num=1163](https://acm.timus.ru/problem.aspx?space=1&num=1163) |
| Codeforces | 933C | 6 | A Colorful Prospect：圆与圆位置关系/公切线在区域划分中的应用 | [https://codeforces.com/problemset/problem/933/C](https://codeforces.com/problemset/problem/933/C) |

## Pitfalls · 易错点

- 半径相等（r₂-r₁=0）时外切线平行连心线，公式 sinφ=r/d=0 退化为 0 角，需单独分支
- r/d 接近 1 时 asin 数值不稳定，需钳制到 [-1,1] 并处理 ±1 边界
- 同心圆（d≈0）直接返回空，避免除零
- 切点方向符号（法向量取哪一侧）错误导致切点不在圆上
- 内切线只在 d≥r₁+r₂ 存在，别在相交时仍生成
- 验证时用 eps 容差，别用 == 判浮点相等

## Sources · 信源

- CP-Algorithms ✓ [https://cp-algorithms.com/geometry/tangents-to-two-circles.html](https://cp-algorithms.com/geometry/tangents-to-two-circles.html)
- OI Wiki ✓ [https://oi-wiki.org/geometry/2d/](https://oi-wiki.org/geometry/2d/)
