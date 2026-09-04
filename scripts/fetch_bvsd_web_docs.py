"""Download public BVSD web documents into data/raw/bvsd/<subfolder>/ and log them.

Run from the repository root:  python scripts/fetch_bvsd_web_docs.py
Never overwrites an existing file (skips it and records "exists"). Writes a
sibling .txt (pdfplumber text layer) for every PDF, and appends one row per
item to data/raw/bvsd/MANIFEST_web_fetch.csv (url, path, md5, bytes, status).
Session: 2026-09-03.
"""
from __future__ import annotations

import csv
import hashlib
import io
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "bvsd"
MANIFEST = RAW / "MANIFEST_web_fetch.csv"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
BV = "https://www.bvsd.org"
FS = "https://resources.finalsite.net/images"

# (url, relative destination under data/raw/bvsd/)
ITEMS: list[tuple[str, str]] = []

# 1. Open-enrollment matrices (planning-and-engineering page, "Open Enrollment Matrices")
_MATRIX = {
    "2025-26": ("v1765210795/bvsdorg/pxki5ikpp8oxvjmrnvvy/ElemMatrix2025-26.pdf",
                "v1765210794/bvsdorg/sqm57moh2n7qmurs2v6o/KMatrix2025-26.pdf"),
    "2024-25": ("v1734030049/bvsdorg/txb83uu3gm2qxmbwcrmi/ElemMatrix2024-25.pdf",
                "v1733773432/bvsdorg/fc5uu5n5zg2ybkqyguiy/KMatrix2024-25.pdf"),
    "2023-24": ("v1702400428/bvsdorg/aetbngspd9ginnzrvhln/ElemMatrix2023-24.pdf",
                "v1704227639/bvsdorg/hv3wchcs4fmjfqmwjlnb/KMatrix2023-24.pdf"),
    "2022-23": ("v1674243989/bvsdorg/cdckyv4yeugqbknn17xg/ElemMatrix2022-23.pdf",
                "v1674243989/bvsdorg/xtc38p0wpavlr13j1sq7/KMatrix2022-23.pdf"),
    "2021-22": ("v1666968472/bvsdorg/xx5b3cibilj68ik9dnme/Elementary_Matrix_2021-22.pdf",
                "v1640894980/bvsdorg/w0o7ymbnp3gr0jfwx5q3/KMatrix2021-22.pdf"),
    "2020-21": ("v1666968717/bvsdorg/e4emdrr3oihi0i4742zr/ElementaryMatrix2020-21.pdf",
                "v1609281017/bvsdorg/enthrge4d63gnyjr1yse/KindergartenMatrix_2020-21.pdf"),
    "2019-20": ("v1666968489/bvsdorg/unatplekaavcyouzcngk/ElemMatrix2019-20.pdf",
                "v1579908930/bvsdorg/dudvjobc0l7946pgzzvx/KinderMatrix2019-20.pdf"),
    "2018-19": ("v1564076568/bvsdorg/bkf2eudj2p86kvqfbu85/ElementarySchoolMatrix2018-19.pdf",
                "v1564076568/bvsdorg/gt9tumbi51mieyroqnle/KindergartenLevelMatrix2018-19.pdf"),
    "2017-18": ("v1564076602/bvsdorg/kuzsyrafndhmdhmuoguz/ElemMatrix2017-18.pdf",
                "v1564076602/bvsdorg/afyuaphye1antobghfij/KMatrix2017-18.pdf"),
    "2016-17": ("v1564076684/bvsdorg/ibwxxk6nnwxc46f0r8v2/ElemMatrix2016-17.pdf",
                "v1564076684/bvsdorg/ayzdsycd0j0jgk6sw88j/KMatrix2016-17.pdf"),
}
for yr, (elem, k) in _MATRIX.items():
    ITEMS.append((f"{FS}/{elem}", f"oe_matrices/elem_matrix_{yr}.pdf"))
    ITEMS.append((f"{FS}/{k}", f"oe_matrices/k_matrix_{yr}.pdf"))

# 2. School profile books (same page)
_PROFILES = {
    "2025": "v1771449488/bvsdorg/ymvdboxktqzmo89tmckq/SchoolProfile2025.pdf",
    "2024": "v1734562774/bvsdorg/erk3lnq7bbuo7sncsbae/SchoolProfile2024.pdf",
    "2023": "v1704920920/bvsdorg/s1vhiay2rjk3ju9afr8y/SchoolProfile2023.pdf",
    "2022": "v1674237244/bvsdorg/mnbwjgpqy5xh4t9azsrm/SchoolProfiles2022.pdf",
    "2021": "v1642021070/bvsdorg/djjm8vhkd7ousoxxk0cy/SchoolProfiles2021.pdf",
    "2020": "v1609785828/bvsdorg/blegnqw5oq5vv9bmq7rr/SchoolProfiles2020.pdf",
    "2019": "v1581355531/bvsdorg/t2ox9blewwlyvl5nswrh/SchoolProfile2019.pdf",
    "2018": "v1565906317/bvsdorg/gd8bhygzta2n6q6eylhb/SchoolProfile2018v1.pdf",
    "2017": "v1565906329/bvsdorg/lxoiz7ow2sjdizi6zd3k/SchoolProfile2017-2018v1.pdf",
    "2016": "v1562097366/bvsdorg/ww4crtlc7f94opql9cu7/SchoolProfiles2016.pdf",
    "2015": "v1562097366/bvsdorg/kn9v0vsgve9jrrnwihmo/SchoolProfiles2015.pdf",
    "2014": "v1562097362/bvsdorg/qgfulkzcyrjylcefrkzv/SchoolProfiles2014.pdf",
    "2013": "v1562097384/bvsdorg/jn8l1msudrup3yuogbrr/SchoolProfiles2013.pdf",
    "2012": "v1562097361/bvsdorg/dgr8izlelnjo3jdmxcgx/SchoolProfiles2012.pdf",
    "2011": "v1562097357/bvsdorg/muwywcagpxtsvjwrddcu/SchoolProfiles2011.pdf",
}
for yr, p in _PROFILES.items():
    ITEMS.append((f"{FS}/{p}", f"school_profiles/school_profiles_{yr}.pdf"))

# 3. 2026-27 weekly enrollment files (enrollment-statistics page)
_WEEKLY = {
    "2026-08-04": "0ded85b4-1fbf-47d2-95ba-2dbb13448cca",
    "2026-08-07": "8d34bc36-ee15-4966-9c17-714ecc9cfb3c",
    "2026-08-12": "42164f62-8884-442f-b5ad-1ae6849ea6df",
    "2026-08-14": "b73562f7-df3f-42cb-a827-b16d1f151782",
    "2026-08-18": "32870f67-a61f-4862-b813-199fa0c84277",
    "2026-08-21": "cae717ee-d109-468e-b537-e22310def0c5",
    "2026-08-25": "78160107-916f-42ef-8443-2184442e7ef2",
    "2026-08-28": "83a94195-1ae0-4b44-bdfa-3cccd9e119d5",
}
for d, rid in _WEEKLY.items():
    ITEMS.append((f"{BV}/fs/resource-manager/view/{rid}", f"enrollment_2026-27_weekly/enrollment_{d}"))

# 4. Pupil-count file missing from the repo
ITEMS.append((f"{BV}/fs/resource-manager/view/7c6ca3f9-6fd0-4069-ba66-92cf77ee9f56",
              "pupil_count/2020-21_fte_summary.pdf"))

# 5. Bond program final reports (capacity history)
ITEMS.append((f"{BV}/fs/resource-manager/view/dc851b6f-4812-4340-8ab5-81a1d9de44f9",
              "bond/bond_2014_program_final_report.pdf"))

# 6. Web pages (HTML saved as-is; text extracted separately)
_PAGES = {
    "web/page_declining_enrollment_2026-09-03.html": f"{BV}/current-topics/declining-enrollment",
    "web/page_supporting_data_2026-09-03.html": f"{BV}/current-topics/declining-enrollment/resilient-schools-proposal-supporting-data",
    "web/page_faq_2026-09-03.html": f"{BV}/current-topics/declining-enrollment/declining-enrollment-frequently-asked-questions",
    "web/page_engagement_map_2026-09-03.html": f"{BV}/current-topics/declining-enrollment/community-engagement-map",
    "web/page_planning_engineering_2026-09-03.html": f"{BV}/departments/operational-services/planning-and-engineering",
    "web/page_enrollment_statistics_2026-09-03.html": f"{BV}/departments/enrollment/enrollment-statistics",
    "web/page_boundary_changes_2026-09-03.html": f"{BV}/current-topics/attendance-area-boundary-changes",
    "web/page_boundary_bear_creek_creekside_2026-09-03.html": f"{BV}/current-topics/attendance-area-boundary-changes/bear-creekcreekside",
    "web/news_developing_the_proposal.html": f"{BV}/about/news/news-article/~board/district-news/post/developing-the-proposal-what-we-have-been-up-to-and-what-to-expect",
    "web/news_teachers_perspective.html": f"{BV}/about/news/news-article/~board/district-news/post/declining-enrollment-a-teachers-perspective",
    "web/comms_01_our_promise.html": f"{BV}/fs/comms-manager/view/d9a540a1-289e-4525-8512-0adb861a1d22",
    "web/comms_02_courage_to_imagine.html": f"{BV}/fs/comms-manager/view/3a2f7408-3b80-4f0e-9108-85a433f11e1b",
    "web/comms_03_engagement_differently.html": f"{BV}/fs/comms-manager/view/26471699-fff9-4de8-aa40-fd98879cb74c",
    "web/comms_04_thank_you_voice.html": f"{BV}/fs/comms-manager/view/8a5dfac9-c02a-4665-965b-bdbf3a50544d",
    "web/comms_05_rest_and_prepare.html": f"{BV}/fs/comms-manager/view/924fbd8d-80f9-4f66-ad09-1ec7ccd45e68",
    "web/comms_06_proposal_presented_aug25.html": f"{BV}/fs/comms-manager/view/f0499f1e-4683-4be4-b845-6fda93fff05c",
}
for dest, url in _PAGES.items():
    ITEMS.append((url, dest))

# 7. Second batch (same session): corrected 2017-18 matrix URL, LRAC page files,
#    2022 bond CBOC update, transportation resource pages for the two schools.
ITEMS.append((f"{FS}/v1564076602/bvsdorg/kuzsyrafndjmdhmuoguz/ElemMatrix2017-18.pdf",
              "oe_matrices/elem_matrix_2017-18.pdf"))
_LRAC_FILES = {  # order as listed on bvsd.org/current-topics/long-range-advisory-committee
    "lrac_01_agenda": "d931991f-c7ea-46fd-8b81-91e7a17e0899",
    "lrac_02_agenda": "5169ccf5-10f1-46fc-8ea2-71b7c78b7002",
    "lrac_02_minutes": "0c8ca955-c337-4f75-b3a4-28011a2d1788",
    "lrac_03_agenda": "964140cf-ced8-4069-9a00-8a49cee4d188",
    "lrac_03_minutes": "48160ef5-06b2-4fd4-89e7-0206f074f27c",
    "lrac_04_agenda": "d5a8c732-52c3-4310-8bef-229361bd19f6",
    "lrac_04_minutes": "cd987567-5ea9-49f1-b2b2-dd1f8bd84831",
    "lrac_05_agenda": "8aad2e48-aa38-415f-a3f7-791dffc3c21e",
    "lrac_05_minutes": "68f6e3c3-20f4-4843-b631-64d6f6eb49c2",
    "lrac_06_agenda": "9e301c3f-667d-4893-8695-f343f55a2c09",
    "lrac_06_minutes": "33d78a7e-d63f-42d9-b65c-e024dea1ebbc",
    "lrac_07_agenda": "e48949fc-8584-45f0-a9f2-c58928ce98db",
    "lrac_08_agenda": "aaf1ae92-b5d8-48f7-89a1-182ced61b9ca",
}
for name, rid in _LRAC_FILES.items():
    ITEMS.append((f"{BV}/fs/resource-manager/view/{rid}", f"lrac/{name}"))
ITEMS.append(("https://go.boarddocs.com/co/bvsd/Board.nsf/files/CF88FE1E1475/$file/BDFF%20Long%20Range%20Advisory%20Committee%20Final.pdf",
              "lrac/policy_bdff_long_range_advisory_committee.pdf"))
ITEMS.append(("https://go.boarddocs.com/co/bvsd/Board.nsf/files/DR5RVH6FD54C/$file/Bond_CBOC%20Update%20for%20BOE%20_%20February%202026.pdf",
              "bond/bond_2022_cboc_update_boe_2026-02.pdf"))
ITEMS.append((f"{BV}/current-topics/long-range-advisory-committee", "web/page_lrac_2026-09-03.html"))
ITEMS.append((f"{BV}/current-topics/long-range-advisory-committee/long-range-advisory-committee-metrics-and-recommendations",
              "web/page_lrac_metrics_2026-09-03.html"))
ITEMS.append((f"{BV}/departments/transportation/bvsd-safe-routes-to-school/school-travel-maps/bearcreek-transportation-resources",
              "web/page_transport_bear_creek_2026-09-03.html"))
ITEMS.append((f"{BV}/departments/transportation/bvsd-safe-routes-to-school/school-travel-maps/mesa-transportation-resources",
              "web/page_transport_mesa_2026-09-03.html"))
ITEMS.append(("https://bond.bvsd.org/", "web/page_bond_2022_2026-09-03.html"))


def md5(b: bytes) -> str:
    return hashlib.md5(b).hexdigest()


def html_to_text(html: str) -> str:
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "lxml")
    for t in soup(["script", "style", "noscript", "nav", "header", "footer"]):
        t.decompose()
    text = soup.get_text("\n")
    text = re.sub(r"[ \t\xa0]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text.strip() + "\n"


def pdf_to_text(b: bytes) -> str:
    import pdfplumber
    with pdfplumber.open(io.BytesIO(b)) as pdf:
        return "\n\f".join((p.extract_text() or "") for p in pdf.pages)


def main() -> None:
    session = requests.Session()
    session.headers["User-Agent"] = UA
    rows = []
    for url, rel in ITEMS:
        dest = RAW / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists() or (dest.suffix == "" and any(dest.parent.glob(dest.name + ".*"))):
            rows.append((url, rel, "", "", "exists"))
            print("exists ", rel)
            continue
        try:
            r = session.get(url, timeout=120, allow_redirects=True)
        except Exception as e:  # noqa: BLE001
            rows.append((url, rel, "", "", f"error {e}"))
            print("ERROR  ", rel, e)
            continue
        if r.status_code != 200:
            rows.append((url, rel, "", "", f"http {r.status_code}"))
            print("HTTP", r.status_code, rel)
            continue
        b = r.content
        ctype = r.headers.get("content-type", "")
        # resource-manager links have no extension: infer from content
        if dest.suffix == "":
            if b[:4] == b"%PDF":
                dest = dest.with_suffix(".pdf")
            elif b[:2] == b"PK":
                dest = dest.with_suffix(".xlsx")
            elif "html" in ctype:
                dest = dest.with_suffix(".html")
            else:
                dest = dest.with_suffix(".bin")
            rel = str(dest.relative_to(RAW)).replace("\\", "/")
        dest.write_bytes(b)
        status = "ok"
        try:
            if dest.suffix == ".pdf":
                dest.with_suffix(".txt").write_text(pdf_to_text(b), encoding="utf-8")
            elif dest.suffix == ".html":
                dest.with_suffix(".txt").write_text(html_to_text(b.decode("utf-8", "ignore")), encoding="utf-8")
        except Exception as e:  # noqa: BLE001
            status = f"ok (text extraction failed: {e})"
        rows.append((url, rel, md5(b), len(b), status))
        print(f"ok     {rel} {len(b):,}B {ctype}")
        time.sleep(0.5)
    new = not MANIFEST.exists()
    with MANIFEST.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["retrieved_utc", "url", "path", "md5", "bytes", "status"])
        ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
        for row in rows:
            w.writerow([ts, *row])
    print("manifest:", MANIFEST)


if __name__ == "__main__":
    sys.exit(main())
