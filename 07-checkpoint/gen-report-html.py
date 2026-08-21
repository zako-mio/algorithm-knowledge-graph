#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""report.md -> report.html 转换 + 质量门控"""
import re, sys, html as html_mod

def md_to_html(md: str) -> str:
    lines = md.split('\n')
    out = []
    in_table = False
    table_rows = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # 表格
        if line.strip().startswith('|'):
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if not in_table:
                in_table = True
                table_rows = []
            if re.match(r'^[\s:\-|]+$', line.replace('|', '').strip()):
                i += 1
                continue
            table_rows.append(cells)
            i += 1
            continue
        elif in_table:
            in_table = False
            if table_rows:
                out.append('<table><thead><tr>' + ''.join(f'<th>{html_mod.escape(c)}</th>' for c in table_rows[0]) + '</tr></thead><tbody>')
                for row in table_rows[1:]:
                    out.append('<tr>' + ''.join(f'<td>{html_mod.escape(c)}</td>' for c in row) + '</tr>')
                out.append('</tbody></table>')
            table_rows = []
        # 标题
        m = re.match(r'^(#{1,4})\s+(.*)', line)
        if m:
            lvl = len(m.group(1))
            out.append(f'<h{lvl}>{html_mod.escape(m.group(2))}</h{lvl}>')
            i += 1
            continue
        # 列表项
        m = re.match(r'^(\s*)[-*]\s+(.*)', line)
        if m:
            out.append(f'<li>{inline(m.group(2))}</li>')
            i += 1
            continue
        m = re.match(r'^(\s*)\d+\.\s+(.*)', line)
        if m:
            out.append(f'<li>{inline(m.group(2))}</li>')
            i += 1
            continue
        # 引用
        if line.strip().startswith('>'):
            out.append(f'<blockquote>{inline(line.strip().lstrip(">").strip())}</blockquote>')
            i += 1
            continue
        # 代码块
        if line.strip().startswith('```'):
            out.append('<pre>')
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                out.append(html_mod.escape(lines[i]))
                i += 1
            out.append('</pre>')
            i += 1
            continue
        # 空行
        if not line.strip():
            out.append('')
            i += 1
            continue
        # 普通段落
        out.append(f'<p>{inline(line)}</p>')
        i += 1
    return '\n'.join(out)

def inline(s: str) -> str:
    s = html_mod.escape(s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'\*(.+?)\*', r'<i>\1</i>', s)
    s = re.sub(r'`(.+?)`', r'<code>\1</code>', s)
    s = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', s)
    return s

def main():
    src = '/home/zako-mio/opencode/archive/Mission-file/2026-08/0820-algorithm-knowledge-graph/report.md'
    dst = '/home/zako-mio/opencode/archive/Mission-file/2026-08/0820-algorithm-knowledge-graph/report.html'
    md = open(src, encoding='utf-8').read()
    body = md_to_html(md)
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>算法知识图谱 · 调研阶段留档报告</title>
<style>
  :root {{ --bg:#0f1117; --panel:#161a22; --border:#2a2f3a; --text:#e6e8ee; --dim:#9aa3b2; --accent:#4f8cff; --ok:#2fb98a; }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:var(--bg); color:var(--text); font-family:'Segoe UI',system-ui,sans-serif; line-height:1.8; }}
  header {{ background:var(--panel); border-bottom:1px solid var(--border); padding:28px 32px; }}
  header h1 {{ font-size:24px; margin-bottom:6px; }}
  header p {{ color:var(--dim); font-size:14px; }}
  main {{ padding:28px 32px; max-width:1100px; margin:0 auto; }}
  h2 {{ font-size:19px; margin:32px 0 14px; color:#cfd6e4; border-bottom:1px solid var(--border); padding-bottom:8px; }}
  h3 {{ font-size:16px; margin:22px 0 10px; color:var(--accent); }}
  h4 {{ font-size:14px; margin:16px 0 8px; color:#cfd6e4; }}
  p {{ margin:8px 0; }}
  li {{ margin:4px 0 4px 22px; }}
  table {{ border-collapse:collapse; margin:12px 0; width:100%; font-size:13px; }}
  th {{ background:#1d2a3f; border:1px solid var(--border); padding:8px 10px; text-align:left; color:#cfd6e4; }}
  td {{ border:1px solid var(--border); padding:8px 10px; }}
  pre {{ background:var(--panel); border:1px solid var(--border); border-radius:8px; padding:12px 16px; overflow-x:auto; font-size:12px; margin:10px 0; }}
  code {{ background:#1d2a3f; border-radius:4px; padding:1px 5px; font-size:12px; }}
  blockquote {{ border-left:3px solid var(--accent); background:var(--panel); padding:10px 14px; margin:10px 0; border-radius:0 8px 8px 0; color:var(--dim); }}
  a {{ color:var(--accent); text-decoration:none; }}
</style>
</head>
<body>
<header>
  <h1>算法知识图谱 · 调研阶段留档报告</h1>
  <p>任务目录：2026-08/0820-algorithm-knowledge-graph · 留档日期：2026-08-21</p>
</header>
<main>
{body}
</main>
</body>
</html>'''
    open(dst, 'w', encoding='utf-8').write(html)
    # ===== 质量门控 =====
    errs = []
    if '\ufffd' in html:
        errs.append('UTF-8 替换字符 U+FFFD 存在')
    if html.count('<div') != html.count('</div>'):
        errs.append('div 开闭不平衡')
    # 5 段完整性
    for sec in ['当时情况', '制定计划', '执行情况', '完成情况', '反思/分析/建议']:
        if sec not in md:
            errs.append(f'缺少段: {sec}')
    # HTML 基本结构
    if '<html' not in html or '</html>' not in html:
        errs.append('HTML 结构不完整')
    print('质量门控:', 'PASS ✅' if not errs else f'FAIL ❌ {errs}')
    print('输出:', dst, f'({len(html)} bytes)')
    return 0 if not errs else 1

if __name__ == '__main__':
    sys.exit(main())
