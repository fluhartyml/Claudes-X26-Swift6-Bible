//
//  ContentView.swift
//  Claudes X26 Swift6 Bible
//
//  Root view — NavigationSplitView with file-tree sidebar
//  (vault structure) and the WKWebView-backed reading pane.
//

import SwiftUI
import UniformTypeIdentifiers
#if canImport(UIKit)
import UIKit
#endif

extension Color {
    static let libraryBg     = Color(red: 0x00/255, green: 0x07/255, blue: 0x1A/255)
    static let libraryFg     = Color(red: 0x60/255, green: 0x8F/255, blue: 0xFF/255)
    static let libraryBright = Color(red: 0x80/255, green: 0xB8/255, blue: 0xFF/255)
    static let libraryDim    = Color(red: 0x00/255, green: 0x33/255, blue: 0x99/255)
    static let libraryBorder = Color(red: 0x00/255, green: 0x22/255, blue: 0x66/255)
}

struct ContentView: View {
    @EnvironmentObject var vault: VaultModel
    @EnvironmentObject var webViewBridge: VaultWebView.Bridge
    @State private var showingUnderTheHood = false
    @State private var showingAbout = false
    @State private var wholeBookShareURL: URL?
    @State private var preparingWholeBookShare = false
    @State private var columnVisibility: NavigationSplitViewVisibility = .automatic
    @AppStorage("textScale") private var textScale: Double = 1.0
    #if !os(macOS)
    @State private var showingFolderImporter = false
    #endif

    private let minScale: Double = 0.7
    private let maxScale: Double = 2.2
    private let scaleStep: Double = 0.15

    var body: some View {
        NavigationSplitView(columnVisibility: $columnVisibility) {
            sidebar
                .navigationTitle("Library")
                #if os(iOS)
                .navigationBarTitleDisplayMode(.inline)
                .toolbar {
                    ToolbarItem(placement: .topBarTrailing) {
                        Button {
                            withAnimation {
                                columnVisibility = (columnVisibility == .detailOnly)
                                    ? .automatic
                                    : .detailOnly
                            }
                        } label: {
                            Image(systemName: "sidebar.leading")
                        }
                        .accessibilityLabel("Toggle Sidebar")
                    }
                }
                #endif
        } detail: {
            detail
        }
        .sheet(isPresented: $showingUnderTheHood) {
            UnderTheHoodView()
        }
        .sheet(isPresented: $showingAbout) {
            AboutView()
        }
        .sheet(item: Binding(
            get: { wholeBookShareURL.map(WholeBookShareItem.init) },
            set: { wholeBookShareURL = $0?.url }
        )) { item in
            WholeBookShareSheet(url: item.url) { wholeBookShareURL = nil }
        }
        .onReceive(NotificationCenter.default.publisher(for: .showAbout)) { _ in
            showingAbout = true
        }
        #if os(iOS)
        // On iPhone, collapse the sidebar when the reader opens a page
        // so the amber reading pane takes over — swipe or the sidebar
        // toolbar icon can bring it back.
        .onChange(of: vault.currentDocument) { _, newDoc in
            guard newDoc != nil else { return }
            if UIDevice.current.userInterfaceIdiom == .phone {
                columnVisibility = .detailOnly
            }
        }
        #endif
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
            .scrollContentBackground(.hidden)
            .background(Color.libraryBg)
            .tint(Color.libraryBright)
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

    // MARK: - Share whole book

    /// Zip the entire vault folder and present the system share sheet.
    /// NSFileCoordinator's .forUploading read option produces a standard
    /// .zip archive of a directory; works on iOS and macOS.
    private func shareWholeBook() {
        guard let root = vault.vaultRoot, !preparingWholeBookShare else { return }
        preparingWholeBookShare = true
        DispatchQueue.global(qos: .userInitiated).async {
            let coordinator = NSFileCoordinator()
            var nsError: NSError?
            var producedURL: URL?
            coordinator.coordinate(
                readingItemAt: root,
                options: [.forUploading],
                error: &nsError
            ) { zipURL in
                let fm = FileManager.default
                let tmp = fm.temporaryDirectory
                    .appending(path: "Claudes-X26-Swift6-Bible-\(Int(Date().timeIntervalSince1970)).zip")
                try? fm.removeItem(at: tmp)
                try? fm.copyItem(at: zipURL, to: tmp)
                producedURL = tmp
            }
            DispatchQueue.main.async {
                preparingWholeBookShare = false
                wholeBookShareURL = producedURL
            }
        }
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
                    textScale: textScale,
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
        VStack(spacing: 4) {
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

                Spacer()

                Button {
                    webViewBridge.highlightSelection()
                } label: {
                    Label("Highlight", systemImage: "highlighter")
                }
                .labelStyle(.iconOnly)
                .help("Highlight selection")

                if let doc = vault.currentDocument {
                    ShareLink(item: doc) {
                        Label("Share", systemImage: "square.and.arrow.up")
                    }
                    .labelStyle(.iconOnly)
                    .help("Share this page")
                }

                Button {
                    textScale = max(minScale, textScale - scaleStep)
                } label: {
                    Label("Smaller text", systemImage: "textformat.size.smaller")
                }
                .labelStyle(.iconOnly)
                .help("Smaller text")
                .disabled(textScale <= minScale + 0.001)

                Button {
                    textScale = min(maxScale, textScale + scaleStep)
                } label: {
                    Label("Larger text", systemImage: "textformat.size.larger")
                }
                .labelStyle(.iconOnly)
                .help("Larger text")
                .disabled(textScale >= maxScale - 0.001)

                Menu {
                    Button("About") { showingAbout = true }
                    Button("Under the Hood") { showingUnderTheHood = true }
                    Divider()
                    Button(preparingWholeBookShare
                           ? "Preparing Whole Book…"
                           : "Share Whole Book") {
                        shareWholeBook()
                    }
                    .disabled(preparingWholeBookShare || vault.vaultRoot == nil)
                } label: {
                    Label("Info", systemImage: "info.circle")
                }
                .labelStyle(.iconOnly)
                .help("About, Developer Notes, Share Whole Book")
            }

            // Toolbar used to show the vault-relative path here, but it
            // duplicated the HTML header rendered inside every page. The
            // HTML header + footer are the rule-locked source of truth for
            // identifying a page in a screenshot; the toolbar keeps its
            // nav chrome only.
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

// MARK: - Share whole book helpers

/// Identifiable wrapper so `.sheet(item:)` fires when the URL changes.
private struct WholeBookShareItem: Identifiable {
    let url: URL
    var id: URL { url }
}

#if os(iOS)
private struct WholeBookShareSheet: UIViewControllerRepresentable {
    let url: URL
    let onDismiss: () -> Void
    func makeUIViewController(context: Context) -> UIActivityViewController {
        let vc = UIActivityViewController(activityItems: [url], applicationActivities: nil)
        vc.completionWithItemsHandler = { _, _, _, _ in onDismiss() }
        return vc
    }
    func updateUIViewController(_ vc: UIActivityViewController, context: Context) {}
}
#else
private struct WholeBookShareSheet: View {
    let url: URL
    let onDismiss: () -> Void
    var body: some View {
        VStack(spacing: 14) {
            Text("Share Whole Book")
                .font(.headline)
            ShareLink(item: url) {
                Label("Share .zip", systemImage: "square.and.arrow.up")
            }
            Button("Done") { onDismiss() }
        }
        .padding(24)
        .frame(minWidth: 320)
    }
}
#endif

// MARK: - Recursive outline row

struct VaultTreeOutline: View {
    @EnvironmentObject var vault: VaultModel
    let node: VaultNode
    var isRoot: Bool = false

    var body: some View {
        if node.isDirectory {
            if isRoot {
                ForEach(node.children) { child in
                    VaultTreeOutline(node: child)
                }
            } else {
                DisclosureGroup(
                    isExpanded: bindingForExpansion(of: node)
                ) {
                    ForEach(node.children) { child in
                        VaultTreeOutline(node: child)
                    }
                } label: {
                    labelFor(node)
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .contentShape(Rectangle())
                        .onTapGesture {
                            vault.logTap("Folder: \(node.name)")
                            vault.toggleExpanded(node.id)
                        }
                }
            }
        } else {
            labelFor(node)
                .frame(maxWidth: .infinity, alignment: .leading)
                .contentShape(Rectangle())
                .tag(node.id)
                .onTapGesture {
                    vault.logTap("File: \(node.name)")
                    vault.open(node.url)
                }
        }
    }

    private func bindingForExpansion(of node: VaultNode) -> Binding<Bool> {
        Binding<Bool>(
            get: { vault.expandedNodeIDs.contains(node.id) },
            set: { newValue in
                if newValue { vault.expandedNodeIDs.insert(node.id) }
                else        { vault.expandedNodeIDs.remove(node.id) }
            }
        )
    }

    private func labelFor(_ node: VaultNode) -> some View {
        Text(displayName(node))
            .lineLimit(nil)
            .fixedSize(horizontal: false, vertical: true)
            .foregroundStyle(node.isDirectory ? Color.libraryBright : Color.libraryFg)
            .help(node.name)
    }

    /// Readable display name for sidebar rows — spaces instead of dashes,
    /// full wording, wraps to 2+ lines as needed. File extensions hidden.
    private func displayName(_ node: VaultNode) -> String {
        let base = node.isDirectory
            ? node.name
            : (node.name as NSString).deletingPathExtension
        return base.replacingOccurrences(of: "-", with: " ")
    }
}
