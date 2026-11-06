#!/usr/bin/env bash
# Fetch arXiv PDFs listed in missing_pdfs.tsv (key<TAB>arxiv_id<TAB>title) into references/pdfs/, resumable.
cd "$(dirname "$0")/../../.."
fetch() { k=$1; a=$2; f=references/pdfs/$k.pdf
  for i in 1 2 3 4 5; do
    curl -sSL -C - -x "${FETCH_PROXY:-http://127.0.0.1:27891}" -A "Mozilla/5.0" -o "$f.part" "https://arxiv.org/pdf/$a" && head -c4 "$f.part" | grep -q %PDF && mv "$f.part" "$f" && { echo "ok $k"; return; }
    sleep 5; done; echo "FAIL $k"; }
export -f fetch
cut -f1,2 references/reviews/20261106_terra_reaudit/missing_pdfs.tsv | while read k a; do [ -s references/pdfs/$k.pdf ] || echo "$k $a"; done | xargs -P 7 -n 2 bash -c "fetch \$0 \$1"
echo DONE
