import struct, shutil, os

# ============================================================
# ACCF City Folk Deluxe - DOL Patcher
# USA Rev1 (RUUE01) - vWii / USB Loader GX
# No Riivolution needed!
# ============================================================
# Credits:
# - Aurum & ACCF Deluxe team for the mod
# - crediar, Vague Rant & TechieSaru for Classic Controller patch
# ============================================================

# ---- CONFIGURE YOUR PATHS HERE ----
EXTRACT_FOLDER = r"ACCF_extract"
MOD_FOLDER     = r"accf_deluxe"
# ------------------------------------

DOL    = os.path.join(EXTRACT_FOLDER, "DATA", "sys", "main.dol")
LOADER = os.path.join(MOD_FOLDER, "game", "Brewster", "loader.USA_REV_1.RELEASE.bin")
WPAD   = os.path.join(MOD_FOLDER, "game", "WPadCL", "wpadcl-usa-rev1-pgww.bin")
MODULE = os.path.join(MOD_FOLDER, "game", "Brewster", "module.USA_REV_1.RELEASE.kmdl")

print("=" * 60)
print("  ACCF City Folk Deluxe - Hard Patcher")
print("  USA Rev1 (RUUE01) - No Riivolution needed")
print("=" * 60)
print()

# Verify files
print("Checking files...")
all_ok = True
for path, name in [
    (DOL,    "main.dol"),
    (LOADER, "loader.USA_REV_1.RELEASE.bin"),
    (WPAD,   "wpadcl-usa-rev1-pgww.bin"),
    (MODULE, "module.USA_REV_1.RELEASE.kmdl"),
]:
    if not os.path.exists(path):
        print(f"  NOT FOUND: {path}")
        all_ok = False
    else:
        print(f"  Found: {name}")

if not all_ok:
    print("\nMissing files! Check your folder structure.")
    exit(1)

print()

# Backup
shutil.copy(DOL, DOL + ".bak")
print("Backup created: main.dol.bak")
print()

# Patch DOL
print("Patching main.dol...")

with open(DOL, 'rb') as f:
    dol = bytearray(f.read())

# PATCH 1 - Brewster Hook
# RAM 0x8016BC90 -> loader at 0x804B0970
dol[0x00166CB0:0x00166CB4] = bytes.fromhex("48344CE0")
print("  Hook written at 0x8016BC90")

# PATCH 2 - Inject loader.bin at 0x804B0970
with open(LOADER, 'rb') as lb:
    loader_data = lb.read()
dol[0x004ACA70:0x004ACA70 + len(loader_data)] = loader_data
print(f"  Loader injected ({len(loader_data)} bytes) at 0x804B0970")

# PATCH 3 - wpadcl.bin as new DOL section at 0x80001800
with open(WPAD, 'rb') as wb:
    wpad_data = wb.read()

pad = (32 - len(dol) % 32) % 32
dol += b'\x00' * pad
new_offset = len(dol)
dol += wpad_data
pad2 = (32 - len(dol) % 32) % 32
dol += b'\x00' * pad2

struct.pack_into('>I', dol, 0x1C + 8*4, new_offset)
struct.pack_into('>I', dol, 0x64 + 8*4, 0x80001800)
struct.pack_into('>I', dol, 0xAC + 8*4, len(wpad_data))
print(f"  wpadcl.bin injected ({len(wpad_data)} bytes) at 0x80001800")

# PATCH 4 - Classic Controller patches (from rvfp-usa-rev1.xml)
cc_patches = [
    (0x000F5644, "4BF071DC"),
    (0x000F56AC, "4BF0718C"),
    (0x002C92A4, "48000010"),
    (0x0043EF6C, "4BBBD8E4"),
    (0x0043EF88, "4BBBD8E0"),
    (0x003B99D8, "4BC42EA8"),
    (0x003BAA0C, "4BC41F44"),
]
for offset, value in cc_patches:
    dol[offset:offset+4] = bytes.fromhex(value)
print("  Classic Controller patches applied")

# Save DOL
with open(DOL, 'wb') as f:
    f.write(dol)

print()

# Copy mod files
print("Copying mod files to disc...")

files_dir = os.path.join(EXTRACT_FOLDER, "DATA", "files")
mod_game  = os.path.join(MOD_FOLDER, "game")

folders = ["AddItem", "Banner", "FgObj", "Item", "Layout", "Npc", "Other", "Prc"]
for folder in folders:
    src = os.path.join(mod_game, folder)
    dst = os.path.join(files_dir, folder)
    if os.path.exists(src):
        shutil.copytree(src, dst, dirs_exist_ok=True)
        print(f"  Copied {folder}/")
    else:
        print(f"  Not found: {folder}/ (skipping)")

# Script/E -> Script/ (USA region)
script_src = os.path.join(mod_game, "Script", "E")
script_dst = os.path.join(files_dir, "Script")
if os.path.exists(script_src):
    shutil.copytree(script_src, script_dst, dirs_exist_ok=True)
    print("  Copied Script/E/ -> Script/")
else:
    print("  Not found: Script/E/ (skipping)")

# module.kmdl to disc root
kmdl_dst = os.path.join(files_dir, "module.kmdl")
if os.path.exists(MODULE):
    shutil.copy(MODULE, kmdl_dst)
    print("  Copied module.kmdl to disc root")
else:
    print("  Not found: module.kmdl (skipping)")

print()

# Verification
print("Verifying patch...")
with open(DOL, 'rb') as f:
    v = f.read()

hook_ok   = v[0x00166CB0:0x00166CB4].hex() == "48344ce0"
loader_ok = v[0x004ACA70:0x004ACA71].hex() == loader_data[:1].hex()
kmdl_ok   = os.path.exists(kmdl_dst)

print(f"  Hook at 0x8016BC90:   {'OK' if hook_ok else 'ERROR'}")
print(f"  Loader at 0x804B0970: {'OK' if loader_ok else 'ERROR'}")
print(f"  module.kmdl at root:  {'OK' if kmdl_ok else 'ERROR'}")

print()
print("=" * 60)
if hook_ok and loader_ok and kmdl_ok:
    print("PATCH COMPLETE!")
    print()
    print("Rebuild your ISO:")
    print(f'  wit copy "{EXTRACT_FOLDER}" "ACCF_Deluxe_USA.wbfs" --wbfs')
    print()
    print("USB Loader GX settings:")
    print("  - Hooktype = None")
    print("  - Ocarina = Off")
else:
    print("PATCH INCOMPLETE - check errors above!")
print("=" * 60)
