#!/usr/bin/env python3
"""Bounded evidence enrichment: product trends and recent associated videos.

No inferred creator activity, competitor counts, or affiliate approval.
All external metrics retain source/coverage information.
"""
import base64
import datetime as dt
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

root = Path("data")
rank = json.loads((root / "echotik-product-rankings.json").read_text())
creator_file = root / "echotik-creator-competition.json"
creator = json.loads(creator_file.read_text()) if creator_file.exists() else {}
ids = list(creator.get("products", {}))[:5]
now = dt.datetime.now(dt.timezone.utc)
start = (now - dt.timedelta(days=31)).date().isoformat()
end = (now - dt.timedelta(days=1)).date().isoformat()
out = {"checked_at_utc": now.isoformat(), "source": "EchoTik offline T+1", "products": {},
       "status": "unavailable", "api_requests_attempted": 0, "request_budget": 10}
user, password = os.environ.get("ECHOTIK_USERNAME", ""), os.environ.get("ECHOTIK_PASSWORD", "")
auth = base64.b64encode((user + ":" + password).encode()).decode() if user and password else ""
def fetch(endpoint, params):
    out["api_requests_attempted"] += 1
    url = "https://open.echotik.live/api/v3/echotik/" + endpoint + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": "Basic " + auth, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            result = json.load(response)
        if isinstance(result, dict) and result.get("code") == 0 and isinstance(result.get("data"), list):
            return result["data"], None
        return None, "invalid_response"
    except (urllib.error.HTTPError, urllib.error.URLError, ValueError, json.JSONDecodeError) as exc:
        return None, type(exc).__name__
if auth:
    for pid in ids:
        entry = {"product_id": pid, "trend": {}, "video_sample": {}, "errors": []}
        rows, error = fetch("product/trend", {"product_id": pid, "start_date": start, "end_date": end, "page_num": 1, "page_size": 10})
        if error:
            entry["errors"].append("trend:" + error)
        elif rows:
            dates = sorted((r for r in rows if isinstance(r, dict) and r.get("dt")), key=lambda x: str(x["dt"]))
            entry["trend"] = {"sampled_days": len(dates), "first_date": dates[0]["dt"] if dates else None,
                "last_date": dates[-1]["dt"] if dates else None,
                "reported_daily_sales_sample_sum": sum(float(r.get("total_sale_1d_cnt") or 0) for r in dates),
                "complete_30_day_window": False,
                "note": "At most 10 daily snapshots fetched; do not label sample sum as 30-day sales"}
        rows, error = fetch("product/video/list", {"product_id": pid, "min_create_time": int((now-dt.timedelta(days=30)).timestamp()),
                 "max_create_time": int(now.timestamp()), "page_num": 1, "page_size": 10})
        if error:
            entry["errors"].append("video:" + error)
        elif rows is not None:
            unique = {str(r.get("user_id")) for r in rows if isinstance(r, dict) and r.get("user_id")}
            views = [float(r.get("total_views_cnt") or 0) for r in rows if isinstance(r, dict)]
            entry["video_sample"] = {"sample_size": len(rows), "unique_creators_in_sample": len(unique),
                "sample_views_max": max(views) if views else None,
                "sample_views_median": sorted(views)[len(views)//2] if views else None,
                "sample_is_complete": len(rows) < 10,
                "unique_active_creators_30d": None,
                "note": "Sampled creators only; full 30-day creator count unverified without pagination and confirmed date filtering"}
        out["products"][pid] = entry
    out["status"] = "partial" if any(v["errors"] for v in out["products"].values()) else "sampled"
elif not ids:
    out["status"] = "no_candidates"
(root / "echotik-advanced-signals.json").write_text(json.dumps(out, indent=2) + "\n")
print("Advanced signal enrichment:", out["status"], out["api_requests_attempted"], "requests")
