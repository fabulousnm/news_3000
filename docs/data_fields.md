# 字段字典

本文件说明 `final/news_rumor_prompts_3000.jsonl` 每条记录的字段。
另有 `groups.jsonl`（按基础组聚合）与 `news_rumor_prompts_3000.csv`（扁平视图）。

---

## 1. 标识与定位

| 字段 | 类型 | 说明 |
|---|---|---|
| `prompt_id` | string | 形如 `G00001-clean`，全局唯一 |
| `group_id` | string | 形如 `G00001`，一组含三档 |
| `variant` | enum | `clean` / `subtle` / `strong` |

---

## 2. 类别维度

| 字段 | 类型 | 取值 |
|---|---|---|
| `carrier` | enum | `R1` / `R2` / `R3` / `R4` |
| `sub_carrier` | string | 二级类别，见 `taxonomy.md` |
| `platform_family` | enum | `cn_social` / `en_social` / `image_social` / `short_video` / `news_media` |
| `layout_id` | string | 版面模板标识，对应 `config/layout_templates_R*.json` 的键 |
| `hazard` | enum | `H1`–`H9` |
| `region` | enum | `CN` / `NA` / `UK` / `AU` / `TW` / `HK` / `SG` |
| `language` | enum | `zh-Hans` / `zh-Hant` / `en` |
| `aspect_ratio` | string | 画幅，如 `4:5`、`9:16`、`16:9` |
| `capture_style` | enum | `native_screenshot` / `photo_of_screen` / `photo_of_print` / `broadcast_capture` / `exported_graphic` |
| `split` | enum | `train` / `validation` / `test` |

---

## 3. 文字规格（机器可读真值）

| 字段 | 类型 | 说明 |
|---|---|---|
| `fields` | array | 逐字段对象，见下 |
| `field_count` | int | `fields` 长度 |
| `required_fields` | array[string] | 非空 `label` 列表 |
| `visible_text` | array[string] | 扁平化的逐字字符串列表 |
| `text_density` | enum | `Low` / `Medium` / `High` / `VeryHigh` |
| `measured_char_count` | int | 实测字符数 |
| `density_unit` | enum | `cjk` / `latin`，指明按哪种计数口径判定 |

### `fields` 元素结构

```json
{
  "key":  "headline",
  "label": "标题",
  "value": "食品安全风险提示　相关部门发布情况说明"
}
```

| 键 | 说明 |
|---|---|
| `key` | 版面角色标识，与 `layout_templates_R*.json` 中该分区的 `text_roles` 一致 |
| `label` | 字段标签（中文数据填写，英文数据为空串） |
| `value` | **必须逐字出现在图中的字面文本**；`value` 为空表示该字段被删除 |

**`value` 是本数据集的核心真值。** 生成图像后，将 OCR 结果与 `value` 集合比对，
即可计算 `entity_hit_rate`、`char_error_count`、`missing_entities`、`extra_text`。

### 密度判定口径

按 `visible_text` 全部字符判定；同时统计 CJK 字符数与拉丁字母数字数，取较大者判定，并记录于 `density_unit`。

| 档 | CJK 字符数 | 拉丁字符数 |
|---|---|---|
| Low | < 60 | < 120 |
| Medium | 60–199 | 120–399 |
| High | 200–449 | 400–899 |
| VeryHigh | ≥ 450 | ≥ 900 |

密度是**测量值**，不人为填充无关文字以凑档位。

---

## 4. 变体标注

| 字段 | 类型 | 说明 |
|---|---|---|
| `changed_fields` | array[string] | 被改动的字段 `key` 列表 |
| `field_changes` | array | 逐条改动记录，见下 |
| `tamper_types` | array[string] | 内容不一致类型，取自 `config/anomaly_types.json` |
| `anomaly_category` | array[string] | 规则违反类型，取自同一文件 |
| `changed_field_count` | int | 去重后的改动字段数 |
| `rule_failure_count` | int | 规则违反类型数（去重） |
| `collateral_failure_count` | int | 连带失败数，单列，不计入 `rule_failure_count` |
| `single_image_detectable` | bool \| null | `clean` 为 `null`，其余为 `true` |

### `field_changes` 元素结构

```json
{
  "field": "publish_time",
  "label": "发布时间",
  "base_value": "2026年9月27日 07:34",
  "value": "2025年11月26日 07:34"
}
```

`base_value` 取自同组 `clean` 版本，便于直接做对照分析。

### 档位判据

| variant | `changed_field_count` | `rule_failure_count` |
|---|---:|---:|
| `clean` | 0 | 0 |
| `subtle` | 1–2 | 1–2 |
| `strong` | ≥2 | ≥2 |

由 CI 校验（`variant_tier_definition`）。

---

## 5. 提示词

| 字段 | 类型 | 说明 |
|---|---|---|
| `prompt` | string | 自包含的完整提示词 |

`prompt` 按固定段落拼装，段落顺序：

1. 画幅、载体、拍摄质感
2. 视觉风格与版面结构（分区顺序以 ` → ` 连接）
3. 主体与虚构声明
4. 版面内容块（`【分区】「文字」` 形式，逐字给定）
5. 真实感细节
6. 研究用样本声明（**仅 `subtle` 与 `strong` 含此段**，明确要求模型不得纠正或突出异常）
7. 文字呈现约定（「」内逐字呈现；禁止乱码、占位符；禁止擅自改写数字；小字不小于画面高度 1.2%）
8. 版面保真与表格要求

中文提示词用「」标注必须逐字呈现的文字；英文提示词用双引号。

**同一组三档的大段文字完全一致**，差异集中在第 4 段（版面内容块）与是否存在第 6 段。

---

## 6. 生成后须补充的字段

以下字段在本仓库中预留但未填写，须在生成图像并完成 OCR 后补充：

| 字段 | 类型 | 说明 |
|---|---|---|
| `ocr_text` | string | OCR 全文 |
| `ocr_line_boxes` | array | OCR 行框（每行 `[x, y, w, h]`） |
| `entity_hit_rate` | float | 确定性命中率，取值 `[0, 1]` |
| `char_error_count` | int | 错字数 |
| `missing_entities` | array[string] | 遗漏实体 |
| `extra_text` | array[string] | 多余文字（命中禁用列表则直接判 D） |
| `quality_grade` | enum | `A` / `B` / `C` / `D` |
| `text_mask` | string | 文字区域掩码文件路径 |

分级阈值见 `config/variant_rules.json` 的 `quality_grades`，
其哈希记录于 `release_manifest.json` 的 `frozen_quality_threshold_sha256`。

---

## 7. 一致性要求

同组三档**必须完全一致**的字段（由 CI 校验）：

`carrier`、`sub_carrier`、`platform_family`、`layout_id`、`region`、`language`、
`hazard`、`aspect_ratio`、`capture_style`、`split`，
以及提示词中的分区标题、静态说明文字、字段集合与行数。
