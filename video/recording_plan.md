# Explanation video

The narrated-slide route below has been executed. The completed
`explanation.mp4` is 293.936 seconds long and passed full decoding and sampled
visual inspection. See `video_metadata.json` for hash-bound evidence. The local
speech track passed objective signal checks; human listening remains a useful
final presenter review.

The teacher requires a video shorter than six minutes. The reproducible local
route uses the eight final slides and computer-generated English narration from
the exact saved speaking notes. It is a narrated slide video, rather than a
recording of a human speaker or live PLC operation. This distinction is recorded
in `video_metadata.json` and the SAPI audio manifest.

## Local production

1. Finish `presentation/slides.pptx`, its visual inspection, and the matching
   `presentation/rendered/01.png` through `08.png` previews.
2. Save `presentation/narration.json` as an ordered JSON array of objects with
   `slide` (1 through 8) and `text` (the full English speaking note).
3. Run from the project root in PowerShell:

   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\create_narration.ps1
   & 'C:\Users\田子佼\.conda\envs\Project1\python.exe' scripts\create_video.py
   ```

   `create_narration.ps1` uses the installed **Microsoft Zira Desktop** voice at
   normal rate. It saves actual WAV files and source/audio hashes. It does not
   use cloud services, imitation voices, or paid APIs.

4. The video script uses the lightweight `imageio-ffmpeg==0.6.0` package, H.264
   video and AAC audio. Intermediate segments remain under `.local/video_build`
   and are excluded from the submission. The script rejects stale audio,
   requires a planned duration below 359 seconds, reads the completed MP4 movie
   header, requires an actual duration below 360 seconds, and decodes the whole
   file to check for corrupt media. It saves logs, hash-bound metadata and
   slide-level subtitles.
5. Watch the complete final MP4 and listen to the narration. Check every slide,
   text size, slide transitions, volume and technical names. Confirm that the
   figures match the report and final benchmark records. The automatic checks
   do not substitute for a human audiovisual review.

The video script has an explicit `--overwrite` option for deliberate recreation.
Do not change the speaking notes without regenerating both audio and video.

## Human-recorded alternative

Open the editable PowerPoint, review `presentation/speaker_notes.md`, and record
the slideshow with a microphone in PowerPoint, OBS or Windows screen recording.
Use the prepared notes as a 4-5 minute script. A practical timing plan is about
25 seconds for the objective, 35 for the dataset, 35 for architecture, 35 for
real compilation, 30 for design, 45 for results, 35 for repair, and 30 for
limitations: approximately 4 minutes 30 seconds plus small transitions.

If recording a live CODESYS demonstration, show the saved known-invalid program,
its actual compiler errors and the repaired program's clean build. Use a local
simulation project only. Do not show credentials or claim a static screenshot
is live execution. Keep the demonstrated source and logs in the submission.

For either route, verify the exported file itself and ensure its total duration
is strictly below six minutes. If media creation is unavailable, submit the
editable deck, notes and this recording plan as recording-ready materials, and
mark the finished video as pending.
