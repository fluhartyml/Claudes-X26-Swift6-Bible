#!/usr/bin/env python3
"""
Publish the book chapters to the GitHub Wiki for
fluhartyml/Claudes-X26-Swift6-Bible.

Strategy:
- Clone (or pull) the .wiki.git repo into ~/Developer.complex/Claudes-X26-Swift6-Bible.wiki
- Read each canonical BibleContent.bundle/Part-X/Book-NN-Title.html chapter source,
  convert to Markdown via the in-script html_to_md() converter, and write to the
  wiki as Book-NN-Title.md with a Jekyll-style header + navigation links.
- Write / refresh Chapters-and-Appendices.md as the wiki's chapter index.
- Rewrite Home.md to point at Issues, Discussions, email, the reader app,
  and the chapter index.
- git add / commit / push.

HTML is canonical (per project_bible_html_canonical memory rule). Markdown is
generated at publish time, never hand-maintained. Run this whenever the book
content changes. Idempotent — re-running produces the same wiki state for a
given source.
"""

import html as html_mod
import re
import subprocess
from pathlib import Path

BOOK_DIR   = Path("/Users/michaelfluharty/Developer.complex/inkwell/Claudes X26 Swift6 Bible/Claudes X26 Swift6 Bible/BibleContent.bundle")
WIKI_REPO  = "https://github.com/fluhartyml/Claudes-X26-Swift6-Bible.wiki.git"
WIKI_LOCAL = Path.home() / "Developer.complex" / "Claudes-X26-Swift6-Bible.wiki"

REPO_BASE  = "https://github.com/fluhartyml/Claudes-X26-Swift6-Bible"
WIKI_BASE  = f"{REPO_BASE}/wiki"
ISSUES     = f"{REPO_BASE}/issues/new/choose"
DISCUSSIONS= f"{REPO_BASE}/discussions"
EMAIL      = "michael.fluharty@mac.com"
MAILTO     = f"mailto:{EMAIL}?subject=%5BX26%20Bible%20feedback%5D"


BOOKS = [
    # (number, title_slug, part_label, part_subdir)
    ( 1, "Introducing-Swift-And-Xcode",                "Part I — Introduction",          "Part-I-Introduction"),
    ( 2, "Introducing-SwiftUI-Views",                  "Part I — Introduction",          "Part-I-Introduction"),
    ( 3, "Introducing-Scenes-And-Windows",             "Part I — Introduction",          "Part-I-Introduction"),
    ( 4, "Gestures-And-Input",                         "Part III — The User Interface", "Part-III-The-User-Interface"),
    ( 5, "Menus-And-Navigation",                       "Part III — The User Interface", "Part-III-The-User-Interface"),
    ( 6, "Controls-Buttons-Toggles-Pickers",           "Part III — The User Interface", "Part-III-The-User-Interface"),
    ( 7, "Toolbars-And-Tab-Views",                     "Part III — The User Interface", "Part-III-The-User-Interface"),
    ( 8, "Lists-Grids-And-ForEach",                    "Part III — The User Interface", "Part-III-The-User-Interface"),
    ( 9, "Text-And-TextField",                         "Part III — The User Interface", "Part-III-The-User-Interface"),
    (10, "TextEditor-And-AttributedString",            "Part III — The User Interface", "Part-III-The-User-Interface"),
    (11, "FileManager-And-Documents",                  "Part III — The User Interface", "Part-III-The-User-Interface"),
    (12, "Sheets-Alerts-And-Confirmations",            "Part III — The User Interface", "Part-III-The-User-Interface"),
    (13, "Multi-Window-And-NavigationSplitView",       "Part IV — The Application",     "Part-IV-The-Application"),
    (14, "Clipboard-DragDrop-ShareSheet",              "Part IV — The Application",     "Part-IV-The-Application"),
    (15, "SwiftData-And-CoreData",                     "Part IV — The Application",     "Part-IV-The-Application"),
    (16, "Extensions-And-Packages",                    "Part IV — The Application",     "Part-IV-The-Application"),
    (17, "Swift-Charts-And-PDFKit",                    "Part IV — The Application",     "Part-IV-The-Application"),
    (18, "Error-Handling-And-Result-Type",             "Part V — Advanced Techniques",  "Part-V-Advanced-Techniques"),
    (19, "Building-Custom-Views-And-Modifiers",        "Part V — Advanced Techniques",  "Part-V-Advanced-Techniques"),
    (20, "Performance-Instruments-And-Best-Practices", "Part V — Advanced Techniques",  "Part-V-Advanced-Techniques"),
    (21, "Git-And-GitHub",                             "Part VI — The Modern Toolchain","Part-VI-The-Modern-Toolchain"),
    (22, "AI-Chatbot-Integration",                     "Part VI — The Modern Toolchain","Part-VI-The-Modern-Toolchain"),
]


def run(cmd, cwd=None, check=True):
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"$ {' '.join(cmd)}")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
        raise SystemExit(result.returncode)
    return result


def ensure_wiki_clone():
    if WIKI_LOCAL.exists() and (WIKI_LOCAL / ".git").exists():
        print(f"Wiki clone exists at {WIKI_LOCAL}; pulling latest.")
        run(["git", "fetch", "origin"], cwd=WIKI_LOCAL)
        run(["git", "reset", "--hard", "origin/master"], cwd=WIKI_LOCAL, check=False)
        run(["git", "reset", "--hard", "origin/main"],   cwd=WIKI_LOCAL, check=False)
    else:
        print(f"Cloning wiki to {WIKI_LOCAL}")
        WIKI_LOCAL.parent.mkdir(parents=True, exist_ok=True)
        run(["git", "clone", WIKI_REPO, str(WIKI_LOCAL)])


def wiki_page_name(n: int, slug: str) -> str:
    return f"Book-{n:02d}-{slug}"


def prev_next_nav(idx: int):
    pieces = []
    if idx > 0:
        p = BOOKS[idx - 1]
        pieces.append(f"← [[{wiki_page_name(p[0], p[1])}]]")
    pieces.append("[[Chapters and Appendices|Chapters-and-Appendices]]")
    if idx < len(BOOKS) - 1:
        n = BOOKS[idx + 1]
        pieces.append(f"[[{wiki_page_name(n[0], n[1])}]] →")
    return " · ".join(pieces)


def strip_first_h1(md: str) -> str:
    """Drop the source's leading `# Chapter N: ...` line; we write our own."""
    lines = md.splitlines()
    for i, ln in enumerate(lines):
        if ln.startswith("# "):
            return "\n".join(lines[i + 1:])
    return md


def _convert_inline(text: str) -> str:
    """Convert inline HTML tags to Markdown equivalents."""
    # Order matters — handle nested constructs first
    text = re.sub(r'<strong>(.*?)</strong>', r'**\1**', text, flags=re.DOTALL)
    text = re.sub(r'<em>(.*?)</em>', r'*\1*', text, flags=re.DOTALL)
    text = re.sub(r'<code(?:\s[^>]*)?>(.*?)</code>', r'`\1`', text, flags=re.DOTALL)
    text = re.sub(r'<a\s+href="([^"]+)"[^>]*>(.*?)</a>', r'[\2](\1)', text, flags=re.DOTALL)
    # Footnote refs: <sup>[<a href="#X">N</a>]</sup> → [^N]
    text = re.sub(r'<sup>\s*\[?\s*<a\s+href="#([^"]+)"[^>]*>([^<]+)</a>\s*\]?\s*</sup>', r'[^\2]', text, flags=re.DOTALL)
    text = re.sub(r'<sup>([^<]*)</sup>', r'[\1]', text, flags=re.DOTALL)
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = html_mod.unescape(text)
    return text


def _convert_block(block: str) -> str:
    """Convert a single <li>...</li> inner block to Markdown."""
    block = block.strip()
    if not block:
        return ""
    # Skip footnote wrapper anchors but keep their text
    block = re.sub(r'<a\s+id="[^"]+"\s*></a>', '', block)
    # Heading 1 — script writes its own header so drop chapter H1
    if re.match(r'^<h1>.*</h1>$', block, re.DOTALL):
        return ""
    if re.match(r'^<h2>.*</h2>$', block, re.DOTALL):
        return f"## {_convert_inline(re.sub(r'^<h2>|</h2>$', '', block))}"
    if re.match(r'^<h3>.*</h3>$', block, re.DOTALL):
        return f"### {_convert_inline(re.sub(r'^<h3>|</h3>$', '', block))}"
    if block in ("<hr>", "<hr/>", "<hr />"):
        return "---"
    # Paragraph
    m = re.match(r'^<p>(.*)</p>$', block, re.DOTALL)
    if m:
        return _convert_inline(m.group(1))
    # Unordered list
    m = re.match(r'^<ul>(.*)</ul>$', block, re.DOTALL)
    if m:
        items = re.findall(r'<li>(.*?)</li>', m.group(1), re.DOTALL)
        return "\n".join(f"- {_convert_inline(item.strip())}" for item in items)
    # Ordered list
    m = re.match(r'^<ol class="body-list">(.*)</ol>$', block, re.DOTALL)
    if m:
        items = re.findall(r'<li>(.*?)</li>', m.group(1), re.DOTALL)
        return "\n".join(f"{i+1}. {_convert_inline(item.strip())}" for i, item in enumerate(items))
    # Code block
    m = re.match(r'^<pre><code(?:\s+class="lang-([^"]*)")?>(.*?)</code></pre>$', block, re.DOTALL)
    if m:
        lang = (m.group(1) or "").strip() or "swift"
        code = html_mod.unescape(m.group(2))
        return f"```{lang}\n{code}\n```"
    # Scope note → blockquote (preserves the visual emphasis)
    m = re.match(r'^<div class="scope-note">(.*)</div>$', block, re.DOTALL)
    if m:
        inner = _convert_inline(m.group(1).strip())
        return "> " + inner.replace("\n", "\n> ")
    # Table — keep as raw HTML (markdown supports inline HTML on GitHub wiki)
    if block.startswith("<table>") or block.startswith("<table "):
        return block
    # Footnote definitions ID anchor pattern: <a id="..."></a>... or list items
    if 'id="' in block and 'fn' in block.lower():
        return _convert_inline(block)
    # Fallback — strip outer <li> if any leftover and convert inline
    return _convert_inline(block)


def html_to_md(html_text: str) -> str:
    """Convert a templated chapter HTML file to Markdown for wiki publishing.

    The chapter format is highly templated: every line is wrapped in
    <li>...</li> inside <ol class="lines">. Each <li> contains exactly one
    logical block (heading, paragraph, list, code block, hr, scope-note, etc.).
    Page chrome (<head>, <header class="page">, <footer class="page">, <style>)
    is dropped.
    """
    # Extract the line-numbered body
    m = re.search(r'<ol class="lines">(.*?)</ol>\s*</div>', html_text, re.DOTALL)
    if not m:
        m = re.search(r'<ol class="lines">(.*?)</ol>', html_text, re.DOTALL)
        if not m:
            return ""
    body = m.group(1)
    # Iterate <li>...</li> blocks (use a simple state-tracking split to handle
    # nested <li> in <ul>/<ol>)
    blocks = []
    depth = 0
    buf = []
    i = 0
    # Find all top-level <li>...</li> by tracking <li> open/close depth
    # We split on <li> at depth 0, then find matching </li>
    pattern = re.compile(r'<(/?)li\b[^>]*>')
    pos = 0
    open_starts = []
    for match in pattern.finditer(body):
        is_close = match.group(1) == "/"
        if is_close:
            if depth > 0:
                depth -= 1
                if depth == 0 and open_starts:
                    start = open_starts.pop()
                    inner = body[start:match.start()]
                    blocks.append(inner)
            else:
                # stray close, ignore
                pass
        else:
            if depth == 0:
                open_starts.append(match.end())
            depth += 1
    md_parts = []
    for block in blocks:
        md = _convert_block(block)
        if md:
            md_parts.append(md)
    return "\n\n".join(md_parts)


def publish_chapter(idx: int):
    n, slug, part, part_subdir = BOOKS[idx]
    src = BOOK_DIR / part_subdir / f"Book-{n:02d}-{slug}.html"
    if not src.exists() or src.stat().st_size == 0:
        print(f"  skip Book {n:02d} (no source at {src})")
        return

    html_text = src.read_text(encoding="utf-8")
    body = html_to_md(html_text).lstrip("\n")

    title_human = slug.replace("-", " ")
    page = wiki_page_name(n, slug)
    out = WIKI_LOCAL / f"{page}.md"

    header = (
        f"# Book {n:02d}: {title_human}\n"
        f"\n"
        f"*{part} · Claude's Xcode 26 Swift Bible*\n"
        f"\n"
        f"{prev_next_nav(idx)}\n"
        f"\n"
        f"---\n"
        f"\n"
    )
    footer = (
        f"\n\n---\n"
        f"\n"
        f"{prev_next_nav(idx)}\n"
        f"\n"
        f"**Feedback:** Found something off? "
        f"[Open an issue]({ISSUES}) · "
        f"[Discuss it]({DISCUSSIONS}) · "
        f"[Email Michael]({MAILTO})\n"
    )

    out.write_text(header + body + footer, encoding="utf-8")
    print(f"  wrote {out.name}")


def write_chapter_index():
    lines = [
        "# Chapters and Appendices",
        "",
        "Every Book in Claude's Xcode 26 Swift Bible, in reading order. "
        "Click a title to read it on the Wiki; the same content renders with "
        "the full amber / line-numbered layout in the reader app.",
        "",
    ]
    last_part = None
    for idx, (n, slug, part, _part_subdir) in enumerate(BOOKS):
        if part != last_part:
            lines.append(f"\n## {part}\n")
            last_part = part
        page = wiki_page_name(n, slug)
        label = f"Book {n:02d} — {slug.replace('-', ' ')}"
        lines.append(f"- [[{label}|{page}]]")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"**Feedback:** [Issues]({ISSUES}) · [Discussions]({DISCUSSIONS}) · "
                 f"[Email]({MAILTO})")
    (WIKI_LOCAL / "Chapters-and-Appendices.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )
    print("  wrote Chapters-and-Appendices.md")


def rewrite_home():
    home = WIKI_LOCAL / "Home.md"
    content = f"""# Claude's X26 Swift6 Bible

![Claude's X26 Swift6 Bible](claudes-x26-swift6-bible-hero.png)

**Version 1.0 (pre-release)** — a living reference for Swift 6, SwiftUI, and Xcode 26 development on Apple platforms.

The book has two reading surfaces:

- **Reader app** (recommended): the native iOS / iPadOS / macOS app in this repo. Amber-on-black layout, line-numbered pages, full-vault search, cross-device last-page sync.
- **Web reader** (this wiki): plain-markdown copies of every chapter, browsable in any web browser. Same content, different styling.

## Start reading

- [[Chapters and Appendices|Chapters-and-Appendices]] — the full table of contents

## Talk to us

Three channels depending on what you want to say:

- **[Issues]({ISSUES})** — errata, broken links, wrong code, things that need a fix
- **[Discussions]({DISCUSSIONS})** — open-ended questions, show-and-tell of what you're building, reader-to-reader help
- **[Email Michael]({MAILTO})** — private feedback or anything you'd rather not post publicly

The reader app's **Info → Send Feedback** menu item pre-fills an email with the page you were looking at.

## Project resources

- [[Developer Notes|Developer-Notes]] — mission, roadmap, architecture decisions for the reader app
- [Source repository]({REPO_BASE})
- [Releases]({REPO_BASE}/releases)

## License

GPL v3 — share and share alike, attribution required.

## Attribution

Structure inspired by Tom Swan's *Delphi 4 Bible* (IDG Books, 1998). The reader app and all vault content are original work.
"""
    home.write_text(content, encoding="utf-8")
    print("  wrote Home.md")


def commit_and_push():
    run(["git", "add", "-A"], cwd=WIKI_LOCAL)
    diff = run(["git", "status", "--porcelain"], cwd=WIKI_LOCAL)
    if not diff.stdout.strip():
        print("Wiki already up to date, nothing to push.")
        return
    run(["git", "commit", "-m", "Sync book chapters and refresh Home + chapter index"], cwd=WIKI_LOCAL)
    run(["git", "push"], cwd=WIKI_LOCAL)
    print("Wiki pushed.")


def main():
    ensure_wiki_clone()
    print("Publishing chapters...")
    for idx in range(len(BOOKS)):
        publish_chapter(idx)
    print("Refreshing index and home...")
    write_chapter_index()
    rewrite_home()
    commit_and_push()


if __name__ == "__main__":
    main()
