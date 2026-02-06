# Jack Torrance Text Generator

A small chaos script inspired by *The Shining*'s typewriter pages.

## What it does

This tool generates unsettling text dumps based on the phrase:

> **All work and no play make Jack a dull boy**

It randomizes indentation, repeated lines, casing, spacing, and typos to create output that looks obsessive and increasingly unstable.

## Why it's fun

- It recreates a famous horror visual in plain text.
- You can tune how broken or structured the output feels.
- It supports multiple export formats, so you can drop it into docs, share files, or print it.

## Requirements

- Python 3.10+
- Optional for PDF output: `reportlab`

Install optional PDF dependency:

```bash
pip install reportlab
```

## How to run

Basic run (writes `.txt` by default):

```bash
python Jack.py
```

Write to a custom file:

```bash
python Jack.py --output output/overlook.txt
```

Generate by page count instead of explicit line count:

```bash
python Jack.py --pages 5
```

## Command-line options

```text
-n, --lines                Number of base lines to generate (default: 1000)
--pages                    Approximate page count (~40 lines each); overrides --lines
--patterns                 Comma-separated patterns: flat,pyramid,spiral,collapse
--typo-intensity           Typo mutation probability from 0.0 to 1.0 (default: 0.12)
--blank-line-frequency     Blank-line probability from 0.0 to 1.0 (default: 0.08)
--format                   Output format: txt, md, pdf, rtf (default: txt)
--output                   Output path (default: overlook_output.txt)
--seed                     Seed for reproducible generation
```

### Pattern examples

Use only spiral + collapse:

```bash
python Jack.py --patterns spiral,collapse --lines 300
```

Less noisy output:

```bash
python Jack.py --typo-intensity 0.03 --blank-line-frequency 0.02
```

Maximum chaos markdown dump:

```bash
python Jack.py --format md --output chaos.md --typo-intensity 0.45 --patterns flat,pyramid,spiral,collapse
```

## Output formats

- **`.txt`**: raw text output.
- **`.md`**: markdown wrapper with metadata and a fenced `text` block.
- **`.pdf`**: fixed-width Courier rendering via `reportlab`.
- **`.rtf`**: rich text file using Courier New for that typewriter feel.

## License

This project is released under the **MIT License** (maximally permissive/open for most use cases).
See [LICENSE](./LICENSE).
