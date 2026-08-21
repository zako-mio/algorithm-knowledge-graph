---
id: expression-eval
name: 表达式求值
group: G-E-7
stage: intermediate
priority: P1
depth_tier: standard
---

# 表达式求值

> 中缀→后缀(逆波兰)→栈求值；双栈法O(n)；含一元/右结合运算符扩展

<!-- 元信息: id=expression-eval · group=G-E-7 · stage=intermediate · priority=P1 · depth_tier=standard -->

## What · 是什么

表达式求值指读入字符串表达式输出其值。核心思路：中缀表达式对人直观但需处理优先级与括号，计算机更适合后缀(逆波兰)表达式。方法有 ①表达式树(递归语法分析后自底向上求值) ②双栈法(数字栈+运算符栈，隐式转后缀边扫边算) ③直接转后缀再求值。所有方法在 O(n) 时间内完成。扩展情形含一元运算符(+/-)与右结合运算符(^)。

## Why · 为什么

### 直觉 · Intuition

中缀的难点在'先算谁'由优先级决定。双栈法把'优先级高的运算符先执行'编码进扫描过程：遇到低优先级/右括号时把栈内优先级不低于它的运算符先弹掉运算，等价于把中缀转成了后缀再算。

### 原理 · Principle

双栈法规则：遇到数字直接入数字栈；左括号入运算符栈；右括号弹运算符栈直到左括号并逐次运算；普通运算符弹出所有优先级>=当前运算符的栈顶后入栈；扫描完把剩余运算符全部弹出运算。一元运算符需用 may_be_unary 标志区分(运算符/左括号/串首后的一元优先；右结合时等优先级不弹)。

### 历史 · History

逆波兰表达式由波兰逻辑学家 Jan Łukasiewicz(1920s)提出，反向的记法被称为 Reverse Polish Notation。双栈法即 Dijkstra 调车场算法(Shunting-yard algorithm)的变形。OI Wiki 表达式求值页(译自 e-maxx.ru / CP-Algorithms)给出含一元与右结合运算符的完整实现，并列出 NOIP2013 普及组表达式求值等经典习题。

## How · 实现

### 伪代码

```python
def priority(op):
  if op in '+-': return 1
  if op in '*/': return 2
  return 0

def process(st, op):
  r = st.pop(); l = st.pop()
  按 op 计算 l (op) r 压回

def evaluate(s):
  st, ops = [], []
  for ch in s:
    if ch.isdigit(): st.push(int(ch))
    elif ch == '(': ops.push(ch)
    elif ch == ')':
      while ops.top() != '(': process(st, ops.pop())
      ops.pop()  # 丢弃左括号
    else:
      while ops and priority(ops.top()) >= priority(ch):
        process(st, ops.pop())
      ops.push(ch)
  while ops: process(st, ops.pop())
  return st.top()
```

### Python 实现

```python
def evaluate(expr):
    """双栈法求中缀表达式值, 支持 + - * / 与括号。
    数字可为多位数; 除法为向下取整(竞赛常用)。
    """
    st = []
    ops = []
    prec = {'+': 1, '-': 1, '*': 2, '/': 2}

    def apply(op):
        r = st.pop()
        l = st.pop()
        if op == '+':
            st.append(l + r)
        elif op == '-':
            st.append(l - r)
        elif op == '*':
            st.append(l * r)
        elif op == '/':
            st.append(l // r)

    i = 0
    n = len(expr)
    while i < n:
        c = expr[i]
        if c == ' ':
            i += 1
            continue
        if c.isdigit():
            num = 0
            while i < n and expr[i].isdigit():
                num = num * 10 + int(expr[i])
                i += 1
            st.append(num)
            continue
        if c == '(':
            ops.append(c)
        elif c == ')':
            while ops and ops[-1] != '(':
                apply(ops.pop())
            ops.pop()  # 移除 '('
        elif c in prec:
            while ops and ops[-1] != '(' and prec[ops[-1]] >= prec[c]:
                apply(ops.pop())
            ops.append(c)
        else:
            raise ValueError(f'未知字符: {c}')
        i += 1
    while ops:
        apply(ops.pop())
    return st[-1]


def to_rpn(expr):
    """中缀转后缀(逆波兰), 演示转换过程。"""
    out = []
    ops = []
    prec = {'+': 1, '-': 1, '*': 2, '/': 2}
    for c in expr:
        if c == ' ':
            continue
        if c.isdigit():
            out.append(c)
        elif c == '(':
            ops.append(c)
        elif c == ')':
            while ops and ops[-1] != '(':
                out.append(ops.pop())
            ops.pop()
        else:
            while ops and ops[-1] != '(' and prec[ops[-1]] >= prec[c]:
                out.append(ops.pop())
            ops.append(c)
    while ops:
        out.append(ops.pop())
    return ''.join(out)


if __name__ == '__main__':
    assert evaluate('3+2*2') == 7
    assert evaluate('(1+2)*3') == 9
    assert evaluate('20/(4+1)') == 4          # 20//5
    assert evaluate('1+2+3') == 6
    assert evaluate('2*(3+4)-5') == 9


    assert to_rpn('3+2*2') == '322*+'
    assert to_rpn('(1+2)*3') == '12+3*'

    # 与 Python 结果对照的复杂表达式(非负整除场景)
    for s in ['2+3*4-6/2', '10-2-3', '4/(2)+6']:
        assert evaluate(s) == eval(s.replace('/', '//')), s

    print('evaluate(3+2*2)  =', evaluate('3+2*2'))
    print('evaluate((1+2)*3) =', evaluate('(1+2)*3'))
    print('evaluate(20/(4+1))=', evaluate('20/(4+1)'))
    print('RPN of 3+2*2     =', to_rpn('3+2*2'))
    print('RPN of (1+2)*3   =', to_rpn('(1+2)*3'))
    print('All expression-eval tests passed!')

```

**PyPy 提示**: 双栈法对 Python 完全是线性开销, PyPy 直接跑即可; 大数据量用 list 当栈, 避免自定义类; 竞赛中遇到取模表达式(如 NOIP P1981 结果对 10000 取模)可在 apply 内同步取模防溢出(CPP 需 long long)。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | O(N) — 每个字符至多进出栈各一次 |
| 空间 | O(N) — 两个栈总长度 O(N) |

### 局限

双栈法默认运算符左结合; 处理右结合(如幂^)或一元运算符需扩展 may_be_unary 与优先级规则; 除法/取模语义需按题目确认(整除/真除法/模负数); 括号不匹配或非法字符需自行判错。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| Luogu | P1981 | 2 | NOIP2013普及组 表达式求值: 中缀转后缀+取模, 标准双栈模板题 | [https://www.luogu.com.cn/problem/P1981](https://www.luogu.com.cn/problem/P1981) |
| Luogu | P1449 | 2 | 后缀表达式: 直接数字栈求值, 逆波兰入门 | [https://www.luogu.com.cn/problem/P1449](https://www.luogu.com.cn/problem/P1449) |
| SPOJ | ONP | 2 | Transform the Expression: 中缀转后缀经典题 | [https://www.spoj.com/problems/ONP/](https://www.spoj.com/problems/ONP/) |

## Pitfalls · 易错点

- 出栈顺序: 先弹的是右操作数, process(op) 里 l=st[-2], r=st[-1], 顺序反了减法/除法错
- 右括号处理时要确保栈非空且最终把左括号丢弃, 漏丢会死循环
- 多位数输入需 while isdigit 连读, 只取单字符会在 20 这类数上出错
- 除法语义: 竞赛中常用向下取整, 但 Python 的 // 对负数向负无穷, 与 C++ 向零截断不同, 需按题确认
- 运算符优先级数组别漏 ( 的特判(它只起分隔作用, 不参与比较优先级)

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/misc/expression/](https://oi-wiki.org/misc/expression/)
- OI Wiki ✓ [https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/expression.md](https://raw.githubusercontent.com/OI-wiki/OI-wiki/master/docs/misc/expression.md)
- CP-Algorithms ✓ [https://cp-algorithms.com/string/expression_parsing.html](https://cp-algorithms.com/string/expression_parsing.html)
