#!/usr/bin/env python3
"""news-image-20261121 round 2 entrypoint.

Ships the pre-rendered front page. The judged image is a fixed PNG stored
next to this script; this program only copies it to the output path, using
the standard library only. No network, no rendering, no randomness: every
run writes byte-identical output.
"""

import hashlib
import os
import struct
import sys

EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
MAX_BYTES = 1024 * 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print("error:", message, file=sys.stderr)
    raise SystemExit(1)


def check_png(data):
    if len(data) < 33:
        fail("entry.png is too short to be a valid PNG")
    if data[:8] != PNG_MAGIC:
        fail("entry.png does not start with the PNG magic bytes")
    length, chunk_type = struct.unpack(">I4s", data[8:16])
    if chunk_type != b"IHDR" or length != 13:
        fail("entry.png has no valid IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if width != EXPECTED_WIDTH or height != EXPECTED_HEIGHT:
        fail("entry.png must be %dx%d, got %dx%d"
             % (EXPECTED_WIDTH, EXPECTED_HEIGHT, width, height))
    bit_depth, color_type = data[24], data[25]
    if bit_depth != 8 or color_type != 2:
        fail("entry.png must be 8-bit RGB, got bit depth %d color type %d"
             % (bit_depth, color_type))
    if len(data) > MAX_BYTES:
        fail("entry.png exceeds 1 MiB")


def main(argv):
    if len(argv) > 2:
        fail("usage: main.py [output_path]")
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    if len(argv) > 1:
        out_path = argv[1]
    else:
        out_path = "/output/entry.png"

    try:
        with open(source, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        fail("cannot read %s: %s" % (source, exc))

    check_png(data)

    parent = os.path.dirname(os.path.abspath(out_path))
    try:
        os.makedirs(parent, exist_ok=True)
    except OSError as exc:
        fail("cannot create output directory %s: %s" % (parent, exc))

    try:
        with open(out_path, "wb") as handle:
            handle.write(data)
    except OSError as exc:
        fail("cannot write %s: %s" % (out_path, exc))

    try:
        with open(out_path, "rb") as handle:
            written = handle.read()
    except OSError as exc:
        fail("cannot read back %s: %s" % (out_path, exc))

    if written != data:
        fail("read-back of %s does not match the source bytes" % out_path)
    if len(written) != len(data):
        fail("read-back size mismatch for %s" % out_path)

    digest = hashlib.sha256(written).hexdigest()
    print("wrote %s (%d bytes, sha256 %s)" % (out_path, len(written), digest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
