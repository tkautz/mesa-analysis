"""One-off: move the hand-downloaded files from data/manual/ into data/raw/bvsd/ with consistent
names, drop byte-identical duplicates, and write data/raw/bvsd/MANIFEST.csv (original name ->
new path, md5, bytes). Uses `git mv` so history follows the file.
"""
import hashlib, re, subprocess, csv
from pathlib import Path
M = Path("data/manual"); B = Path("data/raw/bvsd"); PC = B / "pupil_count"
PC.mkdir(parents=True, exist_ok=True)
def md5(p): return hashlib.md5(p.read_bytes()).hexdigest()
def target(name):
    n = name
    m = re.match(r"(\d{4}-\d{2})CDE?(FTE|HeadCount|SpecialPrograms)Summary", n) or re.match(r"(\d{4}-\d{2})(FTE|HeadCount|SpecialPrograms)Summary", n)
    if m:
        kind = {"FTE": "fte_summary", "HeadCount": "cde_headcount_summary", "SpecialPrograms": "special_programs_summary"}[m.group(2)]
        suffix = ""
        v = re.search(r"(V\d(?:_\d)?|FINAL\d+|lessequal16)", n)
        if v: suffix = "_" + v.group(1).lower()
        return PC / f"{m.group(1)}_{kind}{suffix}.pdf"
    m = re.match(r"(\d{4}-\d{2}) Enrollment Trend Report Executive Summary", n)
    if m: return B / f"trend_report_exec_summary_{m.group(1)}.pdf"
    m = re.match(r"Annual Enrollment Trend Report _ February (\d{4})", n)
    if m: return B / f"trend_report_feb{m.group(1)}.pdf"
    if n.startswith("Enrollment Worksession _ 10.21.2025"): return B / "worksession_2025-10-21.pdf"
    if n.startswith("Resilient Schools Proposal FINAL"): return B / "resilient_schools_proposal_2026-08-25.pdf"
    if n.startswith("Resilient Schools Proposal Frequently Asked"): return B / "resilient_schools_faq.pdf"
    if n.startswith("LRAC Final Metrics"): return B / "lrac_final_metrics_2023-06-13.pdf"
    if n.startswith("BVSD Enrollment Dashboard"): return B / "bvsd_enrollment_dashboard.pdf"
    if n.startswith("Bear Creek_Creekside"): return B / "bvsd_page_bear_creek_creekside.pdf"
    if n.startswith("Enrollment drops more than expected"): return B / "news_bvsd_enrollment_drops_more_than_expected.pdf"
    if n.startswith("Enrollment numbers drop less than expected in 2024"): return B / "news_bvsd_enrollment_drops_less_than_expected_2024.pdf"
    if n.startswith("Supporting students with special needs"): return B / "resilient_schools_special_needs.pdf"
    raise SystemExit(f"no rule for {name!r}")
rows, seen = [], {}
for p in sorted(M.iterdir(), key=lambda q: (len(q.name), q.name)):
    h = md5(p)
    if h in seen:
        rows.append(dict(original_name=p.name, new_path="(duplicate removed)", md5=h, bytes=p.stat().st_size, duplicate_of=seen[h]))
        subprocess.run(["git", "rm", "-q", str(p)], check=True); continue
    t = target(p.name)
    assert not t.exists(), t
    subprocess.run(["git", "mv", str(p), str(t)], check=True)
    seen[h] = str(t)
    rows.append(dict(original_name=p.name, new_path=str(t), md5=h, bytes=p.stat().st_size if p.exists() else t.stat().st_size, duplicate_of=""))
with open(B / "MANIFEST.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["original_name", "new_path", "md5", "bytes", "duplicate_of"]); w.writeheader(); w.writerows(rows)
print(open(B / "MANIFEST.csv").read())
