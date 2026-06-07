#!/usr/bin/env python3
"""Refatora index.html monolítico em estrutura modular AXIOM."""
from __future__ import annotations

import base64
import re
import shutil
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
SRC = SITE / "index.html"
BACKUP = SITE / "index.html.backup"

IMAGE_SPECS = [
    (r'class="nav-logo"><img\s+src="data:image/[^"]+"', "logo-nav", "nav"),
    (r'class="hero-bg-image"[^>]*src="data:image/[^"]+"', "hero-visual", "hero"),
    (r'alt="Marcos Batista"\s+src="data:image/[^"]+"', "profile-marcos", "profile"),
]


def read_html() -> str:
    return SRC.read_text(encoding="utf-8")


def extract_style_sections(css_raw: str) -> list[tuple[str, str]]:
    pattern = re.compile(r"(/\* [═─][^\n]*[═─][^\n]*\*/)", re.MULTILINE)
    parts = pattern.split(css_raw)
    sections: list[tuple[str, str]] = []
    if parts[0].strip():
        sections.append(("00-foundation", parts[0]))
    i = 1
    idx = 1
    while i < len(parts):
        header = parts[i]
        body = parts[i + 1] if i + 1 < len(parts) else ""
        slug = _slug_from_header(header) or f"{idx:02d}-section"
        sections.append((slug, (header + body).strip()))
        idx += 1
        i += 2
    return sections


def _slug_from_header(header: str) -> str:
    t = re.sub(r"[/*═─\s]+", " ", header).strip().lower()
    rules = [
        ("foundation", "00-foundation"),
        ("background", "01-backgrounds"),
        ("scroll progress", "02-scroll-progress"),
        ("navigation", "03-navigation"),
        ("main content", "04-slides"),
        ("glass", "05-glass"),
        ("animation", "06-animations"),
        ("typography", "07-typography"),
        ("button", "08-buttons"),
        ("cards", "09-cards"),
        ("badge", "10-badges"),
        ("section decoration", "11-decorations"),
        ("profile", "12-profile"),
        ("grid", "13-grids"),
        ("hero", "14-hero"),
        ("empresa", "15-empresa"),
        ("idealizador", "16-idealizador"),
        ("diagn", "17-diagnostico"),
        ("contato", "18-contato"),
        ("chatbot", "19-chatbot"),
        ("lead", "20-lead-form"),
        ("performance", "21-performance"),
        ("metric", "22-metrics"),
        ("step", "23-steps"),
        ("two-col", "24-layout-utils"),
    ]
    for needle, slug in rules:
        if needle in t:
            return slug
    safe = re.sub(r"[^a-z0-9]+", "-", t)[:36].strip("-")
    return f"99-{safe}" if safe else ""


def build_css_files(css_raw: str) -> None:
    css_dir = SITE / "assets" / "css"
    css_dir.mkdir(parents=True, exist_ok=True)
    seen: dict[str, int] = {}
    imports: list[str] = []
    for name, content in extract_style_sections(css_raw):
        key = name
        if key in seen:
            seen[key] += 1
            key = f"{name}-{seen[name]}"
        else:
            seen[name] = 0
        fname = f"{key}.css"
        (css_dir / fname).write_text(content + "\n", encoding="utf-8")
        imports.append(fname)
    main = "/* AXIOM Strategic Intelligence — stylesheet entry */\n"
    main += "\n".join(f'@import "./{f}";' for f in imports) + "\n"
    (css_dir / "main.css").write_text(main, encoding="utf-8")


def extract_images(html: str) -> str:
    images_dir = SITE / "assets" / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    def save_and_replace(full_match: str, filename_stem: str) -> str:
        m = re.search(r"data:image/([\w+.-]+);base64,([A-Za-z0-9+/=]+)", full_match)
        if not m:
            return full_match
        mime, b64 = m.group(1), m.group(2)
        ext = "jpg" if "jpeg" in mime or "jpg" in mime else "png" if "png" in mime else "webp"
        out = images_dir / f"{filename_stem}.{ext}"
        out.write_bytes(base64.b64decode(b64))
        return full_match.replace(m.group(0), f"assets/images/{filename_stem}.{ext}")

    for pattern, stem, _ in IMAGE_SPECS:
        html = re.sub(
            pattern,
            lambda m, s=stem: save_and_replace(m.group(0), s),
            html,
            count=1,
        )
    return html


def fix_diagnostico_fences(html: str) -> str:
    return html.replace("        ```\n", "")


def remove_debug_fetch(js: str) -> str:
    return re.sub(r"\s*// #region agent log.*?// #endregion", "", js, flags=re.DOTALL)


def write_js_modules(html: str) -> str:
    js_dir = SITE / "assets" / "js"
    vendors = js_dir / "vendors"
    modules = js_dir / "modules"
    vendors.mkdir(parents=True, exist_ok=True)
    modules.mkdir(parents=True, exist_ok=True)

    unicorn_main = """(function loadUnicornStudio() {
  if (window.UnicornStudio) return;
  window.UnicornStudio = { isInitialized: false };
  const script = document.createElement("script");
  script.src =
    "https://cdn.jsdelivr.net/gh/hiunicornstudio/unicornstudio.js@v1.4.29/dist/unicornStudio.umd.js";
  script.onload = function () {
    if (!window.UnicornStudio.isInitialized) {
      UnicornStudio.init();
      window.UnicornStudio.isInitialized = true;
    }
  };
  (document.head || document.body).appendChild(script);
})();
"""
    unicorn_contato = """(function initContatoUnicorn() {
  if (window.UnicornStudio) {
    try { window.UnicornStudio.init(); } catch (e) {}
    return;
  }
  window.UnicornStudio = { isInitialized: false };
  const script = document.createElement("script");
  script.src =
    "https://cdn.jsdelivr.net/gh/hiunicornstudio/unicornstudio.js@v1.4.29/dist/unicornStudio.umd.js";
  script.onload = function () {
    if (!window.UnicornStudio.isInitialized) {
      UnicornStudio.init();
      window.UnicornStudio.isInitialized = true;
    }
  };
  (document.head || document.body).appendChild(script);
})();
"""
    (vendors / "unicorn-loader-main.js").write_text(unicorn_main, encoding="utf-8")
    (vendors / "unicorn-loader-contato.js").write_text(unicorn_contato, encoding="utf-8")

    html = re.sub(
        r'<script type="text/javascript">\s*!function \(\) \{ if \(!window\.UnicornStudio\).*?</script>',
        '<script src="assets/js/vendors/unicorn-loader-main.js" defer></script>',
        html,
        count=1,
        flags=re.DOTALL,
    )
    html = re.sub(
        r'<script type="text/javascript">\s*!function \(\) \{ if \(window\.UnicornStudio\).*?</script>',
        '<script src="assets/js/vendors/unicorn-loader-contato.js" defer></script>',
        html,
        count=1,
        flags=re.DOTALL,
    )

    main_match = re.search(
        r"<script>\s*(// ─── SCROLL PROGRESS[\s\S]*?)\s*</script>\s*(?=<script data-img-fallback)",
        html,
    )
    if main_match:
        block = remove_debug_fetch(main_match.group(1))
        parts = re.split(r"// ─── CHATBOT COMERCIAL ─+", block, maxsplit=1)
        scroll_js = parts[0].strip()
        (modules / "scroll-ui.js").write_text(scroll_js + "\n", encoding="utf-8")
        if len(parts) > 1:
            chatbot_js = parts[1].lstrip("─ \n")
            (modules / "chatbot.js").write_text(chatbot_js + "\n", encoding="utf-8")
        html = html.replace(main_match.group(0), "")

    fb = re.search(r'<script data-img-fallback-handler="">([\s\S]*?)</script>', html)
    if fb:
        (vendors / "img-fallback.js").write_text(fb.group(1).strip() + "\n", encoding="utf-8")
        html = html.replace(
            fb.group(0),
            '<script src="assets/js/vendors/img-fallback.js" defer></script>',
        )

    (js_dir / "config.js").write_text(
        """/** Configuração global — rotas, API, novas páginas */
window.AXIOM = Object.freeze({
  siteName: "AXIOM Strategic Intelligence",
  lang: "pt-BR",
  chatbot: {
    endpoint: "",
  },
  leadForm: {
    endpoint: "",
  },
  pages: {
    home: "index.html",
  },
  unicorn: {
    mainProjectId: "yWZ2Tbe094Fsjgy9NRnD",
    contatoProjectId: "UtvhDctN8AjL6tvf1yKd",
  },
});
""",
        encoding="utf-8",
    )

    (js_dir / "main.js").write_text(
        'document.addEventListener("DOMContentLoaded", () => { /* módulos auto-init */ });\n',
        encoding="utf-8",
    )

    inject = """
  <script src="assets/js/config.js"></script>
  <script src="assets/js/modules/scroll-ui.js" defer></script>
  <script src="assets/js/modules/chatbot.js" defer></script>
  <script src="assets/js/main.js" defer></script>
"""
    html = html.replace("</body>", inject + "</body>")
    return html


def main() -> None:
    html = read_html()
    if not BACKUP.exists():
        shutil.copy2(SRC, BACKUP)

    style = re.search(r"<style>([\s\S]*?)</style>", html)
    if not style:
        raise SystemExit("style block missing")
    build_css_files(style.group(1))
    html = html.replace(
        style.group(0),
        '  <link rel="stylesheet" href="assets/css/main.css" />',
    )

    html = fix_diagnostico_fences(html)
    html = extract_images(html)
    html = write_js_modules(html)

    SRC.write_text(html, encoding="utf-8")
    print("OK", SRC, "bytes:", SRC.stat().st_size)


if __name__ == "__main__":
    main()
