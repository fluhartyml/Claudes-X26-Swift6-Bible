//
//  ContentView.swift
//  Claudes X26 Swift6 Bible
//
//  Root view — NavigationSplitView with file-tree sidebar
//  (vault structure) and the WKWebView-backed reading pane.
//

import SwiftUI
import UniformTypeIdentifiers

struct ContentView: View {
    @EnvironmentObject var vault: VaultModel
    @State private var showingUnderTheHood = false
    @State private var showingAbout = false
    #if !os(macOS)
    @State private var showingFolderImporter = false
    #endif

    var body: some View {
        NavigationSplitView {
            sidebar
                .navigationTitle("Bible")
        } detail: {
            detail
        }
        .sheet(isPresented: $showingUnderTheHood) {
            UnderTheHoodView()
        }
        .sheet(isPresented: $showingAbout) {
            AboutView()
        }
        .onReceive(NotificationCenter.default.publisher(for: .showAbout)) { _ in
            showingAbout = true
        }
        #if !os(macOS)
        .fileImporter(
            isPresented: $showingFolderImporter,
            allowedContentTypes: [.folder]
        ) { result in
            if case .success(let url) = result {
                vault.handlePickedFolder(url)
            }
        }
        #endif
    }

    // MARK: - Sidebar

    @ViewBuilder
    private var sidebar: some View {
        if let root = vault.rootNode {
            List(selection: $vault.selectedNodeID) {
                VaultTreeOutline(node: root, isRoot: true)
            }
            .listStyle(.sidebar)
            .onChange(of: vault.selectedNodeID) { _, newID in
                if let id = newID, let node = findNode(id: id, in: root), !node.isDirectory {
                    vault.open(node.url)
                }
            }
        } else {
            vaultPicker
        }
    }

    private var vaultPicker: some View {
        VStack(spacing: 14) {
            Spacer()
            Image(systemName: "books.vertical")
                .font(.system(size: 36))
                .foregroundStyle(.secondary)
            Text("Choose a vault")
                .font(.headline)
                .multilineTextAlignment(.center)
                .lineLimit(2)
            Button {
                #if os(macOS)
                vault.chooseVaultRoot()
                #else
                showingFolderImporter = true
                #endif
            } label: {
                Text("Choose…")
                    .frame(maxWidth: .infinity)
            }
            .buttonStyle(.borderedProminent)
            Spacer()
        }
        .padding()
        .frame(maxWidth: .infinity)
    }

    private func findNode(id: VaultNode.ID, in node: VaultNode) -> VaultNode? {
        if node.id == id { return node }
        for child in node.children {
            if let hit = findNode(id: id, in: child) { return hit }
        }
        return nil
    }

    // MARK: - Detail

    @ViewBuilder
    private var detail: some View {
        if vault.vaultRoot != nil, let doc = vault.currentDocument {
            VStack(spacing: 0) {
                toolbar
                Divider()
                VaultWebView(
                    documentURL: doc,
                    vaultRoot: vault.vaultRoot,
                    onInternalNavigate: { url in vault.open(url) }
                )
            }
        } else if vault.vaultRoot == nil {
            emptyVault
        } else {
            emptyDocument
        }
    }

    private var toolbar: some View {
        HStack(spacing: 8) {
            Button(action: vault.goBack) {
                Image(systemName: "chevron.left")
            }
            .disabled(!vault.canGoBack)

            Button(action: vault.goForward) {
                Image(systemName: "chevron.right")
            }
            .disabled(!vault.canGoForward)

            Button(action: vault.goHome) {
                Image(systemName: "house")
            }

            if let doc = vault.currentDocument {
                Spacer(minLength: 8)
                Text(vault.displayPath(for: doc))
                    .font(.caption.monospaced())
                    .foregroundStyle(.secondary)
                    .lineLimit(1)
                    .truncationMode(.middle)
                    .layoutPriority(1)
                    .frame(maxWidth: .infinity)
                Spacer(minLength: 8)
            } else {
                Spacer()
            }

            Button {
                showingUnderTheHood = true
            } label: {
                Label("Under the Hood", systemImage: "gearshape.2")
            }
            .labelStyle(.iconOnly)
            .help("Under the Hood — Developer Notes")

            Button {
                showingAbout = true
            } label: {
                Label("About", systemImage: "info.circle")
            }
            .labelStyle(.iconOnly)
            .help("About")
        }
        .padding(.horizontal, 12)
        .padding(.vertical, 8)
        .background(.ultraThinMaterial)
    }

    private var emptyVault: some View {
        VStack(spacing: 10) {
            Text("No vault open")
                .font(.title3)
            Text("Use the sidebar to choose one.")
                .foregroundStyle(.secondary)
                .multilineTextAlignment(.center)
        }
        .padding()
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }

    private var emptyDocument: some View {
        Text("Pick a Book from the sidebar to start reading.")
            .foregroundStyle(.secondary)
            .multilineTextAlignment(.center)
            .padding()
            .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}

// MARK: - Recursive outline row

struct VaultTreeOutline: View {
    let node: VaultNode
    var isRoot: Bool = false

    var body: some View {
        if node.isDirectory {
            if isRoot {
                // Don't show the root folder itself — just its children.
                ForEach(node.children) { child in
                    VaultTreeOutline(node: child)
                }
            } else {
                DisclosureGroup {
                    ForEach(node.children) { child in
                        VaultTreeOutline(node: child)
                    }
                } label: {
                    labelFor(node)
                }
            }
        } else {
            labelFor(node)
                .tag(node.id)
        }
    }

    private func labelFor(_ node: VaultNode) -> some View {
        Label(displayName(node), systemImage: node.symbolName)
            .lineLimit(1)
            .truncationMode(.middle)
            .help(node.name)
    }

    /// Shorter display name for folders whose raw name is unwieldy in the sidebar.
    /// Target: ≤20 characters per `feedback_short_titles_20_chars` memory.
    private func displayName(_ node: VaultNode) -> String {
        let name = node.name
        if let short = Self.shortNames[name] { return short }
        if name.hasPrefix("Chapter-") {
            return name.replacingOccurrences(of: "-", with: " ")  // "Chapter A"
        }
        return name
    }

    /// Manual short-title map. Every entry here is ≤20 chars.
    private static let shortNames: [String: String] = [
        // Parts
        "Part-I-The-Swift-Language":    "I · Swift Language",
        "Part-II-Introduction":         "II · Intro",
        "Part-III-The-User-Interface":  "III · Interface",
        "Part-IV-The-Application":      "IV · App",
        "Part-V-Advanced-Techniques":   "V · Advanced",
        "Part-VI-The-Modern-Toolchain": "VI · Toolchain",
        // Books (Parts II–VI)
        "Book-01-Introducing-Swift-And-Xcode":               "01 · Swift & Xcode",
        "Book-02-Introducing-SwiftUI-Views":                 "02 · SwiftUI Views",
        "Book-03-Introducing-Scenes-And-Windows":            "03 · Scenes & Windows",
        "Book-04-Gestures-And-Input":                        "04 · Gestures",
        "Book-05-Menus-And-Navigation":                      "05 · Menus",
        "Book-06-Controls-Buttons-Toggles-Pickers":          "06 · Controls",
        "Book-07-Toolbars-And-Tab-Views":                    "07 · Toolbars",
        "Book-08-Lists-Grids-And-ForEach":                   "08 · Lists & Grids",
        "Book-09-Text-And-TextField":                        "09 · Text",
        "Book-10-TextEditor-And-AttributedString":           "10 · TextEditor",
        "Book-11-FileManager-And-Documents":                 "11 · Files",
        "Book-12-Sheets-Alerts-And-Confirmations":           "12 · Sheets",
        "Book-13-Multi-Window-And-NavigationSplitView":      "13 · Windows",
        "Book-14-Clipboard-DragDrop-ShareSheet":             "14 · Clipboard",
        "Book-15-SwiftData-And-CoreData":                    "15 · SwiftData",
        "Book-16-Extensions-And-Packages":                   "16 · Extensions",
        "Book-17-Swift-Charts-And-PDFKit":                   "17 · Charts & PDF",
        "Book-18-Error-Handling-And-Result-Type":            "18 · Errors",
        "Book-19-Building-Custom-Views-And-Modifiers":       "19 · Custom Views",
        "Book-20-Performance-Instruments-And-Best-Practices":"20 · Performance",
        "Book-21-Git-And-GitHub":                            "21 · Git & GitHub",
        "Book-22-AI-Chatbot-Integration":                    "22 · AI Chatbots",
        // Appendices
        "Appendix-A-GitHub-Setup":       "A · GitHub Setup",
        "Appendix-B-Claudes-Web-Wrapper":"B · Web Wrapper",
        "Appendix-C-QuickNote":          "C · QuickNote",
        "Appendix-D-LockBox":            "D · LockBox",
    ]
}
