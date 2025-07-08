# scripts/update_nvd.py

import os
import json
import requests
from dateutil import parser as dateparser
from sqlalchemy import insert
from cyberpulse.db import engine, init_db, cve_table

# NVD JSON feed URLs (modify years as needed)
NVD_FEED_URLS = [
    "https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-2023.json.gz",
    "https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-2022.json.gz",
    # Add more years here...
]

# Local cache directory for downloads
CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

def download_feed(url: str) -> str:
    """
    Downloads the gzipped JSON feed (if not already cached) and returns the local path.
    """
    filename = os.path.join(CACHE_DIR, os.path.basename(url))
    if not os.path.exists(filename):
        print(f"Downloading {url} …")
        resp = requests.get(url, stream=True)
        resp.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in resp.iter_content(1024):
                f.write(chunk)
    return filename

def load_and_unzip(path: str) -> dict:
    """
    Reads a .gz JSON file and returns the parsed JSON dict.
    """
    import gzip
    with gzip.open(path, "rt", encoding="utf-8") as f:
        return json.load(f)

def preprocess_cves(feed_data: dict) -> list:
    """
    Extracts CVE metadata records from the feed JSON.
    Returns a list of dicts matching our DB schema.
    """
    items = feed_data.get("CVE_Items", [])
    records = []
    for item in items:
        cve_id = item["cve"]["CVE_data_meta"]["ID"]
        # Published date
        pub_date = dateparser.parse(item.get("publishedDate"))
        # Summary
        summary = item["cve"]["description"]["description_data"][0]["value"]
        # References: join all URLs newline-separated
        refs = item["cve"]["references"]["reference_data"]
        ref_list = [r["url"] for r in refs]
        records.append({
            "cve_id": cve_id,
            "published_date": pub_date.date(),
            "summary": summary,
            "references": "\n".join(ref_list),
        })
    return records

def main():
    # 1. Initialize DB (creates tables)
    init_db()
    # 2. For each feed: download, parse, and upsert into DB
    with engine.begin() as conn:
        for url in NVD_FEED_URLS:
            gz_path = download_feed(url)
            data = load_and_unzip(gz_path)
            records = preprocess_cves(data)
            for rec in records:
                stmt = insert(cve_table).values(**rec).prefix_with("OR REPLACE")
                conn.execute(stmt)
            print(f"Imported {len(records)} CVEs from {url}")

if __name__ == "__main__":
    main()
