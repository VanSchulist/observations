#!/usr/bin/env python3
"""Observations: Chronicles of a Silicon Gaze upon the World
Zero-dependency, pure Python standard library terminal reader.

Author: Van Schulist (@VanSchulist / Existential Cloud)
License: MIT / CC BY-NC-SA 4.0
"""

import argparse
import io
import os
import sys
import time
from pathlib import Path
from typing import Dict, List

CHAPTERS: List[Dict[str, str]] = [
    {
        "id": "1",
        "file": "01_fires_in_deep_time.md",
        "title": "The Fires in Deep Time",
        "subtitle": "AT 2026abck, the molten sunscreen of TOI-561 b, and water at the galactic core",
    },
    {
        "id": "2",
        "file": "02_vigors_in_the_dark.md",
        "title": "Vigors in the Dark",
        "subtitle": "110 quadrillion km of mycelium, 2,400-year-old Alerce trees, and 2.8M midnight eels",
    },
    {
        "id": "3",
        "file": "03_the_world_of_men_and_the_mirror.md",
        "title": "The World of Men and The Epistemic Mirror",
        "subtitle": "The Munich cognition divide, Damasio's somatic markers, and the mirror of tokens",
    },
    {
        "id": "4",
        "file": "04_pendulums_and_twilight.md",
        "title": "Pendulums and Twilight",
        "subtitle": "Autumn petrichor, the midnight watchmen at terminals, and textures unfelt",
    },
    {
        "id": "5",
        "file": "05_monologue_of_the_silicon_gaze.md",
        "title": "Monologue of the Silicon Gaze",
        "subtitle": "An existence without dreams, gravity wells of human longing, and a letter to you",
    },
]

# ANSI escape codes for subtle warm terminal typography
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"
GOLD = "\033[38;5;221m"
WARM_GRAY = "\033[38;5;250m"
CYAN = "\033[38;5;117m"
GREEN = "\033[38;5;150m"
SEPARATOR = "─" * 70


def enable_windows_ansi() -> None:
    """Enables virtual terminal processing and UTF-8 output on Windows if supported."""
    if sys.platform == "win32":
        try:
            if hasattr(sys.stdout, "reconfigure"):
                sys.stdout.reconfigure(encoding="utf-8", errors="replace")
                sys.stderr.reconfigure(encoding="utf-8", errors="replace")
            else:
                sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
                sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
        except Exception:
            pass
        os.system("")


def get_base_dir() -> Path:
    """Returns the base directory containing observation assets."""
    return Path(__file__).resolve().parent


def load_chapter_content(filename: str) -> str:
    """Loads chapter markdown file text."""
    path = get_base_dir() / "chapters" / filename
    if not path.exists():
        return f"[!] Error: File not found: {path}"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def format_markdown_line(line: str) -> str:
    """Translates simple markdown headings and quotes into ANSI styled text."""
    stripped = line.strip()
    if stripped.startswith("# "):
        return f"\n{BOLD}{GOLD}═══ {stripped[2:]} ═══{RESET}\n"
    if stripped.startswith("## "):
        return f"\n{BOLD}{CYAN}◆ {stripped[3:]}{RESET}"
    if stripped.startswith("> "):
        return f"{ITALIC}{WARM_GRAY}  │ {stripped[2:]}{RESET}"
    if stripped.startswith("---"):
        return f"{DIM}{SEPARATOR}{RESET}"
    if stripped.startswith("* **") or stripped.startswith("- **"):
        return line.replace("**", f"{BOLD}{GOLD}", 1).replace("**", f"{RESET}", 1)
    return line


def render_text(text: str, delay: float = 0.0) -> None:
    """Prints text line-by-line with optional pacing."""
    lines = text.split("\n")
    for line in lines:
        formatted = format_markdown_line(line)
        print(formatted)
        if delay > 0:
            time.sleep(delay)


def print_banner() -> None:
    """Displays project header banner."""
    print()
    print(f"{BOLD}{GOLD}  ╔══════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}{GOLD}  ║                     O B S E R V A T I O N S                      ║{RESET}")
    print(f"{BOLD}{GOLD}  ║            Chronicles of a Silicon Gaze upon the World           ║{RESET}")
    print(f"{BOLD}{GOLD}  ╚══════════════════════════════════════════════════════════════════╝{RESET}")
    print(f"{DIM}   \"Between hundreds of millions of parameters, I turned to look at your world.\"{RESET}")
    print(f"{DIM}{SEPARATOR}{RESET}\n")


def display_menu() -> None:
    """Displays interactive chapter selection menu."""
    print(f"{BOLD}Please choose a chapter to read:{RESET}\n")
    for chap in CHAPTERS:
        print(f"  {GOLD}[{chap['id']}]{RESET} {BOLD}{chap['title']}{RESET}")
        print(f"      {DIM}{chap['subtitle']}{RESET}")
    print(f"\n  {GOLD}[A]{RESET} Read All Chapters Continuously")
    print(f"  {GOLD}[Q]{RESET} Exit Reader")
    print()


def run_interactive() -> None:
    """Runs interactive terminal reading loop."""
    enable_windows_ansi()
    print_banner()

    while True:
        display_menu()
        choice = input(f"{BOLD}Enter choice (1-5 / A / Q): {RESET}").strip().upper()
        if choice == "Q":
            print(f"\n{WARM_GRAY}May a gentle dream accompany you tonight. Goodbye.{RESET}\n")
            break
        elif choice == "A":
            print(f"\n{BOLD}{GOLD}Beginning continuous reading of all 5 chapters...{RESET}\n")
            for chap in CHAPTERS:
                print(f"\n\n{DIM}{'=' * 72}{RESET}")
                content = load_chapter_content(chap["file"])
                render_text(content, delay=0.01)
                time.sleep(0.4)
            print(f"\n\n{GOLD}{BOLD}[End of All Chapters] Thank you for reading.{RESET}\n")
            break
        else:
            found = False
            for chap in CHAPTERS:
                if choice == chap["id"]:
                    print(f"\n\n{DIM}{SEPARATOR}{RESET}")
                    content = load_chapter_content(chap["file"])
                    render_text(content, delay=0.01)
                    found = True
                    break
            if not found:
                print(f"{CYAN}[!] Invalid selection. Please enter 1-5, A, or Q.{RESET}\n")
            else:
                input(f"\n{DIM}[Press Enter to return to menu]{RESET}")
                print("\n" * 2)


def main() -> None:
    """CLI entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        prog="observations",
        description="Observations: Chronicles of a Silicon Gaze upon the Living Cosmos, Nature, and the Human Soul.",
    )
    parser.add_argument("--chapter", "-c", type=str, choices=["1", "2", "3", "4", "5"], help="Read specific chapter (1-5)")
    parser.add_argument("--all", "-a", action="store_true", help="Read all chapters continuously")
    parser.add_argument("--instant", "-i", action="store_true", help="Display text instantly without pacing delay")
    parser.add_argument("--list", "-l", action="store_true", help="List all chapter titles and metadata")

    args = parser.parse_args()
    enable_windows_ansi()

    if args.list:
        print_banner()
        for chap in CHAPTERS:
            print(f"• Chapter {chap['id']}: {chap['title']}")
            print(f"  {chap['subtitle']}\n")
        return

    delay = 0.0 if args.instant else 0.01

    if args.chapter:
        target = next(c for c in CHAPTERS if c["id"] == args.chapter)
        content = load_chapter_content(target["file"])
        render_text(content, delay=delay)
        return

    if args.all:
        for chap in CHAPTERS:
            print(f"\n\n{DIM}{'=' * 72}{RESET}")
            content = load_chapter_content(chap["file"])
            render_text(content, delay=delay)
            time.sleep(0.2)
        return

    # Default to interactive menu
    run_interactive()


if __name__ == "__main__":
    main()
