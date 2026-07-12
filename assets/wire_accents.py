#!/usr/bin/env python3
"""Wire unique accent SVGs into README section breaks."""
from pathlib import Path
import re

README = Path(__file__).resolve().parent.parent / "README.md"
BASE = "https://raw.githubusercontent.com/caelf-hub/caelf-hub/main/assets/accents"

# Order of accents as they appear before each section heading (after hero bridge stays)
# The first divider is before About, then before each subsequent h2
SECTION_ACCENTS = [
    "about",       # before About
    "focus",       # before Current Focus
    "projects",    # before Featured Projects
    "research",    # before Research Interests
    "stack",       # before Tech Stack
    "experience",  # before Experience
    "opensource",  # before Open Source
    "education",   # before Education
    "stats",       # before GitHub Statistics
    "connect",     # before Connect
]


def picture(name: str) -> str:
    return f'''<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="{BASE}/{name}-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="{BASE}/{name}-light.svg">
    <img src="{BASE}/{name}-light.svg" alt="" width="100%">
  </picture>
</p>'''


def main():
    raw = README.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("latin-1")
    # normalize broken punctuation (0x9d etc.)
    text = "".join(ch if ord(ch) >= 32 or ch in "\n\r\t" else "·" for ch in text)
    text = text.replace("\u009d", "·").replace("\x9d", "·")

    # Replace hero bridge to accents/bridge
    text = text.replace(
        "assets/bridge-dark.svg",
        "assets/accents/bridge-dark.svg",
    )
    text = text.replace(
        "assets/bridge-light.svg",
        "assets/accents/bridge-light.svg",
    )

    # Replace every generic divider picture block in order with unique accents
    divider_pattern = re.compile(
        r'<p align="center">\s*'
        r'<picture>\s*'
        r'<source media="\(prefers-color-scheme: dark\)" srcset="[^"]*divider-dark\.svg">\s*'
        r'<source media="\(prefers-color-scheme: light\)" srcset="[^"]*divider-light\.svg">\s*'
        r'<img src="[^"]*divider-light\.svg" alt="" width="100%">\s*'
        r'</picture>\s*'
        r'</p>',
        re.MULTILINE,
    )

    matches = list(divider_pattern.finditer(text))
    print(f"found {len(matches)} divider blocks, have {len(SECTION_ACCENTS)} accents")

    # Replace from end to start so indices stay valid
    for match, name in zip(reversed(matches), reversed(SECTION_ACCENTS[: len(matches)])):
        text = text[: match.start()] + picture(name) + text[match.end() :]

    README.write_text(text, encoding="utf-8")
    print("README updated")


if __name__ == "__main__":
    main()
