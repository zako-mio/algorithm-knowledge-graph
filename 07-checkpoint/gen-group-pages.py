#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 algorithm-dag.json + stage2-nodes 内容库 + inventory.json 生成 60 个组索引页 (03-groups/G-{id}.html)

幂等：已存在则覆盖，可重跑。
页面结构（暗色 rc8 主题，CSS 变量与 02-node-pages 一致）：
  头部(组名 + domain/stage_range/节点数徽章 + 面包屑)
  -> 组简介(节点数 + 优先级分布 P0/P1/P2/P3 + 阶段分布)
  -> 节点目录表(按 inventory 顺序, 每行 id/name/stage/priority 徽章/brief/例题数, 链接到 ../02-node-pages/{id}.html)
  -> 学习路径提示(组内 prerequisite 依赖, 拓扑序推荐阅读顺序)
  -> 组间导航(总览入口 + 相邻组 prev/next + 同 domain 上下组)
"""
import heapq
import html as html_mod
import json
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DAG_PATH = os.path.join(ROOT, '01-dag-data', 'algorithm-dag.json')
NODES_DIR = os.path.join(ROOT, 'research', 'stage2-nodes')
INV_PATH = os.path.join(ROOT, 'research', 'stage1-inventory', 'inventory.json')
OUT_DIR = os.path.join(ROOT, '03-groups')
KNOWN_EXTERNAL = {os.path.normpath(os.path.join(ROOT, '04-interactive'))}

# 与 gen-node-pages.py 完全一致的徽章配色
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


def esc(s):
    return html_mod.escape(str(s) if s is not None else '', quote=True)


def badge_span(text, fg, bg, cls):
    return ('<span class="badge %s" style="color:%s;background:%s;border-color:%s">%s</span>'
            % (cls, fg, bg, fg, esc(text)))


def stage_badge(st):
    fg, bg, _ = STAGE_STYLE.get(st, STAGE_STYLE['basic'])
    return badge_span(st, fg, bg, 'st')


def priority_badge(pr):
    fg, bg, _ = PRIORITY_STYLE.get(pr, PRIORITY_STYLE['P3'])
    return badge_span(pr, fg, bg, 'p')


CSS = '''
:root{--bg:#0f1117;--panel:#161a22;--border:#2a2f3a;--text:#e6e8ee;--dim:#9aa3b2;--accent:#4f8cff;--ok:#2fb98a;--warn:#e8933b;--err:#c0504d;}
*{box-sizing:border-box;margin:0;padding:0;}
body{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,'PingFang SC','Microsoft YaHei',sans-serif;line-height:1.7;}
header{background:var(--panel);border-bottom:1px solid var(--border);padding:14px 24px;}
header .crumb{color:var(--dim);font-size:13px;margin-bottom:6px;}
header .crumb a{color:var(--accent);text-decoration:none;}
header .crumb a:hover{text-decoration:underline;}
header h1{font-size:20px;font-weight:650;color:#f0f3f9;display:inline-block;margin-right:12px;}
.badges{display:inline-flex;gap:6px;flex-wrap:wrap;vertical-align:middle;}
.badge{display:inline-block;padding:2px 10px;border-radius:20px;font-size:12px;font-weight:600;border:1px solid transparent;letter-spacing:.3px;}
.badge.grp{background:#1d2a3f;color:#7fb0ff;border-color:#2b3d5f;}
.badge.cnt{background:#23272f;color:#9aa0ab;border-color:#3a3f4a;}
main{padding:24px;max-width:1150px;margin:0 auto;}
h2{font-size:18px;margin:34px 0 12px;color:#cfd6e4;border-bottom:1px solid var(--border);padding-bottom:8px;}
h2 .dim{font-size:13px;font-weight:400;}
p,li{font-size:14px;}
ul{padding-left:22px;}
a{color:var(--accent);text-decoration:none;}
a:hover{text-decoration:underline;}
.dim{color:var(--dim);}
.section{scroll-margin-top:8px;}
.prchip,.stchip{display:inline-block;font-size:12px;font-weight:600;border-radius:4px;padding:1px 8px;margin-right:4px;border:1px solid transparent;}
.prchip.pr-P0{color:#e08a89;background:#5a1f1f;border-color:#c0504d;}
.prchip.pr-P1{color:#e8b06a;background:#3a2a12;border-color:#e8933b;}
.prchip.pr-P2{color:#8fb5ff;background:#16273f;border-color:#4f8cff;}
.prchip.pr-P3{color:#9aa0ab;background:#23272f;border-color:#6a707c;}
.stchip.st-basic{color:#6fd3ae;background:#122b22;border-color:#2fb98a;}
.stchip.st-intermediate{color:#e0a75e;background:#332412;border-color:#e8933b;}
.stchip.st-advanced{color:#c9a8ef;background:#2b2040;border-color:#b48ae0;}
.stchip.st-frontier{color:#dd8786;background:#3a1717;border-color:#c0504d;}
.tblwrap{overflow-x:auto;margin:8px 0;}
table{border-collapse:collapse;width:100%;}
th,td{border:1px solid var(--border);padding:7px 11px;font-size:13px;text-align:left;vertical-align:top;}
th{background:var(--panel);color:#b8c2d4;white-space:nowrap;}
td.nid{white-space:nowrap;font-family:Consolas,monospace;font-size:12px;}
td.nid a{color:#8fb5ff;}
td .nname{font-weight:600;color:var(--text);}
td.brief{font-size:12.5px;color:#b6c0d0;}
td.ex{text-align:center;color:var(--dim);font-size:12px;}
.pathbox{background:var(--panel);border:1px solid var(--border);border-radius:8px;padding:12px 16px;margin:10px 0;}
.path-label{font-size:12px;color:var(--dim);margin-bottom:8px;}
.path-seq{display:flex;flex-wrap:wrap;gap:4px 0;font-size:13px;}
.path-seq a{display:inline-block;background:#16273f;border:1px solid #2b3d5f;border-radius:6px;padding:2px 8px;color:#7fb0ff;text-decoration:none;margin:2px;}
.path-seq a:hover{background:#2b3d5f;}
.dep-list{list-style:none;padding-left:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:8px;margin-top:8px;}
.dep-list li{background:var(--panel);border:1px solid var(--border);border-radius:8px;padding:8px 12px;font-size:13px;border-left:3px solid var(--warn);}
.dep-list .evi{display:block;font-size:11px;color:var(--dim);margin-top:2px;font-family:Consolas,monospace;}
.treenav{background:var(--panel);border:1px solid var(--border);border-radius:8px;padding:10px 16px;margin:6px 0 18px;display:flex;flex-wrap:wrap;gap:2px 10px;}
.treenav .label{font-size:12px;color:var(--dim);align-self:center;flex-shrink:0;}
.treenav a{color:var(--dim);font-size:12px;text-decoration:none;border-radius:5px;padding:1px 6px;}
.treenav a:hover{color:var(--accent);background:#1d2a3f;}
.navseq{display:flex;gap:10px;margin:16px 0;flex-wrap:wrap;}
.navseq a{display:inline-block;background:var(--panel);border:1px solid var(--border);border-radius:8px;padding:10px 18px;font-size:14px;color:#b8c2d4;text-align:center;min-width:150px;}
.navseq a .dir{display:block;font-size:11px;color:var(--dim);margin-bottom:2px;}
.navseq a .v{font-weight:600;color:var(--accent);}
.navseq a.nav-index .v{color:var(--ok);}
.navseq .spacer{flex:1;min-width:60px;}
.domnav{display:flex;gap:10px;margin:12px 0;flex-wrap:wrap;}
.domnav .box{background:var(--panel);border:1px solid var(--border);border-radius:8px;padding:10px 16px;flex:1;min-width:220px;}
.domnav .box .lab{font-size:11px;color:var(--dim);margin-bottom:4px;}
.domnav .box a{display:block;font-size:13px;color:#b8c2d4;}
.domnav .box a .g{color:var(--accent);font-weight:600;}
footer{margin-top:44px;padding:16px 24px;border-top:1px solid var(--border);color:var(--dim);font-size:12px;text-align:center;}
@media (max-width:720px){
  main{padding:14px;}
  header{padding:12px 14px;}
  header h1{font-size:17px;}
  .navseq a{min-width:100%;}
  .badges{display:flex;margin-top:6px;}
}
@media print{
  body{background:#fff;color:#000;}
  header,footer,.treenav,.navseq,.domnav{display:none;}
  th,td{border-color:#999;color:#000;}
}
'''


def build_in_group_prereq(gid, node_ids, dag):
    node_set = set(node_ids)
    edges = []
    for e in dag['edges']:
        if e.get('type') != 'prerequisite':
            continue
        if e['from'] in node_set and e['to'] in node_set:
            edges.append((e['from'], e['to'], e.get('evidence', '')))
    return edges


def topo_order(node_ids, prereq_edges, inv_pos):
    """Kahn 拓扑排序，按 inventory 顺序稳定取源；有环时兜底补序。"""
    if not prereq_edges:
        return list(node_ids)
    adj = {n: [] for n in node_ids}
    indeg = {n: 0 for n in node_ids}
    for f, t, _ in prereq_edges:
        adj[f].append(t)
        indeg[t] += 1
    heap = []
    for n in node_ids:
        if indeg[n] == 0:
            heapq.heappush(heap, (inv_pos.get(n, 10 ** 9), n))
    order = []
    while heap:
        _, n = heapq.heappop(heap)
        order.append(n)
        for m in adj[n]:
            indeg[m] -= 1
            if indeg[m] == 0:
                heapq.heappush(heap, (inv_pos.get(m, 10 ** 9), m))
    seen = set(order)
    for n in node_ids:
        if n not in seen:
            order.append(n)
    return order


def render_group_page(g, group_list, group_ids, group_index, nodes, name_of, inv_pos, dag):
    gid = g['id']
    node_ids = g['node_ids']
    ordered = sorted(node_ids, key=lambda n: inv_pos.get(n, 10 ** 9))

    # ---- 节点目录表 ----
    rows = []
    for nid in ordered:
        nd = nodes.get(nid) or {}
        rows.append({
            'id': nid,
            'name': nd.get('name') or name_of.get(nid, nid),
            'pr': nd.get('priority', 'P3'),
            'st': nd.get('stage', 'basic'),
            'brief': nd.get('brief') or '',
            'ex': len(nd.get('examples') or []),
        })
    total = len(rows)
    trs = []
    for r in rows:
        trs.append(
            '<tr><td class="nid"><a href="../02-node-pages/%s.html">%s</a></td>'
            '<td><a href="../02-node-pages/%s.html" class="nname">%s</a></td>'
            '<td>%s</td><td>%s</td>'
            '<td class="brief">%s</td><td class="ex">%d</td></tr>'
            % (esc(r['id']), esc(r['id']), esc(r['id']), esc(r['name']),
               stage_badge(r['st']), priority_badge(r['pr']), esc(r['brief']), r['ex'])
        )
    table_html = ('<div class="section"><h2>节点目录 <span class="dim">(%d 个)</span></h2>'
                  '<div class="tblwrap"><table>'
                  '<tr><th>节点 ID</th><th>名称</th><th>阶段</th><th>优先级</th><th>简介</th><th>例题数</th></tr>'
                  '%s</table></div></div>' % (total, ''.join(trs)))

    # ---- 组简介 ----
    pr_counter = Counter(r['pr'] for r in rows)
    st_counter = Counter(r['st'] for r in rows)
    pr_summary = ' &middot; '.join(
        '<span class="prchip pr-%s">%s</span>' % (esc(k), esc('%s ×%d' % (k, v)))
        for k, v in sorted(pr_counter.items()) if v)
    st_summary = ' &middot; '.join(
        '<span class="stchip st-%s">%s</span>' % (esc(k), esc('%s ×%d' % (k, v)))
        for k, v in sorted(st_counter.items()) if v)
    brief_html = (
        '<div class="section"><h2>组简介</h2>'
        '<p>本组 <strong>%d</strong> 个知识点，属于 <strong>%s</strong> 域，覆盖阶段 <strong>%s</strong>。</p>'
        '<p class="dim">优先级分布：%s</p>'
        '<p class="dim">阶段分布：%s</p></div>'
        % (total, esc(g['domain']), esc(' / '.join(g['stage_range'])), pr_summary, st_summary))

    # ---- 学习路径提示 ----
    prereq = build_in_group_prereq(gid, node_ids, dag)
    if prereq:
        torder = topo_order(node_ids, prereq, inv_pos)
        items = []
        for f, t, ev in prereq:
            items.append('<li><a href="../02-node-pages/%s.html">%s</a> &rarr; '
                         '<a href="../02-node-pages/%s.html">%s</a><span class="evi">%s</span></li>'
                         % (esc(f), esc(name_of.get(f, f)), esc(t), esc(name_of.get(t, t)), esc(ev)))
        seq = ' &rarr; '.join('<a href="../02-node-pages/%s.html">%s</a>' % (esc(n), esc(name_of.get(n, n)))
                              for n in torder)
        path_html = (
            '<div class="section"><h2>学习路径提示</h2>'
            '<p class="dim">本组内存在 <strong>%d</strong> 条前置依赖边（prerequisite），'
            '推荐先掌握前置知识点，再进入依赖它的节点。</p>'
            '<div class="pathbox"><div class="path-label">推荐阅读顺序（拓扑序）</div>'
            '<div class="path-seq">%s</div></div>'
            '<ul class="dep-list">%s</ul></div>'
            % (len(prereq), seq, ''.join(items)))
    else:
        path_html = (
            '<div class="section"><h2>学习路径提示</h2>'
            '<p class="dim">本组内节点之间没有显式前置依赖（prerequisite）边，'
            '可按目录表顺序依次学习，或按知识基础灵活跳转。</p></div>')

    # ---- 组间导航 ----
    idx = group_index[gid]
    if idx > 0:
        prev_link, prev_label, prev_class = '../03-groups/%s.html' % group_ids[idx - 1], group_ids[idx - 1], 'nav-node'
    else:
        prev_link, prev_label, prev_class = '../04-interactive/index.html', '算法知识图谱总览', 'nav-index'
    if idx < len(group_ids) - 1:
        next_link, next_label, next_class = '../03-groups/%s.html' % group_ids[idx + 1], group_ids[idx + 1], 'nav-node'
    else:
        next_link, next_label, next_class = '../04-interactive/index.html', '算法知识图谱总览', 'nav-index'

    dom_groups = [x for x in group_list if x['domain'] == g['domain']]
    dom_ids = [x['id'] for x in dom_groups]
    d_idx = dom_ids.index(gid)
    d_prev = dom_ids[d_idx - 1] if d_idx > 0 else None
    d_next = dom_ids[d_idx + 1] if d_idx < len(dom_ids) - 1 else None
    dom_name = {x['id']: x['name'] for x in dom_groups}
    dom_count = len(dom_groups)
    domnav = ''
    if d_prev:
        domnav += ('<div class="box"><div class="lab">同域上一组</div>'
                   '<a href="../03-groups/%s.html"><span class="g">%s</span> · %s</a></div>'
                   % (esc(d_prev), esc(d_prev), esc(dom_name[d_prev])))
    domnav += ('<div class="box"><div class="lab">所属领域</div>'
               '<a><span class="g">%s</span> · 域内共 %d 组</a></div>'
               % (esc(g['domain']), dom_count))
    if d_next:
        domnav += ('<div class="box"><div class="lab">同域下一组</div>'
                   '<a href="../03-groups/%s.html"><span class="g">%s</span> · %s</a></div>'
                   % (esc(d_next), esc(d_next), esc(dom_name[d_next])))
    domnav_html = '<div class="domnav">%s</div>' % domnav

    treenav = '<span class="label">组目录:</span>' + ''.join(
        '<a href="../03-groups/%s.html">%s</a>' % (esc(x['id']), esc(x['name']))
        for x in group_list)

    badges = [badge_span(esc(g['domain']), '#7fb0ff', '#16273f', 'grp')]
    for st in g['stage_range']:
        badges.append(stage_badge(st))
    badges.append(badge_span('%d 节点' % total, '#9aa0ab', '#23272f', 'cnt'))

    page = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%(name)s · 组索引 · 算法知识图谱</title>
<style>%(css)s</style>
</head>
<body>
<header>
  <div class="crumb"><a href="../04-interactive/index.html">算法知识图谱总览</a> / <a href="../03-groups/%(gid)s.html">组目录</a> / <span>组索引</span></div>
  <h1>%(name)s</h1>
  <div class="badges">%(badges)s</div>
</header>
<main>
  <div class="treenav">%(treenav)s</div>

  <div class="navseq">
    <a class="%(prev_class)s" href="%(prev_link)s"><span class="dir">&#8592; 上一组</span><span class="v">%(prev_label)s</span></a>
    <a class="nav-index" href="../04-interactive/index.html"><span class="dir">全局</span><span class="v">返回总览</span></a>
    <a class="%(next_class)s" href="%(next_link)s"><span class="dir">下一组 &#8594;</span><span class="v">%(next_label)s</span></a>
  </div>

%(brief)s

%(table)s

%(path)s

%(domnav)s
</main>
<footer>算法知识图谱 · 372 个知识点 · 60 组 · 4 层 · 组索引页由 algorithm-dag.json + stage2-nodes 内容库生成</footer>
</body>
</html>''' % {
        'css': CSS,
        'name': esc(g['name']),
        'gid': esc(gid),
        'badges': ''.join(badges),
        'treenav': treenav,
        'prev_class': prev_class, 'prev_link': esc(prev_link), 'prev_label': esc(prev_label),
        'next_class': next_class, 'next_link': esc(next_link), 'next_label': esc(next_label),
        'brief': brief_html,
        'table': table_html,
        'path': path_html,
        'domnav': domnav_html,
    }
    return page


def main():
    dag = json.load(open(DAG_PATH, encoding='utf-8'))
    inv = json.load(open(INV_PATH, encoding='utf-8'))
    nodes = {}
    for f in sorted(os.listdir(NODES_DIR)):
        if not f.endswith('.json'):
            continue
        nd = json.load(open(os.path.join(NODES_DIR, f), encoding='utf-8'))
        if nd.get('id') and not nd['id'].startswith('_'):
            nodes[nd['id']] = nd
    inv_pos = {n['id']: i for i, n in enumerate(inv['nodes'])}
    name_of = {n['id']: n.get('name', n['id']) for n in dag['nodes']}

    group_list = dag['groups']
    group_ids = [g['id'] for g in group_list]
    group_index = {gid: i for i, gid in enumerate(group_ids)}

    os.makedirs(OUT_DIR, exist_ok=True)
    generated = []
    for g in group_list:
        page = render_group_page(g, group_list, group_ids, group_index,
                                 nodes, name_of, inv_pos, dag)
        out_path = os.path.join(OUT_DIR, '%s.html' % g['id'])
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(page)
        generated.append(g['id'])

    print('[gen] 生成 %d 组索引页 -> %s' % (len(generated), OUT_DIR))

    # ---- 校验 ----
    fail = []
    for gid in generated:
        ok, msg = validate_page(os.path.join(OUT_DIR, '%s.html' % gid))
        if not ok:
            fail.append((gid, msg))
    print('[validate] 通过 %d / %d' % (len(generated) - len(fail), len(generated)))
    for gid, msg in fail[:50]:
        print('[validate] FAIL %s: %s' % (gid, msg), file=sys.stderr)

    broken = []
    for gid in generated:
        with open(os.path.join(OUT_DIR, '%s.html' % gid), encoding='utf-8') as f:
            content = f.read()
        for href in re.findall(r'href="([^"]+\.html)"', content):
            if href.startswith('http'):
                continue
            resolved = os.path.normpath(os.path.join(OUT_DIR, href))
            if os.path.exists(resolved):
                continue
            if any(resolved.startswith(k) for k in KNOWN_EXTERNAL):
                continue
            broken.append((gid, href))
    print('[links] 内部断链 %d' % len(broken))
    for gid, href in broken[:30]:
        print('[links] BROKEN %s -> %s' % (gid, href), file=sys.stderr)

    link_mismatch = []
    for gid in generated:
        with open(os.path.join(OUT_DIR, '%s.html' % gid), encoding='utf-8') as f:
            content = f.read()
        g = [x for x in group_list if x['id'] == gid][0]
        expected = len(g['node_ids'])
        actual = len(set(re.findall(r'href="../02-node-pages/([^"/]+)\.html"', content)))
        if actual != expected:
            link_mismatch.append((gid, expected, actual))
    print('[nodes] 组内节点链接数全部匹配: %s' % ('YES' if not link_mismatch else 'NO'))
    for gid, e, a in link_mismatch[:30]:
        print('[nodes] MISMATCH %s expected=%d actual=%d' % (gid, e, a), file=sys.stderr)

    return 1 if (fail or broken or link_mismatch) else 0


# ---------------------------------------------------------------- 校验
VALIDATE_TAGS = ['div', 'table', 'thead', 'tbody', 'tr', 'th', 'td',
                 'ul', 'ol', 'li', 'span', 'a', 'h1', 'h2', 'h3', 'header',
                 'main', 'footer', 'strong', 'em', 'p']
TAG_RE = re.compile(r'<(/?)([a-zA-Z][a-zA-Z0-9]*)(?:\s[^<>]*?)?>')


def validate_page(path):
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
    for tag in VALIDATE_TAGS:
        o = len(re.findall(r'<%s(?:\s[^<>]*?)?/?>' % tag, content))
        c = len(re.findall(r'</%s>' % tag, content))
        if o != c:
            return False, '<%s> 开 %d 闭 %d 不平衡' % (tag, o, c)
    cleaned = TAG_RE.sub('', content)
    cleaned = cleaned.replace('<!DOCTYPE html>', '')
    if '<' in cleaned:
        pos = cleaned.find('<')
        return False, '存在未转义 < (位置约 %d)' % pos
    return True, 'OK'


if __name__ == '__main__':
    sys.exit(main())
