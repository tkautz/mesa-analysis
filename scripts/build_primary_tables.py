"""Build the Mesa / Bear Creek tables from PRIMARY BVSD documents in data/raw/bvsd/.

Extraction methods (recorded per row in `extraction`):
  text    - pdfplumber text layer (machine-readable)
  ocr+eye - page is an image; rapidocr output (data/raw/bvsd/page_renders/*.ocr.txt) checked token-by-token
            against the rendered page by a human-style visual read. Values below were typed from that read.
  eye     - value read off a chart (bar label or axis position); approximate unless a printed label existed.
Outputs (data/clean/):
  feb2024_report_p11.csv, feb2025_report_p9.csv, oct2025_deck_s17.csv, feb2026_report_p9.csv  (Mesa + Bear Creek rows)
  aug2026_deck_p50.csv, aug2026_deck_p51.csv, aug2026_deck_p44.csv
  capacity_summary_mesa_bearcreek_by_vintage.csv   (long: school x vintage x year x measure)
  projections_by_vintage.csv                        (rebuilt; supersedes the transcription-based version)
  resident_vs_enrolled_mesa_bearcreek.csv
  verification_headcount_sources.csv                (BVSD official vs the two enrollmentdata series)
"""
import pandas as pd
C = "data/clean/"
YEARS = ["2026-27", "2027-28", "2028-29", "2029-30", "2030-31"]

# ---- capacity summary tables: (capacity, rounds, enroll, pct, rnds), then 5 x (proj, pct, rnds) ----
TABLES = {
 "feb2024": dict(src="data/raw/bvsd/trend_report_feb2024.pdf", page=11, title="BVSD Capacity Summary 2023-24 (updated 1/26/2024)",
                 base="2023-24", years=["2024-25", "2025-26", "2026-27", "2027-28", "2028-29"],
                 rows={"Bear Creek": [467, 3.0, 298, 64, 2.0, 287, 61, 1.9, 273, 58, 1.8, 271, 58, 1.8, 262, 56, 1.7, 248, 53, 1.7],
                       "Mesa":       [418, 3.0, 233, 56, 1.6, 220, 53, 1.5, 211, 50, 1.4, 202, 48, 1.3, 203, 49, 1.4, 202, 48, 1.3]}),
 "feb2025": dict(src="data/raw/bvsd/trend_report_feb2025.pdf", page=9, title="BVSD Capacity Summary 2024-25 (updated 1/24/2025)",
                 base="2024-25", years=["2025-26", "2026-27", "2027-28", "2028-29", "2029-30"],
                 rows={"Bear Creek": [492, 3.5, 318, 65, 2.1, 308, 63, 2.1, 302, 61, 2.0, 290, 59, 1.9, 274, 56, 1.8, 272, 55, 1.8],
                       "Mesa":       [418, 3.0, 230, 55, 1.5, 230, 55, 1.5, 220, 53, 1.5, 218, 52, 1.5, 216, 52, 1.4, 224, 54, 1.5]}),
 "oct2025": dict(src="data/raw/bvsd/worksession_2025-10-21.pdf", page=17, title="Elementary Attendance Area Region - Boulder (slide 17)",
                 base="2024-25", years=["2025-26", "2026-27", "2027-28", "2028-29", "2029-30"],
                 rows={"Bear Creek": [492, 3.5, 318, 65, 2.1, 308, 63, 2.1, 302, 61, 2.0, 290, 59, 1.9, 274, 56, 1.8, 272, 55, 1.8],
                       "Mesa":       [418, 3.0, 230, 55, 1.5, 230, 55, 1.5, 220, 53, 1.5, 218, 52, 1.5, 216, 52, 1.4, 224, 54, 1.5]}),
 "feb2026": dict(src="data/raw/bvsd/trend_report_feb2026.pdf", page=9, title="BVSD Capacity Summary 2025-26 (updated 1/26/2026)",
                 base="2025-26", years=YEARS,
                 rows={"Bear Creek": [492, 3.5, 312, 63, 2.1, 299, 61, 2.0, 293, 60, 2.0, 288, 59, 1.9, 310, 63, 2.1, 320, 65, 2.1],
                       "Mesa":       [418, 3.0, 224, 54, 1.5, 217, 52, 1.4, 203, 49, 1.4, 203, 49, 1.4, 202, 48, 1.3, 201, 48, 1.3]}),
}
long = []
for vint, t in TABLES.items():
    wide = []
    for sch, v in t["rows"].items():
        r = dict(school=sch, capacity=v[0], capacity_rounds=v[1], enroll_base=v[2], pct_cap_base=v[3], rounds_base=v[4], base_year=t["base"])
        long += [dict(school=sch, vintage=vint, school_year="capacity", measure="capacity", value=v[0], data_type="capacity"),
                 dict(school=sch, vintage=vint, school_year="capacity", measure="capacity_rounds", value=v[1], data_type="capacity"),
                 dict(school=sch, vintage=vint, school_year=t["base"], measure="enrollment", value=v[2], data_type="actual (as printed)"),
                 dict(school=sch, vintage=vint, school_year=t["base"], measure="pct_capacity", value=v[3], data_type="actual (as printed)"),
                 dict(school=sch, vintage=vint, school_year=t["base"], measure="rounds", value=v[4], data_type="actual (as printed)")]
        for k, yr in enumerate(t["years"]):
            p, pc, rn = v[5 + 3 * k: 8 + 3 * k]
            r[f"proj_{yr}"] = p; r[f"pct_{yr}"] = pc; r[f"rounds_{yr}"] = rn
            long += [dict(school=sch, vintage=vint, school_year=yr, measure="enrollment", value=p, data_type="projection"),
                     dict(school=sch, vintage=vint, school_year=yr, measure="pct_capacity", value=pc, data_type="projection"),
                     dict(school=sch, vintage=vint, school_year=yr, measure="rounds", value=rn, data_type="projection")]
        wide.append(r)
    for row in long:
        if row["vintage"] == vint and "_source" not in row:
            row.update(_source=t["src"], _page=t["page"], _table=t["title"], extraction="ocr+eye", verified_against_primary=True)
    w = pd.DataFrame(wide); w["_source"] = t["src"]; w["_page"] = t["page"]; w["_table"] = t["title"]; w["extraction"] = "ocr+eye"
    name = {"feb2024": "feb2024_report_p11", "feb2025": "feb2025_report_p9", "oct2025": "oct2025_deck_s17", "feb2026": "feb2026_report_p9"}[vint]
    w.to_csv(f"{C}{name}.csv", index=False)
cap = pd.DataFrame(long)
cap.to_csv(f"{C}capacity_summary_mesa_bearcreek_by_vintage.csv", index=False)

# ---- Aug 25 2026 deck, text layer ----
p51 = pd.DataFrame([
    dict(school="Bear Creek", school_year="2025-26", measure="capacity", value=492, data_type="capacity"),
    dict(school="Bear Creek", school_year="2025-26", measure="resident_students", value=275, data_type="actual"),
    dict(school="Bear Creek", school_year="2025-26", measure="enrolled_students", value=312, data_type="actual"),
    dict(school="Bear Creek", school_year="2025-26", measure="utilization_pct", value=63, data_type="actual"),
    dict(school="Mesa", school_year="2025-26", measure="capacity", value=418, data_type="capacity"),
    dict(school="Mesa", school_year="2025-26", measure="resident_students", value=228, data_type="actual"),
    dict(school="Mesa", school_year="2025-26", measure="enrolled_students", value=224, data_type="actual"),
    dict(school="Mesa", school_year="2025-26", measure="utilization_pct", value=54, data_type="actual"),
    dict(school="Consolidated (Bear Creek bldg)", school_year="2027-28", measure="capacity", value=492, data_type="capacity"),
    dict(school="Consolidated (Bear Creek bldg)", school_year="2027-28", measure="resident_students", value=473, data_type="projection"),
    dict(school="Consolidated (Bear Creek bldg)", school_year="2027-28", measure="enrolled_students_low", value=392, data_type="projection"),
    dict(school="Consolidated (Bear Creek bldg)", school_year="2027-28", measure="enrolled_students_high", value=445, data_type="projection"),
    dict(school="Consolidated (Bear Creek bldg)", school_year="2027-28", measure="utilization_pct_low", value=80, data_type="projection"),
    dict(school="Consolidated (Bear Creek bldg)", school_year="2027-28", measure="utilization_pct_high", value=90, data_type="projection"),
    dict(school="Consolidated (Bear Creek bldg)", school_year="2030-31", measure="resident_students", value=522, data_type="projection"),
    dict(school="Consolidated (Bear Creek bldg)", school_year="2030-31", measure="enrolled_students_low", value=403, data_type="projection"),
    dict(school="Consolidated (Bear Creek bldg)", school_year="2030-31", measure="enrolled_students_high", value=462, data_type="projection"),
    dict(school="Consolidated (Bear Creek bldg)", school_year="2030-31", measure="utilization_pct_low", value=82, data_type="projection"),
    dict(school="Consolidated (Bear Creek bldg)", school_year="2030-31", measure="utilization_pct_high", value=94, data_type="projection"),
])
p51["_source"] = "data/raw/bvsd/resilient_schools_proposal_2026-08-25.pdf"; p51["_page"] = 51; p51["extraction"] = "text"
p51["note"] = "'*Projected enrollment ranges dependent on number of resident students from the sending school attending the receiving school.'"
p51.to_csv(f"{C}aug2026_deck_p51.csv", index=False)

p50 = pd.DataFrame([
    dict(school="Bear Creek", measure="utilization_pct", value=63), dict(school="Mesa", measure="utilization_pct", value=54),
    dict(school="Bear Creek", measure="classes_per_grade", value=2.1), dict(school="Mesa", measure="classes_per_grade", value=1.5),
    dict(school="Bear Creek-Mesa", measure="distance_miles", value=0.71),
])
p50["quote"] = "Bear Creek is currently at 63% utilization and Mesa is at 54%. Bear Creek is at 2.1 classes/grade and Mesa is at 1.5 classes/grade. ... Mesa also has the second lowest number of resident students in its attendance area."
p50["_source"] = "data/raw/bvsd/resilient_schools_proposal_2026-08-25.pdf"; p50["_page"] = 50; p50["extraction"] = "text"
p50.to_csv(f"{C}aug2026_deck_p50.csv", index=False)

p44 = pd.DataFrame([
    dict(school="Mesa", measure="resident_attending_neighborhood_school_2025-26", value=156, extraction="eye (printed bar label)"),
    dict(school="Mesa", measure="resident_students_total_2025-26", value=228, extraction="eye (bar end; equals p.51 text value 228)"),
    dict(school="Mesa", measure="projected_resident_students_2030", value=177, extraction="eye (diamond marker; approximate, +/-5)"),
    dict(school="Bear Creek", measure="resident_attending_neighborhood_school_2025-26", value=217, extraction="eye (printed bar label)"),
    dict(school="Bear Creek", measure="resident_students_total_2025-26", value=275, extraction="eye (bar end; equals p.51 text value 275)"),
    dict(school="Bear Creek", measure="projected_resident_students_2030", value=268, extraction="eye (diamond marker; approximate, +/-5)"),
])
p44["_source"] = "data/raw/bvsd/resilient_schools_proposal_2026-08-25.pdf"; p44["_page"] = 44
p44.to_csv(f"{C}aug2026_deck_p44.csv", index=False)

# ---- resident vs enrolled (open question 4) ----
sp = pd.read_csv(f"{C}bvsd_pupil_count_mesa_bearcreek.csv")
sp = sp[(sp.file_family == "special_programs") & (sp.school_year == "2025-26")].set_index("school")
rv = []
for sch, res, att, enr in [("Mesa", 228, 156, 224), ("Bear Creek", 275, 217, 312)]:
    ood = int(sp.loc[sch, "out_of_district_n"])
    rv += [dict(school=sch, school_year="2025-26", measure="resident_students_in_attendance_area", value=res, _source="aug2026 deck p.51 (text)"),
           dict(school=sch, school_year="2025-26", measure="residents_attending_this_school", value=att, _source="aug2026 deck p.44 (printed bar label)"),
           dict(school=sch, school_year="2025-26", measure="residents_attending_elsewhere (derived)", value=res - att, _source="derived: p.51 resident minus p.44 label"),
           dict(school=sch, school_year="2025-26", measure="enrolled_students", value=enr, _source="aug2026 deck p.51 (text); equals 2025-26 pupil count"),
           dict(school=sch, school_year="2025-26", measure="out_of_district_enrolled", value=ood, _source="data/raw/bvsd/pupil_count/2025-26_special_programs_summary.pdf p.1 'Out of District'"),
           dict(school=sch, school_year="2025-26", measure="in_district_open_enrolled_in (derived)", value=enr - att - ood, _source="derived: enrolled minus residents attending minus out-of-district"),
           dict(school=sch, school_year="2025-26", measure="resident_capture_rate_pct (derived)", value=round(100 * att / res, 1), _source="derived: residents attending / residents in area")]
pd.DataFrame(rv).to_csv(f"{C}resident_vs_enrolled_mesa_bearcreek.csv", index=False)

# ---- projections_by_vintage (rebuilt from primaries) ----
pv = cap[cap.measure == "enrollment"][["school", "vintage", "school_year", "value", "data_type", "_source", "_page", "extraction"]].copy()
pv["verified_against_primary"] = True
add = p51[p51.measure.str.startswith("enrolled_students")].copy()
add["school"] = "Bear Creek (consolidated w/ Mesa)"; add["vintage"] = "aug2026"
add["data_type"] = "projection (post-proposal, " + add.measure.str.replace("enrolled_students_", "") + ")"
add = add[["school", "vintage", "school_year", "value", "data_type", "_source", "_page", "extraction"]]; add["verified_against_primary"] = True
add.loc[add.data_type.str.contains("high"), "note"] = "deck p.51: 'Enrolled Students: 403 to 462' (2030-31); CLAUDE.md's 'pp. 37, 39' page reference is wrong for this deck"
closes = pd.DataFrame([dict(school="Mesa", vintage="aug2026", school_year="2027-28", value=0, data_type="projection (post-proposal): school closes",
                            _source="data/raw/bvsd/resilient_schools_proposal_2026-08-25.pdf", _page=49, extraction="text", verified_against_primary=True)])
pv = pd.concat([pv, add, closes], ignore_index=True)
pv["vintage_note"] = pv.vintage.map({"feb2024": "Feb 27 2024 report; table updated 1/26/2024", "feb2025": "Feb 11 2025 report; table updated 1/24/2025",
                                     "oct2025": "Oct 21 2025 work session slide 17; identical to feb2025 for these two schools",
                                     "feb2026": "Feb 10 2026 report; table updated 1/26/2026", "aug2026": "Aug 25 2026 proposal deck"})
pv.to_csv(f"{C}projections_by_vintage.csv", index=False)

# ---- headcount source comparison ----
hc = pd.read_csv(f"{C}bvsd_pupil_count_mesa_bearcreek.csv"); hc = hc[hc.file_family == "headcount"]
hc["october_year"] = hc.school_year.str[:4].astype(int)
off = hc.set_index(["school", "october_year"])["funded_headcount"].rename("bvsd_official")
ed = pd.read_csv(f"{C}mesa_bearcreek_headcount.csv"); ed = ed[ed.measure == "enrollment"]
ed["school"] = ed.school.str.title(); ed = ed.set_index(["school", "october_year"])["value"].rename("enrollmentdata_csv")
mp = pd.read_csv(f"{C}enrollmentdata_map_history_all_schools.csv"); mp = mp[mp.school.isin(["Mesa Elementary", "Bear Creek Elementary"])]
mp["school"] = mp.school.str.replace(" Elementary", ""); mp = mp.set_index(["school", "october_year"])["enrollment"].rename("enrollmentdata_map")
cmp = pd.concat([off, ed, mp], axis=1)
cmp["csv_minus_official"] = cmp.enrollmentdata_csv - cmp.bvsd_official; cmp["map_minus_official"] = cmp.enrollmentdata_map - cmp.bvsd_official
cmp["_official_source"] = "data/raw/bvsd/pupil_count/<year>_cde_headcount_summary*.pdf p.1, 'FUNDED HEAD COUNT' current-year column"
cmp.reset_index().to_csv(f"{C}verification_headcount_sources.csv", index=False)
print(cmp.reset_index().to_string(index=False))
print(pd.DataFrame(rv)[["school", "measure", "value"]].to_string(index=False))
