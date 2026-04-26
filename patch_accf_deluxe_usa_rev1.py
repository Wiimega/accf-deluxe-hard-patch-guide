import struct, shutil, os

# ============================================================
# ACCF City Folk Deluxe - DOL Patcher
# For USA Rev1 (RUUE01) - vWii / USB Loader GX
# No Riivolution needed!
# ============================================================
# Credits:
# - Aurum & ACCF Deluxe team for the mod
# - crediar, Vague Rant & TechieSaru for Classic Controller patch
# ============================================================

# ---- CONFIGURE YOUR PATHS HERE ----
EXTRACT_FOLDER = r"ACCF_extract"   # Your WIT/BrawlBox extract folder
MOD_FOLDER     = r"accf_deluxe"    # Mod folder (containing 'game' folder)

# File Paths
DOL     = os.path.join(EXTRACT_FOLDER, "sys", "main.dol")
LOADER  = os.path.join(MOD_FOLDER, "game", "Brewster", "loader.USA_REV_1.RELEASE.bin")
MODULE  = os.path.join(MOD_FOLDER, "game", "Brewster", "module.USA_REV_1.RELEASE.kmdl")
FILES_DIR = os.path.join(EXTRACT_FOLDER, "files")

def patch_dol():
    if not os.path.exists(DOL):
        print(f"❌ Error: {DOL} not found!")
        return

    print(f"🚀 Patching {DOL} for USA Rev1...")

    with open(DOL, 'rb+') as f:
        # 1. Main Hook (Brewster)
        # RAM: 0x8016BC90 -> File: 0x00166CB0
        # Value: 48344CE0 (b 0x804B0970)
        f.seek(0x00166CB0)
        f.write(struct.pack(">I", 0x48344CE0))
        print("  ✅ Core Hook applied.")

        # 2. Loader Injection
        # RAM: 0x804B0970 -> File: 0x004ACA70
        if os.path.exists(LOADER):
            with open(LOADER, 'rb') as l:
                loader_data = l.read()
            f.seek(0x004ACA70)
            f.write(loader_data)
            print(f"  ✅ Loader injected ({len(loader_data)} bytes).")
        else:
            print("  ⚠️ Warning: Loader .bin not found, skipping injection.")

        # 3. Classic Controller Patches (USA Rev1 specific)
        cc_patches = [
            (0x000F5644, 0x4BF071DC), # PadRead
            (0x003BC9D4, 0x00001800), # PadInit
            (0x003BCA14, 0x00001800), # PadSetSpec
            (0x003BCA30, 0x00001800), # PadGetType
        ]
        
        for offset, value in cc_patches:
            f.seek(offset)
            f.write(struct.pack(">I", value))
        print("  ✅ Classic Controller patches applied.")

    # 4. Copying External Files
    print("\n📂 Copying mod files to 'files' directory...")
    
    # Copy Script/E/ content to Script/
    script_src = os.path.join(MOD_FOLDER, "game", "Script", "E")
    script_dst = os.path.join(FILES_DIR, "Script")
    if os.path.exists(script_src):
        shutil.copytree(script_src, script_dst, dirs_exist_ok=True)
        print("  ✅ Script files updated.")

    # Copy module.kmdl to root
    kmdl_dst = os.path.join(FILES_DIR, "module.kmdl")
    if os.path.exists(MODULE):
        shutil.copy(MODULE, kmdl_dst)
        print("  ✅ module.kmdl copied.")

    print("\n✨ Done! You can now rebuild the ISO with WIT.")

if __name__ == "__main__":
    patch_dol()
