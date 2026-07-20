# Day 29 - Deck Build

Planned date: 07-29-2026. Executed early on 07-20-2026 at user request.

## Goal

Build the actual presentation deck from the Day 28 slide outline.

## What I Did

- Added `deck/open_source_tax_tooling_draft_deck.pptx` as the Day 29 draft deck.
- Built an 18-slide PowerPoint deck for a 20-30 minute mentor or portfolio walkthrough.
- Kept the deck aligned to `deck/outline.md` and `report/full_report_draft.md`.
- Included slides for the research question, safety boundary, evidence method, ecosystem map, shortlist, synthetic scenario, tool comparison, prototype thesis, demo path, demo readout, recommendation, limitations, future work, and closing takeaway.
- Added speaker notes with source pointers and demo guidance.
- Used the current local run of `python run_day20_demo.py --json` for the demo result slide.
- Updated repository status files and the execution-lab manifest source to point next to Day 30 final QA and rehearsal.

## Evidence Captured

- `deck/open_source_tax_tooling_draft_deck.pptx`
- `deck/outline.md`
- `report/full_report_draft.md`
- `prototype/run_day20_demo.py`
- `prototype/tests/run_failure_matrix.py`
- Current local output from `python run_day20_demo.py --json`

## Verification

- Ran `python run_day20_demo.py --json`; the local live demo passed and reported hledger `1.52.1`, 19 transactions, 38 postings, 14 accounts, checking balance `8964.77`, and 15/15 failure-matrix cases passed.
- Rendered the draft deck to slide PNGs through the presentation QA workflow.
- Inspected a contact sheet from the exported PowerPoint-rendered slides.
- Ran `slides_test.py`; no overflow was detected.
- Rebuilt the execution-lab manifest and app after status updates.
- Ran `git diff --check`.
- Ran a non-ASCII scan over the new and updated Markdown files.

## Decisions Made

- Keep the deck as an editable PowerPoint draft under `deck/`.
- Use a restrained white, black, gray, and orange visual system so evidence and recommendation slides stay readable.
- Keep dense evidence paths in speaker notes rather than on visible slides.
- Use terminal/demo command evidence instead of adding execution-lab screenshots in this draft; screenshots remain optional for Day 30 polish.

## Problems / Open Questions

- Day 30 still needs final QA, rehearsal timing, and consistency checks across report, README, prototype, and deck.
- Final publication still needs a public metadata refresh if current/latest wording remains.
- Execution-lab screenshots can still be added if they materially improve the final deck.

## Tomorrow's Starting Point

Execute Day 30 by rerunning the prototype demo from clean instructions, reading the report as a skeptical reviewer, walking through the deck for timing, fixing mismatches, and confirming no real data, secrets, or private files are included.

