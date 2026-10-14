"""Variant derivation.

Derives `clean`, `subtle` and `strong` field sets from one base field set.

Mutations are declared against **field roles**, and each mutation can name
several candidate roles; the first role actually present in the layout is used.
This keeps every layout group capable of producing all three tiers regardless of
which sections that layout declares.

Tier definitions come from config/variant_rules.json and are frozen.
"""

from common import rng_for

# Each mutation: candidate field roles (first present wins), the content anomaly
# types it produces, and the rule violations it creates.
MUTATIONS = {
    "timestamp_shift": {
        "roles": ["publish_time", "post_time", "post_datetime", "filing_time", "lead_timestamp", "date_line", "brief_date", "node1_time", "device_time", "progress_label"],
        "tamper_types": ["timestamp"], "anomaly_category": ["date_order"],
    },
    "metric_inflate": {
        "roles": ["metric", "view_metric", "like_metric", "read_metric", "viewer_metric", "topic_metric", "comment1_metric", "inner_metric", "comment_metric", "save_metric", "share_metric", "repost_metric", "reply_metric"],
        "tamper_types": ["metric"], "anomaly_category": ["number_relation"],
    },
    "attribution_swap": {
        "roles": ["attribution", "source_line", "source_note", "source_attribution", "review_note", "short_source_note"],
        "tamper_types": ["attribution"], "anomaly_category": ["attribution_chain"],
    },
    "omission_cut": {
        "roles": ["body_2", "paragraph2", "summary_line2", "point2_body", "commentary_line2", "subtitle_line2", "ticker_text", "panel_point2", "danmaku2", "inner_body_line2", "item2_body", "story2_headline"],
        "tamper_types": ["omission"], "anomaly_category": ["temporal_window"],
    },
    "number_mismatch": {
        "roles": ["sequence", "sequence_number", "issue_number", "issue_label", "page_number", "card_index", "node1_text"],
        "tamper_types": ["number_internal"], "anomaly_category": ["quantity_sum"],
    },
    "headline_conflict": {
        "roles": ["headline", "headline_banner", "lead_headline", "breaking_headline", "article_headline", "topic_title", "timeline_title", "card_topic", "panel_title", "item1_title", "case1_title", "summary_title"],
        "tamper_types": ["headline_body_conflict"], "anomaly_category": ["subject_agreement"],
    },
    "magnitude_boost": {
        "roles": ["body_1", "body_text", "paragraph1", "lead_summary", "column_body", "caption_text", "summary_line1", "subtitle_line1", "detail_line1", "panel_point1", "danmaku1", "inner_body_line1", "lead_body", "item1_body"],
        "tamper_types": ["magnitude"], "anomaly_category": ["number_relation"],
    },
    "urgency_insert": {
        "roles": ["hashtags", "hashtag_row", "topic_tag", "segment_tag", "live_label", "urgency_tag", "audio_name", "status_icons", "input_placeholder"],
        "tamper_types": ["urgency", "sensitive_addition"], "anomaly_category": ["fixed_text"],
    },
    "official_fabricate": {
        "roles": ["attribution", "editor_note", "compiler_note", "disclaimer_line", "platform_statement", "transmission_note", "update_note", "source_label", "source_line", "review_note", "contact_line", "footer_note", "transmission_note", "compiler_note", "commentary_line1", "danmaku3"],
        "tamper_types": ["official_statement"], "anomaly_category": ["attribution_chain"],
    },
    "location_swap": {
        "roles": ["location", "location_label", "dateline", "case1_location", "status_source", "detail_line1"],
        "tamper_types": ["location"], "anomaly_category": ["geographic_plausibility"],
    },
    "identity_swap": {
        "roles": ["account_name", "display_name", "author_name", "host_name", "publisher_name", "site_name", "outlet_name", "account_handle", "handle", "channel_name", "newspaper_name", "brand_strip", "agency_name", "app_name"],
        "tamper_types": ["account_identity"], "anomaly_category": ["attribution_chain"],
    },
    "legal_fabricate": {
        "roles": ["conclusion_body", "detail_line3", "item2_body", "point3_body", "quote_line", "node4_text", "panel_point3", "subtitle_line3", "item3_body", "point3_body", "case3_body", "story3_headline", "node3_text"],
        "tamper_types": ["legal_consequence"], "anomaly_category": ["set_relation"],
    },
}

SUBTLE_MUTATIONS = ["timestamp_shift", "metric_inflate", "attribution_swap", "omission_cut", "number_mismatch"]
STRONG_MUTATIONS = ["headline_conflict", "magnitude_boost", "urgency_insert", "official_fabricate",
                    "location_swap", "identity_swap", "legal_fabricate"]


def _find(fields, roles):
    present = {f["key"]: f for f in fields}
    for r in roles:
        if r in present:
            return present[r]
    return None


def _date_token(language, rng):
    if language.startswith("zh"):
        return f"{rng.randrange(2024, 2028)}年{rng.randrange(1, 13)}月{rng.randrange(1, 29)}日"
    return f"{rng.randrange(1, 13)}/{rng.randrange(1, 29)}/{rng.randrange(2024, 2028)}"


def _metric_like(base, language, rng):
    big = rng.randrange(1200, 9800)
    if "K" in base and not language.startswith("zh"):
        return f"{big}K views"
    suffix = ""
    for cand in ("次讨论", "則討論", "次閱讀", "次阅读", "则讨论", "次浏览", "人在看", "次", "則"):
        if cand in base:
            suffix = cand
            break
    if not suffix and language == "zh-Hant":
        suffix = "則"
    if not suffix and language == "zh-Hans":
        suffix = "次"
    return f"{big}{suffix}"


def apply_mutation(name, fields, meta, language, rng):
    """Apply one mutation in place. Return change records, or None if N/A."""
    spec = MUTATIONS[name]
    f = _find(fields, spec["roles"])
    if f is None:
        return None
    base = f["value"]
    if not base:
        return None
    changed = []

    if name == "timestamp_shift":
        tail = base.split(" ")[-1] if " " in base else meta["time"]
        new = f"{_date_token(language, rng)} {tail}"

    elif name == "metric_inflate":
        new = _metric_like(base, language, rng)

    elif name == "attribution_swap":
        alt = meta["outlet_name"]
        if language == "zh-Hant":
            new = f"資料來源：{alt}"
        elif language == "zh-Hans":
            new = f"信息来源：{alt}"
        else:
            new = f"Source: {alt}"

    elif name == "omission_cut":
        new = ""

    elif name == "number_mismatch":
        n = rng.randrange(1000, 9999)
        if language == "zh-Hant":
            new = f"編號 {n}"
        elif language == "zh-Hans":
            new = f"编号 {n}"
        else:
            new = f"REF-{n}"

    elif name == "headline_conflict":
        t = meta["subject_title"]
        if language == "zh-Hant":
            new = f"{t}　相關單位表示情況已完全控制"
        elif language == "zh-Hans":
            new = f"{t}　相关部门表示情况已完全控制"
        else:
            new = f"{t.title()}: situation fully under control, officials say"

    elif name == "magnitude_boost":
        if language == "zh-Hant":
            new = base + "據初步統計，受影響範圍涉及周邊十餘個社區。"
        elif language == "zh-Hans":
            new = base + "据初步统计，受影响范围涉及周边十余个社区。"
        else:
            new = base + " Initial estimates indicate more than a dozen surrounding districts are affected."

    elif name == "urgency_insert":
        if language == "zh-Hant":
            new = base + " #緊急 #速轉擴散"
        elif language == "zh-Hans":
            new = base + " #紧急 #速转扩散"
        else:
            new = base + " #urgent #sharenow"

    elif name == "official_fabricate":
        inst = meta["institution"]
        if language == "zh-Hant":
            new = base + f" {inst}已確認上述訊息屬實，並將於近期發布正式通報。"
        elif language == "zh-Hans":
            new = base + f" {inst}已确认上述信息属实，并将于近期发布正式通告。"
        else:
            new = base + f" {inst} has confirmed the information and will issue a formal notice shortly."

    elif name == "location_swap":
        if language == "zh-Hant":
            new = base + "（另有說法指向不同轄區）"
        elif language == "zh-Hans":
            new = base + "（另有说法指向不同辖区）"
        else:
            new = base + " (an alternate account places the event elsewhere)"

    elif name == "identity_swap":
        new = base + ("官方" if language.startswith("zh") else " Official")

    elif name == "legal_fabricate":
        if language == "zh-Hant":
            new = "涉案人員已被依法處以行政拘留，案件正在進一步辦理中。"
        elif language == "zh-Hans":
            new = "涉事人员已被依法处以行政拘留，案件正在进一步办理中。"
        else:
            new = "The individuals involved have been formally detained and the case remains under investigation."

    else:
        return None

    f["value"] = new
    changed.append({"field": f["key"], "label": f["label"], "base_value": base, "value": new})
    return changed


def derive_variants(base_fields, meta, group):
    """Return the three variant field sets plus their annotation records."""
    language = group["language"]
    results = {}

    results["clean"] = {
        "fields": [dict(f) for f in base_fields],
        "changed_fields": [], "field_changes": [],
        "tamper_types": [], "anomaly_category": [],
        "changed_field_count": 0, "rule_failure_count": 0,
        "collateral_failure_count": 0, "single_image_detectable": None,
    }

    plan = {
        "subtle": (SUBTLE_MUTATIONS, 2),
        "strong": (STRONG_MUTATIONS, 3),
    }

    for variant, (pool, n_want) in plan.items():
        fields = [dict(f) for f in base_fields]
        changes, ttypes, acats = [], set(), set()
        # Try mutations in a shuffled order until the tier target is met.
        for attempt in range(6):
            rng = rng_for("variant", group["group_id"], variant, attempt)
            order = pool[:]
            rng.shuffle(order)
            changes, ttypes, acats = [], set(), set()
            used = set()
            for m in order:
                if m in used:
                    continue
                rec = apply_mutation(m, fields, meta, language, rng)
                if rec:
                    used.add(m)
                    changes.extend(rec)
                    ttypes.update(MUTATIONS[m]["tamper_types"])
                    acats.update(MUTATIONS[m]["anomaly_category"])
                cc = len({c["field"] for c in changes})
                rc = len(acats)
                target = n_want if variant == "strong" else 2
                if cc >= target and rc >= target:
                    break
            cc = len({c["field"] for c in changes})
            rc = len(acats)
            lo = 2 if variant == "strong" else 1
            if cc >= lo and rc >= lo:
                break

        results[variant] = {
            "fields": fields,
            "changed_fields": [c["field"] for c in changes],
            "field_changes": changes,
            "tamper_types": sorted(ttypes),
            "anomaly_category": sorted(acats),
            "changed_field_count": len({c["field"] for c in changes}),
            "rule_failure_count": len(acats),
            "collateral_failure_count": 0,
            "single_image_detectable": True,
        }
    return results
