"""Round 3 (2026-09-03): move the second batch of hand-downloaded files out of data/manual/. Appends to data/raw/bvsd/MANIFEST.csv."""
import hashlib, subprocess, csv
from pathlib import Path
M = Path("data/manual"); B = Path("data/raw/bvsd"); CDE = Path("data/raw/cde"); CDE.mkdir(exist_ok=True)
existing = {hashlib.md5(p.read_bytes()).hexdigest(): str(p) for p in list(B.rglob("*.pdf")) + list(CDE.rglob("*.xlsx"))}
rules = {
 "2019-20_Membership_Grade_bySchool_0.xlsx": CDE / "2019-20_membership_grade_by_school.xlsx",
 "2020-21_Membership_Grade_bySchool_1.xlsx": CDE / "2020-21_membership_grade_by_school.xlsx",
 "2021-22_Membership_Grade_bySchool_0.xlsx": CDE / "2021-22_membership_grade_by_school.xlsx",
 "2022-23_Membership_Grade_bySchool_0.xlsx": CDE / "2022-23_membership_grade_by_school.xlsx",
 "2023-24_Membership_Grade_bySchool_0.xlsx": CDE / "2023-24_membership_grade_by_school.xlsx",
 "2024-25_Membership_Grade_bySchool.xlsx": CDE / "2024-25_membership_grade_by_school.xlsx",
 "2025-2026_PupilMembership_SchoolLevel.xlsx": CDE / "2025-26_pupil_membership_school_level.xlsx",
 "BOE Attendance Boundary Study Item _ 2025.09.09 (1).pdf": B / "boundary_study_item_2025-09-09.pdf",
 "BOE Attendance Boundary Worksession _ 2025.3.11.pdf": B / "boundary_worksession_2025-03-11.pdf",
 "Resilient Schools_ Responding to declining enrollment - Boulder Valley School District.pdf": B / "bvsd_page_declining_enrollment.pdf",
 "2020-21SpecialProgramsSummaryV3.pdf": B / "pupil_count" / "2020-21_special_programs_summary_v3.pdf",
}
rows = []
for p in sorted(M.iterdir()):
    h = hashlib.md5(p.read_bytes()).hexdigest()
    if h in existing:
        rows.append(dict(original_name=p.name, new_path="(duplicate removed)", md5=h, bytes=p.stat().st_size, duplicate_of=existing[h]))
        subprocess.run(["git", "rm", "-q", str(p)], check=True); continue
    t = rules[p.name]; assert not t.exists(), t
    subprocess.run(["git", "mv", str(p), str(t)], check=True)
    rows.append(dict(original_name=p.name, new_path=str(t), md5=h, bytes=t.stat().st_size, duplicate_of=""))
with open(B / "MANIFEST.csv", "a", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["original_name", "new_path", "md5", "bytes", "duplicate_of"]); w.writerows(rows)
for r in rows: print(r["original_name"], "->", r["new_path"], r["duplicate_of"])
