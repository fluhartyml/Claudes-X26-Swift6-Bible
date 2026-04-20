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

            Spacer()

            if let doc = vault.currentDocument {
                Text(vault.displayPath(for: doc))
                    .font(.caption.monospaced())
                    .foregroundStyle(.secondary)
                    .lineLimit(1)
                    .truncationMode(.middle)
            }

            Spacer()

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
                    Label(node.name, systemImage: node.symbolName)
                }
            }
        } else {
            Label(node.name, systemImage: node.symbolName)
                .tag(node.id)
        }
    }
}
