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

├── patch\_accf\_deluxe.py     <- Your script goes HERE (EUR or USA version)

├── ACCF\_extract/            <- Your extracted ISO (via WIT)

└── accf\_deluxe/             <- Your mod files (from the Riivolution SD zip)



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



### 📁 Folder Structure Required

Depending on your region, the mod files inside accf\_deluxe/game/ will have slightly different names. Do NOT rename any files manually — the script expects the official release names and handles everything automatically.



##### For USA Rev1 (RUUE01) users:



YourFolder/

├── patch\_accf\_deluxe\_usa\_rev1.py

├── ACCF\_extract/

│   └── DATA/ ... (extracted game files)

└── accf\_deluxe/

&#x20;   └── game/

&#x20;       ├── Brewster/

&#x20;       │   ├── loader\_USA\_REV\_1\_RELEASE.bin

&#x20;       │   └── module\_USA\_REV\_1\_RELEASE.kmdl

&#x20;       ├── WPadCL/

&#x20;       │   └── wpadcl-usa-rev1-pgww.bin

&#x20;       ├── Prc/

&#x20;       │   └── E.bin                          <- USA/NTSC version

&#x20;       ├── Script/

&#x20;       │   └── E/                             <- USA/NTSC region scripts

&#x20;       └── AddItem/, Banner/, FgObj/, Item/, Layout/, Npc/, Other/







##### For EUR Rev0 (RUUP01) users:



YourFolder/

├── patch\_accf\_deluxe\_eur\_rev0.py

├── ACCF\_extract/

│   └── DATA/ ... (extracted game files)

└── accf\_deluxe/

&#x20;   └── game/

&#x20;       ├── Brewster/

&#x20;       │   ├── loader.EUR\_REV\_0.RELEASE.bin

&#x20;       │   └── module.EUR\_REV\_0.RELEASE.kmdl

&#x20;       ├── WPadCL/

&#x20;       │   └── wpadcl-eur-rev0-pgww.bin

&#x20;       ├── Prc/

&#x20;       │   └── P.bin                          <- PAL version

&#x20;       ├── Script/

&#x20;       │   └── P/                             <- PAL/EUR region scripts

&#x20;       └── AddItem/, Banner/, FgObj/, Item/, Layout/, Npc/, Other/



### 

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

For USA: wit extract RUUE01.iso ACCF\_extract

For EUR: wit extract RUUP01.iso ACCF\_extract



Step 2 — Run the correct script

For USA: python patch\_accf\_deluxe\_usa\_rev1.py

For EUR: python patch\_accf\_deluxe\_eur\_rev0.py



Step 3 — Rebuild the ISO

For USA: wit copy ACCF\_extract ACCF\_Deluxe\_USA.wbfs --wbfs

For EUR: wit copy ACCF\_extract ACCF\_Deluxe\_EUR.wbfs --wbfs



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





\\---



### &#x20; ❓Troubleshooting



|Problem|Solution|

|-|-|

|Blue bus freeze|Check that all mod files are correctly copied|

|Black screen|Check Hooktype = None in USB Loader GX|

|Game doesn't start|Make sure you are using EUR Rev0 (RUUP01)|

|Script error|Check your folder structure matches the one above|

























