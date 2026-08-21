---
id: stack
name: 栈
group: G-A-2
stage: basic
priority: P0
depth_tier: deep
---

# 栈

> LIFO后进先出结构，支持括号匹配/表达式求值等

<!-- 元信息: id=stack · group=G-A-2 · stage=basic · priority=P0 · depth_tier=deep -->

## What · 是什么

栈(Stack)是后进先出(LIFO, Last In First Out)的线性数据结构：只能在栈顶插入(push)和删除(pop)。Python 中用 list 的 append/pop 实现，或用 collections.deque。支持 O(1) 的栈顶访问。

## Why · 为什么

### 直觉 · Intuition

栈模拟了'叠盘子'——最后放上去的最先拿走。这种'最近相关'的属性天然适合需要回溯到上一个状态的问题：括号匹配(最近的左括号配最近的右括号)、函数调用栈(最近调用的最先返回)、表达式求值(最近的操作数先参与运算)。

### 原理 · Principle

栈维护一个线性序列，只允许在称为'栈顶'的一端操作。push(x): 将 x 放在栈顶；pop(): 移除并返回栈顶；top()/peek(): 查看栈顶不删除。用数组(list)实现时，push=append O(1)，pop()=O(1)，均摊。Python list 的 pop() 从尾部删除是 O(1)。关键应用：①括号匹配(遇左括号入栈，遇右括号弹栈匹配) ②表达式求值(双栈: 操作数栈+运算符栈，Shunting-yard 算法) ③DFS 的非递归实现 ④单调栈(进阶)。

### 历史 · History

栈是计算机科学中最基础的数据结构之一，与队列(FIFO)互为对偶。1960年代 ALGOL 的递归调用机制即依赖运行时栈。C++ STL 提供 std::stack(适配器，默认基于 deque)。Python 无专门的 Stack 类，用 list 或 deque 代替。

## How · 实现

### 伪代码

```python
push(x): st.append(x)
pop(): return st.pop()
top(): return st[-1]
empty(): return len(st) == 0
size(): return len(st)

# 括号匹配
for ch in s:
  if ch in '([{': st.push(ch)
  elif ch in ')]}':
    if st.empty() or not match(st.pop(), ch): return False
return st.empty()
```

### Python 实现

```python
from collections import deque

class Stack:
    """基于 deque 的栈实现(比 list 在头部插入更优, 这里仅尾部操作两者等效)。"""
    def __init__(self):
        self._data = deque()

    def push(self, x):
        self._data.append(x)

    def pop(self):
        return self._data.pop()

    def top(self):
        return self._data[-1]

    def empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)


def bracket_match(s):
    """括号匹配: 检查字符串中的括号是否正确配对。
    支持: () [] {}
    """
    pairs = {')': '(', ']': '[', '}': '{'}
    st = Stack()
    for ch in s:
        if ch in '([{':
            st.push(ch)
        elif ch in ')]}':
            if st.empty() or st.pop() != pairs[ch]:
                return False
    return st.empty()


def evaluate_rpn(tokens):
    """逆波兰表达式求值(后缀表达式)。
    示例: ['2','1','+','3','*'] => (2+1)*3 = 9
    """
    st = Stack()
    for tok in tokens:
        if tok in '+-*/':
            b = st.pop()
            a = st.pop()
            if tok == '+':
                st.push(a + b)
            elif tok == '-':
                st.push(a - b)
            elif tok == '*':
                st.push(a * b)
            elif tok == '/':
                st.push(int(a / b))  # 向零取整(竞赛惯例)
        else:
            st.push(int(tok))
    return st.pop()


if __name__ == '__main__':
    # 测试栈基本操作
    st = Stack()
    for i in range(5):
        st.push(i)
    print(f'Stack size: {st.size()}')  # 5
    print(f'Top: {st.top()}')  # 4
    while not st.empty():
        print(st.pop(), end=' ')  # 4 3 2 1 0
    print()

    # 测试括号匹配
    assert bracket_match('(a[b]{c})') == True
    assert bracket_match('([)]') == False
    assert bracket_match('(((') == False
    assert bracket_match('') == True
    print('Bracket match: all tests passed')

    # 测试逆波兰表达式
    assert evaluate_rpn(['2', '1', '+', '3', '*']) == 9
    assert evaluate_rpn(['4', '13', '5', '/', '+']) == 6  # 4 + (13/5=2) = 6
    assert evaluate_rpn(['18']) == 18  # 单个操作数
    print('RPN evaluate: all tests passed')

```

**PyPy 提示**: PyPy 对 list.append/pop 的 JIT 优化极好，性能接近 C；deque 在 PyPy 上也快；深递归用栈替代时注意 list 容量。N>1e6 的栈操作无性能瓶颈。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | push/pop/top/empty/size 均 O(1)；括号匹配 O(N)；RPN 求值 O(N) |
| 空间 | O(N) 最坏情况(全部入栈未弹出) |

### 局限

Python list 作为栈用时 pop() 从尾部 O(1)，但 pop(0) 从头部 O(N) → 需要队列语义时改用 deque；栈空间受递归深度限制(Python 默认 1000，需 sys.setrecursionlimit 提升)。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| LeetCode | 20 | 1 | 有效的括号: 栈经典模板题，括号匹配 | [https://leetcode.cn/problems/valid-parentheses/](https://leetcode.cn/problems/valid-parentheses/) |
| LeetCode | 150 | 2 | 逆波兰表达式求值: 栈模拟运算 | [https://leetcode.cn/problems/evaluate-reverse-polish-notation/](https://leetcode.cn/problems/evaluate-reverse-polish-notation/) |
| LeetCode | 155 | 2 | 最小栈: 辅助栈同步维护最小值 | [https://leetcode.cn/problems/min-stack/](https://leetcode.cn/problems/min-stack/) |

## Pitfalls · 易错点

- Python list.pop() 在空栈上抛 IndexError，需先判 empty()
- 括号匹配忘记处理'栈非空但已遍历完'(如 '(((' 不匹配)
- RPN 求值除法要注意取整方向(竞赛通常向零取整: int(a/b) 而非 a//b)
- 用 list 做栈时不要误用 pop(0)(O(N))，应 pop()(从尾部 O(1))

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/ds/stack/](https://oi-wiki.org/ds/stack/)
- CP-Algorithms ✓ [https://cp-algorithms.com/data_structures/stack.html](https://cp-algorithms.com/data_structures/stack.html)
- 书籍 ✓ `CPH ch4 p45`
