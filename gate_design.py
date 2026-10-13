#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gate_design.py — algorithm-knowledge-graph 的**六类设计门控**（批 H 标准档新建）。

范式来源：`solutions/_shared/SH5-gating.md` §4.2 的六类表 ＋ §4.0 十条。
★ 与 `gate_tokens.py` 的分工（⛔ 不重叠、不互相替代、⛔ 不造第二套实现）：
    `gate_tokens.py` 承担**类① 对比度**与**类② 令牌唯一值**（判据 T1–T12，含空集守卫与覆盖完备性）；
    本件是**六类伞**：① ② 由 `import gate_tokens` **转发**（同一实现，⛔ 不复制），
    ③ 死 CSS ④ 无障碍 ⑤ 响应式 ⑥ 元数据 在本件实现。
★ 本站规模约束（方案 §4.5）：门控分「**全量静态**」与「**抽样渲染**」两档，另加「**变更面增量**」档。
    全量静态：438 页全跑（代价可接受）；
    变更面增量：只对与基线 sha256 不同的页跑全量判据（**变更集为空 ⇒ SKIP**，⛔ 不是 PASS）；
    抽样渲染：12 页 × 4 视口——★ 本机**无浏览器** ⇒ **未测**，如实输出 SKIP ＋ 未覆盖面声明。

判据状态词表（四态）：PASS / FAIL（阻断类不成立）/ REPORT（report-only 档不成立）/ SKIP（未跑或不适用，⛔ 不得读作 PASS）。

用法：
    python3 gate_design.py --site-root . --manifest gate-manifest.json
    python3 gate_design.py --site-root . --mode enforce
    python3 gate_design.py --site-root . --report-out gate-report.json
    python3 gate_design.py --selftest

退出码：0 全过（或报告模式且有 hard/report 类 FAIL 但无 blind FAIL）/ 1 有阻断级 FAIL / 2 输入错误 / 3 护栏拒读
"""
import argparse
import hashlib
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import gate_tokens as GT  # noqa: E402  ★ 复用令牌/对比度两类判据（⛔ 不造第二套）

BLIND, HARD, REPORT, SKIP = "blind", "hard", "report", "skip"

CLASS_TABLE = [
    ("contrast", "① 对比度", "令牌产物的真实色值", "WCAG 正文 4.5:1 / 非文本 3.0:1（usage_tiers）"),
    ("token-consistency", "② 令牌唯一值", "各页面族令牌产物的 sha256 ＋ 同名值一致性", "权威源（值件）展开结果"),
    ("dead-css", "③ 死 CSS", "产物的 class 集合 vs 样式表的选择器集合", "差集为空"),
    ("a11y", "④ 无障碍", "产物的 <main> / skip link / role=img / :focus-visible", "SH2 §4.2"),
    ("responsive", "⑤ 响应式", "四视口下 documentElement.scrollWidth（★ 本机未测，退化为静态判据）", "SH3 §4.2"),
    ("metadata", "⑥ 元数据", "产物的 description / og / canonical / favicon / sitemap", "SH4 §4.2"),
]

STYLE_RE = re.compile(r"<style\b[^>]*>(.*?)</style>", re.S | re.I)
SCRIPT_RE = re.compile(r"<script\b[^>]*>.*?</script>", re.S | re.I)
CLASS_ATTR_RE = re.compile(r'class="([^"]*)"')
SEL_CLASS_RE = re.compile(r"\.(-?[_a-zA-Z][_a-zA-Z0-9-]*)")
SVG_RE = re.compile(r"<(svg|canvas)\b[^>]*>", re.I)
MEDIA_BP_RE = re.compile(r"@media[^{]*\(\s*(?:max|min)-width", re.I)
MEDIA_ANY_RE = re.compile(r"@media", re.I)
VIEWPORT_RE = re.compile(r'<meta[^>]+name=["\']viewport["\'][^>]*>', re.I)
LANG_RE = re.compile(r'<html[^>]+lang=["\']([^"\']+)["\']', re.I)
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'<meta[^>]+name=["\']description["\'][^>]*>', re.I)
OG_RE = re.compile(r'<meta[^>]+property=["\']og:', re.I)
CANON_RE = re.compile(r'<link[^>]+rel=["\']canonical["\'][^>]*>', re.I)
ICON_RE = re.compile(r'<link[^>]+rel=["\'][^"\']*icon[^"\']*["\'][^>]*>', re.I)


def _ok(klass, ok):
    if ok:
        return "PASS"
    return "REPORT" if klass == REPORT else "FAIL"


def pages_with(site_root, profile, only=None):
    pgs = GT.collect_pages(site_root, profile)
    if only is not None:
        pgs = {k: v for k, v in pgs.items() if k in only}
    return pgs


# --------------------------------------------------------------------------- 类③–⑥
def cls_dead_css(site_root, profile, pages):
    """类③ 死 CSS：判据对象 = 页面**静态 HTML** 里的 class 集合 vs 该页 `<style>` 的选择器集合。

    ★ 判据方向的选择（SH5 §4.0 第 1 条「判据对象必须与断言对象一致」）——**本步实测修正了方向**：
      朴素的「用到的 class − 定义的选择器 = ∅」在本站会产生 **5 个假 FAIL**（实测 432/432/431/372/372 页）：
        `dp` `p` `st`  → `<span class="badge dp" style="color:…;background:…">`：视觉由**内联 style** 承担；
        `nav-node`     → `.navseq a`（**元素/后代选择器**）已覆盖它；
        `python`       → `pre code` 已覆盖它。
      ⇒ 静态正则**无法**判「某 class 是否被元素/后代选择器或内联样式覆盖」；把它判 FAIL 就是判据对象与断言对象不一致。
      故本判据拆两层：
        hard（可判且有意义）① 空集守卫：`dead_css.new_classes_this_round` 非空；
                              ② 本步**新增**的 class 必须「用到即定义」（防「用了新 class 忘了写样式」）；
        report（只报告）      ③ 族级 `定义 − 使用`（真正的死选择器候选）；
                              ④ 族级 `使用 − 定义`（⛔ 不判 FAIL，理由见上）。
    """
    cfg = (profile.get("dead_css") or {})
    new_classes = set(cfg.get("new_classes_this_round") or [])
    hard, rep = [], []
    if not new_classes:
        hard.append("profile 未声明 dead_css.new_classes_this_round（空集守卫：新增 class 的成对性无从判起）")
    fam_used, fam_defined = {}, {}
    for rel, v in sorted(pages.items()):
        html = SCRIPT_RE.sub("", v["raw"])
        styles = "\n".join(STYLE_RE.findall(v["raw"]))
        used = set()
        for attr in CLASS_ATTR_RE.findall(html):
            used |= {c for c in attr.split() if c}
        defined = set(SEL_CLASS_RE.findall(styles))
        for c in sorted(new_classes & used):
            if c not in defined:
                hard.append("%s 用到了本步新增的 class「%s」但未在该页 <style> 里定义" % (rel, c))
        fam_used.setdefault(v["family"], set()).update(used)
        fam_defined.setdefault(v["family"], set()).update(defined)
    for fam in sorted(fam_used):
        du = sorted(fam_defined.get(fam, set()) - fam_used.get(fam, set()))
        ud = sorted(fam_used.get(fam, set()) - fam_defined.get(fam, set()))
        if du:
            rep.append("族 %s：定义了但全族未用的 class 选择器 %d 个（%s）"
                       % (fam, len(du), ",".join(du[:6])))
        if ud:
            rep.append("族 %s：用到但无同名 class 规则的 %d 个（%s）——⛔ 不判 FAIL（视觉可能由内联 style 或元素/后代选择器承担）"
                       % (fam, len(ud), ",".join(ud[:6])))
    detail = ("；".join(hard[:4]) if hard else
              "本步新增 %d 个 class 在全部使用页上均已定义；族级 report 观察 %d 条（%s）"
              % (len(new_classes), len(rep), "；".join(rep)[:180]))
    return _ok(HARD if hard else REPORT, not hard), detail, HARD if hard else REPORT


def cls_a11y(site_root, profile, pages):
    """类④ 无障碍：SH2 §4.2 —— 每页 skip link ＋ :focus-visible ＋ <main>；静态图形必须有文本等价物。"""
    cfg = (profile.get("a11y") or {})
    need = cfg.get("required") or {}
    js_graphics = cfg.get("js_rendered_graphics") or []
    hard, rep = [], []
    for rel, v in sorted(pages.items()):
        raw = v["raw"]
        if raw.count('class="skip"') != need.get("skip_link", 1):
            hard.append("%s 的 skip link 数 = %d（应 %d）"
                        % (rel, raw.count('class="skip"'), need.get("skip_link", 1)))
        if len(re.findall(r":focus-visible", raw)) < need.get("focus_visible_min", 1):
            hard.append("%s 缺 :focus-visible" % rel)
        if len(re.findall(r"<main(?:\s[^<>]*?)?>", raw)) != need.get("main", 1):
            hard.append("%s 的 <main> 数 = %d（应 %d）"
                        % (rel, len(re.findall(r"<main(?:\s[^<>]*?)?>", raw)), need.get("main", 1)))
        # 静态图形（<svg>/<canvas>）必须有 role="img" ＋ 非空 aria-label
        for m in SVG_RE.finditer(raw):
            tag = m.group(0)
            if 'role="img"' not in tag:
                hard.append("%s 的静态 <%s> 缺 role=\"img\"" % (rel, m.group(1)))
            if not re.search(r'aria-label="[^"]+"', tag):
                hard.append("%s 的静态 <%s> 缺非空 aria-label" % (rel, m.group(1)))
            if cfg.get("require_dom_table_for_static_svg", True) and "<table" not in raw:
                hard.append("%s 有静态图形却无 DOM 文本等价物（<table>）" % rel)
    for g in js_graphics:
        rel = g.get("page")
        if rel in pages:
            rep.append("%s 的 %s 由 JS 在运行期注入（静态 HTML 无图形元素）⇒ 「节点/边 DOM 表格等价物」%s"
                       % (rel, g.get("container"), g.get("note", "未提供")))
    detail = ("；".join(hard[:4]) if hard else
              "全部 %d 页：skip link 恰 1 · :focus-visible ≥1 · <main> 恰 1；静态图形的 role=img/aria-label/DOM 表齐备"
              % len(pages))
    if rep and not hard:
        detail += "；report 观察 %d 条：%s" % (len(rep), rep[0][:110])
    return _ok(HARD if hard else REPORT, not hard), detail, HARD if hard else REPORT


def cls_responsive(site_root, profile, pages):
    """类⑤ 响应式：★ 本机无浏览器 ⇒ 渲染档（四视口 scrollWidth）**未测**；此处是**静态替代判据**。

    hard 断言（判据对象与断言对象一致的那部分）：
      ① 每页有 `<meta name="viewport">`（缺它则窄视口必然按 980px 排版 ⇒ 溢出是必然的）
      ② 站点级存在 ≥1 个 `@media (max|min)-width` 断点（空集守卫：一个断点都没有 ⇒ 门控致盲）
      ③ profile 声明的「固定布局页」必须有自己的窄视口断点（本站＝交互页 `#side` 固定 300px）
    report 观察：无断点的页面清单 —— ★ 这**不是** FAIL：本站多数页面用
      `grid-template-columns:repeat(auto-fill,minmax(...))` 的**内在响应式**，不依赖断点；
      把「无断点」判 FAIL 属判据对象与断言对象不一致（SH5 §4.0 第 1 条）。
    """
    cfg = (profile.get("responsive") or {})
    fixed_pages = cfg.get("fixed_layout_pages") or []
    hard, no_bp = [], []
    bp_site = 0
    for rel, v in sorted(pages.items()):
        if not VIEWPORT_RE.search(v["raw"]):
            hard.append("%s 缺 <meta name=\"viewport\">" % rel)
        styles = "\n".join(STYLE_RE.findall(v["raw"]))
        if MEDIA_BP_RE.search(styles):
            bp_site += 1
        else:
            no_bp.append(rel)
    if bp_site == 0:
        hard.append("站点级 0 个 `@media (max|min)-width` 断点（空集守卫：判据致盲）")
    for rel in fixed_pages:
        if rel in pages:
            styles = "\n".join(STYLE_RE.findall(pages[rel]["raw"]))
            if not MEDIA_BP_RE.search(styles):
                hard.append("声明的固定布局页 %s 无窄视口断点" % rel)
    detail = ("；".join(hard[:4]) if hard else
              "全部 %d 页有 viewport 声明；站点级断点页 %d 个；声明的固定布局页 %d 个均含断点"
              % (len(pages), bp_site, len(fixed_pages)))
    if no_bp and not hard:
        detail += "；report 观察：无断点页 %d 个（内在响应式布局，⛔ 不判 FAIL）：%s%s" % (
            len(no_bp), ", ".join(no_bp[:3]), " …" if len(no_bp) > 3 else "")
    return _ok(HARD if hard else REPORT, not hard), detail, HARD if hard else REPORT


def cls_metadata(site_root, profile, pages):
    """类⑥ 元数据：SH4 §4.2。★ 拆成两层（⛔ 不把「缺 description」判成阻断级）：

    hard 断言（本站**已经**成立的部分）：每页 `<html lang>` 非空；`<title>` 非空且含站点名。
    report 观察（本站**全缺**、属 SH4 标准档的改动面，⛔ 本批按任务书不实施）：
      `description` / `og:*` / `canonical` / `favicon` / `sitemap.xml` / `robots.txt`。
    """
    cfg = (profile.get("metadata") or {})
    site_name = cfg.get("title_must_contain") or "算法知识图谱"
    hard, rep = [], []
    miss_desc = miss_og = miss_canon = miss_icon = 0
    for rel, v in sorted(pages.items()):
        raw = v["raw"]
        m = LANG_RE.search(raw)
        if not m or not m.group(1).strip():
            hard.append("%s 缺非空 <html lang>" % rel)
        t = TITLE_RE.search(raw)
        if not t or not t.group(1).strip():
            hard.append("%s 缺非空 <title>" % rel)
        elif site_name not in t.group(1):
            hard.append("%s 的 <title> 不含站点名「%s」" % (rel, site_name))
        miss_desc += 0 if DESC_RE.search(raw) else 1
        miss_og += 0 if OG_RE.search(raw) else 1
        miss_canon += 0 if CANON_RE.search(raw) else 1
        miss_icon += 0 if ICON_RE.search(raw) else 1
    for name, cnt in (("description", miss_desc), ("og:*", miss_og),
                      ("canonical", miss_canon), ("favicon", miss_icon)):
        if cnt:
            rep.append("缺 %s 的页 %d / %d" % (name, cnt, len(pages)))
    for f, label in (("sitemap.xml", "sitemap.xml"), ("robots.txt", "robots.txt")):
        if not os.path.isfile(os.path.join(site_root, f)):
            rep.append("仓内无 %s" % label)
    detail = ("；".join(hard[:4]) if hard else
              "全部 %d 页有 <html lang> 且 <title> 非空并含站点名" % len(pages))
    if rep and not hard:
        detail += "；report 观察 %d 条（SH4 标准档改动面，⛔ 本批不实施）：%s" % (len(rep), "；".join(rep))
    return _ok(HARD if hard else REPORT, not hard), detail, HARD if hard else REPORT


# --------------------------------------------------------------------------- 六类伞
def judge_design(ctx, restrict=None):
    site_root, contract, profile = ctx["site_root"], ctx["contract"], ctx["profile"]
    pages = pages_with(site_root, profile, only=restrict)
    R = []

    def add(cid, name, status, detail, klass):
        R.append((cid, name, status, detail, klass))

    # ---- D1 空集守卫（blind）
    reasons = []
    if not pages:
        reasons.append("扫描面 0 页（page_families glob 未命中任何文件）")
    if not (profile.get("page_families") or []):
        reasons.append("profile 未声明 page_families")
    if not (contract.get("usage_tiers") or {}):
        reasons.append("值件未声明 usage_tiers（类①的阈值无从谈起）")
    add("D1", "六类齐全 ＋ 判据对象非空（空集守卫）",
        "FAIL" if reasons else "PASS",
        "；".join(reasons) if reasons else
        "六类：%s；扫描 %d 页" % (" · ".join(c[0] for c in CLASS_TABLE), len(pages)), BLIND)

    # ---- D2/D3 类①②：转发 gate_tokens（同一实现）
    token_judges = {r[0]: r for r in GT.judge({"site_root": site_root, "contract": contract,
                                               "profile": profile, "pages": pages})}
    for cid, want, label in (("D2", ["T6"], "类① 对比度（转发 gate_tokens.T6，⛔ 不造第二套）"),
                             ("D3", ["T2", "T3", "T4"], "类② 令牌唯一值（转发 gate_tokens.T2/T3/T4）")):
        subs = [token_judges[t] for t in want if t in token_judges]
        bad = [s for s in subs if s[2] == "FAIL"]
        status = "PASS" if subs and not bad else ("FAIL" if bad else "REPORT")
        add(cid, label, status,
            "；".join("%s=%s" % (s[0], s[2]) for s in subs) + " — " +
            (bad[0][3][:150] if bad else (subs[0][3][:150] if subs else "子判据缺失")),
            HARD if bad else REPORT)

    # ---- D4–D7 类③–⑥
    for cid, fn, label in (("D4", cls_dead_css, "类③ 死 CSS（本步新增的 class 必须「用到即定义」；两向差集只作 report 观察）"),
                           ("D5", cls_a11y, "类④ 无障碍（skip link / :focus-visible / <main> / 图形文本等价物）"),
                           ("D6", cls_responsive, "类⑤ 响应式（★ 静态替代判据；渲染档未测）"),
                           ("D7", cls_metadata, "类⑥ 元数据（lang/title 为 hard；description/og/canonical/favicon/sitemap 为 report 观察）")):
        status, detail, klass = fn(site_root, profile, pages)
        add(cid, label, status, detail, klass)

    # ---- D8 变更面增量档（★ 变更集为空 ⇒ SKIP，⛔ 不是 PASS）
    base_path = os.path.join(site_root, (profile.get("gate_report") or {}).get(
        "baseline", "build/gate-baseline.json"))
    if not os.path.isfile(base_path):
        add("D8", "变更面增量档（变更集为空 ⇒ SKIP）", "SKIP",
            "SKIP：无基线（%s 不存在）⇒ 本档未跑；⛔ 不得读作 PASS" % os.path.basename(base_path), SKIP)
    else:
        base = json.load(open(base_path, encoding="utf-8"))
        digest, files = GT.tree_digest(site_root)
        old = base.get("files") or {}
        changed = sorted(k for k in set(old) | set(files) if old.get(k) != files.get(k))
        if not changed:
            add("D8", "变更面增量档（变更集为空 ⇒ SKIP）", "SKIP",
                "SKIP：变更集为空（tree_digest=%s）⇒ 全量判据已由 D2–D7 承担；⛔ 不得读作 PASS"
                % digest[:16], SKIP)
        else:
            sub = GT.judge({"site_root": site_root, "contract": contract, "profile": profile,
                            "pages": pages_with(site_root, profile, only=set(changed))})
            # ★ 排除**集合/站点级**判据：它们的判据对象是「全站」，在只含变更页的子集上跑必然假 FAIL
            #   （T1 空集守卫 · T7 零引用令牌登记表 · T11 覆盖完备性 · T12 形态计数）。
            #   ⇒ 这四条只在全量静态档（D2–D7）里判，⛔ 不在增量档重判。
            sub = [s for s in sub if s[0] not in ("T1", "T7", "T11", "T12")]
            bad = [s for s in sub if s[2] == "FAIL"]
            add("D8", "变更面增量档（变更集为空 ⇒ SKIP）",
                "FAIL" if bad else "PASS",
                "变更 %d 个文件（%s%s）；对变更页跑 %d 条判据，%d FAIL%s"
                % (len(changed), ", ".join(changed[:3]), " …" if len(changed) > 3 else "",
                   len(sub), len(bad), ("：" + bad[0][3][:140]) if bad else ""),
                HARD if bad else SKIP)

    # ---- D9 渲染抽样档（★ 本机无浏览器 ⇒ 未测；静态抽样照跑）
    rs = profile.get("render_sample") or {}
    sample = [p for p in (rs.get("pages") or []) if p in pages]
    static_bad = []
    for cid, fn in (("dead-css", cls_dead_css), ("a11y", cls_a11y),
                    ("responsive", cls_responsive), ("metadata", cls_metadata)):
        st, _d, _k = fn(site_root, profile, {k: pages[k] for k in sample})
        if st == "FAIL":
            static_bad.append(cid)
    add("D9", "渲染抽样档（12 页 × 4 视口；★ 本机无浏览器 ⇒ 渲染面未测）", "SKIP",
        "SKIP：渲染档**未测**（%s）；静态抽样 %d/%d 页已跑四类静态判据，FAIL 类：%s"
        % (rs.get("mode_reason", "本机 agent-browser 不在 PATH"), len(sample),
           len(rs.get("pages") or []), static_bad or "无"), SKIP)
    return R


# --------------------------------------------------------------------------- 主流程
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site-root", default=".")
    ap.add_argument("--contract", default=None)
    ap.add_argument("--profile", default=None)
    ap.add_argument("--manifest", default=None)
    ap.add_argument("--mode", choices=["report", "enforce"], default=None)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--report-out", default=None)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()

    site_root = os.path.abspath(a.site_root)
    contract_path = a.contract or os.path.join(site_root, "vendor/pipeline/values/algorithm-knowledge-graph.json")
    profile_path = a.profile or os.path.join(site_root, "build/profile.json")
    if a.manifest and not os.path.isfile(os.path.join(site_root, a.manifest)):
        print("GUARD-REJECT: 清单不存在：%s" % a.manifest)
        return 3
    try:
        contract = GT.load_json(contract_path, "值件")
        profile = GT.load_json(profile_path, "profile")
    except (GT.GateError, GT.D.GuardError) as exc:
        print("GUARD-REJECT: %s" % exc)
        return 3

    R = judge_design({"site_root": site_root, "contract": contract, "profile": profile})
    mode = a.mode or (profile.get("gates", {}) or {}).get("mode_now") or "report"
    for cid, name, status, detail, klass in R:
        print("[%s] %s %s（%s）— %s" % (status, cid, name, klass, detail))
    counts = {"judges": len(R),
              "pass": sum(1 for r in R if r[2] == "PASS"),
              "fail": sum(1 for r in R if r[2] == "FAIL"),
              "report": sum(1 for r in R if r[2] == "REPORT"),
              "skip": sum(1 for r in R if r[2] == "SKIP")}
    print("\n=== 六类设计门控（mode=%s）：%d 项判据 · PASS %d / FAIL %d / REPORT %d / SKIP %d ==="
          % (mode, counts["judges"], counts["pass"], counts["fail"], counts["report"], counts["skip"]))

    if a.report_out:
        digest, _files = GT.tree_digest(site_root)
        doc = {"gate": "gate_design.py",
               "site": contract.get("scope", {}).get("site"),
               "mode": mode,
               "tree_digest": digest,
               "classes_covered": [c[0] for c in CLASS_TABLE],
               "class_table": [{"id": c, "name": n, "object": o, "threshold": t} for c, n, o, t in CLASS_TABLE],
               "counts": counts,
               "judges": [{"id": c, "name": n, "class": k, "status": s, "detail": d}
                          for c, n, s, d, k in R],
               "not_covered": GT.NOT_COVERED}
        GT.write_report(a.report_out, "gate_design.py", doc)
        print("报告已并入：%s（gate=gate_design.py）" % a.report_out)
    if a.json:
        print(json.dumps([{"id": c, "status": s, "class": k} for c, n, s, d, k in R],
                         ensure_ascii=False, indent=1))

    blind_fail = [r for r in R if r[4] == BLIND and r[2] == "FAIL"]
    hard_fail = [r for r in R if r[4] == HARD and r[2] == "FAIL"]
    if blind_fail:
        print("阻断：blind 类判据 FAIL（门控致盲，报告模式也不宽恕）")
        return 1
    if mode == "enforce" and hard_fail:
        print("阻断：enforce 模式下 hard 类判据 FAIL")
        return 1
    if hard_fail or [r for r in R if r[2] == "REPORT"]:
        print("报告模式：上述 FAIL/REPORT 已记基线，不阻断")
    return 0


# --------------------------------------------------------------------------- selftest
def _fixture(tmp):
    """构造一个最小站点：1 个外链族页 ＋ 1 个内联页 ＋ 未覆盖页 ＋ 基线。"""
    import shutil
    import tempfile
    root = tempfile.mkdtemp(prefix="akgdesign-")
    for d in ("g", "assets", "07-checkpoint", "vendor/pipeline", "vendor/tools", "build"):
        os.makedirs(os.path.join(root, d), exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "vendor", "pipeline", "derive_site_tokens.py"),
                    os.path.join(root, "vendor", "pipeline", "derive_site_tokens.py"))
    shutil.copyfile(os.path.join(HERE, "vendor", "tools", "contrast.py"),
                    os.path.join(root, "vendor", "tools", "contrast.py"))
    shutil.copyfile(os.path.join(HERE, "gate_tokens.py"), os.path.join(root, "gate_tokens.py"))
    c = json.loads(json.dumps(FIX_C))
    p = json.loads(json.dumps(FIX_P))
    json.dump(c, open(os.path.join(root, "contract.json"), "w", encoding="utf-8"), ensure_ascii=False)
    json.dump(p, open(os.path.join(root, "build", "profile.json"), "w", encoding="utf-8"), ensure_ascii=False)
    open(os.path.join(root, "assets", "tokens.css"), "w", encoding="utf-8").write(FIX_BLOCK + "\n")
    open(os.path.join(root, "g", "a.html"), "w", encoding="utf-8").write(FIX_EXT)
    open(os.path.join(root, "index.html"), "w", encoding="utf-8").write(FIX_INL)
    open(os.path.join(root, "report.html"), "w", encoding="utf-8").write(
        "<!DOCTYPE html><html><body>uncovered</body></html>\n")
    open(os.path.join(root, "07-checkpoint", "gen.py"), "w", encoding="utf-8").write(
        "#!/usr/bin/env python3\nimport json\nimport os\nimport sys\n"
        "sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'vendor', 'pipeline'))\n"
        "import derive_site_tokens as D\nROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n\n\n"
        "def root_tokens(family='default'):\n"
        "    c = json.load(open(os.path.join(ROOT, 'contract.json'), encoding='utf-8'))\n"
        "    p = json.load(open(os.path.join(ROOT, 'build', 'profile.json'), encoding='utf-8'))\n"
        "    return D.render(D.build_tokens(c, p, family)[1])\n")
    return root


FIX_BLOCK = (":root{--text:#e6e8ee;--border:#6b7280;--border-subtle:#2a2f3a;--bg:#0f1117;"
             "--ok:#2fb98a;--warn:#e8933b;}")
FIX_USES = ("a{color:var(--text);outline-color:var(--border);border-color:var(--border-subtle);"
            "background:var(--bg);}b{color:var(--ok);}i{color:var(--warn);}"
            ".skip{position:absolute;left:-9999px;}")
FIX_EXT = ('<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">'
           '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
           '<title>夹具 · 算法知识图谱</title>'
           '<link rel="stylesheet" href="../assets/tokens.css">'
           '<style>.c{color:red;}:focus-visible{outline:1px solid var(--border);}'
           '@media (max-width:720px){.c{color:blue;}}' + FIX_USES + '</style></head>'
           '<body><a class="skip" href="#main">跳到主要内容</a><main id="main">'
           '<span class="c">x</span></main></body></html>\n')
FIX_INDEX_BLOCK = (":root{--text:#e6e8ee;--border:#6b7280;--border-subtle:#2a2f3a;--bg:#0f1117;"
                   "--ok:#2fb98a;}")
FIX_INL = ('<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">'
           '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
           '<title>夹具首页 · 算法知识图谱</title><style>' + FIX_INDEX_BLOCK +
           '.c{color:red;}:focus-visible{outline:1px solid var(--border);}'
           '@media (max-width:720px){.c{color:blue;}}' + FIX_USES + '</style></head>'
           '<body><a class="skip" href="#main">跳到主要内容</a><main id="main">'
           '<span class="c">x</span><svg role="img" aria-label="分布矩阵"></svg>'
           '<table><tr><td>等价文本</td></tr></table></main></body></html>\n')
FIX_C = {
    "meta": {"id": "t", "contract_version": "0", "frozen_at": "2026-10-13", "title": "t"},
    "scope": {"site": "t", "upstream_repo_head": "0" * 40, "declared_forms": ["dark"]},
    "usage_tiers": {
        "body": {"allowed_use": "x", "min_contrast": {"dark": 4.5}, "gate": "hard"},
        "non-text": {"allowed_use": "x", "min_contrast": {"dark": 3.0}, "gate": "hard"},
        "non-text-decorative": {"allowed_use": "x", "min_contrast": {"dark": 3.0}, "gate": "report-only"},
    },
    "roles": {
        "text.primary": {"tier": "body", "kind": "text", "purpose": "p", "site_source": "s"},
        "border.line": {"tier": "non-text", "kind": "border", "purpose": "p", "site_source": "s"},
        "border.subtle": {"tier": "non-text-decorative", "kind": "border", "purpose": "p", "site_source": "s"},
        "surface.page": {"tier": "non-text", "kind": "surface", "purpose": "p", "site_source": "s"},
        "ok": {"tier": "body", "kind": "semantic-text", "purpose": "p", "site_source": "s"},
    },
    "palettes": {"p": {"family": "f", "provenance": "x", "values": {
        "text.primary": {"dark": "#e6e8ee"}, "border.line": {"dark": "#6b7280"},
        "border.subtle": {"dark": "#2a2f3a"}, "surface.page": {"dark": "#0f1117"},
        "ok": {"dark": "#2fb98a"}}}},
    "binding": {"site_token_names": {"text.primary": "--text", "border.line": "--border",
                                     "border.subtle": "--border-subtle", "surface.page": "--bg",
                                     "ok": "--ok"},
                "override_tiers": {"--warn": "body"}, "passthrough_tokens": {}},
    "families": {"default": {"targets": ["assets/tokens.css"], "overrides": {"--warn": "#e8933b"}},
                 "index": {"targets": ["index.html"], "overrides": {}}},
    "derivation": {"state": "s", "direction": "d", "generator_ref": "g", "rule": "r"},
    "dead_tokens": {"site_level_zero_ref": [], "page_level_unused": []},
}
FIX_P = {
    "site": "t", "form": "mixed", "publish_dir": ".", "value_file": "contract.json",
    "targets": [{"path": "assets/tokens.css", "mode": "whole-file", "family": "default"},
                {"path": "index.html", "mode": "root-block", "family": "index"}],
    "page_families": [{"glob": "g/*.html", "family": "default", "delivery": "external",
                       "stylesheet": "../assets/tokens.css"},
                      {"glob": "index.html", "family": "index", "delivery": "inline"}],
    "uncovered_pages": [{"path": "report.html", "reason": "夹具"}],
    "link_surface": {"artifact": "assets/tokens.css", "expected_pages": 1},
    "inline_surface": {"expected_pages": 1},
    "single_source_invariants": {"value_file": "contract.json",
                                 "literal_free_generators": ["07-checkpoint/gen.py"]},
    "a11y": {"required": {"skip_link": 1, "focus_visible_min": 1, "main": 1},
             "require_dom_table_for_static_svg": True, "js_rendered_graphics": []},
    "dead_css": {"new_classes_this_round": ["c", "skip"]},
    "responsive": {"fixed_layout_pages": []},
    "metadata": {"title_must_contain": "算法知识图谱"},
    "gate_report": {"baseline": "build/gate-baseline.json"},
    "render_sample": {"pages": ["index.html", "g/a.html"], "viewports": [[375, 812]],
                      "mode": "static-only", "mode_reason": "夹具：无浏览器"},
    "gates": {"manifest": "gate-manifest.json", "mode_now": "report"},
}


def _run_design(mutate=None, with_baseline=False):
    root = _fixture(None)
    if with_baseline:
        digest, files = GT.tree_digest(root)
        json.dump({"schema": "site-gate-baseline/1", "tree_digest": digest, "files": files},
                  open(os.path.join(root, "build", "gate-baseline.json"), "w", encoding="utf-8"))
    if mutate:
        mutate(root)
    c = json.load(open(os.path.join(root, "contract.json"), encoding="utf-8"))
    p = json.load(open(os.path.join(root, "build", "profile.json"), encoding="utf-8"))
    return judge_design({"site_root": root, "contract": c, "profile": p}), root


def selftest():
    cases = []

    def case(name, cid, mutate, expect, with_baseline=False):
        try:
            R, _root = _run_design(mutate, with_baseline)
        except Exception as exc:  # noqa: BLE001
            cases.append((name, False, "异常：%s" % exc))
            return
        got = {r[0]: r[2] for r in R}
        cases.append((name, got.get(cid) == expect, ""))

    def edit(name, fn):
        def _m(root):
            fp = os.path.join(root, name)
            s = open(fp, encoding="utf-8").read()
            open(fp, "w", encoding="utf-8").write(fn(s))
        return _m

    def addf(name, text):
        def _m(root):
            open(os.path.join(root, name), "w", encoding="utf-8").write(text)
        return _m

    def setp(fn):
        def _m(root):
            fp = os.path.join(root, "build", "profile.json")
            p = json.load(open(fp, encoding="utf-8"))
            fn(p)
            json.dump(p, open(fp, "w", encoding="utf-8"), ensure_ascii=False)
        return _m

    # 正向：夹具上 D1–D7 全部 PASS，D8/D9 为 SKIP（无基线 / 渲染未测）
    R0, _r0 = _run_design()
    cases.append(("正向夹具：D1–D7 全 PASS，D8/D9 全 SKIP（⛔ 判据非恒真、⛔ SKIP 不得读作 PASS）",
                  all(r[2] == "PASS" for r in R0 if r[0] in ("D1", "D2", "D3", "D4", "D5", "D6", "D7"))
                  and all(r[2] == "SKIP" for r in R0 if r[0] in ("D8", "D9")),
                  "；".join("%s=%s" % (r[0], r[2]) for r in R0)))

    # D1 空集守卫
    case("D1 负例：扫描面 0 页（glob 未命中）⇒ FAIL（空集守卫）",
         "D1", setp(lambda p: p.__setitem__("page_families", [{"glob": "nope/*.html", "family": "default"}])),
         "FAIL")
    # D4 死 CSS
    case("D4 负例：本步新增的 class 被用到但未定义",
         "D4", edit("g/a.html", lambda s: s.replace(".c{color:red;}", "")
                    .replace("@media (max-width:720px){.c{color:blue;}}",
                             "@media (max-width:720px){.d{color:blue;}}")), "FAIL")
    case("D4 假阳样本：**非**本步新增的 class 无同名规则 **不得** FAIL（视觉可能由内联 style 或元素选择器承担）",
         "D4", edit("g/a.html", lambda s: s.replace('<span class="c">', '<span class="c legacy">')), "PASS")
    case("D4 空集守卫：profile 未声明 new_classes_this_round ⇒ FAIL",
         "D4", setp(lambda p: p.__setitem__("dead_css", {})), "FAIL")
    # D5 无障碍
    case("D5 负例：删掉 skip link", "D5",
         edit("g/a.html", lambda s: s.replace('<a class="skip" href="#main">跳到主要内容</a>', "")), "FAIL")
    case("D5 负例：删掉 :focus-visible", "D5",
         edit("g/a.html", lambda s: s.replace(":focus-visible{outline:1px solid var(--border);}", "")), "FAIL")
    case("D5 负例：<main> 数 ≠ 1", "D5",
         edit("g/a.html", lambda s: s.replace("<main id=\"main\">", "<div id=\"main\">")
              .replace("</main>", "</div>")), "FAIL")
    case("D5 负例：静态 SVG 缺 role=img", "D5",
         edit("index.html", lambda s: s.replace('role="img" ', "")), "FAIL")
    case("D5 负例：静态 SVG 有 role=img 但无 DOM 文本等价物", "D5",
         edit("index.html", lambda s: s.replace("<table><tr><td>等价文本</td></tr></table>", "")), "FAIL")
    # D6 响应式
    case("D6 负例：删掉 viewport 声明", "D6",
         edit("g/a.html", lambda s: s.replace(
             '<meta name="viewport" content="width=device-width, initial-scale=1.0">', "")), "FAIL")
    case("D6 负例：站点级 0 个断点（空集守卫）", "D6",
         lambda root: [edit("g/a.html", lambda s: s.replace(
             "@media (max-width:720px){.c{color:blue;}}", ""))(root),
             edit("index.html", lambda s: s.replace(
                 "@media (max-width:720px){.c{color:blue;}}", ""))(root)], "FAIL")
    case("D6 假阳样本：个别页无断点但用内在响应式布局 **不得** FAIL（只 REPORT 观察）", "D6",
         edit("index.html", lambda s: s.replace(
             "@media (max-width:720px){.c{color:blue;}}", "")), "PASS")
    # D7 元数据
    case("D7 负例：<title> 不含站点名", "D7",
         edit("g/a.html", lambda s: s.replace("<title>夹具 · 算法知识图谱</title>", "<title>夹具</title>")), "FAIL")
    case("D7 负例：缺 <html lang>", "D7",
         edit("g/a.html", lambda s: s.replace('<html lang="zh-CN">', "<html>")), "FAIL")
    # D8 变更面增量
    case("D8 变更集为空 ⇒ SKIP（⛔ 不是 PASS）", "D8", None, "SKIP", with_baseline=True)
    case("D8 变更集非空且变更页有问题 ⇒ FAIL",
         "D8", lambda root: edit("index.html", lambda s: s.replace(
             "--text:#e6e8ee", "--text:#101010"))(root), "FAIL", with_baseline=True)
    case("D8 变更集非空但变更页无问题 ⇒ PASS",
         "D8", lambda root: edit("report.html", lambda s: s.replace("uncovered", "uncovered!")) (root),
         "PASS", with_baseline=True)
    # D9 渲染抽样
    case("D9 渲染抽样档：本机无浏览器 ⇒ SKIP（⛔ 不得假称渲染实测）", "D9", None, "SKIP")
    case("D9 负例：抽样页有 FAIL 类 ⇒ 仍在 detail 里点名（状态仍 SKIP）", "D9",
         edit("g/a.html", lambda s: s.replace(".c{color:red;}", "")
              .replace("@media (max-width:720px){.c{color:blue;}}",
                       "@media (max-width:720px){.d{color:blue;}}")), "SKIP")

    ok = all(v for _, v, _ in cases)
    for name, res, note in cases:
        print("  [%s] %s%s" % ("PASS" if res else "FAIL", name, ("  ← " + note) if note else ""))
    print("\n=== gate_design.py 自检：%d 项，%d FAIL ===" % (len(cases), sum(1 for _, v, _ in cases if not v)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
