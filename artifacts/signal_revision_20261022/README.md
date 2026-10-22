# Figures 5–15: signal and label styling

Each PPTX contains one slide and retains the existing component groups. Native time-series traces are black with restrained shadows; point markers use a grayscale contour. Time axes are heavier and use a gray gradient. Short headings and labels use Comic Sans MS; explanatory prose keeps its source font. Overlaid reference series use dashes.

The four small Figure 10 waveform glyphs are digitized from the prior source illustrations into editable paths. Other illustration crops remain separate image objects within editable groups. Figure 6 contains no time-series plot, so its changes concern typography only.

`sources.json` records the prior PPT for each figure; `changes.json` records native shape and text changes. `revise.py` applies these changes to copies. PDFs are exported from the finalized PPTX using LibreOffice with the installed Microsoft fonts. Captions remain in main.tex.
