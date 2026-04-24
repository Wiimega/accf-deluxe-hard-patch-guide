# accf-deluxe-hard-patch-guide
### No Riivolution needed | Works on vWii via USB Loader GX

This script permanently patches Animal Crossing City Folk EUR Rev0 (RUUP01) | --------------- Script/P/ → copies all PAL languages (FRA, ENG, GER, ITA, ESP) to Script/. Your console will automatically use the correct language based on your system settings.
with the ACCF Deluxe mod directly into the ISO — no Riivolution, no physical disc needed.


## ⚠️ Important — Read before running the script!

The script **will NOT work** if you just download and run it anywhere!

You MUST place the script inside `YourFolder/` with the correct structure:
YourFolder/          ← create this folder anywhere on your PC
├── patch_accf_deluxe.py   ← script goes HERE
├── ACCF_extract/          ← your extracted ISO (via WIT)
└── accf_deluxe/           ← your mod files (from Riivolution SD)

The script looks for files **relative to its own location** — if the folders are not next to the script it will fail with "File not found" errors.

💡 **If your folders have different names**, you can easily fix it by asking an AI assistant (Claude, ChatGPT...):

> "Can you modify this Python script to change the folder paths to match mine?"

Just paste the script and tell it your folder names — it takes 10 seconds!



---

## ⚠️ Requirements

- Python 3.x
- WIT (Wiimms ISO Tools)
- Your own legally dumped ACCF EUR Rev0 ISO (RUUP01)    --- If you need a version adapted for USA, JPN or KOR, open an issue on the GitHub repo with your game ID and I'll update the script
- ACCF Deluxe mod files (from the official mod page)

---

## 📁 Folder Structure Required

Place the script in a folder with this structure:

```
YourFolder/
├── patch_accf_deluxe.py   ← this script
├── ACCF_extract/          ← your ISO extracted with WIT
│   └── DATA/
│       ├── sys/
│       │   └── main.dol
│       └── files/
│           ├── Script/
│           ├── Npc/
│           └── ... (original game files)
└── accf_deluxe/           ← mod files from Riivolution SD card
    └── game/
        ├── Brewster/
        │   ├── loader.EUR_REV_0.RELEASE.bin   ← keep original name!
        │   └── module.EUR_REV_0.RELEASE.kmdl  ← keep original name!
        ├── WPadCL/
        │   └── wpadcl-eur-rev0-pgww.bin       ← keep original name!
        ├── AddItem/
        ├── Banner/
        ├── FgObj/
        ├── Item/
        ├── Layout/
        ├── Npc/
        ├── Other/
        ├── Prc/
        │   └── P.bin                          ← PAL version
        └── Script/
            └── P/                             ← PAL/EUR region scripts
```

---

## ⚠️ DO NOT rename any files manually
The script handles everything automatically!

---

## 📋 What the script does automatically

1. **Patches main.dol:**
   - Injects Brewster loader at `0x804B0E30`
   - Writes hook at `0x8016B81C` → jumps to loader
   - Injects wpadcl.bin as new DOL section at `0x80001800`
   - Applies Classic Controller patches

2. **Copies mod folders** to `DATA/files/` replacing originals:
   - `AddItem`, `Banner`, `FgObj`, `Item`, `Layout`, `Npc`, `Other`
   - `Prc` → copies only `P.bin` (PAL version)
   - `Script/P/` → copies to `Script/` (PAL/EUR region)

3. **Copies module.kmdl** to the root of `DATA/files/`:
   - `module.EUR_REV_0.RELEASE.kmdl` → `DATA/files/module.kmdl`
   - This file must be at disc root — the script does this automatically!

### Note about .bin files
- `loader.EUR_REV_0.RELEASE.bin` → injected **directly into the DOL**, do NOT place it manually
- `wpadcl-eur-rev0-pgww.bin` → injected **directly into the DOL**, do NOT place it manually

---

##  How to use

### Step 1 — Extract your ISO
```
wit extract RUUP01.iso ACCF_extract
```

### Step 2 — Run the script
```
python patch_accf_deluxe.py
```

### Step 3 — Rebuild the ISO
```
wit copy ACCF_extract ACCF_Deluxe.wbfs --wbfs
```

### Step 4 — Copy to USB and play!

---

## USB Loader GX Settings (important!)

In USB Loader GX, go to game settings for Animal Crossing:
- **Hooktype = None** ← very important!
- **Ocarina = Off**
- **Alternative DOL = Default**

---

##  Credits

- **Aurum** & the ACCF Deluxe team for the amazing mod
- **crediar, Vague Rant & TechieSaru** for the Classic Controller patch
- Wiimmfi & WiiLink teams for online services

---

## ❓ Troubleshooting

| Problem | Solution |
|---|---|
| Blue bus freeze | Check mod files are correctly copied |
| Black screen | Check Hooktype = None in USB Loader GX |
| Game doesn't start | Make sure you're using EUR Rev0 (RUUP01) |
| Script error | Check your folder structure matches the one above |
