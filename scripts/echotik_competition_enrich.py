#!/usr/bin/env python3
"""Enrich top EchoTik fashion leads with documented product-detail fields.

One batch request, max ten IDs. Unknown metrics remain unknown on API failure.
"""
import base64
import datetime as dt
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path("data")
raw = json.loads((ROOT / "echotik-product-rankings.json").read_text())
items = raw.get("data", {}).get("data", [])
fashion = re.compile(r"\b(leggings?|jeans|pants|trousers|sweaters?|jackets?|shoes?|sneakers?|handbags?|purses?|cardigans?|hoodies?|dresses?|skirts?|blouses?|clogs?|sandals?|socks?|boots?|coats?|knitwear|matching set)\b", re.I)
exclude = re.compile(r"\b(supplements?|magnesium|vitamins?|serum|shampoo|body wash|bras?|bodysuits?|faja|shapewear|cosmetics?|skincare)\b", re.I)
candidates = [p for p in items if fashion.search(str(p.get("product_name", ""))) and not exclude.search(str(p.get("product_name", ""))) and float(p.get("product_commission_rate") or 0) > 0]
candidates.sort(key=lambda p: float(p.get("total_sale_cnt") or 0), reverse=True)
ids = [str(p["product_id"]) for p in candidates[:10] if p.get("product_id")]
out = {"checked_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(), "source": "EchoTik product/detail (offline T+1, not live)", "requested_product_ids": ids, "status": "unavailable", "products": {}, "errors": []}
if ids:
    user, password = os.environ.get("ECHOTIK_USERNAME", ""), os.environ.get("ECHOTIK_PASSWORD", "")
    if user and password:
        url = "https://open.echotik.live/api/v3/echotik/product/detail?" + urllib.parse.urlencode({"product_ids": ",".join(ids)})
        token = base64.b64encode((user + ":" + password).encode()).decode()
        request = urllib.request.Request(url, headers={"Authorization": "Basic " + token, "Accept": "application/json", "User-Agent": "MayaFindsResearch/1.0"})
        try:
            with urllib.request.urlopen(request, timeout=35) as response:
                result = json.load(response)
            if result.get("code") != 0 or not isinstance(result.get("data"), list):
                raise ValueError("Invalid detail response")
            for p in result["data"]:
                pid = str(p.get("product_id", ""))
                if pid not in ids:
                    continue
                fields = ["total_sale_7d_cnt", "total_sale_30d_cnt", "total_video_7d_cnt", "total_video_30d_cnt", "total_ifl_video_7d_cnt", "total_ifl_video_30d_cnt", "total_ifl_cnt", "product_rating", "review_count", "total_sale_cnt"]
                out["products"][pid] = {k: p[k] for k in fields if k in p and p[k] is not None}
            out["status"] = "partial" if len(out["products"]) < len(ids) else "complete"
        except (urllib.error.HTTPError, urllib.error.URLError, ValueError, json.JSONDecodeError) as exc:
            out["errors"].append(type(exc).__name__ + ": detail endpoint unavailable; metrics UNKNOWN")
    else:
        out["errors"].append("Missing EchoTik credentials; metrics UNKNOWN")
else:
    out["status"] = "no_fashion_candidates"
(ROOT / "echotik-competition-evidence.json").write_text(json.dumps(out, indent=2) + "\n")
print("Detail enrichment:", out["status"], len(out["products"]), "of", len(ids))
