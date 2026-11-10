# Video deliverables

`explanation.mp4` is the completed locally encoded narrated slide video. Its
actual duration is **293.936 seconds (4 minutes 53.936 seconds)**, below the
six-minute requirement. It contains H.264 video at 1280 x 720 / 30 fps and an AAC
audio track. Its narration uses the Windows SAPI Microsoft Zira Desktop voice;
it is computer-generated narration. No human speaker recording or live PLC
demonstration footage is claimed.

The source is `presentation/narration.json`; images are the final eight approved
slide PNGs. The completed MP4 passed a complete FFmpeg decode. One actual decoded
frame per slide was visually inspected, with no clipping or encoding corruption
observed. The results frame contains the final functional case counts 42/45,
46/48, 38/38 and 50/52, and states the 81 planned-case denominator and coverage
limits. Source-frame comparisons have PSNR values above 40 dB.

`video_metadata.json` binds the actual duration, successful decoding, source and
media hashes, inspected frames and objective audio checks. `status.json` records
completion. `verification/` retains encoder/probe/decoder logs and the eight
actual frame samples. `explanation.srt` contains slide-level speaking notes;
it does not claim word-level synchronization.

The actual audio has a mean volume of -20.2 dBFS and a peak of -2.4 dBFS, with
non-silent signal and no full-scale clipping peak. **No human listening or
perceptual pronunciation review was performed.** The presenter should listen
once to check technical names and personal presentation preferences.

The production route and human-recorded alternative are described in
[recording_plan.md](recording_plan.md). Changing notes or slide PNGs requires
recreating and rechecking the MP4; the old hashes then no longer describe it.
