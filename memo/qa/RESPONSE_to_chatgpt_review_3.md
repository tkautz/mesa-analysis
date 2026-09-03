# Response to the third review (Sept. 3, 2026, "Comparative Review") and plan

Purpose: decide what to adopt from the third review. Its one new fact is that BVSD
publishes an Enrollment Pattern Matrix (December 2025; the "Open Enrollment
Matrices" link on the declining-enrollment page) that gives residents by
attendance area and where they attend. That document is not in the repository and
could not be fetched from here. Everything the review derives from it is
therefore unverified on our side, but it lands exactly where the previous round's
sensitivity table already pointed, so the current documents do not need to be
withdrawn while we wait for it.

## The matrix: what the review says and what we can check

The review reads the matrix as: about 415 of about 502 residents of the areas that
form the future combined attendance area attend Mesa or Bear Creek (combined-area
capture about 83%), leaving about 121 of the 536 enrolled as external in-district
choice, out-of-district, placements and other; 522 × 0.83 + 121 ≈ 553.

In the notation of the current appendix that is x ≈ 42 (415 − 373 own-school
residents) and external seats ≈ 121 (163 − 42). The x = 40 row of the existing
sensitivity table (Table: "Sensitivity to x") reads capture 82%, external 123,
553 at today's pattern, capture needed for the range 54–65%, cut needed 90 of 123
(73%). So:

- the "about 550" benchmark stands (the review gets 553);
- the two invariant claims in the email stand (capture below today's; a cut of
  more than half of choice enrollment);
- the review's "83% and 121" would replace our "74% and 163" as the headline
  decomposition once the matrix is in hand, and the x = 0 row would stop being the
  headline in the appendix.

Nothing in the email needs to change today. The appendix's fork paragraph will be
rewritten around the matrix categories once the file is in `data/raw/bvsd/`.

**Two cautions about the review's reading, to check against the document:**
1. Its 502 residents differ from the deck's 503 and it mentions "optional" and
   dual areas (Bear Creek/Creekside, Bear Creek/Mesa). The matrix's geography may
   not match the deck's p. 51 area. The reconciliation table will show both.
2. "Placements/other" is a category the review says the matrix carries. Our
   derived 140 includes it. The rebuilt identity will have five terms (residents ×
   capture + external in-district + out-of-district + placements/other), as the
   review proposes.

## Scorecard

| # | Review point | Decision | Reason |
|---|---|---|---|
| 1 | Rebuild the accounting from the matrix; delete "163 → 16–75" | Accept; **blocked on the matrix** | Already demoted to the x = 0 row last round; the email carries only x-invariant claims. Rebuild when the file arrives |
| 2 | Make "show the bridge" the single thesis; demote 521, 57%, 16%, one-in-four to supporting evidence | Accept in the appendix Summary ordering; **author's call for the email** | See "Email length" below |
| 3 | Label 16% / 57% as scenario-conditional (at 90% following, under a stated kindergarten spec) | Accept | The email's range paragraph currently omits "at 90% following"; add it |
| 4 | "Only if" → "of the specifications examined" | Already done | Last round |
| 5 | Interdependence: say "the documents do not say which historical flows are assumed to persist," not "the district has not modeled" | Accept | Cannot establish the negative from the public record |
| 6 | Birth-informed kindergarten entry | Deferred; add an explicit request for the district's birth inputs | No small-area birth series; the staff-request list already asks for the intake assumption, now to name births |
| 7 | 521 vs 462: keep as a reconciliation diagnostic, never as "59 missing students" | Accept; wording check | Fig. 2 caption and framed Summary already say "the gap is an assumption"; add "the two products are not additive after a boundary change" |
| 8 | Trim package-wide criticism from the front | Already done | Softened last round; item list unchanged |
| 9 | Closure literature as a diligence standard only | Already the case | Pearman is a footnote; no Chicago material is used |
| 10 | Nested common + school-specific shock check | Already done | Bracketed in Appendix B; small effect |
| 11 | One-page worksheet as a 16-row checklist | Accept | Becomes a table in the appendix and replaces the prose list in Appendix D "What the Board can ask staff to supply" |
| 12 | Eleven questions for staff | Accept, merged | Six are already in the appendix; the new ones (geography of the 522; crossflow treatment; grandfathering and sibling priority; contingency trigger) go into the worksheet rows |
| 13 | The 174-word Board email | **Author's call**; draft supplied as a separate file | It is the reviewer's best suggestion and a real alternative, not an edit |

## Email length: the decision the author has to make

The reviewer's short email (about 175 words) leads with the bridge, cites the FAQ's
managed-choice sentence, asks for the worksheet, and offers the fair-test decision
rule. It drops the projection-revision history, the model, the probabilities, the
outlier comparison, cost and the open-questions list to the attachment.

Arguments for the short form: Board members read it; it forces staff to answer
the strongest question first; there is less surface for a rebuttal on a secondary
number; the appendix still carries everything.

Arguments for the current 750-word form: it was the author's specification; it
shows the Board in one page that the question is not speculative (the revisions,
the 59-vs-37 range width, the one-in-four); a Board member who never opens the
attachment still sees the evidence.

Recommendation: send the short form as the email body and attach the appendix,
but keep three sentences from the long form that cost nothing to defend: the
59-vs-37 range width (district's own numbers), the district's "can house" sentence
against the FAQ's "transition year" sentence, and the concession paragraph. That is
about 260 words. The long form survives as `memo/board-email-long.md` for a
follow-up or for staff. Two rules from the author's brief are kept in both: the
verbatim ask sentence, and no "hold", "defer" or "postpone" (the reviewer's draft
ends with "please hold this component"; that phrase is replaced by the verbatim
ask).

## Plan

1. **Now, no data needed** (about an hour): add "at 90% following" to the email's
   probability sentence; replace "the district has not modeled" with "the documents
   do not say which flows are assumed to persist"; add the non-additivity clause to
   the Summary; name births in the staff request; convert the staff-request prose
   into the worksheet table; add "placements/other" as an explicit term in the
   identity with a note that it is not separable in the documents on file. Rebuild,
   push.
2. **Draft the short email** as `memo/board-email-short.md` (about 260 words) for
   the author to choose between; rename the current file `board-email-long.md`.
3. **On receipt of the matrix**: log it as a source; build
   `data/clean/enrollment_pattern_matrix_mesa_bearcreek.csv` with the origin and
   destination cells for the Bear Creek, Mesa and any optional/dual areas; rebuild
   Table 11 and Fig. 14 on the five-term identity with the matrix's own categories;
   rewrite the fork paragraph; replace the x sensitivity with the observed split
   (keep one row for the geography question). Half a day.
4. **Deferred**: births-based kindergarten spec.

## What I need from the author

- The Enrollment Pattern Matrix (December 2025). Start at
  https://www.bvsd.org/current-topics/declining-enrollment and follow "Open
  Enrollment Matrices" under Resources; save the elementary matrix (PDF or
  spreadsheet) into `data/manual/`. If it is one file per school, Bear Creek and
  Mesa are enough, plus any file naming an optional or dual area for either.
- A decision on the email form: short (recommended), long, or both.
