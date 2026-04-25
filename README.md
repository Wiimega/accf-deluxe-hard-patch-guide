\# ACCF City Folk Deluxe - Hard Patch Guide



\### No **Riivolution** needed | Works on vWii/Wii via USB Loader GX



This guide and script permanently patch Animal Crossing City Folk directly into the ISO — no Riivolution, no physical disc needed. 



### ✅ Supported Versions: 

&#x20;   **EUR Rev0  (RUUP01)**

&#x20;   **USA Rev1  (RUUE01)**



\*(Make sure to use the correct Python script for your game region!)\*



\---



### \## ⚠️ Important — Read before running the script!



The script will \*\*NOT work\*\* if you just download and run it anywhere.



You MUST place the script inside `YourFolder/` with the correct structure:



```text

YourFolder/                  <- Create this folder anywhere on your PC

├── patch_accf_deluxe.py     <- Your script goes HERE (EUR or USA version)

├── ACCF_extract/            <- Your extracted ISO (via WIT)

└── accf_deluxe/             <- Your mod files (from the Riivolution SD zip)

```


The script looks for files \*\*relative to its own location\*\* — if the folders are not next to the script it will fail with "File not found" errors.



💡 If your folders have different names, you can easily fix it by asking an AI assistant (Claude, ChatGPT...):



> "Can you modify this Python script to change the folder paths to match mine?"



Just paste the script and tell it your folder names.





### ⚠️ Requirements

Python 3.8 or newer



WIT (Wiimms ISO Tools)



Your own legally dumped ACCF ISO: EUR Rev0 (RUUP01) OR USA Rev1 (RUUE01)



ACCF Deluxe mod files (from the official mod page)



If you need a version adapted for JPN or KOR, open an Issue on this GitHub repo with your Game ID.



## 📁 Folder Structure Required

Depending on your region, the mod files inside accf\_deluxe/game/ will have slightly different names. Do NOT rename any files manually — the script expects the official release names and handles everything automatically.


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
└── accf_deluxe/
    └── game/
        ├── Brewster/
        │   ├── loader.EUR_REV_0.RELEASE.bin   <- keep original name!  // loader.USA_REV_1.RELEASE.bin
        │   └── module.EUR_REV_0.RELEASE.kmdl  <- keep original name!  // module.USA_REV_1.RELEASE.kmdl
        ├── WPadCL/
        │   └── wpadcl-eur-rev0-pgww.bin       <- keep original name!  // wpadcl-usa-rev1-pgww.bin
        ├── AddItem/
        ├── Banner/
        ├── FgObj/
        ├── Item/
        ├── Layout/
        ├── Npc/
        ├── Other/
        ├── Prc/
        │   └── P.bin                          <- PAL version  // E.bin <- USA 
        └── Script/
            └── P/                             <- PAL/EUR region scripts  //  E/ 
```

### 📋 What the script does automatically

1. Patches main.dol:



* Writes a hook at 0x8016B81C pointing to the custom loader.



* Injects the Brewster loader binary directly into the DOL.



* Injects wpadcl.bin as a new DOL section at 0x80001800.



* Applies Classic Controller patches.







2\. Copies mod folders to DATA/files/ replacing originals:



* Standard assets: AddItem, Banner, FgObj, Item, Layout, Npc, Other.



* Region-specific data: Prc (P.bin or E.bin) and Script folders depending on your region.



3\. Copies module.kmdl to the root of DATA/files/ and automatically renames it to module.kmdl.





### ❔ How to use

Step 1 — Extract your ISO
````
For USA: wit extract RUUE01.iso ACCF\_extract
````
````
For EUR: wit extract RUUP01.iso ACCF\_extract
````


Step 2 — Run the correct script
````
For USA: python patch_accf_deluxe_usa_rev1.py
````
````
For EUR: python patch_accf_deluxe_eur_rev0.py
````


Step 3 — Rebuild the ISO
```text

wit copy ACCF_extract ACCF_Deluxe.wbfs --wbfs
```
```text
wit copy ACCF_extract ACCF_Deluxe.wbfs --wbfs

```

Step 4 — Copy to your USB drive and play!





### ⚠️/⚙️ USB Loader GX Settings

In USB Loader GX, go to the game settings for Animal Crossing:



Hooktype = None (very important!)



Ocarina = Off



Alternative DOL = Default





#### 👏 Credits

* Aurum \& the ACCF Deluxe team for the mod.

* crediar, Vague Rant \& TechieSaru for the Classic Controller patch.

* Wiimmfi \& WiiLink teams for online services.

## ❓ Troubleshooting

| Problem | Solution |
| :--- | :--- |
| **Blue bus freeze** | Check mod files are correctly copied |
| **Black screen** | Check Hooktype = None in USB Loader GX |
| **Game doesn't start** | Make sure you're using EUR Rev0 (RUUP01) or USA Rev1 (RUUE01) |
| **Script error** | Check your folder structure matches the one above |


