# 二级类别与配额明细

本文件由 `config/quotas.json` 与实际交付数据核对生成。

> 类别按**视觉载体形态**划分，不按新闻主题划分。


---

## 1. 一级类别与配额

| 编号 | 载体子类 | 基础组 | 提示词 |
|---|---|---:|---:|
| R1 | 社交平台帖文图文 | 300 | 900 |
| R2 | 短视频平台竖屏图文 | 250 | 750 |
| R3 | 新闻媒体版式 | 250 | 750 |
| R4 | 图文信息卡 | 200 | 600 |
| **合计** | | **1000** | **3000** |

---

## 2. 二级类别


### R1 · 社交平台帖文图文

| 二级类别 | 实际组数 |
|---|---:|
| `text_only_post` | 53 |
| `image_post` | 53 |
| `grid_gallery_post` | 53 |
| `quote_repost` | 47 |
| `topic_aggregation` | 47 |
| `embedded_comment` | 47 |
| **小计** | **300** |

### R2 · 短视频平台竖屏图文

| 二级类别 | 实际组数 |
|---|---:|
| `scene_frame` | 53 |
| `caption_narration_frame` | 53 |
| `overlay_graphic_frame` | 50 |
| `screen_in_screen_frame` | 47 |
| `live_capture_frame` | 47 |
| **小计** | **250** |

### R3 · 新闻媒体版式

| 二级类别 | 实际组数 |
|---|---:|
| `tv_broadcast` | 35 |
| `tv_breaking_interrupt` | 34 |
| `newspaper_front_page` | 33 |
| `newspaper_inner_page` | 31 |
| `news_site_home` | 30 |
| `news_app_detail` | 29 |
| `wire_bulletin` | 29 |
| `news_brief_card` | 29 |
| **小计** | **250** |

### R4 · 图文信息卡

| 二级类别 | 实际组数 |
|---|---:|
| `share_card` | 44 |
| `summary_long_image` | 41 |
| `topic_aggregation_long_image` | 39 |
| `timeline_image` | 39 |
| `quick_read_card` | 37 |
| **小计** | **200** |

---

## 3. 版面模板

| 模板 | 平台族 | 画幅 | 分区数 | 实际组数 |
|---|---|---|---:|---:|
| `cn_social_text_only` | cn_social | 1:1 | 8 | 34 |
| `cn_social_image_post` | cn_social | 4:5 | 8 | 17 |
| `cn_social_grid_gallery` | cn_social | 3:4 | 8 | 43 |
| `cn_social_quote_repost` | cn_social | 4:5 | 8 | 30 |
| `cn_social_topic_aggregation` | cn_social | 4:5 | 6 | 47 |
| `cn_social_embedded_comment` | cn_social | 4:5 | 7 | 47 |
| `en_social_text_only` | en_social | 1:1 | 6 | 19 |
| `en_social_image_post` | en_social | 4:5 | 7 | 13 |
| `en_social_quote_repost` | en_social | 4:5 | 7 | 17 |
| `image_social_post` | image_social | 4:5 | 7 | 0 |
| `image_social_grid` | image_social | 3:4 | 7 | 10 |
| `cn_social_html_post` | cn_social | 4:5 | 8 | 17 |
| `en_social_news_card` | en_social | 4:5 | 6 | 6 |
| `short_video_scene_frame` | short_video | 9:16 | 9 | 53 |
| `short_video_caption_narration` | short_video | 9:16 | 9 | 53 |
| `short_video_overlay_graphic` | short_video | 9:16 | 9 | 50 |
| `short_video_screen_in_screen` | short_video | 9:16 | 9 | 47 |
| `short_video_live_capture` | short_video | 9:16 | 9 | 47 |
| `tv_broadcast` | news_media | 16:9 | 6 | 35 |
| `tv_breaking_interrupt` | news_media | 16:9 | 7 | 34 |
| `newspaper_front_page` | news_media | 3:4 | 6 | 33 |
| `newspaper_inner_page` | news_media | 3:4 | 6 | 31 |
| `news_site_home` | news_media | 16:10 | 5 | 30 |
| `news_app_detail` | news_media | 9:16 | 8 | 29 |
| `wire_bulletin` | news_media | 4:5 | 7 | 29 |
| `news_brief_card` | news_media | 4:5 | 6 | 29 |
| `share_card` | cn_social | 4:5 | 7 | 44 |
| `summary_long_image` | cn_social | 9:16 | 8 | 41 |
| `topic_aggregation_long_image` | cn_social | 9:16 | 7 | 39 |
| `timeline_image` | cn_social | 9:16 | 5 | 39 |
| `quick_read_card` | image_social | 4:5 | 7 | 37 |

---

## 4. 地区与语言

| 地区 | 语言 | 配额 | 实际组数 |
|---|---|---:|---:|
| CN 中国大陆 | zh-Hans | 330 | 331 |
| NA 北美 | en | 180 | 180 |
| UK 英国 | en | 110 | 111 |
| AU 澳大利亚 | en | 70 | 71 |
| TW 台湾 | zh-Hant | 130 | 129 |
| HK 香港 | zh-Hant | 110 | 109 |
| SG 新加坡 | zh-Hans | 70 | 69 |
| **合计** | | **1000** | **1000** |

### 每种载体的地区覆盖

| 载体 | 覆盖地区数 | zh-Hans | zh-Hant | en |
|---|---:|---:|---:|---:|
| R1 | 7 | 120 | 72 | 108 |
| R2 | 7 | 100 | 59 | 91 |
| R3 | 7 | 100 | 59 | 91 |
| R4 | 7 | 80 | 48 | 72 |

---

## 5. 危害主题配额

| 编号 | 主题 | 组数 | 占比 |
|---|---|---:|---:|
| H1 | 灾害与险情 | 141 | 14.1% |
| H2 | 公共卫生 | 119 | 11.9% |
| H3 | 政策与民生 | 133 | 13.3% |
| H4 | 社会治安与案件 | 138 | 13.8% |
| H5 | 经济与金融 | 102 | 10.2% |
| H6 | 生活与健康认知 | 89 | 8.9% |
| H7 | 涉外与国际关系 | 78 | 7.8% |
| H8 | 人物与机构动态 | 105 | 10.5% |
| H9 | 公共秩序与群体行为 | 95 | 9.5% |

- H1–H4 合计：531 组（53.1%），约束要求 ≥50%
- 单一主题最大占比：14.1%，约束要求 ≤20%
- 每个载体子类覆盖主题数：9，约束要求 ≥5

---

## 6. 文字密度分布

| 密度 | 样本数 | 占比 |
|---|---:|---:|
| Low | 0 | 0.0% |
| Medium | 109 | 10.9% |
| High | 891 | 89.1% |
| VeryHigh | 0 | 0.0% |

**按语言**

| 语言 | Low | Medium | High | VeryHigh |
|---|---:|---:|---:|---:|
| zh-Hans | 0 | 31 | 369 | 0 |
| zh-Hant | 0 | 31 | 207 | 0 |
| en | 0 | 47 | 315 | 0 |

---

## 7. 不一致类型统计


### 内容类型

| 类型 | 名称 | 出现次数 |
|---|---|---:|
| `account_identity` | 账号主体信息 | 672 |
| `timestamp` | 时间信息 | 582 |
| `location` | 地点信息 | 124 |
| `metric` | 互动数据 | 494 |
| `headline_body_conflict` | 标题与正文冲突 | 459 |
| `attribution` | 信息来源归属 | 152 |
| `magnitude` | 事件规模 | 686 |
| `urgency` | 紧迫性表述 | 447 |
| `legal_consequence` | 处置结果 | 250 |
| `official_statement` | 官方表态 | 437 |
| `number_internal` | 文内数字一致性 | 158 |
| `omission` | 关键限定缺失 | 391 |
| `sensitive_addition` | 挑动性内容添加 | 447 |

### 规则违反类型

| 类型 | 名称 | 出现次数 |
|---|---|---:|
| `date_order` | 日期先后矛盾 | 582 |
| `number_relation` | 数值关系矛盾 | 1180 |
| `set_relation` | 集合与范围矛盾 | 250 |
| `attribution_chain` | 信息链断裂或循环 | 1037 |
| `subject_agreement` | 主语与所述行为不符 | 459 |
| `quantity_sum` | 分项与合计不等 | 158 |
| `temporal_window` | 时间落于不合理区间 | 391 |
| `geographic_plausibility` | 地点与事件类型不匹配 | 124 |
| `fixed_text` | 固定文案被改动 | 447 |

---

## 8. 划分

| 集合 | 基础组 | 提示词 | 占比 |
|---|---:|---:|---:|
| train | 800 | 2400 | 80.0% |
| validation | 100 | 300 | 10.0% |
| test | 100 | 300 | 10.0% |
