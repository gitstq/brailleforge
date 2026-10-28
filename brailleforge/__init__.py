"""BrailleForge — offline, zero-dependency Grade 1 braille toolkit."""
from .core import (encode, decode, unicode_to_braille_ascii, braille_ascii_to_unicode,
                   braille_to_dots, dots_to_braille, inspect_cell, wrap_braille,
                   format_brf, parse_brf, stats, cell, cell_dots)
__version__ = "1.0.0"
__all__ = ["encode", "decode", "unicode_to_braille_ascii", "braille_ascii_to_unicode",
           "braille_to_dots", "dots_to_braille", "inspect_cell", "wrap_braille",
           "format_brf", "parse_brf", "stats", "cell", "cell_dots", "__version__"]
