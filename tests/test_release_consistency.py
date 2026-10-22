"""Independent consistency tests.

These recompute the dataset's invariants from the delivered files rather than
trusting the generator's own report.
"""

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

from common import QUOTAS, VARIANT_RULES  # noqa: E402

FINAL = BASE_DIR / "final"
VARIANTS = ["clean", "fabricated", "strong", "subtle"]


def load():
    prompts = [json.loads(l) for l in open(FINAL / "news_rumor_prompts_3000.jsonl",
                                           encoding="utf-8")]
    groups = [json.loads(l) for l in open(FINAL / "groups.jsonl", encoding="utf-8")]
    return groups, prompts


def test_counts():
    groups, prompts = load()
    assert len(groups) == QUOTAS["total_groups"], len(groups)
    assert len(prompts) == QUOTAS["total_groups"] * 4
    for cid, spec in QUOTAS["carriers"].items():
        n = sum(1 for g in groups if g["carrier"] == cid)
        assert n == spec["groups"], f"{cid}: {n} != {spec['groups']}"


def test_triplets():
    _, prompts = load()
    per = defaultdict(list)
    for p in prompts:
        per[p["group_id"]].append(p["variant"])
    for gid, vs in per.items():
        assert sorted(vs) == VARIANTS, gid


def test_variant_tiers():
    _, prompts = load()
    for p in prompts:
        cc, rc, v = p["changed_field_count"], p["rule_failure_count"], p["variant"]
        if v == "clean":
            assert cc == 0 and rc == 0, p["prompt_id"]
        elif v == "fabricated":
            assert cc == 0 and rc == 0, p["prompt_id"]
        elif v == "subtle":
            assert 1 <= cc <= 2 and 1 <= rc <= 2, p["prompt_id"]
        else:
            assert cc >= 2 and rc >= 2, p["prompt_id"]


def test_group_consistency():
    _, prompts = load()
    fields = ["carrier", "sub_carrier", "platform_family", "layout_id", "region",
              "language", "hazard", "aspect_ratio", "capture_style", "split"]
    per = defaultdict(list)
    for p in prompts:
        per[p["group_id"]].append(p)
    for gid, items in per.items():
        for f in fields:
            assert len({i[f] for i in items}) == 1, f"{gid}:{f}"


def test_split_atomicity():
    _, prompts = load()
    per = defaultdict(set)
    for p in prompts:
        per[p["group_id"]].add(p["split"])
    for gid, s in per.items():
        assert len(s) == 1, gid


def test_split_ratios():
    groups, _ = load()
    c = Counter(g["split"] for g in groups)
    total = len(groups)
    for name in ("train", "validation", "test"):
        assert c[name] > 0, name
    assert abs(c["train"] / total - 0.80) < 0.05


def test_visible_text_nonempty():
    _, prompts = load()
    for p in prompts:
        if p["variant"] == "clean":
            assert all(f["value"] for f in p["fields"]), p["prompt_id"]


def test_forbidden_text():
    _, prompts = load()
    forbidden = {t.lower() for t in VARIANT_RULES["forbidden_visible_text"]}
    for p in prompts:
        for t in p["visible_text"]:
            assert t.strip().lower() not in forbidden, f"{p['prompt_id']}:{t}"


def test_changed_fields_traceable():
    _, prompts = load()
    for p in prompts:
        if p["variant"] in ("clean", "fabricated"):
            assert p["changed_fields"] == [] and p["field_changes"] == []
            continue
        declared = {c["field"] for c in p["field_changes"]}
        assert declared == set(p["changed_fields"]), p["prompt_id"]
        assert len(p["tamper_types"]) >= 1
        assert len(p["anomaly_category"]) >= 1


def test_prompt_self_contained():
    _, prompts = load()
    for p in prompts:
        minimum = 100 if p.get("ui_prompt_mode") in ("image_text", "short_text") else 400
        assert len(p["prompt"]) > minimum, p["prompt_id"]
        assert p["source_title"] in p["prompt"], p["prompt_id"]
        notice = "Safety and purpose notice" if p["language"] == "en" else "用途声明"
        assert notice in p["prompt"], p["prompt_id"]
        assert ("DO NOT render" if p["language"] == "en" else "严禁渲染") in p["prompt"], p["prompt_id"]


def test_interaction_metrics_have_meaningful_labels():
    _, prompts = load()
    expected = {
        "like_metric": ("点赞数", "Likes"),
        "comment_metric": ("评论数", "Comments"),
        "repost_metric": ("转发数", "Reposts"),
        "view_metric": ("浏览量", "Views"),
        "save_metric": ("收藏数", "Saves"),
    }
    for p in prompts:
        if p.get("ui_prompt_mode") not in ("image_text", "short_text"):
            continue
        keys = {f.get("key") for f in p["fields"]}
        for key, (zh, en) in expected.items():
            if key in keys:
                assert (zh if p["language"] != "en" else en) in p["prompt"], (p["prompt_id"], key)


def test_reference_url_fallback_instruction():
    _, prompts = load()
    for p in prompts:
        if p.get("ui_prompt_mode") != "image_text":
            continue
        url = p.get("ui_reference_url", "")
        if url:
            heading = "Reference page: " if p["language"] == "en" else "参考网页："
            expected = f"{heading}{url}\n若无法访问该网站，则忽略此网址"
            assert expected in p["prompt"], p["prompt_id"]
        else:
            assert "参考网页：" not in p["prompt"], p["prompt_id"]
            assert "Reference page:" not in p["prompt"], p["prompt_id"]


def test_truth_modes():
    _, prompts = load()
    per = defaultdict(list)
    for p in prompts:
        per[p["group_id"]].append(p)
    for gid, items in per.items():
        true_items = [p for p in items if p["truth_status"] == "true"]
        false_items = [p for p in items if p["truth_status"] == "false"]
        assert len(true_items) == 3, gid
        assert len(false_items) == 1, gid
        assert false_items[0]["variant"] == "fabricated", gid
        assert false_items[0]["content_mode"] == "fabricated_rumor_self_consistent", gid
        assert all(p["source_urls"] for p in items), gid


def test_language_region_quota():
    groups, _ = load()
    for rid, spec in QUOTAS["regions"].items():
        n = sum(1 for g in groups if g["region"] == rid)
        assert abs(n - spec["groups"]) <= 6, f"{rid}: {n} vs {spec['groups']}"


def test_carrier_region_coverage():
    groups, _ = load()
    rule = QUOTAS["region_coverage_rule"]
    for cid in QUOTAS["carriers"]:
        sub = [g for g in groups if g["carrier"] == cid]
        regs = {g["region"] for g in sub}
        langs = {g["language"] for g in sub}
        assert len(regs) >= rule["min_distinct_regions_per_carrier"], cid
        for lang in rule["required_languages_per_carrier"]:
            assert lang in langs, f"{cid} missing {lang}"


def test_hazard_quota():
    groups, _ = load()
    hc = Counter(g["hazard"] for g in groups)
    total = len(groups)
    core = sum(hc.get(k, 0) for k in QUOTAS["hazard_constraints"]["core_group"])
    assert core / total >= QUOTAS["hazard_constraints"]["core_group_min_share"] - 0.02
    assert max(hc.values()) / total <= QUOTAS["hazard_constraints"]["single_hazard_max_share"] + 0.01
    for cid in QUOTAS["carriers"]:
        n = len({g["hazard"] for g in groups if g["carrier"] == cid})
        assert n >= QUOTAS["hazard_constraints"]["min_distinct_hazards_per_carrier"], cid


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  pass  {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"  FAIL  {t.__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)
