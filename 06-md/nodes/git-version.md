---
id: git-version
name: Git版本管理
group: G-E-9
stage: intermediate
priority: P2
depth_tier: standard
---

# Git版本管理

> 代码模板版本管理、提交回退、分支协作与代码回溯；竞赛模板库/团队协作的基础设施

<!-- 元信息: id=git-version · group=G-E-9 · stage=intermediate · priority=P2 · depth_tier=standard -->

## What · 是什么

Git是最广泛使用的分布式版本控制系统，OI Wiki本身就用Git管理。对竞赛选手，Git的价值有三：(1)模板库管理：把常用算法模板(读入优化、数据结构、图论模板)纳入版本控制，改坏可回退，跨机器同步；(2)代码回溯：每场比赛/练习提交留痕，赛后回看当时的AC/WA代码，复盘进步；(3)团队协作：多人出题/组队赛用分支与合并同步代码。核心命令：git init/clone初始化，git add暂存、git commit提交(SHA-1快照)、git status/log查看、git diff对比、git branch/checkout/merge分支、git reset/revert回退、git push/pull远程同步、.gitignore忽略文件(如*.exe)。

## Why · 为什么

### 直觉 · Intuition

Git像'存档点系统'：每次commit就是一个存档，改错了随时读档回退，历史全记录。对模板库而言，'我不记得哪版能过'的问题变成'git log找到那一次commit直接签出'。对协作而言，分支让多人并行改动不互相踩踏，merge合并后冲突可逐行解决。

### 原理 · Principle

核心模型：工作区(你改的文件)→暂存区(git add后的准备提交状态)→版本库(commit后的快照)。每次commit记录一个树快照+SHA-1+作者+信息，形成单向链表(commit历史)。git diff查看工作区与暂存区/HEAD差异; git log --oneline查看提交历史; git checkout -- <file>丢弃工作区改动; git reset --hard回退; 分支(branch)是指向commit的可移动指针，merge把另一分支的改动合并进来(冲突时手动解决); .gitignore里的模式(如*.exe, build/)不被跟踪。远程仓库用push/pull同步，本地每次pull自动merge。对模板库，把常用模板放一个repo按主题分目录，每模板独立commit便于回溯与检索。

### 历史 · History

Git由Linus Torvalds于2005年为Linux内核开发，以速度、分布式、内容寻址著称，目前是开源世界事实标准。GitHub/GitLab等托管平台进一步普及了协作工作流。OI Wiki的git页给出面向竞赛选手的完整入门。

## How · 实现

### 伪代码

```python
# 初始化与首次提交
cd templates
git init
git add -A
git commit -m "init: 常用算法模板"

# 日常
vim binary-search.cpp   # 修改
git diff                 # 看改动
git add binary-search.cpp
git commit -m "fix: 二分边界"

# 回溯
git log --oneline
git checkout <sha> -- binary-search.cpp   # 恢复某版文件

# 分支协作
git branch feature
git checkout feature
<改代码>
git checkout main && git merge feature
```

### Python 实现

```python
"""Git 版本管理: 核心命令的封装与自测(不依赖实际git仓库, 验证概念).
自测: 模拟commit历史、diff、checkout回退逻辑.
"""
import hashlib
import os
import subprocess
import sys
from pathlib import Path


# ---------- 简化模型: 内容寻址快照 ----------
def snapshot(files):
    """files: {path: content}, 返回树快照的哈希标识."""
    h = hashlib.sha256()
    for p in sorted(files):
        h.update(p.encode())
        h.update(b"\0")
        h.update(files[p].encode())
    return h.hexdigest()[:12]


class MiniRepo:
    """极简版本库: 提交历史+回退."""
    def __init__(self):
        self.commits = []   # [(sha, msg, files)]

    def commit(self, files, msg):
        sha = snapshot(files)
        self.commits.append((sha, msg, dict(files)))
        return sha

    def log(self):
        return [c[1] for c in self.commits]

    def checkout(self, idx):
        return self.commits[idx][2]

    def diff(self, a, b):
        """返回两个快照间内容变化的文件列表."""
        sa, sb = self.commits[a][2], self.commits[b][2]
        keys = set(sa) | set(sb)
        return [k for k in keys if sa.get(k) != sb.get(k)]


def run_git(cmd, cwd=None):
    """执行真实git命令并返回输出(用于演示/校验)."""
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


if __name__ == "__main__":
    # MiniRepo: 提交/回退/差异
    repo = MiniRepo()
    files = {"binary-search.cpp": "def bs(arr,t): ..."}
    repo.commit(files, "init")
    files["binary-search.cpp"] = "def bs(arr,t): ... # fixed"
    repo.commit(files, "fix boundary")
    files["dfs.cpp"] = "def dfs(u): ..."
    repo.commit(files, "add dfs")

    assert repo.log() == ["init", "fix boundary", "add dfs"]
    assert repo.diff(0, 1) == ["binary-search.cpp"]
    assert repo.diff(1, 2) == ["dfs.cpp"]  # 第2版仅新增dfs.cpp, bs不变
    # 回退到第2版
    old = repo.checkout(1)
    assert "fixed" in old["binary-search.cpp"] and "dfs" not in old

    # 真实git可用性
    code, _, err = run_git(["git", "--version"])
    assert code == 0, err

    print("git-version: ALL TESTS PASSED")

```

**PyPy 提示**: 对模板库建议: 一个仓库按主题分目录(基础/图论/DP/数据结构), 每个模板独立提交便于回溯; 大型编译产物用.gitignore排除。

### 复杂度

| 维度 | 值 |
| --- | --- |
| 时间 | 操作O(文件数量×内容); git diff/log高效 |
| 空间 | 每次commit存储增量(约等于改动量) |

### 局限

需正确配置user.name/email才能commit; 大二进制文件不适合Git; reset --hard会丢工作区改动; merge冲突需手动解决; 网络受限时远程同步不便。

## Examples · 例题

| OJ | 题号 | 难度 | 考点 | 链接 |
| --- | --- | --- | --- | --- |
| OI Wiki | Git教程 | 0 | 配置/仓库操作/提交/分支/远程同步的完整中文入门 | [https://oi-wiki.org/tools/git/](https://oi-wiki.org/tools/git/) |
| Git | 官方文档 | 0 | Pro Git在线书籍与命令参考 | [https://git-scm.com/doc](https://git-scm.com/doc) |
| GitHub | GitHub Help | 0 | 托管/PR/协作流程官方文档 | [https://docs.github.com](https://docs.github.com) |

## Pitfalls · 易错点

- 未配置user.name/email会commit失败(或提示无身份信息)
- git add -A与git add -u的区别: 前者含新文件, 后者仅已跟踪文件
- git reset --hard会丢弃工作区未提交改动, 谨慎使用
- .gitignore模式(如*.exe)必须在add之前生效, 已跟踪文件不受ignore控制
- 分支未合并前push可能被拒, 需先pull或rebase

## Sources · 信源

- OI Wiki ✓ [https://oi-wiki.org/tools/git/](https://oi-wiki.org/tools/git/)
- 官方文档 ✓ [https://git-scm.com/doc](https://git-scm.com/doc)
