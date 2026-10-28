"""BrailleForge core: English Grade 1 (uncontracted) braille conversion.

Independent implementation based on the public braille cell system:
- 6-dot cells, dots numbered 1-2-3 (left, top to bottom) and 4-5-6 (right).
- Unicode Braille Patterns block U+2800..U+283F.
- Braille ASCII table (the C string published for U+2800..U+283F in order),
  used by .brf (Braille Ready Format) files for embossers / refreshable displays.

Scope: uncontracted English braille (letters, digits, common punctuation),
capital / number signs, dot notation, Braille ASCII, BRF formatting.
Grade 2 contractions are intentionally out of scope (see README roadmap).
"""
from __future__ import annotations

BRAILLE_BASE = 0x2800
CAPITAL_SIGN = "\u2820"   # dots 6
NUMBER_SIGN = "\u283c"    # dots 3-4-5-6
LETTER_SIGN = "\u2830"    # dots 5-6, ends numeric mode before a-j

def cell(*dots: int) -> str:
    bits = 0
    for d in dots:
        if d < 1 or d > 6:
            raise ValueError(f"dot out of range: {d}")
        bits |= 1 << (d - 1)
    return chr(BRAILLE_BASE + bits)

def cell_dots(ch: str) -> tuple[int, ...]:
    if len(ch) != 1 or not (BRAILLE_BASE <= ord(ch) <= BRAILLE_BASE + 0x3F):
        raise ValueError(f"not a 6-dot braille pattern: {ch!r}")
    bits = ord(ch) - BRAILLE_BASE
    return tuple(d for d in range(1, 7) if bits & (1 << (d - 1)))

LETTER_DOTS = {
    "a": (1,), "b": (1, 2), "c": (1, 4), "d": (1, 4, 5), "e": (1, 5),
    "f": (1, 2, 4), "g": (1, 2, 4, 5), "h": (1, 2, 5), "i": (2, 4),
    "j": (2, 4, 5), "k": (1, 3), "l": (1, 2, 3), "m": (1, 3, 4),
    "n": (1, 3, 4, 5), "o": (1, 3, 5), "p": (1, 2, 3, 4),
    "q": (1, 2, 3, 4, 5), "r": (1, 2, 3, 5), "s": (2, 3, 4),
    "t": (2, 3, 4, 5), "u": (1, 3, 6), "v": (1, 2, 3, 6),
    "w": (2, 4, 5, 6), "x": (1, 3, 4, 6), "y": (1, 3, 4, 5, 6),
    "z": (1, 3, 5, 6),
}
LETTERS = {ch: cell(*dots) for ch, dots in LETTER_DOTS.items()}
CELL_TO_LETTER = {v: k for k, v in LETTERS.items()}
DIGIT_TO_LETTER = {"1": "a", "2": "b", "3": "c", "4": "d", "5": "e",
                   "6": "f", "7": "g", "8": "h", "9": "i", "0": "j"}
LETTER_TO_DIGIT = {v: k for k, v in DIGIT_TO_LETTER.items()}

PUNCT_DOTS = {
    ",": (2,), ";": (2, 3), ":": (2, 5), ".": (2, 5, 6),
    "?": (2, 3, 6), "!": (2, 3, 5), "'": (3,), "-": (3, 6),
    "/": (3, 4), "&": (1, 2, 3, 4, 6), "*": (5,), "#": (3, 4, 5, 6),
}
# '#' is special-cased in encode (it is the number sign cell); keep it out of
# the plain punctuation emit path by handling it before punctuation lookup.
PUNCT = {ch: cell(*dots) for ch, dots in PUNCT_DOTS.items() if ch != "#"}
CELL_TO_PUNCT = {v: k for k, v in PUNCT.items()}
OPEN_QUOTE = cell(2, 3, 6)      # same cell as '?'; position decides in decode by toggle in text layer
CLOSE_QUOTE = cell(3, 5, 6)
OPEN_PAREN = cell(5) + cell(1, 2, 6)
CLOSE_PAREN = cell(5) + cell(3, 4, 5)

# Braille ASCII for U+2800..U+283F, in Unicode order (public standard table).
BRAILLE_ASCII = " A1B'K2L@CIF/MSP\"E3H9O6R^DJG>NTQ,*5<-U8V.%[$+X!&;:4\\0Z7(_?W]#Y)="
assert len(BRAILLE_ASCII) == 64
_ASCII_TO_CELL = {c: chr(BRAILLE_BASE + i) for i, c in enumerate(BRAILLE_ASCII)}
for _c in list(_ASCII_TO_CELL):  # lowercase accepted as uppercase equivalent
    if _c.isalpha():
        _ASCII_TO_CELL[_c.lower()] = _ASCII_TO_CELL[_c]

def encode(text: str, *, errors: str = "strict") -> str:
    """Plain text -> Unicode braille (Grade 1, uncontracted)."""
    out: list[str] = []
    i, n = 0, len(text)
    quote_open = False
    while i < n:
        ch = text[i]
        if ch in " \t":
            out.append("\u2800" if ch == " " else " "); i += 1; continue
        if ch == "\n":
            out.append("\n"); i += 1; continue
        if ch.isdigit():
            j = i
            while j < n and (text[j].isdigit() or (text[j] in ",." and j + 1 < n and text[j + 1].isdigit())):
                j += 1
            out.append(NUMBER_SIGN)
            for dch in text[i:j]:
                out.append(LETTERS[DIGIT_TO_LETTER[dch]] if dch.isdigit() else PUNCT[dch])
            if j < n and text[j].isalpha() and text[j].lower() in "abcdefghij":
                out.append(LETTER_SIGN)
            i = j; continue
        if ch.isalpha() and ch.lower() in LETTERS:
            j = i
            while j < n and text[j].isalpha() and text[j].lower() in LETTERS:
                j += 1
            word = text[i:j]
            if len(word) > 1 and word.isupper():
                out.append(CAPITAL_SIGN * 2)
                out.extend(LETTERS[c] for c in word.lower())
            else:
                for c in word:
                    if c.isupper():
                        out.append(CAPITAL_SIGN)
                    out.append(LETTERS[c.lower()])
            i = j; continue
        if ch == "(":
            out.append(OPEN_PAREN); i += 1; continue
        if ch == ")":
            out.append(CLOSE_PAREN); i += 1; continue
        if ch == '"':
            out.append(CLOSE_QUOTE if quote_open else OPEN_QUOTE)
            quote_open = not quote_open; i += 1; continue
        if ch in PUNCT:
            out.append(PUNCT[ch]); i += 1; continue
        if errors == "strict":
            raise ValueError(f"unsupported character for Grade 1 braille: {ch!r}")
        if errors == "replace":
            out.append("\u2800")
        i += 1
    return "".join(out)

def decode(braille: str, *, errors: str = "strict") -> str:
    """Unicode braille -> plain text. Inverse of :func:`encode`."""
    out: list[str] = []
    i, n = 0, len(braille)
    number_mode = False
    caps_word = False
    quote_open = False
    while i < n:
        ch = braille[i]
        if ch in ("\u2800", " "):
            out.append(" "); number_mode = caps_word = False; i += 1; continue
        if ch == "\n":
            out.append("\n"); number_mode = caps_word = False; i += 1; continue
        if ch == CAPITAL_SIGN:
            if i + 1 < n and braille[i + 1] == CAPITAL_SIGN:
                caps_word = True; i += 2; continue
            # single capital: next letter is uppercase
            if i + 1 < n and braille[i + 1] in CELL_TO_LETTER:
                out.append(CELL_TO_LETTER[braille[i + 1]].upper())
                i += 2; continue
            i += 1; continue
        if ch == NUMBER_SIGN:
            number_mode = True; i += 1; continue
        if ch == LETTER_SIGN:
            number_mode = False; i += 1; continue
        if ch == cell(5) and i + 1 < n and braille[i + 1] in (cell(1, 2, 6), cell(3, 4, 5)):
            out.append("(" if braille[i + 1] == cell(1, 2, 6) else ")")
            number_mode = caps_word = False; i += 2; continue
        if number_mode and ch in CELL_TO_LETTER and CELL_TO_LETTER[ch] in LETTER_TO_DIGIT:
            out.append(LETTER_TO_DIGIT[CELL_TO_LETTER[ch]]); i += 1; continue
        if number_mode and ch in (PUNCT[","], PUNCT["."]):
            out.append(CELL_TO_PUNCT[ch]); i += 1; continue
        if ch in CELL_TO_LETTER:
            letter = CELL_TO_LETTER[ch]
            out.append(letter.upper() if caps_word else letter)
            number_mode = False; i += 1; continue
        if ch == OPEN_QUOTE:  # ambiguous cell: '?' or opening quote
            prev_blank = not out or out[-1].endswith((" ", "\n"))
            next_is_letter = i + 1 < n and braille[i + 1] in CELL_TO_LETTER
            if prev_blank and next_is_letter and not quote_open:
                out.append('"'); quote_open = True
            else:
                out.append("?")
            number_mode = caps_word = False; i += 1; continue
        if ch == CLOSE_QUOTE:
            out.append('"'); quote_open = False; number_mode = caps_word = False; i += 1; continue
        if ch in CELL_TO_PUNCT:
            out.append(CELL_TO_PUNCT[ch]); number_mode = caps_word = False; i += 1; continue
        if errors == "strict":
            raise ValueError(f"unsupported braille cell: {ch!r} (U+{ord(ch):04X})")
        if errors == "replace":
            out.append("?")
        i += 1
    return "".join(out)

def unicode_to_braille_ascii(braille: str) -> str:
    out = []
    for ch in braille:
        if ch == "\n" or ch == "\f":
            out.append(ch); continue
        idx = ord(ch) - BRAILLE_BASE
        if ch == "\u2800":
            out.append(" "); continue
        if not (0 <= idx < 64):
            raise ValueError(f"cell needs dots 7/8, not representable in Braille ASCII: U+{ord(ch):04X}")
        out.append(BRAILLE_ASCII[idx])
    return "".join(out)

def braille_ascii_to_unicode(text: str) -> str:
    out = []
    for ch in text:
        if ch in ("\n", "\f", "\r"):
            out.append(ch); continue
        if ch not in _ASCII_TO_CELL:
            raise ValueError(f"character not defined in Braille ASCII: {ch!r}")
        out.append(_ASCII_TO_CELL[ch])
    return "".join(out)

def braille_to_dots(braille: str, sep: str = "-") -> str:
    parts = []
    for ch in braille:
        if ch in ("\u2800", " "):
            parts.append("0")
        elif ch == "\n":
            parts.append("\n")
        else:
            parts.append("".join(str(d) for d in cell_dots(ch)) or "0")
    return sep.join(p for p in parts if p != "\n") if "\n" not in braille else "\n".join(
        sep.join("0" if c in ("\u2800", " ") else "".join(str(d) for d in cell_dots(c)) for c in line)
        for line in braille.split("\n"))

def dots_to_braille(text: str, sep: str = "-") -> str:
    lines = []
    for line in text.strip().splitlines():
        cells = []
        for token in line.split(sep):
            token = token.strip()
            if token in ("", "0"):
                cells.append("\u2800")
            else:
                cells.append(cell(*(int(d) for d in token)))
        lines.append("".join(cells))
    return "\n".join(lines)

def inspect_cell(ch: str) -> str:
    dots = set(cell_dots(ch)) if ch != "\u2800" else set()
    rows = []
    for left, right in ((1, 4), (2, 5), (3, 6)):
        rows.append(f"{'●' if left in dots else '○'} {'●' if right in dots else '○'}")
    label = "".join(str(d) for d in sorted(dots)) or "blank"
    return f"{ch}  dots {label}\n" + "\n".join(rows)

def wrap_braille(braille: str, width: int = 40) -> list[str]:
    if width < 1:
        raise ValueError("width must be >= 1")
    lines: list[str] = []
    for para in braille.split("\n"):
        words = para.split("\u2800")
        cur = ""
        for w in words:
            cand = w if not cur else cur + "\u2800" + w
            if len(cand) <= width:
                cur = cand; continue
            if cur:
                lines.append(cur); cur = ""
            while len(w) > width:  # hard-split overlong words
                lines.append(w[:width]); w = w[width:]
            cur = w
        lines.append(cur)
    return lines

def format_brf(braille: str, width: int = 40, lines_per_page: int = 25) -> str:
    """Unicode braille -> BRF text (Braille ASCII, wrapped, paginated)."""
    lines = wrap_braille(braille, width)
    ascii_lines = [unicode_to_braille_ascii(ln).replace("\u2800", " ").rstrip() for ln in lines]
    pages = [ascii_lines[i:i + lines_per_page] for i in range(0, len(ascii_lines), lines_per_page)] or [[]]
    return "\f".join("\n".join(p) for p in pages) + "\n"

def parse_brf(text: str) -> str:
    """BRF -> Unicode braille, flowing wrapped line/page breaks back to spaces.

    BRF line wraps are formatting, not content: a wrapped line ends where a
    word boundary (blank cell) was, so joining with a blank cell restores the
    original word flow. Hard-split overlong words will gain a space at the
    split point — an inherent property of the BRF format.
    """
    body = text.replace("\f", "\n")
    converted = [braille_ascii_to_unicode(line.rstrip()) for line in body.splitlines()]
    return "\u2800".join(converted).strip("\u2800")

def stats(braille: str, width: int = 40, lines_per_page: int = 25) -> dict:
    cells = [c for c in braille if c not in ("\n",)]
    lines = wrap_braille(braille, width)
    import math
    return {
        "cells": len(cells),
        "blank_cells": sum(1 for c in cells if c == "\u2800"),
        "words": len(braille.replace("\u2800", " ").split()),
        "capital_signs": braille.count(CAPITAL_SIGN),
        "number_signs": braille.count(NUMBER_SIGN),
        "wrapped_lines": len(lines),
        "pages_at_%d_lines" % lines_per_page: math.ceil(len(lines) / lines_per_page) if lines else 0,
    }
