# Maya creator verification integration — 2026-10-27

## Tested state

- GitHub connector can read this repository. Latest collector run observed: 40571042560, completed successfully 2026-10-27T19:39:53Z. This does not test the new reporting changes.
- Available browser was a cloud Chrome with zero tabs, not the user's local signed-in TikTok browser. Opening https://affiliate-us.tiktok.com/ redirected to Seller registration. Following Creator opened https://business.tiktokshop.com/us/creator. Its Log in menu offered Seller Center, Partner Desktop and LIVE Manager, not Product Marketplace. Following LIVE Manager exposed TikTok sign-in redirecting to the streamer dashboard. No creator identity or account product data was observed; marketplace access after sign-in remains untested.
- No creator API authorization was established or API request made. No cookies, passwords or tokens were read or stored. No showcase changes were made.
- The five records are UNAVAILABLE, not INELIGIBLE. checked_at_utc is null because no account product check completed; report_generated_at_utc is not a verification timestamp.

## Official route and access requirements

TikTok documents Affiliate Creator APIs, separate from seller APIs. Affiliate API access is inactive by default, requires partner approval, an app and creator authorization. Possession of Creator Center access or an EchoTik subscription does not supply this authorization.

- Affiliate integration: https://partner.tiktokshop.com/docv2/page/affiliate-integration
- Creator OAuth prerequisites: https://partner.tiktokshop.com/docv2/page/678e3a362dccb8030ea6f98c
- Read showcase membership: https://partner.tiktokshop.com/docv2/page/get-showcase-products-202405 (creator.showcase.read; paginated, up to 2,000 products). This reads membership; it does not prove a product can currently be newly added.
- Creator open collaboration product APIs are documented under Read Creator Affiliate Collaborations in the integration guide. Exact approved endpoint/version, returned fields, regional access and account-specific restriction behavior must be confirmed using the authorized app before implementing a live adapter. API documentation existence is not a tested connection.

## Field coverage

| Field | Browser evidence required | Official API assessment |
|---|---|---|
| Account eligibility | Exact product ID and signed-in creator identity plus explicit eligibility/restriction state | Creator collaboration APIs are the candidate route; missing search result is UNKNOWN, not ineligible. Not tested. |
| Commission | Current account offer, distinguish organic vs Shop Ads and targeted offers | Require creator-specific offer and unit normalization; EchoTik is not proof. Not tested. |
| Price | Displayed USD price/range with variant/coupon context | Require product response and variant context. Not tested. |
| Availability | Explicit stock state and variant/color/size scope | Require returned inventory/status semantics. Not tested. |
| Add to Showcase | Observe enabled/disabled/already-added button; do not click | Read showcase membership is documented; membership is distinct from add eligibility. Not tested. |

Browser inspection is conditional on a supported surface, site terms and access restrictions. Do not use private network endpoints, extract cookies, replay browser sessions, bypass CAPTCHAs or treat user authorization as permission from TikTok. No unattended browser scraper has been installed.

## Implemented daily behavior

The existing Actions collector builds the research shortlist, then runs scripts/maya_affiliate_report.py. This refreshes five IDs, preserves observations without renewing their timestamps, applies the shared fail-closed gate, writes a queue/dashboard, and replaces only the marked affiliate section of HQ. Actions commits these outputs. The shortlist and research audit use the same account/product/source/age gate. Evidence older than 48 hours, future-dated records, wrong creator/region/ID and missing fields cannot become VERIFIED.

Records use decimal commission fractions (0.10 = 10%), USD price amount, stock scope, UI status and an account-specific observation with exact-ID and account confirmation. PARTIALLY VERIFIED means fresh account evidence exists but one or more required fields are missing. UNAVAILABLE means no usable current account evidence. VERIFIED can be eligible OR ineligible; only eligibility=ELIGIBLE passes the promotion gate. No automated product approval or showcase mutation is enabled.

## Best supported next steps

1. Connect a permitted creator session and inspect five exact IDs without clicking Add. If the marketplace is mobile-only for this account, a browser session will not unlock it. A short user-assisted batch of the five product detail screens is a fallback, with evidence recorded honestly as assisted, not unattended.
2. For hands-off verification, use an approved Affiliate Creator app/provider supporting creator OAuth and the required read scopes. Validate profile identity, product/offer fields, showcase pagination, restrictions and token refresh with this account before enabling daily checks.
3. Keep app secrets and OAuth credentials in a managed secret store, never repository files or logs. Use least-privilege read access and a secure callback with state validation. No credentials should be pasted into chat. A provider must expose permitted account-specific data, not merely public product analytics.
4. Until then the automated report will continue to say UNAVAILABLE and retain research leads as conditional. Recheck eligibility/commission/stock at posting time; 48 hours is a reporting freshness threshold, not a guarantee.
