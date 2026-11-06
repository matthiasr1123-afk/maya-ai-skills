# Maya Finds: 7-day / 8-post experiment
Dates: 2026-11-07 through 2026-11-13 (America/Los_Angeles)
Status: Experiment plan created; actual TikTok posts and Metricool schedule NOT created.

## Goal and hypothesis
Test whether eight distinct, accurate videos/day using existing promising creative angles increases total reach, product clicks, attributed sales and commission without collapsing median views/video or retention. No guarantee of virality. Avoid near-duplicate spam.

## Baseline
Nov 6 user profile screenshot: dark leopard matching set 8,409 views, mirror 1,024, seated 958; user reports five leopard-product sales but individual-video attribution not verified. Previous Oct29–Nov4 detail: standing dark leopard CTR 5.34% at 141 views, car-seat CTR 3.84% at 345 views, both 0 attributed sales in that older period. Product user-reported rating 2.6 stars and weak commission: creative reference only, not automatically an approved SKU.

## Daily eight slots, Pacific time (test slots, not verified best times)
08:00 car-seat close-up; 09:30 full-body mirror; 11:00 seated side angle; 12:30 car-seat variation; 14:00 full-body mirror; 16:00 cozy seated; 18:00 car-seat close-up; 20:00 alternate strongest angle.
Use 1–2 eligible, accurately referenced, well-reviewed products initially; balance angle assignments across products and rotate slot positions to reduce time confounding. 6–8s target, distinct authentic hooks and poses; no identical reuploads. Actual posting depends on completed Gemini videos, approval, and Metricool/TikTok upload support.

## Daily schedule
Nov7 baseline; Nov8 alternate hooks; Nov9 angle comparison; Nov10 optimize clicked SKU; Nov11 first-frame test; Nov12 retention/sales refinement; Nov13 confirm repeatability. Keep changes limited, log differences.

## Tracker schema
date_local, post_time_local, platform_post_id, video_url, product_id, product_name, seller, rating_at_selection, commission_rate_at_selection, creative_angle(V1/V2/V3/V4), hook, video_duration_s, status(planned/ready/scheduled/published/failed), views_2h, views_24h, views_48h, avg_watch_time_s, completion_rate, product_clicks, ctr_pct, items_sold, gmv_usd, commission_usd, violation_flag, notes, metrics_observed_at, source.
Use null for unavailable, not zero. Never infer clicks from views*CTR or assign product sales to a video without per-video attribution. Retain AI disclosures and seller accuracy.

## Evaluation
Each day summarize scheduled vs published count, views per video median, 24h and 48h cohort views, total product clicks, clicks per 1k views, attributable sales/commission, commission per video, flagged posts. On Nov14 evaluate full 7-day cohorts (allow 48h maturity for Nov13 posts through Nov15 if necessary), compare with historical baseline on matched time windows, and decide continue 8, increase cautiously, or reduce. Do not claim causal effect from observational comparison.

## Workflow
User sends Kalodata screenshot + product name; assistant verifies exact SKU, commission, rating/reviews, eligibility and product reference, then creates batch stills and Gemini prompts. User makes Gemini clips and supplies files; assistant QC/edits and provides silent exports, captions, and scheduling package. Direct Showcase addition and TikTok native draft creation are not confirmed capabilities; use signed-in Work browser or exact listing link if needed. GitHub is workflow source of truth; no production folder or media automation claimed until tested.

## Exposure Plus tracking (added Nov 6)
TikTok Shop screenshots observed Nov 6 show "You gained 6225 more views" from featuring Exposure Plus products **over the past 7 days** (rolling window, not Nov 6 alone). Per-video UI examples: Nov 5 12:12 PM dark leopard matching-set car-seat post +343 Exposure Plus views; Nov 5 8:15 AM leopard slipper post +70; another slipper post +37 (post timestamp partly obscured). UI explanatory text: "This video received more views than your others in the last 7 days because it features 'Exposure plus' products." These are TikTok's attributed uplift estimates, not proven paid ad/GMV Max views, and not necessarily additive to total video views.
Track columns per video: exposure_plus_product_status (yes/no/unknown), exposure_plus_extra_views (integer/null), exposure_plus_observed_at_local, exposure_plus_reporting_window, total_video_views, video_post_id, evidence_source, notes. For account-level 7d rolling totals record separately (6225 as of Nov 6 screenshot) and never sum rolling windows or add uplift to video total. Do not calculate organic views as total minus Exposure Plus unless TikTok defines non-overlapping counts. Product choice: verify Exposure Plus badge in TikTok Shop, not Kalodata inferred eligibility. Compare video performance with and without Exposure Plus while noting confounders.
