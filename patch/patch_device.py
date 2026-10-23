#!/usr/bin/env python3
"""Patch the checked-out vermeer device repo for the UFS-less link test."""
import shutil
import sys
from pathlib import Path

dev = Path(sys.argv[1]).resolve()
if not (dev / "board.toml").is_file():
    raise SystemExit(f"not a device repo: {dev}")

cfg = dev / "configs" / "vermeer_defconfig"
text = cfg.read_text()
text = text.replace("CONFIG_XNU_NATIVE_UFS=y", "CONFIG_XNU_NATIVE_UFS=n")
if "CONFIG_XNU_EXTRA_LD_ARCHIVES" not in text:
    text = text.rstrip() + '\nCONFIG_XNU_EXTRA_LD_ARCHIVES="{tree}/build/link-stubs/libLinkStubs.a"\n'
cfg.write_text(text)

board = dev / "board.toml"
lines = board.read_text().splitlines()
if not any("build-link-stubs.py" in line for line in lines):
    index = max(i for i, line in enumerate(lines) if "build-libpthread-kernel.py" in line)
    lines.insert(index + 1, '  "build-link-stubs.py",')
    board.write_text("\n".join(lines) + "\n")

shutil.copy(Path(__file__).with_name("build-link-stubs.py"), dev / "scripts" / "build-link-stubs.py")
print(f"patched {dev}: UFS off, LinkStubs builder installed")
