#!/usr/bin/env python3
"""Create a conservative, evidence-labeled fashion shortlist from EchoTik rankings."""
import json
import re
from maya_affiliate_status import eligible_status
from pathlib import Path

SOURCE = Path("data/echotik-product-rankings.json")
OUTPUT = Path("data/maya-echotik-fashion-shortlist.md")
record = json.loads(SOURCE.read_text(encoding="utf-8"))
products = record.get("data", {}).get("data", [])
if not isinstance(products, list):
    raise SystemExit("Unexpected EchoTik response: no product list")
fashion = re.compile(r"\b(leggings?|jeans|pants|trousers|sweaters?|jackets?|shoes?|sneakers?|handbags?|purses?|cardigans?|hoodies?|dresses?|skirts?|blouses?|clogs?|sandals?|socks?|boots?|coats?|knitwear|matching set)\b", re.I)
exclude = re.compile(r"\b(supplements?|magnesium|vitamins?|serum|shampoo|body wash|bras?|bodysuits?|faja|shapewear|cosmetics?|skincare)\b", re.I)

EVIDENCE = Path("data/echotik-competition-evidence.json")
evidence = json.loads(EVIDENCE.read_text()) if EVIDENCE.exists() else {"status": "missing", "products": {}}

CREATOR_EVIDENCE = Path("data/echotik-creator-competition.json")
creator_evidence = json.loads(CREATOR_EVIDENCE.read_text()) if CREATOR_EVIDENCE.exists() else {"status": "missing", "products": {}}

ADVANCED = Path("data/echotik-advanced-signals.json")
advanced = json.loads(ADVANCED.read_text()) if ADVANCED.exists() else {"status": "missing", "products": {}}
AFFILIATE = Path("data/maya-affiliate-verifications.json")
affiliate = json.loads(AFFILIATE.read_text()) if AFFILIATE.exists() else {"products": {}}

LISTINGS = Path("data/echotik-listing-overlap.json")
listings = json.loads(LISTINGS.read_text()) if LISTINGS.exists() else {"products": {}}

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
    "and TikTok Shop eligibility are unverified. Low video count does NOT prove low competition.",
    f"Detail enrichment status: {evidence.get('status', 'missing')}; verified creator/listing saturation: UNKNOWN.", "",
]
for i, p in enumerate(matches[:10], 1):
    price = float(p.get("spu_avg_price") or 0)
    rate = float(p.get("product_commission_rate") or 0)
    detail = evidence.get("products", {}).get(str(p.get("product_id")), {})
    creator = creator_evidence.get("products", {}).get(str(p.get("product_id")), {})
    signal = advanced.get("products", {}).get(str(p.get("product_id")), {})
    videos = signal.get("video_sample", {})
    trend = signal.get("trend", {})
    eligible = affiliate.get("products", {}).get(str(p.get("product_id")), {})
    listing = listings.get("products", {}).get(str(p.get("product_id")), {})
    affiliate_status = eligible_status(eligible, str(p.get("product_id")))
    recent_sales = detail.get("total_sale_30d_cnt")
    weekly_sales = detail.get("total_sale_7d_cnt")
    weekly_rate = round(weekly_sales / (recent_sales / 30 * 7), 2) if isinstance(weekly_sales, (int, float)) and isinstance(recent_sales, (int, float)) and recent_sales > 0 else None
    recent_videos = detail.get("total_video_30d_cnt")
    creator_videos = detail.get("total_ifl_video_30d_cnt")
    lines.extend([
        f"## {i}. {p.get('product_name', 'Unnamed product')}", 
        f"- EchoTik product ID: {p.get('product_id', 'unknown')}",
        f"- Preliminary evidence score: {rank_score(p)}/50 (demand and payout proxies only; not a final recommendation)",
        f"- Reported sales: {p.get('total_sale_cnt', 'unknown')} | reported videos: {p.get('total_video_cnt', 'unknown')}",
        f"- Average price: ${price:.2f} | reported commission: {rate*100:.1f}% | estimated payout: ${price*rate:.2f} (not guaranteed)",
        f"- EchoTik 7d sales: {weekly_sales if weekly_sales is not None else 'UNKNOWN'} | 30d sales: {recent_sales if recent_sales is not None else 'UNKNOWN'} | 7d-vs-30d daily pace ratio: {weekly_rate if weekly_rate is not None else 'UNKNOWN'} (not proof of sustained growth)",
        f"- EchoTik 30d videos: {recent_videos if recent_videos is not None else 'UNKNOWN'} | 30d influencer-linked videos: {creator_videos if creator_videos is not None else 'UNKNOWN'}",
        f"- Video-driven 30d sales: {detail.get('total_video_sale_30d_cnt', 'UNKNOWN')} | Live-driven 30d sales: {detail.get('total_live_sale_30d_cnt', 'UNKNOWN')}",
        f"- Product rating: {detail.get('product_rating', 'UNKNOWN')} | reviews: {detail.get('review_count', 'UNKNOWN')} | free shipping flag: {detail.get('free_shipping', 'UNKNOWN')}",
        f"- Associated creators observed: {creator.get('unique_associated_creators_observed') if creator.get('unique_associated_creators_observed') is not None else 'UNKNOWN'} (sample; pages: {creator.get('pages_sampled', 0)}, exhausted: {creator.get('pagination_exhausted', False)})",
        f"- Total associated creators: {creator.get('total_associated_creators') if creator.get('total_associated_creators') is not None else 'UNKNOWN'} (only shown if pagination fully exhausted)",
        "- Unique ACTIVE creators last 30 days: UNKNOWN (creator activity window not established)",
        f"- Other broad-category listings within our 50-product ranking sample: {listing.get('other_listings_in_ranking_sample', 'UNKNOWN')} (NOT a marketplace competitor count)",
        "- Competing equivalent product listings marketwide: UNKNOWN (requires validated matching product search)",
        f"- Product-associated videos in 30d query sample: {videos.get('sample_size', 'UNKNOWN')} | unique sampled creators: {videos.get('unique_creators_in_sample', 'UNKNOWN')} | max sampled views: {videos.get('sample_views_max', 'UNKNOWN')}",
        f"- Trend snapshot days observed: {trend.get('sampled_days', 'UNKNOWN')} | sales in sampled days: {trend.get('reported_daily_sales_sample_sum', 'UNKNOWN')} (NOT a 30-day total)",
        f"- TikTok Shop affiliate eligibility for @maya._.finds: {affiliate_status} (account-specific, 48-hour freshness gate)",
        "- Growth trend: UNKNOWN until comparable period metrics or historical snapshots are validated",
        "- Status: CONDITIONAL RESEARCH LEAD, never auto-approved; verify exact listing, creator eligibility, commission, recent demand, competition and product fidelity", "",
    ])
if not matches:
    lines.append("No qualifying fashion leads in this sample. Do not invent candidates; broaden research using verified sources.")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Shortlisted {len(matches)} fashion products from {len(products)} sampled products")

