#!/usr/bin/env python3
"""Validate the ICS-Text GitHub release using only the Python standard library."""

from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
META = ROOT / "metadata"

SPLITS = ("train", "validation", "test")


def fail(message):
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def main():
    schema = json.loads((META / "schema.json").read_text(encoding="utf-8"))
    stats = json.loads((META / "dataset_stats.json").read_text(encoding="utf-8"))
    entity_types = set(schema["entity_types"])
    relation_types = set(schema["relation_types"])

    print("ICS-Text validation")
    print("=" * 72)

    for split in SPLITS:
        path = DATA / f"{split}.jsonl"
        raw = path.read_bytes()
        sha1 = hashlib.sha1(raw).hexdigest()
        expected = stats["splits"][split]

        if sha1 != expected["sha1"]:
            fail(f"{split}: SHA-1 mismatch: {sha1} != {expected['sha1']}")

        sample_ids = set()
        doc_ids = set()
        sentences = entities_total = relations_total = 0

        with path.open("r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError as exc:
                    fail(f"{split}:{line_no}: invalid JSON: {exc}")

                sentences += 1

                if obj.get("split") != split:
                    fail(f"{split}:{line_no}: split field is {obj.get('split')!r}")

                sample_id = obj.get("id")
                if sample_id in sample_ids:
                    fail(f"{split}:{line_no}: duplicate sample id {sample_id!r}")
                sample_ids.add(sample_id)
                doc_ids.add(obj.get("doc_id"))

                text = obj.get("text", "")
                entities = obj.get("entities", [])
                relations = obj.get("relations", [])
                entities_total += len(entities)
                relations_total += len(relations)

                entity_by_id = {}
                for ent in entities:
                    entity_id = ent["id"]
                    if entity_id in entity_by_id:
                        fail(f"{split}:{line_no}: duplicate entity id {entity_id}")
                    entity_by_id[entity_id] = ent

                    if ent["type"] not in entity_types:
                        fail(f"{split}:{line_no}: unknown entity type {ent['type']!r}")

                    start, end = ent["start"], ent["end"]
                    if text[start:end] != ent["text"]:
                        fail(
                            f"{split}:{line_no}: offset mismatch for entity {entity_id}: "
                            f"{text[start:end]!r} != {ent['text']!r}"
                        )

                for rel in relations:
                    if rel["type"] not in relation_types:
                        fail(f"{split}:{line_no}: unknown relation type {rel['type']!r}")
                    if rel["head"] not in entity_by_id:
                        fail(f"{split}:{line_no}: missing head entity {rel['head']}")
                    if rel["tail"] not in entity_by_id:
                        fail(f"{split}:{line_no}: missing tail entity {rel['tail']}")

        observed = {
            "sentences": sentences,
            "documents": len(doc_ids),
            "entities": entities_total,
            "relations": relations_total,
        }

        for key, value in observed.items():
            if value != expected[key]:
                fail(f"{split}: {key} mismatch: {value} != {expected[key]}")

        print(
            f"[OK] {split:10s} "
            f"samples={sentences:4d} docs={len(doc_ids):3d} "
            f"entities={entities_total:5d} relations={relations_total:5d} "
            f"sha1={sha1}"
        )

    print("=" * 72)
    print("[OK] All validation checks passed.")


if __name__ == "__main__":
    main()
