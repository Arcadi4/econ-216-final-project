# ECON 216 EDA — Motorcycle Safety Analysis

## TL;DR

> **Quick Summary**: Write a complete EDA R Markdown document analyzing FARS 2011–2020 data to explore motorcycle vs. car fatality patterns and the effect of helmet laws by state.
>
> **Deliverables**:
> - `EDA.Rmd` — fully annotated, knits to PDF without errors
> - Sections A through E per course requirements
> - Exactly 5 poster figures with coherent story arc
>
> **Estimated Effort**: Large
> **Parallel Execution**: YES — 3 waves
> **Critical Path**: Task 1 (setup/load/clean) → Task 2 (Section A) → Task 3 (Section B) → Task 4 (Section C) → Task 5 (Section D+E) → Task 6 (final knit)

---

## Context

### Original Request
Write the EDA for ECON 216 final project on motorcycle safety using FARS data (2011–2020), following the course EDA Guide and Checklist.

### Interview Summary
- **Topic**: Motorcycle safety vs. cars — fatality rates, helmet law effects
- **Research questions**: (1) Fatality rates per crash: motorcycles vs. cars; (2) Helmet law strictness vs. fatality rates by state
- **Data**: FARS 2011–2020, complete, in `data/` folder. Core tables: `accident.csv`, `vehicle.csv`, `person.csv` per year
- **Language**: English annotations, `echo = TRUE`
- **Unit of analysis**: Crash-level (accident) joined with vehicle and person records via `ST_CASE`
- **"Per mile" note**: FARS does not include VMT exposure data — fatality comparisons will be per-crash or per-vehicle-type, not per mile. Narrative scoped accordingly.
- **Healthcare cost**: Motivating context only (from sources), not computed from data

### Metis Review — Gaps Addressed
- Locked unit of analysis to crash-level; person-level for injury/helmet analysis
- "Per mile" scoped out — FARS has no VMT; use per-crash rates and proportions
- Healthcare cost = narrative context only, not a computed variable
- Guardrail: descriptive EDA only, no causal inference or regression
- Guardrail: no additional datasets beyond FARS
- Edge cases to handle: missing helmet values, multiple persons per crash, schema drift across years

---

## Work Objectives

### Core Objective
Produce a complete, knittable EDA.Rmd that satisfies all ECON 216 EDA Guide and Checklist requirements, exploring motorcycle vs. car fatality patterns in FARS 2011–2020.

### Concrete Deliverables
- `EDA.Rmd` with setup chunk + Sections A, B, C, D, E
- PDF output knitted successfully
- ≥10 relationship figures in Section B
- Exactly 5 labeled poster figures in Section C
- Variable rationale table in Section D
- Self-assessment in Section E

### Definition of Done
- [ ] `EDA.Rmd` knits to PDF with zero errors (`rmarkdown::render("EDA.Rmd")`)
- [ ] All 5 sections present and labeled
- [ ] Section A: histogram/bar chart for every key variable
- [ ] Section B: ≥10 relationship plots + Exploration Log
- [ ] Section B: ≥2 annotations cite expert sources
- [ ] Section C: exactly 5 poster figures, labeled "Poster Figure 1–5"
- [ ] Section D: variable table + ≥5 expert sources
- [ ] Section E: all 4 self-assessment questions answered
- [ ] All figures have titles, labeled axes with units, legends where needed
- [ ] `echo = TRUE` throughout

### Must Have
- Data loading, joining, and cleaning code before Section A
- `bind_rows()` across 2011–2020 for each of accident, vehicle, person
- Join accident + vehicle + person on `ST_CASE` (and `YEAR` to avoid cross-year collisions)
- Filter to motorcycles (`BODY_TYPNAME` contains "Motorcycle") vs. passenger cars
- Helmet variable from `REST_USENAME`
- All annotations in English
- Relative file paths (R Project root)

### Must NOT Have (Guardrails)
- No regression, hypothesis tests, or causal language
- No "per mile" fatality rates (no VMT data in FARS)
- No healthcare cost calculations
- No additional external datasets
- No pie charts
- No figures without titles and axis labels
- No hardcoded absolute file paths
- No `echo = FALSE` on code chunks (except setup)
- Do not exceed exactly 5 poster figures in Section C
- No AI slop: no excessive comments, no over-abstraction, no generic variable names like `data` or `temp`

---

## Verification Strategy

### Test Decision
- **Infrastructure exists**: NO (R Markdown academic document)
- **Automated tests**: None
- **Framework**: N/A
- **QA method**: Knit to PDF and visually verify each section

### QA Policy
Each task verified by knitting the document and checking output. Evidence = successful PDF render + section content review.

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Foundation — must run first):
└── Task 1: Setup chunk + data load + join + clean pipeline

Wave 2 (Sections — can run in parallel after Task 1):
├── Task 2: Section A — Univariate visualizations
├── Task 3: Section B — Relationship visualizations + Exploration Log

Wave 3 (Synthesis — after Task 3):
├── Task 4: Section C — 5 Poster figures
├── Task 5: Section D (variable table + sources) + Section E (self-assessment)

Wave FINAL:
└── Task 6: Final knit verification + polish
```

### Agent Dispatch Summary
- Wave 1: Task 1 → `unspecified-high`
- Wave 2: Task 2 → `unspecified-high`, Task 3 → `unspecified-high`
- Wave 3: Task 4 → `visual-engineering`, Task 5 → `writing`
- Final: Task 6 → `quick`

---

## TODOs

- [x] 1. Setup chunk + data load + join + clean pipeline

  **What to do**:
  - Add YAML header: `title: "ECON 216 EDA — Motorcycle Safety"`, `output: pdf_document`, `author: "Arya, Gayathri, Skylar"`
  - Add setup chunk: `knitr::opts_chunk$set(echo = TRUE, warning = FALSE, message = FALSE)`, load libraries: `tidyverse`, `readr`, `lubridate`
  - Write a loop to `read_csv()` and `bind_rows()` all 10 years (2011–2020) for each of `accident.csv`, `vehicle.csv`, `person.csv` from `data/FARS{YEAR}NationalCSV/` paths. Store as `acc_raw`, `veh_raw`, `per_raw`.
  - Add a `YEAR` column derived from the folder name if not already present in the data.
  - Join: `acc_raw %>% left_join(veh_raw, by = c("ST_CASE", "YEAR"))` → `acc_veh`; then `acc_veh %>% left_join(per_raw, by = c("ST_CASE", "YEAR"))` → `fars_full`
  - After join: check row counts before/after, check for NAs introduced, spot-check 3 rows
  - Clean: filter `BODY_TYPNAME` to keep only motorcycles and passenger cars (use `str_detect` on relevant keywords); create `vehicle_type` factor ("Motorcycle" / "Car"); convert `STATENAME`, `WEATHERNAME`, `LGT_CONDNAME`, `RUR_URBNAME`, `SEXNAME`, `PER_TYPNAME`, `INJ_SEVNAME`, `REST_USENAME`, `EJECTIONNAME`, `DRINKINGNAME`, `FUNC_SYSNAME`, `MAN_COLLNAME`, `DAY_WEEKNAME` to factors; ensure `AGE`, `FATALS`, `DRUNK_DR`, `TRAV_SP` are numeric; handle missing/unknown codes (e.g., 99, 999 → NA for AGE and TRAV_SP)
  - Create derived variable: `helmet_used` (binary: TRUE if `REST_USENAME` contains "Helmet", FALSE otherwise, NA if missing)
  - Add short plain-text annotation after each major step explaining what was done

  **Must NOT do**:
  - No hardcoded absolute paths
  - No `echo = FALSE` on this chunk
  - Do not drop rows silently — document any filtering with a comment
  - Do not join across years without `YEAR` in the key (prevents ST_CASE collisions)

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Data engineering task requiring careful multi-year join logic and cleaning decisions
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 1 — must complete before all other tasks
  - **Blocks**: Tasks 2, 3, 4, 5
  - **Blocked By**: None (can start immediately)

  **References**:
  - `Group Proposal.Rmd:54-69` — existing `read_csv` calls for 2018 and 1990 data; follow same pattern but loop across years
  - `Group Proposal.Rmd:75-100` — variable table listing all key variables and their source datasets
  - `data/FARS2020NationalCSV/FARS2020NationalCSV/accident.csv` — inspect column names to confirm `ST_CASE`, `STATENAME`, `FATALS`, `YEAR` presence
  - `data/FARS2020NationalCSV/FARS2020NationalCSV/vehicle.csv` — confirm `BODY_TYPNAME`, `TRAV_SP`, `DEFORMEDNAME`
  - `data/FARS2020NationalCSV/FARS2020NationalCSV/person.csv` — confirm `REST_USENAME`, `AGE`, `INJ_SEVNAME`

  **Acceptance Criteria**:
  - [ ] `acc_raw`, `veh_raw`, `per_raw` each have ~10× the rows of a single year
  - [ ] `fars_full` row count is reasonable (no explosion from many-to-many join)
  - [ ] `vehicle_type` factor has exactly 2 levels: "Motorcycle" and "Car"
  - [ ] `helmet_used` binary variable exists
  - [ ] Numeric codes 99/999 converted to NA for AGE and TRAV_SP
  - [ ] Document knits through this section without error

  **Commit**: YES
  - Message: `feat(eda): add data loading, joining, and cleaning pipeline`
  - Files: `EDA.Rmd`
  - Pre-commit: knit setup chunk only (or verify no parse errors)

- [x] 2. Section A — Univariate visualizations

  **What to do**:
  - Add `## Section A — Univariate Visualizations` header
  - For each numeric variable (`FATALS`, `AGE`, `TRAV_SP`, `DRUNK_DR`): create a histogram with `geom_histogram()`, descriptive title, labeled x-axis with units, appropriate binwidth; after each plot write 1–2 sentence annotation covering shape, center, spread, notable features
  - For each categorical variable (`vehicle_type`, `STATENAME` [top 15 states], `WEATHERNAME`, `LGT_CONDNAME`, `RUR_URBNAME`, `SEXNAME`, `INJ_SEVNAME`, `REST_USENAME`, `EJECTIONNAME`, `DRINKINGNAME`, `FUNC_SYSNAME`, `MAN_COLLNAME`, `DAY_WEEKNAME`, `DEFORMEDNAME`): create a bar chart using `group_by() %>% summarize(n=n()) %>% mutate(pct=n/sum(n))` then `geom_col()`; collapse categories with <2% share into "Other"; after each plot write 1–2 sentence annotation
  - Consider log scale for `TRAV_SP` if heavily skewed
  - All figures: descriptive title, labeled axes, no legend needed for single-variable plots

  **Must NOT do**:
  - No pie charts
  - Do not show all 50 states — top 15 by crash count + "Other"
  - No figures without titles and axis labels

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Requires systematic ggplot2 coding across ~15 variables with annotations
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 3, after Task 1)
  - **Parallel Group**: Wave 2
  - **Blocks**: Task 4
  - **Blocked By**: Task 1

  **References**:
  - `Group Proposal.Rmd:75-100` — full variable list with types
  - EDA Guide: "Step 6: Visualize Single Variables" — histogram for numeric, bar chart from grouped proportions for categorical
  - EDA Checklist: "Univariate Visualizations (Section A)" items

  **Acceptance Criteria**:
  - [ ] Histogram present for each of: FATALS, AGE, TRAV_SP, DRUNK_DR
  - [ ] Bar chart present for each categorical variable listed above
  - [ ] Every plot has title + labeled axes
  - [ ] Every plot followed by 1–2 sentence annotation
  - [ ] No plot has >15 visible categories without collapsing

  **Commit**: YES (grouped with Task 3)
  - Message: `feat(eda): add sections A and B`

- [x] 3. Section B — Relationship visualizations + Exploration Log

  **What to do**:
  - Add `## Section B — Relationship Visualizations` header
  - Produce at least 10 figures progressing from simple to complex. Suggested sequence:
    1. Bar chart: fatality count by `vehicle_type` (motorcycle vs car) — simple comparison
    2. Bar chart: proportion of crashes resulting in fatality by `vehicle_type` — normalized
    3. Faceted histogram: `FATALS` distribution faceted by `vehicle_type`
    4. Bar chart: `INJ_SEVNAME` proportions by `vehicle_type` — injury severity comparison
    5. Bar chart: `EJECTIONNAME` rate by `vehicle_type` — ejection risk
    6. Line chart: fatality count by `YEAR` and `vehicle_type` — temporal trend (`geom_line()`)
    7. Bar chart: `helmet_used` rate by state (top 15 states) — geographic helmet use
    8. Bar chart: fatality rate by `helmet_used` among motorcycle crashes — helmet effect
    9. Faceted bar: `INJ_SEVNAME` by `helmet_used`, faceted — helmet vs injury severity
    10. Bar chart: motorcycle fatalities by `WEATHERNAME` — environmental risk
    11. Bar chart: motorcycle fatalities by `LGT_CONDNAME` — lighting risk
    12. Faceted bar: `RUR_URBNAME` × `vehicle_type` fatality proportions — urban/rural
    13. Scatter or bar: mean `TRAV_SP` by `vehicle_type` and `INJ_SEVNAME`
  - After each figure: 2–3 sentence annotation (what it shows, what you learn, what question it leads to next)
  - At least 2–3 annotations must cite expert sources from Group Proposal (use inline citation like "According to NHTSA (2024)...")
  - End Section B with `### Exploration Log` — ~half page narrative: what was examined first, surprises, dead ends, how one question led to the next

  **Must NOT do**:
  - No causal language ("causes", "leads to") — use "associated with", "correlated with"
  - No regression or statistical tests
  - No overcrowded plots — use faceting instead of overlapping colors when >3 groups
  - No figures without annotations

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Core analytical section requiring thoughtful ggplot2 sequencing and interpretive writing
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 2, after Task 1)
  - **Parallel Group**: Wave 2
  - **Blocks**: Task 4
  - **Blocked By**: Task 1

  **References**:
  - EDA Guide: "Step 7: Visualize Relationships Among Variables" — plot type guidance
  - EDA Guide: "Story Arc framework" — keep poster narrative in mind
  - `Group Proposal.Rmd:108-165` — 5 expert sources for citation in annotations
  - EDA Checklist: "Relationship Visualizations (Section B)" items

  **Acceptance Criteria**:
  - [ ] ≥10 relationship figures present
  - [ ] Each figure followed by 2–3 sentence annotation
  - [ ] ≥2 annotations cite expert sources by name/year
  - [ ] Exploration Log present at end of Section B (~half page)
  - [ ] Figures progress from simple 2-variable to faceted/complex

  **Commit**: YES (grouped with Task 2)
  - Message: `feat(eda): add sections A and B with univariate and relationship visualizations`
  - Files: `EDA.Rmd`

- [x] 4. Section C — Five poster figures

  **What to do**:
  - Add `## Section C — Five Poster Figures` header
  - Select exactly 5 figures from Section B (or refined versions) following the story arc:
    - **Poster Figure 1 — The Setup**: Temporal trend of motorcycle vs. car fatalities 2011–2020 (`geom_line()` by year and vehicle_type). Establishes that motorcycle fatalities are disproportionately high relative to their share of crashes.
    - **Poster Figure 2 — The Zoom-In**: Injury severity proportions by vehicle type (stacked/grouped bar). Shows motorcyclists suffer fatal/severe injuries at far higher rates than car occupants.
    - **Poster Figure 3 — The Nuance**: Helmet use rate by state (top 15), colored by fatality rate. Adds geographic dimension and hints at helmet law variation.
    - **Poster Figure 4 — The Surprise**: Fatality rate by helmet use among motorcycle crashes. Shows the stark difference — the most striking single finding.
    - **Poster Figure 5 — The Big Picture**: Faceted bar of injury severity by helmet use AND rural/urban setting. Synthesizes multiple risk factors together.
  - Label each exactly: `### Poster Figure 1`, `### Poster Figure 2`, etc.
  - Under each figure write a 3–5 sentence paragraph explaining: why it belongs on the poster, what role it plays in the narrative, what a viewer should take away
  - Figures should be polished: larger text (`theme_minimal(base_size=14)`), clear titles, clean legends, publication-ready appearance
  - These may reuse/refine figures from Section B — that is explicitly allowed

  **Must NOT do**:
  - Do not include more or fewer than exactly 5 figures
  - Do not use disconnected figures — they must tell a coherent story
  - No pie charts
  - No figures without 3–5 sentence paragraph below them

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
    - Reason: Poster figures need polished, presentation-quality ggplot2 styling
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 5, after Tasks 2+3)
  - **Parallel Group**: Wave 3
  - **Blocks**: Task 6
  - **Blocked By**: Tasks 2, 3

  **References**:
  - EDA Guide: "Story Arc framework" — Setup → Zoom-In → Nuance → Surprise → Big Picture
  - EDA Guide: "Section C — Five Poster Figures" requirements
  - EDA Checklist: "Choosing Your 5 Poster Figures (Section C)" items
  - Section B figures (already written in EDA.Rmd) — select and refine

  **Acceptance Criteria**:
  - [ ] Exactly 5 figures labeled "Poster Figure 1" through "Poster Figure 5"
  - [ ] Each figure followed by 3–5 sentence paragraph
  - [ ] Figures follow Setup → Zoom-In → Nuance → Surprise → Big Picture arc
  - [ ] All figures use `theme_minimal()` or equivalent clean theme with `base_size ≥ 13`
  - [ ] All figures have descriptive titles, labeled axes, clear legends

  **Commit**: YES (grouped with Task 5)
  - Message: `feat(eda): add sections C, D, E — poster figures, variable rationale, self-assessment`

- [x] 5. Section D (variable rationale table + sources) + Section E (self-assessment)

  **What to do**:

  **Section D**:
  - Add `## Section D — Variable Rationale` header
  - Create a markdown table with columns: Variable Name | Source Dataset | Type | Rationale for Inclusion
  - Include every variable used in the analysis (at minimum all variables from Group Proposal variable table: ST_CASE, YEAR, STATENAME, FATALS, DRUNK_DR, RUR_URBNAME, FUNC_SYSNAME, WEATHERNAME, LGT_CONDNAME, MAN_COLLNAME, DAY_WEEKNAME, HOURNAME, BODY_TYPNAME, ROLLOVERNAME, TRAV_SP, DEFORMEDNAME, L_STATUSNAME, AGE, SEXNAME, PER_TYPNAME, INJ_SEVNAME, REST_USENAME, EJECTIONNAME, DRINKINGNAME, plus derived `vehicle_type` and `helmet_used`)
  - Below the table, list all 5 expert sources from Group Proposal with full citations and 3–5 sentence annotations explaining how each informs the analysis

  **Section E**:
  - Add `## Section E — Self-Assessment` header
  - Answer all 4 questions in a few sentences each:
    1. Which poster figures are you most confident in, and why?
    2. Which are you least confident in?
    3. Describe one dead end and what you learned from it.
    4. What specific feedback would be most helpful from reviewers?
  - Answers should be honest and specific to the actual analysis done

  **Must NOT do**:
  - Do not omit any variable that appears in the code
  - Do not use placeholder text — answers must be substantive
  - Do not copy-paste source annotations verbatim from Proposal without adapting to EDA context

  **Recommended Agent Profile**:
  - **Category**: `writing`
    - Reason: Primarily documentation and academic writing tasks
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 4, after Tasks 2+3)
  - **Parallel Group**: Wave 3
  - **Blocks**: Task 6
  - **Blocked By**: Tasks 2, 3

  **References**:
  - `Group Proposal.Rmd:75-100` — variable table to expand upon
  - `Group Proposal.Rmd:108-165` — 5 expert sources with existing annotations
  - EDA Guide: "Section D — Variable Rationale" and "Section E — Self-Assessment" requirements
  - EDA Checklist: "Final Checks Before Submitting" items

  **Acceptance Criteria**:
  - [ ] Variable table present with all used variables (≥20 rows)
  - [ ] Table has all 4 columns: name, source, type, rationale
  - [ ] ≥5 expert sources listed with annotations
  - [ ] Section E answers all 4 self-assessment questions
  - [ ] Answers are substantive (not placeholder text)

  **Commit**: YES (grouped with Task 4)
  - Message: `feat(eda): add sections C, D, E — poster figures, variable rationale, self-assessment`
  - Files: `EDA.Rmd`

- [x] 6. Final knit verification + polish

  **What to do**:
  - Run `rmarkdown::render("EDA.Rmd", output_format = "pdf_document")` and confirm it produces a PDF without errors
  - Fix any knit errors (missing packages, broken chunk references, path issues)
  - Review PDF output: check all figures render, all sections present, all annotations visible
  - Polish: ensure consistent heading levels, no orphaned code chunks, no duplicate figure labels
  - Verify `echo = TRUE` is set globally and not overridden on content chunks
  - Confirm all figures have titles, axis labels, and legends where color/shape is used
  - Check that Section C figures are labeled exactly "Poster Figure 1" through "Poster Figure 5"
  - Verify Exploration Log is present at end of Section B
  - Final commit

  **Must NOT do**:
  - Do not set `echo = FALSE` on any content chunk
  - Do not suppress warnings by hiding real data issues — fix them
  - Do not submit if PDF has any rendering errors

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Verification and polish task, no new content
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave FINAL — sequential after all other tasks
  - **Blocks**: Nothing (final task)
  - **Blocked By**: Tasks 4, 5

  **References**:
  - EDA Checklist: "Final Checks Before Submitting the Draft EDA" items
  - EDA Guide: "Draft EDA submission requirements"

  **Acceptance Criteria**:
  - [ ] `rmarkdown::render("EDA.Rmd", output_format="pdf_document")` exits with no errors
  - [ ] PDF file produced and opens correctly
  - [ ] All 5 sections (A–E) visible in PDF
  - [ ] All figures render in PDF (no blank figure areas)
  - [ ] Section C has exactly 5 figures labeled "Poster Figure 1–5"

  **Commit**: YES
  - Message: `feat(eda): final polish and verified PDF knit`
  - Files: `EDA.Rmd`

---

## Final Verification Wave

- [x] F1. **Knit Check** — `quick`
  Run `rmarkdown::render("EDA.Rmd", output_format="pdf_document")`. Confirm zero errors, PDF opens, all figures render.
  Output: `KNIT [PASS/FAIL] | Sections [A/B/C/D/E present] | Figures [count] | VERDICT`

- [x] F2. **Checklist Compliance** — `unspecified-high`
  Go through every item in the EDA Checklist. Verify: Section A has histogram/bar for every variable; Section B has ≥10 plots + Exploration Log + ≥2 source citations; Section C has exactly 5 labeled poster figures; Section D has variable table + ≥5 sources; Section E answers all 4 questions. Check all figures have titles, axis labels, legends.
  Output: `Checklist [N/N items] | VERDICT: APPROVE/REJECT`

---

## Commit Strategy

- After Task 1: `feat(eda): add data loading, joining, and cleaning pipeline`
- After Tasks 2+3: `feat(eda): add sections A and B with univariate and relationship visualizations`
- After Tasks 4+5: `feat(eda): add sections C, D, E — poster figures, variable rationale, self-assessment`
- After Task 6: `feat(eda): final polish and verified PDF knit`

---

## Success Criteria

### Verification Commands
```r
rmarkdown::render("EDA.Rmd", output_format = "pdf_document")
# Expected: renders without errors, produces EDA.pdf
```

### Final Checklist
- [ ] Knits to PDF without errors
- [ ] All 5 sections present
- [ ] ≥10 relationship figures in Section B
- [ ] Exactly 5 poster figures in Section C
- [ ] Variable table in Section D
- [ ] ≥5 expert sources in Section D
- [ ] All 4 self-assessment questions in Section E
- [ ] No forbidden patterns (pie charts, absolute paths, echo=FALSE on content chunks)
