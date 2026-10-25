# Metricool → GitHub → Gemini Learning Pipeline

## Status (2026-10-25)
- Metricool brand verified: `maya._.finds` (brand ID `7649128`).
- TikTok posts metric definitions verified: published date TKPO01, video URL TKPO03, views TKPO07, reach TKPO11, completion rate TKPO13, average watch time TKPO15.
- Live queries for Oct 18–25 and Oct 1–25 returned `{"rows":[]}`. **No video-level performance evidence available yet.** This is a missing-data condition, not zero views.
- GitHub read/write verified.
- Daily scheduled task can attempt data collection and GitHub persistence when its execution has the necessary connected tools; this is not a guaranteed external always-on integration.

## Daily run contract
1. Read this file and the learning log before changing anything.
2. Query Metricool for recent TikTok post data (last 30 days), including TKPO01, TKPO03, TKPO07, TKPO11, TKPO13 and TKPO15. Use the verified brand ID.
3. If rows exist, match by **actual video URL**; never match by guessed product names or captions. Keep dates and metric units, and never conflate views with reach or completion with average watch time.
4. Fetch `maya-performance-snapshot.json`; update it with the retrieved rows, fetch time, query window and source. Keep historical snapshots only when justified by observed data.
5. If no rows exist, record a clear status of `no_rows_returned` and preserve any older valid data. Do not infer zero posts, zero views or declining performance.
6. Fetch `gemini-generation-learning-log.md`. Connect performance to a reviewed generation only if a documented shared video URL/ID establishes the match. Do not fabricate a connection.
7. Report top-performing formats only when the evidence supports the grouping. Otherwise say what cannot yet be inferred.
8. GitHub write operations require the current file SHA. Confirm successful writes; on failure report the gap, never claim sync.
9. The next Gemini prompt should consult the learning log and performance snapshot and prioritize views/retention while keeping exact product fidelity and Shop compliance.

## Data quality gates
- No row → no performance inference.
- Missing metric → null, not zero.
- No verified product link → no attribution of sales or commissions.
- No reviewed video → no POST verdict.
- No shared identifier → no claim that a Gemini prompt caused TikTok performance.
- One successful tool call does not prove future unattended runs will succeed.

## Troubleshooting
- If Metricool keeps returning empty rows, inspect account sync / TikTok post visibility and connector coverage.
- If GitHub writes fail, do not overwrite or duplicate data blindly.
- Keep daily status and last-success timestamps visible in the HQ.
