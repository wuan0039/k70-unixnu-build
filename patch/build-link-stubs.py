#!/usr/bin/env python3
"""Archive the weak bring-up stubs for the kernel link."""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "kits" / "vermeer" / "LinkStubs.c"
out = ROOT / "build" / "link-stubs"
out.mkdir(parents=True, exist_ok=True)
obj, archive = out / "LinkStubs.o", out / "libLinkStubs.a"
subprocess.run(
    [
        "xcrun", "--sdk", "iphoneos", "clang", "-arch", "arm64", "-mkernel",
        "-miphoneos-version-min=17.0", "-Os", "-Wall", "-Werror",
        "-c", str(source), "-o", str(obj),
    ],
    check=True,
)
archive.unlink(missing_ok=True)
subprocess.run(["xcrun", "ar", "rcs", str(archive), str(obj)], check=True)
print(archive)
