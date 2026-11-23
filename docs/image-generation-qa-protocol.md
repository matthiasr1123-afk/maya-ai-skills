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

## Retest 2026-11-23: camera-angle correction
- Source visually inspected again: `Black Leopard Trim Pants Set - Car Seat.jpeg` in ChatGPT Library.
- New single-image output at 941x1672 (near 9:16) shows top-down, face-free, both legs and both white sneakers, black pants, leopard waistband, white drawstrings. No collage or text overlay.
- **CAMERA_ANGLE: PASS for framing test.** This is a visual assessment, not exact reference fidelity.
- **PRODUCT_FIDELITY: UNVERIFIED** because the generation was not proven to be a true pixel-conditioned edit of the Library source. Do not claim the source pixels were passed to the image generator.
- Improved direction: lead with `top-down crop, face-free, chest-to-shoes, black leather car seat`, then specify exact garment. Avoid `selfie`, `pout`, `messy bun`, `arm extended` and face description; those cause face-focused output.
- File existence and dimensions checked in current container; not yet approved for posting or tested in Gemini.
- Next gate: actual image-to-image edit using accessible source bytes, compare pattern/fit/angle, then a second distinct approved product. Cozy Approved remains empty.

## Step 3 source-byte access test (2026-11-23)
- **PASS**: Files materialize returned original JPEG bytes at `/mnt/data/maya_reference_test/Black Leopard Trim Pants Set - Car Seat.jpeg` (709x1536, 189876 bytes). This resolves the Library-to-container file access problem.
- **NOT PROVEN**: image_gen call returned a fresh image with metadata `edit_op:null`, `parent_gen_id:null`; therefore this is **not verified source-conditioned editing**. The image resembles the source but similarity is insufficient proof. Do not call it an edited original.
- **PASS**: fresh generation has a face-free chest-to-shoes high-angle composition, both white sneakers, black wide-leg pants, leopard waistband, white drawstrings and no on-image text.
- **BLOCKED**: exact source-pixel preservation and removal of screenshot overlays by the image generator are not verified. Do not approve exact seller fidelity or mark full four-image workflow passed.
- Next: test a true image editing action that accepts the original file bytes as input, or create a lossless pixel-preserving cleanup of the original using image-processing tools with explicit QC; distinguish this from generative image editing. Never replace source pixels silently.

## Pixel-preserving cleanup test (2026-11-23)
- Materialized the exact original source JPEG and tested deterministic image-processing cleanup, not generative editing.
- Crop 709x1296 removed top status bar and bottom playback UI while preserving original camera framing and pixels in the retained region.
- Attempt A: large rectangle inpainting over text/emojis caused an obvious blurred horizontal patch on the black pants. **FAIL**.
- Attempt B: narrow color/brightness segmentation and inpainting left dark ghost lettering/emoji artifacts. **FAIL**.
- Neither cleanup result is approved for posting. Do not call the files clean or deliver them as production assets.
- A pixel-preserving crop of the source is useful for geometry reference but cannot remove middle caption without reconstructing occluded garment pixels; deterministic inpainting may leave visible artifacts. Next step: a true image-editing route with original bytes explicitly attached, or a higher-quality local restoration method; compare the exact source and inspect edited area at full resolution. Never hide failed cleanup behind generic success labels.
