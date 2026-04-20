//
//  VaultModel.swift
//  Claudes X26 Swift6 Bible
//
//  State model for the Bible vault — holds the vault root URL,
//  the file tree, the currently-open document, and navigation history.
//

import Foundation
import SwiftUI
import Combine
#if os(macOS)
import AppKit
#else
import UIKit
#endif

@MainActor
final class VaultModel: ObservableObject {

    // MARK: - Published state

    @Published var vaultRoot: URL?
    @Published var rootNode: VaultNode?
    @Published var currentDocument: URL?
    @Published var selectedNodeID: VaultNode.ID?

    private var history: [URL] = []
    private var forwardHistory: [URL] = []

    // MARK: - Defaults keys

    private let bookmarkKey = "vaultRootBookmark"
    private let lastPathKey = "lastDocumentPath"

    // MARK: - Init

    init() {
        resolveVaultRoot()
    }

    // MARK: - Vault-root resolution

    /// Try to locate a vault root on launch. Priority:
    ///  1. Security-scoped bookmark (user-picked vault).
    ///  2. Extracted vault in Application Support (works on both iOS + macOS).
    ///  3. Bundled BibleContent.bundle (macOS filesystem-sync preserves it).
    ///  4. nil — user must pick.
    private func resolveVaultRoot() {
        if let url = restoreBookmarkedRoot() {
            setVaultRoot(url)
            return
        }
        if let extracted = VaultBundleExtractor.ensureExtracted(),
           FileManager.default.fileExists(atPath: extracted.appending(path: "table-of-contents.html").path) {
            setVaultRoot(extracted)
            return
        }
        if let bundled = Bundle.main.url(forResource: "BibleContent", withExtension: "bundle") {
            setVaultRoot(bundled)
            return
        }
    }

    private func restoreBookmarkedRoot() -> URL? {
        guard let data = UserDefaults.standard.data(forKey: bookmarkKey) else { return nil }
        var stale = false
        #if os(macOS)
        let options: URL.BookmarkResolutionOptions = [.withSecurityScope]
        #else
        let options: URL.BookmarkResolutionOptions = []
        #endif
        guard let url = try? URL(
            resolvingBookmarkData: data,
            options: options,
            relativeTo: nil,
            bookmarkDataIsStale: &stale
        ) else { return nil }
        _ = url.startAccessingSecurityScopedResource()
        return url
    }

    func setVaultRoot(_ url: URL) {
        vaultRoot = url
        rootNode = VaultNode.buildTree(at: url)
        // Priority: last document the reader viewed > table of contents > atlas.
        if let lastRel = UserDefaults.standard.string(forKey: lastPathKey) {
            let lastURL = url.appending(path: lastRel)
            if FileManager.default.fileExists(atPath: lastURL.path) {
                currentDocument = lastURL
                return
            }
        }
        let tocURL = url.appending(path: "table-of-contents.html")
        if FileManager.default.fileExists(atPath: tocURL.path) {
            currentDocument = tocURL
        } else {
            let atlasURL = url.appending(path: "bible-atlas.html")
            if FileManager.default.fileExists(atPath: atlasURL.path) {
                currentDocument = atlasURL
            }
        }
    }

    private func saveLastDocument(_ url: URL) {
        guard let root = vaultRoot else { return }
        let rootPath = root.path
        let docPath = url.path
        guard docPath.hasPrefix(rootPath) else { return }
        var rel = String(docPath.dropFirst(rootPath.count))
        if rel.hasPrefix("/") { rel = String(rel.dropFirst()) }
        UserDefaults.standard.set(rel, forKey: lastPathKey)
    }

    /// Save a security-scoped bookmark to the chosen URL so next launch restores it.
    private func saveBookmark(for url: URL) {
        #if os(macOS)
        let options: URL.BookmarkCreationOptions = [.withSecurityScope]
        #else
        let options: URL.BookmarkCreationOptions = []
        #endif
        if let data = try? url.bookmarkData(
            options: options,
            includingResourceValuesForKeys: nil,
            relativeTo: nil
        ) {
            UserDefaults.standard.set(data, forKey: bookmarkKey)
        }
    }

    // MARK: - Picker

    func chooseVaultRoot() {
        #if os(macOS)
        let panel = NSOpenPanel()
        panel.canChooseFiles = false
        panel.canChooseDirectories = true
        panel.allowsMultipleSelection = false
        panel.message = "Choose the Bible vault folder."
        panel.prompt = "Open"
        if panel.runModal() == .OK, let url = panel.url {
            _ = url.startAccessingSecurityScopedResource()
            saveBookmark(for: url)
            setVaultRoot(url)
        }
        #endif
        // iOS/iPadOS picker is surfaced from ContentView via .fileImporter modifier.
    }

    func handlePickedFolder(_ url: URL) {
        _ = url.startAccessingSecurityScopedResource()
        saveBookmark(for: url)
        setVaultRoot(url)
    }

    // MARK: - Navigation

    func open(_ relativePath: String) {
        guard let root = vaultRoot else { return }
        let url = root.appending(path: relativePath)
        open(url)
    }

    func open(_ url: URL) {
        if let cur = currentDocument {
            history.append(cur)
        }
        forwardHistory.removeAll()
        currentDocument = url
        saveLastDocument(url)
    }

    func goBack() {
        guard let prev = history.popLast() else { return }
        if let cur = currentDocument {
            forwardHistory.append(cur)
        }
        currentDocument = prev
    }

    func goForward() {
        guard let next = forwardHistory.popLast() else { return }
        if let cur = currentDocument {
            history.append(cur)
        }
        currentDocument = next
    }

    var canGoBack: Bool { !history.isEmpty }
    var canGoForward: Bool { !forwardHistory.isEmpty }

    func goHome() {
        open("table-of-contents.html")
    }

    // MARK: - Display

    func displayPath(for url: URL) -> String {
        guard let root = vaultRoot else { return url.lastPathComponent }
        let rootPath = root.path
        let fullPath = url.path
        if fullPath.hasPrefix(rootPath) {
            let rel = String(fullPath.dropFirst(rootPath.count))
            return rel.hasPrefix("/") ? String(rel.dropFirst()) : rel
        }
        return url.lastPathComponent
    }
}

// MARK: - Vault file tree

struct VaultNode: Identifiable, Hashable {
    let id: URL
    let url: URL
    let name: String
    let isDirectory: Bool
    var children: [VaultNode]

    /// Extension icon suggestion (SF Symbol name).
    var symbolName: String {
        if isDirectory { return "folder" }
        switch url.pathExtension.lowercased() {
        case "html", "htm": return "doc.richtext"
        case "md":          return "doc.text"
        case "png", "jpg", "jpeg", "gif", "svg": return "photo"
        case "epub":        return "book.closed"
        case "swift":       return "swift"
        case "pdf":         return "doc"
        default:            return "doc"
        }
    }

    static func buildTree(at url: URL) -> VaultNode? {
        let fm = FileManager.default
        var isDir: ObjCBool = false
        guard fm.fileExists(atPath: url.path, isDirectory: &isDir) else { return nil }

        if !isDir.boolValue {
            return VaultNode(id: url, url: url, name: url.lastPathComponent, isDirectory: false, children: [])
        }

        let children: [VaultNode]
        do {
            let entries = try fm.contentsOfDirectory(
                at: url,
                includingPropertiesForKeys: [.isDirectoryKey],
                options: [.skipsHiddenFiles]
            )
            .filter { !$0.lastPathComponent.hasPrefix("_build-") }
            .sorted { lhs, rhs in
                // Directories first, then alphabetical.
                let lIsDir = (try? lhs.resourceValues(forKeys: [.isDirectoryKey]).isDirectory) ?? false
                let rIsDir = (try? rhs.resourceValues(forKeys: [.isDirectoryKey]).isDirectory) ?? false
                if lIsDir != rIsDir { return lIsDir }
                return lhs.lastPathComponent.localizedStandardCompare(rhs.lastPathComponent) == .orderedAscending
            }
            children = entries.compactMap { buildTree(at: $0) }
        } catch {
            children = []
        }
        return VaultNode(id: url, url: url, name: url.lastPathComponent, isDirectory: true, children: children)
    }
}
