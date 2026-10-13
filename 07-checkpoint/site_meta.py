#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批 J · algorithm-knowledge-graph 的 **head 元数据 + 站点级 SEO 资产** 共用件。

本件是**新增的共用件**（⛔ 不是第二套门控）：三个 HTML 生成器
（`gen-node-pages.py` / `gen-group-pages.py` / `gen-views.py`）运行期 import 它，
从而让「发布根下每一个 .html」的 `<head>` 满足 `gate_seo_meta.py` 的 S4–S8 精确形态。

★ 形态（COMMON.md §2.1，8 行，顺序不限）：
    <meta name="description" content="{desc}">
    <meta property="og:type" content="website">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="{ABS_URL}">
    <meta property="og:image" content="https://zako-mio.github.io/{REPO}/og.png">
    <link rel="canonical" href="{ABS_URL}">
    <link rel="icon" type="image/svg+xml" href="/{REPO}/favicon.svg">

★ `{ABS_URL}` 的 PATH 规则（与 `gate_seo_meta.page_url()` 逐字同口径）：
    `X/index.html` → `X/`；`X/Y.html` → `X/Y.html`；根 `index.html` → 空串。
  ⇒ S6 硬判**自指**，本件必须与门控用同一条规则（⛔ 不各写一套）。

★ 确定性：⛔ 无墙钟时间戳、⛔ 无作者机绝对路径。`sitemap.xml` ⛔ 不含 `<lastmod>`。
★ 单源不变量（`gate_tokens.py` 的 T8）：本件**不得**持有任何令牌字面值
  （`:root{…}` 块 或 `--token:#hex` 赋值）。本件只写 `<head>` 元数据与站点级 SEO 资产。
"""
import html as html_mod
import json
import os
import re
import sys

REPO = 'algorithm-knowledge-graph'
BASE_URL = 'https://zako-mio.github.io/%s/' % REPO
OG_IMAGE = 'https://zako-mio.github.io/%s/og.png' % REPO
FAVICON_HREF = '/%s/favicon.svg' % REPO
SITE_NAME = '算法知识图谱'
SITE_SUBTITLE = '算法 / 数据结构 · 关系结构总览'

# 元数据行在模板里的锚点：紧跟 viewport 声明之后插入。
VIEWPORT_LINE = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
META_ANCHOR = VIEWPORT_LINE + '\n'
META_MARK = '<meta name="description"'


def esc(s):
    """HTML 属性值转义（与生成器模板的转义口径一致）。"""
    return html_mod.escape(str(s) if s is not None else '', quote=True)


# ---------------------------------------------------------------- 文本工具
_WS_RE = re.compile(r'\s+')
_TAG_RE = re.compile(r'<[^>]*>')


def plain(s):
    """把可能含标签/实体/换行的文本压成单行纯文本（description 的取词面）。"""
    s = _TAG_RE.sub('', str(s or ''))
    s = html_mod.unescape(s)
    return _WS_RE.sub(' ', s).strip()


def shorten(s, limit=160):
    """截到 limit 字符以内；在标点处收尾，避免半截词。"""
    s = plain(s)
    if len(s) <= limit:
        return s
    cut = s[:limit]
    for mark in ('。', '；', '，', '、', ' ', '.', ',', ';'):
        pos = cut.rfind(mark)
        if pos >= limit // 2:
            return cut[:pos + 1].strip()
    return cut.strip()


def make_description(parts, limit=160):
    """拼出非空、逐页不同的 description（按 `。` 连接，去重，压到 limit 以内）。"""
    seen, chunks = set(), []
    for p in parts:
        t = plain(p)
        if not t or t in seen:
            continue
        seen.add(t)
        chunks.append(t)
    if not chunks:
        chunks = ['%s · %s' % (SITE_NAME, SITE_SUBTITLE)]
    out = ''
    for c in chunks:
        cand = (out + '。' + c) if out else c
        if len(cand) > limit:
            break
        out = cand
    if not out:
        out = chunks[0]
    return shorten(out, limit)


# ---------------------------------------------------------------- URL 规则
def page_url(rel):
    """页内相对路径 → 该页**自身**的规范 URL（★ 与 gate_seo_meta.page_url() 同口径）。"""
    rel = rel.replace(os.sep, '/')
    if rel == 'index.html':
        return BASE_URL
    if rel.endswith('/index.html'):
        return BASE_URL + rel[: -len('index.html')]
    return BASE_URL + rel


def rel_of(root, path):
    """绝对路径 → 相对发布根（仓根）的 posix 路径。"""
    return os.path.relpath(path, root).replace(os.sep, '/')


# ---------------------------------------------------------------- head 元数据
# ★ 外链页（63 页：60 组页 ＋ 3 视图页）的内联 CSS 规则（COMMON.md §2.3 的精确形态）。
#   为什么外链页也要内联一份：`assets/tokens.css` 是 **whole-file 令牌产物**，
#   `gate_tokens.py` 的 T3 硬判它**逐字节 == 值件派生**（实测：追加规则后 T3 立刻 FAIL）
#   ⇒ ⛔ 不能往它里面加布局规则。门控 A4 是**形态感知**的「内联 ∪ 页内本地外链」并集，
#   把规则放进页的内联 `<style>` 即在同一判据面上成立（COMMON.md §2.3 的第二分支明许）。
#   `.skip-link` 与页内既有的 `.skip` 同声明：skip 锚点用 `class="skip"`
#   （`gate_design.py` 的 D5 硬判 `class="skip"` 恰 1 ⇒ ⛔ 不改成 skip-link）。
FOCUS_RULES = (
    ':focus-visible{outline:0.125rem solid var(--accent,#4f8cff);outline-offset:0.125rem}\n'
    '.skip-link{position:absolute;left:-9999px;top:0;background:var(--accent,#4f8cff);'
    'color:#fff;padding:0.5rem 1rem;z-index:100}\n'
    '.skip-link:focus{left:0}')


def inject_focus_rules(page):
    """把 `:focus-visible` ＋ `.skip-link` 规则追加进页面的**内联** `<style>`（幂等）。

    ★ 追加点是**页面最后一个** `</style>` ⇒ 规则落在该页 CSS 语料的末尾，
      与模板内既有规则同特异性、按后来居生效（`skip-link` 与 `skip` 互不影响）。
    """
    if '.skip-link{' in page:
        return page
    idx = page.rfind('</style>')
    if idx < 0:
        return page
    return page[:idx] + FOCUS_RULES + '\n' + page[idx:]


def meta_block(desc, title, url, with_icon=True):
    """产出 COMMON.md §2.1 的 8 行（顺序固定 ⇒ 逐字节确定性）。

    ★ `with_icon=False`：**外链页（63 页）**专用。`gate_tokens.py` 的 T12 硬判外链页
      「**有且仅有 1 个** `<link>`，且该 `<link>` 必须是指向 `assets/tokens.css` 的 stylesheet」
      （实测：加上 favicon 的 `<link>` 后 T12 立刻 FAIL —— `<link>` 数 = 3）。
      而 `gate_seo_meta.py` 的 S7 是**析取**判据：「每页有 `<link rel=icon>`，**或**发布根存在
      favicon 文件」⇒ 发布根已有 `favicon.svg` 时，S7 由后半条成立，⛔ 不必逐页写 icon link。
      ⇒ 外链页只写 7 行（省掉 favicon 那行），两道门控同时成立（⛔ 两侧判据与阈值都未改）。
    """
    rows = ('<meta name="description" content="%s">\n'
            '<meta property="og:type" content="website">\n'
            '<meta property="og:title" content="%s">\n'
            '<meta property="og:description" content="%s">\n'
            '<meta property="og:url" content="%s">\n'
            '<meta property="og:image" content="%s">\n'
            '<link rel="canonical" href="%s">\n'
            % (esc(desc), esc(title), esc(desc), esc(url), esc(OG_IMAGE), esc(url)))
    if with_icon:
        rows += '<link rel="icon" type="image/svg+xml" href="%s">\n' % esc(FAVICON_HREF)
    return rows


def inject_head_meta(page, rel, desc, title, with_icon=True):
    """把元数据行插进已渲染好的页面 `<head>`（幂等：已注入则原样返回）。

    ★ 同时补齐 `:focus-visible` ＋ `.skip-link` 内联规则（`inject_focus_rules`，幂等）
      —— 内联页与**外链页**都走同一条路径：外链页的 `assets/tokens.css` 只能含令牌
      （T3 硬判逐字节 == 值件派生），故规则必须落在页的内联 `<style>` 里（门控 A4 形态感知并集）。

    ★ `with_icon=False` 供**外链页**用（T12 判「外链页有且仅有 1 个 `<link>`」，
      见 `meta_block` 的说明）。默认 True ⇒ 内联页写满 8 行。

    ★ 为什么用「注入」而不是改三个模板的格式串：三个模板的 `<head>` 结构各不相同
      （节点页/组页/视图页），注入点统一是 viewport 声明之后 ⇒ 一处实现、三处复用，
      ⛔ 不把同一段 8 行在三个文件里各写一遍（那正是「多份真相源」的成因）。
    """
    page = inject_focus_rules(page)
    if META_MARK in page:
        return page
    block = meta_block(desc, title, page_url(rel), with_icon=with_icon)
    if META_ANCHOR in page:
        return page.replace(META_ANCHOR, META_ANCHOR + block, 1)
    return page.replace('</head>', block + '</head>', 1)


# ---------------------------------------------------------------- 站点级资产
SITEMAP_HEAD = ('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
SITEMAP_TAIL = '</urlset>\n'


def sitemap_xml(rels):
    """确定性 `sitemap.xml`：覆盖发布根下**全部** .html 产物页。

    ★ ⛔ 不写 `<lastmod>`（墙钟时间戳会破坏幂等判据；COMMON.md §1.6）。
    ★ `<loc>` 按相对路径字典序 ⇒ 同输入两次运行逐字节相同。
    """
    out = [SITEMAP_HEAD]
    for rel in sorted(set(r.replace(os.sep, '/') for r in rels)):
        out.append('  <loc>%s</loc>\n' % html_mod.escape(page_url(rel), quote=False))
    out.append(SITEMAP_TAIL)
    return ''.join(out)


def robots_txt():
    """确定性 `robots.txt`（含 `Sitemap:` 指向 sitemap.xml —— S8 硬判）。"""
    return ('User-agent: *\n'
            'Allow: /\n'
            'Sitemap: %ssitemap.xml\n' % BASE_URL)


def publish_root_pages(root):
    """发布根（仓根）下全部产物页的相对路径（去 vendor/ 与点目录）。

    ★ 判据对象 == 断言对象：与 `gate_a11y.product_pages()` / `gate_seo_meta.product_pages()`
      的扫描面口径一致（`**/*.html`，去 `/vendor/`）。手写页与生成物**都**在集合里。
    """
    out = []
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d != 'vendor' and not d.startswith('.')]
        for f in fn:
            if f.endswith('.html'):
                out.append(os.path.relpath(os.path.join(dp, f), root).replace(os.sep, '/'))
    return sorted(out)


def write_site_files(root):
    """在发布根写出 `sitemap.xml` / `robots.txt`，返回 (路径列表, 页数)。"""
    rels = publish_root_pages(root)
    written = []
    for name, content in (('sitemap.xml', sitemap_xml(rels)),
                          ('robots.txt', robots_txt())):
        path = os.path.join(root, name)
        with open(path, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(content)
        written.append(path)
    print('[seo] 写出 %s / %s（sitemap 覆盖 %d 页，⛔ 无 <lastmod>）'
          % (os.path.basename(written[0]), os.path.basename(written[1]), len(rels)))
    return written, len(rels)


# ---------------------------------------------------------------- 门控收尾调用
GATE_SUMMARY_RE = re.compile(r'^===\s*(.+?)\s*===\s*$', re.M)


def _summarize(stdout):
    """从门控 stdout 里取最后一行 `=== … ===` 摘要（确定性、⛔ 无时间戳）。"""
    hits = GATE_SUMMARY_RE.findall(stdout or '')
    return hits[-1] if hits else ''


def run_site_gates(root):
    """★ 门控**随生成器收尾内联调用**（fail-closed，留痕 `gate-report.json`）。

    本站**无 CI**（brief §1）⇒ 生成器收尾即唯一的自动门控时机。本函数：

      ① `gate_tokens.py` / `gate_design.py`：`--mode report --report-out gate-report.json`
         （沿用批 H 的 Q5-B 口径；两者会把各自一节**并入**同一份报告）；
      ② `gate_a11y.py` / `gate_seo_meta.py`：硬档实跑（两者无 `--report-out`，输出在 stdout）
         ⇒ 本函数解析其 `=== … ===` 摘要行，把结果并入 `gate-report.json`
         （确定性：⛔ 无墙钟时间戳、⛔ 无作者机绝对路径）。

    ★ **fail-closed**：任一门控 exit 非 0 ⇒ 返回非 0 ⇒ 调用方（`main()`）以非 0 退出。
      ⛔ 不把「门控没跑」或「门控失败」读作通过。
    ★ 与批 H 的差别（如实登记）：批 H 是 report 档不阻断；批 J 起 **a11y / metadata 转硬档**
      （`gate-manifest.json` 的 `mode=hard`），故本函数对这两道门控**真阻断**。
      `gate_tokens.py` / `gate_design.py` 仍按批 H 口径以 report 档留痕（⛔ 未动它们的判据与阈值）。
    """
    steps = (
        ('gate_tokens.py', ['--site-root', root, '--manifest', 'gate-manifest.json',
                            '--mode', 'report', '--report-out', os.path.join(root, 'gate-report.json')]),
        ('gate_design.py', ['--site-root', root, '--manifest', 'gate-manifest.json',
                            '--mode', 'report', '--report-out', os.path.join(root, 'gate-report.json')]),
        ('gate_a11y.py', ['--site-root', root, '--profile', 'build/profile.json']),
        ('gate_seo_meta.py', ['--site-root', root, '--profile', 'build/profile.json']),
    )
    rc, extra = 0, []
    for script, args in steps:
        path = os.path.join(root, script)
        if not os.path.isfile(path):
            print('[gate] FAIL：未找到 %s（fail-closed，⛔ 不静默跳过）' % script)
            rc = rc or 1
            continue
        r = subprocess_run(path, args, root)
        tail = _summarize(r.stdout)
        print('[gate] %s rc=%d %s' % (script, r.returncode, tail))
        if r.returncode != 0:
            err = [ln for ln in (r.stdout or '').strip().splitlines() if ln.startswith('[FAIL]')]
            for ln in err[:6]:
                print('[gate] %s' % ln)
            rc = rc or r.returncode
        if script in ('gate_a11y.py', 'gate_seo_meta.py'):
            extra.append({'gate': script, 'exit_code': r.returncode, 'summary': tail})
    _merge_report(os.path.join(root, 'gate-report.json'), extra)
    return rc


def subprocess_run(path, args, cwd):
    """跑一个门控脚本（stdin 关闭，防门控误读调用方的 stdin）。"""
    import subprocess
    return subprocess.run([sys.executable, path] + args, cwd=cwd,
                          capture_output=True, text=True, stdin=subprocess.DEVNULL)


def _merge_report(path, extra):
    """把 a11y / seo 两节的**摘要**并入 `gate-report.json`（确定性合并，先读后写）。"""
    if not extra:
        return
    doc = {}
    if os.path.isfile(path):
        try:
            with open(path, encoding='utf-8') as fh:
                doc = json.load(fh)
        except Exception:  # noqa: BLE001
            doc = {}
    entries = {}
    for e in (doc.get('gates') or []):
        if isinstance(e, dict) and e.get('gate'):
            entries[e['gate']] = e
    for e in extra:
        entries[e['gate']] = {'gate': e['gate'], 'mode': 'hard', 'exit_code': e['exit_code'],
                              'summary': e['summary'],
                              'determinism_note': '★ 本节的判据与阈值未改；批 J 起执行强度为 hard。'}
    out = {'site': doc.get('site') or 'algorithm-knowledge-graph',
           'schema': doc.get('schema') or 'site-gate-report/1',
           'deterministic': True,
           'determinism_note': doc.get('determinism_note') or
                               '★ 确定性件：⛔ 无墙钟时间戳、⛔ 无作者机绝对路径。',
           'gates': [entries[k] for k in sorted(entries)]}
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write('\n')
