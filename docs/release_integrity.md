# 发布完整性

## 1. 校验方式

```bash
python3 src/verify_saved.py          # 校验现有文件
python3 src/verify_saved.py --write  # 重新生成哈希与清单
```

## 2. 校验内容

| 项目 | 说明 |
|---|---|
| 文件哈希 | `release_manifest.json` 的 `file_hashes` 与磁盘实际内容比对 |
| 内容哈希 | 提示词与组记录的规范化哈希 |
| 冻结阈值 | `quality_grades` 的哈希与发布时比对；若被改动即报错 |
| 配额配置 | `quotas.json` 的哈希 |
| 版面模板 | 全部版面模板的哈希 |

## 3. 冻结与可复现

- 生成过程完全确定：`src/common.py` 的 `rng_for()` 以字符串键派生随机源，
  **不依赖调用顺序**，因此同一份配置必然产出同一份数据集；
- CI 每次提交都会重新生成 `final/` 并与仓库内容比对，
  若不一致则报错 `final/ is not reproducible from config/`；
- 因此**任何配额或阈值的改动都必须同时提交重新生成的 `final/`**，
  否则 CI 会失败——这是防止"事后调整阈值"的机制保障。

## 4. 版本升级流程

1. 修改 `config/` 下的相应文件；
2. 递增 `release_manifest.json` 的 `version`；
3. 在 `CHANGELOG.md` 中记录改动原因；
4. 重新运行 `python3 src/generate.py`；
5. 重新运行 `python3 src/verify_saved.py --write`；
6. 运行 `python3 tests/test_release_consistency.py`。

## 5. 注意

**质量分级阈值一经发布即不得调整。** 若在生成图像后发现 A 级样本不足而回调阈值，
该版本的全部结论作废，应如实报告统计功效不足。
