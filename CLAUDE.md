<!-- PROJECT-MANAGEMENT:AGENT-CONTEXT:START -->
# ProjectManagement Agent Context

Work directly in this project's canonical directory:
- project_id: `IJCAI2027-TIME-SERIES-AGENTS-SURVEY`
- Feishu record: `pending`
- project root: `/mnt/aliyunsb/ProjectManagement/IJCAI2027-Time-Series-Agents-Survey`

Basic rules:
- Keep code, docs, environments, caches, logs, temporary output, and experiments inside this root or an explicitly registered path under /mnt/aliyunsb.
- Start Codex/Claude/shell/SSH/tmux from this root or a subdirectory. Unique tmux names and pm run are optional.
- Load credentials from the central ProjectManagement .secrets vault; never copy keys into files, logs, prompts, Git, or Feishu.
- Use small Git commits and relevant tests. Avoid unbounded recursive scans and full-tree hashes.
- Experiment Supervisor is optional and is not a coding/session gate.
- Do not inspect or manage `/mnt/aliyunsb/frontsea`.

Legacy PM-DRIFT-001/PM-BIO-001 and fixed tmux/session mappings are opt-in for migrations or production experiments only.
<!-- PROJECT-MANAGEMENT:AGENT-CONTEXT:END -->
