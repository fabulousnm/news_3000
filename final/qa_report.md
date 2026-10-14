# QA 报告

- 基础组：1000
- 提示词：3000

## 检查项

| 检查 | 结果 | 说明 |
|---|---|---|
| triplet_integrity | pass | 1000 groups checked |
| variant_tier_definition | pass | 3000 prompts checked |
| group_structural_consistency | pass | all groups consistent |
| forbidden_visible_text | pass | none found |
| split_group_atomicity | pass | all groups atomic |

## 统计

- **groups**：1000
- **prompts**：3000
- **by_variant**：{'clean': 1000, 'subtle': 1000, 'strong': 1000}
- **by_carrier**：{'R1': 900, 'R2': 750, 'R3': 750, 'R4': 600}
- **by_region**：{'CN': 993, 'NA': 540, 'UK': 333, 'AU': 213, 'TW': 387, 'HK': 327, 'SG': 207}
- **by_language**：{'zh-Hans': 1200, 'en': 1086, 'zh-Hant': 714}
- **by_hazard**：{'H3': 399, 'H2': 357, 'H5': 306, 'H1': 423, 'H7': 234, 'H8': 315, 'H6': 267, 'H4': 414, 'H9': 285}
- **by_split**：{'train': 2400, 'validation': 300, 'test': 300}
- **by_density**：{'High': 2523, 'Medium': 165, 'VeryHigh': 312}
- **tamper_type_counts**：{'metric': 494, 'timestamp': 582, 'location': 708, 'magnitude': 536, 'sensitive_addition': 352, 'urgency': 352, 'account_identity': 546, 'official_statement': 393, 'omission': 391, 'headline_body_conflict': 395, 'legal_consequence': 221, 'number_internal': 158, 'attribution': 152}

- 错误数：0