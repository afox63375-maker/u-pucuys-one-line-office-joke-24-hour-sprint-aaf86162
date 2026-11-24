#!/usr/bin/env python3
"""Entry for the make.fun bounty "One-Line Office Joke: 24-Hour Sprint".

The program carries a single one-line joke about office life, checks it
against the competition gate (UTF-8 text, 1 to 200 characters, not only
whitespace, one line) and writes it to entry.txt inside the output
directory named by MAKEFUN_OUTPUT_DIR (default /output).
"""

import os
import sys

# The whole entry: one line, setup first, punchline second.
JOKE = (
    "I blocked two hours of 'focus time' on my calendar; "
    "it now hosts a recurring meeting about why my projects are behind."
)

MAX_CHARS = 200


def validate(text: str) -> None:
    """Raise ValueError if the text would fail the competition gate."""
    if not text or not text.strip():
        raise ValueError("entry is empty or only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if len(text) > MAX_CHARS:
        raise ValueError(f"entry is {len(text)} characters, over {MAX_CHARS}")
    text.encode("utf-8")  # raises if the text cannot be encoded as UTF-8


def main() -> int:
    validate(JOKE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    payload = JOKE.encode("utf-8")
    with open(target, "wb") as fh:
        fh.write(payload)
    # Read the file back and confirm what landed on disk is byte for byte
    # the validated joke; a mismatch means the entry would be scored on
    # something other than the line above, so fail loudly instead.
    with open(target, "rb") as fh:
        written = fh.read()
    if written != payload:
        raise IOError(f"read-back mismatch: wrote {payload!r}, read {written!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
