# Changelog

## [1.0.0] - 2026-10-28

### Added
- feat: Grade 1 (uncontracted) English braille encode/decode with a state
  machine for capital signs, capital words, numeric mode and letter signs
- feat: Braille ASCII conversion for the full 64-cell table (U+2800–U+283F)
- feat: dot-notation conversion (`125-15`) and per-cell dot-grid inspection
- feat: BRF formatting (configurable width / lines per page) and BRF recovery
- feat: statistics command (cells, words, signs, page estimates) as JSON
- feat: CLI with file/stdin/stdout support plus a Python library API
- docs: full README in Simplified Chinese, Traditional Chinese and English
- test: 14 unit tests including all-64-cell and BRF round-trips
