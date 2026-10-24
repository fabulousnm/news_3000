# 仓库结构说明

> 本文档说明仓库中每个文件的内容、作用，以及文件之间的依赖与数据流关系。
> 适合新接手者快速定位"要改什么去哪里改、数据从哪来、产物在哪"。

---

## 1. 全局视图

```
                        ┌─────────────────────────────┐
                        │        config/              │  ← 冻结的配置层
                        │  配额 / 档位 / 阈值 / 模板   │     生成前定稿，改需重生成
                        └──────────────┬──────────────┘
                                       │ 读取
                                       ▼
    ┌──────────────────────────────────────────────────────────┐
    │                        src/                              │  ← 生成管线
    │                                                          │
    │  common.py ──┬──► content.py ──┐                         │
    │  (配置/确定性 │   (按版面角色   │                         │
    │   随机/计划)  │    装配内容)    │                         │
    │              │                 ▼                         │
    │              ├──► variants.py ──► render.py ──► generate.py
    │              │   (三档派生)      (提示词拼装)   (入口+校验)
    │              │                                   │       │
    │              └──► sentences.py                    │       │
    │                  (语句库)                          │       │
    │                                                   ▼       │
    │  verify_saved.py ◄──── export_txt.py ◄──── final/ (产物)  │
    │  (完整性校验)      (纯文本导出)                             │
    └──────────────────────────────────────────────────────────┘
                                       │ 校验
                                       ▼
                        ┌─────────────────────────────┐
                        │  tests/ + .github/          │  ← 质量保障
                        │  一致性测试 + CI            │
                        └─────────────────────────────┘
```

**一句话概括**：`config/` 定义"要生成什么"，`src/` 是"怎么生成"，`final/` 和 `pilot/` 是"生成结果"，`docs/` 是"怎么用和为什么这样设计"，`tests/` 与 `.github/` 是"防止改动走样"。

---

## 2. `config/` — 冻结的配置层

**所有配置在生成任何提示词之前定稿。改动任何一项都必须重新运行生成并提交新产物，否则 CI 会失败。**

| 文件 | 内容 | 被谁读取 |
|---|---|---|
| `quotas.json` | **配额**：4 个载体的组数（R1 300 / R2 250 / R3 250 / R4 200）、7 个地区分布、9 个危害主题及其配额约束、平台族定义、划分比例 | `common.py` |
| `variant_rules.json` | **档位定义**（`clean`/`subtle`/`strong` 的计数判据）、**质量分级阈值**（A/B/C/D）、文字密度阈值、禁用词表 | `common.py` → `generate.py` / `verify_saved.py` |
| `anomaly_types.json` | **不一致类型库**：18 种内容类型（`tamper_types`）× 10 种规则违反类型（`anomaly_category`），及三档的标注策略 | `common.py` |
| `fiction_library.json` | **虚构主体库**：按 7 个地区分组的虚构机构、媒体、人名、地名；黑名单规则 | `common.py` → `content.py` |
| `constraints.json` | **合规与反捷径约束**：实体虚构规则、禁止出现在图中的内容、后处理要求、组一致性要求 | `common.py` → `verify_saved.py` |
| `prompt_templates.json` | **提示词段落模板**：载体描述、拍摄质感描述、分区块格式、禁用附加词 | `common.py` → `render.py` |
| `layout_templates_R1.json` | **R1 社交帖文**的 13 个版面模板：分区顺序 + 每区的文字角色 + 画幅 | `common.py` → `content.py` / `render.py` |
| `layout_templates_R2.json` | **R2 短视频竖屏**的 5 个版面模板 | 同上 |
| `layout_templates_R3.json` | **R3 新闻媒体版式**的 8 个版面模板 | 同上 |
| `layout_templates_R4.json` | **R4 图文信息卡**的 5 个版面模板 | 同上 |

### 关键概念：版面模板

每个模板声明**分区顺序**和**每区应出现哪些文字角色**：

```json
"cn_social_image_post": {
  "platform_family": "cn_social",
  "aspect_ratio": "4:5",
  "sections": [
    {"role": "top_bar",         "pct": 6,  "text_roles": ["platform_label"]},
    {"role": "author_block",    "pct": 10, "text_roles": ["account_name", "account_meta"]},
    {"role": "body",            "pct": 14, "text_roles": ["body_text", "hashtags"]},
    {"role": "media",           "pct": 54, "text_roles": []},
    {"role": "interaction_bar", "pct": 9,  "text_roles": ["comment_metric", "like_metric"]},
    {"role": "timestamp",       "pct": 7,  "text_roles": ["publish_time", "source_label"]}
  ]
}
```

- **`text_roles` 是"槽位"** —— `content.py` 会为每个槽位填一段文字，`render.py` 会把它渲染成 `【分区】「文字」`
- **角色到分区的映射是自动推导的**（遍历所有模板建立索引），而非手工维护字典。这一点很重要：手工字典下，新增槽位没登记就会全部回退到版面首个分区
- 共 **31 个模板**，实测每张图 11–27 个文字槽位

---

## 3. `src/` — 生成管线

### 3.1 依赖关系

```
common.py  ← 所有模块的基础（配置加载 + 确定性随机 + 配额计划）
    ↑
    ├── content.py  ← 依赖 sentences.py
    ├── variants.py
    ├── render.py
    ├── export_txt.py
    ├── verify_saved.py
    └── generate.py ← 依赖 content.py + variants.py + render.py（即管线终点）
```

### 3.2 各文件说明

#### `common.py`（218 行）—— 基础设施

| 提供 | 说明 |
|---|---|
| `load_config(name)` | 统一加载 `config/` 下的 JSON |
| `rng_for(*parts)` | **确定性随机源**：`sha256(键) → 种子`，不依赖调用顺序，保证可复现 |
| `stable_hash(obj)` | 规范化哈希，用于完整性校验 |
| `frozen_threshold_hash()` | 质量分级阈值的哈希 |
| `build_plan()` | **配额计划**：产出 1000 个基础组，分配载体、地区、子类、版面、危害主题、划分 |
| `count_density()` | 按 `visible_text` 实测字符数判定密度 |
| `collect_visible_text()` | 把字段摊平成字符串列表 |

**为什么确定性重要**：CI 每次提交会重新生成并比对 `final/`。若随机源依赖调用顺序，同样的配置会产出不同结果，CI 就永远失败。

#### `sentences.py`（391 行）—— 语句库

- **270 条完整语句**：9 个危害主题 × 3 种语言 × 每主题 10 条
- 每主题内**互不重复**，中文平均 32 字、英文平均 74 字符
- 另含**标题变体**（每语言 6 种）与**短标签**（每语言 8 个）
- 续句池（每语言 20 条）在 `content.py` 中定义，用于槽位数超过语句库时补足

**直接决定文字密度**——扩充此文件是提升密度或降低重复率的唯一正确途径。

#### `content.py`（1052 行，最大）—— 内容装配

按版面声明的**每一个 `text_role`** 逐一填充内容，中英双分支。

- 输入：`group`（含地区、语言、危害主题）+ `layout`（版面模板）
- 输出：`fields`（`[{key, label, value}]`）+ `meta`（虚构主体信息）
- **按 layout 的 section 顺序输出**，确保每个槽位都有内容，且同组三档结构一致
- 从 `fiction_library.json` 取虚构主体，从 `sentences.py` 取语句

**这是"文字级真值"的实际生产地** —— `fields[].value` 就是"这张图应该出现什么字"。

#### `variants.py`（262 行）—— 三档派生

- **12 个变更算子**，每个声明：候选字段角色、产生的内容类型、产生的规则违反
- 算子作用于**字段值**，不作用于版式描述
- 每个算子声明多个候选角色，**取该版面实际存在的第一个** —— 这样不同版面都能产出完整三档
- 输出三套 `fields` + 标注记录（`changed_fields` / `field_changes` / `tamper_types` / `anomaly_category` / 三个计数）

**为什么算子要这样设计**：不同版面槽位不同。若算子只认固定字段名，缺该字段的版面就会退档。

#### `render.py`（486 行）—— 提示词拼装

- 把 `fields` 按版面分区渲染成 `【分区】「文字」…`
- **角色→分区映射自动推导**（`_build_role_index()` / `section_for_role()`）
- 中英双版本：`build_prompt()`（中文，用 `「」`）/ `build_prompt_en()`（英文，用双引号）
- 拼装 13 个固定段落，含**负向约束段**（"不得自动纠正、不得用视觉标记突出异常"）

#### `generate.py`（318 行）—— 管线入口

```
build_records()          遍历配额计划 → 装配内容 → 派生三档 → 拼装提示词
validate()               5 项生成期检查
write_outputs()          写出 jsonl / csv / groups / qa_report / release_manifest
```

用法：
```bash
python3 src/generate.py              # 全量 → final/
python3 src/generate.py --limit 120  # 抽样 → pilot/
```

#### `export_txt.py`（179 行）—— 纯文本导出

- 从配额计划直接生成（可放大 `--target`），或导出既有数据
- 每条提示词之间**以空行分隔**，便于逐条切分
- `--bare`（只要正文）/ `--no-header` / `--out`

#### `verify_saved.py`（118 行）—— 完整性校验

- 校验 `release_manifest.json` 中的文件哈希与内容哈希
- **校验冻结阈值哈希** —— 若阈值被改动即报错
- `--write` 重新生成哈希与清单

---

## 4. `final/` 与 `pilot/` — 产物

**`final/` 是正式交付（1000 组 / 4000 条）；`pilot/` 是前 120 组抽样（480 条），供小规模出图测试。两者结构相同。**

| 文件 | 内容 | 用途 |
|---|---|---|
| `news_rumor_prompts_3000.jsonl` | **主交付物**：4000 条，每条包含提示词、文字真值与标注 | 完整数据集 |
| `groups.jsonl` | 1000 个基础组的聚合记录 | 组级分析、划分检查 |
| `news_rumor_prompts_3000.csv` | 扁平视图（21 个关键列） | 快速浏览、表格工具 |
| `news_rumor_prompts_4000.txt` | 当前完整提示词文本，空行分隔 | **直接投喂生图模型** |
| `news_rumor_prompts_30000.txt` | 30000 条纯文本（约 78 MB） | 扩大版，未进 zip（可 2 分钟重生） |
| `qa_report.json` / `.md` | 生成期检查结果与统计，包含参考图模式配额校验 | 质量凭证 |
| `release_manifest.json` | 计数、内容哈希、**冻结阈值哈希** | 版本与完整性凭证 |

### 产物中的字段从哪来

| 字段组 | 来源 |
|---|---|
| `prompt_id` / `group_id` / `variant` | `generate.py` 组装 |
| `carrier` / `region` / `language` / `hazard` / `split` / `layout_id` | `common.build_plan()`（依据 `quotas.json`） |
| `fields` / `visible_text` / `required_fields` | `content.py` 装配 |
| `field_count` / `text_density` / `measured_char_count` | `common.count_density()` |
| `changed_fields` / `field_changes` / `tamper_types` / `anomaly_category` / 三个计数 | `variants.py` 派生 |
| `prompt` | `render.py` 拼装 |
| `ocr_text` / `entity_hit_rate` / `quality_grade` 等 8 个 | **未填写**，须出图后补 |

---

## 5. `docs/` — 说明文档

| 文件 | 内容 | 给谁看 |
|---|---|---|
| `generation_approach.md` | **生成模板、所用模型、生成思路** | 审阅者、答辩 |
| `taxonomy.md` | 二级类别完整列表 + 实测统计（含密度分布、不一致类型计数） | 数据使用者 |
| `data_fields.md` | **字段字典**：每个字段的类型、含义、取值 | 数据使用者 |
| `real_image_sources.md` | 真实图像获取途径调研（含实测结果与陷阱） | 负责真实图的人 |
| `review_scope.md` | **已完成 / 未完成**的检查清单 | 审阅者、论文写作 |
| `sources_and_limits.md` | 来源说明与局限（含为何不含参考图） | 审阅者 |
| `release_integrity.md` | 校验方式与版本升级流程 | 维护者 |

---

## 6. 根目录文件

| 文件 | 作用 |
|---|---|
| `README.md` | 中文主文档：数据集结构、类别体系、字段、**使用方法（含如何投喂生图模型）** |
| `README_EN.md` | 英文版 |
| `news_rumor_dataset_taxonomy.md` | **分类体系**：一级/二级类别、配额、档位定义、视觉要求、分级阈值——**所有设计决策的定稿文档** |
| `CHANGELOG.md` | 版本记录（v1.0 → v1.1 → v1.2，含每版修复的缺陷） |
| `SHA256SUMS.txt` | 文件哈希清单 |
| `release_manifest.json` | 顶层发布清单 |
| `.gitignore` / `.gitattributes` | Git 配置（强制 LF 换行） |

---

## 7. `tests/` 与 `.github/` — 质量保障

### `tests/test_release_consistency.py`（13 项测试）

**独立复算**产物中的不变量，不信任生成器自己的报告：

| 测试 | 校验内容 |
|---|---|
| `test_counts` | 组数与配额一致 |
| `test_triplets` | 每组恰含三档 |
| `test_variant_tiers` | 三档计数符合冻结定义 |
| `test_group_consistency` | 同组三档的 10 个定位字段完全一致 |
| `test_split_atomicity` | 同组三档落于同一集合 |
| `test_split_ratios` | 划分比例约 80/10/10 |
| `test_visible_text_nonempty` | clean 档所有字段非空 |
| `test_forbidden_text` | 无禁用词 |
| `test_changed_fields_traceable` | 改动字段可追溯 |
| `test_prompt_self_contained` | 提示词自包含 |
| `test_language_region_quota` | 地区配额吻合 |
| `test_carrier_region_coverage` | 每个载体覆盖 ≥4 地区且三语言非空 |
| `test_hazard_quota` | 危害主题配额约束满足 |

### `.github/workflows/validate.yml`

每次提交自动执行：
1. 从冻结配置**重新生成**数据集
2. 比对 `final/`，若不一致则报错 `final/ is not reproducible from config/`
3. 完整性校验
4. 13 项一致性测试
5. 真实标识黑名单检查

**这是防止"事后调整阈值"的机制保障** —— 改了配置却没重新生成，CI 必然失败。

---

## 8. 常见任务：改什么去哪里

| 我想…… | 改这里 | 之后必须 |
|---|---|---|
| 调整各类别组数 | `config/quotas.json` → `carriers` | 重新生成 + 重新打包 |
| 调整地区或语言分布 | `config/quotas.json` → `regions` | 同上 |
| 改变档位的严格程度 | `config/variant_rules.json` → `variant_rules` | 同上 + 更新 CHANGELOG |
| **调整质量分级阈值** | `config/variant_rules.json` → `quality_grades` | ⚠️ **已冻结，不应改**；改了则旧结论作废 |
| 新增一种版面 | `config/layout_templates_R*.json` | 重新生成 |
| 新增一种不一致类型 | `config/anomaly_types.json` + `src/variants.py`（加算子） | 重新生成 |
| **提升文字密度 / 降低重复** | `src/sentences.py`（扩充语句库） | 重新生成 |
| 改提示词的措辞或约束 | `src/render.py` | 重新生成 |
| 改虚构主体 | `config/fiction_library.json` | 重新生成 |
| 新增导出格式 | `src/export_txt.py`（参照现有实现） | — |
| 出图后补实测字段 | 新建脚本，读 `final/*.jsonl` 写回 | 更新 `release_manifest.json` |

---

## 9. 数据流全链路

```
quotas.json ─┐
             ├─► build_plan() ──► 1000 个基础组
             │                       │
             │           ┌───────────┴───────────┐
             │           ▼                       ▼
             │    layout_templates_R*.json    fiction_library.json
             │           │                       │
             │           └───────┬───────────────┘
             │                   ▼
             │            content.py ──► fields（文字级真值）
             │                   │            ↑
             │                   │      sentences.py（语句库）
             │                   ▼
             │            variants.py ──► 三套 fields + 标注
             │                   │            ↑
             │                   │      variant_rules.json（档位判据）
             │                   ▼
             │            render.py ──► prompt 文本
             │                   │            ↑
             │                   │      prompt_templates.json
             │                   ▼
             └────► generate.py ──► final/*.jsonl / *.csv / *.txt / qa_report
                                            │
                        ┌───────────────────┼───────────────────┐
                        ▼                   ▼                   ▼
                 verify_saved.py    export_txt.py    tests/ + CI
                 （完整性）          （纯文本导出）    （不变量校验）
```
