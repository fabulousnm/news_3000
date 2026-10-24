"""Generate SHA256SUMS.txt and release_manifest.json, and verify integrity."""

import hashlib
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import CONSTRAINTS, LAYOUTS, QUOTAS, VARIANT_RULES, stable_hash  # noqa: E402

TRACKED = [
    "final/news_rumor_prompts_3000.jsonl",
    "final/news_rumor_prompts_3000.csv",
    "final/news_rumor_prompts_unified.csv",
    "final/groups.jsonl",
    "final/qa_report.json",
    "final/news_rumor_prompts_4000.txt",
    "src/generate.py",
    "src/generate_ui_reference_pilot.py",
    "src/export_txt.py",
    "src/ui_prompt_modes.py",
    "src/ui_reference_urls.py",
    "config/quotas.json",
    "config/variant_rules.json",
    "config/anomaly_types.json",
    "config/prompt_templates.json",
    "config/constraints.json",
    "config/fiction_library.json",
    "config/layout_templates_R1.json",
    "config/layout_templates_R2.json",
    "config/layout_templates_R3.json",
    "config/layout_templates_R4.json",
]


def release_files():
    """Files covered by the release checksums, including UI template assets."""
    templates = sorted(
        p.relative_to(BASE_DIR).as_posix()
        for p in (BASE_DIR / "final/ui_reference_templates").glob("*")
        if p.is_file()
    )
    return TRACKED + templates


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_sums():
    lines = []
    for rel in release_files():
        p = BASE_DIR / rel
        if p.exists():
            lines.append(f"{sha256_file(p)}  {rel}")
    (BASE_DIR / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return lines


def write_manifest():
    prompts_path = BASE_DIR / "final/news_rumor_prompts_3000.jsonl"
    groups_path = BASE_DIR / "final/groups.jsonl"
    prompts = [json.loads(l) for l in open(prompts_path, encoding="utf-8")]
    groups = [json.loads(l) for l in open(groups_path, encoding="utf-8")]

    manifest = {
        "dataset": "news_rumor_prompts_3000",
        "version": "1.3",
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
        "frozen_quality_threshold_sha256": stable_hash(VARIANT_RULES["quality_grades"]),
        "frozen_variant_rules_sha256": stable_hash(VARIANT_RULES["variant_rules"]),
        "quota_config_sha256": stable_hash(QUOTAS),
        "constraints_sha256": stable_hash(CONSTRAINTS),
        "layout_templates_sha256": stable_hash(LAYOUTS),
        "file_hashes": {rel: sha256_file(BASE_DIR / rel)
                        for rel in release_files() if (BASE_DIR / rel).exists()},
        "note": "配额、档位定义与质量分级阈值均在生成前冻结，生成后不调整。",
    }
    (BASE_DIR / "release_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return manifest


def verify():
    ok = True
    manifest_path = BASE_DIR / "release_manifest.json"
    sums_path = BASE_DIR / "SHA256SUMS.txt"
    if not manifest_path.exists() or not sums_path.exists():
        print("manifest or sums missing; run with --write first")
        return False

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for rel, expected in manifest["file_hashes"].items():
        actual = sha256_file(BASE_DIR / rel)
        if actual != expected:
            print(f"MISMATCH {rel}")
            ok = False

    prompts = [json.loads(l) for l in open(BASE_DIR / "final/news_rumor_prompts_3000.jsonl",
                                           encoding="utf-8")]
    if stable_hash(prompts) != manifest["prompts_sha256"]:
        print("MISMATCH prompts content hash")
        ok = False
    if stable_hash(VARIANT_RULES["quality_grades"]) != manifest["frozen_quality_threshold_sha256"]:
        print("MISMATCH frozen quality threshold changed since release")
        ok = False

    print("integrity OK" if ok else "integrity FAILED")
    return ok


if __name__ == "__main__":
    if "--write" in sys.argv:
        write_sums()
        m = write_manifest()
        write_sums()  # refresh after manifest written
        print(json.dumps(m["counts"], ensure_ascii=False))
        print("wrote SHA256SUMS.txt and release_manifest.json")
    else:
        sys.exit(0 if verify() else 1)
