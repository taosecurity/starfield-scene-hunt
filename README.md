# Scene Hunt: The Kneeling Mourner

Scene Hunt shows, step by step, how we traced a scene a player saw in Starfield back to the plugin records that build it, and how you can run the same search for any scene you spot. It was read from the game's own data files (game version 1.16.244).

Open the site: https://taosecurity.github.io/starfield-scene-hunt/

For AI assistants: step-by-step instructions are in [AGENTS.md](AGENTS.md).

## Example

`cellwalk.py`, the small script in this repository, finds the cell that holds one placed object and lists everything else in that cell. Here it looks up the object `0106AE51` in the Free Lanes plugin, `SFBGS00D.esm`, on a Steam install:

    > python cellwalk.py "C:\Program Files (x86)\Steam\steamapps\common\Starfield\Data\SFBGS00D.esm" 0106AE51 out.json
    0106AE51 in cell 0106AE33 PackInFPIPCMManMadeSFFLPOI048StorageCell: 3 objects
    full listing: out.json

The object sits in the storage cell of a Free Lanes pack-in, together with two other objects. `out.json` lists all three, each with its record type, FormID, base object's FormID and position.

What's new: see the top of the [live page](https://taosecurity.github.io/starfield-scene-hunt/).

## What the page shows

- The first case is a player's screenshot of a figure kneeling at a grave with flowers. The player thought it might come from the Free Lanes update.
- The case is solved. The scene is the `GversGrave` encounter from the mod [GRiNDTerraverse ProcGen Encounters](https://www.nexusmods.com/starfield/mods/14148) by ItsmePaulieB, and the player confirmed it on 2026-11-14. Free Lanes' own grave sites have no person or flowers.
- The page gives each step of the search: what we ran, what it showed and the dead ends.
- Diagrams show the search itself and how Starfield builds a small procedural site out of nested pack-ins.
- "Run it yourself" lists the commands. `cellwalk.py`, the small read-only Python script the search used, is in this repository and in full on the page.

## Install cellwalk.py

`cellwalk.py` needs Python 3.9 or later and nothing else. It only reads the plugin.

1. Install Python 3.11 or newer from [python.org](https://www.python.org/downloads/). On the first screen of the installer, tick **Add python.exe to PATH**. To check that it worked, open a new Command Prompt and type `python --version`. It should print a version number.
2. Download `cellwalk.py` from this repository (click it, then the download button) into a folder of your choice.
3. Open the folder in File Explorer, click the address bar at the top, type `cmd` and press Enter. A Command Prompt window opens in that folder, ready for the command in the Example.

Change the plugin path if your game is somewhere else. A Game Pass install keeps it under `XboxGames\Starfield\Content\Data`. For a mod's plugin, use the folder where your mod manager (Vortex or MO2) keeps that mod's files.

## Words used here

- **Plugin:** a mod's data file (`.esm`, `.esp` or `.esl`). It adds or changes records in the game. Free Lanes is the official plugin `SFBGS00D.esm`.
- **Master:** a plugin that another plugin needs loaded before it. Starfield.esm is the master of nearly every mod.
- **Record:** one thing in a plugin, such as a weapon, a quest, a location or a setting.
- **FormID:** a record's number, such as `0106AE51`. The first two digits depend on the load order.
- **EditorID:** a record's readable name, such as `GversGrave`, used by the Creation Kit and xEdit.
- **Cell:** one area of the game world, such as an interior or a patch of a planet's surface. Every placed object belongs to one cell.
- **Pack-in:** a prefab group of placed objects, such as a grave, its flowers and a marker, that the game reuses in many places. Its objects are kept in a storage cell of their own.
- **xEdit (SF1Edit):** a community tool for viewing and editing plugins record by record.

## The log

Add `--verbose` to write `cellwalk.log` next to `out.json`. The log lists what was read, each object's cell, what wasn't found and any record that couldn't be unpacked.

## Notes

- The page shows only EditorIDs, FormIDs, the player's screenshot and descriptions of what the records do. It holds no game code or game files.
- The search uses [SFSearch](https://github.com/Krawphish37/SFSearch) by Krawphish37 and a text dump made with [xEdit](https://github.com/TES5Edit/TES5Edit). Every tool on the page only reads the game files.

Found a mistake? Open an issue: https://github.com/taosecurity/starfield-scene-hunt/issues

## Credits and License

Richard Bejtlich of [Richard Presents Starfield Essentials](https://www.youtube.com/@RichardBejtlich) made this page. I am the developer, and Claude is the programmer. More Starfield tools and references are on the [Richard Presents Development Hub](https://taosecurity.github.io/).

This is an unofficial page, not made or endorsed by Bethesda. Starfield is a trademark of ZeniMax Media.

The page is a single self-contained `index.html` with no external dependencies. Its code (layout and `cellwalk.py`) is MIT licensed; see [LICENSE](LICENSE).
