#!/usr/bin/env python3
"""
Render Phase 1a content into BibleContent.bundle:
  - 12 chapters with real .md sources -> HTML Books with universal template
  - 10 empty chapters -> proposed-scope HTML pages (outline + planned topics)
  - 4 appendices from .md sources -> HTML appendices

Universal template: line numbers, outline numbering, matching header+footer
with file path (extension hidden) and reading position.
"""

import re
import shutil
from pathlib import Path

BUNDLE = Path(
    "/Users/michaelfluharty/Developer.complex/inkwell/"
    "Claudes X26 Swift6 Bible/Claudes X26 Swift6 Bible/BibleContent.bundle"
)

# Book number -> (part folder, slug used for Book-NN-<slug>/ folder)
BOOKS = [
    (1,  "Part-I-Introduction",          "Introducing-Swift-And-Xcode"),
    (2,  "Part-I-Introduction",          "Introducing-SwiftUI-Views"),
    (3,  "Part-I-Introduction",          "Introducing-Scenes-And-Windows"),
    (4,  "Part-III-The-User-Interface",  "Gestures-And-Input"),
    (5,  "Part-III-The-User-Interface",  "Menus-And-Navigation"),
    (6,  "Part-III-The-User-Interface",  "Controls-Buttons-Toggles-Pickers"),
    (7,  "Part-III-The-User-Interface",  "Toolbars-And-Tab-Views"),
    (8,  "Part-III-The-User-Interface",  "Lists-Grids-And-ForEach"),
    (9,  "Part-III-The-User-Interface",  "Text-And-TextField"),
    (10, "Part-III-The-User-Interface",  "TextEditor-And-AttributedString"),
    (11, "Part-III-The-User-Interface",  "FileManager-And-Documents"),
    (12, "Part-III-The-User-Interface",  "Sheets-Alerts-And-Confirmations"),
    (13, "Part-IV-The-Application",      "Multi-Window-And-NavigationSplitView"),
    (14, "Part-IV-The-Application",      "Clipboard-DragDrop-ShareSheet"),
    (15, "Part-IV-The-Application",      "SwiftData-And-CoreData"),
    (16, "Part-IV-The-Application",      "Extensions-And-Packages"),
    (17, "Part-IV-The-Application",      "Swift-Charts-And-PDFKit"),
    (18, "Part-V-Advanced-Techniques",   "Error-Handling-And-Result-Type"),
    (19, "Part-V-Advanced-Techniques",   "Building-Custom-Views-And-Modifiers"),
    (20, "Part-V-Advanced-Techniques",   "Performance-Instruments-And-Best-Practices"),
    (21, "Part-VI-The-Modern-Toolchain", "Git-And-GitHub"),
    (22, "Part-VI-The-Modern-Toolchain", "AI-Chatbot-Integration"),
]

# Source .md file naming at bundle root
def md_source_name(n, slug):
    # Books 01-03 sources are named "0N-Introducing-<slug-after-Introducing>.md"
    # Rest are named "NN-<slug>.md"
    # But actually from audit: 01-Introducing-Swift-And-Xcode.md etc. - matches slug form
    return f"{n:02d}-{slug}.md"

# Human-friendly title (drop "Introducing-" prefix from slug for display)
def book_title(slug):
    return slug.replace("-", " ")

# Appendix sources
APPENDICES = [
    ("A", "GitHub-Setup",          "appendix-github-setup.md"),
    ("B", "Claudes-Web-Wrapper",   "appendix-claudes-web-wrapper.md"),
    ("C", "QuickNote",             "appendix-quicknote.md"),
    ("D", "LockBox",               None),  # no source - stays as scope page
]

# Proposed scope for empty chapters
SCOPE = {
    4: {
        "why": "Reader has seen Books 01-03 introducing Swift, SwiftUI, and Scenes. Book 04 turns the reader's attention to how users actually interact with a running SwiftUI app: taps, swipes, drags, hardware keyboards, and Apple Pencil.",
        "sections": [
            ("Gesture Basics", [
                "The .onTapGesture, .onLongPressGesture family",
                "DragGesture, MagnificationGesture, RotationGesture",
                "Sequenced and simultaneous gestures",
                "Gesture state via @GestureState",
            ]),
            ("Keyboard and Hardware Input", [
                "Text field focus management with @FocusState",
                "Hardware keyboard shortcuts (.keyboardShortcut)",
                "onKeyPress for arrow-key navigation",
                "Submit / return handling",
            ]),
            ("Apple Pencil and iPad", [
                "Scribble for text entry (no code required)",
                "PencilKit canvas layered over content",
                "Pencil 2 double-tap via UIPencilInteraction",
            ]),
        ],
        "examples": [
            "DragGesture that moves a view and snaps back",
            "Custom long-press menu that reveals actions",
            "PencilKit canvas for sketching over an image",
        ],
        "figures": [
            "Screenshot of a DragGesture in action",
            "Side-by-side: Scribble input vs. keyboard input vs. dictation",
            "PencilKit canvas with sample stroke",
        ],
    },
    13: {
        "why": "Books 04-12 have covered interaction and controls. Book 13 scales the app up: multi-column layouts for iPad and Mac, multi-window on platforms that support it, and how a single SwiftUI codebase shapes itself to each form factor.",
        "sections": [
            ("NavigationSplitView", [
                "Two-column and three-column layouts",
                "NavigationSplitViewVisibility",
                "Column-width controls and sidebar behavior",
                "Programmatic selection across columns",
            ]),
            ("Multi-Window (iPad and Mac)", [
                "WindowGroup and Scene composition",
                "Opening a new window with openWindow",
                "Per-window state vs shared state",
                "Restoring windows across launches",
            ]),
            ("Platform Adaptation", [
                "Compact vs regular size classes",
                "Adaptive layouts using ViewThatFits",
                "Conditional modifiers per platform",
            ]),
        ],
        "examples": [
            "Three-column reader shell (Library | Books | Page)",
            "Settings window spawned from a toolbar button",
            "Layout that collapses to a single column on iPhone",
        ],
        "figures": [
            "iPad three-column layout",
            "Mac multi-window scene with two inspectors",
            "iPhone compact layout of the same app",
        ],
    },
    14: {
        "why": "With the app laid out across windows and columns, users expect to move data between views, apps, and devices. Book 14 covers the three standard transfer mechanisms on Apple platforms.",
        "sections": [
            ("The Clipboard", [
                "UIPasteboard / NSPasteboard basics",
                "Copy / paste menu integration",
                "Transferable for typed clipboard content",
            ]),
            ("Drag and Drop", [
                "draggable and dropDestination modifiers",
                "Transferable conformance",
                "Inter-app drag on iPadOS",
            ]),
            ("Share Sheet", [
                "ShareLink with typed payloads",
                "Custom Transferable for share content",
                "Preview images in the share sheet",
            ]),
        ],
        "examples": [
            "Copy a struct to the clipboard and paste it back",
            "Drag a row between two lists",
            "ShareLink that exports the current page as a file",
        ],
        "figures": [
            "Drag-and-drop between two SwiftUI lists",
            "ShareLink presenting the iOS share sheet",
        ],
    },
    15: {
        "why": "Once the app accepts input and moves data, it needs somewhere to keep it. Book 15 covers Apple's modern persistence story: SwiftData as the default, Core Data as the interop bridge, CloudKit as the sync layer.",
        "sections": [
            ("SwiftData Basics", [
                "@Model macro and model container",
                "@Query to read from the store",
                "Inserts, updates, deletes",
                "Relationships and cascade rules",
            ]),
            ("CloudKit Sync", [
                "Enabling iCloud in capabilities",
                "What SwiftData + CloudKit does automatically",
                "What it does NOT do (schema migrations, private vs shared)",
            ]),
            ("Core Data Interop", [
                "When Core Data is still the answer (NSFetchedResultsController, complex migrations)",
                "Bridging SwiftData to existing Core Data stores",
            ]),
        ],
        "examples": [
            "@Model Note with title, body, timestamp",
            "@Query sorted by date, filtered by search string",
            "CloudKit-synced SwiftData container",
        ],
        "figures": [
            "Xcode iCloud capability toggle",
            "Data flow: @Model -> ModelContext -> ModelContainer -> CloudKit",
        ],
    },
    17: {
        "why": "Persistence covered, the app now needs to visualize and export. Book 17 introduces Swift Charts for visualization and PDFKit for export, covering the cases that commonly ship in real apps.",
        "sections": [
            ("Swift Charts", [
                "BarMark, LineMark, PointMark",
                "Axis and legend configuration",
                "Interactive selection",
                "Accessibility labels for charts",
            ]),
            ("PDFKit", [
                "PDFView to display a document",
                "PDFDocument in code (page extraction, metadata)",
                "Rendering a SwiftUI view to a PDF page",
                "Saving the generated PDF to Files",
            ]),
        ],
        "examples": [
            "Bar chart of weekly totals with selection callout",
            "Export the current page as a one-page PDF",
        ],
        "figures": [
            "Finished bar chart with axis labels",
            "SwiftUI view rendered to a PDF viewer",
        ],
    },
    18: {
        "why": "Real apps handle real failure. Book 18 turns to Swift's error surface: throws / try / catch, the Result type, and how errors flow through async code without losing context.",
        "sections": [
            ("Thrown Errors", [
                "The Error protocol",
                "throws, try, try?, try!",
                "do / catch with multiple patterns",
            ]),
            ("Result<T, E>", [
                "When Result beats thrown errors",
                "Bridging between the two styles",
                "Result in completion-handler code",
            ]),
            ("Errors in async Code", [
                "async throws",
                "Cancellation as an error",
                "Structured concurrency and task groups",
            ]),
        ],
        "examples": [
            "File loader that throws typed errors",
            "Networking call returning Result<Response, NetworkError>",
            "async fetch with cancellation handling",
        ],
        "figures": [
            "Error flow diagram: thrown vs Result vs async",
        ],
    },
    19: {
        "why": "Chapters 02 through 12 have built views from SwiftUI primitives. Book 19 flips the perspective: how the reader builds their own reusable views, modifiers, and styles that other parts of the app can compose with.",
        "sections": [
            ("Custom Views", [
                "Composition over inheritance",
                "Generic views over content",
                "ViewBuilder parameters and @ViewBuilder closures",
            ]),
            ("Custom Modifiers", [
                "The ViewModifier protocol",
                "modifier() vs direct extension on View",
                "Environment-aware modifiers",
            ]),
            ("Style Protocols", [
                "ButtonStyle, LabelStyle, ToggleStyle",
                "When to roll your own style",
            ]),
        ],
        "examples": [
            "A CardView<Content> generic container",
            "A .glow() modifier using shadow layers",
            "A custom ButtonStyle with press animation",
        ],
        "figures": [
            "Before / after of applying a custom modifier",
        ],
    },
    20: {
        "why": "Book 19 built composable pieces; Book 20 measures them. Instruments, Time Profiler, and the discipline of not guessing about performance.",
        "sections": [
            ("Instruments", [
                "Time Profiler for CPU hot spots",
                "Allocations for memory growth",
                "SwiftUI template for view body churn",
            ]),
            ("Common Traps", [
                "Unnecessary view recomputation",
                "Sorting inside body",
                "Synchronous work on the main actor",
            ]),
            ("Best Practices", [
                "Measure before optimizing",
                "Profile builds in Release configuration",
                "Ship with profiling hooks (OSSignposter)",
            ]),
        ],
        "examples": [
            "Profile a laggy List and pinpoint the body call",
            "Reduce recomputation with Equatable views",
        ],
        "figures": [
            "Instruments Time Profiler screenshot",
            "SwiftUI body-count template screenshot",
        ],
    },
    21: {
        "why": "Book 21 pivots from the app to the developer's toolchain. Git is not optional; GitHub is not optional. This Book teaches the daily workflow the reader needs.",
        "sections": [
            ("Git Basics", [
                "clone, add, commit, push, pull",
                "Branches and merges",
                "Undoing: reset, revert, checkout",
            ]),
            ("GitHub Workflow", [
                "Repos, remotes, and SSH keys",
                "Pull requests and code review",
                "Issues, labels, milestones",
                "Wikis and releases",
            ]),
            ("Xcode Integration", [
                "Source Control navigator",
                "Committing from Xcode vs terminal",
                "Conflict resolution in Xcode",
            ]),
        ],
        "examples": [
            "First push of a new Xcode project to GitHub",
            "Branching, merging, and resolving a conflict",
        ],
        "figures": [
            "Xcode Source Control navigator",
            "A GitHub PR review screen",
        ],
    },
    22: {
        "why": "The final Book closes the loop: using AI assistance as part of the development loop, and integrating LLM-backed features into shipping apps.",
        "sections": [
            ("Using AI to Build the App", [
                "Claude Code and the terminal workflow",
                "Xcode + LLM integrations",
                "Prompt patterns that work for Swift code",
            ]),
            ("Integrating LLMs Into Apps", [
                "Anthropic API basics in Swift",
                "Streaming responses in SwiftUI",
                "Privacy: on-device vs cloud, PII handling",
            ]),
            ("Design Patterns", [
                "Conversations as state",
                "Tool use and function calling",
                "Guardrails and prompt hygiene",
            ]),
        ],
        "examples": [
            "Minimal chat view that streams from the Anthropic API",
            "Swift function exposed as a tool to the model",
        ],
        "figures": [
            "Claude Code terminal interacting with an Xcode project",
            "Streaming chat view in SwiftUI",
        ],
    },
}


# ---------- Markdown -> HTML conversion ----------

def esc(s):
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;"))

def inline(s):
    # inline code first (protect from other transforms)
    placeholders = []
    def take(m):
        placeholders.append(esc(m.group(1)))
        return f"\x00{len(placeholders)-1}\x00"
    s = re.sub(r"`([^`]+)`", take, s)

    s = esc(s)
    # bold **x**
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    # italic *x* (avoid eating bolds already replaced)
    s = re.sub(r"(?<![\\*])\*([^*\n]+)\*", r"<em>\1</em>", s)
    # links [text](url)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)

    # restore inline code
    def put(m):
        idx = int(m.group(1))
        return f"<code>{placeholders[idx]}</code>"
    s = re.sub(r"\x00(\d+)\x00", put, s)
    return s

def md_to_blocks(md_text):
    """Convert Markdown to a list of top-level HTML blocks (each becomes a <li> line)."""
    lines = md_text.splitlines()
    blocks = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        # fenced code block
        if line.startswith("```"):
            lang = line[3:].strip()
            buf = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1  # skip closing fence
            code = esc("\n".join(buf))
            blocks.append(f'<pre><code class="lang-{lang}">{code}</code></pre>')
            continue
        # heading
        m = re.match(r"^(#{1,3})\s+(.*)$", line)
        if m:
            level = len(m.group(1))
            text = inline(m.group(2).strip())
            blocks.append(f"<h{level}>{text}</h{level}>")
            i += 1
            continue
        # horizontal rule
        if re.match(r"^---+\s*$", line) or re.match(r"^\*\*\*+\s*$", line):
            blocks.append("<hr>")
            i += 1
            continue
        # list (bullet)
        if re.match(r"^[-*]\s+", line):
            items = []
            while i < len(lines) and re.match(r"^[-*]\s+", lines[i]):
                items.append(inline(re.sub(r"^[-*]\s+", "", lines[i])))
                i += 1
            li = "".join(f"<li>{t}</li>" for t in items)
            blocks.append(f"<ul>{li}</ul>")
            continue
        # list (ordered)
        if re.match(r"^\d+\.\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i]):
                items.append(inline(re.sub(r"^\d+\.\s+", "", lines[i])))
                i += 1
            li = "".join(f"<li>{t}</li>" for t in items)
            blocks.append(f'<ol class="body-list">{li}</ol>')
            continue
        # paragraph (collect until blank or structural)
        buf = [line]
        i += 1
        while (i < len(lines)
               and lines[i].strip()
               and not lines[i].startswith(("#", "```", "---", "- ", "* "))
               and not re.match(r"^\d+\.\s+", lines[i])):
            buf.append(lines[i])
            i += 1
        text = inline(" ".join(b.strip() for b in buf))
        blocks.append(f"<p>{text}</p>")
    return blocks


# ---------- Page template ----------

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
ol.lines > li > p, ol.lines > li > h2, ol.lines > li > h3, ol.lines > li > ul, ol.lines > li > ol, ol.lines > li > pre, ol.lines > li > hr { margin: 0; }
.scope-note { border-left: 3px solid var(--bright); padding: 0.7rem 1rem; background: #140c00; margin: 0.6rem 0; color: var(--bright); }
.nav { display: flex; gap: 0.9rem; flex-wrap: wrap; margin-top: 0.8rem; font-size: 14pt; }
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


def render_page(title, path_display, pos_label, body_blocks, nav_html):
    # Wrap each block in <li>
    body = "\n".join(f"  <li>{b}</li>" for b in body_blocks)
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


def nav_for_book(n, part, slug):
    return (
        f'<a href="../Front-of-Book/table-of-contents.html">&larr; Contents</a>'
        f'<a href="../claudex26-index.html">Index</a>'
    )


def scope_blocks(n, slug, data):
    title = slug.replace("-", " ")
    blocks = []
    blocks.append(f"<h1>Book {n:02d}: {esc(title)}</h1>")
    blocks.append(
        '<div class="scope-note">This Book is <strong>proposed-scope</strong>. '
        'The outline below is what will be written. Leave '
        "<code>MICHAEL:</code> notes anywhere and I will fold them in before writing the prose.</div>"
    )
    blocks.append("<h2>Why This Book Exists</h2>")
    blocks.append(f"<p>{esc(data['why'])}</p>")
    blocks.append("<h2>Planned Sections</h2>")
    for sec_title, bullets in data["sections"]:
        blocks.append(f"<h3>{esc(sec_title)}</h3>")
        ul = "".join(f"<li>{esc(b)}</li>" for b in bullets)
        blocks.append(f"<ul>{ul}</ul>")
    blocks.append("<h2>Planned Code Examples</h2>")
    ul = "".join(f"<li>{esc(e)}</li>" for e in data["examples"])
    blocks.append(f"<ul>{ul}</ul>")
    blocks.append("<h2>Planned Figures</h2>")
    ul = "".join(f"<li>{esc(f)}</li>" for f in data["figures"])
    blocks.append(f"<ul>{ul}</ul>")
    return blocks


# ---------- Write pages ----------

def write_book(n, part, slug):
    file_name   = f"Book-{n:02d}-{slug}.html"
    path_display = f"{part}/Book-{n:02d}-{slug}"

    out_dir = BUNDLE / part
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / file_name

    md_name = f"{n:02d}-{slug}.md"
    md_file = BUNDLE / md_name

    # empty chapter? render scope page
    if n in SCOPE and (not md_file.exists() or md_file.stat().st_size == 0):
        blocks = scope_blocks(n, slug, SCOPE[n])
        pos = f"Part {part.split('-')[1]} &middot; Book {n:02d} &middot; Proposed Scope"
    else:
        md = md_file.read_text() if md_file.exists() else ""
        if md.strip():
            blocks = md_to_blocks(md)
            pos = f"Part {part.split('-')[1]} &middot; Book {n:02d}"
        else:
            blocks = [f"<h1>Book {n:02d}: {book_title(slug)}</h1>",
                      '<p><em>No content written yet.</em></p>']
            pos = f"Part {part.split('-')[1]} &middot; Book {n:02d}"

    html = render_page(
        title=f"Book {n:02d}: {book_title(slug)}",
        path_display=path_display,
        pos_label=pos,
        body_blocks=blocks,
        nav_html=nav_for_book(n, part, slug),
    )
    out_file.write_text(html)
    print(f"  wrote {out_file.relative_to(BUNDLE)}")


def write_appendix(letter, slug, md_name):
    file_name   = f"Appendix-{letter}-{slug}.html"
    path_display = f"Appendices/Appendix-{letter}-{slug}"

    out_dir = BUNDLE / "Appendices"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / file_name

    if md_name:
        md_path = BUNDLE / md_name
        if md_path.exists() and md_path.read_text().strip():
            blocks = md_to_blocks(md_path.read_text())
        else:
            blocks = [f"<h1>Appendix {letter}: {slug.replace('-', ' ')}</h1>",
                      '<p><em>No content written yet.</em></p>']
    else:
        blocks = [f"<h1>Appendix {letter}: {slug.replace('-', ' ')}</h1>",
                  '<div class="scope-note">Appendix D (LockBox build-along) is planned but not yet written.</div>']

    pos = f"Appendix {letter}"
    nav = ('<a href="../Front-of-Book/table-of-contents.html">&larr; Contents</a>'
           '<a href="../claudex26-index.html">Index</a>')
    html = render_page(
        title=f"Appendix {letter}: {slug.replace('-', ' ')}",
        path_display=path_display,
        pos_label=pos,
        body_blocks=blocks,
        nav_html=nav,
    )
    out_file.write_text(html)
    print(f"  wrote {out_file.relative_to(BUNDLE)}")


def main():
    print("Rendering Books (Phase 1a)...")
    for n, part, slug in BOOKS:
        # Skip Book 00 - already written
        if n == 0:
            continue
        write_book(n, part, slug)

    print("\nRendering Appendices...")
    for letter, slug, md in APPENDICES:
        write_appendix(letter, slug, md)

    print("\nPhase 1a render complete.")


if __name__ == "__main__":
    main()
