# Maya Finds — Paid-demand and creator-scarcity evidence specification
Updated 2026-11-03. Research-only; never store tokens, passwords, or private creator account data in this repository.

## Source-of-truth rules
- Exact TikTok Shop US product ID and canonical listing URL must match each research source. Preserve provider product ID separately and mark mapping confidence.
- Ad activity: advertiser identity, exact creative/ad URL or ID, observed active date, number of distinct creatives, first/last observed, source and region. TikTok Creative Center Top Ads is a curated showcase, NOT a complete active-ad inventory. No ad found != no ads.
- Spend: store USD spend only if a provider exposes documented product/advertiser-specific estimated spend with timeframe and method. Otherwise null. Label estimates vs actual. Do not infer spend from ad count, impressions, brand size, or revenue.
- Creator saturation: unique creator IDs promoting the EXACT product in a rolling last-30-day window, with video/creator activity timestamps. Separate historical associated creators, 30d active video creators, LIVE creators, paid creators, and brand-owned posts. Deduplicate creator IDs. If only a sample is available, report sampled count and coverage; marketwide count null.
- Competition: independently find exact equivalent marketplace listings, not merely category or broad keyword matches. Mark unknown unless checked comprehensively.
- Demand: 7d/30d sales, revenue, VIDEO-vs-LIVE attribution, growth and dates, source; never treat cumulative sales as recent.
- Maya affiliate: authorized account-specific exact-ID eligibility, commission, inventory, showcase state, verified_at_utc, expires after 48h. No unauthorized scraping, no auto-add.
- Newness: listing first seen is NOT necessarily listing creation. Keep separate fields and confidence.
- Provider outages: stale data cannot be promoted as current; run reporting and surface outage.
- Status: VERIFIED TEST only if recent sales acceleration, genuinely low 30d active creator competition, documented active paid advertising and fresh Maya eligibility are confirmed. Otherwise CONDITIONAL TEST/WATCHLIST.

## Target filters and ranking
7–30 days since verified launch; <20 active promoting creators/30d (ideal <10); rising VIDEO-driven sales; paid campaign evidence; affordable credible payout; fashion UGC fidelity. Weights: 25 creator scarcity, 25 paid ad intensity, 20 video sales momentum, 10 recency, 10 affiliate economics, 10 AI fidelity. Unknown dimensions N/A; display evidence coverage and confidence, not an inflated score.

## Minimum machine-readable record
```json
{
  "product_id": null,
  "product_url": null,
  "listing_created_at_utc": null,
  "listing_age_confidence": "unknown",
  "advertiser": null,
  "ads": {"source": null, "checked_at_utc": null, "active_creatives_observed": null, "sample_scope": null, "evidence_urls": []},
  "spend": {"usd": null, "window_days": null, "source": null, "method": null, "is_estimate": null},
  "creators": {"unique_active_30d": null, "source": null, "checked_at_utc": null, "coverage": null, "associated_lifetime": null},
  "competition": {"equivalent_listing_count": null, "source": null, "coverage": null},
  "sales": {"units_7d": null, "units_30d": null, "video_revenue_30d_usd": null, "live_revenue_30d_usd": null, "source": null, "checked_at_utc": null},
  "maya_affiliate": {"eligibility": "UNAVAILABLE", "commission_fraction": null, "verified_at_utc": null, "source": null},
  "decision": "WATCHLIST",
  "unknown_fields": []
}
```

## Provider integration prerequisites
- Kalodata Open Center API: inspect official product/creator/video endpoint field definitions and pricing BEFORE buying; a creator ranking endpoint is not proof of exact-product unique active creators. Ask provider explicitly for exact product ID -> unique 30-day active creators, video-only sales, paid ad detection and advertiser-level spend estimates. If not available, leave null.
- TikTok Creative Center: public/manual evidence for advertising creatives only; not spend dollars.
- TikTok Commercial Content API: access-controlled, geographic coverage may not include US. Check eligibility and fields before attempting integration.
- TikTok Shop Creator Affiliate API: approved partner app + creator OAuth/scopes required; not connected merely because TikTok Shop is logged in.
- EchoTik: HTTP 402 until restored; do not use stale snapshots as live signals.

## Rollout acceptance tests
1. Provider permissions/credits verified without revealing secrets.
2. Five test exact product IDs match across product/creator/ad datasets.
3. At least one product's last-30d unique active creator count independently reproducible.
4. Ad evidence includes advertiser and observed date; spend missing unless directly supplied.
5. Account-specific creator OAuth consent and fields tested on a permitted account.
6. Scheduled run writes dated evidence and freshness/coverage status; read-back verified.
7. Deliberate API 402/429 failure yields stale/unknown flags, never fabricated data.
