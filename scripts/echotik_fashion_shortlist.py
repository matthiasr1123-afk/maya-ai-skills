#!/usr/bin/env python3
"""Create a conservative, evidence-labeled fashion shortlist from EchoTik rankings."""
import json
import re
from pathlib import Path

SOURCE = Path("data/echotik-product-rankings.json")
OUTPUT = Path("data/maya-echotik-fashion-shortlist.md")
record = json.loads(SOURCE.read_text(encoding="utf-8"))
products = record.get("data", {}).get("data", [])
if not isinstance(products, list):
    raise SystemExit("Unexpected EchoTik response: no product list")
fashion = re.compile(r"\b(leggings?|jeans|pants|trousers|sweaters?|jackets?|shoes?|sneakers?|handbags?|purses?|cardigans?|hoodies?|dresses?|skirts?|blouses?|clogs?|sandals?|socks?|boots?|coats?|knitwear|matching set)\b", re.I)
exclude = re.compile(r"\b(supplements?|magnesium|vitamins?|serum|shampoo|body wash|bras?|bodysuits?|faja|shapewear|cosmetics?|skincare)\b", re.I)

matches = []
for product in products:
    name = str(product.get("product_name") or "")
    rate = float(product.get("product_commission_rate") or 0)
    if fashion.search(name) and not exclude.search(name) and rate > 0:
        matches.append(product)
def number(value):
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0

def rank_score(p):
    # Evidence-based proxy only. Competition remains unknown without unique creator counts.
    sales = max(0, number(p.get("total_sale_cnt")))
    rate = max(0, number(p.get("product_commission_rate")))
    price = max(0, number(p.get("spu_avg_price")))
    import math
    return round(30 * min(1, math.log1p(sales) / math.log1p(10000)) +
                 20 * min(1, price * rate / 8), 1)

matches.sort(key=lambda p: (rank_score(p), number(p.get("total_sale_cnt"))), reverse=True)

lines = [
    "# Maya Finds — EchoTik Fashion Research Shortlist", "",
    f"Source snapshot date: {record.get('query', {}).get('date', 'unknown')}",
    f"Collected at (UTC): {record.get('checked_at_utc', 'unknown')}",
    f"Sample: {len(products)} unique products across {len(record.get('pages', [1]))} pages; fashion leads: {len(matches)}.", "",
    "EchoTik-reported counts and rates are research leads, not verified live affiliate offers. ",
    "Sales/video reporting windows, creator saturation, recent velocity, product listing URLs, ",
    "and TikTok Shop eligibility are unverified. Low video count does NOT prove low competition.", "",
]
for i, p in enumerate(matches[:10], 1):
    price = float(p.get("spu_avg_price") or 0)
    rate = float(p.get("product_commission_rate") or 0)
    lines.extend([
        f"## {i}. {p.get('product_name', 'Unnamed product')}", 
        f"- EchoTik product ID: {p.get('product_id', 'unknown')}",\n        f"- Preliminary evidence score: {rank_score(p)}/50 (demand and payout proxies only; not a final recommendation)",
        f"- Reported sales: {p.get('total_sale_cnt', 'unknown')} | reported videos: {p.get('total_video_cnt', 'unknown')}",
        f"- Average price: ${price:.2f} | reported commission: {rate*100:.1f}% | estimated payout: ${price*rate:.2f} (not guaranteed)",
        "- Competition: UNKNOWN unless independent unique-creator and competing-listing counts are supplied. Reported videos alone cannot establish saturation.",\n        "- Recent growth: UNKNOWN unless comparable dated snapshots with matching measurement windows exist",
        "- Status: CONDITIONAL RESEARCH LEAD, never auto-approved; verify exact listing, creator eligibility, commission, recent demand, competition and product fidelity", "",
    ])
if not matches:
    lines.append("No qualifying fashion leads in this sample. Do not invent candidates; broaden research using verified sources.")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Shortlisted {len(matches)} fashion products from {len(products)} sampled products")
