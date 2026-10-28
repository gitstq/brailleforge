"""BrailleForge command line interface (stdlib argparse only)."""
from __future__ import annotations
import argparse, json, sys
from . import core

def _read(args) -> str:
    if getattr(args, "file", None):
        with open(args.file, encoding="utf-8") as f:
            return f.read().rstrip("\n")
    if getattr(args, "text", None) is not None:
        return args.text
    return sys.stdin.read().rstrip("\n")

def _write(args, data: str) -> None:
    if getattr(args, "output", None):
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(data)
    else:
        print(data)

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="brailleforge", description="Offline Grade 1 braille toolkit: text / Unicode braille / dot notation / Braille ASCII / BRF")
    sub = p.add_subparsers(dest="cmd", required=True)
    def add(name, **kw):
        s = sub.add_parser(name, **kw)
        s.add_argument("text", nargs="?", help="input text (or use -f / stdin)")
        s.add_argument("-f", "--file", help="read input from file")
        s.add_argument("-o", "--output", help="write output to file instead of stdout")
        return s
    add("encode", help="plain text -> Unicode braille")
    add("decode", help="Unicode braille -> plain text")
    add("to-ascii", help="Unicode braille -> Braille ASCII")
    add("from-ascii", help="Braille ASCII -> Unicode braille")
    add("to-dots", help="Unicode braille -> dot notation, e.g. 125-15")
    add("from-dots", help="dot notation -> Unicode braille")
    s = add("inspect", help="draw every cell as a dot grid")
    s = add("brf", help="plain text -> formatted .brf (Braille ASCII)")
    s.add_argument("--width", type=int, default=40)
    s.add_argument("--lines-per-page", type=int, default=25)
    add("unbrf", help=".brf (Braille ASCII) -> plain text")
    add("stats", help="cell / word / page statistics (JSON)")
    sub.add_parser("demo", help="print a short self-demonstration")
    return p

def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    if args.cmd == "demo":
        sample = "Braille Forge 2026: read by touch!"
        br = core.encode(sample)
        print(f"text:     {sample}")
        print(f"braille:  {br}")
        print(f"dots:     {core.braille_to_dots(br)}")
        print(f"ascii:    {core.unicode_to_braille_ascii(br)}")
        print(f"roundtrip:{core.decode(br)}")
        return 0
    data = _read(args)
    try:
        if args.cmd == "encode":
            _write(args, core.encode(data))
        elif args.cmd == "decode":
            _write(args, core.decode(data))
        elif args.cmd == "to-ascii":
            _write(args, core.unicode_to_braille_ascii(data))
        elif args.cmd == "from-ascii":
            _write(args, core.braille_ascii_to_unicode(data))
        elif args.cmd == "to-dots":
            _write(args, core.braille_to_dots(data))
        elif args.cmd == "from-dots":
            _write(args, core.dots_to_braille(data))
        elif args.cmd == "inspect":
            _write(args, "\n\n".join(core.inspect_cell(c) for c in data if c not in ("\n",)))
        elif args.cmd == "brf":
            _write(args, core.format_brf(core.encode(data), width=args.width, lines_per_page=args.lines_per_page))
        elif args.cmd == "unbrf":
            _write(args, core.decode(core.parse_brf(data)))
        elif args.cmd == "stats":
            br = data if data and all(0x2800 <= ord(c) <= 0x28FF or c in " \n" for c in data) else core.encode(data)
            _write(args, json.dumps(core.stats(br), ensure_ascii=False, indent=2))
    except (ValueError, OSError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
