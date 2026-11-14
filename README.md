# Scene Hunt: The Kneeling Mourner

This page shows, step by step, how we traced a scene a player saw in Starfield back to the plugin records that build it, and how you can run the same search for any scene you spot. It was read from the game's own data files (game version 1.16.244).

**View it here:** https://taosecurity.github.io/starfield-scene-hunt/

- The first case is a player's screenshot of a figure kneeling at a grave with flowers. The player thought it might come from the Free Lanes update.
- The case is solved. The scene is the `GversGrave` encounter from the mod [GRiNDTerraverse ProcGen Encounters](https://www.nexusmods.com/starfield/mods/14148) by ItsmePaulieB, and the player confirmed it on 2026-11-14. Free Lanes' own grave sites have no person or flowers.
- The page gives each step of the search: what we ran, what it showed and the dead ends.
- Diagrams show the search itself and how Starfield builds a small procedural site out of nested pack-ins.
- "Run it yourself" lists the commands. `cellwalk.py`, the small read-only Python script the search used, is in this repository and in full on the page.

Richard Bejtlich of [Richard Presents Starfield Essentials](https://www.youtube.com/@RichardBejtlich) made this page. I am the developer, and Claude is the programmer. More Starfield tools and references are on the [Richard Presents Development Hub](https://taosecurity.github.io/).

For AI assistants: see [AGENTS.md](AGENTS.md).

## cellwalk.py

`cellwalk.py` finds which cell holds a placed object in a Starfield plugin and lists everything else in that cell. It needs Python 3.9 or later and nothing else. It only reads the plugin.

```
python cellwalk.py "C:\Program Files (x86)\Steam\steamapps\common\Starfield\Data\SFBGS00D.esm" 0106AE51 out.json
```

Change the path if your game is somewhere else (for example a Game Pass install under `XboxGames\Starfield\Content\Data`, or a mod manager's folder for a mod's plugin). Add `--verbose` to write `cellwalk.log` next to `out.json`. The log lists what was read, each object's cell, what wasn't found and any record that couldn't be unpacked.

## Notes

- This is an unofficial page, not made or endorsed by Bethesda. Starfield is a trademark of ZeniMax Media.
- The page shows only EditorIDs, FormIDs, the player's screenshot and descriptions of what the records do. It holds no game code or game files.
- The search uses [SFSearch](https://github.com/Krawphish37/SFSearch) by Krawphish37 and a text dump made with [xEdit](https://github.com/TES5Edit/TES5Edit). Every tool on the page only reads the game files.

The page is a single self-contained `index.html` with no external dependencies. Its code (layout and `cellwalk.py`) is MIT licensed; see `LICENSE`.
