"""Export PPTX files to PDF through Keynote (AppleScript).

PowerPoint's sandbox asks for folder access on every new path, which needs a human click;
Keynote opens and exports here without a prompt. Keynote's rendering of PPTX may differ slightly.
"""
import subprocess, sys, os

SCRIPT = '''
on run argv
  set inPath to item 1 of argv
  set outPath to item 2 of argv
  with timeout of 90 seconds
    tell application "Keynote"
      launch
      delay 2
      open (POSIX file inPath)
      repeat 40 times
        if (count of documents) > 0 then exit repeat
        delay 0.5
      end repeat
      set d to front document
      export d to (POSIX file outPath) as PDF
      close d saving no
    end tell
  end timeout
end run
'''

def export(pptx, pdf):
    subprocess.run(['osascript', '-e', SCRIPT, os.path.abspath(pptx), os.path.abspath(pdf)], check=True, timeout=120)

if __name__ == '__main__':
    for f in sys.argv[1:]:
        export(f, os.path.splitext(f)[0] + '.pdf'); print('exported', f)
