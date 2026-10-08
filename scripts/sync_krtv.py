#!/usr/bin/env python3
"""Extract one exact M3U group; never overwrite the last good file on failure."""
import os
from pathlib import Path
import re
import tempfile
import time
from urllib.request import Request, urlopen

SOURCE = "https://raw.githubusercontent.com/krtv322/kortv/main/symftv.M3U"
GROUP = "🐉한국방송🦆"
DESTINATION = Path(__file__).resolve().parents[1] / "KRTV.m3u"
MAX_BYTES = 20 * 1024 * 1024


def extract(text):
    lines = text.lstrip("\ufeff").splitlines()
    if not lines or not re.match(r"^#EXTM3U(?:\s|$)", lines[0]):
        raise ValueError("Source is not an extended M3U playlist")
    selected = []
    block = []

    def finish():
        if not block:
            return
        match = re.search(r'\bgroup-title\s*=\s*"([^"]*)"', block[0])
        if not match or match.group(1) != GROUP:
            return
        urls = [line for line in block[1:] if line and not line.startswith("#")]
        if len(urls) != 1 or not re.match(r"^[A-Za-z][A-Za-z0-9+.-]*://\S+$", urls[0]):
            raise ValueError("Selected channel has a missing or invalid stream URL")
        selected.append("\n".join(block).rstrip())

    for line in lines[1:]:
        line = line.strip()
        if line.startswith("#EXTINF:"):
            finish()
            block = [line]
        elif block and line:
            block.append(line)
    finish()
    if not selected:
        raise ValueError(f"No channels found in exact group {GROUP!r}")
    return lines[0] + "\n" + "\n".join(selected) + "\n", len(selected)


def download():
    for attempt in range(3):
        try:
            request = Request(SOURCE, headers={"User-Agent": "KRTV-playlist-sync/1.0"})
            with urlopen(request, timeout=60) as response:
                data = response.read(MAX_BYTES + 1)
            if len(data) > MAX_BYTES:
                raise ValueError("Source exceeds size limit")
            return data.decode("utf-8-sig")
        except Exception:
            if attempt == 2:
                raise
            time.sleep(5 * (attempt + 1))


def main():
    result, count = extract(download())
    data = result.encode("utf-8")
    if DESTINATION.exists() and DESTINATION.read_bytes() == data:
        print(f"Unchanged: {count} channels in {GROUP}")
        return
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=DESTINATION.parent, delete=False) as handle:
            temporary = handle.name
            handle.write(data)
        os.replace(temporary, DESTINATION)
    finally:
        if temporary and os.path.exists(temporary):
            os.unlink(temporary)
    print(f"Updated: {count} channels in {GROUP}")


if __name__ == "__main__":
    main()
