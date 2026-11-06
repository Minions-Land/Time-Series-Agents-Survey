#!/usr/bin/env bash
# One Codex CLI run per paper (gpt-6.1-terra). Resumable: a key whose out/<key>.json parses is skipped.
#   bash run_terra.sh [parallel_jobs] [keys_file]     e.g.  bash run_terra.sh 1 keys_pilot.txt
# Run on H20 inside tmux, from a login shell (so CODEX_HOME is set):  bash -lc 'bash run_terra.sh 4'
# The H20 kernel cannot start the bwrap sandbox, so runs use danger-full-access, but Codex writes NO files: its final
# message (captured by --output-last-message outside the agent) is split into out/<key>.blind.json and out/<key>.json.
set -u
W="$(cd "$(dirname "$0")" && pwd)"
P="${1:-4}"
KEYS="${2:-$W/keys_ready.txt}"
MODEL="${TERRA_MODEL:-gpt-6.1-terra}"
EFFORT="${TERRA_EFFORT:-high}"
# Codex runs inside a bwrap that leaves only /mnt writable; its final message is captured there, then copied here.
LAST="${REAUDIT_LAST_DIR:-/mnt/.pm-agent/default/tmp/ts_survey_reaudit}"
mkdir -p "$W/out" "$W/logs" "$LAST"

prompt() {
cat <<EOF
You are re-auditing ONE Paper Card for a literature survey. Read-only task: work only inside $W/.
Paper key: $1

1. Read $W/CODER_BRIEF.md and $W/rubric_tree.yaml in full. They are binding.
2. Read the whole packet $W/packets/$1.txt (method, setup and experiments, not only the abstract).
3. Step A: complete the blind classification BEFORE opening the current card.
4. Step B: read $W/cards/$1.json, reconcile, and produce the final record.

DO NOT create, modify or delete any file, and do not run mount, sudo, chmod, chown or any system command; only read
files (cat, sed, grep, rg, python3 for reading). Your FINAL MESSAGE must be exactly one JSON object and nothing else:
{"blind": <Step A record>, "final": <Step B record>}, both following the schema in CODER_BRIEF.md (blind without
"reconciliation"). The runner saves it. Quotes must be verbatim from the packet (without the "L<n>: " prefix).
Before your final message, check that it parses: pipe the exact JSON into
python3 -c 'import json,sys; json.load(sys.stdin); print("valid")' via a heredoc (this reads stdin only), fix any error.
EOF
}

split_last() {  # turn the final message into out/<key>.blind.json and out/<key>.json
python3 - "$1" "$W/out" "$LAST" <<'PY'
import json, re, sys
key, outdir, last = sys.argv[1], sys.argv[2], sys.argv[3]
txt = open(last + '/' + key + '.last.txt').read().strip()
obj, dec = None, json.JSONDecoder()
for i in [j for j, c in enumerate(txt) if c == '{'][:50]:   # raw_decode ignores trailing text, e.g. one extra '}'
    try: cand, _ = dec.raw_decode(txt[i:])
    except ValueError: continue
    if isinstance(cand, dict) and 'blind' in cand and 'final' in cand: obj = cand; break
if obj is None: raise SystemExit('no {"blind","final"} object in final message')
for name, part in (('blind', obj['blind']), ('final', obj['final'])):
    path = outdir + '/' + key + ('.blind.json' if name == 'blind' else '.json')
    with open(path, 'w') as f: json.dump(part, f, ensure_ascii=False, indent=1)
PY
}

job() {
  local k="$1" out="$W/out/$1.json"
  if python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$out" 2>/dev/null; then echo "skip $k"; return 0; fi
  local t0=$(date +%s) rc=0 try
  for try in 1 2 3 4 5 6; do      # provider outages (503 / no channel) are retried every 10 minutes
    rm -f "$LAST/$k.last.txt"
    timeout 2700 codex exec --skip-git-repo-check -C "$W" -m "$MODEL" --sandbox danger-full-access \
      -o "$LAST/$k.last.txt" -c model_reasoning_effort="\"$EFFORT\"" "$(prompt "$k")" > "$W/logs/$k.log" 2>&1
    rc=$?
    [ -s "$LAST/$k.last.txt" ] && cp "$LAST/$k.last.txt" "$W/logs/" && split_last "$k" 2>> "$W/logs/$k.log"
    python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$out" 2>/dev/null && break
    [ -s "$LAST/$k.last.txt" ] && cp "$LAST/$k.last.txt" "$W/logs/$k.fail$try.txt"
    if [ -s "$LAST/$k.last.txt" ]; then [ "$try" -lt 3 ] && { echo "$(date +%H:%M:%S) $k unparsable final message, rerun"; continue; }; break; fi
    grep -q -E "503 Service Unavailable|无可用渠道|at capacity|429 Too Many Requests|rate limit" "$W/logs/$k.log" || break
    echo "$(date +%H:%M:%S) $k provider unavailable, retry $try in 600s"; sleep 600
  done
  local ok=no
  python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$out" 2>/dev/null && ok=yes
  echo "$(date +%H:%M:%S) $k exit=$rc json=$ok $(( $(date +%s) - t0 ))s"
}
export -f job prompt split_last
export W MODEL EFFORT LAST

grep -v '^\s*$' "$KEYS" | xargs -P "$P" -I{} bash -c 'job "$@"' _ {} | tee -a "$W/logs/run.log"
echo "finished: $(ls "$W"/out/*.json 2>/dev/null | grep -vc blind) final outputs"
