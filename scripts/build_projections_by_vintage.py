"""Assemble data/clean/projections_by_vintage.csv for Mesa and Bear Creek.

Vintages:
  oct2025 - BVSD Oct 21 2025 work session deck. Primary PDF NOT retrieved this session; the only
            figures are those supplied in CLAUDE.md 'Key facts'. Flagged verified_against_primary=False.
  feb2026 - BVSD Feb 10 2026 Annual Enrollment Trend Report p.9, via enrollmentdata.org CSV transcription.
  aug2026 - BVSD Aug 25 2026 Resilient Schools Proposal deck (post-change ranges), via enrollmentdata.org
            map transcription (maps/index.html `proposalProjections`).
No row in this file has been checked against a primary BVSD document (all primary hosts were egress-blocked).
"""
import pandas as pd
rows = []
def add(school, vintage, sy, val, dtype, src, verified, note=""):
    rows.append(dict(school=school, vintage=vintage, school_year=sy, value=val, data_type=dtype,
                     _source=src, verified_against_primary=verified, note=note))
u = ("CLAUDE.md 'Key facts' (user-supplied; attributed to BVSD Oct 21 2025 work session deck); "
     "primary PDF NOT retrieved (egress blocked)")
add("Bear Creek", "oct2025", "2029-30", 272, "projection", u, False, "unverified")
add("Mesa", "oct2025", "2029-30", 224, "projection", u, False, "unverified")
add("Bear Creek", "oct2025", "capacity", 492, "capacity", u + "; slide 17", False, "3.5 rounds; equals feb2026 transcription")
add("Mesa", "oct2025", "capacity", 418, "capacity", u + "; slide 17", False, "3.0 rounds; equals feb2026 transcription")

cap = pd.read_csv("data/raw/enrollmentdata/BVSD_Capacity_Forecast_2025-2031.csv")
f = ("data/raw/enrollmentdata/BVSD_Capacity_Forecast_2025-2031.csv (enrollmentdata.org transcription of "
     "Feb 10 2026 Annual Enrollment Trend Report p.9, 'Capacity Summary 2025-26' updated 1/26/2026)")
for _, r in cap[cap.School.isin(["Mesa", "Bear Creek"])].iterrows():
    add(r.School, "feb2026", "2025-26", r["Enroll_2025-26"], "actual (as printed in report)", f, False,
        "report's own 2025-26 enrollment column; Mesa 224 here vs 225 in October headcount transcription (see CONFLICTS.md)")
    add(r.School, "feb2026", "capacity", r.Capacity, "capacity", f, False, f"{r.Cap_Rounds} rounds")
    for sy in ["2026-27", "2027-28", "2028-29", "2029-30", "2030-31"]:
        add(r.School, "feb2026", sy, r[f"Proj_{sy}"], "projection", f, False, "")

pp = pd.read_csv("data/clean/aug2026_proposal_projections_transcribed.csv")
g = ("data/raw/enrollmentdata/maps/index.html line {line} (enrollmentdata.org transcription of BVSD Aug 25 2026 "
     "Resilient Schools Proposal deck, pp. 25/37/39/48/51/54)")
for _, r in pp[pp.school.str.contains("Bear Creek|Mesa")].iterrows():
    sy = f"{r.fall_year}-{str(r.fall_year + 1)[2:]}"
    sch = r.school.replace(" Elementary", "")
    closes = r.closes if isinstance(r.closes, str) else ""
    if closes:
        add(sch, "aug2026", sy, 0, "projection (post-proposal)", g.format(line=r._source_line), False, closes)
    else:
        add(sch, "aug2026", sy, int(r.enroll_lo), "projection (post-proposal, low)", g.format(line=r._source_line), False,
            f"{r.pct_cap_lo}% of capacity; range depends on share of Mesa students who follow")
        add(sch, "aug2026", sy, int(r.enroll_hi), "projection (post-proposal, high)", g.format(line=r._source_line), False,
            f"{r.pct_cap_hi}% of capacity; CLAUDE.md quotes deck pp.37,39 'up to 462 students in 2030'")
df = pd.DataFrame(rows)
df.to_csv("data/clean/projections_by_vintage.csv", index=False)
print(df[df.vintage == "aug2026"][["school", "school_year", "value", "data_type", "note"]].to_string())
