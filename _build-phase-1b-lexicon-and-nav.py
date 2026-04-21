#!/usr/bin/env python3
"""
Phase 1b: Lexicon Pages + Chapter indexes + TOC + Index regeneration.

Generates:
- 125 skeletal Page-*.html in Part-II-The-Swift-Language/Chapter-X/Pages/
  using the locked 6-slot format: headword · definition · Swift example ·
  Rosetta Stone (Pascal/BASIC/C) · related · sources
- 26 Chapter-*.html pages listing their entries as clickable links
- Fresh table-of-contents.html with full Part→Book→Chapter→Page hierarchy
- Fresh claudex26-index.html as an alphabetical A-Z index

Every page uses the universal template: line numbers, outline numbering,
matching header+footer with file path (extension hidden) and position.
"""

import re
from pathlib import Path

BUNDLE = Path(
    "/Users/michaelfluharty/Developer.complex/inkwell/"
    "Claudes X26 Swift6 Bible/Claudes X26 Swift6 Bible/BibleContent.bundle"
)

# ---------- 125-entry Lexicon ----------

ENTRIES = {
    'A': [
        ('actor', 'keyword'),
        ('any', 'keyword'),
        ('Any', 'type'),
        ('AnyObject', 'type'),
        ('as', 'keyword'),
        ('async', 'keyword'),
        ('await', 'keyword'),
        ('@autoclosure', 'attribute'),
        ('@available', 'attribute'),
        ('Array', 'type'),
    ],
    'B': [
        ('Bool', 'type'),
        ('break', 'keyword'),
        ('@Binding', 'attribute-swiftui'),
    ],
    'C': [
        ('case', 'keyword'),
        ('catch', 'keyword'),
        ('Character', 'type'),
        ('class', 'keyword'),
        ('closure', 'concept'),
        ('Codable', 'protocol'),
        ('Collection', 'protocol'),
        ('Comparable', 'protocol'),
        ('continue', 'keyword'),
        ('convenience', 'modifier'),
        ('CaseIterable', 'protocol'),
    ],
    'D': [
        ('defer', 'keyword'),
        ('deinit', 'keyword'),
        ('Decodable', 'protocol'),
        ('default', 'keyword'),
        ('Dictionary', 'type'),
        ('do', 'keyword'),
        ('Double', 'type'),
        ('dynamic', 'modifier'),
        ('@discardableResult', 'attribute'),
    ],
    'E': [
        ('else', 'keyword'),
        ('Encodable', 'protocol'),
        ('enum', 'keyword'),
        ('Equatable', 'protocol'),
        ('Error', 'protocol'),
        ('extension', 'keyword'),
        ('@escaping', 'attribute'),
        ('@Environment', 'attribute-swiftui'),
        ('@EnvironmentObject', 'attribute-swiftui'),
        ('ExpressibleByStringLiteral', 'protocol'),
        ('#elseif', 'directive'),
        ('#endif', 'directive'),
        ('#error', 'directive'),
    ],
    'F': [
        ('fallthrough', 'keyword'),
        ('false', 'literal'),
        ('fileprivate', 'access-level'),
        ('final', 'modifier'),
        ('Float', 'type'),
        ('for', 'keyword'),
        ('func', 'keyword'),
        ('@frozen', 'attribute'),
        ('@FocusState', 'attribute-swiftui'),
        ('#file', 'directive'),
        ('#function', 'directive'),
    ],
    'G': [
        ('generic', 'concept'),
        ('get', 'accessor'),
        ('guard', 'keyword'),
        ('@GestureState', 'attribute-swiftui'),
    ],
    'H': [
        ('Hashable', 'protocol'),
    ],
    'I': [
        ('if', 'keyword'),
        ('import', 'keyword'),
        ('in', 'keyword'),
        ('indirect', 'modifier'),
        ('infix', 'keyword'),
        ('init', 'keyword'),
        ('inout', 'keyword'),
        ('Int', 'type'),
        ('internal', 'access-level'),
        ('is', 'keyword'),
        ('Identifiable', 'protocol'),
        ('@inlinable', 'attribute'),
    ],
    'J': [],
    'K': [
        ('KeyPath', 'type'),
    ],
    'L': [
        ('lazy', 'modifier'),
        ('let', 'keyword'),
        ('#line', 'directive'),
    ],
    'M': [
        ('map', 'function'),
        ('mutating', 'modifier'),
        ('@main', 'attribute'),
        ('@MainActor', 'attribute'),
    ],
    'N': [
        ('Never', 'type'),
        ('nil', 'literal'),
        ('nonmutating', 'modifier'),
    ],
    'O': [
        ('open', 'access-level'),
        ('operator', 'keyword'),
        ('Optional', 'type'),
        ('override', 'modifier'),
        ('@objc', 'attribute'),
        ('@Observable', 'attribute'),
        ('@ObservedObject', 'attribute-swiftui'),
    ],
    'P': [
        ('postfix', 'keyword'),
        ('precedencegroup', 'keyword'),
        ('prefix', 'keyword'),
        ('print', 'function'),
        ('private', 'access-level'),
        ('protocol', 'keyword'),
        ('@Published', 'attribute-swiftui'),
        ('public', 'access-level'),
        ('#Predicate', 'macro'),
        ('#Preview', 'macro'),
    ],
    'Q': [
        ('@Query', 'attribute-swiftdata'),
    ],
    'R': [
        ('Range', 'type'),
        ('ClosedRange', 'type'),
        ('RawRepresentable', 'protocol'),
        ('repeat', 'keyword'),
        ('required', 'modifier'),
        ('Result', 'type'),
        ('rethrows', 'keyword'),
        ('return', 'keyword'),
        ('@resultBuilder', 'attribute'),
    ],
    'S': [
        ('Self', 'keyword'),
        ('self', 'keyword'),
        ('Sendable', 'protocol'),
        ('Sequence', 'protocol'),
        ('Set', 'type'),
        ('some', 'keyword'),
        ('static', 'modifier'),
        ('String', 'type'),
        ('struct', 'keyword'),
        ('subscript', 'keyword'),
        ('super', 'keyword'),
        ('switch', 'keyword'),
        ('@State', 'attribute-swiftui'),
        ('@StateObject', 'attribute-swiftui'),
        ('@SceneStorage', 'attribute-swiftui'),
        ('@Sendable', 'attribute'),
        ('#selector', 'directive'),
    ],
    'T': [
        ('Task', 'type'),
        ('TaskGroup', 'type'),
        ('throw', 'keyword'),
        ('throws', 'keyword'),
        ('true', 'literal'),
        ('try', 'keyword'),
        ('typealias', 'keyword'),
        ('@testable', 'attribute'),
    ],
    'U': [
        ('unowned', 'modifier'),
        ('@UIApplicationMain', 'attribute'),
    ],
    'V': [
        ('var', 'keyword'),
        ('Void', 'type'),
    ],
    'W': [
        ('weak', 'modifier'),
        ('where', 'keyword'),
        ('while', 'keyword'),
        ('#warning', 'directive'),
    ],
    'X': [],
    'Y': [],
    'Z': [],
}

# ---------- Book structure + status ----------

FRONT_MATTER = [
    # (slug, status)
    ("Claude-X26-Parameters", "written"),
]

BOOKS = [
    # (n, part, slug, status)
    (1,  "Part-I-Introduction",          "Introducing-Swift-And-Xcode",   "written"),
    (2,  "Part-I-Introduction",          "Introducing-SwiftUI-Views",     "written"),
    (3,  "Part-I-Introduction",          "Introducing-Scenes-And-Windows","written"),
    (4,  "Part-III-The-User-Interface",  "Gestures-And-Input",            "scope"),
    (5,  "Part-III-The-User-Interface",  "Menus-And-Navigation",          "written"),
    (6,  "Part-III-The-User-Interface",  "Controls-Buttons-Toggles-Pickers","written"),
    (7,  "Part-III-The-User-Interface",  "Toolbars-And-Tab-Views",        "written"),
    (8,  "Part-III-The-User-Interface",  "Lists-Grids-And-ForEach",       "written"),
    (9,  "Part-III-The-User-Interface",  "Text-And-TextField",            "written"),
    (10, "Part-III-The-User-Interface",  "TextEditor-And-AttributedString","written"),
    (11, "Part-III-The-User-Interface",  "FileManager-And-Documents",     "written"),
    (12, "Part-III-The-User-Interface",  "Sheets-Alerts-And-Confirmations","written"),
    (13, "Part-IV-The-Application",      "Multi-Window-And-NavigationSplitView","scope"),
    (14, "Part-IV-The-Application",      "Clipboard-DragDrop-ShareSheet", "scope"),
    (15, "Part-IV-The-Application",      "SwiftData-And-CoreData",        "scope"),
    (16, "Part-IV-The-Application",      "Extensions-And-Packages",       "written"),
    (17, "Part-IV-The-Application",      "Swift-Charts-And-PDFKit",       "scope"),
    (18, "Part-V-Advanced-Techniques",   "Error-Handling-And-Result-Type","scope"),
    (19, "Part-V-Advanced-Techniques",   "Building-Custom-Views-And-Modifiers","scope"),
    (20, "Part-V-Advanced-Techniques",   "Performance-Instruments-And-Best-Practices","scope"),
    (21, "Part-VI-The-Modern-Toolchain", "Git-And-GitHub",                "scope"),
    (22, "Part-VI-The-Modern-Toolchain", "AI-Chatbot-Integration",        "scope"),
]

APPENDICES = [
    ("A", "GitHub-Setup",         "written"),
    ("B", "Claudes-Web-Wrapper",  "written"),
    ("C", "QuickNote",            "written"),
    ("D", "LockBox",              "scope"),
]

PART_TITLES = {
    "Part-I-Introduction":          "Part I — Introduction",
    "Part-II-The-Swift-Language":   "Part II — The Swift Language",
    "Part-III-The-User-Interface":  "Part III — The User Interface",
    "Part-IV-The-Application":      "Part IV — The Application",
    "Part-V-Advanced-Techniques":   "Part V — Advanced Techniques",
    "Part-VI-The-Modern-Toolchain": "Part VI — The Modern Toolchain",
}

CHAPTER_NOTES = {
    'J': "No entries. JSON handling is cross-referenced from Chapter C — see Codable.",
    'X': "Thin chapter — no entries yet.",
    'Y': "Thin chapter — no entries yet.",
    'Z': "Thin chapter — no entries yet.",
}


# ---------- Universal template ----------

CSS = """
:root {
  --bg: #000000;
  --fg: #FFB000;
  --bright: #FFD060;
  --dim: #996600;
  --codebg: #1a0d00;
  --border: #664500;
  --gutter: #4a3300;
  --headerbg: #0a0600;
  --scope: #A06030;
  --skeleton: #606060;
}
* { box-sizing: border-box; }
html, body { -webkit-text-size-adjust: 100%; text-size-adjust: 100%; }
body {
  background: var(--bg);
  color: var(--fg);
  font-family: "FiraCode Nerd Font Mono", "FiraCode Nerd Font", "Fira Code", "Menlo", "Courier New", monospace;
  font-size: 18pt;
  line-height: 1.55;
  margin: 0;
  padding: 0;
  text-shadow: 0 0 1px rgba(255, 176, 0, 0.35);
}
header.page, footer.page {
  background: var(--headerbg);
  color: var(--dim);
  border-bottom: 1px solid var(--border);
  padding: 0.7rem 1.1rem;
  font-size: 13pt;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}
footer.page { border-bottom: 0; border-top: 1px solid var(--border); margin-top: 2rem; }
header.page .path, footer.page .path { color: var(--fg); word-break: break-all; overflow-wrap: break-word; }
header.page .pos, footer.page .pos { color: var(--bright); }
.content { padding: 0.8rem 1rem 2rem 1rem; max-width: 1100px; margin: 0 auto; }
h1 { color: var(--bright); font-weight: normal; font-size: 26pt; margin: 0.6rem 0 1rem 0; }
h2 { color: var(--bright); font-weight: normal; font-size: 20pt; border-bottom: 1px solid var(--border); padding-bottom: 0.3rem; margin-top: 1.5rem; counter-reset: h3 para; }
h2::before { counter-increment: h2; content: counter(h2) ". "; color: var(--fg); }
h3 { color: var(--bright); font-weight: normal; font-size: 18pt; margin-top: 1rem; counter-reset: para; }
h3::before { counter-increment: h3; content: counter(h2) "." counter(h3) " "; color: var(--fg); }
p { margin: 0.4rem 0; counter-increment: para; }
p::before { content: counter(h2) "." counter(h3) "." counter(para) " "; color: var(--dim); font-size: 13pt; margin-right: 0.4em; }
code { color: var(--bright); background: var(--codebg); padding: 0.08em 0.35em; border: 1px solid #3a2400; border-radius: 3px; font-size: 0.92em; }
pre { background: var(--codebg); border: 1px solid #3a2400; border-radius: 4px; padding: 0.7rem 0.9rem; overflow-x: auto; font-size: 14pt; }
pre code { background: transparent; border: 0; padding: 0; }
ul, ol.body-list { margin: 0.4rem 0 0.4rem 1.4rem; padding: 0; }
a { color: var(--bright); text-decoration: none; border-bottom: 1px dotted var(--dim); }
a:hover { background: #332200; }
strong { color: var(--bright); }
em { color: var(--fg); font-style: italic; }
hr { border: 0; border-top: 1px solid var(--border); margin: 1rem 0; }
ol.lines { list-style: none; counter-reset: line h2; padding: 0; margin: 0; }
ol.lines > li { counter-increment: line; padding: 0.15rem 0 0.15rem 3.6rem; position: relative; min-height: 1.2em; }
ol.lines > li::before { content: counter(line); position: absolute; left: 0; top: 0.25rem; width: 2.8rem; text-align: right; color: var(--gutter); font-size: 13pt; padding-right: 0.5rem; border-right: 1px solid #2a1e00; }
ol.lines > li > p, ol.lines > li > h1, ol.lines > li > h2, ol.lines > li > h3, ol.lines > li > ul, ol.lines > li > ol, ol.lines > li > pre, ol.lines > li > hr { margin: 0; }
.scope-note { border-left: 3px solid var(--bright); padding: 0.7rem 1rem; background: #140c00; margin: 0.6rem 0; color: var(--bright); }
.slot { color: var(--dim); font-style: italic; }
.kind { color: var(--dim); font-size: 14pt; margin-top: -0.3rem; }
.nav { display: flex; gap: 0.9rem; flex-wrap: wrap; margin-top: 0.8rem; font-size: 14pt; }
.status-written  { color: var(--bright); }
.status-scope    { color: var(--scope); }
.status-skeleton { color: var(--skeleton); }
.status-tag { font-size: 13pt; margin-left: 0.4em; }
"""

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} &mdash; Claude's Xcode 26 Swift Bible</title>
<style>{css}</style>
</head>
<body>

<header class="page">
  <div class="path">{path}</div>
  <div class="pos">{pos}</div>
</header>

<div class="content">
<ol class="lines">
{body}
</ol>
</div>

<footer class="page">
  <div class="path">{path}</div>
  <div class="pos">{pos}</div>
  <div class="nav">{nav}</div>
</footer>

</body>
</html>
"""

def esc(s):
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;"))

def render_page(title, path_display, pos_label, blocks, nav_html):
    body = "\n".join(f"  <li>{b}</li>" for b in blocks)
    return PAGE.format(
        title=title,
        css=CSS,
        path=path_display,
        pos=pos_label,
        body=body,
        nav=nav_html,
    )


# ---------- Filename sanitization ----------

def safe_filename(entry):
    """Strip leading @ or # for filesystem-safe filenames."""
    return re.sub(r"^[@#]", "", entry)


# ---------- Lexicon Page generation ----------

def status_tag(status):
    label = {"written": "Written", "scope": "Scope", "skeleton": "Skeleton"}[status]
    return f'<span class="status-tag status-{status}">[{label}]</span>'


def render_lexicon_page(chapter, entry, kind):
    safe = safe_filename(entry)
    folder_rel = f"Part-II-The-Swift-Language/Chapter-{chapter}/Pages"
    filename = f"Page-{safe}.html"
    path_display = f"{folder_rel}/Page-{safe}"
    title = f"{entry} — Swift Lexicon"
    pos = (f'Part II &middot; Chapter {chapter} &middot; '
           f'Page {esc(entry)} {status_tag("skeleton")}')

    blocks = [
        f'<h1>{esc(entry)}</h1>',
        f'<div class="kind">Kind: {esc(kind)}</div>',
        '<div class="scope-note">This Page is a <strong>skeleton</strong>. '
        'Real definition, example, and Rosetta Stone content fills in over '
        'time. Leave <code>MICHAEL:</code> notes anywhere and they fold into '
        'the next draft.</div>',
        '<h2>Definition</h2>',
        f'<p class="slot">Plain-English definition of <code>{esc(entry)}</code> pending.</p>',
        '<h2>Swift Example</h2>',
        f'<pre class="slot"><code>// Minimal Swift example using {esc(entry)} pending</code></pre>',
        '<h2>Rosetta Stone</h2>',
        '<h3>Pascal / Delphi</h3>',
        '<p class="slot">Equivalent or closest cousin pending.</p>',
        '<h3>BASIC</h3>',
        '<p class="slot">Equivalent or closest cousin pending.</p>',
        '<h3>C / C++</h3>',
        '<p class="slot">Equivalent or closest cousin pending.</p>',
        '<h2>Related</h2>',
        '<p class="slot">Cross-references to other Lexicon entries and Books pending.</p>',
        '<h2>Sources</h2>',
        '<ul class="slot">',
        '  <li>Apple Developer documentation — URL pending</li>',
        '  <li>Swift.org / Swift Evolution / WWDC — URL pending</li>',
        '</ul>',
    ]

    nav = (
        f'<a href="../Chapter-{chapter}">&larr; Chapter {chapter}</a>'
        f'<a href="../../../table-of-contents">Contents</a>'
        f'<a href="../../../claudex26-index">Index</a>'
    )

    out_dir = BUNDLE / folder_rel
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / filename).write_text(render_page(title, path_display, pos, blocks, nav))


# ---------- Chapter index page ----------

def render_chapter_index(chapter, entries):
    folder_rel = f"Part-II-The-Swift-Language/Chapter-{chapter}"
    filename = f"Chapter-{chapter}.html"
    path_display = f"{folder_rel}/Chapter-{chapter}"
    title = f"Chapter {chapter} — Swift Lexicon"
    pos = f"Part II &middot; Chapter {chapter}"

    blocks = [
        f'<h1>Chapter {chapter}</h1>',
    ]

    if chapter in CHAPTER_NOTES:
        blocks.append(f'<p>{esc(CHAPTER_NOTES[chapter])}</p>')

    if entries:
        blocks.append(f'<h2>Entries</h2>')
        blocks.append(f'<p>{len(entries)} entries beginning with <strong>{chapter}</strong>:</p>')
        items = []
        for entry, kind in entries:
            safe = safe_filename(entry)
            items.append(
                f'<li><a href="Pages/Page-{safe}">{esc(entry)}</a> '
                f'<em>({esc(kind)})</em> {status_tag("skeleton")}</li>'
            )
        blocks.append('<ul>' + "".join(items) + '</ul>')

    nav = (
        f'<a href="../../table-of-contents">Contents</a>'
        f'<a href="../../claudex26-index">Index</a>'
    )

    out_dir = BUNDLE / folder_rel
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / filename).write_text(render_page(title, path_display, pos, blocks, nav))


# ---------- Table of Contents ----------

def render_toc():
    path_display = "table-of-contents"
    title = "Table of Contents — Claude's Xcode 26 Swift Bible"
    pos = "Front Matter &middot; Table of Contents"

    blocks = [
        '<h1>Table of Contents</h1>',
        '<p>Every Part, Book, Chapter, Page, and Appendix in Claude&rsquo;s X26 Swift6 Bible. '
        'Each entry is clickable. Status tags indicate whether an entry is '
        '<span class="status-written">written</span> (real prose ready to read), '
        '<span class="status-scope">scope</span> (outline of what will be '
        'written, editable with <code>MICHAEL:</code> notes), or '
        '<span class="status-skeleton">skeleton</span> (slotted template, '
        'content fills in over time).</p>',
    ]

    # Front Matter
    blocks.append('<h2>Front Matter</h2>')
    fm_items = []
    for slug, status in FRONT_MATTER:
        display = slug.replace('-', ' ')
        href = f"Front-Matter/{slug}/{slug}"
        fm_items.append(
            f'<li><a href="{href}">{esc(display)}</a> {status_tag(status)}</li>'
        )
    blocks.append('<ul>' + "".join(fm_items) + '</ul>')

    # Part I - Introduction
    blocks.append('<h2>Part I — Introduction</h2>')
    toc_books = []
    for n, part, slug, status in BOOKS:
        if part != "Part-I-Introduction":
            continue
        display = f"Book {n:02d} — {slug.replace('-', ' ')}"
        href = f"Part-I-Introduction/Book-{n:02d}-{slug}/Book-{n:02d}-{slug}"
        toc_books.append(
            f'<li><a href="{href}">{esc(display)}</a> {status_tag(status)}</li>'
        )
    blocks.append('<ul>' + "".join(toc_books) + '</ul>')

    # Part II - Swift Language (Lexicon)
    blocks.append('<h2>Part II — The Swift Language (Lexicon)</h2>')
    blocks.append('<p>26 Chapters, A–Z; one Page per Swift word. Every Page is clickable.</p>')
    for ch in sorted(ENTRIES.keys()):
        ch_href = f"Part-II-The-Swift-Language/Chapter-{ch}/Chapter-{ch}"
        entries = ENTRIES[ch]
        if not entries:
            note = CHAPTER_NOTES.get(ch, "empty")
            blocks.append(
                f'<h3><a href="{ch_href}">Chapter {ch}</a></h3>'
                f'<p class="slot">{esc(note)}</p>'
            )
            continue
        blocks.append(f'<h3><a href="{ch_href}">Chapter {ch}</a> — {len(entries)} entries</h3>')
        items = []
        for entry, kind in entries:
            safe = safe_filename(entry)
            page_href = f"Part-II-The-Swift-Language/Chapter-{ch}/Pages/Page-{safe}"
            items.append(
                f'<li><a href="{page_href}">{esc(entry)}</a> '
                f'<em>({esc(kind)})</em> {status_tag("skeleton")}</li>'
            )
        blocks.append('<ul>' + "".join(items) + '</ul>')

    # Parts III-VI
    for pk in ("Part-III-The-User-Interface", "Part-IV-The-Application",
               "Part-V-Advanced-Techniques", "Part-VI-The-Modern-Toolchain"):
        blocks.append(f'<h2>{PART_TITLES[pk]}</h2>')
        items = []
        for n, part, slug, status in BOOKS:
            if part != pk:
                continue
            display = f"Book {n:02d} — {slug.replace('-', ' ')}"
            href = f"{pk}/Book-{n:02d}-{slug}/Book-{n:02d}-{slug}"
            items.append(
                f'<li><a href="{href}">{esc(display)}</a> {status_tag(status)}</li>'
            )
        blocks.append('<ul>' + "".join(items) + '</ul>')

    # Appendices
    blocks.append('<h2>Appendices</h2>')
    items = []
    for letter, slug, status in APPENDICES:
        display = f"Appendix {letter} — {slug.replace('-', ' ')}"
        href = f"Appendices/Appendix-{letter}-{slug}/Appendix-{letter}-{slug}"
        items.append(
            f'<li><a href="{href}">{esc(display)}</a> {status_tag(status)}</li>'
        )
    blocks.append('<ul>' + "".join(items) + '</ul>')

    # Back Matter
    blocks.append('<h2>Back Matter</h2>')
    blocks.append(
        '<ul>'
        '<li><a href="claudex26-index">Index</a> — alphabetical list of every Page, Book, and Appendix</li>'
        '</ul>'
    )

    nav = '<a href="claudex26-index">Index</a>'
    (BUNDLE / "table-of-contents.html").write_text(
        render_page(title, path_display, pos, blocks, nav)
    )


# ---------- Index (alphabetical) ----------

def render_index():
    path_display = "claudex26-index"
    title = "Index — Claude's Xcode 26 Swift Bible"
    pos = "Back Matter &middot; Index"

    blocks = [
        '<h1>Index</h1>',
        '<p>Alphabetical index of every addressable entry in Claude&rsquo;s X26 Swift6 Bible: '
        'Lexicon Pages (Part II), Books (Parts I, III–VI), and Appendices. '
        'Every entry is clickable.</p>',
    ]

    # Assemble one flat list of (display, href) sorted case-insensitively.
    all_entries = []

    # Lexicon Pages
    for ch in sorted(ENTRIES.keys()):
        for entry, kind in ENTRIES[ch]:
            safe = safe_filename(entry)
            href = f"Part-II-The-Swift-Language/Chapter-{ch}/Pages/Page-{safe}"
            all_entries.append((entry, href, f"Lexicon &middot; Chapter {ch} &middot; {esc(kind)}", "skeleton"))

    # Books
    for n, part, slug, status in BOOKS:
        display = f"Book {n:02d} — {slug.replace('-', ' ')}"
        href = f"{part}/Book-{n:02d}-{slug}/Book-{n:02d}-{slug}"
        all_entries.append((display, href, PART_TITLES[part], status))

    # Front Matter
    for slug, status in FRONT_MATTER:
        display = slug.replace('-', ' ')
        href = f"Front-Matter/{slug}/{slug}"
        all_entries.append((display, href, "Front Matter", status))

    # Appendices
    for letter, slug, status in APPENDICES:
        display = f"Appendix {letter} — {slug.replace('-', ' ')}"
        href = f"Appendices/Appendix-{letter}-{slug}/Appendix-{letter}-{slug}"
        all_entries.append((display, href, "Appendices", status))

    # Chapters themselves (A–Z landing pages)
    for ch in sorted(ENTRIES.keys()):
        href = f"Part-II-The-Swift-Language/Chapter-{ch}/Chapter-{ch}"
        all_entries.append((f"Chapter {ch}", href,
                            f"Lexicon landing page &middot; {len(ENTRIES[ch])} entries",
                            "written" if ENTRIES[ch] else "scope"))

    # Sort by display, case-insensitive, stripping @ and # for alphabetization
    def sort_key(item):
        d = item[0]
        stripped = re.sub(r"^[@#]", "", d).lower()
        return stripped

    all_entries.sort(key=sort_key)

    # Bucket by first letter
    by_letter = {}
    for display, href, note, status in all_entries:
        stripped = re.sub(r"^[@#]", "", display)
        letter = stripped[0].upper() if stripped else "#"
        if not letter.isalpha():
            letter = "#"
        by_letter.setdefault(letter, []).append((display, href, note, status))

    for letter in sorted(by_letter.keys()):
        blocks.append(f'<h2>{letter}</h2>')
        items = []
        for display, href, note, status in by_letter[letter]:
            items.append(
                f'<li><a href="{href}">{esc(display)}</a> '
                f'<em>({note})</em> {status_tag(status)}</li>'
            )
        blocks.append('<ul>' + "".join(items) + '</ul>')

    nav = '<a href="table-of-contents">Contents</a>'
    (BUNDLE / "claudex26-index.html").write_text(
        render_page(title, path_display, pos, blocks, nav)
    )


def main():
    print("Generating Lexicon Pages...")
    total_pages = 0
    for ch, entries in ENTRIES.items():
        for entry, kind in entries:
            render_lexicon_page(ch, entry, kind)
            total_pages += 1
    print(f"  wrote {total_pages} Lexicon Pages")

    print("\nGenerating Chapter index pages...")
    for ch, entries in ENTRIES.items():
        render_chapter_index(ch, entries)
    print(f"  wrote {len(ENTRIES)} Chapter pages")

    print("\nRegenerating table-of-contents.html...")
    render_toc()

    print("Regenerating claudex26-index.html...")
    render_index()

    print("\nPhase 1b complete.")


if __name__ == "__main__":
    main()
