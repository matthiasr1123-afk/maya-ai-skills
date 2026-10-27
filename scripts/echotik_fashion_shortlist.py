#!/usr/bin/env python3
"""Produce a conservative fashion-only shortlist from the latest saved EchoTik response."""
import json
import re
from pathlib import Path
source = json.loads(Path("data/echotik-product-rankings.json").read_text())
products = source["data"]["data"]
fashion = re.compile(r"\\b(legging|leggings|jeans|pants|sweater|jacket|shoes|sneakers|handbag|purse|cardigan|hoodie|dress|skirt|blouse|clogs|sandals|socks)\\b", re.I)
exclude = re.compile(r"\\b(supplement|magnesium|vitamin|serum|shampoo|body wash|bra|bodysuit|faja|shapewear)\\b", re.I)
matches = [p for p in products if fashion.search(p.get("product_name", "")) and not exclude.search(p.get("product_name", "")) and (p.get("product_commission_rate") or 0)>0]
lines = ["# Maya Finds — EchoTik Fashion Research Shortlist", "", "Snapshot date: " + str(source["query"]["date"]), "", "EchoTik-reported sales and video counts. Their reporting periods and creator competition are not independently verified. Verify exact TikTok Shop listing, affiliate eligibility and current commission before making videos.", ""]
for p in matches:
    price = p.get("spu_avg_price", 0)
    rate = p.get("product_commission_rate", 0)
    lines.extend(["## " + p["product_name"], "- Product ID: " + str(p["product_id"]), "- Reported sales: " + str(p.get("total_sale_cnt")) + " | videos: " + str(p.get("total_video_cnt")), "- Average price: $" + str(price) + " | Commission: " + str(round(rate*100,1)) + "% | Estimated payout: $" + str(round(price*rate,2)), "- Status: RESEARCH LEAD (not yet approved for posting)", ""])
if not matches:
    lines.append("No qualifying fashion leads in the 10-product general ranking sample. Do not force a recommendation.")
Path("data/maya-echotik-fashion-shortlist.md").write_text("\\n".join(lines) + "\\n")
print("Shortlisted", len(matches), "fashion products")
