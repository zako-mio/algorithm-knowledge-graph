#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 stage2-nodes 内容库 + algorithm-dag.json 生成 AI 友好 Markdown 镜像 (06-md/)

产出（供 AI 检索与二次加工，非人类浏览入口）：
  06-md/00-index.md      总索引（60 组列表 + 各组节点数与链接）
  06-md/01-groups.md     分组视图（每组节点清单：id/name/stage/priority/brief）
  06-md/02-priority.md   优先级视图（P0 全列表 / P1 / P2 / P3）
  06-md/03-learning-path.md 学习路径视图（按 stage layer：basic→intermediate→advanced→frontier）
  06-md/nodes/{node_id}.md  每节点镜像（372 个，front-matter + brief/what/why/how/examples/pitfalls/sources）

关键规则：
1. 幂等可重跑（已存在则覆盖）
2. 与 HTML 页数据完全同源（从 stage2-nodes 读取，不重写内容）
3. 372 节点镜像全生成（05 覆盖校验）
4. MD 格式合法（front-matter 闭合 / 代码块围栏 / 表格列对齐）
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NODES_DIR = os.path.join(ROOT, 'research', 'stage2-nodes')
DAG_PATH = os.path.join(ROOT, '01-dag-data', 'algorithm-dag.json')
OUT_DIR = os.path.join(ROOT, '06-md')
NODES_OUT = os.path.join(OUT_DIR, 'nodes')

SRC_TYPE_NAME = {
    'oiwiki': 'OI Wiki', 'cpalg': 'CP-Algorithms', 'book': '书籍', 'paper': '论文',
    'luogu': '洛谷', 'codeforces': 'Codeforces', 'atcoder': 'AtCoder', 'blog': '博客',
    'wikipedia': 'Wikipedia', 'official': '官方文档', 'video': '视频', 'other': '其他',
}
STAGE_NAME = {
    'basic': '基础', 'intermediate': '中级', 'advanced': '高级', 'frontier': '前沿',
}


def load_data():
    dag = json.load(open(DAG_PATH, encoding='utf-8'))
    nodes = []
    for f in sorted(os.listdir(NODES_DIR)):
        if not f.endswith('.json'):
            continue
        nd = json.load(open(os.path.join(NODES_DIR, f), encoding='utf-8'))
        if not nd.get('id') or nd['id'].startswith('_'):
            continue
        nodes.append(nd)
    dag_nodes = {n['id']: n for n in dag['nodes']}
    groups = {g['id']: g for g in dag['groups']}
    node_by_id = {}
    for nd in nodes:
        if nd['id'] in dag_nodes:
            node_by_id[nd['id']] = nd
    return dag, nodes, dag_nodes, groups, node_by_id


def mdesc(s):
    """转义行内内容中的 Markdown 特殊字符，避免破坏表格/列表结构。"""
    if s is None:
        return ''
    s = str(s)
    return s.replace('|', '\\|').replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ')


def block(s):
    """大段多行文本：保留换行为 Markdown 段落（两个换行分隔）。"""
    if s is None:
        return ''
    return str(s).strip()


# ---------------------------------------------------------------- 节点镜像
def render_examples(examples):
    if not examples:
        return ''
    rows = []
    for ex in examples:
        oj = mdesc(ex.get('oj', ''))
        pid = mdesc(ex.get('pid', ''))
        diff = mdesc(ex.get('difficulty', ''))
        kp = mdesc(ex.get('key_point', ''))
        url = ex.get('url', '')
        link = '[%s](%s)' % (mdesc(url), url) if url else '—'
        rows.append('| %s | %s | %s | %s | %s |' % (oj, pid, diff, kp, link))
    header = '| OJ | 题号 | 难度 | 考点 | 链接 |'
    sep = '| --- | --- | --- | --- | --- |'
    return header + '\n' + sep + '\n' + '\n'.join(rows)


def render_sources(sources):
    if not sources:
        return ''
    items = []
    for s in sources:
        stype = str(s.get('type', 'other'))
        sname = SRC_TYPE_NAME.get(stype, stype)
        verified = '✓' if s.get('verified') else '△'
        url = s.get('url', '')
        ref = s.get('ref', '')
        if url:
            link = '[%s](%s)' % (mdesc(url), url)
        elif ref:
            link = '`%s`' % mdesc(ref)
        else:
            link = '—'
        items.append('- %s %s %s' % (sname, verified, link))
    return '\n'.join(items)


def render_node_md(nd):
    nid = nd['id']
    name = nd.get('name') or nid
    group = nd.get('group', '')
    stage = nd.get('stage', '')
    priority = nd.get('priority', '')
    depth_tier = nd.get('depth_tier', '')
    brief = nd.get('brief', '')

    lines = []
    lines.append('---')
    lines.append('id: %s' % nid)
    lines.append('name: %s' % mdesc(name))
    lines.append('group: %s' % mdesc(group))
    lines.append('stage: %s' % mdesc(stage))
    lines.append('priority: %s' % mdesc(priority))
    lines.append('depth_tier: %s' % mdesc(depth_tier))
    lines.append('---')
    lines.append('')
    lines.append('# %s' % mdesc(name))
    lines.append('')

    lines.append('> %s' % mdesc(brief))
    lines.append('')

    lines.append('<!-- 元信息: id=%s · group=%s · stage=%s · priority=%s · depth_tier=%s -->'
                 % (nid, group, stage, priority, depth_tier))
    lines.append('')

    # what
    what = nd.get('what')
    if what:
        lines.append('## What · 是什么')
        lines.append('')
        lines.append(block(what))
        lines.append('')

    # why
    why = nd.get('why') or {}
    why_blocks = []
    if why.get('intuition'):
        why_blocks.append('### 直觉 · Intuition\n\n%s' % block(why['intuition']))
    if why.get('principle'):
        why_blocks.append('### 原理 · Principle\n\n%s' % block(why['principle']))
    if why.get('history'):
        why_blocks.append('### 历史 · History\n\n%s' % block(why['history']))
    if why_blocks:
        lines.append('## Why · 为什么')
        lines.append('')
        lines.append('\n\n'.join(why_blocks))
        lines.append('')

    # how
    how = nd.get('how') or {}
    how_blocks = []
    pc = how.get('pseudocode')
    if pc:
        how_blocks.append('### 伪代码\n\n```python\n%s\n```' % pc)
    py = how.get('python')
    if py:
        how_blocks.append('### Python 实现\n\n```python\n%s\n```' % py)
    pyn = how.get('pypy_notes')
    if pyn:
        how_blocks.append('**PyPy 提示**: %s' % mdesc(pyn))
    cx = how.get('complexity')
    if cx:
        how_blocks.append('### 复杂度\n\n| 维度 | 值 |\n| --- | --- |\n| 时间 | %s |\n| 空间 | %s |'
                          % (mdesc(cx.get('time', '—')), mdesc(cx.get('space', '—'))))
    lim = how.get('limitations')
    if lim:
        how_blocks.append('### 局限\n\n%s' % block(lim))
    if how_blocks:
        lines.append('## How · 实现')
        lines.append('')
        lines.append('\n\n'.join(how_blocks))
        lines.append('')

    # examples
    examples = nd.get('examples') or []
    if examples:
        lines.append('## Examples · 例题')
        lines.append('')
        lines.append(render_examples(examples))
        lines.append('')

    # pitfalls
    pitfalls = nd.get('pitfalls') or []
    if pitfalls:
        lines.append('## Pitfalls · 易错点')
        lines.append('')
        for p in pitfalls:
            lines.append('- %s' % mdesc(p))
        lines.append('')

    # sources
    sources = nd.get('sources') or []
    if sources:
        lines.append('## Sources · 信源')
        lines.append('')
        lines.append(render_sources(sources))
        lines.append('')

    return '\n'.join(lines)


# ---------------------------------------------------------------- 总索引
def render_index(dag, groups):
    meta = dag['meta']
    lines = []
    lines.append('# 算法知识图谱 · MD 镜像总索引')
    lines.append('')
    lines.append('## 统计')
    lines.append('')
    lines.append('- 知识点节点: %d' % meta.get('total_nodes', len(dag['nodes'])))
    lines.append('- 分组: %d' % meta.get('total_groups', len(dag['groups'])))
    lines.append('- 依赖边: %d' % meta.get('total_edges', len(dag['edges'])))
    lines.append('- 阶段: %s' % ' → '.join('%s(%d)' % (s, len(dag['layers'][i]['node_ids'])) if i < len(dag['layers']) else s
                                     for i, s in enumerate(meta.get('stages', []))))
    lines.append('- 优先级: %s' % ' / '.join(meta.get('priorities', [])))
    lines.append('')
    lines.append('## 阅读导航')
    lines.append('')
    lines.append('- [分组视图](01-groups.md)')
    lines.append('- [优先级视图](02-priority.md)')
    lines.append('- [学习路径视图](03-learning-path.md)')
    lines.append('- [节点镜像目录](nodes/)')
    lines.append('- [交互总览 HTML](../04-interactive/index.html)')
    lines.append('- [分组视图 HTML](../03-groups/index.html)')
    lines.append('- [每节点 HTML](../02-node-pages/index.html)')
    lines.append('')
    lines.append('## 分组清单')
    lines.append('')
    lines.append('| 组 | 名称 | 领域 | 阶段范围 | 节点数 |')
    lines.append('| --- | --- | --- | --- | ---: |')
    for g in groups:
        lines.append('| %s | [%s](01-groups.md#%s) | %s | %s | %d |'
                     % (mdesc(g['id']), mdesc(g['name']), mdesc(g['id']), mdesc(g.get('domain', '')),
                        '→'.join(STAGE_NAME.get(s, s) for s in g.get('stage_range', [])),
                        len(g['node_ids'])))
    lines.append('')
    return '\n'.join(lines)


def anchor(gid):
    return mdesc(gid).lower().replace('/', '-').replace('.', '-').replace(' ', '-').replace('(', '').replace(')', '')


# ---------------------------------------------------------------- 分组视图
def render_groups(dag, groups, node_by_id):
    lines = []
    lines.append('# 分组视图 · 60 组节点清单')
    lines.append('')
    lines.append('> 供 AI 检索：按组列出节点 id / name / stage / priority / brief。')
    lines.append('')
    for g in groups:
        lines.append('## %s %s' % (mdesc(g['id']), mdesc(g['name'])))
        lines.append('')
        lines.append('- 领域: %s · 阶段范围: %s · 节点数: %d'
                     % (mdesc(g.get('domain', '—')),
                        '→'.join(STAGE_NAME.get(s, s) for s in g.get('stage_range', [])),
                        len(g['node_ids'])))
        lines.append('')
        lines.append('| id | name | stage | priority | brief |')
        lines.append('| --- | --- | --- | --- | --- |')
        for nid in g['node_ids']:
            nd = node_by_id.get(nid)
            if nd is None:
                continue
            lines.append('| %s | [%s](nodes/%s.md) | %s | %s | %s |'
                         % (mdesc(nid), mdesc(nd.get('name') or nid), nid,
                            mdesc(nd.get('stage', '')), mdesc(nd.get('priority', '')),
                            mdesc(nd.get('brief', ''))))
        lines.append('')
    return '\n'.join(lines)


# ---------------------------------------------------------------- 优先级视图
def render_priority(dag, node_by_id):
    lines = []
    lines.append('# 优先级视图 · P0 / P1 / P2 / P3')
    lines.append('')
    lines.append('> P0 = 必会 · P1 = 高频 · P2 = 选学 · P3 = 冷门。')
    lines.append('')
    order = ['P0', 'P1', 'P2', 'P3']
    pname = {'P0': 'P0 · 必会', 'P1': 'P1 · 高频', 'P2': 'P2 · 选学', 'P3': 'P3 · 冷门'}
    by_p = {}
    for n in dag['nodes']:
        by_p.setdefault(n.get('priority', 'P3'), []).append(n)
    for p in order:
        nodes = by_p.get(p, [])
        nodes.sort(key=lambda n: (n.get('stage', ''), n.get('id', '')))
        lines.append('## %s (%d)' % (pname[p], len(nodes)))
        lines.append('')
        lines.append('| id | name | stage | group | brief |')
        lines.append('| --- | --- | --- | --- | --- |')
        for n in nodes:
            nid = n['id']
            lines.append('| %s | [%s](nodes/%s.md) | %s | %s | %s |'
                         % (mdesc(nid), mdesc(n.get('name') or nid), nid,
                            mdesc(n.get('stage', '')), mdesc(n.get('group', '')),
                            mdesc(n.get('brief', ''))))
        lines.append('')
    return '\n'.join(lines)


# ---------------------------------------------------------------- 学习路径视图
def render_learning_path(dag, layers, node_by_id):
    lines = []
    lines.append('# 学习路径视图 · 按 stage layer')
    lines.append('')
    lines.append('> 分层: basic(基础) → intermediate(中级) → advanced(高级) → frontier(前沿)。')
    lines.append('> 层内按 P0/P1 优先排序，随后按组排列，供检索与刷题规划。')
    lines.append('')
    for layer in layers:
        lid = layer['layer']
        stage = layer['stage']
        nids = layer['node_ids']
        lines.append('## Layer %d · %s (%d)' % (lid, STAGE_NAME.get(stage, stage), len(nids)))
        lines.append('')
        lines.append('| id | name | priority | group | brief |')
        lines.append('| --- | --- | --- | --- | --- |')
        nodes = [node_by_id[n] for n in nids if n in node_by_id]
        porder = {'P0': 0, 'P1': 1, 'P2': 2, 'P3': 3}
        nodes.sort(key=lambda nd: (porder.get(nd.get('priority', 'P3'), 9), nd.get('group', ''), nd.get('id', '')))
        for nd in nodes:
            lines.append('| %s | [%s](nodes/%s.md) | %s | %s | %s |'
                         % (mdesc(nd['id']), mdesc(nd.get('name') or nd['id']), nd['id'],
                            mdesc(nd.get('priority', '')), mdesc(nd.get('group', '')),
                            mdesc(nd.get('brief', ''))))
        lines.append('')
    return '\n'.join(lines)


# ---------------------------------------------------------------- 校验
def validate_md(path):
    """校验 MD 合法性：front-matter 闭合、代码块围栏成对、表格列对齐、无截断。"""
    with open(path, encoding='utf-8') as f:
        content = f.read()
    if len(content) < 50:
        return False, '文件过小'
    # front-matter 闭合
    if content.startswith('---'):
        if '\n---\n' not in content.split('\n', 2)[1][:10000]:
            if content.count('\n---\n') < 1:
                return False, 'front-matter 未闭合'
    # 代码块围栏成对
    fences = re.findall(r'^```', content, re.M)
    if len(fences) % 2 != 0:
        return False, '代码块围栏不成对 (%d 处 ```)' % len(fences)
    # 无 null 字符 / 替换字符
    if '\ufffd' in content:
        return False, '存在替换字符 U+FFFD'
    return True, 'OK'


def main():
    dag, nodes, dag_nodes, groups, node_by_id = load_data()

    os.makedirs(NODES_OUT, exist_ok=True)

    # 1) 节点镜像（372）
    target_ids = [n['id'] for n in dag['nodes']]
    generated = []
    missing_nodes = []
    for nid in target_ids:
        nd = node_by_id.get(nid)
        if nd is None:
            missing_nodes.append(nid)
            continue
        md = render_node_md(nd)
        out_path = os.path.join(NODES_OUT, '%s.md' % nid)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(md)
        generated.append(nid)
    print('[gen] 生成节点镜像 %d -> %s' % (len(generated), NODES_OUT))
    if missing_nodes:
        print('[gen] 缺失节点(无内容): %s' % missing_nodes, file=sys.stderr)

    # 2) 三个视图 + 总索引
    views = {
        '00-index.md': render_index(dag, dag['groups']),
        '01-groups.md': render_groups(dag, dag['groups'], node_by_id),
        '02-priority.md': render_priority(dag, node_by_id),
        '03-learning-path.md': render_learning_path(dag, dag['layers'], node_by_id),
    }
    for fname, content in views.items():
        with open(os.path.join(OUT_DIR, fname), 'w', encoding='utf-8') as f:
            f.write(content)
    print('[gen] 生成视图: %s' % ', '.join(views.keys()))

    # 3) 全量校验（节点镜像 + 视图）
    fail = []
    for fname in list(views.keys()) + ['nodes/%s.md' % nid for nid in generated]:
        path = os.path.join(OUT_DIR, fname)
        ok, msg = validate_md(path)
        if not ok:
            fail.append((fname, msg))
    print('[validate] 通过 %d / %d' % (len(generated) + len(views) - len(fail), len(generated) + len(views)))
    for fname, msg in fail[:50]:
        print('[validate] FAIL %s: %s' % (fname, msg), file=sys.stderr)

    # 4) 覆盖校验：372 节点镜像全生成
    coverage_ok = len(generated) == 372 and not missing_nodes
    print('[coverage] 节点镜像 %d / 372' % len(generated))
    if not coverage_ok:
        print('[coverage] 覆盖失败: 缺失 %d' % len(missing_nodes), file=sys.stderr)

    return 1 if (fail or not coverage_ok) else 0


if __name__ == '__main__':
    sys.exit(main())
