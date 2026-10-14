# QA 报告

- 基础组：120
- 提示词：480

## 检查项

| 检查 | 结果 | 说明 |
|---|---|---|
| triplet_integrity | pass | 120 groups checked |
| variant_tier_definition | pass | 480 prompts checked |
| group_structural_consistency | pass | all groups consistent |
| forbidden_visible_text | pass | none found |
| split_group_atomicity | pass | all groups atomic |

## 统计

- **groups**：120
- **prompts**：480
- **by_variant**：{'clean': 120, 'subtle': 120, 'strong': 120, 'fabricated': 120}
- **by_truth_status**：{'true': 360, 'false': 120}
- **by_content_mode**：{'real_true_news': 120, 'real_news_with_internal_conflict': 240, 'fabricated_rumor_self_consistent': 120}
- **by_carrier**：{'R1': 480}
- **by_region**：{'CN': 396, 'NA': 84}
- **by_language**：{'zh-Hans': 396, 'en': 84}
- **by_hazard**：{'H3': 80, 'H2': 72, 'H5': 48, 'H1': 60, 'H7': 40, 'H8': 48, 'H6': 32, 'H4': 72, 'H9': 28}
- **by_split**：{'train': 468, 'validation': 12}
- **by_density**：{'High': 401, 'Medium': 78, 'VeryHigh': 1}
- **tamper_type_counts**：{'metric': 111, 'timestamp': 50, 'location': 93, 'magnitude': 84, 'sensitive_addition': 58, 'urgency': 58, 'account_identity': 72, 'official_statement': 56, 'omission': 12, 'headline_body_conflict': 19}

- 错误数：0