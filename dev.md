# [compatch] CAA + CA — developer notes

The only game override is `gui/window_council.gui`. Install Council Assignment Automation 0.1.0 and Council Autopilot 1.0.12 separately; load this patch after both. CAA appoints people; Council Autopilot manages tasks. Their scripts and preferences remain independent.

## Reproducible merge

The portable generator pins the exact CK3 1.20.0.4, CAA 0.1.0 and Council Autopilot 1.0.12 inputs in `tools/upstream-lock.json`. Supply installed paths locally:

```sh
python tools/merge_council_window.py --caa /path/to/caa --autopilot /path/to/council_autopilot --game /path/to/ck3/game --output /path/to/new-output
python -m unittest discover -s tests -p test_merge_council_window.py -v
```

The output directory must not exist. The helper copies the upstream MIT notice and inserts CAA's exact marked button into the unique Council Autopilot council-tab anchor. It proves that removing CAA's insertion restores vanilla after BOM/line-ending normalization, and removing the insertion from the merged file restores Autopilot's bytes. All 82 Autopilot scripted-GUI references are preserved. Upstream drift requires a reviewed new lock, merge and native test. The public generator does not launch CK3 or publish anything.

## Evidence and limits

The release's 27-assertion gameplay integration was executed with both exact dependencies and this GUI. The publication presentation revision changes only the descriptor and thumbnail. Gameplay acceptance is inherited through unchanged GUI, license and dependency hashes; it is not a new gameplay run. Candidate-bound native resolution and genuine translation review cover all 16 non-vanilla control strings in all nine languages configured by CK3 1.20.0.4. This does not certify every unrelated dependency message.

The native scenario exercised CAA appointments, the Council Autopilot marshal control, task restoration after a changed marshal, real scheduling with panels open and closed, and Off stability. Hidden native callbacks do not establish layout, hover or pointer behavior. Multiplayer, performance, all other Autopilot task modes and save/reload of the full stack remain unverified. Council Autopilot's chaplain-change reset and periodic secrets search follow its unchanged scripts.

## Publication and provenance

`publishing/description.en.md` is the exported canonical description; README is a platform projection with a developer link. This portable guide is intentionally generated for the public repository from the workspace developer record. Machine-specific harnesses and raw logs are retained privately. Their source-bound acceptance accompanies the release workflow.

The merged Council Autopilot additions retain `mod/council_assignment_autopilot_compatch/LICENSE-Council-Autopilot.txt`; the CK3 base interface belongs to Paradox Interactive. Integration code and documentation were developed with AI assistance. The cover combines the two required mods' thumbnails with AI assistance; publication media is promotional art, not gameplay evidence. Media provenance and exact prompts are in `publishing/media/`. No new broader reuse license is granted here.

## Release 0.1.1 — CK3 1.20.1

Updated for CK3 1.20.1 and Council Assignment Automation 0.1.1. Preserve the combined council interface and guard the fabricate-claim controls against invalid councillor, task and target states. Update the CAA dependency name.

The committed runtime is the current release source. Earlier generator/test notes above retain their historical scope. Gameplay evidence is inherited from the reviewed development candidate; localization uses static coverage and format checks under publication contract 1.8.0. No additional production engine run or blanket multiplayer/visual guarantee is claimed.

## Compatibility metadata — CK3 1.20.1.1 (2026-10-15)

Version 0.1.1 now targets CK3 1.20.1.1 (Steam build 25913294). This is a publication metadata update; runtime files, mod version, release history and existing download archives are unchanged.

The upstream comparison used the complete Steam manifests for 1.20.1 and 1.20.1.1 and verified the installed main game, Windows and launcher files against the current manifests. All main-game GUI files and gameplay scripts used by this mod retain their upstream hashes; changes are concentrated in translations, name equivalency and French customizable localization. The executable changed. Mod-specific source and localization checks are recorded in the maintained compatibility assessment and release journal.

Earlier native reports retain their original source, game build and scenario coverage. This metadata revision does not claim a fresh native PASS on 1.20.1.1. Visual layout, multiplayer and performance retain their previously recorded limits. Edit the canonical publication source and regenerate its current outputs; preserve historical release records.
