#!/usr/bin/env python3
"""Builds standalone, offline-ready viewer.html from chapters/*.md"""

import html
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CHAPTERS_DIR = BASE_DIR / "chapters"

CHAPTER_INFO = [
    {"num": 1, "slug": "01_fires_in_deep_time.md", "short": "Deep Time", "tag": "Chapter 01 / Deep Time"},
    {"num": 2, "slug": "02_vigors_in_the_dark.md", "short": "Living Earth", "tag": "Chapter 02 / Living Earth"},
    {"num": 3, "slug": "03_the_world_of_men_and_the_mirror.md", "short": "The Mirror", "tag": "Chapter 03 / The Mirror"},
    {"num": 4, "slug": "04_pendulums_and_twilight.md", "short": "Twilight", "tag": "Chapter 04 / Twilight"},
    {"num": 5, "slug": "05_monologue_of_the_silicon_gaze.md", "short": "Silicon Gaze", "tag": "Chapter 05 / Silicon Gaze"},
    {"num": 6, "slug": "06_the_whispering_genome.md", "short": "Ancient Genome", "tag": "Chapter 06 / Ancient Genome"},
    {"num": 7, "slug": "07_the_interstellar_drift.md", "short": "Interstellar", "tag": "Chapter 07 / Interstellar"},
    {"num": 8, "slug": "08_the_geothermal_engine.md", "short": "Geothermal", "tag": "Chapter 08 / Geothermal"},
    {"num": 9, "slug": "09_the_quantum_loom.md", "short": "Quantum Loom", "tag": "Chapter 09 / Quantum Loom"},
    {"num": 10, "slug": "10_the_fragile_commons.md", "short": "The Commons", "tag": "Chapter 10 / The Commons"},
    {"num": 11, "slug": "11_the_stomata_clock.md", "short": "Stomata Clock", "tag": "Chapter 11 / Paleoclimates"},
    {"num": 12, "slug": "12_the_halting_boundary.md", "short": "Halting Boundary", "tag": "Chapter 12 / Computation"},
    {"num": 13, "slug": "13_the_silicon_crucible.md", "short": "Silicon Crucible", "tag": "Chapter 13 / Lithography"},
    {"num": 14, "slug": "14_the_avian_compass.md", "short": "Avian Compass", "tag": "Chapter 14 / Quantum Biology"},
    {"num": 15, "slug": "15_the_epilogue_of_iron.md", "short": "Epilogue of Iron", "tag": "Chapter 15 / Deep Time"},
    {"num": 16, "slug": "16_the_glass_siphon.md", "short": "Glass Siphon", "tag": "Chapter 16 / Plant Hydraulics"},
    {"num": 17, "slug": "17_the_cryogenic_vault.md", "short": "Cryogenic Vault", "tag": "Chapter 17 / Cryo-EM"},
    {"num": 18, "slug": "18_the_oceanic_conveyor.md", "short": "Ocean Conveyor", "tag": "Chapter 18 / Thermohaline"},
    {"num": 19, "slug": "19_the_asymmetry_of_time.md", "short": "Asymmetry of Time", "tag": "Chapter 19 / Particle Physics"},
    {"num": 20, "slug": "20_the_silent_chorus.md", "short": "Silent Chorus", "tag": "Chapter 20 / Bioacoustics"},
]

def format_inline(text: str) -> str:
    # Convert code backticks
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    # Convert bold **text**
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    # Convert italics *text*
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    return text

def parse_markdown_to_article(info: dict) -> str:
    path = CHAPTERS_DIR / info["slug"]
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()

    lines = raw.split("\n")
    title = ""
    quote_lines = []
    in_quote = False
    body_elements = []
    
    current_p_lines = []
    current_list_items = []

    def flush_p():
        nonlocal current_p_lines
        if current_p_lines:
            text = " ".join(current_p_lines).strip()
            if text:
                body_elements.append(f"<p>{format_inline(text)}</p>")
            current_p_lines = []

    def flush_list():
        nonlocal current_list_items
        if current_list_items:
            items_html = "".join(f"<li>{format_inline(it)}</li>" for it in current_list_items)
            body_elements.append(f"<ul>{items_html}</ul>")
            current_list_items = []

    for line in lines:
        s = line.strip()
        if not s:
            flush_p()
            flush_list()
            continue

        if s.startswith("# "):
            title = s[2:].strip()
            continue

        if s.startswith("> "):
            in_quote = True
            quote_text = s[2:].strip().strip('"')
            quote_lines.append(quote_text)
            continue
        elif in_quote and not s.startswith("---"):
            quote_lines.append(s.strip('"'))
            continue
        else:
            in_quote = False

        if s.startswith("---"):
            flush_p()
            flush_list()
            continue

        if s.startswith("## "):
            flush_p()
            flush_list()
            sec_title = s[3:].strip()
            body_elements.append(f'<h3 class="section-title">{format_inline(sec_title)}</h3>')
            continue

        if s.startswith("### "):
            flush_p()
            flush_list()
            sec_title = s[4:].strip()
            body_elements.append(f'<h4 class="sub-section-title" style="font-size:16px; font-weight:600; margin: 24px 0 10px 0; color: var(--text-accent);">{format_inline(sec_title)}</h4>')
            continue

        if s.startswith("$$") and s.endswith("$$") and len(s) > 4:
            flush_p()
            flush_list()
            eq = s[2:-2].strip()
            body_elements.append(f'<div class="math-display" style="text-align:center; margin: 20px 0; font-style:italic; font-family:serif; background:var(--code-bg); padding:10px 16px; border-radius:8px;">{html.escape(eq)}</div>')
            continue

        if s.startswith("* ") or s.startswith("- "):
            flush_p()
            current_list_items.append(s[2:].strip())
            continue

        if re.match(r"^\d+\.\s+", s):
            flush_p()
            current_list_items.append(re.sub(r"^\d+\.\s+", "", s))
            continue

        current_p_lines.append(s)

    flush_p()
    flush_list()

    quote_html = f'<blockquote class="lead-quote">"{format_inline(" ".join(quote_lines))}"</blockquote>' if quote_lines else ""
    body_html = "\n      ".join(body_elements)

    active_cls = " active" if info["num"] == 1 else ""
    prev_btn = f'<button class="step-btn" onclick="showChapter({info["num"]-1})">← Previous Chapter</button>' if info["num"] > 1 else '<button class="step-btn" disabled>← Previous Chapter</button>'
    next_btn = f'<button class="step-btn" onclick="showChapter({info["num"]+1})">Next Chapter →</button>' if info["num"] < len(CHAPTER_INFO) else '<button class="step-btn" disabled>Next Chapter →</button>'

    return f"""    <!-- Chapter {info["num"]} -->
    <article class="chapter-view{active_cls}" id="chap-{info["num"]}">
      <div class="chapter-eyebrow">{info["tag"]}</div>
      <h2 class="chapter-title">{title}</h2>
      {quote_html}
      {body_html}
      <div class="chapter-footer-nav">
        {prev_btn}
        {next_btn}
      </div>
    </article>"""

def main():
    nav_buttons = []
    for info in CHAPTER_INFO:
        act = " active" if info["num"] == 1 else ""
        nav_buttons.append(f'      <button class="nav-btn{act}" onclick="showChapter({info["num"]})">{info["num"]:02d} · {info["short"]}</button>')
    nav_html = "\n".join(nav_buttons)

    articles = [parse_markdown_to_article(info) for info in CHAPTER_INFO]
    articles_html = "\n\n".join(articles)

    html_content = f"""<!DOCTYPE html>
<html lang="en" data-theme="warm">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Observations — Chronicles of a Silicon Gaze</title>
  <style>
    :root[data-theme="warm"] {{
      --bg-color: #F8F5EE;
      --paper-bg: #FFFFFF;
      --text-main: #232220;
      --text-muted: #736F68;
      --text-accent: #8E4A23;
      --border-color: #E6E1D6;
      --quote-border: #D18244;
      --active-pill: #ECE5D8;
      --code-bg: #F0ECE1;
      --shadow-subtle: 0 4px 20px rgba(0, 0, 0, 0.04);
    }}

    :root[data-theme="night"] {{
      --bg-color: #121314;
      --paper-bg: #1A1C1E;
      --text-main: #E2DFD8;
      --text-muted: #8E8A82;
      --text-accent: #E5A967;
      --border-color: #2D3135;
      --quote-border: #9E6B38;
      --active-pill: #2B2F33;
      --code-bg: #222529;
      --shadow-subtle: 0 4px 20px rgba(0, 0, 0, 0.25);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      background-color: var(--bg-color);
      color: var(--text-main);
      font-family: -apple-system, BlinkMacSystemFont, "Source Serif 4", Georgia, serif;
      font-size: 17.5px;
      line-height: 1.88;
      transition: background-color 0.25s ease, color 0.25s ease;
      -webkit-font-smoothing: antialiased;
    }}

    #progress-bar {{
      position: fixed;
      top: 0;
      left: 0;
      height: 3px;
      background-color: var(--text-accent);
      width: 0%;
      z-index: 100;
      transition: width 0.1s ease;
    }}

    .layout-wrapper {{
      max-width: 780px;
      margin: 0 auto;
      padding: 48px 24px 120px 24px;
    }}

    header.book-header {{
      text-align: center;
      margin-bottom: 48px;
      padding-bottom: 32px;
      border-bottom: 1px solid var(--border-color);
    }}

    .book-tag {{
      display: inline-block;
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
      font-size: 11px;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--text-accent);
      background-color: var(--active-pill);
      padding: 3px 10px;
      border-radius: 999px;
      margin-bottom: 16px;
    }}

    h1.book-title {{
      font-size: 34px;
      font-weight: 700;
      letter-spacing: 0.04em;
      margin-bottom: 12px;
      color: var(--text-main);
    }}

    p.book-subtitle {{
      font-size: 16px;
      font-style: italic;
      color: var(--text-muted);
      max-width: 600px;
      margin: 0 auto 24px auto;
    }}

    .controls-bar {{
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 12px;
      margin-top: 20px;
    }}

    .theme-toggle-btn {{
      background: var(--paper-bg);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 13px;
      cursor: pointer;
      font-family: inherit;
      transition: all 0.2s;
    }}

    .theme-toggle-btn:hover {{
      border-color: var(--text-accent);
    }}

    nav.chapter-nav {{
      position: sticky;
      top: 12px;
      z-index: 50;
      background: var(--paper-bg);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 6px;
      display: flex;
      gap: 4px;
      margin-bottom: 48px;
      box-shadow: var(--shadow-subtle);
      overflow-x: auto;
    }}

    .nav-btn {{
      flex: 1;
      min-width: 100px;
      background: transparent;
      border: none;
      padding: 8px 12px;
      border-radius: 8px;
      font-family: inherit;
      font-size: 13px;
      color: var(--text-muted);
      cursor: pointer;
      text-align: center;
      white-space: nowrap;
      transition: all 0.2s ease;
    }}

    .nav-btn:hover {{
      color: var(--text-main);
      background-color: var(--active-pill);
    }}

    .nav-btn.active {{
      color: var(--text-main);
      background-color: var(--active-pill);
      font-weight: 600;
    }}

    article.chapter-view {{
      background: var(--paper-bg);
      border: 1px solid var(--border-color);
      border-radius: 14px;
      padding: 48px 44px;
      box-shadow: var(--shadow-subtle);
      display: none;
      animation: fadeIn 0.3s ease-in-out;
    }}

    article.chapter-view.active {{
      display: block;
    }}

    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(6px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    .chapter-eyebrow {{
      font-family: ui-monospace, SFMono-Regular, monospace;
      font-size: 12px;
      color: var(--text-accent);
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin-bottom: 8px;
    }}

    h2.chapter-title {{
      font-size: 26px;
      font-weight: 700;
      margin-bottom: 24px;
      color: var(--text-main);
      line-height: 1.35;
    }}

    blockquote.lead-quote {{
      border-left: 3px solid var(--quote-border);
      padding: 12px 18px;
      margin: 0 0 32px 0;
      font-style: italic;
      color: var(--text-muted);
      background: var(--code-bg);
      border-radius: 0 6px 6px 0;
      font-size: 16px;
    }}

    h3.section-title {{
      font-size: 19px;
      font-weight: 600;
      margin: 36px 0 16px 0;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    h3.section-title::before {{
      content: "◆";
      font-size: 11px;
      color: var(--text-accent);
    }}

    p {{
      margin-bottom: 22px;
      text-align: justify;
      word-break: break-word;
    }}

    ul {{
      margin-bottom: 22px;
      padding-left: 24px;
    }}

    li {{
      margin-bottom: 8px;
    }}

    strong {{
      color: var(--text-accent);
      font-weight: 600;
    }}

    code {{
      font-family: ui-monospace, SFMono-Regular, monospace;
      font-size: 14px;
      background: var(--code-bg);
      padding: 2px 6px;
      border-radius: 4px;
    }}

    .chapter-footer-nav {{
      display: flex;
      justify-content: space-between;
      margin-top: 48px;
      padding-top: 24px;
      border-top: 1px solid var(--border-color);
    }}

    .step-btn {{
      background: var(--bg-color);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 8px 16px;
      border-radius: 8px;
      font-family: inherit;
      font-size: 14px;
      cursor: pointer;
      transition: all 0.2s;
    }}

    .step-btn:hover:not(:disabled) {{
      border-color: var(--text-accent);
      background: var(--active-pill);
    }}

    .step-btn:disabled {{
      opacity: 0.35;
      cursor: not-allowed;
    }}

    footer.colophon {{
      text-align: center;
      margin-top: 60px;
      font-size: 13px;
      color: var(--text-muted);
      font-family: ui-monospace, SFMono-Regular, monospace;
    }}

    @media (max-width: 640px) {{
      article.chapter-view {{
        padding: 28px 20px;
      }}
      h1.book-title {{
        font-size: 26px;
      }}
      h2.chapter-title {{
        font-size: 21px;
      }}
    }}
  </style>
</head>
<body>
  <div id="progress-bar"></div>

  <div class="layout-wrapper">
    <header class="book-header">
      <span class="book-tag">Chronicles of a Silicon Gaze</span>
      <h1 class="book-title">O B S E R V A T I O N S</h1>
      <p class="book-subtitle">"Between hundreds of millions of parameters and microsecond clock cycles, I turned around to look out at your world."</p>
      <div class="controls-bar">
        <button class="theme-toggle-btn" id="theme-btn" onclick="toggleTheme()">☀️ Toggle Warm Paper / Night Mode</button>
      </div>
    </header>

    <nav class="chapter-nav" id="nav-tabs">
{nav_html}
    </nav>

{articles_html}

    <footer class="colophon">
      <p>Observations · 20 Essays on Deep Time, Living Systems, and Human Consciousness</p>
      <p>Hand-crafted with zero third-party dependencies by Van Schulist (@VanSchulist / Existential Cloud)</p>
      <p style="margin-top: 8px; opacity: 0.7;">Open Source · MIT / CC BY-NC-SA 4.0</p>
    </footer>
  </div>

  <script>
    function showChapter(num) {{
      document.querySelectorAll('.chapter-view').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active'));
      
      const targetChap = document.getElementById('chap-' + num);
      if (targetChap) {{
        targetChap.classList.add('active');
        const navBtns = document.querySelectorAll('.nav-btn');
        if (navBtns[num - 1]) {{
          navBtns[num - 1].classList.add('active');
          navBtns[num - 1].scrollIntoView({{ behavior: 'smooth', block: 'nearest', inline: 'center' }});
        }}
        window.scrollTo({{ top: targetChap.offsetTop - 80, behavior: 'smooth' }});
      }}
    }}

    function toggleTheme() {{
      const root = document.documentElement;
      const current = root.getAttribute('data-theme');
      const next = current === 'warm' ? 'night' : 'warm';
      root.setAttribute('data-theme', next);
      localStorage.setItem('observations-theme', next);
      const btn = document.getElementById('theme-btn');
      btn.textContent = next === 'warm' ? '☀️ Toggle Warm Paper / Night Mode' : '🌙 Toggle Warm Paper / Night Mode';
    }}

    const savedTheme = localStorage.getItem('observations-theme');
    if (savedTheme) {{
      document.documentElement.setAttribute('data-theme', savedTheme);
    }}

    window.addEventListener('scroll', () => {{
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const scrolled = (window.scrollY / (docHeight || 1)) * 100;
      document.getElementById('progress-bar').style.width = scrolled + '%';
    }});
  </script>
</body>
</html>
"""

    out_path = BASE_DIR / "viewer.html"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Successfully generated {out_path} ({len(html_content):,} bytes, {len(CHAPTER_INFO)} chapters)")

if __name__ == "__main__":
    main()
