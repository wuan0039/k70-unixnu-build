// SPDX-License-Identifier: BSD-2-Clause-Patent
// Hooks referenced by the patched XNU when a component is left out of this
// bring-up configuration (NativeUfs is off for the UFS-less link test).
#include <stdint.h>

#define STUB __attribute__((weak))

// offline-component-load-probes.patch, bsd_init: called on offline-legacy-register=1
// whether or not NativeLegacyDisplay is linked.
void native_legacy_display_probe(void);
STUB void native_legacy_display_probe(void)
{
}

// Boot progress hooks referenced by the display/UFS paths.
void boot_progress_poll(void);
STUB void boot_progress_poll(void)
{
}

int boot_progress_prepare_scanout(void);
STUB int boot_progress_prepare_scanout(void)
{
  return 1;
}

void boot_progress_cancel_scanout(void);
STUB void boot_progress_cancel_scanout(void)
{
}

void boot_progress_stage(const char *message);
STUB void boot_progress_stage(const char *message)
{
  (void)message;
}

int boot_progress_pulse_anchor(uintptr_t address, uint64_t bytes, unsigned width, unsigned height, unsigned row);
STUB int boot_progress_pulse_anchor(uintptr_t address, uint64_t bytes, unsigned width, unsigned height, unsigned row)
{
  (void)address;
  (void)bytes;
  (void)width;
  (void)height;
  (void)row;
  return 0;
}

// UFS hooks other block transports reference when NativeUfs is absent.
int native_ufs_block_authenticates(void *provider, const char *uuid, uint8_t *digest);
STUB int native_ufs_block_authenticates(void *provider, const char *uuid, uint8_t *digest)
{
  (void)provider;
  (void)uuid;
  (void)digest;
  return -1;
}

unsigned native_ufs_store_mode(void);
STUB unsigned native_ufs_store_mode(void)
{
  return 0;
}

int native_ufs_store_open(uint64_t blocks, uint64_t *first, const char **why);
STUB int native_ufs_store_open(uint64_t blocks, uint64_t *first, const char **why)
{
  (void)blocks;
  (void)first;
  if (why)
    *why = "no UFS store on this board";
  return 0;
}

int native_ufs_store_read(uint64_t block, uint32_t count, void *buffer);
STUB int native_ufs_store_read(uint64_t block, uint32_t count, void *buffer)
{
  (void)block;
  (void)count;
  (void)buffer;
  return 0;
}

int native_ufs_store_write(uint64_t block, uint32_t count, const void *buffer);
STUB int native_ufs_store_write(uint64_t block, uint32_t count, const void *buffer)
{
  (void)block;
  (void)count;
  (void)buffer;
  return 0;
}

int native_ufs_store_sync(void);
STUB int native_ufs_store_sync(void)
{
  return 0;
}

unsigned native_ufs_store_gpt_check(void);
STUB unsigned native_ufs_store_gpt_check(void)
{
  return 0;
}
