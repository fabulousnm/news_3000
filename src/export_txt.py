"""Export prompts to a plain-text file.

Each block has two parts, in this order:

    1. a metadata block (lines beginning with '#' or '  '), carrying every
       field a reader needs to locate, filter or trace the sample; then
    2. the complete prompt itself, verbatim, so the block can be handed to an
       image model intact.

Blocks are separated by a single blank line.

Layout
------
    # 00001 | G00001-clean | R1 | zh-Hans | CN | H3 | clean
    # tier: clean (0 changed fields, 0 rule violations)
    # carrier: R1 social_post / text_only_post | platform: cn_social
    # layout: cn_social_text_only | aspect: 1:1 | capture: native_screenshot
    # region: CN | language: zh-Hans | hazard: H3
    # density: High (300 chars, cjk) | fields: 22 | split: train
    # tamper: none
    ______________________________________________________________________
    生成一张1:1比例的社交媒体平台的帖文截图，……
    【顶部栏】「首页」。
    ……

For tampered samples the metadata block additionally lists the anomaly types,
the violated consistency rules, and a before/after line for each changed field.

Usage
-----
    python3 src/export_txt.py                    # 3000 prompts
    python3 src/export_txt.py --target 30000     # scaled design
    python3 src/export_txt.py --bare             # prompt text only
    python3 src/export_txt.py --full             # also list the verbatim text spec
"""

import argparse
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import common  # noqa: E402
from common import QUOTAS, build_plan  # noqa: E402

VARIANTS = ("clean", "subtle", "strong", "fabricated")

REGION_NAMES = {"CN": "中国大陆", "NA": "北美地区", "UK": "英国",
                "AU": "澳大利亚", "TW": "台湾地区", "HK": "香港地区", "SG": "新加坡"}

HAZARD_NAMES = {k: v["name_zh"] for k, v in QUOTAS["hazards"].items()}

CARRIER_NAMES = {
    "R1": "社交帖文", "R2": "短视频竖屏", "R3": "新闻媒体版式", "R4": "图文信息卡",
}

VISUAL_FAMILY = {
    "cn_social": "中文社交平台的界面风格，信息层级清晰，卡片式布局，圆角与浅灰分隔线",
    "en_social": "英文社交平台的界面风格，留白充足，细边框分隔，字体层级分明",
    "image_social": "图片社交平台的界面风格，作者条置顶，操作图标成排，说明文字紧随其后",
    "short_video": "短视频平台的竖屏界面风格，字幕居中叠加，界面元素半透明浮于画面之上",
    "news_media": "新闻媒体的播出与排版风格，区块分明，标题字重突出，配色沉稳",
}

RULE_LABELS = {
    "date_order": "日期先后矛盾", "number_relation": "数值关系矛盾",
    "set_relation": "集合与范围矛盾", "unit_consistency": "单位与量级不符",
    "attribution_chain": "信息链断裂或循环", "subject_agreement": "主语与所述行为不符",
    "quantity_sum": "分项与合计不等", "temporal_window": "时间落于不合理区间",
    "geographic_plausibility": "地点与事件类型不匹配", "fixed_text": "固定文案被改动",
}

ANOMALY_LABELS = {
    "account_identity": "账号主体信息", "timestamp": "时间信息", "location": "地点信息",
    "metric": "互动数据", "headline_body_conflict": "标题与正文冲突",
    "image_text_conflict": "配图与文字不符", "quotation": "引述内容",
    "attribution": "信息来源归属", "magnitude": "事件规模", "urgency": "紧迫性表述",
    "causal_claim": "因果关系", "legal_consequence": "处置结果",
    "official_statement": "官方表态", "recommendation": "处置建议",
    "number_internal": "文内数字一致性", "omission": "关键限定缺失",
    "sensitive_addition": "挑动性内容添加", "media_identity": "媒体标识",
}


def scaled_config(scale):
    if scale == 1:
        return QUOTAS
    q = json.loads(json.dumps(QUOTAS))
    for c in q["carriers"]:
        q["carriers"][c]["groups"] *= scale
    for r in q["regions"]:
        q["regions"][r]["groups"] *= scale
    q["total_groups"] = QUOTAS["total_groups"] * scale
    return q


def build_records(limit=None, scale=1, with_fields=False):
    """Build prompt records, optionally from a scaled quota plan."""
    original = common.QUOTAS
    common.QUOTAS = scaled_config(scale)
    try:
        plan = build_plan()
    finally:
        common.QUOTAS = original

    if limit:
        plan = plan[:limit]

    from content import build_base_content
    from render import build_prompt, build_prompt_en
    from variants import derive_variants
    from common import PROMPT_TEMPLATES, collect_visible_text, count_density

    records = []
    for group in plan:
        layout = common.LAYOUTS[group["carrier"]][group["layout_id"]]
        group["region_name"] = REGION_NAMES.get(group["region"], group["region"])
        group["hazard_name"] = HAZARD_NAMES.get(group["hazard"], group["hazard"])

        base_fields, meta = build_base_content(group, layout)
        group["meta"] = meta
        variants = derive_variants(base_fields, meta, group)

        carrier_desc = PROMPT_TEMPLATES["carrier_descriptions"][group["carrier"]]
        realism_desc = PROMPT_TEMPLATES["realism_descriptions"]["native_screenshot"]
        normal_desc = PROMPT_TEMPLATES["normal_descriptions"][group["carrier"]]
        style = VISUAL_FAMILY.get(group["platform_family"], "")

        for variant in VARIANTS:
            rec = variants[variant]
            # Density must be computed before rendering: the prompt states a
            # character-count target, and rendering it first left the value at
            # zero for every sample.
            density, measured, unit = count_density(collect_visible_text(rec["fields"]))
            group["text_density"] = density
            group["measured_char_count"] = measured

            if group["language"] == "en":
                text = build_prompt_en(group, layout, rec, group["carrier"], "native_screenshot")
            else:
                text = build_prompt(group, layout, rec, carrier_desc, realism_desc,
                                    normal_desc, style)
            row = {
                "prompt_id": f"{group['group_id']}-{variant}",
                "group_id": group["group_id"],
                "carrier": group["carrier"],
                "sub_carrier": group["sub_carrier"],
                "platform_family": group["platform_family"],
                "layout_id": group["layout_id"],
                "aspect_ratio": group["aspect_ratio"],
                "capture_style": "native_screenshot",
                "region": group["region"],
                "language": group["language"],
                "hazard": group["hazard"],
                "variant": variant,
                "split": group["split"],
                "text_density": density,
                "measured_char_count": measured,
                "density_unit": unit,
                "field_count": len([f for f in rec["fields"] if f["value"]]),
                "changed_fields": rec["changed_fields"],
                "field_changes": rec["field_changes"],
                "tamper_types": rec["tamper_types"],
                "anomaly_category": rec["anomaly_category"],
                "changed_field_count": rec["changed_field_count"],
                "rule_failure_count": rec["rule_failure_count"],
                "collateral_failure_count": rec["collateral_failure_count"],
            "single_image_detectable": rec["single_image_detectable"],
            "truth_status": rec.get("truth_status", "true"),
            "content_mode": rec.get(
                "content_mode",
                "real_true_news" if variant == "clean" else "real_news_with_internal_conflict",
            ),
            "source_event_id": meta["real_event"]["event_id"],
            "source_title": meta["real_event"]["title_en" if group["language"] == "en" else "title_zh"],
            "source_urls": [meta["real_event"]["source_url"]],
            "fabrication_method": rec.get("fabrication_method", ""),
                "prompt": text,
            }
            if with_fields:
                row["fields"] = rec["fields"]
                row["visible_text"] = collect_visible_text(rec["fields"])
            records.append(row)
    return records


def metadata_lines(i, r, with_fields=False, index=True):
    """Return the metadata block for one record."""
    out = []
    num = f"{i:05d} | " if index else ""
    out.append(f"# {num}{r['prompt_id']} | {r['carrier']} | {r['language']} "
               f"| {r['region']} | {r['hazard']} | {r['variant']}")

    tier = (f"# tier: {r['variant']} ({r['changed_field_count']} changed fields, "
            f"{r['rule_failure_count']} rule violations")
    if r["collateral_failure_count"]:
        tier += f", {r['collateral_failure_count']} collateral"
    tier += ")"
    out.append(tier)

    out.append(f"# carrier: {r['carrier']} {CARRIER_NAMES.get(r['carrier'], '')}"
               f" / {r['sub_carrier']} | platform: {r['platform_family']}")
    out.append(f"# layout: {r['layout_id']} | aspect: {r['aspect_ratio']}"
               f" | capture: {r['capture_style']}")
    out.append(f"# region: {r['region']} {REGION_NAMES.get(r['region'], '')}"
               f" | language: {r['language']}"
               f" | hazard: {r['hazard']} {HAZARD_NAMES.get(r['hazard'], '')}")
    out.append(f"# density: {r['text_density']} ({r['measured_char_count']} chars, "
               f"{r['density_unit']}) | fields: {r['field_count']} | split: {r['split']}")
    out.append(f"# content: {r.get('content_mode', '')} | truth: {r.get('truth_status', '')}"
               f" | source_event: {r.get('source_event_id', '')}")
    if r.get("ui_prompt_mode"):
        out.append(f"# UI prompt mode: {r['ui_prompt_mode']}")
    if r.get("ui_reference_image"):
        out.append(f"# UI reference attachment: {r['ui_reference_image']}")
    if r.get("ui_reference_url"):
        out.append(f"# UI reference URL: {r['ui_reference_url']}")

    if r["tamper_types"]:
        types = ", ".join(f"{t}({ANOMALY_LABELS.get(t, t)})" for t in r["tamper_types"])
        rules = ", ".join(f"{c}({RULE_LABELS.get(c, c)})" for c in r["anomaly_category"])
        out.append(f"# tamper: {types}")
        out.append(f"# rules: {rules}")
        out.append(f"# changed: {', '.join(r['changed_fields'])}")
        for c in r["field_changes"]:
            lbl = c["label"] or c["field"]
            before = c["base_value"] or "（无）"
            after = c["value"] or "（已删除）"
            out.append(f"#   {lbl}：「{before}」→「{after}」")
        out.append(f"# single_image_detectable: {r['single_image_detectable']}")
    else:
        out.append("# tamper: none")
        out.append("# single_image_detectable: null")
    if r.get("fabrication_method"):
        out.append(f"# fabrication: {r['fabrication_method']}")

    if with_fields:
        out.append("# visible_text (应当出现的逐字文字):")
        for t in r.get("visible_text", []):
            out.append(f"#   「{t}」")
    return out


def export(records, out_path, mode="full-meta", index=True, with_fields=False):
    """Write records. mode: 'bare' | 'full-meta' | 'header-only'."""
    lines = []
    for i, r in enumerate(records, 1):
        if mode == "bare":
            lines.append(r["prompt"])
        else:
            if mode == "full-meta":
                lines.extend(metadata_lines(i, r, with_fields=with_fields, index=index))
            elif mode == "header-only":
                prefix = f"# {i:05d} | " if index else "# "
                lines.append(f"{prefix}{r['prompt_id']} | {r['carrier']} | {r['language']}"
                             f" | {r['region']} | {r['hazard']} | {r['variant']}")
            if mode == "full-meta":
                lines.append("# " + "-" * 68)
            lines.append(r["prompt"])
        lines.append("")                      # blank line between blocks
    text = "\n".join(lines).rstrip() + "\n"
    Path(out_path).write_text(text, encoding="utf-8")
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=int, default=None,
                    help="target number of prompts (e.g. 30000)")
    ap.add_argument("--limit", type=int, default=None,
                    help="cap the number of base groups")
    ap.add_argument("--out", default=None, help="output .txt path")
    ap.add_argument("--full", action="store_true",
                    help="also list the verbatim text specification (visible_text)")
    ap.add_argument("--header-only", action="store_true",
                    help="emit a single metadata line instead of the full block")
    ap.add_argument("--no-header", action="store_true",
                    help="omit the metadata block entirely")
    ap.add_argument("--bare", action="store_true",
                    help="emit prompt text only, separated by a blank line")
    args = ap.parse_args()

    if args.target:
        if args.target % len(VARIANTS):
            sys.exit(f"--target must be a multiple of {len(VARIANTS)} ({len(VARIANTS)} variants per group)")
        groups_needed = args.target // len(VARIANTS)
        base_groups = QUOTAS["total_groups"]
        if groups_needed % base_groups:
            sys.exit(f"--target must be a multiple of {base_groups * len(VARIANTS)} "
                     f"(the base design has {base_groups} groups)")
        scale = groups_needed // base_groups
    else:
        scale = 1

    records = build_records(limit=args.limit, scale=scale, with_fields=args.full)

    if args.bare:
        mode = "bare"
    elif args.no_header:
        mode = "bare"
    elif args.header_only:
        mode = "header-only"
    else:
        mode = "full-meta"

    if args.out:
        out_path = args.out
    else:
        out_path = BASE_DIR / "final" / f"news_rumor_prompts_{len(records)}.txt"

    export(records, out_path, mode=mode, index=not args.bare, with_fields=args.full)

    size = Path(out_path).stat().st_size
    print(f"records : {len(records)}")
    print(f"groups  : {len(records) // len(VARIANTS)}")
    print(f"scale   : {scale}x")
    print(f"mode    : {mode}")
    print(f"output  : {out_path}")
    print(f"size    : {size / 1024 / 1024:.1f} MB")


if __name__ == "__main__":
    main()
