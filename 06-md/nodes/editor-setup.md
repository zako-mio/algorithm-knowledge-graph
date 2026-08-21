---
id: editor-setup
name: 编辑器配置
group: G-E-9
stage: intermediate
priority: P2
depth_tier: standard
---

# 编辑器配置

> VSCode/Vim/CLion等编辑器竞赛配置：编译任务、调试launch、代码片段、按键效率优化

<!-- 元信息: id=editor-setup · group=G-E-9 · stage=intermediate · priority=P2 · depth_tier=standard -->

## What · 是什么

编辑器配置是竞赛效率基建。核心目标：让'写码-编译-测试-调试'在编辑器内一键完成。主流方案：(1)VS Code：安装C/C++扩展(编译+调试+IntelliSense)或C/C++ Compile Run/Code Runner扩展(单文件一键运行F6/F7/F8)，配置tasks.json(编译任务)与launch.json(调试配置，gdb/LLDB)，还可配clangd提供补全；(2)Vim/Neovim：掌握模式与键位(命令/插入/底线命令行/可视)、宏录制、.命令、normal命令，配合编译插件与快速跳转；(3)CLion/JetBrains：图形化CMake项目与调试。竞赛专属配置：CP模板代码片段(读入/输出模板)、按F5一键编译带-DDEBUG/-fsanitize、提交前自动切-O2、代码片段快速插入(如STL头文件、二分模板)。

## Why · 为什么

### 直觉 · Intuition

编辑器是'战场工位'：工位越顺手，出枪越快。竞赛代码单文件为主、调试循环频繁，把'编译+跑样例+调试'绑成快捷键，把常用模板做成代码片段，能省下大量机械操作时间，把注意力留给算法。

### 原理 · Principle

VS Code配置要点：(1)tasks.json定义编译任务, 如 {"label":"build","command":"g++","args":["-std=c++17","-g","-Wall","${file}","-o","${fileDirname}/${fileBasenameNoExtension}"]}, 绑定Ctrl+Shift+B；(2)launch.json定义调试, F5启动, 用gdb选'g++ 生成和调试活动文件', 或LLDB(需CodeLLDB扩展)；(3)IntelliSense配置includePath/standard。Vim要点：hjkl移动、i/a/o进入插入、v/V/ctrl-v可视模式、dd/yy/p删除/复制/粘贴、宏q+寄存器录制重复操作、set nu/相对行号、语法高亮syntax on、编译映射:map <F5> :!g++ % -O2 -o a && ./a<CR>。代码片段(Snippets)：VS Code可写json片段, Vim用abbreviation或UltiSnips；竞赛常用头模板+read模板。

### 历史 · History

编辑器配置随编辑器生态演进：VSCode因TypeScript/Electron与丰富扩展成为当代主流，Code Runner/C++ Compile Run专注单文件快速运行，clangd成为C++补全的事实标准之一；Vim以其全键盘效率在资深竞赛选手中长盛不衰。OI Wiki的editor/vscode与editor/vim页给出完整配置教程。

## How · 实现

### 伪代码

```python
# VS Code tasks.json (编译任务)
{
  "label": "build",
  "type": "shell",
  "command": "g++",
  "args": ["-std=c++17", "-g", "-Wall", "-Wextra", "${file}", "-o", "${fileDirname}/${fileBasenameNoExtension}"],
  "group": "build"
}
# 快捷键: Ctrl+Shift+B 编译; F5 调试; F6/F7/F8 (Compile Run扩展)

# Vim 映射
:map <F5> :!g++ % -std=c++17 -O2 -o a && ./a<CR>
:set number relativenumber
:syntax on
```

### Python 实现

```python
"""编辑器配置: 竞赛工作流辅助(模板生成/片段管理)参考实现.
自测: 验证模板代码生成与快捷键配置文件生成逻辑.
"""
import json
import os
import sys
from pathlib import Path

# ---------- 代码片段/模板管理 ----------
TEMPLATES = {
    "c++17_std": """#include <bits/stdc++.h>\nusing namespace std;\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    // TODO\n    return 0;\n}\n""",
    "py_fast": """import sys\ninput = sys.stdin.readline\n\ndef solve():\n    n = int(input())\n    # TODO\n\nif __name__ == '__main__':\n    solve()\n""",
}


def gen_template(lang):
    """按语言生成竞赛模板文件内容."""
    key = {"cpp": "c++17_std", "py": "py_fast"}.get(lang)
    return TEMPLATES.get(key)


# ---------- VSCode tasks.json 生成 ----------
def make_vscode_tasks():
    """生成VS Code编译任务配置(竞赛单文件)."""
    return {
        "version": "2.0.0",
        "tasks": [{
            "label": "build",
            "type": "shell",
            "command": "g++",
            "args": ["-std=c++17", "-g", "-Wall", "-Wextra",
                     "${file}", "-o",
                     "${fileDirname}/${fileBasenameNoExtension}"],
            "group": {"kind": "build", "isDefault": True},
        }]
    }


# ---------- Vim 配置片段 ----------
def make_vim_cfg():
    return (
        "set number relativenumber\n"
        "syntax on\n"
        "set tabstop=4 shiftwidth=4 expandtab\n"
        "map <F5> :!g++ % -std=c++17 -O2 -o a && ./a<CR>\n"
    )


if __name__ == "__main__":
    # 模板生成
    cpp = gen_template("cpp")
    py = gen_template("py")
    assert cpp and "#include <bits/stdc++.h>" in cpp
    assert py and "input = sys.stdin.readline" in py

    # VSCode tasks.json
    t = make_vscode_tasks()
    assert t["tasks"][0]["label"] == "build"
    assert "-std=c++17" in t["tasks"][0]["args"]

    # Vim配置
    v = make_vim_cfg()
    assert "set number" in v and "<F5>" in v

    print("editor-setup: ALL TESTS PASSED")

```

**PyPy 提示**: Python选手可直接用Code Runner一键运行; 注意VS Code集成终端默认使用CMD/PowerShell而非Git Bash(路径兼容性)。Vim的%代表当前文件名。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 配置一次性成本; 运行时代价=编译/调试时间 |
| 空间 | O(1) — 配置文件体积可忽略 |

### 局限

不同OS的g++/调试器路径不同(Windows需MinGW), 配置需按环境微调; Code Runner默认不启用'在终端运行', 需要输入时须勾选Run In Terminal; Vim学习曲线陡峭。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| OI Wiki | VS Code配置 | 0 | C/C++ Compile Run、Code Runner、C/C++扩展+launch.json调试配置 | [https://oi-wiki.org/tools/editor/vscode/](https://oi-wiki.org/tools/editor/vscode/) |
| OI Wiki | Vim配置 | 0 | Vim模式/键位/宏/normal命令的竞赛向用法 | [https://oi-wiki.org/tools/editor/vim/](https://oi-wiki.org/tools/editor/vim/) |
| VS Code | C++官方文档 | 0 | 微软官方C/C++与调试配置指南 | [https://code.visualstudio.com/docs/languages/cpp](https://code.visualstudio.com/docs/languages/cpp) |

## Pitfalls · 易错点

- VS Code集成终端用CMD/PowerShell而非Git Bash可能导致编译器找不到
- Code Runner需勾选Run In Terminal才能交互式输入
- tasks.json/launch.json的${file}等变量拼写错误会静默失效
- 开启-O2后gdb变量查看异常, 调试配置勿带-O2
- Vim的宏/寄存器操作易混淆, 建议单独练习

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/tools/editor/vscode/](https://oi-wiki.org/tools/editor/vscode/)
- OI Wiki ✓ [https://oi-wiki.org/tools/editor/vim/](https://oi-wiki.org/tools/editor/vim/)
