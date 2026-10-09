# ICS-Text 数据集

ICS-Text 是一个面向**工业控制系统（ICS）文本实体—关系联合抽取**的数据集。本版本将原始数据重新整理为适合 GitHub 发布的目录结构，同时保持 `train.jsonl`、`validation.jsonl` 和 `test.jsonl` 三个数据文件的内容不变。

## 目录结构

```text
ics-text-dataset/
├── README.md
├── README_zh-CN.md
├── DATASET_CARD.md
├── .gitignore
├── data/
│   ├── train.jsonl
│   ├── validation.jsonl
│   └── test.jsonl
├── metadata/
│   ├── schema.json
│   ├── dataset_stats.json
│   └── checksums.sha1
└── scripts/
    └── validate_dataset.py
```

## 数据集规模

| 划分 | 样本数 | 文档数 | 实体数 | 关系数 |
|---|---:|---:|---:|---:|
| Train | 6,650 | 332 | 43,194 | 21,301 |
| Validation | 950 | 48 | 6,165 | 3,032 |
| Test | 1,900 | 95 | 12,326 | 6,061 |
| **总计** | **9,500** | **475** | **61,685** | **30,394** |

数据集包含 **7 类实体**和 **5 类关系**，标准标签定义见 `metadata/schema.json`。

## 数据格式

每个 JSONL 文件一行对应一个 JSON 样本，主要字段包括：

- `id`：样本 ID
- `doc_id`：文档/分组 ID
- `split`：数据划分
- `text`：原始文本
- `tokens`：分词结果
- `entities`：实体标注，包含 `id`、`start`、`end`、`text`、`type`
- `relations`：关系标注，包含 `head`、`tail`、`type`
- `flags`：关系重叠、嵌套实体、长文本等样本级标记

实体字符位置采用左闭右开区间，即 `text[start:end] == entity["text"]`。

## 完整性检查

运行：

```bash
python scripts/validate_dataset.py
```

脚本会检查 JSON 格式、数据划分、样本 ID、实体/关系类型、实体字符偏移、关系实体引用、各划分统计量以及 SHA-1 哈希。

## 发布说明

本次整理保留了最终三份 JSONL 数据文件的原始字节内容，并将标准 schema、最终统计信息、校验值和验证脚本一并整理到仓库中。

原压缩包中的 `generation_console.json` 与最终 JSONL 文件的统计量及 SHA-1 不一致，属于生成过程中的旧版/中间统计信息，因此未放入公开发布包，以避免与 `dataset_stats.json` 混淆。

## License 与引用

原始压缩包未包含 License 文件，也没有完整的论文引用元数据。正式公开发布前，请由仓库所有者补充最终采用的 `LICENSE`，以及论文的完整作者、年份、期刊/会议、DOI 等引用信息。本次整理未擅自指定任何开源许可证。
