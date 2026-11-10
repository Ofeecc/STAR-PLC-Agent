"""Create and verify the actual narrated slide video, without remote services.

Inputs are the final slide PNGs, the exact speaking notes and actual SAPI WAVs.
This script records computer-generated narration explicitly. It does not claim
that a human presented the slides or that static slide images are live footage.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
import wave

ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    checksum = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            checksum.update(block)
    return checksum.hexdigest()


def mp4_duration(path: Path) -> float:
    """Read the saved MP4 movie-header duration, including v0/v1 time scales."""
    data = path.read_bytes()

    def boxes(start: int, end: int):
        position = start
        while position + 8 <= end:
            size, kind = struct.unpack_from('>I4s', data, position)
            header = 8
            if size == 1:
                if position + 16 > end:
                    raise ValueError('Truncated extended MP4 box')
                size = struct.unpack_from('>Q', data, position + 8)[0]
                header = 16
            elif size == 0:
                size = end - position
            if size < header or position + size > end:
                raise ValueError('Invalid MP4 box size')
            yield kind, position + header, position + size
            position += size

    for kind, start, end in boxes(0, len(data)):
        if kind != b'moov':
            continue
        for child, payload, bound in boxes(start, end):
            if child != b'mvhd':
                continue
            version = data[payload]
            if version == 0 and payload + 20 <= bound:
                scale, duration = struct.unpack_from('>II', data, payload + 12)
            elif version == 1 and payload + 32 <= bound:
                scale, duration = struct.unpack_from('>IQ', data, payload + 20)
            else:
                raise ValueError('Unsupported or truncated MP4 movie header')
            if scale <= 0:
                raise ValueError('Invalid MP4 time scale')
            return duration / scale
    raise ValueError('MP4 movie-header duration not found')


def wav_duration(path: Path) -> float:
    with wave.open(str(path), 'rb') as audio:
        return audio.getnframes() / audio.getframerate()


def srt_time(seconds: float) -> str:
    milliseconds = round(seconds * 1000)
    hours, milliseconds = divmod(milliseconds, 3_600_000)
    minutes, milliseconds = divmod(milliseconds, 60_000)
    secs, milliseconds = divmod(milliseconds, 1000)
    return f'{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}'


def run(command: list[str], log: Path, *, timeout: float = 300) -> subprocess.CompletedProcess:
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=timeout)
    log.write_text(result.stdout + result.stderr, encoding='utf-8')
    if result.returncode != 0:
        raise RuntimeError(f'FFmpeg failed ({result.returncode}); inspect {log}')
    return result


def create_video(root: Path = ROOT, *, gap: float = 0.5, overwrite: bool = False) -> dict:
    import imageio_ffmpeg

    root = root.resolve()
    narration_path = root / 'presentation/narration.json'
    entries = json.loads(narration_path.read_text(encoding='utf-8-sig'))
    if not isinstance(entries, list) or not 6 <= len(entries) <= 8:
        raise ValueError('Expected 6-8 narration entries')
    manifest_path = root / 'video/audio/narration_manifest.json'
    narration_manifest = json.loads(manifest_path.read_text(encoding='utf-8-sig'))
    if narration_manifest.get('synthetic_narration') is not True:
        raise ValueError('SAPI synthesis disclosure is absent')
    if narration_manifest.get('narration_sha256') != sha256(narration_path):
        raise ValueError('Narration JSON changed after audio synthesis')
    audio_rows = {int(row['slide']): row for row in narration_manifest['slides']}
    slides = []
    for index, entry in enumerate(entries, 1):
        if entry.get('slide') != index or not isinstance(entry.get('text'), str) or not entry['text'].strip():
            raise ValueError('Narration entries must be sequential and non-empty')
        image = root / f'presentation/rendered/{index:02d}.png'
        audio = root / f'video/audio/slide_{index:02d}.wav'
        if not image.is_file() or not audio.is_file():
            raise ValueError(f'Final rendered slide or actual WAV is absent: slide {index}')
        if audio_rows[index]['sha256'] != sha256(audio) or audio_rows[index]['text'] != entry['text']:
            raise ValueError(f'Audio/source manifest mismatch: slide {index}')
        seconds = wav_duration(audio)
        if seconds <= 0:
            raise ValueError('Empty narration WAV')
        slides.append({'slide': index, 'image': image, 'audio': audio, 'narration_seconds': seconds,
                       'planned_seconds': seconds + gap, 'text': entry['text']})
    planned = sum(slide['planned_seconds'] for slide in slides)
    if not 0 < planned < 359:
        raise ValueError(f'Planned video duration is {planned:.3f}s; shorten narration before recording')
    output = root / 'video/explanation.mp4'
    if output.exists() and not overwrite:
        raise FileExistsError('Video already exists; pass --overwrite to explicitly replace it')
    work = root / '.local/video_build'
    work.mkdir(parents=True, exist_ok=True)
    evidence = root / 'video/verification'
    evidence.mkdir(parents=True, exist_ok=True)
    executable = imageio_ffmpeg.get_ffmpeg_exe()
    version = run([executable, '-version'], evidence / 'ffmpeg_version.log', timeout=30).stdout.splitlines()[0]
    segments = []
    for slide in slides:
        segment = work / f"slide_{slide['slide']:02d}.mp4"
        run([executable, '-hide_banner', '-y', '-loop', '1', '-framerate', '30', '-i', str(slide['image']),
             '-i', str(slide['audio']), '-map', '0:v:0', '-map', '1:a:0',
             '-vf', 'scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=white,format=yuv420p',
             '-af', f'apad=pad_dur={gap:.6f}', '-t', f"{slide['planned_seconds']:.6f}",
             '-c:v', 'libx264', '-preset', 'medium', '-tune', 'stillimage', '-crf', '20',
             '-c:a', 'aac', '-b:a', '128k', '-ar', '44100', '-movflags', '+faststart', str(segment)],
            evidence / f"encode_slide_{slide['slide']:02d}.log")
        segments.append(segment)
        print(f"Encoded slide {slide['slide']} ({slide['planned_seconds']:.1f}s)", flush=True)
    # These are local filenames we created, with no apostrophes or newlines.
    # A relative concat list avoids escaping the user's Unicode workspace path.
    playlist = work / 'segments.txt'
    playlist.write_text(''.join(f"file '{segment.name}'\n" for segment in segments), encoding='utf-8')
    run([executable, '-hide_banner', '-y', '-f', 'concat', '-safe', '1', '-i', str(playlist),
         '-c', 'copy', '-movflags', '+faststart', str(output)], evidence / 'concat.log')
    duration = mp4_duration(output)
    if not 0 < duration < 360:
        raise ValueError(f'Actual MP4 duration {duration:.3f}s violates the <360s requirement')
    # Decode the complete actual file; encoded/container presence alone is insufficient.
    run([executable, '-v', 'error', '-xerror', '-err_detect', 'explode', '-i', str(output), '-map', '0:v:0', '-map', '0:a:0', '-f', 'null', '-'],
        evidence / 'full_decode.log', timeout=300)
    probe = subprocess.run([executable, '-hide_banner', '-i', str(output)], capture_output=True,
                           text=True, encoding='utf-8', errors='replace', timeout=30)
    (evidence / 'actual_file_probe.log').write_text(probe.stdout + probe.stderr, encoding='utf-8')
    if not re.search(r'Video:\s+h264', probe.stderr) or not re.search(r'Audio:\s+aac', probe.stderr):
        raise ValueError('Expected actual H.264 video and AAC audio streams')
    subtitles = []
    cursor = 0.0
    for slide in slides:
        # Slide-level speaking-note captions, not a claim of word-level alignment.
        subtitles.append(f"{slide['slide']}\n{srt_time(cursor)} --> {srt_time(cursor + slide['narration_seconds'])}\n{slide['text']}\n")
        cursor += slide['planned_seconds']
    (root / 'video/explanation.srt').write_text('\n'.join(subtitles), encoding='utf-8')
    metadata = {
        'schema_version': 1, 'created_utc': datetime.now(timezone.utc).isoformat(),
        'path': 'video/explanation.mp4', 'sha256': sha256(output), 'bytes': output.stat().st_size,
        'duration_seconds': duration, 'duration_method': 'Actual MP4 moov/mvhd movie-header duration',
        'under_six_minutes': duration < 360, 'complete_decode_passed': True,
        'video_codec': 'H.264', 'audio_codec': 'AAC', 'resolution': [1280, 720], 'fps': 30,
        'narration': {'synthetic': True, 'backend': narration_manifest['backend'], 'voice': narration_manifest['voice'],
                      'rate': narration_manifest['rate'], 'disclosure': narration_manifest['disclosure']},
        'content_scope': 'Static final slides with synthesized English speaking notes; no fabricated live PLC demonstration footage.',
        'ffmpeg_version': version, 'imageio_ffmpeg_version': imageio_ffmpeg.__version__,
        'narration_source': 'presentation/narration.json', 'narration_sha256': sha256(narration_path),
        'between_slide_padding_seconds': gap,
        'slides': [{'slide': s['slide'], 'image': str(s['image'].relative_to(root)).replace('\\', '/'),
                    'image_sha256': sha256(s['image']), 'audio': str(s['audio'].relative_to(root)).replace('\\', '/'),
                    'audio_sha256': sha256(s['audio']), 'narration_seconds': s['narration_seconds'],
                    'planned_seconds': s['planned_seconds']} for s in slides],
        'verification_logs': 'video/verification', 'caption_timing': 'Slide-level narration intervals',
    }
    (root / 'video/video_metadata.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return metadata


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--gap', type=float, default=0.5)
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    if not 0 <= args.gap <= 3:
        parser.error('--gap must be between 0 and 3 seconds')
    try:
        result = create_video(args.root, gap=args.gap, overwrite=args.overwrite)
        print(json.dumps({'path': result['path'], 'duration_seconds': result['duration_seconds'],
                          'sha256': result['sha256'], 'complete_decode_passed': result['complete_decode_passed']}, indent=2))
        return 0
    except (OSError, ValueError, KeyError, RuntimeError, subprocess.SubprocessError) as exc:
        print(json.dumps({'error': str(exc)}), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
