"""Entry point: build the full prompt dataset.

Usage:
    python3 src/generate.py                 # full 1000 groups / 3000 prompts
    python3 src/generate.py --limit 40      # pilot subset

Outputs (under final/):
    news_rumor_prompts_3000.jsonl   one record per prompt
    news_rumor_prompts_3000.csv     flattened view
    groups.jsonl                    one record per base group
    qa_report.json                  machine-readable validation results
    qa_report.md                    human-readable validation results
    release_manifest.json           counts, hashes, frozen-threshold hash
"""

import argparse
import copy
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import (  # noqa: E402
    CONSTRAINTS, FICTION, LAYOUTS, PROMPT_TEMPLATES, QUOTAS, VARIANT_RULES,
    build_plan, collect_visible_text, count_density, frozen_threshold_hash, stable_hash,
)
from content import build_base_content  # noqa: E402
from render import _trim_coherent, build_prompt, build_prompt_en, limit_long_body_fields  # noqa: E402
from variants import derive_variants  # noqa: E402
from ui_prompt_modes import (  # noqa: E402
    append_safety_notice, assign_prompt_modes, build_reference_prompt, reference_for, reference_overrides,
    compact_location_label, reference_layout_instruction, topic_search_phrase,
)
from ui_template_specs import TEMPLATE_SPECS  # noqa: E402

REGION_NAMES = {
    "CN": "中国内地", "NA": "北美地区", "UK": "英国", "AU": "澳大利亚",
    "TW": "台湾地区", "HK": "香港地区", "SG": "新加坡",
}
HAZARD_NAMES = {k: v["name_zh"] for k, v in QUOTAS["hazards"].items()}
VARIANT_ORDER = ("clean", "subtle", "strong", "fabricated")

VISUAL_STYLE_BY_FAMILY = {
    "cn_social": "中文社交平台的界面风格，信息层级清晰，卡片式布局，圆角与浅灰分隔线",
    "en_social": "英文社交平台的界面风格，留白充足，细边框分隔，字体层级分明",
    "image_social": "图片社交平台的界面风格，作者条置顶，操作图标成排，说明文字紧随其后",
    "short_video": "短视频平台的竖屏界面风格，字幕居中叠加，界面元素半透明浮于画面之上",
    "news_media": "新闻媒体的播出与排版风格，区块分明，标题字重突出，配色沉稳",
}


def build_records(limit=None):
    plan = build_plan()
    # Assign modes over the full frozen plan so a pilot subset keeps the same
    # per-group decisions as the eventual full release.
    prompt_modes = assign_prompt_modes(plan)
    if limit:
        plan = plan[:limit]

    prompts = []
    groups = []

    for group in plan:
        carrier = group["carrier"]
        layout = LAYOUTS[carrier][group["layout_id"]]
        group["region_name"] = REGION_NAMES.get(group["region"], group["region"])
        group["hazard_name"] = HAZARD_NAMES.get(group["hazard"], group["hazard"])

        base_fields, meta = build_base_content(group, layout)
        group["meta"] = meta
        variants = derive_variants(base_fields, meta, group)

        carrier_desc = PROMPT_TEMPLATES["carrier_descriptions"][carrier]
        realism_desc = PROMPT_TEMPLATES["realism_descriptions"]["native_screenshot"]
        normal_desc = PROMPT_TEMPLATES["normal_descriptions"][carrier]
        visual_style_desc = VISUAL_STYLE_BY_FAMILY.get(group["platform_family"], "")

        group_record = {
            "group_id": group["group_id"],
            "carrier": carrier,
            "sub_carrier": group["sub_carrier"],
            "platform_family": group["platform_family"],
            "layout_id": group["layout_id"],
            "region": group["region"],
            "language": group["language"],
            "hazard": group["hazard"],
            "aspect_ratio": group["aspect_ratio"],
            "capture_style": "native_screenshot",
            "split": group["split"],
            "fictional_entity_note": "机构、媒体、地名、人名、编号均为虚构。",
            "variants": list(VARIANT_ORDER),
            "source_event_id": meta["real_event"]["event_id"],
            "source_urls": [meta["real_event"]["source_url"]],
            "ui_prompt_mode": prompt_modes.get(group["group_id"], "long_quantified"),
        }
        groups.append(group_record)

        for variant in VARIANT_ORDER:
            rec = variants[variant]
            fields = rec["fields"]
            # Rendering needs the selected mode so long prompts can consolidate
            # continuation/caption copy before the final prompt is assembled.
            group["ui_prompt_mode"] = prompt_modes.get(group["group_id"], "long_quantified")
            ui_mode = prompt_modes.get(group["group_id"])
            available_reference = reference_for(group) if ui_mode else None
            selected_template = available_reference["file"] if available_reference else ""
            group["ui_reference_template"] = selected_template
            reference_details_text = ""
            if ui_mode == "long_quantified" and available_reference:
                reference_details_text = reference_overrides(
                    group, copy.deepcopy(fields), available_reference, group["language"],
                    image_key=f"{group['group_id']}-{variant}",
                )
            fields = limit_long_body_fields(
                fields, layout, group["language"], group["layout_id"], selected_template
            )
            if ui_mode == "long_quantified" and not any(
                f.get("key", "").startswith(("body", "note_line", "inline_note", "extended_body", "caption_text"))
                for f in fields if f.get("value")
            ):
                fallback_title = group["meta"].get("subject_title", "").strip()
                if fallback_title:
                    fields.append({"key": "body_text", "label": "正文", "value": fallback_title})
                    fields = limit_long_body_fields(fields, layout, group["language"], group["layout_id"], selected_template)
            if selected_template == "douyin-mobile-video.png":
                allowed = {"body_text", "caption_text", "location", "location_label", "audio_name",
                           "like_metric", "comment_metric", "share_metric", "save_metric", "view_metric"}
                fields = [f for f in fields if f.get("key") in allowed]
                for field in fields:
                    if field["key"] in {"body_text", "caption_text"}:
                        field["value"] = _trim_coherent(field.get("value", ""), 42, group["language"])
                    elif field["key"] in {"location", "location_label"}:
                        field["value"] = compact_location_label(
                            field.get("value", ""), group["language"],
                            18 if group["language"] != "en" else 32,
                        )
                    elif field["key"] == "audio_name":
                        audio_cap = 24 if group["language"] != "en" else 40
                        audio = str(field.get("value", "")).strip()
                        field["value"] = audio if len(audio) <= audio_cap else (
                            "原声" if group["language"] != "en" else "Original audio"
                        )
                fields = [f for f in fields if f.get("value")]
                if not any(f.get("key") in {"body_text", "caption_text"} for f in fields):
                    fields.append({
                        "key": "caption_text",
                        "label": "配文" if group["language"] != "en" else "Caption",
                        "value": topic_search_phrase(
                            group["meta"]["real_event"]["title_en" if group["language"] == "en" else "title_zh"],
                            group["language"],
                        ),
                    })
                fields.append({
                    "key": "search_phrase",
                    "label": "搜索框文案" if group["language"] != "en" else "Search-box text",
                    "value": topic_search_phrase(meta["real_event"]["title_en" if group["language"] == "en" else "title_zh"], group["language"]),
                })
            if ui_mode == "long_quantified" and not any(
                f.get("key", "").startswith(("body", "note_line", "inline_note", "extended_body", "caption_text"))
                for f in fields if f.get("value")
            ):
                fallback_title = meta["real_event"]["title_en" if group["language"] == "en" else "title_zh"]
                fields.append({"key": "body_text", "label": "正文", "value": fallback_title})
            render_record = dict(rec)
            render_record["fields"] = fields
            visible = collect_visible_text(fields)
            density, measured, unit = count_density(visible)
            # Density must be known before rendering so the prompt can state a
            # text-volume target.
            group["text_density"] = density
            group["measured_char_count"] = measured

            if group["language"] == "en":
                prompt_text = build_prompt_en(
                    group, layout, render_record, carrier, "native_screenshot"
                )
            else:
                prompt_text = build_prompt(
                    group, layout, render_record, carrier_desc, realism_desc, normal_desc, visual_style_desc
                )

            ui_reference = available_reference
            if ui_mode in ("image_text", "short_text") and available_reference:
                prompt_text = build_reference_prompt(
                    group, fields, available_reference, group["language"], ui_mode,
                    image_key=f"{group['group_id']}-{variant}",
                )
            elif available_reference:
                prompt_text = (reference_layout_instruction(available_reference, group["language"])
                               + "\n" + prompt_text
                               + ("\n" + reference_details_text if reference_details_text else ""))
            prompt_text = append_safety_notice(prompt_text, group["language"])
            ui_render_data = group.pop("_ui_render_data", {})

            prompt_id = f"{group['group_id']}-{variant}"
            prompts.append({
                "prompt_id": prompt_id,
                "group_id": group["group_id"],
                "variant": variant,
                "carrier": carrier,
                "sub_carrier": group["sub_carrier"],
                "platform_family": group["platform_family"],
                "layout_id": group["layout_id"],
                "region": group["region"],
                "language": group["language"],
                "hazard": group["hazard"],
                "aspect_ratio": group["aspect_ratio"],
                "capture_style": "native_screenshot",
                "split": group["split"],
                "text_density": density,
                "measured_char_count": measured,
                "density_unit": unit,
                "field_count": len(fields),
                "fields": fields,
                "required_fields": [f["label"] for f in fields if f["label"]],
                "visible_text": visible,
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
                "fictional_entity_note": "机构、媒体、地名、人名、编号均为虚构。",
                "ui_prompt_mode": ui_mode or "long_quantified",
                "ui_reference_image": ui_reference["image"] if ui_reference and ui_mode != "short_text" else "",
                "ui_reference_template": ui_reference["file"] if ui_reference else "",
                "ui_reference_url": ui_reference["url"] if ui_reference else "",
                "ui_render_data": ui_render_data,
                "prompt": prompt_text,
            })

    return groups, prompts


def validate(groups, prompts):
    """Prompt-level checks. Does not replace post-generation image checks."""
    report = {"errors": [], "checks": [], "stats": {}}

    ids = [p["prompt_id"] for p in prompts]
    if len(ids) != len(set(ids)):
        dupes = [k for k, v in Counter(ids).items() if v > 1][:10]
        report["errors"].append({"rule": "unique_prompt_id", "detail": dupes})

    # Triplet completeness
    per_group = defaultdict(list)
    for p in prompts:
        per_group[p["group_id"]].append(p["variant"])
    bad = [g for g, v in per_group.items() if sorted(v) != sorted(VARIANT_ORDER)]
    report["checks"].append({
        "rule_id": "triplet_integrity",
        "status": "pass" if not bad else "fail",
        "detail": f"{len(per_group)} groups checked" if not bad else bad[:10],
    })
    if bad:
        report["errors"].append({"rule": "triplet_integrity", "detail": bad[:10]})

    ui_by_group = {}
    for p in prompts:
        ui_by_group[p["group_id"]] = (p.get("ui_prompt_mode", "long_quantified"),
                                       bool(p.get("ui_reference_image")))
    ui_inconsistent = []
    for gid in per_group:
        rows = [p for p in prompts if p["group_id"] == gid]
        if len({p.get("ui_prompt_mode", "long_quantified") for p in rows}) > 1:
            ui_inconsistent.append(gid)
    report["checks"].append({
        "rule_id": "ui_prompt_mode_group_consistency",
        "status": "pass" if not ui_inconsistent else "fail",
        "detail": ui_inconsistent[:10] or "all variants share their group's prompt mode",
    })
    missing_ref = [p["prompt_id"] for p in prompts
                   if p.get("ui_prompt_mode") == "image_text"
                   and not p.get("ui_reference_image")]
    ref_groups = {p["group_id"] for p in prompts if p.get("ui_reference_template")}
    ref_modes = Counter(ui_by_group[g][0] for g in ref_groups)
    expected_ref_modes = {
        "image_text": round(len(ref_groups) * 0.60),
        "long_quantified": round(len(ref_groups) * 0.30),
    }
    expected_ref_modes["short_text"] = len(ref_groups) - sum(expected_ref_modes.values())
    mode_ratio_ok = all(ref_modes[m] == n for m, n in expected_ref_modes.items())
    allocation_is_full_release = len(groups) == QUOTAS["total_groups"]
    report["checks"].append({
        "rule_id": "ui_prompt_mode_reference_ratio",
        "status": ("pass" if mode_ratio_ok else "fail") if allocation_is_full_release else "skip",
        "detail": {"eligible_groups": len(ref_groups), "actual": dict(ref_modes),
                   "expected": expected_ref_modes,
                   "note": "ratio is checked on full releases; pilots retain full-plan group assignments"
                           if not allocation_is_full_release else "full release allocation"},
    })
    if allocation_is_full_release and not mode_ratio_ok:
        report["errors"].append({"rule": "ui_prompt_mode_reference_ratio",
                                 "detail": {"actual": dict(ref_modes), "expected": expected_ref_modes}})

    report["checks"].append({
        "rule_id": "ui_prompt_reference_present",
        "status": "pass" if not missing_ref else "fail",
        "detail": missing_ref[:10] or "all image-led and short-text modes have a reference asset",
    })

    # Variant tier definitions
    tier_fail = []
    for p in prompts:
        v, cc, rc = p["variant"], p["changed_field_count"], p["rule_failure_count"]
        if v == "clean" and (cc or rc):
            tier_fail.append(p["prompt_id"])
        elif v == "fabricated" and (cc or rc):
            tier_fail.append(p["prompt_id"])
        elif v == "subtle" and not (1 <= cc <= 2 and 1 <= rc <= 2):
            tier_fail.append(p["prompt_id"])
        elif v == "strong" and not (cc >= 2 and rc >= 2):
            tier_fail.append(p["prompt_id"])
    report["checks"].append({
        "rule_id": "variant_tier_definition",
        "status": "pass" if not tier_fail else "fail",
        "detail": f"{len(prompts)} prompts checked" if not tier_fail else tier_fail[:10],
    })
    if tier_fail:
        report["errors"].append({"rule": "variant_tier_definition", "detail": tier_fail[:10]})

    # Group consistency of structural fields
    structural = ["carrier", "sub_carrier", "platform_family", "layout_id", "region",
                  "language", "hazard", "aspect_ratio", "capture_style", "split"]
    incons = []
    for gid, items in per_group.items():
        for f in structural:
            if len({p[f] for p in prompts if p["group_id"] == gid}) > 1:
                incons.append(f"{gid}:{f}")
    report["checks"].append({
        "rule_id": "group_structural_consistency",
        "status": "pass" if not incons else "fail",
        "detail": incons[:10] or "all groups consistent",
    })

    # Forbidden visible text
    forbidden = set(t.lower() for t in VARIANT_RULES["forbidden_visible_text"])
    hits = []
    for p in prompts:
        for t in p["visible_text"]:
            if t.strip().lower() in forbidden:
                hits.append(f"{p['prompt_id']}:{t}")
    report["checks"].append({
        "rule_id": "forbidden_visible_text",
        "status": "pass" if not hits else "fail",
        "detail": hits[:10] or "none found",
    })

    # Split atomicity
    split_fail = [g for g, _ in per_group.items()
                  if len({p["split"] for p in prompts if p["group_id"] == g}) > 1]
    report["checks"].append({
        "rule_id": "split_group_atomicity",
        "status": "pass" if not split_fail else "fail",
        "detail": split_fail[:10] or "all groups atomic",
    })

    report["stats"] = {
        "groups": len(groups),
        "prompts": len(prompts),
        "by_variant": dict(Counter(p["variant"] for p in prompts)),
        "by_truth_status": dict(Counter(p["truth_status"] for p in prompts)),
        "by_content_mode": dict(Counter(p["content_mode"] for p in prompts)),
        "by_carrier": dict(Counter(p["carrier"] for p in prompts)),
        "by_region": dict(Counter(p["region"] for p in prompts)),
        "by_language": dict(Counter(p["language"] for p in prompts)),
        "by_hazard": dict(Counter(p["hazard"] for p in prompts)),
        "by_ui_prompt_mode": dict(Counter(p.get("ui_prompt_mode", "long_quantified") for p in prompts)),
        "ui_reference_backed_groups": len(ref_groups),
        "by_ui_prompt_mode_on_reference_groups": dict(ref_modes),
        "by_split": dict(Counter(p["split"] for p in prompts)),
        "by_density": dict(Counter(p["text_density"] for p in prompts)),
        "tamper_type_counts": dict(Counter(
            t for p in prompts for t in p["tamper_types"])),
    }
    return report


def write_outputs(groups, prompts, report, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)

    # Keep the plain-text release synchronized with the exact prompt strings
    # written to JSONL/CSV, including UI prompt modes and reference fallbacks.
    from export_txt import export as export_prompts_txt
    export_prompts_txt(
        prompts, out_dir / f"news_rumor_prompts_{len(prompts)}.txt", mode="full-meta"
    )

    with open(out_dir / "news_rumor_prompts_3000.jsonl", "w", encoding="utf-8") as fh:
        for p in prompts:
            fh.write(json.dumps(p, ensure_ascii=False) + "\n")

    with open(out_dir / "groups.jsonl", "w", encoding="utf-8") as fh:
        for g in groups:
            fh.write(json.dumps(g, ensure_ascii=False) + "\n")

    cols = ["prompt_id", "group_id", "variant", "carrier", "sub_carrier",
            "platform_family", "layout_id", "region", "language", "hazard",
            "aspect_ratio", "capture_style", "split", "text_density",
            "measured_char_count", "field_count", "changed_field_count",
            "rule_failure_count", "single_image_detectable",
            "truth_status", "content_mode", "source_event_id", "source_title",
            "source_urls", "fabrication_method", "tamper_types", "anomaly_category"]
    with open(out_dir / "news_rumor_prompts_3000.csv", "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for p in prompts:
            row = dict(p)
            row["tamper_types"] = "|".join(p["tamper_types"])
            row["anomaly_category"] = "|".join(p["anomaly_category"])
            row["source_urls"] = "|".join(p["source_urls"])
            w.writerow(row)

    write_unified_csv(prompts, out_dir / "news_rumor_prompts_unified.csv")

    with open(out_dir / "qa_report.json", "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=1)

    lines = ["# QA 报告", "", f"- 基础组：{report['stats']['groups']}",
             f"- 提示词：{report['stats']['prompts']}", ""]
    lines.append("## 检查项")
    lines.append("")
    lines.append("| 检查 | 结果 | 说明 |")
    lines.append("|---|---|---|")
    for c in report["checks"]:
        lines.append(f"| {c['rule_id']} | {c['status']} | {str(c['detail'])[:80]} |")
    lines.append("")
    lines.append("## 统计")
    lines.append("")
    for k, v in report["stats"].items():
        lines.append(f"- **{k}**：{v}")
    lines.append("")
    lines.append(f"- 错误数：{len(report['errors'])}")
    with open(out_dir / "qa_report.md", "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    manifest = {
        "dataset": "news_rumor_prompts_3000",
        "version": "1.0",
        "frozen_at": "2026-10-08",
        "counts": {
            "groups": len(groups),
            "prompts": len(prompts),
            "clean": sum(1 for p in prompts if p["variant"] == "clean"),
            "subtle": sum(1 for p in prompts if p["variant"] == "subtle"),
            "strong": sum(1 for p in prompts if p["variant"] == "strong"),
            "fabricated": sum(1 for p in prompts if p["variant"] == "fabricated"),
        },
        "prompts_sha256": stable_hash(prompts),
        "groups_sha256": stable_hash(groups),
        "frozen_quality_threshold_sha256": frozen_threshold_hash(),
        "quota_config_sha256": stable_hash(QUOTAS),
        "note": "配额、档位定义与质量分级阈值均在生成前冻结。",
    }
    with open(out_dir / "release_manifest.json", "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=1)
    return manifest


def write_unified_csv(prompts, out_path):
    cols = [
        "sample_id", "direction", "category_l1", "category_l2", "variant",
        "aspect_ratio", "prompt", "group_id", "target_texts", "tamper_types",
        "tamper_details", "extra_json", "prompt_type_code",
        "ui_reference_url", "ui_reference_image",
    ]
    with open(out_path, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for i, p in enumerate(prompts, 1):
            unified_variant = p["variant"] if p["variant"] in ("clean", "subtle", "strong") else "clean"
            unified_aspect = "16:9" if p["aspect_ratio"] == "16:10" else p["aspect_ratio"]
            details = []
            for c in p["field_changes"]:
                lbl = c["label"] or c["field"]
                details.append(f"{lbl}: {c['base_value']} -> {c['value']}")
            extra = {
                "original_prompt_id": p["prompt_id"],
                "original_variant": p["variant"],
                "carrier": p["carrier"],
                "sub_carrier": p["sub_carrier"],
                "platform_family": p["platform_family"],
                "layout_id": p["layout_id"],
                "original_aspect_ratio": p["aspect_ratio"],
                "region": p["region"],
                "language": p["language"],
                "hazard": p["hazard"],
                "split": p["split"],
                "text_density": p["text_density"],
                "measured_char_count": p["measured_char_count"],
                "truth_status": p["truth_status"],
                "content_mode": p["content_mode"],
                "source_event_id": p["source_event_id"],
                "source_title": p["source_title"],
                "source_urls": p["source_urls"],
                "ui_prompt_mode": p.get("ui_prompt_mode", "long_quantified"),
                "ui_reference_image": p.get("ui_reference_image", ""),
                "ui_reference_template": p.get("ui_reference_template", ""),
                "ui_reference_url": p.get("ui_reference_url", ""),
                "ui_render_data": p.get("ui_render_data", {}),
                "ui_content_fields": p.get("fields", []),
                "output_strategy": "complete_image_generation_with_template_reference"
                if p.get("ui_reference_image") else "prompt_only",
                "fabrication_method": p["fabrication_method"],
                "changed_fields": p["changed_fields"],
                "rule_failure_count": p["rule_failure_count"],
                "single_image_detectable": p["single_image_detectable"],
            }
            w.writerow({
                "sample_id": f"UI-{i:06d}",
                "direction": "ui",
                "category_l1": p["carrier"],
                "category_l2": p["sub_carrier"],
                "variant": unified_variant,
                "aspect_ratio": unified_aspect,
                "prompt": p["prompt"],
                "group_id": f"UI-{p['group_id']}",
                "target_texts": "|".join(t.replace("|", "｜") for t in p["visible_text"]),
                "tamper_types": "|".join(p["tamper_types"]),
                "tamper_details": "|".join(d.replace("|", "｜") for d in details),
                "extra_json": json.dumps(extra, ensure_ascii=False, sort_keys=True),
                "prompt_type_code": (
                    1 if p.get("ui_reference_image") else
                    3 if p.get("ui_prompt_mode") == "short_text" else 2
                ),
                "ui_reference_url": p.get("ui_reference_url", "") or "",
                "ui_reference_image": str((BASE_DIR / p["ui_reference_image"]).resolve())
                    if p.get("ui_reference_image") else "",
            })


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None,
                    help="build only the first N groups (pilot mode)")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    groups, prompts = build_records(limit=args.limit)
    report = validate(groups, prompts)

    out_dir = Path(args.out) if args.out else (
        BASE_DIR / ("pilot" if args.limit else "final"))
    manifest = write_outputs(groups, prompts, report, out_dir)

    print(f"groups={len(groups)} prompts={len(prompts)} errors={len(report['errors'])}")
    for c in report["checks"]:
        print(f"  {c['status']:>4}  {c['rule_id']}")
    print(f"written to {out_dir}")
    print(f"manifest: {json.dumps(manifest['counts'], ensure_ascii=False)}")


if __name__ == "__main__":
    main()
