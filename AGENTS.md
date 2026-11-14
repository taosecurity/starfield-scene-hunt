# AGENTS.md: Scene Hunt

Instructions for AI assistants working with this repository.

1. **What it is:** a static web page (`index.html`, published with GitHub Pages at https://taosecurity.github.io/starfield-scene-hunt/) and one read-only Python script, `cellwalk.py`.
   - The page is a worked example of tracing a scene seen in Starfield to the plugin records that place it. Its first case, a figure kneeling at a grave, turned out to be the `GversGrave` pack-in of the mod GRiNDTerraverse ProcGen Encounters (Nexus 14148).
   - Use the page to learn the method: search for words, find the objects, list every place that uses them, then look at what sits next to each one.
   - Use `cellwalk.py` when you know a placed object's FormID and need its cell and the other objects in that cell.
2. **Prerequisites:** to view the page, any current web browser. For `cellwalk.py`, Python 3.9 or later (standard library only) and a Starfield plugin file (`.esm`). The page's other steps also use Git Bash (`grep`, `sort`, `uniq`) and [SFSearch](https://github.com/Krawphish37/SFSearch); see its README for that tool's install.
3. **Install:** none. Get a copy with `git clone https://github.com/taosecurity/starfield-scene-hunt.git`.
4. **Prove it works:** from the repo folder, run the line below. It prints the script's usage and exits with code 0.
   ```
   python cellwalk.py --help
   ```
5. **Common tasks:**
   - Find the cell of one placed object in Free Lanes (Steam install; change the path for Game Pass or a mod manager):
     ```
     python cellwalk.py "C:\Program Files (x86)\Steam\steamapps\common\Starfield\Data\SFBGS00D.esm" 0106AE51 out.json
     ```
     It prints `0106AE51 in cell 0106AE33 PackInFPIPCMManMadeSFFLPOI048StorageCell: 3 objects`.
   - Look up several objects and also list given cells: `python cellwalk.py <plugin.esm> 0106AE51,0106B135 out.json --cells 0106AE34,0106AE38`.
   - Troubleshoot a result: add `--verbose`.
6. **Inputs:** a plugin path; FormIDs as stored in that file, 8 hex digits, comma separated (the first two digits are the master index: in `SFBGS00D.esm`, `00` is Starfield.esm and `01` is the plugin's own records); an output path.
7. **Outputs:** one line per object on screen, `not found:` for FormIDs it didn't find, and a JSON file listing every object in each cell found: record type, FormID, base FormID, EditorID when the plugin names it, and position. With `--verbose`, `cellwalk.log` is written next to the JSON file.
8. **Exit codes:** 0 when it ran (even if some FormIDs weren't found); 1 with a message naming the problem when the plugin can't be read, isn't a plugin, or a FormID isn't hex; 2 for wrong arguments.
9. **Limits:**
   - It never writes to the game folder, never changes a plugin and never uploads anything. The page fetches nothing.
   - It reads one plugin at a time. It can't tell which mod wins in a load order or what the game places at runtime.
   - Base objects from a master (FormIDs starting `00` in an add-on) are named only if that plugin names them; look them up in the master with SFSearch.
   - Don't use it on save files or `.ba2` archives.
10. **Corrections:** open an issue at https://github.com/taosecurity/starfield-scene-hunt/issues.
