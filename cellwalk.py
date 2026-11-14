"""cellwalk.py - find which cell holds a placed object in a Starfield plugin, and list what else is in that cell.

Read-only. It reads one .esm file, unpacks compressed records, and never writes to the game folder.

Usage:
    python cellwalk.py <plugin.esm> <ref ids> <out.json> [--cells <cell ids>] [--verbose]

    <ref ids>    placed-object FormIDs as stored in the file, comma separated, 8 hex digits
                 (the first two digits are the master index: in SFBGS00D.esm 00 = Starfield.esm, 01 = its own records)
    <out.json>   where the full listing goes
    --cells      also list these cells, by FormID, even if no ref id points to them
    --verbose    also write cellwalk.log next to out.json: what was read, each ref's cell, what wasn't found,
                 and any compressed record that couldn't be unpacked (use it when a result looks wrong)

Example:
    python cellwalk.py "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Starfield\\Data\\SFBGS00D.esm" 0106AE51 out.json

For each ref it prints the cell FormID and EditorID and how many objects are in it. out.json holds every object in
those cells: record type, FormID, base FormID, EditorID if the plugin names it, and position.
"""
import argparse
import json
import os
import struct
import sys
import zlib

REF_TYPES = (b"REFR", b"ACHR")
CELL_GROUPS = (6, 8, 9, 10)  # GRUP types that belong to one cell: children, persistent, temporary, (exterior) children


def subrecords(buf):
    i, big = 0, None
    while i + 6 <= len(buf):
        t = buf[i:i + 4]
        sz = struct.unpack_from("<H", buf, i + 4)[0]
        i += 6
        if t == b"XXXX":  # next subrecord is bigger than 65535 bytes
            big = struct.unpack_from("<I", buf, i)[0]
            i += sz
            continue
        if big is not None:
            sz, big = big, None
        yield t, buf[i:i + sz]
        i += sz


def main():
    ap = argparse.ArgumentParser(description="Find the cells that hold placed objects in a Starfield plugin.")
    ap.add_argument("plugin")
    ap.add_argument("refs", help="comma-separated FormIDs, 8 hex digits as stored in the file")
    ap.add_argument("out")
    ap.add_argument("--cells", default="", help="comma-separated cell FormIDs to list as well")
    ap.add_argument("--verbose", action="store_true",
                    help="also write a log of what was read and found to cellwalk.log, next to the output file")
    a = ap.parse_args()
    log = []

    def note(msg):
        if a.verbose:
            log.append(msg)

    try:
        targets = {int(x, 16) for x in a.refs.split(",") if x}
        extra = [int(x, 16) for x in a.cells.split(",") if x]
    except ValueError:
        sys.exit("cellwalk: FormIDs must be hex, for example 0106AE51")
    try:
        data = open(a.plugin, "rb").read()
    except OSError as e:
        sys.exit(f"cellwalk: can't read {a.plugin}: {e.strerror}. Check the path to the .esm file.")
    if data[:4] != b"TES4":
        sys.exit(f"cellwalk: {a.plugin} doesn't start with a TES4 header, so it isn't a plugin file.")

    edids, cells, hits, bad = {}, {}, {}, 0

    def walk(start, end, stack):
        nonlocal bad
        i = start
        while i < end:
            sig = data[i:i + 4]
            size = struct.unpack_from("<I", data, i + 4)[0]
            if sig == b"GRUP":
                label, gtype = struct.unpack_from("<Ii", data, i + 8)
                walk(i + 24, i + size, stack + [label] if gtype in CELL_GROUPS else stack)
                i += size
                continue
            flags, fid = struct.unpack_from("<II", data, i + 8)
            body = data[i + 24:i + 24 + size]
            if flags & 0x40000:  # compressed: 4-byte unpacked size, then zlib
                try:
                    body = zlib.decompress(body[4:])
                except zlib.error:
                    bad += 1
                    note(f"could not unpack {sig.decode('ascii', 'replace')} {fid:08X} at byte {i}")
                    body = b""
            edid = base = pos = None
            for t, v in subrecords(body):
                if t == b"EDID":
                    edid = v.rstrip(b"\0").decode("utf-8", "replace")
                elif t == b"NAME" and sig in REF_TYPES and len(v) >= 4:
                    base = struct.unpack_from("<I", v)[0]
                elif t == b"DATA" and sig in REF_TYPES and len(v) >= 12:
                    pos = [round(x, 1) for x in struct.unpack_from("<3f", v)]
            if edid:
                edids[fid] = edid
            if sig in REF_TYPES and stack:
                cells.setdefault(stack[-1], []).append((sig.decode(), fid, base, edid, pos))
                if fid in targets:
                    hits[fid] = stack[-1]
            i += 24 + size

    note(f"read {a.plugin}: {len(data):,} bytes; looking for {len(targets)} refs and {len(extra)} cells")
    walk(24 + struct.unpack_from("<I", data, 4)[0], len(data), [])
    note(f"walked {len(edids):,} records with EditorIDs and {len(cells):,} cells holding placed objects")
    for c in extra:
        if c not in cells:
            note(f"cell {c:08X} from --cells holds no placed objects in this plugin")
        hits[c] = c
    for t, c in hits.items():
        note(f"{t:08X} -> cell {c:08X} {edids.get(c) or '(no EditorID)'}")

    res = {}
    for t, c in hits.items():
        refs = cells.get(c, [])
        res[f"{t:08X}"] = {
            "cell": f"{c:08X}", "cell_edid": edids.get(c),
            "refs": [[s, f"{f:08X}", f"{b:08X}" if b is not None else None, e or edids.get(b), p]
                     for s, f, b, e, p in refs],
        }
        print(f"{t:08X} in cell {c:08X} {edids.get(c) or '(no EditorID)'}: {len(refs)} objects")
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1)
    missing = sorted(targets - set(hits))
    if missing:
        print("not found:", ", ".join(f"{m:08X}" for m in missing))
    if bad:
        print(f"warning: {bad} compressed records could not be unpacked")
    print(f"full listing: {a.out}")
    if a.verbose:
        lp = os.path.join(os.path.dirname(os.path.abspath(a.out)), "cellwalk.log")
        note(f"not found: {', '.join(f'{m:08X}' for m in missing) or 'none'}; unreadable compressed records: {bad}")
        with open(lp, "w", encoding="utf-8") as f:
            f.write("\n".join(log) + "\n")
        print(f"log: {lp}")


if __name__ == "__main__":
    main()
