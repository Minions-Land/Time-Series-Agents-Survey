"""Shared schema vocabulary and conservative task aliases for ledger maintenance."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT/'references/taxonomy_schema.json').read_text())
SCHEMA_VERSION = SCHEMA['version']
TASK_ALIASES = SCHEMA.get('task_aliases', {})
LAYERS = tuple(SCHEMA['contribution_layers'])
DIMENSIONS = tuple(SCHEMA['dimensions'])
RETIRED_DIMENSIONS = SCHEMA.get('retired_dimensions', {})
TASK_FAMILIES = tuple(SCHEMA['task_families'])
FUNCTIONS = tuple(SCHEMA['temporal_function_view']['values'])
VIEW_STATUSES = tuple(SCHEMA['temporal_function_view']['applicability'])
LAYER_VIEW_STATUS = SCHEMA['layer_view_status']
LLM_ROUTES = tuple(SCHEMA['llm_routes'])
MODULE_ROLES = tuple(SCHEMA['module_roles'])
CONFIDENCE = tuple(SCHEMA['module_confidence'])
ROLES_OF_WORK = tuple(SCHEMA['roles_of_work'])
EVALUATION_CRITERIA = tuple(SCHEMA['evaluation_criteria'])
REVIEW_STATES = tuple(SCHEMA['review_states'])
def canonical_task(value):
    return TASK_ALIASES.get(value, value)
def canonical_tasks(values):
    return list(dict.fromkeys(canonical_task(v) for v in values if v))
def dimension_errors(dimensions):
    """Name every label outside the five dimensions; retired seven-dimension labels are named as such."""
    return [f'retired dimension {d!r}' if d in RETIRED_DIMENSIONS else f'unknown dimension {d!r}'
            for d in dimensions if d not in DIMENSIONS]
