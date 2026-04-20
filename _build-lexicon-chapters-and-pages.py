#!/usr/bin/env python3
"""Rename Book-{A-Z} to Chapter-{A-Z} in the Xcode project (Part I lexicon)
and generate one Page-*.swift file per Swift entry in each Chapter.

Also renames the vault's Part-I placeholders to match (Book-X.html →
Chapter-X.html) so Xcode references resolve.

Run from the Xcode project root.
"""
from pathlib import Path
import shutil
import string
import re

PROJECT_ROOT = Path(__file__).parent.resolve()
SRC = PROJECT_ROOT / "Claudes X26 Swift6 Bible"
BOOKS = SRC / "Books"

# Vault lives next to the inkwell workspace — one level up from project root,
# then sibling "Claudes-Xcode-26-Swift-Bible".
VAULT = PROJECT_ROOT.parent.parent / "Claudes-Xcode-26-Swift-Bible"

# ---------- Entries per Chapter (from swift-section-mapping.html) ----------

entries = {
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
    'J': [],  # thin — JSON cross-ref only
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

# ---------- Helpers --------------------------------------------------------

def entry_slug(entry: str) -> str:
    """Filename slug for a Swift entry. Strips @ and # prefixes."""
    return entry.lstrip('@#').replace(' ', '-')

def swift_struct_name(entry: str) -> str:
    """Generate a valid Swift struct identifier: Page<PascalCase>."""
    clean = entry.lstrip('@#')
    # Capitalize first letter; preserve rest
    if clean and clean[0].islower():
        clean = clean[0].upper() + clean[1:]
    return "Page" + clean

def swift_string(s: str) -> str:
    """Return a Swift string literal with embedded quotes/backslashes escaped."""
    if s is None:
        return "nil"
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'

# ---------- Rename Step 1: Xcode project Part I Book-X → Chapter-X ---------

part_i_xcode = BOOKS / "Part-I-The-Swift-Language"

renamed_count = 0
for letter in string.ascii_uppercase:
    old = part_i_xcode / f"Book-{letter}"
    new = part_i_xcode / f"Chapter-{letter}"
    if old.exists() and not new.exists():
        # Also rename the Swift file inside
        old_swift = old / f"Book{letter}.swift"
        new_swift = old / f"Chapter{letter}.swift"
        if old_swift.exists():
            # Update struct name inside the swift file
            content = old_swift.read_text()
            content = content.replace(f"Book{letter}", f"Chapter{letter}")
            # Also update the vault path reference
            content = content.replace(f"Part-I-The-Swift-Language/Book-{letter}/Book-{letter}.html",
                                     f"Part-I-The-Swift-Language/Chapter-{letter}/Chapter-{letter}.html")
            content = content.replace(f"Book {letter} — The Swift Lexicon",
                                     f"Chapter {letter} — The Swift Lexicon")
            new_swift.write_text(content)
            old_swift.unlink()
        shutil.move(str(old), str(new))
        renamed_count += 1

print(f"Renamed {renamed_count} Xcode Book folders to Chapter folders.")

# ---------- Rename Step 2: Vault Part I Book-X → Chapter-X -----------------

part_i_vault = VAULT / "Part-I-The-Swift-Language"
if part_i_vault.exists():
    vault_renamed = 0
    for letter in string.ascii_uppercase:
        old_folder = part_i_vault / f"Book-{letter}"
        new_folder = part_i_vault / f"Chapter-{letter}"
        if old_folder.exists() and not new_folder.exists():
            # Rename HTML file inside first
            old_html = old_folder / f"Book-{letter}.html"
            new_html = old_folder / f"Chapter-{letter}.html"
            if old_html.exists():
                html = old_html.read_text()
                html = html.replace(f"Book-{letter}", f"Chapter-{letter}")
                html = html.replace(f"Book {letter} — The Swift Lexicon",
                                   f"Chapter {letter} — The Swift Lexicon")
                html = html.replace(f"Book {letter}",
                                   f"Chapter {letter}")
                html = html.replace(f"This is Book", f"This is Chapter")
                new_html.write_text(html)
                old_html.unlink()
            shutil.move(str(old_folder), str(new_folder))
            vault_renamed += 1
    print(f"Renamed {vault_renamed} vault Book folders to Chapter folders.")

# ---------- Rename Step 3: Update PartI.swift reference list ---------------

part_i_swift = part_i_xcode / "PartI.swift"
if part_i_swift.exists():
    content = part_i_swift.read_text()
    # Book struct references → Chapter
    content = re.sub(r'Book([A-Z])', r'Chapter\1', content)
    part_i_swift.write_text(content)
    print("Updated PartI.swift references (Book → Chapter).")

# ---------- Generate Page-*.swift per entry -------------------------------

page_template = """//
//  {struct_name}.swift
//  Claudes X26 Swift6 Bible
//
//  Page: {headword}  (Chapter {letter}, kind: {kind})
//  Part of the Swift Lexicon. One Page per entry. See
//  project_lexicon_page_structure memory for the Rosetta-Stone format.
//

import SwiftUI

struct {struct_name}: View {{
    var body: some View {{
        PagePlaceholderView(
            headword: {headword_literal},
            chapter: {chapter_literal},
            kind: {kind_literal}
        )
    }}
}}

#Preview {{
    {struct_name}()
}}
"""

page_count = 0
for letter in string.ascii_uppercase:
    chapter_dir = part_i_xcode / f"Chapter-{letter}"
    if not chapter_dir.exists():
        continue
    pages_dir = chapter_dir / "Pages"
    pages_dir.mkdir(exist_ok=True)

    for entry, kind in entries.get(letter, []):
        struct_name = swift_struct_name(entry)
        slug = entry_slug(entry)
        page_path = pages_dir / f"Page-{slug}.swift"
        page_path.write_text(page_template.format(
            struct_name=struct_name,
            headword=entry,
            letter=letter,
            kind=kind,
            headword_literal=swift_string(entry),
            chapter_literal=swift_string(letter),
            kind_literal=swift_string(kind),
        ))
        page_count += 1

print(f"Wrote {page_count} Page Swift files.")
