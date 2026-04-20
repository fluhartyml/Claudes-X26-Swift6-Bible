// MARK: - Claude's X26 Swift6 Bible — Developer Notes
// Version: 1.0 (pre-release)
// Developer: Michael Lee Fluharty
// Engineered with: Claude by Anthropic
// License: GPL v3 — Share and share alike, attribution required
// Created: 2026-04-20
//
// ============================================================
// MISSION
// ============================================================
//
// This app is the reader / "Obsidian engine" for Claude's Xcode 26
// Swift Bible. The Bible itself is a vault of HTML rich-text
// documents living at:
//
//   ~/Developer.complex/Claudes-Xcode-26-Swift-Bible/
//
// The vault uses HTML (not markdown) as its source of truth —
// every Book (chapter), every appendix, every mapping / roadmap /
// atlas doc is a standalone HTML file with fully-functioning
// hyperlinks and multimedia. The vault folder tree mirrors the
// reading order: Parts contain Books, Books contain the HTML and
// its per-Book figures/media.
//
// Obsidian was considered as the authoring surface and does provide
// a file tree + full-text search for the vault, but it does NOT
// render standalone .html files inside its own panes — clicking an
// HTML file launches it in Safari. That's workable during early
// drafting but gets clunky at scale.
//
// This app solves that. It's a native universal SwiftUI reader that
// opens the vault root, shows a sidebar file tree that mirrors the
// folder structure, and renders the selected HTML file inline via
// WKWebView in a main pane. It is simultaneously:
//
//   1. Michael's authoring navigator while the Bible is being written.
//   2. The reader app for anyone consuming the Bible on their device.
//   3. The eventual EPUB packaging cockpit — the vault's HTML files
//      are already EPUB-shaped, so "Build EPUB" is a package step,
//      not a translation step.
//
// The final product (the EPUB) still ships through Apple Books,
// Amazon Kindle, and other EPUB venues. This app is the in-house
// tool that makes the vault usable as a vault, not just as a pile
// of HTML files.
//
// ============================================================
// RELATIONSHIP TO OTHER PROJECTS
// ============================================================
//
//   ~/Developer.complex/Claudes-Xcode-26-Swift-Bible/
//       The vault itself. This app's content source.
//       Contains: bible-atlas.html, bible-roadmap.html,
//                 swift-section-mapping.html, 22 chapter .md
//                 files (will migrate to HTML), appendices,
//                 figures, Screenshots, EPUB builds.
//
//   ~/Developer.complex/inkwell/Claudes X26 Swift6 Bible/
//       THIS project. The reader engine.
//
//   Claude's Web Wrapper (App Store live)
//       WKWebView-based app that shaped the reader thinking.
//       Where relevant, reuse patterns from its codebase.
//
//   DiamondNotesVault (NightGard family)
//       Scaffold concept that inspired this project's structure
//       (generic notes-vault shell). Not used directly — this
//       project is a fresh Xcode 26 scaffold.
//
//   InkwellJournal / InkwellBinary (inkwell family)
//       Sibling apps under the com.inkwell bundle namespace.
//       Same author, same publisher identity, different
//       editorial purpose.
//
// ============================================================
// PROJECT ROADMAP
// ============================================================
//
// v1.0 — MVP: Vault Reader
// -------------------------
//   [x] Xcode 26 project scaffolded (2026-04-20)
//   [x] SwiftData + CloudKit wired by default scaffold
//   [x] Initial commit on main
//   [ ] Rip out SwiftData scaffold (Item.swift, addItem template)
//       — SwiftData will be added back later if/when we store
//         annotations or bookmarks; MVP doesn't need it.
//   [ ] Vault root picker
//       [ ] NSOpenPanel / DocumentPicker to choose the Bible root
//       [ ] Security-scoped bookmark persisted in UserDefaults
//       [ ] Default-pick when launched inside the known path
//   [ ] Sidebar file tree
//       [ ] Directory walk of the vault root
//       [ ] Expandable / collapsible folders
//       [ ] Hide dotfiles and system folders by default
//       [ ] Icon differentiation: HTML / MD / image / other
//       [ ] Match the vault's Part / Book / Appendix structure
//   [ ] Main pane: WKWebView HTML renderer
//       [ ] Render the selected HTML file with its base URL
//           set so relative links and figures work
//       [ ] Intercept anchor clicks: internal vault links
//           navigate in-app; external links open in Safari
//       [ ] Forward / back history
//       [ ] "Home" button → bible-atlas.html
//   [ ] Address bar showing relative-to-vault path
//   [ ] Dark mode matches the amber-proofing aesthetic
//   [ ] Window chrome: 900x720 default (matches NightGard LC)
//   [ ] Under the Hood view (see UNDER THE HOOD section below)
//
// v1.1 — Navigation & Search
// ---------------------------
//   [ ] Full-text search across all HTML files in the vault
//   [ ] Jump-to-line-number ("open file X at line N")
//   [ ] Breadcrumb trail (Part → Book → sub-heading)
//   [ ] Keyboard shortcuts (cmd-L next Book, cmd-H atlas, etc.)
//   [ ] Bookmarks / recents
//
// v1.2 — Proofing Support
// ------------------------
//   [ ] Proofing-flag state introspection (show count of
//       locked/discussed/interp/approved lines per file)
//   [ ] "Next unfinished" navigation
//   [ ] Side-by-side proof view: edit pane + live render pane
//
// v1.3 — EPUB Packaging Cockpit
// ------------------------------
//   [ ] "Build EPUB" command that zips the vault into a valid EPUB
//       (manifest + spine + nav + meta-inf)
//   [ ] Embed FiraCode Nerd Font into output
//   [ ] Versioning: auto-increment EPUB filename
//
// v2.0 — Annotation Layer (if warranted)
// ---------------------------------------
//   [ ] Reader highlights / notes
//   [ ] SwiftData + CloudKit backing (bring back what we rip out in v1.0)
//   [ ] Sync across iPhone/iPad/Mac
//
// ============================================================
// ARCHITECTURE DECISIONS
// ============================================================
//
// Platforms
// ---------
//   Universal iOS / iPadOS / macOS SwiftUI. macOS is the primary
//   authoring-surface target; iOS/iPadOS are reader-surface targets.
//   Designed to be useful on all three from v1.0 though the macOS
//   build gets the authoring amenities first.
//
// HTML Rendering
// --------------
//   WKWebView. Matches what Claude's Web Wrapper uses and what
//   EPUB readers use under the hood. The vault is designed to be
//   EPUB-shaped, so rendering the vault in a WebView is the same
//   code path as rendering the eventual EPUB output.
//
// Vault Access
// ------------
//   The app is sandbox-compatible. Vault root is chosen via
//   picker + security-scoped bookmark (same pattern as NightGard
//   Library Commander's working-folder picker). No hardcoded path.
//
// State Storage
// -------------
//   SwiftData scaffold stays in the project but is ripped out of
//   the app body for MVP. Re-enabled in v2.0 for annotations.
//   UserDefaults holds simple persistent state (vault bookmark,
//   recent files, preferences).
//
// Internal Navigation
// -------------------
//   WKWebView's decidePolicyFor delegate intercepts link clicks.
//   Relative / same-origin links navigate inside the app.
//   Absolute http/https links launch externally (Safari / OS).
//
// Font
// ----
//   FiraCode Nerd Font Mono embedded (SIL OFL 1.1). Matches the
//   Bible's house font and the amber-proofing aesthetic.
//
// Dark Mode First
// ---------------
//   The proofing docs (atlas / roadmap / mapping) use amber-on-black
//   CRT styling. The reader's default palette complements that.
//   Light mode is an accommodation, not the default.
//
// ============================================================
// VAULT STRUCTURE (for the renderer to reflect)
// ============================================================
//
//   Claudes-Xcode-26-Swift-Bible/
//     bible-atlas.html                (master index)
//     bible-roadmap.html              (whole-product roadmap)
//     swift-section-mapping.html      (Swift section map)
//     Part-I-The-Swift-Language/      (Books A–Z, planned)
//     Part-II-Introduction/           (Books 01–03, migration pending)
//     Part-III-The-User-Interface/    (Books 04–12, migration pending)
//     Part-IV-The-Application/        (Books 13–17, migration pending)
//     Part-V-Advanced-Techniques/     (Books 18–20, migration pending)
//     Part-VI-The-Modern-Toolchain/   (Books 21–22, migration pending)
//     Appendices/
//       Appendix-A-GitHub-Setup/
//       Appendix-B-Claudes-Web-Wrapper/
//       Appendix-C-QuickNote/
//       Appendix-D-LockBox/           (planned)
//     _shared/
//       css/                          (vault-wide stylesheet)
//       fonts/                        (FiraCode Nerd Font)
//       cover.jpg
//
// ============================================================
// KNOWN OPEN QUESTIONS (from bible-roadmap.html)
// ============================================================
//
//   3.1  Part numbering — Swift = Part I vs. Volume Zero
//   3.2  Shared assets location
//   3.3  Cross-linking convention
//   3.4  Multimedia scope (images only / + video / + audio)
//   3.6  Entry format for Swift lexicon Books
//   7.6  SwiftUI wrappers in the Swift lexicon (yes/no)
//   7.7  Operators / punctuation placement
//   7.8  Thin letters Q/X/Y/Z (keep four / collapse to one)
//
// These inform the renderer's feature set but don't block MVP.
//
// ============================================================
// UNDER THE HOOD (reader-visible)
// ============================================================
//
// This app is one of the Bible's companion / sample / build-along
// apps — so the reader must be able to read these Developer Notes
// inside the app itself, not only in source or on the wiki.
//
// v1.0 ships with an "Under the Hood" view (settings tab, menu
// item, or sidebar entry — placement TBD during build) that
// renders this Developer Notes content in a readable layout. The
// same text lives in three places that stay synced:
//
//   1. This file — Claudes_X26_Swift6_Bible_DeveloperNotes.swift
//   2. The wiki — Developer-Notes.md
//   3. In-app — Under the Hood view
//
// The teaching promise of the Swift Bible is that a reader can
// follow an appendix, build the companion app, install it, and
// then open it to find the same developer documentation Michael
// would keep for his own apps. The Under the Hood view is the
// book's window into the engine.
//
// Companion apps with this pattern:
//   • Claude's QuickNote
//   • Claude's Web Wrapper
//   • Claude's LockBox
//   • Claude's X26 Swift6 Bible (this app)
//   • Future: Claude's SketchPad, PulseBoard, TapTally, ...
//
// ============================================================
// ATTRIBUTION
// ============================================================
//
// Inspired by Tom Swan's Delphi 4 Bible (IDG Books, 1998),
// which is the structural pattern for the Bible content itself.
// The reader app is original work — a modern WKWebView-based
// native vault browser for Apple platforms.
//
// ============================================================
