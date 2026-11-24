# Maya + Cozy image generation: QA protocol (2026-11-23)

## Non-negotiable objective
One on-demand "Run Maya" command should eventually produce four **separate** accurate 9:16 photos from available approved references, each with an actual verified file, product-motion Gemini prompt. Do not claim end-to-end success until demonstrated. Never make collages, fake UI, or fake checkmark reports.

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
7. Keep Gemini prompt outside image, use 7–10 seconds of visible product motion as specified below. Gemini policy refusals are a separate category from visual defects.
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

## 2026-11-23 — Run Maya, source-based restoration retest

The original test requested two Maya and two Cozy images. The current allocation rule below supersedes that historical test. Read the current briefs, creative records and this protocol on each run. Enumerate each account's Approved folder directly. Materialize exact originals with the current Files helper, decode, hash, and inspect. Never use a fuzzy title hit or the Needs Verification folder for a production slot.

Maya car-seat framing is downward, face-free, chest to shoes, with both pant legs visible. Avoid the phrase “car selfie” as the main framing instruction. Use the original file as an actual image-edit input. An output generated from text alone cannot pass reference editing. The leopard affiliate item is the pants alone.

Two actual originals decoded at 709 × 1536. Black Leopard Trim Pants Set - Car Seat.jpeg SHA256 897b4806ccf7cb030dc7bcbd1d29a677276dccedbf09a0b1a9e31e940f3e06c3. Taupe Ribbed Flare Pants - Car Seat.jpeg SHA256 c0d2257f6a2885f39dc22534fd7ce7a5c5cd8346d5303e715122d1aebc0b9ddc. For both, send the source directly to image editing; request cleanup only, fixed product/framing, no overlays. Both raw edits were 852 × 1846. These dimensions alone fail delivery.

First composite FAIL: rectangular repair edge on black thigh; box seams and residual “more” near taupe shoe. For leopard, resize the donor edit to source geometry, register visually at the drawstrings, use original everywhere outside the lap caption. Match the donor to nearby source colors before feathering; inspect at native resolution. For taupe, overlapping controls affected multiple lower-leg and shoe areas; use the cleaned edit in the occluded region and preserve the original waistband, button, thigh, hand and seams above it. Feather across clean fabric. Source screenshot content behind lettering is reconstructed and cannot be verified pixel-for-pixel. Inspect ribbing, silhouette and color individually. Crop the screenshot and cleaned edit in source coordinates: leopard (3,128,705,1376), taupe (3,125,705,1373). These coordinates apply only to the exact two sources above. Treat new edits as new candidates and recheck alignment. Raw screenshot UI removal is separate from near-ratio output normalization.

Both final PNGs passed visual product/framing and decoded file checks, 702 × 1248. Leopard output SHA256 fa5131166869344e28769dba1c987fca6282be0f961e573759677b8306506624; taupe c3bf9a04ac026b0e4ebd8182c2ffbd8c851c558e35d196e3d17ebd91a42f647c. Each receives its own 8-second camera-only prompt and caption. Gemini acceptance unverified. Do not count a drafted prompt as an executed video test. Delivery IDs libfile_06ea42ee2b0c819192893962a481bb45 and libfile_895432469dc48191ac8f5f81a394cb45.

Full batch BLOCKED: Cozy/Approved listed zero files, and Cozy/Needs Verification contained Leopard Lounge Mirror.png. Do not promote it or reassign a Maya product. Re-list on each invocation. An automation run completing is insufficient evidence of four-image delivery. Preserve previous results, cap identical attempts at three, and record methods, source, corrections and per-file checks.

## Current Run Maya allocation — November 23

Fill four slots from whichever account has suitable approved references, including four Maya or four Cozy. Keep each asset assigned to its source account. An empty account folder does not block the other account. Prefer four distinct justified assets. Verify source bytes, visual fidelity, 9:16 PNGs, download paths, and individual image/prompt pairs.

## Creative variation for Run Maya

For each four-image batch, keep at most one close reference match as a control. Give each remaining image one intentional change visible at phone-thumbnail size: swap a non-featured top, change the background or setting, or choose a different supported pose or camera angle. For a pants batch, a useful starting mix is one proven car shot, two distinct top swaps, and one standing fit check when the references support it. Select a different mix when the products call for it. Small shifts in feet, fabric folds, crop, drawstrings or print placement do not count as the planned change. Preserve every item included in the affiliate listing, including tops sold as part of a set. Preserve garment color, cut, seams, logos, print motifs and scale. Only reveal surfaces or printed regions supported by approved reference photos. For a partial view of a print, vary styling or background within the supported crop. Keep styling pieces out of the product claim. Record the intended change before editing. Compare each output to the actual reference at thumbnail size for visible variation and at full size for product accuracy. If either check fails, revise the edit or switch concepts before delivery. Keep the account allocation, file checks, and per-image prompt pairing in force.

## Current image delivery and video motion

Deliver one verified image and one 7–10-second Gemini prompt per asset. Write the TikTok caption during video editing, after reviewing the actual clip. Start each clip with a clearly visible physical action in the first second. Choose one simple action supported by the pose and crop that shows how the product moves; describe the start, movement and finish. Keep the camera steady or naturally handheld. A digital zoom or pan over a frozen still is insufficient. Preserve garment geometry, print and anatomy. For an actual Gemini refusal, record the exact message separately from render defects and TikTok notices. If the action cannot render faithfully, change the shot or simplify the action. At video review play the clip at phone size and check for visible motion and product fidelity before approval.
