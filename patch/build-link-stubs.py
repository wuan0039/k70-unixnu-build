#!/usr/bin/env python3
"""Archive the weak bring-up stubs for the kernel link.

The C source is embedded so the builder does not depend on how the device
repository's kits/ directory is copied into the build tree.
"""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / "build" / "link-stubs"
out.mkdir(parents=True, exist_ok=True)
source = out / "LinkStubs.c"
obj, archive = out / "LinkStubs.o", out / "libLinkStubs.a"

source.write_text(r'''
#include <stdint.h>
#define STUB __attribute__((weak))

void native_legacy_display_probe(void);
STUB void native_legacy_display_probe(void) {}

void boot_progress_poll(void);
STUB void boot_progress_poll(void) {}

int boot_progress_prepare_scanout(void);
STUB int boot_progress_prepare_scanout(void) { return 1; }

void boot_progress_cancel_scanout(void);
STUB void boot_progress_cancel_scanout(void) {}

void boot_progress_stage(const char *message);
STUB void boot_progress_stage(const char *message) { (void)message; }

int boot_progress_pulse_anchor(uintptr_t address, uint64_t bytes, unsigned width, unsigned height, unsigned row);
STUB int boot_progress_pulse_anchor(uintptr_t address, uint64_t bytes, unsigned width, unsigned height, unsigned row)
{
  (void)address; (void)bytes; (void)width; (void)height; (void)row;
  return 0;
}

int native_ufs_block_authenticates(void *provider, const char *uuid, uint8_t *digest);
STUB int native_ufs_block_authenticates(void *provider, const char *uuid, uint8_t *digest)
{
  (void)provider; (void)uuid; (void)digest;
  return -1;
}

unsigned native_ufs_store_mode(void);
STUB unsigned native_ufs_store_mode(void) { return 0; }

int native_ufs_store_open(uint64_t blocks, uint64_t *first, const char **why);
STUB int native_ufs_store_open(uint64_t blocks, uint64_t *first, const char **why)
{
  (void)blocks; (void)first;
  if (why) *why = "no UFS store on this board";
  return 0;
}

int native_ufs_store_read(uint64_t block, uint32_t count, void *buffer);
STUB int native_ufs_store_read(uint64_t block, uint32_t count, void *buffer)
{
  (void)block; (void)count; (void)buffer;
  return 0;
}

int native_ufs_store_write(uint64_t block, uint32_t count, const void *buffer);
STUB int native_ufs_store_write(uint64_t block, uint32_t count, const void *buffer)
{
  (void)block; (void)count; (void)buffer;
  return 0;
}

int native_ufs_store_sync(void);
STUB int native_ufs_store_sync(void) { return 0; }

unsigned native_ufs_store_gpt_check(void);
STUB unsigned native_ufs_store_gpt_check(void) { return 0; }
''')

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
