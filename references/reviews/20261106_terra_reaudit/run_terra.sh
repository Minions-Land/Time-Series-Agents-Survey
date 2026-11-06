#!/usr/bin/env bash
# One Codex CLI run per paper (gpt-6.1-terra). Resumable: a key whose out/<key>.json parses is skipped.
#   bash run_terra.sh [parallel_jobs] [keys_file]     e.g.  bash run_terra.sh 1 keys_pilot.txt
# Run on H20 inside tmux, from a login shell (so CODEX_HOME is set):  bash -lc 'bash run_terra.sh 4'
# The H20 kernel cannot start the bwrap sandbox, so runs use danger-full-access; the prompt confines writes to out/<key>*.json.
set -u
W="$(cd "$(dirname "$0")" && pwd)"
P="${1:-4}"
KEYS="${2:-$W/keys_ready.txt}"
MODEL="${TERRA_MODEL:-gpt-6.1-terra}"
EFFORT="${TERRA_EFFORT:-high}"
mkdir -p "$W/out" "$W/logs"

prompt() {
cat <<EOF
You are re-auditing ONE Paper Card for a literature survey. Work only inside $W/.
Paper key: $1

1. Read $W/CODER_BRIEF.md and $W/rubric_tree.yaml in full. They are binding.
2. Read the whole packet $W/packets/$1.txt (method, setup and experiments, not only the abstract).
3. Step A: write $W/out/$1.blind.json exactly as the brief specifies, BEFORE opening the current card.
4. Step B: read $W/cards/$1.json, reconcile, and write the final $W/out/$1.json.

Do not read any other paper's packet, card or output, and do not modify any other file. Quotes must be verbatim
from the packet (without the "L<n>: " prefix). Output valid JSON only in those files.
When done, print one line: "$1: modules N, changed M, needs_human_review true|false".
EOF
}

job() {
  local k="$1" out="$W/out/$1.json"
  if python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$out" 2>/dev/null; then echo "skip $k"; return 0; fi
  local t0=$(date +%s)
  timeout 2700 codex exec --skip-git-repo-check -C "$W" -m "$MODEL" --sandbox danger-full-access \
    -c model_reasoning_effort="\"$EFFORT\"" "$(prompt "$k")" > "$W/logs/$k.log" 2>&1
  local rc=$? ok=no
  python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$out" 2>/dev/null && ok=yes
  echo "$(date +%H:%M:%S) $k exit=$rc json=$ok $(( $(date +%s) - t0 ))s"
}
export -f job prompt
export W MODEL EFFORT

grep -v '^\s*$' "$KEYS" | xargs -P "$P" -I{} bash -c 'job "$@"' _ {} | tee -a "$W/logs/run.log"
echo "finished: $(ls "$W"/out/*.json 2>/dev/null | grep -vc blind) final outputs"
