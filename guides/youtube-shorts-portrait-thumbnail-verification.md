# Verify YouTube Shorts thumbnails before scheduling

Verified against official documentation on 19 November 2026.

## Problem and fix

A successful `thumbnails.set` response does not prove the displayed image matches the artwork. A landscape image supplied for a Short can be cropped to portrait, removing text and other content positioned outside the center. Comparing a landscape source to a legacy 4:3 CDN image can then produce a real mismatch.

Use an authored 9:16 cover for a Short. Wait for `processingDetails.processingStatus == "succeeded"`, set the thumbnail on the **existing video ID**, and verify the actual `snippet.thumbnails.shortsAspectRatio` pixels. Keep the video private if verification fails. Do not re-upload a second copy of the video to fix its cover.

The reusable, read-only verifier is in [`tools/youtube/shorts_thumbnail_readback.py`](../tools/youtube/shorts_thumbnail_readback.py). It downloads only a thumbnail URL returned by the official API on a trusted YouTube CDN hostname. No OAuth credentials are sent to the CDN request. The caller supplies an already authenticated YouTube client; the helper contains no token lookup or storage.

## Integration

```python
from shorts_thumbnail_readback import verify

# y is an existing, authorized YouTube Data API client.
# Identity and asset checks belong to your publishing service.
result = verify(y, existing_video_id, authored_portrait_cover, local_qa_folder)
if not result["match"]:
    # Persist a private/manual-review state. Do not schedule or re-upload.
    return

# Schedule only after checking the channel ID, asset checksum, future date,
# private status and content/rights review. Then GET publishAt to verify it.
```

Treat the perceptual hash as a publication guard, not a complete design or semantic review. Open the returned image to confirm readability, language and composition. It does not guarantee that every personalized Shorts feed surface presents the same crop or UI.

## Queue safeguards

- Authenticate the intended channel ID before any write.
- Save a video ID as soon as upload succeeds; never repeat `videos.insert` when that ID exists.
- If an upload began but its response is ambiguous, require owner reconciliation instead of blindly retrying.
- Serialize related workers with a shared lock and enforce an explicit local daily upload cap. A local cap is **not** a claim about remaining server quota.
- Read processing status before applying a cover. Retry CDN propagation reads with a bounded timeout; do not continuously rewrite thumbnails.
- Verify `publishAt` after scheduling. A private video with a future `publishAt` is scheduled; a private video without it is not.
- Completed jobs should be no-ops even after their scheduled date has passed.

No public video, analytics, channel ID, OAuth file or personal media is included in this example.

## Local tests

Requires Pillow and NumPy in an existing Python environment:

```sh
python3 -m unittest discover -s tools/youtube -p 'test_*.py'
```

The tests verify that a resized copy of the portrait artwork matches, while a blank portrait and a legacy landscape crop do not.

## Official sources

- [YouTube Data API — thumbnails.set](https://developers.google.com/youtube/data/reference/rest/v3/thumbnails/set): supports Shorts; call after video processing succeeds.
- [YouTube Data API — thumbnail resource](https://developers.google.com/youtube/data/reference/rest/v3/thumbnails): describes Shorts portrait cropping and `shortsAspectRatio`.
- [YouTube Help — custom thumbnails](https://support.google.com/youtube/answer/72431): recommends 9:16 artwork for Shorts and notes propagation delays and surface differences.

These docs were updated recently; older blanket statements that the API cannot set any Shorts thumbnail should not be carried forward without checking the current primary sources.
