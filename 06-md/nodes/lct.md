---
id: lct
name: Link-Cut Tree（LCT，动态树）
group: G-D-4
stage: advanced
priority: P1
depth_tier: deep
---

# Link-Cut Tree（LCT，动态树）

> 用 Splay 森林维护实链剖分（Preferred Path Decomposition）的动态树数据结构，支持 O(log n) 均摊的加边、删边、换根、路径修改与路径查询。

<!-- 元信息: id=lct · group=G-D-4 · stage=advanced · priority=P1 · depth_tier=deep -->

## What · 是什么

LCT 用一组 Splay（辅助树）维护动态森林。原树被『实链剖分』为若干条实链（preferred path），每条实链放进一棵 Splay 中，Splay 的中序遍历对应原树上从上到下的一条链；每棵 Splay 的根通过虚边（认父不认子）指向其链顶在原树中的父节点。核心操作 access(x) 把 x 到根的路径暴露成一条实链（放进一棵 Splay），其余一切操作（makeroot 换根、link 连边、cut 删边、split 提取路径、findroot 求连通块根）都由若干次 access + splay 组合而成。所有基于 access 的操作均摊 O(log n)。

## Why · 为什么

### 直觉 · Intuition

树链剖分把静态树切成若干链再放线段树，但静态剖分无法应对动态加删边。LCT 的洞察：我们不需要固定剖分，而是『用哪条链就剖哪条』——让当前需要用到的路径实时变为一条实链，然后用 Splay 的区间操作去处理。虚边『认父不认子』的设计让森林在辅助树中仍然是一棵树，任何时刻辅助树都唯一对应一棵原树。

### 原理 · Principle

① 辅助树性质：每棵 Splay 对应原树一条从上到下的路径（中序遍历即路径顺序）；Splay 根的父亲指向路径顶端节点在原树的父节点（虚边，父不认子）。② access(x)：自下而上把 x 到原树根的路径全部改为实链——每次 splay(x) 后把 x 右儿子设为上一步的 y（y 是上段链的根），并把 x 原右儿子的虚边保留（认父不认子）。③ makeroot(x)：access(x)+splay(x) 后对 x 打翻转标记 rev，则 x 变为该树的新根（利用 Splay 区间翻转）。④ link(x,y)：makeroot(x) 后令 fa[x]=y（若 x,y 已连通则非法）。⑤ cut(x,y)：makeroot(x)+access(y)+splay(y) 后，x 是 y 的左儿子且没有右儿子，直接断开。⑥ split(x,y)：makeroot(x)+access(y)+splay(y)，此时 y 的 Splay 子树（中序整段）即 x→y 路径。复杂度证明基于 Splay 的势能分析：access 中 splay 部分 O(log n)，虚边访问的均摊复杂度亦为 O(log n)，故 m 次 access 为 O((n+m)log n)。

### 历史 · History

LCT 由 Daniel Sleator 与 Robert Tarjan 在 1983 年的论文《A Data Structure for Dynamic Trees》中提出，与 Splay 树同出于这两位作者（Sleator-Tarjan 1985 发表 Splay）。早期是自调整二叉搜索树思想在动态树上的扩展。国内 OI 竞赛中 LCT 模板（Luogu P3690）与大量题目（弹飞绵羊、洞穴勘测、Tree II 等）将其推向普及，OI Wiki 有系统中文教程。

## How · 实现

### 伪代码

```python
struct LCT:
    ch[0..n][2], fa[0..n], rev[0..n], sum[0..n], val[0..n]

    isroot(x):  return ch[fa[x]][0] != x and ch[fa[x]][1] != x
    pushup(x):  sum[x] = sum[ch[x][0]] + val[x] + sum[ch[x][1]]
    pushrev(x): swap(ch[x][0], ch[x][1]); rev[x] ^= 1
    pushdown(x): if rev[x]: pushrev(ch[x][0]); pushrev(ch[x][1]); rev[x]=0

    rotate(x):  # 经典 splay 旋转，注意 isroot 判断
    splay(x):   # 先下放路径上的翻转标记，再双旋

    access(x):
        last = 0
        while x:
            splay(x)
            ch[x][1] = last     # 实边切到 last，原右儿子变虚边
            pushup(x)
            last = x
            x = fa[x]           # 沿虚边向上
        return last

    makeroot(x): access(x); splay(x); pushrev(x)
    findroot(x):
        access(x); splay(x)
        while ch[x][0]: pushdown(x); x = ch[x][0]
        splay(x); return x
    split(x, y): makeroot(x); access(y); splay(y)   # 此时 y 子树即路径
    link(x, y):  makeroot(x); fa[x] = y             # 需判连通
    cut(x, y):   makeroot(x); access(y); splay(y)
                 # ch[y][0]==x 且 ch[x][1]==0 才合法，然后置零
```

### Python 实现

```python
class LinkCutTree:
    """教学实现：点权路径异或和（可改为 sum/max）。
    节点编号 1..n。
    """
    def __init__(self, n, val):
        self.n = n
        self.ch = [[0, 0] for _ in range(n + 1)]
        self.fa = [0] * (n + 1)
        self.rev = [0] * (n + 1)
        self.val = [0] + val[:]
        self.sum = [0] * (n + 1)
        for i in range(1, n + 1):
            self.sum[i] = self.val[i]

    def _isroot(self, x):
        f = self.fa[x]
        return f == 0 or (self.ch[f][0] != x and self.ch[f][1] != x)

    def _pushup(self, x):
        self.sum[x] = self.sum[self.ch[x][0]] ^ self.sum[self.ch[x][1]] ^ self.val[x]

    def _pushrev(self, x):
        self.ch[x][0], self.ch[x][1] = self.ch[x][1], self.ch[x][0]
        self.rev[x] ^= 1

    def _pushdown(self, x):
        if self.rev[x]:
            self._pushrev(self.ch[x][0])
            self._pushrev(self.ch[x][1])
            self.rev[x] = 0

    def _rotate(self, x):
        y, z = self.fa[x], self.fa[self.fa[x]]
        c = self.ch[y][1] == x
        b = self.ch[x][c ^ 1]
        if not self._isroot(y):
            self.ch[z][self.ch[z][1] == y] = x
        self.fa[x] = z
        self.ch[y][c] = b
        if b:
            self.fa[b] = y
        self.fa[y] = x
        self.ch[x][c ^ 1] = y
        self._pushup(y)
        self._pushup(x)

    def _splay(self, x):
        st = [x]
        y = x
        while not self._isroot(y):
            y = self.fa[y]
            st.append(y)
        for v in reversed(st):
            self._pushdown(v)
        while not self._isroot(x):
            y, z = self.fa[x], self.fa[self.fa[x]]
            if not self._isroot(y):
                if (self.ch[y][1] == x) == (self.ch[z][1] == y):
                    self._rotate(y)
                else:
                    self._rotate(x)
            self._rotate(x)

    def access(self, x):
        last = 0
        while x:
            self._splay(x)
            self.ch[x][1] = last
            self._pushup(x)
            last = x
            x = self.fa[x]
        return last

    def makeroot(self, x):
        self.access(x)
        self._splay(x)
        self._pushrev(x)

    def findroot(self, x):
        self.access(x)
        self._splay(x)
        while self.ch[x][0]:
            self._pushdown(x)
            x = self.ch[x][0]
        self._splay(x)
        return x

    def split(self, x, y):
        self.makeroot(x)
        self.access(y)
        self._splay(y)
        return self.sum[y]

    def link(self, x, y):
        self.makeroot(x)
        if self.findroot(y) != x:
            self.fa[x] = y

    def cut(self, x, y):
        self.makeroot(x)
        self.access(y)
        self._splay(y)
        if self.ch[y][0] == x and self.ch[x][1] == 0:
            self.ch[y][0] = 0
            self.fa[x] = 0
            self._pushup(y)

    def connected(self, x, y):
        if x == y:
            return True
        self.makeroot(x)
        return self.findroot(y) == x

if __name__ == '__main__':
    n = 5
    val = [1, 2, 3, 4, 5]
    lct = LinkCutTree(n, val)
    # 建树: 1-2, 1-3, 3-4, 3-5
    lct.link(1, 2)
    lct.link(1, 3)
    lct.link(3, 4)
    lct.link(3, 5)
    assert lct.connected(2, 5)
    print('path 2..5 xor =', lct.split(2, 5))
    assert lct.split(2, 5) == (2 ^ 1 ^ 3 ^ 5)  # 2-1-3-5
    # 换根后查询不同路径
    lct.makeroot(4)
    assert lct.split(4, 1) == (4 ^ 3 ^ 1)
    # 删边 1-3，断开 1 与 3/4/5
    lct.cut(1, 3)
    assert not lct.connected(1, 4)
    assert lct.connected(3, 5)
    print('OK')
```

**PyPy 提示**: Python 教学实现常数大，n 达 1e5 全功能操作在 PyPy 下约 3-5s 量级，竞赛通常仅作了解或小数据题；若必须用，应内联 _isroot/_pushup、用数组替代属性、避免递归。PyPy 的 while 循环性能尚可，真正瓶颈是 _splay 中的 path 收集（可用显式栈）。生产环境建议 C++。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | access/splay/makeroot/link/cut/split 均摊 O(log n)；初始化 O(n) |
| 空间 | O(n) |

### 局限

只维护路径信息，子树信息需配合虚子树维护（较复杂）；均摊而非最坏界，个别操作可能 O(n)（但摊还 O(log n)）；Python 实现常数大，大范围数据不建议用 Python 提交。实现细节极多，isroot 判断、翻转标记顺序、cut 合法性检查缺一不可，稍错即 WA。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P3690 | 5 | 【模板】动态树（LCT）：link/cut/路径异或查询全功能模板 | [https://www.luogu.com.cn/problem/P3690](https://www.luogu.com.cn/problem/P3690) |
| Luogu | P3203 | 4 | [HNOI2010] 弹飞绵羊：i 向 i+a[i] 连边，改装根（n+1 为虚拟根），查询跳出的步数即到虚拟根的路径长度 | [https://www.luogu.com.cn/problem/P3203](https://www.luogu.com.cn/problem/P3203) |
| Luogu | P2147 | 4 | [SDOI2008] 洞穴勘测：link/cut/连通性查询，LCT 基础应用 | [https://www.luogu.com.cn/problem/P2147](https://www.luogu.com.cn/problem/P2147) |
| Luogu | P1501 | 6 | [国家集训队] Tree II：路径加/乘/求和，需在 Splay 上维护 add/mul 双懒标记 | [https://www.luogu.com.cn/problem/P1501](https://www.luogu.com.cn/problem/P1501) |
| Luogu | P4234 | 7 | 最小差值生成树：边权转点权（边结点），LCT 维护最大边权，加边删边求最小差值 | [https://www.luogu.com.cn/problem/P4234](https://www.luogu.com.cn/problem/P4234) |

## Pitfalls · 易错点

- isroot 用 fa 判断而不用『儿子是否为 x』，否则虚边方向错误
- _rotate 中必须先判断 y 是否 isroot 再改 z 的儿子，否则破坏辅助树
- splay 前必须把祖先链上的 rev 标记按序下放，否则翻转错位
- makeroot 的 rev 标记会反转路径，查询路径前要先 pushdown 再取信息
- cut 必须先验证 ch[y][0]==x 且 ch[x][1]==0（x 与 y 直连）才断开
- 节点编号从 1 开始，0 号节点的 fa/ch 恒为 0，isroot(0) 需特判
- access 里要 pushup(x)，忘记更新 sum 是常见 WA 源

## Sources · 信源

- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/lct.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/ds/lct.md)
- OI Wiki ✓ [https://oi-wiki.org/ds/lct/](https://oi-wiki.org/ds/lct/)
