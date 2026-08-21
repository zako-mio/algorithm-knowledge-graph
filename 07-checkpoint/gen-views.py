#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 algorithm-dag.json 生成人类入口 HTML 视图 (05-views/)

产出（人类浏览入口，样式与 02-node-pages 一致，链接指向 ../02-node-pages/{id}.html）：
  05-views/index.html          视图总入口（优先级/学习路径/交互 DAG/分组目录 4 个人类入口）
  05-views/02-priority.html    优先级视图（P0 红 / P1 橙 / P2 蓝 / P3 灰，全 372 节点）
  05-views/03-learning-path.html 学习路径视图（4 层：basic/intermediate/advanced/frontier）

关键规则：
1. 幂等可重跑（已存在则覆盖）
2. 与 HTML 节点页完全同源（从 algorithm-dag.json 读取，不重写内容）
3. 覆盖校验：372 节点全入优先级视图，4 层全入学习路径
4. 所有链接指向 ../02-node-pages/{id}.html，必须存在
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DAG_PATH = os.path.join(ROOT, '01-dag-data', 'algorithm-dag.json')
OUT_DIR = os.path.join(ROOT, '05-views')
NODE_PAGES = os.path.join(ROOT, '02-node-pages')

STAGE_NAME = {'basic': '基础', 'intermediate': '中级', 'advanced': '高级', 'frontier': '前沿'}
STAGE_CLASS = {'basic': 'b-basic', 'intermediate': 'b-intermediate', 'advanced': 'b-advanced', 'frontier': 'b-frontier'}
PRIORITY_NAME = {'P0': 'P0 · 必会', 'P1': 'P1 · 高频', 'P2': 'P2 · 选学', 'P3': 'P3 · 冷门'}
PRIORITY_CLASS = {'P0': 'p-p0', 'P1': 'p-p1', 'P2': 'p-p2', 'P3': 'p-p3'}
PRIORITY_ORDER = ['P0', 'P1', 'P2', 'P3']

CSS = """\
:root{--bg:#0f1117;--panel:#161a22;--border:#2a2f3a;--text:#e6e8ee;--dim:#9aa3b2;--accent:#4f8cff;--ok:#2fb98a;}
*{box-sizing:border-box;margin:0;padding:0;}
body{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,'PingFang SC','Microsoft YaHei',sans-serif;line-height:1.7;}
header{background:var(--panel);border-bottom:1px solid var(--border);padding:24px 28px;}
header h1{font-size:23px;margin-bottom:6px;color:#f0f3f9;}
header p{color:var(--dim);font-size:14px;max-width:980px;}
main{padding:24px 28px;max-width:1200px;margin:0 auto;}
.back{margin-bottom:14px;}
.back a{color:var(--accent);text-decoration:none;font-size:14px;}
.back a:hover{text-decoration:underline;}
h2{font-size:19px;margin:30px 0 12px;color:#cfd6e4;border-bottom:1px solid var(--border);padding-bottom:8px;}
h3{font-size:15px;margin:16px 0 8px;color:#b8c2d4;}
a{color:var(--accent);text-decoration:none;}
a:hover{text-decoration:underline;}
.dim{color:var(--dim);}
.stat{display:inline-block;background:#1d2a3f;border:1px solid #2b3d5f;border-radius:8px;padding:10px 16px;margin:4px;text-align:center;}
.stat b{display:block;font-size:22px;color:#fff;}
.stat span{font-size:12px;color:var(--dim);}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px;margin:12px 0;}
.card{background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:18px;}
.card h3{font-size:16px;color:var(--accent);margin:0 0 8px;}
.card p{font-size:13px;color:var(--dim);margin-bottom:12px;}
.card .go{display:inline-block;background:#1d2a3f;border:1px solid #2b3d5f;border-radius:8px;padding:6px 14px;color:#fff;font-size:13px;}
.card .go:hover{border-color:var(--accent);}
.sec-head{display:flex;align-items:baseline;gap:10px;margin:34px 0 8px;border-bottom:1px solid var(--border);padding-bottom:8px;}
.sec-head h2{margin:0;border:none;padding:0;}
.sec-head span{color:var(--dim);font-size:13px;}
.sec-card{background:var(--panel);border:1px solid var(--border);border-left-width:4px;border-radius:10px;padding:16px 18px;margin:12px 0;}
.p-p0{border-left-color:#c0504d;border-top-color:#c0504d;border-right-color:#c0504d;border-bottom-color:#c0504d;}
.p-p1{border-left-color:#e8933b;border-top-color:#e8933b;border-right-color:#e8933b;border-bottom-color:#e8933b;}
.p-p2{border-left-color:#4f8cff;border-top-color:#4f8cff;border-right-color:#4f8cff;border-bottom-color:#4f8cff;}
.p-p3{border-left-color:#6b7280;border-top-color:#6b7280;border-right-color:#6b7280;border-bottom-color:#6b7280;}
.sec-card h3{margin:0 0 4px;font-size:16px;}
.sec-card h3 a{color:var(--accent);}
.sec-card .brief{font-size:13px;color:var(--dim);}
.sec-card .brief a{color:#7fb0ff;}
.badge{display:inline-block;padding:1px 9px;border-radius:20px;font-size:11.5px;font-weight:600;border:1px solid transparent;margin-right:6px;}
.b-p0{background:#4a1d1c;color:#ff9d97;border-color:#6a3229;}
.b-p1{background:#3d2a12;color:#ffc98a;border-color:#6a4a20;}
.b-p2{background:#16273f;color:#9cc2ff;border-color:#2b3d5f;}
.b-p3{background:#26262b;color:#b3b3ba;border-color:#3a3a40;}
.b-basic{background:#123528;color:#6fd3ae;border-color:#2f5a4a;}
.b-intermediate{background:#1d2a3f;color:#9cc2ff;border-color:#2b3d5f;}
.b-advanced{background:#3d2a12;color:#e8b06a;border-color:#6a4a20;}
.b-frontier{background:#3d1626;color:#e88ab0;border-color:#6a2a4a;}
.b-grp{background:#1d2a3f;color:#7fb0ff;border-color:#2b3d5f;}
.row{display:flex;align-items:baseline;gap:10px;padding:9px 6px;border-bottom:1px solid var(--border);flex-wrap:wrap;}
.row:hover{background:rgba(79,140,255,.06);}
.row .nm{min-width:220px;flex:0 0 auto;font-size:14px;font-weight:600;}
.row .nm a{color:#dbe4f2;}
.row .nm a:hover{color:var(--accent);}
.row .brief{flex:1 1 320px;font-size:12.5px;color:var(--dim);min-width:240px;}
.row .brief a{color:#7fb0ff;}
.legend{display:flex;gap:14px;flex-wrap:wrap;font-size:12px;color:var(--dim);margin:8px 0 4px;}
.lg{display:inline-flex;align-items:center;gap:5px;}
.lg i{width:12px;height:12px;border-radius:3px;display:inline-block;}
.lg .i-p0{background:#c0504d;}.lg .i-p1{background:#e8933b;}.lg .i-p2{background:#4f8cff;}.lg .i-p3{background:#6b7280;}
.lg .i-basic{background:#2fb98a;}.lg .i-intermediate{background:#4f8cff;}.lg .i-advanced{background:#b48a3c;}.lg .i-frontier{background:#b45a3c;}
.layer-nav{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0 4px;}
.layer-nav a{display:inline-block;background:var(--panel);border:1px solid var(--border);border-radius:8px;padding:4px 12px;font-size:13px;color:#b8c2d4;}
.layer-nav a:hover{border-color:var(--accent);color:#fff;}
footer{margin-top:48px;padding:16px 24px;border-top:1px solid var(--border);color:var(--dim);font-size:12px;text-align:center;}
@media (max-width:760px){main,header{padding:14px 16px;}.row .nm{min-width:160px;}}
"""


def esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def page(title, subtitle, body, gen_note=None):
    return ("""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%s — 算法知识图谱</title>
<style>
%s
</style>
</head>
<body>
<header>
  <h1>%s</h1>
  <p>%s</p>
</header>
<main>
  <div class="back"><a href="index.html">&larr; 返回视图入口</a></div>
%s
</main>
<footer>由 07-checkpoint/gen-views.py 生成 · 数据源 01-dag-data/algorithm-dag.json%s</footer>
</body>
</html>""" % (esc(title), CSS, esc(title), esc(subtitle), body, (' · ' + gen_note) if gen_note else ''))


def badge(text, cls):
    return '<span class="badge %s">%s</span>' % (cls, esc(text))


def row_html(n, node_pages_set):
    nid = n['id']
    name = n.get('name') or nid
    group = n.get('group', '')
    group_name = n.get('group_name', '')
    grp_txt = '%s %s' % (group, group_name) if group_name else group
    href = '../02-node-pages/%s.html' % nid if nid in node_pages_set else '#missing:%s' % nid
    brief = n.get('brief', '')
    return ('<div class="row">'
            '<span class="nm"><a href="%s">%s</a></span>'
            '%s%s%s'
            '<span class="brief">%s</span>'
            '</div>') % (
        href, esc(name),
        badge(n.get('priority', 'P3'), PRIORITY_CLASS.get(n.get('priority', 'P3'), 'p-p3')),
        badge(STAGE_NAME.get(n.get('stage', ''), n.get('stage', '')), STAGE_CLASS.get(n.get('stage', ''), '')),
        badge(grp_txt, 'b-grp'),
        esc(brief),
    )


def render_index():
    stats = ['<div class="stat"><b>372</b><span>知识点</span></div>',
             '<div class="stat"><b>60</b><span>知识组</span></div>',
             '<div class="stat"><b>318</b><span>关系边</span></div>',
             '<div class="stat"><b>4</b><span>学习阶段</span></div>',
             '<div class="stat"><b>1037</b><span>真实例题</span></div>']
    cards = [
        ('优先级视图（P0-P3）', '按 P0 必会 / P1 高频 / P2 选学 / P3 冷门四档浏览全部 372 个知识点，规划冲刺节奏。', '02-priority.html', '按优先级浏览'),
        ('学习路径', '按 basic → intermediate → advanced → frontier 四层推进，层内 P0 优先，系统学习路线。', '03-learning-path.html', '按学习阶段浏览'),
        ('交互 DAG 总览', '组级视图 + 点击下钻组内 DAG，理解拓扑推进方向。', '../04-interactive/index.html', '打开交互总览'),
        ('分组目录', '60 个知识组按领域与学习阶段组织，点击组卡片下钻。', '../03-groups/index.html', '打开分组目录'),
    ]
    body = ['<h2>核心统计</h2><div>%s</div>' % ''.join(stats),
            '<h2>视图入口</h2><div class="cards">']
    for name, desc, href, cta in cards:
        body.append('<div class="card"><h3>%s</h3><p>%s</p><a class="go" href="%s">%s</a></div>' % (esc(name), esc(desc), href, esc(cta)))
    body.append('</div>')
    body.append('<h2>快速开始</h2><ul style="padding-left:22px;font-size:14px;color:#cfd6e4;">'
                '<li style="margin:6px 0"><b>总览</b>：交互 DAG 总览看 60 组在四阶段分布。</li>'
                '<li style="margin:6px 0"><b>按优先级冲刺</b>：优先级视图按 P0→P3 集中补缺。</li>'
                '<li style="margin:6px 0"><b>系统学习</b>：学习路径按四层逐层推进，层内 P0 优先。</li>'
                '<li style="margin:6px 0"><b>下钻</b>：分组目录 / 节点页逐层深入，读 what / why / how / 例题 / 易错点。</li>'
                '</ul>')
    body.append('<h2>方法说明</h2><div class="cards">'
                '<div class="card"><h3>三级下钻</h3><p>根入口 → 组页（G-*.html）→ 知识点页（02-node-pages/*.html）。视图为快速检索入口，最终落到节点详情页。</p></div>'
                '<div class="card"><h3>双轨交付</h3><p>本目录（05-views/）与 03-groups/ 04-interactive/ 同为人类入口；06-md/ 为 AI 镜像（供检索与二次加工，非浏览入口）。</p></div>'
                '<div class="card"><h3>徽章语义</h3><p>优先级 P0 红 / P1 橙 / P2 蓝 / P3 灰；阶段 basic 绿 / intermediate 蓝 / advanced 橙 / frontier 玫红；组徽章灰蓝。</p></div>'
                '</div>')
    return page('视图入口', '优先级视图 · 学习路径 · 交互 DAG · 分组目录 4 个人类入口。', '\n'.join(body))


def render_priority(dag_nodes, node_pages_set):
    by_p = {}
    for n in dag_nodes:
        by_p.setdefault(n.get('priority', 'P3'), []).append(n)
    for p in PRIORITY_ORDER:
        nodes = by_p.get(p, [])
        nodes.sort(key=lambda n: (n.get('stage', ''), n.get('id', '')))
    legend = ('<div class="legend">'
              '<span class="lg"><i class="i-p0"></i>P0 必会</span>'
              '<span class="lg"><i class="i-p1"></i>P1 高频</span>'
              '<span class="lg"><i class="i-p2"></i>P2 选学</span>'
              '<span class="lg"><i class="i-p3"></i>P3 冷门</span>'
              '<span class="lg"><i class="i-basic"></i>基础</span>'
              '<span class="lg"><i class="i-intermediate"></i>中级</span>'
              '<span class="lg"><i class="i-advanced"></i>高级</span>'
              '<span class="lg"><i class="i-frontier"></i>前沿</span>'
              '</div>')
    total = len(dag_nodes)
    body = ['<p class="dim" style="margin:6px 0 10px">P0 = 必会 · P1 = 高频 · P2 = 选学 · P3 = 冷门。共 %d 个知识点，按优先级四档排列。</p>' % total]
    body.append(legend)
    for p in PRIORITY_ORDER:
        nodes = by_p.get(p, [])
        nodes.sort(key=lambda n: (n.get('stage', ''), n.get('id', '')))
        body.append('<div class="sec-head"><h2>%s</h2><span>%d 个知识点</span></div>' % (esc(PRIORITY_NAME[p]), len(nodes)))
        body.append('<div class="sec-card %s">' % PRIORITY_CLASS[p])
        rows = []
        for n in nodes:
            rows.append(row_html(n, node_pages_set))
        body.append('\n'.join(rows))
        body.append('</div>')
    return page('优先级视图 P0-P3', '按 P0 必会 / P1 高频 / P2 选学 / P3 冷门四档列出全部 %d 个知识点。' % total, '\n'.join(body))


def render_learning_path(dag, node_pages_set):
    layers = dag['layers']
    porder = {'P0': 0, 'P1': 1, 'P2': 2, 'P3': 3}
    nav = '<div class="layer-nav">' + ''.join(
        '<a href="#layer-%d">%s（%d）</a>' % (l['layer'], esc(STAGE_NAME.get(l['stage'], l['stage'])), len(l['node_ids']))
        for l in layers) + '</div>'
    body = ['<p class="dim" style="margin:6px 0 10px">分层: basic(基础) → intermediate(中级) → advanced(高级) → frontier(前沿)。层内按 P0/P1 优先，随后按组排列。</p>']
    body.append(nav)
    total = sum(len(l['node_ids']) for l in layers)
    for l in layers:
        lid = l['layer']
        stage = l['stage']
        nids = l['node_ids']
        by_id = {n['id']: n for n in dag['nodes']}
        nodes = [by_id[nid] for nid in nids if nid in by_id]
        nodes.sort(key=lambda nd: (porder.get(nd.get('priority', 'P3'), 9), nd.get('group', ''), nd.get('id', '')))
        body.append('<div class="sec-head" id="layer-%d"><h2>Layer %d · %s</h2><span>%d 个知识点</span></div>'
                    % (lid, lid, esc(STAGE_NAME.get(stage, stage)), len(nodes)))
        body.append('<div class="sec-card">')
        body.append('\n'.join(row_html(n, node_pages_set) for n in nodes))
        body.append('</div>')
    return page('学习路径', '按 basic → intermediate → advanced → frontier 四层列出全部 %d 个知识点，层内 P0 优先。' % total, '\n'.join(body))


def validate_html(path):
    with open(path, encoding='utf-8') as f:
        content = f.read()
    if len(content) < 500:
        return False, '文件过小'
    if '<html' not in content or '</html>' not in content:
        return False, 'html 标签未闭合'
    if content.count('<div') != content.count('</div>'):
        return False, 'div 开闭不平衡 (%d vs %d)' % (content.count('<div'), content.count('</div>'))
    if '\ufffd' in content:
        return False, '存在替换字符 U+FFFD'
    return True, 'OK'


def validate_links(path, root):
    with open(path, encoding='utf-8') as f:
        content = f.read()
    problems = []
    for href in re.findall(r'href="([^"]+)"', content):
        if href.startswith('#') or href.startswith('http'):
            continue
        target = os.path.normpath(os.path.join(root, href))
        if not os.path.exists(target):
            problems.append(href)
    return problems


def main():
    dag = json.load(open(DAG_PATH, encoding='utf-8'))
    os.makedirs(OUT_DIR, exist_ok=True)
    node_pages_set = set(f[:-5] for f in os.listdir(NODE_PAGES) if f.endswith('.html'))

    views = {
        'index.html': render_index(),
        '02-priority.html': render_priority(dag['nodes'], node_pages_set),
        '03-learning-path.html': render_learning_path(dag, node_pages_set),
    }
    for fname, content in views.items():
        with open(os.path.join(OUT_DIR, fname), 'w', encoding='utf-8') as f:
            f.write(content)
    print('[gen] 生成视图: %s' % ', '.join('05-views/%s' % f for f in views))

    fail = []
    for fname in views:
        path = os.path.join(OUT_DIR, fname)
        ok, msg = validate_html(path)
        if not ok:
            fail.append(('html:%s' % fname, msg))
        for bad in validate_links(path, os.path.dirname(path)):
            fail.append(('link:%s' % fname, '断链 %s' % bad))
    print('[validate] HTML 结构 + 链接检查: %s' % ('FAIL %r' % fail if fail else 'OK'))

    # 覆盖校验
    by_p = {}
    for n in dag['nodes']:
        by_p.setdefault(n.get('priority', 'P3'), []).append(n)
    coverage_ok = sum(len(by_p.get(p, [])) for p in PRIORITY_ORDER) == len(dag['nodes']) == 372
    layers_ok = sum(len(l['node_ids']) for l in dag['layers']) == len(dag['nodes']) == 372
    print('[coverage] 优先级视图 %d 节点 / 372%s；学习路径 %d 节点 / 372%s'
          % (sum(len(by_p.get(p, [])) for p in PRIORITY_ORDER), ' OK' if coverage_ok else ' FAIL',
             sum(len(l['node_ids']) for l in dag['layers']), ' OK' if layers_ok else ' FAIL'))
    missing = [n['id'] for n in dag['nodes'] if n['id'] not in node_pages_set]
    print('[coverage] 缺 HTML 节点页: %s' % (missing if missing else '无'))

    return 1 if (fail or not coverage_ok or not layers_ok or missing) else 0


if __name__ == '__main__':
    sys.exit(main())
