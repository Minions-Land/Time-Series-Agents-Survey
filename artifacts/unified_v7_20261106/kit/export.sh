#!/bin/zsh
# Export a PPTX to PDF through Keynote (one export at a time, guarded by a lock), then render a PNG preview.
# usage: export.sh /abs/path/Figure.pptx [dpi]   ->  Figure.pdf and Figure.png next to it
set -u
IN=${1:A}; DPI=${2:-110}
OUT=${IN:r}.pdf; PNG=${IN:r}.png
LOCK=${0:A:h}/.keynote.lock
for i in {1..600}; do
  if mkdir $LOCK 2>/dev/null; then break; fi
  # break a stale lock (older than 4 minutes)
  if [[ -n $(find $LOCK -maxdepth 0 -mmin +4 2>/dev/null) ]]; then rmdir $LOCK 2>/dev/null; fi
  sleep 1
done
trap 'rmdir $LOCK 2>/dev/null' EXIT
rm -f $OUT
osascript -e "with timeout of 150 seconds
tell application \"Keynote\"
  open (POSIX file \"$IN\")
  delay 3
  export front document to (POSIX file \"$OUT\") as PDF
  close front document saving no
end tell
end timeout" >/dev/null 2>&1
if [[ ! -s $OUT ]]; then echo "EXPORT FAILED: $IN (Keynote may need the screen unlocked)"; exit 1; fi
pdftoppm -r $DPI -png -singlefile $OUT ${PNG:r}
echo "ok $OUT $PNG"
