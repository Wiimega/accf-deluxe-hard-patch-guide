import struct, shutil, os

# ============================================================
# ACCF City Folk Deluxe - DOL Patcher
# For EUR Rev0 (RUUP01) - vWii / USB Loader GX
# No Riivolution needed!
# ============================================================
# Credits:
# - Aurum & ACCF Deluxe team for the mod
# - crediar, Vague Rant & TechieSaru for Classic Controller patch
# ============================================================

# ---- CONFIGURE YOUR PATHS HERE ----
EXTRACT_FOLDER = r"ACCF_extract"   # WIT extract folder
MOD_FOLDER     = r"accf_deluxe"    # Mod folder (from Riivolution SD card)
# ------------------------------------

DOL    = os.path.join(EXTRACT_FOLDER, "DATA", "sys", "main.dol")
LOADER = os.path.join(MOD_FOLDER, "game", "Brewster", "loader.EUR_REV_0.RELEASE.bin")
WPAD   = os.path.join(MOD_FOLDER, "game", "WPadCL", "wpadcl-eur-rev0-pgww.bin")
MODULE = os.path.join(MOD_FOLDER, "game", "Brewster", "module.EUR_REV_0.RELEASE.kmdl")

print("=" * 60)
print("  ACCF City Folk Deluxe - Hard Patcher")
print("  EUR Rev0 (RUUP01) - No Riivolution needed")
print("=" * 60)
print()

# -------------------------------------------------------
# Verify all required files exist
# -------------------------------------------------------
print("🔍 Checking files...")
all_ok = True
for path, name in [
    (DOL,    "main.dol"),
    (LOADER, "loader.EUR_REV_0.RELEASE.bin"),
    (WPAD,   "wpadcl-eur-rev0-pgww.bin"),
    (MODULE, "module.EUR_REV_0.RELEASE.kmdl"),
]:
    if not os.path.exists(path):
        print(f"  ❌ Not found: {path}")
        all_ok = False
    else:
        print(f"  ✅ Found: {name}")

if not all_ok:
    print()
    print("❌ Missing files! Please check your folder structure.")
    print("   See README.md for details.")
    exit(1)

print()

# -------------------------------------------------------
# Backup original DOL
# -------------------------------------------------------
shutil.copy(DOL, DOL + ".bak")
print("✅ Backup created: main.dol.bak")
print()

# -------------------------------------------------------
# Patch the DOL
# -------------------------------------------------------
print("🔧 Patching main.dol...")

with open(DOL, 'r+b') as f:
    dol = bytearray(f.read())

    # PATCH 1 - Brewster Hook
    # addr 0x8016B81C -> jumps to 0x804B0E30 (loader)
    dol[0x0016683C:0x00166840] = bytes.fromhex("48345614")
    print("  ✅ Brewster hook written at 0x8016B81C")

    # PATCH 2 - Inject loader.bin at 0x804B0E30
    with open(LOADER, 'rb') as lb:
        loader_data = lb.read()
    dol[0x004ACF10:0x004ACF10 + len(loader_data)] = loader_data
    print(f"  ✅ Loader injected ({len(loader_data)} bytes) at 0x804B0E30")

    # PATCH 3 - Add wpadcl.bin as new DOL section at 0x80001800
    with open(WPAD, 'rb') as wb:
        wpad_data = wb.read()

    pad = (32 - len(dol) % 32) % 32
    dol += b'\x00' * pad
    new_offset = len(dol)
    dol += wpad_data
    pad2 = (32 - len(dol) % 32) % 32
    dol += b'\x00' * pad2

    # Write into free DATA slot [8]
    struct.pack_into('>I', dol, 0x1C + 8*4, new_offset)
    struct.pack_into('>I', dol, 0x64 + 8*4, 0x80001800)
    struct.pack_into('>I', dol, 0xAC + 8*4, len(wpad_data))
    print(f"  ✅ wpadcl.bin injected ({len(wpad_data)} bytes) at 0x80001800")

    # PATCH 4 - Classic Controller patches
    # by crediar, Vague Rant & TechieSaru
    cc_patches = [
        (0x000F57A4, "4BF0707C"),
        (0x000F580C, "4BF0702C"),
        (0x002C8FD0, "48000010"),
        (0x0043ECE8, "4BBBDB68"),
        (0x0043ED04, "4BBBDB64"),
        (0x003B95C0, "4BC432C0"),
        (0x003BA5F4, "4BC4235C"),
    ]
    for offset, value in cc_patches:
        dol[offset:offset+4] = bytes.fromhex(value)
    print(f"  ✅ Classic Controller patches applied")

    # Save patched DOL
    f.seek(0)
    f.write(dol)
    f.truncate()

print()

# -------------------------------------------------------
# Copy mod files to disc
# -------------------------------------------------------
print("📁 Copying mod files to disc...")

files_dir = os.path.join(EXTRACT_FOLDER, "DATA", "files")
mod_game  = os.path.join(MOD_FOLDER, "game")

# Copy standard folders (full content)
folders = ["AddItem", "Banner", "FgObj", "Item", "Layout", "Npc", "Other"]
for folder in folders:
    src = os.path.join(mod_game, folder)
    dst = os.path.join(files_dir, folder)
    if os.path.exists(src):
        shutil.copytree(src, dst, dirs_exist_ok=True)
        print(f"  ✅ Copied {folder}/")
    else:
        print(f"  ⚠️  Not found: {folder}/ (skipping)")

# Copy Prc - PAL version only (P.bin)
prc_src = os.path.join(mod_game, "Prc", "P.bin")
prc_dst = os.path.join(files_dir, "Prc", "P.bin")
os.makedirs(os.path.dirname(prc_dst), exist_ok=True)
if os.path.exists(prc_src):
    shutil.copy(prc_src, prc_dst)
    print(f"  ✅ Copied Prc/P.bin (PAL version)")
else:
    print(f"  ⚠️  Not found: Prc/P.bin (skipping)")

# Copy Script/P -> Script/ (PAL/EUR region)
script_src = os.path.join(mod_game, "Script", "P")
script_dst = os.path.join(files_dir, "Script")
if os.path.exists(script_src):
    shutil.copytree(script_src, script_dst, dirs_exist_ok=True)
    print(f"  ✅ Copied Script/P/ -> Script/")
else:
    print(f"  ⚠️  Not found: Script/P/ (skipping)")

# Copy module.kmdl to disc root
kmdl_dst = os.path.join(files_dir, "module.kmdl")
if os.path.exists(MODULE):
    shutil.copy(MODULE, kmdl_dst)
    print(f"  ✅ Copied module.kmdl to disc root")
else:
    print(f"  ⚠️  Not found: module.kmdl (skipping)")

print()

# -------------------------------------------------------
# Verification
# -------------------------------------------------------
print("🔍 Verifying patch...")
with open(DOL, 'rb') as f:
    v = f.read()

hook_ok   = v[0x0016683C:0x00166840].hex() == "48345614"
loader_ok = v[0x004ACF10:0x004ACF11].hex() == "94"
kmdl_ok   = os.path.exists(kmdl_dst)

print(f"  Hook at 0x8016B81C:  {'✅ OK' if hook_ok else '❌ ERROR'}")
print(f"  Loader at 0x804B0E30: {'✅ OK' if loader_ok else '❌ ERROR'}")
print(f"  module.kmdl at root:  {'✅ OK' if kmdl_ok else '❌ ERROR'}")

print()
print("=" * 60)
if hook_ok and loader_ok and kmdl_ok:
    print("🎉 PATCH COMPLETE!")
    print()
    print("Now rebuild your ISO with WIT:")
    print(f'  wit copy "{EXTRACT_FOLDER}" "ACCF_Deluxe.wbfs" --wbfs')
    print()
    print("⚠️  USB Loader GX settings:")
    print("  - Hooktype = None")
    print("  - Ocarina = Off")
else:
    print("❌ PATCH INCOMPLETE - check errors above!")
print("=" * 60)
