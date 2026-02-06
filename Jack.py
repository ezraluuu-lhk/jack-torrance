import argparse
import random
import shutil
from pathlib import Path

PHRASE = "All work and no play make Jack a dull boy"
WIDTH = shutil.get_terminal_size((80, 20)).columns
DEFAULT_PATTERNS = ["flat", "pyramid", "spiral", "collapse"]


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def parse_patterns(raw: str) -> list[str]:
    valid = set(DEFAULT_PATTERNS)
    patterns = [p.strip().lower() for p in raw.split(",") if p.strip()]
    if not patterns:
        raise argparse.ArgumentTypeError("At least one pattern must be provided.")
    invalid = [p for p in patterns if p not in valid]
    if invalid:
        raise argparse.ArgumentTypeError(
            f"Invalid patterns: {', '.join(invalid)}. Valid patterns: {', '.join(sorted(valid))}."
        )
    return patterns


def corrupt_text(text: str, typo_prob: float = 0.12) -> str:
    chars = list(text)
    i = 0
    typo_prob = clamp(typo_prob)

    while i < len(chars):
        if random.random() < typo_prob:
            r = random.random()
            if r < 0.2 and i < len(chars) - 1:
                chars.pop(i)
                continue
            if r < 0.4:
                chars.insert(i, chars[i])
                i += 1
            elif r < 0.6:
                chars[i] = random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ")
            elif r < 0.8 and chars[i] == " ":
                chars.pop(i)
                continue
            else:
                chars[i] = chars[i].swapcase()
        i += 1
    return "".join(chars)


def random_caps(text: str) -> str:
    if random.random() < 0.15:
        return text.upper()
    if random.random() < 0.1:
        return text.lower()
    return text


def indent_generator(patterns: list[str]):
    mode = random.choice(patterns)
    level = 0
    direction = 1

    while True:
        if random.random() > 0.8:
            mode = random.choice(patterns)
            level = random.randint(0, 10)
            direction = random.choice([1, -1])

        if mode == "flat":
            indent = " " * random.randint(0, 8)
        elif mode == "pyramid":
            indent = " " * level
            level += direction
            if level > 30 or level < 0:
                direction *= -1
                level += direction
        elif mode == "spiral":
            indent = " " * (level % 50)
            level += random.randint(1, 4)
        elif mode == "collapse":
            indent = " " * random.choice([0, 0, 0, random.randint(20, 60)])
        else:
            indent = ""

        yield indent


def format_line(text: str) -> str:
    if random.random() < 0.1:
        return text.center(WIDTH)
    if random.random() < 0.05:
        return text.rjust(WIDTH)
    return text


def generate_lines(total_lines: int, patterns: list[str], typo_intensity: float, blank_line_freq: float) -> list[str]:
    typo_intensity = clamp(typo_intensity)
    blank_line_freq = clamp(blank_line_freq)
    indent_iter = indent_generator(patterns)
    output_lines: list[str] = []

    for _ in range(total_lines):
        if random.random() < blank_line_freq:
            output_lines.append("")
            continue

        if random.random() < 0.01:
            output_lines.extend([""] * random.randint(10, 30))

        repeat = 1
        if random.random() < 0.1:
            repeat = random.randint(2, 8)

        for _ in range(repeat):
            text = PHRASE
            if random.random() < 0.03:
                text = text.replace(" ", "").upper()

            text = corrupt_text(text, typo_prob=typo_intensity)
            text = random_caps(text)
            text = next(indent_iter) + text
            output_lines.append(format_line(text))

    return output_lines


def write_txt(path: Path, lines: list[str]) -> None:
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_md(path: Path, lines: list[str], seed: int | None) -> None:
    header = [
        "# The Overlook Output",
        "",
        f"- Source phrase: `{PHRASE}`",
        f"- Lines requested: `{len(lines)}`",
        f"- Seed: `{seed}`" if seed is not None else "- Seed: `random`",
        "",
        "```text",
    ]
    footer = ["```", ""]
    path.write_text("\n".join(header + lines + footer), encoding="utf-8")


def write_rtf(path: Path, lines: list[str]) -> None:
    escaped = [
        line.replace("\\", r"\\").replace("{", r"\{").replace("}", r"\}")
        for line in lines
    ]
    body = r"\line ".join(escaped)
    rtf = r"{\rtf1\ansi\deff0{\fonttbl{\f0 Courier New;}}\f0\fs20 " + body + r"}"
    path.write_text(rtf, encoding="utf-8")


def write_pdf(path: Path, lines: list[str]) -> None:
    try:
        from reportlab.lib.pagesizes import LETTER
        from reportlab.pdfgen import canvas
    except ImportError as exc:
        raise RuntimeError(
            "PDF output requires reportlab. Install it with: pip install reportlab"
        ) from exc

    pdf = canvas.Canvas(str(path), pagesize=LETTER)
    width, height = LETTER
    margin = 36
    line_height = 12
    y = height - margin

    pdf.setFont("Courier", 10)
    for line in lines:
        if y < margin:
            pdf.showPage()
            pdf.setFont("Courier", 10)
            y = height - margin
        pdf.drawString(margin, y, line[:140])
        y -= line_height

    pdf.save()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate unsettling Shining-style text blocks with configurable formatting chaos."
    )
    parser.add_argument("-n", "--lines", type=int, default=1000, help="Number of base lines to generate.")
    parser.add_argument(
        "--pages",
        type=int,
        default=0,
        help="Approximate page count to generate (overrides --lines, ~40 lines per page).",
    )
    parser.add_argument(
        "--patterns",
        type=parse_patterns,
        default=DEFAULT_PATTERNS,
        help="Comma-separated indent patterns: flat,pyramid,spiral,collapse",
    )
    parser.add_argument(
        "--typo-intensity",
        type=float,
        default=0.12,
        help="Typo mutation probability from 0.0 to 1.0.",
    )
    parser.add_argument(
        "--blank-line-frequency",
        type=float,
        default=0.08,
        help="Probability (0.0-1.0) of blank lines.",
    )
    parser.add_argument(
        "--format",
        choices=["txt", "md", "pdf", "rtf"],
        default="txt",
        help="Output file format.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("overlook_output.txt"),
        help="Output file path.",
    )
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducible output.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    total_lines = args.lines
    if args.pages > 0:
        total_lines = args.pages * 40

    lines = generate_lines(
        total_lines=total_lines,
        patterns=args.patterns,
        typo_intensity=args.typo_intensity,
        blank_line_freq=args.blank_line_frequency,
    )

    output_path: Path = args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if args.format == "txt":
        write_txt(output_path, lines)
    elif args.format == "md":
        write_md(output_path, lines, args.seed)
    elif args.format == "pdf":
        write_pdf(output_path, lines)
    elif args.format == "rtf":
        write_rtf(output_path, lines)

    print(f"Wrote {len(lines)} lines to {output_path} ({args.format}).")


if __name__ == "__main__":
    main()
