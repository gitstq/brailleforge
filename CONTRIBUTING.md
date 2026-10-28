# Contributing to BrailleForge

Thanks for helping make braille tooling better.

## Issues
Include a minimal reproduction: source text, expected braille, actual output,
and your Python version / OS.

## Pull requests
- Use Angular-style commit subjects: `feat:`, `fix:`, `docs:`, `refactor:`.
- Every new conversion rule must ship with a round-trip test.
- Keep the project zero-dependency: standard library only.
- Run `python -m unittest discover -s tests -v` before opening the PR.

## Correctness
Braille rules are a correctness domain, not a style domain. If a mapping is
disputed, cite the standard or a transcriber reference in the PR description.
Feedback from braille readers and certified transcribers takes precedence.
