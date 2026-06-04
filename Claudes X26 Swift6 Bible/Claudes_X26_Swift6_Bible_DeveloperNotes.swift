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
//     Part-II-The-Swift-Language/      (Books A–Z, planned)
//     Part-I-Introduction/           (Books 01–03, migration pending)
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
// BOOK AUTHORING — CLAUDE X26 PARAMETERS
// ============================================================
//
// These rules govern every page of the book. They were previously
// published in the Front Matter of the Bible vault as Claude X26
// Parameters, but they're author-scaffolding (instructions Claude
// follows while generating content), not reader material — so they
// live here in Developer Notes now.
//
// CITATION STANDARD
//   • Every factual claim must be double-cited — two independent,
//     verifiable sources.
//   • Same standard as sworn testimony under perjury consequences.
//   • If it can't be double-cited, qualify it as opinion or
//     unverified.
//   • Footnotes on each page, numbered, at the bottom.
//   • Bibliography (back matter) collects all sources organized by
//     Book.
//
// SOURCE REQUIREMENTS
//   • All sources must be named — no anonymous posts, no "sources
//     say."
//   • All sources must be accountable — an author or organization
//     that stands behind the claim.
//   • All sources must be verifiable — the reader can confirm
//     independently.
//   • No political bias, no editorial slant — technical facts only.
//   • Apple is the primary arbiter of truth (they invented Swift).
//   • Second source corroborates: Swift.org, WWDC sessions, Swift
//     Evolution proposals, or named authors.
//
// Good sources:
//   - Apple Developer Documentation
//   - Swift.org (proposals, blog posts, forums — authored)
//   - WWDC sessions (named presenters)
//   - Swift Evolution proposals (authored, reviewed, voted on)
//   - Named authors on published books or articles
//
// Bad sources:
//   - Anonymous Stack Overflow answers
//   - Unsigned blog posts
//   - Reddit comments
//   - Unattributed wikis
//
// WRITING STYLE
//   • Michael's voice — plain American, direct, conversational.
//   • Short sentences. Get to the point.
//   • Explain by what it does, not what it is.
//   • Connect new concepts to familiar ground (Delphi, electronics,
//     military).
//   • No fluff, no hype, no academic tone.
//   • If it's complicated, say so — don't dress it up.
//   • Practical first — "how do I use this" before "how does this
//     work."
//   • Like a technician explaining to another technician at the
//     bench.
//
// FONT AND FORMATTING
//   • FiraCode Nerd Font (embedded, SIL OFL 1.1).
//   • 18pt minimum body text.
//   • Code examples in monospaced blocks.
//   • Every reader-visible page has a header and footer with its
//     file path (extension hidden) and reading position.
//   • Every reader-visible page has line numbers down the left
//     gutter so any sentence is addressable.
//   • Every paragraph is outline-numbered (1, 1.1, 1.1.1).
//
// LICENSE
//   • GPL v3 — share and share alike with attribution required.
//
// PROOFING
//   • Michael reads and proofs each page as it's written.
//   • Inline notes prefixed `MICHAEL:` anywhere in any vault file;
//     Claude grep-finds them, acts, removes the marker.
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
// CAPTURED TASK — AUTO-GENERATE THE TABLE OF CONTENTS
// (recorded 2026-05-31 per Michael; do NOT implement as a tangent)
// ============================================================
//
// DECISION (Michael, 2026-05-31): The hand-maintained
// Front-of-Book/table-of-contents.html is a defect. It must be
// removed from EPUB builds permanently, and THIS reader app must
// generate its own Table of Contents automatically — the way Apple
// Books does — instead of loading the manual HTML file.
//
// WHY the manual TOC is a bug:
//   • In the EPUB, pandoc renames every chapter to ch###.xhtml, so
//     the manual TOC's <a href> links (Book-NN-Title.html, etc.) all
//     point at paths that no longer exist — every tap is dead. Apple
//     Books v15 shipped this; v20 regressed it. The build script
//     Workshop/Tools/build-epub.sh already filters it out
//     (`! -name "table-of-contents.html"`). See apartment memory
//     feedback_epub_excludes_manual_toc. It must NEVER re-enter a spine.
//   • A hand-maintained TOC also rots every time the book's structure
//     changes. Auto-generation removes the whole class of problem.
//
// WHAT TO BUILD (when picked up — not now):
//   The pieces already exist. VaultNode.buildTree(at:) already walks
//   the vault into an ORDERED tree (VaultNode.sortKey encodes reading
//   order: Front-of-Book → Part I…VI → Appendices → figures). The
//   auto-TOC is a SwiftUI view that renders that existing rootNode
//   tree as a navigable contents list — no static HTML required.
//
// THE 4 DEPENDENCIES IN VaultModel.swift TO REPLACE:
//   1. resolveVaultRoot() — validates the extracted vault by checking
//      for "Front-of-Book/table-of-contents.html".
//      → validate on a stable marker instead (a Part-I-* folder,
//        claudex26-index.html, or simply a non-nil rootNode).
//   2. setVaultRoot() — sets the default open document to the manual
//      TOC html. → default to the generated TOC view.
//   3. goHome() — opens the manual TOC html. → route Home to the
//      generated TOC view.
//   4. VaultNode.sortKey — special-cases "table-of-contents.html" to
//      sort position 1. → drop that case once the file is retired.
//
// SEQUENCING / SAFETY:
//   • Build + verify the auto-TOC FIRST. Only AFTER it works may the
//     manual table-of-contents.html be retired from the vault. Do NOT
//     delete the file before the replacement is proven — it is still
//     the live Home/landing document today.
//   • When auto-gen ships, update memory feedback_epub_excludes_manual_toc
//     (its "keep the file on disk for the in-app reader" clause is
//     superseded once the app no longer needs the file).
//
// STATUS: NOT STARTED — captured so it isn't forgotten, explicitly
// deferred. Not to be coded as a tangent. — 2026-05-31
//
// ============================================================
// EPUB IS THE PRODUCT — BUILD-TIME TRANSFORMS THE READER MUST
// ADAPT TO (Michael, 2026-06-04)
// ============================================================
//
// DECISION: The EPUB is most likely the product for sale (Apple
// Books / Kindle / other EPUB venues). Therefore:
//
//   • The inkwell vault HTML stays the UNTOUCHED source of truth.
//     Claude does not edit it. All enrichment and correction is
//     applied at EPUB BUILD time (Workshop/Tools/build-epub.sh
//     plus the proofing Corrections-Buffer).
//   • THIS reader app must adapt in the future so the in-app
//     reading experience matches the shipping EPUB and does not
//     diverge from the product.
//   • This section is the running spec of what the reader has to
//     catch up to. It is recorded HERE (a reader-app file, OUTSIDE
//     BibleContent.bundle) on purpose — so the source of truth is
//     never modified just to capture these notes.
//
// THE MODEL:
//   source (pristine content) -> build (applies transforms) ->
//   EPUB (the product). The reader must mirror the build's
//   transforms — or eventually render the built output — so that
//   reader == product.
//
// ------------------------------------------------------------
// THE OPEN TENSION (surfaced, not resolved):
//   This reader renders the SOURCE directly. If corrections and
//   enrichments live ONLY in the build, the in-app reader shows
//   UN-enriched, UN-corrected text until it adapts. Two ways to
//   reconcile — Michael to choose:
//     (A) the reader runs the same transform/buffer pipeline
//         before rendering, or
//     (B) the reader switches to rendering the built EPUB output.
//   Until then, expect reader-vs-EPUB divergence on the items below.
// ------------------------------------------------------------
//
// TRANSFORMS / CHANGES  (each: what · where it lives · reader impact)
//
//   1. CROSS-LINK SURVIVAL  (~1537 links)
//      What: pandoc renames every file to ch###.xhtml at package
//      time but does NOT rewrite the hrefs, so every internal link
//      dies in the EPUB (renders link-styled but inert — colored,
//      underlined, does nothing when tapped).
//      Where: the BUILD must rewrite internal link targets to the
//      renamed files (or stop renaming). NEVER fix this in source —
//      source links are human-readable and already work in this
//      reader's decidePolicyFor intercept.
//      Reader impact: nav already works on vault filenames; no
//      change needed, but the reader is the REFERENCE for "links
//      work" — the build output must match it. Generalizes the
//      manual-TOC note in the section above.
//
//   2. GLOSSARY — real, shipping Back-of-Book section
//      What: today the vault has NO glossary; a good 24-term
//      glossary.xhtml is stranded in an abandoned project folder
//      (~/Developer.complex/Claudes-Xcode-26-Swift-Bible/OEBPS/) and
//      never ships. Decision: a concepts Glossary (brief, explicit
//      definitions) is a real Back-of-Book section, INDEPENDENT of
//      the Part-II Swift Lexicon (the deep keyword reference). A
//      Swift word may carry a one-line glossary brief AND a full
//      Lexicon entry; a pure concept (e.g. "Source of Truth") lives
//      ONLY in the glossary. Term #25 added: "Source of Truth"
//      (full approved text in Classroom/Proof-Copy/Corrections-
//      Buffer.md, entry A2).
//      Where: the BUILD includes the glossary file (builds last,
//      with the Appendices).
//      Reader impact: render the glossary and surface it in the
//      sidebar tree / auto-generated TOC.
//
//   3. GLOSSARY NAVIGATION BEHAVIOR  (proven in Apple Books 2026-06-04)
//      What: tap a glossary-linked term in the prose -> jump to its
//      definition -> a Back control returns to the reading spot.
//      Requires (a) glossary links wired INTO the prose, and
//      (b) each glossary term starts its own page (page-break-before
//      every term) so an anchor jump lands with the wanted term at
//      the TOP of the page instead of trailing onto the next page.
//      Without (b) the jump lands on the PREVIOUS term — verified
//      failure, then verified fixed, 2026-06-04.
//      Where: link-wiring + page-break CSS at BUILD.
//      Reader impact: support the same tap->define->back flow and
//      the per-term page-break landing.
//
//   4. OUTLINE NUMBERING — the one current source impurity
//      What: paragraphs / sections are outline-numbered (I.1.2.1 …).
//      Status: currently numbered IN PLACE in the inkwell
//      (number-book.py, verified; pristine backup at
//      ~/Developer.complex/inkwell/BibleContent.bundle.backup-2026-06-01-pre-numbering).
//      Under the pristine-source model this SHOULD become a build
//      step and the in-place numbering reverted from the backup.
//      DECISION PENDING (Michael) — do NOT auto-revert.
//      Reader impact: reader must display numbers (apply the same
//      numbering step) so reader == product.
//
//   5. EPUB-ONLY TYPOGRAPHY / CSS
//      • page-break-before on glossary terms (see #3).
//      • non-breaking space welding a quoted symbol to its word
//        (e.g. protocol 'Y') so a page break can't orphan it inside
//        a table cell (Corrections-Buffer L1).
//      • break-inside: avoid on table rows (secondary).
//      Where: BUILD / EPUB stylesheet.
//      Reader impact: match in the reader's stylesheet for parity.
//
//   6. PROSE CORRECTIONS  (the Corrections-Buffer)
//      What: typo / wording / content fixes held in
//      Classroom/Proof-Copy/Corrections-Buffer.md (e.g. the CEET
//      typo, dropping "Michael's 18pt" attribution, the widget-
//      scheme watch-out bullet).
//      Where: applied at the V1.x COMPILE from the buffer; source
//      untouched.
//      Reader impact: see THE OPEN TENSION above — the reader shows
//      uncorrected text until it applies the buffer or reads the
//      built output.
//
//   7. MANUAL TABLE OF CONTENTS — see the captured-task section
//      above. Same root cause (pandoc rename kills its links);
//      already excluded from the build; reader to auto-generate.
//
// SYNC NOTE: per the UNDER THE HOOD section, Developer Notes are
// mirrored in this .swift file, the wiki Developer-Notes.md, and the
// in-app Under-the-Hood view. Propagate this section to those when
// they are next updated.
//
// ------------------------------------------------------------
// DEFERRAL (Michael, 2026-06-04): DO NOT TOUCH THE INKWELL.
// Everything in this section is recorded so it isn't forgotten and
// explicitly PARKED — we cross each bridge when it comes, not now.
// Nothing here is a pending action. In particular:
//   • Do NOT revert the in-place outline numbering (#4).
//   • Do NOT resolve the reader-vs-EPUB tension yet (A vs B above).
//   • Do NOT modify BibleContent.bundle to apply any of this.
// These are design concerns captured for the future, not a to-do
// list. Revisit only when Michael says the bridge has arrived.
// ------------------------------------------------------------
//
// ============================================================
