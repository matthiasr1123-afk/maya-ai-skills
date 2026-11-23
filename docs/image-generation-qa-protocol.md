# Maya + Cozy image generation: QA protocol (2026-11-23)

## Non-negotiable objective
One on-demand "Run Maya" command should eventually produce four **separate** accurate 9:16 photos (two Maya, two Cozy), each with an actual verified file, camera-only Gemini prompt and caption. Do not claim end-to-end success until demonstrated. Never make collages, fake UI, or fake checkmark reports.

## Reference acquisition
List ChatGPT File Library at `/Maya + Cozy Product Reference Library`; use `docs/product-reference-manifest.json` as locator, refresh IDs, read the actual image with Files before generation. Only approved references may be used for posting; currently Cozy/Approved has zero files, so block Cozy production until approved assets exist. Library images do not automatically become image-generation references; verify that the generator actually receives image pixels. If it cannot, stop and report the limitation. Do not substitute text-only approximation and call it reference editing.

## Locked product and camera contract: Maya black leopard-trim pants
Source: `Maya/Approved/Black Leopard Trim Pants Set - Car Seat.jpeg`.
- Black solid-color loose wide-leg pants, leopard-print **waistband only**, white drawstrings, white sneakers, seated in black leather car interior.
- Product-focused high-angle view from neck/chest downward; **both full pant legs and shoes visible**. Original source has a black top with leopard trim; avoid confusing it with a separate leopard matching set.
- No phone UI, timestamps, emojis, subtitles or on-image labels.
- The waist and legs should dominate image area; face cropped above lips or out entirely. Do not use a face-forward, arm-extended selfie composition.
- **No change of seat/camera geometry or visible anatomy inconsistencies.**

## Failure log (actual tests, not performance claims)
1. First four-panel infographic test: FAIL. Collage, text, fabricated download links, fake QA statuses.
2. Leopard attempt 1: FAIL. Legs/shoes cut off, face/torso-focused.
3. Leopard attempt 2: FAIL. Face-focused, pant legs cut off.
4. Leopard attempt 3: FAIL. Face-focused, pant legs cut off.
5. Leopard retest: PARTIAL. One photo; waistband, white drawstrings, black pants, both shoes present; **camera still too selfie-focused**. Exact seller fidelity unverified.

## Corrected execution
1. Choose one exact reference, record account/product and immutable visual details.
2. Prefer true reference-based editing with source pixels provided to generator. If unavailable, mark text-only generation as such and do not assert reference-fidelity.
3. Generate ONE clean photo per tool call, with camera geometry emphasized before clothing styling; no infographics or report graphics.
4. Inspect resulting image and compare product pattern, waistband, drawstrings, pants fit, full legs/shoes, hands, geometry, and 9:16 ratio. Check file exists before linking.
5. Fail fast and record precise error codes: `COLLAGE`, `CAMERA_ANGLE`, `PRODUCT_FIDELITY`, `CROP`, `ANATOMY`, `TEXT_OVERLAY`, `FILE_MISSING`, `GENERATOR_REFERENCE_UNAVAILABLE`.
6. Retry with a **different approach** rather than near-identical face-first prompts. Maximum three attempts per approach. If failure persists, report block and change method.
7. Keep Gemini prompt outside image, use 7–10 sec camera-only motion and static subjects. Gemini policy refusals are a separate category from visual defects.
8. Do not count QA as passed without comparing actual source/output. No fabricated testing or metrics.
9. Only after two individually approved products, attempt four-image batch. Cozy requires approved references before its two slots.

## Next test
Prove source pixels can be passed to the generator for true reference-based editing. Test crop-preserving removal of original source screenshot's phone UI and caption while retaining full pants, shoes and high-angle geometry. If image generation cannot ingest the Library image directly, investigate materialization/attachment route instead of guessing.
