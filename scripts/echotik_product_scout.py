#!/usr/bin/env python3
"""EchoTik product ranking collector. No third-party dependencies."""
import base64
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

URL = "https://open.echotik.live/api/v3/echotik/product/ranklist"
OUTPUT = Path("data/echotik-product-rankings.json")

def main():
    username = os.environ.get("ECHOTIK_USERNAME", "")
    password = os.environ.get("ECHOTIK_PASSWORD", "")
    query = os.environ.get("ECHOTIK_QUERY_JSON", "")
    if not username or not password:
        sys.exit("Missing EchoTik credentials in GitHub Actions secrets.")
    if not query:
        yesterday = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=1)).date().isoformat()
        query = json.dumps({"date": yesterday, "region": "US", "rank_type": 1, "product_rank_field": 1, "page_num": 1, "page_size": 10})
    try:
        params = json.loads(query)
    except json.JSONDecodeError:
        sys.exit("Invalid ECHOTIK_QUERY_JSON; no API request made.")
    if not isinstance(params, dict) or not params:
        sys.exit("Nonempty JSON object of verified API query parameters required; no API request made.")
    if any(not isinstance(k, str) or isinstance(v, (dict, list)) for k, v in params.items()):
        sys.exit("Only scalar query parameters allowed; no API request made.")
    params["page_size"] = min(10, max(1, int(params.get("page_size", 10))))
    first_page = max(1, int(params.get("page_num", 1)))
    max_pages = min(5, max(1, int(os.environ.get("ECHOTIK_MAX_PAGES", "5"))))
    token = base64.b64encode((username + ":" + password).encode()).decode()
    products, seen, pages = [], set(), []
    for page in range(first_page, first_page + max_pages):
        page_params = dict(params, page_num=page)
        url = URL + "?" + urllib.parse.urlencode(page_params)
        req = urllib.request.Request(url, headers={"Authorization": "Basic " + token, "Accept": "application/json", "User-Agent": "MayaFindsResearch/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.load(response)
        except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError) as exc:
            if not pages:
                sys.exit("EchoTik request failed: " + str(exc))
            print("Pagination stopped after successful pages: " + str(exc), file=sys.stderr)
            break
        if not isinstance(data, dict) or data.get("code") != 0 or not isinstance(data.get("data"), list):
            if not pages:
                sys.exit("EchoTik returned an invalid first page.")
            break
        items = data["data"]
        pages.append({"page": page, "returned": len(items)})
        added = 0
        for item in items:
            if not isinstance(item, dict):
                continue
            key = str(item.get("product_id") or item.get("product_name") or "")
            if key and key not in seen:
                seen.add(key)
                products.append(item)
                added += 1
        if len(items) < params["page_size"] or added == 0:
            break
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    record = {"source": "EchoTik Product Ranking List", "endpoint": URL, "checked_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(), "query": params, "pages": pages, "unique_products": len(products), "data": {"code": 0, "data": products}}
    OUTPUT.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    print("Saved", len(products), "unique products from", len(pages), "pages")

if __name__ == "__main__":
    main()
