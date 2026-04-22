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

import html
import re
import sys
from pathlib import Path

# Make the sibling data file importable regardless of where we're invoked from.
sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from _lexicon_definitions import DEFS  # type: ignore
except ModuleNotFoundError:
    # Fall back to the hyphenated filename (Python allows import via path helper).
    import importlib.util
    _spec = importlib.util.spec_from_file_location(
        "_lexicon_definitions",
        Path(__file__).resolve().parent / "_lexicon-definitions.py"
    )
    _mod = importlib.util.module_from_spec(_spec)  # type: ignore
    _spec.loader.exec_module(_mod)                 # type: ignore
    DEFS = _mod.DEFS

# Per-entry Rosetta Stone, topic clusters, book cross-refs, and source URLs.
try:
    from _lexicon_extras import ROSETTA, CLUSTERS, BOOK_REFS, SOURCE_MAP  # type: ignore
except ModuleNotFoundError:
    import importlib.util
    _spec2 = importlib.util.spec_from_file_location(
        "_lexicon_extras",
        Path(__file__).resolve().parent / "_lexicon-extras.py"
    )
    _mod2 = importlib.util.module_from_spec(_spec2)  # type: ignore
    _spec2.loader.exec_module(_mod2)                 # type: ignore
    ROSETTA    = _mod2.ROSETTA
    CLUSTERS   = _mod2.CLUSTERS
    BOOK_REFS  = _mod2.BOOK_REFS
    SOURCE_MAP = _mod2.SOURCE_MAP

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
    'J': [
        ('JSONEncoder', 'type'),
        ('JSONDecoder', 'type'),
        ('JSONSerialization', 'type'),
    ],
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
    'X': [
        ('XMLParser', 'type'),
    ],
    'Y': [],
    'Z': [
        ('ZStack', 'view-swiftui'),
    ],
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
    (4,  "Part-III-The-User-Interface",  "Gestures-And-Input",            "written"),
    (5,  "Part-III-The-User-Interface",  "Menus-And-Navigation",          "written"),
    (6,  "Part-III-The-User-Interface",  "Controls-Buttons-Toggles-Pickers","written"),
    (7,  "Part-III-The-User-Interface",  "Toolbars-And-Tab-Views",        "written"),
    (8,  "Part-III-The-User-Interface",  "Lists-Grids-And-ForEach",       "written"),
    (9,  "Part-III-The-User-Interface",  "Text-And-TextField",            "written"),
    (10, "Part-III-The-User-Interface",  "TextEditor-And-AttributedString","written"),
    (11, "Part-III-The-User-Interface",  "FileManager-And-Documents",     "written"),
    (12, "Part-III-The-User-Interface",  "Sheets-Alerts-And-Confirmations","written"),
    (13, "Part-IV-The-Application",      "Multi-Window-And-NavigationSplitView","written"),
    (14, "Part-IV-The-Application",      "Clipboard-DragDrop-ShareSheet", "written"),
    (15, "Part-IV-The-Application",      "SwiftData-And-CoreData",        "written"),
    (16, "Part-IV-The-Application",      "Extensions-And-Packages",       "written"),
    (17, "Part-IV-The-Application",      "Swift-Charts-And-PDFKit",       "written"),
    (18, "Part-V-Advanced-Techniques",   "Error-Handling-And-Result-Type","written"),
    (19, "Part-V-Advanced-Techniques",   "Building-Custom-Views-And-Modifiers","written"),
    (20, "Part-V-Advanced-Techniques",   "Performance-Instruments-And-Best-Practices","written"),
    (21, "Part-VI-The-Modern-Toolchain", "Git-And-GitHub",                "written"),
    (22, "Part-VI-The-Modern-Toolchain", "AI-Chatbot-Integration",        "written"),
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
    'Y': "No standard Swift entries at publication of this book.",
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
html, body { -webkit-text-size-adjust: 100%; text-size-adjust: 100%; height: 100%; }
body {
  background: var(--bg);
  color: var(--fg);
  font-family: "FiraCode Nerd Font Mono", "FiraCode Nerd Font", "Fira Code", "Menlo", "Courier New", monospace;
  font-size: 18pt;
  line-height: 1.55;
  margin: 0;
  padding: 0;
  text-shadow: 0 0 1px rgba(255, 176, 0, 0.35);
  display: flex;
  flex-direction: column;
}
header.page, footer.page {
  background: var(--headerbg);
  color: var(--dim);
  padding: 0.55rem 1.1rem;
  font-size: 13pt;
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  flex: 0 0 auto;
  z-index: 10;
}
header.page { border-bottom: 1px solid var(--border); }
footer.page { border-top: 1px solid var(--border); padding-bottom: calc(0.55rem + env(safe-area-inset-bottom)); }
header.page .path, footer.page .path { color: var(--fg); word-break: break-all; overflow-wrap: break-word; }
header.page .pos, footer.page .pos { color: var(--bright); }
/* The middle scrolls; header and footer stay put. */
.content { flex: 1 1 auto; overflow-y: auto; -webkit-overflow-scrolling: touch; padding: 0.8rem 1rem 2rem 1rem; max-width: 1100px; margin: 0 auto; width: 100%; }
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
a { color: var(--bright); font-weight: bold; text-decoration: none; border-bottom: 1px dotted var(--dim); }
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
</header>

<div class="content">
<ol class="lines">
{body}
</ol>
</div>

<footer class="page">
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
    # Reader-visible path uses spaces where the filesystem uses dashes.
    visible_path = path_display.replace("-", " ")
    return PAGE.format(
        title=title,
        css=CSS,
        path=visible_path,
        pos=pos_label,
        body=body,
        nav=nav_html,
    )


# ---------- Filename sanitization ----------

def safe_filename(entry):
    """Strip leading @ or # for filesystem-safe filenames."""
    return re.sub(r"^[@#]", "", entry)


# ---------- Related / Sources helpers ----------

def related_for(entry: str):
    """
    Walk CLUSTERS to find every other entry that shares a cluster with `entry`.
    Return (lexicon_entries, book_refs) as two lists of (link_text, href) tuples.
    """
    # Reverse lookup: entry -> set of cluster names it appears in.
    entry_clusters = [name for name, members in CLUSTERS.items() if entry in members]

    # Lexicon cousins: union of other cluster members.
    cousins: dict[str, str] = {}   # name -> chapter letter, for link building
    for cname in entry_clusters:
        for member in CLUSTERS[cname]:
            if member == entry:
                continue
            # Find the chapter letter from ENTRIES.
            for ch, entries in ENTRIES.items():
                if any(e == member for e, _ in entries):
                    cousins[member] = ch
                    break
    lexicon_links = []
    for name in sorted(cousins.keys(), key=lambda n: re.sub(r"^[@#]", "", n).lower()):
        ch = cousins[name]
        safe = safe_filename(name)
        href = f"../../Part-II-The-Swift-Language/Chapter-{ch}/Page-{safe}.html"
        lexicon_links.append((name, href))

    # Book refs: union of BOOK_REFS for each cluster.
    seen_books: set[int] = set()
    book_links = []
    for cname in entry_clusters:
        for (n, part, slug) in BOOK_REFS.get(cname, []):
            if n in seen_books:
                continue
            seen_books.add(n)
            display = f"Book {n:02d} — {slug.replace('-', ' ')}"
            href = f"../../{part}/Book-{n:02d}-{slug}.html"
            book_links.append((display, href))
    book_links.sort(key=lambda x: x[0])

    return lexicon_links, book_links


# ---------- Lexicon Page generation ----------

def status_tag(status):
    label = {"written": "Written", "scope": "Scope", "skeleton": "Skeleton"}[status]
    return f'<span class="status-tag status-{status}">[{label}]</span>'


def render_lexicon_page(chapter, entry, kind):
    safe = safe_filename(entry)
    folder_rel = f"Part-II-The-Swift-Language/Chapter-{chapter}"
    filename = f"Page-{safe}.html"
    path_display = f"{folder_rel}/Page-{safe}"
    title = f"{entry} — Swift Lexicon"

    has_content = entry in DEFS
    entry_status = "written" if has_content else "skeleton"

    pos = (f'Part II &middot; Chapter {chapter} &middot; '
           f'Page {esc(entry)} {status_tag(entry_status)}')

    blocks = [
        f'<h1>{esc(entry)}</h1>',
        f'<div class="kind">Kind: {esc(kind)}</div>',
    ]

    if has_content:
        d = DEFS[entry]
        definition_html = esc(d["def"])
        example_html = html.escape(d["ex"])
        blocks += [
            '<h2>Definition</h2>',
            f'<p>{definition_html}</p>',
            '<h2>Swift Example</h2>',
            f'<pre><code>{example_html}</code></pre>',
        ]

        # Rosetta Stone
        rosetta = ROSETTA.get(entry)
        if rosetta:
            blocks += [
                '<h2>Rosetta Stone</h2>',
                '<h3>Pascal / Delphi</h3>',
                f'<p>{esc(rosetta["pascal"])}</p>',
                '<h3>BASIC</h3>',
                f'<p>{esc(rosetta["basic"])}</p>',
                '<h3>C / C++</h3>',
                f'<p>{esc(rosetta["c"])}</p>',
            ]
        else:
            blocks += [
                '<h2>Rosetta Stone</h2>',
                '<h3>Pascal / Delphi</h3>',
                '<p class="slot">Not written.</p>',
                '<h3>BASIC</h3>',
                '<p class="slot">Not written.</p>',
                '<h3>C / C++</h3>',
                '<p class="slot">Not written.</p>',
            ]

        # Related
        cousins, book_links = related_for(entry)
        if cousins or book_links:
            blocks.append('<h2>Related</h2>')
            if cousins:
                items = [f'<li><a href="{h}"><code>{esc(n)}</code></a></li>' for n, h in cousins]
                blocks.append('<p>Other Lexicon entries in the same topic cluster:</p>')
                blocks.append('<ul>' + "".join(items) + '</ul>')
            if book_links:
                items = [f'<li><a href="{h}">{esc(n)}</a></li>' for n, h in book_links]
                blocks.append('<p>Book chapters that cover this topic:</p>')
                blocks.append('<ul>' + "".join(items) + '</ul>')
        else:
            blocks += [
                '<h2>Related</h2>',
                '<p class="slot">Not written.</p>',
            ]

        # Sources
        sources = SOURCE_MAP.get(entry)
        if sources:
            items = [f'<li><a href="{url}">{esc(label)}</a></li>' for url, label in sources]
            blocks += [
                '<h2>Sources</h2>',
                '<ul>' + "".join(items) + '</ul>',
            ]
        else:
            blocks += [
                '<h2>Sources</h2>',
                '<ul class="slot"><li>Not written.</li></ul>',
            ]
    else:
        blocks += [
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
        f'<a href="../../Front-of-Book/table-of-contents.html">Contents</a>'
        f'<a href="../../claudex26-index.html">Index</a>'
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
            st = "written" if entry in DEFS else "skeleton"
            items.append(
                f'<li><a href="Pages/Page-{safe}.html">{esc(entry)}</a> '
                f'<em>({esc(kind)})</em> {status_tag(st)}</li>'
            )
        blocks.append('<ul>' + "".join(items) + '</ul>')

    nav = (
        f'<a href="../../Front-of-Book/table-of-contents.html">Contents</a>'
        f'<a href="../../claudex26-index.html">Index</a>'
    )

    out_dir = BUNDLE / folder_rel
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / filename).write_text(render_page(title, path_display, pos, blocks, nav))


# ---------- Table of Contents ----------

def render_toc():
    path_display = "Front-of-Book/table-of-contents"
    title = "Table of Contents — Claude's Xcode 26 Swift Bible"
    pos = "Front of Book &middot; Table of Contents"

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

    # Front of Book — TOC lives here, so siblings need no ../
    blocks.append('<h2>Front of Book</h2>')
    fm_items = []
    for slug, status in FRONT_MATTER:
        display = slug.replace('-', ' ')
        href = f"{slug}.html"
        fm_items.append(
            f'<li><a href="{href}">{esc(display)}</a> {status_tag(status)}</li>'
        )
    blocks.append('<ul>' + "".join(fm_items) + '</ul>')

    # Part I - Introduction (one level up from Front-of-Book)
    blocks.append('<h2>Part I — Introduction</h2>')
    toc_books = []
    for n, part, slug, status in BOOKS:
        if part != "Part-I-Introduction":
            continue
        display = f"Book {n:02d} — {slug.replace('-', ' ')}"
        href = f"../Part-I-Introduction/Book-{n:02d}-{slug}.html"
        toc_books.append(
            f'<li><a href="{href}">{esc(display)}</a> {status_tag(status)}</li>'
        )
    blocks.append('<ul>' + "".join(toc_books) + '</ul>')

    # Part II - Swift Language (Lexicon)
    blocks.append('<h2>Part II — The Swift Language (Lexicon)</h2>')
    blocks.append('<p>26 Chapters, A–Z; one Page per Swift word. Every Page is clickable.</p>')
    for ch in sorted(ENTRIES.keys()):
        entries = ENTRIES[ch]
        if not entries:
            note = CHAPTER_NOTES.get(ch, "empty")
            blocks.append(
                f'<h3>Chapter {ch}</h3>'
                f'<p class="slot">{esc(note)}</p>'
            )
            continue
        noun = "entry" if len(entries) == 1 else "entries"
        blocks.append(f'<h3>Chapter {ch} — {len(entries)} {noun}</h3>')
        items = []
        for entry, kind in entries:
            safe = safe_filename(entry)
            page_href = f"../Part-II-The-Swift-Language/Chapter-{ch}/Page-{safe}.html"
            st = "written" if entry in DEFS else "skeleton"
            items.append(
                f'<li><a href="{page_href}">{esc(entry)}</a> '
                f'<em>({esc(kind)})</em> {status_tag(st)}</li>'
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
            href = f"../{pk}/Book-{n:02d}-{slug}.html"
            items.append(
                f'<li><a href="{href}">{esc(display)}</a> {status_tag(status)}</li>'
            )
        blocks.append('<ul>' + "".join(items) + '</ul>')

    # Appendices
    blocks.append('<h2>Appendices</h2>')
    items = []
    for letter, slug, status in APPENDICES:
        display = f"Appendix {letter} — {slug.replace('-', ' ')}"
        href = f"../Appendices/Appendix-{letter}-{slug}.html"
        items.append(
            f'<li><a href="{href}">{esc(display)}</a> {status_tag(status)}</li>'
        )
    blocks.append('<ul>' + "".join(items) + '</ul>')

    # Back Matter
    blocks.append('<h2>Back Matter</h2>')
    blocks.append(
        '<ul>'
        '<li><a href="../claudex26-index.html">Index</a> — alphabetical index of every Page, Book, Appendix, plus every Swift identifier that appears in the prose</li>'
        '<li><a href="../bibliography.html">Bibliography</a> — primary sources the book draws from</li>'
        '</ul>'
    )

    nav = '<a href="../claudex26-index.html">Index</a>'
    out_path = BUNDLE / "Front-of-Book" / "table-of-contents.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_page(title, path_display, pos, blocks, nav))


# ---------- Cross-reference scanner ----------

# Match inline <code>…</code> not wrapped by a <pre> ancestor. We sub out
# <pre>…</pre> blocks first, then grab every remaining <code> content.
_PRE_BLOCK   = re.compile(r"<pre\b[^>]*>.*?</pre>", re.DOTALL | re.IGNORECASE)
_INLINE_CODE = re.compile(r"<code\b[^>]*>([^<]+)</code>", re.IGNORECASE)
# A token that looks like a Swift identifier (optionally @ / # / $ prefixed).
_IDENT = re.compile(r"^[@#$]?[A-Za-z_][A-Za-z0-9_]*$")

def _display_for_file(rel_path: str) -> str:
    """Reader-friendly label for an in-vault path."""
    name = rel_path.replace("\\", "/")
    name = name[:-5] if name.endswith(".html") else name
    last = name.rsplit("/", 1)[-1]
    return last.replace("-", " ")

def scan_code_tokens():
    """
    Walk every .html under the vault, collect inline <code> tokens that look
    like Swift identifiers, map each token to the pages that mention it.
    Skip the Index and Bibliography themselves to avoid circular references.
    """
    refs: dict[str, set[tuple[str, str]]] = {}
    skip = {"claudex26-index.html", "bibliography.html"}
    for path in sorted(BUNDLE.rglob("*.html")):
        if path.name in skip: continue
        rel = str(path.relative_to(BUNDLE))
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        stripped = _PRE_BLOCK.sub("", text)
        for m in _INLINE_CODE.finditer(stripped):
            token = m.group(1).strip()
            if len(token) > 40: continue
            if not _IDENT.match(token): continue
            # Drop common noise: single-letter loop vars, keywords too trivial
            # to index (let them land on their Lexicon Page instead).
            if len(token) <= 1: continue
            refs.setdefault(token, set()).add((rel, _display_for_file(rel)))
    # Return as sorted lists per token for deterministic rendering.
    return {
        t: sorted(pages, key=lambda p: p[1].lower())
        for t, pages in refs.items()
    }


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
            href = f"Part-II-The-Swift-Language/Chapter-{ch}/Page-{safe}.html"
            st = "written" if entry in DEFS else "skeleton"
            all_entries.append((entry, href, f"Lexicon &middot; Chapter {ch} &middot; {esc(kind)}", st))

    # Books
    for n, part, slug, status in BOOKS:
        display = f"Book {n:02d} — {slug.replace('-', ' ')}"
        href = f"{part}/Book-{n:02d}-{slug}.html"
        all_entries.append((display, href, PART_TITLES[part], status))

    # Front of Book
    for slug, status in FRONT_MATTER:
        display = slug.replace('-', ' ')
        href = f"Front-of-Book/{slug}.html"
        all_entries.append((display, href, "Front of Book", status))

    # Appendices
    for letter, slug, status in APPENDICES:
        display = f"Appendix {letter} — {slug.replace('-', ' ')}"
        href = f"Appendices/Appendix-{letter}-{slug}.html"
        all_entries.append((display, href, "Appendices", status))

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

    # ---------- Cross-reference of Swift identifiers ----------
    refs = scan_code_tokens()
    blocks.append('<h2>Swift Identifiers (Cross-Reference)</h2>')
    blocks.append(
        '<p>Every Swift identifier (keyword, type, attribute, API name) that '
        'appears in the prose of this book, and every page it appears on. '
        'Tokens that also have a Lexicon Page link to that page first.</p>'
    )
    # Group by first letter, preserving case for the token itself.
    by_letter_xref: dict[str, list[tuple[str, list[tuple[str, str]]]]] = {}
    for token in sorted(refs.keys(), key=lambda t: re.sub(r"^[@#$]", "", t).lower()):
        stripped = re.sub(r"^[@#$]", "", token)
        letter = stripped[0].upper() if stripped else "#"
        if not letter.isalpha(): letter = "#"
        by_letter_xref.setdefault(letter, []).append((token, refs[token]))

    for letter in sorted(by_letter_xref.keys()):
        blocks.append(f'<h3>{letter}</h3>')
        lines = []
        for token, pages in by_letter_xref[letter]:
            links = ", ".join(
                f'<a href="{href}">{esc(label)}</a>'
                for href, label in pages
            )
            lines.append(f'<li><code>{esc(token)}</code> — {links}</li>')
        blocks.append('<ul>' + "".join(lines) + '</ul>')

    nav = '<a href="Front-of-Book/table-of-contents.html">Contents</a> <a href="bibliography.html">Bibliography</a>'
    (BUNDLE / "claudex26-index.html").write_text(
        render_page(title, path_display, pos, blocks, nav)
    )


# ---------- Bibliography ----------

def render_bibliography():
    path_display = "bibliography"
    title = "Bibliography — Claude's Xcode 26 Swift Bible"
    pos = "Back Matter &middot; Bibliography"

    blocks = [
        '<h1>Bibliography</h1>',
        '<p>Primary sources the book draws from. Individual claims are not '
        'yet footnoted line-by-line; a full citation audit is a later pass. '
        'Everything below is where to go for the authoritative word on the '
        'topics covered in each chapter.</p>',
        '<p><em>Last reviewed 2026-04-22.</em></p>',

        '<h2>Swift Language</h2>',
        '<ul>'
        '<li>Apple Inc. <strong>The Swift Programming Language</strong>. '
        '<a href="https://docs.swift.org/swift-book/">docs.swift.org/swift-book</a>. '
        'The canonical language reference; every keyword, type, and rule lives here.</li>'
        '<li>Apple Inc. <strong>Swift.org</strong>. <a href="https://www.swift.org/">swift.org</a>. '
        'Release notes, compiler announcements, and the Swift blog.</li>'
        '<li>Swift Evolution. <a href="https://github.com/apple/swift-evolution">github.com/apple/swift-evolution</a>. '
        'Every accepted language proposal, with motivation and alternatives considered.</li>'
        '<li>Swift Forums. <a href="https://forums.swift.org/">forums.swift.org</a>. '
        'Where Swift evolution is debated in public.</li>'
        '</ul>',

        '<h2>Apple Platform APIs</h2>',
        '<ul>'
        '<li>Apple Inc. <strong>Apple Developer Documentation</strong>. '
        '<a href="https://developer.apple.com/documentation/">developer.apple.com/documentation</a>. '
        'The authoritative source for every framework API surfaced in the book.</li>'
        '<li>Apple Inc. <strong>SwiftUI</strong>. '
        '<a href="https://developer.apple.com/documentation/swiftui">developer.apple.com/documentation/swiftui</a>.</li>'
        '<li>Apple Inc. <strong>SwiftData</strong>. '
        '<a href="https://developer.apple.com/documentation/swiftdata">developer.apple.com/documentation/swiftdata</a>.</li>'
        '<li>Apple Inc. <strong>Swift Charts</strong>. '
        '<a href="https://developer.apple.com/documentation/charts">developer.apple.com/documentation/charts</a>.</li>'
        '<li>Apple Inc. <strong>PDFKit</strong>. '
        '<a href="https://developer.apple.com/documentation/pdfkit">developer.apple.com/documentation/pdfkit</a>.</li>'
        '<li>Apple Inc. <strong>PencilKit</strong>. '
        '<a href="https://developer.apple.com/documentation/pencilkit">developer.apple.com/documentation/pencilkit</a>.</li>'
        '<li>Apple Inc. <strong>UIKit</strong>. '
        '<a href="https://developer.apple.com/documentation/uikit">developer.apple.com/documentation/uikit</a>.</li>'
        '<li>Apple Inc. <strong>AppKit</strong>. '
        '<a href="https://developer.apple.com/documentation/appkit">developer.apple.com/documentation/appkit</a>.</li>'
        '<li>Apple Inc. <strong>Foundation</strong>. '
        '<a href="https://developer.apple.com/documentation/foundation">developer.apple.com/documentation/foundation</a>.</li>'
        '<li>Apple Inc. <strong>Core Transferable</strong>. '
        '<a href="https://developer.apple.com/documentation/coretransferable">developer.apple.com/documentation/coretransferable</a>.</li>'
        '</ul>',

        '<h2>Design and Platform Guidelines</h2>',
        '<ul>'
        '<li>Apple Inc. <strong>Human Interface Guidelines</strong>. '
        '<a href="https://developer.apple.com/design/human-interface-guidelines/">developer.apple.com/design/human-interface-guidelines</a>. '
        'Hit-target sizes, accessibility, platform-correct UI.</li>'
        '<li>Apple Inc. <strong>App Store Review Guidelines</strong>. '
        '<a href="https://developer.apple.com/app-store/review/guidelines/">developer.apple.com/app-store/review/guidelines</a>.</li>'
        '</ul>',

        '<h2>WWDC Sessions</h2>',
        '<ul>'
        '<li>Apple Inc. <strong>WWDC Session Videos</strong>. '
        '<a href="https://developer.apple.com/videos/">developer.apple.com/videos</a>. '
        'Primary source for each year\'s API additions. SwiftUI, SwiftData, Swift '
        'concurrency, and Swift Charts are particularly well served by the '
        'year-of-introduction sessions.</li>'
        '</ul>',

        '<h2>Xcode and the Build System</h2>',
        '<ul>'
        '<li>Apple Inc. <strong>Xcode Release Notes</strong>. '
        '<a href="https://developer.apple.com/documentation/xcode-release-notes">developer.apple.com/documentation/xcode-release-notes</a>.</li>'
        '<li>Apple Inc. <strong>Xcode Help</strong>. '
        'Bundled in-app via Xcode > Help > Xcode Help. Covers Signing & Capabilities, schemes, and build settings.</li>'
        '</ul>',

        '<h2>Instruments and Performance</h2>',
        '<ul>'
        '<li>Apple Inc. <strong>Instruments User Guide</strong>. '
        '<a href="https://help.apple.com/instruments/">help.apple.com/instruments</a>. '
        'Covers the Time Profiler, Allocations, and SwiftUI instruments cited in Book 20.</li>'
        '</ul>',

        '<h2>Anthropic Claude API</h2>',
        '<ul>'
        '<li>Anthropic PBC. <strong>Anthropic API Reference</strong>. '
        '<a href="https://docs.anthropic.com/">docs.anthropic.com</a>. '
        'Messages API, streaming, rate limits, and model catalog used in Book 22.</li>'
        '<li>Anthropic PBC. <strong>Anthropic Console</strong>. '
        '<a href="https://console.anthropic.com/">console.anthropic.com</a>. '
        'API key management and usage dashboards.</li>'
        '</ul>',

        '<h2>Git and GitHub</h2>',
        '<ul>'
        '<li>Chacon, Scott, and Straub, Ben. <strong>Pro Git</strong>, 2nd ed. Apress, 2014. '
        '<a href="https://git-scm.com/book">git-scm.com/book</a>. The standard free reference.</li>'
        '<li>Git Project. <strong>git-scm.com</strong>. '
        '<a href="https://git-scm.com/">git-scm.com</a>. Command reference and changelog.</li>'
        '<li>GitHub Inc. <strong>GitHub Docs</strong>. '
        '<a href="https://docs.github.com/">docs.github.com</a>. Remote-side workflows: pull requests, releases, actions.</li>'
        '</ul>',

        '<h2>Other Languages Referenced (Rosetta Stone)</h2>',
        '<ul>'
        '<li>ISO/IEC 14882:2020. <strong>Programming languages — C++</strong>. '
        'International Organization for Standardization, 2020. Used for C/C++ comparisons in the Lexicon.</li>'
        '<li>ISO/IEC 7185:1990. <strong>Information technology — Programming languages — Pascal</strong>. '
        'Cited for the Pascal/Delphi cousins in the Lexicon.</li>'
        '<li>Embarcadero Technologies. <strong>Delphi Language Reference</strong>. '
        '<a href="https://docwiki.embarcadero.com/RADStudio/en/Delphi_Language_Reference">docwiki.embarcadero.com/RADStudio</a>.</li>'
        '<li>Microsoft Corporation. <strong>QuickBASIC Language Reference</strong>. '
        'Historical reference for the BASIC dialect used in the Lexicon comparisons.</li>'
        '</ul>',

        '<h2>Fonts and Assets</h2>',
        '<ul>'
        '<li>Van Rossum, Nikita. <strong>Fira Code</strong>. '
        '<a href="https://github.com/tonsky/FiraCode">github.com/tonsky/FiraCode</a>. '
        'Monospaced font used throughout the book and the reader app.</li>'
        '<li>Ryan L. McIntyre and Fira Code contributors. <strong>Nerd Fonts</strong>. '
        '<a href="https://www.nerdfonts.com/">nerdfonts.com</a>. Patched font glyphs.</li>'
        '</ul>',

        '<h2>Notes on Currency and Accuracy</h2>',
        '<p>This edition is written for <strong>Xcode 26 / Swift 6</strong>. Anything '
        'API-shaped moves between Apple releases; when a call site in the book disagrees '
        'with the linked primary source, the primary source is authoritative. The next '
        'major edition will be cut after WWDC 26 and updated to Xcode 27 / Swift 7.</p>',
    ]

    nav = '<a href="Front-of-Book/table-of-contents.html">Contents</a> <a href="claudex26-index.html">Index</a>'
    (BUNDLE / "bibliography.html").write_text(
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

    # Chapter landing pages no longer generated — TOC's Part II section
    # lists every Page directly under each chapter heading.

    print("\nRegenerating table-of-contents.html...")
    render_toc()

    print("Regenerating claudex26-index.html...")
    render_index()

    print("Regenerating bibliography.html...")
    render_bibliography()

    print("\nPhase 1b complete.")


if __name__ == "__main__":
    main()
