# QA 报告

- 基础组：1000
- 提示词：4000

## 检查项

| 检查 | 结果 | 说明 |
|---|---|---|
| triplet_integrity | pass | 1000 groups checked |
| ui_prompt_mode_group_consistency | pass | all variants share their group's prompt mode |
| ui_prompt_mode_reference_ratio | pass | {'eligible_groups': 621, 'actual': {'image_text': 373, 'long_quantified': 186, ' |
| ui_prompt_reference_present | pass | all image-led and short-text modes have a reference asset |
| variant_tier_definition | pass | 4000 prompts checked |
| group_structural_consistency | pass | all groups consistent |
| forbidden_visible_text | pass | none found |
| split_group_atomicity | pass | all groups atomic |

## 统计

- **groups**：1000
- **prompts**：4000
- **by_variant**：{'clean': 1000, 'subtle': 1000, 'strong': 1000, 'fabricated': 1000}
- **by_truth_status**：{'true': 3000, 'false': 1000}
- **by_content_mode**：{'real_true_news': 1000, 'real_news_with_internal_conflict': 2000, 'fabricated_rumor_self_consistent': 1000}
- **by_carrier**：{'R1': 1200, 'R2': 1000, 'R3': 1000, 'R4': 800}
- **by_region**：{'CN': 1324, 'NA': 720, 'UK': 444, 'AU': 284, 'TW': 516, 'HK': 436, 'SG': 276}
- **by_language**：{'zh-Hans': 1600, 'en': 1448, 'zh-Hant': 952}
- **by_hazard**：{'H3': 532, 'H2': 476, 'H5': 408, 'H1': 564, 'H7': 312, 'H8': 420, 'H6': 356, 'H4': 552, 'H9': 380}
- **by_ui_prompt_mode**：{'short_text': 248, 'image_text': 1492, 'long_quantified': 2260}
- **ui_reference_backed_groups**：621
- **by_ui_prompt_mode_on_reference_groups**：{'image_text': 373, 'long_quantified': 186, 'short_text': 62}
- **by_split**：{'train': 3200, 'validation': 400, 'test': 400}
- **by_density**：{'High': 3281, 'Medium': 178, 'VeryHigh': 541}
- **tamper_type_counts**：{'metric': 494, 'timestamp': 582, 'location': 708, 'magnitude': 536, 'sensitive_addition': 352, 'urgency': 352, 'account_identity': 546, 'official_statement': 393, 'omission': 391, 'headline_body_conflict': 395, 'legal_consequence': 221, 'number_internal': 158, 'attribution': 152}

- 错误数：0