import random
import shutil
import sys
import time

RESET = "\033[0m"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
CLEAR_HOME = "\033[2J\033[H"

COLORS = [
    "\033[91m",  # red
    "\033[93m",  # yellow
    "\033[92m",  # green
    "\033[96m",  # cyan
    "\033[94m",  # blue
    "\033[95m",  # magenta
]


def write(text: str) -> None:
    sys.stdout.write(text)
    sys.stdout.flush()


def rainbow(text: str) -> str:
    painted: list[str] = []
    for ch in text:
        if ch == " ":
            painted.append(ch)
            continue
        painted.append(f"{random.choice(COLORS)}{ch}{RESET}")
    return "".join(painted)


def random_confetti_line(width: int = 32) -> str:
    pieces = [".", "*", "+", "x", "o", " "]
    return "".join(random.choice(pieces) for _ in range(width))


def glitch_text(base: str) -> str:
    glitch_chars = ["@", "#", "%", "&", "!", "?"]
    out: list[str] = []
    for ch in base:
        if ch != " " and random.random() < 0.20:
            out.append(random.choice(glitch_chars))
        else:
            out.append(ch)
    return "".join(out)


def play_intro(frames: int = 22) -> None:
    for _ in range(frames):
        write(CLEAR_HOME)
        top = rainbow(random_confetti_line())
        mid = rainbow(glitch_text("          HI MARK!!!          "))
        bot = rainbow(random_confetti_line())
        write(f"{top}\n{mid}\n{bot}\n")
        time.sleep(0.08)


def play_finale() -> None:
    big = [
        "██   ██ ██     ███    ███  █████  ██████  ██   ██",
        "██   ██ ██     ████  ████ ██   ██ ██   ██ ██  ██ ",
        "███████ ██     ██ ████ ██ ███████ ██████  █████  ",
        "██   ██ ██     ██  ██  ██ ██   ██ ██   ██ ██  ██ ",
        "██   ██ ██     ██      ██ ██   ██ ██   ██ ██   ██",
        "",
        "                    !!!!!!                      ",
    ]

    corgi_frames = [
        [
            " / \\__",
            "(    @\\___",
            " /         O",
            "/  /(_____/",
            "/_/   U  U",
        ],
        [
            " / \\__",
            "(    @\\___",
            " /         O",
            "/  /(_____/",
            "/_/  U  U",
        ],
        [
            " / \\__",
            "(    @\\___",
            " /         O",
            "/ /(_____/",
            "//   U  U",
        ],
        [
            " / \\__",
            "(    @\\___",
            " /         O",
            "/ /(_____/",
            "//  U  U",
        ],
    ]
    screen_width = shutil.get_terminal_size(fallback=(80, 24)).columns
    max_offset = max(0, screen_width - 20)

    for frame in range(20):
        write(CLEAR_HOME)
        for line in big:
            write(f"{rainbow(line)}\n")
        write("\n")
        offset = min(max_offset, frame * 3)
        sprite = corgi_frames[frame % len(corgi_frames)]
        bob = frame % 2
        write(f"{' ' * offset}{rainbow('Winston is zoomin!')}\n")
        if bob:
            write("\n")
        for line in sprite:
            write(f"{' ' * offset}{rainbow(line)}\n")
        time.sleep(0.12)


def main() -> None:
    write(HIDE_CURSOR)
    try:
        play_intro()
        play_finale()
    finally:
        write(f"{RESET}{SHOW_CURSOR}")


if __name__ == "__main__":
    main()
