---
id: polygon
name: Polygon出题平台
group: G-E-9
stage: advanced
priority: P3
depth_tier: brief
---

# Polygon出题平台

> Codeforces多人协作出题平台：版本管理+validator/generator/checker/solutions环环相扣+数据自动生成+对拍(stress)

<!-- 元信息: id=polygon · group=G-E-9 · stage=advanced · priority=P3 · depth_tier=brief -->

## What · 是什么

Polygon(polygon.codeforces.com)是Codeforces官方出题平台，支持多人协作、版本管理，是CF出题的唯一入口。其出题管线环环相扣：validator(数据校验) → generator(数据生成) → checker(评测) → solutions(标程/错解标记) → tests(测试数据)。在Polygon中：Files上传源码(generator/checker/validator/interactor)，Tests页用脚本'generator [参数] > test编号'自动生成数据(输出自动由标程生成)，Stresses页对拍找反例，Invocation页跑solution验证，General Info/Statement页填时间空间限制与TeX题面。数据用'少量带命令行参数的generator批量生成'而非手造，pretests需手动添加且为tests子集。题目打包后可导出为CF/其他OJ可用的格式。

## Why · 为什么

### 直觉 · Intuition

出题最怕三件事：数据错、错解AC、正解TLE。Polygon把'出题'做成流水线并引入版本管理：改错数据有历史可回滚，错解AC会自动警告，validator在生成前就拦截非法数据。多人协作时不用互传文件，改动留痕。

### 原理 · Principle

核心流程：(1)General Info设时限/内存/类型/标签; Statement用TeX子集写题面(非Markdown); (2)Files上传validator/generator/checker(或选内置checker如ncmp/rcmp4); (3)Validator Tests/Checker Tests可加样本验证逻辑; (4)Tests页写生成脚本如 gen -n10 > 1, gen -n100 > $  (自动编号), 标程自动产出out; 勾选Use in statements则成为样例; (5)Solutions上传多个solution, 标记'正确/错误(应WA/TLE/RE)', Polygon自动跑所有solution于所有数据并警告'错解AC/正解未AC'; (6)Stresses配置对拍脚本(pattern支持[10..100]范围), 跑出反例可一键加入数据。全部组件绑定版本, 修改即产生新Rev。

### 历史 · History

Polygon由Mike Mirzayanov创建, 是Codeforces多年出题沉淀的产物, 与testlib.h深度绑定(全部内置组件即testlib程序)。已成为国际出题事实标准, ICPC区域赛/CF官方题均经Polygon出产。OI Wiki的polygon页给出中文完整教程。

## How · 实现

### 伪代码

```python
# 出题流程(概念模板)
1. 创建题目, General Info 设时限/内存
2. Files 上传 gen.cpp / val.cpp / chk.cpp / std.cpp
3. Tests 页:
   gen -n10   > 1
   gen -n100  > $        # $ = 自动编号
   gen -n1000 -t=chain > $   # 命名参数
   勾选样例数据 'Use in statements'
4. Solutions 上传正解与错解, 标注预期结果
5. Stresses 配置对拍脚本, 收集反例
6. Invocation 验证所有solution
7. 打包导出题目包
```

### Python 实现

```python
"""Polygon 出题流程的本地等价物(离线快速原型)参考实现.
自测: 验证数据生成/对拍脚本模式逻辑.
"""
import random
import re
import subprocess
import sys
import os
from pathlib import Path


# ---------- 数据生成脚本模式解析 ----------
def parse_test_script(line, test_index):
    """解析Polygon式生成脚本: 'gen -n10 > 1' 或 'gen -n100 > $'.
    返回 (generator, args_list, out_index)
    """
    m = re.match(r"^(\S+)\s+(.*?)\s*>\s*(\$|\d+)$", line.strip())
    if not m:
        raise ValueError(f"bad script: {line}")
    gen, args, out = m.group(1), m.group(2), m.group(3)
    out_idx = test_index if out == "$" else int(out)
    args_list = re.findall(r"(?:-\w+)\s*(?:=|\s)?(\S*)", args) if args else []
    return gen, args_list, out_idx


def gen_data(script_lines, workdir):
    """模拟Polygon Tests页批量生成: 逐条执行并写文件.
    返回生成的测试点编号列表.
    """
    out_idx = 0
    produced = []
    for line in script_lines:
        gen, args, idx = parse_test_script(line, out_idx)
        out_idx += 1
        # 本地用echo模拟generator输出
        data = f"{gen} {' '.join(args)}\n".encode()
        (Path(workdir) / f"{idx}").write_bytes(data)
        produced.append(idx)
    return produced


# ---------- Stress 脚本范围模式 ----------
def expand_script_pattern(pattern, seed):
    """展开 '[10..100]' 为随机值(等价Polygon Stresses pattern)."""
    random.seed(seed)

    def repl(m):
        lo, hi = int(m.group(1)), int(m.group(2))
        return str(random.randint(lo, hi))

    return re.sub(r"\[(\d+)..(\d+)\]", repl, pattern)


if __name__ == "__main__":
    import shutil
    workdir = "/tmp/opencode/batch13/_polygon_test"
    shutil.rmtree(workdir, ignore_errors=True)
    os.makedirs(workdir, exist_ok=True)

    # 脚本解析
    g, a, i = parse_test_script("gen -n10 > 1", 0)
    assert (g, i) == ("gen", 1), (g, i)
    g2, a2, i2 = parse_test_script("gen -n100 -t=chain > $", 3)
    assert i2 == 3 and g2 == "gen"

    # 批量生成
    produced = gen_data(["gen -n10 > 1", "gen -n100 > $"], workdir)
    assert produced == [1, 1]  # 第二条用$取当前计数器1
    assert (Path(workdir) / "1").exists()

    # stress 范围展开
    p = expand_script_pattern("gen -n[10..100] -k[1..5]", seed=7)
    assert re.search(r"-n\d+", p) and re.search(r"-k\d+", p)

    shutil.rmtree(workdir, ignore_errors=True)
    print("polygon(参考): ALL TESTS PASSED")

```

**PyPy 提示**: Polygon本身是web平台(生成/校验/评测在云端), 无需Python脚本; 离线原型可用本文件逻辑理解生成脚本与stress pattern。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 数据生成/校验/评测开销由题目数据规模决定 |
| 空间 | O(测试数据总量) |

### 局限

题面仅支持TeX子集(非Markdown); pretests需手动添加; 所有组件强绑定版本, 修改需重新评测; 多人编辑需注意Edit session冲突(Discard会不可恢复)。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| OI Wiki | Polygon使用教程 | 0 | Polygon题目管理/Statement/Files/Checker/Tests/Stresses全流程 | [https://oi-wiki.org/tools/polygon/](https://oi-wiki.org/tools/polygon/) |
| Polygon | 官方平台 | 0 | 实际出题操作入口 | [https://polygon.codeforces.com](https://polygon.codeforces.com) |
| Codeforces | Polygon帮助 | 0 | 生成脚本与Freemarker批量生成官方文档 | [https://polygon.codeforces.com/docs/freemarker-manual](https://polygon.codeforces.com/docs/freemarker-manual) |

## Pitfalls · 易错点

- 题面不能写Markdown, 必须用TeX(如\textbf{})
- 数据推荐用带参数的generator批量生成, 避免手写一堆文件
- 给CF出题必须手动添加pretests测试集且是tests子集
- Edit session的Discard不可恢复, 慎用
- 改生成器/校验器后需重新跑所有相关solution验证

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/tools/polygon/](https://oi-wiki.org/tools/polygon/)
- polygon ✓ [https://polygon.codeforces.com](https://polygon.codeforces.com)
