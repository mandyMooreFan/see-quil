import random
import shutil
import sys
import time

RESET = "\033[0m"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
CLEAR_HOME = "\033[2J\033[H"

INK = "\033[34m"
GOLD = "\033[33m"
PARCHMENT = "\033[38;5;223m"
FEATHER = "\033[38;5;250m"
SPARKLE = "\033[96m"
DIM = "\033[2m"

WORD = "see-quil"
QUOTE = "Beware; for I am fearless, and therefore powerful."


def write(text: str) -> None:
    sys.stdout.write(text)
    sys.stdout.flush()


def center(text: str, width: int) -> str:
    return text.center(width)


def scroll_lines(width: int) -> list[str]:
    inner = width - 6
    top = f"  ╭{'─' * inner}╮"
    body = [f"  │{' ' * inner}│" for _ in range(7)]
    bottom = f"  ╰{'─' * inner}╯"
    return [top, *body, bottom]


def inkwell(width: int) -> list[str]:
    return [
        center(f"{DIM}     ◠     {RESET}", width),
        center(f"{INK}    ╱ ╲    {RESET}", width),
        center(f"{INK}   │ ◉ │   {RESET}", width),
        center(f"{INK}   └───┘   {RESET}", width),
    ]


def quill_at(column: int, dipped: bool) -> list[str]:
    tip = f"{INK}●{RESET}" if dipped else f"{FEATHER}·{RESET}"
    pad = " " * column
    return [
        f"{pad}{FEATHER}\\{RESET}",
        f"{pad} {FEATHER}\\{RESET}",
        f"{pad}  {FEATHER}>==={tip}{RESET}",
        f"{pad}   {FEATHER}|{RESET}",
    ]


def ink_splatter(width: int) -> str:
    chars = [".", "·", "°", " "]
    colors = [INK, DIM, RESET]
    return "".join(
        random.choice(colors) + random.choice(chars) + RESET for _ in range(width)
    )


def sparkle_line(text: str) -> str:
    glitter = ["✦", "✧", "·", " "]
    out: list[str] = []
    for ch in text:
        if ch == " ":
            out.append(ch)
            continue
        if random.random() < 0.35:
            out.append(f"{SPARKLE}{random.choice(glitter)}{RESET}")
        out.append(f"{GOLD}{ch}{RESET}")
    return "".join(out)


def render_frame(
    width: int,
    scroll: list[str],
    written: str,
    quill_col: int,
    dipped: bool,
    phase: str,
    ripple: int = 0,
) -> None:
    write(CLEAR_HOME)

    title = center(f"{GOLD}✒  see-quil  ✒{RESET}", width)
    write(f"{title}\n\n")

    text_line = center(f"{INK}{written:<{len(WORD)}}{RESET}", width)
    text_row = 4

    for i, line in enumerate(scroll):
        if i == text_row:
            inner = width - 6
            left_pad = (inner - len(WORD)) // 2
            visible = f"{INK}{written}{RESET}"
            blank = " " * (len(WORD) - len(written))
            content = f"{' ' * left_pad}{visible}{blank}"
            content = content.ljust(inner)
            write(f"  │{PARCHMENT}{content}{RESET}│\n")
        else:
            colored = line.replace("│", f"{PARCHMENT}│{RESET}").replace("╭", f"{PARCHMENT}╭{RESET}")
            colored = colored.replace("╮", f"{PARCHMENT}╮{RESET}").replace("╰", f"{PARCHMENT}╰{RESET}")
            colored = colored.replace("╯", f"{PARCHMENT}╯{RESET}").replace("─", f"{PARCHMENT}─{RESET}")
            write(f"{colored}\n")

    quill_start = (width - len(WORD)) // 2 + len(written) - 1
    quill_start = max(4, quill_start)
    for line in quill_at(quill_start, dipped):
        write(f"{line}\n")

    write("\n")
    for i, line in enumerate(inkwell(width)):
        if phase == "dip" and i == 0:
            ripple_char = "◠~" if ripple % 2 else "~◠"
            write(center(f"{DIM}    {ripple_char}    {RESET}", width) + "\n")
        else:
            write(f"{line}\n")

    if phase == "write":
        write(f"\n{center(ink_splatter(min(width, 48)), width)}\n")

    if phase == "finale":
        write(f"\n{center(sparkle_line(QUOTE), width)}\n")
        write(f"\n{center(f'{SPARKLE}the quill never rests{RESET}', width)}\n")


def play_intro(width: int, scroll: list[str]) -> None:
    for step in range(8):
        visible = scroll[: 2 + step]
        write(CLEAR_HOME)
        write(center(f"{GOLD}unrolling parchment...{RESET}", width) + "\n\n")
        for line in visible:
            colored = line.replace("─", f"{PARCHMENT}─{RESET}").replace("╭", f"{PARCHMENT}╭{RESET}")
            colored = colored.replace("╮", f"{PARCHMENT}╮{RESET}").replace("│", f"{PARCHMENT}│{RESET}")
            write(f"{colored}\n")
        time.sleep(0.12)


def play_dip(width: int, scroll: list[str]) -> None:
    for ripple in range(10):
        render_frame(width, scroll, "", 8, dipped=False, phase="dip", ripple=ripple)
        time.sleep(0.1)

    for frame in range(6):
        dipped = frame >= 2
        render_frame(width, scroll, "", 8, dipped=dipped, phase="dip", ripple=frame)
        time.sleep(0.12)


def play_write(width: int, scroll: list[str]) -> None:
    for i in range(1, len(WORD) + 1):
        render_frame(width, scroll, WORD[:i], 8, dipped=True, phase="write")
        time.sleep(0.22)


def play_finale(width: int, scroll: list[str]) -> None:
    for _ in range(18):
        render_frame(width, scroll, WORD, 8, dipped=True, phase="finale")
        time.sleep(0.1)


def main() -> None:
    width = shutil.get_terminal_size(fallback=(72, 24)).columns
    scroll = scroll_lines(min(width, 52))

    write(HIDE_CURSOR)
    try:
        play_intro(width, scroll)
        play_dip(width, scroll)
        play_write(width, scroll)
        play_finale(width, scroll)
    finally:
        write(f"{RESET}{SHOW_CURSOR}\n")


if __name__ == "__main__":
    main()
