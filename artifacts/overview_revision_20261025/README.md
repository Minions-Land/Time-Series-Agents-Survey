# Main overview replacement

The manuscript now uses a right-cropped version of the user-supplied `02_main(2).pdf` as Figure 3; the original source is retained in `assets/02_main_source.pdf`. The radial landscape is placed at the top of its page; the cumulative contribution line chart remains Figure 2 and is placed at the top of the following page.

- Manuscript figure source: `pdf/02_main.pdf`
- Editable PowerPoint source: `pptx/02_main_source.pptx`
- Paper-facing copy: `../../paper_figures/Overvieww.pdf`
- Previous icon-key experiment: `pdf/Time-Series-Agents_Overview_Reorganized.pdf` and `pptx/Time-Series-Agents_Overview_Reorganized.pptx`

## Background-reference tags removed (31 October 2026)

GridMind, Grid-Agent, and Tree-of-Evidence are background references in the ledger and contribute no modules, so their tags were removed from the paper figure; ZARA moved up into the GridMind slot. `remove_background_tags.py` applies this to the exported PDF without re-rendering (two-pass redaction: text first, then only the target logos), and `pptx/02_main_source.pptx` carries the same change. The two TimeClaw tags keep their short label: renaming them to TimeClaw-Harness and TimeClaw-EEL needs 58 pt and 35 pt more width than their rows allow.
