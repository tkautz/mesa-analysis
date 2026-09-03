"""Extract the data tables embedded as JavaScript in the vendored enrollmentdata.org map
(data/raw/enrollmentdata/maps/index.html) into CSVs in data/clean/.

This is a transcription-of-a-transcription: enrollmentdata.org transcribed BVSD documents
into JS literals; we parse those literals. Every output row carries the source line number.
Nothing here is a primary BVSD document.
"""
import re, json
from pathlib import Path
import pandas as pd

SRC_FILE = Path("data/raw/enrollmentdata/maps/index.html")
CLEAN = Path("data/clean")
lines = SRC_FILE.read_text(encoding="utf-8").splitlines()
SRC = "data/raw/enrollmentdata/maps/index.html"

# 1) per-school October history embedded in the `schools` array
hist_rows = []
for i, ln in enumerate(lines, 1):
    m = re.search(r"\{ name: '([^']+)'.*?levels: \[([^\]]*)\]", ln)
    if not m:
        continue
    name = m.group(1)
    # history sits on this line or the next
    blob = ln + (lines[i] if i < len(lines) else "")
    for lvl_m in re.finditer(r"(elementary|middle|high): \{ current: (\d+), peak: (\d+), peakYear: (\d+), pctOfPeak: ([\d.]+), history: \[([^\]]*)\]", blob):
        level, current, peak, peak_year, pct, hist = lvl_m.groups()
        for y, e in re.findall(r"year:(\d+),enrollment:(\d+)", hist):
            hist_rows.append(dict(school=name, level=level, october_year=int(y), enrollment=int(e),
                                  data_type="actual", _source=SRC, _source_line=i))
hist = pd.DataFrame(hist_rows)
hist.to_csv(CLEAN / "enrollmentdata_map_history_all_schools.csv", index=False)

# 2) elementary capacity/forecast block (Feb 2026 report transcription)
fc_rows = []
in_block = False
for i, ln in enumerate(lines, 1):
    if ln.startswith("const elementaryForecast"):
        in_block = True; continue
    if in_block and ln.startswith("};"):
        break
    if in_block:
        m = re.search(r"^\s*(?:'([^']+)'|\"([^\"]+)\"): \{ capacity: (\d+), proj: \[([\d,]+)\]", ln)
        if m:
            name = m.group(1) or m.group(2)
            projs = [int(x) for x in m.group(4).split(",")]
            for yr, p in zip(["2026-27", "2027-28", "2028-29", "2029-30", "2030-31"], projs):
                fc_rows.append(dict(school=name, capacity=int(m.group(3)), school_year=yr, projected_enrollment=p,
                                    data_type="projection", vintage="feb2026", _source=SRC, _source_line=i))
pd.DataFrame(fc_rows).to_csv(CLEAN / "enrollmentdata_map_elementary_forecast.csv", index=False)

# 3) Aug 25 2026 proposal post-change projections (transcribed from deck pp. 25,37,39,48,51,54)
pp_rows = []
in_block = False
for i, ln in enumerate(lines, 1):
    if ln.startswith("const proposalProjections"):
        in_block = True; continue
    if in_block and ln.startswith("};"):
        break
    if in_block:
        name_m = re.search(r"^\s*'([^']+)':", ln)
        if name_m:
            cur_name = name_m.group(1)
        for lvl_m in re.finditer(r"(elementary|middle):\s*\{(.*?)\]\s*\}", ln):
            level, body = lvl_m.groups()
            closes = re.search(r"closes: '([^']*)'", body)
            for y, lo, hi, plo, phi in re.findall(r"y: (\d+), lo: (\d+), hi: (\d+), pctLo: (\d+), pctHi: (\d+)", body):
                pp_rows.append(dict(school=cur_name, level=level, fall_year=int(y), enroll_lo=int(lo), enroll_hi=int(hi),
                                    pct_cap_lo=int(plo), pct_cap_hi=int(phi), closes=closes.group(1) if closes else "",
                                    data_type="projection", vintage="aug2026", _source=SRC, _source_line=i))
pp = pd.DataFrame(pp_rows)
pp.to_csv(CLEAN / "aug2026_proposal_projections_transcribed.csv", index=False)

# 4) proposal action text
pa_rows = []
for i, ln in enumerate(lines, 1):
    m = re.search(r"^\s*'([^']+)':\s*\{ action: '(\w+)', text: '([^']*)' \}", ln)
    if m:
        pa_rows.append(dict(school=m.group(1), action=m.group(2), text=m.group(3), _source=SRC, _source_line=i))
pd.DataFrame(pa_rows).to_csv(CLEAN / "aug2026_proposal_actions_transcribed.csv", index=False)

print(hist[hist.school.str.contains("Mesa|Bear Creek")].pivot(index="october_year", columns="school", values="enrollment"))
print(pp[pp.school.str.contains("Mesa|Bear Creek")])
print(len(hist), "history rows;", len(fc_rows), "forecast rows;", len(pp), "proposal rows;", len(pa_rows), "action rows")
