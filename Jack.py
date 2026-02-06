import random
import shutil

PHRASE = "All work and no play make Jack a dull boy"

# terminal width for centering
WIDTH = shutil.get_terminal_size((80, 20)).columns


def corrupt_text(text, typo_prob=0.12):
    chars = list(text)
    i = 0
    while i < len(chars):
        if random.random() < typo_prob:
            r = random.random()
            if r < 0.2 and i < len(chars) - 1:
                chars.pop(i)  # delete
                continue
            elif r < 0.4:
                chars.insert(i, chars[i])  # duplicate
                i += 1
            elif r < 0.6:
                chars[i] = random.choice(
                    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "
                )
            elif r < 0.8 and chars[i] == " ":
                chars.pop(i)  # remove space
                continue
            else:
                chars[i] = chars[i].swapcase()
        i += 1
    return "".join(chars)


def random_caps(text):
    if random.random() < 0.15:
        return text.upper()
    if random.random() < 0.1:
        return text.lower()
    return text


def indent_generator():
    mode = "flat"
    level = 0
    direction = 1

    while True:
        # switch mode randomly
        if random.random() > 0.8:
            mode = random.choice(["flat", "pyramid", "spiral", "collapse"])
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
            # sudden reset to far left or huge jump
            indent = " " * random.choice([0, 0, 0, random.randint(20, 60)])

        yield indent


def format_line(text):
    # alignment madness
    if random.random() < 0.1:
        return text.center(WIDTH)
    if random.random() < 0.05:
        return text.rjust(WIDTH)
    return text


def main(lines=1000):
    indent_iter = indent_generator()

    for i in range(lines):
        # random blank lines
        if random.random() < 0.08:
            print()
            continue

        # page break style gaps
        if random.random() < 0.01:
            print("\n" * random.randint(10, 30))

        # obsessive repeats
        repeat = 1
        if random.random() < 0.1:
            repeat = random.randint(2, 8)

        for _ in range(repeat):
            indent = next(indent_iter)

            text = PHRASE

            # extreme collapse mode
            if random.random() < 0.03:
                text = text.replace(" ", "").upper()

            text = corrupt_text(text)
            text = random_caps(text)
            text = indent + text
            text = format_line(text)

            print(text)


if __name__ == "__main__":
    main()
