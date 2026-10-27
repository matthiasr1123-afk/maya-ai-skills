#!/usr/bin/env python3
"""Sample EchoTik product-associated creators; never mislabel a sample as total active creators."""
import base64
import datetime as dt
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

root = Path("data")
detail_path = root / "echotik-competition-evidence.json"
detail = json.loads(detail_path.read_text()) if detail_path.exists() else {}
ids = detail.get("requested_product_ids", [])[:5]
out = {"checked_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
       "source": "EchoTik product/influencer/list, offline T+1",
       "coverage": "up to 3 pages of 10 creators per product, top 5 candidates",
       "products": {}, "status": "unavailable"}
user, password = os.environ.get("ECHOTIK_USERNAME", ""), os.environ.get("ECHOTIK_PASSWORD", "")
if ids and user and password:
    auth = base64.b64encode((user + ":" + password).encode()).decode()
    for pid in ids:
        seen = set()
        pages = 0
        error = None
        complete = False
        for page in range(1, 4):
            url = "https://open.echotik.live/api/v3/echotik/product/influencer/list?" + urllib.parse.urlencode(
                {"product_id": pid, "page_num": page, "page_size": 10})
            req = urllib.request.Request(url, headers={"Authorization": "Basic " + auth, "Accept": "application/json"})
            try:
                with urllib.request.urlopen(req, timeout=20) as response:
                    data = json.load(response)
                if not isinstance(data, dict) or data.get("code") != 0 or not isinstance(data.get("data"), list):
                    raise ValueError("Invalid API response")
                rows = data["data"]
                pages += 1
                for creator in rows:
                    if isinstance(creator, dict) and creator.get("user_id"):
                        seen.add(str(creator["user_id"]))
                if len(rows) < 10:
                    complete = True
                    break
            except (urllib.error.HTTPError, urllib.error.URLError, ValueError, json.JSONDecodeError) as exc:
                error = type(exc).__name__
                break
        out["products"][pid] = {
            "unique_associated_creators_observed": len(seen) if pages else None,
            "pages_sampled": pages,
            "pagination_exhausted": complete,
            "total_associated_creators": len(seen) if complete and not error else None,
            "unique_active_creators_last_30d": None,
            "active_creator_status": "UNKNOWN: creator list has no verified last-30-day activity window",
            "competing_listings_count": None,
            "competing_listings_status": "UNKNOWN: no verified equivalent-product matching dataset",
            "current_affiliate_eligibility": "UNVERIFIED: requires connected TikTok Shop creator account",
            "error": error
        }
    out["status"] = "partial" if any(x["error"] for x in out["products"].values()) else "sampled"
elif not ids:
    out["status"] = "no_candidates"
(root / "echotik-creator-competition.json").write_text(json.dumps(out, indent=2) + "\n")
print("Creator competition evidence:", out["status"], len(out["products"]))
