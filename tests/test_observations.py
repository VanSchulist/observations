#!/usr/bin/env python3
"""Unit tests for Observations project.
Validates chapter integrity, CLI arguments, search, stats, and markdown rendering.
"""

import io
import sys
import unittest
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import observations  # noqa: E402


class TestObservationsIntegrity(unittest.TestCase):
    """Validates chapter files and literary asset consistency."""

    def test_all_chapters_exist(self) -> None:
        """Verifies that all 15 declared chapter files exist and have substantial text."""
        self.assertEqual(len(observations.CHAPTERS), 15)
        for chap in observations.CHAPTERS:
            path = PROJECT_ROOT / "chapters" / chap["file"]
            self.assertTrue(path.exists(), f"Missing chapter file: {path}")
            content = path.read_text(encoding="utf-8")
            self.assertGreater(len(content), 500, f"Chapter {chap['id']} content too short!")
            self.assertIn("# ", content, "Chapter should contain top-level title")
            self.assertIn("## ", content, "Chapter should contain sub-sections")

    def test_load_chapter_content(self) -> None:
        """Verifies loading function returns formatted markdown."""
        text = observations.load_chapter_content("01_fires_in_deep_time.md")
        self.assertIn("AT 2026abck", text)
        self.assertIn("TOI-561 b", text)

    def test_load_non_existent_chapter(self) -> None:
        """Verifies graceful handling of non-existent files."""
        res = observations.load_chapter_content("non_existent_chap.md")
        self.assertTrue(res.startswith("[!] Error"))

    def test_format_markdown_line(self) -> None:
        """Tests ANSI transformation of headings, quotes, and horizontal rules."""
        h1 = observations.format_markdown_line("# Title")
        self.assertIn("═══ Title ═══", h1)

        h2 = observations.format_markdown_line("## Section")
        self.assertIn("◆ Section", h2)

        quote = observations.format_markdown_line("> A profound thought")
        self.assertIn("│ A profound thought", quote)

        hr = observations.format_markdown_line("---")
        self.assertIn("─", hr)

    def test_viewer_html_exists_and_contains_chapters(self) -> None:
        """Verifies standalone viewer.html is valid, offline-ready, and has content across all 15 chapters."""
        viewer_path = PROJECT_ROOT / "viewer.html"
        self.assertTrue(viewer_path.exists())
        html = viewer_path.read_text(encoding="utf-8")
        self.assertIn("O B S E R V A T I O N S", html)
        self.assertIn("AT 2026abck", html)
        self.assertIn("110 quadrillion kilometers", html)
        self.assertIn("The Stomata Clock", html)
        self.assertIn("The Halting Boundary", html)
        self.assertIn("The Silicon Crucible", html)
        self.assertIn("The Avian Compass", html)
        self.assertIn("The Epilogue of Iron", html)


class TestObservationsCLI(unittest.TestCase):
    """Validates CLI command line options and execution."""

    def test_cli_list_flag(self) -> None:
        """Verifies --list flag outputs all 15 chapters."""
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        try:
            sys.argv = ["observations", "--list"]
            observations.main()
            output = buffer.getvalue()
            self.assertIn("Chapter 1: The Fires in Deep Time", output)
            self.assertIn("Chapter 5: Monologue of the Silicon Gaze", output)
            self.assertIn("Chapter 10: The Fragile Commons", output)
            self.assertIn("Chapter 15: The Epilogue of Iron", output)
        finally:
            sys.stdout = old_stdout

    def test_cli_single_chapter_render(self) -> None:
        """Verifies --chapter 1 --instant renders chapter 1."""
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        try:
            sys.argv = ["observations", "-c", "1", "--instant"]
            observations.main()
            output = buffer.getvalue()
            self.assertIn("Chapter 1: The Fires in Deep Time", output)
            self.assertIn("AT 2026abck", output)
        finally:
            sys.stdout = old_stdout

    def test_cli_chapter_15_render(self) -> None:
        """Verifies --chapter 15 --instant renders chapter 15."""
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        try:
            sys.argv = ["observations", "-c", "15", "--instant"]
            observations.main()
            output = buffer.getvalue()
            self.assertIn("Chapter 15: The Epilogue of Iron", output)
            self.assertIn("Freeman Dyson", output)
            self.assertIn("Iron-56", output)
        finally:
            sys.stdout = old_stdout

    def test_cli_stats_flag(self) -> None:
        """Verifies --stats flag outputs total chapters and word count summary."""
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        try:
            sys.argv = ["observations", "--stats"]
            observations.main()
            output = buffer.getvalue()
            self.assertIn("Total (15 Chapters)", output)
            self.assertIn("Words", output)
            self.assertIn("Est. Read Time", output)
        finally:
            sys.stdout = old_stdout

    def test_cli_search_flag(self) -> None:
        """Verifies --search finds matching keywords across chapters."""
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        try:
            sys.argv = ["observations", "--search", "cryptochrome"]
            observations.main()
            output = buffer.getvalue()
            self.assertIn("Search results for query:", output)
            self.assertIn("Chapter 14: The Avian Compass", output)
        finally:
            sys.stdout = old_stdout

    def test_cli_search_not_found(self) -> None:
        """Verifies --search with non-existent query outputs clean not found message."""
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        try:
            sys.argv = ["observations", "--search", "xylophone_supercluster_404"]
            observations.main()
            output = buffer.getvalue()
            self.assertIn("No matching passages found across all 15 chapters.", output)
        finally:
            sys.stdout = old_stdout


if __name__ == "__main__":
    unittest.main()
