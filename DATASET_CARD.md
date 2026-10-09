# Dataset Card: ICS-Text

## Overview

ICS-Text is organized for joint entity and relation extraction in Industrial Control System (ICS) text. The public package contains three JSONL splits, a canonical schema, dataset statistics, integrity hashes, and a validation script.

## Splits

| Split | Samples | Documents | Entities | Relations | Avg. sentence length | Relation overlap | Nested entity | Polysemous entity |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Train | 6,650 | 332 | 43,194 | 21,301 | 44.27 | 52.41% | 15.67% | 34.60% |
| Validation | 950 | 48 | 6,165 | 3,032 | 44.39 | 52.42% | 15.16% | 34.63% |
| Test | 1,900 | 95 | 12,326 | 6,061 | 44.33 | 52.42% | 15.26% | 34.58% |

Total: **9,500 samples**, **475 documents**, **61,685 entity mentions**, and **30,394 relation instances**.

## Label schema

### Entity labels

| Label | Count |
|---|---:|
| `control_device` | 16,908 |
| `communication_device` | 13,319 |
| `deployment_location` | 11,951 |
| `firmware_protocol_parameter` | 5,702 |
| `management_platform` | 5,190 |
| `computing_storage_device` | 5,039 |
| `security_authentication_parameter` | 3,576 |

### Relation labels

| Label | Count |
|---|---:|
| `located-in` | 11,586 |
| `configured-with` | 8,110 |
| `communicates-with` | 4,187 |
| `connected-to` | 3,681 |
| `composed-of` | 2,830 |

## Record schema

Each JSONL record contains:

```text
id: string
doc_id: string
split: string
text: string
tokens: list[string]
entities: list[
  {
    id: integer,
    start: integer,
    end: integer,
    text: string,
    type: entity_label
  }
]
relations: list[
  {
    head: entity_id,
    tail: entity_id,
    type: relation_label
  }
]
flags: {
  has_nested_entity: boolean,
  has_polysemous_entity: boolean,
  has_relation_overlap: boolean,
  is_long: boolean
}
```

`start` is inclusive and `end` is exclusive.

## Integrity and validation

The release package was checked for:

- valid JSON on every line;
- unique sample IDs within each split;
- split-field consistency;
- entity labels restricted to the canonical schema;
- relation labels restricted to the canonical schema;
- exact entity span/text agreement;
- valid relation head/tail references;
- split-level sample/document/entity/relation counts;
- SHA-1 agreement with the supplied final statistics.

All checks passed for the packaged release.

## Source-package cleanup

The source archive contained both `dataset_stats.json` and `generation_console.json`. The latter described different entity/relation counts and different SHA-1 hashes from the final JSONL files. Because `dataset_stats.json` matches the packaged JSONL files exactly, it is treated as the authoritative statistics file. `generation_console.json` is therefore excluded from the public GitHub package to avoid publishing stale/intermediate metadata.

No dataset records were rewritten during repackaging.

## Known publication metadata gaps

The source archive did not include:

- a license;
- complete bibliographic/citation metadata;
- a DOI or permanent dataset identifier.

These should be added by the repository owner before the repository is announced as the canonical public release.
