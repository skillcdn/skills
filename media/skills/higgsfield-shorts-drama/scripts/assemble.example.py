#!/usr/bin/env python3
"""Example assembly script for one episode. Served as text; adapt, then run in the sandbox as a background job.

Shape: fetch takes and fonts -> normalize each timeline segment -> concatenate ->
burn ASS subtitles and cards -> loudness -> contact sheet -> upload.
Replaced or finalized takes and line timings come in as environment variables so the script is re-run, not rewritten.
"""
import json, os, subprocess, sys

OUT = os.environ.get("OUT", "episode_final.mp4")
W, H, FPS = 480, 854, 24
V = f"-c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p -r {FPS}".split()
A = "-c:a aac -b:a 160k -ar 48000 -ac 2".split()
NV = f"scale={W}:{H},setsar=1,fps={FPS}"

# Accepted takes by cut key: the hosted URL of each. A replaced or finalized take is passed as CLIP<n>.
TAKES = {
    "E1": os.environ.get("CLIP1", "https://host.example/take_e1.mp4"),
    "E2": os.environ.get("CLIP2", "https://host.example/take_e2.mp4"),
}
FONTS = {  # open-licensed fonts covering the dialogue's script, fetched from the google/fonts repository
    "Sans-ExtraBold.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/<family>/<file>.ttf",
    "Serif-Bold.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/<family>/<file>.ttf",
}

# Timeline: (name, source cut, start in source, duration, freeze padding, extra video filter, audio override)
# audio override = (cut, start) takes the sound from another take at that position: used by flash inserts,
# so the picture of the flash sits over the unbroken sound of the scene around it.
FLASH = "hue=s=0,eq=contrast=1.4,fade=t=in:d=0.08:color=white,fade=t=out:st=0.42:d=0.08:color=white"
SEG = [
    ("s01", "E1", 0.0, 8.0, 0, None, None),
    ("s02a", "E2", 0.0, 4.2, 0, None, None),
    ("s02f", "E1", 6.1, 0.5, 0, FLASH, ("E2", 4.2)),   # flash: picture from E1, sound continues from E2
    ("s02b", "E2", 4.7, 7.3, 0.8, "fade=t=out:st=7.5:d=0.6", None),  # freeze 0.8 s, fade to black
]


def run(cmd):
    r = subprocess.run(cmd, shell=isinstance(cmd, str), capture_output=True, text=True)
    if r.returncode:
        print("FAIL:", cmd if isinstance(cmd, str) else " ".join(cmd)); print(r.stderr[-2000:]); sys.exit(1)


def seg(o, src, ss, d, pad, xv, xa):
    tot = d + pad
    vf = NV + ("," + xv if xv else "") + (f",tpad=stop_mode=clone:stop_duration={pad}" if pad else "")
    af = f"aresample=48000,afade=t=in:d=0.03,afade=t=out:st={max(0, d - 0.04)}:d=0.04,apad"
    if xa:
        asrc, ass = xa
        run(["ffmpeg", "-y", "-ss", str(ss), "-t", str(d), "-i", f"{src}.mp4", "-ss", str(ass), "-t", str(d), "-i", f"{asrc}.mp4",
             "-filter_complex", f"[0:v]{vf}[v];[1:a]{af}[a]", "-map", "[v]", "-map", "[a]", "-t", str(tot)] + V + A + [f"{o}.mp4"])
    else:
        run(["ffmpeg", "-y", "-ss", str(ss), "-t", str(d), "-i", f"{src}.mp4",
             "-filter_complex", f"[0:v]{vf}[v];[0:a]{af}[a]", "-map", "[v]", "-map", "[a]", "-t", str(tot)] + V + A + [f"{o}.mp4"])
    return tot


os.makedirs("fonts", exist_ok=True)
for k, u in TAKES.items():
    if not os.path.exists(f"{k}.mp4"):
        run(["curl", "-sf", "-o", f"{k}.mp4", u])
for f, u in FONTS.items():
    if not os.path.exists(f"fonts/{f}"):
        run(["curl", "-sfL", "-o", f"fonts/{f}", u])

off, t, order = {}, 0.0, []
for o, src, ss, d, pad, xv, xa in SEG:
    tot = seg(o, src, ss, d, pad, xv, xa); off[o] = (t, ss); t += tot; order.append(o)
with open("list.txt", "w") as f:
    for o in order:
        f.write(f"file '{o}.mp4'\n")
run("ffmpeg -y -f concat -safe 0 -i list.txt -c copy concat.mp4")
print("TOTAL", round(t, 2)); print(json.dumps({k: round(v[0], 2) for k, v in off.items()}))


# ---- subtitles: the script's words at the review decode's clock ----
def ts(x):
    x = max(0, x); return f"{int(x // 3600)}:{int(x % 3600 // 60):02d}:{x % 60:05.2f}"


ev = []


def add(style, segname, a, b, text):
    base, ss = off[segname]; ev.append(f"Dialogue: 0,{ts(base + a - ss)},{ts(base + b - ss)},{style},,0,0,0,,{text}")


def card(segname, a, b, name, role, right=False):
    base, ss = off[segname]; s0, s1 = ts(base + a - ss), ts(base + b - ss)
    p1 = r"{\an9\pos(458,140)}" if right else r"{\an7\pos(22,140)}"
    p2 = r"{\an9\pos(458,196)}" if right else r"{\an7\pos(22,196)}"
    ev.append(f"Dialogue: 2,{s0},{s1},Name,,0,0,0,,{p1}{{\\fad(250,350)}}{name}")
    ev.append(f"Dialogue: 2,{s0},{s1},Role,,0,0,0,,{p2}{{\\fad(250,350)}}{role}")


# Line timings from the review of each take, overridable per cut: STT<n>='[[start,end],...]'
T1 = json.loads(os.environ.get("STT1", "[[3.5,5.6]]"))
add("Dlg", "s01", T1[0][0], T1[0][1] + 0.2, "RIVAL's line, as written in the script")
card("s01", 3.3, 6.0, "RIVAL", "the relationship in one phrase")
T2 = json.loads(os.environ.get("STT2", "[[8.5,11.5]]"))
add("VO", "s02b", T2[0][0], T2[0][1] + 0.3, "HERO's inner voice, as written")

ASS = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Dlg,<Sans family>,27,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,2.6,0.8,2,24,24,138,1
Style: VO,<Sans family>,26,&H00F5E8D6,&H000000FF,&H00000000,&H80000000,-1,-1,0,0,100,100,0,0,1,2.4,0.8,2,24,24,138,1
Style: Name,<Serif family>,50,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3.2,1,7,0,0,0,1
Style: Role,<Serif family>,23,&H0080D4F2,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,2.2,0.8,7,0,0,0,1
Style: Term,<Serif family>,24,&H00FFFFFF,&H000000FF,&H00000000,&HA0000000,-1,0,0,0,100,100,0,0,3,10,0,8,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(ev) + "\n"
open("subs.ass", "w", encoding="utf-8").write(ASS)
run('ffmpeg -y -i concat.mp4 -vf "subtitles=subs.ass:fontsdir=fonts" '
    '-af "aformat=channel_layouts=stereo,loudnorm=I=-16:TP=-1.5:LRA=11" '
    + " ".join(V) + " " + " ".join(A) + " " + OUT)
run(f'ffmpeg -y -i {OUT} -vf "fps=1/4,scale=200:-1,tile=6x7" -frames:v 1 -q:v 4 final_sheet.jpg')
print("DONE", OUT)
# Then: curl -f -X PUT -H "Content-Type: video/mp4" --upload-file $OUT "$UPLOAD_URL" (the URL read from a file), and media_confirm after HTTP 200.
