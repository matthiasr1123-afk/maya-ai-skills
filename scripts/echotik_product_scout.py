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
        sys.exit("ECHOTIK_QUERY_JSON is required; no API request made.")
    try:
        params = json.loads(query)
    except json.JSONDecodeError:
        sys.exit("Invalid ECHOTIK_QUERY_JSON; no API request made.")
    if not isinstance(params, dict) or not params:
        sys.exit("Nonempty JSON object of verified API query parameters required; no API request made.")
    if any(not isinstance(k, str) or isinstance(v, (dict, list)) for k, v in params.items()):
        sys.exit("Only scalar query parameters allowed; no API request made.")
    url = URL + "?" + urllib.parse.urlencode(params)
    token = base64.b64encode((username + ":" + password).encode()).decode()
    req = urllib.request.Request(url, headers={"Authorization": "Basic " + token, "Accept": "application/json", "User-Agent": "MayaFindsResearch/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.load(response)
    except urllib.error.HTTPError as exc:
        body = exc.read(2048).decode("utf-8", errors="replace")
        sys.exit("EchoTik HTTP " + str(exc.code) + " response: " + body)
    except (urllib.error.URLError, json.JSONDecodeError) as exc:
        sys.exit("EchoTik request failed: " + str(exc))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    record = {"source": "EchoTik Product Ranking List", "endpoint": URL, "checked_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(), "query": params, "data": data}
    OUTPUT.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    print("Saved EchoTik ranking response to " + str(OUTPUT))

if __name__ == "__main__":
    main()
