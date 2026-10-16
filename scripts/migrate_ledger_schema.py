"""Migrate maintained records without changing bibliographic metadata or module identity."""
import json
import classification_manager as manager
from ledger_schema import SCHEMA_VERSION, canonical_tasks

def migrate(rows):
    for row in rows:
        original = json.loads(row.get('task_aliases_source_json') or '{}')
        original.setdefault('other', row['task_axis_other'])
        original.setdefault('module_tasks', {})
        row['task_axis_other'] = '; '.join(canonical_tasks([v.strip() for v in row['task_axis_other'].split(';')]))
        modules = json.loads(row['reviewed_modules_json'])
        for module in modules:
            for field in ('tasks', 'other_tasks'):
                if field not in module: continue
                old = module[field]; new = canonical_tasks(old)
                if old != new:
                    original['module_tasks'].setdefault(module['id'], {}).setdefault(field, old)
                    module[field] = new
        row['reviewed_modules_json'] = json.dumps(modules, ensure_ascii=False)
        row['task_aliases_source_json'] = json.dumps(original, ensure_ascii=False)
        row['taxonomy_schema_version'] = SCHEMA_VERSION
        row.setdefault('official_resources_json', '[]')
        row.setdefault('resource_review_status', 'pending')
        row.setdefault('boundary_review_json', '{}')
    return rows

if __name__ == '__main__':
    rows=migrate(manager.read_csv(manager.LEDGER))
    manager.write_csv(rows);manager.generate_json(rows)
    print(f'Migrated {len(rows)} records to schema {SCHEMA_VERSION}')
