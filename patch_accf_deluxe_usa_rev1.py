import struct, shutil, os

# ============================================================
# ACCF City Folk Deluxe - DOL Patcher (CORRECTED OFFSETS)
# For USA Rev1 (RUUE01) - Based on Dolphin Logs
# ============================================================

# ---- CONFIGURATION DES CHEMINS ----
EXTRACT_FOLDER = r"ACCF_extract"
MOD_FOLDER     = r"accf_deluxe"
# ------------------------------------

DOL    = os.path.join(EXTRACT_FOLDER, "DATA", "sys", "main.dol")
LOADER = os.path.join(MOD_FOLDER, "game", "Brewster", "loader.USA_REV_1.RELEASE.bin")
WPAD   = os.path.join(MOD_FOLDER, "game", "WPadCL", "wpadcl-usa-rev1-pgww.bin")
MODULE = os.path.join(MOD_FOLDER, "game", "Brewster", "module.USA_REV_1.RELEASE.kmdl")

print("🔍 Vérification des fichiers...")
if not os.path.exists(DOL):
    print(f"❌ Erreur: {DOL} introuvable !"); exit(1)

# Création du backup
if not os.path.exists(DOL + ".bak"):
    shutil.copy(DOL, DOL + ".bak")

with open(DOL, 'rb') as f:
    dol = bytearray(f.read())

print("🔧 Application des patchs avec les offsets corrigés...")

# 1. Brewster Hook (RAM 0x8016BC90)
# Offset fichier corrigé selon log Dolphin : 0x001A49B0
dol[0x001A49B0:0x001A49B4] = bytes.fromhex("48344CE0")
print("  ✅ Hook Brewster corrigé (0x001A49B0)")

# 2. Injection du Loader (RAM 0x804B0970)
# Offset fichier corrigé selon log Dolphin : 0x004EA770
with open(LOADER, 'rb') as lb:
    loader_data = lb.read()
dol[0x004EA770:0x004EA770 + len(loader_data)] = loader_data
print(f"  ✅ Loader injecté (0x004EA770)")

# 3. Injection WPADCL (Nouvelle section DOL)
with open(WPAD, 'rb') as wb:
    wpad_data = wb.read()
pad = (32 - len(dol) % 32) % 32
dol += b'\x00' * pad
new_offset = len(dol)
dol += wpad_data
struct.pack_into('>I', dol, 0x1C + 8*4, new_offset)    # File Offset
struct.pack_into('>I', dol, 0x64 + 8*4, 0x80001800)   # RAM Addr
struct.pack_into('>I', dol, 0xAC + 8*4, len(wpad_data)) # Size
print(f"  ✅ Section WPADCL ajoutée à 0x{new_offset:X}")

# 4. Patchs Manette Classique (Offsets recalculés)
# Formule : RAM - 0x800075C0 + 0x000402E0
cc_patches = [
    (0x00133344, "4BF071DC"), # RAM 0x800FA624
    (0x001333AC, "4BF0718C"), # RAM 0x800FA68C
    (0x00306FA4, "48000010"), # RAM 0x802CE284
    (0x0047CC6C, "4BBBD8E4"), # RAM 0x80443F4C
    (0x0047CC88, "4BBBD8E0"), # RAM 0x80443F68
    (0x003F76D8, "4BC42EA8"), # RAM 0x803BE9B8
    (0x003F870C, "4BC41F44"), # RAM 0x803BF9EC
]
for offset, value in cc_patches:
    dol[offset:offset+4] = bytes.fromhex(value)
print("  ✅ Patchs Classic Controller corrigés")

with open(DOL, 'wb') as f:
    f.write(dol)

# Copie du module.kmdl à la racine (Indispensable !)
files_dir = os.path.join(EXTRACT_FOLDER, "DATA", "files")
shutil.copy(MODULE, os.path.join(files_dir, "module.kmdl"))
print("  ✅ module.kmdl copié à la racine du disque")

print("\n🎉 TERMINÉ ! Reconstruis ton ISO et teste sur Dolphin.")
