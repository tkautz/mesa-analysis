"""Fetch public web pages / PDFs into data/raw/{press,bvsd/budget,bvsd/policy,bvsd/web}.

Usage: python scripts/fetch_public_docs.py jobs.json [--force]
jobs.json: list of {url, out (path under data/raw, no extension), publisher, title, date, notes}

Saves .html (raw bytes) + .txt (article-body text) for HTML pages, or .pdf + .txt (pdfplumber) for PDFs.
Appends one JSON record per saved file to data/raw/_fetch_records.jsonl; build_manifests.py turns those
into the per-folder MANIFEST.csv files. Never overwrites an existing file unless --force.
Browser User-Agent per the task brief.
"""
import sys, json, hashlib, re, datetime, pathlib, io
import requests
from bs4 import BeautifulSoup

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
HDRS = {"User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/pdf,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9"}
RECORDS = RAW / "_fetch_records.jsonl"


def md5(b):
    return hashlib.md5(b).hexdigest()


def html_to_text(html_bytes):
    soup = BeautifulSoup(html_bytes, "html.parser")
    for t in soup(["script", "style", "noscript", "svg", "iframe", "form", "nav", "footer", "header", "aside"]):
        t.decompose()
    title = soup.title.get_text(strip=True) if soup.title else ""
    node = None
    for sel in ["article", "main", "[role=main]", ".entry-content", ".post-content", ".article-body",
                ".fsPageContent", "#fsPageContent", ".fsBody", "body"]:
        node = soup.select_one(sel)
        if node is not None and len(node.get_text(strip=True)) > 400:
            break
    if node is None:
        node = soup
    text = node.get_text("\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text).strip()
    return title, text


def pdf_to_text(pdf_bytes):
    import pdfplumber
    out = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for i, p in enumerate(pdf.pages, 1):
            out.append(f"\n===== page {i} =====\n")
            out.append(p.extract_text() or "")
    return "".join(out)


def fetch(job, force=False):
    url = job["url"]
    out = RAW / job["out"]
    out.parent.mkdir(parents=True, exist_ok=True)
    try:
        r = requests.get(url, headers=HDRS, timeout=90, allow_redirects=True)
    except Exception as e:
        return {"url": url, "status": "error", "error": str(e)}
    ctype = r.headers.get("Content-Type", "")
    body = r.content
    is_pdf = "pdf" in ctype.lower() or body[:5] == b"%PDF-"
    if r.status_code != 200:
        return {"url": url, "status": r.status_code, "final_url": r.url, "ctype": ctype, "len": len(body)}
    is_xlsx = "spreadsheetml" in ctype.lower() or body[:2] == b"PK" and job.get("out", "").endswith("xlsx")
    ext = ".pdf" if is_pdf else (".xlsx" if is_xlsx else ".html")
    main_path = out.with_suffix(ext)
    txt_path = out.with_suffix(".txt")
    if main_path.exists() and not force:
        return {"url": url, "status": "exists", "file": str(main_path)}
    main_path.write_bytes(body)
    title = job.get("title", "")
    try:
        if is_pdf:
            text = pdf_to_text(body)
        elif is_xlsx:
            import openpyxl
            wb = openpyxl.load_workbook(io.BytesIO(body), read_only=True, data_only=True)
            parts = []
            for ws in wb.worksheets:
                parts.append(f"\n===== sheet {ws.title} =====\n")
                for k, row in enumerate(ws.iter_rows(values_only=True)):
                    if k >= 40:
                        parts.append("... (truncated; see the .xlsx)\n"); break
                    parts.append("\t".join("" if v is None else str(v) for v in row) + "\n")
            text = "".join(parts)
        else:
            t, text = html_to_text(body)
            title = title or t
    except Exception as e:
        text = f"[extraction failed: {e}]"
    txt_path.write_text(text, encoding="utf-8")
    rel = lambda p: str(p.relative_to(RAW)).replace("\\", "/")
    rec = {"file": rel(main_path), "txt": rel(txt_path), "url": url, "final_url": r.url,
           "publisher": job.get("publisher", ""), "title": title, "date": job.get("date", ""),
           "retrieved_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "md5": md5(body), "bytes": len(body), "ctype": ctype, "notes": job.get("notes", ""),
           "text_chars": len(text)}
    with open(RECORDS, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")
    return {"url": url, "status": 200, "file": rec["file"], "bytes": len(body),
            "text_chars": len(text), "title": title[:90]}


if __name__ == "__main__":
    force = "--force" in sys.argv
    jobs_path = [a for a in sys.argv[1:] if a != "--force"][0]
    jobs = json.load(open(jobs_path, encoding="utf-8"))
    import time
    for j in jobs:
        print(json.dumps(fetch(j, force)), flush=True)
        time.sleep(float(j.get("sleep", 2.5)))  # be polite; BRL returns 429 on rapid requests
