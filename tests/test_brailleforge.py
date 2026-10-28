import unittest
from brailleforge import (encode, decode, unicode_to_braille_ascii,
                          braille_ascii_to_unicode, braille_to_dots,
                          dots_to_braille, format_brf, parse_brf, stats, cell)
from brailleforge.core import BRAILLE_ASCII

class TestEncodeDecode(unittest.TestCase):
    def test_letters(self):
        self.assertEqual(encode("abc"), "⠁⠃⠉")
        self.assertEqual(encode("hello"), "⠓⠑⠇⠇⠕")
        self.assertEqual(encode("w"), "⠺")  # w: dots 2-4-5-6, the French-origin exception

    def test_numbers(self):
        self.assertEqual(encode("123"), "⠼⠁⠃⠉")
        self.assertEqual(encode("2026"), "⠼⠃⠚⠃⠋")
        self.assertEqual(decode("⠼⠁⠃⠉"), "123")
        self.assertEqual(decode(encode("3.14")), "3.14")
        self.assertEqual(decode(encode("1,000")), "1,000")

    def test_number_then_aj_letter_needs_letter_sign(self):
        self.assertEqual(decode(encode("2a")), "2a")
        self.assertEqual(decode(encode("2k")), "2k")

    def test_capitals(self):
        self.assertEqual(encode("Hello"), "⠠⠓⠑⠇⠇⠕")
        self.assertEqual(decode(encode("Hello World")), "Hello World")
        self.assertEqual(decode(encode("NASA")), "NASA")  # caps-word double sign
        self.assertEqual(encode("NASA").count("⠠"), 2)

    def test_punctuation_and_roundtrip(self):
        samples = [
            "Hello, world!",
            "What is braille?",
            "It is a code: dots; cells.",
            "Braille Forge 2026: read by touch!",
            "well-known / offline-first",
            "(in parentheses)",
            "rock 'n' roll",
        ]
        for s in samples:
            self.assertEqual(decode(encode(s)), s, s)

    def test_quotes_roundtrip(self):
        self.assertEqual(decode(encode('say "hi" now')), 'say "hi" now')

    def test_unsupported_raises(self):
        with self.assertRaises(ValueError):
            encode("hello €")

class TestBrailleAscii(unittest.TestCase):
    def test_known_cells(self):
        self.assertEqual(unicode_to_braille_ascii("⠁"), "A")
        self.assertEqual(unicode_to_braille_ascii("⠼"), "#")  # number sign
        self.assertEqual(unicode_to_braille_ascii("⠠"), ",")  # capital sign
        self.assertEqual(unicode_to_braille_ascii("⠂"), "1")  # comma cell in BRF
        self.assertEqual(unicode_to_braille_ascii("⠲"), "4")  # period cell in BRF

    def test_all_64_cells_roundtrip(self):
        all_cells = "".join(chr(0x2800 + i) for i in range(64))
        self.assertEqual(braille_ascii_to_unicode(unicode_to_braille_ascii(all_cells)), all_cells)
        self.assertEqual(len(BRAILLE_ASCII), 64)

    def test_encode_to_brf_style(self):
        # "Hi 123" as embosser bytes: ,HI #ABC
        self.assertEqual(unicode_to_braille_ascii(encode("Hi 123")), ",HI #ABC")

class TestDots(unittest.TestCase):
    def test_dots(self):
        self.assertEqual(braille_to_dots("⠓⠑"), "125-15")
        self.assertEqual(dots_to_braille("125-15"), "⠓⠑")
        self.assertEqual(braille_to_dots(encode("a b")), "1-0-12")

    def test_cell_helper(self):
        self.assertEqual(cell(1, 2, 5), "⠓")
        with self.assertRaises(ValueError):
            cell(7)

class TestBrfAndStats(unittest.TestCase):
    def test_brf_roundtrip(self):
        text = "Braille helps people read by touch every single day"
        brf = format_brf(encode(text), width=20, lines_per_page=2)
        for line in brf.replace("\f", "\n").splitlines():
            self.assertLessEqual(len(line), 20)
        self.assertEqual(decode(parse_brf(brf)), text)

    def test_stats(self):
        s = stats(encode("Hello 123"))
        self.assertEqual(s["number_signs"], 1)
        self.assertEqual(s["capital_signs"], 1)
        self.assertGreaterEqual(s["cells"], 8)

if __name__ == "__main__":
    unittest.main()
