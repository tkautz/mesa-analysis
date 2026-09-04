"""Build MANIFEST.csv for data/raw/press, data/raw/bvsd/budget, data/raw/bvsd/policy, data/raw/bvsd/web
from the JSONL records written by fetch_public_docs.py (data/raw/_fetch_records.jsonl).

Columns: file, url, publisher, title, date, retrieved_utc, md5, notes
- one row per saved primary file (.html/.pdf/.xlsx/.json); the sibling .txt is named in notes
- date: from the job if given, else parsed from the saved HTML (article:published_time / datePublished / og date)
- md5 is recomputed from the file on disk (so the manifest matches what is in the folder)
"""
import csv, json, hashlib, pathlib, re, collections

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
RECORDS = RAW / "_fetch_records.jsonl"
FOLDERS = ["press", "bvsd/budget", "bvsd/policy", "bvsd/web"]


def md5_file(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def date_from_html(p):
    try:
        h = p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""
    pats = [r'property="article:published_time"\s+content="([^"]+)"',
            r'content="([^"]+)"\s+property="article:published_time"',
            r'"datePublished"\s*:\s*"([^"]+)"',
            r'name="parsely-pub-date"\s+content="([^"]+)"',
            r'name="pubdate"\s+content="([^"]+)"',
            r'post date (\d{4}-\d{2}-\d{2})']
    for pat in pats:
        m = re.search(pat, h)
        if m:
            return m.group(1)[:10]
    return ""


def main():
    recs = collections.OrderedDict()
    for line in RECORDS.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        recs[r["file"]] = r  # last record for a file wins
    rows_by_folder = {f: [] for f in FOLDERS}
    for rel, r in recs.items():
        p = RAW / rel
        if not p.exists():
            continue
        folder = next((f for f in FOLDERS if rel.startswith(f + "/")), None)
        if folder is None:
            continue
        date = r.get("date") or (date_from_html(p) if p.suffix == ".html" else "")
        notes = r.get("notes", "")
        if r.get("txt"):
            notes = (notes + "; " if notes else "") + "text: " + pathlib.Path(r["txt"]).name
        if r.get("final_url") and r["final_url"] != r["url"]:
            notes += "; retrieved from " + r["final_url"]
        rows_by_folder[folder].append({
            "file": p.name, "url": r["url"], "publisher": r.get("publisher", ""),
            "title": (r.get("title") or "").replace("\n", " ").strip(), "date": date,
            "retrieved_utc": r.get("retrieved_utc", ""), "md5": md5_file(p), "notes": notes})
    for folder, rows in rows_by_folder.items():
        rows.sort(key=lambda x: x["file"])
        out = RAW / folder / "MANIFEST.csv"
        with open(out, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["file", "url", "publisher", "title", "date", "retrieved_utc", "md5", "notes"])
            w.writeheader()
            w.writerows(rows)
        print(f"{out.relative_to(ROOT)}: {len(rows)} rows")


if __name__ == "__main__":
    main()
