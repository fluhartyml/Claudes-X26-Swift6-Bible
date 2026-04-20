#!/usr/bin/env python3
"""Generate a Swift file per Book/Part/Appendix in a mirrored folder tree
inside the Xcode project source folder. Filesystem-synced projects
auto-discover the files on next build.

Run from the Xcode project root."""
from pathlib import Path
import string

PROJECT_ROOT = Path(__file__).parent.resolve()
SRC = PROJECT_ROOT / "Claudes X26 Swift6 Bible"
BOOKS = SRC / "Books"
APPENDICES = SRC / "Appendices"

# ---------- Data -----------------------------------------------------------

lexicon = [(L,) for L in string.ascii_uppercase]

parts = [
    (1, "The-Swift-Language", "The Swift Language", "PartI", "I"),
    (2, "Introduction", "Introduction", "PartII", "II"),
    (3, "The-User-Interface", "The User Interface", "PartIII", "III"),
    (4, "The-Application", "The Application", "PartIV", "IV"),
    (5, "Advanced-Techniques", "Advanced Techniques", "PartV", "V"),
    (6, "The-Modern-Toolchain", "The Modern Toolchain", "PartVI", "VI"),
]

# Numbered books under each part (part_num, [(num, slug, title)])
numbered = {
    2: [
        (1, "Introducing-Swift-And-Xcode", "Introducing Swift & Xcode"),
        (2, "Introducing-SwiftUI-Views", "Introducing SwiftUI Views"),
        (3, "Introducing-Scenes-And-Windows", "Introducing Scenes & Windows"),
    ],
    3: [
        (4, "Gestures-And-Input", "Gestures & Input"),
        (5, "Menus-And-Navigation", "Menus & Navigation"),
        (6, "Controls-Buttons-Toggles-Pickers", "Controls: Buttons, Toggles, Pickers"),
        (7, "Toolbars-And-Tab-Views", "Toolbars & Tab Views"),
        (8, "Lists-Grids-And-ForEach", "Lists, Grids & ForEach"),
        (9, "Text-And-TextField", "Text & TextField"),
        (10, "TextEditor-And-AttributedString", "TextEditor & AttributedString"),
        (11, "FileManager-And-Documents", "FileManager & Documents"),
        (12, "Sheets-Alerts-And-Confirmations", "Sheets, Alerts & Confirmations"),
    ],
    4: [
        (13, "Multi-Window-And-NavigationSplitView", "Multi-Window & NavigationSplitView"),
        (14, "Clipboard-DragDrop-ShareSheet", "Clipboard, Drag & Drop, Share Sheet"),
        (15, "SwiftData-And-CoreData", "SwiftData & Core Data"),
        (16, "Extensions-And-Packages", "Extensions & Packages"),
        (17, "Swift-Charts-And-PDFKit", "Swift Charts & PDFKit"),
    ],
    5: [
        (18, "Error-Handling-And-Result-Type", "Error Handling & Result Type"),
        (19, "Building-Custom-Views-And-Modifiers", "Building Custom Views & Modifiers"),
        (20, "Performance-Instruments-And-Best-Practices", "Performance, Instruments & Best Practices"),
    ],
    6: [
        (21, "Git-And-GitHub", "Git & GitHub"),
        (22, "AI-Chatbot-Integration", "AI Chatbot Integration"),
    ],
}

appendices = [
    ("A", "GitHub-Setup",          "Appendix A: GitHub Setup",          "AppendixA_GitHubSetup",       "appendix-github-setup.html"),
    ("B", "Claudes-Web-Wrapper",   "Appendix B: Claude's Web Wrapper",  "AppendixB_WebWrapper",        "appendix-claudes-web-wrapper-v2.html"),
    ("C", "QuickNote",             "Appendix C: QuickNote",             "AppendixC_QuickNote",         "appendix-quicknote.md"),
    ("D", "LockBox",               "Appendix D: Claude's LockBox",      "AppendixD_LockBox",           None),
]

# ---------- Templates ------------------------------------------------------

def book_file(struct_name: str, title: str, vault_path: str, status: str) -> str:
    return f'''//
//  {struct_name}.swift
//  Claudes X26 Swift6 Bible
//
//  Each Book is its own Swift file (see feedback_each_book_own_swift_file
//  memory). This file is the organizational home for this Book; the
//  actual content lives as HTML at the vault path shown below and is
//  rendered via BookPlaceholderView / WKWebView in v1.0. Future native
//  SwiftUI content replaces the placeholder without renaming.
//

import SwiftUI

struct {struct_name}: View {{
    var body: some View {{
        BookPlaceholderView(
            title: {swift_string(title)},
            vaultRelativePath: {swift_string(vault_path)},
            status: {swift_string(status)}
        )
    }}
}}

#Preview {{
    {struct_name}()
        .environmentObject(VaultModel())
}}
'''

def part_file(struct_name: str, part_title: str, roman: str, books_preview: list[str]) -> str:
    books_joined = ", ".join(books_preview) if books_preview else "(to be populated)"
    return f'''//
//  {struct_name}.swift
//  Claudes X26 Swift6 Bible
//
//  Part-level index view. Lists the Books in this Part.
//  Each Book lives in its own subfolder with its own Swift file.
//

import SwiftUI

struct {struct_name}: View {{
    var body: some View {{
        VStack(alignment: .leading, spacing: 12) {{
            Text("Part {roman} — {part_title}")
                .font(.largeTitle.weight(.semibold))
            Text("Books in this Part: {books_joined}")
                .font(.callout)
                .foregroundStyle(.secondary)
            Spacer()
        }}
        .padding()
        .frame(maxWidth: .infinity, alignment: .leading)
    }}
}}

#Preview {{
    {struct_name}()
}}
'''

def swift_string(s: str) -> str:
    """Return a Swift string literal with embedded quotes escaped."""
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'

def swift_identifier(slug: str) -> str:
    """Convert a dashed slug to a CamelCase Swift identifier."""
    return "".join(part.capitalize() for part in slug.split("-"))

# ---------- Build ----------------------------------------------------------

count = 0

# Ensure directories exist
BOOKS.mkdir(parents=True, exist_ok=True)
APPENDICES.mkdir(parents=True, exist_ok=True)

# Parts and their Books
for part_num, part_slug, part_title, part_struct, roman in parts:
    part_folder = BOOKS / f"Part-{roman}-{part_slug}"
    part_folder.mkdir(parents=True, exist_ok=True)

    book_previews = []

    if part_num == 1:
        # Lexicon A-Z
        for (letter,) in lexicon:
            book_folder = part_folder / f"Book-{letter}"
            book_folder.mkdir(parents=True, exist_ok=True)
            struct_name = f"Book{letter}"
            vault_path = f"Part-I-The-Swift-Language/Book-{letter}/Book-{letter}.html"
            title = f"Book {letter} — The Swift Lexicon"
            status = "Placeholder — Book not yet written."
            (book_folder / f"{struct_name}.swift").write_text(
                book_file(struct_name, title, vault_path, status)
            )
            book_previews.append(struct_name)
            count += 1
    else:
        # Numbered Books
        books = numbered.get(part_num, [])
        for num, slug, title in books:
            # Swift struct names: Book01_IntroducingSwiftAndXcode
            struct_name = f"Book{num:02d}_{swift_identifier(slug)}"
            book_folder = part_folder / f"Book-{num:02d}-{slug}"
            book_folder.mkdir(parents=True, exist_ok=True)
            vault_path = f"Part-{roman}-{part_slug}/Book-{num:02d}-{slug}/Book-{num:02d}-{slug}.html"
            full_title = f"Book {num:02d}: {title}"
            status = "Placeholder — Markdown source exists in vault root; HTML migration is Phase 1."
            (book_folder / f"{struct_name}.swift").write_text(
                book_file(struct_name, full_title, vault_path, status)
            )
            book_previews.append(struct_name)
            count += 1

    # Part-level index file
    (part_folder / f"{part_struct}.swift").write_text(
        part_file(part_struct, part_title, roman, book_previews)
    )
    count += 1

# Appendices
for letter, slug, title, struct_name, existing in appendices:
    app_folder = APPENDICES / f"Appendix-{letter}-{slug}"
    app_folder.mkdir(parents=True, exist_ok=True)
    vault_path = f"Appendices/Appendix-{letter}-{slug}/Appendix-{letter}-{slug}.html"
    status = (
        f"Placeholder — existing file at vault root: {existing}"
        if existing else "Placeholder — not yet written."
    )
    (app_folder / f"{struct_name}.swift").write_text(
        book_file(struct_name, title, vault_path, status)
    )
    count += 1

print(f"Wrote {count} Swift files.")
