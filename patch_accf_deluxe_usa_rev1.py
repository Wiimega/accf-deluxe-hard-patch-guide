
import struct, shutil, os

# ============================================================
# ACCF City Folk Deluxe - DOL Patcher
# USA Rev1 (RUUE01) - vWii / USB Loader GX
# ============================================================

EXTRACT_FOLDER = r"ACCF_extract"
MOD_FOLDER     = r"accf_deluxe"

DOL = os.path.join(EXTRACT_FOLDER, "DATA", "sys", "main.dol")

# ✅ NOMS CORRECTS (avec . et pas _)
LOADER = os.path.join(MOD_FOLDER, "game", "Brewster", "loader.USA_REV_1.RELEASE.bin")
WPAD   = os.path.join(MOD_FOLDER, "game", "WPadCL", "wpadcl-usa-rev1-pgww.bin")
MODULE = os.path.join(MOD_FOLDER, "game", "Brewster", "module.USA_REV_1.RELEASE.kmdl")

print("=" * 60)
print("ACCF Deluxe - USA Rev1 Patcher")
print("=" * 60)

# -------------------------------------------------------
# Vérification fichiers
# -------------------------------------------------------
print("\n🔍 Checking files...")
all_ok = True

for path, name in [
    (DOL, "main.dol"),
    (LOADER, "loader"),
    (WPAD, "wpad"),
    (MODULE, "module"),
]:
    if not os.path.exists(path):
        print(f"❌ Not found: {path}")
        all_ok = False
    else:
        print(f"✅ Found: {name}")

if not all_ok:
    print("\n❌ Missing files. Fix paths.")
    exit(1)

# -------------------------------------------------------
# Backup
# -------------------------------------------------------
shutil.copy(DOL, DOL + ".bak")
print("\n✅ Backup created")

# -------------------------------------------------------
# Patch DOL
# -------------------------------------------------------
print("\n🔧 Patching main.dol...")

with open(DOL, 'rb') as f:
    dol = bytearray(f.read())

# Hook (Brewster)
dol[0x00166CB0:0x00166CB4] = bytes.fromhex("48344CE0")
print("✅ Hook OK")

# Injection loader
with open(LOADER, 'rb') as lb:
    loader_data = lb.read()

dol[0x004ACA70:0x004ACA70 + len(loader_data)] = loader_data
print(f"✅ Loader injected ({len(loader_data)} bytes)")

# Injection WPAD (nouvelle section DOL)
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
print("✅ WPAD injected")

# Sauvegarde DOL
with open(DOL, 'wb') as f:
    f.write(dol)

# -------------------------------------------------------
# Copie des fichiers du mod
# -------------------------------------------------------
print("\n📁 Copying mod files...")

files_dir = os.path.join(EXTRACT_FOLDER, "DATA", "files")
mod_game  = os.path.join(MOD_FOLDER, "game")

folders = ["AddItem","Banner","FgObj","Item","Layout","Npc","Other","Prc"]

for folder in folders:
    src = os.path.join(mod_game, folder)
    dst = os.path.join(files_dir, folder)
    if os.path.exists(src):
        shutil.copytree(src, dst, dirs_exist_ok=True)
        print(f"✅ {folder}/")

# Script/E → Script
script_src = os.path.join(mod_game, "Script", "E")
script_dst = os.path.join(files_dir, "Script")

if os.path.exists(script_src):
    shutil.copytree(script_src, script_dst, dirs_exist_ok=True)
    print("✅ Script/")

# module.kmdl à la racine
kmdl_dst = os.path.join(files_dir, "module.kmdl")
shutil.copy(MODULE, kmdl_dst)
print("✅ module.kmdl copied")

print("\n🎉 PATCH COMPLETE")
print("Rebuild avec:")
print(f'wit copy "{EXTRACT_FOLDER}" "ACCF_Deluxe_USA.wbfs" --wbfs')

