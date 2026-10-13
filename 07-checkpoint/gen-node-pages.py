#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 stage2-nodes 内容库 + algorithm-dag.json + inventory.json 生成 372 个算法知识点 HTML 页 (02-node-pages/{node_id}.html)

幂等：已存在则覆盖，可重跑。
页面结构（高度人类可读）：
  头部(名称+stage/priority/depth/组徽章) -> what(brief+what) -> why(直觉/原理/历史 分节)
  -> how(伪代码 + Python高亮实现 + pypy提示条 + 复杂度表 + limitations警告条)
  -> 例题表 -> 易错点 -> 步骤迷你图(cytoscape) -> 信源 -> 组内prev/next + 组索引/总览 + 上下游边链式导航
"""
import html as html_mod
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NODES_DIR = os.path.join(ROOT, 'research', 'stage2-nodes')
DAG_PATH = os.path.join(ROOT, '01-dag-data', 'algorithm-dag.json')
INV_PATH = os.path.join(ROOT, 'research', 'stage1-inventory', 'inventory.json')
OUT_DIR = os.path.join(ROOT, '02-node-pages')

# ---------------------------------------------------------------- 令牌单源（值件展开）
# ★ 本文件内**不得**持有任何令牌字面值：令牌块在运行期由 `vendor/pipeline/` 的派生器
#   从值件展开（三级覆盖：族默认 → 站点覆盖 → 页面族覆盖）。判据见仓根 gate_tokens.py 的 T8。
sys.path.insert(0, os.path.join(ROOT, 'vendor', 'pipeline'))
import derive_site_tokens as _tokens_mod  # noqa: E402

VALUE_FILE = os.path.join(ROOT, 'vendor', 'pipeline', 'values', 'algorithm-knowledge-graph.json')
PROFILE_FILE = os.path.join(ROOT, 'build', 'profile.json')

# ---------------------------------------------------------------- 批 J · head 元数据共用件
# ★ 本件只写 `<head>` 元数据与站点级 SEO 资产，⛔ 不持有任何令牌字面值（T8 不受影响）。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import site_meta  # noqa: E402


def root_tokens(family='default'):
    """运行期从**值件**展开 `:root` 令牌块（确定性：同输入两次结果逐字节相同）。"""
    with open(VALUE_FILE, encoding='utf-8') as fh:
        contract = json.load(fh)
    with open(PROFILE_FILE, encoding='utf-8') as fh:
        profile = json.load(fh)
    _fid, toks = _tokens_mod.build_tokens(contract, profile, family)
    return _tokens_mod.render(toks)

# 已知目标（其他步骤生成的页面/资源，视为合法 href 目标）
KNOWN_EXTERNAL = {
    os.path.join(ROOT, '03-groups'),
    os.path.join(ROOT, '04-interactive'),
}

# ---------------------------------------------------------------- 颜色常量
PRIORITY_STYLE = {
    'P0': ('#c0504d', '#5a1f1f', '#e08a89'),
    'P1': ('#e8933b', '#3a2a12', '#e8b06a'),
    'P2': ('#4f8cff', '#16273f', '#8fb5ff'),
    'P3': ('#6a707c', '#23272f', '#9aa0ab'),
}
STAGE_STYLE = {
    'basic': ('#2fb98a', '#122b22', '#6fd3ae'),
    'intermediate': ('#e8933b', '#332412', '#e0a75e'),
    'advanced': ('#b48ae0', '#2b2040', '#c9a8ef'),
    'frontier': ('#c0504d', '#3a1717', '#dd8786'),
}
DEPTH_STYLE = {
    'deep': ('#7fb0ff', '#16273f', '#9cc2ff'),
    'standard': ('#9aa0ab', '#23272f', '#b6bcc6'),
    'brief': ('#6a707c', '#1c1f26', '#8d939e'),
}
EDGE_TYPE_STYLE = {
    'prerequisite': ('#e8933b', '前置依赖'),
    'variant': ('#2fb98a', '变体'),
    'combination': ('#b48ae0', '组合'),
    'cooccurrence': ('#7fb0ff', '共现'),
}
SRC_TYPE_NAME = {
    'oiwiki': 'OI Wiki',
    'cpalg': 'CP-Algorithms',
    'book': '书籍',
    'paper': '论文',
    'luogu': '洛谷',
    'codeforces': 'Codeforces',
    'atcoder': 'AtCoder',
    'blog': '博客',
    'wikipedia': 'Wikipedia',
    'official': '官方文档',
    'video': '视频',
    'other': '其他',
}

# ---------------------------------------------------------------- Python 语法高亮
KEYWORDS = {
    'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break',
    'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally',
    'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal',
    'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield',
    'match', 'case',
}
BUILTINS = {
    'abs', 'all', 'any', 'bool', 'bytes', 'bytearray', 'callable', 'chr',
    'classmethod', 'complex', 'delattr', 'dict', 'dir', 'divmod', 'enumerate',
    'eval', 'exec', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals',
    'hasattr', 'hash', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass',
    'iter', 'len', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next',
    'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'range', 'repr',
    'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod',
    'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip', 'ValueError',
    'TypeError', 'KeyError', 'IndexError', 'StopIteration', 'RuntimeError',
    'Exception', 'ImportError', 'ArithmeticError', 'ZeroDivisionError',
    'NotImplementedError', 'AttributeError', 'OverflowError', 'EOFError',
}

_STR_RE = re.compile(
    r'(?:[rRbBuUfF]{1,2}|br|rb|fr|rf|Br|Rb|Fr|Rf)?"""(?:\\.|[^"\\])*"""'
    r'|(?:[rRbBuUfF]{1,2}|br|rb|fr|rf|Br|Rb|Fr|Rf)?\'\'\'(?:\\.|[^\'\\])*\'\'\''
    r'|(?:[rRbBuUfF]{1,2}|br|rb|fr|rf|Br|Rb|Fr|Rf)?"(?:\\.|[^"\\\n])*"'
    r"|(?:[rRbBuUfF]{1,2}|br|rb|fr|rf|Br|Rb|Fr|Rf)?'(?:\\.|[^'\\\n])*'"
)
_IDENT_RE = re.compile(r'[A-Za-z_]\w*')
_NUM_RE = re.compile(r'(?:0[xX][0-9a-fA-F_]+|0[bB][01_]+|0[oO][0-7_]+|(?:\d[\d_]*\.?\d*|\.\d[\d_]*)(?:[eE][+-]?\d+)?[jJ]?)')


def py_highlight(code):
    """对 Python 代码做简单语法高亮（关键字/字符串/注释/数字/内建函数），返回 HTML（已转义 span 序列）。"""
    code = code.replace('\r\n', '\n').replace('\r', '\n')
    out = []
    i = 0
    n = len(code)
    while i < n:
        c = code[i]
        if c in ' \t\n':
            j = i
            while j < n and code[j] in ' \t\n':
                j += 1
            out.append(html_mod.escape(code[i:j]))
            i = j
            continue
        if c == '#':
            j = code.find('\n', i)
            if j == -1:
                j = n
            out.append('<span class="t-c">' + html_mod.escape(code[i:j]) + '</span>')
            i = j
            continue
        m = _STR_RE.match(code, i)
        if m:
            out.append('<span class="t-s">' + html_mod.escape(m.group(0)) + '</span>')
            i = m.end()
            continue
        if c.isdigit() or (c == '.' and i + 1 < n and code[i + 1].isdigit()):
            m = _NUM_RE.match(code, i)
            if m:
                out.append('<span class="t-n">' + html_mod.escape(m.group(0)) + '</span>')
                i = m.end()
                continue
        m = _IDENT_RE.match(code, i)
        if m:
            w = m.group(0)
            if w in KEYWORDS:
                out.append('<span class="t-k">' + html_mod.escape(w) + '</span>')
            elif w in BUILTINS:
                out.append('<span class="t-b">' + html_mod.escape(w) + '</span>')
            else:
                j = i + len(w)
                while j < n and code[j] in ' \t':
                    j += 1
                if j < n and code[j] == '(':
                    out.append('<span class="t-f">' + html_mod.escape(w) + '</span>')
                else:
                    out.append(html_mod.escape(w))
            i = m.end()
            continue
        out.append(html_mod.escape(c))
        i += 1
    return ''.join(out)


def esc(s):
    return html_mod.escape(str(s) if s is not None else '', quote=True)


def badge_span(text, fg, bg, cls):
    return ('<span class="badge %s" style="color:%s;background:%s;border-color:%s">%s</span>'
            % (cls, fg, bg, fg, esc(text)))


# ---------------------------------------------------------------- 数据加载
def load_data():
    dag = json.load(open(DAG_PATH, encoding='utf-8'))
    inv = json.load(open(INV_PATH, encoding='utf-8'))
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
    return dag, inv, nodes, dag_nodes, groups, node_by_id


def build_edge_index(dag):
    in_edges = {}
    out_edges = {}
    for e in dag['edges']:
        in_edges.setdefault(e['to'], []).append(e)
        out_edges.setdefault(e['from'], []).append(e)
    return in_edges, out_edges


# ---------------------------------------------------------------- 页面渲染
def render_prev_next(node_id, group, group_nodes):
    idx = group_nodes.index(node_id)
    total = len(group_nodes)
    gurl = '../03-groups/%s.html' % group['id']
    if idx == 0:
        prev_link, prev_label = gurl, '返回组索引'
        prev_class = 'nav-index'
    else:
        pid = group_nodes[idx - 1]
        prev_link, prev_label = '%s.html' % pid, pid
        prev_class = 'nav-node'
    if idx == total - 1:
        next_link, next_label = gurl, '返回组索引'
        next_class = 'nav-index'
    else:
        nid = group_nodes[idx + 1]
        next_link, next_label = '%s.html' % nid, nid
        next_class = 'nav-node'
    return prev_link, prev_label, prev_class, next_link, next_label, next_class


def render_edge_chips(node_id, edges, name_of, label):
    if not edges:
        return ''
    parts = ['<div class="edgegrp"><div class="edgegrp-label">%s</div><div class="chips">' % esc(label)]
    for e in edges:
        other = e['to'] if e['from'] == node_id else e['from']
        style = EDGE_TYPE_STYLE.get(e.get('type'), ('#8d939e', e.get('type', '未知')))
        fg, tname = style
        evi = esc(e.get('evidence', ''))
        parts.append('<a class="chip e-%s" href="%s.html" title="%s">%s<span class="etype">%s</span></a>'
                     % (esc(e.get('type', 'other')), esc(other), evi, esc(name_of.get(other, other)), esc(tname)))
    parts.append('</div></div>')
    return ''.join(parts)


def render_step_dag(node_id, step_dag):
    if not step_dag:
        return ''
    if isinstance(step_dag, dict) and 'nodes' in step_dag:
        dag_nodes = step_dag['nodes']
        dag_edges = step_dag.get('edges', [])
    else:
        # 字符串列表形式: ["a", "b", "c"] -> 链式步骤
        dag_nodes = [{'id': s, 'label': s} for s in step_dag if isinstance(s, str)]
        dag_edges = [{'from': dag_nodes[i]['id'], 'to': dag_nodes[i + 1]['id']}
                     for i in range(len(dag_nodes) - 1)]
    if not dag_nodes:
        return ''
    elements = []
    ids = set()
    for sd in dag_nodes:
        if isinstance(sd, str):
            sid = sd
            label = sd
        else:
            sid = str(sd['id'])
            label = str(sd.get('label', sid))
        ids.add(sid)
        elements.append({'data': {'id': sid, 'label': label}})
    for se in dag_edges:
        if not isinstance(se, dict):
            continue
        sf, st = str(se['from']), str(se['to'])
        if sf not in ids or st not in ids:
            continue
        elements.append({'data': {'id': 'e%s->%s' % (sf, st), 'source': sf, 'target': st}})
    raw_json = json.dumps(elements, ensure_ascii=False).replace('<', '\\u003c')
    return '''
<div class="dagbox">
  <div class="daglabel">步骤迷你图（节点 = 算法步骤 · 边 = 流程 · 绿色 = 起始步骤）</div>
  <div id="step-dag-%(uid)s" class="step-dag"></div>
</div>
<script src="../04-interactive/vendor/cytoscape.min.js"></script>
<script src="../04-interactive/vendor/cytoscape-dagre.min.js"></script>
<script>
(function(){
  var raw = %(raw)s;
  if (!raw.length) return;
  var cy = cytoscape({
    container: document.getElementById('step-dag-%(uid)s'),
    elements: raw,
    style: [
      {selector: 'node', style: {
        'label': 'data(label)', 'background-color': '#4f8cff', 'color': '#e6e8ee',
        'font-size': 11, 'text-valign': 'bottom', 'text-margin-y': 4,
        'width': 60, 'height': 40, 'shape': 'round-rectangle',
        'border-width': 1, 'border-color': '#2a2f3a', 'text-wrap': 'ellipsis',
        'text-max-width': 120
      }},
      {selector: 'edge', style: {
        'width': 1.5, 'line-color': '#4a5263', 'target-arrow-color': '#4a5263',
        'target-arrow-shape': 'triangle', 'curve-style': 'bezier'
      }}
    ],
    layout: {name: 'dagre', rankDir: 'LR', nodeSep: 24, rankSep: 60, padding: 16},
    wheelSensitivity: 0.2, minZoom: 0.2, maxZoom: 2.5
  });
  var hasIn = {};
  cy.edges().forEach(function(e){ hasIn[e.target().id()] = true; });
  cy.nodes().forEach(function(nd){ if (!hasIn[nd.id()]) nd.style('background-color', '#2fb98a'); });
  cy.fit(undefined, 28);
})();
</script>''' % {'raw': raw_json, 'uid': node_id}


def render_examples(examples):
    if not examples:
        return ''
    rows = []
    for ex in examples:
        oj = esc(ex.get('oj', ''))
        pid = esc(ex.get('pid', ''))
        diff = esc(ex.get('difficulty', ''))
        kp = esc(ex.get('key_point', ''))
        url = ex.get('url', '')
        link = ''
        if url:
            link = '<a href="%s" target="_blank" rel="noopener">%s</a>' % (esc(url), esc(url))
        rows.append('<tr><td>%s</td><td><strong>%s</strong></td><td>%s</td><td>%s</td><td class="u">%s</td></tr>'
                    % (oj, pid, diff, kp, link))
    return ('<div class="section"><h2>例题</h2><div class="tblwrap"><table>'
            '<thead><tr><th>OJ</th><th>题号</th><th>难度</th><th>考点</th><th>链接</th></tr></thead>'
            '<tbody>%s</tbody></table></div></div>') % ''.join(rows)


def render_sources(sources):
    if not sources:
        return ''
    items = []
    for s in sources:
        stype = str(s.get('type', 'other'))
        sname = SRC_TYPE_NAME.get(stype, stype)
        verified = bool(s.get('verified'))
        mark = '<span class="v-ok">&#10003;</span>' if verified else '<span class="v-warn">&#9651;</span>'
        url = s.get('url', '')
        ref = s.get('ref', '')
        if url:
            link = '<a href="%s" target="_blank" rel="noopener">%s</a>' % (esc(url), esc(url))
        elif ref:
            link = '<span class="ref">%s</span>' % esc(ref)
        else:
            link = '<span class="ref">—</span>'
        items.append('<li><span class="srctype">%s</span>%s %s</li>' % (esc(sname), mark, link))
    return ('<div class="section"><h2>信源</h2><ul class="srclist">%s</ul>'
            '<div class="legend">&#10003; = 已核验 · &#9651; = 未核验</div></div>') % ''.join(items)


def build_page(nd, dag_node, group, group_nodes, in_edges, out_edges, name_of):
    nid = nd['id']
    gid = group['id']
    gname = nd.get('group_name') or group['name']
    gurl = '../03-groups/%s.html' % gid
    idx = group_nodes.index(nid)
    total = len(group_nodes)

    # 徽章
    pr = nd.get('priority', 'P3')
    pstyle = PRIORITY_STYLE.get(pr, PRIORITY_STYLE['P3'])
    st = nd.get('stage', 'basic')
    sstyle = STAGE_STYLE.get(st, STAGE_STYLE['basic'])
    dt = nd.get('depth_tier', 'standard')
    dstyle = DEPTH_STYLE.get(dt, DEPTH_STYLE['standard'])
    badges = []
    badges.append(badge_span(esc(pr), pstyle[0], pstyle[1], 'p'))
    badges.append(badge_span(esc(st), sstyle[0], sstyle[1], 'st'))
    badges.append(badge_span(esc(dt), dstyle[0], dstyle[1], 'dp'))
    badges.append('<span class="badge grp">%s</span>' % esc(gid))

    # what
    brief = nd.get('brief', '')
    what = nd.get('what', '')
    what_html = ''
    if brief:
        what_html += '<div class="brieflead">%s</div>' % esc(brief)
    if what:
        what_html += '<p>%s</p>' % esc(what)

    # why
    why = nd.get('why') or {}
    why_html = []
    why_order = [('intuition', '直觉 · Intuition', '#2fb98a'), ('principle', '原理 · Principle', '#4f8cff'), ('history', '历史 · History', '#e8933b')]
    for key, title, color in why_order:
        txt = why.get(key)
        if not txt:
            continue
        why_html.append('<div class="whybox" style="border-color:%s"><div class="tag" style="color:%s">%s</div><p>%s</p></div>'
                        % (color, color, esc(title), esc(txt)))
    if not why_html:
        why_html = ['<p class="dim">该知识点未提供 why 详情。</p>']

    # how
    how = nd.get('how') or {}
    how_html = ['<div class="section"><h2>How · 实现</h2>']
    pc = how.get('pseudocode', '')
    if pc:
        how_html.append('<h3>伪代码</h3><pre><code class="python">%s</code></pre>' % py_highlight(pc))
    py = how.get('python', '')
    if py:
        how_html.append('<h3>Python 实现</h3><pre><code class="python">%s</code></pre>' % py_highlight(py))
    pyn = how.get('pypy_notes', '')
    if pyn:
        how_html.append('<div class="callout tip"><span class="ctag">PyPy 提示</span><span class="ctext">%s</span></div>' % esc(pyn))
    cx = how.get('complexity') or {}
    if cx:
        how_html.append('<div class="tblwrap"><table class="cmpl"><tr><th>时间复杂度</th><td>%s</td></tr>'
                        '<tr><th>空间复杂度</th><td>%s</td></tr></table></div>' % (esc(cx.get('time', '—')), esc(cx.get('space', '—'))))
    lim = how.get('limitations', '')
    if lim:
        how_html.append('<div class="callout warn"><span class="ctag">注意 · 局限</span><span class="ctext">%s</span></div>' % esc(lim))
    how_html.append('</div>')

    # 易错点
    pitfalls = nd.get('pitfalls') or []
    if pitfalls:
        how_html.append('<div class="section"><h2>易错点</h2><ul class="pit">%s</ul></div>'
                        % ''.join('<li>%s</li>' % esc(p) for p in pitfalls))

    # prev/next
    prev_link, prev_label, prev_class, next_link, next_label, next_class = render_prev_next(nid, group, group_nodes)

    # 上下游边导航
    edge_html = []
    in_chips = render_edge_chips(nid, in_edges, name_of, '上游 · 本知识点依赖（前置/变体/组合/共现）')
    out_chips = render_edge_chips(nid, out_edges, name_of, '下游 · 依赖本知识点')
    if in_chips or out_chips:
        edge_html.append('<div class="dagnav">%s%s</div>' % (in_chips, out_chips))

    dag_html = render_step_dag(nid, nd.get('step_dag'))

    name_title = esc(nd.get('name', nid))

    # ★ 批 J：逐页 description（取该页已有的 brief / what / 复杂度，截 160 字以内）
    desc = site_meta.make_description([
        brief,
        what,
        '%s · %s · %s' % (nd.get('name', nid), st, pr),
        (nd.get('how') or {}).get('complexity', {}).get('time') and
        '时间复杂度 %s' % (nd.get('how') or {}).get('complexity', {}).get('time'),
    ])

    page = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%(name)s · 算法知识图谱</title>
<style>
%(roottokens)s
*{box-sizing:border-box;margin:0;padding:0;}
.skip{position:absolute;left:-9999px;top:0;z-index:99;background:var(--panel);color:var(--accent);border:1px solid var(--border);border-radius:0 0 8px 0;padding:8px 14px;font-size:13px;text-decoration:none;}
.skip:focus{left:0;}
:focus-visible{outline:0.125rem solid var(--accent,#4f8cff);outline-offset:0.125rem}
.skip-link{position:absolute;left:-9999px;top:0;background:var(--accent,#4f8cff);color:#fff;padding:0.5rem 1rem;z-index:100}
.skip-link:focus{left:0}
body{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,'PingFang SC','Microsoft YaHei',sans-serif;line-height:1.7;}
header{background:var(--panel);border-bottom:1px solid var(--border-subtle);padding:14px 24px;}
header .crumb{color:var(--dim);font-size:13px;margin-bottom:6px;}
header .crumb a{color:var(--accent);text-decoration:none;}
header .crumb a:hover{text-decoration:underline;}
header h1{font-size:20px;font-weight:650;color:#f0f3f9;display:inline-block;margin-right:12px;}
.badges{display:inline-flex;gap:6px;flex-wrap:wrap;vertical-align:middle;}
.badge{display:inline-block;padding:2px 10px;border-radius:20px;font-size:12px;font-weight:600;border:1px solid transparent;letter-spacing:.3px;}
.badge.grp{background:#1d2a3f;color:#7fb0ff;border-color:#2b3d5f;}
main{padding:24px;max-width:1150px;margin:0 auto;}
h2{font-size:18px;margin:34px 0 12px;color:#cfd6e4;border-bottom:1px solid var(--border-subtle);padding-bottom:8px;}
h3{font-size:15px;margin:20px 0 8px;color:#b8c2d4;}
p,li{font-size:14px;}
ul{padding-left:22px;}
a{color:var(--accent);text-decoration:none;}
a:hover{text-decoration:underline;}
.dim{color:var(--dim);}
.section{scroll-margin-top:8px;}
.brieflead{background:#0d1a14;border:1px solid #2f5a4a;border-left:4px solid var(--ok);border-radius:8px;padding:12px 16px;font-size:15px;color:#cfe8dd;margin:12px 0;}
.whybox{background:var(--panel);border:1px solid var(--border);border-left-width:4px;border-radius:8px;padding:14px 18px;margin:10px 0;}
.whybox .tag{font-size:12px;font-weight:700;letter-spacing:1px;margin-bottom:6px;}
.whybox p{font-size:14px;color:#d3d9e4;}
pre{background:#0b0e14;border:1px solid var(--border);border-radius:8px;padding:14px 16px;overflow-x:auto;margin:8px 0;}
pre code{font-family:Consolas,'JetBrains Mono','Courier New',monospace;font-size:12.5px;line-height:1.6;color:#d4dbe6;display:block;}
.t-k{color:#c586c0;font-weight:600;}
.t-s{color:#ce9178;}
.t-c{color:#6a9955;font-style:italic;}
.t-n{color:#b5cea8;}
.t-b{color:#4fc1ff;}
.t-f{color:#dcdcaa;}
.callout{display:flex;gap:12px;align-items:flex-start;border-radius:8px;padding:12px 16px;margin:10px 0;font-size:14px;}
.callout .ctag{font-weight:700;flex-shrink:0;font-size:12px;letter-spacing:1px;padding-top:2px;}
.callout .ctext{color:#d3d9e4;}
.callout.tip{background:#0d1a14;border:1px solid #2f5a4a;}
.callout.tip .ctag{color:var(--ok);}
.callout.warn{background:#2a1713;border:1px solid #6a3229;}
.callout.warn .ctag{color:#e08a7c;}
.tblwrap{overflow-x:auto;margin:8px 0;}
table{border-collapse:collapse;width:100%%;}
th,td{border:1px solid var(--border);padding:7px 11px;font-size:13px;text-align:left;vertical-align:top;}
th{background:var(--panel);color:#b8c2d4;white-space:nowrap;}
td.u{word-break:break-all;font-size:12px;color:var(--dim);}
td.u a{color:#7fb0ff;}
table.cmpl{width:auto;min-width:60%%;}
table.cmpl th{width:110px;}
.pit li{margin:5px 0;font-size:14px;}
.pit li::marker{color:var(--warn);}
.srclist{list-style:none;padding-left:0;}
.srclist li{font-size:13px;margin:6px 0;color:var(--dim);}
.srclist .srctype{display:inline-block;min-width:110px;font-size:11px;background:#1d2a3f;color:#7fb0ff;border-radius:4px;padding:1px 8px;margin-right:8px;text-align:center;}
.srclist a{color:#7fb0ff;word-break:break-all;}
.srclist .ref{color:#9aa3b2;font-family:Consolas,monospace;}
.v-ok{color:var(--ok);font-weight:700;}
.v-warn{color:var(--warn);font-weight:700;}
.legend{font-size:11px;color:var(--dim);margin-top:6px;}
.navseq{display:flex;gap:10px;margin:16px 0;flex-wrap:wrap;}
.navseq a{display:inline-block;background:var(--panel);border:1px solid var(--border);border-radius:8px;padding:10px 18px;font-size:14px;color:#b8c2d4;text-align:center;min-width:150px;}
.navseq a .dir{display:block;font-size:11px;color:var(--dim);margin-bottom:2px;}
.navseq a .v{font-weight:600;color:var(--accent);}
.navseq a.nav-index .v{color:var(--ok);}
.navseq .spacer{flex:1;min-width:60px;}
.dagnav{background:var(--panel);border:1px solid var(--border);border-radius:8px;padding:12px 16px;margin:14px 0;}
.edgegrp{margin:6px 0;}
.edgegrp-label{font-size:12px;color:var(--dim);margin-bottom:6px;}
.chips{display:flex;flex-wrap:wrap;gap:6px;}
.chip{font-size:12px;background:#1d2a3f;border:1px solid #2b3d5f;border-radius:6px;padding:2px 8px;color:#7fb0ff;text-decoration:none;}
.chip:hover{background:#2b3d5f;}
.chip .etype{font-size:10px;opacity:.85;margin-left:4px;}
.chip.e-prerequisite{background:#2a1f10;border-color:#4a3a20;color:#e8b06a;}
.chip.e-variant{background:#0d1a14;border-color:#2f5a4a;color:#6fd3ae;}
.chip.e-combination{background:#2b2040;border-color:#4a3560;color:#c9a8ef;}
.chip.e-cooccurrence{background:#16273f;border-color:#2b3d5f;color:#9cc2ff;}
.dagbox{background:var(--panel);border:1px solid var(--border);border-radius:8px;padding:12px 16px;margin:14px 0;}
.daglabel{font-size:12px;color:var(--dim);margin-bottom:8px;}
.step-dag{width:100%%;height:420px;background:#0b0e14;border:1px solid var(--border);border-radius:8px;}
footer{margin-top:44px;padding:16px 24px;border-top:1px solid var(--border-subtle);color:var(--dim);font-size:12px;text-align:center;}
@media (prefers-reduced-motion:reduce){
  *{animation:none !important;transition:none !important;scroll-behavior:auto !important;}
}
@media (max-width:720px){
  main{padding:14px;}
  header{padding:12px 14px;}
  header h1{font-size:17px;}
  .navseq a{min-width:100%%;}
  .badges{display:flex;margin-top:6px;}
}
@media print{
  body{background:#fff;color:#000;}
  header,footer,.dagnav,.navseq,.dagbox{display:none;}
  pre{background:#f4f4f4;border-color:#ccc;color:#222;}
  pre code{color:#222;}
  th,td{border-color:#999;color:#000;}
  .whybox,.brieflead,.callout{background:#fff;border-color:#999;color:#000;}
  .whybox p,.callout .ctext{color:#000;}
}
</style>
</head>
<body>
<a class="skip" href="#main">跳到主要内容</a>
<header>
  <div class="crumb"><a href="../04-interactive/index.html">算法知识图谱总览</a> / <a href="%(gurl)s">%(gname)s</a> / <span>%(name)s</span></div>
  <h1>%(name)s</h1>
  <div class="badges">%(badges)s</div>
</header>
<main id="main">
  <div class="navseq">
    <a class="%(prev_class)s" href="%(prev_link)s"><span class="dir">&#8592; 上一个 / 组内</span><span class="v">%(prev_label)s</span></a>
    <a class="nav-index" href="%(gurl)s"><span class="dir">组内第 %(idx)d / %(total)d</span><span class="v">返回组索引</span></a>
    <a class="nav-index" href="../04-interactive/index.html"><span class="dir">全局</span><span class="v">返回总览</span></a>
    <a class="%(next_class)s" href="%(next_link)s"><span class="dir">下一个 / 组内</span><span class="v">%(next_label)s</span></a>
  </div>

  <div class="section"><h2>What · 是什么</h2>%(what)s</div>

  <div class="section"><h2>Why · 为什么</h2>%(why)s</div>

  %(how)s

  %(examples)s

  %(dag)s

  %(edges)s

  %(sources)s
</main>
<footer>算法知识图谱 · 372 个知识点 · 60 组 · 4 层 · 由 stage2-nodes 内容库生成（what / why / how / 例题 / 易错点 / 步骤图 / 信源）</footer>
</body>
</html>''' % {
        'roottokens': root_tokens('default'),
        'name': name_title,
        'gurl': gurl,
        'gname': esc(gname),
        'badges': ''.join(badges),
        'what': what_html,
        'why': ''.join(why_html),
        'how': ''.join(how_html),
        'examples': render_examples(nd.get('examples')),
        'dag': dag_html,
        'edges': ''.join(edge_html),
        'sources': render_sources(nd.get('sources')),
        'prev_link': esc(prev_link),
        'prev_label': esc(prev_label),
        'prev_class': prev_class,
        'next_link': esc(next_link),
        'next_label': esc(next_label),
        'next_class': next_class,
        'idx': idx + 1,
        'total': total,
    }
    # ★ 批 J：把 COMMON.md §2.1 的 8 行元数据注入 <head>（幂等）
    return site_meta.inject_head_meta(page, '02-node-pages/%s.html' % nid,
                                      desc, '%s · 算法知识图谱' % nd.get('name', nid))


# ---------------------------------------------------------------- 校验
VALIDATE_TAGS = ['div', 'pre', 'code', 'table', 'thead', 'tbody', 'tr', 'th', 'td',
                 'script', 'ul', 'ol', 'li', 'span', 'a', 'h1', 'h2', 'h3', 'header',
                 'main', 'footer', 'strong', 'em', 'p', 'br']
TAG_RE = re.compile(r'<(/?)([a-zA-Z][a-zA-Z0-9]*)(?:\s[^<>]*?)?>')


def validate_page(path):
    """校验单页：存在、非空、闭合、标签平衡、无未转义 < 破坏结构。"""
    with open(path, encoding='utf-8') as f:
        content = f.read()
    if len(content) < 100:
        return False, '文件过小'
    if '<!DOCTYPE html>' not in content:
        return False, '缺少 DOCTYPE'
    if '<meta charset="UTF-8">' not in content:
        return False, '缺少 UTF-8 声明'
    if '</html>' not in content:
        return False, '缺少 </html> 闭合'
    if content.count('<html') != content.count('</html>'):
        return False, '<html> 数量不匹配'
    # 标签平衡
    for tag in VALIDATE_TAGS:
        if tag == 'br':
            continue
        o = len(re.findall(r'<%s(?:\s[^<>]*?)?/?>' % tag, content))
        c = len(re.findall(r'</%s>' % tag, content))
        if o != c:
            if tag in ('meta', 'link', 'input', 'img'):
                continue
            return False, '<%s> 开 %d 闭 %d 不平衡' % (tag, o, c)
    # 无未转义 <：去掉合法标签后不应残留 '<'（允许 doctype 声明）
    cleaned = TAG_RE.sub('', content)
    cleaned = cleaned.replace('<!DOCTYPE html>', '')
    if '<' in cleaned:
        pos = cleaned.find('<')
        return False, '存在未转义 < (位置约 %d)' % pos
    return True, 'OK'


def run_site_gates():
    """★ Q5-B ＋ 批 J：门控**随生成器收尾内联调用**（留痕 gate-report.json）。

    实现统一在共用件 `site_meta.run_site_gates()`（⛔ 不在三个生成器里各写一份）：
      · `gate_tokens.py` / `gate_design.py` —— report 档留痕（批 H 口径，判据与阈值未改）；
      · `gate_a11y.py` / `gate_seo_meta.py` —— **hard 档实跑**（批 J：a11y / metadata 转硬）。
    ★ **fail-closed**：任一门控 exit 非 0 ⇒ 本函数非 0 ⇒ 生成器非 0 退出（⛔ 不静默跳过）。
    """
    return site_meta.run_site_gates(ROOT)


def main():
    dag, inv, nodes, dag_nodes, groups, node_by_id = load_data()
    in_edges, out_edges = build_edge_index(dag)
    name_of = {nid: (nd.get('name') or nid) for nid, nd in dag_nodes.items()}

    os.makedirs(OUT_DIR, exist_ok=True)

    target_ids = [n['id'] for n in dag['nodes']]
    generated = []
    missing_nodes = []
    for nid in target_ids:
        nd = node_by_id.get(nid)
        if nd is None:
            missing_nodes.append(nid)
            continue
        dag_node = dag_nodes.get(nid)
        group = groups.get(nd.get('group') or dag_node.get('group'))
        if group is None:
            missing_nodes.append(nid)
            continue
        group_nodes = group['node_ids']
        page = build_page(nd, dag_node, group, group_nodes,
                          in_edges.get(nid, []), out_edges.get(nid, []), name_of)
        out_path = os.path.join(OUT_DIR, '%s.html' % nid)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(page)
        generated.append(nid)

    print('[gen] 生成 %d 页 -> %s' % (len(generated), OUT_DIR))
    if missing_nodes:
        print('[gen] 缺失节点(无内容或组): %s' % missing_nodes, file=sys.stderr)

    # 全量校验
    fail = []
    for nid in generated:
        path = os.path.join(OUT_DIR, '%s.html' % nid)
        ok, msg = validate_page(path)
        if not ok:
            fail.append((nid, msg))
    print('[validate] 通过 %d / %d' % (len(generated) - len(fail), len(generated)))
    for nid, msg in fail[:50]:
        print('[validate] FAIL %s: %s' % (nid, msg), file=sys.stderr)

    # 断链检查（组/总览/资源视为已知目标）
    broken = []
    for nid in generated:
        path = os.path.join(OUT_DIR, '%s.html' % nid)
        with open(path, encoding='utf-8') as f:
            content = f.read()
        for href in re.findall(r'href="([^"]+\.html)"', content):
            if href.startswith('http'):
                continue
            resolved = os.path.normpath(os.path.join(OUT_DIR, href))
            if os.path.exists(resolved):
                continue
            if any(resolved.startswith(os.path.normpath(known)) for known in KNOWN_EXTERNAL):
                continue
            broken.append((nid, href))
    print('[links] 内部断链 %d' % len(broken))
    for nid, href in broken[:30]:
        print('[links] BROKEN %s -> %s' % (nid, href), file=sys.stderr)

    # ★ 批 J：站点级 SEO 资产（sitemap.xml 覆盖发布根下**全部** .html ＋ robots.txt）
    site_meta.write_site_files(ROOT)

    return 1 if (fail or broken or missing_nodes or run_site_gates()) else 0


if __name__ == '__main__':
    sys.exit(main())
