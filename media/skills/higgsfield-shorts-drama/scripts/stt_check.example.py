#!/usr/bin/env python3
"""Example review pass for one take. Served as text; adapt, then run in the sandbox as a background job.

Usage: python3 stt_check.example.py <take.mp4> <language code> ["<the cut's lines, space-separated>"]
Prints: the duration; two plain decodes (small and medium, no prompt), each segment with its times and
no-speech probability and every word with its probability; when the lines are given, a third decode
prompted with them, printed as support only; writes a 2 fps contact sheet next to the take.
Voice activity detection stays off: it has missed whispers and invented phrases over wind.
"""
import subprocess, sys

take, lang = sys.argv[1], sys.argv[2]
hint = sys.argv[3] if len(sys.argv) > 3 else ""
subprocess.run(["ffmpeg", "-y", "-i", take, "-af", "loudnorm=I=-16:TP=-1.5", "-ar", "16000", "-ac", "1", "norm.wav"],
               capture_output=True, check=True)
subprocess.run(["ffmpeg", "-y", "-i", take, "-vf", "fps=2,scale=160:-1,tile=6x4", "-frames:v", "1", "-q:v", "4", "sheet.jpg"],
               capture_output=True)
dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", take],
                     capture_output=True, text=True).stdout.strip()
print("DURATION", dur)

from faster_whisper import WhisperModel  # noqa: E402


def decode(size, prompt):
    model = WhisperModel(size, device="cpu", compute_type="int8")
    segs, _ = model.transcribe("norm.wav", language=lang, word_timestamps=True, vad_filter=False,
                               initial_prompt=prompt or None, beam_size=5)
    print(f"== {size}" + (" (prompted, support only)" if prompt else " (plain)"))
    for s in segs:
        print(f"[{s.start:.2f}-{s.end:.2f}] no_speech={s.no_speech_prob:.2f} {s.text.strip()}")
        print("   " + " ".join(f"{w.word.strip()}({w.probability:.2f})" for w in (s.words or [])))


decode("small", "")
decode("medium", "")
if hint:
    decode("medium", hint)

# Reading the result (stt-review.md): both plain decodes agree with the line -> clear; neither writes a word as
# intended -> wrong word, whatever the prompted decode says; a word under 0.1 with no_speech above 0.5 on a
# silent stretch -> hallucination.
