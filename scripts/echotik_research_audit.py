#!/usr/bin/env python3
"""Machine-readable research health, coverage, data freshness, and review gates."""
import datetime as dt
import json
from maya_affiliate_status import eligible_status
from pathlib import Path
p = Path("data")
names = ["echotik-product-rankings.json", "echotik-competition-evidence.json",
         "echotik-creator-competition.json", "echotik-advanced-signals.json",
         "maya-affiliate-verifications.json"]
files = {}
for name in names:
    try:
        files[name] = json.loads((p / name).read_text())
    except (OSError, ValueError):
        files[name] = {}
ranking = files[names[0]]
items = ranking.get("data", {}).get("data", [])
ids = {str(x.get("product_id")) for x in items if isinstance(x, dict) and x.get("product_id")}
now = dt.datetime.now(dt.timezone.utc)
try:
    stamp = dt.datetime.fromisoformat(ranking["checked_at_utc"].replace("Z", "+00:00"))
    fresh = stamp.tzinfo is not None and dt.timedelta(0) <= now-stamp < dt.timedelta(hours=30)
except (KeyError, ValueError, TypeError):
    fresh = False
detail = files[names[1]]
creators = files[names[2]]
signals = files[names[3]]
audit = {
    "checked_at_utc": now.isoformat(),
    "ranking_fresh_under_30h": fresh,
    "ranking_products": len(ids),
    "ranking_pages": len(ranking.get("pages", [])),
    "detail_status": detail.get("status", "missing"),
    "detail_products": len(detail.get("products", {})),
    "creator_status": creators.get("status", "missing"),
    "creator_products": len(creators.get("products", {})),
    "advanced_status": signals.get("status", "missing"),
    "advanced_products": len(signals.get("products", {})),
    "advanced_api_requests": signals.get("api_requests_attempted", 0),
    "affiliate_verified_product_count": sum(1 for pid, v in files[names[4]].get("products", {}).items() if eligible_status(v, pid, now) == "ELIGIBLE"),
    "unique_active_creator_count_verified": False,
    "equivalent_competing_listing_count_verified": False,
    "automated_approval_enabled": False,
    "issues": []
}
if audit["affiliate_verified_product_count"] == 0:
    audit["issues"].append("Creator-specific affiliate verification unavailable: no fresh verified eligible products")
if not fresh: audit["issues"].append("Ranking stale or missing")
if len(ids) < 10: audit["issues"].append("Ranking sample below 10 products")
for key in ("detail_status", "creator_status", "advanced_status"):
    if audit[key] in ("unavailable", "missing", "partial"):
        audit["issues"].append(key + ": " + audit[key])
(p / "maya-product-scout-audit.json").write_text(json.dumps(audit, indent=2) + "\n")
summary = [
    "# Maya Finds — Product Research Health", "",
    "Checked (UTC): " + audit["checked_at_utc"], "",
    "- Ranking fresh: " + str(fresh),
    "- Ranked products: " + str(len(ids)),
    "- Detail enrichment: " + audit["detail_status"],
    "- Creator sampling: " + audit["creator_status"],
    "- Trends and video sampling: " + audit["advanced_status"],
    "- Verified unique active creator totals: NO",
    "- Verified equivalent competing listings: NO",
    "- Creator-specific affiliate eligibility: separate manual/authorized source required",
    "- Auto-approve products: DISABLED", "",
    "## Problems requiring attention"
] + (["- " + x for x in audit["issues"]] if audit["issues"] else ["- None detected in covered checks. Unverified gates still apply."])
(p / "maya-product-scout-health.md").write_text("\n".join(summary) + "\n")
print("Audit complete:", len(audit["issues"]), "issues")

