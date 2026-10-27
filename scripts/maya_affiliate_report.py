#!/usr/bin/env python3
"""Refresh five-product verification queue and HQ. Never simulates live checks."""
import datetime as dt
import json
import re
from pathlib import Path
from maya_affiliate_status import ACCOUNT, evaluate

def main():
    root = Path("data")
    target = root / "maya-affiliate-verifications.json"
    saved = json.loads(target.read_text()) if target.exists() else {"products": {}}
    records = saved.setdefault("products", {})
    shortlist = (root / "maya-echotik-fashion-shortlist.md").read_text()
    candidates = re.findall(r"^## \d+\. (.+)\n- EchoTik product ID: (\d+)$", shortlist, re.M)[:5]
    now = dt.datetime.now(dt.timezone.utc)
    queue = []
    for name, pid in candidates:
        if pid not in records:
            records[pid] = {
                "product_id": pid, "product_name": name, "account": ACCOUNT, "region": "US",
                "verification_status": "UNAVAILABLE", "eligibility": "UNVERIFIED",
                "source_type": None, "source": None, "checked_at_utc": None,
                "commission_rate": None, "price": None, "availability": "UNKNOWN",
                "availability_scope": None, "add_to_showcase_status": "UNKNOWN",
                "reason": "Creator account evidence unavailable; EchoTik is research only",
                "evidence": {},
            }
        status, reason = evaluate(records[pid], pid, now)
        queue.append({"product_id": pid, "product_name": name,
                      "verification_status": status, "reason": reason,
                      "checked_at_utc": records[pid].get("checked_at_utc")})
    saved.update(schema_version=2, account=ACCOUNT, region="US", report_generated_at_utc=now.isoformat(),
                 freshness_hours=48, current_candidate_ids=[pid for _, pid in candidates])
    saved.pop("example_fields_not_a_real_record", None)
    target.write_text(json.dumps(saved, indent=2) + "\n")
    (root / "maya-affiliate-verification-queue.json").write_text(json.dumps({
        "generated_at_utc": now.isoformat(), "account": ACCOUNT,
        "live_account_fetch_performed": False, "candidates": queue}, indent=2) + "\n")
    counts = {s: sum(x["verification_status"] == s for x in queue)
              for s in ("VERIFIED", "PARTIALLY VERIFIED", "UNAVAILABLE")}
    lines = ["## Affiliate verification dashboard", "",
             "Report generated (UTC): " + now.isoformat(), "",
             "Account: " + ACCOUNT + ". These are snapshots, not a guarantee at posting time.", "",
             f"Current candidates: {len(queue)} | VERIFIED: {counts['VERIFIED']} | PARTIALLY VERIFIED: {counts['PARTIALLY VERIFIED']} | UNAVAILABLE: {counts['UNAVAILABLE']}", "",
             "| Candidate | Product ID | Verification |", "|---|---|---|"]
    lines += [f"| {x['product_name'].replace('|', '/')} | {x['product_id']} | {x['verification_status']} |" for x in queue]
    lines += ["", "- Automatic: queue refresh, 48-hour expiry, account/product/source validation, shortlist and HQ reporting.",
              "- Live TikTok account checks: UNAVAILABLE until a permitted signed-in creator surface or approved Creator API integration is tested.",
              "- No product is eligible because it appears in search. No showcase changes are performed.",
              "- Next: establish creator account access; inspect exact five IDs and record observed fields. For unattended checks, obtain approved Creator API access and creator OAuth authorization.",
              "- Evidence: [verification records](data/maya-affiliate-verifications.json); [queue](data/maya-affiliate-verification-queue.json); [integration findings](docs/maya-affiliate-integration.md)."]
    dashboard = "\n".join(lines) + "\n"
    (root / "maya-affiliate-dashboard.md").write_text(dashboard)
    hq = Path("MAYA-FINDS-HQ.md")
    begin, end = "<!-- MAYA_AFFILIATE_START -->", "<!-- MAYA_AFFILIATE_END -->"
    block = begin + "\n" + dashboard + end
    text = hq.read_text()
    if begin in text and end in text:
        text = text[:text.index(begin)] + block + text[text.index(end) + len(end):]
    else:
        text = text.replace("## Latest verified HQ sync", block + "\n\n## Latest verified HQ sync", 1)
    hq.write_text(text)
    print("Affiliate report:", counts, "live account fetch: False")

if __name__ == "__main__":
    main()
