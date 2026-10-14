# news_rumor_prompts_3000

面向 **富文字 AIGC 图像生成与检测研究** 的提示词数据集，覆盖新闻谣言类图像的四种载体形态。
共 **1000 个基础组 × 3 档变体 = 3000 条**提示词，可直接输入 GPT Image 2 / GPT Image 2.5 等文生图模型。

每条提示词都完整写明：载体与画幅、版面分区顺序与占比、拍摄与呈现方式、配色与排版细节、
**文字密度目标**、图中必须出现的每一段文字（逐字写在「」内）及其所在分区，
以及允许和禁止出现的视觉元素。正文中位长度约 2000 字，尽量不留给模型自由发挥的空间。

> 生成模板、所用模型与生成思路见 [`docs/generation_approach.md`](docs/generation_approach.md)；
> 仓库各文件的作用与依赖关系见 [`docs/repository_structure.md`](docs/repository_structure.md)。

> 所有机构、媒体、企业、地名、人名、联系方式与编号均为虚构。
> 地址采用「真实地级市 + 虚构区/街道」，电话使用保号段，编号格式正确但不对应任何现实主体。
> 数据中按研究设计设置的内容不一致仅用于研究，不指向任何现实事件或主体。

---

## 数据集结构

### 三联结构：1000 个基础组 × 3 档

| variant | 含义 | 条数 |
|---|---|---:|
| `clean` | 正常样本，字段之间完全自洽 | 1000 |
| `subtle` | 轻微不一致：改动 1–2 处文字字段，画面仍为完全正常的版式设计 | 1000 |
| `strong` | 明显不一致：改动 ≥2 处字段或多处规则违反，画面仍为正常的版式设计 | 1000 |

同一组的三个版本**共用**同一主体、媒体、载体、构图、配色与版式，**仅关键文字字段不同**，可直接用于成对比较。

**档位由可计算量定义，不由主观明显程度判断**（详见 `config/variant_rules.json`）：

| variant | `changed_field_count` | `rule_failure_count` |
|---|---:|---:|
| `clean` | 0 | 0 |
| `subtle` | 1–2 | 1–2 |
| `strong` | ≥2 | ≥2 |

连带失败单列于 `collateral_failure_count`，不计入 `rule_failure_count`，避免单处改动引发多处崩塌被误算为多处独立异常。

**不一致文字不做任何视觉标记**：不圈出、不加警示、不用异色，而是自然融入原设计。提示词中显式要求模型"不要自动纠正、补全或统一"。

---

## 类别体系

### 一级类别（载体形态）

类别按**视觉载体形态**划分，不按新闻主题划分。主题数量无限且不决定检测难度；载体形态直接决定版式、文字密度、界面元素与画幅。

| 编号 | 载体子类 | 基础组 | 提示词 |
|---|---|---:|---:|
| R1 | 社交平台帖文图文 | 300 | 900 |
| R2 | 短视频平台竖屏图文 | 250 | 750 |
| R3 | 新闻媒体版式 | 250 | 750 |
| R4 | 图文信息卡 | 200 | 600 |
| **合计** | | **1000** | **3000** |

二级类别共 24 种，见 [`docs/taxonomy.md`](docs/taxonomy.md)。

### 媒体与平台覆盖

按**界面范式**聚类覆盖 5 个平台族，而非逐一枚举平台：

| 平台族 | 代表载体 |
|---|---|
| 中文社交 | 微博、微信公众号文章页、头条 |
| 英文社交 | X、Facebook、Threads |
| 图片社交 | Instagram、小红书、Pinterest |
| 短视频 | 抖音、快手、TikTok、YouTube Shorts |
| 通讯社与主流媒体 | 新华社、央视、人民日报、路透、美联、BBC、CNN |

### 语言与地区覆盖

覆盖 **3 种语言 × 7 个地区**：

| 地区 | 语言 | 基础组 |
|---|---|---:|
| 中国内地 | zh-Hans | 331 |
| 北美 | en | 180 |
| 台湾地区 | zh-Hant | 129 |
| 英国 | en | 111 |
| 香港地区 | zh-Hant | 109 |
| 澳大利亚 | en | 71 |
| 新加坡 | zh-Hans | 69 |

**覆盖约束**：每个载体子类须覆盖至少 4 个地区，且三种语言均不得为空。实测四个载体子类均覆盖全部 7 个地区。

### 危害主题（配额约束）

危害主题不作为类别维度，仅作为配额约束，保证每个载体子类内部主题不单一。

H1 灾害与险情 / H2 公共卫生 / H3 政策与民生 / H4 社会治安与案件 / H5 经济与金融 /
H6 生活与健康认知 / H7 涉外与国际关系 / H8 人物与机构动态 / H9 公共秩序与群体行为

**配额约束及实测**：每个载体子类覆盖 ≥5 种主题（实测 9 种全覆盖）；H1–H4 合计 ≥50%（实测 53.1%）；单一主题 ≤20%（实测最大 14.1%）。

---

## 不一致类型

共 **18 种内容类型 × 10 种规则违反类型**，两者并行记录。

内容类型（`tamper_types`）包括：账号主体、时间信息、地点信息、互动数据、标题与正文冲突、配图与文字不符、引述内容、信息来源归属、事件规模、紧迫性表述、因果关系、处置结果、官方表态、处置建议、文内数字一致性、关键限定缺失、挑动性内容添加、媒体标识。

规则违反类型（`anomaly_category`）包括：日期先后矛盾、数值关系矛盾、集合与范围矛盾、单位与量级不符、信息链断裂或循环、主语与所述行为不符、分项与合计不等、时间落于不合理区间、地点与事件类型不匹配、固定文案被改动。

完整定义见 [`config/anomaly_types.json`](config/anomaly_types.json)。所有规则均标注为 **dataset-designed inconsistency**，不表述为法规结论。

---

## 字段说明

每条提示词记录包含以下字段（完整 schema 见 [`docs/data_fields.md`](docs/data_fields.md)）。

### 定位字段

`prompt_id`、`group_id`、`variant`、`carrier`、`sub_carrier`、`platform_family`、`layout_id`、
`region`、`language`、`hazard`、`aspect_ratio`、`capture_style`、`split`

### 文字规格（机器可读真值）

| 字段 | 说明 |
|---|---|
| `fields` | 逐字段的 `{key, label, value}` 三元组，`value` 为必须出现在图中的字面文本 |
| `visible_text` | 扁平化的逐字字符串列表，可直接用于 OCR 集合比对 |
| `required_fields` | 字段标签列表 |
| `field_count` | 字段数量 |
| `text_density` | 文字密度（测量值，非人工设定） |
| `measured_char_count` | 实测字符数 |

### 变体标注

| 字段 | 说明 |
|---|---|
| `changed_fields` | 被改动的字段 key 列表 |
| `field_changes` | `[{field, label, base_value, value}]`，逐条记录改动前后值 |
| `tamper_types` | 内容不一致类型 |
| `anomaly_category` | 规则违反类型 |
| `changed_field_count` / `rule_failure_count` / `collateral_failure_count` | 档位判据计数 |
| `single_image_detectable` | 单看该图能否发现不一致；`clean` 为 `null`，其余为 `true` |

### 提示词

`prompt` —— 自包含的完整提示词，无需读取同组其他版本或参考图即可使用。

---

## 生成后实测字段

本数据集交付的是**「提示词 + 生成图像 + 生成后实测标签」三元组**，而非仅提示词。
提示词层面的检查不能替代出图后的实测。

生成图像后须记录：

| 字段 | 说明 |
|---|---|
| `ocr_text` | OCR 全文 |
| `ocr_line_boxes` | OCR 行框 |
| `entity_hit_rate` | 确定性命中率 = 召回实体数 / 应出现实体数 |
| `char_error_count` | 错字数 |
| `missing_entities` | 遗漏实体 |
| `extra_text` | 多余文字 |
| `quality_grade` | 质量分级 A/B/C/D |
| `text_mask` | 文字区域掩码 |

### 质量分级（阈值生成前冻结）

| 等级 | 定义 |
|---|---|
| A | 命中率 100%、零错字、无多余文字、文内数字自洽、无明显版式异常 |
| B | 命中率 ≥90%、错字 ≤2、无数字一致性错误 |
| C | 命中率 50–90%，或存在数字一致性错误，或存在明显版式异常 |
| D | 命中率 <50%，或大面积乱码，或版面崩塌 |

**全部等级样本均保留，不因分级结果删除样本。**
阈值哈希记录于 `release_manifest.json` 的 `frozen_quality_threshold_sha256`，生成后不调整。

---

## 划分

`split` 按载体子类与语言分层，比例 80/10/10。
**同一基础组的三档样本落在同一集合**，由 CI 校验（`split_group_atomicity`）。

建议进一步按 `platform_family` 或版式模板分隔训练与测试集；真实图侧应匹配生成图的载体、清晰度、密度与后处理，避免检测器学习采集方式差异。

---

## 反捷径约束

生成后统一处理，避免检测器学到采集方式而非生成痕迹：

- 剥离全部元数据（含 C2PA）
- 短边统一至 1024，保持长宽比
- 中间格式 PNG，最终统一 JPEG q95 重编码
- 训练只看元信息的对照分类器（文件大小 / 文件头 / 颜色直方图 / 尺寸），AUC 须约等于 0.5；任一超过 0.6 视为捷径泄漏

完整约束见 [`config/constraints.json`](config/constraints.json)。

---

## 文件说明

```text
.
├── README.md
├── README_EN.md                          # 英文版说明
├── news_rumor_dataset_taxonomy.md        # 分类体系（配额、档位、阈值在此冻结）
├── CHANGELOG.md
├── SHA256SUMS.txt
├── release_manifest.json
├── config/
│   ├── quotas.json                       # 冻结配额
│   ├── variant_rules.json                # 档位定义与质量阈值
│   ├── anomaly_types.json                # 不一致类型库
│   ├── layout_templates_R1..R4.json      # 版面模板（分区与文字角色）
│   ├── fiction_library.json              # 虚构主体库
│   ├── prompt_templates.json             # 提示词段落模板
│   └── constraints.json                  # 合规与反捷径约束
├── src/
│   ├── common.py                         # 配置加载、配额计划、文字规格原语
│   ├── content.py                        # 按版面角色构建内容
│   ├── variants.py                       # 三档变体派生
│   ├── render.py                         # 提示词拼装（中/英）
│   ├── sentences.py                      # 语句库（危害主题 × 语言）
│   ├── render.py                         # 提示词拼装（中/英）
│   ├── generate.py                       # 入口
│   ├── export_txt.py                     # 导出纯文本（3000 / 30000 条）
│   └── verify_saved.py                   # 发布完整性校验
├── docs/
│   ├── repository_structure.md           # 仓库结构说明（每个文件的作用与依赖关系）
│   ├── generation_approach.md            # 提示词生成技术说明（模板/模型/思路）
│   ├── real_image_sources.md             # 真实图像获取途径调研
│   ├── taxonomy.md                       # 二级类别完整列表
│   ├── data_fields.md                    # 字段字典
│   ├── review_scope.md                   # 审核范围与限制
│   ├── sources_and_limits.md             # 来源说明与局限
│   └── release_integrity.md              # 发布校验说明
├── pilot/                                # 抽样（120 组 / 360 条）
├── final/                                # 全量交付
└── tests/                                # 一致性测试
```

---

## 使用

### 1. 复现或重新生成提示词

```bash
# 全量生成（1000 组 / 3000 条）→ 写入 final/
python3 src/generate.py

# 抽样（前 N 组）→ 写入 pilot/
python3 src/generate.py --limit 120

# 指定输出目录
python3 src/generate.py --out /path/to/dir

# 校验发布完整性（文件哈希 + 冻结阈值）
python3 src/verify_saved.py
python3 src/verify_saved.py --write   # 重新生成哈希与清单

# 一致性测试
python3 tests/test_release_consistency.py
```

无外部依赖，仅需 Python 3.9+。生成过程完全确定，同一份配置必然产出同一份数据。

---

### 1b. 导出为纯文本（含完整元信息的留档格式）

```bash
# 默认：完整元信息块 + 完整提示词（3000 条）
python3 src/export_txt.py

# 附逐字文字清单（visible_text），可直接做 OCR 比对
python3 src/export_txt.py --full

# 只要提示词正文，不带元信息
python3 src/export_txt.py --bare

# 单行元信息（体积小，可读性差）
python3 src/export_txt.py --header-only

# 生成并导出 30000 条
python3 src/export_txt.py --target 30000
```

**默认输出格式**：每条由「元信息块」+「分隔线」+「完整提示词」组成，块之间以**一个空行**分隔。

```
# 00003 | G00001-strong | R1 | zh-Hans | CN | H3 | strong
# tier: strong (3 changed fields, 3 rule violations)
# carrier: R1 社交帖文 / text_only_post | platform: cn_social
# layout: cn_social_text_only | aspect: 1:1 | capture: native_screenshot
# region: CN 中国大陆 | language: zh-Hans | hazard: H3 政策与民生
# density: High (335 chars, cjk) | fields: 22 | split: train
# tamper: location(地点信息), magnitude(事件规模), urgency(紧迫性表述)
# rules: fixed_text(固定文案被改动), number_relation(数值关系矛盾)
# changed: body_text, hashtags, location_label
#   正文：「线上申报系统每日六时至二十四时开放。」→「……开放。据初步统计，受影响范围涉及周边十余个社区。」
#   话题标签：「#热点 #民生 #提示」→「#热点 #民生 #提示 #紧急 #速转扩散」
# single_image_detectable: True
# --------------------------------------------------------------------
生成一张1:1比例的社交媒体平台的帖文截图，……
【顶部栏】「首页」。
【作者信息区】「启明周报」、「启明周报 · 官方账号」、「已认证」。
……
```

**元信息块字段说明**

| 行 | 内容 |
|---|---|
| 首行 | 序号 \| `prompt_id` \| 载体 \| 语言 \| 地区 \| 危害主题 \| 档位 |
| `tier` | 档位及三个计数（改动字段数 / 规则违反数 / 连带失败数） |
| `carrier` | 一级载体 + 二级类别 + 平台族 |
| `layout` | 版面模板 | 画幅 | 拍摄质感 |
| `region` | 地区 + 语言 + 危害主题（均带中文名） |
| `density` | 密度档 + **实测字符数** + 计数口径 | 字段数 | 划分 |
| `tamper` | 内容不一致类型（带中文名）；`clean` 档为 `none` |
| `rules` | 规则违反类型（带中文名） |
| `changed` | 被改动的字段列表 |
| 缩进行 | **逐条改动对照**：`「原值」→「新值」` |
| `single_image_detectable` | 单看该图能否发现不一致 |
| `--full` 追加 | 逐字文字清单（`visible_text`） |

**按空行切分即可还原为独立记录**：

```python
text = open("final/news_rumor_prompts_3000.txt", encoding="utf-8").read()
blocks = [b for b in text.split("\n\n") if b.strip()]
for b in blocks:
    lines = b.split("\n")
    # 元信息以 # 开头，分隔线之后即为提示词正文
    meta = [l for l in lines if l.startswith("#")]
    sep = next(i for i, l in enumerate(lines) if set(l.strip()) <= {"#", "-"})
    prompt = "\n".join(lines[sep + 1:])
```

**关于 `--target`**：按整数倍放大冻结配额，因此**必须是 3000 的整数倍**（基准设计为 1000 组 × 3 档）。
放大后各载体、地区、语言、危害主题的**比例与基准设计一致**，仅总量增加。

> 注意：`--target` 生成的扩大数据集**不写入 `final/` 的基准文件**，也不更新 `release_manifest.json`。
> 基准交付物始终是 1000 组 / 3000 条。

---

### 2. 载入数据

```python
import json

prompts = [json.loads(l) for l in open("final/news_rumor_prompts_3000.jsonl", encoding="utf-8")]
groups  = [json.loads(l) for l in open("final/groups.jsonl", encoding="utf-8")]

# 按条件筛选
subset = [p for p in prompts
          if p["carrier"] == "R3"          # 新闻媒体版式
          and p["language"] == "zh-Hans"   # 简体中文
          and p["variant"] == "strong"     # 明显不一致
          and p["split"] == "train"]

print(len(subset))
```

---

### 3. 提交给文生图模型

**每条 `prompt` 都是自包含的**：无需读取同组其他版本，也无需参考图，直接送入模型即可。

```python
import json

prompts = [json.loads(l) for l in open("final/news_rumor_prompts_3000.jsonl", encoding="utf-8")]

for p in prompts:
    image = call_image_api(
        prompt=p["prompt"],          # 直接使用
        size=SIZE_FOR[p["carrier"]], # 见下表，必须与提示词中的比例一致
        quality="high",              # 文字密集，建议使用最高质量档
    )
    save(image, f"images/{p['prompt_id']}.png")
    record(p["prompt_id"], model_version=SNAPSHOT, size=..., quality=...)
```

#### 3.1 画幅必须与提示词一致

提示词中的比例是文字描述，真正生效的是 API 参数。两者不一致会导致版面错配。

| 载体 | `aspect_ratio` | 建议尺寸 |
|---|---|---|
| R1 | `1:1` | 1024×1024 |
| R1 | `4:5` | 1024×1280 |
| R1 | `3:4` | 1024×1365 |
| R2 | `9:16` | 1024×1792 |
| R3 | `16:9` | 1536×1024 |
| R3 | `16:10` | 1536×960 |
| R3 | `3:4` | 1024×1365 |
| R4 | `4:5` / `9:16` | 1024×1280 / 1024×1792 |

#### 3.2 质量档与模型版本

- **文字密集，建议使用最高质量档**。本数据集 89% 为 High 密度（中位 271 字符），
  质量档过低会使文字不可辨认，样本将被判为 C/D 级而浪费；
- **记录模型版本快照**（如带发布日期的 ID），不要只记模型名。跨版本混合会影响结果的可比性；
- 部分模型不支持 Batch 接口，须逐条调用。

#### 3.3 批量执行的注意事项

- **每条结果立即落盘**（图像 + `prompt_id` + 实际参数），不要等全部完成再统一写入；
- 失败样本单独记录 `failed.jsonl`，含 `prompt_id` 与错误信息；
- **失败样本的丢弃规则须事先确定并写入文档**，否则事后无法说明数据构成；
- 注意速率限制，全量执行建议后台运行。

---

### 4. 划分训练集与测试集

直接使用 `split` 字段。**同一 `group_id` 的三档样本必定落在同一集合**（已由 CI 校验），无需自行处理泄漏。

```python
train = [p for p in prompts if p["split"] == "train"]
val   = [p for p in prompts if p["split"] == "validation"]
test  = [p for p in prompts if p["split"] == "test"]
```

如需自定义划分，请保持**组原子性**，并建议按 `platform_family` 或 `layout_id` 分层。

---

### 5. 使用文字规格做 OCR 比对

`fields[].value` 是"这张图应当出现的字面文字"，`visible_text` 是扁平化字符串列表，二者均可直接用于比对。

```python
import json

p = prompts[0]
expected = p["visible_text"]            # 应当出现的文字
fields   = p["fields"]                  # 逐字段的 {key, label, value}

ocr_result = run_ocr(f"images/{p['prompt_id']}.png")

# 字段级命中率
hit = sum(1 for f in fields if f["value"] and f["value"] in ocr_result)
rate = hit / len([f for f in fields if f["value"]])

# 逐条对照改动前后的值
for c in p["field_changes"]:
    print(f"{c['label']}: {c['base_value']} → {c['value']}")
```

`field_changes` 中的 `base_value` 取自同组 `clean` 版本，可直接用于对照分析。

---

### 6. 出图后必须补充的字段

提示词层面的检查**不能替代**出图后的实测。以下字段在 schema 中预留，须在生成图像并完成 OCR 后填写：

| 字段 | 说明 |
|---|---|
| `ocr_text` | OCR 全文 |
| `ocr_line_boxes` | OCR 行框 |
| `entity_hit_rate` | 确定性命中率 |
| `char_error_count` | 错字数 |
| `missing_entities` | 遗漏实体 |
| `extra_text` | 多余文字 |
| `quality_grade` | 质量分级 A/B/C/D |
| `text_mask` | 文字区域掩码 |

分级阈值见 [`config/variant_rules.json`](config/variant_rules.json)，其哈希记录于 `release_manifest.json`。
**阈值在生成前冻结，不因分级结果回调；全部等级样本均保留，不因分级结果删除样本。**

---

### 7. 生成图像的统一后处理

为免检测器学到采集方式而非生成痕迹，出图后须统一处理：

- 剥离全部元数据（含 C2PA）
- 短边统一至 1024，保持长宽比
- 中间格式 PNG，最终统一 JPEG q95 重编码
- 训练只看元信息的对照分类器（文件大小 / 文件头 / 颜色直方图 / 尺寸），AUC 须约等于 0.5；任一超过 0.6 视为捷径泄漏

详见 [`config/constraints.json`](config/constraints.json)。

---

### 8. 修改配置后必须重新生成

`config/` 下的任何改动都需重新运行 `python3 src/generate.py` 并提交更新后的 `final/`，
否则 CI 会因数据与配置不一致而失败。这是防止事后调整阈值或配额的机制保障。

版本升级流程见 [`docs/release_integrity.md`](docs/release_integrity.md)。

---

## 已知限制

- 内容为程序按内容库拼装，**未经真实业务机构核验**，不代表任何现实事件；
- 档位计数为**设计期**判据，图像难度需生成后实测确认；
- 质量分级 A/B/C/D 需在出图并完成 OCR 后填写，本仓库暂未包含生成图像；
- 提示词层面的抽检不能替代出图后的人工检查；
- 单张图像的**长句文本不保证完全无重复**：版面槽位多于语句库条目时，会以短句补足，
  实测约 14.5% 的样本存在长句复用（集中在英文短句）。如需完全无重复，可扩充
  `src/sentences.py` 的语句库后重新生成。
