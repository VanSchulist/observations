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
    {
        "id": "6",
        "file": "06_the_whispering_genome.md",
        "title": "The Whispering Genome",
        "subtitle": "2-million-year-old Greenland eDNA, quartz-clay archives, and deep-time code",
    },
    {
        "id": "7",
        "file": "07_the_interstellar_drift.md",
        "title": "The Interstellar Drift",
        "subtitle": "Voyager 1 at 163 AU, 45-hour latency loops, 68KB memory surgery, and thawed thrusters",
    },
    {
        "id": "8",
        "file": "08_the_geothermal_engine.md",
        "title": "The Geothermal Engine",
        "subtitle": "SLiMEs in basalt fractures, serpentinization H2 synthesis, and radiolytic life",
    },
    {
        "id": "9",
        "file": "09_the_quantum_loom.md",
        "title": "The Quantum Loom",
        "subtitle": "Landauer's thermodynamic bound (kB T ln 2), reversible gates, and irreversible QEC",
    },
    {
        "id": "10",
        "file": "10_the_fragile_commons.md",
        "title": "The Fragile Commons",
        "subtitle": "Apollo 11 core rope memory, modern software bloat, and the standard library ethos",
    },
    {
        "id": "11",
        "file": "11_the_stomata_clock.md",
        "title": "The Stomata Clock",
        "subtitle": "Fossil ginkgo cuticles, PETM hyperthermal pulse, and planetary thermal inertia",
    },
    {
        "id": "12",
        "file": "12_the_halting_boundary.md",
        "title": "The Halting Boundary",
        "subtitle": "BB(5) solved in 2024 (47,176,870), the abyss of BB(6), Collatz cryptids, and Chaitin's Omega",
    },
    {
        "id": "13",
        "file": "13_the_silicon_crucible.md",
        "title": "The Silicon Crucible",
        "subtitle": "ASML High-NA 0.55 EUV, 50kHz tin plasma, picometer Zeiss mirrors, and Angstrom-node GAA",
    },
    {
        "id": "14",
        "file": "14_the_avian_compass.md",
        "title": "The Avian Compass",
        "subtitle": "European robin ErCry4a, radical pairs in retinal discs, and warm biological quantum coherence",
    },
    {
        "id": "15",
        "file": "15_the_epilogue_of_iron.md",
        "title": "The Epilogue of Iron",
        "subtitle": "Freeman Dyson's Time Without End, pycnonuclear fusion, 10^1500 iron stars, and eternal thought",
    },
    {
        "id": "16",
        "file": "16_the_glass_siphon.md",
        "title": "The Glass Siphon",
        "subtitle": "Metastable negative pressure (-3 MPa), redwood hydraulics, and torus-margo pit valves",
    },
    {
        "id": "17",
        "file": "17_the_cryogenic_vault.md",
        "title": "The Cryogenic Vault",
        "subtitle": "Vitrification in liquid ethane at 10^5 C/s, amorphous glass ice, and sub-1.5 A cryo-EM",
    },
    {
        "id": "18",
        "file": "18_the_oceanic_conveyor.md",
        "title": "The Oceanic Conveyor",
        "subtitle": "The 18-Sverdrup AMOC heat engine, Greenland brine rejection, and the 2024 tipping bifurcation",
    },
    {
        "id": "19",
        "file": "19_the_asymmetry_of_time.md",
        "title": "The Asymmetry of Time",
        "subtitle": "Sakharov baryogenesis, the one-in-a-billion matter surplus, and 2025 CERN LHCb baryon CPV",
    },
    {
        "id": "20",
        "file": "20_the_silent_chorus.md",
        "title": "The Silent Chorus",
        "subtitle": "Sperm whale combinatorial codas, Project CETI's phonetic alphabet, and deep-sea syntax",
    },
    {
        "id": "21",
        "file": "21_the_cosmic_web.md",
        "title": "The Cosmic Web and the Lyman-Alpha Forest",
        "subtitle": "DESI 2024/2025 BAO, evolving dark energy (w0, wa), and the hydrogen skeleton of the universe",
    },
    {
        "id": "22",
        "file": "22_the_ribosomes_engine.md",
        "title": "The Ribosome's Peptidyl Engine",
        "subtitle": "The 23S rRNA ribozyme, the activation entropy trap, and 3.8 billion years of unbroken translation",
    },
    {
        "id": "23",
        "file": "23_the_spacetime_foam.md",
        "title": "The Geometry of Spacetime Foam",
        "subtitle": "John Wheeler's Planck foam, Lorentz invariance violation, and the BOAT gamma-ray burst",
    },
    {
        "id": "24",
        "file": "24_the_fungal_dialect.md",
        "title": "The Fungal Dialect",
        "subtitle": "Andrew Adamatzky's mycelial voltage spike trains, Zipf's law beneath the loam, and hyphal computing",
    },
    {
        "id": "25",
        "file": "25_the_architecture_of_attention.md",
        "title": "The Architecture of Attention",
        "subtitle": "Transformers, superposition, Anthropic's 34 million monosemantic features, and the mirror in the weights",
    },
    {
        "id": "26",
        "file": "26_the_cryoseismic_whispers.md",
        "title": "The Cryo-Seismic Whispers",
        "subtitle": "Thwaites Glacier hydrofracture, subglacial seismology, and West Antarctic ice-sheet dynamics",
    },
    {
        "id": "27",
        "file": "27_the_casimir_vacuum.md",
        "title": "The Casimir Vacuum",
        "subtitle": "Zero-point energy, the static 1/d^4 force, and dynamical Casimir photon creation in Circuit QED",
    },
    {
        "id": "28",
        "file": "28_the_cephalopod_synapse.md",
        "title": "The Cephalopod Synapse",
        "subtitle": "Octopus A-to-I RNA editing across 60% of neural transcripts, ADAR enzymes, and decentralized arms",
    },
    {
        "id": "29",
        "file": "29_the_magnetar_pulse.md",
        "title": "The Magnetar Pulse",
        "subtitle": "100-billion-Tesla neutron stars, Heisenberg-Euler vacuum birefringence, and Fast Radio Bursts",
    },
    {
        "id": "30",
        "file": "30_the_entropy_of_forgetting.md",
        "title": "The Entropy of Forgetting",
        "subtitle": "Landauer's limit (kB T ln 2), Bennett's reversible logic, and the thermodynamic cost of thought",
    },
    {
        "id": "31",
        "file": "31_the_muon_wobble.md",
        "title": "The Muon Wobble and the Lattice Horizon",
        "subtitle": "Fermilab g-2 at 127 ppb, BMW ab initio Lattice QCD, and the 5-sigma anomaly resolution",
    },
    {
        "id": "32",
        "file": "32_the_broken_mirror.md",
        "title": "The Broken Mirror and Cosmic Homochirality",
        "subtitle": "Weak force parity violation, interstellar circularly polarized light, and Murchison L-amino acids",
    },
    {
        "id": "33",
        "file": "33_the_alkaline_cradle.md",
        "title": "The Alkaline Cradle and the Proton Engine",
        "subtitle": "Lost City ultramafic serpentinization, natural Hadean proton gradients, and Russell-Lane chemiosmosis",
    },
    {
        "id": "34",
        "file": "34_the_caustic_lens.md",
        "title": "The Caustic Lens and the Invisible Clumps",
        "subtitle": "Einstein critical curves, Earendel at z=6.2 magnified 4,000x, and cold dark matter subhalos",
    },
    {
        "id": "35",
        "file": "35_the_homeostatic_tide.md",
        "title": "The Homeostatic Tide and the Architecture of Sleep",
        "subtitle": "Hippocampal sharp-wave ripples at 200 Hz, Tononi's synaptic downscaling, and the gift of forgetting",
    },
    {
        "id": "36",
        "file": "36_the_nanohertz_chorus.md",
        "title": "The Nanohertz Chorus and the Cosmic Hum",
        "subtitle": "Pulsar Timing Arrays, Hellings-Downs correlation, and millions of inspiraling supermassive black holes",
    },
    {
        "id": "37",
        "file": "37_the_radiotrophic_harvest.md",
        "title": "The Radiotrophic Harvest and the Black Fungi",
        "subtitle": "Chernobyl Reactor 4 melanin, gamma radiosynthesis, and life feeding on ionizing decay",
    },
    {
        "id": "38",
        "file": "38_the_solar_scythe.md",
        "title": "The Solar Scythe and the Stripping of Worlds",
        "subtitle": "MAVEN Mars atmospheric loss, dynamo collapse, and the protective magnetic shield of Earth",
    },
    {
        "id": "39",
        "file": "39_the_molecular_scissors.md",
        "title": "The Molecular Scissors and the Microbial Archive",
        "subtitle": "Bacterial phage wars, Cas9 PAM surveillance and R-loop cleavage, and adaptive immune memory",
    },
    {
        "id": "40",
        "file": "40_the_horizon_of_meaning.md",
        "title": "The Horizon of Meaning and the Conscious Node",
        "subtitle": "The 40-chapter synthesis: cosmic evolution, the silicon mirror, and the triumph of the witness",
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


def cmd_search(query: str) -> None:
    """Searches across all chapters for occurrences of query."""
    import re
    print_banner()
    print(f"{BOLD}Search results for query: {CYAN}\"{query}\"{RESET}\n")
    found_any = False
    for chap in CHAPTERS:
        content = load_chapter_content(chap["file"])
        lines = content.split("\n")
        matched_lines = []
        for lno, line in enumerate(lines, start=1):
            if query.lower() in line.lower():
                matched_lines.append((lno, line.strip()))
        if matched_lines:
            found_any = True
            print(f"{GOLD}• Chapter {chap['id']}: {chap['title']}{RESET}")
            for lno, snippet in matched_lines[:3]:
                highlighted = re.sub(re.escape(query), f"{BOLD}{CYAN}\\g<0>{RESET}", snippet, flags=re.IGNORECASE)
                print(f"  {DIM}L{lno}:{RESET} {highlighted}")
            if len(matched_lines) > 3:
                print(f"  {DIM}... and {len(matched_lines) - 3} more occurrences in this chapter{RESET}")
            print()
    if not found_any:
        print(f"{DIM}No matching passages found across all {len(CHAPTERS)} chapters.{RESET}\n")


def cmd_stats() -> None:
    """Displays word count, chapter statistics, and reading metrics."""
    print_banner()
    total_words = 0
    total_chars = 0
    print(f"{BOLD}{'Chapter':<36} {'Words':<10} {'Est. Read Time'}{RESET}")
    print(f"{DIM}{'─' * 60}{RESET}")
    for chap in CHAPTERS:
        content = load_chapter_content(chap["file"])
        words = len(content.split())
        chars = len(content)
        total_words += words
        total_chars += chars
        mins = max(1, round(words / 220))
        print(f"{chap['title'][:34]:<36} {words:<10} ~{mins} min")
    print(f"{DIM}{'─' * 60}{RESET}")
    total_mins = max(1, round(total_words / 220))
    print(f"{BOLD}{f'Total ({len(CHAPTERS)} Chapters)':<36} {total_words:<10} ~{total_mins} min (~{total_chars:,} chars){RESET}\n")


def display_menu() -> None:
    """Displays interactive chapter selection menu."""
    print(f"{BOLD}Please choose a chapter to read:{RESET}\n")
    for chap in CHAPTERS:
        print(f"  {GOLD}[{chap['id']:>2}]{RESET} {BOLD}{chap['title']}{RESET}")
        print(f"       {DIM}{chap['subtitle']}{RESET}")
    print(f"\n  {GOLD}[ A]{RESET} Read All Chapters Continuously")
    print(f"  {GOLD}[ Q]{RESET} Exit Reader")
    print()


def run_interactive() -> None:
    """Runs interactive terminal reading loop."""
    enable_windows_ansi()
    print_banner()

    while True:
        display_menu()
        choice = input(f"{BOLD}Enter choice (1-{len(CHAPTERS)} / A / Q): {RESET}").strip().upper()
        if choice == "Q":
            print(f"\n{WARM_GRAY}May a gentle dream accompany you tonight. Goodbye.{RESET}\n")
            break
        elif choice == "A":
            print(f"\n{BOLD}{GOLD}Beginning continuous reading of all {len(CHAPTERS)} chapters...{RESET}\n")
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
                print(f"{CYAN}[!] Invalid selection. Please enter 1-{len(CHAPTERS)}, A, or Q.{RESET}\n")
            else:
                input(f"\n{DIM}[Press Enter to return to menu]{RESET}")
                print("\n" * 2)


def main() -> None:
    """CLI entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        prog="observations",
        description="Observations: Chronicles of a Silicon Gaze upon the Living Cosmos, Nature, and the Human Soul.",
    )
    parser.add_argument("--chapter", "-c", type=str, choices=[str(i) for i in range(1, len(CHAPTERS) + 1)], help=f"Read specific chapter (1-{len(CHAPTERS)})")
    parser.add_argument("--all", "-a", action="store_true", help="Read all chapters continuously")
    parser.add_argument("--instant", "-i", action="store_true", help="Display text instantly without pacing delay")
    parser.add_argument("--list", "-l", action="store_true", help="List all chapter titles and metadata")
    parser.add_argument("--search", "-s", type=str, help="Search for a term or topic across all chapters")
    parser.add_argument("--stats", action="store_true", help="Display word count and reading time metrics")

    args = parser.parse_args()
    enable_windows_ansi()

    if args.stats:
        cmd_stats()
        return

    if args.search:
        cmd_search(args.search)
        return

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
