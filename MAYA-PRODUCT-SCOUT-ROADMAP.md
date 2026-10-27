# Maya Finds — Product Scout: capabilities, evidence gates and integrations

Updated 2026-10-27. Research only. No prompts or captions.

## Automated, implemented (requires live workflow test)
- US EchoTik ranking collector: five pages of ten products, deduplicated.
- Fashion candidate filter, preliminary demand/payout proxy, 10-product detail batch.
- EchoTik detail fields: 1d/7d/30d/60d sales, 7d/30d video volume, influencer video volume, video/live sales, reviews, rating, shipping, seller, product variants.
- Up to five products: three pages of ten associated creators each (15 API calls maximum). This is an association sample, not verified 30-day active creator count.
- Up to five products: 30-day-filtered video sample (10 per product) and 10 daily trend snapshots per product. Both are incomplete samples, not full-market counts.
- Freshness/coverage audit and a readable health report. API errors must remain visible as partial/unavailable, never interpreted as zero.
- Affiliate eligibility evidence registry, with 48-hour freshness check. No auto-approval without authorized account-specific proof.
- Daily AI Product Scout instructed to read all evidence and preserve UNKNOWN states.

## Not yet independently verifiable
1. **Unique active creators for the last 30 days.** Needs complete product/video pagination across the date range, distinct creator IDs, confirmed endpoint date filtering, and full EchoTik coverage. Current creator list shows associated creators, not verified recency.
2. **Equivalent competing product listings.** Needs a product/list or real-time product-search connector with product-category, region, material, silhouette, price and brand/variant matching. Keyword counts alone are not validated competitors. Add duplicate-cluster review and match confidence before reporting counts.
3. **Affiliate eligibility for @maya._.finds.** Requires authenticated creator-specific TikTok Shop Product Marketplace / authorized affiliate API or a fresh manual verified record. EchoTik commission is indicative, not creator-specific. Never store TikTok login cookies or credentials in repository files.
4. **Stock, shipping ETA, sample eligibility and creator-specific commission.** Same authorized creator-specific data needed; check per SKU/variant and US region.
5. **True audience retention, CTR and conversion of competitor videos.** Not public from EchoTik. Use own connected TikTok/Metricool analytics when available; do not infer from views.
6. **Exact visual product fidelity.** Requires original listing images, variants, materials, dimensions, and human/vision inspection; text keyword matching alone insufficient.
7. **Full 30-day velocity.** Detail endpoint gives windowed totals if subscribed; trend endpoint must paginate all daily snapshots to independently verify changes.
8. **Returns, cancellations, creator policy eligibility, and restricted product status.** Requires authoritative marketplace or seller data.

## Suggested next integrations
- Authorized TikTok Shop affiliate API / creator marketplace read access: current offer eligibility, commission, stock, variants, product URLs. May not be available to third-party developers.
- EchoTik product/list or product search: collect category-matched equivalent listings; verify endpoint access and query schema before enabling.
- EchoTik full product/video list pagination: exact observed unique creators by published date, subject to EchoTik data coverage.
- Own TikTok Shop analytics export or approved connector: views, 2-second retention, average watch time, completion, clicks and sales; use to learn which *product attributes* work, not claim creative format from views alone.
- A reviewed product-image comparison stage: exact color, pattern, silhouette, seams and variants.
- Product testing ledger: product ID, dates, impressions, retention, clicks, sales, failure reason, decision and cooldown, with verified observations only.

## Cost and reliability
Current expanded workflow can attempt up to 5 ranking calls + 1 detail call + 15 creator-list calls + 5 trend calls + 5 video-list calls = **31 EchoTik calls/day**. Subscription/API billing may apply. These are upper bounds, not guarantees. No speculative high-volume crawl. Run once manually before trusting schedule. Daily scheduled UTC time is fixed and shifts relative to Pacific local time at DST transitions.

## Operator check
After manual GitHub Actions run, inspect `data/maya-product-scout-health.md` and `data/maya-product-scout-audit.json`. A green workflow means code executed, NOT that every API endpoint returned data. Only use verified, fresh values in decisions.
