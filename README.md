# Finding a Starfield Scene

This page shows, step by step, how we traced a scene a player saw in Starfield back to the plugin records that build it, and how you can run the same search for any scene you spot. It was read from the game's own data files (game version 1.16.244).

**View it here:** https://taosecurity.github.io/starfield-scene-hunt/

- The first case is a player's report of a small site with people near a grave and flowers, thought to come from the Free Lanes update.
- The page gives each step of the search: what we ran, what it showed and the dead ends. It closes with the candidates and a verdict for each.
- Diagrams show the search itself and how Starfield builds a small procedural site out of nested pack-ins.
- "Run it yourself" lists the commands, and the page includes the full source of `cellwalk.py`, a small read-only Python script that finds which cell holds a placed object and lists what else is in it.

Richard Bejtlich of [Richard Presents Starfield Essentials](https://www.youtube.com/@RichardBejtlich) made this page. I am the developer, and Claude is the programmer. More Starfield tools and references are on the [Richard Presents Development Hub](https://taosecurity.github.io/).

## Notes

- This is an unofficial page, not made or endorsed by Bethesda. Starfield is a trademark of ZeniMax Media.
- The page shows only editor IDs, FormIDs and descriptions of what the records do. It holds no game code or game files.
- The search uses [SFSearch](https://github.com/Krawphish37/SFSearch) by Krawphish37 and a text dump made with [xEdit](https://github.com/TES5Edit/TES5Edit). Every tool on the page only reads the game files.
- The answer is a strong lead, not a confirmed match: the page lists what would settle it.

The page is a single self-contained `index.html` with no external dependencies. Its code (layout and `cellwalk.py`) is MIT licensed; see `LICENSE`.
