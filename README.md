# ICS-Text Dataset

ICS-Text is a dataset package for **joint entity and relation extraction** in Industrial Control System (ICS) text.  
This release reorganizes the dataset into a GitHub-friendly layout while keeping the three JSONL split files unchanged.

## Repository structure

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

## Dataset summary

| Split | Samples | Documents | Entities | Relations |
|---|---:|---:|---:|---:|
| Train | 6,650 | 332 | 43,194 | 21,301 |
| Validation | 950 | 48 | 6,165 | 3,032 |
| Test | 1,900 | 95 | 12,326 | 6,061 |
| **Total** | **9,500** | **475** | **61,685** | **30,394** |

The dataset defines **7 entity types** and **5 relation types**. See `metadata/schema.json` for the canonical label inventory.

### Entity types

- `control_device`
- `communication_device`
- `computing_storage_device`
- `management_platform`
- `deployment_location`
- `firmware_protocol_parameter`
- `security_authentication_parameter`

### Relation types

- `connected-to`
- `communicates-with`
- `located-in`
- `composed-of`
- `configured-with`

## Data format

Each line in a split file is one JSON object. The main fields are:

- `id`: sample identifier
- `doc_id`: document/group identifier
- `split`: `train`, `validation`, or `test`
- `text`: source text
- `tokens`: tokenized text
- `entities`: entity annotations with `id`, `start`, `end`, `text`, and `type`
- `relations`: relation annotations with `head`, `tail`, and `type`
- `flags`: sample-level indicators such as relation overlap and nested entities

Character offsets use Python-style half-open spans: `text[start:end] == entity["text"]`.

Example:

```json
{
    "doc_id":  "train-doc-0000",
    "entities":  [
                     {
                         "end":  38,
                         "id":  0,
                         "start":  0,
                         "text":  "industrial control management platform",
                         "type":  "management_platform"
                     },
                     {
                         "end":  57,
                         "id":  1,
                         "start":  54,
                         "text":  "RTU",
                         "type":  "control_device"
                     },
                     {
                         "end":  155,
                         "id":  2,
                         "start":  133,
                         "text":  "intelligent controller",
                         "type":  "control_device"
                     },
                     {
                         "end":  191,
                         "id":  3,
                         "start":  174,
                         "text":  "industrial server",
                         "type":  "computing_storage_device"
                     },
                     {
                         "end":  295,
                         "id":  4,
                         "start":  273,
                         "text":  "intelligent controller",
                         "type":  "control_device"
                     },
                     {
                         "end":  337,
                         "id":  5,
                         "start":  312,
                         "text":  "industrial switch cabinet",
                         "type":  "deployment_location"
                     }
                 ],
    "flags":  {
                  "has_nested_entity":  false,
                  "has_polysemous_entity":  false,
                  "has_relation_overlap":  false,
                  "is_long":  true
              },
    "id":  "ics-train-00000",
    "relations":  [
                      {
                          "head":  0,
                          "tail":  1,
                          "type":  "composed-of"
                      },
                      {
                          "head":  2,
                          "tail":  3,
                          "type":  "communicates-with"
                      },
                      {
                          "head":  4,
                          "tail":  5,
                          "type":  "located-in"
                      }
                  ],
    "split":  "train",
    "text":  "industrial control management platform is composed of RTU. The topology description also records the relevant redundancy policy, and intelligent controller communicates with industrial server. The site engineer verified the device state after the scheduled inspection, and intelligent controller is installed in industrial switch cabinet.",
    "tokens":  [
                   "industrial",
                   "control",
                   "management",
                   "platform",
                   "is",
                   "composed",
                   "of",
                   "RTU",
                   ".",
                   "The",
                   "topology",
                   "description",
                   "also",
                   "records",
                   "the",
                   "relevant",
                   "redundancy",
                   "policy",
                   ",",
                   "and",
                   "intelligent",
                   "controller",
                   "communicates",
                   "with",
                   "industrial",
                   "server",
                   ".",
                   "The",
                   "site",
                   "engineer",
                   "verified",
                   "the",
                   "device",
                   "state",
                   "after",
                   "the",
                   "scheduled",
                   "inspection",
                   ",",
                   "and",
                   "intelligent",
                   "controller",
                   "is",
                   "installed",
                   "in",
                   "industrial",
                   "switch",
                   "cabinet",
                   "."
               ]
}
```

## Quick start

```python
import json

with open("data/train.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        sample = json.loads(line)
        print(sample["id"], sample["text"])
        break
```

## Validation

The package includes a standard-library-only validation script:

```bash
python scripts/validate_dataset.py
```

It checks JSON parsing, split labels, unique sample IDs, entity types, relation types, character offsets, relation references, split-level counts, and SHA-1 hashes.

## Integrity

The split files are preserved byte-for-byte from the supplied final dataset package.  
Expected hashes are recorded in `metadata/checksums.sha1` and `metadata/dataset_stats.json`.

## Dataset card

See [`DATASET_CARD.md`](DATASET_CARD.md) for split statistics, schema details, annotation format, and release notes.

## License and citation

The supplied source archive did **not** include a license file or complete citation metadata. Before public release, the repository owner should add the intended `LICENSE` and the final paper citation/DOI. No license has been invented or assigned in this repackaging.
