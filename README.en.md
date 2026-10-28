[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md)

# ⠠⠃⠗⠁⠊⠇⠇⠑⠠⠋⠕⠗⠛⠑ BrailleForge

> An offline, zero-dependency English Grade 1 (uncontracted) braille toolkit: plain text ⇄ Unicode braille ⇄ dot notation ⇄ Braille ASCII ⇄ embosser-ready .brf files — five forms, all interconvertible, in one command.

## 🎉 Introduction

Anyone producing accessible content hits the same wall: online converters turn English into braille patterns, but embossers and refreshable displays actually need **BRF (Braille ASCII)**, teaching materials are written in **dot notation (dots-125)**, and software stores **Unicode braille patterns** — three forms that do not talk to each other. Every conversion means another website, and another upload of your content to someone else's server.

BrailleForge closes that gap with a **local-first** tool: every conversion runs on your machine. No network, no uploads, no third-party dependencies — it keeps working offline after `pip install`.

**How it is different**

- 🔁 **A closed loop of five forms**: most tools only do one-way "text → patterns". BrailleForge connects text / Unicode braille / dot notation / Braille ASCII / BRF, and every path is reversible and covered by round-trip tests.
- 🖨️ **Real BRF layout**: paginated Braille ASCII at 40 cells per line and 25 lines per page by default — not Unicode characters with a renamed extension.
- 🔢 **A state machine, not table stitching**: capital-word signs (double capital), numeric mode, and the letter sign needed when a–j follows digits are handled by rule, so the inputs that usually break converters — `NASA`, `2026`, `2a` — round-trip correctly.
- 🌱 **Inspiration**: the local-first / offline-first wave on GitHub Trending, plus the real format gap in accessible publishing. The implementation is original; mappings follow the public braille cell system and the standard Braille ASCII table. No existing project's code was copied.

## ✨ Features

- 🔤 **Text → braille**: Grade 1 (uncontracted) encoding for letters, digits and common punctuation, with capital-sign, capital-word and number-sign rules
- ↩️ **Braille → text**: state-machine decoding that handles numeric mode, caps-word mode and the ambiguous quote cell
- 🔡 **Braille ASCII**: the full standard 64-cell table (U+2800–U+283F) — the actual byte encoding inside .brf files
- 🎯 **Dot notation**: convert to and from teaching/proofreading notation such as `125-15`
- 👁️ **Cell inspection**: render every cell as a ●○ dot grid for visual proofreading
- 📄 **BRF in and out**: adjustable line width and lines per page for embosser-ready files, plus .brf → readable text recovery
- 📊 **Statistics**: cell counts, word counts, number/capital sign counts and page estimates as JSON
- 📦 **Zero dependencies**: pure Python standard library, Python ≥ 3.9, Windows / macOS / Linux

## 🚀 Quick Start

Requirements: Python ≥ 3.9, nothing else.

```bash
# Option 1: install from source
git clone https://github.com/gitstq/brailleforge.git
cd brailleforge
pip install .

# Option 2: no install, run from the source tree
python -m brailleforge demo
```

```bash
brailleforge demo
brailleforge encode "Hello 123"
# ⠠⠓⠑⠇⠇⠕⠀⠼⠁⠃⠉

brailleforge decode "⠠⠓⠑⠇⠇⠕⠀⠼⠁⠃⠉"
# Hello 123
```

## 📖 Usage Guide

### Commands

| Command | What it does | Example |
|---|---|---|
| `encode` | text → Unicode braille | `brailleforge encode "Read by touch"` |
| `decode` | Unicode braille → text | `brailleforge decode "⠗⠑⠁⠙"` |
| `to-ascii` | Unicode braille → Braille ASCII | `brailleforge to-ascii "⠓⠑"` → `HE` |
| `from-ascii` | Braille ASCII → Unicode braille | `brailleforge from-ascii ",HI #ABC"` |
| `to-dots` | Unicode braille → dot notation | `⠓⠑` → `125-15` |
| `from-dots` | dot notation → Unicode braille | `brailleforge from-dots "125-15"` |
| `inspect` | draw each cell as a dot grid | `brailleforge inspect "⠓"` |
| `brf` | text → formatted .brf | `brailleforge brf -f in.txt -o out.brf --width 40` |
| `unbrf` | .brf → text | `brailleforge unbrf -f out.brf` |
| `stats` | statistics (JSON) | `brailleforge stats "Hello 123"` |

Every command accepts `-f FILE` for input and `-o FILE` for output, and defaults to stdin/stdout so commands compose in pipelines.

### As a Python library

```python
from brailleforge import encode, decode, format_brf, braille_to_dots

br = encode("Accessibility matters 100")
print(br)                       # ⠠⠁⠉⠉⠑⠎⠎⠊⠃⠊⠇⠊⠞⠽⠀...
print(decode(br))               # Accessibility matters 100
print(braille_to_dots(br))      # 6-1-14-14-15-...
brf_text = format_brf(br, width=40, lines_per_page=25)  # embosser-ready Braille ASCII
```

### Typical scenarios

- 🏫 **Teaching materials**: turn lessons into dot-notation worksheets, or demo cells live with `inspect`.
- 🖨️ **Going to emboss**: one `brf` step produces correctly wrapped and paginated files for an embosser or transcription service.
- ✅ **Accessibility proofreading**: recover readable text from an unknown BRF with `unbrf` before you edit it.
- 🤖 **Pipelines**: embed the library in an accessible-content workflow — fully offline, sensitive text never leaves the machine.

> 📸 Screenshots / demo GIFs are reserved for the `docs/` folder in a follow-up.

## 💡 Design Notes & Roadmap

- **Why zero-dependency stdlib**: braille conversion is deterministic rules, not a framework problem. Zero dependencies means this code will very likely still run as-is in ten years.
- **Why a state machine**: capitals and numbers in braille are *mode signs* — they cannot be decoded out of context, and table stitching inevitably breaks on inputs like `2a` or all-caps words.
- **Honest scope**: this project does **Grade 1 uncontracted** braille. Grade 2 contractions are complex and region-dependent; they are not claimed until they are actually implemented.

Roadmap:

- 🗺️ Optional Grade 2 contractions (off by default)
- 🌏 More language tables: French / German braille
- 🖨️ A BRF compliance checker (line width / pagination report)
- 🔌 MCP / editor-plugin form so AI agents can call it directly

## 📦 Packaging & Deployment

This is a **library / CLI tool**, so by design there are no per-platform executable Releases — installing *is* the integration:

```bash
# Build distribution packages (sdist + wheel)
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install build
python -m build        # artifacts land in dist/

# Run the tests
python -m unittest discover -s tests -v
```

Supported environments: Python ≥ 3.9 on Windows / macOS / Linux. No network, no native extensions, no environment variables required.

## 🤝 Contributing

- 🐛 Issues: please include a minimal reproduction (source text + expected braille + actual output) — "feels wrong" is not debuggable.
- 🔀 Pull requests: Angular-style commit subjects (`feat:` / `fix:` / `docs:` / `refactor:`); new conversion rules must ship with round-trip tests.
- ♿ Feedback from braille readers and transcribers is especially welcome: on questions of correctness, your word wins.

## 📄 License

Released under the [MIT License](LICENSE) — use, modify and distribute freely, keeping the copyright notice.
