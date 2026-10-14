# news_rumor_prompts_3000

A prompt dataset for **text-rich AI-generated image generation and detection research**,
covering news-and-rumour imagery across four carrier formats.
**1000 base groups × 3 variants = 3000 prompts**, ready to feed into GPT Image 2 / GPT Image 2.5
or comparable text-to-image models.

Every prompt specifies the carrier, aspect ratio, section order and visual style, and spells out
**verbatim, inside quotation marks, every piece of text that must appear in the image** together
with the section it belongs to.

> All institutions, outlets, companies, place names, person names, contact details and identifiers
> are fictional. Addresses use the pattern "real prefecture-level city + fictional district/street";
> phone numbers use reserved ranges; identifiers are well-formed but correspond to no real entity.
> Content inconsistencies are set by design for research purposes only and refer to no real event.

---

## Structure

### Triplet design: 1000 base groups × 3 tiers

| variant | meaning | count |
|---|---|---:|
| `clean` | fully self-consistent | 1000 |
| `subtle` | 1–2 text fields altered; the image remains a completely normal design | 1000 |
| `strong` | ≥2 fields altered, or multiple rule violations; the image remains a normal design | 1000 |

The three variants of a group **share** the same subject, outlet, carrier, composition, palette and
layout, and differ **only in key text fields**, so they support direct paired comparison.

**Tiers are defined by computable counts, not by subjective severity** (see `config/variant_rules.json`):

| variant | `changed_field_count` | `rule_failure_count` |
|---|---:|---:|
| `clean` | 0 | 0 |
| `subtle` | 1–2 | 1–2 |
| `strong` | ≥2 | ≥2 |

Collateral failures are recorded separately in `collateral_failure_count` and are **not** counted
towards `rule_failure_count`.

**Inconsistent text carries no visual marking** — no circles, highlights, colour shifts or warnings.
The prompt explicitly instructs the model not to auto-correct, complete or normalise the given text.

---

## Categories

### Primary category (carrier format)

Categories follow the **visual carrier format**, not the news topic: topics are unbounded and do not
determine detection difficulty, whereas carrier format directly fixes layout, text density, UI
elements and aspect ratio.

| ID | Carrier | Groups | Prompts |
|---|---|---:|---:|
| R1 | Social post graphic | 300 | 900 |
| R2 | Vertical short-form graphic | 250 | 750 |
| R3 | News media layout | 250 | 750 |
| R4 | Graphic info card | 200 | 600 |
| **Total** | | **1000** | **3000** |

24 secondary categories, listed in [`docs/taxonomy.md`](docs/taxonomy.md).

### Media and platform coverage

Clustered by **interface paradigm** across five platform families rather than enumerated per platform:
Chinese social, English social, image social, short-form video, and news agencies / mainstream media.

### Language and region coverage

**3 languages × 7 regions**: mainland China (331, zh-Hans), North America (180, en),
Taiwan (129, zh-Hant), United Kingdom (111, en), Hong Kong (109, zh-Hant),
Australia (71, en), Singapore (69, zh-Hans).

Each carrier covers all 7 regions and all 3 languages.

### Hazard topics (quota constraint only)

H1 disaster / H2 public health / H3 policy and public services / H4 public safety /
H5 finance / H6 consumer and health claims / H7 international affairs / H8 people and
organisations / H9 public order and supply

Constraints and measured results: H1–H4 ≥50% (measured 53.1%); any single topic ≤20%
(measured max 14.1%); each carrier covers ≥5 topics (measured 9).

---

## Inconsistency taxonomy

**18 content types × 10 rule-violation types**, recorded in parallel.

Content types (`tamper_types`) cover account identity, timestamp, location, metrics,
headline-body conflict, image-text mismatch, quotation, attribution, magnitude, urgency,
causal claims, legal consequence, official statements, recommendations, internal number
consistency, omission, sensitive additions and media identity.

Rule violations (`anomaly_category`) cover date order, number relations, set relations,
unit consistency, attribution chains, subject agreement, quantity sums, temporal windows,
geographic plausibility and fixed-text alteration.

All rules are labelled **dataset-designed inconsistency** and are never presented as legal conclusions.
Full definitions: [`config/anomaly_types.json`](config/anomaly_types.json).

---

## Fields

Full dictionary in [`docs/data_fields.md`](docs/data_fields.md). Highlights:

- **`fields`** — per-field `{key, label, value}` triples; `value` is the literal text that must appear
- **`visible_text`** — a flat list of literal strings, directly usable for OCR set comparison
- **`field_changes`** — `[{field, label, base_value, value}]`, with `base_value` taken from the group's `clean` variant
- **`changed_field_count` / `rule_failure_count` / `collateral_failure_count`** — tier criteria
- **`single_image_detectable`** — `null` for `clean`, `true` otherwise
- **`prompt`** — self-contained; no need to read sibling variants or reference images

---

## Post-generation fields

This dataset delivers a **prompt + generated image + measured label** triple, not prompts alone.
Prompt-level checks do not replace post-generation measurement.

After generating images, record: `ocr_text`, `ocr_line_boxes`, `entity_hit_rate`,
`char_error_count`, `missing_entities`, `extra_text`, `quality_grade`, `text_mask`.

### Quality grades (thresholds frozen before generation)

| Grade | Definition |
|---|---|
| A | 100% entity hit rate, zero character errors, no extra text, internally consistent numbers, no layout anomaly |
| B | ≥90% hit rate, ≤2 character errors, no number-consistency error |
| C | 50–90% hit rate, or a number-consistency error, or a visible layout anomaly |
| D | <50% hit rate, or extensive gibberish, or collapsed layout |

**All grades are retained; no sample is dropped because of its grade.**
The threshold hash is recorded as `frozen_quality_threshold_sha256` in `release_manifest.json`.

---

## Anti-shortcut measures

- strip all metadata (including C2PA)
- normalise short side to 1024, preserving aspect ratio
- intermediate PNG, final re-encode as JPEG q95
- train metadata-only control classifiers (file size / header / colour histogram / dimensions);
  AUC must be ≈0.5, and any value above 0.6 indicates shortcut leakage

See [`config/constraints.json`](config/constraints.json).

---

## Usage

### 1. Regenerating the prompts

```bash
python3 src/generate.py              # full set -> final/
python3 src/generate.py --limit 120  # subset   -> pilot/
python3 src/generate.py --out /path  # custom output directory
python3 src/verify_saved.py          # verify release integrity
python3 src/verify_saved.py --write  # refresh hashes and manifest
python3 tests/test_release_consistency.py
```

No external dependencies; Python 3.9+. Generation is fully deterministic — the same
config always yields the same dataset.

---

### 2. Loading the data

```python
import json

prompts = [json.loads(l) for l in open("final/news_rumor_prompts_3000.jsonl", encoding="utf-8")]

subset = [p for p in prompts
          if p["carrier"] == "R3"          # news media layout
          and p["language"] == "zh-Hans"
          and p["variant"] == "strong"
          and p["split"] == "train"]
```

---

### 3. Submitting to a text-to-image model

**Every `prompt` is self-contained** — no need to read sibling variants, no reference images required.

```python
for p in prompts:
    image = call_image_api(
        prompt=p["prompt"],
        size=SIZE_FOR[p["carrier"]],  # must match the aspect ratio stated in the prompt
        quality="high",               # text-dense; use the highest quality tier
    )
    save(image, f"images/{p['prompt_id']}.png")
    record(p["prompt_id"], model_version=SNAPSHOT, size=..., quality=...)
```

#### 3.1 Aspect ratio must be set at the API layer

The ratio written in the prompt is descriptive text; the API parameter is what actually takes effect.

| Carrier | `aspect_ratio` | Suggested size |
|---|---|---|
| R1 | `1:1` | 1024×1024 |
| R1 | `4:5` | 1024×1280 |
| R1 | `3:4` | 1024×1365 |
| R2 | `9:16` | 1024×1792 |
| R3 | `16:9` | 1536×1024 |
| R3 | `16:10` | 1536×960 |
| R3 | `3:4` | 1024×1365 |
| R4 | `4:5` / `9:16` | 1024×1280 / 1024×1792 |

#### 3.2 Quality tier and model version

- **Use the highest quality tier.** 89% of this dataset is High density (median 271 characters);
  a low tier renders text illegible and the sample will be graded C/D and wasted.
- **Record the model version snapshot** (including the release date), not just the model name —
  mixing versions across a run undermines comparability.
- Some models do not offer a batch endpoint; calls must be made individually.

#### 3.3 Batch execution

- **Persist each result immediately** (image + `prompt_id` + actual parameters).
- Record failures separately in `failed.jsonl` with the `prompt_id` and error message.
- **Decide the failure-discard policy up front and document it** — otherwise the final dataset
  composition cannot be explained after the fact.
- Mind rate limits; running all 3000 prompts overnight in the background is advisable.

---

### 4. Train / test splits

Use the `split` field directly. **All three variants of a `group_id` always fall in the same
split** (enforced by CI), so there is no leakage to handle.

```python
train = [p for p in prompts if p["split"] == "train"]
val   = [p for p in prompts if p["split"] == "validation"]
test  = [p for p in prompts if p["split"] == "test"]
```

If you define custom splits, preserve **group atomicity** and stratify by `platform_family`
or `layout_id`.

---

### 5. OCR comparison against the text specification

`fields[].value` is the literal text that should appear; `visible_text` is a flat string list.
Both are directly usable for comparison.

```python
p = prompts[0]
ocr_result = run_ocr(f"images/{p['prompt_id']}.png")

hit = sum(1 for f in p["fields"] if f["value"] and f["value"] in ocr_result)
rate = hit / len([f for f in p["fields"] if f["value"]])

for c in p["field_changes"]:
    print(f"{c['label']}: {c['base_value']} -> {c['value']}")
```

`base_value` is taken from the group's `clean` variant, so it supports direct paired analysis.

---

### 6. Fields to populate after generation

Prompt-level checks **do not replace** post-generation measurement. These fields are reserved in
the schema and must be filled after generating images and running OCR: `ocr_text`,
`ocr_line_boxes`, `entity_hit_rate`, `char_error_count`, `missing_entities`, `extra_text`,
`quality_grade`, `text_mask`.

Thresholds are in [`config/variant_rules.json`](config/variant_rules.json), with the hash recorded
in `release_manifest.json`. **Thresholds are frozen before generation and are never adjusted in
response to results; no sample is dropped because of its grade.**

---

### 7. Uniform post-processing of generated images

- strip all metadata (including C2PA)
- normalise short side to 1024, preserving aspect ratio
- intermediate PNG, final re-encode as JPEG q95
- train metadata-only control classifiers (file size / header / colour histogram / dimensions);
  AUC must be ≈0.5, and any value above 0.6 indicates shortcut leakage

See [`config/constraints.json`](config/constraints.json).

---

### 8. Regenerate after any config change

Any change under `config/` requires re-running `python3 src/generate.py` and committing the
updated `final/`, otherwise CI fails on the config/data mismatch. This is the mechanism that
prevents post-hoc adjustment of thresholds or quotas.

See [`docs/release_integrity.md`](docs/release_integrity.md).

---

## Known limitations

- Text is assembled programmatically and has **not been reviewed by domain experts**;
- Tier counts are **design-time** criteria; image difficulty must be confirmed post-generation;
- Quality grades require OCR after image generation and are currently unpopulated;
- Prompt-level spot checks do not replace post-generation human review.

See [`docs/review_scope.md`](docs/review_scope.md) and [`docs/sources_and_limits.md`](docs/sources_and_limits.md).
