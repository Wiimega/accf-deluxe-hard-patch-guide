import struct, shutil, os

# ============================================================
# ACCF City Folk Deluxe - DOL Patcher (NO DATA FOLDER VERSION)
# ============================================================

EXTRACT_FOLDER = r"ACCF_extract"   
MOD_FOLDER     = r"accf_deluxe"    

# Chemins adaptés à TA structure (sans le dossier DATA)
DOL    = os.path.join(EXTRACT_FOLDER, "sys", "main.dol")
FILES_DIR = os.path.join(EXTRACT_FOLDER, "files")

# Fichiers du mod
LOADER = os.path.join(MOD_FOLDER, "game", "Brewster", "loader_USA_REV_1_RELEASE.bin")
WPAD   = os.path.join(MOD_FOLDER, "game", "WPadCL", "wpadcl-usa-rev1-pgww.bin")
MODULE = os.path.join(MOD_FOLDER, "game", "Brewster", "module_USA_REV_1_RELEASE.kmdl")

print("🔍 Checking files...")
all_ok = True
for path, name in [(DOL, "main.dol"), (LOADER, "loader"), (WPAD, "wpadcl"), (MODULE, "module")]:
    if not os.path.exists(path):
        print(f"  ❌ Not found: {path}")
        all_ok = False
    else:
        print(f"  ✅ Found: {name}")

if not all_ok:
    print("\n❌ Erreur : Certains fichiers sont introuvables. Vérifie les noms !")
    exit(1)

# --- Début du Patch ---
print("\n🔧 Patching main.dol...")
shutil.copy(DOL, DOL + ".bak")

with open(DOL, 'rb') as f:
    dol = bytearray(f.read())

# Brewster Hook
dol[0x00166CB0:0x00166CB4] = bytes.fromhex("48344CE0")

# Inject Loader
with open(LOADER, 'rb') as lb:
    loader_data = lb.read()
dol[0x004ACA70:0x004ACA70 + len(loader_data)] = loader_data

# Inject WPAD (Classic Controller)
with open(WPAD, 'rb') as wb:
    wpad_data = wb.read()
pad = (32 - len(dol) % 32) % 32
dol += b'\x00' * pad
new_offset = len(dol)
dol += wpad_data
struct.pack_into('>I', dol, 0x1C + 8*4, new_offset)
struct.pack_into('>I', dol, 0x64 + 8*4, 0x80001800)
struct.pack_into('>I', dol, 0xAC + 8*4, len(wpad_data))

# CC Patches
cc_patches = [(0x000F5644, "4BF071DC"),(0x000F56AC, "4BF0718C"),(0x002C92A4, "48000010"),(0x0043EF6C, "4BBBD8E4"),(0x0043EF88, "4BBBD8E0"),(0x003B99D8, "4BC42EA8"),(0x003BAA0C, "4BC41F44")]
for offset, value in cc_patches:
    dol[offset:offset+4] = bytes.fromhex(value)

with open(DOL, 'wb') as f:
    f.write(dol)

# --- Copie des dossiers ---
print("📁 Copying mod files...")
mod_game = os.path.join(MOD_FOLDER, "game")
folders = ["AddItem", "Banner", "FgObj", "Item", "Layout", "Npc", "Other", "Prc"]

for folder in folders:
    src = os.path.join(mod_game, folder)
    dst = os.path.join(FILES_DIR, folder)
    if os.path.exists(src):
        shutil.copytree(src, dst, dirs_exist_ok=True)
        print(f"  ✅ {folder} copied.")

# Script & Module
script_src = os.path.join(mod_game, "Script", "E")
if os.path.exists(script_src):
    shutil.copytree(script_src, os.path.join(FILES_DIR, "Script"), dirs_exist_ok=True)
shutil.copy(MODULE, os.path.join(FILES_DIR, "module.kmdl"))

print("\n🎉 PATCH COMPLETE ! Tu peux maintenant reconstruire l'ISO avec WIT.")
