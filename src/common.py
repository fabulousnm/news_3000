"""Shared helpers for the news-rumor prompt dataset generator.

Loads the frozen configuration, builds the quota plan, and provides the
text-specification primitives used to assemble prompts.
"""

import hashlib
import json
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"


def load_config(name):
    with open(CONFIG_DIR / name, "r", encoding="utf-8") as fh:
        return json.load(fh)


QUOTAS = load_config("quotas.json")
VARIANT_RULES = load_config("variant_rules.json")
ANOMALY_TYPES = load_config("anomaly_types.json")
FICTION = load_config("fiction_library.json")
CONSTRAINTS = load_config("constraints.json")
PROMPT_TEMPLATES = load_config("prompt_templates.json")

LAYOUTS = {}
for _carrier in ("R1", "R2", "R3", "R4"):
    LAYOUTS[_carrier] = load_config(f"layout_templates_{_carrier}.json")["layouts"]


# --------------------------------------------------------------------------
# Determinism
# --------------------------------------------------------------------------

MASTER_SEED = 20261008


def rng_for(*parts):
    """Stable RNG keyed by the given parts, independent of call order."""
    key = "|".join(str(p) for p in parts)
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
    return random.Random(int(digest[:16], 16))


def stable_hash(obj):
    payload = json.dumps(obj, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def frozen_threshold_hash():
    """Hash of the frozen quality-grade thresholds, recorded in the manifest."""
    return stable_hash(VARIANT_RULES["quality_grades"])


# --------------------------------------------------------------------------
# Quota plan
# --------------------------------------------------------------------------

def build_plan():
    """Return the frozen group plan: carrier x region x sub_carrier assignment.

    Deterministic. Produces exactly QUOTAS['total_groups'] groups.
    """
    plan = []
    group_index = 1

    # Distribute region groups across carriers proportionally to carrier size.
    for carrier, cspec in QUOTAS["carriers"].items():
        c_groups = cspec["groups"]
        regions = list(QUOTAS["regions"].keys())
        weights = [QUOTAS["regions"][r]["groups"] for r in regions]
        total_w = sum(weights)

        # Largest-remainder apportionment of carrier groups over regions.
        raw = [c_groups * w / total_w for w in weights]
        floors = [int(x) for x in raw]
        remainder = c_groups - sum(floors)
        order = sorted(range(len(raw)), key=lambda i: raw[i] - floors[i], reverse=True)
        for i in order[:remainder]:
            floors[i] += 1

        sub_carriers = cspec["sub_carriers"]
        for region, n in zip(regions, floors):
            for k in range(n):
                sc = sub_carriers[k % len(sub_carriers)]
                plan.append(
                    {
                        "group_id": f"G{group_index:05d}",
                        "carrier": carrier,
                        "sub_carrier": sc,
                        "region": region,
                        "language": QUOTAS["regions"][region]["language"],
                    }
                )
                group_index += 1

    assign_hazards(plan)
    assign_layouts(plan)
    assign_splits(plan)
    return plan


def assign_hazards(plan):
    """Assign hazard topics honouring the frozen quota constraints."""
    hazards = list(QUOTAS["hazards"].keys())
    core = QUOTAS["hazard_constraints"]["core_group"]
    rng = random.Random(MASTER_SEED)

    for entry in plan:
        # Carrier-local RNG so distribution is independent of global order.
        local = rng_for("hazard", entry["carrier"], entry["group_id"])
        # 55% from the core group, 45% from the remainder.
        if local.random() < 0.55:
            entry["hazard"] = local.choice(core)
        else:
            entry["hazard"] = local.choice([h for h in hazards if h not in core])
    return plan


def assign_layouts(plan):
    """Bind each group to a layout compatible with its platform family."""
    family_for_region = {
        "CN": "cn_social",
        "TW": "cn_social",
        "HK": "cn_social",
        "SG": "cn_social",
        "NA": "en_social",
        "UK": "en_social",
        "AU": "en_social",
    }

    for entry in plan:
        carrier = entry["carrier"]
        layouts = LAYOUTS[carrier]
        # Prefer layouts whose sub_carrier matches the assigned one.
        exact = [k for k, v in layouts.items() if v["sub_carrier"] == entry["sub_carrier"]]
        if not exact:
            exact = list(layouts.keys())

        want_family = family_for_region.get(entry["region"], "cn_social")
        by_family = [k for k in exact if layouts[k]["platform_family"] == want_family]
        pool = by_family or exact

        local = rng_for("layout", entry["carrier"], entry["group_id"], entry["region"])
        layout_id = local.choice(sorted(pool))

        # Fall back within the same carrier if the family has no matching layout.
        entry["layout_id"] = layout_id
        entry["platform_family"] = layouts[layout_id]["platform_family"]
        entry["aspect_ratio"] = layouts[layout_id]["aspect_ratio"]
    return plan


def assign_splits(plan):
    """Stratified split assignment; group-atomic by construction."""
    ratios = QUOTAS["split"]["ratios"]
    buckets = {}
    for entry in plan:
        key = (entry["carrier"], entry["language"])
        buckets.setdefault(key, []).append(entry)

    for key, entries in buckets.items():
        entries.sort(key=lambda e: e["group_id"])
        n = len(entries)
        n_train = int(round(n * ratios["train"]))
        n_val = int(round(n * ratios["validation"]))
        for i, entry in enumerate(entries):
            if i < n_train:
                entry["split"] = "train"
            elif i < n_train + n_val:
                entry["split"] = "validation"
            else:
                entry["split"] = "test"
    return plan


# --------------------------------------------------------------------------
# Text specification primitives
# --------------------------------------------------------------------------

def make_field(key, label, value, display=None):
    """A single machine-readable text field.

    `value` is the literal string that must appear in the image.
    `display` optionally records the unambiguous form used for OCR comparison.
    """
    return {"key": key, "label": label, "value": value, "display": display or value}


def collect_visible_text(fields):
    """Flatten fields into the literal string list fed to OCR comparison."""
    out = []
    for f in fields:
        if f.get("label"):
            out.append(f["label"])
        if f.get("value"):
            out.append(f["value"])
    return out


def count_density(visible_text):
    """Classify text density by measured character count (taxonomy section 7.2)."""
    joined = "".join(visible_text)
    cjk = sum(1 for ch in joined if "\u4e00" <= ch <= "\u9fff")
    latin = sum(1 for ch in joined if ch.isascii() and ch.isalnum())
    thresholds = VARIANT_RULES["text_density_thresholds"]
    if cjk >= latin:
        table, key = thresholds["cjk"], "cjk"
    else:
        table, key = thresholds["latin"], "latin"
    measured = max(cjk, latin)
    for name in ("VeryHigh", "High", "Medium", "Low"):
        lo, hi = table[name]
        if lo <= measured <= hi:
            return name, measured, key
    return "Low", measured, key
