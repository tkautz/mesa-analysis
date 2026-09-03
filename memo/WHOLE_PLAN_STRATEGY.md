# Should the argument be about the whole plan? A critical assessment and, with modifications, a plan

## 1. The idea, stated fairly
Argue that the Resilient Schools package as a whole rests on the same untested assumptions, that its components interact (every projection is conditioned on the portfolio the package abolishes), and that the Board should therefore review the whole thing rather than approve it piecemeal on September 22.

## 2. Where it is right
1. **Interdependence is real and documented.** Every post-change range in the deck (pp. 25, 37, 48, 51, 54) is a standalone projection fitted under the current portfolio plus a reassignment; the FAQ (p. 3) says choice enrollment will be "managed" where receiving schools near capacity, which changes flows everywhere else. The district itself presents the package as integrated: one summary (p. 58), one districtwide boundary map (p. 59), one savings figure (p. 60).
2. **The same unstated-share method underlies every receiving school.** The footnote on p. 51 ("dependent on number of resident students from the sending school attending the receiving school") appears, word for word, on pp. 25, 37, 48 and 54.
3. **The shares are not consistent across components.** Decoding each range against the Feb 2026 standalone projections (`analysis/output/table10_package_implied_shares.csv`, Figure 13):

| Component (deck page) | Implied share following, 2027-28 | 2030-31 | Students outside the range at its top, 2030-31 |
|---|---|---|---|
| Birch → Kohl (p. 25) | 81–100% | 82–100% | 0 |
| Flatirons → Foothill + Whittier (p. 54) | 81–100% | 82–96% | 6 |
| Douglass → Coal Creek + Eisenhower + Heatherwood (p. 48) | 86–100% | 84–100% | 0 |
| Monarch K-5 → Fireside + Superior + Eldorado (p. 37) | 65–81% | 55–71% | 82 |
| Mesa → Bear Creek (p. 51) | 49–75% | 41–71% | 59 |

For three components the top of the range is exactly the sum of the standalone projections (everyone follows) and the bottom is about 82–86%. For the two components where the sum would exceed the receiving buildings (Bear Creek; Superior at 96–98%), the implied share drops to 41–75%. On its face, the ranges were fitted to the buildings where the arithmetic did not fit, rather than derived from one retention assumption. The district may have a resident-based explanation; it has not given one, and the pattern is the same under a resident-based reading. This is the single most important new fact, and it is package-wide by construction.
4. **The package-level headlines depend on the top of every range at once** (14 → 6 schools below two classes, 68% → 75% utilization, p. 58; recount in `ADDENDUM_district_claims.md` §6).
5. **It neutralizes the district's fairness counter** ("why should South Boulder get a study when Broomfield does not?") and the special-pleading perception, and it fits the precedent the district set by holding the dual-language component for study (p. 72).
6. **The standard (i)–(v) is already written for any component.** Nothing in it is Mesa-specific.

## 3. Where it is wrong or risky
1. **"The whole plan has issues" invites the reply "then nothing happens, and it costs $3.5–4.0M a year."** A blanket hold is the most expensive ask available and the easiest to refuse. The Board has tied action to the November 1 choice window (p. 67) and has heard two years of "staying small is not an option".
2. **Our own model supports closing the smallest schools.** It says Mesa stays small; it would say the same, more strongly, of Flatirons (151 students, one round, 47%) and Douglass. An enrollment-based attack on those closures would contradict our own concession and hand the district an inconsistency. The whole-plan critique cannot be "no school should close"; it has to be about assumptions, fit, cost and process.
3. **Depth.** The Mesa analysis is deep because we spent three sessions on it. For other components we have the deck's numbers, the Feb 2026 projections and grade data for every school, but no resident splits by sub-area and no flow data. A whole-plan document that is thin per component is easier to dismiss than a deep one on one component.
4. **Coalitions have different interests.** Douglass and Flatirons parents want their schools kept; receiving-school parents may want the package (smaller classes promised); Monarch/Eldorado is a reconfiguration, not a closure. A "review everything" position speaks for all of them without any of them having asked.
5. **A Mesa parent broadening to the whole district looks tactical.** The district's reviewer flagged "insinuation" as the fastest way to lose the Board; "the whole plan is flawed" reads as insinuation unless every claim is the district's own number.

## 4. Verdict
Agree with the diagnosis, not the headline. The defensible version is:

> **The same gaps run through every component; Mesa/Bear Creek is where they bite hardest. Apply the evidence standard to each component. Proceed with those that meet it. Hold the ones that do not, as the district already did with dual-language.**

This keeps every strength of the whole-plan idea (interdependence, inconsistent shares, package headlines, fairness, precedent), avoids the blanket-stop trap, stays consistent with our concession that small schools are small, and lets the Board sort rather than stall. It also turns the district's fairness counter around: fairness means one standard, applied everywhere, and the deck's own ranges show it was not.

If the Board is invited to sort, the deck's own numbers sort the components roughly as follows (this is our reading, to be stated with care and without endorsing any closure):
- **Clearest fit, most consistent assumptions:** Flatirons → Foothill/Whittier; Douglass → three schools (shares 82–100%; receivers at 87% or below).
- **Fit depends on the top of the range and on an 82–100% share, receiver near capacity:** Birch → Kohl (88% at top).
- **Fit depends on a reduced share and on managing choice; receiver at or over capacity under the district's own assumptions:** Monarch K-5 → Fireside/Superior/Eldorado (Superior 96–98% in 2027-28); Mesa → Bear Creek (41–71%; 521 vs 492).

## 5. The plan
### 5.1 Reframe the three documents (one day)
- **Email.** Keep the Mesa-specific evidence. Change the ask to: "Decline to approve any component of the Resilient Schools proposal that does not meet this standard, beginning with the Mesa/Bear Creek component, and direct staff to return with an analysis that meets it for each." Add one paragraph: the deck's own ranges imply 82–100% of students follow in three components and 41–75% in the two where the receiving buildings would otherwise overflow (Figure 13). Add the study precedent (p. 72). Keep ≤ 750 words by cutting the Heatherwood-style detail.
- **Appendix.** New section "The same gaps across the package": Figure 13; the package fit table (`table08_package_ranges.csv`); the recount (§6 of the addendum); the "10 schools needed, 13 remain" arithmetic; the statement that projections are conditioned on the current portfolio. Retitle the conclusion to the component-by-component ask.
- **Script.** Replace "this piece" with "any component whose numbers don't yet add up, starting with Mesa", and use the 82–100% vs 41–71% contrast as the second point (it is arithmetic a listener can hold).

### 5.2 Package-wide replication of the Mesa analysis (two days; data in hand)
Run the cohort model for every receiving school and its senders, both kindergarten assumptions, using the deck's own post-change resident counts (p. 48 gives 455/387/305 for Coal Creek/Eisenhower/Heatherwood in 2027-28; p. 25 gives 501 for Kohl; p. 37 gives 372/477/360; p. 54 gives 437/413) to apportion sending students, and each receiver's current capture rate. Output: one table with P(over capacity) and P(below two rounds) for all six receiving configurations in 2027-28 and 2030-31. Expected result on the deck's own numbers: Superior and Bear Creek show material over-capacity risk; Kohl and Foothill some; Eisenhower, Heatherwood, Whittier, Eldorado none. That table is the "apply the standard to each component" document.

### 5.3 Package-level cost (half a day; then CORA)
$3.5–4.0M ÷ 6 closed schools; the two one-time lines; no per-school figure for any component; the facility line "some offset by savings from Bond projects" not quantified. The point is the same for every component and the CORA request (interrogation plan §F) should ask for the by-school breakdown of both lines for the whole package, not only Mesa.

### 5.4 Process (no analysis)
Study precedent (p. 72); the February schedule (study in September, action in October; Feb 2026 p. 13) versus the September 22 vote; the Sept 8 "further study" of the open-enrollment priority (FAQ p. 2) that every component depends on. Ask for the priority rules to be settled before any component is approved, since every range assumes them.

### 5.5 Coalition, carefully (your call)
Offer the standard and the Figure 13 arithmetic to the other school communities as a shared frame without endorsing their enrollment claims. The line that travels: "One standard for every component; the deck's own numbers show it was not applied consistently."

### 5.6 What not to do
- Do not argue Flatirons or Douglass should stay open on enrollment grounds; our model does not support it.
- Do not claim the package "fails" in aggregate; claim that its components were not held to one standard and that the Board can sort them.
- Do not ask for a blanket delay; ask for a component-by-component decision against a stated standard.

## 6. Sequence
- **Now:** Figure 13 and `table10` exist; fold into the appendix as a new section and into the email as one paragraph (5.1).
- **Before Sept 8:** 5.2 replication table; 5.4 process points; send the CORA request package-wide.
- **Sept 8–22:** addendum with 5.2 results; offer to walk staff through the shares table; one question for the Board: "What share of each sending school's students does each range assume, and why does it differ by component?"
