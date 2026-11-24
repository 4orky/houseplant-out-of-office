#!/usr/bin/env python3
"""The Houseplant Out-of-Office -- make.fun bounty
u-eager-stork-81-9647-the-houseplant-out-of-office-7c586047

The program writes a single out-of-office auto-reply, as if a
houseplant had written it (1-120 characters), to /output/entry.txt.

Candidates were drafted against the judge's brief, in order of weight:
  1. reads as an out-of-office auto-reply a houseplant would send
  2. actually funny: a fresh joke that surprises, not a mild pun
  3. the plant's own life -- water, roots, sunlight, long stretches
     of being ignored -- drives the joke rather than decorating it
  4. tight: the joke lands inside 120 characters, no wasted words
  5. original: no office cliches, no worn-out auto-reply lines
Each candidate carries a hand-scored craft score (0-10 per criterion,
summed below); selection is deterministic: highest score wins, ties go
to the shorter text. The output is byte-identical on every run.
"""

import os

CANDIDATES = [
    # score: ooo 10, funny 10, plant-life 10, tight 10, original 9 = 49
    {
        "text": "I'm out of the office, slowly dying on the windowsill since March. Please water me — or don't. I can't leave.",
        "score": 49,
    },
    # score: ooo 9, funny 9, plant-life 10, tight 9, original 9 = 46
    {
        "text": "I'm out of the office, photosynthesizing. Please water me and allow 3-5 business days for a reply. I am a fern.",
        "score": 46,
    },
    # score: ooo 10, funny 9, plant-life 9, tight 8, original 9 = 45
    {
        "text": "Out of office: I've been on this windowsill since March, unwatered and unbothered. For urgent matters, please water me.",
        "score": 45,
    },
    # score: ooo 10, funny 8, plant-life 9, tight 9, original 8 = 44
    {
        "text": "Thanks for your email. I'm currently out of the office, being slowly forgotten on a windowsill. Please water me.",
        "score": 44,
    },
    # score: ooo 10, funny 8, plant-life 9, tight 8, original 8 = 43
    {
        "text": "Thank you for your email. I'm a fern, out of the office since March. Nobody waters me. I'll reply when I'm watered.",
        "score": 43,
    },
]


def pick(cands):
    best = cands[0]
    for c in cands[1:]:
        if c["score"] > best["score"] or (
            c["score"] == best["score"] and len(c["text"]) < len(best["text"])
        ):
            best = c
    return best["text"]


LINE = pick(CANDIDATES)

# The gate requires 1-120 characters of non-whitespace UTF-8 text in a
# single line. Validate before writing, then read the file back and
# confirm it holds exactly the chosen line, byte for byte.
if len(LINE) < 1 or len(LINE) > 120:
    raise SystemExit(f"line is {len(LINE)} characters, gate requires 1-120")
if LINE.strip() == "" or "\n" in LINE:
    raise SystemExit("line must be a single non-empty line")

os.makedirs("/output", exist_ok=True)
with open("/output/entry.txt", "w", encoding="utf-8") as f:
    f.write(LINE)
with open("/output/entry.txt", "r", encoding="utf-8") as f:
    written = f.read()
if written != LINE:
    raise SystemExit("entry.txt does not match the chosen line")
print(f"wrote {len(written)} characters to /output/entry.txt")
