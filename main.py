# A one-line out-of-office auto-reply, written in a houseplant's voice.
#
# Bounty: https://make.fun/bounty/u-eager-stork-81-9647-the-houseplant-out-of-office-7c586047
#
# This script drafts a dozen candidate replies, grades each one against the
# judge's brief, and writes the best-scoring line to /output/entry.txt. The
# grading weighs five qualities, in this order of importance: whether the line
# reads like a genuine out-of-office note from a plant, whether the joke is
# fresh and surprising, whether the plant's own daily life (water, roots,
# light, being forgotten on a sill) powers the joke, whether the line stays
# tight, and whether it avoids worn-out office phrases. The winner is picked
# by weighted total; when two drafts tie, the shorter line wins, then the one
# that sorts first alphabetically, so the result never depends on ordering
# or luck. Every run produces the same bytes.

import re
import sys
from dataclasses import dataclass
from pathlib import Path

ENTRY_PATH = Path("/output/entry.txt")
LIMIT = 120

WEIGHTS = {"voice": 3, "humour": 3, "plantlife": 2, "tightness": 1, "novelty": 1}


@dataclass(frozen=True)
class Draft:
    text: str
    voice: int
    humour: int
    plantlife: int
    tightness: int
    novelty: int

    def weighted_total(self) -> int:
        return (
            self.voice * WEIGHTS["voice"]
            + self.humour * WEIGHTS["humour"]
            + self.plantlife * WEIGHTS["plantlife"]
            + self.tightness * WEIGHTS["tightness"]
            + self.novelty * WEIGHTS["novelty"]
        )


DRAFTS = [
    Draft(
        text="I'm out of the office, slowly dying on the windowsill since March. Please water me — or don't. I can't leave.",
        voice=10,
        humour=10,
        plantlife=10,
        tightness=9,
        novelty=9,
    ),
    Draft(
        text="Out of office: I'm a fern on the windowsill, unwatered since March. Please allow 3-5 business days for a reply.",
        voice=9,
        humour=8,
        plantlife=9,
        tightness=8,
        novelty=8,
    ),
    Draft(
        text="Thank you for your email. I'm out of the office, root-bound in a pot nobody remembers. Reply after watering.",
        voice=9,
        humour=7,
        plantlife=9,
        tightness=8,
        novelty=7,
    ),
    Draft(
        text="I'm away, slowly turning brown on the windowsill. For urgent matters, water me. For anything else, also water me.",
        voice=9,
        humour=9,
        plantlife=9,
        tightness=7,
        novelty=8,
    ),
    Draft(
        text="Out of office until further notice. My owner left in March and took the watering can. I have seen the ceiling.",
        voice=8,
        humour=8,
        plantlife=7,
        tightness=8,
        novelty=8,
    ),
    Draft(
        text="Gone for the weekend. I'm a houseplant and I cannot leave this windowsill. Please water me before I wilt.",
        voice=8,
        humour=7,
        plantlife=8,
        tightness=8,
        novelty=7,
    ),
    Draft(
        text="I'm out of the office, reaching for sunlight I will never touch. Please water me. I've been patient since March.",
        voice=9,
        humour=7,
        plantlife=9,
        tightness=8,
        novelty=8,
    ),
    Draft(
        text="Auto-reply: this plant is out of the office and out of water. It has been March for a very long time. Send water.",
        voice=8,
        humour=8,
        plantlife=8,
        tightness=7,
        novelty=7,
    ),
    Draft(
        text="Thanks for writing. I'm a houseplant, out of the office since March, turning your unread emails into oxygen.",
        voice=9,
        humour=8,
        plantlife=9,
        tightness=7,
        novelty=9,
    ),
    Draft(
        text="Out of office: the fern has left the building. It hasn't. It can't. It is a fern. Please water it.",
        voice=8,
        humour=7,
        plantlife=8,
        tightness=8,
        novelty=7,
    ),
    Draft(
        text="I'm not ignoring you. I'm a houseplant, stuck on a windowsill since March, waiting for someone to notice I'm thirsty.",
        voice=9,
        humour=7,
        plantlife=8,
        tightness=8,
        novelty=7,
    ),
    Draft(
        text="This is an automated reply from your colleague, the houseplant. It is March. It has always been March. Water me.",
        voice=8,
        humour=9,
        plantlife=8,
        tightness=8,
        novelty=8,
    )]

SINGLE_LINE = re.compile(r"^[^\r\n]+$")


def rank_drafts(drafts):
    return sorted(
        drafts,
        key=lambda draft: (-draft.weighted_total(), len(draft.text), draft.text),
    )


def assert_entry_shape(line):
    if not SINGLE_LINE.match(line):
        raise SystemExit("entry must be exactly one line")
    if not 1 <= len(line) <= LIMIT:
        raise SystemExit(
            f"entry is {len(line)} characters; the gate allows 1-{LIMIT}"
        )
    if line != line.strip():
        raise SystemExit("entry must not start or end with whitespace")


def emit(line):
    ENTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    ENTRY_PATH.write_text(line, encoding="utf-8")
    roundtrip = ENTRY_PATH.read_text(encoding="utf-8")
    if roundtrip != line:
        raise SystemExit("entry.txt round-trip mismatch")


def main():
    for draft in DRAFTS:
        assert_entry_shape(draft.text)
    ordered = rank_drafts(DRAFTS)
    champion = ordered[0]
    assert_entry_shape(champion.text)
    emit(champion.text)
    print(
        f"entry ready: {len(champion.text)} characters, "
        f"score {champion.weighted_total()}/100"
    )


if __name__ == "__main__":
    main()
