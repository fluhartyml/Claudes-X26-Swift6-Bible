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

struct ContentView: View {
    @EnvironmentObject var vault: VaultModel
    @State private var showingUnderTheHood = false
    @State private var showingAbout = false
    @AppStorage("textScale") private var textScale: Double = 1.0
    #if !os(macOS)
    @State private var showingFolderImporter = false
    #endif

    private let minScale: Double = 0.7
    private let maxScale: Double = 2.2
    private let scaleStep: Double = 0.15

    var body: some View {
        NavigationSplitView {
            sidebar
                .navigationTitle("Library")
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
            VStack(spacing: 0) {
                debugBar
                List(selection: $vault.selectedNodeID) {
                    VaultTreeOutline(node: root, isRoot: true)
                }
                .listStyle(.sidebar)
                .onChange(of: vault.selectedNodeID) { _, newID in
                    if let id = newID, let node = findNode(id: id, in: root), !node.isDirectory {
                        vault.open(node.url)
                    }
                }
            }
        } else {
            vaultPicker
        }
    }

    private var debugBar: some View {
        VStack(alignment: .leading, spacing: 2) {
            Text("DEBUG")
                .font(.caption2).bold()
                .foregroundStyle(Color.orange)
            Text("textScale: \(textScale, specifier: "%.2f")")
                .font(.caption.monospaced())
            Text("sidebar row: .body (Dynamic Type)")
                .font(.caption.monospaced())
            #if canImport(UIKit)
            Text("row pt: \(UIFont.preferredFont(forTextStyle: .body).pointSize, specifier: "%.0f")")
                .font(.caption.monospaced())
            #endif
        }
        .padding(.horizontal, 10)
        .padding(.vertical, 8)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Color.orange.opacity(0.15))
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
                } label: {
                    Label("Info", systemImage: "info.circle")
                }
                .labelStyle(.iconOnly)
                .help("About & Developer Notes")
            }

            if let doc = vault.currentDocument {
                Text(vault.displayPath(for: doc))
                    .font(.caption.monospaced())
                    .foregroundStyle(.secondary)
                    .lineLimit(1)
                    .truncationMode(.middle)
                    .frame(maxWidth: .infinity, alignment: .leading)
            }
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
        Text(displayName(node))
            .lineLimit(nil)
            .fixedSize(horizontal: false, vertical: true)
            .help(node.name)
    }

    /// Readable display name for sidebar rows — spaces instead of dashes,
    /// full wording, wraps to 2+ lines as needed. No abbreviations.
    private func displayName(_ node: VaultNode) -> String {
        node.name.replacingOccurrences(of: "-", with: " ")
    }

}
