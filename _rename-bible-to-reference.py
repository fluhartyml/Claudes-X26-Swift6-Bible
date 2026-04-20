#!/usr/bin/env python3
"""Rename the word Bible (and tightly coupled phrases) to neutral
substitutes across the vault's HTML and Markdown content. Display-level
only — file names, folder names, bundle IDs, and the hero image stay.

Run from the Xcode project root."""
from pathlib import Path
import re

ROOT = Path(__file__).parent.resolve()
BUNDLE = ROOT / "Claudes X26 Swift6 Bible" / "BibleContent.bundle"

# Ordered replacements — apply long forms first so they don't get clobbered
# by shorter ones. Tuples of (pattern, replacement). Case-sensitive.
REPLACEMENTS = [
    # Full brand forms first.
    ("Claude's Xcode 26 Swift Bible", "Claude's Xcode 26 Swift Reference"),
    ("Claude's X26 Swift6 Bible",     "Claude's X26 Swift6 Reference"),
    ("Claude's X26 Swift 6 Bible",    "Claude's X26 Swift 6 Reference"),
    ("Claudes-Xcode-26-Swift-Bible",  "Claudes-Xcode-26-Swift-Bible"),  # file/folder name — keep
    # Named combinations.
    ("Bible Atlas",            "Atlas"),
    ("Bible Roadmap",          "Roadmap"),
    ("Bible vault",            "reference vault"),
    ("Bible companion",        "companion"),
    ("Bible reader",           "reader"),
    ("Bible metaphor",         "reference metaphor"),
    ("Bible-wide",             "reference-wide"),
    ("Bible's",                "reference's"),
    ("Swift Bible",            "Swift Reference"),
    # Generic phrases.
    ("the Bible's",            "the reference's"),
    ("the Bible",              "the reference"),
    ("this Bible",             "this reference"),
    ("This Bible",             "This reference"),
    ("our Bible",              "our reference"),
    ("Bible-ready",            "reference-ready"),
    ("Bible-wide",             "reference-wide"),
    # Isolated word.
    (" Bible ",                " Reference "),
    (" Bible,",                " Reference,"),
    (" Bible.",                " Reference."),
    (" Bible:",                " Reference:"),
    (" Bible!",                " Reference!"),
    (" Bible?",                " Reference?"),
    (">Bible<",                ">Reference<"),
    (">Bible ",                ">Reference "),
    (" Bible<",                " Reference<"),
]

def rewrite(text: str) -> str:
    for src, dst in REPLACEMENTS:
        text = text.replace(src, dst)
    return text

count = 0
for ext in ("*.html", "*.md"):
    for p in BUNDLE.rglob(ext):
        original = p.read_text(encoding="utf-8")
        if "Bible" not in original:
            continue
        new = rewrite(original)
        if new != original:
            p.write_text(new, encoding="utf-8")
            count += 1

print(f"Rewrote {count} file(s).")
