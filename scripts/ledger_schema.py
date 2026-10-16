"""Shared schema vocabulary and conservative task aliases for ledger maintenance."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT/'references/taxonomy_schema.json').read_text())
SCHEMA_VERSION = SCHEMA['version']
TASK_ALIASES = SCHEMA.get('task_aliases', {})
def canonical_task(value):
    return TASK_ALIASES.get(value, value)
def canonical_tasks(values):
    return list(dict.fromkeys(canonical_task(v) for v in values if v))
