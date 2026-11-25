#!/usr/bin/env python3
"""One Star, Written in Sap — make.fun entry.

Writes a single one-line 1-star review, in the voice of a houseplant
reviewing its human owner, to $MAKEFUN_OUTPUT_DIR/entry.txt
(falling back to /output/entry.txt).

The line was chosen from 36 candidates scored 1-5 on each of the judge
brief's five criteria (see candidates.md); the winner scored 25/25, the
only perfect score. Deterministic: no network, no randomness, no time or
environment dependence — two runs produce byte-identical output.
"""

import hashlib
import os
import sys

ENTRY = (
    'One star. My owner thinks "indirect light" means "behind the '
    'bookshelf," and I have been photosynthesizing out of spite for a year.'
)

# sha256 of ENTRY.encode("utf-8") — the write-back check recomputes it
# and refuses to exit 0 on any drift, so a silently altered entry.txt
# can never ship. Verified: 6daa8440...980b2 over 131 bytes.
EXPECTED_SHA256 = (
    "6daa8440568ee91a652bfb7fbe4fd221b89f15da06a8e0e9c308b79e05c980b2"
)

# Gate (competition.yaml: /output/entry.txt must be UTF-8 text of
# 1 to 279 characters, not only white space). Enforced at import time
# so a bad ENTRY fails loudly instead of shipping an invalid entry.
if not (1 <= len(ENTRY) <= 279):
    raise ValueError(f"ENTRY is {len(ENTRY)} chars; gate requires 1-279")
if not ENTRY.strip():
    raise ValueError("ENTRY is whitespace-only")
if "\n" in ENTRY or "\r" in ENTRY:
    raise ValueError("ENTRY must be a single line")
if "http://" in ENTRY or "https://" in ENTRY or "[" in ENTRY:
    raise ValueError("ENTRY must contain no links or markdown")


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = ENTRY.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    # Write-back self-check: read the file back and verify it is exactly
    # the entry we meant to ship.
    with open(path, "rb") as f:
        back = f.read()
    if back != data:
        raise OSError("write-back mismatch: entry.txt differs from ENTRY")
    if len(back.decode("utf-8")) != len(ENTRY):
        raise OSError("write-back mismatch: character count differs")
    if hashlib.sha256(back).hexdigest() != EXPECTED_SHA256:
        raise OSError("write-back mismatch: sha256 digest differs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
