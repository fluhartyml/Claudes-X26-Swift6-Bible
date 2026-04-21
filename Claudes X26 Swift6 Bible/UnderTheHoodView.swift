//
//  UnderTheHoodView.swift
//  Claudes X26 Swift6 Bible
//
//  Reader-visible Developer Notes. Companion-app teaching pattern —
//  every build-along app exposes the same content that lives in the
//  project's DeveloperNotes.swift and the wiki's Developer-Notes.md.
//  Three surfaces, one source of truth.
//

import SwiftUI

struct UnderTheHoodView: View {
    @Environment(\.dismiss) private var dismiss
    @EnvironmentObject var vault: VaultModel

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 16) {
                    header
                    bookRoadmapLink
                    section(title: "Mission", body: missionText)
                    section(title: "Relationship to Other Projects", body: relationshipText)
                    section(title: "Architecture Decisions", body: architectureText)
                    section(title: "Roadmap — v1.0 MVP", body: roadmapText)
                    section(title: "Attribution", body: attributionText)
                }
                .padding()
                .frame(maxWidth: 800, alignment: .leading)
                .frame(maxWidth: .infinity, alignment: .leading)
            }
            .navigationTitle("Under the Hood")
            #if os(iOS)
            .navigationBarTitleDisplayMode(.inline)
            #endif
            .toolbar {
                ToolbarItem(placement: .primaryAction) {
                    Button("Done") { dismiss() }
                }
            }
        }
    }

    private var header: some View {
        VStack(alignment: .leading, spacing: 6) {
            Text("Claude's X26 Swift6 Bible")
                .font(.title.weight(.semibold))
            Text("Version 1.0 (pre-release) · GPL v3")
                .font(.caption)
                .foregroundStyle(.secondary)
            Text("Engineered with Claude by Anthropic. Developed by Michael Lee Fluharty.")
                .font(.footnote)
                .foregroundStyle(.secondary)
        }
    }

    private var bookRoadmapLink: some View {
        Button {
            dismiss()
            vault.open("claudex26-roadmap.html")
        } label: {
            Label("Open Book Roadmap", systemImage: "map")
                .frame(maxWidth: .infinity)
        }
        .buttonStyle(.borderedProminent)
    }

    @ViewBuilder
    private func section(title: String, body: String) -> some View {
        VStack(alignment: .leading, spacing: 6) {
            Text(title)
                .font(.headline)
            Text(body)
                .font(.body)
                .fixedSize(horizontal: false, vertical: true)
        }
        .padding(.top, 8)
    }

    // Text intentionally plain-prose — readers see it on any platform,
    // no syntax highlighting or special typography. Keep parallel with
    // Developer-Notes.md and DeveloperNotes.swift so all three stay synced.

    private let missionText =
    """
    This app is the reader for Claude's Xcode 26 Swift Reference. The reference is a vault of HTML rich-text documents with fully-functioning hyperlinks and embedded multimedia — Parts contain Books, Books contain the HTML plus per-Book figures and media. The folder tree mirrors the reading order, so the Finder tree IS the table of contents.

    The app opens the vault, shows the file tree in a sidebar, and renders the selected document inline via WKWebView. The same binary serves three roles: reader for end-users, authoring navigator for Michael during writing, and EPUB packaging cockpit (planned v1.3) for shipping to Apple Books and Amazon Kindle.
    """

    private let relationshipText =
    """
    • Reference vault content — Claudes-Xcode-26-Swift-Bible/ (working code name)
    • Reader app (this binary) — inkwell/Claudes X26 Swift6 Bible/
    • Claude's Web Wrapper — the App Store SwiftUI WKWebView app whose rendering pattern this reader builds on.
    • DiamondNotesVault (NightGard family) — scaffold concept that inspired this project's vault-browser structure.
    • InkwellJournal / InkwellBinary — sibling apps under the com.inkwell bundle namespace.
    """

    private let architectureText =
    """
    Universal SwiftUI for iOS, iPadOS, and macOS. WKWebView for HTML rendering — same pattern Claude's Web Wrapper uses and what EPUB readers use under the hood; the vault is EPUB-shaped so rendering the vault IS the same code path as rendering an EPUB.

    Vault access via NSOpenPanel on macOS and UIDocumentPicker on iOS, with a security-scoped bookmark saved in UserDefaults so the next launch restores the chosen root. Default dark mode with an amber accent to match the CRT proofing aesthetic. Window default 900×720 on macOS.

    Internal navigation: WKWebView's decidePolicyFor delegate intercepts link clicks — same-vault relative links navigate in-app through VaultModel (keeping history and sidebar in sync); external links open in Safari. SwiftData and CloudKit are present from the scaffold but unused until v2.0 annotations.
    """

    private let roadmapText =
    """
    Shipped in v1.0: file-tree sidebar, vault root picker with security-scoped bookmark, WKWebView reader pane, internal/external link routing, history (back/forward/home), address bar, Under the Hood view, 900×720 macOS window, universal icon (iOS light/dark/tinted + full macOS ladder), hero imageset.

    Planned v1.1: full-text search across the vault, jump-to-line-number, breadcrumb trail, keyboard shortcuts, bookmarks.

    Planned v1.2: proofing-flag introspection (green/yellow/orange/approved line counts per file), side-by-side edit + render proofing view.

    Planned v1.3: Build EPUB command — package the vault into a valid EPUB, embed FiraCode Nerd Font, auto-increment version.

    Planned v2.0: reader annotations backed by SwiftData + CloudKit for cross-device sync.
    """

    private let attributionText =
    """
    Structure inspired by Tom Swan's Delphi 4 Bible (IDG Books, 1998). All code and content are original work. The book-structure metaphor uses "Books" for chapters, drawing on the Bible's own scroll-era terminology.
    """
}

#Preview {
    UnderTheHoodView()
}
