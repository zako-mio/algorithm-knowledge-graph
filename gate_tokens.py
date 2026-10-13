#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gate_tokens.py — algorithm-knowledge-graph 的**站点侧令牌门控**（批 H 标准档新建）。

范式与纪律来源：`solutions/_shared/SH5-gating.md` §4.0 十条；落点见本文件末尾的判据表。
形状来源：批 E 在 `12-factor-methodology-kg` 立的先例（门控放**站点仓根** ＋ `gate-manifest.json`
＋ `build/profile.json` ＋ `vendor/pipeline/**` 薄副本，逐文件 sha256 登记）。
⛔ 本站**不照抄**别站语义：本站是「**一站两形态**」（375 内联页 ＋ 63 外链页），
   故判据必须**分别**断言两种形态（T11/T12）。

用法：
    python3 gate_tokens.py --site-root . --manifest gate-manifest.json
    python3 gate_tokens.py --site-root . --mode enforce
    python3 gate_tokens.py --site-root . --json
    python3 gate_tokens.py --site-root . --baseline-out build/gate-baseline.json
    python3 gate_tokens.py --selftest

执行强度：
    `--mode report`（默认）——判据全跑、逐条打印；**hard 类 FAIL 不阻断**（首轮记基线）。
    `--mode enforce` —— 任一 hard 类 FAIL 即 exit 1。
    ★ blind 类（T1/T11 空集与覆盖守卫）**不随报告模式放宽**：它们守的是「门控自己是否致盲」，
      不是站点缺陷；致盲时报告模式也 exit 1 —— 否则「报告模式全绿」会是假绿。

判据状态词表（★ 四态，⛔ 不是二值）：
    PASS    判据成立
    FAIL    判据不成立且**该判据属阻断类**（blind / hard）
    REPORT  判据不成立但**该判据属 report-only 档**（只报告，不阻断；SH5 §4.0 第 10 条）
    SKIP    判据**不适用/未跑**（⛔ 必须带原因，⛔ 不得读作 PASS）

判据（12 条，逐条声明判据对象；⛔ 无豁免字段、⛔ 不静默跳过）：
  T1  [blind]  空集守卫：扫描面 0 页 / 0 族 / 0 令牌名 / 内联页一个 `:root` 都没有 ⇒ FAIL
  T2  [hard]   族内唯一值：同一族内同名令牌必须同值（⛔ **不**判「全站唯一值」——本站合法存在 --warn 两值）
  T3  [hard]   派生一致性：内联页首个 `:root` == 值件对该族的派生；外链页的 `<link>` 目标 == 该族派生
  T4  [hard]   跨族差异逐族登记：全站同名令牌出现的**每一个**取值，都必须能被某个族的派生解释
  T5  [hard]   border 分档极性：强分隔（--border）对比度必须 > 弱分隔（--border-subtle）
  T6  [混合]   成对对比度：每个色角色令牌与每个覆盖令牌对 surface.page，阈值与门档取自 usage_tiers / override_tiers
  T7  [混合]   零引用令牌登记：站点级零引用（hard）与**内联页**页级未用（report）都必须逐枚登记，且登记不得过期
  T8  [hard]   生成器单源不变量：三个生成器不得持令牌字面值，且必须从同一份值件真跑出令牌块
  T9  [hard]   未声明令牌：盘上出现值件未声明的令牌名 ⇒ FAIL（防「悄悄加令牌」）
  T10 [hard]   目标存在性：profile 声明的每个写入目标必须存在
  T11 [blind]  覆盖完备性：**全仓 HTML = 扫描面 ∪ 已声明未覆盖**，且两集不交、未覆盖项存在
  T12 [hard]   形态分别断言：63 个外链页**有且仅有 1 个 `rel="stylesheet"` 的 `<link>`**（指向
               `assets/tokens.css`、相对路径、`.css` 扩展名、目标可达）、无内联 `:root`；
               375 个内联页**零外链样式**、且自有 `:root` 与派生一致（T3 的另一侧）

退出码：0 全过（或报告模式且有 hard/report 类 FAIL 但无 blind FAIL）/ 1 有阻断级 FAIL / 2 输入错误 / 3 护栏拒读
"""
import argparse
import glob
import hashlib
import importlib.util
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
VENDOR = os.path.join(HERE, "vendor", "pipeline")
for _p in (VENDOR, os.path.join(HERE, "vendor", "tools")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import derive_site_tokens as D  # noqa: E402  ★ 复用派生器的块定位/归一化/三级覆盖（⛔ 不造第二套）
import contrast as C            # noqa: E402  ★ 复用对比度实现（经 vendor/tools/）

VAR_RE = re.compile(r"var\(\s*(--[A-Za-z0-9_-]+)")
LITERAL_RE = re.compile(r"--[A-Za-z0-9_-]+\s*:\s*#[0-9a-fA-F]{3,8}")
LINK_RE = re.compile(r"<link\b[^>]*>", re.I)
# ★ 批 J 新增：只匹配 **stylesheet** 类的 <link>（T12 口径重述的落点，见下方 T12 注释）。
STYLESHEET_LINK_RE = re.compile(r"<link\b[^>]*\brel\s*=\s*[\"']stylesheet[\"'][^>]*>", re.I)
MAIN_RE = re.compile(r"<main(?:\s[^<>]*?)?>", re.I)
SKIP_LINK_RE = re.compile(r'class="skip"', re.I)
FOCUS_RE = re.compile(r":focus-visible")

BLIND, HARD, REPORT, SKIP = "blind", "hard", "report", "skip"
SKIP_DIRS = {".git", "vendor", "node_modules", "__pycache__"}

NOT_COVERED = [
    "★ 外链页的 **HTTP 可达性**未实测（`curl` 200 / `content-type: text/css`）：本机不联网、不起本地 HTTP 服务 ⇒ "
    "T12 只做到「相对路径 ＋ `.css` 扩展名 ＋ 目标文件在仓内存在 ＋ 该页无内联 :root」的**等价静态断言**。"
    "⛔ 不得读作「已验 HTTP 200」。",
    "★ **像素层视觉回归未测**（本机 `agent-browser` 不在 PATH）⇒ 六类门控的渲染档（四视口 scrollWidth / 焦点可见几何）只做到静态判据层。",
    "★ **四类非令牌门控的执行强度是 report_only**：`site-profile.schema.json` 的 `hard_blocking` 枚举只有四项 ⇒ 死 CSS / 无障碍 / 响应式 / 元数据只能进 report_only（扩枚举＝改 schema，须走独立决策）。",
    "★ **JS 动态加的 class 与伪类语义未纳入死 CSS 判据**（只判静态 HTML 里出现的 class）。",
    "★ **运行期由 JS 拼出的 var() 引用未形式化证明**（本站 JS 不拼 CSS 变量，但未证明）。",
    "★ **`report.html` 未覆盖**（Q4-A）：其生成器 `gen-report-html.py` 的输出目标是仓外绝对路径 ⇒ 仓内那份无生成器可复现。",
]


class GateError(Exception):
    """护栏拒读（exit 3）——输入缺失/非法，⛔ 不静默降级为「跳过」。"""


def load_json(path, label):
    if not os.path.isfile(path):
        raise GateError("%s 不存在：%s" % (label, path))
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception as exc:  # noqa: BLE001
        raise GateError("%s 非法 JSON：%s" % (label, exc))


def _strip_py_comments(src):
    """剥掉 Python **行注释**（⛔ 不碰字符串字面量）。

    ★ 为什么要剥：T8 判「生成器是否仍持令牌字面值」，若把说明性注释里的 `:root{…}` 字样
      当成事实就会**假阳**（批 E 在 12-factor 实测踩到过一次）。
    """
    out, q = [], None
    for line in src.split("\n"):
        cut = len(line)
        for i, ch in enumerate(line):
            if q:
                if ch == q:
                    q = None
            elif ch in "\"'":
                q = ch
            elif ch == "#":
                cut = i
                break
        out.append(line[:cut])
    return "\n".join(out)


# --------------------------------------------------------------------------- 采集
def collect_pages(site_root, profile):
    """按 profile.page_families 的 glob 规则采集页面 → {rel: {...}}（含交付形态）。"""
    out = {}
    for rule in profile.get("page_families") or []:
        for absp in sorted(glob.glob(os.path.join(site_root, rule["glob"]), recursive=True)):
            if not os.path.isfile(absp):
                continue
            rel = os.path.relpath(absp, site_root).replace(os.sep, "/")
            raw = open(absp, encoding="utf-8", errors="replace").read()
            blk = D.extract_block(raw)
            out[rel] = {"family": rule["family"], "delivery": rule.get("delivery", "inline"),
                        "stylesheet": rule.get("stylesheet"), "raw": raw, "block": blk,
                        "tokens": D.parse_tokens(blk) if blk else {}}
    return out


def all_repo_html(site_root):
    """全仓 HTML（排除 vendor/ 与点目录）——T11 的「全集」。"""
    out = set()
    for dp, dn, fn in os.walk(site_root):
        dn[:] = [d for d in dn if d not in SKIP_DIRS and not d.startswith(".")]
        for f in fn:
            if f.endswith(".html"):
                out.add(os.path.relpath(os.path.join(dp, f), site_root).replace(os.sep, "/"))
    return out


def declared_token_names(contract):
    """值件声明的全部令牌名 = 角色绑定 ∪ 各族 overrides ∪ 透传。"""
    names = set((contract.get("binding") or {}).get("site_token_names", {}).values())
    for spec in (contract.get("families") or {}).values():
        names |= set((spec.get("overrides") or {}).keys())
    for _g, kv in ((contract.get("binding") or {}).get("passthrough_tokens") or {}).items():
        if isinstance(kv, dict):
            names |= {k for k in kv if str(k).startswith("--")}
    return names


def family_expected(contract, profile, fam):
    """复用派生器的三级覆盖（P1–P7 护栏在内）→ 该族的期望令牌表。"""
    _fid, tokens = D.build_tokens(contract, profile, fam)
    return tokens


def _import_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --------------------------------------------------------------------------- 判据
def judge(ctx):
    """跑全部判据，返回 [(id, 名称, status, detail, class)]。"""
    R = []
    site_root = ctx["site_root"]
    contract = ctx["contract"]
    profile = ctx["profile"]
    pages = ctx["pages"]
    fams = list((contract.get("families") or {}).keys())
    names = (contract.get("binding") or {}).get("site_token_names", {})
    override_tiers = ((contract.get("binding") or {}).get("override_tiers") or {})
    override_tiers = {k: v for k, v in override_tiers.items() if k.startswith("--")}
    form = (contract.get("scope") or {}).get("declared_forms", ["dark"])[0]
    declared = declared_token_names(contract)

    def add(cid, name, ok, detail, klass, skip=False):
        status = "SKIP" if skip else ("PASS" if ok else ("REPORT" if klass == REPORT else "FAIL"))
        R.append((cid, name, status, detail, klass))

    # ---- T1 空集守卫（blind）
    reasons = []
    if not fams:
        reasons.append("值件未声明任何族")
    if not pages:
        reasons.append("扫描面 0 页（page_families glob 未命中任何文件）")
    if not (profile.get("page_families") or []):
        reasons.append("profile 未声明 page_families（扫描面无从谈起）")
    inline_pages = {k: v for k, v in pages.items() if v["delivery"] == "inline"}
    if not any(v["tokens"] for v in inline_pages.values()):
        reasons.append("全部内联页的 :root 块都解析出 0 枚令牌")
    if not declared:
        reasons.append("值件声明的令牌名为空")
    add("T1", "空集守卫（扫描面/族/令牌名/内联 :root 均非空）", not reasons,
        "；".join(reasons) if reasons else
        "族 %d 个 · 页 %d 个（内联 %d / 外链 %d）· 令牌名 %d 枚 · 有 :root 的内联页 %d 个"
        % (len(fams), len(pages), len(inline_pages), len(pages) - len(inline_pages),
           len(declared), sum(1 for v in inline_pages.values() if v["block"])), BLIND)

    # ---- 族期望值缓存（派生失败一律记为错误值，⛔ 不让异常逃出判据）
    exp_cache, exp_err = {}, {}
    for fam in fams:
        try:
            exp_cache[fam] = family_expected(contract, profile, fam)
        except Exception as exc:  # noqa: BLE001
            exp_err[fam] = str(exc)

    # ---- T2 族内唯一值（hard）
    dup_bad = []
    for fam in fams:
        seen = {}
        for rel, v in sorted(pages.items()):
            if v["family"] != fam:
                continue
            for tok, val in v["tokens"].items():
                if tok in seen and seen[tok][1] != val:
                    dup_bad.append("族 %s 的 %s 出现两值：%s(%s) / %s(%s)"
                                   % (fam, tok, seen[tok][1], seen[tok][0], val, rel))
                else:
                    seen.setdefault(tok, (rel, val))
    add("T2", "族内唯一值（同族同名同值；⛔ 不判全站唯一值）", not dup_bad,
        "；".join(dup_bad[:4]) if dup_bad else "各族内同名令牌均为单值", HARD)

    # ---- T3 派生一致性（hard）
    drift, checked = [], 0
    for fam in fams:
        if fam in exp_err:
            drift.append("族 %s 无法派生（%s）" % (fam, exp_err[fam]))
            continue
        want = D.normalize(D.render(exp_cache[fam]))
        for rel, v in sorted(pages.items()):
            if v["family"] != fam or v["delivery"] != "inline" or not v["block"]:
                continue
            checked += 1
            if D.normalize(v["block"]) != want:
                drift.append("%s（族 %s）与值件派生结果不一致" % (rel, fam))
    # 外链页：link 目标文件的内容 == 该族派生
    art_cache = {}
    for rel, v in sorted(pages.items()):
        if v["delivery"] != "external" or v["family"] in exp_err:
            continue
        tgt = v.get("stylesheet") or ""
        if not tgt:
            drift.append("%s（外链页）未声明 stylesheet" % rel)
            continue
        full = os.path.normpath(os.path.join(site_root, os.path.dirname(rel), tgt))
        if full not in art_cache:
            art_cache[full] = (open(full, encoding="utf-8", errors="replace").read()
                               if os.path.isfile(full) else None)
        content = art_cache[full]
        checked += 1
        if content is None:
            drift.append("%s 的外链目标不存在：%s" % (rel, tgt))
        elif D.normalize(content) != D.normalize(D.render(exp_cache[v["family"]])):
            drift.append("%s 的外链目标 %s 与该族派生不一致" % (rel, tgt))
    add("T3", "派生一致性（内联页 :root / 外链页 link 目标 == 值件派生）", not drift,
        "；".join(drift[:4]) if drift else "核对 %d 个对象，全部与值件派生一致" % checked, HARD)

    # ---- T4 跨族差异逐族登记（hard）
    per_token = {}
    for rel, v in pages.items():
        for tok, val in v["tokens"].items():
            per_token.setdefault(tok, {}).setdefault(val, []).append(rel)
    unexplained = []
    for tok, byval in per_token.items():
        if len(byval) < 2:
            continue
        for val, rels in byval.items():
            if not any(exp_cache.get(fam, {}).get(tok) == val for fam in fams):
                unexplained.append("%s=%s（%s）不被任何族解释" % (tok, val, rels[0]))
    multi = sorted(t for t, m in per_token.items() if len(m) > 1)
    add("T4", "跨族差异逐族登记（多值的每一处都能被某族派生解释）", not unexplained,
        "；".join(unexplained[:4]) if unexplained else
        "多值令牌 %d 枚（%s），全部逐族登记" % (len(multi), ",".join(multi) or "无"), HARD)

    # ---- T5 border 分档极性（hard）★ 判**盘上真实取值**
    strong, weak = names.get("border.line"), names.get("border.subtle")
    surf = names.get("surface.page")
    fam_toks = {}
    for fam in fams:
        for rel in sorted(pages):
            v = pages[rel]
            if v["family"] == fam and v["tokens"]:
                fam_toks[fam] = v["tokens"]
                break
        if fam not in fam_toks and fam in exp_cache:
            fam_toks[fam] = exp_cache[fam]      # 纯外链族：取派生值
    pol = []
    if not strong or not weak:
        pol.append("值件未绑定 border.line / border.subtle（极性判据无从谈起）")
    elif not fam_toks:
        pol.append("没有任何族有可判的令牌集（空集守卫）")
    else:
        for fam, toks in sorted(fam_toks.items()):
            a, b, bg = toks.get(strong), toks.get(weak), toks.get(surf)
            if a is None or b is None or bg is None:
                pol.append("族 %s 缺 %s / %s / %s（空集守卫）" % (fam, strong, weak, surf))
                continue
            ra = C.ratio(C.parse_color(str(a)), C.parse_color(str(bg)))
            rb = C.ratio(C.parse_color(str(b)), C.parse_color(str(bg)))
            if ra is None or rb is None or not ra > rb:
                pol.append("族 %s 极性反转：强 %s=%s(%s) 未强于 弱 %s=%s(%s)"
                           % (fam, strong, a, "%.2f" % ra if ra else "n/a",
                              weak, b, "%.2f" % rb if rb else "n/a"))
    add("T5", "border 分档极性（强分隔对比度 > 弱分隔，判盘上取值）", not pol,
        "；".join(pol) if pol else
        "；".join("族 %s %s=%s(%.2f) > %s=%s(%.2f)"
                  % (f, strong, fam_toks[f][strong],
                     C.ratio(C.parse_color(fam_toks[f][strong]), C.parse_color(fam_toks[f][surf])),
                     weak, fam_toks[f][weak],
                     C.ratio(C.parse_color(fam_toks[f][weak]), C.parse_color(fam_toks[f][surf])))
                  for f in sorted(fam_toks)), HARD)

    # ---- T6 成对对比度（hard/report 由 usage_tiers.gate 逐档决定）★ 判盘上取值
    tiers = contract.get("usage_tiers") or {}
    roles = contract.get("roles") or {}
    hardbad, rep = [], []
    for fam, toks in sorted(fam_toks.items()):
        if surf not in toks:
            hardbad.append("族 %s 缺表面令牌 %s（空集守卫）" % (fam, surf))
            continue
        # ① 角色令牌（按 roles[*].tier）
        for role, token in sorted(names.items()):
            spec_role = roles.get(role) or {}
            if spec_role.get("kind") == "dimension":
                continue                      # ★ 尺寸类角色不是颜色对象
            if role.startswith("surface."):
                continue                      # ★ 表面令牌是对比度的参考背景，不是被判对象
            tier = spec_role.get("tier")
            if token not in toks:
                continue                      # 该族未声明此令牌 ⇒ 不属本判据的对象集合
            hardbad, rep = _contrast_row(tiers, tier, fam, token, toks, surf, hardbad, rep)
        # ② 覆盖令牌（按 binding.override_tiers 声明的用途档）
        for token, tier in sorted(override_tiers.items()):
            if token not in toks:
                continue
            hardbad, rep = _contrast_row(tiers, tier, fam, token, toks, surf, hardbad, rep)
    add("T6", "成对对比度（按 usage_tiers / override_tiers 的 min_contrast 与 gate 逐档）",
        not hardbad,
        "；".join(hardbad[:4]) if hardbad else "硬阻断对全部达标；report-only %d 条" % len(rep),
        HARD if hardbad else REPORT)

    # ---- T7 零引用令牌登记（hard: 站点级 / report: 内联页页级）
    # ★ 判据对象 = **盘上真实声明**：内联页取自有 `:root`；外链页取其 `<link>` 目标的 `:root`
    #   （⛔ 不取「派生结果」——那会把「盘上多了令牌」这类事实判成不可见）
    uses_site, uses_page = {}, {}
    art_toks_cache = {}
    for rel, v in sorted(pages.items()):
        refs = set(VAR_RE.findall(v["raw"]))
        if v["delivery"] == "inline":
            toks = v["tokens"]
        else:
            tgt = v.get("stylesheet") or ""
            full = os.path.normpath(os.path.join(site_root, os.path.dirname(rel), tgt))
            if full not in art_toks_cache:
                blk = (D.extract_block(open(full, encoding="utf-8", errors="replace").read())
                       if os.path.isfile(full) else None)
                art_toks_cache[full] = D.parse_tokens(blk) if blk else {}
            toks = art_toks_cache[full]
        for tok in toks:
            uses_site[tok] = uses_site.get(tok, 0) + (1 if tok in refs else 0)
            if v["delivery"] == "inline":
                uses_page[(tok, rel)] = 1 if tok in refs else 0
    reg = contract.get("dead_tokens") or {}
    reg_site = {e.get("token") for e in (reg.get("site_level_zero_ref") or [])}
    reg_page = {(e.get("token"), e.get("page")) for e in (reg.get("page_level_unused") or [])}
    declared_here = {t for t, n in uses_site.items() if n == 0}
    unreg_site = sorted(declared_here - reg_site)
    stale_site = sorted(reg_site - declared_here)
    unreg_page = sorted((t, r) for (t, r), n in uses_page.items()
                        if n == 0 and uses_site.get(t, 0) > 0 and (t, r) not in reg_page)
    stale_page = sorted((t, r) for (t, r) in reg_page if (t, r) in uses_page and uses_page[(t, r)] != 0)
    bad7 = []
    if unreg_site:
        bad7.append("站点级零引用未登记：%s" % unreg_site)
    if stale_site:
        bad7.append("登记了但实际有引用（登记过期）：%s" % stale_site)
    if stale_page:
        bad7.append("页级登记过期：%s" % stale_page)
    rep7 = ["页级未用未登记：%s" % unreg_page] if unreg_page else []
    add("T7", "零引用令牌登记（站点级 hard / 内联页页级 report；登记不得过期）", not bad7,
        "；".join(bad7 + rep7) if (bad7 or rep7) else
        "站点级零引用 %d 枚（%s）全部登记；页级未用 %d 条全部登记"
        % (len(declared_here), ",".join(sorted(declared_here)) or "无", len(reg_page)),
        HARD if bad7 else REPORT)

    # ---- T8 生成器单源不变量（hard）
    inv = profile.get("single_source_invariants") or {}
    g8 = []
    if not inv:
        g8.append("profile 未声明 single_source_invariants（⛔ 不静默跳过）")
    else:
        vf = inv.get("value_file")
        if not vf or not os.path.isfile(os.path.join(site_root, vf)):
            g8.append("声明的值件不存在：%s" % vf)
        want_default = D.normalize(D.render(exp_cache["default"])) if "default" in exp_cache else None
        gens = inv.get("literal_free_generators") or []
        if not gens:
            g8.append("literal_free_generators 为空（空集守卫）")
        for rel in gens:
            fp = os.path.join(site_root, rel)
            if not os.path.isfile(fp):
                g8.append("声明的生成器不存在：%s" % rel)
                continue
            src = _strip_py_comments(open(fp, encoding="utf-8", errors="replace").read())
            if D.extract_block(src):
                g8.append("%s 仍持有 :root 令牌块字面值" % rel)
            m = LITERAL_RE.search(src)
            if m:
                g8.append("%s 仍持有令牌赋值字面值：%s" % (rel, m.group(0)))
            if vf and os.path.basename(vf) not in src:
                g8.append("%s 未引用单源值件（%s）" % (rel, os.path.basename(vf)))
            # ★ 真跑：导入生成器并调它的 root_tokens('default')，必须等于值件派生
            try:
                mod = _import_module(fp, "genmod_%s" % re.sub(r"\W", "_", rel))
                got = D.normalize(mod.root_tokens("default"))
                if want_default is None or got != want_default:
                    g8.append("%s 真跑 root_tokens('default') 与值件派生不一致" % rel)
            except Exception as exc:  # noqa: BLE001
                g8.append("%s 导入/真跑失败：%s" % (rel, str(exc)[-120:]))
    add("T8", "生成器单源不变量（无字面值 ＋ 真跑展开 == 值件派生）", not g8,
        "；".join(g8[:4]) if g8 else "三个生成器均无令牌字面值，且真跑展开与值件派生一致", HARD)

    # ---- T9 未声明令牌（hard）
    unknown = []
    for rel, v in sorted(pages.items()):
        extra = sorted(set(v["tokens"]) - declared)
        if extra:
            unknown.append("%s 出现未声明令牌 %s" % (rel, extra))
    add("T9", "未声明令牌（盘上令牌名 ⊆ 值件声明面）", not unknown,
        "；".join(unknown[:4]) if unknown else "值件声明 %d 枚，盘上无未声明令牌" % len(declared), HARD)

    # ---- T10 目标存在性（hard）
    miss = []
    for t in profile.get("targets") or []:
        if not os.path.isfile(os.path.join(site_root, t["path"])):
            miss.append("目标不存在：%s" % t["path"])
    add("T10", "目标存在性（profile.targets 全在）", not miss,
        "；".join(miss[:4]) if miss else
        "目标 %d 个全部存在" % len(profile.get("targets") or []), HARD)

    # ---- T11 覆盖完备性（blind）
    universe = all_repo_html(site_root)
    covered = set(pages)
    uncovered = {e.get("path") for e in (profile.get("uncovered_pages") or [])}
    c11 = []
    if not uncovered:
        c11.append("profile 未声明 uncovered_pages（覆盖完备性无从判起）")
    miss_u = sorted(u for u in uncovered if not os.path.isfile(os.path.join(site_root, u)))
    if miss_u:
        c11.append("未覆盖项不存在：%s" % miss_u)
    overlap = sorted(covered & uncovered)
    if overlap:
        c11.append("同一页同时被扫描面与未覆盖声明覆盖：%s" % overlap)
    diff = sorted(universe - covered - uncovered)
    if diff:
        c11.append("既不在扫描面也不在未覆盖声明里：%s（前 8 项）" % diff[:8])
    extra = sorted(covered - universe)
    if extra:
        c11.append("扫描面命中全仓 HTML 之外的文件：%s" % extra[:4])
    add("T11", "覆盖完备性（全仓 HTML = 扫描面 ∪ 已声明未覆盖，且不交）", not c11,
        "；".join(c11[:4]) if c11 else
        "全仓 HTML %d 个 = 扫描面 %d ＋ 已声明未覆盖 %d（%s）"
        % (len(universe), len(covered), len(uncovered), ",".join(sorted(uncovered))), BLIND)

    # ---- T12 形态分别断言（hard）
    # ★★ 批 J 口径重述（判据**意图未变**，只把判据对象收窄到它本来要管的那个对象）：
    #   原口径 `len(LINK_RE.findall(raw)) != 1` 把页面里**全部** `<link>` 都当判据对象
    #   ⇒ 一旦页面按 SEO 标准（SH4 §4.2 的 S6/S7 ＋ COMMON.md §2.1）多出
    #   `<link rel="canonical">` 与 `<link rel="icon">`，本判据就在**自己不该管的对象**上 FAIL
    #   （实测：外链页 `<link>` 数 1→2→3，T12 由 PASS 转 FAIL）。
    #   ⇒ 判据对象收窄为 **`rel="stylesheet"` 的 `<link>`**（这正是「外链样式表唯一性」的意图面）。
    #   ★ 依据：① 判据对象 == 断言对象（SH5 §4.0 第 1 条）；② 姊妹站
    #   `control-theory-agent-kb` 的同类判据按 **basename 匹配**写，天然不受 canonical/icon 影响
    #   ⇒ 本次是把两站的同一意图收敛到同一口径，⛔ 不是新造判据、⛔ 不是放宽阈值。
    #   ★ 非恒真已由 `--selftest` 的两条新夹具守住：两个 stylesheet 的 `<link>` ⇒ 照旧 FAIL；
    #     1 stylesheet ＋ 1 canonical ＋ 1 icon ⇒ PASS。
    ls = profile.get("link_surface") or {}
    isurf = profile.get("inline_surface") or {}
    art = ls.get("artifact") or ""
    ext_pages = {k: v for k, v in pages.items() if v["delivery"] == "external"}
    inl_pages = {k: v for k, v in pages.items() if v["delivery"] == "inline"}
    f12 = []
    exp_ext = ls.get("expected_pages")
    exp_inl = isurf.get("expected_pages")
    if exp_ext is not None and len(ext_pages) != exp_ext:
        f12.append("外链页数 %d ≠ 声明 %d" % (len(ext_pages), exp_ext))
    if exp_inl is not None and len(inl_pages) != exp_inl:
        f12.append("内联页数 %d ≠ 声明 %d" % (len(inl_pages), exp_inl))
    if not art:
        f12.append("profile 未声明 link_surface.artifact（空集守卫）")
    for rel, v in sorted(ext_pages.items()):
        links = STYLESHEET_LINK_RE.findall(v["raw"])
        if len(links) != 1:
            f12.append("%s 的 rel=\"stylesheet\" <link> 数 = %d（应为 1）" % (rel, len(links)))
            continue
        if "stylesheet" not in links[0].lower():
            f12.append("%s 的 <link> 不是 stylesheet：%s" % (rel, links[0][:60]))
            continue
        m = re.search(r'href=["\']([^"\']+)["\']', links[0])
        href = m.group(1) if m else ""
        if not href or href.startswith(("http://", "https://", "/")):
            f12.append("%s 的外链不是仓内相对路径：%r" % (rel, href))
            continue
        if not href.endswith(".css"):
            f12.append("%s 的外链扩展名不是 .css：%r（⇒ content-type 无法为 text/css）" % (rel, href))
        full = os.path.normpath(os.path.join(site_root, os.path.dirname(rel), href))
        if not os.path.isfile(full):
            f12.append("%s 的外链目标在仓内不存在：%s" % (rel, href))
        if v["block"]:
            f12.append("%s 是外链页却仍内联 :root（令牌有两个来源）" % rel)
    for rel, v in sorted(inl_pages.items()):
        # ★ 批 J 口径重述的另一侧：内联页断言的是「**零外链样式**」（形态 1/2 的分野），
        #   故判据对象同样是 `rel="stylesheet"` 的 <link>；canonical / icon 不是外链样式，
        #   按 COMMON.md §2.1 它们在内联页上是**必需**的（S6/S7 硬判）。
        if STYLESHEET_LINK_RE.search(v["raw"]):
            f12.append("%s 是内联页却含外链样式 <link rel=\"stylesheet\">（形态 1/2 必须分别成立）" % rel)
    add("T12", "形态分别断言（外链页恰 1 个 rel=\"stylesheet\" 的 <link> ＋ 目标可达；内联页零外链样式）",
        not f12,
        "；".join(f12[:4]) if f12 else
        "外链页 %d 个全部有且仅有 1 个指向 %s 的 rel=\"stylesheet\" <link> 且目标在仓内；"
        "内联页 %d 个零外链样式" % (len(ext_pages), art, len(inl_pages)), HARD)

    return R


def _contrast_row(tiers, tier, fam, token, toks, surf, hardbad, rep):
    spec = tiers.get(tier)
    if not spec:
        hardbad.append("族 %s 令牌 %s 的 tier=%r 未在 usage_tiers 内" % (fam, token, tier))
        return hardbad, rep
    need = (spec.get("min_contrast") or {}).get("dark")
    if not need:
        return hardbad, rep
    a, b = toks.get(token), toks.get(surf)
    if a is None or b is None:
        hardbad.append("族 %s %s/%s 令牌缺失（空集守卫）" % (fam, token, surf))
        return hardbad, rep
    rr = C.ratio(C.parse_color(str(a)), C.parse_color(str(b)))
    if spec.get("gate") == "hard":
        if rr is None or rr < need:
            hardbad.append("族 %s %s=%s 对 %s=%s 仅 %s < %s"
                           % (fam, token, a, surf, b, "n/a" if rr is None else "%.2f" % rr, need))
    else:
        rep.append("族 %s %s=%.2f（report-only 档）" % (fam, token, rr if rr is not None else -1))
    return hardbad, rep


# --------------------------------------------------------------------------- 摘要 / 报告
def summarize(R, pages):
    counts = {"pages": len(pages),
              "inline": sum(1 for v in pages.values() if v["delivery"] == "inline"),
              "external": sum(1 for v in pages.values() if v["delivery"] == "external"),
              "judges": len(R),
              "pass": sum(1 for r in R if r[2] == "PASS"),
              "fail": sum(1 for r in R if r[2] == "FAIL"),
              "report": sum(1 for r in R if r[2] == "REPORT"),
              "skip": sum(1 for r in R if r[2] == "SKIP")}
    counts["blocking_fail"] = sum(1 for r in R if r[2] == "FAIL" and r[4] == BLIND)
    return counts


def tree_digest(site_root, extra_roots=()):
    """确定性树摘要：仓内参与文件的（相对路径 ＋ 内容 sha256）排序后再取一次 sha256。

    ⛔ 不含墙钟时间戳、⛔ 不含作者机绝对路径；⛔ 排除报告自身与基线自身。
    """
    EXCLUDE = {"gate-report.json", "build/gate-baseline.json"}
    files = {}
    for dp, dn, fn in os.walk(site_root):
        dn[:] = [d for d in dn if d not in SKIP_DIRS and not d.startswith(".")]
        for f in fn:
            rel = os.path.relpath(os.path.join(dp, f), site_root).replace(os.sep, "/")
            if rel in EXCLUDE or rel.endswith(".pyc"):
                continue
            with open(os.path.join(dp, f), "rb") as fh:
                files[rel] = hashlib.sha256(fh.read()).hexdigest()
    for rel in extra_roots:
        fp = os.path.join(site_root, rel)
        if os.path.isfile(fp):
            with open(fp, "rb") as fh:
                files[rel] = hashlib.sha256(fh.read()).hexdigest()
    h = hashlib.sha256()
    for rel in sorted(files):
        h.update(("%s\0%s\n" % (rel, files[rel])).encode("utf-8"))
    return h.hexdigest(), files


def write_report(path, gate_name, doc):
    """把本门控的一节**并入** `gate-report.json`（对称合并：先读后写，按 gate 名排序）。

    ★ 为什么合并而不是各写各的：SH5 §4.2 第 3 点要求「把门控输出写入 gate-report.json 随产物入库」，
      而本站有两道门控 ⇒ 若各写各的，后跑的那道会把先跑的**痕迹抹掉**（「跑没跑过」就无从回答）。
    ★ 确定性：⛔ 无墙钟时间戳、⛔ 无作者机绝对路径；同输入两次运行产出**逐字节相同**。
    """
    entries = {}
    if os.path.isfile(path):
        try:
            with open(path, encoding="utf-8") as fh:
                old = json.load(fh)
            for e in (old.get("gates") or []):
                if isinstance(e, dict) and e.get("gate"):
                    entries[e["gate"]] = e
        except Exception:  # noqa: BLE001
            entries = {}
    entries[gate_name] = doc
    out = {"site": doc.get("site"),
           "schema": "site-gate-report/1",
           "deterministic": True,
           "determinism_note": "★ 确定性件：⛔ 无墙钟时间戳、⛔ 无作者机绝对路径；"
                               "tree_digest 排除本报告自身与 build/gate-baseline.json。",
           "gates": [entries[k] for k in sorted(entries)]}
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return out


# --------------------------------------------------------------------------- 主流程
def run(site_root, contract_path, profile_path):
    contract = load_json(contract_path, "值件")
    profile = load_json(profile_path, "profile")
    pages = collect_pages(site_root, profile)
    ctx = {"site_root": site_root, "contract": contract, "profile": profile, "pages": pages}
    return judge(ctx), contract, profile, pages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site-root", default=".")
    ap.add_argument("--contract", default=None)
    ap.add_argument("--profile", default=None)
    ap.add_argument("--manifest", default=None)
    ap.add_argument("--mode", choices=["report", "enforce"], default=None)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--baseline-out", default=None)
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
        R, contract, profile, pages = run(site_root, contract_path, profile_path)
    except (GateError, D.GuardError) as exc:
        print("GUARD-REJECT: %s" % exc)
        return 3

    mode = a.mode or (profile.get("gates", {}) or {}).get("mode_now") or "report"
    for cid, name, status, detail, klass in R:
        print("[%s] %s %s（%s）— %s" % (status, cid, name, klass, detail))
    counts = summarize(R, pages)
    print("\n=== 站点令牌门控（mode=%s）：%d 项判据 · PASS %d / FAIL %d / REPORT %d / SKIP %d；"
          "扫描 %d 页（内联 %d / 外链 %d）==="
          % (mode, counts["judges"], counts["pass"], counts["fail"], counts["report"],
             counts["skip"], counts["pages"], counts["inline"], counts["external"]))

    digest, files = tree_digest(site_root)
    if a.baseline_out or a.report_out:
        doc = {"gate": "gate_tokens.py",
               "site": contract.get("scope", {}).get("site"),
               "mode": mode,
               "tree_digest": digest,
               "classes_covered": ["① 对比度", "② 令牌唯一值"],
               "counts": counts,
               "judges": [{"id": c, "name": n, "class": k, "status": s, "detail": d}
                          for c, n, s, d, k in R],
               "not_covered": NOT_COVERED}
        if a.report_out:
            write_report(a.report_out, "gate_tokens.py", doc)
            print("报告已并入：%s（gate=gate_tokens.py，tree_digest=%s）" % (a.report_out, digest[:16]))
        if a.baseline_out:
            base = {"schema": "site-gate-baseline/1", "deterministic": True,
                    "tree_digest": digest, "files": files}
            with open(a.baseline_out, "w", encoding="utf-8") as fh:
                json.dump(base, fh, ensure_ascii=False, indent=1)
                fh.write("\n")
            print("基线已写入：%s（%d 个文件）" % (a.baseline_out, len(files)))
    if a.json:
        print(json.dumps({"mode": mode, "counts": counts, "tree_digest": digest,
                          "judges": [{"id": c, "name": n, "class": k, "status": s}
                                     for c, n, s, d, k in R]}, ensure_ascii=False, indent=1))

    blind_fail = [r for r in R if r[4] == BLIND and r[2] == "FAIL"]
    hard_fail = [r for r in R if r[4] == HARD and r[2] == "FAIL"]
    if blind_fail:
        print("阻断：blind 类判据 FAIL（门控致盲，报告模式也不宽恕）")
        return 1
    if mode == "enforce" and hard_fail:
        print("阻断：enforce 模式下 hard 类判据 FAIL")
        return 1
    if hard_fail or [r for r in R if r[2] == "REPORT"]:
        print("报告模式：上述 FAIL/REPORT 已记基线，不阻断（转硬条件见 build/profile.json 的 gates.mode_now_transition）")
    return 0


# --------------------------------------------------------------------------- selftest
FIX_TAIL_CONTRACT = {
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
        "text.primary": {"dark": "#e6e8ee"},
        "border.line": {"dark": "#6b7280"},
        "border.subtle": {"dark": "#2a2f3a"},
        "surface.page": {"dark": "#0f1117"},
        "ok": {"dark": "#2fb98a"},
    }}},
    "binding": {"site_token_names": {"text.primary": "--text", "border.line": "--border",
                                     "border.subtle": "--border-subtle", "surface.page": "--bg",
                                     "ok": "--ok"},
                "override_tiers": {"--warn": "body"},
                "passthrough_tokens": {}},
    "families": {"default": {"targets": ["assets/tokens.css"], "overrides": {"--warn": "#e8933b"}},
                 "index": {"targets": ["index.html"], "overrides": {}}},
    "derivation": {"state": "s", "direction": "d", "generator_ref": "g", "rule": "r"},
    "dead_tokens": {"site_level_zero_ref": [], "page_level_unused": []},
}
FIX_TAIL_PROFILE = {
    "site": "t", "form": "mixed", "publish_dir": ".", "value_file": "contract.json",
    "targets": [{"path": "assets/tokens.css", "mode": "whole-file", "family": "default"},
                {"path": "index.html", "mode": "root-block", "family": "index"}],
    "page_families": [{"glob": "g/*.html", "family": "default", "delivery": "external",
                       "stylesheet": "../assets/tokens.css"},
                      {"glob": "n/*.html", "family": "default", "delivery": "inline"},
                      {"glob": "index.html", "family": "index", "delivery": "inline"}],
    "uncovered_pages": [{"path": "report.html", "reason": "夹具：无生成器可复现"}],
    "link_surface": {"artifact": "assets/tokens.css", "expected_pages": 1},
    "inline_surface": {"expected_pages": 2},
    "single_source_invariants": {"value_file": "contract.json",
                                 "literal_free_generators": ["07-checkpoint/gen.py"]},
    "gates": {"manifest": "gate-manifest.json", "mode_now": "report"},
}
FIX_ROOT_BLOCK = (":root{--text:#e6e8ee;--border:#6b7280;--border-subtle:#2a2f3a;--bg:#0f1117;"
                  "--ok:#2fb98a;--warn:#e8933b;}")
FIX_INDEX_BLOCK = (":root{--text:#e6e8ee;--border:#6b7280;--border-subtle:#2a2f3a;--bg:#0f1117;"
                   "--ok:#2fb98a;}")
# 每页都引用它声明的**全部**令牌 ⇒ 站点级零引用集合为空（正向夹具不该有零引用）
FIX_USES_ALL = (":focus-visible{outline:1px solid var(--border);}"
                "a{color:var(--text);outline-color:var(--border-subtle);background:var(--bg);}"
                "b{color:var(--ok);}i{color:var(--warn);}")
FIX_GEN_PY = '''#!/usr/bin/env python3
import json
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'vendor', 'pipeline'))
import derive_site_tokens as D
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def root_tokens(family='default'):
    """夹具生成器：运行期从单源值件（contract.json）展开令牌块。"""
    c = json.load(open(os.path.join(ROOT, 'contract.json'), encoding='utf-8'))
    p = json.load(open(os.path.join(ROOT, 'profile.json'), encoding='utf-8'))
    return D.render(D.build_tokens(c, p, family)[1])
'''


def _fix_page(block, stylesheet=None, uses=FIX_USES_ALL):
    link = ('<link rel="stylesheet" href="%s">' % stylesheet) if stylesheet else ''
    return ('<!DOCTYPE html><html><head>' + link + '<style>' + block + uses + '</style></head>'
            '<body><a class="skip" href="#main">skip</a><main id="main">hi</main></body></html>\n')


def _fixture_tree(tmp):
    import shutil
    for d in ("g", "n", "assets", "07-checkpoint", "vendor/pipeline", "vendor/tools"):
        os.makedirs(os.path.join(tmp, d), exist_ok=True)
    shutil.copyfile(os.path.join(VENDOR, "derive_site_tokens.py"),
                    os.path.join(tmp, "vendor", "pipeline", "derive_site_tokens.py"))
    shutil.copyfile(os.path.join(HERE, "vendor", "tools", "contrast.py"),
                    os.path.join(tmp, "vendor", "tools", "contrast.py"))
    open(os.path.join(tmp, "g", "a.html"), "w", encoding="utf-8").write(
        _fix_page("", "../assets/tokens.css"))
    open(os.path.join(tmp, "n", "c.html"), "w", encoding="utf-8").write(_fix_page(FIX_ROOT_BLOCK))
    open(os.path.join(tmp, "index.html"), "w", encoding="utf-8").write(_fix_page(FIX_INDEX_BLOCK))
    open(os.path.join(tmp, "report.html"), "w", encoding="utf-8").write(
        "<!DOCTYPE html><html><body>uncovered</body></html>\n")
    open(os.path.join(tmp, "assets", "tokens.css"), "w", encoding="utf-8").write(FIX_ROOT_BLOCK + "\n")
    open(os.path.join(tmp, "07-checkpoint", "gen.py"), "w", encoding="utf-8").write(FIX_GEN_PY)
    cp, pp = os.path.join(tmp, "contract.json"), os.path.join(tmp, "profile.json")
    json.dump(FIX_TAIL_CONTRACT, open(cp, "w", encoding="utf-8"), ensure_ascii=False)
    json.dump(FIX_TAIL_PROFILE, open(pp, "w", encoding="utf-8"), ensure_ascii=False)
    return cp, pp


def _run_fixture(mutate=None):
    import tempfile
    tmp = tempfile.mkdtemp(prefix="akggate-")
    cp, pp = _fixture_tree(tmp)
    if mutate:
        mutate(tmp, cp, pp)
    c = json.load(open(cp, encoding="utf-8"))
    p = json.load(open(pp, encoding="utf-8"))
    pages = collect_pages(tmp, p)
    R = judge({"site_root": tmp, "contract": c, "profile": p, "pages": pages})
    return R, tmp


def selftest():
    cases = []

    def case(name, cid, mutate, expect_fail=True):
        try:
            R, _tmp = _run_fixture(mutate)
        except Exception as exc:  # noqa: BLE001
            cases.append((name, False, "异常：%s" % exc))
            return
        got = {r[0]: r[2] for r in R}
        ok = (got.get(cid) == "FAIL") if expect_fail else (got.get(cid) == "PASS")
        cases.append((name, ok, ""))

    def setc(fn):
        def _m(tmp, cp, pp):
            c = json.load(open(cp, encoding="utf-8"))
            fn(c)
            json.dump(c, open(cp, "w", encoding="utf-8"), ensure_ascii=False)
        return _m

    def setp(fn):
        def _m(tmp, cp, pp):
            p = json.load(open(pp, encoding="utf-8"))
            fn(p)
            json.dump(p, open(pp, "w", encoding="utf-8"), ensure_ascii=False)
        return _m

    def edit_page(name, fn):
        def _m(tmp, cp, pp):
            fp = os.path.join(tmp, name)
            s = open(fp, encoding="utf-8").read()
            out = fn(s)
            # ★ 批 J：夹具自检——替换必须真的命中（防「夹具没改到 ⇒ 负例其实没被触发」的假绿）
            assert out != s, "夹具自检：%s 的替换未命中" % name
            open(fp, "w", encoding="utf-8").write(out)
        return _m

    def add_page(name, text):
        def _m(tmp, cp, pp):
            open(os.path.join(tmp, name), "w", encoding="utf-8").write(text)
        return _m

    # ---- 正向夹具（★ 证明判据不是恒真：12 条判据在夹具上必须全 PASS）
    R0, _t0 = _run_fixture()
    cases.append(("T-正例 夹具 12 条判据全部 PASS（⛔ 判据非恒真）",
                  all(r[2] == "PASS" for r in R0),
                  "；".join("%s=%s" % (r[0], r[2]) for r in R0 if r[2] != "PASS")[:160]))

    # ---- 逐判据负例（每条判据至少一个，且必须真的触发）
    case("T1 负例：扫描面 glob 未命中任何文件",
         "T1", setp(lambda p: p.__setitem__("page_families", [{"glob": "nope/*.html", "family": "default"}])))
    case("T1 负例：命中的页全部无 :root（令牌解析出 0 枚）",
         "T1", setp(lambda p: p.__setitem__("page_families", [{"glob": "report.html", "family": "default",
                                                               "delivery": "inline"}])))
    case("T2 负例：同族内同名令牌两值",
         "T2", lambda tmp, cp, pp: (setp(lambda p: p["page_families"].append(
             {"glob": "n/*.html", "family": "index", "delivery": "inline"}))(tmp, cp, pp),
             add_page("n/d.html", _fix_page(FIX_INDEX_BLOCK.replace("--text:#e6e8ee", "--text:#123456")))(
                 tmp, cp, pp)))
    case("T3 负例：内联页取值与值件派生不一致",
         "T3", edit_page("index.html", lambda s: s.replace("--text:#e6e8ee", "--text:#123456")))
    case("T3 负例：外链目标与值件派生不一致",
         "T3", edit_page("assets/tokens.css", lambda s: s.replace("--ok:#2fb98a", "--ok:#000000")))
    case("T4 负例：多值不被任何族解释",
         "T4", edit_page("index.html", lambda s: s.replace("--border-subtle:#2a2f3a", "--border-subtle:#abcdef")))
    case("T5 负例：分档极性反转（强分隔取弱值）",
         "T5", edit_page("index.html", lambda s: s.replace("--border:#6b7280", "--border:#111111")))
    case("T6 负例：正文对比度不达标（--text 压到近背景）",
         "T6", edit_page("index.html", lambda s: s.replace("--text:#e6e8ee", "--text:#101010")))
    case("T7 负例：站点级零引用未登记",
         "T7", edit_page("assets/tokens.css", lambda s: s.replace("--warn:#e8933b;", "--warn:#e8933b;--err:#ff6b6b;")))
    case("T7 负例：登记项其实有引用（登记过期）",
         "T7", lambda tmp, cp, pp: (setc(lambda c: c["dead_tokens"]["site_level_zero_ref"].append(
             {"token": "--ok", "reason": "夹具：登记过期"}))(tmp, cp, pp)))
    case("T8 负例：生成器仍持令牌字面值块",
         "T8", edit_page("07-checkpoint/gen.py", lambda s: s + '\nLITERAL = "' + FIX_ROOT_BLOCK + '"\n'))
    case("T8 负例：生成器真跑结果与值件派生不一致",
         "T8", edit_page("07-checkpoint/gen.py",
                         lambda s: s.replace("D.render(D.build_tokens(c, p, family)[1])",
                                             "':root{--text:#000000;}'")))
    case("T8 负例：profile 未声明单源不变量",
         "T8", setp(lambda p: p.pop("single_source_invariants")))
    case("T9 负例：盘上出现未声明令牌",
         "T9", edit_page("index.html", lambda s: s.replace("--ok:#2fb98a", "--ok:#2fb98a;--ghost:#ffffff")))
    case("T10 负例：声明了不存在的目标",
         "T10", setp(lambda p: p["targets"].append({"path": "ghost.html", "mode": "root-block",
                                                    "family": "index"})))
    case("T11 负例：有页面既不在扫描面也不在未覆盖声明里",
         "T11", add_page("orphan.html", "<!DOCTYPE html><html><body>o</body></html>"))
    case("T11 负例：同一页同时被扫描面与未覆盖声明覆盖",
         "T11", setp(lambda p: p["uncovered_pages"].append({"path": "index.html", "reason": "x"})))
    case("T11 负例：未覆盖项不存在",
         "T11", setp(lambda p: p.__setitem__("uncovered_pages", [{"path": "nope.html", "reason": "x"}])))
    case("T12 负例：外链页没有 <link>",
         "T12", edit_page("g/a.html", lambda s: s.replace(
             '<link rel="stylesheet" href="../assets/tokens.css">', "")))
    case("T12 负例：外链页用绝对 URL",
         "T12", edit_page("g/a.html", lambda s: s.replace(
             'href="../assets/tokens.css"', 'href="https://example.com/assets/tokens.css"')))
    case("T12 负例：外链页扩展名不是 .css（⇒ content-type 无法为 text/css）",
         "T12", edit_page("g/a.html", lambda s: s.replace("tokens.css", "tokens.txt")))
    case("T12 负例：内联页出现外链样式",
         "T12", edit_page("index.html", lambda s: s.replace(
             "</head>", '<link rel="stylesheet" href="assets/tokens.css"></head>')))
    # ---- ★ 批 J 口径重述的成对夹具（证明重述后**不是恒真**）
    case("T12 负例（重述后仍必须 FAIL）：外链页出现**两个** rel=\"stylesheet\" 的 <link>",
         "T12", edit_page("g/a.html", lambda s: s.replace(
             '<link rel="stylesheet" href="../assets/tokens.css">',
             '<link rel="stylesheet" href="../assets/tokens.css">'
             '<link rel="stylesheet" href="../assets/tokens.css">')))
    case("★ T12 正向（重述的核心）：1 个 stylesheet ＋ 1 个 canonical ＋ 1 个 icon ⇒ **必须 PASS**"
         "（原口径在此假 FAIL）",
         "T12", edit_page("g/a.html", lambda s: s.replace(
             '<link rel="stylesheet" href="../assets/tokens.css">',
             '<link rel="canonical" href="https://example.github.io/site/g/a.html">'
             '<link rel="icon" type="image/svg+xml" href="/site/favicon.svg">'
             '<link rel="stylesheet" href="../assets/tokens.css">')),
         expect_fail=False)

    # ---- ★ 假阳样本（这些改动**不应**触发对应判据）
    def fp_family_override(tmp, cp, pp):
        c = json.load(open(cp, encoding="utf-8"))
        c["families"]["index"]["overrides"] = {"--warn": "#e0c35e"}
        json.dump(c, open(cp, "w", encoding="utf-8"), ensure_ascii=False)
        fp = os.path.join(tmp, "index.html")
        s = open(fp, encoding="utf-8").read().replace("--ok:#2fb98a;}", "--ok:#2fb98a;--warn:#e0c35e;}")
        open(fp, "w", encoding="utf-8").write(s)
    case("假阳样本 1：跨族同名不同值（--warn 两值：default #e8933b / index #e0c35e）**不应**触发 T2",
         "T2", fp_family_override, expect_fail=False)
    case("假阳样本 1b：同上 **不应**触发 T4（多值的每一处都被某族解释）",
         "T4", fp_family_override, expect_fail=False)

    def fp_comment(tmp, cp, pp):
        fp = os.path.join(tmp, "07-checkpoint", "gen.py")
        s = open(fp, encoding="utf-8").read()
        open(fp, "w", encoding="utf-8").write(s + "\n# 说明：本文件不持有 " + FIX_ROOT_BLOCK + " 这样的字面值\n")
    case("假阳样本 2：注释里出现 :root 字样 **不应**触发 T8",
         "T8", fp_comment, expect_fail=False)

    def fp_report_only(tmp, cp, pp):
        """report-only 档不达标只报 REPORT，⛔ 不得算 FAIL。"""
        fp = os.path.join(tmp, "n", "c.html")
        s = open(fp, encoding="utf-8").read().replace("--border-subtle:#2a2f3a", "--border-subtle:#20242c")
        open(fp, "w", encoding="utf-8").write(s)
        open(os.path.join(tmp, "assets", "tokens.css"), "w", encoding="utf-8").write(
            FIX_ROOT_BLOCK.replace("--border-subtle:#2a2f3a", "--border-subtle:#20242c") + "\n")
    case("假阳样本 3：report-only 档（border.subtle 不达 3:1）**不得**算 T6 FAIL",
         "T6", fp_report_only, expect_fail=False)

    # ---- ★ 空集守卫负例（0 个文件被扫 ⇒ 必须 FAIL 而不是静默通过）
    case("空集守卫：扫描面 0 个文件必须 FAIL（⛔ 不静默跳过）",
         "T1", setp(lambda p: p.__setitem__("page_families", [])))
    case("空集守卫：全仓 HTML 都在扫描面、未覆盖声明为空 ⇒ T11 必须 FAIL（覆盖完备性无从判起）",
         "T11", setp(lambda p: p.__setitem__("uncovered_pages", [])))

    ok = all(v for _, v, _ in cases)
    for name, res, note in cases:
        print("  [%s] %s%s" % ("PASS" if res else "FAIL", name, ("  ← " + note) if note else ""))
    print("\n=== gate_tokens.py 自检：%d 项，%d FAIL ===" % (len(cases), sum(1 for _, v, _ in cases if not v)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
