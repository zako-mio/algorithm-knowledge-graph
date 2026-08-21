---
id: oj-tool
name: OJ工具
group: G-E-9
stage: intermediate
priority: P2
depth_tier: standard
---

# OJ工具

> cf-tool/Competitive Companion/ac-predictor等命令行与浏览器工具，简化样例拉取、测试、提交与rating跟踪

<!-- 元信息: id=oj-tool · group=G-E-9 · stage=intermediate · priority=P2 · depth_tier=standard -->

## What · 是什么

OJ工具是指辅助在线评测平台使用的命令行工具与浏览器插件，核心是提高'读题-写码-测试-提交-看结果'的流转效率。代表性工具：(1)cf-tool(xalanq/cf-tool)：Codeforces命令行工具，支持cf race(拉取比赛并倒计时)、cf gen(模板生成代码)、cf test(编译测样例)、cf submit(提交)、cf stand(看榜单)、cf list(题目信息)；(2)Competitive Companion：浏览器插件，一键解析题目页面样例数据并推送到本地的监听工具；(3)ac-predictor：Tampermonkey脚本，预测AtCoder rating变化；(4)Codeforces Visualizer：可视化统计个人CF做题分布/对比用户/预测Rating。对Python选手，也可用requests脚本封装提交与状态轮询。

## Why · 为什么

### 直觉 · Intuition

打比赛时最浪费时间的是'复制样例-编译-手动输入-提交-盯状态'这些重复动作。命令行工具把整套流程脚本化：一条cf race拉到全部题与样例，cf test一键测完，cf submit一键提交并轮询结果。解放注意力去思考算法本身。

### 原理 · Principle

cf-tool工作流：cf config配置账号与模板→cf race <id>拉取比赛到当前目录(自动开浏览器并倒计时)→cd 1136/a进入题目目录(内含样例in/out)→cf gen按模板生成a.cpp→写码→cf test编译+跑样例→cf submit提交→cf list/stand查看状态。新增样例: 放inK.txt与ansK.txt即可。Competitive Companion将页面解析的样例以JSON发到本地端口(如127.0.0.1:10045)，配合任何监听工具自动生成测试文件。cfviz读取CF API渲染用户数据图表。ac-predictor在排行榜页覆盖计算rating预测值。

### 历史 · History

随着Codeforces/AtCoder生态繁荣，社区开发了一系列效率工具。cf-tool是CF生态最流行的CLI之一(2019年起持续维护)，Competitive Companion是主流OJ通用的样例抓取插件，ac-predictor在AtCoder社区广泛使用。OI Wiki的oj-tool页集中介绍了这批工具。

## How · 实现

### 伪代码

```python
# cf-tool 基础流
cf config          # 配置用户名/密码/模板
cf race 1136       # 开始比赛1136(拉取题目+样例, 倒计时)
cd 1136/a
cf gen             # 生成模板代码 a.cpp
<写代码>
cf test            # 编译并运行样例
cf submit          # 提交 a.cpp
cf list / cf stand # 查看题目信息/榜单

# Competitive Companion
浏览器打开题目页-> 点插件 -> 样例推送到 127.0.0.1:10045
# 本地监听(任意端口)把JSON写成 in/out 文件
```

### Python 实现

```python
"""OJ工具: 一个极简的CF式工具集(拉样例/对拍提交/轮询状态)参考实现.
自测: 验证本地样例拉取与状态判定逻辑.
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path


def load_samples(json_str):
    """解析Competitive Companion格式的样例JSON.
    返回 [(input_text, output_text), ...]
    """
    d = json.loads(json_str)
    tests = d.get("tests", [])
    return [(t["input"], t["output"]) for t in tests]


def save_samples(samples, problem_dir):
    """把样例写入 problem_dir/in{i}.txt 与 out{i}.txt."""
    p = Path(problem_dir)
    p.mkdir(parents=True, exist_ok=True)
    for i, (inp, out) in enumerate(samples):
        (p / f"in{i}.txt").write_text(inp)
        (p / f"out{i}.txt").write_text(out)
    return len(samples)


def run_samples(exec_cmd, problem_dir):
    """依次跑样例, 返回 [(通过?, 期望, 实际)]"""
    p = Path(problem_dir)
    results = []
    idx = 0
    while (p / f"in{idx}.txt").exists():
        inp = (p / f"in{idx}.txt").read_text()
        exp = (p / f"out{idx}.txt").read_text()
        r = subprocess.run(
            exec_cmd, input=inp, capture_output=True, text=True, shell=True
        )
        got = r.stdout
        results.append((got.strip() == exp.strip(), exp, got))
        idx += 1
    return results


def parse_verdict(status_text):
    """解析提交状态文本为可读verdict."""
    s = status_text.upper()
    if "ACCEPTED" in s:
        return "AC"
    if "WRONG" in s:
        return "WA"
    if "TIME" in s:
        return "TLE"
    if "RUNTIME" in s:
        return "RE"
    if "COMPILATION" in s:
        return "CE"
    return status_text


if __name__ == "__main__":
    # 模拟Competitive Companion样例JSON
    sample_json = json.dumps({
        "tests": [
            {"input": "2 3\n", "output": "5\n"},
            {"input": "10 20\n", "output": "30\n"},
        ]
    })
    samples = load_samples(sample_json)
    assert len(samples) == 2
    saved = save_samples(samples, "/tmp/opencode/batch13/_oj_sample")
    assert saved == 2
    assert (Path("/tmp/opencode/batch13/_oj_sample") / "in0.txt").exists()

    # 用python单行命令模拟评测(输出两数之和)
    res = run_samples("python3 -c \"import sys; a,b=map(int,sys.stdin.read().split()); print(a+b)\"",
                      "/tmp/opencode/batch13/_oj_sample")
    assert all(r[0] for r in res), res

    # verdict解析
    assert parse_verdict("Accepted") == "AC"
    assert parse_verdict("Wrong answer on test 3") == "WA"
    assert parse_verdict("Time limit exceeded") == "TLE"

    # 清理
    import shutil
    shutil.rmtree("/tmp/opencode/batch13/_oj_sample", ignore_errors=True)
    print("oj-tool: ALL TESTS PASSED")

```

**PyPy 提示**: cf-tool是Go二进制, 直接放PATH即可。Python选手自建工具链注意: subprocess跑选手程序用shell=True时注意转义; 拉取样例JSON用requests+BeautifulSoup更稳。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 工具开销=IO/网络时间, 与题目规模无关 |
| 空间 | O(样例规模) |

### 局限

cf-tool主要支持Codeforces(Gym也支持); Competitive Companion需浏览器插件+本地监听器配合; ac-predictor仅AtCoder; 各OJ自定义评测环境仍需手动适配。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| GitHub | cf-tool | 0 | CF命令行工具: race/gen/test/submit/stand全流程 | [https://github.com/xalanq/cf-tool](https://github.com/xalanq/cf-tool) |
| GitHub | Competitive Companion | 0 | 浏览器插件: 解析主流OJ样例JSON推送本地端口 | [https://github.com/jmerle/competitive-companion](https://github.com/jmerle/competitive-companion) |
| OI Wiki | OJ工具页 | 0 | cf-tool/CF Visualizer/ac-predictor使用说明汇总 | [https://oi-wiki.org/tools/oj-tool/](https://oi-wiki.org/tools/oj-tool/) |

## Pitfalls · 易错点

- cf config需正确配置账号与模板路径, 否则submit会失败
- cf-tool需加入PATH才能作为cf命令调用
- Competitive Companion需先启动本地监听再点插件, 顺序颠倒收不到数据
- 新增样例命名必须为inK.txt/ansK.txt(K为数字)
- 不同OJ对提交状态轮询接口差异大, 自写脚本需分别适配

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/tools/oj-tool/](https://oi-wiki.org/tools/oj-tool/)
- github ✓ [https://github.com/xalanq/cf-tool](https://github.com/xalanq/cf-tool)
- github ✓ [https://github.com/jmerle/competitive-companion](https://github.com/jmerle/competitive-companion)
