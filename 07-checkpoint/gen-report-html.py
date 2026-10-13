#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""report.md -> report.html 转换 + 质量门控

★ 批 J 注意（**归属实测结论**，brief §5 要求先实测）：
  · 本脚本的 `src`/`dst` 是**仓外绝对路径**（见本文件 `main()`）⇒ 它写的是
    `2026-08/0820-algorithm-knowledge-graph/report.html`，**不是**站点仓内的 `report.html`；
  · 站点仓内那份 `report.html` 与仓外产物**逐字节相同**（sha256 `ad486b5c…`，实测）⇒ 仓内那份是
    「仓外产物的过期副本」，**没有任何生成器把它当输出目标**（仓内 grep `report\\.html` 只命中
    README / 门控夹具 / profile 登记表）。
  ⇒ 仓内 `report.html` 按 COMMON.md §1.2 的**手写源**路径直接改（补 a11y 三件 ＋ head 8 行元数据）。
    本脚本模板**同步**补上同样四处，使「源」与「产物」不再分叉；
    ⛔ 本文件仍**不在** `profile.generator_commands` 里（跑它会写仓外），⛔ 收尾也**不**内联调用门控
    （它不产发布根页面，且会污染仓内 gate-report.json 的判据面）。
"""
import os
import re
import sys
import html as html_mod

# ★ 复用批 J 的共用件（同目录 `site_meta.py`）：只取站点常量，⛔ 不复制字面值。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import site_meta  # noqa: E402

REL_PATH_FOR_CANON = 'report.html'


def meta_lines(desc, title):
    """COMMON.md §2.1 的 8 行（canonical / og:url 用发布根下 report.html 的规范 URL）。"""
    url = site_meta.page_url(REL_PATH_FOR_CANON)
    return ('<meta name="description" content="%s">\n'
            '<meta property="og:type" content="website">\n'
            '<meta property="og:title" content="%s">\n'
            '<meta property="og:description" content="%s">\n'
            '<meta property="og:url" content="%s">\n'
            '<meta property="og:image" content="%s">\n'
            '<link rel="canonical" href="%s">\n'
            '<link rel="icon" type="image/svg+xml" href="%s">\n'
            % (desc, title, desc, url, site_meta.OG_IMAGE, url, site_meta.FAVICON_HREF))


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
    # ★ 批 J：head 8 行元数据 ＋ a11y 三件（与站点侧 report.html 手写源的补丁逐条对应）
    desc = site_meta.make_description([
        '算法知识图谱的调研阶段留档报告：372 个知识点 / 60 知识组 / 318 关系边的两阶段调研与构建过程留档。',
        '含当时情况、制定计划、执行情况、完成情况与反思建议五段；记录 42 次子 Agent 委派、'
        '6 次批次失败重跑与 104 文件规范化修复等关键过程事件。',
    ])
    title = '算法知识图谱 · 调研阶段留档报告'
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{meta_lines(desc, title)}<title>{title}</title>
<style>
  :root {{ --bg:#0f1117; --panel:#161a22; --border:#2a2f3a; --text:#e6e8ee; --dim:#9aa3b2; --accent:#4f8cff; --ok:#2fb98a; }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  :focus-visible{{outline:0.125rem solid var(--accent,#4f8cff);outline-offset:0.125rem}}
  .skip-link{{position:absolute;left:-9999px;top:0;background:var(--accent,#4f8cff);color:#fff;padding:0.5rem 1rem;z-index:100}}
  .skip-link:focus{{left:0}}
  .skip{{position:absolute;left:-9999px;top:0;background:var(--panel);color:var(--accent);border:1px solid var(--border);padding:8px 14px;font-size:13px;text-decoration:none;}}
  .skip:focus{{left:0;}}
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
<a class="skip" href="#main">跳到主要内容</a>
<header>
  <h1>算法知识图谱 · 调研阶段留档报告</h1>
  <p>任务目录：2026-08/0820-algorithm-knowledge-graph · 留档日期：2026-08-21</p>
</header>
<main id="main">
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
