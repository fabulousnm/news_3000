# QA 报告

- 基础组：120
- 提示词：360

## 检查项

| 检查 | 结果 | 说明 |
|---|---|---|
| triplet_integrity | pass | 120 groups checked |
| variant_tier_definition | pass | 360 prompts checked |
| group_structural_consistency | pass | all groups consistent |
| forbidden_visible_text | pass | none found |
| split_group_atomicity | pass | all groups atomic |

## 统计

- **groups**：120
- **prompts**：360
- **by_variant**：{'clean': 120, 'subtle': 120, 'strong': 120}
- **by_carrier**：{'R1': 360}
- **by_region**：{'CN': 297, 'NA': 63}
- **by_language**：{'zh-Hans': 297, 'en': 63}
- **by_hazard**：{'H3': 60, 'H2': 54, 'H5': 36, 'H1': 45, 'H7': 30, 'H8': 36, 'H6': 24, 'H4': 54, 'H9': 21}
- **by_split**：{'train': 351, 'validation': 9}
- **by_density**：{'High': 298, 'Medium': 61, 'VeryHigh': 1}
- **tamper_type_counts**：{'metric': 111, 'timestamp': 50, 'location': 93, 'magnitude': 84, 'sensitive_addition': 58, 'urgency': 58, 'account_identity': 72, 'official_statement': 56, 'omission': 12, 'headline_body_conflict': 19}

- 错误数：0